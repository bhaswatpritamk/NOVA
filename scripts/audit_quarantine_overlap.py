#!/usr/bin/env python3
"""Project NOVA Phase 11.4 A6: PAGAC Quarantine Overlap Audit.

Computes exact 8-gram overlap between each of the 5 accepted PAGAC documents and
the two quarantined PAGAC extracts:
1. PAGAC-CONCEPTS (data/staging_phase11/sources_raw/pagac_2018_part_c_key_concepts.txt)
2. PAGAC-GLOSSARY (data/staging_phase11/sources_raw/pagac_2018_part_h_app1_glossary.txt)

Reports:
- Overlap 8-gram counts per accepted doc
- Verbatim overlapping 8-gram spans
- Page labels of overlapping spans
Outputs structured JSON to data/staging_phase11_4/audit_outputs/pagac_quarantine_overlap.json.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
TRAIN_STAGING_PATH = REPO_ROOT / "data" / "staging_phase11" / "train_staging.json"
SOURCES_RAW_DIR = REPO_ROOT / "data" / "staging_phase11" / "sources_raw"

CONCEPTS_PATH = SOURCES_RAW_DIR / "pagac_2018_part_c_key_concepts.txt"
GLOSSARY_PATH = SOURCES_RAW_DIR / "pagac_2018_part_h_app1_glossary.txt"

LABEL_PATTERN = re.compile(
    r"(?:2018\s+Physical\s+Activity\s+Guidelines\s+Advisory\s+Committee\s+Scientific\s+Report\s+)?\b([A-H]\d*-\d+|[ivx]+\b)\b",
    re.IGNORECASE,
)


def get_words_and_labels(text: str) -> List[Tuple[str, str]]:
    """Tokenize text into words while tracking nearest preceding printed page label."""
    lines = text.splitlines()
    word_label_pairs: List[Tuple[str, str]] = []
    current_label = "UNKNOWN"

    for line in lines:
        m = LABEL_PATTERN.search(line)
        if m:
            current_label = m.group(1).strip()
        words = line.split()
        for w in words:
            clean = re.sub(r"[^\w\-]", "", w).lower()
            if clean:
                word_label_pairs.append((clean, current_label))
    return word_label_pairs


def extract_labeled_8grams(text: str) -> Dict[str, str]:
    """Extract dict mapping 8-gram string to its associated page label."""
    pairs = get_words_and_labels(text)
    if len(pairs) < 8:
        return {}
    grams: Dict[str, str] = {}
    for i in range(len(pairs) - 7):
        span = pairs[i : i + 8]
        gram_str = " ".join(p[0] for p in span)
        # Use page label of the starting word
        label = span[0][1]
        if gram_str not in grams:
            grams[gram_str] = label
    return grams


def run_quarantine_overlap_audit(
    output_dir: Path = REPO_ROOT / "data" / "staging_phase11_4" / "audit_outputs",
) -> Dict[str, Any]:
    """Execute A6 quarantine overlap analysis."""
    train_docs = json.loads(TRAIN_STAGING_PATH.read_text(encoding="utf-8"))
    pagac_accepted = [d for d in train_docs if d["source_id"].startswith("US-HHS-PAGAC-2018")]

    if not CONCEPTS_PATH.is_file():
        raise FileNotFoundError(f"Missing PAGAC-CONCEPTS file at {CONCEPTS_PATH}")
    if not GLOSSARY_PATH.is_file():
        raise FileNotFoundError(f"Missing PAGAC-GLOSSARY file at {GLOSSARY_PATH}")

    concepts_text = CONCEPTS_PATH.read_text(encoding="utf-8", errors="ignore")
    glossary_text = GLOSSARY_PATH.read_text(encoding="utf-8", errors="ignore")

    concepts_8grams = extract_labeled_8grams(concepts_text)
    glossary_8grams = extract_labeled_8grams(glossary_text)

    print("=" * 105)
    print("PHASE 11.4 A6: ACCEPTED PAGAC vs QUARANTINED 8-GRAM OVERLAP AUDIT")
    print("=" * 105)
    print(f"Quarantined PAGAC-CONCEPTS unique 8-grams: {len(concepts_8grams)}")
    print(f"Quarantined PAGAC-GLOSSARY unique 8-grams: {len(glossary_8grams)}")
    print("-" * 105)

    results: Dict[str, Any] = {}

    for doc in pagac_accepted:
        sid = doc["source_id"]
        doc_8grams = extract_labeled_8grams(doc["text"])

        # Intersect with CONCEPTS
        overlap_concepts_keys = set(doc_8grams.keys()) & set(concepts_8grams.keys())
        overlap_concepts = [
            {
                "ngram": k,
                "doc_page_label": doc_8grams[k],
                "quarantine_page_label": concepts_8grams[k],
            }
            for k in sorted(list(overlap_concepts_keys))
        ]

        # Intersect with GLOSSARY
        overlap_glossary_keys = set(doc_8grams.keys()) & set(glossary_8grams.keys())
        overlap_glossary = [
            {
                "ngram": k,
                "doc_page_label": doc_8grams[k],
                "quarantine_page_label": glossary_8grams[k],
            }
            for k in sorted(list(overlap_glossary_keys))
        ]

        results[sid] = {
            "source_id": sid,
            "title": doc.get("title", ""),
            "doc_unique_8grams": len(doc_8grams),
            "overlap_concepts_count": len(overlap_concepts),
            "overlap_glossary_count": len(overlap_glossary),
            "total_quarantine_overlap_count": len(overlap_concepts) + len(overlap_glossary),
            "concepts_overlapping_labels": sorted(list({o["doc_page_label"] for o in overlap_concepts})),
            "glossary_overlapping_labels": sorted(list({o["doc_page_label"] for o in overlap_glossary})),
            "sample_concepts_overlaps": overlap_concepts[:5],
            "sample_glossary_overlaps": overlap_glossary[:5],
        }

        print(
            f"{sid:<34} | "
            f"vs CONCEPTS: {len(overlap_concepts):<4} (labels: {results[sid]['concepts_overlapping_labels']}) | "
            f"vs GLOSSARY: {len(overlap_glossary):<4} (labels: {results[sid]['glossary_overlapping_labels']})"
        )

    print("=" * 105)

    output_data = {
        "timestamp_utc": "2026-10-21T12:00:00Z",
        "concepts_source_path": str(CONCEPTS_PATH.relative_to(REPO_ROOT)),
        "glossary_source_path": str(GLOSSARY_PATH.relative_to(REPO_ROOT)),
        "concepts_unique_8grams": len(concepts_8grams),
        "glossary_unique_8grams": len(glossary_8grams),
        "results": results,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / "pagac_quarantine_overlap.json"
    out_file.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
    print(f"Quarantine overlap audit JSON written to {out_file}")
    return output_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit PAGAC quarantine 8-gram overlap.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "data" / "staging_phase11_4" / "audit_outputs",
        help="Directory to save audit outputs",
    )
    args = parser.parse_args()
    run_quarantine_overlap_audit(output_dir=args.output_dir)
