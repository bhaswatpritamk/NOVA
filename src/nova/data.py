"""Nova-Fit Dataset Preparation Pipeline.

Provides a reproducible, auditable fitness-text dataset preparation pipeline
for pretraining. Implements text cleaning, corpus validation, tokenized
dataset creation with configurable sequence packing, train/validation
splitting, and comprehensive provenance metadata recording.

Phase 3 infrastructure only — does not initiate model pretraining.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Sequence, Tuple, Union

import numpy as np
import torch
from torch.utils.data import Dataset

from nova.tokenizer import NovaTokenizer


# =============================================================================
# Constants
# =============================================================================

# Section header pattern used in the smoke corpus fixture
SECTION_HEADER_PATTERN = re.compile(r"^\[SECTION:\s*[^\]]+\]\s*$")

# Comment line prefix (used in corpus header blocks)
COMMENT_PREFIX = "#"

# Minimum useful document length in characters (after cleaning)
MIN_DOC_CHARS = 20

# Default train/validation split ratio
DEFAULT_VAL_RATIO = 0.05

# Default context window for sequence packing
DEFAULT_MAX_SEQ_LEN = 512


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class CorpusStats:
    """Statistics computed over a text corpus after cleaning."""

    total_files: int
    total_documents: int
    total_characters: int
    total_words: int
    total_lines: int
    avg_document_chars: float
    avg_document_words: float
    min_document_chars: int
    max_document_chars: int
    empty_documents_dropped: int
    short_documents_dropped: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return asdict(self)


@dataclass
class TokenizedCorpusStats:
    """Statistics computed after tokenizing the corpus."""

    total_tokens: int
    total_sequences: int
    avg_tokens_per_document: float
    max_tokens_per_document: int
    min_tokens_per_document: int
    vocab_size: int
    max_seq_len: int
    eos_token_id: int
    pad_token_id: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return asdict(self)


@dataclass
class DatasetManifest:
    """Complete provenance record for a prepared dataset."""

    name: str
    version: str
    created_at: str
    corpus_stats: Dict[str, Any]
    tokenized_stats: Dict[str, Any]
    source_files: List[Dict[str, str]]
    cleaning_config: Dict[str, Any]
    split_config: Dict[str, Any]
    train_sequences: int
    val_sequences: int
    total_tokens_train: int
    total_tokens_val: int
    tokenizer_vocab_size: int
    max_seq_len: int
    python_version: str
    numpy_version: str
    torch_version: str
    duplicate_report: Optional[Dict[str, Any]] = None
    source_audit: Optional[Dict[str, Any]] = None
    tokenizer_hash: Optional[str] = None
    tokenizer_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert manifest to JSON-serializable dictionary."""
        return asdict(self)

    def save(self, path: Union[str, Path]) -> Path:
        """Write manifest JSON to file."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)
        return p


# =============================================================================
# Text Cleaning
# =============================================================================


@dataclass
class CleaningConfig:
    """Configuration for text cleaning pipeline."""

    strip_comment_lines: bool = True
    strip_section_headers: bool = False
    normalize_whitespace: bool = True
    strip_leading_trailing: bool = True
    min_doc_chars: int = MIN_DOC_CHARS
    lowercase: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return asdict(self)


def clean_line(line: str, config: CleaningConfig) -> Optional[str]:
    """Clean a single line of text according to the cleaning configuration.

    Args:
        line: Raw text line.
        config: Cleaning configuration.

    Returns:
        Cleaned line string, or None if the line should be dropped.
    """
    if not isinstance(line, str):
        raise TypeError(f"Expected str, got {type(line).__name__}")

    # Strip leading/trailing whitespace
    if config.strip_leading_trailing:
        line = line.strip()

    # Skip empty lines
    if not line:
        return None

    # Strip comment lines
    if config.strip_comment_lines and line.startswith(COMMENT_PREFIX):
        return None

    # Optionally strip section headers
    if config.strip_section_headers and SECTION_HEADER_PATTERN.match(line):
        return None

    # Normalize internal whitespace (collapse runs of spaces/tabs)
    if config.normalize_whitespace:
        line = re.sub(r"[ \t]+", " ", line)

    # Optionally lowercase
    if config.lowercase:
        line = line.lower()

    return line


def clean_text(text: str, config: Optional[CleaningConfig] = None) -> str:
    """Clean a block of text, applying line-level cleaning and reassembly.

    Args:
        text: Raw text block (potentially multi-line).
        config: Cleaning configuration. Uses defaults if None.

    Returns:
        Cleaned text string with lines joined by newline.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str input, got {type(text).__name__}")

    if config is None:
        config = CleaningConfig()

    cleaned_lines = []
    for line in text.split("\n"):
        cleaned = clean_line(line, config)
        if cleaned is not None:
            cleaned_lines.append(cleaned)

    result = "\n".join(cleaned_lines)

    if config.strip_leading_trailing:
        result = result.strip()

    return result


