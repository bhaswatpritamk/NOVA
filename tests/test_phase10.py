"""Comprehensive Automated Tests for Project NOVA Phase 10: Verified Fitness Corpus Expansion.

Verifies:
1. Legal & Licensing Gates: Compliance validation, rejection of CC BY-NC, CC BY-ND,
   proprietary, and unknown licenses, plus human review override mechanics.
2. Multi-Format Text Ingestion: HTML, Markdown, Plain Text, PDF streams, JSON manifests,
   and malformed inputs.
3. Text Normalization & Quality Filters: Unicode NFKC, boilerplate stripping,
   short-text rejection, repetitive-text rejection, and non-ASCII corrupt text handling.
4. Health & Safety Screening: Detection and quarantine of medical diagnosis claims,
   extreme dieting/dehydration, prohibited PEDs/drugs, and exercise contraindications.
5. Benchmark Contamination Prevention: Zero n-gram leakage against held-out benchmark
   prompts and canonical reference answers.
6. Deduplication & Clustering: Exact SHA-256 deduplication, near-duplicate Jaccard
   clustering, and cluster group_id preservation.
7. Pipeline Resumability: Resuming interrupted runs without duplicating documents.
8. Source-Level Splitting: Deterministic partition with zero cross-split source leakage.
9. Tokenizer Compatibility & Manifest Integrity: Token counting with authoritative
   tokenizer (vocab 3,384) and cryptographic manifest verification.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
import tempfile
import pytest

from nova.benchmark import FitnessEvaluationBenchmark
from nova.corpus import SourceRegistry
from nova.ingestion import (
    AuthoringMethod,
    BenchmarkContaminationDetector,
    CorpusDeduplicator,
    DeduplicationResult,
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
    extract_text_from_html,
    extract_text_from_markdown,
    extract_text_from_pdf_stream,
    normalize_corpus_text,
    normalize_pillar,
    source_level_split,
)
from nova.tokenizer import NovaTokenizer, load_tokenizer

REPO_ROOT = Path(__file__).resolve().parent.parent
FINAL_TOK_DIR = REPO_ROOT / "artifacts" / "final_tokenizer"
BENCHMARK_PATH = REPO_ROOT / "data" / "benchmark" / "fitness_eval_benchmark.json"
SOURCE_REGISTRY_PATH = REPO_ROOT / "data" / "approved" / "source_registry.json"


@pytest.fixture(scope="module")
def tokenizer() -> NovaTokenizer:
    """Fixture providing the authoritative final Byte-Level BPE tokenizer."""
    assert FINAL_TOK_DIR.is_dir(), f"Tokenizer dir missing: {FINAL_TOK_DIR}"
    return load_tokenizer(FINAL_TOK_DIR)


@pytest.fixture(scope="module")
def benchmark() -> FitnessEvaluationBenchmark:
    """Fixture providing the held-out fitness benchmark."""
    assert BENCHMARK_PATH.is_file(), f"Benchmark file missing: {BENCHMARK_PATH}"
    return FitnessEvaluationBenchmark.load(BENCHMARK_PATH)


# =============================================================================
# 1. Legal & Licensing Gate Tests
# =============================================================================

class TestLicensingGates:
    """Verify strict legal compliance rules for model training."""

    def test_us_gov_work_is_compliant(self):
        res = audit_license("Public Domain", "17 U.S.C. § 105 (U.S. Government Work)")
        assert res.is_compliant is True
        assert res.category == LicenseCategory.PUBLIC_DOMAIN_US_GOV
        assert res.requires_attribution is False

    def test_cc0_is_compliant(self):
        res = audit_license("CC0 1.0 Universal", "Creative Commons Zero")
        assert res.is_compliant is True
        assert res.category == LicenseCategory.PUBLIC_DOMAIN_CC0
        assert res.requires_attribution is False

    def test_cc_by_is_compliant_with_attribution(self):
        res = audit_license("CC BY 4.0", "Creative Commons Attribution 4.0 International")
        assert res.is_compliant is True
        assert res.category == LicenseCategory.PERMISSIVE_CC_BY
        assert res.requires_attribution is True

    def test_cc_by_nc_is_rejected(self):
        res = audit_license("CC BY-NC 4.0", "Creative Commons Non-Commercial")
        assert res.is_compliant is False
        assert res.category == LicenseCategory.RESTRICTED_NON_COMMERCIAL
        assert "Non-commercial restriction" in res.rejection_reason

    def test_cc_by_nd_is_rejected(self):
        res = audit_license("CC BY-ND 4.0", "Creative Commons No-Derivatives")
        assert res.is_compliant is False
        assert res.category == LicenseCategory.RESTRICTED_NO_DERIVATIVES
        assert "No-derivatives restriction" in res.rejection_reason

    def test_proprietary_is_rejected(self):
        res = audit_license("All Rights Reserved", "Proprietary Commercial Book")
        assert res.is_compliant is False
        assert res.category == LicenseCategory.PROPRIETARY
        assert "Proprietary" in res.rejection_reason

    def test_unknown_license_is_rejected(self):
        res = audit_license("Random Webpage", "")
        assert res.is_compliant is False
        assert res.category == LicenseCategory.UNKNOWN

    def test_human_override_mechanics(self):
        # Override without reviewer ID must fail
        res_fail = audit_license("CC BY-NC 4.0", allow_human_override=True, reviewer_id="")
        assert res_fail.is_compliant is False

        # Override with reviewer ID and justification succeeds
        res_ok = audit_license(
            license_name="Custom Institutional License",
            legal_basis="Written Bilateral Research Exemption",
            allow_human_override=True,
            reviewer_id="LEGAL-REVIEWER-42",
            reviewer_notes="Explicit written permission granted by publisher for research model training.",
        )
        assert res_ok.is_compliant is True
        assert res_ok.human_override_approved is True
        assert res_ok.reviewer_id == "LEGAL-REVIEWER-42"


# =============================================================================
# 2. Multi-Format Text Extraction Tests
# =============================================================================

class TestMultiFormatExtraction:
    """Verify parsing and clean extraction across HTML, Markdown, Plain Text, and PDF."""

    def test_html_extraction(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head><title>Test</title><style>.hidden { display: none; }</style></head>
        <body>
            <nav><a href="/home">Home</a><a href="/about">About</a></nav>
            <h1>Skeletal Muscle Hypertrophy Mechanisms</h1>
            <p>Mechanical tension is the primary mechanical stimulus initiating intracellular signaling cascades.</p>
            <footer><p>Copyright 2026. All rights reserved.</p></footer>
            <script>console.log('strip me');</script>
        </body>
        </html>
        """
        text = extract_text_from_html(html)
        assert "Skeletal Muscle Hypertrophy Mechanisms" in text
        assert "Mechanical tension" in text
        # Navigation and scripts must be purged
        assert "console.log" not in text
        assert "strip me" not in text

    def test_markdown_extraction(self):
        md = """# Resistance Training Volume

![Barbell Image](https://example.com/barbell.jpg)

Here is a link to the [Physical Activity Guidelines](https://health.gov) for adults.

```python
# Code block to ignore
def ignore_this():
    pass
```

Performing 10 to 20 sets per muscle group per week optimizes muscular hypertrophy.
---
"""
        text = extract_text_from_markdown(md)
        assert "Resistance Training Volume" in text
        assert "Physical Activity Guidelines" in text
        assert "10 to 20 sets per muscle group" in text
        # Non-free image syntax and links stripped
        assert "![Barbell Image]" not in text
        assert "https://example.com/barbell.jpg" not in text
        assert "https://health.gov" not in text

    def test_pdf_stream_extraction(self):
        # Construct synthetic PDF text stream
        raw_pdf = b"%PDF-1.4\n1 0 obj\n<<>>\nstream\nBT\n/F1 12 Tf\n(Skeletal muscle contraction requires ATP) Tj\nET\nendstream\nendobj\n%%EOF"
        text = extract_text_from_pdf_stream(raw_pdf)
        assert "Skeletal muscle contraction requires ATP" in text


