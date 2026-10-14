#!/usr/bin/env python3
"""Project Nova-Fit: Pretraining CLI Script.

Executes causal language model pretraining (Phase 5):
- Causal next-token prediction with shifted targets
- Masked cross-entropy excluding padding tokens (<pad> = 0)
- Configurable AdamW, LR schedule, gradient accumulation, and clipping
- Atomic checkpointing and robust resumption
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Optional

# Ensure utf-8 stdout encoding on Windows console
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import torch

from nova.train import Trainer, TrainingConfig


def parse_args(args: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments for model pretraining."""
    parser = argparse.ArgumentParser(
        description="Nova-Fit Language Model Pretraining Engine (Phase 5).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default="configs/training_smoke.json",
        help="Path to training JSON configuration file.",
    )
    parser.add_argument(
        "-d",
        "--data-dir",
        type=str,
        default=None,
        help="Path to directory containing prepared train.pt, val.pt, and manifest.json.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default=None,
        help="Directory to save training checkpoints and artifacts.",
    )
    parser.add_argument(
        "--tokenizer",
        type=str,
        default=None,
        help="Path to tokenizer artifact directory or tokenizer.json.",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=None,
        help="Maximum optimizer steps to run.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=None,
        help="Batch size per optimizer step.",
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=None,
        help="Peak learning rate.",
    )
    parser.add_argument(
        "--grad-accum",
        type=int,
        default=None,
        help="Number of micro-batches to accumulate gradients over.",
    )
    parser.add_argument(
        "--resume-from",
        type=str,
        default=None,
        help="Path to checkpoint file (.pt) to resume training from.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default=None,
        help="Target execution device: 'auto', 'cpu', or 'cuda'.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducible training.",
    )

    return parser.parse_args(args)


def main(args: Optional[list[str]] = None) -> int:
    """Entrypoint for the training CLI script."""
    parsed = parse_args(args)

    print("=" * 75)
    print("Project Nova-Fit: Pretraining Engine (Phase 5)")
    print("=" * 75)

    # Load configuration
    cfg_path = Path(parsed.config) if parsed.config else None
    if cfg_path and cfg_path.is_file():
        print(f"Loading base configuration from: {cfg_path}")
        config = TrainingConfig.from_json_file(cfg_path)
    else:
        print("Using default training configuration.")
        config = TrainingConfig()

    # Apply CLI overrides
    if parsed.data_dir is not None:
        config.data_dir = parsed.data_dir
    if parsed.output_dir is not None:
        config.output_dir = parsed.output_dir
    if parsed.tokenizer is not None:
        config.tokenizer_path = parsed.tokenizer
    if parsed.max_steps is not None:
        config.max_steps = parsed.max_steps
    if parsed.batch_size is not None:
        config.batch_size = parsed.batch_size
    if parsed.learning_rate is not None:
        config.learning_rate = parsed.learning_rate
    if parsed.grad_accum is not None:
        config.gradient_accumulation_steps = parsed.grad_accum
    if parsed.resume_from is not None:
        config.resume_from = parsed.resume_from
    if parsed.device is not None:
        config.device = parsed.device
    if parsed.seed is not None:
        config.seed = parsed.seed

    # Hardware Detection
    cuda_avail = torch.cuda.is_available()
    cuda_device_name = torch.cuda.get_device_name(0) if cuda_avail else "N/A"
    print(f"Hardware Telemetry:")
    print(f"  PyTorch Version:  {torch.__version__}")
    print(f"  CUDA Available:   {cuda_avail}")
    if cuda_avail:
        print(f"  CUDA Device:      {cuda_device_name}")
        vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        print(f"  Total VRAM:       {vram_gb:.2f} GB")

    print(f"\nTraining Run Configuration:")
    print(f"  Data Directory:     {config.data_dir}")
    print(f"  Output Directory:   {config.output_dir}")
    print(f"  Tokenizer Path:     {config.tokenizer_path}")
    print(f"  Batch Size:         {config.batch_size}")
    print(f"  Max Steps:          {config.max_steps}")
    print(f"  Learning Rate:      {config.learning_rate}")
    print(f"  LR Schedule:        {config.lr_schedule} (warmup={config.warmup_steps})")
    print(f"  Gradient Accum:     {config.gradient_accumulation_steps}")
    print(f"  Max Grad Norm:      {config.max_grad_norm}")
    print(f"  Target Device:      {config.device}")
    print(f"  Resume Checkpoint:  {config.resume_from or 'None (training from scratch)'}")
    print("-" * 75)

    try:
        trainer = Trainer(config)
    except Exception as e:
        print(f"\nERROR: Failed to initialize Trainer: {e}", file=sys.stderr)
        return 1

    model_params = sum(p.numel() for p in trainer.model.parameters())
    trainable_params = sum(p.numel() for p in trainer.model.parameters() if p.requires_grad)
    print(f"Model Summary:")
    print(f"  Architecture:       Decoder-Only Transformer (NovaForCausalLM)")
    print(f"  Vocabulary Size:    {trainer.model.config.vocab_size:,}")
    print(f"  Total Parameters:   {model_params:,}")
    print(f"  Trainable Params:   {trainable_params:,}")
    print(f"  Active Device:      {trainer.device}")
    print("-" * 75)

    print("Beginning training loop...")
    start_time = time.perf_counter()

    try:
        result = trainer.train()
    except Exception as e:
        print(f"\nTRAINING FAILURE: {e}", file=sys.stderr)
        return 1

    elapsed = time.perf_counter() - start_time
    tokens_per_sec = result.total_tokens_processed / max(elapsed, 1e-4)

    print("\n" + "=" * 75)
    print("Training Completed Successfully")
    print("=" * 75)
    print(f"  Total Optimizer Steps:     {result.total_steps}")
    print(f"  Initial Training Loss:     {result.initial_loss:.4f}")
    print(f"  Final Training Loss:       {result.final_loss:.4f}")
    if result.best_val_loss is not None:
        print(f"  Best Validation Loss:      {result.best_val_loss:.4f}")
    if result.final_val_loss is not None:
        print(f"  Final Validation Loss:     {result.final_val_loss:.4f}")
    if result.final_perplexity is not None:
        print(f"  Final Perplexity:          {result.final_perplexity:.4f}")
    print(f"  Tokens Processed:          {result.total_tokens_processed:,}")
    print(f"  Throughput:                {tokens_per_sec:.1f} tokens/second")
    print(f"  Elapsed Time:              {elapsed:.2f} seconds")
    print(f"  Checkpoints Saved ({len(result.checkpoints_saved)}):")
    for cp in result.checkpoints_saved:
        print(f"    - {cp}")
    print("=" * 75)

    print("\n[NOTE] Corpus Size Limitation:")
    print("The current dataset is a small initial seed corpus. Validation metrics are diagnostic")
    print("indicators of numerical health, not an assessment of full conversational fitness ability.")
    print("=" * 75)

    return 0


if __name__ == "__main__":
    sys.exit(main())
