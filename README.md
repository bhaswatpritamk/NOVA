# Nova-Fit: Fitness-Specialized Language Model

> **Project Objective**: Build an original, fitness-specialized language model trained from scratch (randomly initialized weights) dedicated to exercise science, strength training, nutrition fundamentals, recovery, physiology, biomechanics, and fitness education.

Target base model: Decoder-only Transformer (~20M parameters), optimized for lightweight local and edge deployment (including future Android mobile inference).

---

## Current Status: Phase 9 (Google Colab Accelerator Benchmark & Training Pilot)

- **Phase 0 (Completed)**: Reproducible foundation, PyTorch CPU smoke test, diagnostic reporting, and environment verification.
- **Phase 1 (Completed)**: Byte-Level BPE Tokenizer built from scratch using Hugging Face `tokenizers` library with explicit special-token handling, strict input validation, round-trip fidelity, and portable artifact serialization.
- **Phase 2 (Completed)**: Tiny decoder-only Transformer implemented from scratch in PyTorch with Token Embeddings, Rotary Position Embeddings (RoPE), Causal Multi-Head Self-Attention, RMSNorm, SwiGLU feed-forward networks, next-token cross-entropy loss, and CPU smoke test verification.
- **Phase 3 (Completed)**: Reproducible, auditable fitness-text dataset preparation pipeline with text cleaning, document extraction, sequence packing (512 max seq len), deterministic train/val splitting, cryptographic SHA-256 provenance tracking (`manifest.json`), and PyTorch Dataset/DataLoader integration.
- **Phase 4 (Completed)**: Approved fitness corpus acquisition plan, legal provenance registry (`source_registry.json`), frozen train and val corpora (16 documents, 24,825 characters), final Byte-Level BPE tokenizer trained from scratch (3,384 vocab), token fertility evaluation (2.81 tokens/word, 100% round-trip fidelity), and complete Phase 4 test suite (128 tests passing).
- **Phase 5 (Completed)**: Pretraining engine (`src/nova/train.py`, `scripts/train.py`), evaluation engine with zero weight mutation (`src/nova/evaluate.py`, `scripts/evaluate.py`), atomic checkpointing with full state restoration (`src/nova/checkpoint.py`), strict compatibility verification, and 143 passing tests.
- **Phase 6 (Completed)**: Baseline audit recalculation, 7-pillar corpus architecture, 21 approved sources (U.S. Public Domain 17 U.S.C. § 105 and CC BY 4.0), raw text repository (`data/sources_raw/`), repeatable acquisition and near-deduplication pipeline (`src/nova/corpus.py`), zero cross-split leakage, scale target achieved (**125,486 raw training tokens**, 242 packed sequences, 0.15% padding), 1M/10M token scaling projections, and 156 passing tests.
- **Phase 7 (Completed)**: Pretraining readiness audit, source authenticity investigation (curated educational texts vs verbatim downloads), independent dataset recalculation, architecture parameter reconciliation (533K tiny vs 20.30M Nova-20M in `configs/nova_20m.json`), Chinchilla scaling law mismatch assessment (0.006 tokens/param vs 20 tokens/param optimal), infrastructure smoke verification, and 166 passing automated tests.
- **Phase 8 (Completed)**: Source-grounded content pipeline and held-out evaluation benchmark. Delivered full traceability for all 306 educational documents (`document_traceability.json`), 5-tier scientific claim review taxonomy (`src/nova/claims.py`, `claim_reviews.json`), documented acquisition workflow and candidate source queue for scaling past 1M+ tokens (`docs/candidate_sources_for_review.md`), held-out 12-item fitness evaluation benchmark across all 7 pillars and 8 question types with 0 n-gram leakage (`fitness_eval_benchmark.json`), baseline evaluation script (`scripts/evaluate_benchmark.py`), and 174 passing automated tests.
- **Phase 9 (Completed)**: Google Colab accelerator benchmark and training pilot. Reconciled authoritative tokenizer (`1639cec0...`) and manifest (`9ebb8353...`) SHA-256 hashes. Integrated FP16/BF16 Automatic Mixed Precision (`torch.amp.GradScaler`) in the training engine. Created reproducible Google Colab workflow (`notebooks/phase9_colab_benchmark.ipynb`) covering runtime detection, artifact validation, T4 GPU benchmarking, 20.3M feasibility (>85% VRAM headroom), bounded 20-step pilot training, atomic Google Drive checkpoint persistence, and bit-level logit parity restoration (0.0 max diff). Added 16 automated tests in `tests/test_phase9.py` (**190 passing automated tests** across the project). Authored comprehensive benchmark report (`docs/phase9_accelerator_benchmark_report.md`). Full pretraining remains responsibly blocked pending corpus expansion.

