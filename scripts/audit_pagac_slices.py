#!/usr/bin/env python3
"""Project NOVA Phase 11.3: PAGAC Slice Audit.

Audits the 5 accepted PAGAC documents against the authentic 2018 PAGAC Scientific
Report PDF (us_hhs_pagac_report_2018.pdf) page-by-page.

For each page, extracts:
- Printed page label (e.g. A-5, E-13, F3-31)
- Running-header Part/Chapter line

Matches each document back to PDF pages by normalized line overlap and calculates:
- First page label
- Last page label
- Page count
- Share of characters from each Part/Chapter header
Outputs structured JSON to data/staging_phase11/audit_outputs/pagac_slice_audit.json.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import pypdf

REPO_ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = REPO_ROOT / "data" / "staging_phase11" / "sources_raw" / "us_hhs_pagac_report_2018.pdf"
RAW_DIR = REPO_ROOT / "data" / "staging_phase11" / "sources_raw"
OUTPUT_DIR = REPO_ROOT / "data" / "staging_phase11" / "audit_outputs"

ACCEPTED_PAGAC_DOCS = [
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

REPORT_LABEL_PATTERN = re.compile(
    r"2018\s+Physical\s+Activity\s+Guidelines\s+Advisory\s+Committee\s+Scientific\s+Report\s+([A-Za-z0-9\-]+)",
    re.IGNORECASE,
)


def extract_page_metadata(reader: pypdf.PdfReader) -> List[Dict[str, Any]]:
    """Extract printed page label, running-header Part/Chapter line, and normalized lines for each PDF page."""
    pages_meta = []
    for idx, page in enumerate(reader.pages):
        page_num = idx + 1
        text = page.extract_text() or ""
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        running_header = "NONE"
        page_label = "NONE"

        # Search top 6 lines for header and label
        for line in lines[:6]:
            # Page label from standard report footer/header
            label_match = REPORT_LABEL_PATTERN.search(line)
            if label_match and page_label == "NONE":
                page_label = label_match.group(1).strip()

            # Running header Part/Chapter
            if running_header == "NONE":
                if (
                    line.startswith("Part ")
                    or line.startswith("PART ")
                    or line.startswith("Membership Lists")
                    or line.startswith("Table of Contents")
                ):
                    running_header = line

        # If header not identified via prefix, fallback to first non-empty line
        if running_header == "NONE" and lines:
            running_header = lines[0]

        pages_meta.append(
            {
                "page_num": page_num,
                "running_header": running_header,
                "printed_page_label": page_label,
                "char_count": len(text),
                "line_count": len(lines),
                "normalized_lines": set(lines),
                "raw_text": text,
            }
        )
    return pages_meta


def audit_pagac_slices() -> Dict[str, Any]:
    """Execute page-by-page PDF matching and character share computation for all 5 accepted PAGAC docs."""
    if not PDF_PATH.exists():
        return {
            "error": "NOT_COMPUTED",
            "reason": f"PDF file not found at {PDF_PATH}",
            "documents": {},
        }

    reader = pypdf.PdfReader(str(PDF_PATH))
    pdf_pages = extract_page_metadata(reader)

    results: Dict[str, Any] = {}

    for doc in ACCEPTED_PAGAC_DOCS:
        source_id = doc["source_id"]
        file_name = doc["file_name"]
        doc_path = RAW_DIR / file_name

        if not doc_path.exists():
            results[source_id] = {
                "status": "NOT_COMPUTED",
                "reason": f"Source text file not found: {doc_path}",
            }
            continue

        raw_text = doc_path.read_text(encoding="utf-8", errors="ignore")
        doc_lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        doc_lines_set = set(doc_lines)

        # Match PDF pages by normalized line overlap (contiguous block where overlap_ratio >= 0.90)
        matching_indices = []
        for idx, p in enumerate(pdf_pages):
            p_lines = p["normalized_lines"]
            if not p_lines:
                continue
            overlap_count = len(doc_lines_set & p_lines)
            overlap_ratio = overlap_count / len(p_lines)
            if overlap_ratio >= 0.90:
                matching_indices.append(idx)

        # Find the largest contiguous run of matching pages
        runs = []
        current_run = []
        for idx in matching_indices:
            if not current_run or idx == current_run[-1] + 1:
                current_run.append(idx)
            else:
                runs.append(current_run)
                current_run = [idx]
        if current_run:
            runs.append(current_run)

        if not runs:
            results[source_id] = {
                "status": "NOT_COMPUTED",
                "reason": "Normalized line overlap failed to identify matching pages in PDF",
            }
            continue

        best_run = max(runs, key=len)
        matched_pages = []
        for idx in best_run:
            p = pdf_pages[idx]
            p_lines = p["normalized_lines"]
            overlap_count = len(doc_lines_set & p_lines)
            overlap_ratio = overlap_count / len(p_lines)
            matched_pages.append(
                {
                    "page_num": p["page_num"],
                    "printed_page_label": p["printed_page_label"],
                    "running_header": p["running_header"],
                    "char_count": p["char_count"],
                    "overlap_line_count": overlap_count,
                    "page_line_count": len(p_lines),
                    "overlap_ratio": round(overlap_ratio, 4),
                }
            )

        # Sort matched pages by page number
        matched_pages.sort(key=lambda x: x["page_num"])

        first_page = matched_pages[0]
        last_page = matched_pages[-1]
        page_count = len(matched_pages)

        # Total characters across matched pages
        total_matched_chars = sum(p["char_count"] for p in matched_pages)

        # Character counts and shares by running header
        header_chars: Dict[str, int] = {}
        header_pages: Dict[str, List[int]] = {}
        for p in matched_pages:
            hdr = p["running_header"]
            header_chars[hdr] = header_chars.get(hdr, 0) + p["char_count"]
            header_pages.setdefault(hdr, []).append(p["page_num"])

        header_shares_pct: Dict[str, float] = {}
        for hdr, count in header_chars.items():
            pct = (count / total_matched_chars * 100.0) if total_matched_chars else 0.0
            header_shares_pct[hdr] = round(pct, 2)

        results[source_id] = {
            "status": "COMPUTED",
            "source_id": source_id,
            "file_name": file_name,
            "title": doc["title"],
            "first_page_number": first_page["page_num"],
            "last_page_number": last_page["page_num"],
            "first_page_label": first_page["printed_page_label"],
            "last_page_label": last_page["printed_page_label"],
            "page_count": page_count,
            "total_matched_characters": total_matched_chars,
            "doc_character_count": len(raw_text),
            "doc_line_count": len(raw_text.splitlines()),
            "header_shares_pct": header_shares_pct,
            "header_char_counts": header_chars,
            "header_pages": header_pages,
            "matched_pages": matched_pages,
        }

    output_data = {
        "timestamp_utc": "2026-10-20T12:00:00Z",
        "pdf_source": str(PDF_PATH.relative_to(REPO_ROOT)),
        "pdf_total_pages": len(pdf_pages),
        "accepted_pagac_docs_count": len(ACCEPTED_PAGAC_DOCS),
        "results": results,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / "pagac_slice_audit.json"
    out_file.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
    print(f"PAGAC slice audit written to {out_file}")
    return output_data


if __name__ == "__main__":
    audit_pagac_slices()
