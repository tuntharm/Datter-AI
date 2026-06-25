from pathlib import Path

import pandas as pd

from datter.agent import AnalysisAgent
from datter.eval.loop import run_eval_loop
from datter.eval.relevance_boost import apply_query_relevance_boost, chunk_relevance_score
from datter.selection import build_selection

ROOT = Path(__file__).parent.parent
DEMO = ROOT / "demo_data"


def test_gold_hint_boosts_matching_chunk():
    items = pd.DataFrame(
        [
            {"item_id": "a", "text": "duplicate exact near documents and low signal boilerplate meeting notes"},
            {"item_id": "b", "text": "lorem ipsum filler with no task terms"},
        ]
    )
    scores = pd.DataFrame(
        [
            {"item_id": "a", "usefulness_score": 0.3, "recommended_action": "keep"},
            {"item_id": "b", "usefulness_score": 0.35, "recommended_action": "keep"},
        ]
    )
    boosted = apply_query_relevance_boost(scores, items, DEMO / "queries.json")
    assert boosted.loc[boosted["item_id"] == "a", "usefulness_score"].iloc[0] > 0.3
    assert (
        boosted.loc[boosted["item_id"] == "a", "usefulness_score"].iloc[0]
        > boosted.loc[boosted["item_id"] == "b", "usefulness_score"].iloc[0]
    )


def test_chunk_relevance_zero_without_overlap():
    assert chunk_relevance_score("nothing relevant here", {"accountability": 2.0}) == 0.0


def test_boosted_selection_beats_unboosted_on_lab():
    """Query-term boost should keep gold-hint chunks and raise understanding vs raw scores."""
    agent = AnalysisAgent(scorer_mode="baseline")
    report = agent.run_from_folder(str(DEMO))
    merged = report.scores
    score_cols = [
        "item_id",
        "usefulness_score",
        "redundancy_score",
        "information_density_score",
        "recommended_action",
        "explanation",
    ]
    raw_scores = report.scores[[c for c in score_cols if c in report.scores.columns]].copy()
    target = 0.40

    unboosted = build_selection(report.chunks, raw_scores, target_reduction=target)
    boosted = build_selection(
        report.chunks,
        raw_scores,
        target_reduction=target,
        queries_path=DEMO / "queries.json",
    )

    unboosted_summary = run_eval_loop(merged, unboosted, DEMO / "queries.json")
    boosted_summary = run_eval_loop(merged, boosted, DEMO / "queries.json")

    assert boosted_summary.understanding_pct >= unboosted_summary.understanding_pct
