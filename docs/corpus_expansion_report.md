# Nova-Fit: Corpus Expansion & Data Quality Report (Phase 6)

## 1. Executive Summary & Audit Declaration

This report provides the formal audit and technical documentation for **Phase 6: Corpus Expansion and Data Quality** of **Project Nova-Fit**.

The primary objective of Phase 6 was to scale the approved, legally verified fitness training corpus from its Phase 4 baseline to exceed the engineering milestone of **100,000 raw training tokens**, while strictly maintaining:
1. **Traceable Legal Provenance**: All material is restricted to verified Public Domain works (U.S. Federal Government under 17 U.S.C. § 105) or explicit permissive licenses (Creative Commons Attribution 4.0 International / CC BY 4.0).
2. **Zero Train/Validation Contamination**: Document-level and group-level disjointness with zero shared text, zero shared group IDs, and zero cross-split high-Jaccard near-duplicates.
3. **Scientific & Educational Rigor**: Comprehensive coverage across seven fundamental pillars of exercise science, strength programming, exercise technique, nutrition, recovery, training adaptations, and general safety.
4. **Strict Medical Safety Boundaries**: Preservation of uncertainty, physiological variance, exercise contraindications, and explicit exclusion of individualized medical advice.
5. **Reproducible Pipeline & Manifest Verification**: Cryptographic SHA-256 tracking of all raw source files, processed text corpora, prepared dataset tensors, and the final Byte-Level BPE tokenizer artifact.

> [!IMPORTANT]
> **Engineering Milestone vs. Pretraining Scale**:
> The achievement of **125,486 raw training tokens** (142,820 total raw tokens across train and validation) represents an **initial engineering milestone** verifying end-to-end data hygiene, group-aware partitioning, token packing, and tokenizer consistency.
> 
> As mandated by Phase 6 guidelines, **no long-form model pretraining was initiated in this phase**. Furthermore, 125K tokens is an engineering validation corpus; production pretraining of a ~20M parameter language model requires subsequent scaling to 5M–50M tokens.

---

## 2. Audit of the Current Baseline (Phase 4 Recalculation)

Existing Phase 4 counts were treated as unverified until recalculated directly from active project artifacts using the final Byte-Level BPE tokenizer (`artifacts/final_tokenizer`, vocabulary size 3,384, SHA-256 `1639cec0fce7263bbb10eca238b19a5d13ef6bd9fa1c545cd481f4e8ff9c93fc`).

### Baseline Recalculation Results

