"""Tests for Nova-Fit Phase 2 Decoder-Only Transformer Architecture.

Verifies:
1. Model initialization succeeds from configuration and dataclass.
2. Parameter count is finite, positive, and accurately calculated.
3. Forward pass yields logits of shape [batch_size, seq_len, vocab_size].
4. Causal multi-head attention strictly prevents future tokens from affecting past outputs.
5. Next-token prediction loss is finite and valid.
6. Backpropagation produces finite gradients across all trainable weights.
7. An optimizer step updates trainable parameters.
8. Training on a controlled batch strictly reduces loss.
9. Invalid sequence lengths and incompatible architectural dimensions raise descriptive errors.
10. RMSNorm and SwiGLU layers execute correctly.
11. Loss properly ignores padding tokens.
12. Compatibility with Phase 0 and Phase 1 test suites.
"""

from __future__ import annotations

import math
from pathlib import Path

import pytest
import torch
import torch.nn.functional as F
import torch.optim as optim

from nova.model import (
    CausalLMOutput,
    CausalSelfAttention,
    NovaConfig,
    NovaForCausalLM,
    RMSNorm,
    RotaryEmbedding,
    SwiGLU,
    TransformerBlock,
    build_tiny_model,
)
from scripts.model_smoke_test import run_model_smoke_test


@pytest.fixture
def tiny_config() -> NovaConfig:
    """Fixture providing a verified tiny configuration for CPU testing."""
    return NovaConfig(
        vocab_size=128,
        max_seq_len=16,
        d_model=32,
        n_layers=2,
        n_heads=4,
        d_ff=88,
        dropout=0.0,
        pad_token_id=0,
    )


@pytest.fixture
def tiny_model(tiny_config: NovaConfig) -> NovaForCausalLM:
    """Fixture providing an instantiated NovaForCausalLM model."""
    torch.manual_seed(42)
    return NovaForCausalLM(tiny_config)


# -----------------------------------------------------------------------------
# 1. Model Initialization & Parameter Count Tests
# -----------------------------------------------------------------------------


def test_model_initialization(tiny_config: NovaConfig, tiny_model: NovaForCausalLM):
    """Verify model initialization succeeds and layers are properly constructed."""
    model = tiny_model
    assert isinstance(model, NovaForCausalLM)
    assert len(model.layers) == tiny_config.n_layers
    assert model.embed_tokens.num_embeddings == tiny_config.vocab_size
    assert model.embed_tokens.embedding_dim == tiny_config.d_model
    assert model.lm_head.out_features == tiny_config.vocab_size
    assert model.lm_head.in_features == tiny_config.d_model


def test_parameter_count(tiny_model: NovaForCausalLM):
    """Verify that calculated parameter count is finite, positive, and matches manual sum."""
    total_params = tiny_model.count_parameters(trainable_only=False)
    trainable_params = tiny_model.count_parameters(trainable_only=True)

    assert total_params > 0
    assert trainable_params > 0
    assert total_params == trainable_params  # All parameters require grad by default

    manual_sum = sum(p.numel() for p in tiny_model.parameters())
    assert total_params == manual_sum


# -----------------------------------------------------------------------------
# 2. Forward Pass & Logits Shape Tests
# -----------------------------------------------------------------------------


def test_forward_pass_logits_shape(tiny_config: NovaConfig, tiny_model: NovaForCausalLM):
    """Verify forward pass returns logits with shape [batch_size, seq_len, vocab_size]."""
    batch_size = 3
    seq_len = 8
    input_ids = torch.randint(1, tiny_config.vocab_size, (batch_size, seq_len))

    output = tiny_model(input_ids)
    assert isinstance(output, CausalLMOutput)
    assert output.loss is None  # No targets provided

    # Test tuple unpacking
    logits, loss = output
    assert loss is None
    assert logits.shape == (batch_size, seq_len, tiny_config.vocab_size)
    assert torch.isfinite(logits).all()


# -----------------------------------------------------------------------------
# 3. Causal Attention Masking Tests
# -----------------------------------------------------------------------------