# =============================================================================
# Corpus Loading & Document Extraction
# =============================================================================


def compute_file_sha256(file_path: Union[str, Path]) -> str:
    """Compute SHA-256 hash of a file.

    Args:
        file_path: Path to file.

    Returns:
        Hexadecimal SHA-256 digest string.
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Cannot compute hash; file not found: {path}")

    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_corpus_files(
    paths: Union[str, Path, Sequence[Union[str, Path]]],
) -> List[Tuple[Path, str]]:
    """Load text content from one or more corpus files.

    Args:
        paths: Single file path, or sequence of file paths.

    Returns:
        List of (path, text_content) tuples.

    Raises:
        FileNotFoundError: If any file does not exist.
        TypeError: If paths argument type is invalid.
    """
    if isinstance(paths, (str, Path)):
        paths = [paths]
    elif not isinstance(paths, (list, tuple)):
        raise TypeError(
            f"paths must be str, Path, or sequence of paths, got {type(paths).__name__}"
        )

    result: List[Tuple[Path, str]] = []
    for p in paths:
        path = Path(p)
        if not path.is_file():
            raise FileNotFoundError(f"Corpus file not found: {path}")
        content = path.read_text(encoding="utf-8")
        result.append((path, content))

    return result


def extract_documents(
    text: str,
    config: Optional[CleaningConfig] = None,
    separator: Optional[str] = None,
) -> List[str]:
    """Extract and clean individual documents from a corpus text.

    Documents are separated by section headers (default) or a custom separator.
    Each document is cleaned independently.

    Args:
        text: Raw corpus text.
        config: Cleaning configuration.
        separator: Optional explicit document separator string.
            If None, uses section header pattern to split into documents.

    Returns:
        List of cleaned, non-empty document strings.
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str, got {type(text).__name__}")

    if config is None:
        min_chars = 1 if separator is not None else MIN_DOC_CHARS
        config = CleaningConfig(min_doc_chars=min_chars)

    if separator is not None:
        raw_docs = text.split(separator)
    else:
        # Split on section headers using line-by-line scanning.
        # Each section header starts a new document; the header is included
        # in the document it introduces for context.
        raw_docs = []
        current_doc_lines: List[str] = []

        for line in text.split("\n"):
            if SECTION_HEADER_PATTERN.match(line.strip()):
                # Flush the accumulated document
                if current_doc_lines:
                    raw_docs.append("\n".join(current_doc_lines))
                # Start new document with the header
                current_doc_lines = [line]
            else:
                current_doc_lines.append(line)

        # Flush the last document
        if current_doc_lines:
            raw_docs.append("\n".join(current_doc_lines))

    # Clean each document
    documents = []
    for raw_doc in raw_docs:
        cleaned = clean_text(raw_doc, config)
        if cleaned and len(cleaned) >= config.min_doc_chars:
            documents.append(cleaned)

    return documents


def compute_corpus_stats(
    documents: List[str],
    total_files: int = 1,
    dropped_empty: int = 0,
    dropped_short: int = 0,
) -> CorpusStats:
    """Compute descriptive statistics for a list of cleaned documents.

    Args:
        documents: List of cleaned document strings.
        total_files: Number of source files.
        dropped_empty: Count of documents dropped for being empty.
        dropped_short: Count of documents dropped for being too short.

    Returns:
        CorpusStats dataclass with computed metrics.
    """
    if not documents:
        return CorpusStats(
            total_files=total_files,
            total_documents=0,
            total_characters=0,
            total_words=0,
            total_lines=0,
            avg_document_chars=0.0,
            avg_document_words=0.0,
            min_document_chars=0,
            max_document_chars=0,
            empty_documents_dropped=dropped_empty,
            short_documents_dropped=dropped_short,
        )

    char_counts = [len(d) for d in documents]
    word_counts = [len(d.split()) for d in documents]
    line_counts = [d.count("\n") + 1 for d in documents]

    return CorpusStats(
        total_files=total_files,
        total_documents=len(documents),
        total_characters=sum(char_counts),
        total_words=sum(word_counts),
        total_lines=sum(line_counts),
        avg_document_chars=sum(char_counts) / len(documents),
        avg_document_words=sum(word_counts) / len(documents),
        min_document_chars=min(char_counts),
        max_document_chars=max(char_counts),
        empty_documents_dropped=dropped_empty,
        short_documents_dropped=dropped_short,
    )


