#!/usr/bin/env python3
"""Project Nova-Fit: Dataset Preparation CLI Script.

Executes the reproducible dataset preparation pipeline (Phase 3):
1. Loads and cleans corpus text files.
2. Tokenizes documents using the trained Nova-Fit tokenizer.
3. Packs token sequences to fixed context-window length.
4. Splits into train/validation sets.
5. Saves PyTorch tensor files and a provenance manifest.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

# Ensure utf-8 stdout encoding on Windows console
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from nova.data import (
    CleaningConfig,
    PrepareDatasetConfig,
    prepare_dataset,
)


def parse_args(args: Optional[list[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments for dataset preparation."""
    parser = argparse.ArgumentParser(
        description="Nova-Fit Dataset Preparation Pipeline (Phase 3).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-c",
        "--corpus",
        type=str,
        nargs="+",
        default=["data/raw/fitness_smoke_corpus.txt"],
        help="Path(s) to training text corpus file(s).",
    )
    parser.add_argument(
        "-t",
        "--tokenizer",
        type=str,
        default="artifacts/tokenizer",
        help="Path to trained tokenizer directory or tokenizer.json.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default="data/prepared",
        help="Directory to save prepared dataset files.",
    )
    parser.add_argument(
        "--max-seq-len",
        type=int,
        default=512,
        help="Maximum sequence length for packed training sequences.",
    )
    parser.add_argument(
        "--val-ratio",
        type=float,
        default=0.05,
        help="Fraction of sequences to reserve for validation.",
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Optional path to dataset JSON configuration file.",
    )
    parser.add_argument(
        "--train-corpus",
        type=str,
        default=None,
        help="Path to dedicated frozen training corpus file.",
    )
    parser.add_argument(
        "--val-corpus",
        type=str,
        default=None,
        help="Path to dedicated frozen validation corpus file.",
    )
    parser.add_argument(
        "--split-level",
        type=str,
        choices=["document", "sequence"],
        default="sequence",
        help="Splitting level: 'document' (recommended) or 'sequence'.",
    )
    parser.add_argument(
        "--source-registry",
        type=str,
        default=None,
        help="Path to approved source registry JSON file for provenance auditing.",
    )
    parser.add_argument(
        "--split-seed",
        type=int,
        default=42,
        help="Random seed for reproducible train/validation split.",
    )
    parser.add_argument(
        "--drop-last",
        action="store_true",
        help="Drop the final short sequence instead of padding it.",
    )
    parser.add_argument(
        "--no-eos",
        action="store_true",
        help="Do not append EOS token after each document.",
    )
    parser.add_argument(
        "--strip-headers",
        action="store_true",
        help="Strip [SECTION: ...] headers from corpus text.",
    )
    parser.add_argument(
        "--lowercase",
        action="store_true",
        help="Lowercase all text during cleaning.",
    )
    parser.add_argument(
        "--min-doc-chars",
        type=int,
        default=20,
        help="Minimum document length in characters after cleaning.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress detailed console output.",
    )

    return parser.parse_args(args)


def main(cli_args: Optional[list[str]] = None) -> int:
    """Execute dataset preparation pipeline."""
    args = parse_args(cli_args)

    if args.config:
        import json
        with open(args.config, "r", encoding="utf-8") as f:
            cfg_data = json.load(f)

        cleaning_dict = cfg_data.get("cleaning", {})
        cleaning_config = CleaningConfig(
            strip_comment_lines=cleaning_dict.get("strip_comment_lines", True),
            strip_section_headers=cleaning_dict.get("strip_section_headers", False),
            normalize_whitespace=cleaning_dict.get("normalize_whitespace", True),
            strip_leading_trailing=cleaning_dict.get("strip_leading_trailing", True),
            min_doc_chars=cleaning_dict.get("min_doc_chars", 20),
            lowercase=cleaning_dict.get("lowercase", False),
        )

        pipeline_config = PrepareDatasetConfig(
            corpus_paths=cfg_data.get("corpus_paths", args.corpus),
            tokenizer_path=cfg_data.get("tokenizer_path", args.tokenizer),
            output_dir=cfg_data.get("output_dir", args.output_dir),
            max_seq_len=cfg_data.get("max_seq_len", args.max_seq_len),
            val_ratio=cfg_data.get("val_ratio", args.val_ratio),
            split_seed=cfg_data.get("split_seed", args.split_seed),
            drop_last_short=cfg_data.get("drop_last_short", args.drop_last),
            cleaning=cleaning_config,
            add_eos=cfg_data.get("add_eos", not args.no_eos),
            split_level=cfg_data.get("split_level", "document"),
            detect_duplicates=cfg_data.get("detect_duplicates", True),
            train_corpus_path=cfg_data.get("train_corpus_path"),
            val_corpus_path=cfg_data.get("val_corpus_path"),
            source_registry_path=cfg_data.get("source_registry_path"),
        )
    else:
        cleaning_config = CleaningConfig(
            strip_section_headers=args.strip_headers,
            lowercase=args.lowercase,
            min_doc_chars=args.min_doc_chars,
        )

        pipeline_config = PrepareDatasetConfig(
            corpus_paths=args.corpus,
            tokenizer_path=args.tokenizer,
            output_dir=args.output_dir,
            max_seq_len=args.max_seq_len,
            val_ratio=args.val_ratio,
            split_seed=args.split_seed,
            drop_last_short=args.drop_last,
            cleaning=cleaning_config,
            add_eos=not args.no_eos,
            split_level=args.split_level,
            train_corpus_path=args.train_corpus,
            val_corpus_path=args.val_corpus,
            source_registry_path=args.source_registry,
        )

    result = prepare_dataset(
        config=pipeline_config,
        verbose=not args.quiet,
    )

    if not result.success:
        print(f"Dataset preparation failed: {result.message}", file=sys.stderr)
        return 1

    if not args.quiet:
        print(f"\n✓ {result.message}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
