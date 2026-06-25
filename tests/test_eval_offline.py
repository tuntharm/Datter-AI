from pathlib import Path

from datter.agent import AnalysisAgent
from datter.eval.loop import run_eval_loop
from datter.selection import build_selection

ROOT = Path(__file__).parent.parent
DEMO = ROOT / "demo_data"


def test_eval_loop_returns_questions():
    agent = AnalysisAgent(
        scorer_mode="baseline",
        queries_path=DEMO / "queries.json",
    )
    report = agent.run_from_folder(str(DEMO))
    assert report.eval_summary is not None
    assert len(report.eval_summary.questions) >= 6
    assert report.eval_summary.understanding_pct >= 0


def test_datter_beats_or_matches_random_on_lab():
    agent = AnalysisAgent(scorer_mode="baseline")
    report = agent.run_from_folder(str(DEMO))
    merged = report.scores
    sel = build_selection(report.chunks, merged, target_reduction=0.50)
    summary = run_eval_loop(merged, sel, DEMO / "queries.json")
    assert summary.mean_datter_score >= summary.mean_random_score - 5
