"""Project Nova-Fit: Pretraining Engine.

Implements causal language model pretraining for Nova-Fit:
- Causal next-token prediction with correctly shifted targets
- Masked cross-entropy loss excluding padding tokens (<pad> = 0)
- AdamW optimizer with configurable learning rate and weight decay
- Learning rate schedules (cosine with warmup, linear with warmup, constant)
- Gradient accumulation and gradient clipping
- Atomic checkpointing (latest, best-validation, and per-step)
- Checkpoint resumption restoring weights, optimizer, scheduler, and RNG states
- Strict compatibility verification (model architecture, vocab size, tokenizer hash)
- Non-finite loss (NaN/Inf) detection and immediate clean failure
- Support for CPU and CUDA execution with automatic hardware detection
"""

from __future__ import annotations

import json
import math
import random
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import AdamW, Optimizer
from torch.optim.lr_scheduler import LambdaLR, _LRScheduler
from torch.utils.data import DataLoader, Dataset

from nova.checkpoint import (
    CheckpointCompatibilityError,
    CheckpointCorruptedError,
    CheckpointError,
    compute_file_sha256,
    load_checkpoint,
    save_checkpoint,
)
from nova.evaluate import EvaluationResult, evaluate_model
from nova.model import NovaConfig, NovaForCausalLM


def set_seed(seed: int) -> None:
    """Set random seeds across Python, NumPy, and PyTorch for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def get_lr_scheduler(
    optimizer: Optimizer,
    schedule: str = "cosine",
    warmup_steps: int = 5,
    max_steps: int = 50,
    min_lr_ratio: float = 0.1,
) -> LambdaLR:
    """Construct a learning rate scheduler with warmup and decay.

    Args:
        optimizer: PyTorch optimizer.
        schedule: Schedule type ('cosine', 'linear', or 'constant').
        warmup_steps: Number of initial linear warmup steps.
        max_steps: Total number of optimizer steps.
        min_lr_ratio: Minimum LR as a fraction of initial LR (for cosine/linear).

    Returns:
        LambdaLR scheduler instance.
    """
    schedule_lower = schedule.lower()
    if schedule_lower not in ("cosine", "linear", "constant"):
        raise ValueError(
            f"Invalid lr_schedule: '{schedule}'. Supported schedules: 'cosine', 'linear', 'constant'."
        )

    def lr_lambda(current_step: int) -> float:
        # Linear warmup phase (1-indexed so step 0 gets non-zero learning rate)
        if warmup_steps > 0 and current_step < warmup_steps:
            return float(current_step + 1) / float(warmup_steps)

        # Progress after warmup [0.0, 1.0]
        progress = float(current_step - warmup_steps) / float(max(1, max_steps - warmup_steps))
        progress = min(max(progress, 0.0), 1.0)

        if schedule_lower == "constant":
            return 1.0
        elif schedule_lower == "linear":
            return max(min_lr_ratio, 1.0 - progress * (1.0 - min_lr_ratio))
        elif schedule_lower == "cosine":
            coeff = 0.5 * (1.0 + math.cos(math.pi * progress))
            return min_lr_ratio + coeff * (1.0 - min_lr_ratio)
        return 1.0

    return LambdaLR(optimizer, lr_lambda)


@dataclass
class TrainingConfig:
    """Configuration for pretraining Nova-Fit causal language models."""

    # Data and Paths
    data_dir: str = "data/prepared_final"
    output_dir: str = "checkpoints/run_01"
    model_config_path: Optional[str] = None
    tokenizer_path: str = "artifacts/final_tokenizer"
    manifest_path: Optional[str] = None

    # Optimization Hyperparameters
    batch_size: int = 2
    max_seq_len: int = 512
    gradient_accumulation_steps: int = 1
    max_steps: int = 20
    learning_rate: float = 3e-4
    min_learning_rate: float = 3e-5
    weight_decay: float = 0.01
    beta1: float = 0.9
    beta2: float = 0.95
    eps: float = 1e-8
    max_grad_norm: Optional[float] = 1.0

    # Learning Rate Schedule
    warmup_steps: int = 5
    lr_schedule: str = "cosine"  # 'cosine', 'linear', 'constant'

    # Evaluation and Checkpointing
    eval_interval: int = 5
    save_interval: int = 10
    save_step_checkpoints: bool = True
    seed: int = 42
    device: str = "auto"  # 'auto', 'cpu', 'cuda'
    mixed_precision: str = "no"  # 'no', 'fp16', 'bf16'
    resume_from: Optional[str] = None
    log_interval: int = 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TrainingConfig:
        """Create configuration from dictionary."""
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore
        filtered = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered)

    @classmethod
    def from_json_file(cls, path: Union[str, Path]) -> TrainingConfig:
        """Load configuration from JSON file."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def validate(self) -> None:
        """Validate configuration parameters."""
        if self.batch_size <= 0:
            raise ValueError(f"batch_size must be positive, got {self.batch_size}")
        if self.max_seq_len <= 0:
            raise ValueError(f"max_seq_len must be positive, got {self.max_seq_len}")
        if self.gradient_accumulation_steps <= 0:
            raise ValueError(
                f"gradient_accumulation_steps must be positive, got {self.gradient_accumulation_steps}"
            )
        if self.max_steps <= 0:
            raise ValueError(f"max_steps must be positive, got {self.max_steps}")
        if self.learning_rate <= 0:
            raise ValueError(f"learning_rate must be positive, got {self.learning_rate}")
        if self.lr_schedule.lower() not in ("cosine", "linear", "constant"):
            raise ValueError(f"Unsupported lr_schedule: '{self.lr_schedule}'")
        if self.mixed_precision.lower() not in ("no", "fp16", "bf16"):
            raise ValueError(
                f"Unsupported mixed_precision: '{self.mixed_precision}'. Supported: 'no', 'fp16', 'bf16'."
            )


