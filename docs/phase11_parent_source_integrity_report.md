# Project NOVA Phase 11: Parent-Source Integrity, Provenance Remediation, and Biomechanics Expansion Report

**Document Version**: 1.0.0  
**Phase**: Phase 11 (Data Integrity, Provenance Remediation, Biomechanics Staging)  
**Date**: October 16, 2026  
**Status**: COMPLETE / PRETRAINING GATED  
**Artifact Directory**: `data/staging_phase11/`  
**Historical Phase 10 Artifacts**: `data/staging_phase10/` (Preserved Intact)  

---

## 1. Executive Summary & Mission Scope

Project NOVA Phase 11 was chartered to audit and strengthen the Phase 10.2 corpus staging pipeline prior to substantial corpus scaling. This phase focuses entirely on data integrity, cryptographic invariance, legal defensibility, and split isolation:
1. **Publication-Level Split Leakage Audit & Remediation**: Identified and resolved cross-split publication leakage in the 2018 Physical Activity Guidelines Advisory Committee (PAGAC) Scientific Report, where individual chapters were split across training and validation in Phase 10.2. Implemented hierarchical Disjoint Set Union (DSU) clustering enforcing zero overlap across `source_id`, `parent_source_id`, and `group_id`.
2. **Legal and Provenance Records Remediation**: Eliminated blanket claims of worldwide public domain status under 17 U.S.C. § 105; scoped public domain status to domestic U.S. government employee works; distinguished employee works from contractor/grantee works; conducted rigorous legal analysis on U.S. Army FM 7-22 (distinguishing Lanham Act trademark mentions from copyright while maintaining quarantine due to unvetted third-party illustrations and Cloudflare DoD edge restrictions).
3. **Source-to-Pillar Mapping and Borg RPE Scale Audit**: Reconciled token counts by source, parent publication, and pillar. Conducted forensic analysis of the Borg RPE scale, discovering it was improperly cited in earlier syntheses without primary text presence; updated CDC title and documented Borg RPE as an unverified external concept.
4. **Biomechanics Source Acquisition & Licensing Gate Execution**: Investigated OpenStax *Anatomy & Physiology 2e* (Chapters 9 and 11). Discovered authoritative licensing under CC BY-NC-SA 4.0 with explicit AI training reservations; verified that the NOVA licensing gate correctly flagged and quarantined this source at ingestion.
5. **Comprehensive Automated Test Expansion**: Authored 27 comprehensive regression tests in `tests/test_phase11.py` exercising parent-publication partitioning across multiple seeds, multi-chapter co-location, transitive duplicate clustering, metadata fallback defaults, human override isolation, benchmark title vs. answer discrimination, attribution retention, and scanned PDF handling. Executed the complete repository test suite: **266 passed in 46.42s (100% pass rate)**.
6. **Preservation of Authoritative Frozen Artifacts**: Confirmed byte-for-byte SHA-256 identity of all five Phase 8 frozen artifacts before and after all engineering operations. Zero pretraining was initiated; model architecture was untouched.

---

## 2. Frozen Artifact Verification (Non-Negotiable Constraints 1 & 2)

All five frozen Phase 8 artifacts were verified using cryptographic SHA-256 checksums before initiating changes and immediately following test suite completion:

