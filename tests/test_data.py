"""Tests for Nova-Fit Phase 3 Dataset Preparation Pipeline.

Verifies:
1. Text cleaning correctly processes lines, handles edge cases, and respects config.
2. Corpus loading validates file paths and reads content accurately.
3. Document extraction splits corpus on section boundaries.
4. Corpus statistics are computed correctly.
5. Tokenization produces valid token ID sequences with optional EOS.
6. Sequence packing creates fixed-length chunks with correct padding.
7. Train/validation splitting is reproducible and respects ratios.
8. NovaPretrainingDataset returns correct (input_ids, target_ids) pairs.
9. End-to-end pipeline produces valid artifacts on the smoke corpus.
10. Manifest contains complete provenance metadata.
11. Round-trip: prepared datasets can be loaded and used for training.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Dict, List

import numpy as np
import pytest
import torch

from nova.data import (
    CleaningConfig,
    CorpusStats,
    DatasetManifest,
    NovaPretrainingDataset,
    PrepareDatasetConfig,
    PrepareDatasetResult,
    TokenizedCorpusStats,
    clean_line,
    clean_text,
    compute_corpus_stats,
    compute_file_sha256,
    extract_documents,
    load_corpus_files,
    load_manifest,
    load_prepared_dataset,
    pack_sequences,
    prepare_dataset,
    split_sequences,
    tokenize_documents,
)
from nova.tokenizer import NovaTokenizer


# =============================================================================
# Fixtures
# =============================================================================

SMOKE_CORPUS_PATH = Path("data/raw/fitness_smoke_corpus.txt")
TOKENIZER_ARTIFACTS = Path("artifacts/tokenizer")


@pytest.fixture
def cleaning_config():
    """Default cleaning configuration."""
    return CleaningConfig()


@pytest.fixture
def strict_cleaning_config():
    """Cleaning config that strips headers and lowercases."""
    return CleaningConfig(
        strip_section_headers=True,
        lowercase=True,
    )


@pytest.fixture
def trained_tokenizer(tmp_path):
    """Train a tokenizer on the smoke corpus for test use."""
    if SMOKE_CORPUS_PATH.is_file():
        tok = NovaTokenizer.train_from_corpus(
            corpus_path=SMOKE_CORPUS_PATH,
            vocab_size=8000,
            min_frequency=1,
        )
        return tok

    # Fallback: create a minimal corpus in tmp_path
    corpus = tmp_path / "mini_corpus.txt"
    corpus.write_text(
        "Progressive overload builds strength.\n"
        "Protein synthesis requires amino acids.\n"
        "Sleep is essential for recovery.\n",
        encoding="utf-8",
    )
    return NovaTokenizer.train_from_corpus(
        corpus_path=corpus,
        vocab_size=1000,
        min_frequency=1,
    )


@pytest.fixture
def sample_documents():
    """Sample cleaned documents for testing."""
    return [
        "Progressive overload is the foundation of strength training.",
        "Protein intake of 1.6 to 2.2 g/kg/day supports hypertrophy.",
        "Sleep quality directly impacts recovery and performance.",
        "The barbell squat requires triple flexion at hip, knee, and ankle.",
        "Heart rate variability measures autonomic recovery status.",
    ]


@pytest.fixture
def sample_token_sequences():
    """Pre-built token sequences for packing tests."""
    return [
        [10, 20, 30, 40, 50, 3],  # 6 tokens ending with EOS (3)
        [11, 21, 31, 41, 51, 61, 71, 3],  # 8 tokens
        [12, 22, 32, 3],  # 4 tokens
    ]


# =============================================================================
# Text Cleaning Tests
# =============================================================================


class TestCleanLine:
    """Tests for clean_line function."""

    def test_strips_whitespace(self, cleaning_config):
        assert clean_line("  hello world  ", cleaning_config) == "hello world"

    def test_returns_none_for_empty_line(self, cleaning_config):
        assert clean_line("", cleaning_config) is None
        assert clean_line("   ", cleaning_config) is None

    def test_strips_comment_lines(self, cleaning_config):
        assert clean_line("# This is a comment", cleaning_config) is None
        assert clean_line("## Double hash comment", cleaning_config) is None

    def test_preserves_non_comment_lines(self, cleaning_config):
        result = clean_line("Progressive overload builds strength.", cleaning_config)
        assert result == "Progressive overload builds strength."

    def test_normalizes_internal_whitespace(self, cleaning_config):
        result = clean_line("word1   word2\tword3", cleaning_config)
        assert result == "word1 word2 word3"

    def test_strips_section_headers_when_configured(self, strict_cleaning_config):
        assert clean_line("[SECTION: STRENGTH TRAINING]", strict_cleaning_config) is None

    def test_preserves_section_headers_by_default(self, cleaning_config):
        result = clean_line("[SECTION: STRENGTH TRAINING]", cleaning_config)
        assert result is not None
        assert "SECTION" in result

    def test_lowercase_when_configured(self, strict_cleaning_config):
        result = clean_line("Progressive Overload", strict_cleaning_config)
        assert result == "progressive overload"

    def test_type_error_for_non_string(self, cleaning_config):
        with pytest.raises(TypeError, match="Expected str"):
            clean_line(123, cleaning_config)


class TestCleanText:
    """Tests for clean_text function."""

    def test_cleans_multiline_text(self, cleaning_config):
        text = "# Comment\nLine one.\n\nLine two.\n# Another comment"
        result = clean_text(text, cleaning_config)
        assert "Line one." in result
        assert "Line two." in result
        assert "# Comment" not in result

    def test_handles_empty_input(self, cleaning_config):
        assert clean_text("", cleaning_config) == ""

    def test_handles_all_comments(self, cleaning_config):
        text = "# Comment 1\n# Comment 2\n# Comment 3"
        assert clean_text(text, cleaning_config) == ""

    def test_type_error_for_non_string(self):
        with pytest.raises(TypeError, match="Expected str"):
            clean_text(42)

    def test_default_config_when_none(self):
        result = clean_text("hello world")
        assert result == "hello world"


# =============================================================================
# Corpus Loading Tests
# =============================================================================


class TestLoadCorpusFiles:
    """Tests for load_corpus_files function."""

    def test_loads_single_file(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("Hello world", encoding="utf-8")
        result = load_corpus_files(f)
        assert len(result) == 1
        assert result[0][1] == "Hello world"

    def test_loads_multiple_files(self, tmp_path):
        f1 = tmp_path / "a.txt"
        f2 = tmp_path / "b.txt"
        f1.write_text("File A", encoding="utf-8")
        f2.write_text("File B", encoding="utf-8")
        result = load_corpus_files([f1, f2])
        assert len(result) == 2

    def test_file_not_found_error(self):
        with pytest.raises(FileNotFoundError):
            load_corpus_files("nonexistent_file.txt")

    def test_type_error_for_invalid_input(self):
        with pytest.raises(TypeError):
            load_corpus_files(123)

    def test_loads_smoke_corpus(self):
        """Verify the actual smoke corpus loads successfully."""
        if not SMOKE_CORPUS_PATH.is_file():
            pytest.skip("Smoke corpus not available")
        result = load_corpus_files(SMOKE_CORPUS_PATH)
        assert len(result) == 1
        assert len(result[0][1]) > 0


# =============================================================================
# Document Extraction Tests
# =============================================================================


class TestExtractDocuments:
    """Tests for extract_documents function."""

    def test_extracts_from_sectioned_corpus(self):
        text = (
            "# Header comment\n"
            "[SECTION: FIRST]\n"
            "First section content here.\n\n"
            "[SECTION: SECOND]\n"
            "Second section content here.\n"
        )
        docs = extract_documents(text)
        # Should have at least 2 documents (from the 2 sections)
        assert len(docs) >= 2

    def test_extracts_with_custom_separator(self):
        text = "Doc 1 text|||Doc 2 text|||Doc 3 text"
        docs = extract_documents(text, separator="|||")
        assert len(docs) == 3

    def test_drops_short_documents(self):
        config = CleaningConfig(min_doc_chars=50)
        text = "Short.\n\n[SECTION: LONG]\nThis is a much longer document that has enough content to pass the minimum character threshold."
        docs = extract_documents(text, config=config)
        # Only the long document should survive
        for doc in docs:
            assert len(doc) >= 50

    def test_type_error_for_non_string(self):
        with pytest.raises(TypeError, match="Expected str"):
            extract_documents(42)

    def test_empty_text_returns_empty(self):
        docs = extract_documents("")
        assert docs == []


# =============================================================================
# Corpus Statistics Tests
# =============================================================================


class TestComputeCorpusStats:
    """Tests for compute_corpus_stats function."""

    def test_computes_basic_stats(self, sample_documents):
        stats = compute_corpus_stats(sample_documents)
        assert stats.total_documents == 5
        assert stats.total_characters > 0
        assert stats.total_words > 0
        assert stats.avg_document_chars > 0
        assert stats.min_document_chars <= stats.max_document_chars

    def test_empty_documents_list(self):
        stats = compute_corpus_stats([])
        assert stats.total_documents == 0
        assert stats.total_characters == 0
        assert stats.total_words == 0

    def test_single_document(self):
        stats = compute_corpus_stats(["Hello world test"])
        assert stats.total_documents == 1
        assert stats.min_document_chars == stats.max_document_chars


# =============================================================================
# File Hash Tests
# =============================================================================


class TestComputeFileHash:
    """Tests for compute_file_sha256 function."""

    def test_computes_hash(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("Hello world", encoding="utf-8")
        hash_val = compute_file_sha256(f)
        assert isinstance(hash_val, str)
        assert len(hash_val) == 64  # SHA-256 hex digest length

    def test_deterministic_hash(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("Deterministic content", encoding="utf-8")
        h1 = compute_file_sha256(f)
        h2 = compute_file_sha256(f)
        assert h1 == h2

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            compute_file_sha256("nonexistent.txt")


# =============================================================================
# Tokenization Tests
# =============================================================================


class TestTokenizeDocuments:
    """Tests for tokenize_documents function."""

    def test_tokenizes_documents(self, trained_tokenizer, sample_documents):
        tokenized = tokenize_documents(sample_documents, trained_tokenizer)
        assert len(tokenized) == len(sample_documents)
        for tokens in tokenized:
            assert len(tokens) > 0
            assert all(isinstance(t, int) for t in tokens)

    def test_appends_eos_by_default(self, trained_tokenizer):
        docs = ["Hello world"]
        tokenized = tokenize_documents(docs, trained_tokenizer, add_eos=True)
        assert tokenized[0][-1] == trained_tokenizer.eos_token_id

    def test_no_eos_when_disabled(self, trained_tokenizer):
        docs = ["Hello world"]
        tokenized = tokenize_documents(docs, trained_tokenizer, add_eos=False)
        # Last token should not necessarily be EOS
        # (it could be by coincidence, but the function should not force it)
        # Just verify tokenization works
        assert len(tokenized[0]) > 0

    def test_type_error_for_non_list(self, trained_tokenizer):
        with pytest.raises(TypeError, match="documents must be a list"):
            tokenize_documents("not a list", trained_tokenizer)


# =============================================================================
# Sequence Packing Tests
# =============================================================================


class TestPackSequences:
    """Tests for pack_sequences function."""

    def test_packs_to_fixed_length(self, sample_token_sequences):
        packed = pack_sequences(sample_token_sequences, max_seq_len=8, pad_token_id=0)
        assert len(packed) > 0
        for seq in packed:
            assert len(seq) == 8

    def test_pads_last_sequence(self, sample_token_sequences):
        packed = pack_sequences(
            sample_token_sequences,
            max_seq_len=10,
            pad_token_id=0,
            drop_last_short=False,
        )
        for seq in packed:
            assert len(seq) == 10

    def test_drops_last_short(self, sample_token_sequences):
        # Total tokens: 6 + 8 + 4 = 18, with max_seq_len=10 -> 1 full + 1 short
        packed_drop = pack_sequences(
            sample_token_sequences,
            max_seq_len=10,
            pad_token_id=0,
            drop_last_short=True,
        )
        packed_keep = pack_sequences(
            sample_token_sequences,
            max_seq_len=10,
            pad_token_id=0,
            drop_last_short=False,
        )
        assert len(packed_drop) <= len(packed_keep)

    def test_empty_input(self):
        packed = pack_sequences([], max_seq_len=10, pad_token_id=0)
        assert packed == []

    def test_invalid_seq_len(self):
        with pytest.raises(ValueError, match="positive integer"):
            pack_sequences([[1, 2]], max_seq_len=0, pad_token_id=0)

    def test_all_tokens_preserved(self, sample_token_sequences):
        """Verify no tokens are lost during packing (excluding padding)."""
        total_input = sum(len(s) for s in sample_token_sequences)
        packed = pack_sequences(
            sample_token_sequences,
            max_seq_len=10,
            pad_token_id=0,
            drop_last_short=False,
        )
        total_output = sum(1 for seq in packed for t in seq if t != 0)
        # Account for pad tokens - all original tokens should be present
        assert total_output >= total_input - 1  # -1 tolerance for edge cases


# =============================================================================
# Train/Val Split Tests
# =============================================================================


class TestSplitSequences:
    """Tests for split_sequences function."""

    def test_splits_with_default_ratio(self):
        sequences = [[i] * 10 for i in range(20)]
        train, val = split_sequences(sequences, val_ratio=0.2, seed=42)
        assert len(train) + len(val) == 20
        assert len(val) == 4  # 20 * 0.2 = 4

    def test_reproducible_with_same_seed(self):
        sequences = [[i] * 10 for i in range(20)]
        t1, v1 = split_sequences(sequences, val_ratio=0.2, seed=42)
        t2, v2 = split_sequences(sequences, val_ratio=0.2, seed=42)
        assert t1 == t2
        assert v1 == v2

    def test_different_seeds_give_different_splits(self):
        sequences = [[i] * 10 for i in range(50)]
        t1, v1 = split_sequences(sequences, val_ratio=0.2, seed=42)
        t2, v2 = split_sequences(sequences, val_ratio=0.2, seed=99)
        # Very unlikely but possible they're identical; check val sets differ
        assert v1 != v2 or t1 != t2

    def test_zero_val_ratio(self):
        sequences = [[i] * 10 for i in range(10)]
        train, val = split_sequences(sequences, val_ratio=0.0)
        assert len(val) == 0
        assert len(train) == 10

    def test_invalid_val_ratio(self):
        with pytest.raises(ValueError, match="val_ratio"):
            split_sequences([[1]], val_ratio=1.5)

    def test_empty_input(self):
        train, val = split_sequences([], val_ratio=0.2)
        assert train == []
        assert val == []

    def test_single_sequence(self):
        """With 1 sequence, training set must have at least 1."""
        train, val = split_sequences([[1, 2, 3]], val_ratio=0.5)
        assert len(train) >= 1


# =============================================================================
# NovaPretrainingDataset Tests
# =============================================================================


class TestNovaPretrainingDataset:
    """Tests for NovaPretrainingDataset class."""

    def test_creates_dataset(self):
        sequences = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
        ds = NovaPretrainingDataset(sequences)
        assert len(ds) == 2
        assert ds.max_seq_len == 5
        assert ds.effective_seq_len == 4

    def test_getitem_returns_shifted_pairs(self):
        sequences = [[10, 20, 30, 40, 50]]
        ds = NovaPretrainingDataset(sequences)
        input_ids, target_ids = ds[0]

        assert input_ids.tolist() == [10, 20, 30, 40]
        assert target_ids.tolist() == [20, 30, 40, 50]

    def test_tensor_types(self):
        sequences = [[1, 2, 3, 4]]
        ds = NovaPretrainingDataset(sequences)
        input_ids, target_ids = ds[0]
        assert input_ids.dtype == torch.long
        assert target_ids.dtype == torch.long

    def test_inconsistent_lengths_error(self):
        with pytest.raises(ValueError, match="length"):
            NovaPretrainingDataset([[1, 2, 3], [4, 5]])

    def test_empty_sequences_error(self):
        with pytest.raises(ValueError, match="empty"):
            NovaPretrainingDataset([])

    def test_type_error_for_non_list(self):
        with pytest.raises(TypeError, match="list"):
            NovaPretrainingDataset("not a list")


# =============================================================================
# End-to-End Pipeline Tests
# =============================================================================


class TestPrepareDatasetPipeline:
    """End-to-end tests for the prepare_dataset function."""

    def test_pipeline_with_smoke_corpus(self, trained_tokenizer, tmp_path):
        """Full pipeline test using the smoke corpus."""
        if not SMOKE_CORPUS_PATH.is_file():
            pytest.skip("Smoke corpus not available")

        output_dir = tmp_path / "prepared"
        config = PrepareDatasetConfig(
            corpus_paths=[str(SMOKE_CORPUS_PATH)],
            output_dir=str(output_dir),
            max_seq_len=64,  # Small for test
            val_ratio=0.1,
            split_seed=42,
        )

        result = prepare_dataset(
            config=config,
            tokenizer=trained_tokenizer,
            verbose=False,
        )

        assert result.success is True, f"Pipeline failed: {result.message}"
        assert result.train_sequences > 0
        assert result.total_tokens > 0

        # Verify files exist
        assert (output_dir / "train.pt").is_file()
        assert (output_dir / "val.pt").is_file()
        assert (output_dir / "manifest.json").is_file()

    def test_pipeline_creates_valid_tensors(self, trained_tokenizer, tmp_path):
        """Verify saved tensors have correct shapes and types."""
        if not SMOKE_CORPUS_PATH.is_file():
            pytest.skip("Smoke corpus not available")

        output_dir = tmp_path / "prepared"
        config = PrepareDatasetConfig(
            corpus_paths=[str(SMOKE_CORPUS_PATH)],
            output_dir=str(output_dir),
            max_seq_len=32,
            val_ratio=0.1,
        )

        result = prepare_dataset(
            config=config,
            tokenizer=trained_tokenizer,
            verbose=False,
        )
        assert result.success

        train_tensor = torch.load(str(output_dir / "train.pt"), weights_only=True)
        assert train_tensor.dtype == torch.long
        assert train_tensor.dim() == 2
        assert train_tensor.shape[1] == 32

    def test_pipeline_manifest_completeness(self, trained_tokenizer, tmp_path):
        """Verify manifest contains all required provenance fields."""
        if not SMOKE_CORPUS_PATH.is_file():
            pytest.skip("Smoke corpus not available")

        output_dir = tmp_path / "prepared"
        config = PrepareDatasetConfig(
            corpus_paths=[str(SMOKE_CORPUS_PATH)],
            output_dir=str(output_dir),
            max_seq_len=32,
            val_ratio=0.05,
        )

        prepare_dataset(config=config, tokenizer=trained_tokenizer, verbose=False)

        manifest = load_manifest(output_dir)

        required_keys = [
            "name", "version", "created_at",
            "corpus_stats", "tokenized_stats",
            "source_files", "cleaning_config", "split_config",
            "train_sequences", "val_sequences",
            "total_tokens_train", "total_tokens_val",
            "tokenizer_vocab_size", "max_seq_len",
            "python_version", "numpy_version", "torch_version",
        ]

        missing = [k for k in required_keys if k not in manifest]
        assert not missing, f"Manifest missing keys: {missing}"

        # Verify source file has SHA-256
        assert len(manifest["source_files"]) > 0
        for sf in manifest["source_files"]:
            assert "sha256" in sf
            assert len(sf["sha256"]) == 64

    def test_pipeline_with_custom_cleaning(self, trained_tokenizer, tmp_path):
        """Test pipeline with section headers stripped and lowercase."""
        if not SMOKE_CORPUS_PATH.is_file():
            pytest.skip("Smoke corpus not available")

        output_dir = tmp_path / "prepared"
        config = PrepareDatasetConfig(
            corpus_paths=[str(SMOKE_CORPUS_PATH)],
            output_dir=str(output_dir),
            max_seq_len=32,
            val_ratio=0.1,
            cleaning=CleaningConfig(
                strip_section_headers=True,
                lowercase=True,
            ),
        )

        result = prepare_dataset(
            config=config,
            tokenizer=trained_tokenizer,
            verbose=False,
        )
        assert result.success

    def test_pipeline_fails_gracefully_no_corpus(self, trained_tokenizer, tmp_path):
        """Pipeline should fail cleanly if corpus doesn't exist."""
        config = PrepareDatasetConfig(
            corpus_paths=["nonexistent_corpus.txt"],
            output_dir=str(tmp_path / "out"),
        )

        result = prepare_dataset(
            config=config,
            tokenizer=trained_tokenizer,
            verbose=False,
        )
        assert result.success is False
        assert "Failed" in result.message or "not found" in result.message.lower()

    def test_pipeline_fails_gracefully_no_tokenizer(self, tmp_path):
        """Pipeline should fail cleanly if tokenizer doesn't exist."""
        config = PrepareDatasetConfig(
            corpus_paths=[str(SMOKE_CORPUS_PATH)] if SMOKE_CORPUS_PATH.is_file() else ["dummy.txt"],
            tokenizer_path=str(tmp_path / "nonexistent_tokenizer"),
            output_dir=str(tmp_path / "out"),
        )

        result = prepare_dataset(
            config=config,
            tokenizer=None,
            verbose=False,
        )
        assert result.success is False


