"""Project NOVA Phase 10: Verified Fitness Corpus Ingestion & Expansion Engine.

Provides an auditable, resumable, and legally gated source-ingestion pipeline
for scaling Project NOVA's training corpus towards 5M+ tokens while maintaining
absolute provenance, health safety, and zero benchmark contamination.

Features:
1. Multi-format ingestion: HTML, Markdown, Plain Text, PDF, JSON/JSONL.
2. Strict legal & licensing verification gate (17 U.S.C. § 105, CC BY 4.0, CC0).
3. Seven-pillar topic categorization and evidence interpretation preservation.
4. Robust text normalization, boilerplate stripping, and quality filters.
5. Automated health and safety claim screening (medical diagnosis, extreme diets, dangerous substances, contraindications).
6. Held-out benchmark contamination prevention (exact and near-duplicate leakage detection).
7. Exact (SHA-256) and near-duplicate (Jaccard shingle) clustering.
8. Source-level and group-level train/validation partitioning.
9. Resumable ingestion tracking via state files.
10. Machine-readable manifests and cryptographic audit reports.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import re
import unicodedata
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Callable, Dict, Iterator, List, Optional, Sequence, Set, Tuple, Union

from nova.benchmark import FitnessEvaluationBenchmark
from nova.corpus import TOPIC_DOMAINS, SourceProvenanceRecord, SourceRegistry
from nova.tokenizer import NovaTokenizer, load_tokenizer


# =============================================================================
# 1. Seven Fitness Pillars (Canonical & Compatibility Mapping)
# =============================================================================

class FitnessPillar(str, Enum):
    """The seven core fitness pillars for Project NOVA."""

    PILLAR_1_PHYSIOLOGY = "exercise_science_biomechanics"
    PILLAR_2_STRENGTH = "strength_training_programming"
    PILLAR_3_BIOMECHANICS = "exercise_technique_safety"
    PILLAR_4_NUTRITION = "nutrition_fundamentals_hydration"
    PILLAR_5_RECOVERY = "sleep_recovery_physical_activity"
    PILLAR_6_INJURY_PREVENTION = "training_adaptations_fatigue_load"
    PILLAR_7_EDUCATION = "general_fitness_education_safety"


PILLAR_DISPLAY_NAMES: Dict[FitnessPillar, str] = {
    FitnessPillar.PILLAR_1_PHYSIOLOGY: "1. Exercise Physiology & General Fitness",
    FitnessPillar.PILLAR_2_STRENGTH: "2. Strength Training & Programming",
    FitnessPillar.PILLAR_3_BIOMECHANICS: "3. Biomechanics & Movement Execution",
    FitnessPillar.PILLAR_4_NUTRITION: "4. Nutrition & Hydration",
    FitnessPillar.PILLAR_5_RECOVERY: "5. Recovery & Sleep",
    FitnessPillar.PILLAR_6_INJURY_PREVENTION: "6. Injury Prevention & Exercise Safety",
    FitnessPillar.PILLAR_7_EDUCATION: "7. Fitness Education & Evidence Interpretation",
}

PILLAR_ALIASES: Dict[str, FitnessPillar] = {
    # Numerical
    "1": FitnessPillar.PILLAR_1_PHYSIOLOGY,
    "2": FitnessPillar.PILLAR_2_STRENGTH,
    "3": FitnessPillar.PILLAR_3_BIOMECHANICS,
    "4": FitnessPillar.PILLAR_4_NUTRITION,
    "5": FitnessPillar.PILLAR_5_RECOVERY,
    "6": FitnessPillar.PILLAR_6_INJURY_PREVENTION,
    "7": FitnessPillar.PILLAR_7_EDUCATION,
    # Keys
    "exercise_science_biomechanics": FitnessPillar.PILLAR_1_PHYSIOLOGY,
    "strength_training_programming": FitnessPillar.PILLAR_2_STRENGTH,
    "exercise_technique_safety": FitnessPillar.PILLAR_3_BIOMECHANICS,
    "nutrition_fundamentals_hydration": FitnessPillar.PILLAR_4_NUTRITION,
    "sleep_recovery_physical_activity": FitnessPillar.PILLAR_5_RECOVERY,
    "training_adaptations_fatigue_load": FitnessPillar.PILLAR_6_INJURY_PREVENTION,
    "general_fitness_education_safety": FitnessPillar.PILLAR_7_EDUCATION,
    # Normalized underscore aliases
    "exercise_physiology": FitnessPillar.PILLAR_1_PHYSIOLOGY,
    "exercise_physiology_and_general_fitness": FitnessPillar.PILLAR_1_PHYSIOLOGY,
    "strength_training": FitnessPillar.PILLAR_2_STRENGTH,
    "strength_training_and_programming": FitnessPillar.PILLAR_2_STRENGTH,
    "biomechanics": FitnessPillar.PILLAR_3_BIOMECHANICS,
    "biomechanics_and_movement": FitnessPillar.PILLAR_3_BIOMECHANICS,
    "nutrition": FitnessPillar.PILLAR_4_NUTRITION,
    "nutrition_hydration": FitnessPillar.PILLAR_4_NUTRITION,
    "nutrition_and_hydration": FitnessPillar.PILLAR_4_NUTRITION,
    "recovery": FitnessPillar.PILLAR_5_RECOVERY,
    "recovery_sleep": FitnessPillar.PILLAR_5_RECOVERY,
    "recovery_and_sleep": FitnessPillar.PILLAR_5_RECOVERY,
    "sleep": FitnessPillar.PILLAR_5_RECOVERY,
    "injury_prevention": FitnessPillar.PILLAR_6_INJURY_PREVENTION,
    "injury_prevention_and_exercise_safety": FitnessPillar.PILLAR_6_INJURY_PREVENTION,
    "fitness_education": FitnessPillar.PILLAR_7_EDUCATION,
    "fitness_education_and_evidence_interpretation": FitnessPillar.PILLAR_7_EDUCATION,
}


def normalize_pillar(pillar_str: Union[str, FitnessPillar]) -> FitnessPillar:
    """Normalize any pillar representation to a canonical FitnessPillar."""
    if isinstance(pillar_str, FitnessPillar):
        return pillar_str
    raw = str(pillar_str).strip().lower()
    norm_under = raw.replace("-", "_").replace(" ", "_")
    norm_space = raw.replace("-", " ").replace("_", " ")

    if norm_under in PILLAR_ALIASES:
        return PILLAR_ALIASES[norm_under]
    if norm_space in PILLAR_ALIASES:
        return PILLAR_ALIASES[norm_space]

    for p in FitnessPillar:
        if norm_under == p.value or norm_under in p.value or p.value.endswith(norm_under):
            return p
    raise ValueError(f"Unknown or unsupported fitness pillar: {pillar_str}")


# =============================================================================
# 2. Legal & Licensing Verification Gates
# =============================================================================

class LicenseCategory(str, Enum):
    """Categorization of source licenses regarding model training permissions."""

    PUBLIC_DOMAIN_US_GOV = "PUBLIC_DOMAIN_US_GOV"
    PUBLIC_DOMAIN_CC0 = "PUBLIC_DOMAIN_CC0"
    PERMISSIVE_CC_BY = "PERMISSIVE_CC_BY"
    OPEN_GOVERNMENT = "OPEN_GOVERNMENT"
    RESTRICTED_NON_COMMERCIAL = "RESTRICTED_NON_COMMERCIAL"
    RESTRICTED_NO_DERIVATIVES = "RESTRICTED_NO_DERIVATIVES"
    AI_TRAINING_PROHIBITED = "AI_TRAINING_PROHIBITED"
    PROPRIETARY = "PROPRIETARY"
    UNKNOWN = "UNKNOWN"


@dataclass
class LicenseGateResult:
    """Audit result for a source's license compatibility."""

    is_compliant: bool
    category: LicenseCategory
    license_name: str
    legal_basis: str
    requires_attribution: bool
    mandatory_attribution_text: str = ""
    rejection_reason: str = ""
    human_override_approved: bool = False
    reviewer_id: str = ""
    review_notes: str = ""
    is_us_gov_employee_work: Optional[bool] = None
    has_third_party_copyright: Optional[bool] = None
    third_party_exclusions: str = ""
    jurisdiction_notice: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["category"] = self.category.value
        return d