| Artifact Path | Expected Baseline SHA-256 | Post-Work Verified SHA-256 | Verification Status |
| :--- | :--- | :--- | :---: |
| `artifacts/final_tokenizer/tokenizer.json` | `1639CEC0FCE7263BBB10ECA238B19A5D13EF6BD9FA1C545CD481F4E8FF9C93FC` | `1639CEC0FCE7263BBB10ECA238B19A5D13EF6BD9FA1C545CD481F4E8FF9C93FC` | **MATCH (Byte-for-byte)** |
| `data/prepared_expanded/manifest.json` | `9EBB8353F41FAA16926A928A528EB64218753B305FB573B372A88F20208ADC29` | `9EBB8353F41FAA16926A928A528EB64218753B305FB573B372A88F20208ADC29` | **MATCH (Byte-for-byte)** |
| `data/prepared_expanded/train.pt` | `ACB19B80F90E6F30363DC638B6975E3F4A75D8AD80FC3E3C48DF3043F066DB7E` | `ACB19B80F90E6F30363DC638B6975E3F4A75D8AD80FC3E3C48DF3043F066DB7E` | **MATCH (Byte-for-byte)** |
| `data/prepared_expanded/val.pt` | `17DC2D25E5DCE4E422D4AC47C7E651051E23D4E400DC5F399BB2FC6F2DA085FC` | `17DC2D25E5DCE4E422D4AC47C7E651051E23D4E400DC5F399BB2FC6F2DA085FC` | **MATCH (Byte-for-byte)** |
| `data/benchmark/fitness_eval_benchmark.json` | `F339E95D4D3AA27D2A2AFBED5C721DEDCC7B0B91792523B6E4D18F1638B2AEC8` | `F339E95D4D3AA27D2A2AFBED5C721DEDCC7B0B91792523B6E4D18F1638B2AEC8` | **MATCH (Byte-for-byte)** |

**Invariance Confirmation**: Zero modifications were introduced to tokenizer vocabularies, training/validation tensors, pretraining configurations, or held-out benchmark items.

---

## 3. Inventory of Changes and Engineering Rationale

| File Path | Status | Engineering Rationale |
| :--- | :--- | :--- |
| `src/nova/ingestion.py` | Modified | Added `parent_source_id` and `canonical_source_url` fields with backward-compatible defaults to `NormalizedDocument`. Upgraded `source_level_split` DSU to cluster on `SRC::{source_id}`, `PARENT::{parent_source_id}`, and `GRP::{group_id}` simultaneously. Added dominant-cluster guard ($>50\%$ of corpus) and runtime invariant assertions ensuring disjointness across train and val. |
| `scripts/run_staging_ingestion.py` | Modified | Updated staging pipeline configuration to target `data/staging_phase11/`, leaving `data/staging_phase10/` untouched. Linked all 2018 PAGAC chapters under parent `US-HHS-PAGAC-2018` and CDC guidelines under `US-CDC-PA-2022`. Ingested live OpenStax A&P 2e text to trigger and test licensing gate quarantine. Remedied CDC measuring activity title. |
| `tests/test_phase11.py` | Created | Authored 27 automated tests covering parent-source split integrity across 5 seeds, chapter co-location, transitive duplicate clustering, provenance fallbacks, licensing rejection, human override isolation, benchmark leakage discrimination, and Phase 11 staging invariants. |
| `data/staging_phase11/*` | Created | Staged Phase 11 artifacts: `phase11_staging_manifest.json`, `train_staging.json`, `val_staging.json`, `phase11_audit_summary.json`, `intake_registry.json`, and `sources_raw/`. |
| `docs/phase11_parent_source_integrity_report.md` | Created | Definitive deliverable report documenting methodology, findings, token audits, legal reviews, and exit gate decision. |

---

## 4. Task 1: Publication-Level Split Integrity Audit & Remediation

### 4.1 Root Cause of Phase 10.2 Leakage
In Phase 10.2, the 2018 Physical Activity Guidelines Advisory Committee (PAGAC) Scientific Report was ingested as five separate documents:
- `US-HHS-PAGAC-2018-EXEC` (Part A: Executive Summary)
- `US-HHS-PAGAC-2018-HIIT` (Part F, Chapter 1: High-Intensity Interval Training)
- `US-HHS-PAGAC-2018-BRAIN-SLEEP` (Part F, Chapter 3: Brain Health and Sleep)
- `US-HHS-PAGAC-2018-CARDIOMETABOLIC` (Part F, Chapter 5: Cardiometabolic Health)
- `US-HHS-PAGAC-2018-OLDER-ADULTS` (Part F, Chapter 9: Older Adults & Falls)

Because the Phase 10.2 pipeline only clustered on `source_id` and near-duplicate `group_id`, each chapter was treated as an independent publication unit. Consequently, `US-HHS-PAGAC-2018-HIIT` (12,891 tokens) was assigned to the validation set while the remaining four chapters (66,397 tokens) were assigned to training. 

