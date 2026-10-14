# Nova-Fit: Corpus Acquisition Plan & Legal Provenance Strategy

## 1. Executive Summary

Project Nova-Fit is dedicated to training a fitness-specialized language model from randomly initialized weights. Under zero-capital budget and strict legal compliance constraints, pretraining data must be:
1. **Legally Auditable**: Sourced exclusively from materials in the **Public Domain** (e.g., U.S. Federal Government works under 17 U.S.C. § 105) or under explicit permissive licenses (**CC BY 4.0**, **CC0**).
2. **Domain Comprehensive**: Grounded in exercise physiology, resistance training, biomechanics, clinical sports nutrition, sleep architecture, and fitness safety.
3. **Leakage-Free**: Segregated at the document level before tokenization and sequence packing, ensuring zero validation bleed.
4. **Reproducible**: Every document and corpus partition is tied to cryptographic SHA-256 hashes, source registries, and tamper-evident manifests.

Arbitrary web-scraping, copyrighted textbook piracy, paid course scraping, and unverified data downloads are strictly prohibited.

---

## 2. Target Domain Coverage & Approved Sources

The corpus acquisition strategy covers five foundational pillars:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        NOVA-FIT CORPUS DOMAINS                         │
├────────────────────┬────────────────────┬──────────────────────────────┤
│ Domain             │ Primary Focus      │ Approved Initial Sources     │
├────────────────────┼────────────────────┼──────────────────────────────┤
│ 1. Strength &      │ Progressive load,  │ • US Army ATP 7-22.02        │
│    Programming     │ RPE/RIR, sets/reps │ • CDC Muscle-Strengthening   │
│                    │ periodization      │ • HHS PAG Ch 2-4             │
├────────────────────┼────────────────────┼──────────────────────────────┤
│ 2. Biomechanics &  │ Squat, Deadlift,   │ • OpenStax Anatomy (CC BY)   │
│    Physiology      │ Bench, Press,      │ • Army ATP 7-22.02 Drills    │
│                    │ Muscle fibers      │ • NIH NIAMS Bioenergetics    │
├────────────────────┼────────────────────┼──────────────────────────────┤
│ 3. Nutrition       │ Protein synthesis, │ • USDA/HHS DGA 2020-2025     │
│    Fundamentals    │ energy balance,    │ • NIH ODS Exercise Factsheet │
│                    │ hydration, macros  │ • CDC Nutrition Guidelines   │
├────────────────────┼────────────────────┼──────────────────────────────┤
│ 4. Recovery, Sleep │ Sleep architecture,│ • CDC Sleep Recovery Factsheet│
│    & Activity      │ autonomic nervous  │ • HHS PAG Aerobic Guidelines │
│                    │ system, HRV, DOMS  │ • NIH Somatic Recovery       │
├────────────────────┼────────────────────┼──────────────────────────────┤
│ 5. Education &     │ Contraindications, │ • HHS Physical Activity      │
│    Safety          │ warmup, mobility,  │ • CDC Injury Prevention      │
│                    │ form cues          │ • Army Readiness Drills      │
└────────────────────┴────────────────────┴──────────────────────────────┘
```

---

## 3. Legal & Copyright Framework

### U.S. Federal Government Works (17 U.S.C. § 105)
Under United States copyright law, works created by an officer or employee of the U.S. Government as part of their official duties are not subject to copyright protection within the United States and reside in the public domain.
- **CDC, NIH, HHS, USDA, Department of the Army**: Public domain works.
- **Condition**: While commercial and non-commercial training is fully permitted, models and documentation must not claim official endorsement or sponsorship by the U.S. Government or its agencies.

### Creative Commons Attribution (CC BY 4.0)
Materials licensed under CC BY 4.0 (e.g., OpenStax Anatomy and Physiology 2e, and open-access peer-reviewed literature from PubMed Central) permit sharing and adaptation for any purpose, including commercial model training, provided:
- Appropriate credit and attribution are given.
- A link to the license is provided.
- Any modifications made are indicated.

### Prohibited Sources
- Unlicensed fitness blogs and paywalled journalism.
- Copyrighted commercial books (e.g., Starting Strength, Supertraining, NSCA Essentials) without explicit publisher licensing.
- Reddit posts, forums, or proprietary coaching apps without explicit commercial data licenses.

---

## 4. Ingestion, Cleaning & Provenance Pipeline

```
Raw Approved Document
         │
         ▼
Source Whitelist Verification (data/approved/source_registry.json)
         │ [Reject if source_id not registered or SHA-256 mismatch]
         ▼
Exact & Near-Duplicate Detection (hash table & Jaccard token n-gram filter)
         │ [Discard duplicates or group related versions]
         ▼
Text Normalization & Cleansing (strip boilerplate, normalize unicode, validate length)
         │
         ▼
Document-Level Train/Validation Split (val_ratio = 0.10, seed = 42)
  ├── train_docs ──► Frozen Train Corpus (data/approved/train_corpus.txt)
  └── val_docs   ──► Frozen Val Corpus   (data/approved/val_corpus.txt)
         │
         ▼
Tokenization & Packing (NovaTokenizer -> max_seq_len 512 chunks)
  ├── data/prepared_final/train.pt
  ├── data/prepared_final/val.pt
  └── data/prepared_final/manifest.json
```

---

## 5. Scaling Strategy (From Initial Seed to 20M Pretraining)

1. **Phase 4 Initial Approved Corpus**:
   - High-density, pristine textual seeds across all 5 domains.
   - Purpose: Train the final tokenizer, calibrate token fertility, verify document-level splits, and ensure zero leakage.
2. **Phase 5 Scaling**:
   - Expand via open-access PMC papers (CC BY 4.0 / CC0) filtered for sports medicine, biomechanics, and nutrition keywords.
   - Integrate complete historical public-domain physical culture texts from Project Gutenberg (e.g., Sandow, Hackenschmidt).
   - Target token scale: ~5M to ~50M tokens for Nova-20M compute budget on Colab T4.
