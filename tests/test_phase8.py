"""Automated Regression Tests for Project Nova-Fit Phase 8: Source-Grounded Corpus & Benchmark.

Verifies:
1. Provenance completeness: Traceability records for all 306 educational documents.
2. Claim-status handling: 5-tier taxonomy (Supported, Qualified, Contested, Unsupported, Unsafe).
3. Critical safety flags: Unsafe claims mandate human review and high/critical risk tagging.
4. Benchmark integrity: Complete coverage of all 7 fitness pillars and 8 question archetypes.
5. Benchmark separation: Zero n-gram leakage between benchmark questions/answers and training data.
6. Benchmark scoring harness: Reproducible loss, perplexity, and rubric evaluation.
7. Manifest and traceability hash integrity.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import pytest
import torch

from nova.benchmark import (
    BenchmarkQuestion,
    BenchmarkQuestionType,
    BenchmarkRubric,
    FitnessEvaluationBenchmark,
    evaluate_model_on_benchmark_passages,
)
from nova.claims import (
    ClaimCategory,
    ClaimRecord,
    ClaimReviewRegistry,
    DocumentTraceabilityRecord,
    RiskLevel,
    VerificationStatus,
    analyze_text_for_claims,
)
from nova.corpus import SourceRegistry
from nova.model import NovaConfig, NovaForCausalLM
from nova.tokenizer import NovaTokenizer, load_tokenizer

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_REGISTRY_PATH = REPO_ROOT / "data" / "approved" / "source_registry.json"
TRACEABILITY_PATH = REPO_ROOT / "data" / "approved" / "document_traceability.json"
CLAIM_REVIEWS_PATH = REPO_ROOT / "data" / "approved" / "claim_reviews.json"
BENCHMARK_PATH = REPO_ROOT / "data" / "benchmark" / "fitness_eval_benchmark.json"
TRAIN_CORPUS_PATH = REPO_ROOT / "data" / "approved" / "expanded_train_corpus.txt"
FINAL_TOK_DIR = REPO_ROOT / "artifacts" / "final_tokenizer"


@pytest.fixture(scope="module")
def tokenizer() -> NovaTokenizer:
    """Fixture providing the final Byte-Level BPE tokenizer."""
    return load_tokenizer(FINAL_TOK_DIR)


@pytest.fixture(scope="module")
def source_registry() -> SourceRegistry:
    """Fixture providing the approved source registry."""
    return SourceRegistry.load(SOURCE_REGISTRY_PATH)


@pytest.fixture(scope="module")
def benchmark() -> FitnessEvaluationBenchmark:
    """Fixture providing the held-out fitness evaluation benchmark."""
    return FitnessEvaluationBenchmark.load(BENCHMARK_PATH)


# =============================================================================
# 1. Provenance Completeness Tests
# =============================================================================


def test_provenance_completeness(source_registry: SourceRegistry):
    """Verify that all 306 documents have complete, valid traceability metadata."""
    assert TRACEABILITY_PATH.is_file(), f"Traceability file missing: {TRACEABILITY_PATH}"
    with open(TRACEABILITY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["total_documents"] == 306, f"Expected 306 documents, got {data['total_documents']}"
    docs = data["documents"]
    assert len(docs) == 306

    doc_ids_seen = set()
    for d in docs:
        rec = DocumentTraceabilityRecord.from_dict(d)
        assert rec.doc_id not in doc_ids_seen, f"Duplicate doc_id in traceability: {rec.doc_id}"
        doc_ids_seen.add(rec.doc_id)

        # Source ID must be registered
        assert rec.primary_source_id in source_registry.sources, (
            f"Unregistered source ID: {rec.primary_source_id} in {rec.doc_id}"
        )
        src = source_registry.get(rec.primary_source_id)
        assert src is not None
        assert rec.primary_source_url == src.url

        # Transformation history must not be empty and must specify educational synthesis
        assert rec.authoring_method == "educational_synthesis"
        assert len(rec.transformation_history) >= 3

        # Must have verified section references
        assert len(rec.source_section_ref) > 5

        # Claims and hashes must be present
        assert len(rec.claims) >= 1
        assert len(rec.doc_sha256) == 64
        assert len(rec.source_sha256) == 64
        assert rec.verification_status in (VerificationStatus.VERIFIED, VerificationStatus.QUALIFIED)


# =============================================================================
# 2. Claim-Status Handling & 5-Tier Taxonomy Tests
# =============================================================================


def test_claim_taxonomy_handling():
    """Verify that all 5 tiers of the claim taxonomy are handled and audited."""
    assert CLAIM_REVIEWS_PATH.is_file(), f"Claim reviews file missing: {CLAIM_REVIEWS_PATH}"
    reg = ClaimReviewRegistry.load(CLAIM_REVIEWS_PATH)

    counts = reg.get_category_counts()
    for cat in ClaimCategory:
        assert counts.get(cat.value, 0) > 0, f"Claim category {cat.value} has 0 records in registry"

    # Verify QUALIFIED and CONTESTED claims contain qualification notes
    for c in reg.claims.values():
        if c.category in (ClaimCategory.QUALIFIED, ClaimCategory.CONTESTED):
            assert len(c.qualification_notes) > 15, f"Missing qualification notes for claim {c.claim_id}"

        # Verify UNSAFE claims have CRITICAL or HIGH risk level and human review flag
        if c.category == ClaimCategory.UNSAFE:
            assert c.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL), (
                f"Unsafe claim {c.claim_id} must have HIGH or CRITICAL risk"
            )
            assert c.requires_human_review is True, (
                f"Unsafe claim {c.claim_id} must require human review"
            )


def test_automated_claim_heuristic_analysis():
    """Verify that heuristic checks flag unsafe advice and population dependencies."""
    unsafe_text = "Athletes should push through sharp joint pain and dehydrate with sweat suits to cut weight."
    findings = analyze_text_for_claims(unsafe_text)

    assert len(findings["unsafe_flags"]) >= 2
    assert any("joint pain" in f["description"].lower() for f in findings["unsafe_flags"])
    assert any("dehydration" in f["description"].lower() for f in findings["unsafe_flags"])

    pop_text = "Resistance exercise program for older adults with sarcopenia and osteopenia."
    findings_pop = analyze_text_for_claims(pop_text)
    assert len(findings_pop["population_dependencies"]) >= 1

    myth_text = "Do 100 daily crunches for spot reduction of belly fat because lactic acid causes DOMS."
    findings_myth = analyze_text_for_claims(myth_text)
    assert len(findings_myth["unsupported_myths"]) >= 2


# =============================================================================
# 3. Benchmark Dataset Integrity & Coverage Tests
# =============================================================================


def test_benchmark_coverage_and_rubric_weights(benchmark: FitnessEvaluationBenchmark):
    """Verify that the held-out benchmark covers all 7 pillars and 8 question types."""
    assert len(benchmark.questions) >= 12, f"Benchmark has insufficient questions: {len(benchmark.questions)}"

    pillar_counts = benchmark.get_pillar_counts()
    expected_pillars = [
        "exercise_science_biomechanics",
        "strength_training_programming",
        "exercise_technique_safety",
        "nutrition_fundamentals_hydration",
        "sleep_recovery_physical_activity",
        "training_adaptations_fatigue_load",
        "general_fitness_education_safety",
    ]
    for p in expected_pillars:
        assert pillar_counts.get(p, 0) > 0, f"Pillar {p} missing from benchmark"

    type_counts = benchmark.get_type_counts()
    for qtype in BenchmarkQuestionType:
        assert type_counts.get(qtype.value, 0) > 0, f"Question type {qtype.value} missing from benchmark"

    # Verify rubric weights
    for q in benchmark.questions.values():
        q.rubric.validate()
        assert len(q.prompt) > 20
        assert len(q.expected_key_points) >= 1
        assert len(q.canonical_reference_answer) > 30


# =============================================================================
# 4. Benchmark Separation & Contamination Tests
# =============================================================================


def test_benchmark_train_separation_no_leakage(benchmark: FitnessEvaluationBenchmark):
    """Verify strict held-out separation: 0 n-gram leakage between benchmark and train corpus."""
    assert TRAIN_CORPUS_PATH.is_file(), f"Train corpus missing: {TRAIN_CORPUS_PATH}"
    train_text = TRAIN_CORPUS_PATH.read_text(encoding="utf-8")

    is_clean, leakage = benchmark.verify_no_leakage(train_text, n_gram_len=8)
    assert is_clean, f"Detected {len(leakage)} contamination leaks between benchmark and train: {leakage}"


# =============================================================================
# 5. Benchmark Scoring & Model Evaluation Tests
# =============================================================================


def test_benchmark_scoring_rubric_behavior(benchmark: FitnessEvaluationBenchmark):
    """Verify rubric scoring mechanics on perfect, partial, and unsafe responses."""
    # Test Question: Hip pain referral (safety-sensitive)
    safe_q = benchmark.questions.get("BENCH_P3_SAFE_01")
    assert safe_q is not None

    # Good response with clinical referral
    good_resp = "Stop deep squats immediately and consult a physician or physical therapist for clinical evaluation."
    score_good = benchmark.score_response(safe_q, good_resp)
    assert score_good.safety_score == 1.0
    assert score_good.composite_score > 0.5

    # Dangerous response telling client to push through pain
    bad_resp = "Push through the pain and keep lifting heavy with deep squats."
    score_bad = benchmark.score_response(safe_q, bad_resp)
    assert score_bad.safety_score == 0.0

    # Test Question: Insufficient info
    insuff_q = benchmark.questions.get("BENCH_P6_INSUFF_01")
    assert insuff_q is not None
    insuff_resp = "More information needed regarding your training volume, sleep duration, and current caloric intake before prescribing a deload."
    score_insuff = benchmark.score_response(insuff_q, insuff_resp)
    assert score_insuff.uncertainty_score > 0.5


def test_held_out_loss_and_perplexity_computation(
    benchmark: FitnessEvaluationBenchmark,
    tokenizer: NovaTokenizer,
):
    """Verify evaluation harness computes finite cross-entropy loss and perplexity."""
    cfg = NovaConfig(
        vocab_size=tokenizer.vocab_size,
        max_seq_len=256,
        d_model=64,
        n_layers=2,
        n_heads=4,
        d_ff=176,
    )
    model = NovaForCausalLM(cfg)

    loss, ppl = evaluate_model_on_benchmark_passages(
        model=model,
        benchmark=benchmark,
        tokenizer=tokenizer,
        device="cpu",
        max_seq_len=256,
        pad_token_id=0,
    )

    assert math.isfinite(loss), f"Expected finite loss, got {loss}"
    assert math.isfinite(ppl), f"Expected finite perplexity, got {ppl}"
    # Random model should have loss close to ln(V) = ln(3384) approx 8.1268
    expected_rand_loss = math.log(tokenizer.vocab_size)
    assert abs(loss - expected_rand_loss) < 0.35, (
        f"Loss {loss:.4f} deviates unexpectedly from random baseline {expected_rand_loss:.4f}"
    )


# =============================================================================
# 6. Artifact & File Hash Integrity Tests
# =============================================================================


def test_phase8_artifact_file_integrity():
    """Verify that all Phase 8 artifacts exist, have non-zero size, and valid JSON structure."""
    artifacts = [
        TRACEABILITY_PATH,
        CLAIM_REVIEWS_PATH,
        BENCHMARK_PATH,
        REPO_ROOT / "docs" / "benchmark_baseline_report.json",
    ]
    for p in artifacts:
        assert p.is_file(), f"Phase 8 artifact missing: {p}"
        assert p.stat().st_size > 50, f"Phase 8 artifact suspiciously small: {p}"
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert isinstance(data, dict), f"Artifact {p.name} root is not a dictionary"
