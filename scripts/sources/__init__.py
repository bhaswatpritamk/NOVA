"""Nova-Fit Educational Source Document Collections across all 7 Pillars."""

from __future__ import annotations

import importlib
from typing import Any, Dict, List

SOURCE_MODULES = [
    "scripts.sources.pillar1_exercise_science",
    "scripts.sources.pillar1_part2",
    "scripts.sources.pillar2_strength_principles",
    "scripts.sources.pillar2_part2",
    "scripts.sources.pillar3_exercise_technique",
    "scripts.sources.pillar3_part2",
    "scripts.sources.pillar4_nutrition_hydration",
    "scripts.sources.pillar4_part2",
    "scripts.sources.pillar5_sleep_recovery",
    "scripts.sources.pillar5_part2",
    "scripts.sources.pillar6_adaptations_fatigue",
    "scripts.sources.pillar6_part2",
    "scripts.sources.pillar7_general_safety",
    "scripts.sources.pillar7_part2",
    "scripts.sources.pillars_part3",
    "scripts.sources.pillars_part4",
    "scripts.sources.pillars_part5",
]


def get_all_documents() -> List[Dict[str, Any]]:
    """Load and aggregate all educational documents across all 7 pillars."""
    all_docs: List[Dict[str, Any]] = []
    for mod_name in SOURCE_MODULES:
        mod = importlib.import_module(mod_name)
        docs = getattr(mod, "DOCUMENTS", [])
        all_docs.extend(docs)
    return all_docs