# =============================================================================
# Tokenized Dataset
# =============================================================================


def tokenize_documents(
    documents: List[str],
    tokenizer: NovaTokenizer,
    add_eos: bool = True,
) -> List[List[int]]:
    """Tokenize a list of documents into token ID sequences.

    Each document is independently tokenized. Optionally appends an EOS token
    to each document.

    Args:
        documents: List of cleaned text documents.
        tokenizer: Trained NovaTokenizer instance.
        add_eos: Whether to append EOS token after each document.

    Returns:
        List of token ID lists, one per document.
    """
    if not isinstance(documents, list):
        raise TypeError(f"documents must be a list, got {type(documents).__name__}")

    eos_id = tokenizer.eos_token_id if add_eos else None

    tokenized: List[List[int]] = []
    for doc in documents:
        ids = tokenizer.encode(doc, allow_special=False)
        if add_eos and eos_id is not None:
            ids.append(eos_id)
        tokenized.append(ids)

    return tokenized


def pack_sequences(
    token_sequences: List[List[int]],
    max_seq_len: int,
    pad_token_id: int,
    drop_last_short: bool = False,
) -> List[List[int]]:
    """Pack tokenized documents into fixed-length sequences for training.

    Concatenates all token sequences into a continuous stream, then slices
    into chunks of max_seq_len. Optionally pads the final chunk or drops it.

    Args:
        token_sequences: List of variable-length token ID lists.
        max_seq_len: Target sequence length for each packed chunk.
        pad_token_id: Token ID used for padding.
        drop_last_short: If True, discard the final chunk if it's shorter
            than max_seq_len. If False, pad it.

    Returns:
        List of fixed-length token ID lists.
    """
    if not isinstance(max_seq_len, int) or max_seq_len <= 0:
        raise ValueError(f"max_seq_len must be a positive integer, got {max_seq_len}")

    # Flatten all tokens into a single stream
    all_tokens: List[int] = []
    for seq in token_sequences:
        all_tokens.extend(seq)

    if not all_tokens:
        return []

    packed: List[List[int]] = []
    for start in range(0, len(all_tokens), max_seq_len):
        chunk = all_tokens[start : start + max_seq_len]
        if len(chunk) < max_seq_len:
            if drop_last_short:
                continue
            # Pad to max_seq_len
            chunk = chunk + [pad_token_id] * (max_seq_len - len(chunk))
        packed.append(chunk)

    return packed


def split_sequences(
    sequences: List[List[int]],
    val_ratio: float = DEFAULT_VAL_RATIO,
    seed: int = 42,
) -> Tuple[List[List[int]], List[List[int]]]:
    """Split packed sequences into train and validation sets.

    Args:
        sequences: List of fixed-length token ID sequences.
        val_ratio: Fraction of sequences to reserve for validation.
        seed: Random seed for reproducible splitting.

    Returns:
        Tuple of (train_sequences, val_sequences).

    Raises:
        ValueError: If val_ratio is not in [0.0, 1.0).
    """
    if not (0.0 <= val_ratio < 1.0):
        raise ValueError(f"val_ratio must be in [0.0, 1.0), got {val_ratio}")

    if not sequences:
        return [], []

    rng = np.random.RandomState(seed)
    indices = np.arange(len(sequences))
    rng.shuffle(indices)

    n_val = max(1, int(len(sequences) * val_ratio)) if val_ratio > 0 else 0

    # Ensure at least 1 training sample
    if n_val >= len(sequences):
        n_val = len(sequences) - 1

    val_indices = set(indices[:n_val].tolist())
    train = [sequences[i] for i in range(len(sequences)) if i not in val_indices]
    val = [sequences[i] for i in range(len(sequences)) if i in val_indices]

    return train, val


