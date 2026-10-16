"""Phase 11.1 Real-Data Integration Tests & License Gate Hardening Verification.

Validates:
1. Actual staged dataset files in data/staging_phase11/ (train_staging.json, val_staging.json,
   phase11_staging_manifest.json, intake_registry.json).
2. Explicit disjointness assertions across train and validation for:
   - source_id
   - parent_source_id
   - duplicate group_id
3. Complete absence of any rejected or quarantined sources in either staging file.
4. Token reconciliation: sum of per-pillar tokens == sum of per-parent tokens == train+val tokens in manifest.
5. Hardened License Gate tests:
   - CC BY + AI-prohibition notice -> REJECTED (AI_TRAINING_PROHIBITED)
   - Plain CC BY -> ACCEPTED (PERMISSIVE_CC_BY)
   - NC (Non-commercial) -> REJECTED (RESTRICTED_NON_COMMERCIAL)
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from nova.ingestion import LicenseCategory, audit_license

REPO_ROOT = Path(__file__).resolve().parent.parent
STAGING_DIR = REPO_ROOT / "data" / "staging_phase11"


@pytest.fixture(scope="module")
def staging_data() -> dict:
    """Load actual staging artifacts from disk."""
    train_file = STAGING_DIR / "train_staging.json"
    val_file = STAGING_DIR / "val_staging.json"
    manifest_file = STAGING_DIR / "phase11_staging_manifest.json"
    registry_file = STAGING_DIR / "intake_registry.json"

    assert train_file.is_file(), f"Missing train_staging.json at {train_file}"
    assert val_file.is_file(), f"Missing val_staging.json at {val_file}"
    assert manifest_file.is_file(), f"Missing phase11_staging_manifest.json at {manifest_file}"
    assert registry_file.is_file(), f"Missing intake_registry.json at {registry_file}"

    train_docs = json.loads(train_file.read_text(encoding="utf-8"))
    val_docs = json.loads(val_file.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    registry = json.loads(registry_file.read_text(encoding="utf-8"))

    return {
        "train_docs": train_docs,
        "val_docs": val_docs,
        "manifest": manifest,
        "registry": registry,
    }


# ==============================================================================
# Task 2: Real-Data Integration Tests
# ==============================================================================

class TestPhase11StagedDataIntegrity:
    """Verifies invariant integrity on actual staged dataset files."""

    def test_train_val_source_id_disjoint(self, staging_data):
        """Assertion 1: train and validation partitions must have zero overlapping source_id."""
        train_sources = {d["source_id"] for d in staging_data["train_docs"]}
        val_sources = {d["source_id"] for d in staging_data["val_docs"]}
        overlap = train_sources & val_sources

        assert len(overlap) == 0, (
            f"VIOLATION: Cross-partition source_id leakage detected! "
            f"Overlapping sources: {sorted(list(overlap))}"
        )

    def test_train_val_parent_source_id_disjoint(self, staging_data):
        """Assertion 2: train and validation partitions must have zero overlapping parent_source_id."""
        train_parents = {d.get("parent_source_id") or d["source_id"] for d in staging_data["train_docs"]}
        val_parents = {d.get("parent_source_id") or d["source_id"] for d in staging_data["val_docs"]}
        overlap = train_parents & val_parents

        assert len(overlap) == 0, (
            f"VIOLATION: Cross-partition publication-level leakage detected! "
            f"Overlapping parent publications: {sorted(list(overlap))}"
        )

    def test_train_val_duplicate_group_id_disjoint(self, staging_data):
        """Assertion 3: train and validation partitions must have zero overlapping duplicate group_ids."""
        train_groups = {d["group_id"] for d in staging_data["train_docs"] if d.get("group_id")}
        val_groups = {d["group_id"] for d in staging_data["val_docs"] if d.get("group_id")}
        overlap = train_groups & val_groups

        assert len(overlap) == 0, (
            f"VIOLATION: Cross-partition near-duplicate cluster leakage detected! "
            f"Overlapping duplicate groups: {sorted(list(overlap))}"
        )

    def test_no_rejected_or_quarantined_sources_in_staging(self, staging_data):
        """Assertion 4: No rejected or quarantined candidate source contributes any document to staging."""
        # Identify non-approved sources from intake registry
        non_approved_sources = {
            entry["source_id"]
            for entry in staging_data["registry"]
            if entry.get("expected_result") != "APPROVED"
        }

        # Expected rejected/quarantined set includes FM 7-22, OpenStax, Proprietary, Unsafe, Scanned, etc.
        assert len(non_approved_sources) > 0, "No rejected/quarantined sources tracked in registry."

        train_sources = {d["source_id"] for d in staging_data["train_docs"]}
        val_sources = {d["source_id"] for d in staging_data["val_docs"]}
        staged_sources = train_sources | val_sources

        contaminated = staged_sources & non_approved_sources
        assert len(contaminated) == 0, (
            f"VIOLATION: Rejected or quarantined sources admitted into staging! "
            f"Admitted sources: {sorted(list(contaminated))}"
        )

    def test_token_sums_equal_manifest_totals(self, staging_data):
        """Assertion 5: Sum of per-pillar tokens == sum of per-parent tokens == train+val tokens in manifest."""
        manifest = staging_data["manifest"]
        train_docs = staging_data["train_docs"]
        val_docs = staging_data["val_docs"]

        # 1. Sum train and val tokens from actual document records
        sum_train = sum(d["token_count"] for d in train_docs)
        sum_val = sum(d["token_count"] for d in val_docs)
        sum_train_val = sum_train + sum_val

        # 2. Sum tokens by pillar from manifest
        sum_pillar = sum(p["token_count"] for p in manifest["pillar_coverage"].values())

        # 3. Sum tokens by parent publication from actual documents
        parent_totals: dict[str, int] = {}
        for d in train_docs + val_docs:
            pid = d.get("parent_source_id") or d["source_id"]
            parent_totals[pid] = parent_totals.get(pid, 0) + d["token_count"]
        sum_parent = sum(parent_totals.values())

        # Assert equality
        assert sum_pillar == sum_train_val, (
            f"Pillar token sum mismatch: sum_pillar={sum_pillar} vs sum_train_val={sum_train_val}"
        )
        assert sum_parent == sum_train_val, (
            f"Parent token sum mismatch: sum_parent={sum_parent} vs sum_train_val={sum_train_val}"
        )
        assert manifest["total_combined_tokens"] == sum_train_val, (
            f"Manifest total mismatch: manifest['total_combined_tokens']={manifest['total_combined_tokens']} "
            f"vs sum_train_val={sum_train_val}"
        )
        assert sum_train_val == 97808, f"Unexpected token total: {sum_train_val} (expected 97,808)"


# ==============================================================================
# Task 6(d): License Gate Hardening Tests
# ==============================================================================

class TestHardenedLicenseGate:
    """Verifies AI training prohibition detection and strict licensing precedence."""

    def test_cc_by_with_ai_prohibition_rejected(self):
        """A source labeled CC BY but containing an explicit AI-training prohibition MUST be rejected."""
        gate_res = audit_license(
            license_name="CC BY 4.0",
            legal_basis="Creative Commons Attribution 4.0 International",
            text_content=(
                "This publication is licensed under Creative Commons Attribution 4.0 International. "
                "NOTICE: Textbook content and resources may not be used for the training of artificial "
                "intelligence or large language models without prior written permission."
            ),
        )

        assert not gate_res.is_compliant, "CC BY with AI-training prohibition was incorrectly approved!"
        assert gate_res.category == LicenseCategory.AI_TRAINING_PROHIBITED
        assert "AI/LLM training prohibition" in gate_res.rejection_reason

    def test_plain_cc_by_accepted(self):
        """A standard CC BY 4.0 source without AI training prohibitions MUST be accepted."""
        gate_res = audit_license(
            license_name="CC BY 4.0",
            legal_basis="Creative Commons Attribution 4.0 International",
            text_content="This scientific research article is freely licensed under CC BY 4.0 without restrictions.",
        )

        assert gate_res.is_compliant, f"Plain CC BY 4.0 was unexpectedly rejected: {gate_res.rejection_reason}"
        assert gate_res.category == LicenseCategory.PERMISSIVE_CC_BY
        assert gate_res.requires_attribution is True

    def test_non_commercial_rejected(self):
        """A CC BY-NC or CC BY-NC-SA source MUST be rejected due to non-commercial restriction."""
        gate_res = audit_license(
            license_name="CC BY-NC-SA 4.0",
            legal_basis="Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International",
            text_content="Content is licensed for non-commercial educational use only.",
        )

        assert not gate_res.is_compliant, "Non-commercial license was incorrectly approved!"
        assert gate_res.category == LicenseCategory.RESTRICTED_NON_COMMERCIAL
        assert "Non-commercial restriction" in gate_res.rejection_reason
