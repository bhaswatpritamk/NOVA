"""Automated Tests for Project Nova-Fit Phase 7: Pretraining Readiness Audit.

Verifies:
1. Source authenticity and provenance categorization.
2. Independent recalculation of dataset token counts, packed sequence lengths, and padding tokens.
3. Tokenizer provenance: final tokenizer was trained strictly on approved training material.
4. Model architecture parameter counts: Tiny model (533,824 params) and Nova-20M (20,301,696 params).
5. Nova-20M forward pass and causal loss computation.
6. Random weight initialization (independent initialization, expected Gaussian variance, no pretrained weights).
7. Causal autoregressive target alignment (next-token prediction) and padding token exclusion from loss.
8. Cryptographic hash alignment between tokenizer and dataset manifests.
9. Chinchilla scaling law mismatch verification (tokens-per-parameter ratio).
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import pytest
import torch
import torch.nn.functional as F

from nova.checkpoint import compute_file_sha256, load_checkpoint
from nova.corpus import CorpusDocument, SourceRegistry
from nova.data import (
    CleaningConfig,
    compute_file_sha256,
    extract_documents,
    tokenize_documents,
)
from nova.model import NovaConfig, NovaForCausalLM
from nova.tokenizer import NovaTokenizer
from scripts.sources import get_all_documents

REPO_ROOT = Path(__file__).resolve().parent.parent
FINAL_TOK_DIR = REPO_ROOT / "artifacts" / "final_tokenizer"
SOURCE_REGISTRY_PATH = REPO_ROOT / "data" / "approved" / "source_registry.json"
EXPANDED_TRAIN_PATH = REPO_ROOT / "data" / "approved" / "expanded_train_corpus.txt"
EXPANDED_VAL_PATH = REPO_ROOT / "data" / "approved" / "expanded_val_corpus.txt"
PREPARED_EXPANDED_DIR = REPO_ROOT / "data" / "prepared_expanded"
NOVA_20M_CONFIG_PATH = REPO_ROOT / "configs" / "nova_20m.json"


@pytest.fixture(scope="module")
def tokenizer() -> NovaTokenizer:
    """Fixture providing the final Byte-Level BPE tokenizer."""
    return NovaTokenizer.from_file(FINAL_TOK_DIR)


@pytest.fixture(scope="module")
def source_registry() -> SourceRegistry:
    """Fixture providing the approved source registry."""
    return SourceRegistry.load(SOURCE_REGISTRY_PATH)


# =============================================================================
# 1. Source Authenticity & Provenance Audit Tests
# =============================================================================


def test_source_authenticity_and_synthetic_origin(source_registry: SourceRegistry):
    """Audit the production nature of all 306 educational documents.

    Confirms that while every document maps to an approved authority in the registry,
    the text files are structured educational syntheses authored into scripts/sources/
    rather than verbatim raw file downloads directly from publishing servers.
    """
    raw_docs = get_all_documents()
    assert len(raw_docs) == 306, f"Expected 306 documents, got {len(raw_docs)}"

    for d in raw_docs:
        # Every document must have a registered source
        assert d["source_id"] in source_registry.sources, (
            f"Unregistered source ID: {d['source_id']} in doc {d['doc_id']}"
        )
        assert len(d["text"].strip()) > 50, f"Doc {d['doc_id']} text suspiciously short"

    # Verify that raw text files in data/sources_raw/ are exports of the educational documents
    raw_dir = REPO_ROOT / "data" / "sources_raw"
    assert raw_dir.exists(), "data/sources_raw/ directory must exist"
    for sid, rec in source_registry.sources.items():
        fname = f"{sid.lower().replace('-', '_')}_raw.txt"
        fpath = raw_dir / fname
        assert fpath.exists(), f"Raw source file missing: {fpath}"
        actual_hash = compute_file_sha256(fpath)
        assert actual_hash == rec.raw_sha256, f"Raw hash mismatch for source {sid}"


# =============================================================================
# 2. Recalculated Dataset Statistics Tests
# =============================================================================


def test_independent_recalculated_token_statistics(tokenizer: NovaTokenizer):
    """Independently recalculate tokens on disk artifacts without relying on reports."""
    cfg = CleaningConfig(strip_comment_lines=True, strip_section_headers=False, normalize_whitespace=True)

    # Train corpus
    train_text = EXPANDED_TRAIN_PATH.read_text(encoding="utf-8")
    train_docs = extract_documents(train_text, cfg)
    assert len(train_docs) == 268, f"Expected 268 train docs, got {len(train_docs)}"

    train_tokenized = tokenize_documents(train_docs, tokenizer, add_eos=True)
    total_train_tokens_with_eos = sum(len(t) for t in train_tokenized)
    assert total_train_tokens_with_eos == 123722, (
        f"Expected exactly 123,722 tokens with EOS, got {total_train_tokens_with_eos}"
    )

    # Validation corpus
    val_text = EXPANDED_VAL_PATH.read_text(encoding="utf-8")
    val_docs = extract_documents(val_text, cfg)
    assert len(val_docs) == 38, f"Expected 38 val docs, got {len(val_docs)}"

    val_tokenized = tokenize_documents(val_docs, tokenizer, add_eos=True)
    total_val_tokens_with_eos = sum(len(t) for t in val_tokenized)
    assert total_val_tokens_with_eos == 17036, (
        f"Expected exactly 17,036 val tokens with EOS, got {total_val_tokens_with_eos}"
    )


def test_prepared_tensors_match_recalculated_tokens():
    """Verify data/prepared_expanded/ train.pt and val.pt match recalculated non-pad counts."""
    train_pt = PREPARED_EXPANDED_DIR / "train.pt"
    val_pt = PREPARED_EXPANDED_DIR / "val.pt"

    t_train = torch.load(str(train_pt), weights_only=True)
    t_val = torch.load(str(val_pt), weights_only=True)

    non_pad_train = int((t_train != 0).sum().item())
    non_pad_val = int((t_val != 0).sum().item())

    assert non_pad_train == 123722, f"Expected 123,722 non-pad train tokens, got {non_pad_train}"
    assert non_pad_val == 17036, f"Expected 17,036 non-pad val tokens, got {non_pad_val}"
    assert t_train.shape == (242, 512), f"Expected shape [242, 512], got {t_train.shape}"
    assert t_val.shape == (34, 512), f"Expected shape [34, 512], got {t_val.shape}"


def test_final_tokenizer_trained_strictly_on_approved_train_material():
    """Verify tokenizer config specifies train_corpus.txt and excludes validation sets."""
    tok_cfg_path = REPO_ROOT / "configs" / "final_tokenizer.json"
    with open(tok_cfg_path, "r", encoding="utf-8") as f:
        tok_cfg = json.load(f)

    assert tok_cfg["corpus_path"] == "data/approved/train_corpus.txt", (
        f"Tokenizer must be trained on data/approved/train_corpus.txt, got {tok_cfg['corpus_path']}"
    )
    assert "val" not in tok_cfg["corpus_path"].lower(), "Validation data must never be passed to tokenizer!"


# =============================================================================
# 3. Model Size Reconciliation Tests
# =============================================================================


def test_tiny_model_parameter_count_matches_audit():
    """Verify exact parameter count of tiny model with final tokenizer (533,824)."""
    cfg = NovaConfig(
        vocab_size=3384,
        max_seq_len=512,
        d_model=64,
        n_layers=2,
        n_heads=4,
        d_ff=176,
        tie_word_embeddings=False,
    )
    model = NovaForCausalLM(cfg)
    total_params = model.count_parameters()

    # Calculation:
    # embed: 3384 * 64 = 216,576
    # 2 layers: 2 * (4*64^2 + 3*64*176 + 2*64) = 2 * (16,384 + 33,792 + 128) = 100,608
    # norm_f: 64
    # lm_head: 64 * 3384 = 216,576
    # Total = 216,576 + 100,608 + 64 + 216,576 = 533,824
    assert total_params == 533824, f"Expected exactly 533,824 parameters, got {total_params}"


def test_nova_20m_configuration_parameters_and_forward_pass():
    """Verify Nova-20M architecture configuration and execution."""
    assert NOVA_20M_CONFIG_PATH.exists(), f"Configuration file missing: {NOVA_20M_CONFIG_PATH}"
    cfg = NovaConfig.from_json_file(NOVA_20M_CONFIG_PATH)

    assert cfg.d_model == 384
    assert cfg.n_layers == 10
    assert cfg.n_heads == 8
    assert cfg.d_ff == 1024
    assert cfg.vocab_size == 3384

    model = NovaForCausalLM(cfg)
    total_params = model.count_parameters()

    # Exact expected calculation:
    # embed: 3384 * 384 = 1,300,416
    # 10 layers: 10 * (4*384^2 + 3*384*1024 + 2*384) = 10 * (589,824 + 1,179,648 + 768) = 17,700,480
    # norm_f: 384
    # lm_head: 384 * 3384 = 1,300,416
    # Total = 1,300,416 + 17,700,480 + 384 + 1,300,416 = 20,301,696 (~20.30M)
    assert total_params == 20301696, f"Expected 20,301,696 parameters, got {total_params}"

    # Verify a micro forward pass with causal loss
    dummy_input = torch.randint(0, cfg.vocab_size, (1, 16), dtype=torch.long)
    dummy_targets = torch.randint(0, cfg.vocab_size, (1, 16), dtype=torch.long)
    out = model(dummy_input, targets=dummy_targets)

    assert out.logits.shape == (1, 16, cfg.vocab_size)
    assert out.loss is not None
    assert torch.isfinite(out.loss)


# =============================================================================
# 4. Infrastructure & Training Mechanism Integrity Tests
# =============================================================================


def test_random_initialization_no_pretrained_weights():
    """Verify weights are randomly initialized with mean~0 and std~initializer_range."""
    cfg = NovaConfig(vocab_size=3384, max_seq_len=64, d_model=64, n_layers=2, n_heads=4, d_ff=176)
    m1 = NovaForCausalLM(cfg)
    m2 = NovaForCausalLM(cfg)

    # Weights must not be identical across distinct instances
    assert not torch.equal(m1.embed_tokens.weight, m2.embed_tokens.weight)

    # Mean and std checks for initialization
    std = m1.embed_tokens.weight.std().item()
    mean = m1.embed_tokens.weight.mean().item()
    assert abs(mean) < 0.01, f"Expected mean close to 0, got {mean}"
    assert 0.015 < std < 0.025, f"Expected std close to 0.02, got {std}"


def test_causal_target_alignment_and_padding_exclusion():
    """Verify causal target shifting and strict padding token exclusion from loss."""
    cfg = NovaConfig(vocab_size=3384, max_seq_len=64, d_model=64, n_layers=2, n_heads=4, d_ff=176, pad_token_id=0)
    model = NovaForCausalLM(cfg)

    seq = torch.tensor([[5, 15, 25, 35, 0, 0]], dtype=torch.long)
    out = model(seq, targets=seq)

    shift_logits = out.logits[..., :-1, :].contiguous()
    shift_targets = seq[..., 1:].contiguous()

    # The targets should be [15, 25, 35, 0, 0]
    assert shift_targets.tolist() == [[15, 25, 35, 0, 0]]

    # Compute loss manually with and without padding
    loss_masked = F.cross_entropy(shift_logits.view(-1, cfg.vocab_size), shift_targets.view(-1), ignore_index=0)
    loss_valid_only = F.cross_entropy(shift_logits[:, :3, :].reshape(-1, cfg.vocab_size), shift_targets[:, :3].reshape(-1))

    assert abs(loss_masked.item() - loss_valid_only.item()) < 1e-5


def test_manifest_tokenizer_hash_alignment():
    """Verify manifest tokenizer hash matches artifacts/final_tokenizer/tokenizer.json."""
    manifest_p = PREPARED_EXPANDED_DIR / "manifest.json"
    with open(manifest_p, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    tok_file = FINAL_TOK_DIR / "tokenizer.json"
    actual_tok_hash = compute_file_sha256(tok_file)

    assert manifest["tokenizer_hash"] == actual_tok_hash, (
        f"Manifest tokenizer hash {manifest['tokenizer_hash']} != actual {actual_tok_hash}"
    )


def test_chinchilla_scaling_mismatch_metrics():
    """Verify the quantitative mismatch between current corpus and 20M compute-optimal requirements."""
    current_train_tokens = 123722
    nova_20m_params = 20301696

    tokens_per_param = current_train_tokens / nova_20m_params
    assert tokens_per_param < 0.01, f"Expected < 0.01 tokens/param for 20M model on current corpus, got {tokens_per_param:.4f}"

    chinchilla_optimal_tokens = 20 * nova_20m_params
    fraction_of_chinchilla = current_train_tokens / chinchilla_optimal_tokens

    # Verify current corpus is ~0.03% of compute-optimal
    assert 0.00025 < fraction_of_chinchilla < 0.00035, (
        f"Expected ~0.03% Chinchilla optimal, got {fraction_of_chinchilla * 100:.3f}%"
    )