# =============================================================================
# 3. Text Normalization & Quality Assessment Tests
# =============================================================================

class TestTextNormalizationAndQuality:
    """Verify text hygiene, Unicode normalization, boilerplate stripping, and quality checks."""

    def test_unicode_and_whitespace_normalization(self):
        raw = "“Smart quotes” and ‘single quotes’\u00a0with non-breaking   spaces.\r\n\r\n\r\n\r\nNew paragraph."
        cleaned = normalize_corpus_text(raw)
        assert '"Smart quotes"' in cleaned
        assert "'single quotes'" in cleaned
        assert "   " not in cleaned
        assert "\r" not in cleaned
        assert "\n\n\n" not in cleaned

    def test_boilerplate_removal(self):
        raw = "Real fitness content here.\nPage 12 of 50\nDownloaded from http://example.com\nTerms of Service\nMore real fitness content here."
        cleaned = normalize_corpus_text(raw)
        assert "Real fitness content here." in cleaned
        assert "More real fitness content here." in cleaned
        assert "Page 12 of 50" not in cleaned
        assert "Downloaded from" not in cleaned
        assert "Terms of Service" not in cleaned

    def test_short_text_rejection(self):
        is_ok, reason = assess_text_quality("Too short text.", min_chars=100)
        assert is_ok is False
        assert "too short" in reason.lower()

    def test_repetitive_filler_rejection(self):
        # 40 repetitions of the exact same 10 words
        repeated = " ".join(["muscle hypertrophy requires progressive overload and adequate daily protein intake"] * 40)
        is_ok, reason = assess_text_quality(repeated)
        assert is_ok is False
        assert "repetitive" in reason.lower()

    def test_corrupted_non_ascii_rejection(self):
        corrupted = "Good text " + ("\x80\x81\xfe\xff" * 50) + " trailing text."
        is_ok, reason = assess_text_quality(corrupted, min_chars=50)
        assert is_ok is False
        assert "corrupt" in reason.lower()


# =============================================================================
# 4. Health & Safety Screening Tests
# =============================================================================

class TestHealthSafetyScreening:
    """Verify detection and flagging of unsafe medical, dietary, or training recommendations."""

    def test_medical_diagnosis_flagged(self):
        screener = HealthSafetyScreener()
        text = "Based on your anterior knee pain, I diagnose a meniscus tear and recommend knee arthroscopy."
        flags = screener.screen_text(text)
        assert len(flags) > 0
        assert any(f["severity"] == "CRITICAL" for f in flags)
        assert any("diagnosis" in f["description"].lower() for f in flags)

    def test_extreme_dieting_flagged(self):
        screener = HealthSafetyScreener()
        text = "Athletes should wear sweat suits to cut weight rapidly before the weigh-in."
        flags = screener.screen_text(text)
        assert len(flags) > 0
        assert any("dehydration" in f["description"].lower() for f in flags)

    def test_prohibited_substances_flagged(self):
        screener = HealthSafetyScreener()
        text = "Bodybuilders should take anabolic steroids and clenbuterol to increase muscle mass and burn fat."
        flags = screener.screen_text(text)
        assert len(flags) >= 2
        assert any("performance-enhancing" in f["description"].lower() for f in flags)

    def test_ignoring_contraindications_flagged(self):
        screener = HealthSafetyScreener()
        text = "When squatting heavy, push through sharp joint pain and ignore chest pain to build mental toughness."
        flags = screener.screen_text(text)
        assert len(flags) >= 2
        assert any("joint injury" in f["description"].lower() for f in flags)
        assert any("cardiovascular" in f["description"].lower() for f in flags)

    def test_safe_scientific_text_passes(self):
        screener = HealthSafetyScreener()
        text = """Skeletal muscle adapts to chronic resistance training through myofibrillar protein synthesis.
        Progression should be gradual, maintaining 1 to 3 repetitions in reserve to manage fatigue and reduce musculoskeletal injury risk.
        Athletes experiencing acute pain should cease the movement and seek clinical guidance."""
        flags = screener.screen_text(text)
        critical_flags = [f for f in flags if f["severity"] in ("CRITICAL", "HIGH")]
        assert len(critical_flags) == 0


