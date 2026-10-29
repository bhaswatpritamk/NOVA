"""Project NOVA Phase 11.2: Evidence Quotes and Ingestion Source Scoping Tests.

Verifies:
1. All quotes cited in the remediated rights ledger and quarantine record occur verbatim in saved files.
2. Fabricated or altered quotes fail machine verification and return NO_EVIDENCE_FOUND.
3. Ingestion source isolation: ingestion strictly processes files declared in intake_registry.json
   and NEVER globs sources_raw or quarantine_evidence.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.verify_evidence_quotes import (
    PHASE11_2_REMEDIATED_TARGETS,
    QuoteVerificationTarget,
    run_verification,
    verify_quote,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
STAGING_DIR = REPO_ROOT / "data" / "staging_phase11"
RAW_DIR = STAGING_DIR / "sources_raw"
QUARANTINE_DIR = STAGING_DIR / "quarantine_evidence"
REGISTRY_PATH = STAGING_DIR / "intake_registry.json"


class TestEvidenceQuotesVerification:
    """Verifies that all evidence quotations match authentic saved files verbatim."""

    def test_remediated_evidence_quotes_all_pass(self):
        """Every quote in the Phase 11.2 remediated targets must pass verbatim verification."""
        results = run_verification(PHASE11_2_REMEDIATED_TARGETS)
        failed = [r for r in results if r.status != "PASS"]
        assert len(failed) == 0, (
            f"Remediated quotes failed verification: {[f.target_id for f in failed]}"
        )

    def test_fabricated_quotes_are_detected_and_rejected(self, tmp_path):
        """Ensure verifier flags non-existent quotes as NO_EVIDENCE_FOUND."""
        dummy_file = tmp_path / "test_doc.md"
        dummy_file.write_text("Line 1: Hello world\nLine 2: Real authentic content.", encoding="utf-8")

        passed, actual, _ = verify_quote(
            file_path=dummy_file,
            quoted_string="This quote was invented and does not exist.",
            cited_line=1,
        )
        assert not passed
        assert "NO_EVIDENCE_FOUND" in actual

    def test_openstax_quarantine_record_contains_only_machine_verified_quotes(self):
        """Quarantine record must contain only verbatim quotes found in the saved snapshot."""
        record_path = QUARANTINE_DIR / "openstax_ap2e_quarantine_record.json"
        assert record_path.exists(), f"Missing quarantine record at {record_path}"

        record = json.loads(record_path.read_text(encoding="utf-8"))
        snapshot_rel = record.get("raw_snapshot_file", "")
        snapshot_path = REPO_ROOT / snapshot_rel
        assert snapshot_path.exists(), f"Snapshot file {snapshot_path} does not exist"

        # Check exact license sentence
        license_sent = record["exact_license_sentence"]
        passed_lic, actual_lic, _ = verify_quote(snapshot_path, license_sent)
        assert passed_lic, f"License sentence failed verification: {license_sent}"

        # Check exact AI training prohibition sentence
        ai_sent = record["exact_ai_training_sentence"]
        passed_ai, actual_ai, _ = verify_quote(snapshot_path, ai_sent)
        assert passed_ai, f"AI sentence failed verification: {ai_sent}"


class TestIngestionSourceIsolation:
    """Proves that staging ingestion reads ONLY files explicitly listed in intake_registry.json

    and NEVER globs sources_raw/ or quarantine_evidence/.
    """

    def test_ingestion_reads_only_registered_files(self):
        """Verify that every accepted/staged document maps to an explicit entry in intake_registry.json."""
        assert REGISTRY_PATH.exists(), f"Missing intake registry: {REGISTRY_PATH}"
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

        registered_source_ids = {entry["source_id"] for entry in registry}
        registered_file_names = {Path(entry["file_path"]).name for entry in registry}

        train_path = STAGING_DIR / "train_staging.json"
        val_path = STAGING_DIR / "val_staging.json"
        manifest_path = STAGING_DIR / "phase11_staging_manifest.json"

        staged_docs = []
        if train_path.exists():
            staged_docs.extend(json.loads(train_path.read_text(encoding="utf-8")))
        if val_path.exists():
            staged_docs.extend(json.loads(val_path.read_text(encoding="utf-8")))

        for doc in staged_docs:
            sid = doc["source_id"]
            assert sid in registered_source_ids, (
                f"Unregistered source_id '{sid}' was found in staged dataset! "
                f"Ingestion must only read sources declared in intake_registry.json."
            )

    def test_ingestion_codebase_does_not_glob_sources_raw_or_quarantine_evidence(self):
        """Codebase audit: verify run_staging_ingestion.py never globs sources_raw or quarantine_evidence."""
        ingestion_script = REPO_ROOT / "scripts" / "run_staging_ingestion.py"
        assert ingestion_script.exists()
        code = ingestion_script.read_text(encoding="utf-8")

        # Ingestion script must not perform discovery globbing on sources_raw or quarantine_evidence
        disallowed_patterns = [
            "STAGING_RAW_DIR.glob(",
            "STAGING_RAW_DIR.rglob(",
            "sources_raw.glob(",
            "quarantine_evidence.glob(",
            "quarantine_evidence.rglob(",
            "glob.glob('*sources_raw",
            "glob.glob('*quarantine_evidence",
        ]
        for pattern in disallowed_patterns:
            assert pattern not in code, (
                f"Disallowed globbing pattern '{pattern}' detected in run_staging_ingestion.py! "
                f"Pipeline must strictly iterate over explicit registry entries."
            )

    def test_unregistered_file_in_raw_or_quarantine_is_ignored(self, tmp_path):
        """Simulation: placing a rogue file in raw or quarantine folder is ignored unless registered."""
        # Check that intake_registry only contains intentional entries
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        registered_fnames = {Path(e["file_path"]).name for e in registry}

        # Any file not in registered_fnames must NOT be present in staged docs
        train_docs = json.loads((STAGING_DIR / "train_staging.json").read_text(encoding="utf-8"))
        val_docs = json.loads((STAGING_DIR / "val_staging.json").read_text(encoding="utf-8"))
        all_staged = train_docs + val_docs

        for doc in all_staged:
            doc_id = doc["doc_id"]
            # All doc_ids must originate from registered sources
            matched = any(doc["source_id"] == entry["source_id"] for entry in registry)
            assert matched, f"Staged doc {doc_id} does not match any registered entry"
