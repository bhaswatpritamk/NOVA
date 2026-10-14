"""Project Nova-Fit: Evaluation Engine.

Provides rigorous evaluation for Nova-Fit causal language models on held-out validation data.
Features:
- Pure evaluation mode without gradient calculation (torch.no_grad())
- Guarantees zero model weight mutation
- Correctly shifted targets for causal next-token prediction
- Strict masking/exclusion of padding tokens (<pad> = 0) from loss and perplexity
- Token-weighted cross-entropy loss aggregation
- Perplexity computation with numerical overflow guards
- Non-finite loss/logits detection (NaN / Inf)
- Manifest provenance tracking
"""

from __future__ import annotations

import math
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset

from nova.checkpoint import compute_file_sha256


@dataclass
class EvaluationResult:
    """Diagnostic metrics and provenance report from model evaluation.

    Note:
        On small seed or fixture corpora, validation loss and perplexity are
        strictly diagnostic metrics of numerical stability and optimization behavior.
        They do not represent real-world conversational fitness intelligence.
    """

    loss: float
    perplexity: float
    total_valid_tokens: int
    total_pad_tokens: int
    total_sequences: int
    manifest_hash: Optional[str] = None
    duration_seconds: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert results to a JSON-serializable dictionary."""
        return asdict(self)

    def summary(self) -> str:
        """Formatted human-readable summary string."""
        ppl_str = f"{self.perplexity:.4f}" if math.isfinite(self.perplexity) else "inf"
        return (
            f"Evaluation Summary:\n"
            f"  Cross-Entropy Loss:    {self.loss:.4f}\n"
            f"  Perplexity:            {ppl_str}\n"
            f"  Non-pad Valid Tokens:  {self.total_valid_tokens:,}\n"
            f"  Padding Tokens:        {self.total_pad_tokens:,}\n"
            f"  Sequences Evaluated:   {self.total_sequences:,}\n"
            f"  Duration:              {self.duration_seconds:.3f}s\n"
            f"  Manifest Hash:         {self.manifest_hash or 'N/A'}"
        )


@torch.no_grad()
def evaluate_model(
    model: nn.Module,
    val_data: Union[torch.Tensor, Dataset, DataLoader, str, Path],
    device: Optional[Union[str, torch.device]] = None,
    batch_size: int = 4,
    pad_token_id: int = 0,
    max_batches: Optional[int] = None,
    manifest_path: Optional[Union[str, Path]] = None,
) -> EvaluationResult:
    """Evaluate a causal language model on held-out validation data.

    Executes strictly in evaluation mode (model.eval()) under torch.no_grad().
    Ensures that model weights are not altered during evaluation.

    Args:
        model: NovaForCausalLM or compatible causal Transformer model.
        val_data: Validation data source (Tensor of shape [N, T], Dataset, DataLoader,
            or path to .pt tensor file).
        device: Device to run evaluation on (e.g., 'cpu', 'cuda'). Defaults to model device.
        batch_size: Batch size to use if val_data is a Tensor or path.
        pad_token_id: Special token ID for padding to exclude from loss computation.
        max_batches: Optional cap on the number of validation batches to evaluate.
        manifest_path: Optional path to dataset manifest.json for provenance recording.

    Returns:
        EvaluationResult containing aggregate cross-entropy loss, perplexity,
        token counts, and runtime duration.

    Raises:
        ValueError: If non-finite loss or non-finite logits are encountered.
        FileNotFoundError: If manifest_path or file path does not exist.
    """
    start_time = time.perf_counter()

    # Determine target device
    if device is None:
        try:
            device = next(model.parameters()).device
        except StopIteration:
            device = torch.device("cpu")
    else:
        device = torch.device(device)

    # Set model to evaluation mode
    was_training = model.training
    model.eval()

    # Resolve manifest hash if manifest path is provided
    manifest_hash: Optional[str] = None
    if manifest_path is not None:
        mp = Path(manifest_path)
        if mp.is_file():
            manifest_hash = compute_file_sha256(mp)

    # Prepare batches
    batches: list[Any] = []
    if isinstance(val_data, (str, Path)):
        p = Path(val_data)
        if not p.is_file():
            raise FileNotFoundError(f"Validation data file not found: {p}")
        tensor = torch.load(str(p), map_location=device, weights_only=True)
        for i in range(0, len(tensor), batch_size):
            batches.append(tensor[i : i + batch_size])
    elif isinstance(val_data, torch.Tensor):
        tensor = val_data.to(device)
        for i in range(0, len(tensor), batch_size):
            batches.append(tensor[i : i + batch_size])
    elif isinstance(val_data, DataLoader):
        batches = list(val_data)
    else:  # Assume Dataset
        loader = DataLoader(val_data, batch_size=batch_size, shuffle=False)
        batches = list(loader)

    total_loss_sum = 0.0
    total_valid_tokens = 0
    total_pad_tokens = 0
    total_sequences = 0

    try:
        for batch_idx, batch in enumerate(batches):
            if max_batches is not None and batch_idx >= max_batches:
                break

            # Handle different batch representations
            max_len = getattr(getattr(model, "config", None), "max_seq_len", None)

            if isinstance(batch, (tuple, list)) and len(batch) == 2:
                # Pre-shifted pair (input_ids, target_ids) from NovaPretrainingDataset
                input_ids, targets = batch
                input_ids = input_ids.to(device)
                targets = targets.to(device)
                if max_len is not None and input_ids.size(1) > max_len:
                    input_ids = input_ids[:, :max_len]
                    targets = targets[:, :max_len]
                seq_count = input_ids.size(0)

                output = model(input_ids)
                logits = output.logits

                if not torch.isfinite(logits).all():
                    raise ValueError(
                        f"Non-finite logits (NaN/Inf) detected during evaluation at batch {batch_idx}."
                    )

                shift_logits = logits
                shift_targets = targets

            elif isinstance(batch, torch.Tensor):
                # Full sequences [B, T]
                seqs = batch.to(device)
                if max_len is not None and seqs.size(1) > max_len:
                    seqs = seqs[:, :max_len]
                seq_count = seqs.size(0)

                output = model(seqs)
                logits = output.logits


                if not torch.isfinite(logits).all():
                    raise ValueError(
                        f"Non-finite logits (NaN/Inf) detected during evaluation at batch {batch_idx}."
                    )

                # Shift for causal prediction: logits at t predict seqs at t+1
                shift_logits = logits[..., :-1, :].contiguous()
                shift_targets = seqs[..., 1:].contiguous()
            else:
                raise TypeError(
                    f"Unsupported batch type: {type(batch).__name__}. Expected Tensor or (input, target) tuple."
                )

            total_sequences += seq_count

            # Count valid vs padding tokens
            valid_mask = shift_targets != pad_token_id
            num_valid = int(valid_mask.sum().item())
            num_pad = int((~valid_mask).sum().item())

            total_valid_tokens += num_valid
            total_pad_tokens += num_pad

            if num_valid > 0:
                vocab_size = shift_logits.size(-1)
                # Compute token-summed cross-entropy loss, ignoring pad tokens
                loss_sum = F.cross_entropy(
                    shift_logits.view(-1, vocab_size),
                    shift_targets.view(-1),
                    ignore_index=pad_token_id,
                    reduction="sum",
                )

                if not torch.isfinite(loss_sum):
                    raise ValueError(
                        f"Non-finite loss (NaN/Inf) detected during evaluation at batch {batch_idx}."
                    )

                total_loss_sum += float(loss_sum.item())

    finally:
        # Restore original training mode
        if was_training:
            model.train()

    # Aggregate metrics
    if total_valid_tokens > 0:
        avg_loss = total_loss_sum / total_valid_tokens
        # Guard against math overflow in exp(loss)
        perplexity = math.exp(min(avg_loss, 100.0))
    else:
        avg_loss = float("nan")
        perplexity = float("nan")

    duration = time.perf_counter() - start_time

    return EvaluationResult(
        loss=avg_loss,
        perplexity=perplexity,
        total_valid_tokens=total_valid_tokens,
        total_pad_tokens=total_pad_tokens,
        total_sequences=total_sequences,
        manifest_hash=manifest_hash,
        duration_seconds=duration,
    )
