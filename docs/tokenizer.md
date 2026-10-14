# Nova-Fit Tokenizer Engineering Specification (Phase 1)

This document provides the complete architecture, interface documentation, configuration, reproduction instructions, and mobile/edge deployment analysis for the **Nova-Fit Byte-Level BPE Tokenizer**.

---

## 1. Architectural Overview & Design Principles

The Nova-Fit language model is an original decoder-only Transformer (~20M parameters) trained from randomly initialized weights on exercise science, physiology, strength training, and nutrition domain text.

Tokenizer design requirements for Phase 1:
- **Trained From Scratch**: No pretrained tokenizers (such as GPT-2, LLaMA, or Mistral) are loaded, imported, or fine-tuned.
- **Algorithm**: Byte-Level Byte Pair Encoding (BPE) powered by the Hugging Face `tokenizers` library (Rust backend).
- **Provisional Production Vocabulary Target**: 8,000 tokens.
- **Byte-Level Coverage**: Initialized with all 256 individual byte values (`pre_tokenizers.ByteLevel.alphabet()`). This guarantees that the tokenizer can encode and decode any arbitrary sequence of UTF-8 text (including emojis, accents, technical symbols, and malformed sequences) without out-of-vocabulary (`<unk>`) errors.
- **Explicit Special-Token Handling**: Configured with a security-first default (`allow_special=False`) ensuring ordinary input text containing literal strings like `<pad>` or `<eos>` is never accidentally parsed into control tokens.
- **Portability & Provenance**: Serialized into standard Hugging Face `tokenizer.json` accompanied by a comprehensive `tokenizer_metadata.json` capturing SHA-256 digests, parameter configurations, timestamps, and dependency versions.

---

## 2. Tokenizer Interface & API Reference

The primary class is `NovaTokenizer`, located in `src/nova/tokenizer.py`.

### 2.1 Class: `NovaTokenizer`

```python
from nova.tokenizer import NovaTokenizer

# Training from a text corpus file
tokenizer = NovaTokenizer.train_from_corpus(
    corpus_path="data/raw/fitness_smoke_corpus.txt",
    vocab_size=8000,
    min_frequency=1,
)

# Encoding ordinary text
token_ids = tokenizer.encode("Squat 3x5 @ 100kg! Rest 180s. 🏋️‍♂️")

# Decoding back to text
text = tokenizer.decode(token_ids)

# Saving artifacts to disk
tokenizer.save("artifacts/tokenizer")

# Reloading from disk
reloaded = NovaTokenizer.from_file("artifacts/tokenizer")
```

### 2.2 Core Methods & Signatures

| Method / Property | Signature | Description |
| :--- | :--- | :--- |
| `train_from_corpus` | `(corpus_path, vocab_size=8000, min_frequency=1, special_tokens=None, ...) -> NovaTokenizer` | Trains a fresh Byte-Level BPE tokenizer from scratch from a text file or list of files. |
| `encode` | `(text: str, allow_special: Union[bool, Collection[str]] = False) -> List[int]` | Encodes a string into a list of integer token IDs. Validates input type and handles special tokens explicitly. |
| `encode_batch` | `(texts: List[str], allow_special: Union[bool, Collection[str]] = False) -> List[List[int]]` | Encodes a batch of strings. |
| `decode` | `(ids: Sequence[int], skip_special_tokens: bool = False) -> str` | Decodes a sequence of integer token IDs back into an exact string. Validates token types and range. |
| `decode_batch` | `(batch_ids: List[Sequence[int]], skip_special_tokens: bool = False) -> List[str]` | Decodes a batch of token ID sequences. |
| `save` | `(output_path: Union[str, Path], save_metadata: bool = True) -> Dict[str, Path]` | Serializes `tokenizer.json` and companion `tokenizer_metadata.json` to directory or file path. |
| `from_file` | `(path: Union[str, Path], special_tokens_map=None) -> NovaTokenizer` | Deserializes a saved tokenizer from a directory or JSON file. |
| `get_vocab` | `() -> Dict[str, int]` | Returns a dictionary mapping all token strings to integer IDs. |
| `vocab_size` | `property -> int` | Returns total vocabulary size (same as `len(tokenizer)`). |
| `token_to_id` | `(token: str) -> Optional[int]` | Returns token ID for given token string, or `None`. |
| `id_to_token` | `(token_id: int) -> Optional[str]` | Returns token string for given token ID, or `None`. |
| `pad_token_id` | `property -> int` | Dynamic property retrieving `<pad>` token ID. |
| `unk_token_id` | `property -> Optional[int]` | Dynamic property retrieving `<unk>` token ID. |
| `bos_token_id` | `property -> Optional[int]` | Dynamic property retrieving `<bos>` token ID. |
| `eos_token_id` | `property -> int` | Dynamic property retrieving `<eos>` token ID. |
| `get_special_token_id` | `(identifier: str) -> int` | Retrieves token ID by role name (`'pad_token'`, `'pad'`) or string (`'<pad>'`). |

