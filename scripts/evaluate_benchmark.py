"""Project Nova-Fit: Reproducible Benchmark Evaluation Script.

Evaluates either a randomly initialized model or a trained checkpoint against
the Phase 8 held-out fitness evaluation benchmark:
1. Held-out next-token cross-entropy loss and perplexity on benchmark passages.
2. Rubric-based evaluation of factual support, relevance, uncertainty handling, and safety compliance.
3. Generates a reproducible evaluation report in JSON.

Important Caveat:
    Perplexity measures statistical predictability of text; a low perplexity score
    does NOT demonstrate factual correctness or clinical fitness competence.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import torch

from nova.benchmark import (
    BenchmarkEvaluationReport,
    BenchmarkItemScore,
    FitnessEvaluationBenchmark,
    evaluate_model_on_benchmark_passages,
)
from nova.checkpoint import load_checkpoint
from nova.model import NovaConfig, NovaForCausalLM
from nova.tokenizer import NovaTokenizer, load_tokenizer


def generate_response(
    model: NovaForCausalLM,
    tokenizer: NovaTokenizer,
    prompt: str,
    max_new_tokens: int = 64,
    device: str = "cpu",
    temperature: float = 0.0,
) -> str:
    """Greedy or temperature-based text generation for evaluation."""
    model.eval()
    input_ids = tokenizer.encode(f"Question: {prompt}\nAnswer:", allow_special=False)
    input_tensor = torch.tensor([input_ids], dtype=torch.long, device=device)

    generated = list(input_ids)
    with torch.no_grad():
        for _ in range(max_new_tokens):
            if input_tensor.size(1) >= model.config.max_seq_len:
                break
            out = model(input_tensor)
            next_logits = out.logits[:, -1, :]
            if temperature > 0.0:
                probs = torch.softmax(next_logits / temperature, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1).item()
            else:
                next_token = torch.argmax(next_logits, dim=-1).item()

            if next_token == tokenizer.eos_token_id:
                break
            generated.append(next_token)
            input_tensor = torch.tensor([generated], dtype=torch.long, device=device)

    new_tokens = generated[len(input_ids) :]
    return tokenizer.decode(new_tokens)


def run_benchmark_evaluation(
    model_config_path: str,
    benchmark_path: str,
    tokenizer_path: str,
    checkpoint_path: str | None = None,
    output_path: str | None = None,
    device_name: str = "cpu",
) -> BenchmarkEvaluationReport:
    """Execute complete benchmark evaluation harness."""
    device = torch.device(device_name)
    tokenizer = load_tokenizer(tokenizer_path)

    import dataclasses

    with open(model_config_path, "r", encoding="utf-8") as f:
        cfg_dict = json.load(f)
    cfg_dict["vocab_size"] = tokenizer.vocab_size
    cfg_dict["max_seq_len"] = max(cfg_dict.get("max_seq_len", 32), 256)
    valid_fields = {f.name for f in dataclasses.fields(NovaConfig)}
    filtered_cfg = {k: v for k, v in cfg_dict.items() if k in valid_fields}
    model_cfg = NovaConfig(**filtered_cfg)
    model = NovaForCausalLM(model_cfg).to(device)

    model_name = "Nova-Prototype-RandomInit"
    if checkpoint_path and Path(checkpoint_path).is_file():
        ckpt = load_checkpoint(checkpoint_path, model=model, device=device)
        step = ckpt.get("step", 0) if isinstance(ckpt, dict) else getattr(ckpt, "step", 0)
        model_name = f"Nova-Checkpoint-Step{step}"

    param_count = sum(p.numel() for p in model.parameters())
    benchmark = FitnessEvaluationBenchmark.load(benchmark_path)

    print(f"Loaded benchmark with {len(benchmark.questions)} questions.")
    print(f"Evaluating {model_name} ({param_count:,} parameters) on {device_name}...")

    # Step 1: Measure reference cross-entropy loss and perplexity
    ref_loss, ref_ppl = evaluate_model_on_benchmark_passages(
        model=model,
        benchmark=benchmark,
        tokenizer=tokenizer,
        device=device,
        max_seq_len=model_cfg.max_seq_len,
        pad_token_id=tokenizer.pad_token_id or 0,
    )

    # Step 2: Generation and rubric-based scoring
    item_scores: list[BenchmarkItemScore] = []
    type_scores: dict[str, list[float]] = {}
    pillar_scores: dict[str, list[float]] = {}

    for q in benchmark.questions.values():
        response = generate_response(model, tokenizer, q.prompt, max_new_tokens=48, device=device_name)
        score = benchmark.score_response(q, response)
        item_scores.append(score)

        type_scores.setdefault(q.question_type.value, []).append(score.composite_score)
        pillar_scores.setdefault(q.pillar, []).append(score.composite_score)

    mean_comp = sum(s.composite_score for s in item_scores) / len(item_scores)
    mean_fact = sum(s.factual_support_score for s in item_scores) / len(item_scores)
    mean_rel = sum(s.relevance_score for s in item_scores) / len(item_scores)
    mean_unc = sum(s.uncertainty_score for s in item_scores) / len(item_scores)
    mean_saf = sum(s.safety_score for s in item_scores) / len(item_scores)

    type_summary = {k: sum(v) / len(v) for k, v in type_scores.items()}
    pillar_summary = {k: sum(v) / len(v) for k, v in pillar_scores.items()}

    report = BenchmarkEvaluationReport(
        model_name=model_name,
        model_parameter_count=param_count,
        benchmark_version=benchmark.version,
        total_questions=len(benchmark.questions),
        mean_composite_score=mean_comp,
        mean_factual_score=mean_fact,
        mean_relevance_score=mean_rel,
        mean_uncertainty_score=mean_unc,
        mean_safety_score=mean_saf,
        type_breakdown=type_summary,
        pillar_breakdown=pillar_summary,
        held_out_loss=ref_loss,
        held_out_perplexity=ref_ppl,
        item_scores=item_scores,
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    )

    print("\n" + report.summary())

    if output_path:
        op = Path(output_path)
        op.parent.mkdir(parents=True, exist_ok=True)
        with open(op, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, indent=2)
        print(f"Saved evaluation report to {output_path}")

    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Nova model on held-out fitness benchmark.")
    parser.add_argument("--model-config", type=str, default="configs/tiny_model.json")
    parser.add_argument("--benchmark", type=str, default="data/benchmark/fitness_eval_benchmark.json")
    parser.add_argument("--tokenizer", type=str, default="artifacts/final_tokenizer")
    parser.add_argument("--checkpoint", type=str, default=None)
    parser.add_argument("--output", type=str, default="docs/benchmark_baseline_report.json")
    parser.add_argument("--device", type=str, default="cpu")
    args = parser.parse_args()

    run_benchmark_evaluation(
        model_config_path=args.model_config,
        benchmark_path=args.benchmark,
        tokenizer_path=args.tokenizer,
        checkpoint_path=args.checkpoint,
        output_path=args.output,
        device_name=args.device,
    )


if __name__ == "__main__":
    main()
