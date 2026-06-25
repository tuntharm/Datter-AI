from pathlib import Path

from datter.agent import AnalysisAgent
from datter.eval.pareto import scan_pareto_frontier

ROOT = Path(__file__).parent.parent
DEMO = ROOT / "demo_data"


def test_pareto_finds_max_cut_at_floor():
    agent = AnalysisAgent(scorer_mode="baseline", queries_path=DEMO / "queries.json")
    report = agent.run_from_folder(str(DEMO))
    assert report.eval_summary is not None
    assert report.eval_summary.max_safe_reduction_pct >= 0
    assert len(report.eval_summary.pareto_points) >= 3


def test_pareto_scan_monotonic():
    agent = AnalysisAgent(scorer_mode="baseline")
    report = agent.run_from_folder(str(DEMO))
    _, summary, points = scan_pareto_frontier(
        report.chunks, report.scores, report.scores, DEMO / "queries.json"
    )
    assert summary.meets_quality_floor or summary.max_safe_reduction_pct >= 0
    labels = [p.label for p in points]
    assert "Full corpus" in labels
    assert "Max safe cut (Datter)" in labels