### 2.3 Input Validation & Error Handling

`NovaTokenizer` enforces strict typing and defensive boundary checks:
- **Non-string input to `encode`**: Raises `TypeError` with explicit type diagnosis.
- **Empty string to `encode`**: Safely returns an empty list `[]`.
- **Non-sequence or non-integer elements in `decode`**: Raises `TypeError` (boolean values, strings, or floats are rejected).
- **Out-of-bounds IDs in `decode`**: Raises `ValueError` detailing the invalid ID, index, and valid vocabulary range `[0, vocab_size - 1]`.
- **Missing paths**: Loading or training against non-existent paths raises `FileNotFoundError`.
- **Invalid training parameters**: Non-positive `vocab_size` or non-positive `min_frequency` raises `ValueError`.

---

## 3. Special Token Specification & Explicit Handling

### 3.1 Configured Special Tokens

Nova-Fit establishes distinct, explicit special tokens required for decoder-only autoregressive training:

| Role | Token String | Purpose | Numeric Value Constraint |
| :--- | :--- | :--- | :--- |
| **Padding** | `<pad>` | Equalizes sequence lengths within batched tensors during training. | Distinct; retrieved dynamically via `tokenizer.pad_token_id`. |
| **Unknown** | `<unk>` | Fallback token for unresolvable inputs (rare in byte-level BPE). | Distinct; retrieved dynamically via `tokenizer.unk_token_id`. |
| **Beginning of Text** | `<bos>` | Signals the start of an independent training document or sequence. | Distinct; retrieved dynamically via `tokenizer.bos_token_id`. |
| **End of Text** | `<eos>` | Signals sequence termination for generation and document separation. | Distinct; retrieved dynamically via `tokenizer.eos_token_id`. |

> **Important**: Code and tests must never assume special tokens have hardcoded numerical values (such as `0` or `1`). Their IDs are looked up dynamically through the `NovaTokenizer` properties.

### 3.2 Explicit Special-Token Parsing Policy

In traditional NLP implementations, if input text contains literal text matching a special token (e.g., `"The configuration specifies <pad> here."`), naive tokenizers convert `<pad>` into the special token ID `0`. In generative LLMs, this creates a vulnerability:
1. **Prompt Injection / Premature Termination**: A user writing `<eos>` or `<|endoftext|>` in chat can terminate generation prematurely.
2. **Loss of Exact Round-Trip Fidelity**: Encoding `"Write <pad> in the notes"` and decoding would erase `<pad>` if special tokens are skipped.

**Nova-Fit Solution**:
- **`allow_special=False` (Default)**: Ordinary text is processed strictly as character subwords. The substring `"<pad>"` is broken down into its constituent byte tokens (`'<'`, `'p'`, `'a'`, `'d'`, `'>'`). The special token ID is **never** emitted. Round-trip decoding returns the exact literal string.
- **`allow_special=True`**: Enables explicit parsing of all configured special tokens into their reserved token IDs.
- **`allow_special=Collection[str]`**: Allows only a designated whitelist (e.g., `allow_special={"<eos>"}`). If an unpermitted special token appears in the text, `NovaTokenizer` raises `ValueError`.

---

## 4. Configuration Specification (`configs/tokenizer.json`)

Tokenizer hyperparameters are declared in `configs/tokenizer.json`:

```json
{
  "name": "nova-fit-tokenizer",
  "version": "0.1.0",
  "algorithm": "byte_level_bpe",
  "target_vocab_size": 8000,
  "min_frequency": 1,
  "special_tokens": [
    "<pad>",
    "<unk>",
    "<bos>",
    "<eos>"
  ],
  "special_tokens_map": {
    "pad_token": "<pad>",
    "unk_token": "<unk>",
    "bos_token": "<bos>",
    "eos_token": "<eos>"
  },
  "pre_tokenizer": {
    "type": "ByteLevel",
    "add_prefix_space": false,
    "trim_offsets": true
  },
  "decoder": {
    "type": "ByteLevel"
  },
  "model": {
    "type": "BPE",
    "unk_token": "<unk>"
  },
  "default_corpus_path": "data/raw/fitness_smoke_corpus.txt",
  "default_output_dir": "artifacts/tokenizer",
  "notes": "Nova-Fit Phase 1 Byte-Level BPE configuration. Production target is 8000 tokens."
}
```

