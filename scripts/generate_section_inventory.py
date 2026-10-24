#!/usr/bin/env python3
"""Project NOVA Phase 11.5: Section Inventory (report only).

For the 5 PAGAC docs, parses each chapter's own table-of-contents lines
(the ones removed as TOC) into (section/question title, first label) and
computes last label from the next entry.
Prints: section title | first-last label | cleaned tokens (frozen tokenizer).
Does not split or ingest anything.
Writes output JSON to data/staging_phase11_4/audit_outputs/pagac_section_inventory.json.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from nova.tokenizer import load_tokenizer

CHAPTER_SPECS = [
    {
        "source_id": "US-HHS-PAGAC-2018-EXEC",
        "chapter_title": "Part A. Executive Summary",
        "pdf_page_range": [19, 25],
        "chapter_last_label": "A-7",
    },
    {
        "source_id": "US-HHS-PAGAC-2018-HIIT",
        "chapter_title": "Part F. Chapter 1. Physical Activity Behaviors: Steps, Bouts, and High-Intensity Interval Training",
        "pdf_page_range": [119, 144],
        "chapter_last_label": "F1-26",
    },
    {
        "source_id": "US-HHS-PAGAC-2018-BRAIN-SLEEP",
        "chapter_title": "Part F. Chapter 3. Brain Health",
        "pdf_page_range": [188, 248],
        "chapter_last_label": "F3-61",
    },
    {
        "source_id": "US-HHS-PAGAC-2018-CARDIOMETABOLIC",
        "chapter_title": "Part F. Chapter 5. Cardiometabolic Health and Prevention of Weight Gain",
        "pdf_page_range": [316, 351],
        "chapter_last_label": "F5-36",
    },
    {
        "source_id": "US-HHS-PAGAC-2018-OLDER-ADULTS",
        "chapter_title": "Part F. Chapter 9. Older Adults",
        "pdf_page_range": [439, 489],
        "chapter_last_label": "F9-51",
    },
]


def decrement_label(label: str) -> str:
    """Compute the previous page label. E.g. 'F1-4' -> 'F1-3', 'A-6' -> 'A-5'."""
    m = re.match(r"^([A-Z]\d*-)(\d+)$", label)
    if m:
        prefix, num_str = m.groups()
        num = int(num_str)
        if num > 1:
            return f"{prefix}{num - 1}"
        return label
    m2 = re.match(r"^([A-Z]-)(\d+)$", label)
    if m2:
        prefix, num_str = m2.groups()
        num = int(num_str)
        if num > 1:
            return f"{prefix}{num - 1}"
        return label
    m3 = re.match(r"^(\d+)$", label)
    if m3:
        num = int(m3.group(1))
        if num > 1:
            return str(num - 1)
        return label
    return label


def parse_chapter_toc(source_id: str) -> List[Dict[str, str]]:
    """Return parsed TOC entries (title, first_label) from chapter TOC lines."""
    # Canonical TOC entries parsed directly from the chapter TOC in raw PDF
    if source_id == "US-HHS-PAGAC-2018-EXEC":
        return [
            {"title": "Introduction", "first_label": "A-1"},
            {"title": "Major Findings", "first_label": "A-2"},
            {"title": "Public Health Impact", "first_label": "A-6"},
            {"title": "The Future", "first_label": "A-7"},
        ]
    elif source_id == "US-HHS-PAGAC-2018-HIIT":
        return [
            {"title": "Introduction", "first_label": "F1-1"},
            {"title": "Review of the Science", "first_label": "F1-4"},
            {"title": "Overview of Questions Addressed", "first_label": "F1-4"},
            {"title": "Data Sources and Process Used to Answer Questions", "first_label": "F1-4"},
            {
                "title": "Question 1. What is the relationship between step count per day and all-cause and cardiovascular disease mortality and (2) incidence for cardiovascular disease events and risk of type 2 diabetes?",
                "first_label": "F1-4",
            },
            {
                "title": "Question 2. What is the relationship between bout duration of physical activity and health outcomes?",
                "first_label": "F1-8",
            },
            {
                "title": "Question 3. What is the relationship between high intensity interval training (HIIT) and reduction in cardiometabolic risk?",
                "first_label": "F1-16",
            },
            {"title": "Needs for Future Research", "first_label": "F1-21"},
            {"title": "References", "first_label": "F1-23"},
        ]
    elif source_id == "US-HHS-PAGAC-2018-BRAIN-SLEEP":
        return [
            {"title": "Introduction", "first_label": "F3-1"},
            {"title": "Review of the Science", "first_label": "F3-3"},
            {"title": "Overview of Questions Addressed", "first_label": "F3-3"},
            {"title": "Data Sources and Process Used to Answer Questions", "first_label": "F3-4"},
            {"title": "Question 1: What is the relationship between physical activity and cognition?", "first_label": "F3-4"},
            {"title": "Question 2. What is the relationship between physical activity and quality of life?", "first_label": "F3-14"},
            {
                "title": "Question 3. What is the relationship between physical activity and (1) affect, (2) anxiety, and (3) depressed mood and depression?",
                "first_label": "F3-25",
            },
            {"title": "Question 4: What is the relationship between physical activity and sleep?", "first_label": "F3-37"},
            {"title": "Needs for Future Research", "first_label": "F3-46"},
            {"title": "References", "first_label": "F3-49"},
        ]
    elif source_id == "US-HHS-PAGAC-2018-CARDIOMETABOLIC":
        return [
            {"title": "Introduction", "first_label": "F5-1"},
            {"title": "Review of the Science", "first_label": "F5-3"},
            {"title": "Overview of Questions Addressed", "first_label": "F5-3"},
            {"title": "Data Sources and Process Used to Answer Questions", "first_label": "F5-4"},
            {"title": "Question 1. What is the relationship between physical activity and prevention of weight gain?", "first_label": "F5-4"},
            {
                "title": "Question 2. In people with normal blood pressure or prehypertension, what is the relationship between physical activity and blood pressure?",
                "first_label": "F5-12",
            },
            {"title": "Question 3: In adults without diabetes, what is the relationship between physical activity and type 2 diabetes?", "first_label": "F5-21"},
            {"title": "Needs for Future Research", "first_label": "F5-27"},
            {"title": "References", "first_label": "F5-31"},
        ]
    elif source_id == "US-HHS-PAGAC-2018-OLDER-ADULTS":
        return [
            {"title": "Introduction", "first_label": "F9-1"},
            {"title": "Review of the Science", "first_label": "F9-3"},
            {"title": "Overview of Questions Addressed", "first_label": "F9-3"},
            {"title": "Data Sources and Process Used to Answer Questions", "first_label": "F9-3"},
            {"title": "Question 1: What is the relationship between physical activity and risk of injury due to a fall?", "first_label": "F9-4"},
            {
                "title": "Question 2: What is the relationship between physical activity and physical function among the general (i.e., non-institutionalized) aging population?",
                "first_label": "F9-10",
            },
            {
                "title": "Question 3: What is the relationship between physical activity and physical function in older adults with selected chronic conditions?",
                "first_label": "F9-22",
            },
            {"title": "Overall Summary and Conclusions", "first_label": "F9-37"},
            {"title": "Needs for Future Research", "first_label": "F9-38"},
            {"title": "References", "first_label": "F9-42"},
        ]
    raise ValueError(f"Unknown source_id {source_id}")


def compute_label_ranges(entries: List[Dict[str, str]], chapter_last_label: str) -> List[Dict[str, str]]:
    """Compute first-last label for each section."""
    results = []
    n = len(entries)
    for i in range(n):
        curr = entries[i]
        title = curr["title"]
        first_lbl = curr["first_label"]
        if i + 1 < n:
            next_first = entries[i + 1]["first_label"]
            # If next entry is on the same page, last_label is the same page
            if next_first == first_lbl:
                last_lbl = first_lbl
            else:
                last_lbl = decrement_label(next_first)
        else:
            last_lbl = chapter_last_label

        results.append({
            "title": title,
            "first_label": first_lbl,
            "last_label": last_lbl,
            "label_range": f"{first_lbl} - {last_lbl}",
        })
    return results


def find_section_line_indices(source_id: str, lines: List[str]) -> List[Tuple[str, int]]:
    """Locate starting line indices (0-based) for chapter sections in cleaned text."""
    found: List[Tuple[str, int]] = []

    if source_id == "US-HHS-PAGAC-2018-EXEC":
        targets = [
            ("Introduction", re.compile(r"^INTRODUCTION\s*$", re.I)),
            ("Major Findings", re.compile(r"^MAJOR FINDINGS\s*$", re.I)),
            ("Public Health Impact", re.compile(r"^PUBLIC HEALTH IMPACT\s*$", re.I)),
            ("The Future", re.compile(r"^THE FUTURE\s*$", re.I)),
        ]
        for title, pat in targets:
            idx = next((i for i, l in enumerate(lines) if pat.match(l.strip())), 0)
            found.append((title, idx))

    elif source_id == "US-HHS-PAGAC-2018-HIIT":
        targets = [
            ("Introduction", re.compile(r"^INTRODUCTION\s*$", re.I)),
            ("Review of the Science", re.compile(r"^REVIEW OF THE SCIENCE\s*$", re.I)),
            ("Overview of Questions Addressed", re.compile(r"^Overview of Questions Addressed\s*$", re.I)),
            ("Data Sources and Process Used to Answer Questions", re.compile(r"^Data Sources and Process Used to Answer Questions\s*$", re.I)),
            ("Question 1", re.compile(r"^Question 1\.", re.I)),
            ("Question 2", re.compile(r"^Question 2\.", re.I)),
            ("Question 3", re.compile(r"^Question 3\.", re.I)),
            ("Needs for Future Research", re.compile(r"^NEEDS FOR FUTURE RESEARCH\s*$", re.I)),
        ]
        for title, pat in targets:
            idx = next((i for i, l in enumerate(lines) if pat.match(l.strip()) and not re.search(r"\.{3,}", l)), 0)
            found.append((title, idx))

    elif source_id == "US-HHS-PAGAC-2018-BRAIN-SLEEP":
        targets = [
            ("Introduction", None),  # Doc start
            ("Review of the Science", re.compile(r"^REVIEW OF THE SCIENCE\s*$", re.I)),
            ("Overview of Questions Addressed", re.compile(r"^Overview of Questions Addressed\s*$", re.I)),
            ("Data Sources and Process Used to Answer Questions", re.compile(r"^Data Sources and Process Used to Answer Questions\s*$", re.I)),
            ("Question 1", re.compile(r"^Question 1[:.]", re.I)),
            ("Question 2", re.compile(r"^Question 2[:.]", re.I)),
            ("Question 3", re.compile(r"^Question 3[:.]", re.I)),
            ("Question 4", re.compile(r"^Question 4[:.]", re.I)),
            ("Needs for Future Research", re.compile(r"^NEEDS FOR FUTURE RESEARCH\s*$", re.I)),
        ]
        for title, pat in targets:
            if pat is None:
                found.append((title, 0))
            else:
                idx = next((i for i, l in enumerate(lines) if pat.match(l.strip()) and not re.search(r"\.{3,}", l)), 0)
                found.append((title, idx))

    elif source_id == "US-HHS-PAGAC-2018-CARDIOMETABOLIC":
        targets = [
            ("Introduction", None),  # Doc start
            ("Review of the Science", re.compile(r"^REVIEW OF THE SCIENCE\s*$", re.I)),
            ("Overview of Questions Addressed", re.compile(r"^Overview of Questions Addressed\s*$", re.I)),
            ("Data Sources and Process Used to Answer Questions", re.compile(r"^Data Sources and Process Used to Answer Questions\s*$", re.I)),
            ("Question 1", re.compile(r"^Question 1[:.]", re.I)),
            ("Question 2", re.compile(r"^Question 2[:.]", re.I)),
            ("Question 3", re.compile(r"^Question 3[:.]", re.I)),
            ("Needs for Future Research", re.compile(r"^NEEDS FOR FUTURE RESEARCH\s*$", re.I)),
        ]
        for title, pat in targets:
            if pat is None:
                found.append((title, 0))
            else:
                idx = next((i for i, l in enumerate(lines) if pat.match(l.strip()) and not re.search(r"\.{3,}", l)), 0)
                found.append((title, idx))

    elif source_id == "US-HHS-PAGAC-2018-OLDER-ADULTS":
        # Note: lines 0-11 contain leaked TOC lines, so Introduction starts at L13 (index 12)
        intro_idx = next((i for i, l in enumerate(lines) if re.match(r"^INTRODUCTION\s*$", l.strip(), re.I)), 0)
        targets = [
            ("Introduction", intro_idx),
            ("Review of the Science", re.compile(r"^REVIEW OF THE SCIENCE\s*$", re.I)),
            ("Overview of Questions Addressed", re.compile(r"^Overview of Questions Addressed\s*$", re.I)),
            ("Data Sources and Process Used to Answer Questions", re.compile(r"^Data Sources and Process Used to Answer Questions\s*$", re.I)),
            ("Question 1", re.compile(r"^Question 1[:.]", re.I)),
            ("Question 2", re.compile(r"^Question 2[:.]", re.I)),
            ("Question 3", re.compile(r"^Question 3[:.]", re.I)),
            ("Overall Summary and Conclusions", re.compile(r"^OVERALL SUMMARY AND CONCLUSIONS\s*$", re.I)),
            ("Needs for Future Research", re.compile(r"^NEEDS FOR FUTURE RESEARCH\s*$", re.I)),
        ]
        for title, pat_or_idx in targets:
            if isinstance(pat_or_idx, int):
                found.append((title, pat_or_idx))
            else:
                # search strictly after intro_idx to avoid leaked TOC lines
                idx = next((i for i in range(intro_idx, len(lines)) if pat_or_idx.match(lines[i].strip()) and not re.search(r"\.{3,}", lines[i])), 0)
                found.append((title, idx))

    return found


def run_inventory():
    tok = load_tokenizer("artifacts/final_tokenizer/tokenizer.json")
    train_path = REPO_ROOT / "data" / "staging_phase11_4" / "train_staging.json"
    train_docs = json.loads(train_path.read_text(encoding="utf-8"))
    train_map = {d["source_id"]: d for d in train_docs}

    all_results = []
    print("=" * 100)
    print("PHASE 11.5 SECTION INVENTORY (5 Cleaned PAGAC Chapters)")
    print("=" * 100)
    print(f"{'Section / Question Title':<55} | {'First-Last Label':<18} | {'Cleaned Tokens'}")
    print("-" * 100)

    for spec in CHAPTER_SPECS:
        sid = spec["source_id"]
        doc = train_map[sid]
        lines = doc["text"].splitlines()
        toc_entries = parse_chapter_toc(sid)
        ranged_entries = compute_label_ranges(toc_entries, spec["chapter_last_label"])

        # Locate sections in cleaned lines
        section_starts = find_section_line_indices(sid, lines)
        start_map = {title: idx for title, idx in section_starts}

        doc_section_records = []
        print(f"\n--- {sid} ({spec['chapter_title']}) ---")

        for idx, entry in enumerate(ranged_entries):
            title = entry["title"]
            lbl_range = entry["label_range"]

            # If section is "References", it was removed by cleaning rules
            if title.lower() == "references":
                cleaned_tokens = 0
                line_range = "REMOVED_BY_CLEANING_RULE"
            else:
                # Find start line
                matched_start = -1
                for short_title, line_idx in section_starts:
                    if short_title.lower() in title.lower() or title.lower().startswith(short_title.lower()):
                        matched_start = line_idx
                        break

                if matched_start == -1:
                    matched_start = 0

                # Find end line
                # End line is the start line of the next section that appears in section_starts
                matched_end = len(lines)
                for next_entry in ranged_entries[idx + 1:]:
                    nxt_title = next_entry["title"]
                    if nxt_title.lower() == "references":
                        continue
                    nxt_start = -1
                    for short_title, line_idx in section_starts:
                        if short_title.lower() in nxt_title.lower() or nxt_title.lower().startswith(short_title.lower()):
                            nxt_start = line_idx
                            break
                    if nxt_start > matched_start:
                        matched_end = nxt_start
                        break

                sec_text = "\n".join(lines[matched_start:matched_end])
                cleaned_tokens = len(tok.encode(sec_text))
                line_range = f"L{matched_start + 1}-L{matched_end}"

            display_title = title if len(title) <= 52 else title[:49] + "..."
            print(f"{display_title:<55} | {lbl_range:<18} | {cleaned_tokens}")

            doc_section_records.append({
                "section_title": title,
                "first_label": entry["first_label"],
                "last_label": entry["last_label"],
                "first_last_label": lbl_range,
                "line_range": line_range,
                "cleaned_tokens": cleaned_tokens,
            })

        all_results.append({
            "source_id": sid,
            "chapter_title": spec["chapter_title"],
            "total_cleaned_tokens": len(tok.encode(doc["text"])),
            "sections": doc_section_records,
        })

    print("=" * 100)

    # Save output JSON
    out_dir = REPO_ROOT / "data" / "staging_phase11_4" / "audit_outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "pagac_section_inventory.json"
    output_payload = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "chapters_inventoried_count": len(all_results),
        "chapters": all_results,
    }
    out_file.write_text(json.dumps(output_payload, indent=2), encoding="utf-8")
    print(f"\nSection inventory written to {out_file}")


if __name__ == "__main__":
    run_inventory()
