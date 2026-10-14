"""Script to build, verify, deduplicate, partition, and prepare the expanded Nova-Fit corpus.

Executes the end-to-end Phase 6 data pipeline:
1. Establishes raw source repository in data/sources_raw/ with exact SHA-256 hashes.
2. Updates data/approved/source_registry.json with legal provenance for all approved sources.
3. Ingests all educational documents across all 7 Nova-Fit pillars.
4. Performs exact and near-duplicate detection with cluster grouping.
5. Performs group-aware train/val partitioning with zero split leakage.
6. Asserts training token volume >= 100,000 tokens using artifacts/final_tokenizer.
7. Exports data/approved/expanded_train_corpus.txt and expanded_val_corpus.txt.
8. Prepares PyTorch dataset tensors in data/prepared_expanded/ with tokenizer verification.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from typing import Any, Dict, List

from nova.corpus import (
    CorpusDocument,
    SourceProvenanceRecord,
    SourceRegistry,
    calculate_split_statistics,
    detect_duplicates_and_group,
    partition_documents_by_group,
)
from nova.data import (
    PrepareDatasetConfig,
    PrepareDatasetResult,
    compute_file_sha256,
    prepare_dataset,
)
from nova.tokenizer import NovaTokenizer
from scripts.sources import get_all_documents


APPROVED_SOURCES_METADATA: List[Dict[str, Any]] = [
    {
        "source_id": "US-HHS-PAG-2018",
        "title": "Physical Activity Guidelines for Americans, 2nd Edition",
        "author": "U.S. Department of Health and Human Services",
        "publication_year": 2018,
        "license": "Public Domain",
        "legal_basis": "U.S. Government Work under 17 U.S.C. § 105",
        "commercial_use_permitted": True,
        "attribution_required": False,
        "attribution_text": "Sourced from U.S. Department of Health and Human Services, Physical Activity Guidelines for Americans, 2nd edition.",
        "url": "https://health.gov/our-work/nutrition-physical-activity/physical-activity-guidelines",
        "domains": ["general_fitness_education_safety", "strength_training_programming", "sleep_recovery_physical_activity"],
        "restrictions": "No endorsement by HHS implied.",
    },
    {
        "source_id": "US-HHS-PAGAC-REPORT",
        "title": "Physical Activity Guidelines Advisory Committee Scientific Report",
        "author": "U.S. Department of Health and Human Services",
        "publication_year": 2018,
        "license": "Public Domain",
        "legal_basis": "U.S. Government Work under 17 U.S.C. § 105",
        "commercial_use_permitted": True,
        "attribution_required": False,
        "attribution_text": "2018 Physical Activity Guidelines Advisory Committee Scientific Report. Washington, DC: U.S. Department of Health and Human Services.",
        "url": "https://health.gov/our-work/nutrition-physical-activity/physical-activity-guidelines/current-guidelines/scientific-report",
        "domains": ["exercise_science_biomechanics", "training_adaptations_fatigue_load"],
        "restrictions": "No endorsement by HHS implied.",
    },
    {
        "source_id": "US-HHS-PAGAC-2018",
        "title": "Physical Activity Guidelines Advisory Committee Scientific Report (Cardiovascular)",
        "author": "U.S. Department of Health and Human Services",
        "publication_year": 2018,
        "license": "Public Domain",
        "legal_basis": "U.S. Government Work under 17 U.S.C. § 105",
        "commercial_use_permitted": True,
        "attribution_required": False,
        "attribution_text": "2018 Physical Activity Guidelines Advisory Committee. Washington, DC: U.S. Department of Health and Human Services.",
        "url": "https://health.gov/our-work/nutrition-physical-activity/physical-activity-guidelines",
        "domains": ["exercise_science_biomechanics"],
        "restrictions": "No endorsement by HHS implied.",
    },
    {
        "source_id": "US-CDC-PA-2022",
        "title": "CDC Physical Activity Basics and Recommendations",
        "author": "Centers for Disease Control and Prevention",
        "publication_year": 2022,
        "license": "Public Domain",
        "legal_basis": "U.S. Government Work under 17 U.S.C. § 105",
        "commercial_use_permitted": True,
        "attribution_required": False,
        "attribution_text": "Centers for Disease Control and Prevention (CDC). Physical Activity Basics.",
        "url": "https://www.cdc.gov/physicalactivity/basics/index.htm",
        "domains": ["general_fitness_education_safety"],
        "restrictions": "No endorsement by CDC implied.",
    },
    {
        "source_id": "US-CDC-RTG-2023",
        "title": "CDC Guidelines on Muscle-Strengthening Physical Activity",
        "author": "Centers for Disease Control and Prevention",
        "publication_year": 2023,
        "license": "Public Domain",
        "legal_basis": "U.S. Government Work under 17 U.S.C. § 105",
        "commercial_use_permitted": True,
        "attribution_required": False,
        "attribution_text": "Centers for Disease Control and Prevention. Muscle-Strengthening Physical Activity.",
        "url": "https://www.cdc.gov/physicalactivity/basics/adults/index.htm",
        "domains": ["strength_training_programming", "general_fitness_education_safety"],
        "restrictions": "No endorsement by CDC implied.",
    },
    {
        "source_id": "US-CDC-SLEEP-2022",
        "title": "Sleep and Sleep Disorders: Recovery and Health Promotion",
        "author": "Centers for Disease Control and Prevention",
        "publication_year": 2022,
        "license": "Public Domain",
        "legal_basis": "U.S. Government Work under 17 U.S.C. § 105",
        "commercial_use_permitted": True,
        "attribution_required": False,
        "attribution_text": "Centers for Disease Control and Prevention. Sleep and Sleep Disorders.",
        "url": "https://www.cdc.gov/sleep/index.html",
        "domains": ["sleep_recovery_physical_activity"],
        "restrictions": "No endorsement by CDC implied.",
    },
    {
        "source_id": "US-CDC-HYDRATION-2022",
        "title": "Water and Healthier Drinks: Hydration Fundamentals",
        "author": "Centers for Disease Control and Prevention",
        "publication_year": 2022,
        "license": "Public Domain",
        "legal_basis": "U.S. Government Work under 17 U.S.C. § 105",
        "commercial_use_permitted": True,
        "attribution_required": False,
        "attribution_text": "Centers for Disease Control and Prevention. Water and Healthier Drinks.",
        "url": "https://www.cdc.gov/healthyweight/healthy_eating/water-and-healthier-drinks.html",
        "domains": ["nutrition_fundamentals_hydration"],
        "restrictions": "No endorsement by CDC implied.",
    },
    {
        "source_id": "CDC-NIOSH-HYDRATE",
        "title": "NIOSH Workplace Solutions: Preventing Heat Stress and Maintaining Hydration",
        "author": "National Institute for Occupational Safety and Health (NIOSH / CDC)",
        "publication_year": 2021,
        "license": "Public Domain",
        "legal_basis": "U.S. Government Work under 17 U.S.C. § 105",
        "commercial_use_permitted": True,
        "attribution_required": False,
        "attribution_text": "National Institute for Occupational Safety and Health (NIOSH). Preventing Heat Stress.",
        "url": "https://www.cdc.gov/niosh/topics/heatstress/",
        "domains": ["nutrition_fundamentals_hydration", "general_fitness_education_safety"],
        "restrictions": "No endorsement by CDC or NIOSH implied.",
    },
    {
        "source_id": "US-CDC-INJURY-PREV",
        "title": "CDC STEADI: Older Adult Fall Prevention and Clinical Practice",
        "author": "Centers for Disease Control and Prevention",
        "publication_year": 2022,
        "license": "Public Domain",
        "legal_basis": "U.S. Government Work under 17 U.S.C. § 105",
        "commercial_use_permitted": True,
        "attribution_required": False,
        "attribution_text": "Centers for Disease Control and Prevention. STEADI - Older Adult Fall Prevention.",
        "url": "https://www.cdc.gov/steadi/",
        "domains": ["general_fitness_education_safety"],
        "restrictions": "No endorsement by CDC implied.",
    },
    {
        "source_id": "USDA-HHS-DGA-2020",
        "title": "Dietary Guidelines for Americans, 2020-2025",
        "author": "U.S. Department of Agriculture & U.S. Department of Health and Human Services",
        "publication_year": 2020,
        "license": "Public Domain",
        "legal_basis": "U.S. Government Work under 17 U.S.C. § 105",
        "commercial_use_permitted": True,
        "attribution_required": False,
        "attribution_text": "U.S. Department of Agriculture and U.S. Department of Health and Human Services. Dietary Guidelines for Americans, 2020-2025. 9th Edition.",
        "url": "https://www.dietaryguidelines.gov/",
        "domains": ["nutrition_fundamentals_hydration"],
        "restrictions": "No endorsement by USDA or HHS implied.",
    },
    {
        "source_id": "US-ARMY-FM-7-22",
        "title": "Holistic Health and Fitness (FM 7-22)",
        "author": "Headquarters, Department of the Army",
        "publication_year": 2020,
        "license": "Public Domain",
        "legal_basis": "U.S. Government Work under 17 U.S.C. § 105",
        "commercial_use_permitted": True,
        "attribution_required": False,
        "attribution_text": "Headquarters, Department of the Army. Field Manual 7-22: Holistic Health and Fitness (October 2020). Distribution Unlimited.",
        "url": "https://armypubs.army.mil/ProductMaps/PubForm/Details.aspx?PUB_ID=1021134",
        "domains": [
            "strength_training_programming",
            "exercise_technique_safety",
            "sleep_recovery_physical_activity",
            "training_adaptations_fatigue_load",
            "general_fitness_education_safety",
        ],
        "restrictions": "Approved for public release; distribution is unlimited. No military endorsement claimed.",
    },
    {
        "source_id": "US-ARMY-ATP-7-22",
        "title": "Holistic Health and Fitness Drills and Exercises (ATP 7-22.02)",
        "author": "Headquarters, Department of the Army",
        "publication_year": 2020,
        "license": "Public Domain",
        "legal_basis": "U.S. Government Work under 17 U.S.C. § 105",
        "commercial_use_permitted": True,
        "attribution_required": False,
        "attribution_text": "Headquarters, Department of the Army. Army Techniques Publication 7-22.02: Holistic Health and Fitness Drills and Exercises (October 2020). Distribution Unlimited.",
        "url": "https://armypubs.army.mil/ProductMaps/PubForm/Details.aspx?PUB_ID=1021135",
        "domains": ["exercise_technique_safety", "strength_training_programming"],
        "restrictions": "Approved for public release; distribution is unlimited. No military endorsement claimed.",
    },
    {
        "source_id": "US-NIH-NHLBI-SLEEP",
        "title": "Your Guide to Healthy Sleep",
        "author": "National Institutes of Health, National Heart, Lung, and Blood Institute",
        "publication_year": 2021,
        "license": "Public Domain",
        "legal_basis": "U.S. Government Work under 17 U.S.C. § 105",
        "commercial_use_permitted": True,
        "attribution_required": False,
        "attribution_text": "National Institutes of Health, National Heart, Lung, and Blood Institute. Your Guide to Healthy Sleep. NIH Publication No. 11-5271.",
        "url": "https://www.nhlbi.nih.gov/health-topics/all-publications-and-resources/your-guide-healthy-sleep",
        "domains": ["sleep_recovery_physical_activity"],
        "restrictions": "No endorsement by NIH implied.",
    },
    {
        "source_id": "US-NIH-ODS-SUPP",
        "title": "Dietary Supplements for Exercise and Athletic Performance Fact Sheet",
        "author": "National Institutes of Health, Office of Dietary Supplements",
        "publication_year": 2022,
        "license": "Public Domain",
        "legal_basis": "U.S. Government Work under 17 U.S.C. § 105",
        "commercial_use_permitted": True,
        "attribution_required": False,
        "attribution_text": "National Institutes of Health, Office of Dietary Supplements. Dietary Supplements for Exercise and Athletic Performance.",
        "url": "https://ods.od.nih.gov/factsheets/ExerciseAndAthleticPerformance-HealthProfessional/",
        "domains": ["nutrition_fundamentals_hydration"],
        "restrictions": "No endorsement by NIH implied.",
    },
    {
        "source_id": "US-NIH-ODS-PERF",
        "title": "Performance Nutrition and Dietary Supplements Guidance",
        "author": "National Institutes of Health, Office of Dietary Supplements",
        "publication_year": 2022,
        "license": "Public Domain",
        "legal_basis": "U.S. Government Work under 17 U.S.C. § 105",
        "commercial_use_permitted": True,
        "attribution_required": False,
        "attribution_text": "National Institutes of Health, Office of Dietary Supplements.",
        "url": "https://ods.od.nih.gov/factsheets/ExerciseAndAthleticPerformance-HealthProfessional/",
        "domains": ["nutrition_fundamentals_hydration"],
        "restrictions": "No endorsement by NIH implied.",
    },
    {
        "source_id": "US-NIH-NIA-EXERCISE",
        "title": "Exercise & Physical Activity Guidelines for Older Adults",
        "author": "National Institutes of Health, National Institute on Aging",
        "publication_year": 2022,
        "license": "Public Domain",
        "legal_basis": "U.S. Government Work under 17 U.S.C. § 105",
        "commercial_use_permitted": True,
        "attribution_required": False,
        "attribution_text": "National Institutes of Health, National Institute on Aging. Exercise and Physical Activity: Getting Started.",
        "url": "https://www.nia.nih.gov/health/exercise-and-physical-activity",
        "domains": ["general_fitness_education_safety"],
        "restrictions": "No endorsement by NIH or NIA implied.",
    },
    {
        "source_id": "NIH-NIAMS-BIOMEC",
        "title": "Biomechanics of Musculoskeletal Health and Joint Mechanics",
        "author": "National Institutes of Health, NIAMS",
        "publication_year": 2021,
        "license": "Public Domain",
        "legal_basis": "U.S. Government Work under 17 U.S.C. § 105",
        "commercial_use_permitted": True,
        "attribution_required": False,
        "attribution_text": "National Institute of Arthritis and Musculoskeletal and Skin Diseases (NIAMS), NIH.",
        "url": "https://www.niams.nih.gov/health-topics",
        "domains": ["exercise_science_biomechanics"],
        "restrictions": "No endorsement by NIH implied.",
    },
    {
        "source_id": "NIAMS-SPORTS-SAFETY",
        "title": "Preventing Musculoskeletal Sports Injuries",
        "author": "National Institutes of Health, NIAMS",
        "publication_year": 2021,
        "license": "Public Domain",
        "legal_basis": "U.S. Government Work under 17 U.S.C. § 105",
        "commercial_use_permitted": True,
        "attribution_required": False,
        "attribution_text": "National Institute of Arthritis and Musculoskeletal and Skin Diseases (NIAMS), NIH.",
        "url": "https://www.niams.nih.gov/health-topics/sports-injuries",
        "domains": ["general_fitness_education_safety"],
        "restrictions": "No endorsement by NIH implied.",
    },
    {
        "source_id": "OPENSTAX-ANAT-PHYS-2E",
        "title": "Anatomy and Physiology 2e: Musculoskeletal and Neuromuscular Chapters",
        "author": "J. Gordon Betts et al. / OpenStax, Rice University",
        "publication_year": 2022,
        "license": "CC BY 4.0",
        "legal_basis": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
        "commercial_use_permitted": True,
        "attribution_required": True,
        "attribution_text": "Betts, J. G. et al. (2022). Anatomy and Physiology 2e. OpenStax, Rice University. Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). Available at: https://openstax.org/details/books/anatomy-and-physiology-2e",
        "url": "https://openstax.org/details/books/anatomy-and-physiology-2e",
        "domains": [
            "exercise_science_biomechanics",
            "strength_training_programming",
            "training_adaptations_fatigue_load",
        ],
        "restrictions": "Attribution must be retained in all derived documentation, manifests, and publications.",
    },
    {
        "source_id": "OPENSTAX-AP-MUSCLE",
        "title": "Anatomy and Physiology 2e: Chapter 10 Muscle Tissue",
        "author": "J. Gordon Betts et al. / OpenStax, Rice University",
        "publication_year": 2022,
        "license": "CC BY 4.0",
        "legal_basis": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
        "commercial_use_permitted": True,
        "attribution_required": True,
        "attribution_text": "Betts, J. G. et al. (2022). Anatomy and Physiology 2e. OpenStax, Rice University. Licensed under Creative Commons Attribution 4.0 International.",
        "url": "https://openstax.org/details/books/anatomy-and-physiology-2e",
        "domains": ["exercise_science_biomechanics"],
        "restrictions": "Attribution must be retained in all derived documentation and manifests.",
    },
    {
        "source_id": "US-NASA-EXERCISE-PHYSIOL",
        "title": "NASA Human Research Program Evidence Book: Risk of Impaired Performance Due to Reduced Muscle Mass, Strength, and Endurance",
        "author": "National Aeronautics and Space Administration (NASA)",
        "publication_year": 2021,
        "license": "Public Domain",
        "legal_basis": "U.S. Government Work under 17 U.S.C. § 105",
        "commercial_use_permitted": True,
        "attribution_required": False,
        "attribution_text": "National Aeronautics and Space Administration. Human Research Program Evidence Book. Houston, TX: Lyndon B. Johnson Space Center.",
        "url": "https://humanresearchroadmap.nasa.gov/evidence/",
        "domains": ["training_adaptations_fatigue_load", "exercise_science_biomechanics"],
        "restrictions": "No endorsement by NASA or U.S. Government claimed.",
    },
]


def write_raw_source_files(raw_dir: Path, documents: List[Dict[str, Any]]) -> Dict[str, Tuple[str, int]]:
    """Group documents by source_id, write un-split raw files, and compute SHA-256."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    source_docs: Dict[str, List[Dict[str, Any]]] = {}
    for d in documents:
        sid = d["source_id"]
        source_docs.setdefault(sid, []).append(d)

    source_hashes: Dict[str, Tuple[str, int]] = {}

    for sid, docs in source_docs.items():
        filename = f"{sid.lower().replace('-', '_')}_raw.txt"
        file_path = raw_dir / filename
        
        # Assemble raw text
        lines = [
            f"# SOURCE ID: {sid}",
            f"# TOTAL DOCUMENTS: {len(docs)}",
            "# NOTICE: Raw un-split educational material",
            "=" * 72,
            "",
        ]
        for d in docs:
            lines.append(f"[SECTION: {d['section_title']}]")
            lines.append(f"[SOURCE: {sid}]")
            lines.append(f"[GROUP: {d.get('group_id', sid)}]")
            lines.append(d["text"].strip())
            lines.append("")

        raw_content = "\n".join(lines)
        file_path.write_text(raw_content, encoding="utf-8", newline="\n")

        sha256 = compute_file_sha256(file_path)
        byte_size = file_path.stat().st_size
        source_hashes[sid] = (sha256, byte_size)
        print(f"  [RAW] {sid} -> {filename} ({byte_size:,} bytes, sha256={sha256[:12]}...)")

    return source_hashes