---

## Repository Structure

```
NOVA/
├── .gitignore               # Strict exclusion for weights, datasets, .venv, artifacts
├── pyproject.toml           # Package configuration and pytest settings
├── requirements.txt         # Pinned reproducible dependencies
├── README.md                # Project documentation and quickstart
├── src/
│   └── nova/               # Core Nova package
│       ├── __init__.py      # Package entrypoint & public exports
│       ├── tokenizer.py     # NovaTokenizer (Byte-Level BPE, encode/decode, save/load)
│       ├── model.py         # NovaForCausalLM (RoPE, RMSNorm, SwiGLU, CausalAttention)
│       ├── data.py          # Dataset pipeline (cleaning, packing, manifest, duplicate detection)
│       ├── corpus.py        # Corpus acquisition, provenance registry, grouping, deduplication
│       ├── checkpoint.py    # Resumable, atomic checkpoint serializer & loader
│       ├── evaluate.py      # Validation evaluator (loss, perplexity, padding exclusion)
│       ├── train.py         # Pretraining engine (Trainer, AdamW, LR schedule, accumulation)
│       ├── claims.py        # Phase 8 5-tier claim taxonomy, safety heuristics & traceability
│       └── benchmark.py     # Phase 8 Held-out evaluation benchmark, rubrics & contamination
├── scripts/
│   ├── environment_report.py # System, hardware, and PyTorch diagnostic report
│   ├── smoke_test.py         # Phase 0 deterministic CPU MLP training smoke test
│   ├── train_tokenizer.py    # Phase 1 & 4 Byte-Level BPE tokenizer training script
│   ├── model_smoke_test.py   # Phase 2 Tiny Transformer architecture smoke test
│   ├── prepare_dataset.py    # Phase 3 & 4 Dataset preparation CLI script
│   ├── evaluate_tokenizer.py # Phase 4 Tokenizer fertility & robustness evaluator
│   ├── train.py              # Phase 5 Pretraining CLI script with checkpoint resumption
│   ├── evaluate.py           # Phase 5 Checkpoint & validation evaluation CLI script
│   ├── build_corpus.py       # Phase 6 Automated corpus acquisition & preparation pipeline
│   ├── build_traceability_and_claims.py # Phase 8 Traceability & claim review dataset generator
│   ├── build_benchmark.py    # Phase 8 Held-out evaluation benchmark generator & contamination check
│   ├── evaluate_benchmark.py # Phase 8 Reproducible benchmark evaluation harness
│   └── sources/              # Phase 6 Rigorous educational documents across all 7 pillars
│       ├── pillar1_exercise_science.py & pillar1_part2.py
│       ├── pillar2_strength_principles.py & pillar2_part2.py
│       ├── pillar3_exercise_technique.py & pillar3_part2.py
│       ├── pillar4_nutrition_hydration.py & pillar4_part2.py
│       ├── pillar5_sleep_recovery.py & pillar5_part2.py
│       ├── pillar6_adaptations_fatigue.py & pillar6_part2.py
│       ├── pillar7_general_safety.py & pillar7_part2.py
│       └── pillars_part3.py, pillars_part4.py, pillars_part5.py
├── tests/
│   ├── __init__.py
│   ├── test_smoke.py        # Phase 0 smoke test & environment validation (4 tests)
│   ├── test_tokenizer.py    # Phase 1 tokenizer verification (27 tests)
│   ├── test_model.py        # Phase 2 Transformer architecture correctness (17 tests)
│   ├── test_data.py         # Phase 3 Dataset pipeline & DataLoader tests (64 tests)
│   ├── test_phase4.py       # Phase 4 Approved corpus, tokenizer & split tests (16 tests)
│   ├── test_training.py     # Phase 5 Pretraining, evaluation, & checkpoint tests (15 tests)
│   ├── test_phase6.py       # Phase 6 Provenance, legal decisions, scale, 7 pillars (13 tests)
│   ├── test_phase7.py       # Phase 7 Readiness audit, parameter reconciliation (10 tests)
│   ├── test_phase8.py       # Phase 8 Traceability, claims, benchmark & separation (8 tests)
│   └── test_phase9.py       # Phase 9 Accelerator benchmark, AMP, recovery & pilot (16 tests)
├── notebooks/
│   └── phase9_colab_benchmark.ipynb # Phase 9 Google Colab accelerator benchmark & pilot workflow
├── configs/
│   ├── tokenizer.json       # Phase 1 Byte-Level BPE prototype configuration
│   ├── final_tokenizer.json # Phase 4 Final Byte-Level BPE configuration
│   ├── tiny_model.json      # Phase 2 Tiny Transformer configuration (392K params)
│   ├── prototype_model.json # Phase 9 Prototype model configuration (533K params)
│   ├── nova_20m.json        # Phase 7 & 9 Nova-20M target architecture configuration (20.30M params)
│   ├── dataset.json         # Phase 3 Dataset preparation configuration
│   ├── dataset_final.json   # Phase 4 Approved dataset preparation configuration
│   ├── dataset_expanded.json # Phase 6 Expanded dataset preparation configuration
│   ├── training_smoke.json  # Phase 5 Pretraining smoke configuration on CPU
│   ├── training_colab_pilot.json # Phase 9 Controlled Colab pilot training configuration
│   └── training_colab_20m_pilot.json # Phase 9 Nova-20M feasibility pilot configuration
├── data/
│   ├── raw/
│   │   └── fitness_smoke_corpus.txt # Original version-controlled fitness text fixture
│   ├── sources_raw/         # Phase 6 raw text exports for 21 sources (with SHA-256)
│   ├── approved/            # Version-controlled registry (corpora ignored in git)
│   │   ├── source_registry.json     # Legal provenance registry (v2.0, 21 sources)
│   │   ├── document_traceability.json # Phase 8 Traceability records for all 306 documents
│   │   ├── claim_reviews.json       # Phase 8 Audited scientific claims across 5-tier taxonomy
│   │   ├── train_corpus.txt         # (Git-ignored) Baseline approved train text
│   │   ├── val_corpus.txt           # (Git-ignored) Baseline approved val text
│   │   ├── expanded_train_corpus.txt # Phase 6 expanded train text (125K raw tokens)
│   │   └── expanded_val_corpus.txt   # Phase 6 expanded val text (17K raw tokens)
│   ├── benchmark/           # Phase 8 Held-out evaluation benchmark
│   │   └── fitness_eval_benchmark.json # 12 held-out questions across 7 pillars & 8 types
│   ├── prepared/            # Prototype prepared dataset (train.pt, val.pt, manifest.json)
│   ├── prepared_final/      # Phase 4 prepared dataset (train.pt, val.pt, manifest.json)
│   └── prepared_expanded/   # Phase 6 expanded prepared dataset (242 train seqs, manifest.json)
├── checkpoints/             # Model checkpoints (ignored in git) (.gitkeep)
│   └── smoke/               # Checkpoint artifacts from Phase 5 smoke experiment
├── artifacts/
│   ├── tokenizer/           # Prototype tokenizer artifacts (2,274 vocab)
│   └── final_tokenizer/     # Phase 4 Final tokenizer artifacts (3,384 vocab)
└── docs/
    ├── environment_setup.md # In-depth setup, Colab GPU checks, and operations
    ├── colab_training_strategy.md # Cloud training architecture and persistence
    ├── tokenizer.md         # Phase 1 tokenizer interface, config, and GGUF/Android analysis
    ├── architecture.md      # Phase 2 Transformer mathematical specification & scaling
    ├── dataset_pipeline.md  # Phase 3 Dataset pipeline, cleaning, packing & manifest spec
    ├── corpus_acquisition_plan.md # Phase 4 Legal acquisition plan across fitness pillars
    ├── corpus_audit_report.md     # Phase 4 Corpus provenance, volume & duplicate audit
    ├── corpus_expansion_report.md # Phase 6 Corpus expansion, legal audit, & scale targets
    ├── pretraining_readiness_report.md # Phase 7 Pretraining readiness audit & scaling analysis
    ├── candidate_sources_for_review.md # Phase 8 Scaling acquisition workflow & candidate queue
    ├── phase8_corpus_quality_report.md # Phase 8 Content traceability, claims & benchmark report
    ├── experiments.md       # Phase 4 & 5 Experiment log & execution telemetry
    └── training.md          # Phase 5 Pretraining engine, checkpointing, & Colab workflows
```


