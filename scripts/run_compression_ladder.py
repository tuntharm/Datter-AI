#!/usr/bin/env python3
"""Progressive compression ladder — score each step with Paper Summary Team offline eval."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from datter.agent import AnalysisAgent
from datter.eval.llm_judge import get_model_roster, has_llm_keys
from datter.eval.paper_summary_team import (
    _run_model_exams,
    corpus_text_from_chunks,
)
from datter.project import get_project
from datter.selection import build_selection

LADDER_TARGETS = (0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70)


def run_ladder(
    project_id: str,
    quality_floor: float = 0.90,
    targets: tuple[float, ...] = LADDER_TARGETS,
) -> dict:
    project = get_project(project_id)
    if project is None:
        raise SystemExit(f"Unknown project: {project_id}")

    agent = AnalysisAgent(
        scorer_mode="baseline",
        project_id=project.id,
        project_name=project.name,
        queries_path=project.queries_path,
        target_token_reduction=targets[0],
    )
    report = agent.run_from_folder(str(project.corpus_path))
    chunks = report.chunks
    scores = report.scores
    floor_pct = quality_floor * 100.0

    steps: list[dict] = []
    best_pass: dict | None = None
    stopped_early = False

    for target in targets:
        selection = build_selection(
            chunks,
            scores,
            target_reduction=target,
            queries_path=project.queries_path,
        )
        actual_reduction = (
            1.0 - selection.datter_tokens / selection.full_tokens
            if selection.full_tokens
            else 0.0
        )
        full_text = corpus_text_from_chunks(chunks, {c.item_id for c in chunks})
        compressed_text = corpus_text_from_chunks(chunks, set(selection.datter_chunk_ids))

        model_results = _run_model_exams(
            full_text,
            compressed_text,
            get_model_roster(),
            project.queries_path,
            quality_floor,
        )
        min_score = min(r.mean_score for r in model_results)
        passed = min_score >= floor_pct
        tokens_saved = selection.full_tokens - selection.datter_tokens

        step = {
            "target_reduction": target,
            "actual_reduction_pct": round(actual_reduction * 100, 1),
            "tokens_full": selection.full_tokens,
            "tokens_compressed": selection.datter_tokens,
            "tokens_saved": tokens_saved,
            "min_score": round(min_score, 1),
            "passed": passed,
            "model_scores": {r.model_family: r.mean_score for r in model_results},
        }
        steps.append(step)

        if passed:
            best_pass = step
        else:
            stopped_early = True
            break

    assert steps
    best = best_pass or steps[0]
    tokens_saved = best["tokens_full"] - best["tokens_compressed"]

    return {
        "project_id": project.id,
        "project_name": project.name,
        "quality_floor": quality_floor,
        "api_mode": "live" if has_llm_keys() else "offline",
        "disclaimer": (
            ""
            if has_llm_keys()
            else "Offline TF-IDF judge fallback — production claims require live multi-model run."
        ),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "ladder_targets": list(targets),
        "steps": steps,
        "stopped_early": stopped_early,
        "best_at_floor": {
            "target_reduction": best["target_reduction"],
            "actual_reduction_pct": best["actual_reduction_pct"],
            "min_score": best["min_score"],
            "tokens_full": best["tokens_full"],
            "tokens_compressed": best["tokens_compressed"],
            "tokens_saved": tokens_saved,
        },
    }


def write_summary_md(project_path: Path, result: dict) -> Path:
    best = result["best_at_floor"]
    lines = [
        f"# Compression ladder — {result['project_name']}",
        "",
        f"Generated: {result['generated_at'][:10]} · Mode: **{result['api_mode']}**",
        "",
        "## Best at quality floor",
        "",
        f"- **Max safe compression:** {best['actual_reduction_pct']:.1f}% "
        f"(target {best['target_reduction']:.0%})",
        f"- **Min score:** {best['min_score']:.1f}% (floor {result['quality_floor'] * 100:.0f}%)",
        f"- **Tokens saved:** {best['tokens_saved']:,} "
        f"({best['tokens_full']:,} → {best['tokens_compressed']:,})",
        "",
        "## Ladder",
        "",
        "| Target | Actual cut | Min score | Passed | Tokens kept |",
        "|-------:|-----------:|----------:|:------:|------------:|",
    ]
    for s in result["steps"]:
        lines.append(
            f"| {s['target_reduction']:.0%} | {s['actual_reduction_pct']:.1f}% | "
            f"{s['min_score']:.1f}% | {'✓' if s['passed'] else '✗'} | "
            f"{s['tokens_compressed']:,} |"
        )
    if result["disclaimer"]:
        lines.extend(["", f"*{result['disclaimer']}*"])
    lines.append("")
    out = project_path / "compression_ladder_summary.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Run progressive compression ladder")
    parser.add_argument("--project", required=True)
    parser.add_argument("--quality-floor", type=float, default=0.90)
    args = parser.parse_args()

    project = get_project(args.project)
    if project is None:
        print(f"Unknown project: {args.project}", file=sys.stderr)
        return 1

    result = run_ladder(args.project, quality_floor=args.quality_floor)
    json_path = project.corpus_path / "compression_ladder.json"
    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    md_path = write_summary_md(project.corpus_path, result)

    best = result["best_at_floor"]
    print(f"\n=== Compression Ladder — {result['project_name']} ===")
    print(f"Mode: {result['api_mode']}")
    print(f"Best at floor: {best['actual_reduction_pct']:.1f}% cut, score {best['min_score']:.1f}%")
    print(f"Tokens saved: {best['tokens_saved']:,}")
    print("\n| Target | Actual | Score | Pass |")
    print("|-------:|-------:|------:|:----:|")
    for s in result["steps"]:
        print(
            f"| {s['target_reduction']:.0%} | {s['actual_reduction_pct']:.1f}% | "
            f"{s['min_score']:.1f}% | {'Yes' if s['passed'] else 'No'} |"
        )
    print(f"\nJSON: {json_path}")
    print(f"Summary: {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
