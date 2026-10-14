# Nova-Fit: Google Colab Training & Compute Strategy

## 1. Operating Philosophy: Dual-Environment Architecture

Project Nova-Fit strictly separates **local development** from **cloud accelerator execution**:

| Component | Local Computer (Workstation) | Google Colab (Cloud Accelerator) |
| :--- | :--- | :--- |
| **Role** | Primary development, architecture design, unit testing, git management | Model training, throughput benchmarking, GPU evaluation |
| **Compute Profile** | CPU only (16 GB RAM, no dedicated GPU) | Ephemeral GPU runtime (e.g., NVIDIA T4, V100, A100 when allocated) |
| **Cost** | ₹0 | ₹0 (Free tier allocation) |
| **Data & Artifacts** | Code, tests, configs, documentation tracked in Git | Large datasets & checkpoints stored in Google Drive (excluded from Git) |
| **Invocation Style** | Direct CLI (`powershell`, `bash`, `pytest`) | Headless CLI invoked via Colab notebook cells (`!python ...`) |

---

## 2. Phase 0 Principles & Safeguards

1. **Provider-Independent Code**: All Python scripts in `scripts/` and modules in `src/nova` must remain agnostic of Google Colab, Jupyter, or proprietary cloud APIs. They must execute seamlessly from standard operating system command lines.
2. **Terminal-First & Notebook-Callable**: Any script executable locally via `python scripts/<name>.py --flags` can be invoked in Colab via `!python scripts/<name>.py --flags`.
3. **Zero Local GPU Requirement**: Local development never assumes the presence of CUDA. CPU execution is the default fallback for all Phase 0 scripts and tests.
4. **No Premature Model Training**: Phase 0 establishes reproducibility, verification, and diagnostics. No Transformer implementation or training jobs are initiated.

---

## 3. Ephemeral Runtime Management & Checkpointing Strategy (For Subsequent Phases)

Google Colab free-tier runtimes are **temporary, interruptible, and stateless**. A session may disconnect due to idle timeouts (90 minutes), total connection limits (12 hours max, often less), or quota preemptions.

### 3.1 Persistent Storage via Google Drive
All persistent assets (checkpoints, tokenized shards, experiment logs) must reside outside the ephemeral `/content` directory:
```python
from google.colab import drive
drive.mount('/content/drive')
```
Target persistent directory structure:
```
/content/drive/MyDrive/nova_fit/
├── checkpoints/
│   ├── checkpoint_step_000500.pt
│   ├── checkpoint_step_001000.pt
│   └── checkpoint_latest.pt
├── logs/
│   └── run_20261014_metadata.jsonl
└── data/
    └── tokenized_shards/
```

### 3.2 State Preservation Schema (Atomic Checkpointing)
A valid checkpoint is not merely model weights; it must allow exact, mathematically deterministic resumption. Checkpoints must preserve:

```python
checkpoint = {
    # 1. Model parameters
    "model_state_dict": model.state_dict(),
    # 2. Optimizer internal moments
    "optimizer_state_dict": optimizer.state_dict(),
    # 3. Learning rate scheduler progress
    "scheduler_state_dict": scheduler.state_dict() if scheduler else None,
    # 4. Deterministic Random Number Generator (RNG) states across devices
    "rng_state_cpu": torch.get_rng_state(),
    "rng_state_cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None,
    # 5. Training progression metadata
    "step": current_step,
    "tokens_processed": total_tokens_processed,
    "epoch": current_epoch,
    # 6. Run configuration & loss metrics
    "config": model_and_training_config,
    "train_loss": current_train_loss,
    "val_loss": current_val_loss,
    "timestamp": time.time(),
}
```

### 3.3 Atomic Write Protocol
To prevent corrupted checkpoints caused by mid-write runtime terminations, write checkpoints atomically via a temporary file:
```python
import os
import torch

def save_atomic_checkpoint(checkpoint: dict, target_path: str):
    tmp_path = target_path + ".tmp"
    torch.save(checkpoint, tmp_path)
    os.replace(tmp_path, target_path)  # Atomic on POSIX filesystems
```

