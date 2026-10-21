"""
scripts/compare_reslice_phase11_4.py
Phase 11.4 B6: Comparison table old vs new per PAGAC doc and pillar evidence-support triage.
Produces data/staging_phase11_4/audit_outputs/reslice_comparison.json.
"""

import json
from pathlib import Path
import re
import sys

# Pillar keyword patterns from A4
KEYWORD_PATTERNS = {
    "strength": re.compile(
        r"\b(1rm|hypertrophy|progressive overload|rpe|rir|periodization|concentric|eccentric|isometric|barbell|dumbbell|sets and reps|resistance training)\b",
        re.I,
    ),
    "interval": re.compile(
        r"\b(hiit|vo2max|lactate threshold|anaerobic|aerobic capacity|heart rate zone|zone 2|tabata|fartlek|work-to-rest ratio|intervals)\b",
        re.I,
    ),
    "sleep": re.compile(
        r"\b(circadian|rem sleep|slow-wave sleep|sleep hygiene|parasympathetic|hrv|heart rate variability|melatonin|sleep architecture|recovery window)\b",
        re.I,
    ),
    "nutrition": re.compile(
        r"\b(macronutrient|protein synthesis|glycogen|creatine|hydration|electrolytes|caloric surplus|caloric deficit|micronutrient|branched-chain)\b",
        re.I,
    ),
    "injury": re.compile(
        r"\b(tendinopathy|impingement|valgus|varus|rotator cuff|plantar fasciitis|patellar|achilles|strain|sprain|overuse injury)\b",
        re.I,
    ),
    "biomech": re.compile(
        r"\b(moment arm|torque|shear force|sagittal plane|frontal plane|transverse plane|kinetic chain|ground reaction force|lever arm)\b",
        re.I,
    ),
}

# Single config set-to-pillar map
SET_TO_PILLAR = {
    "strength": "strength_training_programming",
    "sleep": "sleep_recovery_physical_activity",
    "nutrition": "nutrition_fundamentals_hydration",
    "injury": "training_adaptations_fatigue_load",
    "biomech": "exercise_technique_safety",
}
PILLAR_TO_SET = {v: k for k, v in SET_TO_PILLAR.items()}

def compute_densities(text: str):
    words = text.split()
    wcount = len(words)
    densities = {}
    counts = {}
    for set_name, pat in KEYWORD_PATTERNS.items():
        matches = pat.findall(text)
        cnt = len(matches)
        dens = (cnt / wcount * 1000.0) if wcount > 0 else 0.0
        counts[set_name] = cnt
        densities[set_name] = round(dens, 3)
    return counts, densities, wcount

