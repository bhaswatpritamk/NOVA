"""Project Nova-Fit: Resumable Checkpoint Engine.

Provides robust, atomic, and verifiable checkpoint serialization and recovery for Nova-Fit models.
Preserves:
- Model weights (state_dict)
- Optimizer state (moments, step)
- Learning rate scheduler state
- Global step, epoch, and tokens processed
- Deterministic RNG states across PyTorch (CPU & CUDA), NumPy, and Python's random module
- Model and training configuration
- Tokenizer vocabulary size and artifact SHA-256 hash
- Dataset manifest SHA-256 hash
- Evaluation metrics (best and current validation loss)
- Runtime environment telemetry (Python, PyTorch, platform, device)
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import sys
import uuid
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import numpy as np
import torch
import torch.nn as nn
from torch.optim import Optimizer
from torch.optim.lr_scheduler import _LRScheduler


class CheckpointError(Exception):
    """Base exception for all checkpoint-related failures."""


class CheckpointCompatibilityError(CheckpointError):
    """Raised when a checkpoint is incompatible with the target model, tokenizer, or configuration."""


class CheckpointCorruptedError(CheckpointError):
    """Raised when a checkpoint file is incomplete, damaged, or cannot be deserialized."""


def compute_file_sha256(path: Union[str, Path]) -> str:
    """Compute the hexadecimal SHA-256 hash of a file.

    Args:
        path: Path to the target file.

    Returns:
        Hexadecimal SHA-256 digest string.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"File not found for hash calculation: {p}")

    hasher = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def get_rng_states() -> Dict[str, Any]:
    """Capture random number generator states across all active generators.

    Returns:
        Dictionary of RNG states for torch (CPU), torch (CUDA if available),
        numpy, and Python's random module.
    """
    states: Dict[str, Any] = {
        "torch_cpu": torch.get_rng_state(),
        "torch_cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None,
        "numpy": np.random.get_state(),
        "python": random.getstate(),
    }
    return states


def set_rng_states(rng_states: Dict[str, Any]) -> None:
    """Restore random number generator states from a checkpoint.

    Args:
        rng_states: Dictionary containing RNG state objects.
    """
    if not isinstance(rng_states, dict):
        return

    if "torch_cpu" in rng_states and rng_states["torch_cpu"] is not None:
        try:
            torch.set_rng_state(rng_states["torch_cpu"])
        except Exception as e:
            sys.stderr.write(f"Warning: Failed to restore torch CPU RNG state: {e}\n")

    if (
        "torch_cuda" in rng_states
        and rng_states["torch_cuda"] is not None
        and torch.cuda.is_available()
    ):
        try:
            torch.cuda.set_rng_state_all(rng_states["torch_cuda"])
        except Exception as e:
            sys.stderr.write(f"Warning: Failed to restore torch CUDA RNG state: {e}\n")

    if "numpy" in rng_states and rng_states["numpy"] is not None:
        try:
            np.random.set_state(rng_states["numpy"])
        except Exception as e:
            sys.stderr.write(f"Warning: Failed to restore NumPy RNG state: {e}\n")

    if "python" in rng_states and rng_states["python"] is not None:
        try:
            random.setstate(rng_states["python"])
        except Exception as e:
            sys.stderr.write(f"Warning: Failed to restore Python random state: {e}\n")


def _config_to_dict(config: Any) -> Dict[str, Any]:
    """Convert a configuration object (dict, dataclass, or custom class) to a dictionary."""
    if config is None:
        return {}
    if isinstance(config, dict):
        return config
    if hasattr(config, "to_dict") and callable(config.to_dict):
        return config.to_dict()
    if is_dataclass(config):
        return asdict(config)
    if hasattr(config, "__dict__"):
        return {k: v for k, v in config.__dict__.items() if not k.startswith("_")}
    return {}


