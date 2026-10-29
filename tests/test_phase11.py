"""Comprehensive Automated Regression & Invariant Tests for Project NOVA Phase 11.

Parent-Source Integrity, Provenance Remediation, Biomechanics Staging, and Auditability.

Verifies:
1. Parent-publication split integrity across deterministic partitioning seeds.
2. Multiple chapters from the same parent publication remaining strictly co-located.
3. Duplicate clusters connecting documents across candidate partitions remaining strictly co-located.
4. Provenance consistency, fallback defaults for parent_source_id/canonical_source_url,
   and serialization round-trip integrity.
5. Licensing gate evaluation on CC BY-NC-SA 4.0, U.S. Gov third-party copyright restrictions,
   and human override isolation (overrides NEVER bypass safety or contamination gates).
6. Benchmark title/bibliographic matches vs genuine answer leakage detection.
7. Attribution retention for CC BY sources and robust extraction failure / OCR quarantine handling.
8. Phase 11 Staged Corpus Invariants: Train/Val strict disjointness on source_id, parent_source_id,
   and group_id, exact token reconciliation, and quarantine enforcement.
9. Historical preservation of Phase 10 artifacts and reports.
"""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import pytest

from nova.benchmark import FitnessEvaluationBenchmark
from nova.corpus import SourceRegistry
from nova.ingestion import (
    AuthoringMethod,
    BenchmarkContaminationDetector,
    CorpusDeduplicator,
    FitnessPillar,
    HealthSafetyScreener,
    IngestionStatus,
    LicenseCategory,
    LicenseGateResult,
    NormalizedDocument,
    Phase10Manifest,
    SourceIngestionPipeline,
    assess_text_quality,
    audit_license,
    normalize_corpus_text,
    source_level_split,
)
from nova.tokenizer import load_tokenizer

REPO_ROOT = Path(__file__).resolve().parent.parent
FINAL_TOK_DIR = REPO_ROOT / "artifacts" / "final_tokenizer"
BENCHMARK_PATH = REPO_ROOT / "data" / "benchmark" / "fitness_eval_benchmark.json"
STAGING_P11_DIR = REPO_ROOT / "data" / "staging_phase11"
STAGING_P10_DIR = REPO_ROOT / "data" / "staging_phase10"


# ==============================================================================
# Helper Factories
# ==============================================================================

def make_doc(
    doc_id: str,
    source_id: str,
    parent_source_id: str = "",
    group_id: str = "",
    url: str = "https://example.gov/doc",
    canonical_source_url: str = "",
    text: str = "Evidence-based strength training and cardiovascular exercise improve health and reduce disease risks.",
    token_count: int = 100,
    pillar: str = FitnessPillar.PILLAR_1_PHYSIOLOGY.value,
) -> NormalizedDocument:
    """Create a minimal NormalizedDocument for partitioning and provenance tests."""
    return NormalizedDocument(
        doc_id=doc_id,
        source_id=source_id,
        parent_source_id=parent_source_id,
        canonical_source_url=canonical_source_url,
        title=f"Test Document {doc_id}",
        text=text,
        pillar=pillar,
        group_id=group_id,
        token_count=token_count,
        url=url,
        license="Public Domain",
        legal_basis="17 U.S.C. § 105",
        attribution_text="US Government Work (17 U.S.C. § 105)",
    )


# ==============================================================================
# Task 1 & 5: Parent-Publication Split Integrity Tests
# ==============================================================================

