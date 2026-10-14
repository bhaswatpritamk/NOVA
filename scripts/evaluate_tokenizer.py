#!/usr/bin/env python3
"""Project Nova-Fit: Final Tokenizer Fertility and Robustness Evaluation.

Measures:
1. Actual vocabulary size and special token IDs.
2. Token fertility (characters per token, tokens per word) on representative fitness text.
3. Handling of numbers, units, punctuation, Unicode, and unfamiliar terms.
4. Save/load and encode/decode round-trip fidelity.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure UTF-8 stdout
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from nova.tokenizer import NovaTokenizer


def run_evaluation(tokenizer_path: str = "artifacts/final_tokenizer") -> None:
    tok = NovaTokenizer.from_file(tokenizer_path)

    print("=" * 70)
    print("NOVA-FIT FINAL TOKENIZER EVALUATION REPORT")
    print("=" * 70)
    print(f"Tokenizer Path:        {tokenizer_path}")
    print(f"Actual Vocab Size:     {tok.vocab_size:,}")
    print(f"Special Tokens:")
    print(f"  pad_token_id:        {tok.pad_token_id} ({tok.pad_token})")
    print(f"  unk_token_id:        {tok.unk_token_id} ({tok.unk_token})")
    print(f"  bos_token_id:        {tok.bos_token_id} ({tok.bos_token})")
    print(f"  eos_token_id:        {tok.eos_token_id} ({tok.eos_token})")
    print("-" * 70)

    test_samples = {
        "Technical Lifting": "Athletes should maintain neutral lumbar lordosis and execute the Valsalva maneuver during the eccentric descent of the barbell squat.",
        "Biomechanics & Anatomy": "The gluteus medius acts as a primary hip abductor while the rectus femoris crosses both the acetabulofemoral and tibiofemoral joints.",
        "Sets, Reps, Intensity": "Bench Press: 4 sets x 8 reps @ 77.5% 1RM, RPE 8.5, rest 180s. Squat 5x5 @ 82.5% 1RM.",
        "Nutrition & Units": "Consume 2.2 g/kg/day of high-quality protein with 2.5-3.0g leucine per meal; target a 350 kcal/day deficit.",
        "Punctuation & Symbols": "RIR 1-2 | 1RM: 140kg (±2.5kg); tempo 3-0-1-0 — rest 2:30 min:sec.",
        "Unicode & Emojis": "Heavy lifting session complete! 🏋️‍♂️ Room temperature: 20 ℃. Effort level: 100%.",
        "Unfamiliar / OOV Terms": "Z-disc titin mechanotransduction xenobiotic proprioceptive uncalibrated ultrafiltration",
    }

    print("REPRESENTATIVE FITNESS TEXT EVALUATIONS:")
    print("-" * 70)

    total_tokens_all = 0
    total_words_all = 0
    total_chars_all = 0
    all_roundtrips_passed = True

    for category, text in test_samples.items():
        tokens = tok.encode(text, allow_special=False)
        decoded = tok.decode(tokens, skip_special_tokens=False)
        exact_match = (text == decoded)
        if not exact_match:
            all_roundtrips_passed = False

        num_chars = len(text)
        num_words = len(text.split())
        num_tokens = len(tokens)

        total_chars_all += num_chars
        total_words_all += num_words
        total_tokens_all += num_tokens

        chars_per_token = num_chars / num_tokens if num_tokens else 0
        tokens_per_word = num_tokens / num_words if num_words else 0

        print(f"[{category}]")
        print(f"  Text:              \"{text}\"")
        print(f"  Tokens ({num_tokens}):       {tokens[:10]}{'...' if len(tokens) > 10 else ''}")
        print(f"  Tokens / Word:     {tokens_per_word:.2f}")
        print(f"  Chars / Token:     {chars_per_token:.2f}")
        print(f"  Exact Round-Trip:  {exact_match}")
        print()

    avg_tokens_per_word = total_tokens_all / total_words_all if total_words_all else 0
    avg_chars_per_token = total_chars_all / total_tokens_all if total_tokens_all else 0

    print("-" * 70)
    print(f"Aggregate Token Fertility Across Test Samples:")
    print(f"  Average Tokens / Word: {avg_tokens_per_word:.2f}")
    print(f"  Average Chars / Token: {avg_chars_per_token:.2f}")
    print(f"  All Round-Trips Match: {all_roundtrips_passed}")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Evaluate Nova-Fit tokenizer.")
    parser.add_argument(
        "-t",
        "--tokenizer",
        type=str,
        default="artifacts/final_tokenizer",
        help="Path to tokenizer directory or tokenizer.json",
    )
    args = parser.parse_args()
    run_evaluation(args.tokenizer)


if __name__ == "__main__":
    main()
