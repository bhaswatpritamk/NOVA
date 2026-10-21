"""
scripts/generate_chapter_inventory.py
Phase 11.4 B1: Inventory every Part and every Part F chapter in the PAGAC report.
Produces data/staging_phase11_4/audit_outputs/pagac_chapter_inventory.json.
"""

import json
from pathlib import Path
import pypdf
import sys

sys.path.insert(0, "src")
from nova.tokenizer import load_tokenizer

def main():
    tokenizer_path = Path("artifacts/final_tokenizer/tokenizer.json")
    tok = load_tokenizer(str(tokenizer_path))
    pdf_path = Path("data/staging_phase11/sources_raw/us_hhs_pagac_report_2018.pdf")
    reader = pypdf.PdfReader(str(pdf_path))

    # Define all Parts and all Part F Chapters
    # Note: Part F as an overall section spans 117-711. We list Parts A-H and Part F chapters 1-11.
    inventory_specs = [
        # Parts A-E
        {
            "unit_type": "Part",
            "unit_id": "Part A",
            "name": "Part A. Executive Summary",
            "header_text": "Part A. Executive Summary",
            "first_pdf_page_index": 19,
            "last_pdf_page_index": 25,
            "first_label": "A-1",
            "last_label": "A-7",
        },
        {
            "unit_type": "Part",
            "unit_id": "Part B",
            "name": "Part B. Introduction",
            "header_text": "Part B. Introduction",
            "first_pdf_page_index": 26,
            "last_pdf_page_index": 33,
            "first_label": "B-1",
            "last_label": "B-8",
        },
        {
            "unit_type": "Part",
            "unit_id": "Part C",
            "name": "Part C. Background and Key Physical Activity Concepts",
            "header_text": "Part C. Background and Key Physical Activity Concepts",
            "first_pdf_page_index": 34,
            "last_pdf_page_index": 64,
            "first_label": "C-1",
            "last_label": "C-31",
        },
        {
            "unit_type": "Part",
            "unit_id": "Part D",
            "name": "Part D. Integrating the Evidence",
            "header_text": "Part D. Integrating the Evidence",
            "first_pdf_page_index": 65,
            "last_pdf_page_index": 94,
            "first_label": "D-1",
            "last_label": "D-30",
        },
        {
            "unit_type": "Part",
            "unit_id": "Part E",
            "name": "Part E. Systematic Review Literature Search Methodology",
            "header_text": "Part E. Systematic Review Literature Search Methodology",
            "first_pdf_page_index": 95,
            "last_pdf_page_index": 116,
            "first_label": "E-1",
            "last_label": "E-22",
        },
        # Part F Chapters 1-11
        {
            "unit_type": "Part F Chapter",
            "unit_id": "Part F Chapter 1",
            "name": "Part F. Chapter 1. Physical Activity Behaviors: Steps, Bouts, and High-Intensity Interval Training",
            "header_text": "Part F. Chapter 1. Physical Activity Behaviors: Steps, Bouts, and High-Intensity Interval Training",
            "first_pdf_page_index": 119,
            "last_pdf_page_index": 144,
            "first_label": "F1-1",
            "last_label": "F1-26",
        },
        {
            "unit_type": "Part F Chapter",
            "unit_id": "Part F Chapter 2",
            "name": "Part F. Chapter 2. Sedentary Behavior",
            "header_text": "Part F. Chapter 2. Sedentary Behavior",
            "first_pdf_page_index": 145,
            "last_pdf_page_index": 186,
            "first_label": "F2-1",
            "last_label": "F2-42",
        },
        {
            "unit_type": "Part F Chapter",
            "unit_id": "Part F Chapter 3",
            "name": "Part F. Chapter 3. Brain Health",
            "header_text": "Part F. Chapter 3. Brain Health",
            "first_pdf_page_index": 188,
            "last_pdf_page_index": 248,
            "first_label": "F3-1",
            "last_label": "F3-61",
        },
        {
            "unit_type": "Part F Chapter",
            "unit_id": "Part F Chapter 4",
            "name": "Part F. Chapter 4. Cancer Prevention",
            "header_text": "Part F. Chapter 4. Cancer Prevention",
            "first_pdf_page_index": 249,
            "last_pdf_page_index": 315,
            "first_label": "F4-1",
            "last_label": "F4-67",
        },
        {
            "unit_type": "Part F Chapter",
            "unit_id": "Part F Chapter 5",
            "name": "Part F. Chapter 5. Cardiometabolic Health and Prevention of Weight Gain",
            "header_text": "Part F. Chapter 5. Cardiometabolic Health and Prevention of Weight Gain",
            "first_pdf_page_index": 316,
            "last_pdf_page_index": 351,
            "first_label": "F5-1",
            "last_label": "F5-36",
        },
        {
            "unit_type": "Part F Chapter",
            "unit_id": "Part F Chapter 6",
            "name": "Part F. Chapter 6. All-cause Mortality, Cardiovascular Mortality, and Cardiovascular Disease",
            "header_text": "Part F. Chapter 6. All-cause Mortality, Cardiovascular Mortality, and Cardiovascular Disease",
            "first_pdf_page_index": 352,
            "last_pdf_page_index": 377,
            "first_label": "F6-1",
            "last_label": "F6-26",
        },
        {
            "unit_type": "Part F Chapter",
            "unit_id": "Part F Chapter 7",
            "name": "Part F. Chapter 7. Youth",
            "header_text": "Part F. Chapter 7. Youth",
            "first_pdf_page_index": 379,
            "last_pdf_page_index": 404,
            "first_label": "F7-1",
            "last_label": "F7-26",
        },
        {
            "unit_type": "Part F Chapter",
            "unit_id": "Part F Chapter 8",
            "name": "Part F. Chapter 8. Women Who Are Pregnant or Postpartum",
            "header_text": "Part F. Chapter 8. Women Who Are Pregnant or Postpartum",
            "first_pdf_page_index": 405,
            "last_pdf_page_index": 438,
            "first_label": "F8-1",
            "last_label": "F8-34",
        },
        {
            "unit_type": "Part F Chapter",
            "unit_id": "Part F Chapter 9",
            "name": "Part F. Chapter 9. Older Adults",
            "header_text": "Part F. Chapter 9. Older Adults",
            "first_pdf_page_index": 439,
            "last_pdf_page_index": 489,
            "first_label": "F9-1",
            "last_label": "F9-51",
        },
        {
            "unit_type": "Part F Chapter",
            "unit_id": "Part F Chapter 10",
            "name": "Part F. Chapter 10. Individuals with Chronic Conditions",
            "header_text": "Part F. Chapter 10. Individuals with Chronic Conditions",
            "first_pdf_page_index": 490,
            "last_pdf_page_index": 606,
            "first_label": "F10-1",
            "last_label": "F10-117",
        },
        {
            "unit_type": "Part F Chapter",
            "unit_id": "Part F Chapter 11",
            "name": "Part F. Chapter 11. Promoting Regular Physical Activity",
            "header_text": "Part F. Chapter 11. Promoting Regular Physical Activity",
            "first_pdf_page_index": 608,
            "last_pdf_page_index": 711,
            "first_label": "F11-1",
            "last_label": "F11-104",
        },
        # Parts G and H
        {
            "unit_type": "Part",
            "unit_id": "Part G",
            "name": "Part G. Needs for Future Research",
            "header_text": "Part G. Needs for Future Research",
            "first_pdf_page_index": 712,
            "last_pdf_page_index": 755,
            "first_label": "G-1",
            "last_label": "G-44",
        },
        {
            "unit_type": "Part",
            "unit_id": "Part H",
            "name": "Part H. Appendices",
            "header_text": "Part H. Appendices",
            "first_pdf_page_index": 756,
            "last_pdf_page_index": 779,
            "first_label": "H1-1",
            "last_label": "H4-3",
        },
    ]

    inventory_results = []
    print(f"{'Unit':<22} | {'Header Text':<45} | {'Pages':<12} | {'Labels':<15} | {'Pgs':<4} | {'Tokens':<8}")
    print("-" * 115)

    for item in inventory_specs:
        sp = item["first_pdf_page_index"]
        ep = item["last_pdf_page_index"]
        page_count = ep - sp + 1
        
        # Extract raw text from these pages
        raw_text_parts = []
        for pno in range(sp, ep + 1):
            page_text = reader.pages[pno - 1].extract_text() or ""
            raw_text_parts.append(page_text)
        full_text = "\n".join(raw_text_parts)
        
        token_count = len(tok.encode(full_text))
        
        record = {
            "unit_type": item["unit_type"],
            "unit_id": item["unit_id"],
            "unit_name": item["name"],
            "header_text": item["header_text"],
            "first_pdf_page_index": sp,
            "last_pdf_page_index": ep,
            "first_label": item["first_label"],
            "last_label": item["last_label"],
            "page_count": page_count,
            "approximate_tokens": token_count,
            "ingested_in_b2": item["unit_id"] in ["Part A", "Part F Chapter 1", "Part F Chapter 3", "Part F Chapter 5", "Part F Chapter 9"]
        }
        inventory_results.append(record)
        print(f"{record['unit_id']:<22} | {record['header_text'][:43]:<45} | pp. {sp:3d}-{ep:3d}   | {record['first_label']} to {record['last_label']:<7} | {page_count:3d}  | {token_count:7d}")

    out_dir = Path("data/staging_phase11_4/audit_outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "pagac_chapter_inventory.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(inventory_results, f, indent=2)
    print(f"\nSaved inventory of {len(inventory_results)} units to {out_path}")

if __name__ == "__main__":
    main()