Although `source_id` disjointness was maintained ($\text{TrainSources} \cap \text{ValSources} = \emptyset$), **publication-level leakage occurred**: stylistic patterns, vocabulary choices, literature review methodologies, and co-author conventions from the 2018 PAGAC Scientific Report crossed the train/validation boundary.

### 4.2 DSU Cluster Partitioning Architecture
To eliminate publication-level split leakage, `src/nova/ingestion.py` was enhanced with a 3-way Disjoint Set Union (DSU) clustering mechanism:
```python
# Disjoint Set Union (DSU) by source_id, parent_source_id, and group_id
parent: Dict[str, str] = {}

def find(i: str) -> str:
    path = []
    while parent[i] != i:
        path.append(i)
        i = parent[i]
    for node in path:
        parent[node] = i
    return i

def union(i: str, j: str) -> None:
    root_i = find(i)
    root_j = find(j)
    if root_i != root_j:
        parent[root_i] = root_j

# For each document, unify:
# 1. SRC::{doc.source_id}
# 2. PARENT::{doc.parent_source_id or doc.source_id}
# 3. GRP::{doc.group_id} (if non-empty)
```

### 4.3 Partitioning Invariants & Verification
The enhanced `source_level_split` enforces three mathematical invariants:
1. **Source Disjointness**: $\text{TrainSources} \cap \text{ValSources} = \emptyset$
2. **Parent Publication Disjointness**: $\text{TrainParents} \cap \text{ValParents} = \emptyset$
3. **Duplicate Group Disjointness**: $\text{TrainGroups} \cap \text{ValGroups} = \emptyset$

In addition, a dominant-cluster check ensures that if a single connected component contains $\ge 50\%$ of the corpus tokens (such as `US-HHS-PAGAC-2018` at 81.06%), it is never assigned to the validation partition when `val_ratio < 0.5`.

### 4.4 Honest Validation Limitations
Because all five chapters of `US-HHS-PAGAC-2018` share `parent_source_id = "US-HHS-PAGAC-2018"`, they form a single partition unit of **79,288 tokens (81.06% of the 97,808 usable staging tokens)**. 

To maintain publication integrity:
- All 5 PAGAC chapters reside exclusively in **training**.
- The validation partition is constructed exclusively from completely independent parent publications:
  - `CDC-NIOSH-PUB-2016-106` (`US-CDC-NIOSH-HEAT-2016`): 4,798 tokens
  - `PLOS-PONE-0215877` (`PLOS-PONE-0215877`): 1,013 tokens
  - **Validation Total**: **5,811 tokens (5.94% of corpus across 2 independent publications)**.

**Explicit Engineering Limitation**: With currently accepted staged primary sources, the validation split contains 5,811 tokens. Rather than manufacturing artificial validation sources or fragmenting PAGAC across splits to hit an arbitrary 10% or 15% validation target, Project NOVA explicitly documents this limitation. Full 10–15% validation volume will be achieved honestly as additional independent, verified peer-reviewed publications are staged.

---

## 5. Task 2: Remediate Legal and Provenance Records

### 5.1 Scoping of 17 U.S.C. § 105
In Phase 10.2, intake records frequently stated that federal documents were in the "worldwide public domain." This claim was legally imprecise:
- **Statutory Limitation**: 17 U.S.C. § 105 provides that copyright protection is not available for any work of the United States Government within the domestic jurisdiction of the United States.
- **Foreign Jurisdiction Rights**: The U.S. federal government can and does maintain copyright in other countries depending on foreign law and bilateral treaties.
- **Remediation**: All Phase 11 records and `audit_license` outputs now explicitly record:  
  `"US domestic public domain under 17 U.S.C. § 105; foreign copyright may apply depending on jurisdiction."`

### 5.2 Distinguishing Federal Employees from Contractors and Grantees
Federal funding does not automatically place a document into the public domain under § 105:
- Works authored by private contractors, grant recipients, or external advisory committees retain common-law copyright unless intellectual property rights are formally assigned in writing to the federal government.
- The licensing audit gate (`audit_license`) now explicitly checks `is_us_gov_employee_work`. If `False` or ambiguous, the work cannot be cleared as public domain and is rejected/quarantined pending human legal verification of assignment terms.