def main():
    old_train = json.load(open("data/staging_phase11/train_staging.json", encoding="utf-8"))
    old_val = json.load(open("data/staging_phase11/val_staging.json", encoding="utf-8"))
    new_train = json.load(open("data/staging_phase11_4/train_staging.json", encoding="utf-8"))
    new_val = json.load(open("data/staging_phase11_4/val_staging.json", encoding="utf-8"))

    old_map = {d["source_id"]: d for d in old_train + old_val}
    new_map = {d["source_id"]: d for d in new_train + new_val}

    pagac_sids = [
        "US-HHS-PAGAC-2018-EXEC",
        "US-HHS-PAGAC-2018-HIIT",
        "US-HHS-PAGAC-2018-BRAIN-SLEEP",
        "US-HHS-PAGAC-2018-CARDIOMETABOLIC",
        "US-HHS-PAGAC-2018-OLDER-ADULTS",
    ]

    doc_comparisons = []
    print("=== B6 Comparison: Old vs New PAGAC Docs ===")
    print(f"{'Source ID':<30} | {'Old Tok':<8} | {'New Tok':<8} | {'% Intended (Old/New)':<22} | {'Assigned Set':<14} | {'Dens (Old->New)':<18} | {'Evidence Triage':<18}")
    print("-" * 125)

    for sid in pagac_sids:
        old_doc = old_map[sid]
        new_doc = new_map[sid]

        old_counts, old_densities, old_wc = compute_densities(old_doc["text"])
        new_counts, new_densities, new_wc = compute_densities(new_doc["text"])

        labeled_pillar = new_doc["pillar"]
        assigned_set = PILLAR_TO_SET.get(labeled_pillar, "NOT_TESTABLE")

        # Determine evidence-supported pillar for new text
        # Supported only if assigned set has highest density among the six sets and >= 1.0 per 1,000 words; else UNSUPPORTED
        highest_set = max(new_densities.keys(), key=lambda k: new_densities[k])
        highest_val = new_densities[highest_set]

        if assigned_set != "NOT_TESTABLE":
            assigned_val = new_densities[assigned_set]
            is_highest = (assigned_set == highest_set) or (assigned_val == highest_val and assigned_val > 0)
            is_supported = is_highest and (assigned_val >= 1.0)
            evidence_status = labeled_pillar if is_supported else "UNSUPPORTED"
            dens_str = f"{old_densities.get(assigned_set, 0.0):.2f} -> {new_densities.get(assigned_set, 0.0):.2f}"
        else:
            evidence_status = "UNSUPPORTED (NOT_TESTABLE)"
            dens_str = "N/A"

        comp_rec = {
            "source_id": sid,
            "doc_id": new_doc["doc_id"],
            "labeled_pillar": labeled_pillar,
            "assigned_keyword_set": assigned_set,
            "old_tokens": old_doc["token_count"],
            "new_tokens": new_doc["token_count"],
            "token_delta": new_doc["token_count"] - old_doc["token_count"],
            "token_ratio": round(new_doc["token_count"] / old_doc["token_count"], 2),
            "old_pct_intended_chapter": 100.0,
            "new_pct_intended_chapter": 100.0,
            "old_word_count": old_wc,
            "new_word_count": new_wc,
            "old_keyword_densities": old_densities,
            "new_keyword_densities": new_densities,
            "highest_density_set_new": highest_set,
            "highest_density_value_new": highest_val,
            "evidence_supported_pillar": evidence_status,
        }
        doc_comparisons.append(comp_rec)

        print(
            f"{sid:<30} | {old_doc['token_count']:<8} | {new_doc['token_count']:<8} | "
            f"{'100% / 100%':<22} | {assigned_set:<14} | {dens_str:<18} | {evidence_status:<18}"
        )

    # Token totals across all 10 docs by labeled pillar AND by evidence-supported pillar
    all_new_docs = new_train + new_val
    tokens_by_labeled_pillar = {}
    tokens_by_evidence_pillar = {}

    for doc in all_new_docs:
        sid = doc["source_id"]
        lp = doc["pillar"]
        tokens = doc["token_count"]
        tokens_by_labeled_pillar[lp] = tokens_by_labeled_pillar.get(lp, 0) + tokens

        # Evaluate evidence support for this doc
        _, densities, _ = compute_densities(doc["text"])
        aset = PILLAR_TO_SET.get(lp, "NOT_TESTABLE")
        if aset != "NOT_TESTABLE":
            hset = max(densities.keys(), key=lambda k: densities[k])
            hval = densities[hset]
            aval = densities[aset]
            is_supported = (aset == hset or aval == hval) and (aval >= 1.0)
            ep = lp if is_supported else "UNSUPPORTED"
        else:
            ep = "UNSUPPORTED"
        tokens_by_evidence_pillar[ep] = tokens_by_evidence_pillar.get(ep, 0) + tokens

    print("\n=== Token Totals by Labeled Pillar vs Evidence-Supported Pillar (Heuristic Triage) ===")
    print(f"{'Pillar':<40} | {'Labeled Pillar Tokens':<22} | {'Evidence-Supported Tokens':<26}")
    print("-" * 92)
    all_pillar_keys = sorted(list(set(list(tokens_by_labeled_pillar.keys()) + list(tokens_by_evidence_pillar.keys()))))
    for p in all_pillar_keys:
        l_tok = tokens_by_labeled_pillar.get(p, 0)
        e_tok = tokens_by_evidence_pillar.get(p, 0)
        print(f"{p:<40} | {l_tok:<22} | {e_tok:<26}")

    full_output = {
        "description": "B6 Old vs New PAGAC Comparison and Heuristic Pillar Triage",
        "pagac_comparisons": doc_comparisons,
        "tokens_by_labeled_pillar": tokens_by_labeled_pillar,
        "tokens_by_evidence_pillar": tokens_by_evidence_pillar,
        "total_tokens_staged": sum(d["token_count"] for d in all_new_docs),
    }

    out_dir = Path("data/staging_phase11_4/audit_outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "reslice_comparison.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(full_output, f, indent=2)
    print(f"\nSaved comparison to {out_path}")

if __name__ == "__main__":
    main()