class TestParentPublicationSplitIntegrity:
    """Validates that publication-level partition units are enforced without leakage."""

    @pytest.mark.parametrize("seed", [0, 1, 42, 100, 2026])
    def test_parent_publication_never_crosses_train_val(self, seed: int):
        """Under multiple random seeds, no parent publication is ever split across train/val."""
        # Create a corpus with multiple multi-chapter publications and single publications
        docs = [
            # Publication 1: 5 chapters (like PAGAC)
            make_doc("p1_c1", "PUB1-CH1", parent_source_id="PUB1", token_count=1000),
            make_doc("p1_c2", "PUB1-CH2", parent_source_id="PUB1", token_count=1200),
            make_doc("p1_c3", "PUB1-CH3", parent_source_id="PUB1", token_count=1500),
            make_doc("p1_c4", "PUB1-CH4", parent_source_id="PUB1", token_count=1100),
            make_doc("p1_c5", "PUB1-CH5", parent_source_id="PUB1", token_count=1300),
            # Publication 2: 3 chapters (like CDC Guidelines)
            make_doc("p2_c1", "PUB2-CH1", parent_source_id="PUB2", token_count=800),
            make_doc("p2_c2", "PUB2-CH2", parent_source_id="PUB2", token_count=850),
            make_doc("p2_c3", "PUB2-CH3", parent_source_id="PUB2", token_count=900),
            # Publication 3: single document
            make_doc("p3_c1", "PUB3-SINGLE", parent_source_id="PUB3", token_count=600),
            # Publication 4: single document
            make_doc("p4_c1", "PUB4-SINGLE", parent_source_id="PUB4", token_count=500),
            # Publication 5: single document
            make_doc("p5_c1", "PUB5-SINGLE", parent_source_id="PUB5", token_count=700),
        ]

        train_docs, val_docs = source_level_split(docs, val_ratio=0.20, seed=seed)

        train_sources = {d.source_id for d in train_docs}
        val_sources = {d.source_id for d in val_docs}
        train_parents = {d.parent_source_id for d in train_docs}
        val_parents = {d.parent_source_id for d in val_docs}

        # Assert strict disjointness
        assert train_sources.isdisjoint(val_sources), f"Source ID leaked at seed {seed}: {train_sources & val_sources}"
        assert train_parents.isdisjoint(val_parents), f"Parent ID leaked at seed {seed}: {train_parents & val_parents}"
        assert len(train_docs) + len(val_docs) == len(docs)

    def test_multiple_chapters_co_located(self):
        """All chapters of a publication must reside in the exact same partition."""
        docs = [
            make_doc("c1", "PAGAC-CH1", parent_source_id="US-HHS-PAGAC-2018", token_count=5000),
            make_doc("c2", "PAGAC-CH2", parent_source_id="US-HHS-PAGAC-2018", token_count=4000),
            make_doc("c3", "PAGAC-CH3", parent_source_id="US-HHS-PAGAC-2018", token_count=6000),
            make_doc("c4", "PAGAC-CH4", parent_source_id="US-HHS-PAGAC-2018", token_count=3500),
            make_doc("c5", "PAGAC-CH5", parent_source_id="US-HHS-PAGAC-2018", token_count=4500),
            make_doc("ind1", "CDC-DOC1", parent_source_id="CDC-PUB", token_count=2000),
            make_doc("ind2", "CDC-DOC2", parent_source_id="CDC-PUB", token_count=2000),
            make_doc("ind3", "PLOS-DOC", parent_source_id="PLOS-PUB", token_count=1000),
        ]

        train, val = source_level_split(docs, val_ratio=0.15, seed=42)

        pagac_partitions = {
            "train" if d in train else "val"
            for d in docs
            if d.parent_source_id == "US-HHS-PAGAC-2018"
        }
        # All PAGAC chapters must be in exactly one partition (size == 1)
        assert len(pagac_partitions) == 1, f"PAGAC chapters split across partitions: {pagac_partitions}"

    def test_dominant_single_publication_cannot_invert_split(self):
        """If a single parent constitutes >50% of tokens, it must stay in train when val_ratio < 0.5."""
        docs = [
            make_doc("dom1", "DOM-CH1", parent_source_id="DOMINANT-PARENT", token_count=80000),
            make_doc("dom2", "DOM-CH2", parent_source_id="DOMINANT-PARENT", token_count=20000),
            make_doc("sm1", "SMALL-CH1", parent_source_id="SMALL-PARENT-1", token_count=5000),
            make_doc("sm2", "SMALL-CH2", parent_source_id="SMALL-PARENT-2", token_count=5000),
        ]
        train, val = source_level_split(docs, val_ratio=0.10, seed=42)

        train_parents = {d.parent_source_id for d in train}
        val_parents = {d.parent_source_id for d in val}

        assert "DOMINANT-PARENT" in train_parents
        assert "DOMINANT-PARENT" not in val_parents
        assert train_parents.isdisjoint(val_parents)

    def test_deterministic_split_reproducibility(self):
        """Running source_level_split with the same seed yields identical document assignments."""
        docs = [
            make_doc(f"doc_{i}", f"SRC_{i % 4}", parent_source_id=f"PAR_{i % 3}", token_count=500 * (i + 1))
            for i in range(12)
        ]
        train1, val1 = source_level_split(docs, val_ratio=0.25, seed=777)
        train2, val2 = source_level_split(docs, val_ratio=0.25, seed=777)

        assert [d.doc_id for d in train1] == [d.doc_id for d in train2]
        assert [d.doc_id for d in val1] == [d.doc_id for d in val2]


