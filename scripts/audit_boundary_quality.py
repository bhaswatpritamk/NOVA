#!/usr/bin/env python3
"""Project NOVA Phase 11.3: Boundary and Extraction-Quality Evidence Audit.

Audits all 10 accepted documents in data/staging_phase11/sources_raw/:
For each doc extracts:
- First 5 lines
- Last 15 lines
- Character counts and % of total characters for:
  1. reference-list lines (numbered citations containing doi or year;volume)
  2. table-of-contents lines (dot leaders)
  3. running-header lines
  4. "Source: Adapted" lines
  5. page-number artifacts

Outputs structured JSON to data/staging_phase11/audit_outputs/boundary_extraction_quality.json.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "data" / "staging_phase11" / "sources_raw"
OUTPUT_DIR = REPO_ROOT / "data" / "staging_phase11" / "audit_outputs"

ACCEPTED_DOCS = [
    {
        "source_id": "US-CDC-PA-ADULTS-2022",
        "file_name": "us_cdc_pa_adults_2022.md",
        "title": "CDC Physical Activity Guidelines for Adults: Overview and Aerobic/Strength Recommendations",
    },
    {
        "source_id": "US-CDC-PA-MEASURING-2022",
        "file_name": "us_cdc_pa_measuring_2022.md",
        "title": "Measuring Physical Activity Intensity: Target Heart Rate and 0-to-10 Effort Rating",
    },
    {
        "source_id": "US-CDC-PA-OLDER-2022",
        "file_name": "us_cdc_pa_older_2022.md",
        "title": "Physical Activity Guidelines for Older Adults: Multicomponent Functional Training and Fall Prevention",
    },
    {
        "source_id": "US-CDC-NIOSH-HEAT-2016",
        "file_name": "us_cdc_niosh_heat_2016.md",
        "title": "NIOSH Workplace Recommendations for Heat Stress: Acclimatization, Hydration, and Rest Cycles",
    },
    {
        "source_id": "PLOS-PONE-0215877",
        "file_name": "plos_pone_0215877.html",
        "title": "Effects of resistance training frequency on measures of muscle hypertrophy: a systematic review and meta-analysis",
    },
    {
        "source_id": "US-HHS-PAGAC-2018-EXEC",
        "file_name": "pagac_2018_part_a_executive_summary.txt",
        "title": "2018 PAGAC Scientific Report: Part A. Executive Summary",
    },
    {
        "source_id": "US-HHS-PAGAC-2018-HIIT",
        "file_name": "pagac_2018_part_f_ch1_bouts_hiit.txt",
        "title": "2018 PAGAC Scientific Report: Part F. Chapter 1: Physical Activity and Habitual Physical Activity / High-Intensity Interval Training",
    },
    {
        "source_id": "US-HHS-PAGAC-2018-BRAIN-SLEEP",
        "file_name": "pagac_2018_part_f_ch3_brain_sleep.txt",
        "title": "2018 PAGAC Scientific Report: Part F. Chapter 3: Brain Health and Sleep",
    },
    {
        "source_id": "US-HHS-PAGAC-2018-CARDIOMETABOLIC",
        "file_name": "pagac_2018_part_f_ch5_cardiometabolic.txt",
        "title": "2018 PAGAC Scientific Report: Part F. Chapter 5: Cardiometabolic Health and Weight Management",
    },
    {
        "source_id": "US-HHS-PAGAC-2018-OLDER-ADULTS",
        "file_name": "pagac_2018_part_f_ch9_older_adults.txt",
        "title": "2018 PAGAC Scientific Report: Part F. Chapter 9: Physical Activity and Older Adults: Fall Prevention and Sarcopenia",
    },
]

# Detection regular expressions
REF_LIST_PATTERN = re.compile(
    r"^\s*(\d+[\.\)]|\[\d+\]).*?(doi|(?:\b(?:19|20)\d{2}\s*;\s*\d+))",
    re.IGNORECASE,
)
TOC_PATTERN = re.compile(r"(\.{3,}|\.\s\.\s\.)")
RUNNING_HEADER_PATTERN = re.compile(
    r"^\s*(Part\s+[A-Z]|PART\s+[A-Z]|2018\s+Physical\s+Activity\s+Guidelines\s+Advisory\s+Committee\s+Scientific\s+Report|Membership\s+Lists|Table\s+of\s+Contents)",
    re.IGNORECASE,
)
SOURCE_ADAPTED_PATTERN = re.compile(
    r"(source:\s*adapted|adapted\s+from)",
    re.IGNORECASE,
)
PAGE_NUMBER_PATTERN = re.compile(
    r"2018\s+Physical\s+Activity\s+Guidelines\s+Advisory\s+Committee\s+Scientific\s+Report\s+([A-Za-z0-9\-]+)|^\s*(?:page\s*)?([A-Za-z0-9\-]+|\d+)\s*$",
    re.IGNORECASE,
)


def audit_document(doc_info: Dict[str, str]) -> Dict[str, Any]:
    """Audit single document for boundary lines and extraction-quality artifacts."""
    source_id = doc_info["source_id"]
    file_name = doc_info["file_name"]
    doc_path = RAW_DIR / file_name

    if not doc_path.exists():
        return {
            "source_id": source_id,
            "status": "NOT_COMPUTED",
            "reason": f"File does not exist: {doc_path}",
        }

    raw_text = doc_path.read_text(encoding="utf-8", errors="ignore")
    lines = raw_text.splitlines()
    total_chars = sum(len(line) for line in lines)
    total_lines = len(lines)

    # First 5 lines
    first_5 = [
        {"line_number": idx + 1, "content": lines[idx]}
        for idx in range(min(5, total_lines))
    ]

    # Last 15 lines
    last_15_start = max(0, total_lines - 15)
    last_15 = [
        {"line_number": idx + 1, "content": lines[idx]}
        for idx in range(last_15_start, total_lines)
    ]

    # Categorize artifact lines
    categories: Dict[str, Dict[str, Any]] = {
        "reference_list_lines": {"pattern": REF_LIST_PATTERN, "matches": []},
        "table_of_contents_lines": {"pattern": TOC_PATTERN, "matches": []},
        "running_header_lines": {"pattern": RUNNING_HEADER_PATTERN, "matches": []},
        "source_adapted_lines": {"pattern": SOURCE_ADAPTED_PATTERN, "matches": []},
        "page_number_artifacts": {"pattern": PAGE_NUMBER_PATTERN, "matches": []},
    }

    for idx, line in enumerate(lines):
        line_num = idx + 1
        line_len = len(line)

        for cat_key, cat_data in categories.items():
            pat = cat_data["pattern"]
            if cat_key == "page_number_artifacts":
                # For standalone page numbers, ensure line is short
                m = pat.search(line)
                if m:
                    # If report header line, it matches
                    if "Physical Activity Guidelines Advisory Committee" in line:
                        cat_data["matches"].append({"line_number": line_num, "content": line, "char_count": line_len})
                    elif len(line.strip()) <= 12 and re.match(r"^\s*(?:page\s*)?([A-Za-z0-9\-]+|\d+)\s*$", line, re.I):
                        cat_data["matches"].append({"line_number": line_num, "content": line, "char_count": line_len})
            else:
                if pat.search(line):
                    cat_data["matches"].append({"line_number": line_num, "content": line, "char_count": line_len})

    # Summary metrics per category
    category_summaries: Dict[str, Any] = {}
    for cat_key, cat_data in categories.items():
        matches = cat_data["matches"]
        chars = sum(m["char_count"] for m in matches)
        pct = (chars / total_chars * 100.0) if total_chars else 0.0
        sample_matches = [
            {"line_number": m["line_number"], "content": m["content"][:120]}
            for m in matches[:5]
        ]
        category_summaries[cat_key] = {
            "line_count": len(matches),
            "char_count": chars,
            "char_percentage": round(pct, 2),
            "sample_lines": sample_matches,
        }

    return {
        "source_id": source_id,
        "file_name": file_name,
        "title": doc_info["title"],
        "status": "COMPUTED",
        "total_lines": total_lines,
        "total_characters": total_chars,
        "first_5_lines": first_5,
        "last_15_lines": last_15,
        "artifact_categories": category_summaries,
    }


def audit_all_boundaries() -> Dict[str, Any]:
    """Audit all 10 accepted documents and save output JSON."""
    results: Dict[str, Any] = {}
    for doc in ACCEPTED_DOCS:
        sid = doc["source_id"]
        results[sid] = audit_document(doc)

    output_data = {
        "timestamp_utc": "2026-10-20T12:00:00Z",
        "documents_audited_count": len(ACCEPTED_DOCS),
        "results": results,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / "boundary_extraction_quality.json"
    out_file.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
    print(f"Boundary and extraction quality audit written to {out_file}")
    return output_data


if __name__ == "__main__":
    audit_all_boundaries()