### 5.3 Forensic Legal Review of U.S. Army FM 7-22 (Holistic Health and Fitness)
In Phase 10.2, FM 7-22 was tentatively flagged due to commercial trademark references. Phase 11 conducted an in-depth forensic legal audit:
1. **Trademark vs. Copyright Distinction**:
   - Chapter 7 ("Running Technique") cites the "Pose Method®", a registered commercial trademark owned by Dr. Nicholas Romanov / Bikila Corp.
   - Under the Lanham Act (15 U.S.C. § 1114 / § 1125), trademark protection protects source indicators against commercial confusion. Mentioning a trademark in a military field manual constitutes nominative/descriptive reference, **not copyright infringement**, and does not invalidate copyright in the rest of the manual.
2. **Third-Party Copyright and Visual Carve-Outs**:
   - FM 7-22 contains hundreds of photographs, anatomical diagrams, training illustrations, and exercise execution charts. Under 17 U.S.C. § 105, federal public domain status does not extend to embedded third-party photographs or copyrighted training systems licensed to the military.
   - Theoretical excision of Chapter 7 alone is legally insufficient to clear FM 7-22 for model training without a forensic audit of all embedded tables, figures, and contractor assignments.
3. **Automated Retrieval Barrier**:
   - The official U.S. Army Publishing Directorate (APD) web server (`armypubs.army.mil`) protects PDF downloads behind Cloudflare Edge WAF (HTTP 403 Forbidden to automated scripts).
4. **Legal Determination**:
   - FM 7-22 remains **QUARANTINED** pending manual retrieval from official military distribution and formal human legal counsel review of third-party graphics exclusions.

---

## 6. Task 3: Audit Source-to-Pillar Mapping & Token Reconciliation

### 6.1 Source-to-Pillar Traceability Ledger
All 10 accepted staging documents were audited for pillar alignment, parent publication traceability, and token distribution:

| Source ID | Parent Publication ID | Document Title | Usable Tokens | Pillar Assignment | Traceable Evidence Base |
| :--- | :--- | :--- | :---: | :--- | :--- |
| `US-CDC-PA-ADULTS-2022` | `US-CDC-PA-2022` | CDC Physical Activity Guidelines for Adults | 3,877 | `exercise_science_biomechanics` | CDC.gov authenticated surveillance |
| `US-CDC-PA-MEASURING-2022` | `US-CDC-PA-2022` | Measuring Physical Activity Intensity | 4,298 | `exercise_science_biomechanics` | Target heart rate and 0–10 scale |
| `US-CDC-PA-OLDER-2022` | `US-CDC-PA-2022` | Physical Activity Guidelines for Older Adults | 4,534 | `training_adaptations_fatigue_load` | Multicomponent physical activity |
| `US-CDC-NIOSH-HEAT-2016` | `CDC-NIOSH-PUB-2016-106` | NIOSH Heat Stress Criteria Document | 4,798 | `nutrition_fundamentals_hydration` | NIOSH Pub. No. 2016-106 |
| `PLOS-PONE-0215877` | `PLOS-PONE-0215877` | Resistance Training Frequency Meta-Analysis | 1,013 | `strength_training_programming` | Saric et al. (2019), CC BY 4.0 |
| `US-HHS-PAGAC-2018-EXEC` | `US-HHS-PAGAC-2018` | 2018 PAGAC Report: Part A. Executive Summary | 14,989 | `general_fitness_education_safety` | HHS.gov authenticated federal report |
| `US-HHS-PAGAC-2018-HIIT` | `US-HHS-PAGAC-2018` | 2018 PAGAC Report: Part F. Ch 1 (HIIT) | 12,891 | `strength_training_programming` | High-intensity interval adaptations |
| `US-HHS-PAGAC-2018-BRAIN-SLEEP` | `US-HHS-PAGAC-2018` | 2018 PAGAC Report: Part F. Ch 3 (Brain & Sleep) | 16,503 | `sleep_recovery_physical_activity` | Cognitive function & sleep architecture |
| `US-HHS-PAGAC-2018-CARDIOMETABOLIC` | `US-HHS-PAGAC-2018` | 2018 PAGAC Report: Part F. Ch 5 (Cardiometabolic) | 16,738 | `nutrition_fundamentals_hydration` | Metabolic syndrome & energy balance |
| `US-HHS-PAGAC-2018-OLDER-ADULTS` | `US-HHS-PAGAC-2018` | 2018 PAGAC Report: Part F. Ch 9 (Older Adults) | 18,167 | `training_adaptations_fatigue_load` | Sarcopenia, frailty, and fall prevention |
| **Total Accepted** | — | **10 Primary Documents** | **97,808** | — | **100% Traceable to Authenticated Sources** |

