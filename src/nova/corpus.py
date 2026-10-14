"""Nova-Fit Corpus Expansion and Data Quality Engine.

Implements the repeatable acquisition, legal verification, text extraction,
exact/near deduplication, group-aware partitioning, and auditing workflows
for Phase 6 corpus expansion.

Maintains provenance, attribution requirements, and strict separation between
training and validation corpora with zero document leakage.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Sequence, Set, Tuple, Union

from nova.tokenizer import NovaTokenizer


# =============================================================================
# Topic Domains (7 Core Pillars of Nova-Fit)
# =============================================================================

TOPIC_DOMAINS: Dict[str, str] = {
    "exercise_science_biomechanics": "1. Exercise science, physiology, and biomechanics",
    "strength_training_programming": "2. Strength training principles and programming",
    "exercise_technique_safety": "3. Exercise technique and safe equipment use",
    "nutrition_fundamentals_hydration": "4. Nutrition fundamentals and hydration",
    "sleep_recovery_physical_activity": "5. Sleep, recovery, and physical activity",
    "training_adaptations_fatigue_load": "6. Training adaptations, fatigue, and load management",
    "general_fitness_education_safety": "7. General fitness education and age-appropriate safety",
}

SECTION_HEADER_RE = re.compile(r"^\[SECTION:\s*([^\]]+)\]\s*$", re.MULTILINE)
SOURCE_TAG_RE = re.compile(r"^\[SOURCE:\s*([^\]]+)\]\s*$", re.MULTILINE)


# =============================================================================
# Source Provenance & Registry
# =============================================================================


@dataclass
class SourceProvenanceRecord:
    """Legal provenance and attribution metadata for an approved source."""

    source_id: str
    title: str
    author: str
    publication_year: int
    license: str
    legal_basis: str
    commercial_use_permitted: bool = True
    attribution_required: bool = False
    attribution_text: str = ""
    url: str = ""
    acquisition_date: str = ""
    version: str = "1.0.0"
    raw_sha256: str = ""
    raw_bytes: int = 0
    domains: List[str] = field(default_factory=list)
    restrictions: str = ""
    third_party_exclusions: str = "Third-party figures, photographs, and external excerpts excluded."

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SourceProvenanceRecord:
        """Create record from dictionary with default fallbacks."""
        return cls(
            source_id=data["source_id"],
            title=data.get("title", ""),
            author=data.get("author", ""),
            publication_year=int(data.get("publication_year", 0)),
            license=data.get("license", "Public Domain"),
            legal_basis=data.get("legal_basis", "17 U.S.C. § 105"),
            commercial_use_permitted=bool(data.get("commercial_use_permitted", True)),
            attribution_required=bool(data.get("attribution_required", False)),
            attribution_text=data.get("attribution_text", ""),
            url=data.get("url", ""),
            acquisition_date=data.get("acquisition_date", "2026-10-14"),
            version=data.get("version", "1.0.0"),
            raw_sha256=data.get("raw_sha256", ""),
            raw_bytes=int(data.get("raw_bytes", 0)),
            domains=list(data.get("domains", [])),
            restrictions=data.get("restrictions", ""),
            third_party_exclusions=data.get(
                "third_party_exclusions",
                "Third-party figures, photographs, and external excerpts excluded.",
            ),
        )


class SourceRegistry:
    """Registry managing approved sources and legal provenance verification."""

    def __init__(self, sources: Optional[List[SourceProvenanceRecord]] = None, version: str = "2.0.0") -> None:
        self.version = version
        self.updated_at = datetime.now(timezone.utc).isoformat()
        self.sources: Dict[str, SourceProvenanceRecord] = {}
        if sources:
            for s in sources:
                self.sources[s.source_id] = s

    @classmethod
    def load(cls, path: Union[str, Path]) -> SourceRegistry:
        """Load registry from JSON file."""
        p = Path(path)
        if not p.is_file():
            raise FileNotFoundError(f"Source registry not found: {p}")
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        registry = cls(version=data.get("version", "2.0.0"))
        registry.updated_at = data.get("updated_at", registry.updated_at)
        for s_data in data.get("approved_sources", []):
            rec = SourceProvenanceRecord.from_dict(s_data)
            registry.sources[rec.source_id] = rec
        return registry

    def save(self, path: Union[str, Path]) -> None:
        """Save registry to JSON file."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": self.version,
            "project": "Nova-Fit",
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "approved_sources": [s.to_dict() for s in self.sources.values()],
        }
        with open(p, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def register(self, record: SourceProvenanceRecord) -> None:
        """Register or update an approved source."""
        self.sources[record.source_id] = record

    def get(self, source_id: str) -> Optional[SourceProvenanceRecord]:
        """Retrieve source provenance by ID."""
        return self.sources.get(source_id)

    def validate_file_hash(self, source_id: str, file_path: Union[str, Path]) -> bool:
        """Check if a file's SHA-256 matches its registered hash."""
        rec = self.get(source_id)
        if not rec or not rec.raw_sha256:
            return False
        p = Path(file_path)
        if not p.is_file():
            return False
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        return h.lower() == rec.raw_sha256.lower()


# =============================================================================
# Document Representation
# =============================================================================


@dataclass
class CorpusDocument:
    """Individual document within the training or validation corpus."""

    doc_id: str
    section_title: str
    source_id: str
    text: str
    topic_domain: str
    group_id: str
    char_count: int = 0
    word_count: int = 0
    raw_tokens: int = 0

    def __post_init__(self):
        if not self.char_count:
            self.char_count = len(self.text)
        if not self.word_count:
            self.word_count = len(self.text.split())

    def to_formatted_text(self) -> str:
        """Return canonical formatted text block with headers."""
        return f"[SECTION: {self.section_title}]\n[SOURCE: {self.source_id}]\n{self.text.strip()}"


# =============================================================================
# Exact & Near Duplicate Detection
# =============================================================================


@dataclass
class DuplicateAuditResult:
    """Detailed report on duplicate detection across documents."""

    total_documents: int
    unique_documents: int
    exact_duplicates_found: int
    near_duplicates_found: int
    connected_groups: int
    multi_document_groups: List[List[str]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def detect_duplicates_and_group(
    documents: List[CorpusDocument],
    near_dup_threshold: float = 0.85,
    shingle_k: int = 5,
) -> Tuple[List[CorpusDocument], DuplicateAuditResult, Dict[str, str]]:
    """Detect exact and near duplicates and cluster related documents into groups.

    Guarantees that duplicate and near-duplicate documents are assigned the same group_id,
    preventing them from being split between training and validation sets.

    Args:
        documents: Input CorpusDocument list.
        near_dup_threshold: Jaccard threshold on k-character shingles (0.0 to 1.0).
        shingle_k: Shingle length in characters.

    Returns:
        Tuple of (retained_documents, DuplicateAuditResult, doc_to_cluster_map).
    """
    if not documents:
        return [], DuplicateAuditResult(0, 0, 0, 0, 0, []), {}

    # Step 1: Detect exact duplicates via normalized text hash
    exact_hashes: Dict[str, str] = {}  # norm_hash -> primary_doc_id
    retained_docs: List[CorpusDocument] = []
    exact_dup_count = 0

    for doc in documents:
        norm = re.sub(r"\s+", " ", doc.text.strip().lower())
        h = hashlib.sha256(norm.encode("utf-8")).hexdigest()
        if h in exact_hashes:
            exact_dup_count += 1
            # Exact duplicate found; skip duplicate copy from retained
        else:
            exact_hashes[h] = doc.doc_id
            retained_docs.append(doc)

    n = len(retained_docs)
    doc_ids = [d.doc_id for d in retained_docs]
    parent: Dict[str, str] = {did: did for did in doc_ids}

    # If documents explicitly have a shared group_id, group them
    group_to_docs: Dict[str, List[str]] = {}
    for d in retained_docs:
        group_to_docs.setdefault(d.group_id, []).append(d.doc_id)

    def find(i: str) -> str:
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]

    def union(i: str, j: str):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j

    # Group explicitly co-grouped documents
    for members in group_to_docs.values():
        if len(members) > 1:
            for m in members[1:]:
                union(members[0], m)

    # Step 2: Near-duplicate detection via character k-grams
    def get_shingles(text: str) -> Set[str]:
        norm = re.sub(r"\s+", " ", text.strip().lower())
        if len(norm) < shingle_k:
            return {norm}
        return {norm[i : i + shingle_k] for i in range(len(norm) - shingle_k + 1)}

    shingles_list = [get_shingles(d.text) for d in retained_docs]
    near_dup_count = 0

    shingle_lens = [len(s) for s in shingles_list]
    for i in range(n):
        s1 = shingles_list[i]
        len1 = shingle_lens[i]
        for j in range(i + 1, n):
            len2 = shingle_lens[j]
            if len1 < len2:
                if (len1 / len2) < near_dup_threshold:
                    continue
            else:
                if (len2 / len1) < near_dup_threshold:
                    continue
            s2 = shingles_list[j]
            inter = len(s1 & s2)
            if inter == 0:
                continue
            union_len = len1 + len2 - inter
            sim = inter / union_len if union_len > 0 else 0.0
            if sim >= near_dup_threshold:
                near_dup_count += 1
                union(doc_ids[i], doc_ids[j])

    # Build cluster mapping
    cluster_map: Dict[str, str] = {did: find(did) for did in doc_ids}
    cluster_groups: Dict[str, List[str]] = {}
    for did, cid in cluster_map.items():
        cluster_groups.setdefault(cid, []).append(did)

    multi_groups = [members for members in cluster_groups.values() if len(members) > 1]

    # Update doc group_id with resolved cluster ID
    for doc in retained_docs:
        doc.group_id = cluster_map[doc.doc_id]

    audit = DuplicateAuditResult(
        total_documents=len(documents),
        unique_documents=len(retained_docs),
        exact_duplicates_found=exact_dup_count,
        near_duplicates_found=near_dup_count,
        connected_groups=len(cluster_groups),
        multi_document_groups=multi_groups,
    )

    return retained_docs, audit, cluster_map


# =============================================================================
# Document-Level & Group-Aware Partitioning
# =============================================================================


def partition_documents_by_group(
    documents: List[CorpusDocument],
    val_ratio: float = 0.15,
    seed: int = 42,
) -> Tuple[List[CorpusDocument], List[CorpusDocument]]:
    """Partition documents into train and val sets by group with zero cross-split leakage.

    All documents sharing the same group_id are guaranteed to reside in the same split.

    Args:
        documents: List of unique CorpusDocument items.
        val_ratio: Fraction of groups reserved for validation.
        seed: Random seed for deterministic reproducibility.

    Returns:
        Tuple of (train_documents, val_documents).
    """
    if not documents:
        return [], []
    if val_ratio <= 0.0:
        return list(documents), []

    import numpy as np

    rng = np.random.RandomState(seed)

    # Group documents by group_id
    groups: Dict[str, List[CorpusDocument]] = {}
    for doc in documents:
        groups.setdefault(doc.group_id, []).append(doc)

    unique_group_keys = sorted(list(groups.keys()))
    group_array = np.array(unique_group_keys)
    rng.shuffle(group_array)

    n_val_groups = max(1, int(len(unique_group_keys) * val_ratio))
    if n_val_groups >= len(unique_group_keys):
        n_val_groups = max(1, len(unique_group_keys) - 1)

    val_keys = set(group_array[:n_val_groups].tolist())

    train_docs: List[CorpusDocument] = []
    val_docs: List[CorpusDocument] = []

    for gid, docs in groups.items():
        if gid in val_keys:
            val_docs.extend(docs)
        else:
            train_docs.extend(docs)

    return train_docs, val_docs


# =============================================================================
# Corpus Quality & Statistics Calculator
# =============================================================================


@dataclass
class SplitStats:
    """Detailed statistical breakdown for a dataset split."""

    split_name: str
    document_count: int
    character_count: int
    word_count: int
    line_count: int
    raw_token_count: int
    tokens_with_eos: int
    packed_sequence_count: int
    padded_token_count: int
    avg_tokens_per_doc: float
    avg_words_per_doc: float
    domain_distribution: Dict[str, int]
    source_distribution: Dict[str, int]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def calculate_split_statistics(
    documents: List[CorpusDocument],
    split_name: str,
    tokenizer: NovaTokenizer,
    max_seq_len: int = 512,
    add_eos: bool = True,
) -> SplitStats:
    """Compute exact corpus statistics using the NovaTokenizer."""
    if not documents:
        return SplitStats(
            split_name=split_name,
            document_count=0,
            character_count=0,
            word_count=0,
            line_count=0,
            raw_token_count=0,
            tokens_with_eos=0,
            packed_sequence_count=0,
            padded_token_count=0,
            avg_tokens_per_doc=0.0,
            avg_words_per_doc=0.0,
            domain_distribution={},
            source_distribution={},
        )

    char_count = sum(len(d.text) for d in documents)
    word_count = sum(len(d.text.split()) for d in documents)
    line_count = sum(d.text.count("\n") + 1 for d in documents)

    tokenized_docs: List[List[int]] = []
    for d in documents:
        toks = tokenizer.encode(d.to_formatted_text(), allow_special=False)
        d.raw_tokens = len(toks)
        if add_eos and tokenizer.eos_token_id is not None:
            toks.append(tokenizer.eos_token_id)
        tokenized_docs.append(toks)

    raw_tokens = sum(d.raw_tokens for d in documents)
    tokens_with_eos = sum(len(toks) for toks in tokenized_docs)

    # Calculate packed sequences and padding
    all_tokens: List[int] = []
    for toks in tokenized_docs:
        all_tokens.extend(toks)

    n_packed = math.ceil(len(all_tokens) / max_seq_len) if all_tokens else 0
    total_slots = n_packed * max_seq_len
    padded_tokens = total_slots - len(all_tokens) if all_tokens else 0

    # Domain & source counts
    domain_dist: Dict[str, int] = {}
    source_dist: Dict[str, int] = {}
    for d in documents:
        domain_dist[d.topic_domain] = domain_dist.get(d.topic_domain, 0) + 1
        source_dist[d.source_id] = source_dist.get(d.source_id, 0) + 1

    return SplitStats(
        split_name=split_name,
        document_count=len(documents),
        character_count=char_count,
        word_count=word_count,
        line_count=line_count,
        raw_token_count=raw_tokens,
        tokens_with_eos=tokens_with_eos,
        packed_sequence_count=n_packed,
        padded_token_count=padded_tokens,
        avg_tokens_per_doc=raw_tokens / len(documents),
        avg_words_per_doc=word_count / len(documents),
        domain_distribution=domain_dist,
        source_distribution=source_dist,
    )
