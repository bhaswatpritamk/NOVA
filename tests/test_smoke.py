"""Tests for Nova-Fit Phase 0 environment and smoke test.

Verifies:
1. PyTorch CPU smoke test executes without errors.
2. Loss strictly decreases and achieves required reduction threshold.
3. Random seed produces deterministic and reproducible training trajectories.
4. Environment diagnostics report generates valid non-empty metadata.
"""

from __future__ import annotations

import pytest

from scripts.environment_report import collect_environment_report
from scripts.smoke_test import run_smoke_test


def test_cpu_smoke_test_reduces_loss():
    """Verify that training the tiny model on synthetic data strictly reduces loss."""
    result = run_smoke_test(steps=25, learning_rate=0.05, seed=42, verbose=False)

    assert result.success is True, (
        f"Smoke test failed unexpectedly: {result.message} "
        f"(Initial Loss: {result.initial_loss:.6f}, Final Loss: {result.final_loss:.6f})"
    )
    assert result.final_loss < result.initial_loss, (
        f"Final loss ({result.final_loss}) was not strictly less than initial loss ({result.initial_loss})."
    )
    assert result.loss_reduction_pct >= 50.0, (
        f"Loss reduction was only {result.loss_reduction_pct:.2f}%, expected >= 50.0%."
    )
    assert result.device == "cpu", (
        f"Smoke test must run strictly on CPU, but reported device={result.device}."
    )


def test_smoke_test_determinism():
    """Verify that fixing the seed yields identical initial and final loss trajectories."""
    run1 = run_smoke_test(steps=15, learning_rate=0.05, seed=123, verbose=False)
    run2 = run_smoke_test(steps=15, learning_rate=0.05, seed=123, verbose=False)

    assert run1.initial_loss == pytest.approx(run2.initial_loss, rel=1e-6), (
        "Non-deterministic initial loss across identical seeds."
    )
    assert run1.final_loss == pytest.approx(run2.final_loss, rel=1e-6), (
        "Non-deterministic final loss across identical seeds."
    )
    assert len(run1.losses) == len(run2.losses)
    for i, (l1, l2) in enumerate(zip(run1.losses, run2.losses)):
        assert l1 == pytest.approx(l2, rel=1e-6), f"Trajectory divergence at step {i}: {l1} != {l2}"


def test_environment_report_fields():
    """Verify that environment_report returns all required system diagnosis fields."""
    report = collect_environment_report()

    required_keys = [
        "python_version",
        "executable_path",
        "os_system",
        "cpu_count_logical",
        "ram_total_human",
        "ram_available_human",
        "disk_free_human",
        "pytorch_installed",
        "pytorch_version",
        "cuda_available",
    ]

    missing_keys = [k for k in required_keys if k not in report]
    assert not missing_keys, f"Environment report is missing required keys: {missing_keys}"

    assert report["python_version"], "Python version cannot be empty"
    assert report["executable_path"], "Executable path cannot be empty"
    assert report["os_system"], "OS system cannot be empty"
    assert report["cpu_count_logical"] is not None and report["cpu_count_logical"] > 0
    assert report["pytorch_installed"] is True, "PyTorch must be reported as installed"