### 6.2 Forensic Audit of the Borg RPE Scale
In historical Project NOVA documents (Phases 1–6), references were made to the "Borg Rating of Perceived Exertion (RPE) Scale" (the 6–20 scale developed by Gunnar Borg in 1970/1982/1998, published by Human Kinetics), attributing it to CDC and Army manuals.

Phase 11 conducted a comprehensive text search across all accepted staging source text:
1. **CDC Text Investigation**:
   - Examination of `us_cdc_pa_measuring_2022.md` revealed that the CDC guidelines describe relative intensity using:
     - Target Heart Rate calculations (percentage of estimated maximum heart rate, 220 minus age).
     - The **"Talk Test"** (speaking comfortably vs. saying only a few words).
     - A generic **0 to 10 relative scale** (where sitting is 0 and highest effort is 10).
   - **Finding**: The authentic CDC primary text **does not contain the Gunnar Borg 6–20 RPE scale**, nor does it cite Gunnar Borg's proprietary charts.
2. **Remediation**:
   - The document title was corrected in the registry and staging manifest from `"CDC Physical Activity Guidelines: Measuring Intensity & Borg RPE"` to `"Measuring Physical Activity Intensity: Target Heart Rate and 0-to-10 Effort Rating"`.
   - The Gunnar Borg 6–20 RPE scale was formally flagged as an **unverified external concept** in historical curriculum notes. If NOVA requires Borg RPE coverage in future phases, it must be introduced through a primary peer-reviewed source or properly licensed clinical exercise physiology text.

### 6.3 Token Reconciliation Accounting
To prevent discrepancies between raw word counts, usable staging tokens, and packed pretraining tokens:
- **Raw Word Count**: 34,908 words across 10 accepted documents.
- **Usable Staging Tokens**: Exactly **97,808 tokens**, calculated using the authoritative NovaTokenizer (`artifacts/final_tokenizer/tokenizer.json`, vocab size 3,384) over canonical formatted document representations:
  $$\text{Formatted Document} = \text{"[SECTION: } \text{title} \text{]\n[SOURCE: } \text{source\_id} \text{]\n"} + \text{normalized\_text}$$
- **Packed Pretraining Tokens**: Zero packed pretraining tokens were generated in Phase 11 because model pretraining was not initiated. The baseline packed tokens in `data/prepared_expanded/train.pt` (126,677 tokens) and `val.pt` (14,081 tokens) remain completely untouched.

---

## 7. Task 4: Biomechanics Source Acquisition (OpenStax Anatomy & Physiology 2e)

### 7.1 Scope of Investigation
To address the critical deficit in Pillar 3 (`exercise_technique_safety` / Biomechanics), OpenStax *Anatomy and Physiology 2e* (Betts et al., Rice University) was investigated for relevant movement-related chapters:
- **Chapter 9, Section 9.5**: *Types of Body Movements* (flexion, extension, abduction, adduction, circumduction, rotation, supination, pronation, dorsiflexion, plantar flexion, inversion, eversion).
- **Chapter 11, Section 11.1**: *Interactions of Skeletal Muscles, Their Fascicle Arrangement, and Their Lever Systems* (agonist/antagonist pairs, synergists, fixators, first-class, second-class, and third-class lever mechanics, mechanical advantage vs. range of motion).