@dataclass
class TrainerResult:
    """Summary of training run execution and outcomes."""

    success: bool
    initial_loss: float
    final_loss: float
    total_steps: int
    total_tokens_processed: int
    best_val_loss: Optional[float]
    final_val_loss: Optional[float]
    final_perplexity: Optional[float]
    checkpoints_saved: List[str]
    elapsed_seconds: float
    device: str
    mixed_precision: str = "no"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SequenceTensorDataset(Dataset):
    """Simple in-memory Dataset over a 2D LongTensor of sequences [N, T]."""

    def __init__(self, tensor: torch.Tensor) -> None:
        if tensor.dim() != 2:
            raise ValueError(f"Expected 2D tensor [N, T], got shape {tensor.shape}")
        self.tensor = tensor

    def __len__(self) -> int:
        return self.tensor.size(0)

    def __getitem__(self, idx: int) -> torch.Tensor:
        return self.tensor[idx]


class Trainer:
    """Orchestrates causal language model pretraining for Project Nova-Fit."""

    def __init__(
        self,
        config: TrainingConfig,
        model: Optional[NovaForCausalLM] = None,
        train_data: Optional[Union[torch.Tensor, Dataset]] = None,
        val_data: Optional[Union[torch.Tensor, Dataset]] = None,
    ) -> None:
        """Initialize the trainer.

        Args:
            config: Training configuration.
            model: Optional pre-constructed NovaForCausalLM model.
            train_data: Optional pre-loaded training dataset or tensor.
            val_data: Optional pre-loaded validation dataset or tensor.
        """
        config.validate()
        self.config = config

        # Set reproducible seeds
        set_seed(self.config.seed)

        # Resolve device
        if self.config.device == "auto":
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        elif self.config.device == "cuda":
            if not torch.cuda.is_available():
                raise RuntimeError("CUDA was requested in training config but is not available.")
            self.device = torch.device("cuda")
        else:
            self.device = torch.device(self.config.device)

        # Output and checkpoints directory
        self.output_dir = Path(self.config.output_dir).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Resolve tokenizer hash
        self.tokenizer_path = Path(self.config.tokenizer_path)
        self.tokenizer_hash: Optional[str] = None
        tok_json = self.tokenizer_path if self.tokenizer_path.is_file() else self.tokenizer_path / "tokenizer.json"
        if tok_json.is_file():
            self.tokenizer_hash = compute_file_sha256(tok_json)

        # Resolve manifest path and hash
        self.manifest_path = Path(self.config.manifest_path) if self.config.manifest_path else None
        if self.manifest_path is None:
            cand = Path(self.config.data_dir) / "manifest.json"
            if cand.is_file():
                self.manifest_path = cand

        self.manifest_hash: Optional[str] = None
        if self.manifest_path and self.manifest_path.is_file():
            self.manifest_hash = compute_file_sha256(self.manifest_path)

        # Initialize or assign model
        if model is not None:
            self.model = model.to(self.device)
        else:
            self.model = self._init_model().to(self.device)

        # Setup Optimizer
        self.optimizer = self._init_optimizer()

        # Setup Scheduler
        min_ratio = (
            self.config.min_learning_rate / self.config.learning_rate
            if self.config.learning_rate > 0
            else 0.1
        )
        self.scheduler = get_lr_scheduler(
            optimizer=self.optimizer,
            schedule=self.config.lr_schedule,
            warmup_steps=self.config.warmup_steps,
            max_steps=self.config.max_steps,
            min_lr_ratio=min_ratio,
        )
        # Mixed precision setup
        self.mixed_precision = self.config.mixed_precision.lower()
        self.use_amp = (
            (self.mixed_precision == "fp16" and self.device.type == "cuda")
            or (self.mixed_precision == "bf16" and self.device.type in ("cuda", "cpu"))
        )
        if self.mixed_precision == "fp16":
            self.amp_dtype = torch.float16
        elif self.mixed_precision == "bf16":
            self.amp_dtype = torch.bfloat16
        else:
            self.amp_dtype = torch.float32

        scaler_enabled = (self.device.type == "cuda" and self.mixed_precision == "fp16")
        if hasattr(torch.amp, "GradScaler"):
            self.scaler = torch.amp.GradScaler("cuda", enabled=scaler_enabled)
        else:
            self.scaler = torch.cuda.amp.GradScaler(enabled=scaler_enabled)

        # Datasets
        if train_data is not None:
            self.train_data = train_data
            self.val_data = val_data
        else:
            self.train_data = self._load_split_tensor("train")
            self.val_data = val_data if val_data is not None else self._load_split_tensor("val", optional=True)

        # State tracking
        self.global_step = 0
        self.tokens_processed = 0
        self.epoch = 0
        self.best_val_loss: Optional[float] = None
        self.saved_checkpoints: List[str] = []

        # Handle Resumption if requested
        if self.config.resume_from:
            self._resume_from_checkpoint(self.config.resume_from)

    def _init_model(self) -> NovaForCausalLM:
        """Instantiate NovaForCausalLM from config file or default final-tokenizer dimensions."""
        if self.config.model_config_path and Path(self.config.model_config_path).is_file():
            model_cfg = NovaConfig.from_json_file(self.config.model_config_path)
        else:
            # Check if dataset manifest has vocab_size
            vocab_size = 3384  # Default to Phase 4 final tokenizer vocab size
            if self.manifest_path and self.manifest_path.is_file():
                try:
                    with open(self.manifest_path, "r", encoding="utf-8") as f:
                        m_data = json.load(f)
                        if "tokenizer_vocab_size" in m_data:
                            vocab_size = m_data["tokenizer_vocab_size"]
                except Exception:
                    pass

            model_cfg = NovaConfig(
                vocab_size=vocab_size,
                max_seq_len=self.config.max_seq_len,
                d_model=64,
                n_layers=2,
                n_heads=4,
                d_ff=176,
                pad_token_id=0,
            )

        return NovaForCausalLM(model_cfg)

    def _init_optimizer(self) -> Optimizer:
        """Initialize AdamW optimizer with weight decay applied exclusively to 2D matrix weights."""
        decay_params = []
        no_decay_params = []

        for name, param in self.model.named_parameters():
            if not param.requires_grad:
                continue
            if param.dim() >= 2:
                decay_params.append(param)
            else:
                # 1D tensors: RMSNorm scales, biases
                no_decay_params.append(param)

        optim_groups = [
            {"params": decay_params, "weight_decay": self.config.weight_decay},
            {"params": no_decay_params, "weight_decay": 0.0},
        ]

        return AdamW(
            optim_groups,
            lr=self.config.learning_rate,
            betas=(self.config.beta1, self.config.beta2),
            eps=self.config.eps,
        )

    def _load_split_tensor(self, split: str, optional: bool = False) -> Optional[torch.Tensor]:
        """Load prepared PyTorch tensor for train or val split."""
        data_dir = Path(self.config.data_dir)
        p = data_dir / f"{split}.pt"
        if not p.is_file():
            if optional:
                return None
            raise FileNotFoundError(f"Required dataset split file not found: {p}")
        tensor = torch.load(str(p), weights_only=True)
        return tensor

    def _resume_from_checkpoint(self, checkpoint_path: str) -> None:
        """Restore model, optimizer, scheduler, and RNG state from a checkpoint."""
        ckpt = load_checkpoint(
            checkpoint_path=checkpoint_path,
            model=self.model,
            optimizer=self.optimizer,
            scheduler=self.scheduler,
            device=self.device,
            restore_rng=True,
            verify_compatibility=True,
            expected_config=self.model.config,
            expected_tokenizer_hash=self.tokenizer_hash,
            expected_vocab_size=self.model.config.vocab_size,
        )
        self.global_step = ckpt.get("step", 0)
        self.epoch = ckpt.get("epoch", 0)
        self.tokens_processed = ckpt.get("tokens_processed", 0)
        self.best_val_loss = ckpt.get("best_val_loss")

    def train(self) -> TrainerResult:
        """Execute the pretraining loop.

        Returns:
            TrainerResult containing training metrics and checkpoint records.

        Raises:
            ValueError: If non-finite loss or non-finite gradients are encountered.
        """
        start_time = time.perf_counter()
        self.model.train()

        # Build DataLoader
        if isinstance(self.train_data, torch.Tensor):
            dataset: Dataset = SequenceTensorDataset(self.train_data)
        else:
            dataset = self.train_data

        loader = DataLoader(
            dataset,
            batch_size=self.config.batch_size,
            shuffle=True,
            drop_last=False,
        )

        pad_token_id = getattr(self.model.config, "pad_token_id", 0)
        initial_loss: Optional[float] = None
        last_step_loss: float = 0.0
        final_val_loss: Optional[float] = None
        final_ppl: Optional[float] = None

        accum_loss = 0.0
        accum_steps = 0
        self.optimizer.zero_grad()

        # Loop through epochs until max_steps reached
        while self.global_step < self.config.max_steps:
            for batch in loader:
                if self.global_step >= self.config.max_steps:
                    break

                # Prepare inputs and targets
                if isinstance(batch, (tuple, list)) and len(batch) == 2:
                    input_ids, targets = batch
                    input_ids = input_ids.to(self.device)
                    targets = targets.to(self.device)
                    with torch.autocast(device_type=self.device.type, dtype=self.amp_dtype, enabled=self.use_amp):
                        logits = self.model(input_ids).logits
                        shift_logits = logits
                        shift_targets = targets
                elif isinstance(batch, torch.Tensor):
                    seqs = batch.to(self.device)
                    with torch.autocast(device_type=self.device.type, dtype=self.amp_dtype, enabled=self.use_amp):
                        logits = self.model(seqs).logits
                        shift_logits = logits[..., :-1, :].contiguous()
                        shift_targets = seqs[..., 1:].contiguous()
                else:
                    raise TypeError(f"Unsupported batch type: {type(batch).__name__}")

                # Mask padding tokens
                valid_mask = shift_targets != pad_token_id
                num_valid_tokens = int(valid_mask.sum().item())

                if num_valid_tokens == 0:
                    continue

                vocab_size = shift_logits.size(-1)
                with torch.autocast(device_type=self.device.type, dtype=self.amp_dtype, enabled=self.use_amp):
                    # Compute token-averaged cross-entropy loss for this micro-batch
                    loss = F.cross_entropy(
                        shift_logits.view(-1, vocab_size),
                        shift_targets.view(-1),
                        ignore_index=pad_token_id,
                    )

                if not torch.isfinite(loss):
                    raise ValueError(
                        f"Non-finite loss ({loss.item()}) encountered at global step {self.global_step}."
                    )

                if initial_loss is None:
                    initial_loss = float(loss.item())

                last_step_loss = float(loss.item())
                self.tokens_processed += num_valid_tokens

                # Scale loss by gradient accumulation steps
                scaled_loss = loss / self.config.gradient_accumulation_steps
                if self.scaler.is_enabled():
                    self.scaler.scale(scaled_loss).backward()
                else:
                    scaled_loss.backward()

                accum_loss += float(loss.item())
                accum_steps += 1

                # Check if accumulation window is reached
                if accum_steps % self.config.gradient_accumulation_steps == 0:
                    # Unscale gradients prior to clipping and finiteness check
                    if self.scaler.is_enabled():
                        self.scaler.unscale_(self.optimizer)

                    # Clip gradients if configured
                    if self.config.max_grad_norm is not None:
                        torch.nn.utils.clip_grad_norm_(
                            self.model.parameters(), max_norm=self.config.max_grad_norm
                        )

                    # Verify gradient finiteness
                    for name, p in self.model.named_parameters():
                        if p.grad is not None and not torch.isfinite(p.grad).all():
                            raise ValueError(
                                f"Non-finite gradient in '{name}' at step {self.global_step}."
                            )

                    if self.scaler.is_enabled():
                        self.scaler.step(self.optimizer)
                        self.scaler.update()
                    else:
                        self.optimizer.step()

                    self.scheduler.step()
                    self.optimizer.zero_grad()

                    self.global_step += 1
                    avg_accum_loss = accum_loss / self.config.gradient_accumulation_steps
                    accum_loss = 0.0

                    # Periodic logging
                    if self.global_step % self.config.log_interval == 0:
                        current_lr = self.scheduler.get_last_lr()[0]
                        pass

                    # Periodic Evaluation
                    if (
                        self.val_data is not None
                        and self.config.eval_interval > 0
                        and (self.global_step % self.config.eval_interval == 0 or self.global_step == self.config.max_steps)
                    ):
                        eval_res = self.evaluate()
                        final_val_loss = eval_res.loss
                        final_ppl = eval_res.perplexity

                        # Best model checkpointing
                        if self.best_val_loss is None or eval_res.loss < self.best_val_loss:
                            self.best_val_loss = eval_res.loss
                            best_path = self.output_dir / "checkpoint_best.pt"
                            self._save_checkpoint(best_path, val_loss=eval_res.loss)

                    # Periodic Checkpoint Saving
                    if (
                        self.config.save_interval > 0
                        and (self.global_step % self.config.save_interval == 0 or self.global_step == self.config.max_steps)
                    ):
                        # Save step checkpoint if enabled
                        if self.config.save_step_checkpoints:
                            step_path = self.output_dir / f"checkpoint_step_{self.global_step:06d}.pt"
                            self._save_checkpoint(step_path, val_loss=final_val_loss)

                        # Always update checkpoint_latest.pt
                        latest_path = self.output_dir / "checkpoint_latest.pt"
                        self._save_checkpoint(latest_path, val_loss=final_val_loss)

            self.epoch += 1

        # Final checkpoint save at end of training
        latest_path = self.output_dir / "checkpoint_latest.pt"
        self._save_checkpoint(latest_path, val_loss=final_val_loss)

        elapsed = time.perf_counter() - start_time

        return TrainerResult(
            success=True,
            initial_loss=initial_loss if initial_loss is not None else 0.0,
            final_loss=last_step_loss,
            total_steps=self.global_step,
            total_tokens_processed=self.tokens_processed,
            best_val_loss=self.best_val_loss,
            final_val_loss=final_val_loss,
            final_perplexity=final_ppl,
            checkpoints_saved=self.saved_checkpoints,
            elapsed_seconds=elapsed,
            device=str(self.device),
            mixed_precision=self.config.mixed_precision,
        )

    def evaluate(self, max_batches: Optional[int] = None) -> EvaluationResult:
        """Run evaluation on validation split."""
        if self.val_data is None:
            raise ValueError("No validation data available for evaluation.")

        pad_token_id = getattr(self.model.config, "pad_token_id", 0)
        return evaluate_model(
            model=self.model,
            val_data=self.val_data,
            device=self.device,
            batch_size=self.config.batch_size,
            pad_token_id=pad_token_id,
            max_batches=max_batches,
            manifest_path=self.manifest_path,
        )

    def _save_checkpoint(self, path: Path, val_loss: Optional[float] = None) -> Path:
        """Save an atomic checkpoint using the checkpoint module."""
        saved_path = save_checkpoint(
            checkpoint_path=path,
            model=self.model,
            optimizer=self.optimizer,
            scheduler=self.scheduler,
            step=self.global_step,
            epoch=self.epoch,
            tokens_processed=self.tokens_processed,
            val_loss=val_loss,
            best_val_loss=self.best_val_loss,
            model_config=self.model.config,
            training_config=self.config,
            tokenizer_path=self.tokenizer_path,
            manifest_path=self.manifest_path,
            device=self.device,
        )
        p_str = str(saved_path)
        if p_str not in self.saved_checkpoints:
            self.saved_checkpoints.append(p_str)
        return saved_path
