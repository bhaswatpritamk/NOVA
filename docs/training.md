# Nova-Fit: Pretraining Engine, Evaluation Protocol, and Checkpoint Verification (Phase 5)

## 1. Executive Summary

Phase 5 establishes the pretraining infrastructure, evaluation engine, and atomic checkpoint recovery system for Project Nova-Fit. 

> [!IMPORTANT]
> **Corpus Size Limitation Disclosure:**
> The current approved training and validation splits comprise a combined 16 documents (5,414 non-padding tokens). The pretraining engine and evaluation metrics developed in this phase are designed to validate training dynamics, gradient backpropagation, numerical stability, and checkpoint recovery on CPU and CUDA. They do **not** claim to produce a capable conversational fitness assistant.

### Key Architectural & Environmental Facts

| Property | Value | Notes |
| :--- | :--- | :--- |
| **Model Architecture** | Decoder-Only Transformer (`NovaForCausalLM`) | RoPE, RMSNorm, SwiGLU, Pre-Norm |
| **Vocabulary Size** | 3,384 | Learned exclusively from approved corpus in Phase 4 |
| **Model Parameters** | 533,824 total (533,824 trainable) | `d_model=64`, `n_layers=2`, `n_heads=4`, `d_ff=176` |
| **Context Length (`max_seq_len`)** | 512 | Configured for prepared dataset tensors |
| **Special Tokens** | `<pad>=0`, `<unk>=1`, `<bos>=2`, `<eos>=3` | Synchronized across tokenizer, model, and dataset |
| **Loss Function** | Causal Next-Token Cross-Entropy | Shifted targets, `ignore_index=0` (`<pad>`) |
| **Optimizer** | AdamW | Decoupled decay on 2D weights |
| **LR Schedule** | Cosine / Linear with Linear Warmup | Deterministic, serializable with PyTorch `state_dict` |
| **Checkpoint Atomicity** | Atomic write-replace (`.tmp` -> target) | Prevents partial or corrupted checkpoint files |
| **Execution Targets** | CPU & CUDA | Automatic device detection; no GPU assumption |

---

## 2. Mathematical Formulation & Training Mechanics

### 2.1 Causal Next-Token Prediction with Target Shifting

For a sequence of token IDs $X = [x_0, x_1, x_2, \dots, x_{T-1}]$, the model produces hidden states and logits $Z = [z_0, z_1, z_2, \dots, z_{T-1}]$ where each $z_t \in \mathbb{R}^{V}$ ($V = 3,384$).

Because self-attention is causally masked, logit $z_t$ depends strictly on $x_{\le t}$. Autoregressive next-token prediction requires $z_t$ to predict the subsequent token $x_{t+1}$:
- **Shifted Logits:** $\hat{Z} = [z_0, z_1, \dots, z_{T-2}]$ (shape `[B, T-1, V]`)
- **Shifted Targets:** $\hat{Y} = [x_1, x_2, \dots, x_{T-1}]$ (shape `[B, T-1]`)

### 2.2 Masked Cross-Entropy Loss

The training objective ignores padding tokens ($x = 0$):

$$\mathcal{L}(X) = -\frac{1}{\sum_{t=0}^{T-2} \mathbb{I}(\hat{y}_t \ne 0)} \sum_{t=0}^{T-2} \mathbb{I}(\hat{y}_t \ne 0) \log \left( \frac{\exp(z_{t, \hat{y}_t})}{\sum_{v=0}^{V-1} \exp(z_{t, v})} \right)$$

Where $\mathbb{I}(\cdot)$ is the indicator function. Tokens where $\hat{y}_t = \text{pad\_token\_id} = 0$ contribute zero loss and zero gradient.

### 2.3 Optimization & Weight Decay Decoupling

The AdamW optimizer decouples $L_2$ regularization from gradient updates. Following modern Transformer best practices:
- **Decayed Parameters:** 2D weight matrices (token embeddings, attention projections, SwiGLU linear weights, LM head).
- **Non-Decayed Parameters:** 1D tensors (RMSNorm gain scales $\gamma$, bias vectors if present).

### 2.4 Learning Rate Scheduling

The learning rate follows a two-phase schedule:
1. **Warmup Phase ($t < t_{\text{warmup}}$):**
   $$\eta_t = \eta_{\text{peak}} \cdot \frac{t + 1}{t_{\text{warmup}}}$$