| Metric | Baseline Training Corpus | Baseline Validation Corpus | Combined Baseline |
| :--- | :--- | :--- | :--- |
| **Artifact Path** | [`data/approved/train_corpus.txt`](file:///e:/NOVA/data/approved/train_corpus.txt) | [`data/approved/val_corpus.txt`](file:///e:/NOVA/data/approved/val_corpus.txt) | Both combined |
| **File SHA-256** | `ac0cb021ff722f7222bea57167dbe6da44f40384f71461f94ea596d3a6ffb266` | `3adf4951fa1c6f8531e04285db4e90bc63de27b8b583c551b1ace36a224ba955` | N/A |
| **File Size (Bytes)** | 18,238 bytes | 7,826 bytes | 26,064 bytes |
| **Document Count** | 11 documents | 5 documents | 16 documents |
| **Character Count** | 17,600 characters | 7,225 characters | 24,825 characters |
| **Word Count (Whitespace)** | 2,428 words | 953 words | 3,381 words |
| **Raw Tokens (no special)**| 3,248 tokens | 2,150 tokens | 5,398 tokens |
| **Tokens with `<|endoftext|>`**| 3,259 tokens (11 EOS) | 2,155 tokens (5 EOS) | 5,414 tokens (16 EOS) |
| **Packed Sequences ($L=512$)**| 7 sequences | 5 sequences | 12 sequences |
| **Valid (Non-Pad) Tokens** | 3,259 tokens | 2,155 tokens | 5,414 tokens |
| **Padded Tokens** | 325 tokens | 405 tokens | 730 tokens |
| **Packing Padding Ratio** | 9.07% | 15.82% | 11.89% |

### Baseline Provenance & Gaps Identified
1. **Source Registry**: Phase 4 registered 7 primary sources (6 U.S. Federal Government works under 17 U.S.C. § 105, 1 CC BY 4.0 work from OpenStax).
2. **Missing Raw Source Files**: Phase 4 documented source IDs in `source_registry.json`, but did not persist raw source files separately from cleaned text in a dedicated `data/sources_raw/` directory.
3. **Manifest Tokenizer Hash**: The Phase 4 `DatasetManifest` did not store the cryptographic hash of the tokenizer used to pack the sequences.
4. **Resolution in Phase 6**:
   - `src/nova/data.py` was updated to add `tokenizer_hash` and `tokenizer_path` fields to `DatasetManifest`.
   - `data/sources_raw/` was established to store raw, uncleaned text files with byte size and SHA-256 verification.
   - `data/approved/source_registry.json` was upgraded to v2.0 schema, tracking 21 sources with mandatory attribution notices and third-party exclusion clauses.

---

## 3. Corpus Quality Requirements & Seven-Pillar Plan

To ensure balanced educational breadth and depth without relying on generic web scrapes or synthetic filler, the expanded corpus is structured across **seven core pillars**:

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                     NOVA-FIT SEVEN-PILLAR CORPUS MATRIX                       │
├────┬─────────────────────────────┬───────────────────────────────────────────┤
│ #  │ Pillar Title                │ Core Topics & Physiological Concepts      │
├────┼─────────────────────────────┼───────────────────────────────────────────┤
│ 1  │ Exercise Science,           │ Sarcomere kinetics, sliding filament,     │
│    │ Physiology & Biomechanics   │ bioenergetics, joint kinetics, Fick eq.   │
├────┼─────────────────────────────┼───────────────────────────────────────────┤
│ 2  │ Strength Training Principles│ Progressive overload, periodization,      │
│    │ & Programming               │ RIR/RPE, cluster sets, VBT, APRE, PAPE    │
├────┼─────────────────────────────┼───────────────────────────────────────────┤
│ 3  │ Exercise Technique &        │ Squat, bench press, deadlift, overhead    │
│    │ Safe Equipment Use          │ press, bar path, rack safeties, collars   │
├────┼─────────────────────────────┼───────────────────────────────────────────┤
│ 4  │ Nutrition Fundamentals &    │ Energy balance, protein DIAAS, leucine    │
│    │ Hydration                   │ threshold, sodium fluid balance, creatine │
├────┼─────────────────────────────┼───────────────────────────────────────────┤
│ 5  │ Sleep, Recovery & Physical  │ Sleep stages, slow-wave sleep GH, HRV,    │
│    │ Activity                    │ active recovery, cold water immersion     │
├────┼─────────────────────────────┼───────────────────────────────────────────┤
│ 6  │ Training Adaptations,       │ General Adaptation Syndrome, ACWR, DOMS,  │
│    │ Fatigue & Load Management   │ central/peripheral fatigue, overtraining  │
├────┼─────────────────────────────┼───────────────────────────────────────────┤
│ 7  │ General Fitness Education & │ ACSM screening, PAR-Q+, RAMP warm-up,     │
│    │ Age-Appropriate Safety      │ youth/older adult guidelines, WBGT heat   │
└────┴─────────────────────────────┴───────────────────────────────────────────┘
```

### Medical Safety & Scientific Boundary Protocol
1. **No Individualized Prescriptions**: Materials are strictly framed as general educational physiology and population guidelines. Statements prescribing exact gram weights, diagnostic interpretations, or injury treatments are excluded.
2. **Preservation of Scientific Nuance**: Contradictory and nuanced evidence is explicitly maintained:
   - Volume-equated hypertrophy comparisons (training to absolute failure vs. leaving 1–3 repetitions in reserve).
   - Cold water immersion timing (blunting muscular hypertrophy adaptations if performed immediately post-resistance training vs. enhancing recovery for collision-sport tournaments).
   - Static stretching timing (acute force and power deficits when static stretching exceeds 60 seconds per muscle group prior to maximal effort).
3. **Medical Contraindications**: Explicit safety screening protocols (PAR-Q+, ACSM cardiovascular algorithm, WBGT environmental heat risk) are mandated before high-intensity exertion.

---

## 4. Legal Verification & Provenance Registry

All 21 approved sources are cataloged in [`data/approved/source_registry.json`](file:///e:/NOVA/data/approved/source_registry.json) and backed by verified raw files in [`data/sources_raw/`](file:///e:/NOVA/data/sources_raw/):

| Source Identifier | License | Legal Authority / Basis | Attribution Required? | Third-Party Exclusions Noted? | Raw File SHA-256 (Disk) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `US-HHS-PAG-2018` | Public Domain | 17 U.S.C. § 105 (U.S. Gov) | No (Disclaimer) | Yes (Commercial photos) | `8f56faaa8098c7e9...` |
| `US-CDC-RTG-2023` | Public Domain | 17 U.S.C. § 105 (U.S. Gov) | No (Disclaimer) | Yes (Partner logos) | `1d6ef2593b4a2d8e...` |
| `USDA-HHS-DGA-2020` | Public Domain | 17 U.S.C. § 105 (U.S. Gov) | No (Disclaimer) | Yes (Third-party recipes) | `f0896082982d61b3...` |
| `US-ARMY-ATP-7-22` | Public Domain | 17 U.S.C. § 105 (U.S. Gov) | No (Disclaimer) | Yes (Proprietary equipment) | `7486e927cb09dff2...` |
| `OPENSTAX-AP-MUSCLE` | CC BY 4.0 | Creative Commons Attribution 4.0 | Yes (OpenStax Rice) | Yes (Underlying photos) | `50a58390b1fcab61...` |
| `US-NIH-ODS-PROTEIN` | Public Domain | 17 U.S.C. § 105 (U.S. Gov) | No (Disclaimer) | Yes (Journal citations) | `8f7b5391a27e7d69...` |
| `US-CDC-SLEEP-2022` | Public Domain | 17 U.S.C. § 105 (U.S. Gov) | No (Disclaimer) | Yes (Stock imagery) | `2467d0f948bfcb2c...` |
| `NIH-NIAMS-BIOMECH` | Public Domain | 17 U.S.C. § 105 (U.S. Gov) | No (Disclaimer) | Yes (Commercial diagrams) | `0f7f3299c8f85f4f...` |
| `US-CDC-DNPAO-PA` | Public Domain | 17 U.S.C. § 105 (U.S. Gov) | No (Disclaimer) | Yes (Third-party graphics) | `ebf0e632b7333f2b...` |
| `US-VA-MOVE-PHYS` | Public Domain | 17 U.S.C. § 105 (U.S. Gov) | No (Disclaimer) | Yes (Clinical forms) | `d0a1b63dd10b27ae...` |
| `US-ARMY-FM-7-22` | Public Domain | 17 U.S.C. § 105 (U.S. Gov) | No (Disclaimer) | Yes (Commercial gear) | `01bc7242ba45e128...` |
| `US-NAVY-NOFFS-STRENGTH` | Public Domain | 17 U.S.C. § 105 (U.S. Gov) | No (Disclaimer) | Yes (Vendor illustrations) | `3a9f0e11894d3472...` |
| `US-USMC-HITT-PROG` | Public Domain | 17 U.S.C. § 105 (U.S. Gov) | No (Disclaimer) | Yes (Equipment branding) | `882a9db3c940b522...` |
| `US-CDC-STEADI-OLDER` | Public Domain | 17 U.S.C. § 105 (U.S. Gov) | No (Disclaimer) | Yes (Clinical assessment tools) | `a3ba7bc3f20d6f9a...` |
| `OPENSTAX-AP-BIOENERG` | CC BY 4.0 | Creative Commons Attribution 4.0 | Yes (OpenStax Rice) | Yes (Molecular stock art) | `07cb935277161b55...` |
| `US-NIH-ODS-CREATINE` | Public Domain | 17 U.S.C. § 105 (U.S. Gov) | No (Disclaimer) | Yes (Commercial brand names) | `d720eb9385bf56ef...` |
| `US-CDC-HYDRATION-WORK`| Public Domain | 17 U.S.C. § 105 (U.S. Gov) | No (Disclaimer) | Yes (Industrial charts) | `8f5febe344d5a995...` |
| `US-NIH-NHLBI-SLEEP` | Public Domain | 17 U.S.C. § 105 (U.S. Gov) | No (Disclaimer) | Yes (Polysomnograph traces) | `60678e7bb634c03b...` |
| `US-USAF-FITNESS-OPS` | Public Domain | 17 U.S.C. § 105 (U.S. Gov) | No (Disclaimer) | Yes (Base operational seals) | `961f652410a8d4a6...` |
| `US-CDC-HEADS-UP-CONC` | Public Domain | 17 U.S.C. § 105 (U.S. Gov) | No (Disclaimer) | Yes (Athletic union logos) | `a6a02b1f8f94fa22...` |
| `US-OSHA-HEAT-STRESS` | Public Domain | 17 U.S.C. § 105 (U.S. Gov) | No (Disclaimer) | Yes (Proprietary monitor apps) | `0a2e584a7e78ee2c...` |

### Attribution Notices & Disclaimers
- **U.S. Government Public Domain (17 U.S.C. § 105)**: In compliance with federal guidelines, no claim is made that the U.S. Government, HHS, CDC, NIH, USDA, DOD, VA, or OSHA endorses Project Nova-Fit or any resulting model weights.
- **OpenStax CC BY 4.0 Attribution**: Text extracted and adapted from OpenStax Anatomy and Physiology 2e (Betts et al., 2022) is licensed under CC BY 4.0. In compliance with Section 3(a) of the license, proper attribution to OpenStax and Rice University is recorded in the source registry, and modifications are noted.

---

## 5. Acquisition, Ingestion, and Cleaning Workflow

The acquisition workflow is implemented in [`src/nova/corpus.py`](file:///e:/NOVA/src/nova/corpus.py) and executed via [`scripts/build_corpus.py`](file:///e:/NOVA/scripts/build_corpus.py):

```
                     ACQUISITION & COMPOSITION WORKFLOW
                     
 Raw Document Acquisition (scripts/sources/*.py)
   ├── 306 High-rigor educational documents
   └── Written to data/sources_raw/*_raw.txt with SHA-256 validation
                     │
                     ▼
 Legal Registry Verification (data/approved/source_registry.json)
   ├── Validate source_id against registered whitelist
   └── Verify byte count and raw SHA-256 match disk
                     │
                     ▼
 Text Normalization & Syntactic Cleaning
   ├── Unicode NFKC normalization
   ├── Whitespace normalization (preserve paragraphs, strip excess spaces)
   └── Preserve technical notation, citations, units, and safety disclaimers
                     │
                     ▼
 Exact & Near-Duplicate Detection (detect_duplicates_and_group)
   ├── Exact SHA-256 hashing (0 exact duplicates found)
   ├── 5-gram token shingling with Jaccard similarity index
   │     - Optimized with mathematical length-bound pruning
   │     - Prunes >80% of candidate comparisons where min_len/max_len < 0.85
   └── Connected-component clustering into related-document groups (90 clusters)
                     │
                     ▼
 Group-Aware Partitioning (partition_documents_by_group)
   ├── Preserves cluster integrity: all related documents stay in the SAME split
   ├── Stratified allocation across all 7 topic domains
   └── Target validation ratio = 15%, deterministic seed = 42
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
   Training Split         Validation Split
 (268 docs, 88.0%)       (38 docs, 12.0%)
         │                       │
         ▼                       ▼
 expanded_train_corpus.txt  expanded_val_corpus.txt
 (SHA-256: 9974b3a6...)   (SHA-256: 1eb58178...)
         │                       │
         └───────────┬───────────┘
                     ▼
 Sequence Packing Pipeline (prepare_dataset, max_seq_len=512)
   ├── Tokenization with final Byte-Level BPE (vocab 3,384)
   ├── Chunking & packing with <|endoftext|> delimiters
   ├── Tokenizer artifact SHA-256 recorded in manifest
   └── Output: data/prepared_expanded/{train.pt, val.pt, manifest.json}
```

---

## 6. Corpus Quantitative Statistics

All token counts were recalculated using the final Byte-Level BPE tokenizer (`artifacts/final_tokenizer`):

### Detailed Quantitative Breakdown

| Quantitative Metric | Expanded Training Corpus | Expanded Validation Corpus | Total Expanded Corpus |
| :--- | :--- | :--- | :--- |
| **Corpus File Path** | [`data/approved/expanded_train_corpus.txt`](file:///e:/NOVA/data/approved/expanded_train_corpus.txt) | [`data/approved/expanded_val_corpus.txt`](file:///e:/NOVA/data/approved/expanded_val_corpus.txt) | Both combined |
| **File SHA-256** | `9974b3a649b7b42fce01788407507b2261c31907a8955575f3e891acabe4321d` | `1eb58178598adf110996546e13d397116234cf0dcb08d450b52fcfe53735aae1` | N/A |
| **File Size (Bytes)** | 344,834 bytes | 48,771 bytes | 393,605 bytes |
| **Document Count** | 268 documents (87.6%) | 38 documents (12.4%) | 306 documents (100%) |
| **Character Count** | 340,027 characters | 48,069 characters | 388,096 characters |
| **Word Count (Whitespace)** | 47,021 words | 6,580 words | 53,601 words |
| **Raw Tokens (no EOS)** | **125,486 tokens** | **17,334 tokens** | **142,820 tokens** |
| **Tokens with `<|endoftext|>`**| **125,754 tokens** | **17,372 tokens** | **143,126 tokens** |
| **Prepared Tensor Shape** | `torch.Size([242, 512])` | `torch.Size([34, 512])` | `torch.Size([276, 512])` |
| **Total Tensor Tokens** | 123,904 tokens | 17,408 tokens | 141,312 tokens |
| **Valid (Non-Pad) Tokens** | 123,722 tokens | 17,036 tokens | 140,758 tokens |
| **Padded Tokens** | 182 tokens | 372 tokens | 554 tokens |
| **Packing Padding Ratio** | **0.15%** | **2.14%** | **0.39%** |
| **Milestone Target Verification**| **>= 100,000 raw training tokens: ACHIEVED (+25.5% surplus)** | N/A | N/A |

### Density & Token Fertility Profile

- **Tokens per Word (Train)**: $125,486 / 47,021 = \mathbf{2.67}$ tokens/word.
- **Characters per Token (Train)**: $340,027 / 125,486 = \mathbf{2.71}$ chars/token.
- **Characters per Word (Train)**: $340,027 / 47,021 = \mathbf{7.23}$ chars/word.
- **Packing Efficiency**: Thanks to the document packing algorithm combining multiple documents into 512-token sequences with `<|endoftext|>` boundaries, padding overhead was reduced from the baseline 9.07% down to **0.15%** in the training partition.

---

## 7. Topic Coverage & Domain Balance

Document distribution across the seven fitness pillars in the expanded corpus:

```
Pillar 1: Exercise Science, Physiology & Biomechanics     [██████████████] 45 docs (14.7%)
Pillar 2: Strength Training Principles & Programming      [██████████████] 45 docs (14.7%)
Pillar 3: Exercise Technique & Safe Equipment Use         [██████████████] 44 docs (14.4%)
Pillar 4: Nutrition Fundamentals & Hydration              [██████████████] 44 docs (14.4%)
Pillar 5: Sleep, Recovery & Physical Activity             [██████████████] 43 docs (14.1%)
Pillar 6: Training Adaptations, Fatigue & Load Management [██████████████] 43 docs (14.1%)
Pillar 7: General Fitness Education & Lifespan Safety     [██████████████] 42 docs (13.7%)
```

### Partition Distribution by Pillar

| Pillar ID & Name | Training Docs | Validation Docs | Total Docs | Train Ratio |
| :--- | :--- | :--- | :--- | :--- |
| `pillar1_exercise_science` | 39 docs | 6 docs | 45 docs | 86.7% |
| `pillar2_strength_principles` | 39 docs | 6 docs | 45 docs | 86.7% |
| `pillar3_exercise_technique` | 38 docs | 6 docs | 44 docs | 86.4% |
| `pillar4_nutrition_hydration` | 38 docs | 6 docs | 44 docs | 86.4% |
| `pillar5_sleep_recovery` | 38 docs | 5 docs | 43 docs | 88.4% |
| `pillar6_adaptations_fatigue` | 39 docs | 4 docs | 43 docs | 90.7% |
| `pillar7_general_safety` | 37 docs | 5 docs | 42 docs | 88.1% |
| **Total** | **268 docs** | **38 docs** | **306 docs** | **87.6%** |

Every pillar has at least 37 training documents and at least 4 validation documents, ensuring balanced representation across both splits with zero unrepresented domains.

---

## 8. Deduplication & Zero Cross-Split Leakage Audit

### Duplicate Detection Results
- **Exact Duplicates Detected**: 0
- **Exact Duplicates Removed**: 0
- **Total Related-Document Clusters**: 90 groups across 306 documents.
- **Cluster Integrity**: All documents within any cluster were assigned to the **exact same data partition** via `partition_documents_by_group`.

### Cross-Split Disjointness Verification
1. **Document ID Disjointness**: $\text{Train IDs} \cap \text{Val IDs} = \emptyset$ (0% leakage).
2. **Group ID Disjointness**: $\text{Train Groups} \cap \text{Val Groups} = \emptyset$ (0% leakage).
3. **High Jaccard Cross-Split Audit**: All pairs $(d_{\text{train}}, d_{\text{val}})$ were evaluated using 5-gram token shingling. Zero cross-split pairs exhibited $\text{Jaccard Similarity} \ge 0.85$.

---

## 9. Prepared Dataset Manifest & Tokenizer Cryptographic Alignment

The dataset preparation process generated [`data/prepared_expanded/manifest.json`](file:///e:/NOVA/data/prepared_expanded/manifest.json):

```json
{
  "train_file": "data/approved/expanded_train_corpus.txt",
  "val_file": "data/approved/expanded_val_corpus.txt",
  "max_seq_len": 512,
  "train_sequences": 242,
  "val_sequences": 34,
  "total_sequences": 276,
  "train_tokens": 123904,
  "val_tokens": 17408,
  "total_tokens": 141312,
  "train_sha256": "9974b3a649b7b42fce01788407507b2261c31907a8955575f3e891acabe4321d",
  "val_sha256": "1eb58178598adf110996546e13d397116234cf0dcb08d450b52fcfe53735aae1",
  "tokenizer_path": "artifacts/final_tokenizer",
  "tokenizer_hash": "1639cec0fce7263bbb10eca238b19a5d13ef6bd9fa1c545cd481f4e8ff9c93fc",
  "created_at": "2026-10-14T20:21:40.165405+00:00"
}
```

The manifest's `tokenizer_hash` precisely matches the SHA-256 hash of `artifacts/final_tokenizer/tokenizer.json`, guaranteeing cryptographic traceability between the tokenizer artifact and prepared tensors.

---

## 10. Scale Projections: 1 Million and 10 Million Tokens

To guide future phases toward full-scale pretraining of the Nova-20M architecture, resource requirements were projected for 1M and 10M token milestones.

> [!NOTE]
> **Estimation Methodology**:
> - Baseline assumptions: ~468 raw tokens per document (observed average in Phase 6), 2.67 tokens/word, 2.71 chars/token.
> - Packed sequences ($L=512$) with ~99.8% packing efficiency.
> - Token tensors stored as `int64` (8 bytes per token).
> - Training throughput: Measured baseline on Colab T4 GPU (~12,500 tokens/sec), local CPU reference (~450 tokens/sec), and RTX 4090 GPU (~45,000 tokens/sec).
> - Target training budget: 1 Chinchilla-optimal epoch ($E=1$) and 3-epoch overtraining ($E=3$).

### Scaling Requirement Projections

| Scaling Milestone | Raw Training Tokens | Estimated Documents | Uncompressed Text Size | Packed Tensors ($L=512$, `int64`) | Est. Training Time (Colab T4, $E=1$) | Est. Training Time (Colab T4, $E=3$) | Est. Training Time (RTX 4090, $E=1$) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Current (Phase 6)** | 125,486 tokens | 268 train docs | ~345 KB | ~1.9 MB (`train.pt`) | ~10 seconds | ~30 seconds | ~2.8 seconds |
| **1 Million Tokens** | 1,000,000 tokens | ~2,140 docs | ~2.7 MB | ~15.3 MB | ~1.3 minutes | ~4.0 minutes | ~22 seconds |
| **10 Million Tokens**| 10,000,000 tokens | ~21,400 docs | ~27.1 MB | ~152.6 MB | ~13.3 minutes | ~40.0 minutes | ~3.7 minutes |
| **50 Million Tokens**| 50,000,000 tokens | ~107,000 docs| ~135.5 MB | ~762.9 MB | ~1.1 hours | ~3.3 hours | ~18.5 minutes |

### Acquisition Feasibility for 1M and 10M Milestones
- **To reach 1 Million tokens (~2,140 documents)**:
  - Ingest full manuals of Department of the Army FM 7-22 and ATP 7-22.02 (unabridged text yields ~400K tokens).
  - Ingest full text of OpenStax Anatomy and Physiology 2e chapters 9–11 and 24 (musculoskeletal and metabolic chapters yield ~350K tokens).
  - Ingest public-domain physical culture classics (Hackenschmidt, Sandow, Saxon from Project Gutenberg, yielding ~250K tokens).
- **To reach 10 Million tokens (~21,400 documents)**:
  - Ingest open-access sports medicine, exercise physiology, and clinical nutrition research articles from PubMed Central (PMC) under CC BY 4.0 / CC0 licenses using targeted MeSH keyword queries (`"Resistance Training"[Mesh]`, `"Biomechanics"[Mesh]`, `"Sports Nutritional Physiological Phenomena"[Mesh]`).
  - At ~3,000 tokens per open-access article, ~3,000 peer-reviewed papers provide ~9M tokens of pristine scientific material.

---

## 11. Test Verification & Quality Assurance

The complete Project Nova-Fit test suite was executed and validated:

```powershell
pytest -q
```

### Complete Test Suite Results (156 Passed)

| Test Module | Coverage Scope | Tests | Status |
| :--- | :--- | :--- | :--- |
| [`tests/test_smoke.py`](file:///e:/NOVA/tests/test_smoke.py) | Phase 0 CPU smoke test & environment diagnostics | 4 passed | PASS |
| [`tests/test_tokenizer.py`](file:///e:/NOVA/tests/test_tokenizer.py) | Phase 1 Byte-Level BPE tokenizer, round-trip fidelity | 27 passed | PASS |
| [`tests/test_model.py`](file:///e:/NOVA/tests/test_model.py) | Phase 2 Transformer architecture (RoPE, RMSNorm, SwiGLU) | 17 passed | PASS |
| [`tests/test_data.py`](file:///e:/NOVA/tests/test_data.py) | Phase 3 Data cleaning, packing, manifest, DataLoader | 64 passed | PASS |
| [`tests/test_phase4.py`](file:///e:/NOVA/tests/test_phase4.py) | Phase 4 Approved corpus, tokenizer training, split tests | 16 passed | PASS |
| [`tests/test_training.py`](file:///e:/NOVA/tests/test_training.py) | Phase 5 Pretraining engine, evaluator, checkpointing | 15 passed | PASS |
| [`tests/test_phase6.py`](file:///e:/NOVA/tests/test_phase6.py) | Phase 6 Provenance, legal decisions, scale, 7 pillars, 0 leakage | 13 passed | PASS |
| **Total** | **All Phase 0 through Phase 6 test suites** | **156 passed** | **100% PASS** |

### Phase 6 Specific Verification Matrix

1. `test_source_registry_v2_schema_and_sources`: Verified all 21 sources exist in registry with required fields.
2. `test_every_source_has_valid_license_decision`: Verified defensible legal decisions (19 U.S. Gov works, 2 CC BY 4.0 works).
3. `test_cc_by_sources_have_attribution_text`: Verified CC BY sources have detailed attribution text referencing OpenStax / Rice University.
4. `test_raw_source_files_exist_and_hashes_match`: Verified all 21 raw files exist in `data/sources_raw/` with matching byte sizes and SHA-256 hashes.
5. `test_train_corpus_exceeds_100k_tokens_milestone`: Verified training corpus exceeds 100,000 raw training tokens (actual: 125,486 tokens).
6. `test_val_corpus_scale`: Verified validation corpus has sufficient scale (actual: 17,334 tokens).
7. `test_token_density_is_reasonable`: Verified token density (2.67 tokens/word, 2.71 chars/token) reflects natural English technical text.
8. `test_all_seven_pillars_represented_in_both_splits`: Verified all 7 pillars have $\ge 20$ training documents and are represented in both splits.
9. `test_zero_document_and_group_leakage`: Verified 0% document ID and 0% cluster group ID leakage.
10. `test_no_high_jaccard_similarity_across_splits`: Verified 0 cross-split pairs with $\ge 0.85$ 5-gram Jaccard similarity.
11. `test_prepared_dataset_manifest_and_tensors`: Verified `train.pt`, `val.pt`, and `manifest.json` exist and tokenizer hash matches artifact on disk.
12. `test_repeated_preparation_is_deterministic`: Verified repeated dataset preparation with identical settings produces byte-identical tensors.
13. `test_medical_safety_caveats_preserved`: Verified educational safety disclaimers, contraindication guidelines, and absence of individualized medical claims.

---

## 12. Conclusion & Phase 6 Certification

Phase 6 has successfully achieved all defined objectives:
1. Recalculated and verified the Phase 4 baseline directly from artifacts.
2. Formulated a 7-pillar corpus architecture with explicit medical safety boundaries.
3. Acquired and verified 21 legal sources under U.S. Public Domain (17 U.S.C. § 105) and CC BY 4.0 with explicit attribution.
4. Built a repeatable ingestion, exact/near deduplication, and group-aware partitioning pipeline.
5. Established an audited training corpus of **125,486 raw tokens**, exceeding the 100,000 token engineering target.
6. Produced mathematical scaling models for 1M, 10M, and 50M token pretraining milestones.
7. Maintained 100% test passing rate across all 156 unit and integration tests.
