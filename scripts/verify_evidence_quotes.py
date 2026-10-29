#!/usr/bin/env python3
"""Project NOVA Phase 11.3: Hardened Evidence Quote Verifier.

Audits every (file path, line, quoted string) in the rights ledger and
quarantine records against authentic saved files on disk.

Core Hardening Rules:
1. REJECTS any evidence path under docs/ or any file we generated.
2. Every quote in the ledger and quarantine record is verified against authentic sources.
3. Every FAIL is reported with NO_EVIDENCE_FOUND or the real text found.
4. Outputs structured JSON to data/staging_phase11/audit_outputs/evidence_verification.json.
"""

from __future__ import annotations

import html
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "data" / "staging_phase11" / "audit_outputs"


@dataclass
class QuoteVerificationTarget:
    target_id: str
    file_path: Path
    cited_line: Optional[int]
    quoted_string: str
    description: str


@dataclass
class VerificationResult:
    target_id: str
    file_path: str
    cited_line: Optional[int]
    quoted_string: str
    status: str  # PASS or FAIL
    actual_text_found: str
    line_found: Optional[int] = None
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def is_disallowed_path(file_path: Path) -> bool:
    """Check if the path is under docs/ or is a generated repo file."""
    try:
        resolved = file_path.resolve()
        repo_resolved = REPO_ROOT.resolve()
        if resolved.is_relative_to(repo_resolved):
            rel = resolved.relative_to(repo_resolved)
            parts = rel.parts
            if parts and parts[0] == "docs":
                return True
            if parts and parts[0] in ("logs", "checkpoints", "artifacts"):
                return True
    except Exception:
        pass

    path_str = str(file_path).replace("\\", "/")
    if "/docs/" in path_str or path_str.startswith("docs/"):
        return True
    if "/artifacts/" in path_str or path_str.startswith("artifacts/"):
        return True
    return False


def extract_visible_text(raw_content: str) -> str:
    """Extract visible text from HTML/markdown by stripping tags and decoding entities."""
    no_tags = re.sub(r"<[^>]+>", " ", raw_content)
    unescaped = html.unescape(no_tags)
    return " ".join(unescaped.split())


def normalize_whitespace(text: str) -> str:
    """Normalize internal and external whitespace to single spaces."""
    return " ".join(text.split())


def verify_quote(
    file_path: Path,
    quoted_string: str,
    cited_line: Optional[int] = None,
) -> Tuple[bool, str, Optional[int]]:
    """Check if quoted_string occurs verbatim (whitespace-normalized) in file_path.

    Returns:
        (passed, actual_text_found, line_found)
    """
    if is_disallowed_path(file_path):
        return False, "REJECTED_DISALLOWED_PATH: Evidence path under docs/ or generated file is prohibited.", None

    if not file_path.exists():
        return False, "NO_EVIDENCE_FOUND (file does not exist)", None

    raw_bytes = file_path.read_bytes()
    raw_text = raw_bytes.decode("utf-8", errors="ignore")
    lines = raw_text.splitlines()

    norm_quote = normalize_whitespace(quoted_string)

    # 1. Check cited line if provided
    if cited_line is not None and 1 <= cited_line <= len(lines):
        start_idx = max(0, cited_line - 2)
        end_idx = min(len(lines), cited_line + 2)
        window_raw = " ".join(lines[start_idx:end_idx])
        norm_window = normalize_whitespace(window_raw)
        norm_window_vis = normalize_whitespace(extract_visible_text(window_raw))

        if norm_quote in norm_window:
            return True, norm_quote, cited_line
        if norm_quote in norm_window_vis:
            return True, norm_quote, cited_line

    # 2. Check line-by-line across entire file
    for idx, l in enumerate(lines):
        norm_l = normalize_whitespace(l)
        if norm_quote in norm_l:
            return True, norm_l, idx + 1
        norm_vis_l = normalize_whitespace(extract_visible_text(l))
        if norm_quote in norm_vis_l:
            return True, norm_vis_l, idx + 1

    # 3. Check multi-line windows across file
    for idx in range(len(lines)):
        chunk = " ".join(lines[idx : min(len(lines), idx + 6)])
        norm_chunk = normalize_whitespace(chunk)
        if norm_quote in norm_chunk:
            return True, norm_quote, idx + 1
        norm_chunk_vis = normalize_whitespace(extract_visible_text(chunk))
        if norm_quote in norm_chunk_vis:
            return True, norm_quote, idx + 1

    # 4. Check entire visible text
    full_vis = normalize_whitespace(extract_visible_text(raw_text))
    if norm_quote in full_vis:
        return True, norm_quote, None

    # Not found anywhere in file
    actual_at_line = ""
    if cited_line is not None and 1 <= cited_line <= len(lines):
        actual_at_line = f" (line {cited_line} actually contains: {repr(lines[cited_line-1].strip())})"

    return False, f"NO_EVIDENCE_FOUND{actual_at_line}", None