---

## Quickstart

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.14).
- Git.

### 2. Create and Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

### 4. Run Environment Diagnostics
```powershell
python scripts/environment_report.py
```
*(Prints Python version, OS, CPU cores, RAM, disk space, PyTorch version, and CUDA status)*

### 5. Run CPU Smoke Test
```powershell
python scripts/smoke_test.py
```
*(Executes deterministic CPU training on synthetic data and verifies that loss decreases)*

### 6. Train Tokenizer on Smoke Corpus
```powershell
python scripts/train_tokenizer.py
```
*(Trains Byte-Level BPE tokenizer from scratch on `data/raw/fitness_smoke_corpus.txt` and saves artifacts to `artifacts/tokenizer`)*

### 7. Run Phase 2 Transformer Model Smoke Test
```powershell
python scripts/model_smoke_test.py
```
*(Verifies tiny Transformer initialization, 391,744 parameter count, forward pass, causal attention non-leakage, and controlled loss reduction on CPU)*

### 8. Prepare Pretraining Dataset (Smoke Fixture)
```powershell
python scripts/prepare_dataset.py
```
*(Cleans smoke corpus, tokenizes documents, packs sequences of max_seq_len 512, splits train/val sets, writes `data/prepared/{train.pt, val.pt, manifest.json}`)*

