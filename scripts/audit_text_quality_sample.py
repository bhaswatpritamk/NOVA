#!/usr/bin/env python3
"""scripts/audit_text_quality_sample.py

Project NOVA Phase 11.5 Task 7: Text-quality sample (report only).
For each of the 10 docs:
- A seeded (seed=42) random sample of 20 body lines verbatim with line numbers (not TOC or references)
- Count per 1,000 words of:
  (a) words with 1-3 digits fused to the end of letters (regex [A-Za-z]{3,}\d{1,3}\b)
  (b) lines shorter than 6 characters
  (c) lines that start with a lowercase fragment of 1-3 letters
Do not modify any text.

Outputs structured JSON to data/staging_phase11_4/audit_outputs/text_quality_sample.json.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import random
import re
import sys
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent

TRAIN_PATH = REPO_ROOT / "data" / "staging_phase11_4" / "train_staging.json"
VAL_PATH = REPO_ROOT / "data" / "staging_phase11_4" / "val_staging.json"

FUSED_DIGITS_PATTERN = re.compile(r"[A-Za-z]{3,}\d{1,3}\b")
LOWER_FRAGMENT_PATTERN = re.compile(r"^[a-z]{1,3}\b")
TOC_DOT_LEADER_PATTERN = re.compile(r"\.{3,}")
REFERENCES_HEADING_PATTERN = re.compile(r"^references\s*$", re.I)


def is_body_line(line: str) -> bool:
    """Return True if line is a body text line (not TOC, references, or blank)."""
    s = line.strip()
    if not s:
        return False
    if "table of contents" in s.lower() or TOC_DOT_LEADER_PATTERN.search(s):
        return False
    if REFERENCES_HEADING_PATTERN.match(s):
        return False
    return True


def audit_text_quality():
    train_docs = json.loads(TRAIN_PATH.read_text(encoding="utf-8"))
    val_docs = json.loads(VAL_PATH.read_text(encoding="utf-8"))
    all_docs = train_docs + val_docs

    print("=" * 115)
    print("PHASE 11.5 TASK 7: TEXT-QUALITY SAMPLE AUDIT (10 Documents in staging_phase11_4, seed=42)")
    print("=" * 115)

    doc_summaries = []

    for doc in all_docs:
        sid = doc["source_id"]
        partition = "train" if doc in train_docs else "val"
        raw_text = doc["text"]
        all_lines = raw_text.splitlines()
        words = raw_text.split()
        total_words = len(words)
        k_words = total_words / 1000.0 if total_words > 0 else 1.0

        # Compute metric (a): fused digits
        fused_matches = FUSED_DIGITS_PATTERN.findall(raw_text)
        count_fused = len(fused_matches)
        fused_per_1k = count_fused / k_words

        # Compute metric (b): short lines (< 6 characters)
        count_short_lines = sum(1 for l in all_lines if len(l.strip()) < 6)
        short_lines_per_1k = count_short_lines / k_words

        # Compute metric (c): starts with lowercase fragment of 1-3 letters
        count_lower_frag = sum(1 for l in all_lines if LOWER_FRAGMENT_PATTERN.match(l.strip()))
        lower_frag_per_1k = count_lower_frag / k_words

        # Collect eligible body lines with 1-based line numbers
        eligible_body_lines: List[Tuple[int, str]] = []
        for idx, line in enumerate(all_lines, 1):
            if is_body_line(line):
                eligible_body_lines.append((idx, line))

        # Seeded random sample of 20 body lines
        rng = random.Random(42)
        sample_size = min(20, len(eligible_body_lines))
        sampled_lines = rng.sample(eligible_body_lines, sample_size)
        sampled_lines.sort(key=lambda x: x[0])

        print(f"\n--- {sid} ({partition}, total lines: {len(all_lines)}, words: {total_words}) ---")
        print(f"  (a) Fused digits [A-Za-z]{{3,}}\\d{{1,3}}\\b:          {count_fused:4d} ({fused_per_1k:6.2f} / 1k words)")
        print(f"  (b) Lines < 6 chars:                             {count_short_lines:4d} ({short_lines_per_1k:6.2f} / 1k words)")
        print(f"  (c) Starts with lowercase 1-3 letter fragment:   {count_lower_frag:4d} ({lower_frag_per_1k:6.2f} / 1k words)")
        print("  Sample of 20 body lines verbatim (seed=42):")
        for line_no, line_str in sampled_lines:
            truncated = line_str if len(line_str) <= 85 else line_str[:82] + "..."
            print(f"    Line {line_no:4d}: {truncated}")

        doc_summaries.append({
            "source_id": sid,
            "partition": partition,
            "total_lines": len(all_lines),
            "total_words": total_words,
            "metrics_per_1k_words": {
                "fused_digits_count": count_fused,
                "fused_digits_per_1k": round(fused_per_1k, 2),
                "fused_digits_samples": list(set(fused_matches))[:10],
                "short_lines_count": count_short_lines,
                "short_lines_per_1k": round(short_lines_per_1k, 2),
                "lower_fragment_count": count_lower_frag,
                "lower_fragment_per_1k": round(lower_frag_per_1k, 2),
            },
            "sample_20_body_lines": [
                {"line_number": lno, "text": lstr}
                for lno, lstr in sampled_lines
            ],
        })

    # Summary table
    print("\n" + "=" * 115)
    print("TEXT QUALITY METRICS SUMMARY (Counts per 1,000 words)")
    print("=" * 115)
    print(f"{'Source ID':<35} | {'Words':<6} | {'(a) Fused /1k':<15} | {'(b) Short /1k':<15} | {'(c) Lower /1k'}")
    print("-" * 115)
    for s in doc_summaries:
        m = s["metrics_per_1k_words"]
        sid = s["source_id"]
        words = s["total_words"]
        print(f"{sid:<35} | {words:<6} | {m['fused_digits_count']:3d} ({m['fused_digits_per_1k']:5.2f}/1k) | {m['short_lines_count']:3d} ({m['short_lines_per_1k']:5.2f}/1k) | {m['lower_fragment_count']:3d} ({m['lower_fragment_per_1k']:5.2f}/1k)")
    print("=" * 115)

    # Save output JSON
    out_dir = REPO_ROOT / "data" / "staging_phase11_4" / "audit_outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "text_quality_sample.json"
    out_payload = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "random_seed": 42,
        "sample_size_per_doc": 20,
        "documents_audited_count": len(doc_summaries),
        "results": doc_summaries,
    }
    out_file.write_text(json.dumps(out_payload, indent=2), encoding="utf-8")
    print(f"\nText quality sample audit written to {out_file}")
    return out_payload


if __name__ == "__main__":
    audit_text_quality()
