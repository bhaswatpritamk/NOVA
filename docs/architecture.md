# Nova-Fit Transformer Architecture Specification (Phase 2)

This document provides the architectural specification, mathematical formulation, configuration guidelines, and verification details for the **Nova-Fit Decoder-Only Transformer Language Model**.

---

## 1. Architectural Overview & Design Philosophy

Project Nova-Fit builds an original, domain-specialized language model dedicated to exercise science, biomechanics, strength training, and nutrition.

### Core Architectural Principles:
1. **Decoder-Only Autoregressive Transformer**: Predicts subsequent tokens conditioned strictly on preceding tokens ($p(w_t \mid w_{<t})$).
2. **Trained from Scratch**: Randomly initialized weights without loading, adapting, or distilling from external pretrained checkpoints.
3. **Modern LLM Standards**: Incorporates Rotary Position Embeddings (RoPE), Root Mean Square Layer Normalization (RMSNorm), and SwiGLU gated activations, matching state-of-the-art architectures (e.g., LLaMA, Mistral).
4. **Pre-Norm Formulation**: Applies normalization before attention and feed-forward sublayers with residual connections, ensuring gradient stability across deep networks.
5. **Strict Causality**: Lower-triangular attention masking guarantees that future tokens can never influence past or current representations.

```
Input Token IDs [B, T]
       │
       ▼
Token Embeddings (vocab_size -> d_model)
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ Transformer Block (repeated n_layers times)           │
│                                                        │
│   ┌────────────────────────────────────────────────┐   │
│   │ Input x                                        │   │
│   │   ├──> RMSNorm -> Causal Attention (with RoPE) │   │
│   │   └──> (Add residual) ─────────────────────────┼─> h
│   │                                                │   │
│   │ Intermediate h                                 │   │
│   │   ├──> RMSNorm -> SwiGLU FFN                  │   │
│   │   └──> (Add residual) ─────────────────────────┼─> out
│   └────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────┘
       │
       ▼
Final RMSNorm (d_model)
       │
       ▼
LM Head Linear (d_model -> vocab_size)
       │
       ▼
Logits [B, T, vocab_size] ──> Autoregressive Cross-Entropy Loss
```

---

## 2. Mathematical Formulation of Layers

### 2.1 Token Embeddings
Given an input sequence of integer token IDs $\mathbf{x} = [x_1, x_2, \dots, x_T]$ where $x_t \in \{0, \dots, V-1\}$ and $V$ is vocabulary size:
$$\mathbf{E} = \text{Embedding}(\mathbf{x}) \in \mathbb{R}^{B \times T \times d_{model}}$$
Weights are initialized from $\mathcal{N}(0, 0.02^2)$.

### 2.2 Root Mean Square Layer Normalization (RMSNorm)
RMSNorm regularizes the inputs across the hidden dimension without calculating or subtracting the mean, reducing computational overhead while maintaining numerical stability:
$$\text{RMS}(\mathbf{x}) = \sqrt{\frac{1}{d} \sum_{i=1}^d x_i^2 + \epsilon}$$
$$\text{RMSNorm}(\mathbf{x}) = \frac{\mathbf{x}}{\text{RMS}(\mathbf{x})} \odot \boldsymbol{\gamma}$$
where $\boldsymbol{\gamma} \in \mathbb{R}^d$ is a learnable scaling parameter initialized to $\mathbf{1}$, and $\epsilon = 10^{-5}$. No additive bias is used.

### 2.3 Rotary Position Embeddings (RoPE)
RoPE encodes positional information by rotating query and key representations in 2D subplanes:
For each head dimension index $i \in \{0, 1, \dots, d_{head}/2 - 1\}$:
$$\theta_i = \text{base}^{-2i / d_{head}} \quad (\text{with } \text{base} = 10000.0)$$
For position $t \in \{0, \dots, T-1\}$, the rotation applied to a vector $\mathbf{v} \in \mathbb{R}^{d_{head}}$ split into halves $(\mathbf{v}_1, \mathbf{v}_2)$ is:
$$\mathbf{v}_{\text{rot}} = (\mathbf{v} \odot \cos(t \boldsymbol{\theta})) + (\text{rotate\_half}(\mathbf{v}) \odot \sin(t \boldsymbol{\theta}))$$
where $\text{rotate\_half}([\mathbf{v}_1, \mathbf{v}_2]) = [-\mathbf{v}_2, \mathbf{v}_1]$.