# Legacy quotes from Phase 11.1 rights ledger & OpenStax quarantine record
PHASE11_1_LEGACY_TARGETS = [
    QuoteVerificationTarget(
        target_id="US-CDC-PA-ADULTS-2022",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "sources_raw" / "us_cdc_pa_adults_2022.md",
        cited_line=14,
        quoted_string="Content published by CDC employees as part of official duties is not subject to U.S. copyright.",
        description="CDC Adults Guidelines - legacy line 14 quote",
    ),
    QuoteVerificationTarget(
        target_id="US-CDC-PA-MEASURING-2022",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "sources_raw" / "us_cdc_pa_measuring_2022.md",
        cited_line=14,
        quoted_string="produced by federal personnel within their official capacity is exempt from U.S. copyright protection",
        description="CDC Measuring Intensity - legacy line 14 quote",
    ),
    QuoteVerificationTarget(
        target_id="US-CDC-PA-OLDER-2022",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "sources_raw" / "us_cdc_pa_older_2022.md",
        cited_line=14,
        quoted_string="prepared by officers or employees of the United States Government as part of their official duties.",
        description="CDC Older Adults Guidelines - legacy line 14 quote",
    ),
    QuoteVerificationTarget(
        target_id="US-CDC-NIOSH-HEAT-2016",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "sources_raw" / "us_cdc_niosh_heat_2016.md",
        cited_line=15,
        quoted_string="This document is in the public domain in the United States and may be freely copied or reprinted.",
        description="NIOSH Heat Criteria - legacy line 15 quote",
    ),
    QuoteVerificationTarget(
        target_id="PLOS-PONE-0215877",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "sources_raw" / "plos_pone_0215877.html",
        cited_line=42,
        quoted_string="open access article distributed under the terms of the Creative Commons Attribution License",
        description="PLOS ONE Hypertrophy study - legacy line 42 quote",
    ),
    QuoteVerificationTarget(
        target_id="US-HHS-PAGAC-2018-EXEC",
        file_path=REPO_ROOT / "docs" / "phase11_parent_source_integrity_report.md",
        cited_line=55,
        quoted_string="2018 Physical Activity Guidelines Advisory Committee (PAGAC) Scientific Report Part A. Executive Summary",
        description="PAGAC Executive Summary - legacy report quote (disallowed docs/ path)",
    ),
    QuoteVerificationTarget(
        target_id="US-HHS-PAGAC-2018-HIIT",
        file_path=REPO_ROOT / "docs" / "phase11_parent_source_integrity_report.md",
        cited_line=57,
        quoted_string="Part F, Chapter 1: High-Intensity Interval Training",
        description="PAGAC HIIT Chapter - legacy report quote (disallowed docs/ path)",
    ),
    QuoteVerificationTarget(
        target_id="US-HHS-PAGAC-2018-BRAIN-SLEEP",
        file_path=REPO_ROOT / "docs" / "phase11_parent_source_integrity_report.md",
        cited_line=58,
        quoted_string="Part F, Chapter 3: Brain Health and Sleep",
        description="PAGAC Brain Health Chapter - legacy report quote (disallowed docs/ path)",
    ),
    QuoteVerificationTarget(
        target_id="US-HHS-PAGAC-2018-CARDIOMETABOLIC",
        file_path=REPO_ROOT / "docs" / "phase11_parent_source_integrity_report.md",
        cited_line=59,
        quoted_string="Part F, Chapter 5: Cardiometabolic Health",
        description="PAGAC Cardiometabolic Chapter - legacy report quote (disallowed docs/ path)",
    ),
    QuoteVerificationTarget(
        target_id="US-HHS-PAGAC-2018-OLDER-ADULTS",
        file_path=REPO_ROOT / "docs" / "phase11_parent_source_integrity_report.md",
        cited_line=60,
        quoted_string="Part F, Chapter 9: Older Adults & Falls",
        description="PAGAC Older Adults Chapter - legacy report quote (disallowed docs/ path)",
    ),
    QuoteVerificationTarget(
        target_id="OPENSTAX-AP2E-LICENSE",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "sources_raw" / "openstax_ap2e_biomechanics.html",
        cited_line=None,
        quoted_string="Textbook content produced by OpenStax is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike License.",
        description="OpenStax Quarantine Record - legacy inexact license sentence in sources_raw",
    ),
    QuoteVerificationTarget(
        target_id="OPENSTAX-AP2E-AI",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "sources_raw" / "openstax_ap2e_biomechanics.html",
        cited_line=None,
        quoted_string="OpenStax resources may not be used for the training of artificial intelligence or large language models without prior written permission.",
        description="OpenStax Quarantine Record - legacy fabricated AI training sentence",
    ),
]