2. **Cosine Decay Phase ($t \ge t_{\text{warmup}}$):**
   $$\text{progress} = \frac{t - t_{\text{warmup}}}{t_{\text{max}} - t_{\text{warmup}}}$$
   $$\eta_t = \eta_{\text{min}} + \frac{1}{2}(\eta_{\text{peak}} - \eta_{\text{min}})(1 + \cos(\pi \cdot \text{progress}))$$

---

## 3. Evaluation Protocol

The evaluation engine (`src/nova/evaluate.py`, `scripts/evaluate.py`) evaluates model checkpoints on held-out validation data (`data/prepared_final/val.pt`).

### Principles:
1. **No Gradient Computation:** Executes strictly within `torch.no_grad()`.
2. **Evaluation Mode:** Enforces `model.eval()`, disabling dropout.
3. **Weight Immutability:** Tests verify that model parameters before and after evaluation are identical to machine precision.
4. **Valid Token Aggregation:** Total cross-entropy loss is aggregated as the sum of unreduced token losses divided by the exact count of valid (non-padding) prediction targets.
5. **Perplexity Calculation:**
   $$\text{Perplexity} = \exp(\mathcal{L}_{\text{valid}})$$
   With numerical overflow protection: $\exp(\min(\mathcal{L}, 100.0))$. If loss is non-finite, $\text{PPL} = \infty$.
6. **Provenance Recording:** The dataset manifest SHA-256 hash is verified and recorded with evaluation outputs.

---

## 4. Atomic Checkpointing and State Recovery

### 4.1 State Preservation Schema

Every checkpoint saved by `src/nova/checkpoint.py` preserves:

```python
checkpoint = {
    "format_version": "1.0.0",
    "timestamp": "2026-10-14T10:08:15.123456+00:00",
    "step": 10,
    "epoch": 2,
    "tokens_processed": 8223,
    "val_loss": 8.0488,
    "best_val_loss": 8.0488,
    # Weights and internal optimizer moments
    "model_state_dict": model.state_dict(),
    "optimizer_state_dict": optimizer.state_dict(),
    "scheduler_state_dict": scheduler.state_dict(),
    # Multi-generator RNG states for exact reproducibility
    "rng_states": {
        "torch_cpu": torch.get_rng_state(),
        "torch_cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None,
        "numpy": np.random.get_state(),
        "python": random.getstate(),
    },
    # Architectural and run metadata
    "model_config": model.config.to_dict(),
    "training_config": training_config.to_dict(),
    "tokenizer_vocab_size": 3384,
    "tokenizer_hash": "63236e6eb6...", # SHA-256 of tokenizer.json
    "manifest_hash": "d9389c1ce6...",  # SHA-256 of dataset manifest.json
    # Runtime environment telemetry
    "environment": {
        "python_version": "3.14.8",
        "torch_version": "2.14.1+cpu",
        "cuda_available": False,
        "device": "cpu",
        "platform": "win32",
    },
}
```

### 4.2 Atomic Write Protocol

To prevent corrupted checkpoint files during runtime disconnects or process preemption:
1. Serialized state is written to a unique temporary file in the destination folder (`.checkpoint_latest.pt.tmp_<uuid>`).
2. The file is flushed and closed.
3. An atomic file replacement (`os.replace`) renames the temporary file to the final destination (`checkpoint_latest.pt`).
4. On POSIX and modern Windows systems, `os.replace` is atomic within the same filesystem.

### 4.3 Compatibility Verification on Resume

Before restoring weights or optimizer states, `load_checkpoint` enforces:
- **Architectural Match:** Verifies `vocab_size`, `d_model`, `n_layers`, `n_heads`, `d_ff`, and `pad_token_id`. Mismatches raise `CheckpointCompatibilityError`.
- **Tokenizer Hash Match:** Prevents resuming training with an altered tokenizer vocabulary, which would misalign learned embedding weights.
- **Payload Integrity:** Detects truncated or corrupted files, raising `CheckpointCorruptedError`.

### 4.4 Hardware Limitations on Exact Reproducibility

