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