### 3.4 Mandatory Checkpoint Recovery Verification
Before launching extended training:
1. Run training for 20 steps and save `checkpoint_step_000020.pt`.
2. Terminate the Python process (or restart runtime).
3. Reload `checkpoint_step_000020.pt` and restore model, optimizer, scheduler, and RNG states.
4. Execute step 21: verify that loss and gradients match the continuous run to within machine precision.

---

## 4. Hardware Diagnostic & GPU Memory Inspection Procedure

Never assume a specific GPU model, VRAM limit, or CUDA compute capability. Run the diagnostic suite upon starting every Colab session.

### 4.1 Invoking the Provider-Independent Diagnostics Script
In a Colab cell, execute:
```bash
!python scripts/environment_report.py
```

### 4.2 Inline Colab Hardware Inspection Snippet
```python
import sys
import torch

print("=" * 64)
print("GOOGLE COLAB ACCELERATOR & MEMORY CHECK")
print("=" * 64)
print(f"Python Runtime : {sys.version.split()[0]}")
print(f"PyTorch Version: {torch.__version__}")

if torch.cuda.is_available():
    dev_count = torch.cuda.device_count()
    dev_name = torch.cuda.get_device_name(0)
    cap = torch.cuda.get_device_capability(0)
    free_bytes, total_bytes = torch.cuda.mem_get_info(0)
    
    print(f"CUDA Available : True ({dev_count} device(s) detected)")
    print(f"Primary Device : {dev_name}")
    print(f"Compute Cap.   : {cap[0]}.{cap[1]}")
    print(f"Total VRAM     : {total_bytes / (1024**3):.2f} GiB")
    print(f"Free VRAM      : {free_bytes / (1024**3):.2f} GiB")
    print(f"Allocated VRAM : {torch.cuda.memory_allocated(0) / (1024**2):.2f} MiB")
else:
    print("CUDA Available : False (Running on CPU runtime)")
    print("Action Required: Go to Runtime -> Change runtime type -> T4 GPU")
print("=" * 64)
```

---

## 5. Measured Throughput Benchmarking vs. Naive Extrapolation

Never calculate total training time based on theoretical FLOPs or desktop estimations.

1. **Warmup Steps**: Run 10 initial forward/backward batches to warm up CUDA kernels, memory allocators, and PyTorch autograd engine.
2. **Measure Actual Throughput**:
   $$\text{Throughput} = \frac{\text{Tokens in Batch} \times \text{Measurement Steps}}{\text{Elapsed Time (seconds)}} \quad [\text{tokens/sec}]$$
3. **Compute Real Runtime Budget**:
   $$\text{Estimated Hours} = \frac{\text{Dataset Total Tokens} - \text{Processed Tokens}}{\text{Measured Throughput} \times 3600}$$
4. **Session Splitting**: If estimated duration exceeds 4 hours, partition the training plan into multiple discrete sessions orchestrated around verified checkpoints.

---

## 6. Experiment Metadata & Telemetry Recording

Every training session must append an immutable telemetry record (e.g., in `metadata.jsonl` in Google Drive) containing:

```json
{
  "experiment_id": "nova_20m_run_01",
  "timestamp_start": 1792000000,
  "elapsed_seconds": 3612.4,
  "hardware": {
    "device_name": "Tesla T4",
    "compute_capability": "7.5",
    "vram_total_gib": 14.75,
    "system_ram_gib": 12.68
  },
  "software": {
    "pytorch_version": "2.14.1+cu124",
    "python_version": "3.11.x"
  },
  "hyperparameters": {
    "batch_size": 32,
    "sequence_length": 256,
    "learning_rate": 0.0003,
    "weight_decay": 0.1
  },
  "progress": {
    "start_step": 1000,
    "end_step": 2500,
    "tokens_processed": 12288000,
    "throughput_tokens_per_sec": 3402.1
  },
  "metrics": {
    "initial_train_loss": 5.421,
    "final_train_loss": 3.104,
    "final_val_loss": 3.287
  }
}
```

---

## 7. Phase 0 Readiness Checklist

- [x] Local CPU smoke test passes (`python scripts/smoke_test.py`).
- [x] Deterministic seed reproducibility verified.
- [x] Automated test suite passes (`pytest -v`).
- [x] Hardware diagnostics script handles CPU and CUDA VRAM details.
- [x] Datasets and checkpoints excluded from git repository.
- [x] Dual-environment Colab training strategy fully documented.
