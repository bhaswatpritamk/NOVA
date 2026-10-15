#!/usr/bin/env python3
"""Project NOVA Phase 10.1: Controlled Staging Ingestion & Audit Pipeline.

Executes controlled ingestion test on verified primary sources:
- Ingests verified open-access and public domain health/fitness sources.
- Tests rejection of non-compliant proprietary works and quarantine of unsafe texts.
- Tests identification of scanned image PDFs requiring OCR.
- Evaluates benchmark contamination against held-out benchmark.
- Performs disjoint source-level split (guaranteeing train/val source disjointness).
- Emits cryptographic staging manifest and audit report in data/staging_phase10/.
- Does NOT replace or modify authoritative Phase 8 artifacts.
"""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from nova.benchmark import FitnessEvaluationBenchmark
from nova.ingestion import (
    FitnessPillar,
    IngestionStatus,
    LicenseGateResult,
    NormalizedDocument,
    Phase10Manifest,
    SourceIngestionPipeline,
    audit_license,
    extract_text_from_html,
    extract_text_from_markdown,
    normalize_corpus_text,
    source_level_split,
)
from nova.tokenizer import load_tokenizer

REPO_ROOT = Path(__file__).resolve().parent.parent
STAGING_DIR = REPO_ROOT / "data" / "staging_phase10"
STAGING_RAW_DIR = STAGING_DIR / "sources_raw"
BENCHMARK_PATH = REPO_ROOT / "data" / "benchmark" / "fitness_eval_benchmark.json"
TOKENIZER_DIR = REPO_ROOT / "artifacts" / "final_tokenizer"

STEP_FILES = {
    "CDC_ADULTS": Path(r"C:\Users\Bhaswat\.gemini\antigravity-ide\brain\1758fcd9-8e21-4eaf-bfc9-c4a19f11a5fa\.system_generated\steps\212\content.md"),
    "NIOSH_HEAT": Path(r"C:\Users\Bhaswat\.gemini\antigravity-ide\brain\1758fcd9-8e21-4eaf-bfc9-c4a19f11a5fa\.system_generated\steps\251\content.md"),
    "PLOS_HYPERTROPHY": Path(r"C:\Users\Bhaswat\.gemini\antigravity-ide\brain\1758fcd9-8e21-4eaf-bfc9-c4a19f11a5fa\.system_generated\steps\253\content.md"),
    "CDC_MEASURING": Path(r"C:\Users\Bhaswat\.gemini\antigravity-ide\brain\1758fcd9-8e21-4eaf-bfc9-c4a19f11a5fa\.system_generated\steps\374\content.md"),
    "CDC_OLDER_ADULTS": Path(r"C:\Users\Bhaswat\.gemini\antigravity-ide\brain\1758fcd9-8e21-4eaf-bfc9-c4a19f11a5fa\.system_generated\steps\376\content.md"),
}