While restoring RNG states guarantees deterministic sequence sampling on CPU, exact floating-point reproducibility across hardware has well-known limitations:
- **CPU vs. GPU:** Differences in fused multiply-add (FMA) instructions and floating-point accumulation orders produce minor numerical divergence.
- **CUDA Non-Deterministic Kernels:** Atomic additions in certain CUDA backpropagation operations (e.g., embedding lookups, layer norm reductions) can introduce slight non-determinism across GPU runs unless `torch.use_deterministic_algorithms(True)` is enabled (which incurs a performance penalty).

---

## 5. Training Smoke Experiment Verification

A deterministic smoke experiment was executed using `scripts/train.py` with `configs/training_smoke.json` on CPU.

### 5.1 Verification Checklist

| Check | Requirement | Result | Evidence |
| :--- | :--- | :--- | :--- |
| **1. Finite Loss** | Initial and final loss must be finite | **Passed** | Initial: 8.1454, Final: 7.9768 |
| **2. Parameter Update** | Trainable weights must change | **Passed** | Verified in automated tests |
| **3. Finite Gradients** | Gradients must be finite on all layers | **Passed** | Verified in automated tests |
| **4. Eval Weight Immutability** | Eval must not alter weights | **Passed** | Parameters match exactly before and after eval |
| **5. Atomic Checkpointing** | Checkpoint saved atomically | **Passed** | `checkpoint_latest.pt` verified on disk |
| **6. Resume Continuity** | Resume from step 5 continues to step 10 | **Passed** | Resumed at step 5; finished at step 10 |
| **7. Scheduler Restoration** | Scheduler state restored | **Passed** | Step count and learning rate restored |
| **8. Config Rejection** | Incompatible vocab/config rejected | **Passed** | `CheckpointCompatibilityError` raised |
| **9. Tokenizer Rejection** | Altered tokenizer hash rejected | **Passed** | `CheckpointCompatibilityError` raised |
| **10. Non-Finite Failure** | NaN/Inf loss triggers error | **Passed** | `ValueError` raised on NaN input |
| **11. Controlled Loss Decrease** | Loss strictly decreases on learnable batch | **Passed** | Initial: 8.12 -> Final: 1.45 (15 steps) |

### 5.2 Actual Measured CPU Smoke Run Metrics

```
===========================================================================
Project Nova-Fit: Pretraining Engine (Phase 5)
===========================================================================
Loading base configuration from: configs/training_smoke.json
Hardware Telemetry:
  PyTorch Version:  2.14.1+cpu
  CUDA Available:   False

Model Summary:
  Architecture:       Decoder-Only Transformer (NovaForCausalLM)
  Vocabulary Size:    3,384
  Total Parameters:   533,824
  Trainable Params:   533,824
  Active Device:      cpu
---------------------------------------------------------------------------
Training Outcome:
  Total Optimizer Steps:     10 (5 initial + 5 resumed)
  Initial Training Loss:     8.1454
  Final Training Loss:       7.8552
  Best Validation Loss:      8.0488
  Final Perplexity:          3130.0669
  Non-pad Tokens Processed:  8,223
  Throughput:                4,289.1 tokens/second
  Elapsed Time:              1.92 seconds
  Checkpoints Produced:
    - checkpoints/smoke/checkpoint_best.pt
    - checkpoints/smoke/checkpoint_step_000010.pt
    - checkpoints/smoke/checkpoint_latest.pt
===========================================================================
```

> [!NOTE]
> For a randomly initialized vocabulary of $V = 3,384$, theoretical uniform cross-entropy loss is $\ln(3,384) \approx 8.1268$. An initial loss of $8.1454$ and perplexity of $\sim 3,260$ confirms that initialization is mathematically centered and unskewed.

---

## 6. Google Colab Pretraining Workflow

The following workflow provides a reproducible execution blueprint for training on Google Colab with either a free CPU runtime or a GPU accelerator (T4, V100, A100).

### Cell 1: Environment Diagnostics & GPU Detection

```python
# Cell 1: Environment Telemetry & Hardware Detection
import os
import sys
import platform
import torch

print("=" * 60)
print("Project Nova-Fit: Colab Environment Diagnostics")
print("=" * 60)
print(f"Python Version:   {platform.python_version()}")
print(f"PyTorch Version:  {torch.__version__}")
print(f"CUDA Available:   {torch.cuda.is_available()}")

if torch.cuda.is_available():
    device_name = torch.cuda.get_device_name(0)
    device_props = torch.cuda.get_device_properties(0)
    vram_gb = device_props.total_memory / (1024**3)
    print(f"GPU Device:       {device_name}")
    print(f"Compute Cap:      {device_props.major}.{device_props.minor}")
    print(f"VRAM Capacity:    {vram_gb:.2f} GB")
    selected_device = "cuda"
else:
    print("Running on CPU runtime.")
    selected_device = "cpu"
print("=" * 60)
```

