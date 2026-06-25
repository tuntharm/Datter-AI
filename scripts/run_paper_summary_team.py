#!/usr/bin/env python3
"""CLI runner for Paper Summary Team multi-model exam loop."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from datter.agent import AnalysisAgent
from datter.eval.llm_judge import has_llm_keys
from datter.eval.paper_summary_team import (
    PaperSummaryTeamResult,
    run_team_loop,
    save_exam_results,
)
from datter.project import get_project


def _print_summary(result: PaperSummaryTeamResult) -> None:
    print("\n=== Paper Summary Team Results ===")
    print(f"Project:        {result.project_id}")
    print(f"API mode:       {result.api_mode}")
    print(f"Quality floor:  {result.quality_floor * 100:.0f}%")
    print(f"Iterations:     {result.iterations_run}")
    print(f"Passed:         {result.passed}")
    print(f"Compression:    {result.compression_pct:.1f}%")
    print(f"Min score:      {result.min_score_across_models:.1f}%")
    print(f"Tokens full:    {result.tokens_full:,}")
    print(f"Tokens compressed: {result.tokens_compressed:,}")
    if result.disclaimer:
        print(f"Note:           {result.disclaimer}")
    print("\n| Model    | Score | Passed | Full tok | Comp tok |")
    print("|----------|------:|--------|----------:|---------:|")
    for m in result.model_results:
        print(
            f"| {m.model_family:<8} | {m.mean_score:5.1f} | "
            f"{'Yes' if m.passed else 'No':<6} | {m.tokens_full:9,} | {m.tokens_compressed:9,} |"
        )
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Paper Summary Team exam loop")
    parser.add_argument("--project", required=True, help="Project id (e.g. lab, government)")
    parser.add_argument(
        "--quality-floor",
        type=float,
        default=1.0,
        help="Minimum understanding score 0-1 (default 1.0 = 100%%)",
    )
    parser.add_argument("--max-iterations", type=int, default=6)
    args = parser.parse_args()

    project = get_project(args.project)
    if project is None:
        print(f"Unknown project: {args.project}", file=sys.stderr)
        return 1

    if not has_llm_keys():
        print("No API keys — running offline TF-IDF judge fallback.")

    agent = AnalysisAgent(
        scorer_mode="baseline",
        project_id=project.id,
        project_name=project.name,
        queries_path=project.queries_path,
        target_token_reduction=project.target_token_reduction,
    )
    report = agent.run_from_folder(str(project.corpus_path))

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
    _print_summary(result)
    print(f"Results written to: {out_path}")
    return 0 if result.passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
