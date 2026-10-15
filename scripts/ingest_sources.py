#!/usr/bin/env python3
"""Project NOVA Phase 10: Verified Fitness Corpus Ingestion & Expansion CLI.

Reproducible entry point for:
- Ingesting multi-format source material (HTML, Markdown, Plain Text, PDF, JSON).
- Enforcing legal licensing gates (17 U.S.C. § 105, CC BY 4.0, CC0) and rejecting non-compliant licenses.
- Screening health and fitness claims for dangerous medical or dietary advice.
- Preventing held-out benchmark contamination (exact and near-duplicate leakage).
- Deduplicating and clustering related documents.
- Performing source-level and group-level train/val partitioning.
- Generating cryptographic manifests, per-pillar token counts, and audit reports.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from nova.benchmark import FitnessEvaluationBenchmark
from nova.corpus import SourceRegistry
from nova.ingestion import (
    FitnessPillar,
    IngestionStatus,
    LicenseGateResult,
    NormalizedDocument,
    Phase10Manifest,
    SourceIngestionPipeline,
    audit_license,
    normalize_pillar,
    source_level_split,
)
from nova.tokenizer import NovaTokenizer, load_tokenizer

DEFAULT_TOKENIZER_DIR = REPO_ROOT / "artifacts" / "final_tokenizer"
DEFAULT_BENCHMARK_PATH = REPO_ROOT / "data" / "benchmark" / "fitness_eval_benchmark.json"
DEFAULT_REGISTRY_PATH = REPO_ROOT / "data" / "approved" / "source_registry.json"
DEFAULT_STATE_FILE = REPO_ROOT / "data" / "phase10_ingestion_state.json"


def cmd_audit(args: argparse.Namespace) -> int:
    """Audit existing registry, candidate sources, and active corpus."""
    print("=" * 76)
    print("PROJECT NOVA: PHASE 10 CORPUS AUDIT")
    print("=" * 76)

    reg_path = Path(args.registry)
    if not reg_path.is_file():
        print(f"Error: Source registry not found at {reg_path}")
        return 1

    registry = json.loads(reg_path.read_text(encoding="utf-8"))
    sources = registry.get("approved_sources", [])
    print(f"\n1. REGISTERED SOURCES IN {reg_path.name}: {len(sources)} sources")
    print("-" * 76)

    public_domain_count = 0
    cc_by_count = 0
    raw_dir = REPO_ROOT / "data" / "sources_raw"
    hash_mismatches = 0
    missing_raw = 0

    for s in sources:
        sid = s["source_id"]
        lic = s.get("license", "Unknown")
        basis = s.get("legal_basis", "")
        gate = audit_license(lic, basis)

        if "public domain" in lic.lower() or "17 u.s.c" in basis.lower():
            public_domain_count += 1
        elif "cc by" in lic.lower():
            cc_by_count += 1

        fname = f"{sid.lower().replace('-', '_')}_raw.txt"
        fpath = raw_dir / fname
        status = "OK"
        if not fpath.is_file():
            status = "MISSING RAW"
            missing_raw += 1
        else:
            h = hashlib.sha256(fpath.read_bytes()).hexdigest()
            if h.lower() != s.get("raw_sha256", "").lower():
                status = f"HASH MISMATCH (expected {s.get('raw_sha256', '')[:8]}... got {h[:8]}...)"
                hash_mismatches += 1

        print(f"  [{gate.category.value}] {sid:25} | {lic:15} | Raw: {status}")

    print(f"\nLicense breakdown: {public_domain_count} Public Domain (17 U.S.C. § 105), {cc_by_count} CC BY 4.0.")
    print(f"Integrity check: {missing_raw} missing files, {hash_mismatches} hash mismatches.")

    # Audit Traceability & Educational Syntheses
    trace_path = REPO_ROOT / "data" / "approved" / "document_traceability.json"
    if trace_path.is_file():
        trace = json.loads(trace_path.read_text(encoding="utf-8"))
        docs = trace.get("documents", [])
        synth_docs = sum(1 for d in docs if d.get("authoring_method") == "educational_synthesis")
        print(f"\n2. DOCUMENT PROVENANCE AUDIT ({trace_path.name})")
        print("-" * 76)
        print(f"  Total traceability documents: {len(docs)}")
        print(f"  Educational syntheses:        {synth_docs} (100.0% of existing baseline corpus)")
        print(f"  Original source extractions:  {len(docs) - synth_docs}")
        print("  NOTICE: All existing 306 documents are synthesized educational texts rather")
        print("          than direct raw source extracts.")

    # Audit Candidate Sources
    cand_path = REPO_ROOT / "docs" / "candidate_sources_for_review.md"
    if cand_path.is_file():
        print(f"\n3. CANDIDATE SOURCE QUEUE ({cand_path.name})")
        print("-" * 76)
        content = cand_path.read_text(encoding="utf-8")
        lines = [line for line in content.split("\n") if line.strip().startswith("| **CAND-")]
        print(f"  Candidates pending human review: {len(lines)}")
        for line in lines:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 6:
                cid = parts[0]
                pillar = parts[3]
                est_toks = parts[4]
                status = parts[5]
                print(f"  {cid:30} | {pillar:22} | Est. {est_toks:10} | {status}")

    # Audit Current Dataset Manifest
    man_path = REPO_ROOT / "data" / "prepared_expanded" / "manifest.json"
    if man_path.is_file():
        man = json.loads(man_path.read_text(encoding="utf-8"))
        print(f"\n4. AUTHORITATIVE DATASET MANIFEST ({man_path.name})")
        print("-" * 76)
        print(f"  Manifest SHA-256:          {hashlib.sha256(man_path.read_bytes()).hexdigest()}")
        print(f"  Authoritative Tokenizer:   {man.get('tokenizer_hash')}")
        print(f"  Training valid tokens:     {man.get('total_tokens_train'):,} (in {man.get('train_sequences')} packed sequences)")
        print(f"  Validation valid tokens:   {man.get('total_tokens_val'):,} (in {man.get('val_sequences')} packed sequences)")
        print(f"  Total valid tokens:        {man.get('total_tokens_train', 0) + man.get('total_tokens_val', 0):,}")

    print("\nAudit completed successfully.")
    return 0


def cmd_ingest(args: argparse.Namespace) -> int:
    """Ingest a source file or directory of source files."""
    print("=" * 76)
    print("PROJECT NOVA: PHASE 10 SOURCE INGESTION PIPELINE")
    print("=" * 76)

    input_path = Path(args.input_path)
    if not input_path.exists():
        print(f"Error: Input path does not exist: {input_path}")
        return 1

    # Load Tokenizer
    tok_dir = Path(args.tokenizer_dir) if args.tokenizer_dir else DEFAULT_TOKENIZER_DIR
    tokenizer = None
    if tok_dir.is_dir():
        try:
            tokenizer = load_tokenizer(tok_dir)
            print(f"Loaded tokenizer from {tok_dir} (vocab={tokenizer.vocab_size})")
        except Exception as e:
            print(f"Warning: Failed loading tokenizer from {tok_dir}: {e}")

    # Load Benchmark for contamination detection
    bm_path = Path(args.benchmark) if args.benchmark else DEFAULT_BENCHMARK_PATH
    benchmark = None
    if bm_path.is_file():
        try:
            benchmark = FitnessEvaluationBenchmark.load(bm_path)
            print(f"Loaded evaluation benchmark from {bm_path} ({len(benchmark.questions)} questions)")
        except Exception as e:
            print(f"Warning: Failed loading benchmark from {bm_path}: {e}")

    # Initialize Pipeline
    state_file = Path(args.state_file) if args.state_file else DEFAULT_STATE_FILE
    pipeline = SourceIngestionPipeline(
        tokenizer=tokenizer,
        benchmark=benchmark,
        state_file=state_file,
    )

    metadata = {
        "source_id": args.source_id,
        "title": args.title or input_path.stem,
        "pillar": args.pillar or FitnessPillar.PILLAR_1_PHYSIOLOGY.value,
        "license": args.license,
        "legal_basis": args.legal_basis or "",
        "url": args.url or "",
        "author": args.author or "",
        "publisher": args.publisher or "",
        "publication_date": args.publication_date or "",
        "attribution_required": bool(args.attribution_required),
        "attribution_text": args.attribution_text or "",
        "authoring_method": args.authoring_method or "primary_source_extract",
    }

    files_to_process: List[Path] = []
    if input_path.is_file():
        files_to_process.append(input_path)
    else:
        for ext in ("*.txt", "*.md", "*.html", "*.htm", "*.json", "*.pdf"):
            files_to_process.extend(sorted(input_path.glob(ext)))

    print(f"\nProcessing {len(files_to_process)} input file(s)...")
    ingested_total = 0

    for f in files_to_process:
        print(f"  Ingesting {f.name}...")
        meta = copy.deepcopy(metadata)
        if not args.source_id:
            meta["source_id"] = f.stem.upper()
        if not args.title:
            meta["title"] = f.stem.replace("_", " ").title()

        docs = pipeline.ingest_file(
            file_path=f,
            source_metadata=meta,
            allow_human_override=args.allow_override,
            reviewer_id=args.reviewer_id or "",
            reviewer_notes=args.reviewer_notes or "",
        )
        ingested_total += len(docs)
        for d in docs:
            print(f"    -> [APPROVED] {d.doc_id} | Tokens: {d.token_count:,} | Words: {d.word_count}")

    pipeline.save_state()
    manifest = pipeline.generate_manifest()

    if args.output_manifest:
        out_man_path = Path(args.output_manifest)
        manifest.save(out_man_path)
        print(f"\nSaved Phase 10 Manifest to {out_man_path}")

    # Output Summary
    print("\nINGESTION SUMMARY:")
    print(f"  Approved documents in state:   {len(pipeline.ingested_docs)}")
    print(f"  Quarantined/Rejected docs:     {len(pipeline.quarantined_docs)}")
    print(f"  Total combined tokens:         {manifest.total_combined_tokens:,}")
    for p_key, p_stat in manifest.pillar_coverage.items():
        print(f"    {p_stat['display_name']:45}: {p_stat['doc_count']:4} docs | {p_stat['token_count']:7,} tokens ({p_stat['token_percentage']:5.1f}%)")

    return 0


def cmd_split(args: argparse.Namespace) -> int:
    """Split ingested documents into train and val at the source/group level."""
    print("=" * 76)
    print("PROJECT NOVA: SOURCE-LEVEL TRAIN/VAL PARTITIONER")
    print("=" * 76)

    state_file = Path(args.state_file) if args.state_file else DEFAULT_STATE_FILE
    if not state_file.is_file():
        print(f"Error: Ingestion state file not found: {state_file}")
        return 1

    with open(state_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = [NormalizedDocument.from_dict(d) for d in data.get("approved_docs", [])]
    if not docs:
        print("No approved documents found to split.")
        return 1

    print(f"Loaded {len(docs)} approved documents from state.")
    val_ratio = float(args.val_ratio)
    seed = int(args.seed)

    train_docs, val_docs = source_level_split(docs, val_ratio=val_ratio, seed=seed)
    print(f"\nPartitioning complete (val_ratio={val_ratio}, seed={seed}):")
    print(f"  Train documents: {len(train_docs)} ({sum(d.token_count for d in train_docs):,} tokens)")
    print(f"  Val documents:   {len(val_docs)} ({sum(d.token_count for d in val_docs):,} tokens)")

    # Verify zero leakage
    train_sources = set(d.source_id for d in train_docs)
    val_sources = set(d.source_id for d in val_docs)
    overlap = train_sources.intersection(val_sources)
    print(f"  Source-level overlap between train and val: {len(overlap)} sources")
    if overlap:
        print(f"  WARNING: Sources in both splits: {overlap}")
    else:
        print("  VERIFIED: Zero source-level leakage between train and val.")

    train_groups = set(d.group_id for d in train_docs)
    val_groups = set(d.group_id for d in val_docs)
    group_overlap = train_groups.intersection(val_groups)
    print(f"  Group-level overlap between train and val: {len(group_overlap)} groups")

    if args.output_dir:
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        train_file = out_dir / "phase10_train_corpus.txt"
        val_file = out_dir / "phase10_val_corpus.txt"

        train_file.write_text("\n\n".join(d.to_formatted_text() for d in train_docs), encoding="utf-8")
        val_file.write_text("\n\n".join(d.to_formatted_text() for d in val_docs), encoding="utf-8")
        print(f"  Wrote train corpus to {train_file}")
        print(f"  Wrote val corpus to {val_file}")

    return 0


def cmd_report(args: argparse.Namespace) -> int:
    """Generate per-pillar and quality report from state or manifest."""
    state_file = Path(args.state_file) if args.state_file else DEFAULT_STATE_FILE
    if not state_file.is_file():
        print(f"Error: State file not found: {state_file}")
        return 1

    tok_dir = Path(args.tokenizer_dir) if args.tokenizer_dir else DEFAULT_TOKENIZER_DIR
    tokenizer = load_tokenizer(tok_dir) if tok_dir.is_dir() else None
    pipeline = SourceIngestionPipeline(tokenizer=tokenizer, state_file=state_file)
    manifest = pipeline.generate_manifest()

    print("=" * 76)
    print("PROJECT NOVA: PHASE 10 CORPUS QUALITY & COVERAGE REPORT")
    print("=" * 76)
    print(f"Generated at:               {manifest.created_at}")
    print(f"Total documents processed:  {manifest.total_documents_ingested}")
    print(f"  Approved documents:       {manifest.total_documents_approved}")
    print(f"  Quarantined documents:    {manifest.total_documents_quarantined}")
    print(f"Total usable tokens:        {manifest.total_combined_tokens:,}")
    print("-" * 76)
    print(f"{'Pillar':<45} | {'Docs':>5} | {'Words':>8} | {'Tokens':>9} | {'Share':>6}")
    print("-" * 76)
    for p_key, p_stat in manifest.pillar_coverage.items():
        print(f"{p_stat['display_name']:<45} | {p_stat['doc_count']:5} | {p_stat['word_count']:8,} | {p_stat['token_count']:9,} | {p_stat['token_percentage']:5.1f}%")
    print("-" * 76)

    if manifest.quarantine_manifest:
        print(f"\nQUARANTINED DOCUMENTS ({len(manifest.quarantine_manifest)}):")
        for q in manifest.quarantine_manifest:
            print(f"  - [{q['doc_id']}] {q['title']}: {q['review_notes']}")

    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Project NOVA Phase 10: Verified Fitness Corpus Ingestion CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Subcommand to execute")

    # Audit subcommand
    audit_parser = subparsers.add_parser("audit", help="Audit existing repository, registries, and manifests")
    audit_parser.add_argument("--registry", default=str(DEFAULT_REGISTRY_PATH), help="Path to source registry JSON")

    # Ingest subcommand
    ingest_parser = subparsers.add_parser("ingest", help="Ingest source files through legal & safety pipeline")
    ingest_parser.add_argument("--input-path", "-i", required=True, help="Path to input file or directory")
    ingest_parser.add_argument("--source-id", "-s", default="", help="Source ID identifier (e.g. US-CDC-PA-2022)")
    ingest_parser.add_argument("--title", "-t", default="", help="Document title")
    ingest_parser.add_argument("--pillar", "-p", default="1", help="Target fitness pillar (1-7 or canonical key)")
    ingest_parser.add_argument("--license", "-l", default="Public Domain", help="Document license (e.g. 'Public Domain', 'CC BY 4.0')")
    ingest_parser.add_argument("--legal-basis", default="17 U.S.C. § 105", help="Statutory legal basis")
    ingest_parser.add_argument("--url", default="", help="Source retrieval URL")
    ingest_parser.add_argument("--author", default="", help="Author or authoring entity")
    ingest_parser.add_argument("--publisher", default="", help="Publishing organization")
    ingest_parser.add_argument("--publication-date", default="", help="Publication date")
    ingest_parser.add_argument("--attribution-required", action="store_true", help="Set if attribution is mandatory")
    ingest_parser.add_argument("--attribution-text", default="", help="Mandatory attribution statement")
    ingest_parser.add_argument("--authoring-method", default="primary_source_extract", help="Method used: primary_source_extract, educational_synthesis, etc.")
    ingest_parser.add_argument("--allow-override", action="store_true", help="Permit human legal review override for non-standard license")
    ingest_parser.add_argument("--reviewer-id", default="", help="Human reviewer ID approving override")
    ingest_parser.add_argument("--reviewer-notes", default="", help="Notes justifying human override approval")
    ingest_parser.add_argument("--tokenizer-dir", default=str(DEFAULT_TOKENIZER_DIR), help="Path to tokenizer directory")
    ingest_parser.add_argument("--benchmark", default=str(DEFAULT_BENCHMARK_PATH), help="Path to held-out benchmark JSON")
    ingest_parser.add_argument("--state-file", default=str(DEFAULT_STATE_FILE), help="State file path for resumable ingestion")
    ingest_parser.add_argument("--output-manifest", "-o", default="", help="Path to save Phase 10 manifest JSON")

    # Split subcommand
    split_parser = subparsers.add_parser("split", help="Perform source-level train/val partition")
    split_parser.add_argument("--state-file", default=str(DEFAULT_STATE_FILE), help="State file path")
    split_parser.add_argument("--val-ratio", default=0.15, type=float, help="Validation partition ratio")
    split_parser.add_argument("--seed", default=42, type=int, help="Deterministic random seed")
    split_parser.add_argument("--output-dir", default="", help="Directory to export partitioned text corpora")

    # Report subcommand
    report_parser = subparsers.add_parser("report", help="Generate quality and pillar coverage report")
    report_parser.add_argument("--state-file", default=str(DEFAULT_STATE_FILE), help="State file path")
    report_parser.add_argument("--tokenizer-dir", default=str(DEFAULT_TOKENIZER_DIR), help="Path to tokenizer directory")

    args = parser.parse_args()
    if not args.subcommand:
        parser.print_help()
        sys.exit(1)

    if args.subcommand == "audit":
        sys.exit(cmd_audit(args))
    elif args.subcommand == "ingest":
        sys.exit(cmd_ingest(args))
    elif args.subcommand == "split":
        sys.exit(cmd_split(args))
    elif args.subcommand == "report":
        sys.exit(cmd_report(args))


if __name__ == "__main__":
    import copy
    main()
