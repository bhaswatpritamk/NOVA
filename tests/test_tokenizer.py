"""Tests for Nova-Fit Phase 1 Byte-Level BPE Tokenizer.

Verifies:
1. Training a new tokenizer from scratch on a text corpus fixture.
2. Encoding nonempty text into valid token IDs.
3. Decoding token IDs back into text.
4. Exact round-trip preservation of ordinary text (punctuation, spaces, digits, newlines).
5. Robust handling of diverse Unicode text (emojis, accents, scientific symbols).
6. Empty input handling for encode and decode.
7. Special-token ID uniqueness across all configured special tokens.
8. Explicit special-token handling (ordinary text matching reserved strings is not hijacked).
9. Vocabulary access and consistency (get_vocab, vocab_size, token_to_id, id_to_token).
10. Saving and reloading the tokenizer and metadata.
11. Identical encoding and decoding before and after reloading.
12. Strict input validation and useful error reporting for invalid types/bounds/missing files.
13. Deterministic repeatability when training twice with identical configurations.
14. Module-level convenience functions.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

import pytest

from nova.tokenizer import (
    DEFAULT_SPECIAL_TOKENS,
    DEFAULT_SPECIAL_TOKENS_MAP,
    NovaTokenizer,
    compute_file_sha256,
    decode,
    encode,
    load_tokenizer,
    train_tokenizer,
)


@pytest.fixture(scope="session")
def corpus_path() -> Path:
    """Provide path to version-controlled fitness smoke corpus fixture."""
    p = Path("data/raw/fitness_smoke_corpus.txt")
    assert p.is_file(), f"Fixture corpus file missing: {p}"
    return p


@pytest.fixture(scope="session")
def trained_tokenizer(corpus_path: Path) -> NovaTokenizer:
    """Train and cache a NovaTokenizer instance for the test session."""
    return NovaTokenizer.train_from_corpus(
        corpus_path=corpus_path,
        vocab_size=8000,
        min_frequency=1,
    )


# -----------------------------------------------------------------------------
# 1. Training Tests
# -----------------------------------------------------------------------------


def test_train_tokenizer_on_fixture(corpus_path: Path, trained_tokenizer: NovaTokenizer):
    """Verify that training from scratch on the smoke fixture succeeds with valid metadata."""
    tok = trained_tokenizer
    assert isinstance(tok, NovaTokenizer)

    # Initial byte alphabet (256) + 4 special tokens = at least 260 tokens
    assert tok.vocab_size > 260
    assert len(tok) == tok.vocab_size

    # Verify provenance metadata
    meta = tok.metadata
    assert meta["algorithm"] == "byte_level_bpe"
    assert meta["target_vocab_size"] == 8000
    assert meta["actual_vocab_size"] == tok.vocab_size
    assert meta["corpus_sha256"] == compute_file_sha256(corpus_path)
    assert "tokenizers==" in meta["dependency_version"]
    assert "special_tokens" in meta
    assert meta["training_config"]["min_frequency"] == 1


# -----------------------------------------------------------------------------
# 2. Encoding & Decoding Basic Tests
# -----------------------------------------------------------------------------


def test_encode_nonempty_text(trained_tokenizer: NovaTokenizer):
    """Verify encoding returns a non-empty sequence of positive integers."""
    sample = "Barbell back squat with 3 sets of 5 repetitions."
    ids = trained_tokenizer.encode(sample)

    assert isinstance(ids, list)
    assert len(ids) > 0
    assert all(isinstance(i, int) for i in ids)
    assert all(0 <= i < trained_tokenizer.vocab_size for i in ids)


def test_decode_encoded_text(trained_tokenizer: NovaTokenizer):
    """Verify decoding recovers the original string."""
    sample = "Deadlift 1x5 @ 85% 1RM. Maintain neutral spinal alignment."
    ids = trained_tokenizer.encode(sample)
    recovered = trained_tokenizer.decode(ids)

    assert recovered == sample


# -----------------------------------------------------------------------------
# 3. Round-Trip Preservation
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        "Simple strength training sentence.",
        "Numbers and units: 100kg, 225lbs, 3x5, 1.6-2.2 g/kg/day, 90-180s.",
        "Punctuation check: !@#$%^&*()-_=+[]{};:'\",.<>/?\\|`~",
        "Multiple   spaces   between   words   and   trailing   ",
        "Tab\tseparated\tvalues\tand\twhitespace",
        "Single newline\nSeparated line\nAnother line",
        "Multiple consecutive newlines:\n\n\n\nPreserved exactly?\n\nYes.",
        "Mixed: Squat 4x6 @ 80% 1RM; Bench 3x8 @ 72.5%.\nRest 180s between sets! (RPE 8.5)",
    ],
)
def test_roundtrip_preservation_ordinary_text(trained_tokenizer: NovaTokenizer, text: str):
    """Verify exact round-trip preservation of numbers, symbols, spaces, and newlines."""
    ids = trained_tokenizer.encode(text)
    reconstructed = trained_tokenizer.decode(ids)
    assert reconstructed == text, (
        f"Round-trip failed.\nExpected: {text!r}\nGot:      {reconstructed!r}"
    )


# -----------------------------------------------------------------------------
# 4. Unicode Handling
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "unicode_text",
    [
        "Fitness emojis: 🏋️‍♂️ 💪 🏃‍♀️ 🥗 🔥 🥇",
        "European accents: café, résumé, Über, naïve, Señor, façade",
        "German umlauts and eszett: ä, ö, ü, Ä, Ö, Ü, ß",
        "Scientific units and symbols: VO₂max, kg/m², 37°C, ΔHRV, ±5%, µg/dL, α-amino acids",
        "Greek letters: α, β, γ, δ, ε, λ, π, ω (mTORC1, ATP-CP)",
        "East Asian characters: 力量训练 (strength training) 筋力トレーニング (hypertrophy)",
        "Multi-byte mixed: 🏋️ Bench Press 100kg: café break afterwards! 100% #gains",
    ],
)
def test_handling_unicode_text(trained_tokenizer: NovaTokenizer, unicode_text: str):
    """Verify byte-level BPE flawlessly preserves all arbitrary UTF-8 unicode sequences."""
    ids = trained_tokenizer.encode(unicode_text)
    reconstructed = trained_tokenizer.decode(ids)
    assert reconstructed == unicode_text, (
        f"Unicode round-trip failed.\nExpected: {unicode_text!r}\nGot:      {reconstructed!r}"
    )


# -----------------------------------------------------------------------------
# 5. Empty Input Handling
# -----------------------------------------------------------------------------


def test_empty_input(trained_tokenizer: NovaTokenizer):
    """Verify handling of empty strings and empty sequences."""
    assert trained_tokenizer.encode("") == []
    assert trained_tokenizer.decode([]) == ""
    assert trained_tokenizer.decode(()) == ""
    assert trained_tokenizer.decode(trained_tokenizer.encode("")) == ""


# -----------------------------------------------------------------------------
# 6. Special Tokens Uniqueness & Allocation
# -----------------------------------------------------------------------------


def test_special_token_id_uniqueness(trained_tokenizer: NovaTokenizer):
    """Verify that all configured special tokens have distinct, valid IDs."""
    tok = trained_tokenizer

    pad_id = tok.pad_token_id
    unk_id = tok.unk_token_id
    eos_id = tok.eos_token_id
    bos_id = tok.bos_token_id

    # Ensure none are None
    assert pad_id is not None
    assert unk_id is not None
    assert eos_id is not None
    assert bos_id is not None

    # Ensure all are valid non-negative integers
    special_ids = [pad_id, unk_id, eos_id, bos_id]
    for tid in special_ids:
        assert isinstance(tid, int)
        assert 0 <= tid < tok.vocab_size

    # Ensure uniqueness (do NOT assume specific numeric values)
    assert len(set(special_ids)) == len(special_ids), (
        f"Special token IDs must all be distinct: {special_ids}"
    )

    # Verify retrieval by role and content string
    assert tok.get_special_token_id("pad_token") == pad_id
    assert tok.get_special_token_id("pad") == pad_id
    assert tok.get_special_token_id("<pad>") == pad_id

    assert tok.get_special_token_id("eos_token") == eos_id
    assert tok.get_special_token_id("eos") == eos_id
    assert tok.get_special_token_id("<eos>") == eos_id


# -----------------------------------------------------------------------------
# 7. Explicit Special-Token Handling (Accidental Token Hijacking Prevention)
# -----------------------------------------------------------------------------


def test_special_token_handling_explicit(trained_tokenizer: NovaTokenizer):
    """Verify ordinary input text does not become a special token merely by spelling match."""
    tok = trained_tokenizer
    pad_id = tok.pad_token_id
    eos_id = tok.eos_token_id

    # Ordinary text mentioning special token spellings literally
    text = "The reserved tokens are <pad> and <eos> in our configuration."

    # 1. Default (allow_special=False): MUST NOT contain special token IDs
    ordinary_ids = tok.encode(text, allow_special=False)
    assert pad_id not in ordinary_ids, (
        f"pad_token_id ({pad_id}) was unexpectedly emitted in ordinary text: {ordinary_ids}"
    )
    assert eos_id not in ordinary_ids, (
        f"eos_token_id ({eos_id}) was unexpectedly emitted in ordinary text: {ordinary_ids}"
    )

    # Exact roundtrip of the ordinary text
    assert tok.decode(ordinary_ids) == text

    # 2. Explicit permission (allow_special=True): Special tokens are recognized
    special_ids = tok.encode(text, allow_special=True)
    assert pad_id in special_ids, (
        f"pad_token_id ({pad_id}) was expected when allow_special=True, but missing: {special_ids}"
    )
    assert eos_id in special_ids, (
        f"eos_token_id ({eos_id}) was expected when allow_special=True, but missing: {special_ids}"
    )

    # When decoded without skipping specials, text matches
    assert tok.decode(special_ids, skip_special_tokens=False) == text

    # 3. Restricted collection of allowed special tokens
    # Allowing only <pad>: text containing <eos> must raise ValueError
    with pytest.raises(ValueError, match="Encountered disallowed special token '<eos>'"):
        tok.encode(text, allow_special={"<pad>"})

    # When only allowed specials are present, succeeds
    text_pad_only = "Insert <pad> padding here."
    pad_only_ids = tok.encode(text_pad_only, allow_special={"<pad>"})
    assert pad_id in pad_only_ids


# -----------------------------------------------------------------------------
# 8. Vocabulary Access
# -----------------------------------------------------------------------------


def test_vocabulary_access(trained_tokenizer: NovaTokenizer):
    """Verify vocabulary dictionary access, length, and token mapping."""
    tok = trained_tokenizer
    vocab = tok.get_vocab()

    assert isinstance(vocab, dict)
    assert len(vocab) == tok.vocab_size
    assert len(vocab) == len(tok)

    # Check all configured special tokens are in vocabulary
    for tok_str in tok.special_tokens_map.values():
        assert tok_str in vocab
        assert vocab[tok_str] == tok.token_to_id(tok_str)

    # Verify token_to_id and id_to_token consistency
    for token_id in range(min(50, tok.vocab_size)):
        token_str = tok.id_to_token(token_id)
        assert token_str is not None
        assert tok.token_to_id(token_str) == token_id


# -----------------------------------------------------------------------------
# 9. Serialization and Reloading
# -----------------------------------------------------------------------------


def test_saving_and_reloading_tokenizer(trained_tokenizer: NovaTokenizer, tmp_path: Path):
    """Verify that saving to disk and reloading creates an identical functional tokenizer."""
    tok = trained_tokenizer
    save_dir = tmp_path / "saved_tokenizer"

    saved_files = tok.save(save_dir)
    assert "tokenizer" in saved_files
    assert saved_files["tokenizer"].is_file()
    assert "metadata" in saved_files
    assert saved_files["metadata"].is_file()

    # Load from directory
    reloaded_from_dir = NovaTokenizer.from_file(save_dir)
    assert reloaded_from_dir.vocab_size == tok.vocab_size
    assert reloaded_from_dir.pad_token_id == tok.pad_token_id
    assert reloaded_from_dir.eos_token_id == tok.eos_token_id
    assert reloaded_from_dir.unk_token_id == tok.unk_token_id
    assert reloaded_from_dir.bos_token_id == tok.bos_token_id

    # Load from explicit file path
    reloaded_from_file = NovaTokenizer.from_file(saved_files["tokenizer"])
    assert reloaded_from_file.vocab_size == tok.vocab_size
    assert reloaded_from_file.pad_token_id == tok.pad_token_id


def test_identical_encoding_before_and_after_reloading(
    trained_tokenizer: NovaTokenizer, tmp_path: Path
):
    """Verify that encodings and decodings are strictly identical before and after reloading."""
    tok = trained_tokenizer
    save_dir = tmp_path / "reload_test"
    tok.save(save_dir)

    reloaded = NovaTokenizer.from_file(save_dir)

    test_samples = [
        "Hypertrophy stimulus requires mechanical tension and metabolic stress.",
        "Squat: 4 sets x 8 reps with 120s rest. 🏋️‍♂️",
        "Protein intake: 2.0g/kg bodyweight daily across 4 meals.",
        "Punctuation and symbols: 100% #fitness-plan (RPE 8.0 @ 100kg)!",
        "Special token literal: This <pad> should not become id 0 by default.",
    ]

    for sample in test_samples:
        orig_ids = tok.encode(sample, allow_special=False)
        reloaded_ids = reloaded.encode(sample, allow_special=False)
        assert orig_ids == reloaded_ids, f"Encoding diverged after reloading for {sample!r}"

        orig_decoded = tok.decode(orig_ids)
        reloaded_decoded = reloaded.decode(reloaded_ids)
        assert orig_decoded == reloaded_decoded
        assert orig_decoded == sample


# -----------------------------------------------------------------------------
# 10. Invalid Inputs and Missing Files
# -----------------------------------------------------------------------------


def test_invalid_inputs_and_missing_files(trained_tokenizer: NovaTokenizer, corpus_path: Path):
    """Verify strict input validation and descriptive error reporting."""
    tok = trained_tokenizer

    # Invalid text types for encode
    with pytest.raises(TypeError, match="Expected str input for text"):
        tok.encode(12345)  # type: ignore

    with pytest.raises(TypeError, match="Expected str input for text"):
        tok.encode(None)  # type: ignore

    with pytest.raises(TypeError, match="texts must be a list of strings"):
        tok.encode_batch("not a list")  # type: ignore

    # Invalid sequence types for decode
    with pytest.raises(TypeError, match="Expected sequence of token IDs"):
        tok.decode("12345")  # type: ignore

    with pytest.raises(TypeError, match="All token IDs must be integers"):
        tok.decode([1, "bad_id", 3])  # type: ignore

    with pytest.raises(TypeError, match="All token IDs must be integers"):
        tok.decode([True, 1, 2])  # type: ignore (bool is subclass of int)

    # Out-of-bounds token IDs
    with pytest.raises(ValueError, match="out of bounds"):
        tok.decode([-1])

    with pytest.raises(ValueError, match="out of bounds"):
        tok.decode([tok.vocab_size + 1000])

    # Special token lookup invalid types and missing keys
    with pytest.raises(TypeError, match="Special token identifier must be str"):
        tok.get_special_token_id(123)  # type: ignore

    with pytest.raises(KeyError, match="not found in configured special tokens"):
        tok.get_special_token_id("nonexistent_special_token")

    # Missing files and paths
    with pytest.raises(FileNotFoundError, match="Path does not exist"):
        NovaTokenizer.from_file("completely/nonexistent/directory/or/file")

    with pytest.raises(FileNotFoundError, match="Corpus file not found"):
        NovaTokenizer.train_from_corpus("missing_corpus_file.txt")

    # Invalid training parameters
    with pytest.raises(ValueError, match="Target vocab_size must be a positive integer"):
        NovaTokenizer.train_from_corpus(corpus_path, vocab_size=0)

    with pytest.raises(ValueError, match="Target vocab_size must be a positive integer"):
        NovaTokenizer.train_from_corpus(corpus_path, vocab_size=-100)

    with pytest.raises(ValueError, match="min_frequency must be a positive integer"):
        NovaTokenizer.train_from_corpus(corpus_path, min_frequency=0)

    # Instantiating with invalid tokenizer type
    with pytest.raises(TypeError, match="Expected hf_tokenizer to be an instance of tokenizers.Tokenizer"):
        NovaTokenizer("not_a_tokenizer")  # type: ignore


# -----------------------------------------------------------------------------
# 11. Repeatability (Deterministic Training)
# -----------------------------------------------------------------------------


def test_repeatability_deterministic_training(corpus_path: Path):
    """Verify that training twice on the exact same corpus yields identical vocabularies."""
    tok1 = NovaTokenizer.train_from_corpus(corpus_path, vocab_size=1000, min_frequency=1)
    tok2 = NovaTokenizer.train_from_corpus(corpus_path, vocab_size=1000, min_frequency=1)

    assert tok1.vocab_size == tok2.vocab_size
    assert tok1.get_vocab() == tok2.get_vocab()

    sample = "Deterministic BPE training verification with squats and deadlifts."
    ids1 = tok1.encode(sample)
    ids2 = tok2.encode(sample)
    assert ids1 == ids2


# -----------------------------------------------------------------------------
# 12. Batch Encoding and Convenience Functions
# -----------------------------------------------------------------------------


def test_batch_and_convenience_functions(corpus_path: Path, trained_tokenizer: NovaTokenizer):
    """Verify batch encoding/decoding and module-level helper functions."""
    tok = trained_tokenizer
    texts = [
        "Exercise technique matters.",
        "Rest 90-120 seconds between sets.",
        "Protein intake: 1.6 to 2.2 g/kg/day.",
    ]

    batch_ids = tok.encode_batch(texts)
    assert len(batch_ids) == len(texts)
    decoded_batch = tok.decode_batch(batch_ids)
    assert decoded_batch == texts

    # Convenience functions
    c_ids = encode("Compound lifts recruit multiple muscle groups.", tok)
    assert isinstance(c_ids, list)
    c_text = decode(c_ids, tok)
    assert c_text == "Compound lifts recruit multiple muscle groups."

    # load_tokenizer helper
    loaded = load_tokenizer("artifacts/tokenizer")
    assert isinstance(loaded, NovaTokenizer)