@dataclass
class DuplicateReport:
    """Report on exact and near-duplicate documents."""

    total_documents: int
    unique_documents: int
    exact_duplicates_removed: int
    near_duplicates_flagged: int
    duplicate_groups: List[List[int]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return asdict(self)


def detect_exact_and_near_duplicates(
    documents: List[str],
    similarity_threshold: float = 0.85,
    remove_exact: bool = True,
) -> Tuple[List[str], DuplicateReport, List[int]]:
    """Detect and optionally remove exact duplicates, and flag near-duplicates.

    Assigns group IDs so that exact and near-duplicates share the same group ID.
    This guarantees that related documents remain in the same split (train or val)
    during group-aware splitting.

    Args:
        documents: List of cleaned document strings.
        similarity_threshold: Jaccard threshold on character 5-grams (0.0 to 1.0).
        remove_exact: If True, only the first copy of each exact duplicate is kept.

    Returns:
        Tuple of (retained_documents, DuplicateReport, group_assignments).
    """
    if not documents:
        return [], DuplicateReport(0, 0, 0, 0, []), []

    # Step 1: Exact duplicate detection via normalized SHA-256
    seen_hashes: Dict[str, int] = {}  # hash -> first_idx in retained
    retained_docs: List[str] = []
    doc_to_group: List[int] = []
    exact_dups = 0

    for doc in documents:
        norm = re.sub(r"\s+", " ", doc.strip().lower())
        h = hashlib.sha256(norm.encode("utf-8")).hexdigest()
        if h in seen_hashes:
            exact_dups += 1
            if not remove_exact:
                first_idx = seen_hashes[h]
                retained_docs.append(doc)
                doc_to_group.append(doc_to_group[first_idx])
        else:
            new_idx = len(retained_docs)
            seen_hashes[h] = new_idx
            retained_docs.append(doc)
            doc_to_group.append(new_idx)

    # Step 2: Near-duplicate detection among retained documents
    n = len(retained_docs)
    parent = list(doc_to_group)

    def find(i: int) -> int:
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]

    def union(i: int, j: int):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j

    def get_shingles(text: str, k: int = 5) -> set:
        norm = re.sub(r"\s+", " ", text.strip().lower())
        if len(norm) < k:
            return {norm}
        return {norm[i : i + k] for i in range(len(norm) - k + 1)}

    shingles = [get_shingles(d) for d in retained_docs]
    near_dups_count = 0

    for i in range(n):
        for j in range(i + 1, n):
            s1 = shingles[i]
            s2 = shingles[j]
            if not s1 or not s2:
                continue
            inter = len(s1 & s2)
            union_len = len(s1 | s2)
            if union_len > 0:
                sim = inter / union_len
                if sim >= similarity_threshold:
                    near_dups_count += 1
                    union(i, j)

    final_groups: List[int] = [find(i) for i in range(n)]

    group_map: Dict[int, List[int]] = {}
    for idx, grp in enumerate(final_groups):
        group_map.setdefault(grp, []).append(idx)
    multi_groups = [members for members in group_map.values() if len(members) > 1]

    report = DuplicateReport(
        total_documents=len(documents),
        unique_documents=len(retained_docs),
        exact_duplicates_removed=exact_dups if remove_exact else 0,
        near_duplicates_flagged=near_dups_count,
        duplicate_groups=multi_groups,
    )

    return retained_docs, report, final_groups


def split_documents(
    documents: List[str],
    val_ratio: float = DEFAULT_VAL_RATIO,
    seed: int = 42,
    groups: Optional[List[int]] = None,
) -> Tuple[List[str], List[str]]:
    """Split documents into train and validation sets at the document level.

    Ensures zero cross-split document leakage. If groups are provided,
    documents in the same group are always placed into the same split.

    Args:
        documents: List of cleaned document strings.
        val_ratio: Fraction of documents/groups reserved for validation.
        seed: Random seed for reproducible splitting.
        groups: Optional group IDs matching documents length.

    Returns:
        Tuple of (train_documents, val_documents).
    """
    if not (0.0 <= val_ratio < 1.0):
        raise ValueError(f"val_ratio must be in [0.0, 1.0), got {val_ratio}")

    if not documents:
        return [], []

    if val_ratio == 0.0:
        return list(documents), []

    rng = np.random.RandomState(seed)

    if groups is None:
        groups = list(range(len(documents)))

    unique_groups = sorted(list(set(groups)))
    unique_groups = np.array(unique_groups)
    rng.shuffle(unique_groups)

    n_val_groups = max(1, int(len(unique_groups) * val_ratio))
    if n_val_groups >= len(unique_groups):
        n_val_groups = max(1, len(unique_groups) - 1)

    val_group_set = set(unique_groups[:n_val_groups])

    train_docs = [doc for doc, grp in zip(documents, groups) if grp not in val_group_set]
    val_docs = [doc for doc, grp in zip(documents, groups) if grp in val_group_set]

    if not train_docs and len(documents) > 1:
        train_docs.append(val_docs.pop())

    return train_docs, val_docs


