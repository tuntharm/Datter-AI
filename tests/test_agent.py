from pathlib import Path

from datter.agent import AnalysisAgent
from datter.project import get_project, match_upload_to_project

ROOT = Path(__file__).parent.parent
DEMO = ROOT / "demo_data"


class _UploadStub:
    def __init__(self, name: str, data: bytes):
        self.name = name
        self.size = len(data)
        self._data = data

    def getvalue(self) -> bytes:
        return self._data


def test_demo_pipeline_runs():
    agent = AnalysisAgent(scorer_mode="baseline")
    report = agent.run_from_folder(str(DEMO))
    assert report.total_documents >= 5
    assert report.total_chunks > 0
    assert report.total_tokens > 0
    assert report.avoidable_tokens > 0
    assert len(report.agent_log) >= 5


def test_government_upload_wires_eval():
    gov = get_project("government", ROOT)
    if gov is None:
        return
    pdf_path = gov.corpus_path / gov.primary_pdf
    if not pdf_path.is_file():
        return

    upload = _UploadStub(gov.primary_pdf, pdf_path.read_bytes())
    matched = match_upload_to_project([upload], ROOT)
    assert matched is not None
    assert matched.id == "government"

    agent = AnalysisAgent(
        scorer_mode="baseline",
        project_id=matched.id,
        project_name=matched.name,
        queries_path=matched.queries_path,
        target_token_reduction=matched.target_token_reduction,
        eval_cache_path=matched.corpus_path / "eval_cache.json",
    )
    report = agent.run_from_uploads([upload])

    assert report.eval_summary is not None
    assert report.eval_summary.understanding_pct >= 85.0
    assert report.eval_summary.max_safe_reduction_pct >= 45.0
    assert report.eval_summary.meets_quality_floor
