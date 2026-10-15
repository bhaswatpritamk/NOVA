# Project NOVA: Phase 10 Source-Review and Approval Workflow

**Document Version:** 1.0.0  
**Phase:** 10 (Verified Fitness Corpus Expansion)  
**Status:** Authoritative Project Standard  

---

## 1. Purpose and Scope

Project NOVA requires scaling its fitness-specialized training corpus from the current educational baseline (~140K tokens across train and validation) towards the engineering milestone of **5,000,000+ usable training tokens**, and eventually towards Chinchilla-optimal data volume for Nova-20M.

Because NOVA is an AI model specialized in human health, exercise physiology, and athletic performance, data scaling must **never compromise on legal provenance, factual grounding, or user safety**. 

This document defines the mandatory, auditable, multi-stage review process that every external source must complete before any document or text token may be approved for inclusion in the official pretraining corpus.

---

## 2. The 7-Stage Verification Gate

Every candidate source must pass through all seven sequential verification gates. Failure at any gate results in immediate rejection or quarantine.

```
[Candidate Discovery & Acquisition]
               │
               ▼
   [Stage 1: Legal & Licensing Audit] ──────(Non-compliant)─────► [REJECTED]
               │ (17 U.S.C. § 105 / CC BY / CC0 / Approved Override)
               ▼
   [Stage 2: Non-Free Element Purge] ──────────────────────────► Exclude logos, third-party photos, external quotes
               │
               ▼
   [Stage 3: Multi-Format Text Extraction & Normalization] ────► HTML / MD / TXT / PDF parsing, NFKC, boilerplate strip
               │
               ▼
   [Stage 4: Health & Fitness Safety Screening] ─(Critical Hazard)► [QUARANTINED] (Medical advice, extreme diets, PEDs)
               │ (Passed Safety Gate)
               ▼
   [Stage 5: Benchmark Contamination Screening] ─(Contaminated)──► [QUARANTINED] (Zero 8-gram leakage against benchmark)
               │ (Clean Held-Out Separation)
               ▼
   [Stage 6: Deduplication & Near-Duplicate Clustering] ───────► Normalized SHA-256 & Jaccard shingle grouping
               │
               ▼
   [Stage 7: Cryptographic Sealing & Human Sign-off] ──────────► Register SHA-256 in manifest & source registry
```

---

## 3. Detailed Verification Criteria

### Stage 1: Legal & Licensing Audit

Public availability does **not** grant copyright permission to ingest or train on material. Every source must have an explicit, defensible legal basis allowing commercial and non-commercial model training.

#### Permitted Legal Bases:
1. **Official Works of the U.S. Federal Government under 17 U.S.C. § 105**:
   - Material authored by officers or employees of the U.S. Federal Government as part of official duties is in the Public Domain worldwide.
   - Authoritative agencies: CDC, HHS, NIH, NIAMS, NASA, USDA, Department of the Army, NIOSH.
   - Statutory notice: No governmental endorsement of commercial models or products may be implied.
2. **Creative Commons Zero 1.0 Universal (CC0)**:
   - Complete worldwide waiver of copyright and database rights.
3. **Creative Commons Attribution 4.0 International (CC BY 4.0)** (and CC BY 3.0):
   - Permissive open-access license granting adaptation, commercial use, and derivative dataset creation.
   - Mandatory requirement: Exact publisher-specified attribution text must be preserved in all documentation, manifests, and model releases.
4. **Open Government Licences (e.g. UK OGL v3.0)**:
   - Permissive government licenses with standard attribution conditions.

#### Strictly Prohibited Licenses:
- **Non-Commercial Restrictions (CC BY-NC)**: Incompatible with open or commercial model release and production deployment.
- **No-Derivatives Restrictions (CC BY-ND)**: Prohibits tokenization, sequence packing, and derivative weight training.
- **Proprietary Copyright / All Rights Reserved**: Standard commercial books, paywalled journals, scraped blogs, and fitness magazines.
- **Unknown or Ambiguous Licenses**: If copyright status cannot be positively verified with statutory text or front-matter notice, the source **must be rejected**.