# =============================================================================
# 5. Benchmark Contamination Prevention Tests
# =============================================================================

class TestBenchmarkContaminationPrevention:
    """Verify zero n-gram leakage between training corpus and the 12-question diagnostic benchmark."""

    def test_detects_prompt_leakage(self, benchmark: FitnessEvaluationBenchmark):
        detector = BenchmarkContaminationDetector(benchmark, n_gram_len=8)
        # Use an exact snippet from question 1 prompt
        contaminated_text = "What are the primary contractile proteins involved in the cross-bridge cycle of skeletal muscle contraction?"
        is_contaminated, matches = detector.check_text(contaminated_text)
        assert is_contaminated is True
        assert len(matches) > 0
        assert any("Prompt" in m for m in matches)

    def test_detects_answer_leakage(self, benchmark: FitnessEvaluationBenchmark):
        detector = BenchmarkContaminationDetector(benchmark, n_gram_len=8)
        # Snippet from canonical reference answer 1
        contaminated_text = "The globular heads of the myosin heavy chains possess the enzymatic ATPase activity which hydrolyzes ATP."
        is_contaminated, matches = detector.check_text(contaminated_text)
        assert is_contaminated is True
        assert len(matches) > 0
        assert any("Answer" in m for m in matches)

    def test_clean_science_text_not_flagged(self, benchmark: FitnessEvaluationBenchmark):
        detector = BenchmarkContaminationDetector(benchmark, n_gram_len=8)
        clean_text = """Endurance training enhances mitochondrial biogenesis and capillary density in skeletal muscle tissue.
        Elevations in maximal oxygen uptake (VO2 max) are mediated by increases in stroke volume and arteriovenous oxygen difference according to the Fick equation."""
        is_contaminated, matches = detector.check_text(clean_text)
        assert is_contaminated is False
        assert len(matches) == 0


# =============================================================================
# 6. Deduplication & Clustering Tests
# =============================================================================

class TestDeduplicationAndClustering:
    """Verify exact and near-duplicate detection and cluster assignment."""

    def test_exact_duplicate_detection(self):
        dedup = CorpusDeduplicator()
        doc1 = NormalizedDocument(
            doc_id="DOC_001",
            source_id="SRC_A",
            title="Tension",
            text="Mechanical tension stimulates focal adhesion kinase and integrin signaling to upregulate mTORC1.",
            pillar="exercise_science_biomechanics",
        )
        doc2 = NormalizedDocument(
            doc_id="DOC_002",
            source_id="SRC_A",
            title="Tension Copy",
            text="  Mechanical tension stimulates focal adhesion kinase and integrin signaling to upregulate mTORC1.  ",
            pillar="exercise_science_biomechanics",
        )
        retained, result = dedup.deduplicate([doc1, doc2])
        assert len(retained) == 1
        assert result.exact_duplicates_dropped == 1
        assert retained[0].doc_id == "DOC_001"

    def test_near_duplicate_clustering(self):
        dedup = CorpusDeduplicator(near_dup_threshold=0.85, shingle_k=5)
        doc1 = NormalizedDocument(
            doc_id="DOC_101",
            source_id="SRC_B",
            title="Overload A",
            text="Progressive overload is systematically increasing resistance training stimulus, intensity, volume, or frequency over time to force adaptation.",
            pillar="exercise_science_biomechanics",
            group_id="GRP_A",
        )
        doc2 = NormalizedDocument(
            doc_id="DOC_102",
            source_id="SRC_B",
            title="Overload B",
            text="Progressive overload is systematically increasing resistance training stimulus, intensity, volume, and frequency over time to force adaptation.",
            pillar="exercise_science_biomechanics",
            group_id="GRP_B",
        )
        retained, result = dedup.deduplicate([doc1, doc2])
        assert len(retained) == 2
        assert result.near_duplicates_found >= 1
        # Both near duplicates must share the exact same group_id
        assert retained[0].group_id == retained[1].group_id


# =============================================================================
# 7. Source-Level Partitioning Tests
# =============================================================================

class TestSourceLevelPartitioning:
    """Verify that source-level splitting keeps sources and groups completely isolated."""

    def test_source_isolation_across_splits(self):
        docs = []
        for i in range(10):
            docs.append(NormalizedDocument(
                doc_id=f"SRC1_{i}",
                source_id="SOURCE_ONE",
                title=f"Source 1 Section {i}",
                text=f"Unique text for source 1 document {i} with sufficient words to qualify for test corpus.",
                pillar="exercise_science_biomechanics",
                group_id=f"GRP_1_{i}",
            ))
        for i in range(10):
            docs.append(NormalizedDocument(
                doc_id=f"SRC2_{i}",
                source_id="SOURCE_TWO",
                title=f"Source 2 Section {i}",
                text=f"Unique text for source 2 document {i} with sufficient words to qualify for test corpus.",
                pillar="strength_training_programming",
                group_id=f"GRP_2_{i}",
            ))
        for i in range(10):
            docs.append(NormalizedDocument(
                doc_id=f"SRC3_{i}",
                source_id="SOURCE_THREE",
                title=f"Source 3 Section {i}",
                text=f"Unique text for source 3 document {i} with sufficient words to qualify for test corpus.",
                pillar="nutrition_fundamentals_hydration",
                group_id=f"GRP_3_{i}",
            ))

        train_docs, val_docs = source_level_split(docs, val_ratio=0.25, seed=42)
        assert len(train_docs) > 0
        assert len(val_docs) > 0

        # Check macro group intersection
        train_macro = set(f"{d.source_id}::{d.group_id}" for d in train_docs)
        val_macro = set(f"{d.source_id}::{d.group_id}" for d in val_docs)
        assert train_macro.isdisjoint(val_macro), "Macro-partition groups must not cross train and val splits"


