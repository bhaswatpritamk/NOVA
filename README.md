# Nova-Fit: Fitness-Specialized Language Model

> **Project Objective**: Build an original, fitness-specialized language model trained from scratch (randomly initialized weights) dedicated to exercise science, strength training, nutrition fundamentals, recovery, physiology, biomechanics, and fitness education.

Target base model: Decoder-only Transformer (~20M parameters), optimized for lightweight local and edge deployment (including future Android mobile inference).

---

## Current Status: Phase 0 (Environment Setup & Foundation)

Phase 0 establishes a reproducible development and testing foundation:
- Clean modular repository structure.
- Virtual environment with verified dependencies.
- Hardware and environment diagnostic reporting.
- Deterministic CPU-only PyTorch smoke test.
- Automated pytest regression test suite.
- Zero-cost workflow preparation (Local CPU development + Free Cloud GPU for future training).

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
│       └── __init__.py      # Package entrypoint
├── scripts/
│   ├── environment_report.py # System, hardware, and PyTorch diagnostic report
│   └── smoke_test.py         # Deterministic CPU MLP training smoke test
├── tests/
│   ├── __init__.py
│   └── test_smoke.py        # Automated test suite (smoke test & env validation)
├── configs/                 # Model and training configuration files (.gitkeep)
├── data/                    # Datasets (ignored in git) (.gitkeep)
├── checkpoints/             # Model checkpoints (ignored in git) (.gitkeep)
├── artifacts/               # Experiment logs and metrics (ignored in git) (.gitkeep)
└── docs/
    └── environment_setup.md # In-depth setup, Colab GPU checks, and operations
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

### 6. Run Automated Tests
```powershell
pytest
```

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