def save_checkpoint(
    checkpoint_path: Union[str, Path],
    model: nn.Module,
    optimizer: Optional[Optimizer] = None,
    scheduler: Optional[Any] = None,
    step: int = 0,
    epoch: int = 0,
    tokens_processed: int = 0,
    val_loss: Optional[float] = None,
    best_val_loss: Optional[float] = None,
    model_config: Optional[Any] = None,
    training_config: Optional[Any] = None,
    tokenizer_path: Optional[Union[str, Path]] = None,
    manifest_path: Optional[Union[str, Path]] = None,
    device: Optional[Union[str, torch.device]] = None,
) -> Path:
    """Save an atomic, complete, and reproducible training checkpoint.

    Writes the state payload to a unique temporary file in the target directory,
    and then performs an atomic file replacement to avoid corrupt partial files
    if training or runtime is interrupted during writing.

    Args:
        checkpoint_path: Destination path for the checkpoint (.pt file).
        model: PyTorch model instance.
        optimizer: Optional optimizer whose state should be preserved.
        scheduler: Optional learning rate scheduler whose state should be preserved.
        step: Current global optimizer step.
        epoch: Current dataset epoch.
        tokens_processed: Cumulative number of non-padding tokens processed.
        val_loss: Most recent validation loss.
        best_val_loss: Best observed validation loss.
        model_config: Model configuration object or dictionary.
        training_config: Training configuration object or dictionary.
        tokenizer_path: Optional path to tokenizer directory or tokenizer.json.
        manifest_path: Optional path to dataset manifest.json.
        device: Device where training was executed.

    Returns:
        Path to the saved checkpoint file.
    """
    target = Path(checkpoint_path).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)

    # Resolve model config
    if model_config is None and hasattr(model, "config"):
        model_config_dict = _config_to_dict(model.config)
    else:
        model_config_dict = _config_to_dict(model_config)

    # Compute tokenizer hash and vocab size
    tokenizer_hash: Optional[str] = None
    tokenizer_vocab_size: Optional[int] = model_config_dict.get("vocab_size")

    if tokenizer_path is not None:
        tok_p = Path(tokenizer_path)
        tok_json = tok_p if tok_p.is_file() else tok_p / "tokenizer.json"
        if tok_json.is_file():
            tokenizer_hash = compute_file_sha256(tok_json)
            try:
                with open(tok_json, "r", encoding="utf-8") as f:
                    tok_data = json.load(f)
                    if "model" in tok_data and "vocab" in tok_data["model"]:
                        tokenizer_vocab_size = len(tok_data["model"]["vocab"])
            except Exception:
                pass

    # Compute dataset manifest hash
    manifest_hash: Optional[str] = None
    if manifest_path is not None:
        man_p = Path(manifest_path)
        if man_p.is_file():
            manifest_hash = compute_file_sha256(man_p)

    payload: Dict[str, Any] = {
        "format_version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "step": int(step),
        "epoch": int(epoch),
        "tokens_processed": int(tokens_processed),
        "val_loss": float(val_loss) if val_loss is not None else None,
        "best_val_loss": float(best_val_loss) if best_val_loss is not None else None,
        # Weights and optimizer states
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict() if optimizer is not None else None,
        "scheduler_state_dict": scheduler.state_dict() if scheduler is not None else None,
        # RNG states
        "rng_states": get_rng_states(),
        # Configurations & Artifact Provenance
        "model_config": model_config_dict,
        "training_config": _config_to_dict(training_config),
        "tokenizer_vocab_size": tokenizer_vocab_size,
        "tokenizer_hash": tokenizer_hash,
        "manifest_hash": manifest_hash,
        # System Telemetry
        "environment": {
            "python_version": sys.version.split()[0],
            "torch_version": torch.__version__,
            "cuda_available": torch.cuda.is_available(),
            "device": str(device) if device is not None else ("cuda" if torch.cuda.is_available() else "cpu"),
            "platform": sys.platform,
        },
    }

    # Atomic write pattern: save to temporary file in same directory, then rename
    tmp_path = target.parent / f".{target.name}.tmp_{uuid.uuid4().hex[:8]}"
    try:
        torch.save(payload, str(tmp_path))
        os.replace(str(tmp_path), str(target))
    except Exception as e:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except Exception:
                pass
        raise CheckpointError(f"Failed to save checkpoint atomically to {target}: {e}") from e

    return target


