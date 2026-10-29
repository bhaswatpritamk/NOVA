"""
scripts/screen_reslice_phase11_4.py
Phase 11.4 B5: Contamination and safety screening on the new PAGAC docs in data/staging_phase11_4/.
Produces data/staging_phase11_4/audit_outputs/reslice_screening.json.
"""

import json
from pathlib import Path
import sys

sys.path.insert(0, "src")
from nova.benchmark import FitnessEvaluationBenchmark
from nova.ingestion import HealthSafetyScreener, BenchmarkContaminationDetector

def main():
    bench_path = Path("data/benchmark/fitness_eval_benchmark.json")
    benchmark = FitnessEvaluationBenchmark.load(bench_path)
    detector = BenchmarkContaminationDetector(benchmark)
    screener = HealthSafetyScreener()

    train_path = Path("data/staging_phase11_4/train_staging.json")
    train_docs = json.load(open(train_path, encoding="utf-8"))

    results = {}
    print(f"{'Source ID':<35} | {'Safety Flags':<14} | {'Contaminated?':<14} | {'Benchmark Matches':<18}")
    print("-" * 88)

    for doc in train_docs:
        sid = doc["source_id"]
        if "PAGAC" in sid:
            text = doc["text"]
            safety_flags = screener.screen_text(text)
            critical_flags = [f for f in safety_flags if f.get("severity") in ("CRITICAL", "HIGH")]
            check_res = detector.check_text(text)
            
            results[sid] = {
                "source_id": sid,
                "doc_id": doc["doc_id"],
                "total_safety_flags": len(safety_flags),
                "critical_safety_flags": len(critical_flags),
                "safety_flags": safety_flags,
                "is_contaminated": check_res.is_contaminated,
                "has_bibliographic_match": check_res.has_bibliographic_match,
                "benchmark_match_count": len(check_res.matches),
                "benchmark_matches": [m.to_dict() for m in check_res.matches],
                "screening_status": "PASSED" if not check_res.is_contaminated and not critical_flags else "FAILED",
            }
            
            print(f"{sid:<35} | {len(safety_flags):<14} | {str(check_res.is_contaminated):<14} | {len(check_res.matches):<18}")

    out_dir = Path("data/staging_phase11_4/audit_outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "reslice_screening.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nScreening results saved to {out_path}")

if __name__ == "__main__":
    main()
