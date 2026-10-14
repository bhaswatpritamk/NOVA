#!/usr/bin/env python3
"""Nova-Fit Phase 2 Model Smoke Test.

Validates the tiny decoder-only Transformer implementation on CPU by:
1. Instantiating the model from configuration with random initialization.
2. Calculating and reporting the exact parameter count.
3. Verifying forward pass tensor shapes [batch_size, seq_len, vocab_size].
4. Verifying causal attention masking (future tokens cannot influence earlier outputs).
5. Running a controlled training experiment on synthetic token sequences to verify that
   gradients are finite, parameters update, and loss strictly decreases.
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import torch
import torch.optim as optim

# Ensure utf-8 stdout on Windows console
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from nova.model import NovaConfig, NovaForCausalLM


@dataclass
class ModelSmokeTestResult:
    """Summary of model smoke test execution metrics."""

    success: bool
    total_parameters: int
    trainable_parameters: int
    forward_logits_shape: List[int]
    causal_mask_passed: bool
    initial_loss: float
    final_loss: float
    loss_reduction_pct: float
    elapsed_time_sec: float
    steps_per_sec: float
    message: str


def run_model_smoke_test(
    config_path: Union[str, Path] = "configs/tiny_model.json",
    steps: int = 25,
    learning_rate: float = 0.02,
    seed: int = 42,
    device_name: str = "cpu",
    verbose: bool = True,
) -> ModelSmokeTestResult:
    """Execute complete model smoke test workflow."""
    torch.manual_seed(seed)
    device = torch.device(device_name)

    # 1. Load configuration
    cfg_path = Path(config_path)
    if cfg_path.is_file():
        config = NovaConfig.from_json_file(cfg_path)
    else:
        config = NovaConfig()

    if verbose:
        print("=" * 70)
        print("PROJECT NOVA-FIT : PHASE 2 TRANSFORMER SMOKE TEST")
        print("=" * 70)
        print(f"Target Device:      {device}")
        print(f"Random Seed:        {seed}")
        print(f"Vocab Size:         {config.vocab_size:,}")
        print(f"Context Length:     {config.max_seq_len} tokens")
        print(f"Layers (n_layers):  {config.n_layers}")
        print(f"Hidden Dim (d_model): {config.d_model}")
        print(f"Attention Heads:    {config.n_heads} (head_dim: {config.head_dim})")
        print(f"SwiGLU FFN Dim (d_ff): {config.d_ff}")
        print("-" * 70)

    # 2. Instantiate model and count parameters
    model = NovaForCausalLM(config).to(device)
    total_params = model.count_parameters(trainable_only=False)
    trainable_params = model.count_parameters(trainable_only=True)

    if verbose:
        print(f"Calculated Parameters: {total_params:,} (Trainable: {trainable_params:,})")

    # 3. Forward pass verification
    batch_size = 2
    seq_len = min(16, config.max_seq_len)
    synthetic_tokens = torch.randint(
        low=1,
        high=config.vocab_size,
        size=(batch_size, seq_len),
        device=device,
    )

    output = model(synthetic_tokens, targets=synthetic_tokens)
    logits_shape = list(output.logits.shape)
    expected_shape = [batch_size, seq_len, config.vocab_size]

    if logits_shape != expected_shape:
        return ModelSmokeTestResult(
            success=False,
            total_parameters=total_params,
            trainable_parameters=trainable_params,
            forward_logits_shape=logits_shape,
            causal_mask_passed=False,
            initial_loss=0.0,
            final_loss=0.0,
            loss_reduction_pct=0.0,
            elapsed_time_sec=0.0,
            steps_per_sec=0.0,
            message=f"Logits shape mismatch: expected {expected_shape}, got {logits_shape}",
        )

    if output.loss is None or not torch.isfinite(output.loss):
        return ModelSmokeTestResult(
            success=False,
            total_parameters=total_params,
            trainable_parameters=trainable_params,
            forward_logits_shape=logits_shape,
            causal_mask_passed=False,
            initial_loss=0.0,
            final_loss=0.0,
            loss_reduction_pct=0.0,
            elapsed_time_sec=0.0,
            steps_per_sec=0.0,
            message="Loss was not finite on initial forward pass.",
        )

    if verbose:
        print(f"Forward Pass Output: Logits shape = {logits_shape}, Initial loss = {output.loss.item():.4f}")

    # 4. Causal Attention Verification
    model.eval()
    with torch.no_grad():
        t1 = torch.tensor([[10, 25, 42, 88, 12]], device=device)
        t2 = torch.tensor([[10, 25, 42, 88, 99]], device=device)  # Only last token differs
        o1 = model(t1).logits
        o2 = model(t2).logits
        # Output for all positions before the last token must be strictly identical
        past_diff = (o1[:, :4, :] - o2[:, :4, :]).abs().max().item()
        causal_passed = past_diff < 1e-6

    if not causal_passed:
        return ModelSmokeTestResult(
            success=False,
            total_parameters=total_params,
            trainable_parameters=trainable_params,
            forward_logits_shape=logits_shape,
            causal_mask_passed=False,
            initial_loss=output.loss.item(),
            final_loss=0.0,
            loss_reduction_pct=0.0,
            elapsed_time_sec=0.0,
            steps_per_sec=0.0,
            message=f"Causal attention check failed: future token leaked to past (max diff: {past_diff}).",
        )

    if verbose:
        print(f"Causal Attention Check: PASSED (max discrepancy in past positions: {past_diff:.2e})")

    # 5. Controlled Training Experiment
    model.train()
    optimizer = optim.AdamW(model.parameters(), lr=learning_rate)

    # Fixed synthetic training sequence
    train_batch = torch.tensor(
        [
            [12, 45, 89, 102, 34, 56, 78, 91, 15, 28],
            [99, 14, 23, 77, 85, 92, 11, 40, 62, 83],
        ],
        device=device,
    )

    losses: List[float] = []
    initial_param_sample = model.embed_tokens.weight.data.clone()

    start_time = time.perf_counter()
    for step in range(1, steps + 1):
        optimizer.zero_grad()
        out = model(train_batch, targets=train_batch)
        loss = out.loss
        assert loss is not None

        loss.backward()

        # Check gradients are finite
        for name, param in model.named_parameters():
            if param.requires_grad:
                if param.grad is None or not torch.isfinite(param.grad).all():
                    return ModelSmokeTestResult(
                        success=False,
                        total_parameters=total_params,
                        trainable_parameters=trainable_params,
                        forward_logits_shape=logits_shape,
                        causal_mask_passed=True,
                        initial_loss=losses[0] if losses else 0.0,
                        final_loss=loss.item(),
                        loss_reduction_pct=0.0,
                        elapsed_time_sec=0.0,
                        steps_per_sec=0.0,
                        message=f"Non-finite gradients detected on parameter '{name}' at step {step}.",
                    )

        optimizer.step()
        loss_val = loss.item()
        losses.append(loss_val)

        if verbose and (step == 1 or step % 5 == 0 or step == steps):
            print(f"  Step {step:2d}/{steps} | Loss: {loss_val:.6f}")

    elapsed = time.perf_counter() - start_time
    steps_per_sec = steps / elapsed if elapsed > 0 else 0.0

    initial_loss = losses[0]
    final_loss = losses[-1]
    reduction_pct = ((initial_loss - final_loss) / initial_loss) * 100.0

    # Verify parameters changed
    param_changed = not torch.equal(initial_param_sample, model.embed_tokens.weight.data)
    if not param_changed:
        return ModelSmokeTestResult(
            success=False,
            total_parameters=total_params,
            trainable_parameters=trainable_params,
            forward_logits_shape=logits_shape,
            causal_mask_passed=True,
            initial_loss=initial_loss,
            final_loss=final_loss,
            loss_reduction_pct=reduction_pct,
            elapsed_time_sec=elapsed,
            steps_per_sec=steps_per_sec,
            message="Trainable parameters did not change after optimizer step.",
        )

    if final_loss >= initial_loss:
        return ModelSmokeTestResult(
            success=False,
            total_parameters=total_params,
            trainable_parameters=trainable_params,
            forward_logits_shape=logits_shape,
            causal_mask_passed=True,
            initial_loss=initial_loss,
            final_loss=final_loss,
            loss_reduction_pct=reduction_pct,
            elapsed_time_sec=elapsed,
            steps_per_sec=steps_per_sec,
            message=f"Loss failed to decrease: initial={initial_loss:.6f}, final={final_loss:.6f}",
        )

    success_msg = (
        f"Smoke test PASSED: Loss reduced from {initial_loss:.6f} to {final_loss:.6f} "
        f"({reduction_pct:.1f}% reduction) across {steps} steps in {elapsed:.3f}s ({steps_per_sec:.1f} steps/s)."
    )

    if verbose:
        print("-" * 70)
        print(success_msg)
        print("=" * 70)

    return ModelSmokeTestResult(
        success=True,
        total_parameters=total_params,
        trainable_parameters=trainable_params,
        forward_logits_shape=logits_shape,
        causal_mask_passed=True,
        initial_loss=initial_loss,
        final_loss=final_loss,
        loss_reduction_pct=reduction_pct,
        elapsed_time_sec=elapsed,
        steps_per_sec=steps_per_sec,
        message=success_msg,
    )


def main(cli_args: Optional[list[str]] = None) -> int:
    """CLI entrypoint for model smoke test."""
    parser = argparse.ArgumentParser(
        description="Nova-Fit Phase 2 Tiny Transformer Smoke Test.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--config",
        type=str,
        default="configs/tiny_model.json",
        help="Path to tiny model configuration JSON.",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=25,
        help="Number of optimization steps.",
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=0.02,
        help="Optimization learning rate.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Deterministic random seed.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        help="Compute device (cpu, cuda, auto).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress detailed console logging.",
    )

    args = parser.parse_args(cli_args)

    device_name = args.device.lower()
    if device_name == "auto":
        device_name = "cuda" if torch.cuda.is_available() else "cpu"

    result = run_model_smoke_test(
        config_path=args.config,
        steps=args.steps,
        learning_rate=args.learning_rate,
        seed=args.seed,
        device_name=device_name,
        verbose=not args.quiet,
    )

    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
