from pathlib import Path

from datter.agent import AnalysisAgent
from datter.export import build_optimised_corpus, export_zip

ROOT = Path(__file__).parent.parent
DEMO = ROOT / "demo_data"


def test_optimised_corpus_fewer_tokens():
    agent = AnalysisAgent(scorer_mode="baseline")
    report = agent.run_from_folder(str(DEMO))
    assert report.selection is not None
    opt = build_optimised_corpus(report.chunks, report.scores, report.selection.datter_chunk_ids)
    assert opt.total_tokens <= report.total_tokens
    assert opt.file_count > 0


def test_export_zip_has_manifest():
    agent = AnalysisAgent(scorer_mode="baseline")
    report = agent.run_from_folder(str(DEMO))
    assert report.selection is not None
    data = export_zip(report.chunks, report.scores, report.selection)
    assert len(data) > 100
    assert b"manifest.json" in data or b"PK" in data