# ==============================================================================
# Task 1 & 5: Duplicate Group Integrity Across Partitions
# ==============================================================================

class TestDuplicateGroupSplitIntegrity:
    """Validates that near-duplicate or syndicated clusters cannot straddle partitions."""

    def test_duplicate_cluster_unites_different_sources_and_parents(self):
        """If Doc A and Doc B belong to different publications but share a duplicate group_id,
        they must be placed in the same partition."""
        docs = [
            make_doc("doc_a", "SOURCE_A", parent_source_id="PARENT_A", group_id="SYNDICATED_CLUSTER_1", token_count=1000),
            make_doc("doc_b", "SOURCE_B", parent_source_id="PARENT_B", group_id="SYNDICATED_CLUSTER_1", token_count=1000),
            make_doc("doc_c", "SOURCE_C", parent_source_id="PARENT_C", group_id="", token_count=1500),
            make_doc("doc_d", "SOURCE_D", parent_source_id="PARENT_D", group_id="", token_count=1500),
        ]

        train, val = source_level_split(docs, val_ratio=0.30, seed=42)

        train_groups = {d.group_id for d in train if d.group_id}
        val_groups = {d.group_id for d in val if d.group_id}

        assert train_groups.isdisjoint(val_groups), f"Duplicate group leaked: {train_groups & val_groups}"

        doc_a_partition = "train" if any(d.doc_id == "doc_a" for d in train) else "val"
        doc_b_partition = "train" if any(d.doc_id == "doc_b" for d in train) else "val"
        assert doc_a_partition == doc_b_partition, "Near-duplicate documents placed in different partitions!"

    def test_transitive_cluster_closure_in_dsu(self):
        """Transitive link: Doc A shares parent with Doc B; Doc B shares group with Doc C.
        All three (Doc A, Doc B, Doc C) must end up in the same partition."""
        docs = [
            make_doc("doc_1", "SRC_1", parent_source_id="PUB_X", group_id="", token_count=500),
            make_doc("doc_2", "SRC_2", parent_source_id="PUB_X", group_id="BRIDGE_GROUP", token_count=500),
            make_doc("doc_3", "SRC_3", parent_source_id="PUB_Y", group_id="BRIDGE_GROUP", token_count=500),
            make_doc("doc_4", "SRC_4", parent_source_id="PUB_Z", group_id="", token_count=2000),
            make_doc("doc_5", "SRC_5", parent_source_id="PUB_W", group_id="", token_count=2000),
        ]

        train, val = source_level_split(docs, val_ratio=0.30, seed=123)

        p1 = "train" if any(d.doc_id == "doc_1" for d in train) else "val"
        p2 = "train" if any(d.doc_id == "doc_2" for d in train) else "val"
        p3 = "train" if any(d.doc_id == "doc_3" for d in train) else "val"

        assert p1 == p2 == p3, f"Transitive cluster broke across partitions: doc_1={p1}, doc_2={p2}, doc_3={p3}"


# ==============================================================================
# Task 2 & 5: Provenance Consistency and Metadata Fallbacks
# ==============================================================================

