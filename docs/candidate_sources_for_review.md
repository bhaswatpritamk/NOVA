# Project NOVA — Candidate Source Ingestion & Review Registry

**Document Version:** 1.0.0  
**Phase:** 8 (Source-Grounded Corpus & Evaluation Benchmark)  
**Status:** Approved Workflow & Candidate Queue Pending Human Legal Review  

---

## 1. Documented Source Acquisition Workflow

To scale Project NOVA towards and beyond the 1,000,000-token engineering milestone and eventually towards Chinchilla-optimal data volume (~400M tokens for Nova-20M), all additional content must pass through a strict 5-stage verification gate:

```
[Candidate Discovery] 
       │
       ▼
[Stage 1: Legal & Licensing Audit] ──(Fails)──> [REJECTED / EXCLUDED]
       │ (Passes: 17 U.S.C. § 105 or CC BY 4.0 / CC0)
       ▼
[Stage 2: Third-Party Content Exclusion] ──> Exclude non-free images, corporate logos, proprietary text
       │
       ▼
[Stage 3: Scientific Grounding & Accuracy Check] ──> Audit against 5-tier claim taxonomy
       │
       ▼
[Stage 4: Text Normalization & Near-Deduplication] ──> Jaccard k-shingle clustering (theta=0.85)
       │
       ▼
[Stage 5: Final Tokenizer Measurement & Manifest Entry] ──> Cryptographic SHA-256 recording
```

### Mandatory Acceptance Criteria
1. **Verifiable Open License & Jurisdiction Boundary**:
   - Primary basis: Official works of the U.S. Federal Government created by federal employees/officers within the scope of their official employment under **17 U.S.C. § 105** (Domestic U.S. Public Domain).
     * *Territorial Scope Note*: 17 U.S.C. § 105 precludes copyright protection within the United States. It does not automatically guarantee worldwide public domain status, as foreign jurisdictions may enforce copyright unless explicitly waived or governed by bilateral conventions.
     * *Contractor Exclusion*: Works prepared by independent contractors, research grantees, or academic consortiums funded by federal grants do NOT automatically fall under § 105 and require proof of formal intellectual property assignment or independent open licensing.
   - Secondary basis: Open-access scientific and educational publications under **Creative Commons Attribution 4.0 International (CC BY 4.0)** or **CC0 1.0 Universal** (Worldwide public domain dedication).
   - Strictly prohibited: Commercial copyrighted books, non-commercial restricted material (CC BY-NC), no-derivatives material (CC BY-ND), or scraping gated subscription journals.
2. **Attribution and Provenance Preservation**:
   - Full statutory attribution, authoring body, publication year, retrieval timestamp, and source URL must be logged in `data/approved/source_registry.json`.
3. **Exclusion of Non-Free Third-Party Elements**:
   - Diagrams, commercial trade names, photographs, and external quotations from third-party copyright holders must be purged before ingestion. Federal reports often include third-party copyrighted figures that do not enter the public domain.
4. **No Synthetic Filler**:
   - Text must never be hallucinated or generated merely to pad token counts. Summaries or syntheses must be formally designated as `educational_synthesis` rather than primary extracts.
5. **Human Review Override Isolation**:
   - Human review overrides are restricted to resolving ambiguous licensing or contractor IP assignment. An override CANNOT bypass text quality filters, health safety screening, or held-out benchmark contamination checks.

---

## 2. Prioritized Candidate Sources for Corpus Scaling (Target: 1M+ Tokens)

The following candidates have been vetted for statutory open access and domain relevance, and are queued for human review and ingestion:

| Candidate ID | Title & Publishing Authority | Legal Basis / License | Target Pillar | Est. Raw Tokens | Review Status |
| :--- | :--- | :--- | :--- | :---: | :---: |
| **CAND-ARMY-FM7-22-FULL** | *U.S. Army Field Manual 7-22: Holistic Health and Fitness (Full Manual)*<br>Headquarters, Dept of the Army (2020) | 17 U.S.C. § 105 (U.S. Federal Work) | Pillars 2, 3, 5, 6, 7 | ~220,000 | Pending Human Review |
| **CAND-ARMY-ATP7-22-FULL** | *U.S. Army ATP 7-22.02: Holistic Health and Fitness Drills & Exercises*<br>Headquarters, Dept of the Army (2020) | 17 U.S.C. § 105 (U.S. Federal Work) | Pillars 2, 3, 6 | ~180,000 | Pending Human Review |
| **CAND-OPENSTAX-AP2E-CH09-11** | *OpenStax Anatomy and Physiology 2e (Chapters 9-11 Full Text)*<br>Betts et al., OpenStax / Rice University (2022) | CC BY 4.0 International | Pillars 1, 3 | ~150,000 | Pending Human Review |
| **CAND-HHS-PAGAC-2018-FULL** | *2018 Physical Activity Guidelines Advisory Committee Scientific Report (Full 779-page Report)*<br>U.S. HHS (2018) | 17 U.S.C. § 105 (U.S. Federal Work) | Pillars 1, 5, 6, 7 | ~380,000 | Pending Human Review |
| **CAND-NASA-SP-2021-HUMAN** | *NASA Human Research Program: Evidence Report on Risk of Impaired Physical Performance*<br>NASA Johnson Space Center (2021) | 17 U.S.C. § 105 (U.S. Federal Work) | Pillars 1, 6 | ~95,000 | Pending Human Review |
| **CAND-NIOSH-HEAT-2016** | *NIOSH Criteria for a Recommended Standard: Occupational Exposure to Heat and Hot Environments*<br>CDC / NIOSH Publication 2016-106 | 17 U.S.C. § 105 (U.S. Federal Work) | Pillars 3, 4, 7 | ~110,000 | Pending Human Review |
| **CAND-PMC-OA-BIOMEC-CCBY** | *Open-Access Sports Biomechanics & Resistance Training Subset*<br>PubMed Central Open Access Subset (Selected CC BY 4.0 articles) | CC BY 4.0 / CC0 | Pillars 1, 2, 6 | ~200,000 | Pending Human Review |
| **Total Pipeline Potential** | | | | **~1,335,000** | |

---

## 3. Human Review & Verification Checklist

Before converting any candidate from `docs/candidate_sources_for_review.md` into an approved record in `data/approved/source_registry.json`, an authorized reviewer must confirm:

1. [ ] **Source Authenticity**: Verify that the document originates from the stated federal or academic agency without unauthorized alterations.
2. [ ] **License Deed Verification**: Inspect the front matter or statutory copyright notice to confirm public domain or CC BY 4.0 terms.
3. [ ] **Attribution Compliance**: Verify exact text string required by publisher (e.g., OpenStax mandatory citation clause).
4. [ ] **Image / Table Cleanse**: Confirm that all third-party photographs, commercial brand references, and non-free tables are removed.
5. [ ] **Scientific Consistency**: Cross-check major assertions against the Nova-Fit 5-tier claim taxonomy (`data/approved/claim_reviews.json`).
6. [ ] **Artifact Hash Sealing**: Calculate raw file SHA-256 digest and register in `source_registry.json`.