def load_checkpoint(
    checkpoint_path: Union[str, Path],
    model: Optional[nn.Module] = None,
    optimizer: Optional[Optimizer] = None,
    scheduler: Optional[Any] = None,
    device: Optional[Union[str, torch.device]] = "cpu",
    restore_rng: bool = True,
    verify_compatibility: bool = True,
    expected_config: Optional[Any] = None,
    expected_tokenizer_hash: Optional[str] = None,
    expected_vocab_size: Optional[int] = None,
) -> Dict[str, Any]:
    """Load and optionally verify a checkpoint.

    Restores model weights, optimizer moments, scheduler progress, and RNG states.
    Validates structural and architectural compatibility before modifying any weights.

    Args:
        checkpoint_path: Path to the checkpoint file to load.
        model: Optional model to restore state_dict into.
        optimizer: Optional optimizer to restore state_dict into.
        scheduler: Optional scheduler to restore state_dict into.
        device: Device to map tensors onto ('cpu', 'cuda', etc.).
        restore_rng: Whether to restore random number generator states.
        verify_compatibility: Whether to enforce compatibility checks.
        expected_config: Expected model configuration to verify against.
        expected_tokenizer_hash: Expected tokenizer SHA-256 hash.
        expected_vocab_size: Expected vocabulary size.

    Returns:
        The loaded checkpoint dictionary.

    Raises:
        FileNotFoundError: If checkpoint file does not exist.
        CheckpointCorruptedError: If file is incomplete or unreadable.
        CheckpointCompatibilityError: If architecture or tokenizer hashes mismatch.
    """
    path = Path(checkpoint_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Checkpoint file does not exist: {path}")

    # Load with weights_only=False to support complete optimizer and RNG objects
    try:
        checkpoint = torch.load(str(path), map_location=device, weights_only=False)
    except Exception as e:
        raise CheckpointCorruptedError(
            f"Failed to load checkpoint file at {path}: {e}"
        ) from e

    if not isinstance(checkpoint, dict):
        raise CheckpointCorruptedError(
            f"Checkpoint at {path} is not a valid dictionary payload, got {type(checkpoint).__name__}"
        )

    required_keys = ["model_state_dict", "step", "model_config"]
    missing = [k for k in required_keys if k not in checkpoint]
    if missing:
        raise CheckpointCorruptedError(
            f"Checkpoint at {path} is missing required keys: {missing}"
        )

    # Compatibility verification
    if verify_compatibility:
        saved_model_config = checkpoint.get("model_config", {})

        # 1. Expected config check
        if expected_config is not None:
            exp_dict = _config_to_dict(expected_config)
            critical_arch_keys = [
                "vocab_size",
                "d_model",
                "n_layers",
                "n_heads",
                "d_ff",
                "pad_token_id",
            ]
            for key in critical_arch_keys:
                if key in exp_dict and key in saved_model_config:
                    if exp_dict[key] != saved_model_config[key]:
                        raise CheckpointCompatibilityError(
                            f"Model configuration mismatch on '{key}': expected "
                            f"{exp_dict[key]}, but checkpoint has {saved_model_config[key]}."
                        )

        # 2. Vocabulary size check
        if expected_vocab_size is not None:
            saved_vocab = saved_model_config.get("vocab_size") or checkpoint.get("tokenizer_vocab_size")
            if saved_vocab is not None and saved_vocab != expected_vocab_size:
                raise CheckpointCompatibilityError(
                    f"Vocabulary size mismatch: expected {expected_vocab_size}, "
                    f"but checkpoint has {saved_vocab}."
                )

        # 3. Tokenizer hash check
        if expected_tokenizer_hash is not None:
            saved_tok_hash = checkpoint.get("tokenizer_hash")
            if saved_tok_hash is not None and saved_tok_hash != expected_tokenizer_hash:
                raise CheckpointCompatibilityError(
                    f"Tokenizer SHA-256 hash mismatch: expected {expected_tokenizer_hash}, "
                    f"but checkpoint has {saved_tok_hash}. Resuming with a different tokenizer "
                    f"would corrupt token embeddings."
                )

    # Restore Model Weights
    if model is not None:
        try:
            model.load_state_dict(checkpoint["model_state_dict"])
        except Exception as e:
            raise CheckpointCompatibilityError(
                f"Failed to load model state_dict from checkpoint into target model: {e}"
            ) from e

    # Restore Optimizer State
    if optimizer is not None:
        opt_state = checkpoint.get("optimizer_state_dict")
        if opt_state is not None:
            try:
                optimizer.load_state_dict(opt_state)
            except Exception as e:
                raise CheckpointCompatibilityError(
                    f"Failed to load optimizer state_dict from checkpoint: {e}"
                ) from e

    # Restore Scheduler State
    if scheduler is not None:
        sched_state = checkpoint.get("scheduler_state_dict")
        if sched_state is not None:
            try:
                scheduler.load_state_dict(sched_state)
            except Exception as e:
                raise CheckpointCompatibilityError(
                    f"Failed to load scheduler state_dict from checkpoint: {e}"
                ) from e

    # Restore RNG States
    if restore_rng and "rng_states" in checkpoint:
        set_rng_states(checkpoint["rng_states"])

    return checkpoint
