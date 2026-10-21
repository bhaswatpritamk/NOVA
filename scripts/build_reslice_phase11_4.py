"""
scripts/build_reslice_phase11_4.py
Phase 11.4 B2-B4: Candidate Re-slice in data/staging_phase11_4/
Re-extracts complete units for 5 PAGAC docs, applies deterministic cleaning,
copies unchanged CDC/NIOSH/PLOS docs, and generates staging manifest.
"""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import pypdf
import re
import sys

sys.path.insert(0, "src")
from nova.tokenizer import load_tokenizer
from nova.ingestion import PILLAR_DISPLAY_NAMES

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def clean_extracted_pages(reader, start_page, end_page, tok):
    raw_lines = []
    rule_headers = []
    
    # 1. Page-by-page header/footer/page-label removal
    for p in range(start_page, end_page + 1):
        txt = reader.pages[p - 1].extract_text() or ""
        page_lines = txt.splitlines()
        n = len(page_lines)
        p_lines_kept = []
        i = 0
        
        # Check top lines of the page for headers
        while i < min(n, 6):
            line = page_lines[i]
            s = line.strip()
            if re.match(r"^Part\s+[A-Z]\.?\s*(Chapter|\b)", s, re.I):
                rule_headers.append(line)
                i += 1
                continue
            if "2018 Physical Activity Guidelines Advisory Committee" in s:
                rule_headers.append(line)
                i += 1
                continue
            if re.match(r"^[A-Z]\d*-\d+$", s):
                rule_headers.append(line)
                i += 1
                continue
            if p == start_page and re.match(r"^PART\s+[A-Z]\.?\s*CHAPTER", s, re.I):
                rule_headers.append(line)
                i += 1
                continue
            if p == start_page and re.match(r"^PART\s+A\.?\s*EXECUTIVE\s+SUMMARY", s, re.I):
                rule_headers.append(line)
                i += 1
                continue
            if p == start_page and s in [
                "STEPS, BOUTS, AND HIGH INTENSITY TRAINING",
                "AND PREVENTION OF WEIGHT GAIN",
            ]:
                rule_headers.append(line)
                i += 1
                continue
            break
            
        while i < n:
            line = page_lines[i]
            s = line.strip()
            if re.match(r"^[A-Z]\d*-\d+$", s):
                rule_headers.append(line)
            else:
                p_lines_kept.append(line)
            i += 1
            
        raw_lines.extend(p_lines_kept)

    # 2. Table of Contents removal
    lines_after_toc = []
    rule_toc = []
    in_toc = False
    
    for line in raw_lines:
        s = line.strip()
        if not in_toc:
            if s.lower() == "table of contents":
                in_toc = True
                rule_toc.append(line)
                continue
            else:
                lines_after_toc.append(line)
        else:
            if re.match(r"^\.{3,}|\.\s*\.\s*\.\s*\.", s) or re.search(r"\.{3,}\s*[A-Z0-9\-]+", s):
                rule_toc.append(line)
                continue
            elif s.upper() in ["INTRODUCTION", "INTRODUCTION "] or (s.startswith("Introduction") and not re.search(r"\.{3,}", s)):
                in_toc = False
                lines_after_toc.append(line)
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
                rule_toc.append(line)
                continue
            else:
                in_toc = False
                lines_after_toc.append(line)

    # 3. Trailing references list removal
    rule_refs = []
    cleaned_lines = []
    ref_idx = -1
    for idx, line in enumerate(lines_after_toc):
        s = line.strip()
        if re.match(r"^REFERENCES\s*$", s, re.I):
            if idx > len(lines_after_toc) * 0.5:
                ref_idx = idx
                break
                
    if ref_idx != -1:
        cleaned_lines = lines_after_toc[:ref_idx]
        rule_refs = lines_after_toc[ref_idx:]
    else:
        cleaned_lines = lines_after_toc

    # 4. Third-party exclusions scan in cleaned lines (1-based line numbers)
    third_party_exclusions = []
    for line_no, line in enumerate(cleaned_lines, 1):
        if re.search(r"adapted\s+from|source:\s*adapted", line, re.I):
            third_party_exclusions.append({
                "line_number": line_no,
                "text": line.strip()
            })

    cleaned_text = "\n".join(cleaned_lines)
    
    # Calculate log stats
    hdr_text = "\n".join(rule_headers)
    toc_text = "\n".join(rule_toc)
    ref_text = "\n".join(rule_refs)
    
    hdr_tokens = len(tok.encode(hdr_text)) if hdr_text else 0
    toc_tokens = len(tok.encode(toc_text)) if toc_text else 0
    ref_tokens = len(tok.encode(ref_text)) if ref_text else 0
    
    cleaning_log = {
        "headers_footers": {
            "lines_removed": len(rule_headers),
            "characters_removed": len(hdr_text),
            "tokens_removed": hdr_tokens,
        },
        "table_of_contents": {
            "lines_removed": len(rule_toc),
            "characters_removed": len(toc_text),
            "tokens_removed": toc_tokens,
        },
        "references_list": {
            "lines_removed": len(rule_refs),
            "characters_removed": len(ref_text),
            "tokens_removed": ref_tokens,
        },
        "total_lines_removed": len(rule_headers) + len(rule_toc) + len(rule_refs),
        "total_chars_removed": len(hdr_text) + len(toc_text) + len(ref_text),
        "total_tokens_removed": hdr_tokens + toc_tokens + ref_tokens,
        "final_cleaned_lines": len(cleaned_lines),
        "final_cleaned_chars": len(cleaned_text),
        "final_cleaned_words": len(cleaned_text.split()),
        "final_cleaned_tokens": len(tok.encode(cleaned_text)),
        "third_party_exclusions_count": len(third_party_exclusions),
        "third_party_exclusions": third_party_exclusions,
    }
    
    return cleaned_text, third_party_exclusions, cleaning_log