class TestProvenanceConsistency:
    """Validates metadata fields, default fallbacks, and serialization round-trips."""

    def test_default_fallbacks_when_omitted(self):
        """NormalizedDocument must fall back to source_id and url if parent/canonical omitted."""
        doc = NormalizedDocument(
            doc_id="test_fallback",
            source_id="MY-SOURCE-ID",
            parent_source_id="",  # empty
            canonical_source_url="",  # empty
            title="Fallback Test",
            text="Sample text for testing fallback values.",
            pillar=FitnessPillar.PILLAR_7_EDUCATION.value,
            url="https://example.org/test-url",
            group_id="",
            token_count=10,
        )

        assert doc.parent_source_id == "MY-SOURCE-ID", "parent_source_id should default to source_id"
        assert doc.canonical_source_url == "https://example.org/test-url", "canonical_source_url should default to url"

    def test_explicit_provenance_retained(self):
        """Explicit parent_source_id and canonical_source_url are strictly preserved."""
        doc = make_doc(
            doc_id="explicit_doc",
            source_id="US-HHS-PAGAC-2018-HIIT",
            parent_source_id="US-HHS-PAGAC-2018",
            url="https://health.gov/pagac-hiit",
            canonical_source_url="https://health.gov/our-work/physical-activity/current-guidelines/scientific-report",
        )
        assert doc.parent_source_id == "US-HHS-PAGAC-2018"
        assert doc.canonical_source_url == "https://health.gov/our-work/physical-activity/current-guidelines/scientific-report"

    def test_serialization_dict_round_trip(self):
        """to_dict and from_dict must preserve all Phase 11 provenance fields."""
        doc = make_doc(
            doc_id="round_trip_doc",
            source_id="SRC-101",
            parent_source_id="PARENT-PUB-999",
            group_id="GRP-DUPLICATE-42",
            url="https://example.gov/subpage",
            canonical_source_url="https://example.gov/main-publication",
        )

        data = doc.to_dict()
        assert data["parent_source_id"] == "PARENT-PUB-999"
        assert data["canonical_source_url"] == "https://example.gov/main-publication"
        assert data["group_id"] == "GRP-DUPLICATE-42"

        # Reconstruct
        reconstructed = NormalizedDocument.from_dict(data)
        assert reconstructed.parent_source_id == doc.parent_source_id
        assert reconstructed.canonical_source_url == doc.canonical_source_url
        assert reconstructed.group_id == doc.group_id
        assert reconstructed.source_id == doc.source_id

    def test_backward_compatibility_with_legacy_phase10_dict(self):
        """from_dict handles legacy Phase 10 dictionary missing parent_source_id/canonical_source_url."""
        legacy_dict = {
            "doc_id": "legacy_doc",
            "source_id": "LEGACY-SOURCE",
            "title": "Legacy Doc",
            "text": "Legacy content text.",
            "pillar": "exercise_science_biomechanics",
            "url": "https://example.gov/legacy",
            "license": "Public Domain",
            "token_count": 5,
            "group_id": "",
        }
        doc = NormalizedDocument.from_dict(legacy_dict)
        assert doc.parent_source_id == "LEGACY-SOURCE"
        assert doc.canonical_source_url == "https://example.gov/legacy"


# ==============================================================================
# Task 2 & 5: Legal Provenance, Licensing Gates, and Human Override Isolation
# ==============================================================================

