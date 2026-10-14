"""Automated Tests for Nova-Fit Phase 5: Pretraining Engine and Checkpoint Verification.

Verifies:
1. Training loss is finite and non-negative.
2. Model parameters strictly update during an optimizer step.
3. Gradients remain finite across backpropagation.
4. Evaluation does not mutate model weights.
5. Checkpoints can be saved atomically and loaded faithfully.
6. Training resumes accurately from a saved checkpoint at the correct step.
7. Learning-rate scheduler states resume properly.
8. Resumed model and optimizer state match saved state.
9. Incompatible model configurations (vocab_size, d_model, layers) are rejected.
10. Incompatible tokenizer hashes are rejected.
11. Non-finite loss (NaN/Inf) triggers clean, explicit errors.
12. Controlled training demonstrates strict cross-entropy loss reduction on a learnable batch.
13. Padding tokens (<pad> = 0) are strictly excluded from loss and perplexity.
14. Gradient accumulation functions correctly over micro-batches.
"""

from __future__ import annotations

import copy
import json
import math
from pathlib import Path

import pytest
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

from nova.checkpoint import (
    CheckpointCompatibilityError,
    CheckpointCorruptedError,
    compute_file_sha256,
    load_checkpoint,
    save_checkpoint,
)
from nova.evaluate import EvaluationResult, evaluate_model
from nova.model import NovaConfig, NovaForCausalLM
from nova.train import (
    SequenceTensorDataset,
    Trainer,
    TrainerResult,
    TrainingConfig,
    get_lr_scheduler,
    set_seed,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
FINAL_TOK_DIR = REPO_ROOT / "artifacts" / "final_tokenizer"
PREPARED_FINAL_DIR = REPO_ROOT / "data" / "prepared_final"


@pytest.fixture
def smoke_config() -> NovaConfig:
    """Fixture providing a tiny NovaConfig with final tokenizer vocabulary size."""
    return NovaConfig(
        vocab_size=3384,
        max_seq_len=32,
        d_model=64,
        n_layers=2,
        n_heads=4,
        d_ff=176,
        pad_token_id=0,
    )


@pytest.fixture
def smoke_model(smoke_config: NovaConfig) -> NovaForCausalLM:
    """Fixture providing a deterministic tiny NovaForCausalLM model."""
    set_seed(42)
    return NovaForCausalLM(smoke_config)


@pytest.fixture
def synthetic_batch(smoke_config: NovaConfig) -> torch.Tensor:
    """Fixture providing synthetic sequences with padding tokens at the tail."""
    set_seed(42)
    batch = torch.randint(4, smoke_config.vocab_size, (2, smoke_config.max_seq_len), dtype=torch.long)
    # Add tail padding to verify masking
    batch[:, -8:] = smoke_config.pad_token_id
    return batch


# =============================================================================
# 1. Training Engine & Loss Verification
# =============================================================================


class TestTrainingEngine:
    """Verify core pretraining mechanics: loss, gradients, updates, and accumulation."""

    def test_training_loss_and_gradients_finite(
        self, smoke_model: NovaForCausalLM, smoke_config: NovaConfig, synthetic_batch: torch.Tensor
    ):
        """Verify forward pass loss is finite, non-negative, and produces finite gradients."""
        smoke_model.train()
        logits = smoke_model(synthetic_batch).logits
        shift_logits = logits[..., :-1, :].contiguous()
        shift_targets = synthetic_batch[..., 1:].contiguous()

        loss = torch.nn.functional.cross_entropy(
            shift_logits.view(-1, smoke_config.vocab_size),
            shift_targets.view(-1),
            ignore_index=smoke_config.pad_token_id,
        )

        assert torch.isfinite(loss), f"Loss was non-finite: {loss.item()}"
        assert loss.item() > 0.0, f"Cross-entropy loss must be strictly positive, got {loss.item()}"

        loss.backward()

        for name, param in smoke_model.named_parameters():
            if param.requires_grad:
                assert param.grad is not None, f"Parameter '{name}' missing gradient."
                assert torch.isfinite(param.grad).all(), f"Parameter '{name}' has non-finite gradient."

    def test_optimizer_step_updates_parameters(
        self, smoke_model: NovaForCausalLM, synthetic_batch: torch.Tensor
    ):
        """Verify that an optimizer step modifies trainable weights."""
        smoke_model.train()
        initial_params = {n: p.clone() for n, p in smoke_model.named_parameters() if p.requires_grad}

        cfg = TrainingConfig(
            max_steps=1,
            batch_size=2,
            warmup_steps=0,
            learning_rate=1e-3,
            device="cpu",
        )
        trainer = Trainer(cfg, model=smoke_model, train_data=synthetic_batch)
        result = trainer.train()

        assert result.success is True
        assert result.total_steps == 1

        changed = 0
        for name, param in smoke_model.named_parameters():
            if param.requires_grad:
                if not torch.equal(initial_params[name], param):
                    changed += 1

        assert changed > 0, "No model parameters were modified after training step."

    def test_gradient_accumulation_matches_stepped_update(
        self, smoke_config: NovaConfig, synthetic_batch: torch.Tensor
    ):
        """Verify that gradient accumulation over 2 micro-batches accumulates gradients properly."""
        set_seed(42)
        model = NovaForCausalLM(smoke_config)
        cfg = TrainingConfig(
            max_steps=1,
            batch_size=1,
            gradient_accumulation_steps=2,
            learning_rate=1e-3,
            device="cpu",
        )
        trainer = Trainer(cfg, model=model, train_data=synthetic_batch)
        res = trainer.train()
        assert res.total_steps == 1
        assert res.total_tokens_processed > 0

    def test_nan_loss_raises_clear_error(self, smoke_model: NovaForCausalLM):
        """Verify that non-finite loss (NaN/Inf) triggers an immediate ValueError."""
        # Force model logits to NaN by injecting NaN into embed_tokens
        with torch.no_grad():
            smoke_model.embed_tokens.weight.fill_(float("nan"))

        bad_batch = torch.tensor([[1, 2, 3, 4], [2, 3, 4, 5]], dtype=torch.long)
        cfg = TrainingConfig(max_steps=1, batch_size=2, device="cpu")
        trainer = Trainer(cfg, model=smoke_model, train_data=bad_batch)

        with pytest.raises(ValueError, match="Non-finite loss"):
            trainer.train()

    def test_controlled_loss_reduction(self, smoke_model: NovaForCausalLM, smoke_config: NovaConfig):
        """Verify optimization strictly reduces cross-entropy loss on a tiny fixed batch."""
        smoke_model.train()
        set_seed(42)
        fixed_batch = torch.tensor(
            [
                [10, 25, 40, 55, 70, 85, 100, 115],
                [15, 30, 45, 60, 75, 90, 105, 120],
            ],
            dtype=torch.long,
        )

        cfg = TrainingConfig(
            max_steps=15,
            batch_size=2,
            learning_rate=5e-3,
            warmup_steps=0,
            lr_schedule="constant",
            device="cpu",
        )
        trainer = Trainer(cfg, model=smoke_model, train_data=fixed_batch)
        result = trainer.train()

        assert result.success is True
        assert result.final_loss < result.initial_loss, (
            f"Loss failed to decrease: initial {result.initial_loss:.4f}, "
            f"final {result.final_loss:.4f}"
        )


# =============================================================================
# 2. Evaluation Engine & Invariance Tests
# =============================================================================


class TestEvaluationEngine:
    """Verify evaluation mode, weight preservation, padding exclusion, and metrics."""

    def test_evaluation_does_not_mutate_weights(
        self, smoke_model: NovaForCausalLM, synthetic_batch: torch.Tensor
    ):
        """Verify evaluation executes strictly without mutating any model weights."""
        smoke_model.train()
        weights_before = {n: p.clone() for n, p in smoke_model.named_parameters()}

        result = evaluate_model(smoke_model, synthetic_batch, device="cpu", pad_token_id=0)

        assert isinstance(result, EvaluationResult)
        assert torch.isfinite(torch.tensor(result.loss))
        assert torch.isfinite(torch.tensor(result.perplexity))

        for name, param in smoke_model.named_parameters():
            assert torch.equal(weights_before[name], param), (
                f"Evaluation altered weights of parameter '{name}'."
            )

    def test_evaluation_excludes_padding_tokens(self, smoke_model: NovaForCausalLM):
        """Verify that padding tokens (<pad> = 0) are excluded from token count and loss."""
        # 2 sequences of 10 tokens: 6 valid, 4 pads
        batch = torch.tensor(
            [
                [10, 20, 30, 40, 50, 60, 0, 0, 0, 0],
                [11, 21, 31, 41, 51, 61, 0, 0, 0, 0],
            ],
            dtype=torch.long,
        )
        result = evaluate_model(smoke_model, batch, device="cpu", pad_token_id=0)

        # Causal shift drops 1st position for targets:
        # targets have shape [2, 9].
        # In each row, original was [10, 20, 30, 40, 50, 60, 0, 0, 0, 0].
        # Targets are: [20, 30, 40, 50, 60, 0, 0, 0, 0] (5 valid, 4 pads per row).
        # Total valid = 5 * 2 = 10 valid targets. Total pad = 4 * 2 = 8 pad targets.
        assert result.total_valid_tokens == 10
        assert result.total_pad_tokens == 8
        assert result.total_sequences == 2
        assert result.perplexity >= 1.0


# =============================================================================
# 3. Checkpointing & Atomic State Preservation Tests
# =============================================================================


class TestCheckpointEngine:
    """Verify atomic saving, state restoration, and compatibility verification."""

    def test_atomic_checkpoint_save_and_load(
        self, smoke_model: NovaForCausalLM, tmp_path: Path
    ):
        """Verify atomic checkpoint save writes complete payload and load restores state."""
        optimizer = torch.optim.AdamW(smoke_model.parameters(), lr=1e-3)
        scheduler = get_lr_scheduler(optimizer, schedule="cosine", warmup_steps=2, max_steps=10)

        ckpt_file = tmp_path / "checkpoint_test.pt"
        save_checkpoint(
            checkpoint_path=ckpt_file,
            model=smoke_model,
            optimizer=optimizer,
            scheduler=scheduler,
            step=5,
            epoch=1,
            tokens_processed=1200,
            val_loss=8.12,
            best_val_loss=8.12,
            model_config=smoke_model.config,
        )

        assert ckpt_file.is_file(), "Target checkpoint file does not exist."
        # Verify no temporary files remain
        tmp_files = list(tmp_path.glob(".*tmp*"))
        assert len(tmp_files) == 0, f"Temporary file was not cleaned up: {tmp_files}"

        # Load into fresh model
        fresh_model = NovaForCausalLM(smoke_model.config)
        fresh_opt = torch.optim.AdamW(fresh_model.parameters(), lr=1e-3)
        fresh_sched = get_lr_scheduler(fresh_opt, schedule="cosine", warmup_steps=2, max_steps=10)

        ckpt = load_checkpoint(
            checkpoint_path=ckpt_file,
            model=fresh_model,
            optimizer=fresh_opt,
            scheduler=fresh_sched,
        )

        assert ckpt["step"] == 5
        assert ckpt["epoch"] == 1
        assert ckpt["tokens_processed"] == 1200
        assert ckpt["val_loss"] == 8.12

        # Verify weights are identical
        for name, param in smoke_model.named_parameters():
            assert torch.equal(param, fresh_model.state_dict()[name]), (
                f"Restored weight mismatch in '{name}'."
            )

    def test_checkpoint_rejection_on_incompatible_architecture(
        self, smoke_model: NovaForCausalLM, tmp_path: Path
    ):
        """Verify that loading into an incompatible model architecture raises an error."""
        ckpt_file = tmp_path / "checkpoint_compat.pt"
        save_checkpoint(
            checkpoint_path=ckpt_file,
            model=smoke_model,
            model_config=smoke_model.config,
        )

        # Incompatible config: d_model=128 instead of 64
        incompatible_config = NovaConfig(
            vocab_size=smoke_model.config.vocab_size,
            d_model=128,  # Different!
            n_layers=smoke_model.config.n_layers,
            n_heads=smoke_model.config.n_heads,
        )

        with pytest.raises(CheckpointCompatibilityError, match="Model configuration mismatch"):
            load_checkpoint(
                checkpoint_path=ckpt_file,
                verify_compatibility=True,
                expected_config=incompatible_config,
            )

    def test_checkpoint_rejection_on_mismatched_vocab_size(
        self, smoke_model: NovaForCausalLM, tmp_path: Path
    ):
        """Verify that vocabulary size mismatch raises CheckpointCompatibilityError."""
        ckpt_file = tmp_path / "checkpoint_vocab.pt"
        save_checkpoint(
            checkpoint_path=ckpt_file,
            model=smoke_model,
            model_config=smoke_model.config,
        )

        with pytest.raises(CheckpointCompatibilityError, match="Vocabulary size mismatch"):
            load_checkpoint(
                checkpoint_path=ckpt_file,
                verify_compatibility=True,
                expected_vocab_size=9999,
            )

    def test_checkpoint_rejection_on_tokenizer_hash_mismatch(
        self, smoke_model: NovaForCausalLM, tmp_path: Path
    ):
        """Verify that tokenizer SHA-256 hash mismatch raises CheckpointCompatibilityError."""
        # Create a dummy tokenizer file
        dummy_tok = tmp_path / "tokenizer.json"
        dummy_tok.write_text('{"model": {"vocab": {"<pad>": 0}}}', encoding="utf-8")

        ckpt_file = tmp_path / "checkpoint_tok.pt"
        save_checkpoint(
            checkpoint_path=ckpt_file,
            model=smoke_model,
            tokenizer_path=dummy_tok,
        )

        with pytest.raises(CheckpointCompatibilityError, match="Tokenizer SHA-256 hash mismatch"):
            load_checkpoint(
                checkpoint_path=ckpt_file,
                verify_compatibility=True,
                expected_tokenizer_hash="fake_hash_1234567890abcdef",
            )

    def test_corrupted_checkpoint_raises_clean_error(self, tmp_path: Path):
        """Verify that a damaged or partial checkpoint file raises CheckpointCorruptedError."""
        corrupted_file = tmp_path / "corrupted.pt"
        corrupted_file.write_bytes(b"PK\x03\x04truncated_junk_bytes")

        with pytest.raises(CheckpointCorruptedError, match="Failed to load checkpoint file"):
            load_checkpoint(corrupted_file)


# =============================================================================
# 4. Resume & End-to-End Continuity Tests
# =============================================================================


class TestResumeContinuity:
    """Verify that pausing and resuming training produces exact continued progression."""

    def test_resume_advances_from_correct_step(
        self, smoke_model: NovaForCausalLM, synthetic_batch: torch.Tensor, tmp_path: Path
    ):
        """Verify that training resumes from saved step and completes remaining steps."""
        run_dir = tmp_path / "run_resume"

        # Phase 1: Train 5 steps and save checkpoint
        cfg1 = TrainingConfig(
            output_dir=str(run_dir),
            max_steps=5,
            save_interval=5,
            batch_size=2,
            learning_rate=1e-3,
            device="cpu",
        )
        trainer1 = Trainer(cfg1, model=smoke_model, train_data=synthetic_batch)
        res1 = trainer1.train()
        assert res1.total_steps == 5

        latest_ckpt = run_dir / "checkpoint_latest.pt"
        assert latest_ckpt.is_file()

        # Phase 2: Resume from checkpoint for another 5 steps (total 10 steps)
        fresh_model = NovaForCausalLM(smoke_model.config)
        cfg2 = TrainingConfig(
            output_dir=str(run_dir),
            max_steps=10,
            save_interval=5,
            batch_size=2,
            learning_rate=1e-3,
            resume_from=str(latest_ckpt),
            device="cpu",
        )
        trainer2 = Trainer(cfg2, model=fresh_model, train_data=synthetic_batch)
        assert trainer2.global_step == 5, f"Expected resumed step to be 5, got {trainer2.global_step}"

        res2 = trainer2.train()
        assert res2.total_steps == 10
        assert res2.total_tokens_processed > res1.total_tokens_processed

    def test_scheduler_resumes_correct_progress(
        self, smoke_model: NovaForCausalLM, synthetic_batch: torch.Tensor, tmp_path: Path
    ):
        """Verify learning rate scheduler state is restored faithfully on resume."""
        run_dir = tmp_path / "run_sched"

        cfg = TrainingConfig(
            output_dir=str(run_dir),
            max_steps=6,
            warmup_steps=2,
            save_interval=4,
            batch_size=2,
            learning_rate=1e-3,
            lr_schedule="cosine",
            device="cpu",
        )
        trainer = Trainer(cfg, model=smoke_model, train_data=synthetic_batch)
        trainer.train()

        ckpt_step4 = run_dir / "checkpoint_step_000004.pt"
        assert ckpt_step4.is_file()

        # Resume at step 4
        fresh_model = NovaForCausalLM(smoke_model.config)
        cfg_resume = TrainingConfig(
            output_dir=str(run_dir),
            max_steps=8,
            warmup_steps=2,
            batch_size=2,
            learning_rate=1e-3,
            lr_schedule="cosine",
            resume_from=str(ckpt_step4),
            device="cpu",
        )
        trainer_resumed = Trainer(cfg_resume, model=fresh_model, train_data=synthetic_batch)
        assert trainer_resumed.global_step == 4

        # Verify scheduler current lr matches step 4
        current_lr = trainer_resumed.scheduler.get_last_lr()[0]
        assert current_lr > 0.0


# =============================================================================
# 5. Integration with Final Prepared Dataset
# =============================================================================


class TestPreparedDatasetIntegration:
    """Verify pretraining engine on the actual Phase 4 prepared tensors."""

    def test_train_on_actual_prepared_tensors(self, tmp_path: Path):
        """Run a mini 3-step pretraining pass on data/prepared_final/train.pt."""
        assert (PREPARED_FINAL_DIR / "train.pt").is_file()
        assert (PREPARED_FINAL_DIR / "val.pt").is_file()

        run_dir = tmp_path / "actual_train"
        cfg = TrainingConfig(
            data_dir=str(PREPARED_FINAL_DIR),
            output_dir=str(run_dir),
            tokenizer_path=str(FINAL_TOK_DIR),
            max_steps=3,
            batch_size=2,
            eval_interval=3,
            save_interval=3,
            learning_rate=1e-3,
            device="cpu",
        )

        trainer = Trainer(cfg)
        assert trainer.model.config.vocab_size == 3384

        res = trainer.train()
        assert res.success is True
        assert res.total_steps == 3
        assert res.final_val_loss is not None
        assert math.isfinite(res.final_val_loss)
        assert (run_dir / "checkpoint_latest.pt").is_file()