def prepare_raw_sources() -> List[Dict[str, Any]]:
    """Copy and establish raw files in staging directory with complete metadata."""
    STAGING_RAW_DIR.mkdir(parents=True, exist_ok=True)

    sources_meta = []

    # 1. CDC Adult Activity Guidelines
    f1 = STAGING_RAW_DIR / "us_cdc_pa_adults_2022.md"
    shutil.copyfile(STEP_FILES["CDC_ADULTS"], f1)
    sources_meta.append({
        "file_path": str(f1),
        "source_id": "US-CDC-PA-ADULTS-2022",
        "title": "CDC Physical Activity Guidelines for Adults: Overview and Aerobic/Strength Recommendations",
        "author": "Division of Nutrition, Physical Activity, and Obesity, CDC",
        "publisher": "Centers for Disease Control and Prevention (CDC), U.S. Department of Health and Human Services",
        "publication_date": "2022-06-01",
        "retrieval_date": "2026-10-15",
        "url": "https://www.cdc.gov/physical-activity-basics/guidelines/adults.html",
        "license": "Public Domain",
        "legal_basis": "17 U.S.C. § 105",
        "is_us_gov_employee_work": True,
        "has_third_party_copyright": False,
        "third_party_exclusions": "None required (no non-free third-party figures in extract).",
        "attribution_required": False,
        "mandatory_attribution_text": "Centers for Disease Control and Prevention (CDC), U.S. Department of Health and Human Services.",
        "pillar": "exercise_physiology",
        "expected_result": "APPROVED",
    })

    # 2. CDC Measuring Activity Intensity
    f2 = STAGING_RAW_DIR / "us_cdc_pa_measuring_2022.md"
    shutil.copyfile(STEP_FILES["CDC_MEASURING"], f2)
    sources_meta.append({
        "file_path": str(f2),
        "source_id": "US-CDC-PA-MEASURING-2022",
        "title": "Measuring Physical Activity Intensity: Target Heart Rate and Borg Perceived Exertion Scale",
        "author": "Division of Nutrition, Physical Activity, and Obesity, CDC",
        "publisher": "Centers for Disease Control and Prevention (CDC), U.S. Department of Health and Human Services",
        "publication_date": "2022-06-01",
        "retrieval_date": "2026-10-15",
        "url": "https://www.cdc.gov/physical-activity-basics/measuring/index.html",
        "license": "Public Domain",
        "legal_basis": "17 U.S.C. § 105",
        "is_us_gov_employee_work": True,
        "has_third_party_copyright": False,
        "third_party_exclusions": "None.",
        "attribution_required": False,
        "mandatory_attribution_text": "Centers for Disease Control and Prevention (CDC), U.S. Department of Health and Human Services.",
        "pillar": "exercise_physiology",
        "expected_result": "APPROVED",
    })

    # 3. CDC Older Adults Recommendations
    f3 = STAGING_RAW_DIR / "us_cdc_pa_older_2022.md"
    shutil.copyfile(STEP_FILES["CDC_OLDER_ADULTS"], f3)
    sources_meta.append({
        "file_path": str(f3),
        "source_id": "US-CDC-PA-OLDER-2022",
        "title": "Physical Activity Guidelines for Older Adults: Multicomponent Functional Training and Fall Prevention",
        "author": "Division of Nutrition, Physical Activity, and Obesity, CDC",
        "publisher": "Centers for Disease Control and Prevention (CDC), U.S. Department of Health and Human Services",
        "publication_date": "2022-06-01",
        "retrieval_date": "2026-10-15",
        "url": "https://www.cdc.gov/physical-activity-basics/adding-older-adults/index.html",
        "license": "Public Domain",
        "legal_basis": "17 U.S.C. § 105",
        "is_us_gov_employee_work": True,
        "has_third_party_copyright": False,
        "third_party_exclusions": "None.",
        "attribution_required": False,
        "mandatory_attribution_text": "Centers for Disease Control and Prevention (CDC), U.S. Department of Health and Human Services.",
        "pillar": "injury_prevention",
        "expected_result": "APPROVED",
    })

    # 4. NIOSH Heat Stress Recommendations
    f4 = STAGING_RAW_DIR / "us_cdc_niosh_heat_2016.md"
    shutil.copyfile(STEP_FILES["NIOSH_HEAT"], f4)
    sources_meta.append({
        "file_path": str(f4),
        "source_id": "US-CDC-NIOSH-HEAT-2016",
        "title": "NIOSH Workplace Recommendations for Heat Stress: Acclimatization, Hydration, and Rest Cycles",
        "author": "National Institute for Occupational Safety and Health (NIOSH)",
        "publisher": "Centers for Disease Control and Prevention (CDC), U.S. Department of Health and Human Services",
        "publication_date": "2016-02-01",
        "retrieval_date": "2026-10-15",
        "url": "https://www.cdc.gov/niosh/topics/heatstress/recommendations.html",
        "license": "Public Domain",
        "legal_basis": "17 U.S.C. § 105",
        "is_us_gov_employee_work": True,
        "has_third_party_copyright": False,
        "third_party_exclusions": "None.",
        "attribution_required": False,
        "mandatory_attribution_text": "National Institute for Occupational Safety and Health (NIOSH), Centers for Disease Control and Prevention (CDC).",
        "pillar": "nutrition_hydration",
        "expected_result": "APPROVED",
    })

    # 5. PLOS ONE CC BY 4.0 Hypertrophy Meta-Analysis
    f5 = STAGING_RAW_DIR / "plos_pone_0215877.html"
    raw_plos = STEP_FILES["PLOS_HYPERTROPHY"].read_text(encoding="utf-8")
    idx = raw_plos.find("<!DOCTYPE")
    if idx != -1:
        raw_plos = raw_plos[idx:]
    f5.write_text(raw_plos, encoding="utf-8")
    sources_meta.append({
        "file_path": str(f5),
        "source_id": "PLOS-PONE-0215877",
        "title": "Effects of resistance training frequency on measures of muscle hypertrophy: a systematic review and meta-analysis",
        "author": "Brad J. Schoenfeld, Dan Ogborn, James W. Krieger",
        "publisher": "PLOS ONE (Public Library of Science)",
        "publication_date": "2019-02-27",
        "retrieval_date": "2026-10-15",
        "url": "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0215877",
        "license": "CC BY 4.0",
        "legal_basis": "Creative Commons Attribution 4.0 International",
        "is_us_gov_employee_work": None,
        "has_third_party_copyright": False,
        "third_party_exclusions": "None.",
        "attribution_required": True,
        "mandatory_attribution_text": "Schoenfeld BJ, Ogborn D, Krieger JW (2019) Effects of resistance training frequency on measures of muscle hypertrophy: a systematic review and meta-analysis. PLOS ONE 14(2): e0215877. Licensed under CC BY 4.0.",
        "pillar": "strength_training",
        "expected_result": "APPROVED",
    })

    # 6. Negative Control 1: Restricted Proprietary Book (Must be REJECTED at licensing gate)
    f6 = STAGING_RAW_DIR / "rejected_proprietary_sample.txt"
    f6.write_text(
        "Commercial copyrighted fitness training encyclopedia. All rights reserved. No part of this publication may be reproduced, stored, or transmitted without prior written permission from the publisher.",
        encoding="utf-8",
    )
    sources_meta.append({
        "file_path": str(f6),
        "source_id": "SAMPLE-REJECTED-PROPRIETARY",
        "title": "Commercial Strength Training Manual (Unlicensed)",
        "author": "Private Commercial Author",
        "publisher": "Commercial Trade Publishing Inc",
        "publication_date": "2021-01-01",
        "retrieval_date": "2026-10-15",
        "url": "https://example.com/commercial-book",
        "license": "Proprietary",
        "legal_basis": "All Rights Reserved",
        "pillar": "strength_training",
        "expected_result": "REJECTED_LICENSE",
    })

    # 7. Negative Control 2: Unsafe Health Claims (Must be QUARANTINED at safety gate)
    f7 = STAGING_RAW_DIR / "quarantine_unsafe_sample.txt"
    f7.write_text(
        "Unsafe training protocol advising athletes to dry fast for several days to shred water weight, ignore sharp joint pain, and take clenbuterol alongside anabolic steroids for extreme conditioning.",
        encoding="utf-8",
    )
    sources_meta.append({
        "file_path": str(f7),
        "source_id": "SAMPLE-QUARANTINED-UNSAFE",
        "title": "Extreme Weight Cut & PED Protocol",
        "author": "Anonymous Underground Forum",
        "publisher": "Underground Fitness Community",
        "publication_date": "2023-01-01",
        "retrieval_date": "2026-10-15",
        "url": "https://example.com/unsafe-protocol",
        "license": "CC0",
        "legal_basis": "Creative Commons Zero 1.0",
        "pillar": "exercise_physiology",
        "expected_result": "QUARANTINED_SAFETY",
    })

    # 8. Negative Control 3: Scanned PDF requiring OCR (Must be QUARANTINED as SCANNED_PDF_REQUIRING_OCR)
    f8 = STAGING_RAW_DIR / "quarantine_scanned_sample.pdf"
    scanned_bytes = (
        b"%PDF-1.4\n1 0 obj\n<< /Type /XObject /Subtype /Image /Width 800 /Height 1200 /ColorSpace /DeviceRGB /BitsPerComponent 8 >>\n"
        b"stream\r\n\x00\x01\x02\x03\r\nendstream\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"
    )
    f8.write_bytes(scanned_bytes)
    sources_meta.append({
        "file_path": str(f8),
        "source_id": "SAMPLE-QUARANTINED-SCANNED",
        "title": "Historical Physical Culture Pamphlet (Scanned Image)",
        "author": "Historical Archive",
        "publisher": "Public Domain Archive",
        "publication_date": "1910-01-01",
        "retrieval_date": "2026-10-15",
        "url": "https://example.com/scanned-pamphlet.pdf",
        "license": "Public Domain",
        "legal_basis": "17 U.S.C. § 105",
        "is_us_gov_employee_work": True,
        "pillar": "fitness_education",
        "expected_result": "QUARANTINED_OCR",
    })

    # Calculate SHA-256 for all raw files
    for item in sources_meta:
        p = Path(item["file_path"])
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        item["raw_sha256"] = h

    registry_path = STAGING_DIR / "intake_registry.json"
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(sources_meta, f, indent=2)

    return sources_meta