RoPE ensures that the dot product between queries and keys satisfies:
$$\langle \mathbf{q}_m, \mathbf{k}_n \rangle = g(\mathbf{q}, \mathbf{k}, m - n)$$
meaning attention scores depend strictly on relative token distances.

### 2.4 Causal Multi-Head Self-Attention
1. **Linear Projections**:
   $$\mathbf{Q} = \mathbf{x} \mathbf{W}_q, \quad \mathbf{K} = \mathbf{x} \mathbf{W}_k, \quad \mathbf{V} = \mathbf{x} \mathbf{W}_v \quad (\mathbf{W}_{q,k,v} \in \mathbb{R}^{d_{model} \times d_{model}})$$
2. **Head Reshaping**:
   Each projection is reshaped to $[B, n_{heads}, T, d_{head}]$ where $d_{head} = d_{model} / n_{heads}$.
3. **RoPE Modulation**:
   $\mathbf{Q} \leftarrow \text{RoPE}(\mathbf{Q}), \quad \mathbf{K} \leftarrow \text{RoPE}(\mathbf{K})$.
4. **Causal Masked Scaled Dot-Product**:
   $$\mathbf{S} = \frac{\mathbf{Q} \mathbf{K}^T}{\sqrt{d_{head}}}$$
   $$\mathbf{M}_{i,j} = \begin{cases} 0 & \text{if } j \le i \\ -\infty & \text{if } j > i \end{cases}$$
   $$\mathbf{A} = \text{Softmax}(\mathbf{S} + \mathbf{M}, \text{dim}=-1)$$
   $$\mathbf{O} = (\mathbf{A} \mathbf{V}) \mathbf{W}_o \quad (\mathbf{W}_o \in \mathbb{R}^{d_{model} \times d_{model}})$$

### 2.5 SwiGLU Feed-Forward Network
SwiGLU replaces standard ReLU/GELU multilayer perceptrons with a gated activation:
$$\text{SwiGLU}(\mathbf{x}) = \left( \text{SiLU}(\mathbf{x} \mathbf{W}_{\text{gate}}) \odot (\mathbf{x} \mathbf{W}_{\text{up}}) \right) \mathbf{W}_{\text{down}}$$
where $\text{SiLU}(z) = z \cdot \sigma(z)$, and:
- $\mathbf{W}_{\text{gate}} \in \mathbb{R}^{d_{model} \times d_{ff}}$
- $\mathbf{W}_{\text{up}} \in \mathbb{R}^{d_{model} \times d_{ff}}$
- $\mathbf{W}_{\text{down}} \in \mathbb{R}^{d_{ff} \times d_{model}}$
The intermediate dimension is computed as $d_{ff} \approx \lfloor \frac{8}{3} d_{model} \rfloor$ rounded to an appropriate multiple.

### 2.6 Next-Token Prediction & Loss
During autoregressive training, targets are shifted by 1 token position:
$$\mathbf{Logits}_{\text{shift}} = \mathbf{Logits}[:, :T-1, :]$$
$$\mathbf{Targets}_{\text{shift}} = \mathbf{Targets}[:, 1:T]$$
$$\mathcal{L} = -\frac{1}{N} \sum_{i=1}^N \log \left( \frac{\exp(\mathbf{Logits}_{i, \mathbf{Targets}_i})}{\sum_{j=1}^V \exp(\mathbf{Logits}_{i, j})} \right)$$
Padding tokens ($\text{pad\_token\_id} = 0$) are masked using `ignore_index` to prevent unpadded loss distortion.

---

