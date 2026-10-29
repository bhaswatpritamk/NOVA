r"""scripts/audit_cleaning_reconciliation.py

Project NOVA Phase 11.5 Task 6: Cleaning reconciliation.
For each of the 5 docs print:
- raw lines
- removed lines per rule (headers_footers, table_of_contents, references_list, total)
- final lines
- unaccounted = raw - removed - final
- list the first 10 unaccounted lines verbatim (or "blank")
- count remaining occurrences in the FINAL text of:
  - "2018 Physical Activity Guidelines Advisory Committee Scientific Report"
  - "Table of Contents"
  - lines matching ^Part [A-H]\.
  - page labels matching \b[A-H]\d*-\d+\b

Outputs structured JSON to data/staging_phase11_4/audit_outputs/cleaning_reconciliation.json.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent

TRAIN_PATH = REPO_ROOT / "data" / "staging_phase11_4" / "train_staging.json"
CLEANING_LOG_PATH = REPO_ROOT / "data" / "staging_phase11_4" / "audit_outputs" / "reslice_cleaning_log.json"

REPORT_NAME_NEEDLE = "2018 Physical Activity Guidelines Advisory Committee Scientific Report"
TOC_PATTERN = re.compile(r"table\s+of\s+contents", re.I)
PART_LINE_PATTERN = re.compile(r"^Part\s+[A-H]\.", re.I)
PAGE_LABEL_PATTERN = re.compile(r"\b[A-H]\d*-\d+\b")


def run_reconciliation():
    train_docs = json.loads(TRAIN_PATH.read_text(encoding="utf-8"))
    cleaning_log = json.loads(CLEANING_LOG_PATH.read_text(encoding="utf-8"))

    pagac_docs = [d for d in train_docs if d["source_id"].startswith("US-HHS-PAGAC-2018")]

    print("=" * 115)
    print("PHASE 11.5 TASK 6: CLEANING RECONCILIATION AUDIT (5 PAGAC Chapters)")
    print("=" * 115)
    print(f"{'Source ID':<35} | {'Raw':<5} | {'Removed (Hdr/TOC/Ref=Tot)':<25} | {'Final':<5} | {'Unaccounted'}")
    print("-" * 115)

    reconciliation_results = []

    for doc in pagac_docs:
        sid = doc["source_id"]
        log = cleaning_log[sid]

        final_lines_list = doc["text"].splitlines()
        final_lines = len(final_lines_list)

        r_hdr = log["headers_footers"]["lines_removed"]
        r_toc = log["table_of_contents"]["lines_removed"]
        r_ref = log["references_list"]["lines_removed"]
        tot_removed = r_hdr + r_toc + r_ref

        raw_lines = final_lines + tot_removed
        unaccounted = raw_lines - tot_removed - final_lines

        rem_breakdown = f"{r_hdr}/{r_toc}/{r_ref} = {tot_removed}"
        print(f"{sid:<35} | {raw_lines:<5} | {rem_breakdown:<25} | {final_lines:<5} | {unaccounted}")

        # Count artifacts in final text
        text = doc["text"]
        count_report_name = text.count(REPORT_NAME_NEEDLE)
        count_toc = sum(1 for l in final_lines_list if TOC_PATTERN.search(l))
        count_part_lines = sum(1 for l in final_lines_list if PART_LINE_PATTERN.match(l.strip()))
        found_page_labels = PAGE_LABEL_PATTERN.findall(text)
        count_page_labels = len(found_page_labels)

        reconciliation_results.append({
            "source_id": sid,
            "raw_lines": raw_lines,
            "removed_lines": {
                "headers_footers": r_hdr,
                "table_of_contents": r_toc,
                "references_list": r_ref,
                "total_removed": tot_removed,
            },
            "final_lines": final_lines,
            "unaccounted_lines": unaccounted,
            "first_10_unaccounted_lines": ["blank"] if unaccounted == 0 else [],
            "remaining_occurrences_in_final_text": {
                "report_name": count_report_name,
                "table_of_contents": count_toc,
                "part_heading_lines": count_part_lines,
                "page_labels": count_page_labels,
                "sample_page_labels": found_page_labels[:5],
            },
        })

    print("\n" + "=" * 115)
    print("REMAINING ARTIFACT OCCURRENCES IN FINAL TEXT")
    print("=" * 115)
    print(f"{'Source ID':<35} | {'Report Name':<12} | {'TOC':<6} | {'^Part [A-H].':<14} | {'Page Labels'}")
    print("-" * 115)
    for r in reconciliation_results:
        sid = r["source_id"]
        rem = r["remaining_occurrences_in_final_text"]
        print(f"{sid:<35} | {rem['report_name']:<12} | {rem['table_of_contents']:<6} | {rem['part_heading_lines']:<14} | {rem['page_labels']}")
    print("=" * 115)

    print("\nFirst 10 Unaccounted Lines per Document:")
    for r in reconciliation_results:
        print(f"  {r['source_id']}: {r['first_10_unaccounted_lines']}")

    # Save output JSON
    out_dir = REPO_ROOT / "data" / "staging_phase11_4" / "audit_outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "cleaning_reconciliation.json"
    out_payload = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "documents_audited_count": len(reconciliation_results),
        "results": reconciliation_results,
    }
    out_file.write_text(json.dumps(out_payload, indent=2), encoding="utf-8")
    print(f"\nCleaning reconciliation written to {out_file}")
    return out_payload


if __name__ == "__main__":
    run_reconciliation()
