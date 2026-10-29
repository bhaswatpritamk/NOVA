#!/usr/bin/env python3
"""Project NOVA Phase 11.5: Quarantine Overlap on New Docs.

Loads the cleaned PAGAC docs from data/staging_phase11_4/train_staging.json;
applies the same cleaning rules (headers, TOC, references) to the quarantined
Part C and Glossary texts; excludes any 8-gram made only of header or reference strings.

Prints per doc: longest contiguous shared run in words, with doc line numbers and both texts.
Also prints the Glossary's flagged "high/critical health claim" sentence verbatim
from its quarantine record and whether that exact string appears in any accepted doc.

Outputs structured JSON to:
data/staging_phase11_4/audit_outputs/pagac_quarantine_overlap_phase11_5.json
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent

TRAIN_STAGING_PATH = REPO_ROOT / "data" / "staging_phase11_4" / "train_staging.json"
VAL_STAGING_PATH = REPO_ROOT / "data" / "staging_phase11_4" / "val_staging.json"
SOURCES_RAW_DIR = REPO_ROOT / "data" / "staging_phase11" / "sources_raw"

CONCEPTS_PATH = SOURCES_RAW_DIR / "pagac_2018_part_c_key_concepts.txt"
GLOSSARY_PATH = SOURCES_RAW_DIR / "pagac_2018_part_h_app1_glossary.txt"

GLOSSARY_FLAGGED_HEALTH_CLAIM = (
    "The current criteria used to diagnose diabetes are an HbA1C of 6.5% or higher, "
    "fasting blood glucose of 126 mg per dL or higher, and/or a 2-hour oral glucose "
    "tolerance test (OGTT) blood glucose of 200 mg per dL or higher."
)

BOILERPLATE_PATTERNS = [
    re.compile(r"physical\s+activity\s+guidelines\s+advisory\s+committee\s+scientific\s+report", re.I),
    re.compile(r"department\s+of\s+health\s+and\s+human\s+services", re.I),
    re.compile(r"centers\s+for\s+disease\s+control\s+and\s+prevention", re.I),
    re.compile(r"washington\s+dc\s+u\s+s\s+department", re.I),
    re.compile(r"table\s+of\s+contents", re.I),
    re.compile(r"doi\s+org\s+10\s+\d+", re.I),
]


def clean_raw_lines(raw_lines: List[str]) -> List[str]:
    """Apply standard PAGAC cleaning rules (headers, TOC, references) to raw text lines."""
    cleaned = []
    in_toc = False
    in_refs = False

    for line in raw_lines:
        s = line.strip()

        # Rule 1: Headers, footers, page labels
        if re.match(r"^Part\s+[A-Z]\.?\s*(Chapter|Appendix|\b)", s, re.I):
            continue
        if "2018 Physical Activity Guidelines Advisory Committee" in s:
            continue
        if re.match(r"^[A-Z]\d*-\d+$", s):
            continue
        if re.match(r"^PART\s+[A-Z]\.?", s):
            continue

        # Rule 2: Table of Contents
        if s.lower() == "table of contents":
            in_toc = True
            continue
        if in_toc:
            if re.match(r"^\.{3,}|\.\s*\.\s*\.\s*\.", s) or re.search(r"\.{3,}\s*[A-Z0-9\-]+", s):
                continue
            elif re.search(r"[A-Z0-9\-]+$", s) and len(s) < 80:
                continue
            else:
                in_toc = False

        # Rule 3: Trailing references list
        if re.match(r"^REFERENCES\s*$", s, re.I):
            in_refs = True
            continue
        if in_refs:
            continue

        cleaned.append(line)

    return cleaned


def is_boilerplate(span_text: str) -> bool:
    """Return True if span consists entirely of header/reference/boilerplate strings."""
    for pat in BOILERPLATE_PATTERNS:
        if pat.search(span_text):
            return True
    return False


def get_words_with_line_numbers(lines: List[str]) -> List[Dict[str, Any]]:
    """Tokenize lines into word units preserving 1-based line numbers and raw strings."""
    words: List[Dict[str, Any]] = []
    for line_no, line in enumerate(lines, 1):
        for w in line.split():
            clean = re.sub(r"[^\w\-]", "", w).lower()
            if clean:
                words.append({
                    "clean": clean,
                    "raw": w,
                    "line_no": line_no,
                })
    return words


def find_longest_contiguous_run(
    doc_words: List[Dict[str, Any]],
    quar_words: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Find the longest contiguous run of normalized words between doc and quarantined text."""
    w1 = [x["clean"] for x in doc_words]
    w2 = [x["clean"] for x in quar_words]

    # Inverted index on quar_words for fast lookup
    index2: Dict[str, List[int]] = {}
    for j, word in enumerate(w2):
        index2.setdefault(word, []).append(j)

    best_len = 0
    best_doc_span = (0, 0)
    best_quar_span = (0, 0)

    for i, word in enumerate(w1):
        if word in index2:
            for j in index2[word]:
                k = 0
                while i + k < len(w1) and j + k < len(w2) and w1[i + k] == w2[j + k]:
                    k += 1

                if k > best_len:
                    span_str = " ".join(w1[i : i + k])
                    if is_boilerplate(span_str) and k <= 10:
                        continue
                    best_len = k
                    best_doc_span = (i, i + k)
                    best_quar_span = (j, j + k)

    if best_len > 0:
        doc_raw = " ".join(doc_words[x]["raw"] for x in range(best_doc_span[0], best_doc_span[1]))
        quar_raw = " ".join(quar_words[x]["raw"] for x in range(best_quar_span[0], best_quar_span[1]))
        doc_lstart = doc_words[best_doc_span[0]]["line_no"]
        doc_lend = doc_words[best_doc_span[1] - 1]["line_no"]
        quar_lstart = quar_words[best_quar_span[0]]["line_no"]
        quar_lend = quar_words[best_quar_span[1] - 1]["line_no"]
        return {
            "longest_run_words": best_len,
            "doc_line_range": f"L{doc_lstart}-L{doc_lend}",
            "doc_line_start": doc_lstart,
            "doc_line_end": doc_lend,
            "doc_matched_text": doc_raw,
            "quarantine_line_range": f"L{quar_lstart}-L{quar_lend}",
            "quarantine_line_start": quar_lstart,
            "quarantine_line_end": quar_lend,
            "quarantine_matched_text": quar_raw,
        }
    else:
        return {
            "longest_run_words": 0,
            "doc_line_range": "N/A",
            "doc_line_start": None,
            "doc_line_end": None,
            "doc_matched_text": "",
            "quarantine_line_range": "N/A",
            "quarantine_line_start": None,
            "quarantine_line_end": None,
            "quarantine_matched_text": "",
        }