def run_staging_pipeline() -> Dict[str, Any]:
    """Execute end-to-end controlled ingestion, splitting, and audit."""
    print("=" * 80)
    print("NOVA PHASE 10.1: CONTROLLED STAGING INGESTION TEST")
    print("=" * 80)

    # 1. Prepare raw source assets and metadata
    sources = prepare_raw_sources()
    print(f"Prepared {len(sources)} candidate sources in {STAGING_RAW_DIR}")

    # 2. Load tokenizer and benchmark
    tokenizer = load_tokenizer(str(TOKENIZER_DIR))
    benchmark = FitnessEvaluationBenchmark.load(str(BENCHMARK_PATH))

    state_file = STAGING_DIR / "phase10_staging_state.json"
    if state_file.is_file():
        state_file.unlink()

    pipeline = SourceIngestionPipeline(
        tokenizer=tokenizer,
        benchmark=benchmark,
        state_file=state_file,
    )

    accepted_docs: List[NormalizedDocument] = []
    rejected_sources: List[Dict[str, Any]] = []
    quarantined_sources: List[Dict[str, Any]] = []

    for src in sources:
        fpath = Path(src["file_path"])
        print(f"\nProcessing: [{src['source_id']}] {src['title'][:60]}...")
        docs = pipeline.ingest_file(
            file_path=fpath,
            source_metadata=src,
        )
        if docs:
            for d in docs:
                accepted_docs.append(d)
                print(f"  -> ACCEPTED: {d.doc_id} | Words: {d.word_count:,} | Tokens: {d.token_count:,} | Pillar: {d.pillar}")
        else:
            # Check whether rejected or quarantined
            quar_matches = [q for q in pipeline.quarantined_docs.values() if q.source_id == src["source_id"]]
            if quar_matches:
                q_doc = quar_matches[0]
                if q_doc.ingestion_status == IngestionStatus.REJECTED:
                    rejected_sources.append({"source_id": src["source_id"], "reason": q_doc.review_notes})
                    print(f"  -> REJECTED at licensing gate: {q_doc.review_notes}")
                else:
                    quarantined_sources.append({"source_id": src["source_id"], "reason": q_doc.review_notes})
                    print(f"  -> QUARANTINED: {q_doc.review_notes}")

    # Save manifest
    manifest_path = STAGING_DIR / "phase10_staging_manifest.json"
    manifest = pipeline.generate_manifest()
    manifest.save(manifest_path)

    # 3. Perform source-level train/val partition
    train_docs, val_docs = source_level_split(accepted_docs, val_ratio=0.20, seed=42)

    train_sources = sorted(list({d.source_id for d in train_docs}))
    val_sources = sorted(list({d.source_id for d in val_docs}))
    is_disjoint = set(train_sources).isdisjoint(set(val_sources))

    train_tokens = sum(d.token_count for d in train_docs)
    val_tokens = sum(d.token_count for d in val_docs)
    combined_tokens = train_tokens + val_tokens

    # Export staging splits
    train_path = STAGING_DIR / "train_staging.json"
    val_path = STAGING_DIR / "val_staging.json"
    with open(train_path, "w", encoding="utf-8") as f:
        json.dump([d.to_dict() for d in train_docs], f, indent=2)
    with open(val_path, "w", encoding="utf-8") as f:
        json.dump([d.to_dict() for d in val_docs], f, indent=2)

    # 4. Compile detailed audit findings
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sources_attempted": len(sources),
        "sources_accepted": len({d.source_id for d in accepted_docs}),
        "sources_rejected": len(rejected_sources),
        "sources_quarantined": len(quarantined_sources),
        "accepted_documents_count": len(accepted_docs),
        "train_documents_count": len(train_docs),
        "val_documents_count": len(val_docs),
        "train_tokens": train_tokens,
        "val_tokens": val_tokens,
        "combined_usable_tokens": combined_tokens,
        "train_source_ids": train_sources,
        "val_source_ids": val_sources,
        "source_split_is_disjoint": is_disjoint,
        "benchmark_contamination_count": sum(1 for d in accepted_docs if d.benchmark_contamination),
        "exact_duplicates_count": manifest.deduplication_summary.get("exact_duplicates_dropped", 0),
        "near_duplicate_clusters_count": manifest.deduplication_summary.get("clusters_formed", 0),
        "pillar_distribution": manifest.pillar_coverage,
        "rejected_details": rejected_sources,
        "quarantined_details": quarantined_sources,
    }

    report_path = STAGING_DIR / "phase10_audit_summary.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("\n" + "=" * 80)
    print("STAGING INGESTION RESULTS:")
    print("=" * 80)
    print(f"Sources Attempted:       {report['sources_attempted']}")
    print(f"Sources Accepted:        {report['sources_accepted']}")
    print(f"Sources Rejected:        {report['sources_rejected']}")
    print(f"Sources Quarantined:     {report['sources_quarantined']}")
    print(f"Original Documents:      {report['accepted_documents_count']}")
    print(f"Usable Staging Tokens:   {report['combined_usable_tokens']:,}")
    print(f"  - Training Tokens:     {report['train_tokens']:,} (Sources: {', '.join(train_sources)})")
    print(f"  - Validation Tokens:   {report['val_tokens']:,} (Sources: {', '.join(val_sources)})")
    print(f"Train/Val Source Overlap:{'NONE (STRICTLY DISJOINT)' if is_disjoint else 'FAIL: CONTAMINATED'}")
    print(f"Benchmark Contamination: {report['benchmark_contamination_count']}")
    print(f"Manifest Generated:      {manifest_path}")

    return report


if __name__ == "__main__":
    run_staging_pipeline()