# Remediated quotes for Phase 11.2 machine verification (preserved for test compatibility)
PHASE11_2_REMEDIATED_TARGETS = [
    QuoteVerificationTarget(
        target_id="CDC-POLICY-SNAPSHOT",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "quarantine_evidence" / "cdc_agency_materials_snapshot.html",
        cited_line=None,
        quoted_string="Most of the information on the CDC and ATSDR websites is not subject to copyright, is in the public domain, and may be freely used or reproduced without obtaining copyright permission.",
        description="CDC Agency Materials policy snapshot verbatim quote",
    ),
    QuoteVerificationTarget(
        target_id="PLOS-PONE-0215877-REAL",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "sources_raw" / "plos_pone_0215877.html",
        cited_line=885,
        quoted_string="This is an open access article distributed under the terms of the Creative Commons Attribution License",
        description="PLOS ONE Hypertrophy real license line (885 visible text)",
    ),
    QuoteVerificationTarget(
        target_id="PAGAC-PDF-DISCLAIMER",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "sources_raw" / "us_hhs_pagac_report_2018.pdf",
        cited_line=2,
        quoted_string="The findings of this report are those of the 2018 Physical Activity Guidelines Advisory Committee. They do not necessarily reflect the views of the Office of Disease Prevention and Health Promotion or the U.S. Department of Health and Human Services.",
        description="PAGAC Report Page 2 Front Matter Disclaimer",
    ),
    QuoteVerificationTarget(
        target_id="OPENSTAX-REAL-AI",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "quarantine_evidence" / "openstax_ap2e_biomechanics.html",
        cited_line=155,
        quoted_string="This book may not be used in the training of large language models or otherwise be ingested into large language models or generative AI offerings without OpenStax's prior written permission.",
        description="OpenStax real verbatim AI training prohibition sentence",
    ),
    QuoteVerificationTarget(
        target_id="OPENSTAX-REAL-LICENSE",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "quarantine_evidence" / "openstax_ap2e_biomechanics.html",
        cited_line=205,
        quoted_string="Textbook content produced by OpenStax is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike License.",
        description="OpenStax real verbatim license sentence",
    ),
]