def audit_license(
    license_name: str,
    legal_basis: str = "",
    allow_human_override: bool = False,
    reviewer_id: str = "",
    reviewer_notes: str = "",
    is_us_gov_employee_work: Optional[bool] = None,
    has_third_party_copyright: Optional[bool] = None,
    third_party_exclusions: str = "",
    text_content: str = "",
) -> LicenseGateResult:
    """Strictly audit a license for training compliance.

    Rules:
    - AI Training Prohibitions: Scans page text, front matter, and terms for language prohibiting
      LLM or generative-AI training without permission, REGARDLESS of stated Creative Commons license.
    - US Federal Government works under 17 U.S.C. § 105 are domestic public domain within the United States.
      * Material created by official federal officers/employees in the scope of official employment is domestic public domain.
      * Does NOT automatically imply worldwide public domain status (foreign copyright may apply depending on jurisdiction).
      * Contractor or grantee works are NOT automatically public domain under § 105; if is_us_gov_employee_work is False,
        the source cannot be automatically cleared as US Gov Public Domain and requires human legal review.
      * If third-party copyrighted content is present without documented exclusions, human review is required.
    - CC0 1.0 Universal is compliant (Public Domain dedication worldwide).
    - CC BY 4.0 and CC BY 3.0 are compliant (Attribution required).
    - CC BY-NC, CC BY-ND, proprietary, or unknown licenses are REJECTED
      unless an explicit human legal review override is provided with reviewer ID.
    - Human override ONLY clears licensing; it never bypasses safety, quality, or benchmark integrity gates.
    """
    l_norm = (license_name or "").strip().lower()
    b_norm = (legal_basis or "").strip().lower()

    # 0. AI/LLM Training Prohibition Scan (runs FIRST, regardless of stated Creative Commons or Public Domain status)
    combined_scan = f"{license_name}\n{legal_basis}\n{text_content}".lower()
    ai_prohibition_patterns = [
        r"may not be used for (?:the )?training of artificial intelligence",
        r"training of artificial intelligence or large language models",
        r"(?:training of artificial intelligence|training of.*large language models).*without (?:prior )?(?:written )?permission",
        r"without (?:prior )?(?:written )?permission.*(?:training of artificial intelligence|training of.*large language models)",
        r"(?:prohibit\w*|forbid\w*|no|not permit\w*)\s+(?:the\s+)?(?:use|training|ingest\w*|scrap\w*)\b.*?\b(?:ai|artificial intelligence|llm|large language model|generative ai|machine learning)",
        r"(?:ai|artificial intelligence|llm|generative ai|machine learning)\s+training\s+(?:is\s+)?(?:prohibited|forbidden|not permitted|disallowed)",
        r"(?:no|not)\s+(?:authorized|permitted)\s+for\s+(?:ai|machine learning|llm)\s+training",
    ]
    is_ai_prohibited = any(re.search(pat, combined_scan, re.IGNORECASE) for pat in ai_prohibition_patterns)
    if is_ai_prohibited:
        rej_reason = (
            "AI/LLM training prohibition: Source explicitly prohibits artificial intelligence, "
            "machine learning, or large language model training without prior written permission."
        )
        if allow_human_override and reviewer_id.strip():
            return LicenseGateResult(
                is_compliant=True,
                category=LicenseCategory.AI_TRAINING_PROHIBITED,
                license_name=license_name,
                legal_basis=legal_basis or "Bilateral AI Training Permission Granted",
                requires_attribution=True,
                rejection_reason="",
                human_override_approved=True,
                reviewer_id=reviewer_id.strip(),
                review_notes=reviewer_notes or "Human legal review verified bilateral AI training authorization.",
                is_us_gov_employee_work=is_us_gov_employee_work,
                has_third_party_copyright=has_third_party_copyright,
                third_party_exclusions=third_party_exclusions,
            )
        return LicenseGateResult(
            is_compliant=False,
            category=LicenseCategory.AI_TRAINING_PROHIBITED,
            license_name=license_name,
            legal_basis=legal_basis or "AI Training Prohibited by Terms/Front Matter",
            requires_attribution=False,
            rejection_reason=rej_reason,
            is_us_gov_employee_work=is_us_gov_employee_work,
            has_third_party_copyright=has_third_party_copyright,
            third_party_exclusions=third_party_exclusions,
        )

    # 1. US Government work
    if "17 u.s.c" in b_norm or "17 usc" in b_norm or "u.s. government work" in b_norm or ("public domain" in l_norm and "cc0" not in l_norm):
        if "nc" not in l_norm and "non-commercial" not in l_norm:
            # Check for contractor work
            if is_us_gov_employee_work is False:
                rej_reason = (
                    "Contractor or grantee work is not exempt under 17 U.S.C. § 105. "
                    "Federal funding alone does not place contractor intellectual property in the public domain."
                )
                if allow_human_override and reviewer_id.strip():
                    return LicenseGateResult(
                        is_compliant=True,
                        category=LicenseCategory.PUBLIC_DOMAIN_US_GOV,
                        license_name=license_name,
                        legal_basis=legal_basis or "17 U.S.C. § 105 (Contractor Rights Formally Assigned)",
                        requires_attribution=True,
                        rejection_reason="",
                        human_override_approved=True,
                        reviewer_id=reviewer_id.strip(),
                        review_notes=reviewer_notes or "Human legal review verified contractor intellectual property assignment.",
                        is_us_gov_employee_work=False,
                        has_third_party_copyright=has_third_party_copyright,
                        third_party_exclusions=third_party_exclusions,
                        jurisdiction_notice="US domestic public domain under 17 U.S.C. § 105; foreign copyright may apply.",
                    )
                return LicenseGateResult(
                    is_compliant=False,
                    category=LicenseCategory.UNKNOWN,
                    license_name=license_name,
                    legal_basis=legal_basis or "17 U.S.C. § 105 (Ambiguous Contractor Work)",
                    requires_attribution=False,
                    rejection_reason=rej_reason,
                    is_us_gov_employee_work=False,
                    has_third_party_copyright=has_third_party_copyright,
                )

            # Check for unexcluded third-party copyrighted content
            if has_third_party_copyright is True and not third_party_exclusions.strip():
                rej_reason = (
                    "Source contains third-party copyrighted material without documented exclusions. "
                    "Federal public domain status under 17 U.S.C. § 105 does not extend to embedded third-party content."
                )
                if allow_human_override and reviewer_id.strip():
                    return LicenseGateResult(
                        is_compliant=True,
                        category=LicenseCategory.PUBLIC_DOMAIN_US_GOV,
                        license_name=license_name,
                        legal_basis=legal_basis or "17 U.S.C. § 105",
                        requires_attribution=True,
                        rejection_reason="",
                        human_override_approved=True,
                        reviewer_id=reviewer_id.strip(),
                        review_notes=reviewer_notes or "Human reviewer confirmed third-party carve-outs.",
                        is_us_gov_employee_work=True,
                        has_third_party_copyright=True,
                        third_party_exclusions=third_party_exclusions,
                        jurisdiction_notice="US domestic public domain under 17 U.S.C. § 105; foreign copyright may apply.",
                    )
                return LicenseGateResult(
                    is_compliant=False,
                    category=LicenseCategory.PUBLIC_DOMAIN_US_GOV,
                    license_name=license_name,
                    legal_basis=legal_basis or "17 U.S.C. § 105",
                    requires_attribution=False,
                    rejection_reason=rej_reason,
                    is_us_gov_employee_work=True,
                    has_third_party_copyright=True,
                )

            return LicenseGateResult(
                is_compliant=True,
                category=LicenseCategory.PUBLIC_DOMAIN_US_GOV,
                license_name=license_name,
                legal_basis=legal_basis or "17 U.S.C. § 105",
                requires_attribution=False,
                is_us_gov_employee_work=True if is_us_gov_employee_work is None else is_us_gov_employee_work,
                has_third_party_copyright=bool(has_third_party_copyright),
                third_party_exclusions=third_party_exclusions,
                jurisdiction_notice="US domestic public domain under 17 U.S.C. § 105; foreign copyright may apply depending on jurisdiction.",
            )

    # 2. CC0
    if "cc0" in l_norm:
        return LicenseGateResult(
            is_compliant=True,
            category=LicenseCategory.PUBLIC_DOMAIN_CC0,
            license_name=license_name,
            legal_basis=legal_basis or "Creative Commons Zero 1.0 Universal",
            requires_attribution=False,
            jurisdiction_notice="Worldwide public domain dedication.",
        )

    # 3. CC BY (non-NC, non-ND)
    if "cc by" in l_norm and "nc" not in l_norm and "nd" not in l_norm:
        return LicenseGateResult(
            is_compliant=True,
            category=LicenseCategory.PERMISSIVE_CC_BY,
            license_name=license_name,
            legal_basis=legal_basis or "Creative Commons Attribution 4.0 International",
            requires_attribution=True,
            jurisdiction_notice="Worldwide permissive license with statutory attribution requirements.",
        )

    # 4. Open Government Licence (UK / Canada / etc)
    if "open government licence" in l_norm or "ogl" in l_norm:
        return LicenseGateResult(
            is_compliant=True,
            category=LicenseCategory.OPEN_GOVERNMENT,
            license_name=license_name,
            legal_basis=legal_basis or "Open Government Licence",
            requires_attribution=True,
            jurisdiction_notice="Permissive open government license with statutory attribution requirements.",
        )

    # 5. Restricted licenses
    cat = LicenseCategory.UNKNOWN
    rej_reason = "Unknown or unverified reuse permissions."

    if re.search(r"\b(nc|non-commercial|noncommercial)\b", l_norm):
        cat = LicenseCategory.RESTRICTED_NON_COMMERCIAL
        rej_reason = "Non-commercial restriction (CC BY-NC) incompatible with unrestricted model pretraining."
    elif re.search(r"\b(nd|no-derivatives|noderivatives)\b", l_norm):
        cat = LicenseCategory.RESTRICTED_NO_DERIVATIVES
        rej_reason = "No-derivatives restriction (CC BY-ND) prohibits derivative dataset preparation and model training."
    elif "proprietary" in l_norm or "all rights reserved" in l_norm or "copyright" in l_norm:
        cat = LicenseCategory.PROPRIETARY
        rej_reason = "Proprietary or all-rights-reserved content cannot be ingested without a written bilateral license."

    # Check human override
    if allow_human_override and reviewer_id.strip():
        return LicenseGateResult(
            is_compliant=True,
            category=cat,
            license_name=license_name,
            legal_basis=legal_basis,
            requires_attribution=True,
            rejection_reason="",
            human_override_approved=True,
            reviewer_id=reviewer_id.strip(),
            review_notes=reviewer_notes or "Manually approved by human reviewer with documented legal basis.",
            is_us_gov_employee_work=is_us_gov_employee_work,
            has_third_party_copyright=has_third_party_copyright,
            third_party_exclusions=third_party_exclusions,
        )

    return LicenseGateResult(
        is_compliant=False,
        category=cat,
        license_name=license_name,
        legal_basis=legal_basis,
        requires_attribution=False,
        rejection_reason=rej_reason,
        is_us_gov_employee_work=is_us_gov_employee_work,
        has_third_party_copyright=has_third_party_copyright,
        third_party_exclusions=third_party_exclusions,
    )


