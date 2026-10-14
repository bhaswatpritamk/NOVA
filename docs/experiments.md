# Nova-Fit: Experiment & Model Artifact Log

## Experiment Run: EXP-PHASE4-TOK-FINAL (2026-10-14)

### Objective
Train the project's final Byte-Level BPE tokenizer from scratch exclusively on the legally audited, frozen approved training corpus (`data/approved/train_corpus.txt`), establishing the finalized vocabulary for Nova-Fit before Transformer pretraining.

---

### Artifact Versions & Provenance

| Component | Prototype (Phase 1) | Final (Phase 4) | Status |
| :--- | :--- | :--- | :--- |
| **Corpus Source** | `data/raw/fitness_smoke_corpus.txt` | `data/approved/train_corpus.txt` | Frozen & Audited |
| **Corpus SHA-256** | `b90548dcb22d2bd5552...` | `ac0cb021ff722f7222bea57...` | Verified |
| **Corpus Size** | 8,800 bytes (7 docs) | 18,238 bytes (11 docs) | Cleaned text |
| **Target Vocab Size** | 8,000 | 8,000 | Configured |
| **Actual Vocab Size** | 2,274 | 3,384 | BPE Merges Exhausted |
| **Tokenizer Config** | `configs/tokenizer.json` | `configs/final_tokenizer.json` | Preserved Side-by-Side |
| **Tokenizer Artifacts** | `artifacts/tokenizer/` | `artifacts/final_tokenizer/` | Both Available |
| **Prepared Dataset** | `data/prepared/` (3 seqs) | `data/prepared_final/` (12 seqs) | Tensors & Manifest |
| **Model Parameters** | 391,744 (vocab 2,274) | 533,824 (vocab 3,384) | Verified on CPU |

---

### Special-Token Alignment

Both tokenizers strictly maintain identical special token mapping:
- `pad_token`: `<pad>` -> ID `0`
- `unk_token`: `<unk>` -> ID `1`
- `bos_token`: `<bos>` -> ID `2`
- `eos_token`: `<eos>` -> ID `3`

---

### Tokenizer Fertility & Efficiency

Evaluating across diverse fitness test sentences (lifting terminology, biomechanics, sets/reps, nutrition units, punctuation, emojis, OOV terms):
- **Average Characters per Token**: 2.34
- **Average Tokens per Word**: 2.81
- **Round-Trip Exact Match**: 100% across all categories
- **Out-of-Vocabulary (OOV) Robustness**: 0 `<unk>` emissions (byte fallback guarantees lossless coverage)
- **Unicode Support**: Emojis (e.g., 🏋️‍♂️) and special units (℃, ±) encoded and decoded with byte-level fidelity.

---

## Experiment Run: EXP-PHASE5-TRAIN-SMOKE (2026-10-14)

### Objective
Validate causal Transformer pretraining infrastructure, target shifting, masked cross-entropy, AdamW optimization, evaluation without weight modification, atomic checkpointing, and interruption recovery on CPU.

### Configuration & Hardware
- **Hardware Target**: CPU (Intel/AMD, Windows, Python 3.14.8, PyTorch 2.14.1+cpu)
- **Model Architecture**: `NovaForCausalLM` (2 layers, `d_model=64`, 4 heads, `d_ff=176`, `vocab_size=3384`, `max_seq_len=512`)
- **Parameters**: 533,824 total (533,824 trainable)
- **Data Source**: `data/prepared_final/train.pt` (7 seqs) and `data/prepared_final/val.pt` (5 seqs)
- **Optimizer**: AdamW (`lr=1e-3`, `weight_decay=0.01`, cosine schedule with 2 warmup steps)
- **Checkpoints**: `checkpoints/smoke/` (`checkpoint_best.pt`, `checkpoint_step_000010.pt`, `checkpoint_latest.pt`)

### Execution Telemetry
| Phase | Step Range | Initial Loss | Final Loss | Best Val Loss | Val Perplexity | Tokens Processed | Runtime (s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Initial Run** | 0 → 5 | 8.1454 | 7.9768 | 8.0896 | 3260.54 | 4,274 | 1.78s |
| **Resumed Run** | 5 → 10 | 7.9411 | 7.8552 | 8.0488 | 3130.07 | 8,223 | 1.92s |

### Findings & Verification
1. **Mathematical Initialization**: Initial training loss ($8.1454$) closely matches theoretical uniform cross-entropy $\ln(3384) \approx 8.1268$.
2. **Deterministic Resumption**: Checkpoint at step 5 restored model, optimizer, scheduler, and RNG state; continuation advanced smoothly to step 10.
3. **Loss Dynamics**: Training loss decreased from $8.1454$ to $7.8552$; validation loss improved from $8.0896$ to $8.0488$.
4. **Padding Masking**: 405 padding tokens in validation set were strictly excluded from loss and perplexity.
5. **Limitations**: Seed corpus is diagnostic only; not indicative of domain fitness conversational mastery.

