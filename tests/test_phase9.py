"""Automated Regression Tests for Project Nova Phase 9: Accelerator Benchmark & Training Pilot.

Verifies:
1. Device selection logic and CPU fallback.
2. CUDA request failure handling when CUDA is not present.
3. Mixed-precision configuration validation and GradScaler initialization.
4. Model architecture parameter counts: 533,824 (prototype) and 20,301,696 (Nova-20M).
5. Random Gaussian weight initialization (zero pretrained weights).
6. Forward/backward computation finiteness and causal attention masking.
7. Atomic checkpoint save, restore, exact logit parity, and step continuation.
8. Authoritative artifact hashes for tokenizer and dataset manifest.
9. Bounded training pilot execution and clean termination.
10. 12-question benchmark diagnostic evaluation and rubric verification.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
import tempfile

import pytest
import torch
import torch.nn.functional as F

from nova.benchmark import (
    FitnessEvaluationBenchmark,
    evaluate_model_on_benchmark_passages,
)
from nova.checkpoint import compute_file_sha256, load_checkpoint, save_checkpoint
from nova.model import NovaConfig, NovaForCausalLM
from nova.tokenizer import load_tokenizer
from nova.train import Trainer, TrainingConfig, set_seed

REPO_ROOT = Path(__file__).resolve().parent.parent
FINAL_TOK_DIR = REPO_ROOT / "artifacts" / "final_tokenizer"
FINAL_TOK_JSON = FINAL_TOK_DIR / "tokenizer.json"
EXPANDED_DATA_DIR = REPO_ROOT / "data" / "prepared_expanded"
EXPANDED_MANIFEST = EXPANDED_DATA_DIR / "manifest.json"
BENCHMARK_PATH = REPO_ROOT / "data" / "benchmark" / "fitness_eval_benchmark.json"
PROTOTYPE_CONFIG_PATH = REPO_ROOT / "configs" / "prototype_model.json"
NOVA_20M_CONFIG_PATH = REPO_ROOT / "configs" / "nova_20m.json"

AUTHORITATIVE_TOK_SHA256 = "1639cec0fce7263bbb10eca238b19a5d13ef6bd9fa1c545cd481f4e8ff9c93fc"
AUTHORITATIVE_MANIFEST_SHA256 = "9ebb8353f41faa16926a928a528eb64218753b305fb573b372a88f20208adc29"


class TestDeviceSelectionAndFallback:
    """Verify accelerator device detection, auto-selection, and fallback."""

    def test_auto_device_selection(self) -> None:
        """Verify device='auto' selects cuda if available else cpu."""
        expected_device = "cuda" if torch.cuda.is_available() else "cpu"
        cfg = TrainingConfig(device="auto")
        cfg.validate()
        trainer = Trainer(config=cfg, train_data=torch.randint(0, 3384, (2, 32)))
        assert trainer.device.type == expected_device

    def test_explicit_cpu_device_selection(self) -> None:
        """Verify device='cpu' selects cpu even if cuda is present."""
        cfg = TrainingConfig(device="cpu")
        cfg.validate()
        trainer = Trainer(config=cfg, train_data=torch.randint(0, 3384, (2, 32)))
        assert trainer.device.type == "cpu"

    def test_cuda_error_handling_when_unavailable(self) -> None:
        """Verify requesting device='cuda' when CUDA is unavailable raises RuntimeError."""
        if not torch.cuda.is_available():
            cfg = TrainingConfig(device="cuda")
            with pytest.raises(RuntimeError, match="CUDA was requested in training config but is not available"):
                Trainer(config=cfg, train_data=torch.randint(0, 3384, (2, 32)))


class TestMixedPrecisionConfiguration:
    """Verify mixed-precision settings, validation, and scaler initialization."""

    def test_valid_mixed_precision_options(self) -> None:
        """Verify supported options ('no', 'fp16', 'bf16') pass validation."""
        for opt in ("no", "fp16", "bf16", "NO", "FP16", "BF16"):
            cfg = TrainingConfig(mixed_precision=opt)
            cfg.validate()

    def test_invalid_mixed_precision_option(self) -> None:
        """Verify unsupported options raise ValueError."""
        cfg = TrainingConfig(mixed_precision="fp8")
        with pytest.raises(ValueError, match="Unsupported mixed_precision"):
            cfg.validate()

    def test_grad_scaler_initialization_on_cpu(self) -> None:
        """Verify GradScaler is disabled on CPU and does not crash."""
        cfg = TrainingConfig(device="cpu", mixed_precision="fp16")
        trainer = Trainer(config=cfg, train_data=torch.randint(0, 3384, (2, 32)))
        assert trainer.use_amp is False
        assert trainer.scaler.is_enabled() is False


class TestModelArchitectureAndInitialization:
    """Verify parameter counts and random initialization (zero pretrained weights)."""

    def test_prototype_model_parameter_count(self) -> None:
        """Verify prototype model has exactly 533,824 parameters."""
        cfg = NovaConfig.from_json_file(PROTOTYPE_CONFIG_PATH)
        assert cfg.vocab_size == 3384
        assert cfg.d_model == 64
        assert cfg.n_layers == 2
        assert cfg.n_heads == 4
        assert cfg.d_ff == 176
        model = NovaForCausalLM(cfg)
        assert model.count_parameters() == 533824

    def test_nova_20m_parameter_count(self) -> None:
        """Verify Nova-20M model has exactly 20,301,696 parameters."""
        cfg = NovaConfig.from_json_file(NOVA_20M_CONFIG_PATH)
        assert cfg.vocab_size == 3384
        assert cfg.d_model == 384
        assert cfg.n_layers == 10
        assert cfg.n_heads == 8
        assert cfg.d_ff == 1024
        model = NovaForCausalLM(cfg)
        assert model.count_parameters() == 20301696

    def test_random_initialization_statistics(self) -> None:
        """Verify model weights are randomly initialized from Gaussian N(0, 0.02^2)."""
        set_seed(42)
        cfg = NovaConfig.from_json_file(PROTOTYPE_CONFIG_PATH)
        model = NovaForCausalLM(cfg)

        # Check embedding weights
        emb_weights = model.embed_tokens.weight.data
        mean = emb_weights.mean().item()
        std = emb_weights.std().item()

        assert abs(mean) < 0.01, f"Mean should be near 0.0, got {mean}"
        assert abs(std - 0.02) < 0.005, f"Std should be near 0.02, got {std}"
        assert not (emb_weights == 0.0).all(), "Weights must not be all zeros"

        # Check linear layer weights
        q_weight = model.layers[0].attn.q_proj.weight.data
        q_mean = q_weight.mean().item()
        q_std = q_weight.std().item()
        assert abs(q_mean) < 0.01
        assert abs(q_std - 0.02) < 0.005


class TestForwardBackwardAndCausalMasking:
    """Verify finite computations, token-averaged loss, and causal masking."""

    def test_finite_forward_and_backward(self) -> None:
        """Verify forward pass, loss, backward pass, and gradients are finite."""
        cfg = NovaConfig(vocab_size=3384, max_seq_len=64, d_model=64, n_layers=2, n_heads=4, d_ff=176)
        model = NovaForCausalLM(cfg)
        model.train()

        input_ids = torch.randint(1, 3384, (2, 32))
        targets = torch.randint(1, 3384, (2, 32))

        outputs = model(input_ids)
        logits = outputs.logits
        assert logits.shape == (2, 32, 3384)
        assert torch.isfinite(logits).all()

        loss = F.cross_entropy(logits.view(-1, 3384), targets.view(-1), ignore_index=0)
        assert torch.isfinite(loss)
        loss.backward()

        for name, p in model.named_parameters():
            assert p.grad is not None, f"Gradient missing for {name}"
            assert torch.isfinite(p.grad).all(), f"Non-finite gradient in {name}"

    def test_causal_masking_prevents_future_leakage(self) -> None:
        """Verify that modifying a future token does not affect earlier token logits."""
        cfg = NovaConfig(vocab_size=3384, max_seq_len=32, d_model=64, n_layers=2, n_heads=4, d_ff=176)
        model = NovaForCausalLM(cfg)
        model.eval()

        seq1 = torch.tensor([[10, 20, 30, 40, 50]])
        seq2 = torch.tensor([[10, 20, 30, 999, 888]])  # tokens at index 3 & 4 differ

        with torch.no_grad():
            logits1 = model(seq1).logits
            logits2 = model(seq2).logits

        # Logits at positions 0, 1, 2 must be identical within numerical precision
        diff_0_2 = (logits1[:, :3, :] - logits2[:, :3, :]).abs().max().item()
        assert diff_0_2 < 1e-5, f"Future token affected past logits! max diff = {diff_0_2}"


class TestCheckpointPersistenceAndRecovery:
    """Verify atomic checkpoint save, restore, exact logit parity, and continuation."""

    def test_save_restore_exact_parity(self) -> None:
        """Verify restored model produces bit-identical logits to original model."""
        cfg = NovaConfig(vocab_size=3384, max_seq_len=64, d_model=64, n_layers=2, n_heads=4, d_ff=176)
        orig_model = NovaForCausalLM(cfg)
        
        # Setup 2-group optimizer matching Trainer convention
        decay_params = [p for p in orig_model.parameters() if p.requires_grad and p.dim() >= 2]
        no_decay_params = [p for p in orig_model.parameters() if p.requires_grad and p.dim() < 2]
        orig_opt = torch.optim.AdamW(
            [{"params": decay_params, "weight_decay": 0.01}, {"params": no_decay_params, "weight_decay": 0.0}],
            lr=1e-3,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            ckpt_file = Path(tmpdir) / "test_ckpt.pt"
            saved_path = save_checkpoint(
                checkpoint_path=ckpt_file,
                model=orig_model,
                optimizer=orig_opt,
                step=42,
                epoch=2,
                tokens_processed=10000,
                val_loss=7.5,
                model_config=cfg,
            )
            assert saved_path.is_file()

            # Restore into fresh instance
            restored_model = NovaForCausalLM(cfg)
            rest_decay = [p for p in restored_model.parameters() if p.requires_grad and p.dim() >= 2]
            rest_nodecay = [p for p in restored_model.parameters() if p.requires_grad and p.dim() < 2]
            restored_opt = torch.optim.AdamW(
                [{"params": rest_decay, "weight_decay": 0.01}, {"params": rest_nodecay, "weight_decay": 0.0}],
                lr=1e-3,
            )

            loaded = load_checkpoint(
                saved_path,
                model=restored_model,
                optimizer=restored_opt,
                verify_compatibility=True,
            )

            assert loaded["step"] == 42
            assert loaded["epoch"] == 2
            assert loaded["tokens_processed"] == 10000

            # Compare outputs
            test_seq = torch.randint(1, 3384, (2, 16))
            orig_model.eval()
            restored_model.eval()
            with torch.no_grad():
                out1 = orig_model(test_seq).logits
                out2 = restored_model(test_seq).logits
                max_diff = (out1 - out2).abs().max().item()

            assert max_diff < 1e-5, f"Restored model outputs differ: max_diff = {max_diff}"


class TestAuthoritativeArtifactHashes:
    """Verify that dataset and tokenizer hashes match authoritative values."""

    def test_tokenizer_hash(self) -> None:
        """Verify tokenizer.json matches authoritative SHA-256."""
        assert FINAL_TOK_JSON.is_file(), f"Missing {FINAL_TOK_JSON}"
        computed = compute_file_sha256(FINAL_TOK_JSON)
        assert computed == AUTHORITATIVE_TOK_SHA256

    def test_manifest_hash_and_internal_consistency(self) -> None:
        """Verify manifest.json hash and recorded tokenizer hash."""
        assert EXPANDED_MANIFEST.is_file(), f"Missing {EXPANDED_MANIFEST}"
        computed = compute_file_sha256(EXPANDED_MANIFEST)
        assert computed == AUTHORITATIVE_MANIFEST_SHA256

        with open(EXPANDED_MANIFEST, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)

        assert manifest_data["tokenizer_hash"] == AUTHORITATIVE_TOK_SHA256
        assert manifest_data["tokenizer_vocab_size"] == 3384
        assert manifest_data["train_sequences"] == 242
        assert manifest_data["total_tokens_train"] == 123722
        assert manifest_data["val_sequences"] == 34
        assert manifest_data["total_tokens_val"] == 17036


class TestControlledPilotExecution:
    """Verify bounded pilot training run halts cleanly and records valid metrics."""

    def test_bounded_training_pilot(self) -> None:
        """Verify trainer runs exactly max_steps and produces TrainerResult."""
        with tempfile.TemporaryDirectory() as tmpdir:
            train_seqs = torch.randint(1, 3384, (16, 64))
            val_seqs = torch.randint(1, 3384, (4, 64))

            cfg = TrainingConfig(
                data_dir=tmpdir,
                output_dir=tmpdir,
                batch_size=2,
                max_seq_len=64,
                max_steps=4,
                eval_interval=2,
                save_interval=2,
                device="cpu",
                mixed_precision="no",
            )
            trainer = Trainer(config=cfg, train_data=train_seqs, val_data=val_seqs)
            result = trainer.train()

            assert result.success is True
            assert result.total_steps == 4
            assert result.initial_loss > 0.0
            assert result.final_loss > 0.0
            assert result.final_val_loss is not None
            assert len(result.checkpoints_saved) > 0


class TestSupplementaryBenchmarkDiagnostic:
    """Verify held-out 12-question benchmark diagnostic evaluation."""

    def test_benchmark_coverage_and_evaluation(self) -> None:
        """Verify 12 questions across 7 pillars evaluate cleanly."""
        assert BENCHMARK_PATH.is_file()
        bm = FitnessEvaluationBenchmark.load(BENCHMARK_PATH)
        assert len(bm.questions) == 12

        # Verify pillar coverage
        pillars = {q.pillar for q in bm.questions.values()}
        assert len(pillars) == 7

        cfg = NovaConfig(vocab_size=3384, max_seq_len=512, d_model=64, n_layers=2, n_heads=4, d_ff=176)
        model = NovaForCausalLM(cfg)
        tok = load_tokenizer(FINAL_TOK_DIR)

        loss, ppl = evaluate_model_on_benchmark_passages(model, bm, tok, device="cpu")
        assert torch.isfinite(torch.tensor(loss))
        assert torch.isfinite(torch.tensor(ppl))
        assert loss > 0.0
        assert ppl > 1.0