## 3. Tiny Test Configuration & Parameter Breakdown

The smoke test configuration (`configs/tiny_model.json`) is tailored for CPU execution and automated verification:

| Hyperparameter | Value | Description |
| :--- | :--- | :--- |
| `vocab_size` | 2,274 | Derived from Phase 1 fitness smoke tokenizer |
| `max_seq_len` | 32 | Context window for smoke test |
| `d_model` | 64 | Hidden embedding dimension |
| `n_layers` | 2 | Number of Transformer decoder layers |
| `n_heads` | 4 | Attention heads ($d_{head} = 64/4 = 16$) |
| `d_ff` | 176 | SwiGLU intermediate dimension ($\approx \frac{8}{3} \times 64$) |
| `dropout` | 0.0 | Deterministic evaluation |
| `norm_eps` | $10^{-5}$ | RMSNorm epsilon |
| `rope_theta` | 10,000.0 | RoPE base frequency |
| `tie_word_embeddings` | false | Independent LM head projection |

### Exact Parameter Count Calculation

$$\text{Embeddings} = V \times d_{model} = 2274 \times 64 = 145,536$$
$$\text{LM Head} = d_{model} \times V = 64 \times 2274 = 145,536$$
$$\text{Final Norm} = d_{model} = 64$$

**Per Layer Breakdown ($n_{layers} = 2$):**
- $\text{Norm}_1$: $64$
- $\mathbf{W}_q$: $64 \times 64 = 4,096$
- $\mathbf{W}_k$: $64 \times 64 = 4,096$
- $\mathbf{W}_v$: $64 \times 64 = 4,096$
- $\mathbf{W}_o$: $64 \times 64 = 4,096$
- $\text{Norm}_2$: $64$
- $\mathbf{W}_{\text{gate}}$: $64 \times 176 = 11,264$
- $\mathbf{W}_{\text{up}}$: $64 \times 176 = 11,264$
- $\mathbf{W}_{\text{down}}$: $176 \times 64 = 11,264$
- **Total per layer**: $50,240$ parameters

$$\text{Total Parameters} = 145,536 + (2 \times 50,240) + 64 + 145,536 = \mathbf{391,744}$$

All 391,744 parameters are trainable.

---

## 4. Architectural Scaling: From Tiny to Nova-20M

Phase 2 establishes architectural correctness on CPU using the tiny model. The future production architecture will scale as follows:

| Parameter | Tiny Smoke Model (Phase 2) | Target Nova-20M (Future Phase) |
| :--- | :--- | :--- |
| **Parameters** | 391,744 (~392K) | ~20,000,000 (~20M) |
| **Vocab Size** | 2,274 (smoke fixture) | 8,000 (full production corpus) |
| **Context Length** | 32 tokens | 512 - 1,024 tokens |
| **Hidden Dim ($d_{model}$)** | 64 | 288 |
| **Layers ($n_{layers}$)** | 2 | 12 |
| **Attention Heads** | 4 ($d_{head}=16$) | 6 ($d_{head}=48$) |
| **SwiGLU Dim ($d_{ff}$)** | 176 | 768 |
| **Compute Target** | Local CPU | Google Colab Free T4 GPU |
| **Hardware Alignment** | $d_{head} \pmod 2 = 0$ | $V \pmod {64} = 0$, SIMD-optimized |

---

## 5. Verification & Testing Instructions

### 5.1 Run Model Smoke Test Script
```powershell
python scripts/model_smoke_test.py
```
Validates initialization, parameter calculation, forward logits shape `[2, 16, 2274]`, causal attention non-leakage, backpropagation, and loss reduction (>80%).

### 5.2 Run Full Test Suite
```powershell
python -m pytest -v
```
Executes all 48 automated tests:
- 17 Phase 2 Transformer unit tests (`tests/test_model.py`)
- 27 Phase 1 tokenizer unit tests (`tests/test_tokenizer.py`)
- 4 Phase 0 environment/smoke tests (`tests/test_smoke.py`)
