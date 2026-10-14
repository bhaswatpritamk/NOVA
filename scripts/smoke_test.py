#!/usr/bin/env python3
"""Nova-Fit Phase 0 Smoke Test.

Validates that PyTorch executes correctly by training a tiny multi-layer
perceptron (MLP) on synthetic regression data with fixed random seeds and
verifying that optimization strictly reduces the loss.

Design Principles:
- Provider-independent: Can run directly from a local terminal, bash shell, or Colab cell.
- Flexible compute targets: Defaults to CPU (suitable for local Phase 0 workstations),
  with optional CUDA / auto support when GPU accelerators are provisioned in Colab.
- Strict determinism: Controls generator seeds for reproducible training loss trajectories.
- Zero external dependencies: Relies solely on PyTorch and synthetic tensors.
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass
from typing import List, Tuple

import torch
import torch.nn as nn
import torch.optim as optim


@dataclass
class SmokeTestResult:
    """Summary of smoke test execution."""

    success: bool
    initial_loss: float
    final_loss: float
    loss_reduction_pct: float
    losses: List[float]
    device: str
    elapsed_time_sec: float
    steps_per_sec: float
    message: str


class TinyRegressionModel(nn.Module):
    """A minimal 2-layer MLP for compute and convergence sanity testing."""

    def __init__(self, in_features: int = 8, hidden_features: int = 16, out_features: int = 1):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, hidden_features),
            nn.ReLU(),
            nn.Linear(hidden_features, out_features),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def generate_synthetic_data(
    num_samples: int = 128, in_features: int = 8, seed: int = 42
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Generate deterministic synthetic regression data."""
    generator = torch.Generator().manual_seed(seed)
    x = torch.randn(num_samples, in_features, generator=generator)
    # True weights for synthetic target: linear combination with slight noise
    true_weights = torch.linspace(0.5, 2.0, in_features).unsqueeze(1)
    noise = 0.05 * torch.randn(num_samples, 1, generator=generator)
    y = x @ true_weights + 0.3 + noise
    return x, y


def resolve_device(device_choice: str) -> torch.device:
    """Resolve compute device string to a valid torch.device.

    Args:
        device_choice: 'cpu', 'cuda', or 'auto'. Defaults to 'cpu'.

    Returns:
        torch.device instance.
    """
    choice = device_choice.strip().lower()
    if choice == "auto":
        if torch.cuda.is_available():
            return torch.device("cuda")
        return torch.device("cpu")
    elif choice == "cuda":
        if not torch.cuda.is_available():
            raise RuntimeError(
                "CUDA was explicitly requested, but torch.cuda.is_available() is False. "
                "Ensure an NVIDIA GPU is allocated and CUDA drivers are active."
            )
        return torch.device("cuda")
    elif choice == "cpu":
        return torch.device("cpu")
    else:
        return torch.device(choice)


def run_smoke_test(
    steps: int = 25,
    learning_rate: float = 0.05,
    seed: int = 42,
    device_name: str = "cpu",
    verbose: bool = True,
) -> SmokeTestResult:
    """Execute the neural network training smoke test.

    Args:
        steps: Number of optimization steps.
        learning_rate: Optimizer learning rate.
        seed: Random seed for reproducibility.
        device_name: 'cpu', 'cuda', or 'auto'. Defaults to 'cpu'.
        verbose: Whether to print step-by-step progress.

    Returns:
        SmokeTestResult with metrics, timing, and success status.
    """
    device = resolve_device(device_name)

    # Seed all available devices for reproducibility
    torch.manual_seed(seed)
    if device.type == "cuda":
        torch.cuda.manual_seed_all(seed)

    x, y = generate_synthetic_data(num_samples=128, in_features=8, seed=seed)
    x = x.to(device)
    y = y.to(device)

    model = TinyRegressionModel(in_features=8, hidden_features=16, out_features=1).to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    losses: List[float] = []

    # Synchronize before timing if on CUDA
    if device.type == "cuda":
        torch.cuda.synchronize()
    start_time = time.perf_counter()

    for step in range(steps):
        optimizer.zero_grad()
        predictions = model(x)
        loss = criterion(predictions, y)
        loss_val = float(loss.item())
        losses.append(loss_val)

        loss.backward()
        optimizer.step()

        if verbose and (step == 0 or (step + 1) % 5 == 0 or step == steps - 1):
            print(f"  Step {step + 1:2d}/{steps} | Loss: {loss_val:.6f}")

    if device.type == "cuda":
        torch.cuda.synchronize()
    elapsed = time.perf_counter() - start_time
    steps_per_sec = steps / elapsed if elapsed > 0 else 0.0

    initial_loss = losses[0]
    final_loss = losses[-1]
    loss_reduction = (initial_loss - final_loss) / initial_loss * 100.0

    # Verification criteria:
    # 1. Final loss must be strictly lower than initial loss.
    # 2. Must achieve at least a 50% relative reduction over 25 steps.
    is_reduced = final_loss < initial_loss
    has_meaningful_drop = loss_reduction >= 50.0
    success = is_reduced and has_meaningful_drop

    device_label = str(device)
    if device.type == "cuda":
        device_label = f"cuda ({torch.cuda.get_device_name(0)})"

    if success:
        msg = (
            f"Smoke test PASSED on {device_label}: loss decreased from "
            f"{initial_loss:.6f} to {final_loss:.6f} ({loss_reduction:.1f}% reduction) "
            f"in {elapsed:.4f}s ({steps_per_sec:.1f} steps/s)."
        )
    else:
        msg = (
            f"Smoke test FAILED: initial_loss={initial_loss:.6f}, "
            f"final_loss={final_loss:.6f}, reduction={loss_reduction:.1f}%"
        )

    return SmokeTestResult(
        success=success,
        initial_loss=initial_loss,
        final_loss=final_loss,
        loss_reduction_pct=loss_reduction,
        losses=losses,
        device=str(device.type),
        elapsed_time_sec=elapsed,
        steps_per_sec=steps_per_sec,
        message=msg,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Nova-Fit Phase 0 Neural Network Smoke Test"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        choices=["cpu", "cuda", "auto"],
        help="Device to run smoke test on. Default is 'cpu' for Phase 0 local workstations.",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=25,
        help="Number of optimization steps (default: 25).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42).",
    )
    args = parser.parse_args()

    print("=" * 64)
    print(" PROJECT NOVA-FIT : PHASE 0 SMOKE TEST")
    print("=" * 64)
    print(f"Target Device: {args.device} | Steps: {args.steps} | Seed: {args.seed}")
    print("Initializing tensor operations and synthetic dataset...")

    try:
        result = run_smoke_test(
            steps=args.steps,
            learning_rate=0.05,
            seed=args.seed,
            device_name=args.device,
            verbose=True,
        )
        print("\n" + result.message)
        print("=" * 64)

        if not result.success:
            sys.exit(1)
        sys.exit(0)
    except Exception as exc:
        print(f"\nExecution ERROR: {exc}", file=sys.stderr)
        print("=" * 64)
        sys.exit(1)


if __name__ == "__main__":
    main()
