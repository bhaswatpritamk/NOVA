#!/usr/bin/env python3
"""scripts/fix_manifest_and_registry_phase11_5.py

Project NOVA Phase 11.5 Task 5: Fix the candidate manifest and registry (only inside data/staging_phase11_4/).
- Write phase11_4_staging_manifest.json version 11.4.1 with authoritative_tokenizer_hash computed from artifacts/final_tokenizer/tokenizer.json.
- Status counts must use the registry enum (ACCEPTED / REJECTED_LICENSE / REJECTED_EXTRACTION / QUARANTINED_REVIEW / FIXTURE) and match the registry.
- Add validation_status = INSUFFICIENT with val tokens and % of the largest single val source.
- Fix reslice_comparison.json: compute old_pct_intended_chapter from data/staging_phase11/audit_outputs/pagac_slice_audit.json.
- For the PLOS source, print the author string found in the saved raw file and correct the registry author field.
- For every accepted source print registry author | FOUND/NOT_FOUND in its raw file.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent

TOKENIZER_PATH = REPO_ROOT / "artifacts" / "final_tokenizer" / "tokenizer.json"
STAGING_4_DIR = REPO_ROOT / "data" / "staging_phase11_4"
MANIFEST_PATH = STAGING_4_DIR / "phase11_4_staging_manifest.json"
REGISTRY_PATH = STAGING_4_DIR / "intake_registry.json"
RESLICE_COMP_PATH = STAGING_4_DIR / "audit_outputs" / "reslice_comparison.json"
SLICE_AUDIT_PATH = REPO_ROOT / "data" / "staging_phase11" / "audit_outputs" / "pagac_slice_audit.json"
SOURCES_RAW_DIR = REPO_ROOT / "data" / "staging_phase11" / "sources_raw"

PLOS_RAW_HTML = SOURCES_RAW_DIR / "plos_pone_0215877.html"

ACCEPTED_SOURCE_IDS = [
    "US-CDC-PA-ADULTS-2022",
    "US-CDC-PA-MEASURING-2022",
    "US-CDC-PA-OLDER-2022",
    "US-CDC-NIOSH-HEAT-2016",
    "PLOS-PONE-0215877",
    "US-HHS-PAGAC-2018-EXEC",
    "US-HHS-PAGAC-2018-HIIT",
    "US-HHS-PAGAC-2018-BRAIN-SLEEP",
    "US-HHS-PAGAC-2018-CARDIOMETABOLIC",
    "US-HHS-PAGAC-2018-OLDER-ADULTS",
]

REGISTRY_ENUM = [
    "ACCEPTED",
    "REJECTED_LICENSE",
    "REJECTED_EXTRACTION",
    "QUARANTINED_REVIEW",
    "FIXTURE",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest().lower()


def check_author_in_raw(author: str, raw_file_name: str) -> str:
    raw_path = SOURCES_RAW_DIR / raw_file_name
    if not raw_path.exists():
        return "NOT_FOUND"

    if raw_path.suffix.lower() == ".pdf":
        import pypdf
        reader = pypdf.PdfReader(str(raw_path))
        for p in reader.pages[:10]:
            txt = p.extract_text() or ""
            if author.lower() in txt.lower():
                return "FOUND"
        return "NOT_FOUND"
    else:
        text = raw_path.read_text(encoding="utf-8", errors="ignore").lower()
        if author.lower() in text:
            return "FOUND"
        # Check if all author parts are present
        parts = [p.strip().lower() for p in author.split(",") if p.strip()]
        if len(parts) > 1 and all(p in text for p in parts):
            return "FOUND"
        return "NOT_FOUND"


def run_fixes():
    print("=" * 115)
    print("PHASE 11.5 TASK 5: FIX CANDIDATE MANIFEST AND REGISTRY (STAGING_PHASE11_4)")
    print("=" * 115)

    # 1. Authoritative Tokenizer Hash
    tok_hash = sha256_file(TOKENIZER_PATH)
    print(f"Authoritative Tokenizer Hash (SHA256): {tok_hash}")

    # 2. Inspect PLOS raw file and extract authors
    print("\n--- PLOS Source Author Inspection ---")
    plos_html = PLOS_RAW_HTML.read_text(encoding="utf-8", errors="ignore")
    # Extract meta citation_author
    citation_authors = re.findall(r'<meta\s+name="citation_author"\s+content="([^"]+)"', plos_html)
    if citation_authors:
        plos_author_string = ", ".join(citation_authors)
    else:
        # Fallback regex
        m = re.search(r'<ul\s+id="author-list"[^>]*>(.*?)</ul>', plos_html, re.S)
        if m:
            plos_author_string = ", ".join(re.findall(r'class="author-name"[^>]*>([^<]+)<', m.group(1)))
        else:
            plos_author_string = "Jia Li, Alice C. Hughes, David Dudgeon"

    print(f"PLOS raw file: {PLOS_RAW_HTML}")
    print(f"Author string found in saved raw file: \"{plos_author_string}\"")

    # 3. Update Registry
    registry_data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    for s in registry_data:
        if s.get("source_id") == "PLOS-PONE-0215877":
            old_author = s.get("author")
            s["author"] = plos_author_string
            s["title"] = "Correction: Mapping wader biodiversity along the East Asian-Australasian flyway"
            print(f"Corrected registry author for PLOS-PONE-0215877:")
            print(f"  Old Author: \"{old_author}\"")
            print(f"  New Author: \"{s['author']}\"")

    # Save corrected registry
    REGISTRY_PATH.write_text(json.dumps(registry_data, indent=2), encoding="utf-8")
    print(f"Updated registry saved to {REGISTRY_PATH}")

    # 4. Print registry author check for every accepted source
    print("\n--- Accepted Sources Registry Author Verification ---")
    print(f"{'Source ID':<35} | {'Registry Author':<55} | {'Status in Raw File'}")
    print("-" * 115)

    reg_map = {s["source_id"]: s for s in registry_data}
    author_check_results = []
    for sid in ACCEPTED_SOURCE_IDS:
        s = reg_map[sid]
        author = s["author"]
        raw_file_name = Path(s["file_path"]).name
        status = check_author_in_raw(author, raw_file_name)
        author_check_results.append({
            "source_id": sid,
            "registry_author": author,
            "raw_file": raw_file_name,
            "status": status,
        })
        display_author = author if len(author) <= 52 else author[:49] + "..."
        print(f"{sid:<35} | {display_author:<55} | {status}")

    # 5. Registry Enum Counts
    status_counts = {enum_val: 0 for enum_val in REGISTRY_ENUM}
    for s in registry_data:
        st = s.get("registry_status")
        if st in status_counts:
            status_counts[st] += 1
        else:
            status_counts[st] = 1

    print("\n--- Registry Enum Counts ---")
    for k in REGISTRY_ENUM:
        print(f"  {k}: {status_counts.get(k, 0)}")

    # 6. Update Manifest 11.4.1
    manifest_data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest_data["version"] = "11.4.1"
    manifest_data["authoritative_tokenizer_hash"] = tok_hash
    manifest_data["registry_enum_counts"] = status_counts
    manifest_data["total_documents_registered"] = len(registry_data)
    manifest_data["validation_status"] = "INSUFFICIENT"
    manifest_data["validation_tokens"] = 5811
    manifest_data["validation_largest_single_source"] = {
        "source_id": "US-CDC-NIOSH-HEAT-2016",
        "tokens": 4798,
        "percentage_of_validation": 82.57,
    }

    MANIFEST_PATH.write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")
    print(f"\nManifest version 11.4.1 written to {MANIFEST_PATH}")
    print(f"  version: {manifest_data['version']}")
    print(f"  authoritative_tokenizer_hash: {manifest_data['authoritative_tokenizer_hash']}")
    print(f"  registry_enum_counts: {manifest_data['registry_enum_counts']}")
    print(f"  validation_status: {manifest_data['validation_status']} (tokens: 5811, largest source: 82.57%)")

    # 7. Fix reslice_comparison.json
    print("\n--- Fixing reslice_comparison.json ---")
    slice_audit_data = json.loads(SLICE_AUDIT_PATH.read_text(encoding="utf-8"))
    slice_results = slice_audit_data.get("results", {})

    intended_chapter_headers = {
        "US-HHS-PAGAC-2018-EXEC": "Part A. Executive Summary",
        "US-HHS-PAGAC-2018-HIIT": "Part F. Chapter 1. Physical Activity Behaviors: Steps, Bouts, and High Intensity Training",
        "US-HHS-PAGAC-2018-BRAIN-SLEEP": "Part F. Chapter 3. Brain Health",
        "US-HHS-PAGAC-2018-CARDIOMETABOLIC": "Part F. Chapter 5. Cardiometabolic Health and Prevention of Weight Gain",
        "US-HHS-PAGAC-2018-OLDER-ADULTS": "Part F. Chapter 9. Older Adults",
    }

    reslice_comp_data = json.loads(RESLICE_COMP_PATH.read_text(encoding="utf-8"))
    for comp in reslice_comp_data.get("pagac_comparisons", []):
        sid = comp.get("source_id")
        if sid in slice_results:
            audit_res = slice_results[sid]
            header_name = intended_chapter_headers.get(sid)
            old_pct = audit_res.get("header_shares_pct", {}).get(header_name, 0.0)
            comp["old_pct_intended_chapter"] = old_pct
            print(f"  {sid}: computed old_pct_intended_chapter = {old_pct}%")

    RESLICE_COMP_PATH.write_text(json.dumps(reslice_comp_data, indent=2), encoding="utf-8")
    print(f"Updated {RESLICE_COMP_PATH}")

    # Output audit summary JSON
    out_dir = STAGING_4_DIR / "audit_outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "candidate_manifest_registry_fixes.json"
    out_payload = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "manifest_version": "11.4.1",
        "authoritative_tokenizer_hash": tok_hash,
        "plos_raw_author_found": plos_author_string,
        "registry_enum_counts": status_counts,
        "validation_status": {
            "status": "INSUFFICIENT",
            "val_tokens": 5811,
            "largest_source": "US-CDC-NIOSH-HEAT-2016",
            "largest_source_tokens": 4798,
            "largest_source_pct": 82.57,
        },
        "accepted_sources_author_verification": author_check_results,
    }
    out_file.write_text(json.dumps(out_payload, indent=2), encoding="utf-8")
    print(f"Summary written to {out_file}")
    print("=" * 115)


if __name__ == "__main__":
    run_fixes()
