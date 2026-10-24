#!/usr/bin/env python3
"""scripts/print_bench_matches.py

Project NOVA Phase 11.5 Task 4: Benchmark Overlap Table (print only).
For every doc in staging_phase11_4 AND the quarantined Part C and Glossary,
and every item in data/benchmark/fitness_eval_benchmark.json,
compute the longest contiguous word run against each benchmark field
(prompt, each expected_key_point, canonical reference answer, other).

Print a table of pairs with a longest run >= 8 words:
doc | item | field | longest run | the matched text.
Do not edit the benchmark.
Outputs structured JSON to data/staging_phase11_4/audit_outputs/benchmark_overlap_table.json.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent

BENCH_PATH = REPO_ROOT / "data" / "benchmark" / "fitness_eval_benchmark.json"
TRAIN_PATH = REPO_ROOT / "data" / "staging_phase11_4" / "train_staging.json"
VAL_PATH = REPO_ROOT / "data" / "staging_phase11_4" / "val_staging.json"

SOURCES_RAW_DIR = REPO_ROOT / "data" / "staging_phase11" / "sources_raw"
CONCEPTS_PATH = SOURCES_RAW_DIR / "pagac_2018_part_c_key_concepts.txt"
GLOSSARY_PATH = SOURCES_RAW_DIR / "pagac_2018_part_h_app1_glossary.txt"


def clean_words(text: str) -> List[Dict[str, Any]]:
    """Tokenize text into words with clean normalized form and raw string."""
    tokens = []
    # Match words
    for m in re.finditer(r"\b[\w\-]+\b", text):
        raw = m.group(0)
        clean = re.sub(r"[^\w\-]", "", raw).lower()
        if clean:
            tokens.append({
                "clean": clean,
                "raw": raw,
                "start": m.start(),
                "end": m.end(),
            })
    return tokens


def longest_contiguous_match(
    doc_words: List[Dict[str, Any]],
    field_words: List[Dict[str, Any]],
) -> Tuple[int, str]:
    """Find longest contiguous match of words between doc and field."""
    w1 = [x["clean"] for x in doc_words]
    w2 = [x["clean"] for x in field_words]
    m, n = len(w1), len(w2)
    if m == 0 or n == 0:
        return 0, ""

    # Inverted index on w2
    index2: Dict[str, List[int]] = {}
    for j, word in enumerate(w2):
        index2.setdefault(word, []).append(j)

    max_len = 0
    best_span = (0, 0)

    for i, word in enumerate(w1):
        if word in index2:
            for j in index2[word]:
                k = 0
                while i + k < m and j + k < n and w1[i + k] == w2[j + k]:
                    k += 1
                if k > max_len:
                    max_len = k
                    best_span = (i, i + k)

    if max_len > 0:
        matched_text = " ".join(doc_words[x]["raw"] for x in range(best_span[0], best_span[1]))
        return max_len, matched_text
    return 0, ""


def extract_benchmark_fields(bench_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract individual fields per benchmark item."""
    items = bench_data.get("questions", [])
    fields_list = []

    for item in items:
        qid = item.get("question_id") or item.get("id") or "UNKNOWN"

        # 1. Prompt
        prompt = item.get("prompt") or item.get("question") or ""
        if prompt:
            fields_list.append({
                "item_id": qid,
                "field_type": "prompt",
                "field_name": "prompt",
                "text": prompt,
                "words": clean_words(prompt),
            })

        # 2. Canonical reference answer
        ref_ans = item.get("canonical_reference_answer") or item.get("reference_answer") or ""
        if ref_ans:
            fields_list.append({
                "item_id": qid,
                "field_type": "canonical reference answer",
                "field_name": "canonical_reference_answer",
                "text": ref_ans,
                "words": clean_words(ref_ans),
            })

        # 3. Expected key points
        key_points = item.get("expected_key_points") or []
        for idx, kp in enumerate(key_points):
            if isinstance(kp, str):
                fields_list.append({
                    "item_id": qid,
                    "field_type": "expected_key_point",
                    "field_name": f"expected_key_points[{idx}]",
                    "text": kp,
                    "words": clean_words(kp),
                })

        # 4. Other fields (rubric, acceptable_alternatives, unacceptable_or_unsafe_points, etc.)
        for k, v in item.items():
            if k in ("question_id", "id", "pillar", "question_type", "sha256", "prompt", "question", "canonical_reference_answer", "reference_answer", "expected_key_points"):
                continue
            if isinstance(v, str) and v.strip():
                fields_list.append({
                    "item_id": qid,
                    "field_type": "other",
                    "field_name": k,
                    "text": v,
                    "words": clean_words(v),
                })
            elif isinstance(v, list):
                for idx, elem in enumerate(v):
                    if isinstance(elem, str) and elem.strip():
                        fields_list.append({
                            "item_id": qid,
                            "field_type": "other",
                            "field_name": f"{k}[{idx}]",
                            "text": elem,
                            "words": clean_words(elem),
                        })

    return fields_list