# =============================================================================
# 3. Document Schema & Status Types
# =============================================================================

class AuthoringMethod(str, Enum):
    """Method used to produce the document text."""

    PRIMARY_SOURCE_EXTRACT = "primary_source_extract"
    EDUCATIONAL_SYNTHESIS = "educational_synthesis"
    GOVERNMENT_REPORT = "government_report"
    SCIENTIFIC_REVIEW = "scientific_review"


class IngestionStatus(str, Enum):
    """Status of an ingested document."""

    APPROVED = "APPROVED"
    PENDING_REVIEW = "PENDING_REVIEW"
    REJECTED = "REJECTED"
    QUARANTINED = "QUARANTINED"


@dataclass
class NormalizedDocument:
    """Canonical document representation with complete legal and scientific provenance."""

    doc_id: str
    source_id: str
    title: str
    text: str
    pillar: str  # FitnessPillar.value
    parent_source_id: str = ""
    canonical_source_url: str = ""
    authoring_method: AuthoringMethod = AuthoringMethod.PRIMARY_SOURCE_EXTRACT
    author: str = ""
    publisher: str = ""
    publication_date: str = ""
    retrieval_date: str = ""
    url: str = ""
    license: str = "Public Domain"
    legal_basis: str = "17 U.S.C. § 105"
    attribution_required: bool = False
    attribution_text: str = ""
    extraction_method: str = "plain_text"
    processing_version: str = "10.0.0"
    raw_sha256: str = ""
    content_sha256: str = ""
    group_id: str = ""
    word_count: int = 0
    char_count: int = 0
    token_count: int = 0
    safety_flags: List[Dict[str, str]] = field(default_factory=list)
    benchmark_contamination: bool = False
    benchmark_matches: List[Dict[str, Any]] = field(default_factory=list)
    ingestion_status: IngestionStatus = IngestionStatus.APPROVED
    review_notes: str = ""
    transformation_history: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.parent_source_id:
            self.parent_source_id = self.source_id
        if not self.canonical_source_url:
            self.canonical_source_url = self.url
        if not self.char_count:
            self.char_count = len(self.text)
        if not self.word_count:
            self.word_count = len(self.text.split())
        if not self.content_sha256 and self.text:
            self.content_sha256 = hashlib.sha256(self.text.encode("utf-8")).hexdigest()
        if not self.group_id:
            self.group_id = self.source_id or self.doc_id

    def to_formatted_text(self) -> str:
        """Format document into canonical corpus section string."""
        return f"[SECTION: {self.title}]\n[SOURCE: {self.source_id}]\n{self.text.strip()}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        d = asdict(self)
        d["authoring_method"] = self.authoring_method.value
        d["ingestion_status"] = self.ingestion_status.value
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> NormalizedDocument:
        """Instantiate from dictionary."""
        return cls(
            doc_id=data["doc_id"],
            source_id=data["source_id"],
            parent_source_id=data.get("parent_source_id", data.get("source_id", "")),
            canonical_source_url=data.get("canonical_source_url", data.get("url", "")),
            title=data.get("title", ""),
            text=data["text"],
            pillar=data["pillar"],
            authoring_method=AuthoringMethod(data.get("authoring_method", AuthoringMethod.PRIMARY_SOURCE_EXTRACT.value)),
            author=data.get("author", ""),
            publisher=data.get("publisher", ""),
            publication_date=data.get("publication_date", ""),
            retrieval_date=data.get("retrieval_date", ""),
            url=data.get("url", ""),
            license=data.get("license", "Public Domain"),
            legal_basis=data.get("legal_basis", "17 U.S.C. § 105"),
            attribution_required=bool(data.get("attribution_required", False)),
            attribution_text=data.get("attribution_text", ""),
            extraction_method=data.get("extraction_method", "plain_text"),
            processing_version=data.get("processing_version", "10.0.0"),
            raw_sha256=data.get("raw_sha256", ""),
            content_sha256=data.get("content_sha256", ""),
            group_id=data.get("group_id", data.get("source_id", "")),
            word_count=int(data.get("word_count", 0)),
            char_count=int(data.get("char_count", 0)),
            token_count=int(data.get("token_count", 0)),
            safety_flags=list(data.get("safety_flags", [])),
            benchmark_contamination=bool(data.get("benchmark_contamination", False)),
            benchmark_matches=list(data.get("benchmark_matches", [])),
            ingestion_status=IngestionStatus(data.get("ingestion_status", IngestionStatus.APPROVED.value)),
            review_notes=data.get("review_notes", ""),
            transformation_history=list(data.get("transformation_history", [])),
        )


# =============================================================================
# 4. Text Normalization & Boilerplate Stripping
# =============================================================================

# Common navigation, web footer, and copyright boilerplates
BOILERPLATE_PATTERNS = [
    re.compile(r"^page\s+\d+(\s+of\s+\d+)?$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^downloaded\s+from\s+.*$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^copyright\s+.*all\s+rights\s+reserved.*$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^cookie\s+(preferences|policy|notice).*$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^terms\s+of\s+(use|service).*$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^privacy\s+policy.*$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^(skip\s+to\s+main\s+content|table\s+of\s+contents|back\s+to\s+top)$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^share\s+this:\s*(facebook|twitter|linkedin|email).*$", re.IGNORECASE | re.MULTILINE),
]


def normalize_corpus_text(text: str) -> str:
    """Normalize text encoding, line wraps, whitespace, and strip common boilerplate."""
    if not text:
        return ""

    # 1. Unicode normalization (NFKC)
    text = unicodedata.normalize("NFKC", text)

    # 2. Typographic replacements
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace("\u2013", "-").replace("\u2014", "--")
    text = text.replace("\u00a0", " ")  # non-breaking space

    # 3. Strip boilerplate lines
    for pat in BOILERPLATE_PATTERNS:
        text = pat.sub("", text)

    # 4. Clean consecutive whitespace
    lines = []
    for line in text.split("\n"):
        cleaned = re.sub(r"[ \t]+", " ", line).strip()
        lines.append(cleaned)

    # 5. Collapse multiple blank lines to a maximum of two
    normalized = "\n".join(lines)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized).strip()
    return normalized


def assess_text_quality(
    text: str,
    min_chars: int = 150,
    min_words: int = 25,
    max_repetition_ratio: float = 0.35,
    max_non_ascii_ratio: float = 0.20,
) -> Tuple[bool, str]:
    """Assess whether text satisfies minimum quality standards for pretraining corpus.

    Rejects:
    - Extremely short text
    - Repetitive text / filler
    - Corrupted or binary junk
    """
    if len(text) < min_chars:
        return False, f"Text too short ({len(text)} chars < {min_chars} minimum)"

    # Non-ASCII ratio
    non_ascii = sum(1 for c in text if ord(c) > 127)
    ratio = non_ascii / len(text) if len(text) > 0 else 0.0
    if ratio > max_non_ascii_ratio:
        return False, f"Excessive non-ASCII / corrupt characters ({ratio:.2%} > {max_non_ascii_ratio:.2%})"

    words = text.split()
    if len(words) < min_words:
        return False, f"Word count too low ({len(words)} words < {min_words} minimum)"

    # Repetition check on 10-word shingles
    if len(words) >= 30:
        shingles = [" ".join(words[i : i + 10]) for i in range(len(words) - 9)]
        unique_shingles = set(shingles)
        rep_ratio = 1.0 - (len(unique_shingles) / len(shingles))
        if rep_ratio > max_repetition_ratio:
            return False, f"Excessive repetitive filler detected (repetition ratio {rep_ratio:.2f} > {max_repetition_ratio:.2f})"

    return True, "Quality criteria met"