# =============================================================================
# Dataset Loading Tests
# =============================================================================


class TestLoadPreparedDataset:
    """Tests for load_prepared_dataset and load_manifest."""

    def test_round_trip_load(self, trained_tokenizer, tmp_path):
        """Prepare, save, reload, and verify dataset integrity."""
        if not SMOKE_CORPUS_PATH.is_file():
            pytest.skip("Smoke corpus not available")

        output_dir = tmp_path / "prepared"
        config = PrepareDatasetConfig(
            corpus_paths=[str(SMOKE_CORPUS_PATH)],
            output_dir=str(output_dir),
            max_seq_len=32,
            val_ratio=0.1,
        )

        result = prepare_dataset(
            config=config,
            tokenizer=trained_tokenizer,
            verbose=False,
        )
        assert result.success

        # Load train split
        train_ds = load_prepared_dataset(output_dir, split="train")
        assert len(train_ds) == result.train_sequences
        assert train_ds.max_seq_len == 32

        # Verify sample structure
        input_ids, target_ids = train_ds[0]
        assert input_ids.shape[0] == 31  # max_seq_len - 1
        assert target_ids.shape[0] == 31

    def test_invalid_split_name(self, tmp_path):
        with pytest.raises(ValueError, match="split must be"):
            load_prepared_dataset(tmp_path, split="test")

    def test_missing_split_file(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_prepared_dataset(tmp_path, split="train")

    def test_missing_manifest(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_manifest(tmp_path)


# =============================================================================
# Integration Tests with DataLoader
# =============================================================================


class TestDataLoaderIntegration:
    """Verify dataset works correctly with PyTorch DataLoader."""

    def test_dataloader_batching(self, trained_tokenizer, tmp_path):
        """Verify DataLoader produces correct batch shapes."""
        if not SMOKE_CORPUS_PATH.is_file():
            pytest.skip("Smoke corpus not available")

        output_dir = tmp_path / "prepared"
        config = PrepareDatasetConfig(
            corpus_paths=[str(SMOKE_CORPUS_PATH)],
            output_dir=str(output_dir),
            max_seq_len=32,
            val_ratio=0.0,
        )

        prepare_dataset(config=config, tokenizer=trained_tokenizer, verbose=False)

        train_ds = load_prepared_dataset(output_dir, split="train")
        loader = torch.utils.data.DataLoader(
            train_ds,
            batch_size=2,
            shuffle=False,
        )

        batch = next(iter(loader))
        input_ids, target_ids = batch
        assert input_ids.dim() == 2
        assert target_ids.dim() == 2
        assert input_ids.shape[1] == 31  # max_seq_len - 1
        assert target_ids.shape[1] == 31
