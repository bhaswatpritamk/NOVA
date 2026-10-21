#!/usr/bin/env python3
"""Project NOVA Phase 11.4: Boundary and Extraction-Quality Evidence Audit.

Audits the 10 accepted staging documents from data/staging_phase11/train_staging.json
and data/staging_phase11/val_staging.json.

Hard rules:
- Load documents ONLY from train_staging.json and val_staging.json.
- No directory globbing.
- Fail unless exactly 10 docs load and their source_ids match the 10 accepted ones.
- Print per doc: doc_id, source_id, parent_source_id, partition, tokens, lines, words, SHA-256 of text.
- Re-run repaired extraction metrics and print per-doc counts and %.
- Writes structured JSON to data/staging_phase11_4/audit_outputs/boundary_extraction_quality.json.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from nova.tokenizer import load_tokenizer

ACCEPTED_SOURCE_IDS = {
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
}

# Repaired detection regular expressions
REF_LIST_PATTERN = re.compile(
    r"^\s*(?:\d+[\.\)]|\[\d+\])\s+[A-Za-z]|(?:doi\s*:\s*10\.\d{4,9}|\bdoi\.org/|\b(?:19|20)\d{2}\s*;\s*\d+)",
    re.IGNORECASE,
)
TOC_PATTERN = re.compile(
    r"(\.{3,}|\.\s*\.\s*\.\s*\.|\.\s\.\s\.)",
    re.IGNORECASE,
)
RUNNING_HEADER_PATTERN = re.compile(
    r"^\s*(?:Part\s+[A-Z]|PART\s+[A-Z]|2018\s+Physical\s+Activity\s+Guidelines\s+Advisory\s+Committee\s+Scientific\s+Report|Membership\s+Lists|Table\s+of\s+Contents)",
    re.IGNORECASE,
)
SOURCE_ADAPTED_PATTERN = re.compile(
    r"(?:source:\s*adapted|adapted\s+from)",
    re.IGNORECASE,
)
PAGE_NUMBER_PATTERN = re.compile(
    r"2018\s+Physical\s+Activity\s+Guidelines\s+Advisory\s+Committee\s+Scientific\s+Report\s+([A-Za-z0-9\-]+)|^\s*(?:page\s*)?([A-Za-z0-9\-]+|\d+)\s*$",
    re.IGNORECASE,
)


def load_staged_documents(staging_dir: Path) -> List[Dict[str, Any]]:
    """Load staged documents strictly from train_staging.json and val_staging.json."""
    train_path = staging_dir / "train_staging.json"
    val_path = staging_dir / "val_staging.json"

    if not train_path.is_file():
        raise FileNotFoundError(f"Missing train_staging.json at {train_path}")
    if not val_path.is_file():
        raise FileNotFoundError(f"Missing val_staging.json at {val_path}")

    train_docs: List[Dict[str, Any]] = json.loads(train_path.read_text(encoding="utf-8"))
    val_docs: List[Dict[str, Any]] = json.loads(val_path.read_text(encoding="utf-8"))

    combined: List[Dict[str, Any]] = []
    for d in train_docs:
        doc_copy = dict(d)
        doc_copy["partition"] = "train"
        combined.append(doc_copy)

    for d in val_docs:
        doc_copy = dict(d)
        doc_copy["partition"] = "val"
        combined.append(doc_copy)

    # Invariant checks
    if len(combined) != 10:
        raise ValueError(f"Expected exactly 10 staged documents, loaded {len(combined)}")

    loaded_ids = {d["source_id"] for d in combined}
    if loaded_ids != ACCEPTED_SOURCE_IDS:
        missing = ACCEPTED_SOURCE_IDS - loaded_ids
        unexpected = loaded_ids - ACCEPTED_SOURCE_IDS
        raise ValueError(
            f"Staged documents mismatch accepted IDs. Missing: {missing}, Unexpected: {unexpected}"
        )

    return combined


def audit_document_boundaries(
    doc: Dict[str, Any],
    tokenizer: Any,
) -> Dict[str, Any]:
    """Audit single document for boundary lines and extraction-quality artifacts."""
    source_id = doc["source_id"]
    doc_id = doc.get("doc_id", "NOT_COMPUTED")
    parent_source_id = doc.get("parent_source_id", "NOT_COMPUTED")
    partition = doc.get("partition", "NOT_COMPUTED")
    text = doc["text"]

    lines = text.splitlines()
    total_chars = sum(len(line) for line in lines)
    total_lines = len(lines)
    words = text.split()
    total_words = len(words)
    token_ids = tokenizer.encode(text)
    total_tokens = len(token_ids)
    text_sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()

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
                m = pat.search(line)
                if m:
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
        pct_chars = (chars / total_chars * 100.0) if total_chars else 0.0
        pct_lines = (len(matches) / total_lines * 100.0) if total_lines else 0.0
        sample_matches = [
            {"line_number": m["line_number"], "content": m["content"][:120]}
            for m in matches[:5]
        ]
        category_summaries[cat_key] = {
            "line_count": len(matches),
            "line_percentage": round(pct_lines, 2),
            "char_count": chars,
            "char_percentage": round(pct_chars, 2),
            "sample_lines": sample_matches,
        }

    return {
        "source_id": source_id,
        "doc_id": doc_id,
        "parent_source_id": parent_source_id,
        "partition": partition,
        "title": doc.get("title", "NOT_COMPUTED"),
        "status": "COMPUTED",
        "total_tokens": total_tokens,
        "total_lines": total_lines,
        "total_words": total_words,
        "total_characters": total_chars,
        "text_sha256": text_sha256,
        "first_5_lines": first_5,
        "last_15_lines": last_15,
        "categories": category_summaries,
    }


def run_boundary_quality_audit(
    staging_dir: Path = REPO_ROOT / "data" / "staging_phase11",
    output_dir: Path = REPO_ROOT / "data" / "staging_phase11_4" / "audit_outputs",
) -> Dict[str, Any]:
    """Execute boundary and extraction quality audit across all 10 accepted documents."""
    tokenizer_path = REPO_ROOT / "artifacts" / "final_tokenizer" / "tokenizer.json"
    tokenizer = load_tokenizer(tokenizer_path)

    documents = load_staged_documents(staging_dir)

    print("=" * 110)
    print("PHASE 11.4 A1 DOCUMENT MANIFEST & CHECKSUMS (from train_staging.json & val_staging.json)")
    print("=" * 110)
    print(f"{'doc_id':<42} {'source_id':<30} {'parent_source_id':<24} {'part':<5} {'toks':<6} {'lines':<5} {'words':<6} {'SHA-256'}")
    print("-" * 110)

    results: Dict[str, Any] = {}
    summary_table: List[Dict[str, Any]] = []

    for doc in documents:
        doc_res = audit_document_boundaries(doc, tokenizer)
        sid = doc_res["source_id"]
        results[sid] = doc_res

        print(
            f"{doc_res['doc_id']:<42} "
            f"{doc_res['source_id']:<30} "
            f"{str(doc_res['parent_source_id']):<24} "
            f"{doc_res['partition']:<5} "
            f"{doc_res['total_tokens']:<6} "
            f"{doc_res['total_lines']:<5} "
            f"{doc_res['total_words']:<6} "
            f"{doc_res['text_sha256'][:16]}..."
        )

        cats = doc_res["categories"]
        summary_table.append({
            "source_id": sid,
            "partition": doc_res["partition"],
            "total_lines": doc_res["total_lines"],
            "total_chars": doc_res["total_characters"],
            "references_lines": cats["reference_list_lines"]["line_count"],
            "references_chars": cats["reference_list_lines"]["char_count"],
            "references_pct": cats["reference_list_lines"]["char_percentage"],
            "toc_lines": cats["table_of_contents_lines"]["line_count"],
            "toc_chars": cats["table_of_contents_lines"]["char_count"],
            "toc_pct": cats["table_of_contents_lines"]["char_percentage"],
            "headers_lines": cats["running_header_lines"]["line_count"],
            "headers_chars": cats["running_header_lines"]["char_count"],
            "headers_pct": cats["running_header_lines"]["char_percentage"],
            "adapted_lines": cats["source_adapted_lines"]["line_count"],
            "adapted_chars": cats["source_adapted_lines"]["char_count"],
            "adapted_pct": cats["source_adapted_lines"]["char_percentage"],
            "page_art_lines": cats["page_number_artifacts"]["line_count"],
            "page_art_chars": cats["page_number_artifacts"]["char_count"],
            "page_art_pct": cats["page_number_artifacts"]["char_percentage"],
        })

    print("=" * 110)
    print("A3 EXTRACTION METRICS (COUNTS AND PERCENTAGES)")
    print("=" * 110)
    print(f"{'source_id':<32} {'lines':<5} {'chars':<7} {'ref_lines':<9} {'ref_chars(%)':<14} {'toc_lines':<9} {'toc_chars(%)':<14}")
    print("-" * 110)
    for r in summary_table:
        ref_str = f"{r['references_chars']} ({r['references_pct']}%)"
        toc_str = f"{r['toc_chars']} ({r['toc_pct']}%)"
        print(f"{r['source_id']:<32} {r['total_lines']:<5} {r['total_chars']:<7} {r['references_lines']:<9} {ref_str:<14} {r['toc_lines']:<9} {toc_str:<14}")
    print("=" * 110)

    output_data = {
        "timestamp_utc": "2026-10-21T12:00:00Z",
        "staging_source": str(staging_dir),
        "documents_audited_count": len(documents),
        "summary_table": summary_table,
        "results": results,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / "boundary_extraction_quality.json"
    out_file.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
    print(f"Boundary extraction quality audit written to {out_file}")
    return output_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit boundary and extraction quality.")
    parser.add_argument(
        "--staging-dir",
        type=Path,
        default=REPO_ROOT / "data" / "staging_phase11",
        help="Path to directory containing train_staging.json and val_staging.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "data" / "staging_phase11_4" / "audit_outputs",
        help="Path to directory where audit outputs JSON will be saved",
    )
    args = parser.parse_args()
    run_boundary_quality_audit(staging_dir=args.staging_dir, output_dir=args.output_dir)
