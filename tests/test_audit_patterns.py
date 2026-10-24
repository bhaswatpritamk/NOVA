"""Tests for Phase 11.4 extraction metric patterns and audit invariants."""

import pytest
from scripts.audit_boundary_quality import (
    REF_LIST_PATTERN,
    TOC_PATTERN,
    RUNNING_HEADER_PATTERN,
    SOURCE_ADAPTED_PATTERN,
    PAGE_NUMBER_PATTERN,
)


def test_cardiometabolic_citation_fixture():
    """A3 requirement: repair pattern and verify exact numbered citation line matches."""
    citation_fixture = (
        "90. Shen D, Mao W, Liu T, et al. Sedentary behavior and incident cancer: "
        "a meta-analysis of prospective"
    )
    assert REF_LIST_PATTERN.search(citation_fixture) is not None, (
        f"REF_LIST_PATTERN failed to match citation fixture: {citation_fixture}"
    )


def test_cardiometabolic_toc_dot_leader_fixture():
    """A3 requirement: repair pattern and verify exact TOC dot leader line matches."""
    toc_fixture = (
        "Question 1. What is the relationship between physical activity and prevention of "
        "weight gain? ...... F5-4"
    )
    assert TOC_PATTERN.search(toc_fixture) is not None, (
        f"TOC_PATTERN failed to match TOC dot leader fixture: {toc_fixture}"
    )


def test_ref_pattern_numbered_and_doi():
    """Verify various forms of citations match."""
    assert REF_LIST_PATTERN.search("1. Physical Activity Guidelines Advisory Committee.") is not None
    assert REF_LIST_PATTERN.search("84. Giné-Garriga M, Roqué-Fíguls M, Coll-Planas L, et al.") is not None
    assert REF_LIST_PATTERN.search("doi:10.1371/journal.pone.0105709.") is not None
    assert REF_LIST_PATTERN.search("[12] Smith J. Journal of Science 2020;12:34-56") is not None


def test_toc_pattern_variations():
    """Verify variations of dot leaders match."""
    assert TOC_PATTERN.search("Introduction ....................................... F5-1") is not None
    assert TOC_PATTERN.search("Review of the Science . . . . . . . . . . . . . . . F5-3") is not None
    assert TOC_PATTERN.search("Normal text without dot leaders") is None


def test_keyword_counter_repair_fixtures():
    """Phase 11.5 requirement: Unit tests with fixtures: 'Falls', 'falls', 'Injury', 'Sleep', 'muscle‑strengthening' (non-breaking hyphen)."""
    from scripts.audit_pillar_keywords import REGEX_SETS, normalize_keyword_text

    # Injury regex set tests (case-insensitivity)
    assert REGEX_SETS["injury"].search(normalize_keyword_text("Falls")) is not None
    assert REGEX_SETS["injury"].search(normalize_keyword_text("falls")) is not None
    assert REGEX_SETS["injury"].search(normalize_keyword_text("Injury")) is not None

    # Sleep regex set test (case-insensitivity)
    assert REGEX_SETS["sleep"].search(normalize_keyword_text("Sleep")) is not None
    assert REGEX_SETS["sleep"].search(normalize_keyword_text("sleep")) is not None

    # Strength regex set tests (muscle-strengthening variants, non-breaking hyphen U+2011)
    non_breaking_hyphen_fixture = "muscle\u2011strengthening"
    assert "\u2011" in non_breaking_hyphen_fixture
    normalized = normalize_keyword_text(non_breaking_hyphen_fixture)
    assert normalized == "muscle-strengthening"
    assert REGEX_SETS["strength"].search(normalized) is not None

    # Space variant equals hyphen variant
    assert REGEX_SETS["strength"].search(normalize_keyword_text("muscle strengthening")) is not None
    assert REGEX_SETS["strength"].search(normalize_keyword_text("muscle-strengthening")) is not None

    # All unicode hyphens U+2010 through U+2015 and U+2212
    for uchar in ["\u2010", "\u2011", "\u2012", "\u2013", "\u2014", "\u2015", "\u2212"]:
        sample = f"muscle{uchar}strengthening"
        norm = normalize_keyword_text(sample)
        assert norm == "muscle-strengthening"
        assert REGEX_SETS["strength"].search(norm) is not None