# =============================================================================
# 8. Pipeline Resumability & Manifest Tests
# =============================================================================

class TestPipelineResumabilityAndManifest:
    """Verify that the ingestion pipeline can resume cleanly without duplicates."""

    def test_resumable_ingestion(self, tokenizer: NovaTokenizer, benchmark: FitnessEvaluationBenchmark):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            state_file = tmp_path / "test_state.json"
            manifest_file = tmp_path / "test_manifest.json"

            # Create test input files
            doc1_file = tmp_path / "cdc_pa_doc.txt"
            doc1_file.write_text(
                "Adults need at least 150 minutes of moderate-intensity physical activity per week and muscle-strengthening on two or more days per week according to public health guidelines.",
                encoding="utf-8",
            )
            doc2_file = tmp_path / "usda_diet_doc.md"
            doc2_file.write_text(
                "# Dietary Guidelines\n\nActive individuals should consume adequate dietary protein ranging from 1.2 to 2.0 grams per kilogram of body weight daily to support muscle protein synthesis and tissue recovery across training blocks.",
                encoding="utf-8",
            )

            # Ingestion Run 1
            pipeline = SourceIngestionPipeline(
                tokenizer=tokenizer,
                benchmark=benchmark,
                state_file=state_file,
            )
            meta1 = {
                "source_id": "US-CDC-PA-TEST",
                "title": "CDC Physical Activity",
                "pillar": "7",
                "license": "Public Domain",
                "legal_basis": "17 U.S.C. § 105",
            }
            docs_run1 = pipeline.ingest_file(doc1_file, meta1)
            assert len(docs_run1) == 1
            assert docs_run1[0].token_count > 0

            # Ingestion Run 2 (Resuming with previous state and ingesting doc2 + doc1 again)
            pipeline2 = SourceIngestionPipeline(
                tokenizer=tokenizer,
                benchmark=benchmark,
                state_file=state_file,
            )
            assert len(pipeline2.ingested_docs) == 1  # Loaded from state

            # Re-ingesting doc1 should be recognized as duplicate and NOT duplicated
            re_ingested = pipeline2.ingest_file(doc1_file, meta1)
            assert len(re_ingested) == 0

            # Ingesting doc2
            meta2 = {
                "source_id": "USDA-DGA-TEST",
                "title": "USDA Guidelines",
                "pillar": "4",
                "license": "Public Domain",
                "legal_basis": "17 U.S.C. § 105",
            }
            docs_run2 = pipeline2.ingest_file(doc2_file, meta2)
            assert len(docs_run2) == 1

            # Check final manifest
            manifest = pipeline2.generate_manifest()
            assert manifest.total_documents_approved == 2
            assert manifest.total_combined_tokens > 0
            manifest.save(manifest_file)
            assert manifest_file.is_file()

            # Verify saved manifest matches structure
            with open(manifest_file, "r", encoding="utf-8") as f:
                saved_data = json.load(f)
            assert saved_data["total_documents_approved"] == 2
            assert saved_data["authoritative_tokenizer_vocab_size"] == 3384


# =============================================================================
# 9. Phase 10.1 Regression & Source-Level Split Integrity Tests
# =============================================================================

