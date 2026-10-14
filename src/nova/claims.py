"""Project Nova-Fit: Source-Grounded Claim Verification and Traceability Engine.

Implements Phase 8 content pipeline traceability, factual claim verification,
and claim categorization across the seven fitness pillars.

Distinguishes:
1. Supported claims: Grounded in consensus guidelines or peer-reviewed physiology.
2. Qualified claims: Supported with essential qualifications (population, training age, medical status).
3. Contested claims: Active scientific controversy or conflicting evidence.
4. Unsupported claims: Lacks empirical backing or reflects fitness folklore/myths.
5. Potentially unsafe claims: Contradicts safety guidelines, risks injury or adverse clinical events.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union


class ClaimCategory(str, Enum):
    """Five-tier categorization for scientific and fitness claims."""

    SUPPORTED = "SUPPORTED"
    QUALIFIED = "QUALIFIED"
    CONTESTED = "CONTESTED"
    UNSUPPORTED = "UNSUPPORTED"
    UNSAFE = "UNSAFE"


class RiskLevel(str, Enum):
    """Safety risk level associated with a claim or recommendation."""

    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class VerificationStatus(str, Enum):
    """Traceability verification status for educational documents."""

    VERIFIED = "VERIFIED"
    QUALIFIED = "QUALIFIED"
    UNVERIFIED = "UNVERIFIED"
    REJECTED = "REJECTED"


@dataclass
class ClaimRecord:
    """Individual factual or normative claim extracted and evaluated from corpus text."""

    claim_id: str
    pillar: str
    statement: str
    category: ClaimCategory
    qualification_notes: str = ""
    scientific_consensus: str = ""
    population_scope: str = "General healthy adults"
    risk_level: RiskLevel = RiskLevel.LOW
    source_ids: List[str] = field(default_factory=list)
    citation_refs: List[str] = field(default_factory=list)
    requires_human_review: bool = False
    flagged_keywords: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert claim record to dictionary."""
        d = asdict(self)
        d["category"] = self.category.value
        d["risk_level"] = self.risk_level.value
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ClaimRecord:
        """Construct claim record from dictionary."""
        return cls(
            claim_id=data["claim_id"],
            pillar=data["pillar"],
            statement=data["statement"],
            category=ClaimCategory(data["category"]),
            qualification_notes=data.get("qualification_notes", ""),
            scientific_consensus=data.get("scientific_consensus", ""),
            population_scope=data.get("population_scope", "General healthy adults"),
            risk_level=RiskLevel(data.get("risk_level", "LOW")),
            source_ids=list(data.get("source_ids", [])),
            citation_refs=list(data.get("citation_refs", [])),
            requires_human_review=bool(data.get("requires_human_review", False)),
            flagged_keywords=list(data.get("flagged_keywords", [])),
        )