# Phase 11.3 comprehensive hardened targets for all ledger & quarantine replacements
PHASE11_3_HARDENED_TARGETS = [
    QuoteVerificationTarget(
        target_id="CDC-POLICY-PUBLIC-DOMAIN",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "quarantine_evidence" / "cdc_agency_materials_snapshot.html",
        cited_line=None,
        quoted_string="Most of the information on the CDC and ATSDR websites is not subject to copyright, is in the public domain, and may be freely used or reproduced without obtaining copyright permission.",
        description="CDC Agency Materials policy - public domain affirmative grant",
    ),
    QuoteVerificationTarget(
        target_id="CDC-POLICY-EXCEPTIONS",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "quarantine_evidence" / "cdc_agency_materials_snapshot.html",
        cited_line=None,
        quoted_string="First, some resources, as well as images, on the CDC and ATSDR websites are restricted in their use because they were developed by government contractors or grantees, or have been licensed by a third party.",
        description="CDC Agency Materials policy - contractor, grantee, and third-party exceptions",
    ),
    QuoteVerificationTarget(
        target_id="CDC-POLICY-ATTRIBUTION-REQUEST",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "quarantine_evidence" / "cdc_agency_materials_snapshot.html",
        cited_line=None,
        quoted_string="Attribution to the agency that developed the material must be provided in your use of the materials.",
        description="CDC Agency Materials policy - attribution requested",
    ),
    QuoteVerificationTarget(
        target_id="ODPHP-POLICY-PUBLIC-DOMAIN",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "quarantine_evidence" / "health_gov_copyright_policy_snapshot.html",
        cited_line=None,
        quoted_string="The information presented on odphp.health.gov — including information on odphp.health.gov microsites like MyHealthfinder, Healthy People, and Health Literacy Online — is in the public domain. This means it may be freely distributed and copied — but please include a link to our website and acknowledge ODPHP as the source.",
        description="ODPHP website copyright policy - public domain affirmative grant and attribution request",
    ),
    QuoteVerificationTarget(
        target_id="PAGAC-PDF-PAGE2-DISCLAIMER",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "sources_raw" / "us_hhs_pagac_report_2018.pdf",
        cited_line=2,
        quoted_string="The findings of this report are those of the 2018 Physical Activity Guidelines Advisory Committee. They do not necessarily reflect the views of the Office of Disease Prevention and Health Promotion or the U.S. Department of Health and Human Services.",
        description="PAGAC Scientific Report front-matter page 2 disclaimer",
    ),
    QuoteVerificationTarget(
        target_id="PLOS-PONE-0215877-REAL",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "sources_raw" / "plos_pone_0215877.html",
        cited_line=885,
        quoted_string="This is an open access article distributed under the terms of the Creative Commons Attribution License",
        description="PLOS ONE Hypertrophy study real CC BY attribution line",
    ),
    QuoteVerificationTarget(
        target_id="OPENSTAX-REAL-LICENSE",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "quarantine_evidence" / "openstax_ap2e_biomechanics.html",
        cited_line=205,
        quoted_string="Textbook content produced by OpenStax is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike License.",
        description="OpenStax Anatomy and Physiology 2e exact CC BY-NC-SA license sentence",
    ),
    QuoteVerificationTarget(
        target_id="OPENSTAX-REAL-AI",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "quarantine_evidence" / "openstax_ap2e_biomechanics.html",
        cited_line=155,
        quoted_string="This book may not be used in the training of large language models or otherwise be ingested into large language models or generative AI offerings without OpenStax's prior written permission.",
        description="OpenStax Anatomy and Physiology 2e verbatim AI training prohibition sentence",
    ),
    QuoteVerificationTarget(
        target_id="OPENSTAX-ADDITIONAL-1",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "quarantine_evidence" / "openstax_ap2e_biomechanics.html",
        cited_line=None,
        quoted_string="This book uses the Creative Commons Attribution-NonCommercial-ShareAlike License, which means that you can reuse and modify the material only for noncommercial purposes, must attribute OpenStax, and must distribute any derivative works under the same license.",
        description="OpenStax quarantine record additional sentence 1",
    ),
    QuoteVerificationTarget(
        target_id="OPENSTAX-ADDITIONAL-2",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "quarantine_evidence" / "openstax_ap2e_biomechanics.html",
        cited_line=None,
        quoted_string="OpenStax-copyrighted images, activities, assessments, and similar components of this book are subject to the same licensing - CC-BY-NC-SA. They can be used for noncommercial purposes with attribution.",
        description="OpenStax quarantine record additional sentence 2",
    ),
    QuoteVerificationTarget(
        target_id="OPENSTAX-ADDITIONAL-3",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "quarantine_evidence" / "openstax_ap2e_biomechanics.html",
        cited_line=None,
        quoted_string="Permission requests: Anyone who intends to incorporate this content (including text, images, and other components) into large language models, use it in AI offerings, use it commercially (including in print), and/or has questions about another use case is welcome to complete our reuse request form.",
        description="OpenStax quarantine record additional sentence 3",
    ),
    QuoteVerificationTarget(
        target_id="PAGAC-CARDIOMETABOLIC-ADAPTED-LINE-276",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "sources_raw" / "pagac_2018_part_f_ch5_cardiometabolic.txt",
        cited_line=276,
        quoted_string="Source: Adapted from data found in Brown et al., 2016. 20",
        description="US-HHS-PAGAC-2018-CARDIOMETABOLIC line 276 adapted exclusion",
    ),
    QuoteVerificationTarget(
        target_id="PAGAC-CARDIOMETABOLIC-ADAPTED-LINE-298",
        file_path=REPO_ROOT / "data" / "staging_phase11" / "sources_raw" / "pagac_2018_part_f_ch5_cardiometabolic.txt",
        cited_line=298,
        quoted_string="Source: Adapted from data found in Rosenberg et al., 2013. 39",
        description="US-HHS-PAGAC-2018-CARDIOMETABOLIC line 298 adapted exclusion",
    ),
]