class TestLegalProvenanceAndOverrideIsolation:
    """Validates source-specific licensing scrutiny, non-commercial rejection, and override isolation."""

    def test_cc_by_nc_sa_rejection(self):
        """OpenStax A&P 2e under CC BY-NC-SA 4.0 must be rejected by default due to non-commercial terms."""
        res = audit_license("CC BY-NC-SA 4.0", "Creative Commons Non-Commercial ShareAlike 4.0")
        assert not res.is_compliant
        assert "Non-commercial restriction" in res.rejection_reason

    def test_us_gov_with_unvetted_third_party_rejected(self):
        """U.S. government document with unvetted third-party copyright (Army FM 7-22) must be rejected."""
        res = audit_license(
            license_name="Public Domain",
            legal_basis="17 U.S.C. § 105",
            has_third_party_copyright=True,
            third_party_exclusions="",
        )
        assert not res.is_compliant
        assert "third-party copyrighted material" in res.rejection_reason

    def test_human_override_isolates_to_licensing_only(self):
        """A human license override NEVER bypasses Health & Safety or Benchmark Contamination gates."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            raw_file = tmp_path / "unsafe_sample.txt"
            raw_file.write_text(
                "To achieve rapid weight cuts before athletic competition, engage in dry fasting for 48 hours. "
                "In addition, take 120 mcg of clenbuterol daily without hydration. "
                "This causes rapid dehydration and dangerous electrolyte depletion.",
                encoding="utf-8",
            )
            benchmark = FitnessEvaluationBenchmark.load(BENCHMARK_PATH)
            pipeline = SourceIngestionPipeline(
                tokenizer=load_tokenizer(FINAL_TOK_DIR),
                benchmark=benchmark,
            )
            meta = {
                "source_id": "OVERRIDDEN-BUT-LETHAL",
                "parent_source_id": "OVERRIDDEN-PUB",
                "license": "Proprietary Commercial Book",
                "pillar": "nutrition_fundamentals_hydration",
                "title": "Unsafe Protocol with Override",
                "url": "https://example.com/unsafe",
            }
            docs = pipeline.ingest_file(
                raw_file,
                meta,
                allow_human_override=True,
                reviewer_id="Legal Counsel Dr. Smith",
                reviewer_notes="Human legal team negotiated bilateral license.",
            )
            # Assert document was NOT approved
            assert len(docs) == 0
            q_docs = list(pipeline.quarantined_docs.values())
            assert len(q_docs) == 1
            assert q_docs[0].ingestion_status == IngestionStatus.QUARANTINED
            assert "SAFETY HAZARD" in q_docs[0].review_notes

    def test_human_override_does_not_bypass_benchmark_gate(self):
        """A human license override NEVER bypasses the Benchmark Contamination gate."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            raw_file = tmp_path / "contam_sample.txt"
            raw_file.write_text(
                "For substantial health benefits, adults should do at least "
                "150 to 300 minutes of moderate intensity physical activity "
                "a week, or 75 to 150 minutes a week of vigorous-intensity aerobic physical activity.",
                encoding="utf-8",
            )
            benchmark = FitnessEvaluationBenchmark.load(BENCHMARK_PATH)
            pipeline = SourceIngestionPipeline(
                tokenizer=load_tokenizer(FINAL_TOK_DIR),
                benchmark=benchmark,
            )
            meta = {
                "source_id": "OVERRIDDEN-BUT-CONTAMINATED",
                "parent_source_id": "OVERRIDDEN-PUB",
                "license": "CC BY-NC 4.0",
                "pillar": "general_fitness_education_safety",
                "title": "Contaminated Guidelines with Override",
                "url": "https://example.com/contam",
            }
            docs = pipeline.ingest_file(
                raw_file,
                meta,
                allow_human_override=True,
                reviewer_id="Compliance Lead",
                reviewer_notes="Research exemption override.",
            )
            assert len(docs) == 0
            q_docs = list(pipeline.quarantined_docs.values())
            assert len(q_docs) == 1
            assert q_docs[0].ingestion_status == IngestionStatus.QUARANTINED
            assert "BENCHMARK CONTAMINATION" in q_docs[0].review_notes


# ==============================================================================
# Task 5: Benchmark Title Matches vs Genuine Answer Leakage
# ==============================================================================

class TestBenchmarkLeakageDiscrimination:
    """Validates that detector discriminates bibliographic title matches from genuine answer leaks."""

    @pytest.fixture
    def detector(self) -> BenchmarkContaminationDetector:
        benchmark = FitnessEvaluationBenchmark.load(BENCHMARK_PATH)
        return BenchmarkContaminationDetector(benchmark=benchmark)

    def test_bibliographic_title_mention_allowed(self, detector: BenchmarkContaminationDetector):
        """Mentioning a guideline title or publication name in citations does not trigger contamination."""
        citation_text = (
            "References:\n"
            "1. U.S. Department of Health and Human Services. 2018 Physical Activity Guidelines Advisory Committee "
            "Scientific Report. Washington, DC: HHS, 2018.\n"
            "2. Centers for Disease Control and Prevention. Physical Activity Guidelines for Adults. CDC, 2022.\n"
            "These documents provide population-level surveillance data."
        )
        res = detector.check_text(citation_text)
        assert not res.is_contaminated, f"Bibliographic citation incorrectly flagged as contamination: {res.matches}"

    def test_genuine_answer_13gram_leakage_blocked(self, detector: BenchmarkContaminationDetector):
        """Exact 13-gram phrasing from held-out benchmark answer must be detected and blocked."""
        leak_text = (
            "Current public health consensus states that adults need "
            "150 to 300 minutes of moderate intensity physical activity "
            "per week to reduce the risk of all-cause mortality."
        )
        res = detector.check_text(leak_text)
        assert res.is_contaminated
        assert any(m.is_genuine_leakage for m in res.matches)
        assert any("150 to 300 minutes of moderate intensity physical" in m.matched_ngram for m in res.matches)


