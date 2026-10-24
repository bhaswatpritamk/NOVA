#!/usr/bin/env python3
"""
scripts/dump_removed_lines.py
Phase 11.5: Dry-run cleaning rules on PAGAC re-sliced docs and dump first/last 5 removed lines.
Read-only script. Writes nothing into any staging directory.
"""

from pathlib import Path
import pypdf
import re

pagac_specs = [
    {
        "source_id": "US-HHS-PAGAC-2018-EXEC",
        "chapter_title": "Part A. Executive Summary",
        "pdf_page_range": [19, 25],
    },
    {
        "source_id": "US-HHS-PAGAC-2018-HIIT",
        "chapter_title": "Part F. Chapter 1. Physical Activity Behaviors: Steps, Bouts, and High-Intensity Interval Training",
        "pdf_page_range": [119, 144],
    },
    {
        "source_id": "US-HHS-PAGAC-2018-BRAIN-SLEEP",
        "chapter_title": "Part F. Chapter 3. Brain Health",
        "pdf_page_range": [188, 248],
    },
    {
        "source_id": "US-HHS-PAGAC-2018-CARDIOMETABOLIC",
        "chapter_title": "Part F. Chapter 5. Cardiometabolic Health and Prevention of Weight Gain",
        "pdf_page_range": [316, 351],
    },
    {
        "source_id": "US-HHS-PAGAC-2018-OLDER-ADULTS",
        "chapter_title": "Part F. Chapter 9. Older Adults",
        "pdf_page_range": [439, 489],
    },
]

def run_dry_run():
    pdf_path = Path("data/staging_phase11/sources_raw/us_hhs_pagac_report_2018.pdf")
    reader = pypdf.PdfReader(str(pdf_path))

    for spec in pagac_specs:
        sid = spec["source_id"]
        title = spec["chapter_title"]
        start_page, end_page = spec["pdf_page_range"]

        print("=" * 80)
        print(f"DOCUMENT: {sid}")
        print(f"Title:    {title}")
        print(f"Pages:    PDF pages {start_page} to {end_page} (count: {end_page - start_page + 1})")
        print("=" * 80)

        # 1. Page-by-page header/footer/page-label removal
        raw_items = []
        rule_headers = []
        raw_line_counter = 0

        for p in range(start_page, end_page + 1):
            txt = reader.pages[p - 1].extract_text() or ""
            page_lines = txt.splitlines()
            n = len(page_lines)
            p_items_kept = []
            i = 0

            while i < min(n, 6):
                line = page_lines[i]
                raw_line_counter += 1
                curr_item = (raw_line_counter, p, i + 1, line)
                s = line.strip()

                if re.match(r"^Part\s+[A-Z]\.?\s*(Chapter|\b)", s, re.I):
                    rule_headers.append(curr_item)
                    i += 1
                    continue
                if "2018 Physical Activity Guidelines Advisory Committee" in s:
                    rule_headers.append(curr_item)
                    i += 1
                    continue
                if re.match(r"^[A-Z]\d*-\d+$", s):
                    rule_headers.append(curr_item)
                    i += 1
                    continue
                if p == start_page and re.match(r"^PART\s+[A-Z]\.?\s*CHAPTER", s, re.I):
                    rule_headers.append(curr_item)
                    i += 1
                    continue
                if p == start_page and re.match(r"^PART\s+A\.?\s*EXECUTIVE\s+SUMMARY", s, re.I):
                    rule_headers.append(curr_item)
                    i += 1
                    continue
                if p == start_page and s in [
                    "STEPS, BOUTS, AND HIGH INTENSITY TRAINING",
                    "AND PREVENTION OF WEIGHT GAIN",
                ]:
                    rule_headers.append(curr_item)
                    i += 1
                    continue
                break

            while i < n:
                line = page_lines[i]
                raw_line_counter += 1
                curr_item = (raw_line_counter, p, i + 1, line)
                s = line.strip()
                if re.match(r"^[A-Z]\d*-\d+$", s):
                    rule_headers.append(curr_item)
                else:
                    p_items_kept.append(curr_item)
                i += 1

            raw_items.extend(p_items_kept)

        # 2. Table of Contents removal
        items_after_toc = []
        rule_toc = []
        in_toc = False

        for item in raw_items:
            line = item[3]
            s = line.strip()
            if not in_toc:
                if s.lower() == "table of contents":
                    in_toc = True
                    rule_toc.append(item)
                    continue
                else:
                    items_after_toc.append(item)
            else:
                if re.match(r"^\.{3,}|\.\s*\.\s*\.\s*\.", s) or re.search(r"\.{3,}\s*[A-Z0-9\-]+", s):
                    rule_toc.append(item)
                    continue
                elif s.upper() in ["INTRODUCTION", "INTRODUCTION "] or (s.startswith("Introduction") and not re.search(r"\.{3,}", s)):
                    in_toc = False
                    items_after_toc.append(item)
                elif in_toc and len(rule_toc) < 40 and (
                    re.search(r"[A-Z]\d*-\d+$", s)
                    or s.startswith("Question")
                    or s.startswith("Review")
                    or s.startswith("Overview")
                    or s.startswith("Data Sources")
                    or s.startswith("Major Findings")
                    or s.startswith("Public Health")
                    or s.startswith("The Future")
                    or s in ["Pu", "blic Health Impact"]
                ):
                    rule_toc.append(item)
                    continue
                else:
                    in_toc = False
                    items_after_toc.append(item)

        # 3. Trailing references list removal
        rule_refs = []
        cleaned_items = []
        ref_idx = -1
        for idx, item in enumerate(items_after_toc):
            line = item[3]
            s = line.strip()
            if re.match(r"^REFERENCES\s*$", s, re.I):
                if idx > len(items_after_toc) * 0.5:
                    ref_idx = idx
                    break

        if ref_idx != -1:
            cleaned_items = items_after_toc[:ref_idx]
            rule_refs = items_after_toc[ref_idx:]
        else:
            cleaned_items = items_after_toc

        # Helper to print items
        def print_rule_items(rule_name: str, items: list):
            count = len(items)
            print(f"\n--- RULE: {rule_name} (Total removed: {count} lines) ---")
            if count == 0:
                print("  [No lines removed]")
                return

            if count <= 10:
                for raw_lno, page_no, page_lno, line_str in items:
                    print(f"  Line {raw_lno:4d} (PDF p.{page_no}:{page_lno}): {line_str}")
            else:
                print("  First 5 removed lines:")
                for raw_lno, page_no, page_lno, line_str in items[:5]:
                    print(f"    Line {raw_lno:4d} (PDF p.{page_no}:{page_lno}): {line_str}")
                print(f"    ... [{count - 10} lines omitted] ...")
                print("  Last 5 removed lines:")
                for raw_lno, page_no, page_lno, line_str in items[-5:]:
                    print(f"    Line {raw_lno:4d} (PDF p.{page_no}:{page_lno}): {line_str}")

        print_rule_items("1. headers_footers", rule_headers)
        print_rule_items("2. table_of_contents", rule_toc)
        print_rule_items("3. references_list", rule_refs)
        print(f"\nSummary for {sid}: raw extracted={raw_line_counter}, removed={len(rule_headers)+len(rule_toc)+len(rule_refs)}, final cleaned={len(cleaned_items)}")
        print()

if __name__ == "__main__":
    run_dry_run()