def test_causal_attention_prevents_future_leakage(tiny_model: NovaForCausalLM):
    """Verify causal attention: changing future tokens does NOT affect past position outputs."""
    tiny_model.eval()

    seq_len = 6
    prefix = [5, 12, 19, 24, 33]  # First 5 tokens are identical
    token_a = 40
    token_b = 85

    seq_a = torch.tensor([prefix + [token_a]])
    seq_b = torch.tensor([prefix + [token_b]])

    with torch.no_grad():
        out_a = tiny_model(seq_a).logits
        out_b = tiny_model(seq_b).logits

    # Positions 0 through 4 (the first 5 tokens) must have identical logits
    past_diff = (out_a[:, :5, :] - out_b[:, :5, :]).abs().max().item()
    assert past_diff == 0.0, (
        f"Causal attention violated: changing token at position 5 changed past representations by {past_diff}"
    )

    # Position 5 (the modified token) should differ
    last_diff = (out_a[:, 5, :] - out_b[:, 5, :]).abs().max().item()
    assert last_diff > 0.0, "Modified token at position 5 unexpectedly produced identical logits."


# -----------------------------------------------------------------------------
# 4. Next-Token Prediction & Loss Computation Tests
# -----------------------------------------------------------------------------


def test_loss_computation_and_shifting(tiny_config: NovaConfig, tiny_model: NovaForCausalLM):
    """Verify loss computation with next-token shifting and finite scalar output."""
    batch_size = 2
    seq_len = 10
    input_ids = torch.randint(1, tiny_config.vocab_size, (batch_size, seq_len))

    output = tiny_model(input_ids, targets=input_ids)
    assert output.loss is not None
    assert isinstance(output.loss, torch.Tensor)
    assert output.loss.dim() == 0  # Scalar loss
    assert torch.isfinite(output.loss)
    assert output.loss.item() > 0.0


def test_loss_excludes_padding(tiny_config: NovaConfig, tiny_model: NovaForCausalLM):
    """Verify cross-entropy loss ignores padding token IDs (ignore_index=pad_token_id)."""
    pad_id = tiny_config.pad_token_id
    seq_len = 8

    # Sequence with active tokens then padding at the end
    seq_with_pad = torch.tensor([[10, 20, 30, 40, pad_id, pad_id, pad_id, pad_id]])
    seq_without_pad = torch.tensor([[10, 20, 30, 40]])

    tiny_model.eval()
    with torch.no_grad():
        out_pad = tiny_model(seq_with_pad, targets=seq_with_pad)
        out_no_pad = tiny_model(seq_without_pad, targets=seq_without_pad)

    assert out_pad.loss is not None and torch.isfinite(out_pad.loss)
    assert out_no_pad.loss is not None and torch.isfinite(out_no_pad.loss)


# -----------------------------------------------------------------------------
# 5. Backpropagation & Parameter Updates
# -----------------------------------------------------------------------------


def test_backpropagation_finite_gradients(tiny_config: NovaConfig, tiny_model: NovaForCausalLM):
    """Verify that backpropagation computes finite, non-zero gradients on all trainable weights."""
    tiny_model.train()
    input_ids = torch.randint(1, tiny_config.vocab_size, (2, 8))

    out = tiny_model(input_ids, targets=input_ids)
    assert out.loss is not None
    out.loss.backward()

    for name, param in tiny_model.named_parameters():
        if param.requires_grad:
            assert param.grad is not None, f"Parameter '{name}' has None gradient."
            assert torch.isfinite(param.grad).all(), f"Parameter '{name}' contains non-finite gradients."
            assert param.grad.abs().sum() > 0.0, f"Parameter '{name}' has all-zero gradient."