def main():
    tok = load_tokenizer("artifacts/final_tokenizer/tokenizer.json")
    pdf_path = Path("data/staging_phase11/sources_raw/us_hhs_pagac_report_2018.pdf")
    reader = pypdf.PdfReader(str(pdf_path))
    
    # Load old staging documents
    old_train = json.load(open("data/staging_phase11/train_staging.json", encoding="utf-8"))
    old_val = json.load(open("data/staging_phase11/val_staging.json", encoding="utf-8"))
    
    old_train_map = {d["source_id"]: d for d in old_train}
    old_val_map = {d["source_id"]: d for d in old_val}
    
    # 5 PAGAC specs
    pagac_specs = [
        {
            "source_id": "US-HHS-PAGAC-2018-EXEC",
            "chapter_title": "Part A. Executive Summary",
            "first_label": "A-1",
            "last_label": "A-7",
            "pdf_page_range": [19, 25],
        },
        {
            "source_id": "US-HHS-PAGAC-2018-HIIT",
            "chapter_title": "Part F. Chapter 1. Physical Activity Behaviors: Steps, Bouts, and High-Intensity Interval Training",
            "first_label": "F1-1",
            "last_label": "F1-26",
            "pdf_page_range": [119, 144],
        },
        {
            "source_id": "US-HHS-PAGAC-2018-BRAIN-SLEEP",
            "chapter_title": "Part F. Chapter 3. Brain Health",
            "first_label": "F3-1",
            "last_label": "F3-61",
            "pdf_page_range": [188, 248],
        },
        {
            "source_id": "US-HHS-PAGAC-2018-CARDIOMETABOLIC",
            "chapter_title": "Part F. Chapter 5. Cardiometabolic Health and Prevention of Weight Gain",
            "first_label": "F5-1",
            "last_label": "F5-36",
            "pdf_page_range": [316, 351],
        },
        {
            "source_id": "US-HHS-PAGAC-2018-OLDER-ADULTS",
            "chapter_title": "Part F. Chapter 9. Older Adults",
            "first_label": "F9-1",
            "last_label": "F9-51",
            "pdf_page_range": [439, 489],
        },
    ]

    new_staging_dir = Path("data/staging_phase11_4")
    new_staging_dir.mkdir(parents=True, exist_ok=True)
    audit_out_dir = new_staging_dir / "audit_outputs"
    audit_out_dir.mkdir(parents=True, exist_ok=True)
    
    all_cleaning_logs = {}
    new_train_docs = []
    
    # Copy unchanged CDC docs from old train
    for sid in ["US-CDC-PA-ADULTS-2022", "US-CDC-PA-MEASURING-2022", "US-CDC-PA-OLDER-2022"]:
        doc = dict(old_train_map[sid])
        new_train_docs.append(doc)
        
    # Re-extract and clean the 5 PAGAC docs
    for spec in pagac_specs:
        sid = spec["source_id"]
        old_rec = old_train_map[sid]
        
        cleaned_text, third_party, clog = clean_extracted_pages(
            reader,
            spec["pdf_page_range"][0],
            spec["pdf_page_range"][1],
            tok
        )
        all_cleaning_logs[sid] = clog
        
        new_rec = dict(old_rec)
        new_rec["chapter_title"] = spec["chapter_title"]
        new_rec["first_label"] = spec["first_label"]
        new_rec["last_label"] = spec["last_label"]
        new_rec["pdf_page_range"] = spec["pdf_page_range"]
        new_rec["third_party_exclusions"] = third_party
        new_rec["text"] = cleaned_text
        new_rec["char_count"] = len(cleaned_text)
        new_rec["word_count"] = len(cleaned_text.split())
        new_rec["token_count"] = len(tok.encode(cleaned_text))
        new_rec["content_sha256"] = sha256_text(cleaned_text)
        
        new_train_docs.append(new_rec)
        
    # Copy unchanged docs into new val
    new_val_docs = [dict(old_val_map[sid]) for sid in ["PLOS-PONE-0215877", "US-CDC-NIOSH-HEAT-2016"]]
    
    # Save train and val staging files
    train_out_path = new_staging_dir / "train_staging.json"
    val_out_path = new_staging_dir / "val_staging.json"
    
    with open(train_out_path, "w", encoding="utf-8") as f:
        json.dump(new_train_docs, f, indent=2)
    with open(val_out_path, "w", encoding="utf-8") as f:
        json.dump(new_val_docs, f, indent=2)
        
    # Save cleaning log
    cleaning_log_path = audit_out_dir / "reslice_cleaning_log.json"
    with open(cleaning_log_path, "w", encoding="utf-8") as f:
        json.dump(all_cleaning_logs, f, indent=2)
        
    # Copy intake_registry.json from staging_phase11
    intake_registry = json.load(open("data/staging_phase11/intake_registry.json", encoding="utf-8"))
    with open(new_staging_dir / "intake_registry.json", "w", encoding="utf-8") as f:
        json.dump(intake_registry, f, indent=2)
        
    # Build phase11_4_staging_manifest.json
    total_train_tokens = sum(d["token_count"] for d in new_train_docs)
    total_val_tokens = sum(d["token_count"] for d in new_val_docs)
    total_combined_tokens = total_train_tokens + total_val_tokens
    
    # Pillar coverage
    all_docs = new_train_docs + new_val_docs
    pillar_coverage = {}
    for pid, dname in PILLAR_DISPLAY_NAMES.items():
        pdocs = [d for d in all_docs if d["pillar"] == pid]
        p_tokens = sum(d["token_count"] for d in pdocs)
        p_chars = sum(d["char_count"] for d in pdocs)
        p_words = sum(d["word_count"] for d in pdocs)
        p_pct = round((p_tokens / total_combined_tokens) * 100, 2) if total_combined_tokens > 0 else 0.0
        pillar_coverage[pid] = {
            "pillar": pid,
            "display_name": dname,
            "doc_count": len(pdocs),
            "char_count": p_chars,
            "word_count": p_words,
            "token_count": p_tokens,
            "token_percentage": p_pct,
        }
        
    manifest = {
        "version": "11.4.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "authoritative_tokenizer_hash": "",
        "authoritative_tokenizer_vocab_size": len(tok.get_vocab()),
        "total_raw_sources_registered": 10,
        "total_documents_ingested": 17,
        "total_documents_approved": 10,
        "total_documents_quarantined": 7,
        "total_training_tokens": total_train_tokens,
        "total_validation_tokens": total_val_tokens,
        "total_combined_tokens": total_combined_tokens,
        "pillar_coverage": pillar_coverage,
    }
    
    manifest_out_path = new_staging_dir / "phase11_4_staging_manifest.json"
    with open(manifest_out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    print(f"Candidate re-slice complete in {new_staging_dir}:")
    print(f"  Train docs: {len(new_train_docs)} ({total_train_tokens} tokens)")
    print(f"  Val docs:   {len(new_val_docs)} ({total_val_tokens} tokens)")
    print(f"  Total tokens: {total_combined_tokens}")
    print(f"  Manifest written to {manifest_out_path}")
    print(f"  Cleaning log written to {cleaning_log_path}")

if __name__ == "__main__":
    main()
