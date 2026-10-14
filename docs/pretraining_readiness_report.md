# Nova-Fit: Pretraining Readiness Audit Report (Phase 7)

## 1. Executive Summary & Readiness Determination

This report provides the formal readiness audit for **Project Nova-Fit** prior to initiating language model pretraining.

Project Nova-Fit is dedicated to training one standalone, fitness-specialized language model from randomly initialized weights. It is not a family of subordinate models.

### Readiness Determination

| Operational Scope | Status | Technical Rationale |
| :--- | :--- | :--- |
| **Pipeline Debugging & Smoke Engine** | **READY** | Pretraining engine, dataset pipeline, tokenizer alignment, causal target shifting, padding exclusion, and atomic checkpointing are verified with 166 passing automated tests. |
| **Small-Scale Exploratory Training (<1M params)** | **READY** | The tiny model (533,824 parameters) can be trained on the current 123K token dataset for 1–2 epochs to validate learning dynamics on CPU. |
| **Full Pretraining of Nova-20M** | **BLOCKED** | The current training corpus (123,722 packed tokens) represents only **0.031% of the Chinchilla compute-optimal corpus** required for a 20M parameter model (~400M tokens). Launching 20M pretraining at this scale guarantees rapid memorization and severe overfitting without generalizable representations. |

