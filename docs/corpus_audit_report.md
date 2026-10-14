# Nova-Fit: Corpus Audit Report (Phase 4)

## 1. Executive Summary & Audit Declaration

This audit report documents the legal provenance, composition, cleaning, duplicate handling, and statistical profile of the initial approved training and validation corpora for **Project Nova-Fit**.

> [!IMPORTANT]
> **Corpus Volume & Diversity Assessment**:
> The current approved corpus is an **initial seed corpus** (16 documents, 24,825 characters, 3,381 words, 5,414 tokens). It is designed to establish reproducible data hygiene, verify document-level train/validation separation, and train the project's final tokenizer. It is **NOT** a full production pretraining corpus (which requires 5M to 50M tokens for Nova-20M).
> 
> Furthermore, automated text cleaning and validation guarantee syntactic hygiene, encoding fidelity, and structural integrity, but **do not independently guarantee empirical or medical truth**. Scientific uncertainty and health safety caveats are explicitly preserved in the text and documented herein.

---

## 2. Source Provenance & Legal Verification

All ingested materials have been verified against the approved source registry at [`data/approved/source_registry.json`](file:///e:/NOVA/data/approved/source_registry.json):

| Source Identifier | Publishing Entity | License | Legal Authority / Basis | Attribution Requirements |
| :--- | :--- | :--- | :--- | :--- |
| `US-HHS-PAG-2018` | U.S. Dept. of Health and Human Services | Public Domain | 17 U.S.C. § 105 (U.S. Gov Work) | No federal endorsement claimed |
| `US-CDC-RTG-2023` | Centers for Disease Control and Prevention | Public Domain | 17 U.S.C. § 105 (U.S. Gov Work) | No CDC endorsement claimed |
| `USDA-HHS-DGA-2020` | U.S. Dept. of Agriculture & HHS | Public Domain | 17 U.S.C. § 105 (U.S. Gov Work) | No USDA endorsement claimed |
| `US-ARMY-ATP-7-22` | Headquarters, Dept. of the Army | Public Domain | 17 U.S.C. § 105 (U.S. Gov Work) | Public release; distribution unlimited |
| `OPENSTAX-AP-MUSCLE` | OpenStax / Rice University | CC BY 4.0 | Creative Commons Attribution 4.0 | Betts et al. (2022) Rice University |
| `US-NIH-ODS-PROTEIN` | NIH Office of Dietary Supplements | Public Domain | 17 U.S.C. § 105 (U.S. Gov Work) | No NIH endorsement claimed |
| `US-CDC-SLEEP-2022` | Centers for Disease Control and Prevention | Public Domain | 17 U.S.C. § 105 (U.S. Gov Work) | No CDC endorsement claimed |

### Cryptographic Hashes (SHA-256)
- **Approved Train Corpus** (`data/approved/train_corpus.txt`):
  `ac0cb021ff722f7222bea57167dbe6da44f40384f71461f94ea596d3a6ffb266` (18,238 bytes)
- **Approved Val Corpus** (`data/approved/val_corpus.txt`):
  `3adf4951fa1c6f8531e04285db4e90bc63de27b8b583c551b1ace36a224ba955` (7,826 bytes)
- **Smoke Fixture** (`data/raw/fitness_smoke_corpus.txt`):
  `b90548dcb22d2bd5552d8577c472858c274d6c014a8a82af14acc1447c147e6d` (8,800 bytes)

---

## 3. Corpus Quantitative Profile

### Split Breakdown

| Metric | Frozen Training Corpus | Frozen Validation Corpus | Total Approved Corpus |
| :--- | :--- | :--- | :--- |
| **Source File** | `data/approved/train_corpus.txt` | `data/approved/val_corpus.txt` | Both combined |
| **Total Documents** | 11 | 5 | 16 |
| **Total Characters** | 17,600 | 7,225 | 24,825 |
| **Total Words** | 2,428 | 953 | 3,381 |
| **Total Lines** | 118 | 49 | 167 |
| **Avg Chars / Document** | 1,600.0 | 1,445.0 | 1,551.6 |
| **Avg Words / Document** | 220.7 | 190.6 | 211.3 |
| **Total Tokens (Final Vocab)** | 3,248 | 2,150 | 5,414 |
| **Packed Sequences (L=512)** | 7 sequences | 5 sequences | 12 sequences |

---

## 4. Leakage Prevention & Duplicate Audit

### Document-Level Splitting
To eliminate cross-chunk contamination, splitting is conducted at the **document level prior to tokenization and sequence packing**.
- Training documents and validation documents originate from distinct sections and chapters.
- Zero documents or partial paragraphs are shared between train and validation partitions.

### Duplicate Detection Results
Using normalized SHA-256 hash sets and 5-gram Jaccard similarity indexing:
- **Exact Duplicates Detected**: 0
- **Exact Duplicates Removed**: 0
- **Near-Duplicates Flagged (>0.85 Jaccard)**: 0
- **Disjointness Verification**: Intersection between train document hashes and validation document hashes is **strictly empty** ($\emptyset$).

---

## 5. Domain Diversity & Thematic Balance

```
Pillar 1: Strength Training & Progressive Overload     [██████████] 28%
Pillar 2: Exercise Biomechanics & Movement Execution   [█████████ ] 25%
Pillar 3: Clinical & Sports Nutrition Fundamentals     [████████  ] 20%
Pillar 4: Recovery, Sleep Architecture & Autonomic ANS [██████    ] 15%
Pillar 5: Fitness Safety, Warmup & Injury Prevention   [████      ] 12%
```

### Safety Caveats & Scientific Uncertainty
The corpus explicitly preserves medical disclaimers and physiological nuance:
- Clear warnings regarding pre-existing cardiovascular risk factors and consulting healthcare professionals before maximal exertion.
- Scientific nuance regarding repetitions in reserve (RIR 1–3 vs. training to absolute muscular failure).
- Caloric and hydration guidelines presented as empirical ranges (e.g., 1.6–2.2 g/kg/day protein, 200–400 kcal surplus) rather than dogmatic absolutes.

---

## 6. Phase 6 Expansion & Baseline Recalculation Note

As part of **Phase 6: Corpus Expansion and Data Quality**, the baseline figures above were recalculated directly from artifacts:
- **Baseline Training Corpus**: 11 docs, 17,600 chars, 2,428 words, 3,248 raw tokens (3,259 tokens with EOS), 7 packed sequences ($L=512$, 325 padded tokens).
- **Baseline Validation Corpus**: 5 docs, 7,225 chars, 953 words, 2,150 raw tokens (2,155 tokens with EOS), 5 packed sequences ($L=512$, 405 padded tokens).
- **Baseline Total**: 16 docs, 24,825 chars, 3,381 words, 5,398 raw tokens, 5,414 tokens with EOS.

### Transition to Phase 6 Expanded Corpus
- **Expanded Training Corpus** (`data/approved/expanded_train_corpus.txt`): 268 documents, 340,027 characters, 47,021 words, **125,486 raw tokens** (125,754 with EOS), 242 packed sequences, 182 padded tokens (0.15% padding).
- **Expanded Validation Corpus** (`data/approved/expanded_val_corpus.txt`): 38 documents, 48,069 characters, 6,580 words, **17,334 raw tokens** (17,372 with EOS), 34 packed sequences, 372 padded tokens (2.14% padding).
- **Expanded Total**: 306 documents, 388,096 characters, 53,601 words, **142,820 raw tokens**, 276 packed sequences.
- **Source Registry**: Upgraded to v2.0 (`data/approved/source_registry.json`) tracking 21 sources with raw text hashes in `data/sources_raw/`.

For the complete legal audit, seven-pillar curriculum matrix, and 1M/10M token scaling projections, consult the [Phase 6 Corpus Expansion Report](file:///e:/NOVA/docs/corpus_expansion_report.md).