### 9. Train Final Tokenizer on Approved Training Corpus
```powershell
python scripts/train_tokenizer.py -c data/approved/train_corpus.txt -o artifacts/final_tokenizer --config configs/final_tokenizer.json
```
*(Trains final Byte-Level BPE tokenizer on audited, legally verified public-domain training corpus to `artifacts/final_tokenizer`)*

### 10. Evaluate Tokenizer Fertility & Unicode Robustness
```powershell
python scripts/evaluate_tokenizer.py
```
*(Evaluates token fertility, unit handling, Unicode emojis, and round-trip fidelity on representative fitness text)*

### 11. Prepare Final Pretraining Dataset
```powershell
python scripts/prepare_dataset.py --config configs/dataset_final.json
```
*(Processes approved frozen train and val corpora with document-level splitting and provenance auditing, saving to `data/prepared_final/`)*

### 12. Run Phase 6 Corpus Acquisition & Preparation Pipeline
```powershell
python scripts/build_corpus.py
```
*(Ingests 306 verified educational documents across all 7 fitness pillars, registers 21 sources to `source_registry.json`, validates raw hashes in `data/sources_raw/`, detects exact/near duplicates, performs group-aware splitting with zero leakage, achieves 125,486 raw training tokens, and prepares packed tensors in `data/prepared_expanded/`)*

### 13. Run Complete Automated Test Suite
```powershell
pytest
```
*(Runs complete 166-test suite across Phases 0–7 with 100% pass rate)*

---

## Cloud GPU & Colab Workflow

Google Colab is the designated execution environment for GPU training, while local workstations serve as the primary development environment.
- In-depth training and persistence architecture: [`docs/colab_training_strategy.md`](docs/colab_training_strategy.md)
- Environment setup and non-assumptive CUDA verification: [`docs/environment_setup.md`](docs/environment_setup.md)

All scripts are provider-independent and can be executed either directly in a local terminal or called from Colab notebook cells (e.g., `!python scripts/environment_report.py`).

---

## Project Constraints

- **From Scratch**: Trained from randomly initialized weights. No pretrained models (e.g. LLaMA, GPT, Mistral) are used.
- **Strict Budget**: ₹0 capital cost constraint.
- **Git Exclusions**: Raw datasets, training checkpoints (`*.pt`, `*.bin`, `*.safetensors`), and virtual environments are strictly untracked.
