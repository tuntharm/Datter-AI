"""Tests for Paper Summary Team multi-model exam loop (offline mock path)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from datter.agent import AnalysisAgent
from datter.eval.llm_judge import ModelFamily, ModelSpec
from datter.eval.paper_summary_team import (
    ExamItem,
    answer_exam,
    build_exam,
    run_team_loop,
    save_exam_results,
    score_exam,
)

ROOT = Path(__file__).parent.parent
DEMO = ROOT / "demo_data"


def _mock_model() -> ModelSpec:
    return ModelSpec(
        family=ModelFamily.GPT55,
        provider="openai",
        api_id="gpt-4o",
        available=False,
    )


def test_build_exam_uses_queries_json():
    exam = build_exam("full corpus text here", _mock_model(), queries_path=DEMO / "queries.json")
    assert len(exam) >= 6
    assert all(e.reference_answer for e in exam)


def test_answer_exam_offline():
    questions = [
        ExamItem("q1", "What is X?", "X is important.", "X important"),
    ]
    answers = answer_exam("compressed corpus about X", questions, _mock_model())
    assert len(answers) == 1
    assert isinstance(answers[0], str)


def test_score_exam_offline():
    questions = [
        ExamItem("q1", "What is X?", "X is important for research.", "X research"),
    ]
    scored, aggregate = score_exam(questions, ["X is important for research."], _mock_model())
    assert len(scored) == 1
    assert aggregate >= 0


def test_retry_triggers_on_low_score():
    agent = AnalysisAgent(scorer_mode="baseline", queries_path=DEMO / "queries.json")
    report = agent.run_from_folder(str(DEMO))

    call_count = {"n": 0}
    original = score_exam

    def flaky_score(questions, answers, model):
        call_count["n"] += 1
        if call_count["n"] <= 2:
            return original(questions, answers, model)[0], 50.0
        return original(questions, answers, model)

    with patch("datter.eval.paper_summary_team.score_exam", side_effect=flaky_score):
        result = run_team_loop(
            project_path=DEMO,
            queries_path=DEMO / "queries.json",
            chunks=report.chunks,
            scores=report.scores,
            selection=report.selection,
            quality_floor=1.0,
            max_iterations=6,
            project_id="lab",
        )

    assert result.iterations_run >= 2
    assert (DEMO / "exam_corpus" / "full_corpus.txt").is_file()


def test_save_exam_results_json():
    agent = AnalysisAgent(scorer_mode="baseline", queries_path=DEMO / "queries.json")
    report = agent.run_from_folder(str(DEMO))
    result = run_team_loop(
        project_path=DEMO,
        queries_path=DEMO / "queries.json",
        chunks=report.chunks,
        scores=report.scores,
        selection=report.selection,
        quality_floor=0.50,
        max_iterations=1,
        project_id="lab",
    )
    path = save_exam_results(DEMO, result)
    assert path.is_file()
    assert "model_results" in path.read_text()