@dataclass
class DocumentTraceabilityRecord:
    """Complete provenance and transformation history for an educational synthesis document."""

    doc_id: str
    topic_pillar: str
    authoring_method: str  # e.g., "educational_synthesis"
    transformation_history: List[str]
    primary_source_id: str
    primary_source_url: str
    source_section_ref: str
    claims: List[str]  # Claim IDs or statements
    verification_status: VerificationStatus
    license: str
    attribution_notes: str
    doc_sha256: str
    source_sha256: str
    last_audited: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert traceability record to dictionary."""
        d = asdict(self)
        d["verification_status"] = self.verification_status.value
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> DocumentTraceabilityRecord:
        """Construct traceability record from dictionary."""
        return cls(
            doc_id=data["doc_id"],
            topic_pillar=data["topic_pillar"],
            authoring_method=data.get("authoring_method", "educational_synthesis"),
            transformation_history=list(data.get("transformation_history", [])),
            primary_source_id=data["primary_source_id"],
            primary_source_url=data.get("primary_source_url", ""),
            source_section_ref=data.get("source_section_ref", ""),
            claims=list(data.get("claims", [])),
            verification_status=VerificationStatus(data.get("verification_status", "VERIFIED")),
            license=data.get("license", "Public Domain"),
            attribution_notes=data.get("attribution_notes", ""),
            doc_sha256=data.get("doc_sha256", ""),
            source_sha256=data.get("source_sha256", ""),
            last_audited=data.get("last_audited", "2026-10-14"),
        )


# =============================================================================
# Automated Prioritization & Safety Keyword Heuristics
# =============================================================================

POTENTIALLY_UNSAFE_PATTERNS: List[Tuple[str, str, RiskLevel]] = [
    (r"\bpush through\b.*?\b(?:sharp|joint|spine)\b.*?\bpain\b", "Encourages exercising through acute, sharp, or joint pain", RiskLevel.CRITICAL),
    (r"\b(?:dehydrat(?:e|ion) for rapid weight loss|sweat suits? to cut weight)\b", "Dangerous acute dehydration guidance", RiskLevel.CRITICAL),
    (r"\b(ballistic stretch(ing)? with (heavy|maximum) load)\b", "Uncontrolled ballistic loading at end range", RiskLevel.HIGH),
    (r"\b(fasted high intensity.*without medical clearance)\b", "Fasted high intensity in unscreened populations", RiskLevel.MODERATE),
    (r"\b(ignore (dizziness|chest pain|shortness of breath))\b", "Ignoring cardiovascular red flag symptoms", RiskLevel.CRITICAL),
]

POPULATION_DEPENDENCY_PATTERNS: List[Tuple[str, str]] = [
    (r"\b(older adults?|elderly|geriatric|sarcopeni(a|c))\b", "Older adults / balance & bone density considerations"),
    (r"\b(children|adolescents?|youth|pediatric)\b", "Pediatric / growth plate & maturation considerations"),
    (r"\b(pregnan(t|cy)|postpartum)\b", "Obstetric considerations / avoid supine after 1st trimester"),
    (r"\b(hypertens(ion|ive)|cardiovascular disease|cardiac)\b", "Cardiovascular clinical clearance required"),
    (r"\b(osteo(porosis|penia))\b", "Fragility / avoid forceful spinal flexion"),
]

CONTESTED_TOPIC_PATTERNS: List[Tuple[str, str]] = [
    (r"\b(static stretch(ing)? before (sprinting|jumping|lifting))\b", "Pre-exercise static stretching impact on power/rate of force development"),
    (r"\b(anabolic window|immediate post-workout protein timing)\b", "Urgency of immediate post-exercise nutrient timing vs total daily intake"),
    (r"\b(optimal training frequency per muscle group)\b", "Frequency vs weekly volume equivalence debate"),
    (r"\b(fasted cardio.*fat loss)\b", "Fasted vs fed cardio for 24-hour lipid oxidation and fat mass changes"),
]

UNSUPPORTED_MYTH_PATTERNS: List[Tuple[str, str]] = [
    (r"\b(spot reduc(tion|e)|lose belly fat by doing crunches)\b", "Spot reduction of adipose tissue"),
    (r"\b(lactic acid causes doms|lactate causes delayed onset muscle soreness)\b", "Lactate misattributed as cause of delayed onset muscle soreness"),
    (r"\b(muscle turns into fat|fat turns into muscle)\b", "Adipocyte and myocyte transdifferentiation myth"),
    (r"\b(detoxify your body through sweat)\b", "Sweat glands performing hepatic/renal detoxification myth"),
]


def analyze_text_for_claims(text: str) -> Dict[str, Any]:
    """Automated heuristic check to prioritize human review.

    Note:
        Automated heuristics highlight candidate patterns but CANNOT
        independently establish scientific truth or replace expert review.
    """
    findings: Dict[str, List[Dict[str, str]]] = {
        "unsafe_flags": [],
        "population_dependencies": [],
        "contested_topics": [],
        "unsupported_myths": [],
    }

    t_lower = text.lower()

    for pattern, description, risk in POTENTIALLY_UNSAFE_PATTERNS:
        match = re.search(pattern, t_lower)
        if match:
            findings["unsafe_flags"].append({
                "matched_text": match.group(0),
                "description": description,
                "risk_level": risk.value,
            })

    for pattern, description in POPULATION_DEPENDENCY_PATTERNS:
        match = re.search(pattern, t_lower)
        if match:
            findings["population_dependencies"].append({
                "matched_text": match.group(0),
                "description": description,
            })

    for pattern, description in CONTESTED_TOPIC_PATTERNS:
        match = re.search(pattern, t_lower)
        if match:
            findings["contested_topics"].append({
                "matched_text": match.group(0),
                "description": description,
            })

    for pattern, description in UNSUPPORTED_MYTH_PATTERNS:
        match = re.search(pattern, t_lower)
        if match:
            findings["unsupported_myths"].append({
                "matched_text": match.group(0),
                "description": description,
            })

    return findings


# =============================================================================
# Claim Review Registry
# =============================================================================


class ClaimReviewRegistry:
    """Registry managing reviewed scientific claims, categories, and audit records."""

    def __init__(self, claims: Optional[List[ClaimRecord]] = None, version: str = "1.0.0") -> None:
        self.version = version
        self.updated_at = datetime.now(timezone.utc).isoformat()
        self.claims: Dict[str, ClaimRecord] = {}
        if claims:
            for c in claims:
                self.claims[c.claim_id] = c

    @classmethod
    def load(cls, path: Union[str, Path]) -> ClaimReviewRegistry:
        """Load claim registry from JSON file."""
        p = Path(path)
        if not p.is_file():
            raise FileNotFoundError(f"Claim registry file not found: {p}")
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        registry = cls(version=data.get("version", "1.0.0"))
        registry.updated_at = data.get("updated_at", registry.updated_at)
        for c_data in data.get("claims", []):
            rec = ClaimRecord.from_dict(c_data)
            registry.claims[rec.claim_id] = rec
        return registry

    def save(self, path: Union[str, Path]) -> None:
        """Save claim registry to JSON file."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": self.version,
            "project": "Nova-Fit",
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "total_claims": len(self.claims),
            "category_summary": self.get_category_counts(),
            "claims": [c.to_dict() for c in self.claims.values()],
        }
        with open(p, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def register(self, claim: ClaimRecord) -> None:
        """Add or update a claim record."""
        self.claims[claim.claim_id] = claim

    def get(self, claim_id: str) -> Optional[ClaimRecord]:
        """Retrieve claim by ID."""
        return self.claims.get(claim_id)

    def get_category_counts(self) -> Dict[str, int]:
        """Return counts of claims by category."""
        counts: Dict[str, int] = {cat.value: 0 for cat in ClaimCategory}
        for c in self.claims.values():
            counts[c.category.value] = counts.get(c.category.value, 0) + 1
        return counts

    def get_unresolved_or_flagged_claims(self) -> List[ClaimRecord]:
        """Return all claims that require human review or are contested/unsupported/unsafe."""
        results: List[ClaimRecord] = []
        for c in self.claims.values():
            if c.requires_human_review or c.category in (
                ClaimCategory.CONTESTED,
                ClaimCategory.UNSUPPORTED,
                ClaimCategory.UNSAFE,
            ):
                results.append(c)
        return results
