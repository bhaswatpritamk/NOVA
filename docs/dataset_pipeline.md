# Nova-Fit: Dataset Preparation Pipeline (Phase 3)

## 1. Overview and Design Objectives

Phase 3 establishes a reproducible, auditable, and deterministic dataset preparation pipeline for Project Nova-Fit. Before pretraining begins, raw fitness domain text must be cleaned, validated, tokenized, packed into fixed-length sequences, partitioned into train/validation sets, and recorded with cryptographic provenance.

### Core Objectives

1. **Fitness Domain Focus**: Ingest and structure textual data across strength training, exercise biomechanics, nutrition fundamentals, recovery/sleep, and workout programming.
2. **Deterministic & Auditable**: Every dataset preparation run computes SHA-256 hashes of input corpora, tracks document and token statistics, and produces a tamper-evident `manifest.json`.
3. **Optimized Sequence Packing**: Concatenate tokenized documents separated by end-of-sequence (`<|endoftext|>`) tokens into uniform fixed-length context windows (default: 512 tokens), avoiding padding waste while maintaining cross-document attention boundaries.
4. **PyTorch Integration**: Provide native `torch.utils.data.Dataset` and DataLoader compatibility, returning standard `(input_ids, labels)` pairs where `labels` is shifted for next-token prediction and `<|pad|>` tokens are masked with `-100`.
5. **Zero External Data Leakage**: Pipeline operates completely offline on local or mounted storage with no telemetry or non-reproducible external calls.

---

## 2. Pipeline Architecture

```
Raw Text Corpora (data/raw/*.txt)
        │
        ▼
Corpus Validation & Loading (path existence, UTF-8 reading, SHA-256 computation)
        │
        ▼
Document Extraction & Cleaning
  ├── Strip comments (# ...)
  ├── Section header parsing ([SECTION: ...])
  ├── Whitespace normalization & line trimming
  └── Minimum document length filtering
        │
        ▼
Document Tokenization (NovaTokenizer Byte-Level BPE)
  ├── Token ID mapping
  └── EOS token appending (<|endoftext|>)
        │
        ▼
Sequence Packing (max_seq_len = 512)
  ├── Continuous token stream aggregation
  ├── Chunking into exact max_seq_len blocks
  └── Padding / dropping of terminal chunk
        │
        ▼
Deterministic Train / Val Split
  ├── Configurable validation ratio (default: 0.05)
  └── Seeded random permutation (default seed: 42)
        │
        ▼
Artifact Serialization & Provenance Manifest
  ├── data/prepared/train.pt (torch.LongTensor)
  ├── data/prepared/val.pt (torch.LongTensor)
  └── data/prepared/manifest.json (provenance metadata)
```

---

## 3. Data Cleansing Specification

The cleaning pipeline is controlled via `CleaningConfig`:

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `strip_comment_lines` | `bool` | `True` | Remove lines starting with `#` (metadata / comments). |
| `strip_section_headers` | `bool` | `False` | Strip section boundary tags (e.g., `[SECTION: ...]`). Default retains them for structural context. |
| `normalize_whitespace` | `bool` | `True` | Collapse internal consecutive spaces/tabs to a single space. |
| `strip_leading_trailing` | `bool` | `True` | Strip leading and trailing whitespace per line. |
| `min_doc_chars` | `int` | `20` | Discard documents with fewer characters than this threshold. |
| `lowercase` | `bool` | `False` | Convert text to lowercase (retained as False to preserve capitalization). |

---

## 4. Sequence Packing & Training Representation

### Token Packing
Rather than padding individual documents to `max_seq_len` (which wastes up to 80% of compute on short documents), Nova-Fit packs documents end-to-end:
```
[Doc 1 tokens] <|endoftext|> [Doc 2 tokens] <|endoftext|> [Doc 3 tokens ...]
|-------------------------- 512 tokens --------------------------|
```