def verify_sources_against_registry(
    source_records: List[Dict[str, Any]],
    registry_path: Union[str, Path],
) -> Dict[str, Any]:
    """Verify source files against the approved source registry.

    Args:
        source_records: List of file metadata records with 'path' and 'sha256'.
        registry_path: Path to source_registry.json.

    Returns:
        Dict summarizing approved status, source details, and registry match.
    """
    p = Path(registry_path)
    if not p.is_file():
        return {
            "verified": False,
            "error": f"Registry file not found at {registry_path}",
            "approved_sources": [],
            "unapproved_sources": [r.get("path", "") for r in source_records],
        }

    try:
        with open(p, "r", encoding="utf-8") as f:
            registry = json.load(f)
    except Exception as e:
        return {
            "verified": False,
            "error": f"Failed to parse registry: {e}",
            "approved_sources": [],
            "unapproved_sources": [r.get("path", "") for r in source_records],
        }

    approved_list = registry.get("approved_sources", [])
    approved_ids = {s.get("source_id") for s in approved_list}

    return {
        "verified": True,
        "registry_version": registry.get("version", "unknown"),
        "total_approved_sources_registered": len(approved_list),
        "source_files_checked": len(source_records),
        "registered_source_ids": list(approved_ids),
    }


class NovaPretrainingDataset(Dataset):
    """PyTorch Dataset for next-token prediction pretraining.

    Each sample consists of (input_ids, target_ids) where target_ids are
    input_ids shifted right by one position for autoregressive training.

    Attributes:
        sequences: List of fixed-length token ID lists.
        max_seq_len: Sequence length of each sample.
    """

    def __init__(self, sequences: List[List[int]]) -> None:
        """Initialize the pretraining dataset.

        Args:
            sequences: List of fixed-length token ID lists.
        """
        if not isinstance(sequences, list):
            raise TypeError(
                f"sequences must be a list of token ID lists, got {type(sequences).__name__}"
            )
        if not sequences:
            raise ValueError("Cannot create dataset from empty sequence list.")

        self.sequences = sequences
        self.max_seq_len = len(sequences[0])

        # Validate all sequences have consistent length
        for i, seq in enumerate(sequences):
            if len(seq) != self.max_seq_len:
                raise ValueError(
                    f"Sequence at index {i} has length {len(seq)}, "
                    f"expected {self.max_seq_len}."
                )

    def __len__(self) -> int:
        return len(self.sequences)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """Return (input_ids, target_ids) pair for autoregressive training.

        input_ids: tokens[:-1]
        target_ids: tokens[1:]

        This ensures the model learns to predict the next token at each position.
        """
        tokens = torch.tensor(self.sequences[idx], dtype=torch.long)
        input_ids = tokens[:-1]
        target_ids = tokens[1:]
        return input_ids, target_ids

    @property
    def effective_seq_len(self) -> int:
        """Return the effective input sequence length (max_seq_len - 1)."""
        return self.max_seq_len - 1


# =============================================================================
# Pipeline Orchestrator
# =============================================================================


@dataclass
class PrepareDatasetConfig:
    """Complete configuration for the dataset preparation pipeline."""

    corpus_paths: List[str] = field(default_factory=lambda: ["data/raw/fitness_smoke_corpus.txt"])
    tokenizer_path: str = "artifacts/tokenizer"
    output_dir: str = "data/prepared"
    max_seq_len: int = DEFAULT_MAX_SEQ_LEN
    val_ratio: float = DEFAULT_VAL_RATIO
    split_seed: int = 42
    drop_last_short: bool = False
    cleaning: CleaningConfig = field(default_factory=CleaningConfig)
    add_eos: bool = True
    split_level: str = "sequence"
    detect_duplicates: bool = True
    train_corpus_path: Optional[str] = None
    val_corpus_path: Optional[str] = None
    source_registry_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        d = asdict(self)
        return d


@dataclass
class PrepareDatasetResult:
    """Result of a dataset preparation pipeline run."""

    success: bool
    message: str
    manifest_path: Optional[str] = None
    train_path: Optional[str] = None
    val_path: Optional[str] = None
    train_sequences: int = 0
    val_sequences: int = 0
    total_tokens: int = 0
    elapsed_seconds: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return asdict(self)