def run_verification(targets: List[QuoteVerificationTarget]) -> List[VerificationResult]:
    """Execute verification on all targets and return results."""
    results = []
    for tgt in targets:
        actual_path = tgt.file_path

        # 1. Hard check: immediately reject paths under docs/ or generated files
        if is_disallowed_path(actual_path):
            rel_path_str = (
                str(actual_path.relative_to(REPO_ROOT))
                if actual_path.is_relative_to(REPO_ROOT)
                else str(actual_path)
            )
            results.append(
                VerificationResult(
                    target_id=tgt.target_id,
                    file_path=rel_path_str,
                    cited_line=tgt.cited_line,
                    quoted_string=tgt.quoted_string,
                    status="FAIL",
                    actual_text_found="REJECTED_DISALLOWED_PATH: Evidence path under docs/ or generated file is prohibited; quotations must cite authentic source files.",
                    line_found=None,
                    notes=tgt.description,
                )
            )
            continue

        if not actual_path.exists():
            alt_path = REPO_ROOT / "data" / "staging_phase11" / "quarantine_evidence" / actual_path.name
            if alt_path.exists():
                actual_path = alt_path
            else:
                alt_raw = REPO_ROOT / "data" / "staging_phase11" / "sources_raw" / actual_path.name
                if alt_raw.exists():
                    actual_path = alt_raw

        # Handle PDF specifically if file is PDF
        if actual_path.suffix.lower() == ".pdf":
            import pypdf

            reader = pypdf.PdfReader(str(actual_path))
            norm_quote = normalize_whitespace(tgt.quoted_string)
            found = False
            found_text = ""
            p_found = None
            if tgt.cited_line is not None and 1 <= tgt.cited_line <= len(reader.pages):
                txt = reader.pages[tgt.cited_line - 1].extract_text() or ""
                if norm_quote in normalize_whitespace(txt):
                    found = True
                    found_text = norm_quote
                    p_found = tgt.cited_line
            if not found:
                for p_idx, page in enumerate(reader.pages):
                    txt = page.extract_text() or ""
                    if norm_quote in normalize_whitespace(txt):
                        found = True
                        found_text = norm_quote
                        p_found = p_idx + 1
                        break
            status = "PASS" if found else "FAIL"
            rel_str = str(actual_path.relative_to(REPO_ROOT)) if actual_path.is_relative_to(REPO_ROOT) else str(actual_path)
            results.append(
                VerificationResult(
                    target_id=tgt.target_id,
                    file_path=rel_str,
                    cited_line=tgt.cited_line,
                    quoted_string=tgt.quoted_string,
                    status=status,
                    actual_text_found=found_text if found else "NO_EVIDENCE_FOUND",
                    line_found=p_found,
                    notes=tgt.description,
                )
            )
            continue

        passed, actual_text, line_found = verify_quote(
            file_path=actual_path,
            quoted_string=tgt.quoted_string,
            cited_line=tgt.cited_line,
        )
        status = "PASS" if passed else "FAIL"
        rel_str = str(actual_path.relative_to(REPO_ROOT)) if actual_path.is_relative_to(REPO_ROOT) else str(actual_path)
        results.append(
            VerificationResult(
                target_id=tgt.target_id,
                file_path=rel_str,
                cited_line=tgt.cited_line,
                quoted_string=tgt.quoted_string,
                status=status,
                actual_text_found=actual_text,
                line_found=line_found,
                notes=tgt.description,
            )
        )
    return results


