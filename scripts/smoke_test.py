#!/usr/bin/env python3
"""Nova-Fit Phase 0 CPU Smoke Test.

Validates that PyTorch runs correctly in a CPU-only environment by training
a tiny multi-layer perceptron (MLP) on synthetic regression data with fixed
random seeds and asserting that training strictly reduces the loss.

Constraints:
- CPU-only execution.
- Fixed random seeds for deterministic reproducibility.
- No pretrained models or external weights.
- Self-contained synthetic data generation.
"""

from __future__ import annotations

import sys
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
    message: str


class TinyRegressionModel(nn.Module):
    """A minimal 2-layer MLP for CPU sanity testing."""

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
    """Generate deterministic synthetic regression data on CPU."""
    generator = torch.Generator().manual_seed(seed)
    x = torch.randn(num_samples, in_features, generator=generator)
    # True weights for synthetic target: linear combination with slight noise
    true_weights = torch.linspace(0.5, 2.0, in_features).unsqueeze(1)
    noise = 0.05 * torch.randn(num_samples, 1, generator=generator)
    y = x @ true_weights + 0.3 + noise
    return x, y


def run_smoke_test(
    steps: int = 25,
    learning_rate: float = 0.05,
    seed: int = 42,
    verbose: bool = True,
) -> SmokeTestResult:
    """Execute the CPU smoke test.

    Args:
        steps: Number of optimization steps.
        learning_rate: Optimizer learning rate.
        seed: Random seed for reproducibility.
        verbose: Whether to print step-by-step progress.

    Returns:
        SmokeTestResult with metrics and success status.
    """
    # Enforce CPU execution and deterministic seeds
    device = torch.device("cpu")
    torch.manual_seed(seed)

    x, y = generate_synthetic_data(num_samples=128, in_features=8, seed=seed)
    x = x.to(device)
    y = y.to(device)

    model = TinyRegressionModel(in_features=8, hidden_features=16, out_features=1).to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    losses: List[float] = []

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

    initial_loss = losses[0]
    final_loss = losses[-1]
    loss_reduction = (initial_loss - final_loss) / initial_loss * 100.0

    # Verification criteria:
    # 1. Final loss must be strictly lower than initial loss.
    # 2. Must achieve at least a 50% relative reduction over 25 steps.
    is_reduced = final_loss < initial_loss
    has_meaningful_drop = loss_reduction >= 50.0
    success = is_reduced and has_meaningful_drop

    if success:
        msg = (
            f"Smoke test PASSED on {device}: loss decreased from "
            f"{initial_loss:.6f} to {final_loss:.6f} ({loss_reduction:.1f}% reduction)."
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
        device=str(device),
        message=msg,
    )


def main() -> None:
    print("=" * 64)
    print(" PROJECT NOVA-FIT : PHASE 0 CPU SMOKE TEST")
    print("=" * 64)
    print("Initializing CPU tensor operations and synthetic dataset...")

    result = run_smoke_test(steps=25, learning_rate=0.05, seed=42, verbose=True)

    print("\n" + result.message)
    print("=" * 64)

    if not result.success:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