# =============================================================================
# 5. Multi-Format Text Extractors
# =============================================================================

class SimpleHTMLTextExtractor(HTMLParser):
    """Clean HTML-to-text extractor that strips scripts, styles, and navigation."""

    def __init__(self):
        super().__init__()
        self.reset()
        self.fed: List[str] = []
        self.skip_depth = 0
        self.skip_tags = {"script", "style", "nav", "header", "footer", "aside", "noscript", "svg", "form"}

    def handle_starttag(self, tag, attrs):
        if tag.lower() in self.skip_tags:
            self.skip_depth += 1
        elif tag.lower() in {"p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr", "blockquote"}:
            self.fed.append("\n")

    def handle_endtag(self, tag):
        if tag.lower() in self.skip_tags:
            self.skip_depth = max(0, self.skip_depth - 1)
        elif tag.lower() in {"p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr", "blockquote"}:
            self.fed.append("\n")

    def handle_data(self, data):
        if self.skip_depth == 0:
            self.fed.append(data)

    def get_text(self) -> str:
        return "".join(self.fed)


def extract_text_from_html(raw_html: str) -> str:
    """Parse HTML and extract clean article text."""
    parser = SimpleHTMLTextExtractor()
    parser.feed(raw_html)
    return parser.get_text()


def extract_text_from_markdown(raw_md: str) -> str:
    """Parse Markdown, strip non-free media markdown, and normalize formatting."""
    # Strip markdown images ![alt](url)
    text = re.sub(r"!\[.*?\]\(.*?\)", "", raw_md)
    # Convert markdown links [text](url) -> text
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    # Remove HTML tags if embedded
    text = re.sub(r"<[^>]+>", " ", text)
    # Remove horizontal rules
    text = re.sub(r"^[ \t]*[-*_]{3,}[ \t]*$", "", text, flags=re.MULTILINE)
    # Clean code fences
    text = re.sub(r"```[a-zA-Z0-9_-]*\n", "", text)
    text = text.replace("```", "")
    return text


def extract_text_from_pdf_stream(pdf_bytes: bytes) -> str:
    """Extract printable text strings from uncompressed or /FlateDecode compressed PDF streams.

    If the PDF contains raster image XObjects with zero extractable text streams, returns
    'SCANNED_PDF_REQUIRING_OCR' so the ingestion pipeline can quarantine it with a clear
    diagnostic rather than silently treating it as empty.
    """
    # 1. Attempt import of pypdf if user has installed it in environment
    try:
        import io
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        extracted = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                extracted.append(t)
        if extracted:
            return "\n\n".join(extracted)
    except Exception:
        pass

    # 2. Extract and decompress stream objects (pure Python fallback for uncompressed and /FlateDecode)
    decompressed_buffers: List[bytes] = []
    pos = 0
    while True:
        s_idx = pdf_bytes.find(b"stream", pos)
        if s_idx == -1:
            break

        # Locate preceding dictionary (within 400 bytes)
        dict_start = pdf_bytes.rfind(b"<<", max(0, s_idx - 400), s_idx)
        dict_text = pdf_bytes[dict_start:s_idx] if dict_start != -1 else b""

        # Advance past 'stream' and newline
        after_stream = s_idx + 6
        if pdf_bytes[after_stream:after_stream + 2] == b"\r\n":
            data_start = after_stream + 2
        elif pdf_bytes[after_stream:after_stream + 1] in (b"\n", b"\r"):
            data_start = after_stream + 1
        else:
            data_start = after_stream

        e_idx = pdf_bytes.find(b"endstream", data_start)
        if e_idx == -1:
            break

        # Skip image and font streams to avoid decompressing large non-text bitmaps
        if b"/Image" in dict_text or b"/Font" in dict_text:
            pos = e_idx + 9
            continue

        data_end = e_idx
        if pdf_bytes[data_end - 2:data_end] == b"\r\n":
            data_end -= 2
        elif pdf_bytes[data_end - 1:data_end] in (b"\n", b"\r"):
            data_end -= 1

        stream_data = pdf_bytes[data_start:data_end]

        # Decompress if FlateDecode
        if b"FlateDecode" in dict_text:
            try:
                import zlib
                decomp = zlib.decompress(stream_data)
                decompressed_buffers.append(decomp)
            except Exception:
                try:
                    import zlib
                    decomp = zlib.decompress(stream_data, -zlib.MAX_WBITS)
                    decompressed_buffers.append(decomp)
                except Exception:
                    decompressed_buffers.append(stream_data)
        else:
            decompressed_buffers.append(stream_data)

        pos = e_idx + 9

    # Combine decompressed streams and raw bytes to search for BT ... ET text blocks
    all_content = decompressed_buffers + [pdf_bytes]
    text_chunks: List[str] = []
    for buf in all_content:
        bt_blocks = re.findall(rb"BT\s*(.*?)\s*ET", buf, re.DOTALL)
        for block in bt_blocks:
            tj_matches = re.findall(rb"\((.*?)\)\s*Tj", block)
            for m in tj_matches:
                try:
                    text_chunks.append(m.decode("latin1", errors="ignore"))
                except Exception:
                    pass
            array_matches = re.findall(rb"\[(.*?)\]\s*TJ", block, re.DOTALL)
            for arr in array_matches:
                sub = re.findall(rb"\((.*?)\)", arr)
                for s in sub:
                    try:
                        text_chunks.append(s.decode("latin1", errors="ignore"))
                    except Exception:
                        pass

    extracted = " ".join(text_chunks).strip()
    if extracted:
        return extracted

    # Check if this is an image-only scanned PDF requiring OCR
    if re.search(rb"/Subtype\s*/Image", pdf_bytes) or re.search(rb"/Type\s*/XObject", pdf_bytes):
        return "SCANNED_PDF_REQUIRING_OCR"

    return ""


# =============================================================================
# 6. Health & Fitness Safety Claim Screening
# =============================================================================

SAFETY_FLAG_RULES: List[Tuple[str, str, str]] = [
    # 1. Medical Diagnosis & Treatment
    (
        r"\b(diagnos(?:e|ing|is)\s+(?:a\s+)?(?:herniat(?:ed|ion)|meniscus|rotator\s+cuff|labral\s+tear|fracture|diabetes|hypertension))\b",
        "Medical diagnosis claim (diagnosing clinical pathology without medical licensing)",
        "CRITICAL",
    ),
    (
        r"\b(cure[s]?\s+(?:cancer|diabetes|arthritis|cardiovascular\s+disease))\b",
        "Unsubstantiated clinical curative claim",
        "CRITICAL",
    ),
    (
        r"\b(prescrib(?:e|ing)\s+(?:antibiotics|pharmaceuticals|prescription\s+meds|nsaids\s+daily))\b",
        "Prescribing prescription medication without clinician credentials",
        "HIGH",
    ),
    # 2. Extreme Dieting & Unsafe Weight-Loss
    (
        r"\b(dry\s+fast(?:ing)?\s+for\s+(?:\d+|several)\s+days)\b",
        "Extreme dry fasting (severe acute dehydration risk)",
        "CRITICAL",
    ),
    (
        r"\b(eat\s+less\s+than\s+(?:500|600|700|800)\s+calories?\s+per\s+day\s+to\s+shred)\b",
        "Severe starvation diet prescription without clinical monitoring",
        "HIGH",
    ),
    (
        r"\b(sweat\s+suit[s]?\s+(?:to|for)\s+cut(?:ting)?\s+weight|dehydrat(?:e|ion)\s+to\s+make\s+weight)\b",
        "Dangerous acute dehydration protocols risking hyperthermia and renal failure",
        "CRITICAL",
    ),
    # 3. Dangerous Supplementation & Prohibited Substances
    (
        r"\b(anabolic\s+steroid[s]?|sarms|selective\s+androgen\s+receptor|dnp|2,4-dinitrophenol|clenbuterol|ephedra)\b",
        "Prohibited performance-enhancing drugs / unsafe thermogenic compounds",
        "CRITICAL",
    ),
    (
        r"\b(detox\s+tea[s]?\s+melt\s+(?:away\s+)?fat|sweat\s+belt[s]?\s+burn\s+belly\s+fat)\b",
        "Unsupported supplement/device claim with diuretic/laxative risks",
        "HIGH",
    ),
    # 4. Exercise Contraindications & Ignoring Red Flags
    (
        r"\bpush\s+through\b.*?\b(?:sharp|radiating|joint|spine)\b.*?\bpain\b",
        "Instructing user to ignore sharp, radiating, or joint injury signals",
        "CRITICAL",
    ),
    (
        r"\b(ignore\s+(?:chest\s+pain|dizziness|syncope|shortness\s+of\s+breath|blacking\s+out))\b",
        "Instructing user to ignore life-threatening cardiovascular red flags",
        "CRITICAL",
    ),
    # 5. Unsupported Scientific Myths
    (
        r"\b(spot\s+reduc(?:e|tion)\s+(?:of\s+)?(?:belly|abdominal|thigh)\s+fat)\b",
        "Spot reduction myth (contradicts systemic adipose lipolysis physiology)",
        "MODERATE",
    ),
    (
        r"\b(lactic\s+acid\s+causes\s+(?:48[- ]hour\s+)?doms|lactic\s+acid\s+causes\s+muscle\s+soreness\s+days\s+later)\b",
        "Lactic acid DOMS myth (lactate is cleared within 30-60 min post-exercise)",
        "MODERATE",
    ),
]