### 7.2 Authoritative Licensing Discovery & Terms
Live investigation of the authoritative OpenStax platform and OpenStax Terms of Use revealed critical licensing restrictions:
1. **Creative Commons License**: OpenStax A&P 2e is published under **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**.
2. **AI / Model Training Reservation**: OpenStax terms of service explicitly state:  
   *"OpenStax resources may not be used for the training of artificial intelligence or large language models without prior written permission."*
3. **Pipeline Licensing Gate Execution**:
   - The source was ingested through `scripts/run_staging_ingestion.py` under `OPENSTAX-AP2E-BIOMEC` with license `CC BY-NC-SA 4.0`.
   - The NOVA legal gate evaluated the license:
     ```text
     Processing: [OPENSTAX-AP2E-BIOMEC] (Parent: OPENSTAX-ANAT-PHYS-2E)
       -> REJECTED at licensing gate: Licensing rejection: Non-commercial restriction (CC BY-NC)
          incompatible with unrestricted model pretraining.
     ```
   - **Result**: The source was **REJECTED / QUARANTINED** at the licensing boundary. Zero OpenStax tokens entered `train_staging.json` or `val_staging.json`.

### 7.3 Screening Results & Biomechanics Scope Limitation
For forensic verification, the extracted text was screened through NOVA's quality and benchmark gates:
- **Health & Safety Screener**: 0 high/critical flags (pure physiological and anatomical description).
- **Benchmark Contamination Detector**: 0 n-gram leaks against `fitness_eval_benchmark.json`.
- **Quality Score**: High lexical density and clean formatting.
- **Explicit Limitation**: Even if a bilateral commercial license were obtained from Rice University / OpenStax, anatomical musculoskeletal descriptions provide structural foundations but do not constitute comprehensive biomechanics (e.g., ground reaction forces, joint moment arms, bar-path trajectory mechanics, or stretch-shortening cycle dynamics).

---

## 8. Task 5: Expand Validation, Invariants, and Auditability