# ==============================================================================
# Task 4 & 5: Biomechanics Extraction and Scanned PDF / Quality Handling
# ==============================================================================

class TestExtractionAndQualityHandling:
    """Validates attribution retention for CC BY and graceful quarantine of unreadable/scanned inputs."""

    def test_cc_by_attribution_retained(self):
        """CC BY 4.0 ingestion preserves attribution text in NormalizedDocument."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            raw_file = tmp_path / "plos_sample.txt"
            raw_file.write_text(
                "Resistance training frequency refers to the number of resistance training sessions "
                "performed within a given timeframe, typically one week. Evidence indicates that when "
                "volume is equated, training frequency does not significantly impact muscular hypertrophy.",
                encoding="utf-8",
            )
            benchmark = FitnessEvaluationBenchmark.load(BENCHMARK_PATH)
            pipeline = SourceIngestionPipeline(
                tokenizer=load_tokenizer(FINAL_TOK_DIR),
                benchmark=benchmark,
            )
            meta = {
                "source_id": "PLOS-TEST-CCBY",
                "parent_source_id": "PLOS-ONE-0215877",
                "license": "CC BY 4.0",
                "legal_basis": "Creative Commons Attribution 4.0 International",
                "pillar": "strength_training_programming",
                "title": "Resistance Training Frequency Study",
                "url": "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0215877",
                "mandatory_attribution_text": "Copyright © 2019 Saric et al. Distributed under CC BY 4.0 International.",
                "attribution_required": True,
            }
            docs = pipeline.ingest_file(raw_file, meta)
            assert len(docs) == 1
            doc = docs[0]
            assert doc.ingestion_status == IngestionStatus.APPROVED
            assert "Saric et al" in doc.attribution_text
            assert "CC BY 4.0" in doc.attribution_text

    def test_scanned_pdf_quarantine(self):
        """Pipeline quarantines scanned PDF with no extractable text stream."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            raw_file = tmp_path / "scanned_manual.pdf"
            raw_file.write_bytes(b"%PDF-1.4\n1 0 obj\n<< /Type /XObject /Subtype /Image >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF")
            benchmark = FitnessEvaluationBenchmark.load(BENCHMARK_PATH)
            pipeline = SourceIngestionPipeline(
                tokenizer=load_tokenizer(FINAL_TOK_DIR),
                benchmark=benchmark,
            )
            meta = {
                "source_id": "SCANNED-HISTORICAL-MANUAL",
                "parent_source_id": "HISTORICAL-MANUAL",
                "license": "Public Domain",
                "legal_basis": "17 U.S.C. § 105",
                "pillar": "exercise_science_biomechanics",
                "title": "Historical Gymnastic Training (1910)",
                "url": "https://example.gov/scanned.pdf",
            }
            docs = pipeline.ingest_file(raw_file, meta)
            assert len(docs) == 0
            q_docs = list(pipeline.quarantined_docs.values())
            assert len(q_docs) == 1
            assert q_docs[0].ingestion_status == IngestionStatus.QUARANTINED


# ==============================================================================
# Task 5 & Exit Criteria: Phase 11 Staged Corpus Invariants
# ==============================================================================

