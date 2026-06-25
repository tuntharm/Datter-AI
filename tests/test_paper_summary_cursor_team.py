"""Tests for Cursor multi-model Paper Summary Team path."""

from __future__ import annotations

from pathlib import Path

from datter.agent import AnalysisAgent
from datter.eval.llm_judge import CURSOR_MODEL_SLUGS, ModelFamily
from datter.eval.paper_summary_team import (
    run_cursor_simulated_eval,
    save_cursor_exam_results,
    write_cursor_exam_prompts,
)

ROOT = Path(__file__).parent.parent
DEMO = ROOT / "demo_data"


def test_write_cursor_exam_prompts():
    agent = AnalysisAgent(scorer_mode="baseline", queries_path=DEMO / "queries.json")
    report = agent.run_from_folder(str(DEMO))
    from datter.eval.paper_summary_team import build_exam, corpus_text_from_chunks
    from datter.eval.llm_judge import get_model_roster

    full_text = corpus_text_from_chunks(report.chunks, {c.item_id for c in report.chunks})
    compressed_text = corpus_text_from_chunks(
        report.chunks, set(report.selection.datter_chunk_ids)
    )
    exam = build_exam(full_text, get_model_roster()[0], queries_path=DEMO / "queries.json", num_questions=4)
    prompts_dir = write_cursor_exam_prompts(DEMO, exam, compressed_text)
    assert prompts_dir.is_dir()
    for family in ModelFamily:
        slug = CURSOR_MODEL_SLUGS[family]
        assert (prompts_dir / f"{family.value}.md").is_file()
        assert (prompts_dir / f"{slug}.md").is_file()
        assert slug in (prompts_dir / f"{slug}.md").read_text()


def test_run_cursor_simulated_eval():
    agent = AnalysisAgent(scorer_mode="baseline", queries_path=DEMO / "queries.json")
    report = agent.run_from_folder(str(DEMO))
    result = run_cursor_simulated_eval(
        project_path=DEMO,
        queries_path=DEMO / "queries.json",
        chunks=report.chunks,
        scores=report.scores,
        selection=report.selection,
        quality_floor=0.50,
        num_questions=4,
        project_id="lab",
    )
    assert result.api_mode == "cursor_simulated"
    assert len(result.model_results) == 4
    path = save_cursor_exam_results(DEMO, result)
    assert path.name == "exam_results_cursor.json"
    assert "cursor_model_slugs" in path.read_text()
