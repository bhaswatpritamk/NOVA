# Nova-Fit Environment Setup & Diagnostics Guide

This document describes how to configure, verify, and test the local development environment for **Project Nova-Fit**, as well as how to inspect CUDA acceleration in cloud environments such as Google Colab.

---

## 1. System Requirements & Architecture Constraints

- **Python**: Supported versions: Python 3.10 through 3.14.
- **Operating System**: Windows, macOS, or Linux.
- **Hardware Profile (Phase 0)**:
  - Local CPU development (16 GB RAM recommended, no dedicated local GPU required).
  - Training budget: ₹0.
  - Compute targets: CPU for development/testing, free cloud GPU notebooks for training, mobile/Android for future edge deployment.
- **Strict Phase 0 Rule**: No pretrained language models, no large datasets, no Transformer implementation until environment and reproducibility are verified.

---

## 2. Setting Up the Local Python Virtual Environment

### Step 2.1: Clone & Navigate to Repository
```powershell
cd e:\NOVA
```

### Step 2.2: Create Virtual Environment
Using Python 3.10+:
```powershell
# Windows (PowerShell)
python -m venv .venv
```
```bash
# Linux / macOS
python3 -m venv .venv
```

### Step 2.3: Activate Virtual Environment
- **Windows (PowerShell)**:
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
  *(If execution policies restrict script running, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`)*
- **Windows (Command Prompt / cmd.exe)**:
  ```cmd
  .venv\Scripts\activate.bat
  ```
- **Linux / macOS (bash / zsh)**:
  ```bash
  source .venv/bin/activate
  ```

### Step 2.4: Upgrade pip & Install Dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

---

## 3. Running Environment Diagnostics

The script `scripts/environment_report.py` inspects the machine's hardware, Python executable, CPU count, measurable RAM, workspace disk space, PyTorch build, and CUDA availability.

### Execution Command:
```powershell
python scripts/environment_report.py
```

### JSON Format (Machine-Readable):
```powershell
python scripts/environment_report.py --json
```

### Expected Output Summary:
- **Python**: Shows active Python interpreter and version.
- **OS**: Windows / Linux / Darwin with architecture.
- **CPU**: Logical and physical core count.
- **RAM**: Total and currently available physical memory.
- **Disk**: Total and available workspace drive capacity.
- **PyTorch**: Framework version.
- **CUDA**: On local machines without an NVIDIA GPU, this reports `Not Available (CPU mode)` which is normal and expected for local Phase 0 development.

---

## 4. Running the CPU Smoke Test

The script `scripts/smoke_test.py` validates tensor operations, automatic differentiation, optimizer step execution, and reproducibility on CPU.

### What it tests:
- Generates a synthetic dataset of 128 samples ($X \in \mathbb{R}^{128 \times 8}, y \in \mathbb{R}^{128 \times 1}$).
- Initializes a 2-layer MLP (`Linear(8, 16) -> ReLU -> Linear(16, 1)`) on CPU with a deterministic seed (`seed=42`).
- Optimizes using MSELoss and Adam for 25 steps.
- Asserts that final loss is strictly lower than initial loss and achieves $\ge 50\%$ relative reduction.

### Execution Command:
```powershell
python scripts/smoke_test.py
```

### Expected Exit Code:
- `0`: Smoke test passed.
- `1`: Smoke test failed (loss did not decrease or threshold not met).

---

## 5. Running the Automated Test Suite (pytest)

Pytest runs all verification tests in `tests/`, asserting smoke test convergence, deterministic random seeding across repeated runs, and environment report schema integrity.

### Execution Command:
```powershell
pytest
```

### Verbose Mode:
```powershell
pytest -v -s
```

---

## 6. Google Colab CUDA Verification Guide

When utilizing free cloud notebooks (Google Colab) for future training sessions, GPU availability must never be assumed. Free instances often allocate CPU runtimes by default or have GPU quota limits.

### Step 6.1: How to Enable GPU in Google Colab
1. Open your Colab notebook (`.ipynb`).
2. Navigate to top menu: **Runtime** -> **Change runtime type**.
3. Under **Hardware accelerator**, select **T4 GPU** (or any available GPU accelerator).
4. Under **GPU type**, keep the default (Standard).
5. Click **Save**.

### Step 6.2: Safe CUDA Verification Script for Colab
Paste and execute the following cell at the top of your Colab notebook:

```python
import sys
import torch

print("=" * 60)
print("GOOGLE COLAB ACCELERATOR CHECK")
print("=" * 60)
print(f"Python version : {sys.version.split()[0]}")
print(f"PyTorch version: {torch.__version__}")

cuda_available = torch.cuda.is_available()
print(f"CUDA Available : {cuda_available}")

if cuda_available:
    num_devices = torch.cuda.device_count()
    device_name = torch.cuda.get_device_name(0)
    capability = torch.cuda.get_device_capability(0)
    memory_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
    
    print(f"GPU Device Count: {num_devices}")
    print(f"Primary GPU     : {device_name}")
    print(f"Compute Cap.    : {capability[0]}.{capability[1]}")
    print(f"Total VRAM      : {memory_gb:.2f} GiB")
    print("\nStatus: GPU is ready for training.")
else:
    print("\nWARNING: No GPU detected. The notebook is running on CPU.")
    print("Action Required: Go to 'Runtime' -> 'Change runtime type' and select 'T4 GPU'.")
print("=" * 60)
```

### Step 6.3: Fallback Strategy if GPU is Unavailable
If Colab denies GPU allocation due to usage limits:
1. Switch notebook runtime to standard CPU for data exploration, tokenization preprocessing, or test runs.
2. Schedule training runs during lower-demand periods or utilize Kaggle Notebooks (offers 30 hours/week of free T4/P100 GPUs) as an alternative zero-cost cloud GPU provider.