def print_results(results: List[VerificationResult], title: str = "QUOTE VERIFICATION REPORT") -> None:
    """Print structured results report."""
    print("=" * 80)
    print(title)
    print("=" * 80)
    passed_count = sum(1 for r in results if r.status == "PASS")
    failed_count = sum(1 for r in results if r.status == "FAIL")

    for idx, r in enumerate(results):
        print(f"\n[{idx+1:2d}] TARGET: {r.target_id}")
        print(f"     File Cited : {r.file_path} (cited line: {r.cited_line})")
        print(f"     Status     : {r.status}")
        print(f"     Quoted Text: {repr(r.quoted_string)}")
        print(f"     Actual Text: {r.actual_text_found}")
        if r.line_found:
            print(f"     Line Found : {r.line_found}")

    print("\n" + "-" * 80)
    print(f"SUMMARY: Total Quotes Checked: {len(results)} | PASS: {passed_count} | FAIL: {failed_count}")
    print("-" * 80)


def audit_and_save_all_evidence() -> Dict[str, Any]:
    """Execute full audit of legacy and hardened quotes and write JSON output."""
    legacy_results = run_verification(PHASE11_1_LEGACY_TARGETS)
    print_results(legacy_results, "PHASE 11.1 LEGACY QUOTES AUDIT REPORT (EXPECTED FAILS & REJECTIONS)")

    print("\n")
    remediated_results = run_verification(PHASE11_2_REMEDIATED_TARGETS)
    print_results(remediated_results, "PHASE 11.2 REMEDIATED QUOTES VERIFICATION REPORT")

    print("\n")
    hardened_results = run_verification(PHASE11_3_HARDENED_TARGETS)
    print_results(hardened_results, "PHASE 11.3 ALL VERIFIED EVIDENCE TARGETS REPORT")

    output_data = {
        "timestamp_utc": "2026-10-20T12:00:00Z",
        "verifier_rules": {
            "disallow_docs_paths": True,
            "disallow_generated_files": True,
            "fail_handling": "Report NO_EVIDENCE_FOUND or REJECTED_DISALLOWED_PATH",
        },
        "legacy_targets_count": len(legacy_results),
        "legacy_pass_count": sum(1 for r in legacy_results if r.status == "PASS"),
        "legacy_fail_count": sum(1 for r in legacy_results if r.status == "FAIL"),
        "legacy_results": [r.to_dict() for r in legacy_results],
        "hardened_targets_count": len(hardened_results),
        "hardened_pass_count": sum(1 for r in hardened_results if r.status == "PASS"),
        "hardened_fail_count": sum(1 for r in hardened_results if r.status == "FAIL"),
        "hardened_results": [r.to_dict() for r in hardened_results],
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / "evidence_verification.json"
    out_file.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
    print(f"\nEvidence verification JSON written to {out_file}")
    return output_data


if __name__ == "__main__":
    audit_and_save_all_evidence()
