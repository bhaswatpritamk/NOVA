"""Comprehensive test suite for Phase 6: Corpus Expansion and Data Quality.

Verifies:
1. Source Registry & Provenance Integrity (legal basis, licenses, hashes).
2. Raw Source File Traceability and SHA-256 matching.
3. Training Corpus Scale Target (>= 100,000 training tokens).
4. Zero Cross-Split Leakage (document-level and group-level train/val isolation).
5. Comprehensive 7-Pillar Coverage and Balance.
6. Prepared Dataset Integrity & Tokenizer Hash Verification.
7. Deterministic Pipeline Reproducibility.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Set

import pytest
import torch

from nova.corpus import (
    CorpusDocument,
    SourceRegistry,
    TOPIC_DOMAINS,
    calculate_split_statistics,
    detect_duplicates_and_group,
    partition_documents_by_group,
)
from nova.data import compute_file_sha256
from nova.tokenizer import NovaTokenizer
from scripts.sources import get_all_documents


ROOT_DIR = Path(__file__).resolve().parent.parent
APPROVED_DIR = ROOT_DIR / "data" / "approved"
SOURCES_RAW_DIR = ROOT_DIR / "data" / "sources_raw"
PREPARED_DIR = ROOT_DIR / "data" / "prepared_expanded"
TOKENIZER_DIR = ROOT_DIR / "artifacts" / "final_tokenizer"


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def tokenizer() -> NovaTokenizer:
    """Load the final Byte-Level BPE tokenizer."""
    assert TOKENIZER_DIR.exists(), f"Final tokenizer not found at {TOKENIZER_DIR}"
    return NovaTokenizer.from_file(TOKENIZER_DIR)


@pytest.fixture(scope="module")
def source_registry() -> SourceRegistry:
    """Load the v2.0 Source Registry."""
    reg_path = APPROVED_DIR / "source_registry.json"
    assert reg_path.exists(), f"Source registry not found at {reg_path}"
    return SourceRegistry.load(reg_path)


@pytest.fixture(scope="module")
def all_documents() -> list[dict]:
    """Load all raw documents across the 7 pillars."""
    docs = get_all_documents()
    assert len(docs) > 0, "No educational documents returned by get_all_documents()"
    return docs


@pytest.fixture(scope="module")
def train_corpus_text() -> str:
    """Load the expanded training corpus file."""
    path = APPROVED_DIR / "expanded_train_corpus.txt"
    assert path.exists(), f"Expanded train corpus not found at {path}"
    return path.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def val_corpus_text() -> str:
    """Load the expanded validation corpus file."""
    path = APPROVED_DIR / "expanded_val_corpus.txt"
    assert path.exists(), f"Expanded val corpus not found at {path}"
    return path.read_text(encoding="utf-8")


# =============================================================================
# 1. Source Registry & Legal Provenance Tests
# =============================================================================


def test_source_registry_schema_and_version(source_registry: SourceRegistry):
    """Verify source registry conforms to v2.0 specifications."""
    assert source_registry.version == "2.0.0"
    assert len(source_registry.sources) >= 14, "Expected at least 14 approved sources"


def test_every_source_has_defensible_license(source_registry: SourceRegistry):
    """Verify all approved sources have explicit, valid licenses allowing training."""
    allowed_licenses = {"Public Domain", "CC BY 4.0"}
    for sid, record in source_registry.sources.items():
        assert record.license in allowed_licenses, f"Source {sid} has unapproved license: {record.license}"
        assert record.commercial_use_permitted is True, f"Source {sid} must permit commercial training use"
        assert len(record.legal_basis) > 0, f"Source {sid} missing legal basis citation"
        assert len(record.url) > 0, f"Source {sid} missing source URL"
        assert len(record.author) > 0, f"Source {sid} missing author"
        assert record.publication_year > 1900, f"Source {sid} invalid publication year: {record.publication_year}"


def test_cc_by_attribution_obligation_preserved(source_registry: SourceRegistry):
    """Verify CC BY 4.0 sources have mandatory attribution notices recorded."""
    for sid, record in source_registry.sources.items():
        if record.license == "CC BY 4.0":
            assert record.attribution_required is True, f"CC BY 4.0 source {sid} must have attribution_required=True"
            assert len(record.attribution_text) > 20, f"Source {sid} missing detailed attribution text"
            assert "OpenStax" in record.attribution_text, f"Source {sid} attribution must reference OpenStax"


def test_raw_source_files_exist_and_hashes_match(source_registry: SourceRegistry):
    """Verify raw files exist in data/sources_raw/ and match SHA-256 hashes in registry."""
    assert SOURCES_RAW_DIR.exists()
    for sid, record in source_registry.sources.items():
        filename = f"{sid.lower().replace('-', '_')}_raw.txt"
        file_path = SOURCES_RAW_DIR / filename
        assert file_path.exists(), f"Raw source file missing: {file_path}"
        computed_hash = compute_file_sha256(file_path)
        assert computed_hash == record.raw_sha256, (
            f"Hash mismatch for {sid}: expected {record.raw_sha256}, got {computed_hash}"
        )
        assert file_path.stat().st_size == record.raw_bytes, f"Byte size mismatch for {sid}"


# =============================================================================
# 2. Corpus Scale and Token Target Tests
# =============================================================================


def test_train_corpus_exceeds_100k_tokens_milestone(train_corpus_text: str, tokenizer: NovaTokenizer):
    """Verify the training corpus reaches the 100,000 raw training token milestone."""
    tokens = tokenizer.encode(train_corpus_text, allow_special=False)
    raw_token_count = len(tokens)
    assert raw_token_count >= 100000, (
        f"Scale milestone FAILED: Expected >= 100,000 training tokens, got {raw_token_count:,}"
    )


def test_val_corpus_scale(val_corpus_text: str, tokenizer: NovaTokenizer):
    """Verify the validation corpus has sufficient scale (>= 10,000 tokens)."""
    tokens = tokenizer.encode(val_corpus_text, allow_special=False)
    assert len(tokens) >= 10000, f"Validation corpus too small: {len(tokens):,} tokens"


def test_token_density_is_reasonable(train_corpus_text: str, tokenizer: NovaTokenizer):
    """Verify token density (tokens/word and chars/token) reflects natural English."""
    tokens = tokenizer.encode(train_corpus_text, allow_special=False)
    words = train_corpus_text.split()
    chars = len(train_corpus_text)

    tokens_per_word = len(tokens) / len(words)
    chars_per_token = chars / len(tokens)

    # Typical BPE on technical text: 1.5 to 2.8 tokens per word, 3.0 to 4.5 chars per token
    assert 1.4 <= tokens_per_word <= 3.0, f"Unusual tokens per word: {tokens_per_word:.2f}"
    assert 2.5 <= chars_per_token <= 5.0, f"Unusual chars per token: {chars_per_token:.2f}"


# =============================================================================
# 3. Topic Coverage and Representation Tests
# =============================================================================


def test_all_seven_pillars_represented_in_both_splits(all_documents: list[dict]):
    """Verify all 7 Nova-Fit pillars are populated and partitioned into train and val."""
    corpus_docs = [
        CorpusDocument(
            doc_id=d["doc_id"],
            section_title=d["section_title"],
            source_id=d["source_id"],
            topic_domain=d["topic_domain"],
            text=d["text"],
            group_id=d["group_id"],
        )
        for d in all_documents
    ]
    retained_docs, _, _ = detect_duplicates_and_group(corpus_docs)
    train_docs, val_docs = partition_documents_by_group(retained_docs, val_ratio=0.15, seed=42)

    train_domains = set(d.topic_domain for d in train_docs)
    val_domains = set(d.topic_domain for d in val_docs)

    expected_domains = set(TOPIC_DOMAINS.keys())

    assert train_domains == expected_domains, f"Train missing domains: {expected_domains - train_domains}"
    assert val_domains == expected_domains, f"Val missing domains: {expected_domains - val_domains}"

    # Verify no domain is severely under-represented in train (>= 20 docs each)
    for dom in expected_domains:
        cnt = sum(1 for d in train_docs if d.topic_domain == dom)
        assert cnt >= 20, f"Domain {dom} has only {cnt} training documents (minimum 20 expected)"


# =============================================================================
# 4. Zero Cross-Split Leakage & Deduplication Tests
# =============================================================================


def test_zero_document_and_group_leakage(all_documents: list[dict]):
    """Verify 0% document ID and 0% cluster group ID leakage between train and val."""
    corpus_docs = [
        CorpusDocument(
            doc_id=d["doc_id"],
            section_title=d["section_title"],
            source_id=d["source_id"],
            topic_domain=d["topic_domain"],
            text=d["text"],
            group_id=d["group_id"],
        )
        for d in all_documents
    ]
    retained_docs, audit, _ = detect_duplicates_and_group(corpus_docs, near_dup_threshold=0.85)
    train_docs, val_docs = partition_documents_by_group(retained_docs, val_ratio=0.15, seed=42)

    train_ids = set(d.doc_id for d in train_docs)
    val_ids = set(d.doc_id for d in val_docs)
    assert len(train_ids & val_ids) == 0, f"Document ID leakage detected: {train_ids & val_ids}"

    train_groups = set(d.group_id for d in train_docs)
    val_groups = set(d.group_id for d in val_docs)
    assert len(train_groups & val_groups) == 0, f"Group ID leakage detected: {train_groups & val_groups}"


def test_no_high_jaccard_similarity_across_splits(all_documents: list[dict]):
    """Verify that no document in val has >= 0.85 Jaccard similarity to any train doc."""
    corpus_docs = [
        CorpusDocument(
            doc_id=d["doc_id"],
            section_title=d["section_title"],
            source_id=d["source_id"],
            topic_domain=d["topic_domain"],
            text=d["text"],
            group_id=d["group_id"],
        )
        for d in all_documents
    ]
    retained_docs, _, _ = detect_duplicates_and_group(corpus_docs, near_dup_threshold=0.85)
    train_docs, val_docs = partition_documents_by_group(retained_docs, val_ratio=0.15, seed=42)

    def get_shingles(text: str, k: int = 5) -> Set[str]:
        import re
        norm = re.sub(r"\s+", " ", text.strip().lower())
        if len(norm) < k:
            return {norm}
        return {norm[i : i + k] for i in range(len(norm) - k + 1)}

    train_shingles = [get_shingles(d.text) for d in train_docs]
    val_shingles = [get_shingles(d.text) for d in val_docs]

    # Sample check across validation set with mathematical upper-bound pruning
    for vi, vs in enumerate(val_shingles):
        len_vs = len(vs)
        for ti, ts in enumerate(train_shingles):
            len_ts = len(ts)
            min_len = min(len_vs, len_ts)
            max_len = max(len_vs, len_ts)
            if min_len / max_len < 0.85:
                continue
            inter = len(vs & ts)
            if inter == 0:
                continue
            sim = inter / (len_vs + len_ts - inter)
            assert sim < 0.85, (
                f"Near-duplicate leakage: Val doc {val_docs[vi].doc_id} matches Train doc {train_docs[ti].doc_id} (sim={sim:.3f})"
            )


# =============================================================================
# 5. Prepared Dataset Pipeline & Manifest Integrity Tests
# =============================================================================


def test_prepared_dataset_manifest_and_tensors():
    """Verify prepared tensors exist and manifest matches tokenizer hash."""
    manifest_path = PREPARED_DIR / "manifest.json"
    train_pt = PREPARED_DIR / "train.pt"
    val_pt = PREPARED_DIR / "val.pt"

    assert manifest_path.exists(), f"Manifest missing at {manifest_path}"
    assert train_pt.exists(), f"train.pt missing at {train_pt}"
    assert val_pt.exists(), f"val.pt missing at {val_pt}"

    manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
    tok_json = TOKENIZER_DIR / "tokenizer.json"
    expected_tok_hash = compute_file_sha256(tok_json)

    assert manifest_data.get("tokenizer_hash") == expected_tok_hash, (
        f"Manifest tokenizer hash mismatch: {manifest_data.get('tokenizer_hash')} vs {expected_tok_hash}"
    )

    # Check tensors
    train_tensor = torch.load(train_pt, weights_only=True)
    val_tensor = torch.load(val_pt, weights_only=True)

    assert isinstance(train_tensor, torch.Tensor)
    assert isinstance(val_tensor, torch.Tensor)
    assert train_tensor.ndim == 2 and train_tensor.shape[1] == 512
    assert val_tensor.ndim == 2 and val_tensor.shape[1] == 512
    assert train_tensor.dtype == torch.int64
    assert val_tensor.dtype == torch.int64
    assert train_tensor.shape[0] >= 200, f"Expected >= 200 packed sequences in train, got {train_tensor.shape[0]}"
    assert val_tensor.shape[0] >= 20, f"Expected >= 20 packed sequences in val, got {val_tensor.shape[0]}"


def test_deterministic_partitioning_reproducibility(all_documents: list[dict]):
    """Verify that partitioning with identical inputs and seeds produces byte-identical splits."""
    corpus_docs_1 = [
        CorpusDocument(
            doc_id=d["doc_id"],
            section_title=d["section_title"],
            source_id=d["source_id"],
            topic_domain=d["topic_domain"],
            text=d["text"],
            group_id=d["group_id"],
        )
        for d in all_documents
    ]
    corpus_docs_2 = [
        CorpusDocument(
            doc_id=d["doc_id"],
            section_title=d["section_title"],
            source_id=d["source_id"],
            topic_domain=d["topic_domain"],
            text=d["text"],
            group_id=d["group_id"],
        )
        for d in all_documents
    ]

    r1, _, _ = detect_duplicates_and_group(corpus_docs_1, near_dup_threshold=0.85)
    r2, _, _ = detect_duplicates_and_group(corpus_docs_2, near_dup_threshold=0.85)

    t1, v1 = partition_documents_by_group(r1, val_ratio=0.15, seed=42)
    t2, v2 = partition_documents_by_group(r2, val_ratio=0.15, seed=42)

    assert [d.doc_id for d in t1] == [d.doc_id for d in t2]
    assert [d.doc_id for d in v1] == [d.doc_id for d in v2]


# =============================================================================
# 6. Safety Caveat & Medical Advice Boundary Tests
# =============================================================================


def test_corpus_contains_educational_disclaimers(all_documents: list[dict]):
    """Verify that scope of practice and non-clinical advice boundaries are maintained."""
    scope_docs = [d for d in all_documents if "SCOPE" in d.get("group_id", "") or "P7_17" in d["doc_id"]]
    assert len(scope_docs) >= 1, "Must contain document specifying scope of practice boundaries"
    combined_scope_text = " ".join(d["text"] for d in scope_docs).lower()

    assert "medical advice" in combined_scope_text
    assert "educational" in combined_scope_text
    assert "physician" in combined_scope_text or "professional" in combined_scope_text