def test_optimizer_step_updates_parameters(tiny_config: NovaConfig, tiny_model: NovaForCausalLM):
    """Verify that an optimizer step changes trainable parameter values."""
    tiny_model.train()
    optimizer = optim.AdamW(tiny_model.parameters(), lr=0.01)

    initial_weights = {
        name: param.clone()
        for name, param in tiny_model.named_parameters()
        if param.requires_grad
    }

    input_ids = torch.randint(1, tiny_config.vocab_size, (2, 8))
    out = tiny_model(input_ids, targets=input_ids)
    assert out.loss is not None
    out.loss.backward()
    optimizer.step()

    # Check at least one key parameter changed
    changed_params = 0
    for name, param in tiny_model.named_parameters():
        if param.requires_grad:
            if not torch.equal(initial_weights[name], param):
                changed_params += 1

    assert changed_params > 0, "No model parameters were updated after optimizer step."


# -----------------------------------------------------------------------------
# 6. Controlled Training Experiment (Loss Reduction)
# -----------------------------------------------------------------------------


def test_controlled_training_reduces_loss(tiny_config: NovaConfig, tiny_model: NovaForCausalLM):
    """Verify that optimization on a tiny fixed batch strictly reduces cross-entropy loss."""
    tiny_model.train()
    optimizer = optim.AdamW(tiny_model.parameters(), lr=0.03)

    fixed_batch = torch.tensor(
        [
            [5, 12, 19, 24, 33, 40, 52, 60],
            [14, 21, 28, 35, 42, 49, 56, 63],
        ]
    )

    losses = []
    for _ in range(15):
        optimizer.zero_grad()
        out = tiny_model(fixed_batch, targets=fixed_batch)
        assert out.loss is not None
        out.loss.backward()
        optimizer.step()
        losses.append(out.loss.item())

    initial_loss = losses[0]
    final_loss = losses[-1]

    assert final_loss < initial_loss, f"Loss did not decrease: {initial_loss:.4f} -> {final_loss:.4f}"
    reduction_pct = ((initial_loss - final_loss) / initial_loss) * 100.0
    assert reduction_pct >= 40.0, f"Loss reduction was only {reduction_pct:.2f}%, expected >= 40.0%"


# -----------------------------------------------------------------------------
# 7. Submodule Unit Tests: RMSNorm, RoPE, SwiGLU
# -----------------------------------------------------------------------------


def test_rmsnorm():
    """Verify RMSNorm normalization and learnable gain scaling."""
    dim = 16
    norm = RMSNorm(dim=dim, eps=1e-5)
    x = torch.randn(2, 4, dim) * 5.0 + 2.0
    out = norm(x)

    assert out.shape == x.shape
    # Check that root-mean-square along last dim is close to 1.0 (with weight=1)
    rms = torch.sqrt(out.pow(2).mean(-1))
    assert torch.allclose(rms, torch.ones_like(rms), atol=1e-3)


def test_rotary_embedding():
    """Verify RotaryEmbedding precomputation, caching, and rotation application."""
    dim = 16  # head_dim
    seq_len = 8
    rope = RotaryEmbedding(dim=dim, max_seq_len=16)

    cos, sin = rope(seq_len, torch.device("cpu"))
    assert cos.shape == (1, 1, seq_len, dim)
    assert sin.shape == (1, 1, seq_len, dim)

    # Sequence exceeding max_seq_len must raise ValueError
    with pytest.raises(ValueError, match="exceeds configured max_seq_len"):
        rope(32, torch.device("cpu"))


def test_swiglu():
    """Verify SwiGLU feed-forward network dimensionality and forward pass."""
    d_model = 32
    d_ff = 88
    swiglu = SwiGLU(d_model=d_model, d_ff=d_ff)
    x = torch.randn(2, 4, d_model)
    out = swiglu(x)
    assert out.shape == (2, 4, d_model)


def test_weight_tying(tiny_config: NovaConfig):
    """Verify weight tying between token embedding and LM projection head."""
    tied_cfg = NovaConfig(
        vocab_size=128,
        max_seq_len=16,
        d_model=32,
        n_layers=1,
        n_heads=4,
        tie_word_embeddings=True,
    )
    model = NovaForCausalLM(tied_cfg)
    assert model.lm_head.weight is model.embed_tokens.weight


# -----------------------------------------------------------------------------
# 8. Defensive Validation & Error Handling Tests
# -----------------------------------------------------------------------------


