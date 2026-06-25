from __future__ import annotations

from pathlib import Path

import pandas as pd

from datter.eval.loop import run_eval_loop
from datter.eval.queries import load_queries
from datter.models import Chunk, EvalSummary, ParetoPoint, SelectedCorpus
from datter.selection import build_selection, select_random_cut

# Sweep targets from conservative to aggressive (max token drop at quality floor)
REDUCTION_TARGETS = (0.20, 0.30, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80)


def scan_pareto_frontier(
    chunks: list[Chunk],
    merged_scores: pd.DataFrame,
    scores: pd.DataFrame,
    queries_path: Path,
) -> tuple[SelectedCorpus, EvalSummary, list[ParetoPoint]]:
    """Find maximum token reduction that still meets the project's quality floor."""
    config = load_queries(queries_path)
    floor_pct = config.quality_floor * 100.0

    frontier: list[ParetoPoint] = [
        ParetoPoint(token_reduction_pct=0.0, understanding_pct=100.0, label="Full corpus"),
    ]

    best_selection: SelectedCorpus | None = None
    best_summary: EvalSummary | None = None
    best_reduction = 0.0

    for target in REDUCTION_TARGETS:
        selection = build_selection(
            chunks, scores, target_reduction=target, queries_path=queries_path
        )
        actual_reduction = (
            1.0 - selection.datter_tokens / selection.full_tokens if selection.full_tokens else 0.0
        )
        summary = run_eval_loop(merged_scores, selection, queries_path)
        understanding = summary.understanding_pct

        frontier.append(
            ParetoPoint(
                token_reduction_pct=round(actual_reduction * 100, 1),
                understanding_pct=round(understanding, 1),
                label=f"Cut {round(target * 100)}% target",
            )
        )

        if understanding >= floor_pct:
            best_selection = selection
            best_summary = summary
            best_reduction = actual_reduction
        else:
            break

    if best_selection is None:
        best_selection = build_selection(
            chunks, scores, target_reduction=0.20, queries_path=queries_path
        )
        best_summary = run_eval_loop(merged_scores, best_selection, queries_path)
        best_reduction = (
            1.0 - best_selection.datter_tokens / best_selection.full_tokens
            if best_selection.full_tokens
            else 0.0
        )

    assert best_summary is not None
    random_ids = select_random_cut(chunks, scores, best_selection.datter_chunk_ids)
    compare_selection = SelectedCorpus(
        full_tokens=best_selection.full_tokens,
        datter_tokens=best_selection.datter_tokens,
        random_tokens=best_selection.datter_tokens,
        target_reduction=best_selection.target_reduction,
        datter_chunk_ids=best_selection.datter_chunk_ids,
        random_chunk_ids=random_ids,
    )
    random_summary = run_eval_loop(merged_scores, compare_selection, queries_path)

    frontier.append(
        ParetoPoint(
            token_reduction_pct=round(best_reduction * 100, 1),
            understanding_pct=round(best_summary.understanding_pct, 1),
            label="Max safe cut (Datter)",
        )
    )
    frontier.append(
        ParetoPoint(
            token_reduction_pct=round(best_reduction * 100, 1),
            understanding_pct=round(random_summary.understanding_pct, 1),
            label="Random at same budget",
        )
    )

    best_summary.pareto_points = frontier
    best_summary.max_safe_reduction_pct = round(best_reduction * 100, 1)
    best_summary.meets_quality_floor = best_summary.understanding_pct >= floor_pct
    best_summary.random_understanding_pct = random_summary.understanding_pct
    best_summary.actual_reduction = round(best_reduction, 4)

    return best_selection, best_summary, frontier


def run_eval_at_quality_floor(
    chunks: list[Chunk],
    merged_scores: pd.DataFrame,
    scores: pd.DataFrame,
    queries_path: Path,
) -> tuple[SelectedCorpus, EvalSummary]:
    """Select max token cut subject to quality floor, then return eval summary."""
    selection, summary, _ = scan_pareto_frontier(chunks, merged_scores, scores, queries_path)
    return selection, summary