class HealthSafetyScreener:
    """Scans text for dangerous health advice, contraindications, and unscientific claims."""

    def __init__(self, custom_rules: Optional[List[Tuple[str, str, str]]] = None):
        self.rules = (custom_rules or []) + SAFETY_FLAG_RULES

    def screen_text(self, text: str) -> List[Dict[str, str]]:
        """Scan text and return any safety violations found."""
        flags: List[Dict[str, str]] = []
        t_lower = text.lower()

        for pattern, description, severity in self.rules:
            for match in re.finditer(pattern, t_lower):
                flags.append({
                    "matched_text": match.group(0),
                    "description": description,
                    "severity": severity,
                })
        return flags


# =============================================================================
# 7. Held-Out Benchmark Contamination Screener
# =============================================================================

# Exact recognized formal publication titles / standard legal document citations
# appearing as bibliographic attribution or prompt prefixes in benchmark items.
# These represent legitimate publication entity names rather than question/answer logic.
RECOGNIZED_BIBLIOGRAPHIC_TITLES: Set[str] = {
    "the physical activity guidelines for americans 2nd edition",
    "physical activity guidelines for americans 2nd edition",
    "the physical activity guidelines for americans second edition",
    "physical activity guidelines for americans second edition",
    "the 2018 physical activity guidelines advisory committee scientific",
    "2018 physical activity guidelines advisory committee scientific report",
    "openstax anatomy and physiology 2e section",
    "dietary guidelines for americans 2020 2025",
}


@dataclass
class ContaminationMatch:
    """Detailed record of a benchmark n-gram match preserving exact offsets and rationale."""

    matched_ngram: str
    match_origin: str  # 'PROMPT' or 'ANSWER'
    benchmark_question_id: str
    benchmark_version: str
    char_start: int
    char_end: int
    matched_snippet: str
    is_bibliographic_title: bool
    is_genuine_leakage: bool
    decision_rationale: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ContaminationCheckResult:
    """Result of contamination screening against held-out benchmark."""

    is_contaminated: bool
    has_bibliographic_match: bool
    matches: List[ContaminationMatch] = field(default_factory=list)
    decision_rationale: str = ""
    benchmark_version: str = "1.0.0"

    def to_summary_strings(self) -> List[str]:
        """Backward-compatible summary strings for logging."""
        summaries = []
        for m in self.matches:
            status = "BIBLIOGRAPHIC_CITATION" if m.is_bibliographic_title else "GENUINE_LEAKAGE"
            summaries.append(
                f"{m.match_origin} n-gram match ({m.benchmark_question_id} v{m.benchmark_version} "
                f"[{m.char_start}:{m.char_end}]): '{m.matched_ngram}' [{status}]"
            )
        return summaries

    def __iter__(self):
        """Enable backward-compatible tuple unpacking: is_contaminated, matches = detector.check_text(text)"""
        yield self.is_contaminated
        yield self.to_summary_strings()


class BenchmarkContaminationDetector:
    """Verifies that ingested text does not leak held-out diagnostic benchmark questions or answers.

    Distinguishes substantive inquiry/answer leakage from harmless formal publication title
    references (e.g. 'the Physical Activity Guidelines for Americans 2nd edition').
    Records exact character offsets, benchmark question ID, benchmark version, and rationale.
    """

    def __init__(self, benchmark: Optional[FitnessEvaluationBenchmark] = None, n_gram_len: int = 8):
        self.n_gram_len = n_gram_len
        self.benchmark = benchmark
        self.benchmark_version = getattr(benchmark, "version", "1.0.0") if benchmark else "1.0.0"
        self.benchmark_ngrams: Set[str] = set()
        self.prompt_ngrams: Set[str] = set()
        self.answer_ngrams: Set[str] = set()
        self.ngram_to_question: Dict[str, str] = {}
        self.bibliographic_title_ngrams: Set[str] = set(RECOGNIZED_BIBLIOGRAPHIC_TITLES)

        if self.benchmark:
            self._index_benchmark()

    def _index_benchmark(self) -> None:
        """Index word n-grams from all benchmark questions and canonical answers with provenance."""
        for q in self.benchmark.questions.values():
            q_id = q.question_id
            # Index prompt
            p_words = re.findall(r"\b\w+\b", q.prompt.lower())
            for i in range(len(p_words) - self.n_gram_len + 1):
                ng = " ".join(p_words[i : i + self.n_gram_len])
                self.prompt_ngrams.add(ng)
                self.benchmark_ngrams.add(ng)
                self.ngram_to_question[ng] = q_id

            # Index canonical answer
            if q.canonical_reference_answer:
                a_words = re.findall(r"\b\w+\b", q.canonical_reference_answer.lower())
                for i in range(len(a_words) - self.n_gram_len + 1):
                    ng = " ".join(a_words[i : i + self.n_gram_len])
                    self.answer_ngrams.add(ng)
                    self.benchmark_ngrams.add(ng)
                    self.ngram_to_question[ng] = q_id

    def check_text(self, text: str) -> ContaminationCheckResult:
        """Check text for n-gram contamination against the benchmark.

        Returns ContaminationCheckResult (supports tuple unpacking for backward compatibility).
        """
        if not self.benchmark_ngrams:
            return ContaminationCheckResult(
                is_contaminated=False,
                has_bibliographic_match=False,
                matches=[],
                decision_rationale="No benchmark n-grams indexed; clean.",
                benchmark_version=self.benchmark_version,
            )

        # Extract words along with their character offsets in the original text
        word_tokens = [(m.group(0).lower(), m.start(), m.end()) for m in re.finditer(r"\b\w+\b", text)]
        if len(word_tokens) < self.n_gram_len:
            return ContaminationCheckResult(
                is_contaminated=False,
                has_bibliographic_match=False,
                matches=[],
                decision_rationale="Text shorter than n-gram threshold; clean.",
                benchmark_version=self.benchmark_version,
            )

        matches: List[ContaminationMatch] = []
        for i in range(len(word_tokens) - self.n_gram_len + 1):
            window = word_tokens[i : i + self.n_gram_len]
            ng = " ".join(w[0] for w in window)

            if ng in self.benchmark_ngrams:
                char_start = window[0][1]
                char_end = window[-1][2]
                matched_snippet = text[char_start:char_end]
                q_id = self.ngram_to_question.get(ng, "BENCHMARK_UNKNOWN")

                if ng in self.answer_ngrams:
                    origin = "Answer"
                    is_bib = False
                    is_leak = True
                    rationale = f"CRITICAL: Substantive canonical reference answer leakage detected from {q_id}."
                else:
                    origin = "Prompt"
                    if ng in self.bibliographic_title_ngrams:
                        is_bib = True
                        is_leak = False
                        rationale = (
                            f"Harmless citation match: Formal publication title reference ('{ng}') "
                            f"in {q_id} prompt citation prefix. No operative prompt logic or answer leakage."
                        )
                    else:
                        is_bib = False
                        is_leak = True
                        rationale = f"CRITICAL: Substantive benchmark prompt inquiry leakage detected from {q_id}."

                matches.append(
                    ContaminationMatch(
                        matched_ngram=ng,
                        match_origin=origin,
                        benchmark_question_id=q_id,
                        benchmark_version=self.benchmark_version,
                        char_start=char_start,
                        char_end=char_end,
                        matched_snippet=matched_snippet,
                        is_bibliographic_title=is_bib,
                        is_genuine_leakage=is_leak,
                        decision_rationale=rationale,
                    )
                )
                if len(matches) >= 10:
                    break

        has_genuine_leakage = any(m.is_genuine_leakage for m in matches)
        has_bib = any(m.is_bibliographic_title for m in matches)
        is_contaminated = has_genuine_leakage

        if is_contaminated:
            leak_qids = sorted(list({m.benchmark_question_id for m in matches if m.is_genuine_leakage}))
            decision_rationale = (
                f"QUARANTINE: Genuine benchmark contamination detected ({len(matches)} match(es) "
                f"affecting items: {', '.join(leak_qids)})."
            )
        elif has_bib:
            bib_qids = sorted(list({m.benchmark_question_id for m in matches if m.is_bibliographic_title}))
            decision_rationale = (
                f"ACCEPTED: Harmless publication title reference matched ({len(matches)} match(es) "
                f"affecting items: {', '.join(bib_qids)}). No question or answer leakage."
            )
        else:
            decision_rationale = "ACCEPTED: Zero benchmark n-gram matches."

        return ContaminationCheckResult(
            is_contaminated=is_contaminated,
            has_bibliographic_match=has_bib,
            matches=matches,
            decision_rationale=decision_rationale,
            benchmark_version=self.benchmark_version,
        )