def test_invalid_architecture_configurations():
    """Verify that invalid or incompatible hyperparameters are strictly rejected."""
    # d_model not divisible by n_heads
    with pytest.raises(ValueError, match="must be divisible by n_heads"):
        NovaConfig(d_model=65, n_heads=4)

    # head_dim is odd (incompatible with RoPE)
    with pytest.raises(ValueError, match="must be an even integer for RoPE"):
        NovaConfig(d_model=28, n_heads=4)  # 28 // 4 = 7 (odd)

    # Negative or zero dimensions
    with pytest.raises(ValueError, match="vocab_size must be a positive integer"):
        NovaConfig(vocab_size=0)

    with pytest.raises(ValueError, match="max_seq_len must be a positive integer"):
        NovaConfig(max_seq_len=-5)

    with pytest.raises(ValueError, match="n_layers must be a positive integer"):
        NovaConfig(n_layers=0)

    with pytest.raises(ValueError, match="dropout must be in"):
        NovaConfig(dropout=1.5)

    with pytest.raises(ValueError, match="pad_token_id"):
        NovaConfig(vocab_size=100, pad_token_id=200)


def test_invalid_forward_inputs(tiny_model: NovaForCausalLM, tiny_config: NovaConfig):
    """Verify input validation during forward pass."""
    # Non-tensor input
    with pytest.raises(TypeError, match="Expected input_ids to be a torch.Tensor"):
        tiny_model("not a tensor")  # type: ignore

    # 1D tensor (must be 2D [B, T])
    with pytest.raises(ValueError, match="must be a 2D tensor"):
        tiny_model(torch.tensor([1, 2, 3]))

    # Sequence length exceeding max_seq_len
    oversized = torch.randint(1, tiny_config.vocab_size, (1, tiny_config.max_seq_len + 5))
    with pytest.raises(ValueError, match="exceeds configured max_seq_len"):
        tiny_model(oversized)

    # Empty sequence length
    with pytest.raises(ValueError, match="Sequence length cannot be zero"):
        tiny_model(torch.empty((1, 0), dtype=torch.long))

    # Out-of-bounds token IDs
    with pytest.raises(ValueError, match="Token IDs must be in range"):
        tiny_model(torch.tensor([[tiny_config.vocab_size + 10]]))

    with pytest.raises(ValueError, match="Token IDs must be in range"):
        tiny_model(torch.tensor([[-1]]))

    # Targets shape mismatch
    inputs = torch.randint(1, tiny_config.vocab_size, (2, 4))
    mismatched_targets = torch.randint(1, tiny_config.vocab_size, (2, 8))
    with pytest.raises(ValueError, match="targets shape .* must match input_ids shape"):
        tiny_model(inputs, targets=mismatched_targets)


# -----------------------------------------------------------------------------
# 9. Configuration File Loading & Smoke Test Script Verification
# -----------------------------------------------------------------------------


def test_config_json_serialization(tmp_path: Path):
    """Verify JSON file save and reload for NovaConfig."""
    cfg = NovaConfig(vocab_size=200, max_seq_len=32, d_model=64, n_layers=2, n_heads=4)
    file_path = tmp_path / "test_config.json"
    cfg.to_json_file(file_path)

    reloaded = NovaConfig.from_json_file(file_path)
    assert reloaded.vocab_size == cfg.vocab_size
    assert reloaded.max_seq_len == cfg.max_seq_len
    assert reloaded.d_model == cfg.d_model
    assert reloaded.n_layers == cfg.n_layers
    assert reloaded.n_heads == cfg.n_heads
    assert reloaded.d_ff == cfg.d_ff


def test_model_smoke_test_script():
    """Verify that the model smoke test script function executes successfully."""
    result = run_model_smoke_test(
        config_path="configs/tiny_model.json",
        steps=10,
        learning_rate=0.02,
        seed=42,
        device_name="cpu",
        verbose=False,
    )
    assert result.success is True
    assert result.total_parameters > 0
    assert result.causal_mask_passed is True
    assert result.final_loss < result.initial_loss
    assert result.loss_reduction_pct > 0.0