def main() -> None:
    print("=" * 72)
    print("NOVA-FIT PHASE 6: CORPUS EXPANSION ENGINE")
    print("=" * 72)

    root_dir = Path("e:/NOVA")
    raw_dir = root_dir / "data" / "sources_raw"
    approved_dir = root_dir / "data" / "approved"
    prepared_dir = root_dir / "data" / "prepared_expanded"
    tokenizer_dir = root_dir / "artifacts" / "final_tokenizer"
    config_path = root_dir / "configs" / "dataset_expanded.json"

    # Step 1: Ingest all educational documents
    raw_documents = get_all_documents()
    print(f"\n1. Loaded {len(raw_documents)} educational documents across 7 pillars.")

    # Step 2: Write raw source files and record SHA-256 hashes
    print("\n2. Writing raw source repository to data/sources_raw/...")
    raw_hashes = write_raw_source_files(raw_dir, raw_documents)

    # Step 3: Build and save updated Source Registry (schema v2.0)
    print("\n3. Building updated Source Registry (data/approved/source_registry.json)...")
    records = []
    for meta in APPROVED_SOURCES_METADATA:
        sid = meta["source_id"]
        sha256, byte_size = raw_hashes.get(sid, ("", 0))
        record = SourceProvenanceRecord(
            source_id=sid,
            title=meta["title"],
            author=meta["author"],
            publication_year=meta["publication_year"],
            license=meta["license"],
            legal_basis=meta["legal_basis"],
            commercial_use_permitted=meta["commercial_use_permitted"],
            attribution_required=meta["attribution_required"],
            attribution_text=meta["attribution_text"],
            url=meta["url"],
            acquisition_date="2026-10-14",
            version="2.0.0",
            raw_sha256=sha256,
            raw_bytes=byte_size,
            domains=meta["domains"],
            restrictions=meta["restrictions"],
        )
        records.append(record)

    registry = SourceRegistry(
        sources=records,
        version="2.0.0",
    )
    registry_path = approved_dir / "source_registry.json"
    registry.save(registry_path)
    print(f"  Successfully registered {len(records)} approved sources.")

    # Step 4: Duplicate detection and clustering
    print("\n4. Running exact and near-duplicate detection (k=5, threshold=0.85)...")
    corpus_docs = [
        CorpusDocument(
            doc_id=d["doc_id"],
            section_title=d["section_title"],
            source_id=d["source_id"],
            topic_domain=d["topic_domain"],
            text=d["text"],
            group_id=d["group_id"],
        )
        for d in raw_documents
    ]

    retained_docs, audit_result, cluster_map = detect_duplicates_and_group(
        corpus_docs, near_dup_threshold=0.85, shingle_k=5
    )
    print(f"  Total input documents:    {audit_result.total_documents}")
    print(f"  Unique retained:          {audit_result.unique_documents}")
    print(f"  Exact duplicates removed: {audit_result.exact_duplicates_found}")
    print(f"  Near duplicates found:    {audit_result.near_duplicates_found}")
    print(f"  Connected groups:         {audit_result.connected_groups}")
    print(f"  Multi-document clusters:  {len(audit_result.multi_document_groups)}")

    # Step 5: Group-aware partitioning (0 cross-split leakage)
    print("\n5. Partitioning documents into train and val splits (val_ratio=0.15, seed=42)...")
    train_docs, val_docs = partition_documents_by_group(retained_docs, val_ratio=0.15, seed=42)

    # Verification: Group leakage check
    train_groups = set(d.group_id for d in train_docs)
    val_groups = set(d.group_id for d in val_docs)
    leakage = train_groups & val_groups
    if leakage:
        raise ValueError(f"FATAL: Cross-split group leakage detected on groups: {leakage}")
    print(f"  Zero split leakage verified across {len(train_groups)} train groups and {len(val_groups)} val groups.")

    # Step 6: Tokenizer statistics verification
    print("\n6. Computing token statistics using final tokenizer...")
    tok = NovaTokenizer.from_file(tokenizer_dir)
    train_stats = calculate_split_statistics(train_docs, "train", tok)
    val_stats = calculate_split_statistics(val_docs, "val", tok)

    print("\n  --- Training Corpus Statistics ---")
    print(f"  Documents:   {train_stats.document_count:,}")
    print(f"  Characters:  {train_stats.character_count:,}")
    print(f"  Words:       {train_stats.word_count:,}")
    print(f"  Raw Tokens:  {train_stats.raw_token_count:,}")
    print(f"  With EOS:    {train_stats.tokens_with_eos:,}")
    print(f"  Packed Seqs: {train_stats.packed_sequence_count:,} (L=512)")
    print(f"  Padded Toks: {train_stats.padded_token_count:,}")
    print(f"  Topic Domains Covered: {len(train_stats.domain_distribution)}")
    for dom, cnt in sorted(train_stats.domain_distribution.items()):
        print(f"    - {dom}: {cnt} docs")

    print("\n  --- Validation Corpus Statistics ---")
    print(f"  Documents:   {val_stats.document_count:,}")
    print(f"  Characters:  {val_stats.character_count:,}")
    print(f"  Words:       {val_stats.word_count:,}")
    print(f"  Raw Tokens:  {val_stats.raw_token_count:,}")
    print(f"  With EOS:    {val_stats.tokens_with_eos:,}")
    print(f"  Packed Seqs: {val_stats.packed_sequence_count:,} (L=512)")
    print(f"  Padded Toks: {val_stats.padded_token_count:,}")
    print(f"  Topic Domains Covered: {len(val_stats.domain_distribution)}")

    # Assert training tokens >= 100,000 milestone
    if train_stats.raw_token_count < 100000:
        raise ValueError(
            f"Training token milestone FAILED: Expected >= 100,000 tokens, got {train_stats.raw_token_count:,}"
        )
    print(f"\n  [MILESTONE PASSED] Training corpus has {train_stats.raw_token_count:,} raw tokens (>= 100,000)!")

    # Step 7: Export expanded corpus text files
    print("\n7. Exporting expanded training and validation corpus files...")
    train_corpus_path = approved_dir / "expanded_train_corpus.txt"
    val_corpus_path = approved_dir / "expanded_val_corpus.txt"

    def format_corpus(docs: List[CorpusDocument]) -> str:
        blocks = []
        for d in docs:
            blocks.append(
                f"[SECTION: {d.section_title}]\n[SOURCE: {d.source_id}]\n{d.text.strip()}"
            )
        return "\n\n".join(blocks) + "\n"

    train_text = format_corpus(train_docs)
    val_text = format_corpus(val_docs)

    train_corpus_path.write_text(train_text, encoding="utf-8", newline="\n")
    val_corpus_path.write_text(val_text, encoding="utf-8", newline="\n")

    train_sha256 = compute_file_sha256(train_corpus_path)
    val_sha256 = compute_file_sha256(val_corpus_path)

    print(f"  Exported {train_corpus_path} ({len(train_text):,} chars, SHA-256={train_sha256})")
    print(f"  Exported {val_corpus_path} ({len(val_text):,} chars, SHA-256={val_sha256})")

    # Step 8: Create configuration for expanded dataset
    print("\n8. Generating configs/dataset_expanded.json...")
    prep_cfg = PrepareDatasetConfig(
        train_corpus_path=str(train_corpus_path),
        val_corpus_path=str(val_corpus_path),
        tokenizer_path=str(tokenizer_dir),
        output_dir=str(prepared_dir),
        source_registry_path=str(registry_path),
        max_seq_len=512,
        drop_last_short=False,
        add_eos=True,
        detect_duplicates=True,
    )
    config_path.write_text(json.dumps(prep_cfg.to_dict(), indent=2), encoding="utf-8")

    # Step 9: Run preparation pipeline
    print("\n9. Running prepare_dataset() pipeline...")
    prep_result = prepare_dataset(prep_cfg, verbose=True)
    if not prep_result.success:
        raise RuntimeError(f"prepare_dataset failed: {prep_result.message}")

    manifest_file = prepared_dir / "manifest.json"
    manifest_data = json.loads(manifest_file.read_text(encoding="utf-8"))

    print("\n  --- Prepared Dataset Manifest Summary ---")
    print(f"  Tokenizer Hash:    {manifest_data.get('tokenizer_hash')}")
    print(f"  Train Sequences:   {manifest_data.get('train_sequences'):,} (packed L=512)")
    print(f"  Val Sequences:     {manifest_data.get('val_sequences'):,} (packed L=512)")
    print(f"  Total Tokens Train:{manifest_data.get('total_tokens_train'):,}")
    print(f"  Total Tokens Val:  {manifest_data.get('total_tokens_val'):,}")

    print("\n" + "=" * 72)
    print("NOVA-FIT PHASE 6 CORPUS EXPANSION COMPLETED SUCCESSFULLY!")
    print("=" * 72)


if __name__ == "__main__":
    main()