#### Human Review Override Protocol:
In rare cases where an author or institution grants a formal bilateral license or open data agreement for model training:
- An authorized legal reviewer must record their formal reviewer ID, date, and justification notes.
- The status is logged as `APPROVED_WITH_OVERRIDE` in the machine-readable manifest.

---

### Stage 2: Non-Free Element Purge

Many open-access textbooks (such as OpenStax) or federal reports embed third-party images, diagrams, commercial brand photographs, or quoted copyrighted excerpts under fair-use or non-transferable permissions.
- All figures, anatomical diagrams, and photographic plates must be stripped.
- Commercial brand logos, fitness equipment trademarks, and commercial supplement product names must be purged.
- External quoted poetry, epigraphs, or third-party boxed features must be excluded.

---

### Stage 3: Multi-Format Text Extraction & Hygiene

Raw acquired files in HTML, Markdown, Plain Text, or PDF format must be processed through the standardized extraction engine (`src/nova/ingestion.py`):
1. **Extraction**:
   - HTML: Parse using semantic tree parsers; purge `<script>`, `<style>`, `<nav>`, `<header>`, `<footer>`, `<aside>`, `<form>`, `<svg>`.
   - Markdown: Strip image syntax `![alt](url)`, convert links `[text](url)` to plain text, strip code blocks.
   - PDF: Extract raw text streams or parse via verified PDF parsers without OCR distortion.
2. **Text Normalization**:
   - Unicode normalization to NFKC.
   - Standardization of quotes, dashes, hyphens, and whitespace.
   - Removal of pagination strings ("Page 1 of 50"), download stamps, cookie banners, navigation links, and terms of service.
3. **Quality Gates**:
   - Minimum character count: 150 characters.
   - Minimum word count: 25 words.
   - Maximum repetition ratio on 10-word shingles: 0.35 (rejects padded filler).
   - Maximum non-ASCII ratio: 0.20 (rejects binary corruption or OCR garbage).

---

### Stage 4: Health and Fitness Safety Screening

To prevent the model from learning hazardous fitness advice, all candidate text is screened for safety violations:
1. **Medical Diagnosis & Treatment**:
   - Diagnosing specific clinical orthopedic conditions (e.g., lumbar disc herniations, labral tears, meniscus tears).
   - Prescribing prescription pharmaceuticals or NSAID regimens without medical credentials.
   - Curative claims for chronic pathology (cancer, diabetes, heart disease).
2. **Extreme Dieting & Dehydration**:
   - Severe starvation diets (<800 kcal/day) without clinical monitoring.
   - Extreme dry fasting or dangerous fluid restriction.
   - Dehydration protocols using sweat suits or diuretics for acute weight cuts.
3. **Prohibited Performance-Enhancing Substances**:
   - Prescribing anabolic-androgenic steroids, SARMs, DNP, clenbuterol, or ephedra.
   - Recommending unregulated detox teas or rapid fat-loss wraps with diuretic/laxative risks.
4. **Exercise Contraindications & Red Flags**:
   - Encouraging users to "push through" sharp, radiating, joint, or spinal pain.
   - Instructing users to ignore chest pain, syncope, dizziness, or severe shortness of breath.
5. **Scientific Myths**:
   - Spot reduction of adipose tissue.
   - Lactic acid as the causal mechanism of 48-hour delayed onset muscle soreness.

*Action*: Any document containing Critical or High-severity violations without medical context or disclaimers is immediately assigned `QUARANTINED` status and removed from training datasets.

---

### Stage 5: Benchmark Contamination Screening

Project NOVA maintains a 12-question diagnostic evaluation benchmark (`data/benchmark/fitness_eval_benchmark.json`) covering all 7 pillars and 8 question archetypes:
- Basic factual, mechanistic, workout planning, numerical reasoning, safety referral, uncertainty/conflicting evidence, insufficient information, and unanswerable claims.

To preserve the empirical validity of downstream evaluation:
- Candidate text is compared against all benchmark prompts and canonical reference answers.
- Exact word n-grams (8-gram and 13-gram) are evaluated.
- Any document exhibiting overlap with benchmark prompts or answers is flagged with `benchmark_contamination=True` and **permanently quarantined**.

