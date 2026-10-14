"""Tests for Nova-Fit Phase 4 Approved Corpus and Final Tokenizer.

Verifies:
1. Final tokenizer artifacts exist and previous prototype artifacts are preserved.
2. Special-token assignments are exact and conform to specification.
3. Encode/decode round-trip fidelity across text, units, symbols, and Unicode emojis.
4. Save/load consistency of the final tokenizer.
5. Strict separation between training corpus and validation corpus (zero overlap).
6. Training occurred only from approved training data registered in source_registry.json.
7. Model architecture compatibility with the final tokenizer vocabulary size.
8. Duplicate detection and document-level train/validation splitting.
9. Manifest integrity and provenance verification.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import torch

from nova.data import (
    CleaningConfig,
    DuplicateReport,
    PrepareDatasetConfig,
    compute_file_sha256,
    detect_exact_and_near_duplicates,
    extract_documents,
    prepare_dataset,
    split_documents,
    verify_sources_against_registry,
)
from nova.model import NovaConfig, NovaForCausalLM
from nova.tokenizer import NovaTokenizer, train_tokenizer


REPO_ROOT = Path(__file__).resolve().parent.parent
FINAL_TOK_DIR = REPO_ROOT / "artifacts" / "final_tokenizer"
PROTO_TOK_DIR = REPO_ROOT / "artifacts" / "tokenizer"
APPROVED_TRAIN_PATH = REPO_ROOT / "data" / "approved" / "train_corpus.txt"
APPROVED_VAL_PATH = REPO_ROOT / "data" / "approved" / "val_corpus.txt"
SOURCE_REGISTRY_PATH = REPO_ROOT / "data" / "approved" / "source_registry.json"
PREPARED_FINAL_DIR = REPO_ROOT / "data" / "prepared_final"


class TestArtifactPreservation:
    """Verify that both final and prototype artifacts are preserved."""

    def test_prototype_artifacts_preserved(self):
        """Phase 1 prototype tokenizer artifacts must still exist."""
        assert PROTO_TOK_DIR.is_dir(), f"Prototype dir {PROTO_TOK_DIR} missing"
        assert (PROTO_TOK_DIR / "tokenizer.json").is_file()
        assert (PROTO_TOK_DIR / "tokenizer_metadata.json").is_file()

        proto_tok = NovaTokenizer.from_file(PROTO_TOK_DIR)
        assert proto_tok.vocab_size == 2274

    def test_final_tokenizer_artifacts_exist(self):
        """Phase 4 final tokenizer artifacts must exist and be valid."""
        assert FINAL_TOK_DIR.is_dir(), f"Final tokenizer dir {FINAL_TOK_DIR} missing"
        assert (FINAL_TOK_DIR / "tokenizer.json").is_file()
        assert (FINAL_TOK_DIR / "tokenizer_metadata.json").is_file()

        final_tok = NovaTokenizer.from_file(FINAL_TOK_DIR)
        assert final_tok.vocab_size == 3384
        assert final_tok.vocab_size > 2274  # Expanded from larger approved corpus


class TestFinalTokenizerProperties:
    """Test final tokenizer special tokens, encoding, decoding, and save/load."""

    @pytest.fixture
    def final_tokenizer(self) -> NovaTokenizer:
        return NovaTokenizer.from_file(FINAL_TOK_DIR)

    def test_special_token_ids(self, final_tokenizer: NovaTokenizer):
        assert final_tokenizer.pad_token_id == 0
        assert final_tokenizer.unk_token_id == 1
        assert final_tokenizer.bos_token_id == 2
        assert final_tokenizer.eos_token_id == 3

    def test_round_trip_ascii_and_units(self, final_tokenizer: NovaTokenizer):
        text = "Squat 4x6 @ 80% 1RM. Rest 180s. Nutrition: 2.2 g/kg protein."
        tokens = final_tokenizer.encode(text)
        decoded = final_tokenizer.decode(tokens)
        assert decoded == text

    def test_round_trip_unicode_and_emojis(self, final_tokenizer: NovaTokenizer):
        text = "Workout finished! 🏋️‍♂️ Room: 20 ℃. Effort: ±5%."
        tokens = final_tokenizer.encode(text)
        decoded = final_tokenizer.decode(tokens)
        assert decoded == text

    def test_out_of_vocabulary_byte_fallback(self, final_tokenizer: NovaTokenizer):
        text = "Xenobiotic proprioceptive mechanotransduction uncalibrated."
        tokens = final_tokenizer.encode(text, allow_special=False)
        assert final_tokenizer.unk_token_id not in tokens
        decoded = final_tokenizer.decode(tokens)
        assert decoded == text

    def test_save_load_consistency(self, final_tokenizer: NovaTokenizer, tmp_path: Path):
        save_dir = tmp_path / "saved_tokenizer"
        final_tokenizer.save(save_dir)

        reloaded = NovaTokenizer.from_file(save_dir)
        assert reloaded.vocab_size == final_tokenizer.vocab_size
        assert reloaded.pad_token_id == final_tokenizer.pad_token_id
        assert reloaded.eos_token_id == final_tokenizer.eos_token_id

        sample = "Bench Press 3x10 @ 70% 1RM."
        assert reloaded.encode(sample) == final_tokenizer.encode(sample)


class TestApprovedCorpusAndSeparation:
    """Verify approved sources, legal registry, and disjointness of train and val sets."""

    def test_source_registry_exists_and_valid(self):
        assert SOURCE_REGISTRY_PATH.is_file()
        with open(SOURCE_REGISTRY_PATH, "r", encoding="utf-8") as f:
            registry = json.load(f)

        assert "approved_sources" in registry
        assert len(registry["approved_sources"]) >= 5

        for src in registry["approved_sources"]:
            assert "source_id" in src
            assert "license" in src
            assert "legal_basis" in src
            assert "domains" in src

    def test_train_and_val_corpora_exist(self):
        assert APPROVED_TRAIN_PATH.is_file()
        assert APPROVED_VAL_PATH.is_file()

        train_size = APPROVED_TRAIN_PATH.stat().st_size
        val_size = APPROVED_VAL_PATH.stat().st_size
        assert train_size > 10000
        assert val_size > 5000

    def test_zero_document_overlap_between_train_and_val(self):
        """Train and val corpora must have strictly zero document overlap."""
        train_text = APPROVED_TRAIN_PATH.read_text(encoding="utf-8")
        val_text = APPROVED_VAL_PATH.read_text(encoding="utf-8")

        train_docs = set(extract_documents(train_text))
        val_docs = set(extract_documents(val_text))

        overlap = train_docs.intersection(val_docs)
        assert len(overlap) == 0, f"Found overlapping documents: {overlap}"

    def test_training_only_from_approved_training_data(self):
        """Verify final tokenizer was trained from train_corpus.txt, not val."""
        meta_path = FINAL_TOK_DIR / "tokenizer_metadata.json"
        assert meta_path.is_file()

        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        assert "data/approved/train_corpus.txt" in meta["corpus_path"].replace("\\", "/")
        assert "val_corpus.txt" not in meta["corpus_path"]

        # Verify hash in metadata matches current train_corpus.txt
        expected_sha = compute_file_sha256(APPROVED_TRAIN_PATH)
        assert meta["corpus_sha256"] == expected_sha


class TestDuplicateDetectionAndSplitting:
    """Verify duplicate detection and document-level train/val splitting."""

    def test_exact_duplicate_detection(self):
        docs = [
            "This is unique document one for resistance training.",
            "This is unique document one for resistance training.",  # Exact dup
            "This is a second distinct document about sports nutrition.",
        ]
        retained, report, groups = detect_exact_and_near_duplicates(docs, remove_exact=True)
        assert len(retained) == 2
        assert report.exact_duplicates_removed == 1
        assert report.unique_documents == 2

    def test_split_documents_preserves_boundaries(self):
        docs = [f"Fitness document number {i} detailing exercise biomechanics." for i in range(10)]
        train_docs, val_docs = split_documents(docs, val_ratio=0.2, seed=42)

        assert len(train_docs) + len(val_docs) == len(docs)
        assert len(val_docs) == 2
        assert len(train_docs) == 8
        # Ensure zero overlap
        assert set(train_docs).isdisjoint(set(val_docs))

    def test_group_aware_split_keeps_duplicates_in_same_split(self):
        docs = [
            "Doc A original text about progressive overload.",
            "Doc A duplicate text about progressive overload.",
            "Doc B unique text on myofibrillar hypertrophy.",
            "Doc C unique text on sleep architecture.",
        ]
        retained, report, groups = detect_exact_and_near_duplicates(
            docs, similarity_threshold=0.5, remove_exact=False
        )
        train_docs, val_docs = split_documents(retained, val_ratio=0.5, seed=42, groups=groups)

        # Both Doc A versions must be in the same split
        if docs[0] in train_docs:
            assert docs[1] in train_docs
        else:
            assert docs[1] in val_docs


class TestModelCompatibility:
    """Verify that final tokenizer vocabulary size integrates cleanly with NovaForCausalLM."""

    def test_model_instantiation_with_final_vocab(self):
        final_tok = NovaTokenizer.from_file(FINAL_TOK_DIR)
        config = NovaConfig(
            vocab_size=final_tok.vocab_size,
            max_seq_len=64,
            n_layers=2,
            d_model=64,
            n_heads=4,
            d_ff=176,
            pad_token_id=final_tok.pad_token_id,
        )
        model = NovaForCausalLM(config)
        assert model.config.vocab_size == final_tok.vocab_size

        batch_size = 2
        seq_len = 16
        input_ids = torch.randint(0, final_tok.vocab_size, (batch_size, seq_len), dtype=torch.long)
        targets = input_ids.clone()

        output = model(input_ids, targets=targets)
        assert output.logits.shape == (batch_size, seq_len, final_tok.vocab_size)
        assert output.loss is not None
        assert torch.isfinite(output.loss)
        assert output.loss.item() > 0.0


class TestPreparedDatasetManifest:
    """Verify final prepared dataset files and manifest."""

    def test_prepared_final_files_exist(self):
        assert PREPARED_FINAL_DIR.is_dir()
        assert (PREPARED_FINAL_DIR / "train.pt").is_file()
        assert (PREPARED_FINAL_DIR / "val.pt").is_file()
        assert (PREPARED_FINAL_DIR / "manifest.json").is_file()

        manifest_path = PREPARED_FINAL_DIR / "manifest.json"
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        assert manifest["tokenizer_vocab_size"] == 3384
        assert manifest["train_sequences"] > 0
        assert manifest["val_sequences"] > 0
        assert manifest["total_tokens_train"] > 0
        assert manifest["total_tokens_val"] > 0
        assert "duplicate_report" in manifest
        assert "source_audit" in manifest
        assert manifest["source_audit"]["verified"] is True
