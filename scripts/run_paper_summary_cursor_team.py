#!/usr/bin/env python3
"""Cursor multi-model Paper Summary Team runner.

Production paths:
  (A) API keys set  → full automated loop via provider APIs
  (B) No API keys   → export exam_corpus + exam_prompts for Cursor chat replay,
                      plus orchestrator-simulated offline scores per model slot

Usage:
  python scripts/run_paper_summary_cursor_team.py --project lab
  python scripts/run_paper_summary_cursor_team.py --project government --quality-floor 0.90
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from datter.agent import AnalysisAgent
from datter.eval.llm_judge import CURSOR_MODEL_SLUGS, get_model_roster, has_llm_keys
from datter.eval.paper_summary_team import (
    PaperSummaryTeamResult,
    build_exam,
    corpus_text_from_chunks,
    export_cursor_corpus_aliases,
    run_cursor_simulated_eval,
    run_team_loop,
    save_cursor_exam_results,
    save_exam_results,
    write_cursor_exam_prompts,
)
from datter.eval.paper_summary_team import _export_exam_corpus  # noqa: PLC2701
from datter.project import get_project


def _print_summary(result: PaperSummaryTeamResult, prompts_dir: Path | None = None) -> None:
    print("\n=== Paper Summary Team (Cursor multi-model) ===")
    print(f"Project:        {result.project_id}")
    print(f"API mode:       {result.api_mode}")
    print(f"Quality floor:  {result.quality_floor * 100:.0f}%")
    print(f"Passed:         {result.passed}")
    print(f"Compression:    {result.compression_pct:.1f}%")
    print(f"Min score:      {result.min_score_across_models:.1f}%")
    if result.disclaimer:
        print(f"Note:           {result.disclaimer}")
    print("\n| Model slot | Cursor slug                         | Score | Passed |")
    print("|------------|-------------------------------------|------:|--------|")
    for m in result.model_results:
        print(
            f"| {m.model_family:<10} | {m.api_id:<35} | {m.mean_score:5.1f} | "
            f"{'Yes' if m.passed else 'No':<6} |"
        )
    if prompts_dir:
        print(f"\nExam prompts:   {prompts_dir}/")
        for slug in CURSOR_MODEL_SLUGS.values():
            print(f"  - {prompts_dir / (slug + '.md')}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run Paper Summary Team with Cursor multi-model support"
    )
    parser.add_argument("--project", required=True, help="Project id (lab, government, …)")
    parser.add_argument(
        "--quality-floor",
        type=float,
        default=0.90,
        help="Minimum understanding score 0-1 (default 0.90)",
    )
    parser.add_argument(
        "--num-questions",
        type=int,
        default=4,
        help="Exam questions for Cursor replay (default 4)",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=6,
        help="Compression retries when using API mode (default 6)",
    )
    parser.add_argument(
        "--export-only",
        action="store_true",
        help="Only export exam_corpus + exam_prompts; skip scoring",
    )
    args = parser.parse_args()

    project = get_project(args.project)
    if project is None:
        print(f"Unknown project: {args.project}", file=sys.stderr)
        return 1

    agent = AnalysisAgent(
        scorer_mode="baseline",
        project_id=project.id,
        project_name=project.name,
        queries_path=project.queries_path,
        target_token_reduction=project.target_token_reduction,
    )
    report = agent.run_from_folder(str(project.corpus_path))

    full_ids = {c.item_id for c in report.chunks}
    compressed_ids = set(report.selection.datter_chunk_ids)
    full_text = corpus_text_from_chunks(report.chunks, full_ids)
    compressed_text = corpus_text_from_chunks(report.chunks, compressed_ids)
    exam_dir = _export_exam_corpus(
        project.corpus_path, full_text, compressed_text, iteration=0
    )
    export_cursor_corpus_aliases(exam_dir, full_text, compressed_text)

    roster = get_model_roster()
    shared_exam = build_exam(
        full_text,
        roster[0],
        queries_path=project.queries_path,
        num_questions=args.num_questions,
    )
    prompts_dir = write_cursor_exam_prompts(
        project.corpus_path, shared_exam, compressed_text, roster
    )
    print(f"Exported corpus → {exam_dir}")
    print(f"Exported prompts → {prompts_dir}")

    if args.export_only:
        return 0

    if has_llm_keys():
        print("API keys detected — running live multi-model loop via providers.")
        result = run_team_loop(
            project_path=project.corpus_path,
            queries_path=project.queries_path,
            chunks=report.chunks,
            scores=report.scores,
            selection=report.selection,
            quality_floor=args.quality_floor,
            max_iterations=args.max_iterations,
            project_id=project.id,
        )
        out_path = save_exam_results(project.corpus_path, result)
        api_mode_label = "live_api"
    else:
        print("No API keys — running orchestrator-simulated eval per model slot.")
        result = run_cursor_simulated_eval(
            project_path=project.corpus_path,
            queries_path=project.queries_path,
            chunks=report.chunks,
            scores=report.scores,
            selection=report.selection,
            quality_floor=args.quality_floor,
            num_questions=args.num_questions,
            project_id=project.id,
        )
        out_path = save_cursor_exam_results(project.corpus_path, result)
        api_mode_label = result.api_mode

    _print_summary(result, prompts_dir)
    print(f"Results written to: {out_path}")
    print(f"Mode: {api_mode_label}")
    return 0 if result.passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