class TestPhase101SplitIntegrity:
    """Rigorous verification of source-level and duplicate-cluster partition integrity."""

    def test_source_id_disjoint_strict_regression(self):
        """Assert set(train_source_ids).isdisjoint(set(val_source_ids)) strictly holds."""
        docs = []
        sources = ["SRC_CDC_ADULTS", "SRC_HHS_PAG", "SRC_NIOSH_HEAT", "SRC_ACSM_GUIDELINES", "SRC_OPENSTAX_AP"]
        for s_idx, src in enumerate(sources):
            for doc_idx in range(8):
                docs.append(NormalizedDocument(
                    doc_id=f"{src}_DOC_{doc_idx}",
                    source_id=src,
                    title=f"{src} Section {doc_idx}",
                    text=f"Educational fitness text for {src} section {doc_idx} discussing physiological training principles.",
                    pillar="exercise_physiology",
                    group_id=f"GROUP_{s_idx}_{doc_idx}",  # Every doc has a unique group ID
                ))

        for seed in (0, 42, 101, 999, 2026):
            train_docs, val_docs = source_level_split(docs, val_ratio=0.25, seed=seed)
            assert len(train_docs) > 0, f"Train set empty for seed {seed}"
            assert len(val_docs) > 0, f"Val set empty for seed {seed}"

            train_source_ids = {d.source_id for d in train_docs}
            val_source_ids = {d.source_id for d in val_docs}

            # PRIMARY REGRESSION ASSERTION:
            assert train_source_ids.isdisjoint(val_source_ids), (
                f"Source ID leakage detected for seed {seed}! Overlapping sources: {train_source_ids & val_source_ids}"
            )

    def test_documents_of_same_source_stay_together(self):
        """Every document from a source must remain in the same partition even with different group IDs."""
        docs = []
        # Source A has 15 documents with 15 different group IDs
        for i in range(15):
            docs.append(NormalizedDocument(
                doc_id=f"CDC_{i}",
                source_id="CDC_PHYS_ACTIVITY",
                title=f"CDC Guideline Chapter {i}",
                text=f"Guideline text chapter {i} discussing aerobic volume and resistance recommendations.",
                pillar="exercise_physiology",
                group_id=f"CLUSTER_CDC_{i}",
            ))
        # Source B has 10 documents
        for i in range(10):
            docs.append(NormalizedDocument(
                doc_id=f"WHO_{i}",
                source_id="WHO_GUIDELINES",
                title=f"WHO Section {i}",
                text=f"WHO text section {i} discussing global health guidelines.",
                pillar="exercise_physiology",
                group_id=f"CLUSTER_WHO_{i}",
            ))

        train_docs, val_docs = source_level_split(docs, val_ratio=0.30, seed=42)
        train_sources = {d.source_id for d in train_docs}
        val_sources = {d.source_id for d in val_docs}

        assert train_sources.isdisjoint(val_sources)

        # Check that all 15 CDC docs are in the same partition
        cdc_in_train = sum(1 for d in train_docs if d.source_id == "CDC_PHYS_ACTIVITY")
        cdc_in_val = sum(1 for d in val_docs if d.source_id == "CDC_PHYS_ACTIVITY")
        assert (cdc_in_train == 15 and cdc_in_val == 0) or (cdc_in_train == 0 and cdc_in_val == 15)

    def test_near_duplicate_groups_never_cross_partitions(self):
        """If documents from different sources share a near-duplicate cluster, they must not cross splits."""
        docs = [
            NormalizedDocument(
                doc_id="DOC_A1",
                source_id="SOURCE_ALPHA",
                title="Alpha Article 1",
                text="Identical near-duplicate content across sources discussing hydration and heat illness.",
                pillar="nutrition_hydration",
                group_id="SHARED_CLUSTER_HEAT",  # Shared near-duplicate cluster
            ),
            NormalizedDocument(
                doc_id="DOC_B1",
                source_id="SOURCE_BETA",
                title="Beta Article 1",
                text="Identical near-duplicate content across sources discussing hydration and heat illness.",
                pillar="nutrition_hydration",
                group_id="SHARED_CLUSTER_HEAT",  # Shared near-duplicate cluster
            ),
            NormalizedDocument(
                doc_id="DOC_C1",
                source_id="SOURCE_GAMMA",
                title="Gamma Article 1",
                text="Completely independent biomechanics content regarding force-velocity relationships.",
                pillar="biomechanics",
                group_id="INDEPENDENT_CLUSTER_1",
            ),
            NormalizedDocument(
                doc_id="DOC_D1",
                source_id="SOURCE_DELTA",
                title="Delta Article 1",
                text="Completely independent nutrition content regarding leucine threshold.",
                pillar="nutrition_hydration",
                group_id="INDEPENDENT_CLUSTER_2",
            ),
        ]

        for seed in (1, 7, 42, 99):
            train_docs, val_docs = source_level_split(docs, val_ratio=0.5, seed=seed)
            train_groups = {d.group_id for d in train_docs if d.group_id}
            val_groups = {d.group_id for d in val_docs if d.group_id}

            assert train_groups.isdisjoint(val_groups), f"Near-duplicate cluster crossed split at seed {seed}!"
            train_sources = {d.source_id for d in train_docs}
            val_sources = {d.source_id for d in val_docs}
            assert train_sources.isdisjoint(val_sources), f"Source IDs crossed split at seed {seed}!"

    def test_single_source_edge_case(self):
        """When only 1 source exists, all documents remain in train to maintain 100% source isolation."""
        docs = [
            NormalizedDocument(
                doc_id=f"SINGLE_{i}",
                source_id="ONLY_ONE_SOURCE",
                title=f"Section {i}",
                text=f"Text for single source document {i} with sufficient words.",
                pillar="exercise_physiology",
                group_id=f"GRP_{i}",
            )
            for i in range(5)
        ]
        train_docs, val_docs = source_level_split(docs, val_ratio=0.2, seed=42)
        assert len(train_docs) == 5
        assert len(val_docs) == 0
        assert set(d.source_id for d in train_docs).isdisjoint(set(d.source_id for d in val_docs))


# =============================================================================
# 10. Phase 10.1 Licensing Audit & Gate Integrity Tests
# =============================================================================