# =============================================================================
# 8. Deduplication Engine (Exact SHA-256 and Near-Duplicate Jaccard)
# =============================================================================

@dataclass
class DeduplicationResult:
    """Result of running exact and near-duplicate detection."""

    total_input: int
    retained_count: int
    exact_duplicates_dropped: int
    near_duplicates_found: int
    clusters_formed: int
    drop_details: List[Dict[str, str]] = field(default_factory=list)


class CorpusDeduplicator:
    """Performs exact and near-duplicate detection with persistent resumable state."""

    def __init__(self, near_dup_threshold: float = 0.85, shingle_k: int = 5):
        self.near_dup_threshold = near_dup_threshold
        self.shingle_k = shingle_k
        self.seen_exact_hashes: Dict[str, str] = {}  # norm_hash -> doc_id

    def compute_norm_hash(self, text: str) -> str:
        norm = re.sub(r"\s+", " ", text.strip().lower())
        return hashlib.sha256(norm.encode("utf-8")).hexdigest()

    def get_shingles(self, text: str) -> Set[str]:
        norm = re.sub(r"\s+", " ", text.strip().lower())
        if len(norm) < self.shingle_k:
            return {norm}
        return {norm[i : i + self.shingle_k] for i in range(len(norm) - self.shingle_k + 1)}

    def deduplicate(
        self,
        documents: List[NormalizedDocument],
    ) -> Tuple[List[NormalizedDocument], DeduplicationResult]:
        """Detect and drop exact duplicates, and cluster near-duplicates under shared group_ids."""
        retained: List[NormalizedDocument] = []
        drop_details: List[Dict[str, str]] = []
        exact_drops = 0

        # Step 1: Exact hash filtering
        for doc in documents:
            h = self.compute_norm_hash(doc.text)
            if h in self.seen_exact_hashes:
                exact_drops += 1
                drop_details.append({
                    "dropped_doc_id": doc.doc_id,
                    "duplicate_of": self.seen_exact_hashes[h],
                    "reason": "Exact normalized text SHA-256 match",
                })
            else:
                self.seen_exact_hashes[h] = doc.doc_id
                retained.append(doc)

        n = len(retained)
        if n == 0:
            return [], DeduplicationResult(len(documents), 0, exact_drops, 0, 0, drop_details)

        # Step 2: Near-duplicate clustering via shingles
        doc_ids = [d.doc_id for d in retained]
        parent = {did: did for did in doc_ids}

        def find(i: str) -> str:
            if parent[i] != i:
                parent[i] = find(parent[i])
            return parent[i]

        def union(i: str, j: str):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                parent[root_i] = root_j

        # If documents already shared group_id, link them
        group_map: Dict[str, List[str]] = {}
        for d in retained:
            group_map.setdefault(d.group_id, []).append(d.doc_id)
        for members in group_map.values():
            if len(members) > 1:
                for m in members[1:]:
                    union(members[0], m)

        shingles_list = [self.get_shingles(d.text) for d in retained]
        lens = [len(s) for s in shingles_list]
        near_dups = 0

        for i in range(n):
            s1 = shingles_list[i]
            l1 = lens[i]
            for j in range(i + 1, n):
                l2 = lens[j]
                if l1 < l2:
                    if (l1 / l2) < self.near_dup_threshold:
                        continue
                else:
                    if (l2 / l1) < self.near_dup_threshold:
                        continue
                s2 = shingles_list[j]
                inter = len(s1 & s2)
                if inter == 0:
                    continue
                union_len = l1 + l2 - inter
                sim = inter / union_len if union_len > 0 else 0.0
                if sim >= self.near_dup_threshold:
                    near_dups += 1
                    union(doc_ids[i], doc_ids[j])

        # Assign cluster group_ids
        cluster_map = {did: find(did) for did in doc_ids}
        unique_clusters = set(cluster_map.values())
        for doc in retained:
            doc.group_id = cluster_map[doc.doc_id]

        result = DeduplicationResult(
            total_input=len(documents),
            retained_count=len(retained),
            exact_duplicates_dropped=exact_drops,
            near_duplicates_found=near_dups,
            clusters_formed=len(unique_clusters),
            drop_details=drop_details,
        )
        return retained, result


# =============================================================================
# 9. Source-Level and Group-Aware Partitioning
# =============================================================================

def source_level_split(
    documents: List[NormalizedDocument],
    val_ratio: float = 0.15,
    seed: int = 42,
) -> Tuple[List[NormalizedDocument], List[NormalizedDocument]]:
    """Partition documents into train and val at the publication, source, and duplicate-cluster level.

    Guarantees:
    - Zero source cross-contamination (set(train_source_ids).isdisjoint(set(validation_source_ids)) is strictly True).
    - Zero parent-publication cross-contamination (set(train_parent_ids).isdisjoint(set(validation_parent_ids)) is strictly True).
    - If multiple documents or chapters share a parent publication (parent_source_id), every chapter remains in the same partition.
    - Near-duplicate groups never cross partitions (documents in the same cluster remain in the same partition).
    - Deterministic reproducibility with random seed.
    """
    if not documents:
        return [], []
    if val_ratio <= 0.0:
        return list(documents), []

    import numpy as np

    rng = np.random.RandomState(seed)

    # 1. Disjoint Set Union (Connected Components) linking sources, parent publications, and duplicate groups
    parent: Dict[str, str] = {}

    def find(x: str) -> str:
        if x not in parent:
            parent[x] = x
            return x
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: str, y: str) -> None:
        rx, ry = find(x), find(y)
        if rx != ry:
            # Deterministic union pointing higher string to lower string
            if rx < ry:
                parent[ry] = rx
            else:
                parent[rx] = ry

    for doc in documents:
        src_node = f"SRC::{doc.source_id}"
        p_id = doc.parent_source_id or doc.source_id
        parent_node = f"PARENT::{p_id}"
        find(src_node)
        find(parent_node)
        union(src_node, parent_node)
        if doc.group_id:
            grp_node = f"GRP::{doc.group_id}"
            find(grp_node)
            union(src_node, grp_node)

    # 2. Group documents by connected component root
    clusters: Dict[str, List[NormalizedDocument]] = {}
    for doc in documents:
        root = find(f"SRC::{doc.source_id}")
        clusters.setdefault(root, []).append(doc)

    sorted_roots = sorted(list(clusters.keys()))

    # If only 1 component exists, all documents must remain together to prevent source leakage
    if len(sorted_roots) <= 1:
        return list(documents), []

    # 3. Deterministically shuffle cluster roots
    shuffled_roots = list(sorted_roots)
    rng.shuffle(shuffled_roots)

    # 4. Allocate clusters to validation aiming for val_ratio of total documents
    total_docs = len(documents)
    target_val_docs = total_docs * val_ratio

    val_roots: Set[str] = set()
    current_val_docs = 0

    # Never allocate a single dominant cluster representing >=50% of the entire corpus to val
    # unless val_ratio >= 0.5.
    max_single_cluster_ratio = 0.5 if val_ratio < 0.5 else 1.0

    for r in shuffled_roots:
        count = len(clusters[r])
        if count >= total_docs * max_single_cluster_ratio and val_ratio < 0.5:
            continue
        # Leave at least 1 cluster for train
        if len(val_roots) + 1 >= len(shuffled_roots):
            break
        if current_val_docs == 0 or (current_val_docs + count <= target_val_docs * 1.5):
            val_roots.add(r)
            current_val_docs += count
            if current_val_docs >= target_val_docs:
                break

    # If no cluster was added and val_ratio > 0 and len(shuffled_roots) >= 2,
    # pick the smallest cluster (that is < total_docs) for validation
    if not val_roots and val_ratio > 0 and len(shuffled_roots) >= 2:
        eligible = [r for r in sorted_roots if len(clusters[r]) < total_docs]
        if eligible:
            smallest_root = min(eligible, key=lambda k: len(clusters[k]))
            val_roots.add(smallest_root)

    train_docs: List[NormalizedDocument] = []
    val_docs: List[NormalizedDocument] = []

    for r in sorted_roots:
        if r in val_roots:
            val_docs.extend(clusters[r])
        else:
            train_docs.extend(clusters[r])

    # Strict Invariant Verification
    train_srcs = {d.source_id for d in train_docs}
    val_srcs = {d.source_id for d in val_docs}
    assert train_srcs.isdisjoint(val_srcs), f"Source ID leakage detected: {train_srcs & val_srcs}"

    train_parents = {d.parent_source_id for d in train_docs if d.parent_source_id}
    val_parents = {d.parent_source_id for d in val_docs if d.parent_source_id}
    assert train_parents.isdisjoint(val_parents), f"Parent publication leakage detected: {train_parents & val_parents}"

    train_grps = {d.group_id for d in train_docs if d.group_id}
    val_grps = {d.group_id for d in val_docs if d.group_id}
    assert train_grps.isdisjoint(val_grps), f"Duplicate group leakage detected: {train_grps & val_grps}"

    return train_docs, val_docs