def main():
    bench_data = json.loads(BENCH_PATH.read_text(encoding="utf-8"))
    train_docs = json.loads(TRAIN_PATH.read_text(encoding="utf-8"))
    val_docs = json.loads(VAL_PATH.read_text(encoding="utf-8"))

    bench_fields = extract_benchmark_fields(bench_data)

    # 12 documents to check: 10 accepted + Part C + Glossary
    target_docs: List[Dict[str, str]] = []
    for d in train_docs + val_docs:
        target_docs.append({
            "doc_id": d["source_id"],
            "text": d["text"],
            "type": "accepted_staging",
        })

    if CONCEPTS_PATH.is_file():
        target_docs.append({
            "doc_id": "US-HHS-PAGAC-2018-CONCEPTS (Quarantined)",
            "text": CONCEPTS_PATH.read_text(encoding="utf-8", errors="ignore"),
            "type": "quarantined",
        })

    if GLOSSARY_PATH.is_file():
        target_docs.append({
            "doc_id": "US-HHS-PAGAC-2018-GLOSSARY (Quarantined)",
            "text": GLOSSARY_PATH.read_text(encoding="utf-8", errors="ignore"),
            "type": "quarantined",
        })

    print("=" * 125)
    print("PHASE 11.5 TASK 4: BENCHMARK OVERLAP TABLE (Longest Contiguous Word Run >= 8 Words)")
    print("=" * 125)
    print(f"{'Document':<35} | {'Item ID':<18} | {'Field':<28} | {'Run':<4} | {'Matched Text'}")
    print("-" * 125)

    matches_table: List[Dict[str, Any]] = []

    for doc in target_docs:
        doc_id = doc["doc_id"]
        doc_words = clean_words(doc["text"])

        for bf in bench_fields:
            item_id = bf["item_id"]
            field_name = bf["field_name"]
            field_words = bf["words"]

            if len(field_words) < 8:
                continue

            run_len, matched_str = longest_contiguous_match(doc_words, field_words)
            if run_len >= 8:
                matches_table.append({
                    "doc": doc_id,
                    "item": item_id,
                    "field": field_name,
                    "field_type": bf["field_type"],
                    "longest_run": run_len,
                    "matched_text": matched_str,
                })
                # Print row
                display_doc = doc_id if len(doc_id) <= 33 else doc_id[:30] + "..."
                display_field = field_name if len(field_name) <= 26 else field_name[:23] + "..."
                display_text = matched_str if len(matched_str) <= 32 else matched_str[:29] + "..."
                print(f"{display_doc:<35} | {item_id:<18} | {display_field:<28} | {run_len:<4} | {display_text}")

    print("=" * 125)
    print(f"Total pairs with longest contiguous run >= 8 words: {len(matches_table)}")

    # Write JSON output
    out_dir = REPO_ROOT / "data" / "staging_phase11_4" / "audit_outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "benchmark_overlap_table.json"
    out_payload = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "total_documents_checked": len(target_docs),
        "total_benchmark_fields_checked": len(bench_fields),
        "matches_count": len(matches_table),
        "matches": matches_table,
    }
    out_file.write_text(json.dumps(out_payload, indent=2), encoding="utf-8")
    print(f"\nBenchmark overlap table written to {out_file}")


if __name__ == "__main__":
    main()
