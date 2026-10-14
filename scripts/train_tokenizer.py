#!/usr/bin/env python3
"""Project Nova-Fit: Tokenizer Training CLI Script.

Trains a Byte-Level Byte Pair Encoding (BPE) tokenizer from scratch on a text
corpus and exports portable artifacts and metadata for Phase 1.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

# Ensure utf-8 stdout encoding on Windows console
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from nova.tokenizer import (
    DEFAULT_SPECIAL_TOKENS,
    DEFAULT_SPECIAL_TOKENS_MAP,
    NovaTokenizer,
    compute_file_sha256,
)




def parse_args(args: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments for tokenizer training."""
    parser = argparse.ArgumentParser(
        description="Train an original Byte-Level BPE tokenizer from scratch for Nova-Fit.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-c",
        "--corpus",
        type=str,
        default="data/raw/fitness_smoke_corpus.txt",
        help="Path to training text corpus file.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default="artifacts/tokenizer",
        help="Directory to save trained tokenizer.json and metadata.",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="configs/tokenizer.json",
        help="Path to tokenizer configuration JSON file (loads defaults).",
    )
    parser.add_argument(
        "-v",
        "--vocab-size",
        type=int,
        default=None,
        help="Target vocabulary size (defaults to config value or 8000).",
    )
    parser.add_argument(
        "-m",
        "--min-frequency",
        type=int,
        default=None,
        help="Minimum pair occurrence frequency (defaults to config value or 1).",
    )
    parser.add_argument(
        "--test-sentence",
        type=str,
        default="Squat 4x6 @ 80% 1RM. Rest 180s. Nutrition: 2.0 g/kg protein. 🏋️‍♂️",
        help="Sample sentence to verify encode/decode fidelity upon completion.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress detailed console progress output.",
    )

    return parser.parse_args(args)


def main(cli_args: Optional[list[str]] = None) -> int:
    """Execute tokenizer training workflow."""
    args = parse_args(cli_args)

    corpus_path = Path(args.corpus)
    output_dir = Path(args.output_dir)
    config_path = Path(args.config)

    # Load configuration file if present
    config_data = {}
    if config_path.is_file():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load config from {config_path}: {e}", file=sys.stderr)

    # Resolve target vocab size and min_frequency
    target_vocab_size = (
        args.vocab_size
        if args.vocab_size is not None
        else config_data.get("target_vocab_size", 8000)
    )
    min_frequency = (
        args.min_frequency
        if args.min_frequency is not None
        else config_data.get("min_frequency", 1)
    )
    special_tokens = config_data.get("special_tokens", DEFAULT_SPECIAL_TOKENS)
    special_tokens_map = config_data.get("special_tokens_map", DEFAULT_SPECIAL_TOKENS_MAP)

    if not corpus_path.is_file():
        print(f"Error: Corpus file not found at {corpus_path.resolve()}", file=sys.stderr)
        return 1

    corpus_size_bytes = corpus_path.stat().st_size
    corpus_sha = compute_file_sha256(corpus_path)

    if not args.quiet:
        print("=" * 70)
        print("Nova-Fit Tokenizer Training (Phase 1)")
        print("=" * 70)
        print(f"Corpus Path:         {corpus_path.resolve()}")
        print(f"Corpus Size:         {corpus_size_bytes:,} bytes")
        print(f"Corpus SHA-256:      {corpus_sha}")
        print(f"Target Vocab Size:   {target_vocab_size:,}")
        print(f"Min Frequency:       {min_frequency}")
        print(f"Output Directory:    {output_dir.resolve()}")
        print("Special Tokens:     ", special_tokens)
        print("-" * 70)

    try:
        tokenizer = NovaTokenizer.train_from_corpus(
            corpus_path=corpus_path,
            vocab_size=target_vocab_size,
            min_frequency=min_frequency,
            special_tokens=special_tokens,
            special_tokens_map=special_tokens_map,
        )
    except Exception as e:
        print(f"Training failed with error: {e}", file=sys.stderr)
        return 1

    actual_vocab_size = tokenizer.vocab_size

    # Save artifacts
    output_dir.mkdir(parents=True, exist_ok=True)
    saved_files = tokenizer.save(output_dir)

    if not args.quiet:
        print("Training successfully completed.")
        print(f"Actual Vocab Size:   {actual_vocab_size:,}")

        if actual_vocab_size < target_vocab_size:
            print()
            print("Notice on Vocabulary Size:")
            print(
                f"  The actual learned vocabulary size ({actual_vocab_size}) is smaller than "
                f"the requested target ({target_vocab_size}). This is expected behavior for "
                f"a small test fixture because BPE terminates when all recurrent byte-pair merges "
                f"in the text are exhausted. Scaling to the full 8,000-token target requires "
                f"a larger production training corpus."
            )
            print()

        print("Special Token Assignments:")
        for role, tok_str in tokenizer.special_tokens_map.items():
            tok_id = tokenizer.token_to_id(tok_str)
            print(f"  - {role:<12} {tok_str:<10} -> ID: {tok_id}")

        print("\nSaved Artifacts:")
        for key, path in saved_files.items():
            print(f"  - {key:<12}: {path.resolve()} ({path.stat().st_size:,} bytes)")

        # Verification on test sentence
        if args.test_sentence:
            print("-" * 70)
            print("Sample Encoding & Round-Trip Verification:")
            print(f"  Input:   {args.test_sentence}")
            encoded_ids = tokenizer.encode(args.test_sentence, allow_special=False)
            decoded_text = tokenizer.decode(encoded_ids)
            print(f"  Tokens:  {len(encoded_ids)} token IDs")
            print(f"  Round-trip exact match: {decoded_text == args.test_sentence}")

        print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
