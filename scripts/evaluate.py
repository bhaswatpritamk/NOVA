#!/usr/bin/env python3
"""Project Nova-Fit: Evaluation CLI Script.

Evaluates a Nova-Fit model checkpoint on held-out validation data (Phase 5):
- Evaluates in pure eval mode under torch.no_grad()
- Masks padding tokens from loss and perplexity
- Verifies model weights are not updated
- Reports cross-entropy loss, perplexity, and token counts
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

# Ensure utf-8 stdout encoding on Windows console
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import torch

from nova.checkpoint import load_checkpoint
from nova.evaluate import evaluate_model
from nova.model import NovaConfig, NovaForCausalLM


def parse_args(args: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments for model evaluation."""
    parser = argparse.ArgumentParser(
        description="Nova-Fit Model Evaluation Script (Phase 5).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-c",
        "--checkpoint",
        type=str,
        default=None,
        help="Path to trained checkpoint (.pt) file to evaluate.",
    )
    parser.add_argument(
        "-d",
        "--data-dir",
        type=str,
        default="data/prepared_final",
        help="Directory containing val.pt and manifest.json.",
    )
    parser.add_argument(
        "--val-file",
        type=str,
        default=None,
        help="Explicit path to validation tensor file (defaults to {data-dir}/val.pt).",
    )
    parser.add_argument(
        "--manifest",
        type=str,
        default=None,
        help="Explicit path to dataset manifest.json.",
    )
    parser.add_argument(
        "-b",
        "--batch-size",
        type=int,
        default=4,
        help="Batch size for validation inference.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        help="Device to run evaluation on: 'auto', 'cpu', or 'cuda'.",
    )

    return parser.parse_args(args)


def main(args: Optional[list[str]] = None) -> int:
    """Entrypoint for the evaluation CLI script."""
    parsed = parse_args(args)

    print("=" * 75)
    print("Project Nova-Fit: Checkpoint & Validation Evaluation (Phase 5)")
    print("=" * 75)

    # Determine device
    if parsed.device == "auto":
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    elif parsed.device == "cuda":
        if not torch.cuda.is_available():
            print("ERROR: CUDA requested but not available.", file=sys.stderr)
            return 1
        device = torch.device("cuda")
    else:
        device = torch.device(parsed.device)

    print(f"Active Evaluation Device: {device}")

    # Determine validation data path
    val_path = Path(parsed.val_file) if parsed.val_file else Path(parsed.data_dir) / "val.pt"
    if not val_path.is_file():
        print(f"ERROR: Validation data file not found: {val_path}", file=sys.stderr)
        return 1

    manifest_path = Path(parsed.manifest) if parsed.manifest else Path(parsed.data_dir) / "manifest.json"

    # Instantiate or load model
    if parsed.checkpoint:
        ckpt_path = Path(parsed.checkpoint)
        if not ckpt_path.is_file():
            print(f"ERROR: Checkpoint file not found: {ckpt_path}", file=sys.stderr)
            return 1

        print(f"Loading checkpoint from: {ckpt_path}")
        raw_ckpt = torch.load(str(ckpt_path), map_location="cpu", weights_only=False)
        m_cfg_dict = raw_ckpt.get("model_config", {})
        config = NovaConfig.from_dict(m_cfg_dict) if m_cfg_dict else NovaConfig()
        model = NovaForCausalLM(config).to(device)

        load_checkpoint(
            checkpoint_path=ckpt_path,
            model=model,
            device=device,
            verify_compatibility=True,
        )
        print(f"Successfully restored checkpoint from step {raw_ckpt.get('step', 'unknown')}.")
    else:
        print("Notice: No checkpoint specified; initializing model from default configuration.")
        config = NovaConfig(vocab_size=3384, max_seq_len=512, d_model=64, n_layers=2, n_heads=4, d_ff=176)
        model = NovaForCausalLM(config).to(device)

    model_params = sum(p.numel() for p in model.parameters())
    print(f"Model Parameters: {model_params:,} (vocab_size={model.config.vocab_size:,})")
    print(f"Evaluating validation data: {val_path}...")

    pad_id = getattr(model.config, "pad_token_id", 0)

    try:
        result = evaluate_model(
            model=model,
            val_data=val_path,
            device=device,
            batch_size=parsed.batch_size,
            pad_token_id=pad_id,
            manifest_path=manifest_path if manifest_path.is_file() else None,
        )
    except Exception as e:
        print(f"\nEVALUATION FAILED: {e}", file=sys.stderr)
        return 1

    print("\n" + result.summary())
    print("\n" + "=" * 75)
    print("[NOTE] Metric Interpretation:")
    print("The validation set comprises 5 documents from the frozen approved corpus.")
    print("Loss and perplexity reported here are strictly diagnostic indicators of mathematical")
    print("soundness, and do NOT imply real-world fitness competence.")
    print("=" * 75)

    return 0


if __name__ == "__main__":
    sys.exit(main())