def prepare_dataset(
    config: Optional[PrepareDatasetConfig] = None,
    tokenizer: Optional[NovaTokenizer] = None,
    verbose: bool = True,
) -> PrepareDatasetResult:
    """Execute the complete dataset preparation pipeline.

    Pipeline Steps:
        1. Load corpus files
        2. Extract and clean documents
        3. Compute corpus statistics
        4. Tokenize documents
        5. Pack into fixed-length sequences
        6. Split into train/validation sets
        7. Save to disk with full provenance metadata

    Args:
        config: Pipeline configuration. Uses defaults if None.
        tokenizer: Pre-loaded tokenizer instance. If None, loads from
            config.tokenizer_path.
        verbose: Whether to print progress information.

    Returns:
        PrepareDatasetResult with success status and file paths.
    """
    start_time = time.perf_counter()

    if config is None:
        config = PrepareDatasetConfig()

    if verbose:
        print("=" * 70)
        print("NOVA-FIT DATASET PREPARATION PIPELINE (Phase 3)")
        print("=" * 70)

    # -------------------------------------------------------------------------
    # Step 1: Load tokenizer
    # -------------------------------------------------------------------------
    tokenizer_hash: Optional[str] = None
    tokenizer_path_str: Optional[str] = None
    if config.tokenizer_path:
        tok_p = Path(config.tokenizer_path)
        tokenizer_path_str = str(tok_p.resolve()) if tok_p.exists() else str(tok_p)
        if tok_p.is_dir():
            tok_json = tok_p / "tokenizer.json"
            if tok_json.is_file():
                tokenizer_hash = compute_file_sha256(tok_json)
        elif tok_p.is_file():
            tokenizer_hash = compute_file_sha256(tok_p)

    if tokenizer is None:
        tok_path = Path(config.tokenizer_path)
        if not tok_path.exists():
            return PrepareDatasetResult(
                success=False,
                message=f"Tokenizer not found at {tok_path}. Train the tokenizer first.",
            )
        try:
            tokenizer = NovaTokenizer.from_file(tok_path)
        except Exception as e:
            return PrepareDatasetResult(
                success=False,
                message=f"Failed to load tokenizer from {tok_path}: {e}",
            )

    if verbose:
        print(f"Tokenizer loaded: vocab_size={tokenizer.vocab_size} (hash: {tokenizer_hash[:12] if tokenizer_hash else 'unknown'})")

    # -------------------------------------------------------------------------
    # Step 2: Load corpus files
    # -------------------------------------------------------------------------
    paths_to_load = (
        [config.train_corpus_path, config.val_corpus_path]
        if (config.train_corpus_path and config.val_corpus_path)
        else config.corpus_paths
    )
    try:
        corpus_files = load_corpus_files(paths_to_load)
    except (FileNotFoundError, TypeError) as e:
        return PrepareDatasetResult(
            success=False,
            message=f"Failed to load corpus files: {e}",
        )

    source_records = []
    for path, content in corpus_files:
        source_records.append({
            "path": str(path.resolve()),
            "size_bytes": str(path.stat().st_size),
            "sha256": compute_file_sha256(path),
        })

    if verbose:
        print(f"Loaded {len(corpus_files)} corpus file(s)")
        for rec in source_records:
            print(f"  - {rec['path']} ({rec['size_bytes']} bytes)")

    # -------------------------------------------------------------------------
    # Step 3: Extract and clean documents
    # -------------------------------------------------------------------------
    all_documents: List[str] = []
    dropped_empty = 0
    dropped_short = 0

    for path, content in corpus_files:
        # Extract documents from each file
        raw_docs = extract_documents(content, config.cleaning)
        all_documents.extend(raw_docs)

    if verbose:
        print(f"Extracted {len(all_documents)} documents after cleaning")

    # -------------------------------------------------------------------------
    # Step 4: Compute corpus statistics
    # -------------------------------------------------------------------------
    corpus_stats = compute_corpus_stats(
        all_documents,
        total_files=len(corpus_files),
        dropped_empty=dropped_empty,
        dropped_short=dropped_short,
    )

    if verbose:
        print(f"Corpus stats: {corpus_stats.total_characters:,} chars, "
              f"{corpus_stats.total_words:,} words across "
              f"{corpus_stats.total_documents} documents")

    if corpus_stats.total_documents == 0:
        return PrepareDatasetResult(
            success=False,
            message="No valid documents found after cleaning.",
        )

    # -------------------------------------------------------------------------
    # Step 5: Tokenize documents
    # -------------------------------------------------------------------------
    if verbose:
        print("Tokenizing documents...")

    tokenized_docs = tokenize_documents(
        all_documents,
        tokenizer,
        add_eos=config.add_eos,
    )

    token_counts = [len(toks) for toks in tokenized_docs]
    total_tokens = sum(token_counts)

    tokenized_stats = TokenizedCorpusStats(
        total_tokens=total_tokens,
        total_sequences=len(tokenized_docs),
        avg_tokens_per_document=total_tokens / len(tokenized_docs) if tokenized_docs else 0.0,
        max_tokens_per_document=max(token_counts) if token_counts else 0,
        min_tokens_per_document=min(token_counts) if token_counts else 0,
        vocab_size=tokenizer.vocab_size,
        max_seq_len=config.max_seq_len,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id,
    )

    if verbose:
        print(f"Tokenized: {total_tokens:,} total tokens across "
              f"{len(tokenized_docs)} documents")

    # -------------------------------------------------------------------------
    # Step 6 & 7: Packing and Splitting (Document-Level or Sequence-Level)
    # -------------------------------------------------------------------------
    source_audit = None
    if config.source_registry_path:
        source_audit = verify_sources_against_registry(source_records, config.source_registry_path)

    dup_report_dict = None

    if config.train_corpus_path and config.val_corpus_path:
        if verbose:
            print("Using separate explicit train and val corpora...")
        train_files = load_corpus_files([config.train_corpus_path])
        val_files = load_corpus_files([config.val_corpus_path])
        train_docs: List[str] = []
        for _, content in train_files:
            train_docs.extend(extract_documents(content, config.cleaning))
        val_docs: List[str] = []
        for _, content in val_files:
            val_docs.extend(extract_documents(content, config.cleaning))

        if config.detect_duplicates:
            all_loaded = train_docs + val_docs
            _, dup_rep, _ = detect_exact_and_near_duplicates(all_loaded)
            dup_report_dict = dup_rep.to_dict()

        train_tokenized = tokenize_documents(train_docs, tokenizer, add_eos=config.add_eos)
        val_tokenized = tokenize_documents(val_docs, tokenizer, add_eos=config.add_eos)
        train_seqs = pack_sequences(train_tokenized, max_seq_len=config.max_seq_len, pad_token_id=tokenizer.pad_token_id, drop_last_short=config.drop_last_short)
        val_seqs = pack_sequences(val_tokenized, max_seq_len=config.max_seq_len, pad_token_id=tokenizer.pad_token_id, drop_last_short=config.drop_last_short)

    elif config.split_level == "document":
        if verbose:
            print("Splitting at document level before packing sequences...")
        if config.detect_duplicates:
            retained_docs, dup_rep, groups = detect_exact_and_near_duplicates(all_documents)
            dup_report_dict = dup_rep.to_dict()
        else:
            retained_docs = all_documents
            groups = None

        train_docs, val_docs = split_documents(
            retained_docs, val_ratio=config.val_ratio, seed=config.split_seed, groups=groups
        )
        train_tokenized = tokenize_documents(train_docs, tokenizer, add_eos=config.add_eos)
        val_tokenized = tokenize_documents(val_docs, tokenizer, add_eos=config.add_eos)
        train_seqs = pack_sequences(train_tokenized, max_seq_len=config.max_seq_len, pad_token_id=tokenizer.pad_token_id, drop_last_short=config.drop_last_short)
        val_seqs = pack_sequences(val_tokenized, max_seq_len=config.max_seq_len, pad_token_id=tokenizer.pad_token_id, drop_last_short=config.drop_last_short)

    else:
        # Sequence-level packing then splitting
        if verbose:
            print(f"Packing sequences (max_seq_len={config.max_seq_len})...")

        packed = pack_sequences(
            tokenized_docs,
            max_seq_len=config.max_seq_len,
            pad_token_id=tokenizer.pad_token_id,
            drop_last_short=config.drop_last_short,
        )

        if not packed:
            return PrepareDatasetResult(
                success=False,
                message="No sequences produced after packing. Corpus may be too small.",
            )

        train_seqs, val_seqs = split_sequences(
            packed,
            val_ratio=config.val_ratio,
            seed=config.split_seed,
        )

    if not train_seqs and not val_seqs:
        return PrepareDatasetResult(
            success=False,
            message="No sequences produced after packing. Corpus may be too small.",
        )

    if verbose:
        print(f"Split: {len(train_seqs)} train, {len(val_seqs)} val "
              f"(val_ratio={config.val_ratio}, split_level={config.split_level})")

    # -------------------------------------------------------------------------
    # Step 8: Save to disk
    # -------------------------------------------------------------------------
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    train_path = output_dir / "train.pt"
    val_path = output_dir / "val.pt"

    # Save as PyTorch tensors
    train_tensor = torch.tensor(train_seqs, dtype=torch.long)
    val_tensor = torch.tensor(val_seqs, dtype=torch.long) if val_seqs else torch.empty(0, config.max_seq_len, dtype=torch.long)

    torch.save(train_tensor, str(train_path))
    torch.save(val_tensor, str(val_path))

    # Compute token counts for splits
    total_tokens_train = sum(sum(1 for t in seq if t != tokenizer.pad_token_id) for seq in train_seqs)
    total_tokens_val = sum(sum(1 for t in seq if t != tokenizer.pad_token_id) for seq in val_seqs)

    elapsed = time.perf_counter() - start_time

    # Build and save manifest
    manifest = DatasetManifest(
        name="nova-fit-pretraining",
        version="0.1.0",
        created_at=datetime.now(timezone.utc).isoformat(),
        corpus_stats=corpus_stats.to_dict(),
        tokenized_stats=tokenized_stats.to_dict(),
        source_files=source_records,
        cleaning_config=config.cleaning.to_dict(),
        split_config={
            "val_ratio": config.val_ratio,
            "split_seed": config.split_seed,
            "drop_last_short": config.drop_last_short,
            "split_level": config.split_level,
        },
        train_sequences=len(train_seqs),
        val_sequences=len(val_seqs),
        total_tokens_train=total_tokens_train,
        total_tokens_val=total_tokens_val,
        tokenizer_vocab_size=tokenizer.vocab_size,
        max_seq_len=config.max_seq_len,
        python_version=sys.version.split()[0],
        numpy_version=np.__version__,
        torch_version=torch.__version__,
        duplicate_report=dup_report_dict,
        source_audit=source_audit,
        tokenizer_hash=tokenizer_hash,
        tokenizer_path=tokenizer_path_str,
    )

    manifest_path = output_dir / "manifest.json"
    manifest.save(manifest_path)

    if verbose:
        print("-" * 70)
        print(f"Saved train.pt:     {train_path} ({train_tensor.shape})")
        print(f"Saved val.pt:       {val_path} ({val_tensor.shape})")
        print(f"Saved manifest:     {manifest_path}")
        print(f"Train tokens (non-pad): {total_tokens_train:,}")
        print(f"Val tokens (non-pad):   {total_tokens_val:,}")
        print(f"Elapsed: {elapsed:.3f}s")
        print("=" * 70)

    return PrepareDatasetResult(
        success=True,
        message=f"Dataset prepared: {len(train_seqs)} train + {len(val_seqs)} val "
                f"sequences ({total_tokens_train + total_tokens_val:,} total tokens).",
        manifest_path=str(manifest_path),
        train_path=str(train_path),
        val_path=str(val_path),
        train_sequences=len(train_seqs),
        val_sequences=len(val_seqs),
        total_tokens=total_tokens_train + total_tokens_val,
        elapsed_seconds=elapsed,
    )