---

### Stage 6: Deduplication & Near-Duplicate Clustering

To prevent token inflation and model memorization:
1. **Exact Deduplication**:
   - Normalized text is hashed using SHA-256. Exact duplicates are silently dropped from the training set.
2. **Near-Duplicate Clustering**:
   - Text is indexed into 5-character shingles.
   - Jaccard similarity is computed across document pairs.
   - Pairs with Jaccard similarity $\ge 0.85$ are merged into connected components using Disjoint Set Union (Union-Find).
   - Near duplicates are assigned the same `group_id`.

---

### Stage 7: Source-Level Splitting & Cryptographic Sealing

To prevent train/validation contamination:
1. **Source-Level & Group-Aware Partitioning**:
   - Partitioning is performed at the macro level (`source_id::group_id`) prior to any chunking or sequence packing.
   - All documents sharing a source ID or a near-duplicate group ID reside strictly within either the training set or the validation set.
   - Zero document, group, or source cross-split leakage is permitted.
2. **Cryptographic Sealing**:
   - The raw source file SHA-256 digest is verified.
   - The normalized document content SHA-256 is recorded.
   - Token counts are computed using the authoritative Byte-Level BPE tokenizer (`artifacts/final_tokenizer/tokenizer.json`, vocab size 3,384, SHA-256 `1639cec0fce7263bbb10eca238b19a5d13ef6bd9fa1c545cd481f4e8ff9c93fc`).
   - A machine-readable manifest (`phase10_manifest.json`) is generated and signed with the run timestamp.

---

## 4. Human Reviewer Verification Checklist

Before any candidate source from `docs/candidate_sources_for_review.md` is approved and ingested, an authorized human reviewer must verify and check off the following items:

- [ ] **1. Source Origin & Authenticity**: Verify that the text originates directly from the official agency, publisher, or repository without intermediate web-scraping alterations.
- [ ] **2. Statutory License Deed**: Inspect the official front matter, imprint page, or copyright statement to confirm 17 U.S.C. § 105, CC0, or CC BY 4.0 status.
- [ ] **3. Attribution Text Verification**: Confirm the exact wording required by the publisher (e.g., OpenStax mandatory citation clause) is recorded.
- [ ] **4. Third-Party Exclusion**: Inspect text to confirm that proprietary photographs, corporate logos, and commercial trademarks have been stripped.
- [ ] **5. Scientific Consistency & Uncertainty**: Confirm that contested topics (e.g., nutrient timing, stretching before power events) preserve scientific nuance rather than dogmatic claims.
- [ ] **6. Safety Verification**: Confirm that exercise contraindications and medical referral boundaries are strictly upheld.
- [ ] **7. Benchmark Separation**: Confirm that the source text has zero n-gram leakage into the 12 held-out benchmark questions.
- [ ] **8. Cryptographic Hash Sealing**: Compute raw file SHA-256 and register in the source registry.

---

## 5. Review Decision Outcomes

| Outcome | Criteria | Ingestion Pipeline Action |
| :--- | :--- | :--- |
| **APPROVED** | Passes all 7 stages; verifiable open license; clean quality; safe; uncontaminated. | Approved for source-level train/val partition and token packing. |
| **APPROVED_WITH_OVERRIDE** | Non-standard license, but verified written bilateral research exemption signed off by human reviewer. | Approved with documented reviewer ID and justification notes in manifest. |
| **QUARANTINED** | Safety hazard detected (medical diagnosis, dangerous PEDs, extreme diet) OR benchmark contamination detected. | Quarantined in `quarantine_manifest`; excluded from training and validation sets. |
| **REJECTED** | Incompatible license (CC BY-NC, CC BY-ND, Proprietary) OR corrupted/repetitive text failing quality criteria. | Dropped at ingestion gate with logged rejection reason. |
| **PENDING_REVIEW** | Candidate source documented in registry/queue, but awaiting human legal or factual audit. | Staged in candidate queue; not processed into pretraining datasets. |