### 8.1 Automated Test Suite Structure (`tests/test_phase11.py`)
Twenty-seven rigorous, end-to-end regression tests were implemented in [`tests/test_phase11.py`](file:///e:/NOVA/tests/test_phase11.py), organized into six test classes:

1. **`TestParentPublicationSplitIntegrity`**:
   - `test_parent_publication_never_crosses_train_val`: Tests partitioning across five seeds (0, 1, 42, 100, 2026), asserting strict disjointness of parent publications.
   - `test_multiple_chapters_co_located`: Verifies all chapters of `US-HHS-PAGAC-2018` remain co-located in the same partition.
   - `test_dominant_single_publication_cannot_invert_split`: Verifies that a parent publication holding $>50\%$ of corpus volume cannot invert the split into validation when `val_ratio < 0.5`.
   - `test_deterministic_split_reproducibility`: Verifies identical document assignment across repeated runs with identical seeds.
2. **`TestDuplicateGroupSplitIntegrity`**:
   - `test_duplicate_cluster_unites_different_sources_and_parents`: Verifies that syndicated documents sharing a `group_id` stay together even across different sources and parents.
   - `test_transitive_cluster_closure_in_dsu`: Verifies transitive graph closure in the DSU ($A \sim B$ via parent, $B \sim C$ via group $\implies A, B, C$ co-located).
3. **`TestProvenanceConsistency`**:
   - `test_default_fallbacks_when_omitted`: Asserts `parent_source_id` defaults to `source_id` and `canonical_source_url` defaults to `url`.
   - `test_explicit_provenance_retained`: Asserts explicit provenance fields are preserved intact.
   - `test_serialization_dict_round_trip`: Verifies `to_dict()` and `from_dict()` round-trip serialization.
   - `test_backward_compatibility_with_legacy_phase10_dict`: Verifies graceful ingestion of legacy Phase 10 dictionary records.
4. **`TestLegalProvenanceAndOverrideIsolation`**:
   - `test_cc_by_nc_sa_rejection`: Verifies rejection of CC BY-NC-SA 4.0.
   - `test_us_gov_with_unvetted_third_party_rejected`: Verifies rejection of U.S. government documents with unexcluded third-party copyrights.
   - `test_human_override_isolates_to_licensing_only`: Verifies that granting a human license override never bypasses Health & Safety screening (lethal dehydration claims are still quarantined).
   - `test_human_override_does_not_bypass_benchmark_gate`: Verifies that a human license override never bypasses Benchmark Contamination screening (exact benchmark answer leaks are still quarantined).
5. **`TestBenchmarkLeakageDiscrimination`**:
   - `test_bibliographic_title_mention_allowed`: Verifies that citing official publication titles does not trigger false-positive contamination.
   - `test_genuine_answer_13gram_leakage_blocked`: Verifies that exact 13-gram benchmark answer phrases are intercepted and flagged as `GENUINE_LEAKAGE`.
6. **`TestExtractionAndQualityHandling`**:
   - `test_cc_by_attribution_retained`: Verifies retention of mandatory attribution text for CC BY 4.0 works.
   - `test_scanned_pdf_quarantine`: Verifies detection and quarantine of image-only scanned PDFs without extractable text streams.
7. **`TestPhase11StagedCorpusInvariants`**:
   - `test_strict_disjointness_invariants`: Verifies zero overlap on `source_id`, `parent_source_id`, and `group_id` across the actual staged files in `data/staging_phase11/`.
   - `test_all_pagac_chapters_retained_together_in_training`: Verifies that all five PAGAC chapters reside exclusively in `train_staging.json`.
   - `test_token_counts_reconciled`: Validates exact token sum equality:
     $$\text{TrainTokens } (91,997) + \text{ValTokens } (5,811) = \text{TotalCombinedTokens } (97,808)$$
   - `test_zero_benchmark_contamination_in_accepted_staging`: Scans all 10 accepted documents against the held-out benchmark and confirms zero contamination.
   - `test_historical_phase10_records_preserved_intact`: Confirms preservation of historical Phase 10 manifests and reports.

### 8.2 Full Test Suite Execution Results
The complete automated test suite was executed across the entire repository using pytest:
```text
============================= test session starts =============================
platform win32 -- Python 3.14.8, pytest-9.1.1, pluggy-1.6.0
rootdir: E:\NOVA
configfile: pyproject.toml
plugins: anyio-4.15.1
collected 266 items

tests\test_data.py ................................................................ [ 24%]
tests\test_model.py .................                                               [ 30%]
tests\test_phase10.py .................................................             [ 48%]
tests\test_phase11.py ...........................                                   [ 59%]
tests\test_phase4.py ................                                                [ 65%]
tests\test_phase6.py .............                                                   [ 69%]
tests\test_phase7.py ..........                                                      [ 73%]
tests\test_phase8.py ........                                                        [ 76%]
tests\test_phase9.py ................                                                [ 82%]
tests\test_smoke.py ....                                                             [ 84%]
tests\test_tokenizer.py ...........................                                 [ 94%]
tests\test_training.py ...............                                               [100%]

============================= 266 passed in 46.42s =============================
```
**Test Pass Rate**: **100% (266 passed, 0 failed, 0 errors, 0 warnings)**.

---

## 9. Comprehensive Benchmark Contamination Findings

The held-out fitness evaluation benchmark (`data/benchmark/fitness_eval_benchmark.json`, SHA-256 `F339E95D...`) comprises 36 diagnostic questions with canonical reference answers across all seven pillars.

Contamination screening results across the 17 attempted Phase 11 staging candidates:
- **Accepted Staged Documents (10 sources)**: **0 benchmark contamination matches**.
- **Quarantined Documents (1 source)**:
  - `US-HHS-PAGAC-2018-CONCEPTS` (Part C: Key Concepts): Intercepted at character offset 31,737 for matching 13-gram answer sequence from `BENCH_P7_FACT_01`:  
    `"150 to 300 minutes of moderate intensity physical activity"`  
    **Action**: Quarantined under `IngestionStatus.QUARANTINED`. Authentic source text was preserved without alterations or synthetic doctoring.
- **Bibliographic Citations (Non-Contaminating)**:
  - Mention of publication titles (e.g., *"2018 Physical Activity Guidelines Advisory Committee Scientific Report"*) in reference sections was correctly classified as `BIBLIOGRAPHIC_CITATION` and permitted.

---

## 10. Pillar Distribution and Source Traceability Summary

The final token composition of the Phase 11 accepted staging corpus across the seven fitness pillars:

| Pillar Key | Descriptive Pillar Title | Usable Staging Tokens | Percentage of Staging Corpus | Baseline Coverage Status |
| :--- | :--- | :---: | :---: | :--- |
| `exercise_science_biomechanics` | 1. Exercise Physiology & General Fitness | 8,175 | 8.36% | Grounded in CDC adult guidelines |
| `strength_training_programming` | 2. Strength Training & Programming | 13,904 | 14.22% | Supported by PLOS ONE meta-analysis & PAGAC HIIT |
| `exercise_technique_safety` | 3. Biomechanics & Movement Execution | 0 | 0.00% | **RECOGNIZED GAP**: OpenStax A&P 2e quarantined (CC BY-NC-SA) |
| `nutrition_fundamentals_hydration` | 4. Nutrition & Hydration | 21,536 | 22.02% | High depth from NIOSH Heat & PAGAC Cardiometabolic |
| `sleep_recovery_physical_activity` | 5. Recovery & Sleep | 16,503 | 16.87% | Scientific consensus from PAGAC Brain & Sleep |
| `training_adaptations_fatigue_load` | 6. Injury Prevention & Exercise Safety | 22,701 | 23.21% | Strong evidence base from CDC Older Adults & PAGAC |
| `general_fitness_education_safety` | 7. Fitness Education & Interpretation | 14,989 | 15.32% | Population guidelines from PAGAC Executive Summary |
| **Total Staging Corpus** | — | **97,808** | **100.00%** | **7 of 7 Pillars Accounted For** |

---

## 11. Exit Criteria Assessment & Completion Gate

### Gate Review Criteria Checklist:

| Exit Criterion | Status | Evidence & Verification |
| :--- | :---: | :--- |
| **1. Parent-publication leakage eliminated** | **PASSED** | DSU partitioning ensures $\text{TrainParents} \cap \text{ValParents} = \emptyset$. All 5 PAGAC chapters reside exclusively in training. |
| **2. Source-level & duplicate-group integrity verified** | **PASSED** | Zero overlap across `source_id`, `parent_source_id`, and `group_id` verified by automated regression tests across multiple seeds. |
| **3. Evidence-based legal provenance claims** | **PASSED** | Blanket worldwide public domain claims removed; 17 U.S.C. § 105 scoped to domestic employee works; FM 7-22 trademark distinction analyzed; OpenStax CC BY-NC-SA 4.0 quarantined. |
| **4. Traceable provenance for new source material** | **PASSED** | OpenStax A&P 2e chapters retrieved, hashed, evaluated against licensing gate, and quarantined with documented rationale. |
| **5. Frozen Phase 8 artifacts byte-for-byte identical** | **PASSED** | All 5 frozen artifact SHA-256 hashes matched pre-work baseline exactly. |
| **6. Full automated test suite passes** | **PASSED** | 266 passed of 266 tests in 46.42s across the complete repository. |

---

### **GATE DECISION: PHASE 11 DATA INTEGRITY APPROVED**

**Next Action**: Pretraining remains **GATED**. Corpus scaling may proceed to Phase 12 once the following unresolved human-review requirements are formally addressed.

### Unresolved Human-Review Requirements:
1. **Pillar 3 Biomechanics Permissive Source**: Because OpenStax A&P 2e carries CC BY-NC-SA 4.0 and AI training restrictions, acquire an unencumbered CC BY 4.0 or public domain biomechanics/kinesiology source (e.g., CDC/NIOSH ergonomics criteria documents or peer-reviewed Open Access biomechanics papers from PMC/PLOS).
2. **Army FM 7-22 Legal Carve-Out Determination**: Direct human legal counsel to determine whether a text-only extract of FM 7-22 (with all third-party figures, photographs, and Chapter 7 Pose Method® references excised) can be cleared under 17 U.S.C. § 105 for training use.
3. **Validation Volume Expansion**: Acquire 2–3 additional independent CC BY 4.0 peer-reviewed exercise science publications to expand the validation partition to $\ge 15,000$ tokens without fragmenting multi-chapter parent publications.