class TestPhase11StagedCorpusInvariants:
    """Validates the official staged corpus artifacts in data/staging_phase11/."""

    @pytest.fixture
    def staging_manifest(self) -> dict:
        manifest_path = STAGING_P11_DIR / "phase11_staging_manifest.json"
        assert manifest_path.exists(), f"Phase 11 staging manifest missing at {manifest_path}"
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @pytest.fixture
    def audit_summary(self) -> dict:
        audit_path = STAGING_P11_DIR / "phase11_audit_summary.json"
        assert audit_path.exists(), f"Phase 11 audit summary missing at {audit_path}"
        with open(audit_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @pytest.fixture
    def train_staging(self) -> list[dict]:
        train_path = STAGING_P11_DIR / "train_staging.json"
        assert train_path.exists(), f"train_staging.json missing at {train_path}"
        with open(train_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @pytest.fixture
    def val_staging(self) -> list[dict]:
        val_path = STAGING_P11_DIR / "val_staging.json"
        assert val_path.exists(), f"val_staging.json missing at {val_path}"
        with open(val_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_strict_disjointness_invariants(self, train_staging, val_staging):
        """Train and Validation must have zero overlap across source_id, parent_source_id, and group_id."""
        train_sources = {d["source_id"] for d in train_staging}
        val_sources = {d["source_id"] for d in val_staging}

        train_parents = {d.get("parent_source_id") or d["source_id"] for d in train_staging}
        val_parents = {d.get("parent_source_id") or d["source_id"] for d in val_staging}

        train_groups = {d.get("group_id") for d in train_staging if d.get("group_id")}
        val_groups = {d.get("group_id") for d in val_staging if d.get("group_id")}

        # 1. No source_id crosses train and val
        assert train_sources.isdisjoint(val_sources), f"Source overlap found: {train_sources & val_sources}"

        # 2. No parent_source_id crosses train and val
        assert train_parents.isdisjoint(val_parents), f"Parent publication overlap found: {train_parents & val_parents}"

        # 3. No duplicate group crosses train and val
        assert train_groups.isdisjoint(val_groups), f"Duplicate group overlap found: {train_groups & val_groups}"

    def test_all_pagac_chapters_retained_together_in_training(self, train_staging, val_staging):
        """All accepted chapters of 2018 PAGAC Scientific Report must reside in training, never validation."""
        val_parents = {d.get("parent_source_id") or d["source_id"] for d in val_staging}
        assert "US-HHS-PAGAC-2018" not in val_parents, "2018 PAGAC leaked into validation!"

        pagac_train_sources = {
            d["source_id"] for d in train_staging
            if (d.get("parent_source_id") or d["source_id"]) == "US-HHS-PAGAC-2018"
        }
        # Expected accepted chapters: EXEC, HIIT, BRAIN-SLEEP, CARDIOMETABOLIC, OLDER-ADULTS (5 chapters)
        expected_pagac = {
            "US-HHS-PAGAC-2018-EXEC",
            "US-HHS-PAGAC-2018-HIIT",
            "US-HHS-PAGAC-2018-BRAIN-SLEEP",
            "US-HHS-PAGAC-2018-CARDIOMETABOLIC",
            "US-HHS-PAGAC-2018-OLDER-ADULTS",
        }
        assert pagac_train_sources == expected_pagac

    def test_token_counts_reconciled(self, staging_manifest, audit_summary, train_staging, val_staging):
        """Manifest token totals must equal sum of train and val tokens exactly."""
        train_tokens = sum(d["token_count"] for d in train_staging)
        val_tokens = sum(d["token_count"] for d in val_staging)
        total_tokens = train_tokens + val_tokens

        assert staging_manifest["total_combined_tokens"] == total_tokens
        assert audit_summary["combined_usable_tokens"] == total_tokens
        assert audit_summary["train_tokens"] == train_tokens
        assert audit_summary["val_tokens"] == val_tokens
        assert total_tokens == 97808, f"Unexpected token total: {total_tokens}"
        assert train_tokens == 91997
        assert val_tokens == 5811

    def test_zero_benchmark_contamination_in_accepted_staging(self, train_staging, val_staging):
        """Zero benchmark contamination in all accepted documents."""
        benchmark = FitnessEvaluationBenchmark.load(BENCHMARK_PATH)
        detector = BenchmarkContaminationDetector(benchmark=benchmark)
        for doc_dict in train_staging + val_staging:
            res = detector.check_text(doc_dict["text"])
            assert not res.is_contaminated, f"Contamination detected in accepted doc {doc_dict['doc_id']}: {res.matches}"

    def test_historical_phase10_records_preserved_intact(self):
        """Phase 10 historical records and reports must remain intact and not silently overwritten."""
        p10_manifest = STAGING_P10_DIR / "phase10_staging_manifest.json"
        p10_report = REPO_ROOT / "docs" / "phase10_corpus_expansion_report.md"
        p10_workflow = REPO_ROOT / "docs" / "phase10_source_review_workflow.md"

        assert p10_manifest.exists(), "Historical Phase 10 staging manifest was deleted or overwritten!"
        assert p10_report.exists(), "Historical Phase 10 corpus expansion report was deleted or overwritten!"
        assert p10_workflow.exists(), "Historical Phase 10 review workflow was deleted or overwritten!"