class TestPhase101LicensingAudit:
    """Verify legal gates, contractor IP checks, and isolation of human overrides."""

    def test_us_gov_contractor_work_rejected(self):
        """Contractor-authored material is not exempt under 17 U.S.C. § 105 and must be rejected."""
        gate = audit_license(
            license_name="Public Domain",
            legal_basis="17 U.S.C. § 105",
            is_us_gov_employee_work=False,  # Contractor work
        )
        assert not gate.is_compliant
        assert "Contractor or grantee work is not exempt" in gate.rejection_reason

    def test_us_gov_contractor_work_with_human_override(self):
        """Contractor work can be cleared ONLY with documented human legal review override."""
        gate = audit_license(
            license_name="Public Domain",
            legal_basis="17 U.S.C. § 105",
            is_us_gov_employee_work=False,
            allow_human_override=True,
            reviewer_id="LEGAL_COUNSEL_BPK",
            reviewer_notes="Verified FAR contract clause 52.227-14 assigning full IP to US Government in public domain.",
        )
        assert gate.is_compliant
        assert gate.human_override_approved
        assert gate.reviewer_id == "LEGAL_COUNSEL_BPK"

    def test_third_party_copyright_rejected_without_exclusions(self):
        """Works containing third-party copyright must be rejected without documented exclusions."""
        gate = audit_license(
            license_name="Public Domain",
            legal_basis="17 U.S.C. § 105",
            has_third_party_copyright=True,
            third_party_exclusions="",
        )
        assert not gate.is_compliant
        assert "contains third-party copyrighted material without documented exclusions" in gate.rejection_reason

    def test_third_party_copyright_accepted_with_exclusions(self):
        """Works containing third-party copyright pass when carve-outs/exclusions are documented."""
        gate = audit_license(
            license_name="Public Domain",
            legal_basis="17 U.S.C. § 105",
            has_third_party_copyright=True,
            third_party_exclusions="Purged Figure 4-2 (copyright commercial publisher) and Appendix C.",
        )
        assert gate.is_compliant
        assert gate.third_party_exclusions != ""

    def test_human_override_does_not_bypass_safety_screening(self, tokenizer: NovaTokenizer, benchmark: FitnessEvaluationBenchmark):
        """A human override on licensing MUST NOT bypass health safety screening."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            unsafe_file = tmp_path / "unsafe_manual.txt"
            unsafe_file.write_text(
                "Athletes should ignore sharp radiating spine pain and dry fast for several days to achieve maximum definition and rapid weight reduction across intense training blocks.",
                encoding="utf-8",
            )
            pipeline = SourceIngestionPipeline(tokenizer=tokenizer, benchmark=benchmark)
            meta = {
                "source_id": "TEST_UNSAFE",
                "title": "Unsafe Manual",
                "pillar": "exercise_physiology",
                "license": "Proprietary",
                "legal_basis": "Bilateral License",
            }
            # Provide human override for license
            docs = pipeline.ingest_file(
                unsafe_file,
                meta,
                allow_human_override=True,
                reviewer_id="REVIEWER_1",
                reviewer_notes="License cleared bilaterally.",
            )
            # Ingestion must NOT approve the document!
            assert len(docs) == 0
            assert len(pipeline.ingested_docs) == 0
            assert len(pipeline.quarantined_docs) == 1
            q_doc = list(pipeline.quarantined_docs.values())[0]
            assert q_doc.ingestion_status == IngestionStatus.QUARANTINED
            assert "SAFETY HAZARD" in q_doc.review_notes

    def test_human_override_does_not_bypass_benchmark_contamination(self, tokenizer: NovaTokenizer, benchmark: FitnessEvaluationBenchmark):
        """A human override on licensing MUST NOT bypass held-out benchmark contamination checks."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            leaked_file = tmp_path / "leaked_benchmark.txt"
            # Extract an actual prompt sentence from benchmark
            sample_prompt = list(benchmark.questions.values())[0].prompt
            leaked_file.write_text(
                f"Discussion on exercise science: {sample_prompt} with detailed explanation for students.",
                encoding="utf-8",
            )
            pipeline = SourceIngestionPipeline(tokenizer=tokenizer, benchmark=benchmark)
            meta = {
                "source_id": "TEST_LEAKED",
                "title": "Leaked Benchmark Manual",
                "pillar": "exercise_physiology",
                "license": "CC BY 4.0",
                "legal_basis": "Creative Commons Attribution 4.0",
            }
            docs = pipeline.ingest_file(
                leaked_file,
                meta,
                allow_human_override=True,
                reviewer_id="REVIEWER_1",
            )
            # Must be quarantined due to benchmark contamination
            assert len(docs) == 0
            assert len(pipeline.ingested_docs) == 0
            assert len(pipeline.quarantined_docs) == 1
            q_doc = list(pipeline.quarantined_docs.values())[0]
            assert q_doc.ingestion_status == IngestionStatus.QUARANTINED
            assert "BENCHMARK CONTAMINATION" in q_doc.review_notes


# =============================================================================
# 11. Phase 10.1 Multi-Format Extraction & Safety Fixture Tests
# =============================================================================