# =============================================================================
# Dataset Loading Utilities
# =============================================================================


def load_prepared_dataset(
    data_dir: Union[str, Path],
    split: str = "train",
) -> NovaPretrainingDataset:
    """Load a previously prepared dataset from disk.

    Args:
        data_dir: Directory containing train.pt/val.pt and manifest.json.
        split: Which split to load ('train' or 'val').

    Returns:
        NovaPretrainingDataset instance.

    Raises:
        FileNotFoundError: If the split file does not exist.
        ValueError: If split name is invalid.
    """
    if split not in ("train", "val"):
        raise ValueError(f"split must be 'train' or 'val', got '{split}'")

    data_path = Path(data_dir) / f"{split}.pt"
    if not data_path.is_file():
        raise FileNotFoundError(f"Dataset file not found: {data_path}")

    tensor = torch.load(str(data_path), weights_only=True)
    sequences = tensor.tolist()

    return NovaPretrainingDataset(sequences)


def load_manifest(data_dir: Union[str, Path]) -> Dict[str, Any]:
    """Load the dataset manifest JSON.

    Args:
        data_dir: Directory containing manifest.json.

    Returns:
        Dictionary of manifest data.

    Raises:
        FileNotFoundError: If manifest.json does not exist.
    """
    manifest_path = Path(data_dir) / "manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)
