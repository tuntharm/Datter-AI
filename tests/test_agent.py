from pathlib import Path

from datter.agent import AnalysisAgent

ROOT = Path(__file__).parent.parent
DEMO = ROOT / "demo_data"


def test_demo_pipeline_runs():
    agent = AnalysisAgent(scorer_mode="baseline")
    report = agent.run_from_folder(str(DEMO))
    assert report.total_documents >= 5
    assert report.total_chunks > 0
    assert report.total_tokens > 0
    assert report.avoidable_tokens > 0
    assert len(report.agent_log) >= 5