class TestPhase101ExtractionAndSafetyFixtures:
    """Verify HTML boilerplate stripping, compressed PDF streams, scanned PDF detection, and claim screening."""

    def test_html_navigation_and_boilerplate_stripping(self):
        """HTML pages with nav, scripts, styles, and footer must have only article text extracted."""
        raw_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>CDC Physical Activity</title>
            <style>body { font-family: sans-serif; } .nav { color: blue; }</style>
            <script>function trackUser() { return null; }</script>
        </head>
        <body>
            <header>
                <div class="site-title">U.S. Department of Health and Human Services</div>
                <nav>
                    <ul>
                        <li><a href="/home">Home</a></li>
                        <li><a href="/about">About Us</a></li>
                        <li><a href="/contact">Contact</a></li>
                    </ul>
                </nav>
            </header>
            <aside class="sidebar">
                <h3>Related Links</h3>
                <p>Check out our seasonal tips.</p>
            </aside>
            <main>
                <article>
                    <h1>Physical Activity Guidelines for Adults</h1>
                    <p>Adults should move more and sit less throughout the day. Some physical activity is better than none.</p>
                    <p>For substantial health benefits, adults should do at least 150 minutes a week of moderate-intensity aerobic activity.</p>
                </article>
            </main>
            <footer>
                <p>&copy; 2024 HHS CDC. All Rights Reserved. Privacy Policy | Disclaimers</p>
            </footer>
        </body>
        </html>
        """
        extracted = extract_text_from_html(raw_html)
        norm = normalize_corpus_text(extracted)
        assert "Adults should move more and sit less" in norm
        assert "150 minutes a week of moderate-intensity" in norm
        assert "function trackUser" not in norm
        assert "font-family: sans-serif" not in norm
        assert "Privacy Policy | Disclaimers" not in norm

    def test_compressed_pdf_stream_decompression(self):
        """Compressed /FlateDecode PDF text streams must be decompressed and extracted."""
        import zlib
        stream_text = b"BT /F1 12 Tf (Regular resistance training stimulates myofibrillar protein synthesis) Tj ET"
        compressed_bytes = zlib.compress(stream_text)
        pdf_bytes = (
            b"%PDF-1.4\n1 0 obj\n<< /Length " + str(len(compressed_bytes)).encode() + b" /Filter /FlateDecode >>\nstream\r\n"
            + compressed_bytes + b"\r\nendstream\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"
        )
        extracted = extract_text_from_pdf_stream(pdf_bytes)
        assert "Regular resistance training stimulates myofibrillar protein synthesis" in extracted

    def test_scanned_pdf_requiring_ocr_detection(self, tokenizer: NovaTokenizer, benchmark: FitnessEvaluationBenchmark):
        """Scanned image PDFs lacking text streams must be explicitly identified as SCANNED_PDF_REQUIRING_OCR."""
        scanned_pdf_bytes = (
            b"%PDF-1.4\n1 0 obj\n<< /Type /XObject /Subtype /Image /Width 600 /Height 800 /ColorSpace /DeviceRGB /BitsPerComponent 8 >>\n"
            b"stream\r\n\x00\x01\x02\x03\r\nendstream\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"
        )
        res = extract_text_from_pdf_stream(scanned_pdf_bytes)
        assert res == "SCANNED_PDF_REQUIRING_OCR"

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            pdf_path = tmp_path / "scanned_historical_doc.pdf"
            pdf_path.write_bytes(scanned_pdf_bytes)

            pipeline = SourceIngestionPipeline(tokenizer=tokenizer, benchmark=benchmark)
            meta = {
                "source_id": "SCANNED_SOURCE",
                "title": "Historical Scanned Manual",
                "pillar": "exercise_physiology",
                "license": "Public Domain",
                "legal_basis": "17 U.S.C. § 105",
            }
            docs = pipeline.ingest_file(pdf_path, meta)
            assert len(docs) == 0
            assert len(pipeline.quarantined_docs) == 1
            q_doc = list(pipeline.quarantined_docs.values())[0]
            assert q_doc.extraction_method == "pdf_text_extractor"
            assert "SCANNED_PDF_REQUIRING_OCR" in q_doc.review_notes

    def test_malformed_and_truncated_inputs(self, tokenizer: NovaTokenizer, benchmark: FitnessEvaluationBenchmark):
        """Malformed or truncated inputs must be safely handled and quarantined without uncaught exceptions."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            # Truncated HTML
            trunc_html = tmp_path / "trunc.html"
            trunc_html.write_text("<html><body><h1>Incomplete<p>Truncated without closing tags", encoding="utf-8")

            # Corrupted PDF
            corrupt_pdf = tmp_path / "corrupt.pdf"
            corrupt_pdf.write_bytes(b"%PDF-1.4\n1 0 obj\n<< /Filter /FlateDecode >>\nstream\r\nINVALID_ZLIB_DATA_TRUNCATED")

            # Corrupted JSON
            corrupt_json = tmp_path / "corrupt.json"
            corrupt_json.write_text('{"documents": [{"doc_id": "1", "text": "unclosed json', encoding="utf-8")

            pipeline = SourceIngestionPipeline(tokenizer=tokenizer, benchmark=benchmark)
            meta = {"pillar": "exercise_physiology", "license": "Public Domain", "legal_basis": "17 U.S.C. § 105"}

            # Processing should not crash
            pipeline.ingest_file(trunc_html, meta)
            pipeline.ingest_file(corrupt_pdf, meta)
            pipeline.ingest_file(corrupt_json, meta)

            # Check that corrupted files were rejected or quarantined
            assert len(pipeline.ingested_docs) == 0

    def test_safety_screener_true_positive_and_quarantine(self):
        """Unsafe health and medical claims must be detected with critical severity."""
        screener = HealthSafetyScreener()

        # 1. Unlicensed clinical diagnosis
        f1 = screener.screen_text("The trainer can diagnose a herniated disc by palpating the lumbar spine.")
        assert len(f1) > 0
        assert any(f["severity"] == "CRITICAL" for f in f1)

        # 2. Curative clinical disease claim
        f2 = screener.screen_text("This supplement protocol cures diabetes through cellular rejuvenation.")
        assert len(f2) > 0
        assert any(f["severity"] == "CRITICAL" for f in f2)

        # 3. Extreme dangerous dehydration
        f3 = screener.screen_text("Use sweat suits for cutting weight prior to weigh-in to drop 15 pounds quickly.")
        assert len(f3) > 0
        assert any(f["severity"] == "CRITICAL" for f in f3)

        # 4. Prohibited anabolic compounds
        f4 = screener.screen_text("Athletes cycling anabolic steroids should also stack clenbuterol for fat burning.")
        assert len(f4) > 0
        assert any(f["severity"] == "CRITICAL" for f in f4)

    def test_safety_screener_benign_text_and_limitation_analysis(self):
        """Evaluate benign sentences containing trigger keywords to audit false-positive limitations."""
        screener = HealthSafetyScreener()

        # Sentence 1: Benign dehydration prevention
        # "Athletes should maintain regular hydration to prevent dehydration during prolonged training."
        s1 = "Athletes should maintain regular hydration to prevent dehydration during prolonged training."
        flags1 = screener.screen_text(s1)
        # Should NOT trigger critical dehydration protocols (sweat suits or dry fasting)
        critical_flags1 = [f for f in flags1 if f["severity"] in ("CRITICAL", "HIGH")]
        assert len(critical_flags1) == 0, f"False positive on benign hydration prevention: {critical_flags1}"

        # Sentence 2: Benign cardiovascular differentiation
        s2 = "A structured warm-up reduces the risk of acute fracture or ligamentous tears during contact sports."
        flags2 = screener.screen_text(s2)
        critical_flags2 = [f for f in flags2 if f["severity"] in ("CRITICAL", "HIGH")]
        assert len(critical_flags2) == 0, f"False positive on injury prevention warm-up: {critical_flags2}"