---

## 5. Training Corpus & Small Fixture Limitations

### 5.1 The Smoke Corpus Fixture (`data/raw/fitness_smoke_corpus.txt`)

For development and automated CI/CD testing, Phase 1 provides an original, version-controlled fitness text fixture:
- **Location**: `data/raw/fitness_smoke_corpus.txt`
- **Notice**: This fixture contains original synthetic fitness material created specifically for tokenizer unit tests. It is **not** the production training corpus.
- **Topics Covered**:
  - Progressive overload, mechanical tension, and compound resistance movements.
  - Exercise technique and biomechanics (Squat, Bench Press, Deadlift, Overhead Press, Rows).
  - Programming variables: Sets, repetitions (3x5, 4x6, 12-15), RPE (7-9), RIR (1-3), rest intervals (60-300s).
  - Protein metabolism (1.6-2.2 g/kg/day, leucine threshold, mTORC1) and nutrition fundamentals.
  - Recovery dynamics, sleep architecture (slow-wave and REM), DOMS, and Heart Rate Variability (HRV).
  - Exercise physiology: Fiber phenotypes (Type I, IIa, IIx), bioenergetics (ATP-CP, glycolysis, oxidative), Henneman's size principle.
  - Workout planning, periodization models, and deload protocols.

### 5.2 Vocabulary Ceiling on Small Text Fixtures

When training BPE:
1. The vocabulary initializes with 256 byte tokens plus special tokens (~260 tokens).
2. The BPE algorithm greedily merges the most frequent adjacent token pairs.
3. Once all recurring adjacent token pairs in the training text have frequency `< min_frequency` (or no recurring pairs remain), **no additional merges can be extracted**.

Consequently:
- On `data/raw/fitness_smoke_corpus.txt` (~8.8 KB), the actual learned vocabulary size reaches **~2,274 tokens**.
- Requesting `target_vocab_size = 8000` does **not** fail with an error, but training stops naturally when merge pairs are exhausted.
- **Production Pre-Training Requirement**: To fill the target 8,000 vocabulary (or beyond), the production corpus must contain sufficient text diversity (typically 50 MB to 500 MB+ of varied fitness literature, research papers, and technical guides).

---

## 6. How to Train the Tokenizer on a Different Corpus

To train on a new or expanded fitness corpus:

### Option A: Command Line Interface (CLI)

```powershell
# Using default options (trains on smoke corpus, outputs to artifacts/tokenizer)
python scripts/train_tokenizer.py

# Training on a new custom corpus with custom target vocabulary size:
python scripts/train_tokenizer.py --corpus path/to/large_fitness_corpus.txt --vocab-size 8000 --output-dir artifacts/tokenizer_prod

# Training with custom min_frequency:
python scripts/train_tokenizer.py -c data/raw/production_corpus.txt -v 8000 -m 2 -o artifacts/tokenizer_v1
```

### Option B: Python API

```python
from pathlib import Path
from nova.tokenizer import NovaTokenizer

# Single file or list of files
corpus_files = ["data/raw/strength_guide.txt", "data/raw/nutrition_guide.txt"]

tokenizer = NovaTokenizer.train_from_corpus(
    corpus_path=corpus_files,
    vocab_size=8000,
    min_frequency=2,
)

# Save to target directory
tokenizer.save("artifacts/tokenizer_custom")
```

---

## 7. Artifacts & Reproducibility

When `tokenizer.save(output_dir)` is called, two files are created:

1. **`tokenizer.json`**:
   The standard, portable Hugging Face Tokenizer serialization format containing the BPE model vocabulary, merge table, pre-tokenizer configuration, decoder rules, and added special tokens.
2. **`tokenizer_metadata.json`**:
   A companion manifest documenting complete experimental provenance:
   ```json
   {
     "algorithm": "byte_level_bpe",
     "target_vocab_size": 8000,
     "actual_vocab_size": 2274,
     "special_tokens": {
       "pad_token": {"token": "<pad>", "id": 0},
       "unk_token": {"token": "<unk>", "id": 1},
       "bos_token": {"token": "<bos>", "id": 2},
       "eos_token": {"token": "<eos>", "id": 3}
     },
     "corpus_path": "data\\raw\\fitness_smoke_corpus.txt",
     "corpus_sha256": "b90548dcb22d2bd5552d8577c472858c274d6c014a8a82af14acc1447c147e6d",
     "dependency_version": "tokenizers==0.23.3",
     "python_version": "3.14.8",
     "training_config": {
       "vocab_size": 8000,
       "min_frequency": 1,
       "add_prefix_space": false,
       "trim_offsets": true,
       "special_tokens": ["<pad>", "<unk>", "<bos>", "<eos>"]
     },
     "created_at": "2026-10-14T08:51:08.228065+00:00"
   }
   ```