If the remaining tokens at the end of the corpus do not fill a full `max_seq_len` sequence:
- By default (`drop_last_short=False`), the terminal sequence is padded with `<|pad|>` tokens (ID `0`).
- If `drop_last_short=True`, the incomplete sequence is discarded.

### Training Item Format
The `NovaPretrainingDataset` yields dictionaries matching PyTorch language modeling standards:
- `input_ids`: `torch.LongTensor` of shape `(seq_len - 1,)` (tokens $t_0, t_1, \dots, t_{L-2}$)
- `labels`: `torch.LongTensor` of shape `(seq_len - 1,)` (target tokens $t_1, t_2, \dots, t_{L-1}$)
- `attention_mask`: `torch.LongTensor` of shape `(seq_len - 1,)` (`1` for real tokens, `0` for `<|pad|>`)

Any label corresponding to a `<|pad|>` token has its label set to `-100`, which is ignored by `torch.nn.functional.cross_entropy`.

---

## 5. Provenance Manifest Schema

Every prepared dataset output includes `manifest.json`:

```json
{
  "name": "nova-fit-pretraining",
  "version": "0.1.0",
  "created_at": "2026-10-14T09:24:48.598219+00:00",
  "corpus_stats": {
    "total_files": 1,
    "total_documents": 7,
    "total_characters": 8248,
    "total_words": 1118,
    "total_lines": 59,
    "avg_document_chars": 1178.29,
    "avg_document_words": 159.71,
    "min_document_chars": 974,
    "max_document_chars": 1363,
    "empty_documents_dropped": 0,
    "short_documents_dropped": 0
  },
  "tokenized_stats": {
    "total_tokens": 1495,
    "total_sequences": 7,
    "avg_tokens_per_document": 213.57,
    "max_tokens_per_document": 268,
    "min_tokens_per_document": 160,
    "vocab_size": 2274,
    "max_seq_len": 512,
    "eos_token_id": 3,
    "pad_token_id": 0
  },
  "source_files": [
    {
      "path": "E:\\NOVA\\data\\raw\\fitness_smoke_corpus.txt",
      "size_bytes": "8800",
      "sha256": "b90548dcb22d2bd5552d8577c472858c274d6c014a8a82af14acc1447c147e6d"
    }
  ],
  "cleaning_config": {
    "strip_comment_lines": true,
    "strip_section_headers": false,
    "normalize_whitespace": true,
    "strip_leading_trailing": true,
    "min_doc_chars": 20,
    "lowercase": false
  },
  "split_config": {
    "val_ratio": 0.05,
    "split_seed": 42,
    "drop_last_short": false
  },
  "train_sequences": 2,
  "val_sequences": 1,
  "total_tokens_train": 983,
  "total_tokens_val": 512,
  "tokenizer_vocab_size": 2274,
  "max_seq_len": 512,
  "python_version": "3.14.8",
  "numpy_version": "2.5.4",
  "torch_version": "2.14.1+cpu"
}
```

---

## 6. CLI Usage & Verification

### Running the Dataset Preparation CLI
```powershell
python scripts/prepare_dataset.py \
  --corpus data/raw/fitness_smoke_corpus.txt \
  --tokenizer artifacts/tokenizer \
  --output-dir data/prepared \
  --max-seq-len 512 \
  --val-ratio 0.05 \
  --split-seed 42
```

### Loading in Python
```python
from nova.data import load_prepared_dataset

train_ds, val_ds, manifest = load_prepared_dataset("data/prepared")
print(f"Train sequences: {len(train_ds)}, Val sequences: {len(val_ds)}")
print(f"First item input_ids shape: {train_ds[0]['input_ids'].shape}")
```

### Running Test Suite
```powershell
pytest tests/test_data.py -v
```
All 64 unit and integration tests verify cleaning, extraction, tokenization, sequence packing, splitting, serialization, dataset loading, and DataLoader batch generation.