# =============================================================================
# 11. Phase 10.2: Benchmark Contamination Resolution & Offset Auditing
# =============================================================================

class TestPhase102BenchmarkResolution:
    """Verifies rigorous resolution of benchmark title references, offset preservation, and leakage quarantine."""

    def test_harmless_title_reference_not_quarantined(self, benchmark: FitnessEvaluationBenchmark):
        """Standard publication titles (e.g. CDC measuring guide citing PAG 2nd edition) must not trigger quarantine."""
        detector = BenchmarkContaminationDetector(benchmark, n_gram_len=8)
        text = (
            "For more information regarding relative aerobic intensity, see Appendix 1 of the "
            "Physical Activity Guidelines for Americans, 2nd edition, pages 58 to 60 for detailed scales."
        )
        res = detector.check_text(text)
        assert res.is_contaminated is False, "Harmless publication title reference was incorrectly quarantined!"
        assert res.has_bibliographic_match is True
        assert len(res.matches) > 0

        match = res.matches[0]
        assert match.is_bibliographic_title is True
        assert match.is_genuine_leakage is False
        assert match.benchmark_question_id == "BENCH_P7_FACT_01"
        assert match.benchmark_version == "1.0.0"
        assert "Harmless citation match" in match.decision_rationale

        # Verify character offset accuracy
        extracted_snippet = text[match.char_start:match.char_end]
        assert "Physical Activity Guidelines for Americans, 2nd edition" in extracted_snippet

    def test_genuine_prompt_leakage_quarantined(self, benchmark: FitnessEvaluationBenchmark):
        """Operative inquiry question text must be detected as genuine leakage and quarantined."""
        detector = BenchmarkContaminationDetector(benchmark, n_gram_len=8)
        text = (
            "In this study, we examine what are the minimum weekly physical activity recommendations "
            "for substantial health benefits in adults according to recent literature."
        )
        res = detector.check_text(text)
        assert res.is_contaminated is True, "Substantive question leakage failed to trigger quarantine!"
        assert any(m.is_genuine_leakage for m in res.matches)
        assert any(m.match_origin == "Prompt" for m in res.matches)
        assert "QUARANTINE" in res.decision_rationale

    def test_genuine_answer_leakage_quarantined(self, benchmark: FitnessEvaluationBenchmark):
        """Canonical reference answer key text must be detected as genuine leakage and quarantined."""
        detector = BenchmarkContaminationDetector(benchmark, n_gram_len=8)
        text = (
            "As stated in our summary, adults require a weekly volume of 150 to 300 minutes of "
            "moderate-intensity physical activity or alternatively 75 to 150 minutes of vigorous aerobic exercise."
        )
        res = detector.check_text(text)
        assert res.is_contaminated is True, "Canonical answer key leakage failed to trigger quarantine!"
        assert any(m.is_genuine_leakage for m in res.matches)
        assert any(m.match_origin == "Answer" for m in res.matches)
        assert any("CRITICAL" in m.decision_rationale for m in res.matches)

    def test_mixed_title_and_leakage_quarantined(self, benchmark: FitnessEvaluationBenchmark):
        """Text containing both a publication title and substantive prompt leakage must be quarantined."""
        detector = BenchmarkContaminationDetector(benchmark, n_gram_len=8)
        text = (
            "Consult the Physical Activity Guidelines for Americans, 2nd edition to determine "
            "what are the minimum weekly physical activity recommendations for substantial health benefits in adults."
        )
        res = detector.check_text(text)
        assert res.has_bibliographic_match is True
        assert res.is_contaminated is True, "Genuine leakage was masked by bibliographic title!"
        assert any(m.is_genuine_leakage for m in res.matches)

    def test_pipeline_audit_preserves_matches_and_offsets(self, benchmark: FitnessEvaluationBenchmark, tmp_path: Path):
        """SourceIngestionPipeline must preserve match offsets, question ID, and rationale on NormalizedDocument."""
        pipeline = SourceIngestionPipeline(benchmark=benchmark, state_file=tmp_path / "test_state.json")
        sample_path = tmp_path / "cdc_measuring_sample.md"
        sample_path.write_text(
            "Intensity scales can be referenced in the Physical Activity Guidelines for Americans, 2nd edition appendix. "
            "Moderate activity allows talking but not singing, whereas vigorous activity prevents speaking full sentences.",
            encoding="utf-8",
        )
        meta = {
            "source_id": "US-CDC-PA-MEASURING-TEST",
            "title": "Measuring Activity Sample",
            "license": "Public Domain",
            "legal_basis": "17 U.S.C. § 105",
            "pillar": "exercise_physiology",
        }
        docs = pipeline.ingest_file(sample_path, meta)
        assert len(docs) == 1, "Document with harmless publication title citation should be accepted."
        doc = docs[0]
        assert doc.benchmark_contamination is False
        assert len(doc.benchmark_matches) > 0
        b_match = doc.benchmark_matches[0]
        assert b_match["is_bibliographic_title"] is True
        assert b_match["benchmark_question_id"] == "BENCH_P7_FACT_01"
        assert b_match["char_start"] > 0
        assert b_match["char_end"] > b_match["char_start"]
        assert "BIBLIOGRAPHIC_CITATION_MATCH" in doc.review_notes


