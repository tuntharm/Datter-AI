from __future__ import annotations

from pathlib import Path

import pandas as pd

from datter.eval.answer import synthesize_answer
from datter.eval.judge import judge_answer
from datter.eval.queries import EvalConfig, load_queries
from datter.eval.retrieval import build_index, retrieve_top_k
from datter.models import EvalQuestionResult, EvalSummary, ParetoPoint, SelectedCorpus

DISCLAIMER = (
    "Building demo — offline understanding proxy (TF-IDF retrieval + token overlap). "
    "Production claims use developed eval harness."
)


def run_eval_loop(
    merged_scores: pd.DataFrame,
    selection: SelectedCorpus,
    queries_path: Path,
    max_iterations: int = 6,
) -> EvalSummary:
    config = load_queries(queries_path)
    if merged_scores.empty or not config.questions:
        return EvalSummary(disclaimer=DISCLAIMER)

    vectorizer, matrix = build_index(merged_scores)
    full_ids = set(merged_scores["item_id"].tolist())
    datter_ids = set(selection.datter_chunk_ids)
    random_ids = set(selection.random_chunk_ids)

    questions: list[EvalQuestionResult] = []
    datter_scores: list[float] = []
    random_scores: list[float] = []

    for q in config.questions:
        full_ret = retrieve_top_k(q.query, merged_scores, vectorizer, matrix, k=3, allowed_ids=full_ids)
        datter_ret = retrieve_top_k(q.query, merged_scores, vectorizer, matrix, k=3, allowed_ids=datter_ids)
        random_ret = retrieve_top_k(q.query, merged_scores, vectorizer, matrix, k=3, allowed_ids=random_ids)

        full_answer = synthesize_answer(q.query, full_ret)
        datter_answer = synthesize_answer(q.query, datter_ret)
        random_answer = synthesize_answer(q.query, random_ret)

        d_score, d_missing = judge_answer(full_answer, datter_answer, q.gold_hint)
        r_score, r_missing = judge_answer(full_answer, random_answer, q.gold_hint)

        datter_scores.append(d_score)
        random_scores.append(r_score)

        questions.append(
            EvalQuestionResult(
                question_id=q.id,
                query=q.query,
                full_answer=full_answer[:500],
                datter_answer=datter_answer[:500],
                random_answer=random_answer[:500],
                datter_score=d_score,
                random_score=r_score,
                missing_points=d_missing,
            )
        )

    mean_datter = sum(datter_scores) / len(datter_scores) if datter_scores else 0.0
    mean_random = sum(random_scores) / len(random_scores) if random_scores else 0.0
    actual_reduction = (
        1.0 - selection.datter_tokens / selection.full_tokens if selection.full_tokens else 0.0
    )

    pareto = [
        ParetoPoint(token_reduction_pct=0.0, understanding_pct=100.0, label="Full corpus"),
        ParetoPoint(
            token_reduction_pct=round(actual_reduction * 100, 1),
            understanding_pct=round(mean_datter, 1),
            label="Datter cut",
        ),
        ParetoPoint(
            token_reduction_pct=round(actual_reduction * 100, 1),
            understanding_pct=round(mean_random, 1),
            label="Random cut",
        ),
    ]

    return EvalSummary(
        mean_full_score=100.0,
        mean_datter_score=round(mean_datter, 1),
        mean_random_score=round(mean_random, 1),
        understanding_pct=round(mean_datter, 1),
        random_understanding_pct=round(mean_random, 1),
        quality_floor=config.quality_floor,
        target_reduction=config.target_token_reduction,
        actual_reduction=round(actual_reduction, 4),
        questions=questions,
        pareto_points=pareto,
        disclaimer=DISCLAIMER,
    )
