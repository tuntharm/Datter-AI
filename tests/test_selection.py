from pathlib import Path

import pandas as pd

from datter.agent import AnalysisAgent
from datter.selection import build_selection

ROOT = Path(__file__).parent.parent
DEMO = ROOT / "demo_data"


def test_datter_cut_reduces_tokens():
    agent = AnalysisAgent(scorer_mode="baseline")
    report = agent.run_from_folder(str(DEMO))
    sel = build_selection(report.chunks, report.scores, target_reduction=0.50)
    assert sel.datter_tokens < sel.full_tokens
    assert sel.datter_tokens > 0


def test_random_matches_datter_budget():
    agent = AnalysisAgent(scorer_mode="baseline")
    report = agent.run_from_folder(str(DEMO))
    sel = build_selection(report.chunks, report.scores, target_reduction=0.50)
    assert abs(sel.random_tokens - sel.datter_tokens) <= max(50, sel.datter_tokens * 0.2)