def run_quarantine_overlap_audit():
    train_docs = json.loads(TRAIN_STAGING_PATH.read_text(encoding="utf-8"))
    val_docs = json.loads(VAL_STAGING_PATH.read_text(encoding="utf-8"))
    all_accepted = train_docs + val_docs

    pagac_docs = [d for d in train_docs if d["source_id"].startswith("US-HHS-PAGAC-2018")]

    # Load and clean Part C and Glossary
    c_raw = CONCEPTS_PATH.read_text(encoding="utf-8", errors="ignore").splitlines()
    g_raw = GLOSSARY_PATH.read_text(encoding="utf-8", errors="ignore").splitlines()

    c_clean = clean_raw_lines(c_raw)
    g_clean = clean_raw_lines(g_raw)

    c_words = get_words_with_line_numbers(c_clean)
    g_words = get_words_with_line_numbers(g_clean)

    print("=" * 110)
    print("PHASE 11.5 TASK 3: QUARANTINE OVERLAP AUDIT ON NEW CLEANED PAGAC DOCS")
    print("=" * 110)
    print(f"Quarantined Part C (cleaned lines: {len(c_clean)}, words: {len(c_words)})")
    print(f"Quarantined Glossary (cleaned lines: {len(g_clean)}, words: {len(g_words)})")
    print("-" * 110)

    per_doc_results = []

    for doc in pagac_docs:
        sid = doc["source_id"]
        doc_lines = doc["text"].splitlines()
        doc_words = get_words_with_line_numbers(doc_lines)

        part_c_res = find_longest_contiguous_run(doc_words, c_words)
        glossary_res = find_longest_contiguous_run(doc_words, g_words)

        print(f"\nDOCUMENT: {sid} ({len(doc_lines)} lines, {len(doc_words)} words)")
        print(f"  Longest shared run with Part C:    {part_c_res['longest_run_words']} words "
              f"(Doc: {part_c_res['doc_line_range']}, Part C: {part_c_res['quarantine_line_range']})")
        if part_c_res['longest_run_words'] > 0:
            print(f"    Doc Text:        \"{part_c_res['doc_matched_text'][:120]}...\"")
            print(f"    Part C Text:     \"{part_c_res['quarantine_matched_text'][:120]}...\"")

        print(f"  Longest shared run with Glossary:  {glossary_res['longest_run_words']} words "
              f"(Doc: {glossary_res['doc_line_range']}, Glossary: {glossary_res['quarantine_line_range']})")
        if glossary_res['longest_run_words'] > 0:
            print(f"    Doc Text:        \"{glossary_res['doc_matched_text'][:120]}...\"")
            print(f"    Glossary Text:   \"{glossary_res['quarantine_matched_text'][:120]}...\"")

        per_doc_results.append({
            "source_id": sid,
            "doc_lines_count": len(doc_lines),
            "doc_words_count": len(doc_words),
            "part_c_overlap": part_c_res,
            "glossary_overlap": glossary_res,
        })

    # Check Glossary flagged health claim sentence against ALL accepted docs
    normalized_claim = " ".join(GLOSSARY_FLAGGED_HEALTH_CLAIM.split()).lower()
    claim_found_in: List[str] = []

    for doc in all_accepted:
        normalized_doc = " ".join(doc["text"].split()).lower()
        if normalized_claim in normalized_doc:
            claim_found_in.append(doc["source_id"])

    print("\n" + "=" * 110)
    print("GLOSSARY FLAGGED HEALTH CLAIM VERIFICATION")
    print("=" * 110)
    print("Flagged Sentence Verbatim:")
    print(f"  \"{GLOSSARY_FLAGGED_HEALTH_CLAIM}\"")
    print(f"Status in Accepted Documents: {'FOUND in ' + ', '.join(claim_found_in) if claim_found_in else 'NOT_FOUND in any accepted doc'}")
    print("=" * 110)

    out_payload = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "quarantined_sources": {
            "part_c": {
                "path": str(CONCEPTS_PATH),
                "cleaned_lines": len(c_clean),
                "cleaned_words": len(c_words),
            },
            "glossary": {
                "path": str(GLOSSARY_PATH),
                "cleaned_lines": len(g_clean),
                "cleaned_words": len(g_words),
            },
        },
        "glossary_flagged_health_claim": {
            "sentence_verbatim": GLOSSARY_FLAGGED_HEALTH_CLAIM,
            "found_in_accepted_docs": claim_found_in,
            "status": "NOT_FOUND" if not claim_found_in else "FOUND",
        },
        "per_doc_overlap": per_doc_results,
    }

    out_dir = REPO_ROOT / "data" / "staging_phase11_4" / "audit_outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "pagac_quarantine_overlap_phase11_5.json"
    out_file.write_text(json.dumps(out_payload, indent=2), encoding="utf-8")
    print(f"\nQuarantine overlap audit written to {out_file}")
    return out_payload


if __name__ == "__main__":
    run_quarantine_overlap_audit()
