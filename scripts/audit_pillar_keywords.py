#!/usr/bin/env python3
"""Project NOVA Phase 11.3: Pillar Keyword Evidence Audit (no narrative).

For each accepted document, counts occurrences per 1,000 words, with 3 verbatim sample
lines (with line numbers) per set, for these regex sets:
- strength: resistance training|muscle-strengthening|strength training|repetition|hypertrophy
- interval: high-intensity interval|HIIT|interval
- sleep: sleep
- nutrition: diet|dietary|energy intake|calorie|nutrition|hydration|fluid
- injury: injur|fall|adverse event
- biomech: biomechanic|joint|torque|moment arm|kinematic

Outputs structured JSON to data/staging_phase11/audit_outputs/pillar_keyword_density.json.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "data" / "staging_phase11" / "sources_raw"
OUTPUT_DIR = REPO_ROOT / "data" / "staging_phase11" / "audit_outputs"

DOCUMENTS = [
    {
        "source_id": "US-CDC-PA-ADULTS-2022",
        "file_name": "us_cdc_pa_adults_2022.md",
        "assigned_pillar": "exercise_physiology",
        "pillar_set_key": "biomech",  # exercise_science_biomechanics
    },
    {
        "source_id": "US-CDC-PA-MEASURING-2022",
        "file_name": "us_cdc_pa_measuring_2022.md",
        "assigned_pillar": "exercise_physiology",
        "pillar_set_key": "biomech",
    },
    {
        "source_id": "US-CDC-PA-OLDER-2022",
        "file_name": "us_cdc_pa_older_2022.md",
        "assigned_pillar": "injury_prevention",
        "pillar_set_key": "injury",
    },
    {
        "source_id": "US-CDC-NIOSH-HEAT-2016",
        "file_name": "us_cdc_niosh_heat_2016.md",
        "assigned_pillar": "nutrition_hydration",
        "pillar_set_key": "nutrition",
    },
    {
        "source_id": "PLOS-PONE-0215877",
        "file_name": "plos_pone_0215877.html",
        "assigned_pillar": "strength_training",
        "pillar_set_key": "strength",
    },
    {
        "source_id": "US-HHS-PAGAC-2018-EXEC",
        "file_name": "pagac_2018_part_a_executive_summary.txt",
        "assigned_pillar": "fitness_education",
        "pillar_set_key": None,  # General education (no dedicated keyword set)
    },
    {
        "source_id": "US-HHS-PAGAC-2018-HIIT",
        "file_name": "pagac_2018_part_f_ch1_bouts_hiit.txt",
        "assigned_pillar": "strength_training",
        "pillar_set_key": "strength",
    },
    {
        "source_id": "US-HHS-PAGAC-2018-BRAIN-SLEEP",
        "file_name": "pagac_2018_part_f_ch3_brain_sleep.txt",
        "assigned_pillar": "recovery_sleep",
        "pillar_set_key": "sleep",
    },
    {
        "source_id": "US-HHS-PAGAC-2018-CARDIOMETABOLIC",
        "file_name": "pagac_2018_part_f_ch5_cardiometabolic.txt",
        "assigned_pillar": "nutrition_hydration",
        "pillar_set_key": "nutrition",
    },
    {
        "source_id": "US-HHS-PAGAC-2018-OLDER-ADULTS",
        "file_name": "pagac_2018_part_f_ch9_older_adults.txt",
        "assigned_pillar": "injury_prevention",
        "pillar_set_key": "injury",
    },
]

REGEX_SETS: Dict[str, re.Pattern] = {
    "strength": re.compile(
        r"resistance training|muscle-strengthening|strength training|repetition|hypertrophy",
        re.IGNORECASE,
    ),
    "interval": re.compile(
        r"high-intensity interval|HIIT|interval",
        re.IGNORECASE,
    ),
    "sleep": re.compile(
        r"sleep",
        re.IGNORECASE,
    ),
    "nutrition": re.compile(
        r"diet|dietary|energy intake|calorie|nutrition|hydration|fluid",
        re.IGNORECASE,
    ),
    "injury": re.compile(
        r"injur|fall|adverse event",
        re.IGNORECASE,
    ),
    "biomech": re.compile(
        r"biomechanic|joint|torque|moment arm|kinematic",
        re.IGNORECASE,
    ),
}


def audit_document_keywords(doc_info: Dict[str, Any]) -> Dict[str, Any]:
    """Audit single document for pillar keyword frequencies and verbatim sample lines."""
    source_id = doc_info["source_id"]
    file_name = doc_info["file_name"]
    doc_path = RAW_DIR / file_name

    if not doc_path.exists():
        return {
            "source_id": source_id,
            "status": "NOT_COMPUTED",
            "reason": f"File not found: {doc_path}",
        }

    raw_text = doc_path.read_text(encoding="utf-8", errors="ignore")
    lines = raw_text.splitlines()
    words = raw_text.split()
    word_count = len(words)

    set_results: Dict[str, Any] = {}

    for set_name, pattern in REGEX_SETS.items():
        matches_count = len(pattern.findall(raw_text))
        density = (matches_count / word_count * 1000.0) if word_count > 0 else 0.0

        # Find matching lines with line numbers
        sample_lines = []
        for line_idx, line_text in enumerate(lines):
            if pattern.search(line_text):
                sample_lines.append(
                    {
                        "line_number": line_idx + 1,
                        "verbatim_line": line_text.strip()[:140],
                    }
                )
                if len(sample_lines) >= 3:
                    break

        set_results[set_name] = {
            "match_count": matches_count,
            "density_per_1000_words": round(density, 2),
            "sample_lines": sample_lines,
        }

    assigned_pillar = doc_info["assigned_pillar"]
    pillar_set_key = doc_info["pillar_set_key"]

    assigned_density: Optional[float] = None
    if pillar_set_key and pillar_set_key in set_results:
        assigned_density = set_results[pillar_set_key]["density_per_1000_words"]

    other_densities: Dict[str, float] = {}
    for s_name, s_data in set_results.items():
        if s_name != pillar_set_key:
            other_densities[s_name] = s_data["density_per_1000_words"]

    return {
        "source_id": source_id,
        "file_name": file_name,
        "assigned_pillar": assigned_pillar,
        "pillar_set_key": pillar_set_key,
        "word_count": word_count,
        "assigned_set_density": assigned_density,
        "other_set_densities": other_densities,
        "all_set_results": set_results,
    }


def audit_all_pillar_keywords() -> Dict[str, Any]:
    """Audit all 10 accepted documents for pillar keyword evidence."""
    results: Dict[str, Any] = {}
    table_rows: List[Dict[str, Any]] = []

    for doc in DOCUMENTS:
        sid = doc["source_id"]
        doc_res = audit_document_keywords(doc)
        results[sid] = doc_res

        # Format row for summary table
        assigned_d_str = (
            f"{doc_res['assigned_set_density']:.2f}"
            if doc_res["assigned_set_density"] is not None
            else "N/A"
        )
        other_str = "; ".join(
            f"{k}={v:.2f}" for k, v in doc_res["other_set_densities"].items()
        )
        table_rows.append(
            {
                "doc": sid,
                "assigned_pillar": doc["assigned_pillar"],
                "assigned_set_key": doc["pillar_set_key"] or "none",
                "assigned_set_density": assigned_d_str,
                "other_set_densities": other_str,
                "raw_densities": {
                    k: v["density_per_1000_words"]
                    for k, v in doc_res["all_set_results"].items()
                },
            }
        )

    output_data = {
        "timestamp_utc": "2026-10-20T12:00:00Z",
        "documents_audited_count": len(DOCUMENTS),
        "regex_definitions": {
            "strength": "resistance training|muscle-strengthening|strength training|repetition|hypertrophy",
            "interval": "high-intensity interval|HIIT|interval",
            "sleep": "sleep",
            "nutrition": "diet|dietary|energy intake|calorie|nutrition|hydration|fluid",
            "injury": "injur|fall|adverse event",
            "biomech": "biomechanic|joint|torque|moment arm|kinematic",
        },
        "table_rows": table_rows,
        "results": results,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / "pillar_keyword_density.json"
    out_file.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
    print(f"Pillar keyword density audit written to {out_file}")
    return output_data


if __name__ == "__main__":
    audit_all_pillar_keywords()