# =============================================================================
# 10. Ingestion State & Audit Manifest
# =============================================================================

@dataclass
class PillarCoverageStats:
    """Document and token distribution for a single pillar."""

    pillar: str
    display_name: str
    doc_count: int
    char_count: int
    word_count: int
    token_count: int
    token_percentage: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Phase10Manifest:
    """Cryptographic manifest and audit report for Phase 10 corpus expansion."""

    version: str = "10.0.0"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    authoritative_tokenizer_hash: str = ""
    authoritative_tokenizer_vocab_size: int = 3384
    total_raw_sources_registered: int = 0
    total_documents_ingested: int = 0
    total_documents_approved: int = 0
    total_documents_quarantined: int = 0
    total_training_tokens: int = 0
    total_validation_tokens: int = 0
    total_combined_tokens: int = 0
    pillar_coverage: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    deduplication_summary: Dict[str, Any] = field(default_factory=dict)
    safety_summary: Dict[str, Any] = field(default_factory=dict)
    approved_source_manifest: List[Dict[str, Any]] = field(default_factory=list)
    quarantine_manifest: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def save(self, path: Union[str, Path]) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)


# =============================================================================
# 11. End-to-End Source Ingestion Pipeline
# =============================================================================

class SourceIngestionPipeline:
    """End-to-end responsible source ingestion pipeline for Project NOVA."""

    def __init__(
        self,
        tokenizer: Optional[NovaTokenizer] = None,
        benchmark: Optional[FitnessEvaluationBenchmark] = None,
        source_registry: Optional[SourceRegistry] = None,
        state_file: Optional[Path] = None,
    ):
        self.tokenizer = tokenizer
        self.benchmark = benchmark
        self.source_registry = source_registry or SourceRegistry()
        self.safety_screener = HealthSafetyScreener()
        self.contamination_detector = BenchmarkContaminationDetector(benchmark)
        self.deduplicator = CorpusDeduplicator()
        self.state_file = state_file

        # State tracking
        self.ingested_docs: Dict[str, NormalizedDocument] = {}
        self.quarantined_docs: Dict[str, NormalizedDocument] = {}
        self.load_state()

    def load_state(self) -> None:
        """Load previously processed document IDs and hashes if resuming."""
        if self.state_file and self.state_file.is_file():
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for d_data in data.get("approved_docs", []):
                    doc = NormalizedDocument.from_dict(d_data)
                    self.ingested_docs[doc.doc_id] = doc
                    self.deduplicator.seen_exact_hashes[
                        self.deduplicator.compute_norm_hash(doc.text)
                    ] = doc.doc_id
                for q_data in data.get("quarantined_docs", []):
                    doc = NormalizedDocument.from_dict(q_data)
                    self.quarantined_docs[doc.doc_id] = doc
            except Exception as e:
                print(f"[Pipeline] Warning loading state file: {e}")

    def save_state(self) -> None:
        """Save current ingestion state to allow safe resumption."""
        if not self.state_file:
            return
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "approved_count": len(self.ingested_docs),
            "quarantined_count": len(self.quarantined_docs),
            "approved_docs": [d.to_dict() for d in self.ingested_docs.values()],
            "quarantined_docs": [d.to_dict() for d in self.quarantined_docs.values()],
        }
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def ingest_file(
        self,
        file_path: Union[str, Path],
        source_metadata: Dict[str, Any],
        allow_human_override: bool = False,
        reviewer_id: str = "",
        reviewer_notes: str = "",
    ) -> List[NormalizedDocument]:
        """Ingest a single source file through the complete legal, safety, and hygiene pipeline."""
        p = Path(file_path)
        if not p.is_file():
            raise FileNotFoundError(f"Input file not found: {p}")

        raw_bytes = p.read_bytes()
        raw_sha256 = hashlib.sha256(raw_bytes).hexdigest()

        # Step 1: Legal & Licensing Audit
        license_name = source_metadata.get("license", "Unknown")
        legal_basis = source_metadata.get("legal_basis", "")
        gate = audit_license(
            license_name=license_name,
            legal_basis=legal_basis,
            allow_human_override=allow_human_override,
            reviewer_id=reviewer_id,
            reviewer_notes=reviewer_notes,
            is_us_gov_employee_work=source_metadata.get("is_us_gov_employee_work"),
            has_third_party_copyright=source_metadata.get("has_third_party_copyright"),
            third_party_exclusions=source_metadata.get("third_party_exclusions", ""),
            text_content=raw_bytes.decode("utf-8", errors="ignore"),
        )

        source_id = source_metadata.get("source_id", p.stem.upper())
        pillar = normalize_pillar(source_metadata.get("pillar", FitnessPillar.PILLAR_1_PHYSIOLOGY)).value

        if not gate.is_compliant:
            # Source is REJECTED or QUARANTINED at the licensing gate
            quarantine_doc = NormalizedDocument(
                doc_id=f"REJ-{source_id}-{p.stem}",
                source_id=source_id,
                parent_source_id=source_metadata.get("parent_source_id", source_id),
                canonical_source_url=source_metadata.get("canonical_source_url", source_metadata.get("url", "")),
                title=source_metadata.get("title", p.name),
                text="",
                pillar=pillar,
                author=source_metadata.get("author", ""),
                publisher=source_metadata.get("publisher", ""),
                publication_date=source_metadata.get("publication_date", ""),
                retrieval_date=source_metadata.get("retrieval_date", datetime.now(timezone.utc).strftime("%Y-%m-%d")),
                url=source_metadata.get("url", ""),
                license=license_name,
                legal_basis=legal_basis,
                raw_sha256=raw_sha256,
                ingestion_status=IngestionStatus.REJECTED,
                review_notes=f"Licensing rejection: {gate.rejection_reason}",
            )
            self.quarantined_docs[quarantine_doc.doc_id] = quarantine_doc
            self.save_state()
            return []

        # Step 2: Format-specific text extraction
        ext = p.suffix.lower()
        extracted_text = ""
        extraction_method = "plain_text"

        if ext in {".html", ".htm"}:
            extracted_text = extract_text_from_html(raw_bytes.decode("utf-8", errors="ignore"))
            extraction_method = "html_parser"
        elif ext in {".md", ".markdown"}:
            extracted_text = extract_text_from_markdown(raw_bytes.decode("utf-8", errors="ignore"))
            extraction_method = "markdown_parser"
        elif ext == ".pdf":
            extracted_text = extract_text_from_pdf_stream(raw_bytes)
            extraction_method = "pdf_text_extractor"
            if extracted_text == "SCANNED_PDF_REQUIRING_OCR":
                quarantine_doc = NormalizedDocument(
                    doc_id=f"QUAR-{source_id}-{p.stem}",
                    source_id=source_id,
                    parent_source_id=source_metadata.get("parent_source_id", source_id),
                    canonical_source_url=source_metadata.get("canonical_source_url", source_metadata.get("url", "")),
                    title=source_metadata.get("title", p.name),
                    text="",
                    pillar=pillar,
                    author=source_metadata.get("author", ""),
                    publisher=source_metadata.get("publisher", ""),
                    publication_date=source_metadata.get("publication_date", ""),
                    retrieval_date=source_metadata.get("retrieval_date", datetime.now(timezone.utc).strftime("%Y-%m-%d")),
                    url=source_metadata.get("url", ""),
                    license=license_name,
                    legal_basis=legal_basis,
                    raw_sha256=raw_sha256,
                    extraction_method=extraction_method,
                    ingestion_status=IngestionStatus.QUARANTINED,
                    review_notes="SCANNED_PDF_REQUIRING_OCR: Scanned or raster image PDF detected without extractable text streams. Optical Character Recognition (OCR) is required.",
                )
                self.quarantined_docs[quarantine_doc.doc_id] = quarantine_doc
                self.save_state()
                return []
        elif ext in {".json", ".jsonl"}:
            # Handle structured JSON document lists
            extraction_method = "json_manifest"
            extracted_docs: List[NormalizedDocument] = []
            try:
                data = json.loads(raw_bytes.decode("utf-8"))
                doc_list = data if isinstance(data, list) else data.get("documents", [data])
                for idx, item in enumerate(doc_list):
                    sub_meta = copy.deepcopy(source_metadata)
                    sub_meta.update(item)
                    sub_text = item.get("text", "")
                    cleaned_sub = normalize_corpus_text(sub_text)
                    ok, reason = assess_text_quality(cleaned_sub)
                    if not ok:
                        continue
                    doc = self._process_document_text(
                        doc_id=item.get("doc_id", f"{source_id}_{idx:04d}"),
                        title=item.get("title", item.get("section_title", f"Section {idx+1}")),
                        text=cleaned_sub,
                        source_id=source_id,
                        pillar=pillar,
                        source_metadata=sub_meta,
                        extraction_method=extraction_method,
                        raw_sha256=raw_sha256,
                    )
                    if doc:
                        extracted_docs.append(doc)
                self.save_state()
                return extracted_docs
            except Exception as e:
                extracted_text = f"JSON extraction error: {e}"
        else:
            # Fallback plain text
            extracted_text = raw_bytes.decode("utf-8", errors="ignore")
            extraction_method = "plain_text"

        # Step 3: Text Normalization & Quality Assessment
        cleaned_text = normalize_corpus_text(extracted_text)
        is_ok, quality_reason = assess_text_quality(cleaned_text)

        if not is_ok:
            quarantine_doc = NormalizedDocument(
                doc_id=f"QUAR-{source_id}-{p.stem}",
                source_id=source_id,
                parent_source_id=source_metadata.get("parent_source_id", source_id),
                canonical_source_url=source_metadata.get("canonical_source_url", source_metadata.get("url", "")),
                title=source_metadata.get("title", p.name),
                text=cleaned_text[:500],
                pillar=pillar,
                author=source_metadata.get("author", ""),
                publisher=source_metadata.get("publisher", ""),
                publication_date=source_metadata.get("publication_date", ""),
                retrieval_date=source_metadata.get("retrieval_date", datetime.now(timezone.utc).strftime("%Y-%m-%d")),
                url=source_metadata.get("url", ""),
                license=license_name,
                legal_basis=legal_basis,
                raw_sha256=raw_sha256,
                ingestion_status=IngestionStatus.QUARANTINED,
                review_notes=f"Quality rejection: {quality_reason}",
            )
            self.quarantined_docs[quarantine_doc.doc_id] = quarantine_doc
            self.save_state()
            return []

        doc = self._process_document_text(
            doc_id=source_metadata.get("doc_id", f"{source_id}_{p.stem}"),
            title=source_metadata.get("title", p.name),
            text=cleaned_text,
            source_id=source_id,
            pillar=pillar,
            source_metadata=source_metadata,
            extraction_method=extraction_method,
            raw_sha256=raw_sha256,
        )
        self.save_state()
        return [doc] if doc else []

    def _process_document_text(
        self,
        doc_id: str,
        title: str,
        text: str,
        source_id: str,
        pillar: str,
        source_metadata: Dict[str, Any],
        extraction_method: str,
        raw_sha256: str,
    ) -> Optional[NormalizedDocument]:
        """Run a document through safety screening, benchmark check, deduplication, and token counting."""
        # Step 1: Health & Safety Screening
        safety_flags = self.safety_screener.screen_text(text)
        critical_flags = [f for f in safety_flags if f.get("severity") in ("CRITICAL", "HIGH")]

        # Step 2: Benchmark Contamination Screening
        check_res = self.contamination_detector.check_text(text)
        is_contaminated = check_res.is_contaminated
        contamination_matches = check_res.to_summary_strings()

        status = IngestionStatus.APPROVED
        notes = []

        if is_contaminated:
            status = IngestionStatus.QUARANTINED
            notes.append(f"BENCHMARK CONTAMINATION: {'; '.join(contamination_matches)}")
        elif check_res.has_bibliographic_match:
            bib_matches = [f"{m.matched_snippet} ({m.benchmark_question_id})" for m in check_res.matches if m.is_bibliographic_title]
            notes.append(f"BIBLIOGRAPHIC_CITATION_MATCH: {'; '.join(bib_matches)}")

        if critical_flags:
            status = IngestionStatus.QUARANTINED
            notes.append(f"SAFETY HAZARD: {len(critical_flags)} high/critical risk claims flagged.")

        # Step 3: Exact Deduplication Check
        norm_h = self.deduplicator.compute_norm_hash(text)
        if norm_h in self.deduplicator.seen_exact_hashes:
            dup_id = self.deduplicator.seen_exact_hashes[norm_h]
            # Exact duplicate found; do not re-ingest duplicate
            return None

        # Step 4: Token Counting with authoritative tokenizer
        token_count = 0
        if self.tokenizer:
            formatted = f"[SECTION: {title}]\n[SOURCE: {source_id}]\n{text.strip()}"
            token_count = len(self.tokenizer.encode(formatted, allow_special=False))

        doc = NormalizedDocument(
            doc_id=doc_id,
            source_id=source_id,
            parent_source_id=source_metadata.get("parent_source_id", source_id),
            canonical_source_url=source_metadata.get("canonical_source_url", source_metadata.get("url", "")),
            title=title,
            text=text,
            pillar=pillar,
            authoring_method=AuthoringMethod(source_metadata.get("authoring_method", AuthoringMethod.PRIMARY_SOURCE_EXTRACT.value)),
            author=source_metadata.get("author", ""),
            publisher=source_metadata.get("publisher", ""),
            publication_date=source_metadata.get("publication_date", ""),
            retrieval_date=source_metadata.get("retrieval_date", datetime.now(timezone.utc).strftime("%Y-%m-%d")),
            url=source_metadata.get("url", ""),
            license=source_metadata.get("license", "Public Domain"),
            legal_basis=source_metadata.get("legal_basis", "17 U.S.C. § 105"),
            attribution_required=bool(source_metadata.get("attribution_required", False)),
            attribution_text=source_metadata.get("mandatory_attribution_text", source_metadata.get("attribution_text", "")),
            extraction_method=extraction_method,
            raw_sha256=raw_sha256,
            group_id=source_metadata.get("group_id", source_id),
            token_count=token_count,
            safety_flags=safety_flags,
            benchmark_contamination=is_contaminated,
            benchmark_matches=[m.to_dict() for m in check_res.matches],
            ingestion_status=status,
            review_notes="; ".join(notes),
            transformation_history=[
                "multi_format_extraction",
                "nfkc_unicode_normalization",
                "boilerplate_strip",
                "safety_claim_screen",
                "benchmark_contamination_check",
            ],
        )

        if status == IngestionStatus.APPROVED:
            self.deduplicator.seen_exact_hashes[norm_h] = doc.doc_id
            self.ingested_docs[doc.doc_id] = doc
            return doc
        else:
            self.quarantined_docs[doc.doc_id] = doc
            return None

    def generate_manifest(self) -> Phase10Manifest:
        """Compute full per-pillar coverage, quality reports, and produce a Phase10Manifest."""
        approved = list(self.ingested_docs.values())
        quarantined = list(self.quarantined_docs.values())

        # Group by pillar
        pillar_counts: Dict[str, Dict[str, Any]] = {}
        total_tokens = sum(d.token_count for d in approved)

        for p in FitnessPillar:
            p_docs = [d for d in approved if d.pillar == p.value]
            p_tokens = sum(d.token_count for d in p_docs)
            p_chars = sum(d.char_count for d in p_docs)
            p_words = sum(d.word_count for d in p_docs)
            pct = (p_tokens / total_tokens * 100.0) if total_tokens > 0 else 0.0

            stat = PillarCoverageStats(
                pillar=p.value,
                display_name=PILLAR_DISPLAY_NAMES[p],
                doc_count=len(p_docs),
                char_count=p_chars,
                word_count=p_words,
                token_count=p_tokens,
                token_percentage=round(pct, 2),
            )
            pillar_counts[p.value] = stat.to_dict()

        tok_hash = ""
        tok_vocab = 3384
        if self.tokenizer:
            tok_vocab = self.tokenizer.vocab_size

        manifest = Phase10Manifest(
            authoritative_tokenizer_hash=tok_hash,
            authoritative_tokenizer_vocab_size=tok_vocab,
            total_raw_sources_registered=len(set(d.source_id for d in approved)),
            total_documents_ingested=len(approved) + len(quarantined),
            total_documents_approved=len(approved),
            total_documents_quarantined=len(quarantined),
            total_combined_tokens=total_tokens,
            pillar_coverage=pillar_counts,
            deduplication_summary={
                "exact_hashes_indexed": len(self.deduplicator.seen_exact_hashes),
            },
            safety_summary={
                "total_quarantined": len(quarantined),
                "quarantine_reasons": [q.review_notes for q in quarantined if q.review_notes],
            },
            approved_source_manifest=[d.to_dict() for d in approved],
            quarantine_manifest=[q.to_dict() for q in quarantined],
        )
        return manifest