> [!IMPORTANT]
> **Audit Conclusion**:
> Long-form pretraining of the **Nova-20M** architecture must be **deferred** until:
> 1. The approved corpus is expanded to at least **5M to 50M tokens** of primary scientific and educational literature.
> 2. Training is transitioned to GPU infrastructure (e.g., Google Colab T4/A100) as documented in [`docs/colab_training_strategy.md`](file:///e:/NOVA/docs/colab_training_strategy.md).

---

## 2. Verified Facts vs. Unresolved Claims

To establish an honest scientific baseline, previous phase reports were cross-examined against disk artifacts:

| Item / Claim | Reported in Phase 6 | Audited Reality (Phase 7) | Status & Finding |
| :--- | :--- | :--- | :--- |
| **Document Count** | 306 documents | 306 documents (268 train, 38 val) | **Verified** from disk |
| **Document Origin** | "Drawn from public domain / CC BY sources" | Structured educational texts authored in `scripts/sources/` | **Clarified**: Synthesized passages, not verbatim primary source text dumps |
| **Raw Source Files** | "data/sources_raw/ populated from sources" | Dumped exports of `scripts/sources/` texts | **Clarified**: Hashes represent dumped generated text, not official agency PDFs |
| **Training Tokens** | 125,486 raw tokens | 125,486 raw body tokens / 123,722 packed tensor tokens | **Verified & Reconciled** mathematically |
| **Validation Tokens** | 17,334 raw tokens | 17,334 raw body tokens / 17,036 packed tensor tokens | **Verified & Reconciled** mathematically |
| **Test Suite** | 156 passed | 166 passed (added 10 Phase 7 regression tests) | **Verified** across all modules |
| **Tokenizer Hash** | `1639cec0fce7...` | `1639cec0fce7263bbb10eca238b19a5d13ef6bd9fa1c545cd481f4e8ff9c93fc` | **Verified** in manifest and on disk |
| **Model Size** | "Nova-20M" vs "533K" | Tiny model = 533,824 params; Nova-20M = 20,301,696 params | **Reconciled**: Distinct configurations |
| **Web Verification** | Verified licenses | License terms verified; verbatim text match unverified offline | **Documented Limitation** |

---

## 3. Source Authenticity & Licensing Audit Findings

### Production Methodology of the 306 Documents
An inspection of [`scripts/sources/`](file:///e:/NOVA/scripts/sources/) and [`scripts/build_corpus.py`](file:///e:/NOVA/scripts/build_corpus.py) reveals how the 306 documents were produced:
1. **Curated Educational Passages**: The 306 documents were authored in Python dictionaries across 17 files in `scripts/sources/`. They were written as structured, textbook-style educational passages grounded in the topics, physiological concepts, and guidelines of the attributed authorities (e.g., HHS Physical Activity Guidelines, CDC STEADI, OpenStax Anatomy & Physiology 2e, Army FM 7-22 / ATP 7-22.02).
2. **Not Direct Verbatim Scrapes**: The documents are **not** automated direct downloads or verbatim scrapings of official government PDF manuals or websites. Rather, they represent transformed educational expositions.
3. **Nature of `data/sources_raw/`**: The raw text files in `data/sources_raw/` were created by `build_corpus.py` concatenating and writing these educational passages to disk. The cryptographic SHA-256 hashes in `source_registry.json` match these local files, not the official publisher PDFs.

### Licensing & Legal Analysis
All 21 registered sources fall under two verifiable legal regimes:
1. **U.S. Federal Government Works (17 U.S.C. § 105)**:
   - 19 of the 21 sources (HHS, CDC, USDA, Army, Navy, USMC, USAF, NIH, NIOSH, OSHA, NASA, VA) are works of the U.S. Federal Government.
   - Under 17 U.S.C. § 105, such works are not subject to copyright in the United States and are in the public domain.
   - Training use, commercial use, and derivative adaptations are permitted.
   - **Restriction**: The models and documentation must not claim official endorsement or sponsorship by the U.S. Government or its agencies.
2. **Creative Commons Attribution 4.0 International (CC BY 4.0)**:
   - 2 sources (`OPENSTAX-AP-MUSCLE` and `OPENSTAX-ANAT-PHYS-2E`) originate from OpenStax Anatomy and Physiology 2e (Betts et al., Rice University).
   - CC BY 4.0 explicitly permits commercial and non-commercial adaptation and model training.
   - **Requirement**: Mandatory attribution to OpenStax / Rice University is recorded in `source_registry.json` and corpus documentation.
3. **Third-Party Exclusions**:
   - Official government publications and OpenStax textbooks frequently include commercial photographs, brand-name equipment, and third-party diagrams under separate copyright.
   - Because our corpus consists of text-only educational passages authored into `scripts/sources/`, **all third-party photographs, logos, and external excerpts were excluded by construction**.

### Unverified External Elements
- Because internet scraping was not executed during Phase 6, exact character-for-character equivalence between these educational summaries and official agency PDF pages was not independently verified against live HTTP endpoints. They must be recognized as **expert-curated educational adaptations**, not primary raw source scans.

---

## 4. Independent Recalculation of Dataset Statistics

Using the actual files and the final Byte-Level BPE tokenizer ([`artifacts/final_tokenizer`](file:///e:/NOVA/artifacts/final_tokenizer)), all statistics were independently recalculated from disk:

### Summary Comparison Table

| Metric | Baseline Train (`train_corpus.txt`) | Baseline Val (`val_corpus.txt`) | Expanded Train (`expanded_train_corpus.txt`) | Expanded Val (`expanded_val_corpus.txt`) |
| :--- | :--- | :--- | :--- | :--- |
| **File SHA-256** | `ac0cb021ff72...` | `3adf4951fa1c...` | `9974b3a649b7...` | `1eb58178598a...` |
| **File Size on Disk** | 18,238 bytes | 7,826 bytes | 369,571 bytes | 52,239 bytes |
| **Extracted Documents** | 11 documents | 5 documents | 268 documents | 38 documents |
| **File Characters (total)**| 18,236 chars | 7,824 chars | 369,368 chars | 52,207 chars |
| **Cleaned Body Chars** | 17,600 chars | 7,225 chars | 340,027 chars | 48,069 chars |
| **File Words (total)** | 2,488 words | 1,004 words | 50,010 words | 7,009 words |
| **Cleaned Body Words** | 2,428 words | 953 words | 47,021 words | 6,580 words |
| **Raw Tokens (body only)**| 3,248 tokens | 2,150 tokens | 125,486 tokens | 17,334 tokens |
| **Packed Tensor Non-Pad**| 3,259 tokens | 2,155 tokens | 123,722 tokens | 17,036 tokens |
| **EOS Tokens in Tensors**| 11 tokens | 5 tokens | 268 tokens | 38 tokens |
| **Packed Sequences ($L=512$)**| 7 sequences | 5 sequences | 242 sequences | 34 sequences |
| **Padded Tokens** | 325 tokens (9.07%) | 405 tokens (15.82%) | 182 tokens (0.15%) | 372 tokens (2.14%) |

### Mathematical Reconciliation of Discrepancies
1. **Raw Body Tokens (125,486) vs. Extracted Tokens with EOS (123,722)**:
   - When `build_corpus.py` computed 125,486 raw tokens, it tokenized each `CorpusDocument.text` before writing to file.
   - When `prepare_dataset()` ran on `expanded_train_corpus.txt`, it read the file with `CleaningConfig(strip_comment_lines=True, strip_section_headers=False, normalize_whitespace=True)`.
   - `extract_documents()` parsed 268 documents and stripped excess whitespace. Tokenizing these 268 cleaned documents plus 1 appended `<|endoftext|>` per document produced exactly **123,722 tokens**.
   - Slicing into 242 sequences of 512 tokens ($242 \times 512 = 123,904$ positions) left $123,904 - 123,722 = \mathbf{182}$ padding positions (0.15% padding).
2. **Validation Partition**:
   - Cleaned documents plus 38 appended EOS tokens produced exactly **17,036 tokens**.
   - Slicing into 34 sequences of 512 tokens ($34 \times 512 = 17,408$ positions) left $17,408 - 17,036 = \mathbf{372}$ padding positions (2.14% padding).
3. **Train/Validation Separation**:
   - Exact text SHA-256 cross-split overlap: **0 documents** ($\emptyset$).
   - Group ID cross-split overlap: **0 groups** ($\emptyset$).
   - Cross-split near-duplicate pairs ($\text{Jaccard} \ge 0.85$ on 5-grams): **0 pairs**.

### Tokenizer Provenance Audit
- Verified [`configs/final_tokenizer.json`](file:///e:/NOVA/configs/final_tokenizer.json):
  ```json
  "corpus_path": "data/approved/train_corpus.txt"
  ```
- The final Byte-Level BPE tokenizer was trained **strictly on the approved training corpus**. All validation data was completely excluded during tokenizer training.
- The tokenizer SHA-256 hash (`1639cec0fce7263bbb10eca238b19a5d13ef6bd9fa1c545cd481f4e8ff9c93fc`) matches both `data/prepared_final/manifest.json` and `data/prepared_expanded/manifest.json`.

---

## 5. Model Architecture & Parameter Reconciliation

The project architecture is an original decoder-only Transformer (`NovaForCausalLM`) implemented from scratch in PyTorch.

### Mathematical Parameter Breakdown
For a vocabulary size $V$, model dimension $d_{\text{model}}$, $N$ layers, and feed-forward dimension $d_{\text{ff}}$:
1. **Token Embeddings**: $P_{\text{embed}} = V \times d_{\text{model}}$
2. **Attention per Layer**: $4 \times d_{\text{model}}^2$ ($W_q, W_k, W_v, W_o$, no bias)
3. **SwiGLU MLP per Layer**: $3 \times d_{\text{model}} \times d_{\text{ff}}$ ($W_{\text{gate}}, W_{\text{up}}, W_{\text{down}}$, no bias)
4. **RMSNorm per Layer**: $2 \times d_{\text{model}}$ (input norm and post-attention norm)
5. **Final RMSNorm**: $d_{\text{model}}$
6. **LM Head Projection**: $P_{\text{head}} = V \times d_{\text{model}}$ (untied; 0 if tied)

$$\text{Total Parameters} = 2 V d_{\text{model}} + N (4 d_{\text{model}}^2 + 3 d_{\text{model}} d_{\text{ff}} + 2 d_{\text{model}}) + d_{\text{model}}$$

### Architecture Comparison Table

| Parameter / Dimension | Tiny Prototype (Phase 1) | Tiny Final (Phase 4–6) | Proposed Nova-20M (Phase 7) |
| :--- | :--- | :--- | :--- |
| **Config File** | `configs/tiny_model.json` | Final Tokenizer on Tiny | [`configs/nova_20m.json`](file:///e:/NOVA/configs/nova_20m.json) |
| **Vocabulary Size ($V$)**| 2,274 | 3,384 | 3,384 |
| **Max Sequence Length ($L$)**| 32 | 512 | 512 |
| **Model Dimension ($d_{\text{model}}$)**| 64 | 64 | **384** |
| **Layers ($N$)** | 2 | 2 | **10** |
| **Attention Heads ($H$)**| 4 | 4 | **8** |
| **Head Dimension ($d_{\text{head}}$)**| 16 | 16 | **48** |
| **FFN Dimension ($d_{\text{ff}}$)**| 176 | 176 | **1,024** |
| **Weight Tying** | False | False | False |
| **Embedding Parameters**| 145,536 | 216,576 | 1,300,416 |
| **Transformer Block Params**| 100,608 | 100,608 | 17,700,480 |
| **Output Head Params** | 145,536 | 216,576 | 1,300,416 |
| **Final RMSNorm Params**| 64 | 64 | 384 |
| **Total Parameter Count**| **391,744** | **533,824** | **20,301,696 (~20.30M)** |

### Architectural Recommendation
1. **Retain the 533K tiny model for pipeline debugging, smoke tests, and CI/CD verification** on CPU.
2. **Formally establish `configs/nova_20m.json`** as the official Nova-20M target architecture specification.
3. **Delay full training of Nova-20M** until the corpus is expanded to 5M–50M tokens and execution is moved to a GPU runtime. Previous checkpoints are preserved.

---

## 6. Corpus-to-Model Mismatch & Chinchilla Scaling Analysis

### The Chinchilla Scaling Law
The Chinchilla scaling law (Hoffmann et al., DeepMind, 2022) establishes that for compute-optimal language model pretraining from random initialization, the number of training tokens ($D$) should scale proportionally with model parameters ($N$):
$$D_{\text{optimal}} \approx 20 \times N$$

For the **Nova-20M** architecture ($N = 20,301,696$ parameters):
$$D_{\text{optimal}} \approx 20 \times 20,301,696 = \mathbf{406,033,920 \text{ tokens}} \approx \mathbf{406 \text{M tokens}}$$

### Current Corpus Comparison
- Our current expanded training corpus contains **123,722 valid packed tokens**.
- Fraction of compute-optimal data:
  $$\frac{123,722}{406,033,920} \approx \mathbf{0.0305\%} \quad (\approx 1/3,300\text{-th of optimal})$$
- Tokens-per-parameter ratio:
  $$\frac{123,722 \text{ tokens}}{20,301,696 \text{ parameters}} \approx \mathbf{0.0061 \text{ tokens/parameter}}$$
  *(Equivalent to **164 parameters per training token**)*

### Multi-Epoch Training & Overfitting Projections

| Epoch Count | Total Tokens Processed | Tokens / Parameter (20M) | Overfitting & Generalization Risk |
| :--- | :--- | :--- | :--- |
| **1 Epoch** | 123,722 tokens | 0.0061 | Under-trained; insufficient gradient steps to converge 20M weights |
| **5 Epochs** | 618,610 tokens | 0.0305 | Early memorization; high risk of training loss divergence from val loss |
| **10 Epochs** | 1,237,220 tokens | 0.0609 | Significant memorization of surface syntax; validation perplexity increases |
| **25 Epochs** | 3,093,050 tokens | 0.1524 | Severe overfitting; near-zero training loss, exploding validation loss |
| **50 Epochs** | 6,186,100 tokens | 0.3047 | Complete memorization; zero generalization capacity |

> [!WARNING]
> **More Epochs Do Not Solve Data Scarcity**:
> In transformer language models, repeating a small dataset over dozens of epochs does not simulate a larger corpus. Instead, the model quickly memorizes exact phrases, degrading its ability to generate coherent or novel sentences.

### Measured Throughput vs. Projections

| Metric / Scenario | Hardware | Model Configuration | Measured / Projected | Throughput | Epoch Time (123K tokens) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Phase 5 Smoke Test** | Intel/AMD CPU | Tiny 533K (`d_model=64`, 2 layers) | **Measured** | 2,401.1 tokens/sec | ~51.5 seconds |
| **Phase 7 Audit Test** | Intel/AMD CPU | Tiny 533K (`d_model=64`, 2 layers) | **Measured** | 689.0 tokens/sec | ~179.6 seconds |
| **Nova-20M on CPU** | Intel/AMD CPU | Nova-20M (`d_model=384`, 10 layers)| *Projected (CPU)* | ~20 to ~60 tokens/sec | ~35 to ~100 minutes |
| **Nova-20M on GPU** | Colab T4 GPU | Nova-20M (`d_model=384`, 10 layers)| *Unmeasured Projection*| ~12,500 tokens/sec | ~10 seconds |

All GPU throughput estimates remain **unmeasured projections** until validated in a live Colab T4/A100 session.

---

## 7. Pretraining Infrastructure Verification

A live pretraining infrastructure test was conducted using [`scratch/test_train_infra.py`](file:///C:/Users/Bhaswat/.gemini/antigravity-ide/brain/f1c13ac6-bf48-4fda-b9e8-b92bc9da383e/scratch/test_train_infra.py):

### Infrastructure Verification Checklist
- [x] **Random Weight Initialization**: Independent instances produce distinct weight tensors. Initial weights match Gaussian $\mathcal{N}(0, 0.02^2)$ (mean = $-0.00003$, std = $0.02001$).
- [x] **Autoregressive Target Alignment**: Targets are shifted right by 1 position (`targets = seqs[:, 1:]` predicted by `logits[:, :-1]`).
- [x] **Padding Masking**: Loss computed with `ignore_index=0` matches loss on valid tokens only ($\text{difference} = 0.00\text{e}+00$).
- [x] **Initial Loss Sanity**: Initial training loss ($8.1372$) matches theoretical uniform cross-entropy $\ln(3384) \approx 8.1268$.
- [x] **Finite Loss Convergence**: 5 training steps on `data/prepared_expanded` reduced loss from $8.1372 \to 8.0190$ with finite validation loss ($8.0012$, perplexity $2984.65$).
- [x] **Atomic Checkpointing & Resumption**: Checkpoint saved at step 5; resumption restored model weights and 2-group AdamW optimizer state with bitwise identity.

---

## 8. Complete Test Suite Audit Results

All unit and integration tests across the entire repository were executed:
```powershell
pytest -q
```
**Test Result**: **166 passed in 26.54s (100% pass rate)**.

### Breakdown by Test Module
- [`tests/test_smoke.py`](file:///e:/NOVA/tests/test_smoke.py): 4 passed (Phase 0 environment & deterministic smoke)
- [`tests/test_tokenizer.py`](file:///e:/NOVA/tests/test_tokenizer.py): 27 passed (Phase 1 Byte-Level BPE tokenizer)
- [`tests/test_model.py`](file:///e:/NOVA/tests/test_model.py): 17 passed (Phase 2 Transformer architecture)
- [`tests/test_data.py`](file:///e:/NOVA/tests/test_data.py): 64 passed (Phase 3 Dataset preparation & DataLoader)
- [`tests/test_phase4.py`](file:///e:/NOVA/tests/test_phase4.py): 16 passed (Phase 4 Approved baseline & tokenizer)
- [`tests/test_training.py`](file:///e:/NOVA/tests/test_training.py): 15 passed (Phase 5 Pretraining engine & checkpoints)
- [`tests/test_phase6.py`](file:///e:/NOVA/tests/test_phase6.py): 13 passed (Phase 6 Provenance, scale, 7 pillars)
- [`tests/test_phase7.py`](file:///e:/NOVA/tests/test_phase7.py): 10 passed (Phase 7 Readiness audit, parameter reconciliation, scaling mismatch)

---

## 9. Final Recommendations & Roadmap to Pretraining

1. **Do Not Launch Long-Form 20M Pretraining Today**:
   Pretraining Nova-20M on 125,000 tokens will cause severe memorization without producing a functional general-purpose model.
2. **Execute Diagnostic Smoke Run on Tiny Model**:
   Run a short 20-step smoke run on the 533K tiny model using `data/prepared_expanded` to verify pipeline logging, checkpoint rotation, and validation evaluation.
3. **Phase 8 Milestone — Expand Corpus to $\ge 5\text{M}$ Tokens**:
   Ingest complete primary-source public-domain texts:
   - Full unabridged text of U.S. Army FM 7-22 and ATP 7-22.02 (~1M tokens).
   - Full musculoskeletal and metabolic chapters of OpenStax Anatomy and Physiology 2e (~400K tokens).
   - PubMed Central (PMC) open-access sports science and nutrition literature under CC BY / CC0 (~4M tokens).
4. **Transition to GPU (Google Colab)**:
   Mount the expanded dataset in a Colab T4 GPU notebook to execute pretraining at ~12,500 tokens/sec.