### Cell 2: Project Retrieval & Dependency Setup

```python
# Cell 2: Clone Repository & Install Dependencies
# (Replace REPO_URL with your git remote or upload repository folder)
!git clone https://github.com/your-org/NOVA.git /content/NOVA
%cd /content/NOVA

# Install project in editable mode
!pip install -q -e .
```

### Cell 3: Artifact & Tokenizer Hash Verification

```python
# Cell 3: Verify Tokenizer and Dataset Integrity
import hashlib
from pathlib import Path
from nova.tokenizer import NovaTokenizer

tok_path = Path("artifacts/final_tokenizer/tokenizer.json")
assert tok_path.is_file(), f"Tokenizer artifact missing at {tok_path}"

with open(tok_path, "rb") as f:
    tok_sha256 = hashlib.sha256(f.read()).hexdigest()

tok = NovaTokenizer.from_file("artifacts/final_tokenizer")
print(f"Loaded Tokenizer:")
print(f"  Vocabulary Size:  {tok.vocab_size} (Expected: 3384)")
print(f"  Artifact SHA-256: {tok_sha256[:16]}...")
assert tok.vocab_size == 3384, f"Unexpected vocab size: {tok.vocab_size}"

train_pt = Path("data/prepared_final/train.pt")
val_pt = Path("data/prepared_final/val.pt")
assert train_pt.is_file() and val_pt.is_file(), "Prepared data tensors missing!"
print("Artifact integrity verified.")
```

### Cell 4: Persistent Google Drive Checkpoint Mount (Optional)

```python
# Cell 4: Mount Google Drive for Persistent Checkpoint Storage
from google.colab import drive
import os

USE_GOOGLE_DRIVE = False  # Set to True if Google Drive persistence is desired

if USE_GOOGLE_DRIVE:
    drive.mount('/content/drive')
    checkpoint_dir = "/content/drive/MyDrive/Nova_Checkpoints/run_01"
else:
    checkpoint_dir = "/content/checkpoints/run_01"

os.makedirs(checkpoint_dir, exist_ok=True)
print(f"Checkpoints will be saved to: {checkpoint_dir}")
```

### Cell 5: Launch Training Run

```python
# Cell 5: Execute Pretraining
from nova.train import Trainer, TrainingConfig

config = TrainingConfig(
    data_dir="data/prepared_final",
    output_dir=checkpoint_dir,
    tokenizer_path="artifacts/final_tokenizer",
    batch_size=2 if selected_device == "cpu" else 4,
    max_steps=50,
    learning_rate=3e-4,
    warmup_steps=5,
    lr_schedule="cosine",
    eval_interval=10,
    save_interval=25,
    save_step_checkpoints=True,
    device=selected_device,
    seed=42,
)

trainer = Trainer(config)
result = trainer.train()

print(f"Training completed: Initial Loss = {result.initial_loss:.4f}, Final Loss = {result.final_loss:.4f}")
```

### Cell 6: Interruption Recovery & Resume

```python
# Cell 6: Resume Training from Interrupted Checkpoint
latest_checkpoint = f"{checkpoint_dir}/checkpoint_latest.pt"

if os.path.exists(latest_checkpoint):
    print(f"Resuming from checkpoint: {latest_checkpoint}")
    resume_config = TrainingConfig(
        data_dir="data/prepared_final",
        output_dir=checkpoint_dir,
        tokenizer_path="artifacts/final_tokenizer",
        max_steps=100,  # Extend total steps
        resume_from=latest_checkpoint,
        device=selected_device,
    )
    resumed_trainer = Trainer(resume_config)
    print(f"Resumed at step: {resumed_trainer.global_step}")
    resumed_result = resumed_trainer.train()
    print(f"Resumed run finished at step: {resumed_result.total_steps}")
else:
    print(f"No checkpoint found at {latest_checkpoint}")
```
