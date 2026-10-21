#!/usr/bin/env python3
"""Project NOVA Phase 11.4: Pillar Keyword Evidence Audit (no narrative).

Audits the 10 accepted staging documents from data/staging_phase11/train_staging.json
and data/staging_phase11/val_staging.json.

Hard rules:
- Load documents ONLY from train_staging.json and val_staging.json.
- No directory globbing.
- Fail unless exactly 10 docs load and their source_ids match the 10 accepted ones.
- Take each doc's pillar from its staged record and fail unless it is one of the 7 canonical IDs in PILLAR_DISPLAY_NAMES.
- Define set-to-pillar map in one config:
    strength -> strength_training_programming
    sleep -> sleep_recovery_physical_activity
    nutrition -> nutrition_fundamentals_hydration
    injury -> training_adaptations_fatigue_load
    biomech -> exercise_technique_safety
  Pillars with no set are NOT_TESTABLE.
- Regex sets: strength, interval, sleep, nutrition, injury, biomech.
- Counts occurrences per 1,000 words, with up to 3 verbatim sample lines (with line numbers).
- Outputs structured JSON to data/staging_phase11_4/audit_outputs/pillar_keyword_density.json.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from nova.ingestion import FitnessPillar, PILLAR_DISPLAY_NAMES

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

CANONICAL_PILLAR_IDS = {p.value for p in FitnessPillar}

# A4: Set-to-pillar map defined in one config
SET_TO_PILLAR_MAP: Dict[str, str] = {
    "strength": "strength_training_programming",
    "sleep": "sleep_recovery_physical_activity",
    "nutrition": "nutrition_fundamentals_hydration",
    "injury": "training_adaptations_fatigue_load",
    "biomech": "exercise_technique_safety",
}
PILLAR_TO_SET_MAP: Dict[str, str] = {v: k for k, v in SET_TO_PILLAR_MAP.items()}

# Exact regex sets
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

    if len(combined) != 10:
        raise ValueError(f"Expected exactly 10 staged documents, loaded {len(combined)}")

    loaded_ids = {d["source_id"] for d in combined}
    if loaded_ids != ACCEPTED_SOURCE_IDS:
        missing = ACCEPTED_SOURCE_IDS - loaded_ids
        unexpected = loaded_ids - ACCEPTED_SOURCE_IDS
        raise ValueError(
            f"Staged documents mismatch accepted IDs. Missing: {missing}, Unexpected: {unexpected}"
        )

    # Validate canonical pillar IDs
    for d in combined:
        pillar = d.get("pillar")
        if pillar not in CANONICAL_PILLAR_IDS:
            raise ValueError(
                f"Document {d['source_id']} has invalid non-canonical pillar ID: {pillar}. "
                f"Must be one of {sorted(list(CANONICAL_PILLAR_IDS))}"
            )

    return combined


def audit_document_keywords(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Audit single document for pillar keyword frequencies and verbatim sample lines."""
    source_id = doc["source_id"]
    assigned_pillar = doc["pillar"]
    partition = doc.get("partition", "NOT_COMPUTED")
    raw_text = doc["text"]

    lines = raw_text.splitlines()
    words = raw_text.split()
    word_count = len(words)

    # Determine assigned set key from PILLAR_TO_SET_MAP
    pillar_set_key = PILLAR_TO_SET_MAP.get(assigned_pillar, "NOT_TESTABLE")

    set_results: Dict[str, Any] = {}

    for set_name, pattern in REGEX_SETS.items():
        matches_count = len(pattern.findall(raw_text))
        density = (matches_count / word_count * 1000.0) if word_count > 0 else 0.0

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

    assigned_density: Optional[float] = None
    if pillar_set_key != "NOT_TESTABLE" and pillar_set_key in set_results:
        assigned_density = set_results[pillar_set_key]["density_per_1000_words"]

    other_densities: Dict[str, float] = {}
    for s_name, s_data in set_results.items():
        if s_name != pillar_set_key:
            other_densities[s_name] = s_data["density_per_1000_words"]

    return {
        "source_id": source_id,
        "partition": partition,
        "assigned_pillar": assigned_pillar,
        "pillar_display_name": PILLAR_DISPLAY_NAMES.get(FitnessPillar(assigned_pillar), assigned_pillar),
        "pillar_set_key": pillar_set_key,
        "word_count": word_count,
        "assigned_set_density": assigned_density if assigned_density is not None else "NOT_TESTABLE",
        "other_set_densities": other_densities,
        "all_set_results": set_results,
    }


def run_pillar_keyword_audit(
    staging_dir: Path = REPO_ROOT / "data" / "staging_phase11",
    output_dir: Path = REPO_ROOT / "data" / "staging_phase11_4" / "audit_outputs",
) -> Dict[str, Any]:
    """Execute pillar keyword audit across all 10 accepted documents."""
    documents = load_staged_documents(staging_dir)

    results: Dict[str, Any] = {}
    table_rows: List[Dict[str, Any]] = []

    print("=" * 115)
    print("PHASE 11.4 A4 PILLAR KEYWORD DENSITY MATRIX (10 Real Documents)")
    print("=" * 115)
    print(f"{'source_id':<32} {'assigned_pillar':<35} {'set':<12} {'assigned_d':<12} {'all densities (strength, interval, sleep, nutrition, injury, biomech)'}")
    print("-" * 115)

    for doc in documents:
        doc_res = audit_document_keywords(doc)
        sid = doc_res["source_id"]
        results[sid] = doc_res

        assigned_d_str = (
            f"{doc_res['assigned_set_density']:.2f}"
            if isinstance(doc_res["assigned_set_density"], (int, float))
            else str(doc_res["assigned_set_density"])
        )

        all_d_str = "; ".join(
            f"{k}={v['density_per_1000_words']:.2f}" for k, v in doc_res["all_set_results"].items()
        )

        print(
            f"{sid:<32} "
            f"{doc_res['assigned_pillar']:<35} "
            f"{doc_res['pillar_set_key']:<12} "
            f"{assigned_d_str:<12} "
            f"{all_d_str}"
        )

        table_rows.append(
            {
                "doc": sid,
                "partition": doc_res["partition"],
                "assigned_pillar": doc_res["assigned_pillar"],
                "assigned_set_key": doc_res["pillar_set_key"],
                "assigned_set_density": assigned_d_str,
                "raw_densities": {
                    k: v["density_per_1000_words"]
                    for k, v in doc_res["all_set_results"].items()
                },
            }
        )

    print("=" * 115)

    output_data = {
        "timestamp_utc": "2026-10-21T12:00:00Z",
        "staging_source": str(staging_dir),
        "documents_audited_count": len(documents),
        "set_to_pillar_map": SET_TO_PILLAR_MAP,
        "canonical_pillar_ids": sorted(list(CANONICAL_PILLAR_IDS)),
        "regex_definitions": {k: p.pattern for k, p in REGEX_SETS.items()},
        "table_rows": table_rows,
        "results": results,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / "pillar_keyword_density.json"
    out_file.write_text(json.dumps(output_data, indent=2), encoding="utf-8")
    print(f"Pillar keyword density audit written to {out_file}")
    return output_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit pillar keyword densities.")
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
    run_pillar_keyword_audit(staging_dir=args.staging_dir, output_dir=args.output_dir)