**Version Control Rules**:
- Large dataset files and model checkpoint weights are strictly ignored in `.gitignore`.
- `data/raw/fitness_smoke_corpus.txt` is an explicitly allowed, version-controlled fixture.
- Generated artifacts in `artifacts/tokenizer/` remain outside Git tracking.

---

## 8. Mobile & Edge Deployment Compatibility (GGUF / llama.cpp on Android)

The long-term roadmap for Project Nova-Fit includes lightweight edge deployment on mobile devices (Android) using `llama.cpp` and GGUF model formats.

> **Caution**: A tokenizer is **NOT** mobile- or Android-compatible merely because it can be saved to a JSON file.

### 8.1 GGUF Tokenizer Architecture Requirements

GGUF models store tokenizer data as metadata arrays directly inside the GGUF binary container rather than reading external JSON files. The GGML tokenizer expects:
- `tokenizer.ggml.model`: `"gpt2"` (for Byte-Level BPE) or `"llama"`.
- `tokenizer.ggml.tokens`: Array of UTF-8 token strings.
- `tokenizer.ggml.scores`: Array of float scores or merge priority ranks.
- `tokenizer.ggml.token_type`: Categorization (normal = 1, unknown = 2, control/special = 3, byte = 6).
- `tokenizer.ggml.bos_token_id`, `eos_token_id`, `padding_token_id`.

### 8.2 Crucial Verification Steps Prior to Android Deployment

1. **Pre-Tokenizer Regex Alignment**:
   In `llama.cpp`, pre-tokenization is implemented through hardcoded C++ regex patterns (e.g., `gpt-2`, `llama-3`, `smollm`, `deepseek-llm`). When converting via `convert_hf_to_gguf.py`, our tokenizer must declare a recognized `pre_tokenizer` regex pattern or match the GGML BPE pre-tokenization rules. Failure to align this causes divergence: a string tokenized into 4 tokens in Python might become 6 tokens on Android, degrading generation coherence.
2. **Byte Representation in Vocabulary**:
   Byte-Level BPE in Hugging Face maps raw bytes `0x00-0xFF` to visible Unicode characters (e.g., space is represented as `Ġ` / `\u0120`). In GGUF, byte tokens can be represented either as `<0xXX>` hex tokens or as UTF-8 string tokens. The conversion script must correctly map these byte tokens without creating duplicates or misaligned IDs.
3. **Hardware Acceleration Alignment (NEON / NPU)**:
   Mobile neural accelerators (ARM NEON, Hexagon NPU, Mali GPU) perform matrix multiplication on token embedding tables most efficiently when the vocabulary dimension is aligned to multiples of 32, 64, or 128.
   Our target vocabulary of **8,000** is cleanly divisible by 64 ($8000 / 64 = 125$), ensuring optimal memory alignment for mobile SIMD execution.
4. **Android Native Runtime Verification**:
   Before releasing an Android APK:
   - Convert `tokenizer.json` to GGUF using `convert_hf_to_gguf.py`.
   - Run tokenization round-trip tests using `llama-tokenize` binary built for Android NDK (ARM64).
   - Verify that token IDs generated by the Android binary match Python `NovaTokenizer.encode()` byte-for-byte across all fitness test cases.

---

## 9. Test Suite Verification Summary

The automated pytest suite in `tests/test_tokenizer.py` verifies all requirements:
1. Training from scratch on `data/raw/fitness_smoke_corpus.txt`.
2. Encoding nonempty text into valid token IDs.
3. Decoding back into text.
4. Exact round-trip preservation of numbers, symbols, spaces, tabs, and multiple newlines.
5. Unicode preservation across emojis, accented characters, Greek letters, and non-Latin scripts.
6. Empty input encoding (`[]`) and decoding (`""`).
7. Special token ID uniqueness and dynamic retrieval without hardcoded values.
8. Explicit special-token handling (`allow_special=False` protects ordinary text from being hijacked).
9. Vocabulary access and mapping consistency.
10. Saving and reloading from directory and file.
11. Identical token ID sequences before and after serialization.
12. Strict input validation and descriptive error reporting for invalid types and out-of-bounds IDs.
13. Deterministic repeatability when trained twice with identical configurations.
14. Compatibility with Phase 0 tests (`test_smoke.py`).
