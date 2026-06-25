"""Paper Summary Team — multi-model exam loop (CTO eval).

Compares full corpus text vs compressed export per model family:
examiner on FULL, examinee on COMPRESSED, same family scores answers.
Retries compression strategy until quality floor met (max 6 iterations).
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from pathlib import Path

import pandas as pd

from datter.eval.llm_judge import (
    ModelFamily,
    ModelSpec,
    cursor_slug_for,
    get_model_roster,
    has_llm_keys,
    llm_complete,
    llm_judge_answer,
)
from datter.eval.pareto import run_eval_at_quality_floor
from datter.eval.queries import EvalQuestion, load_queries
from datter.eval.relevance_boost import apply_query_relevance_boost
from datter.export import build_optimised_corpus
from datter.models import Chunk, ParetoPoint, SelectedCorpus
from datter.report import chunks_to_dataframe, merge_scores
from datter.selection import build_selection

logger = logging.getLogger(__name__)

OFFLINE_NOTE = (
    "API required for Paper Summary Team production run — using TF-IDF judge fallback."
)

EXAM_BUILD_PROMPT = """You are an examiner. From the FULL corpus below, write {n} exam questions
where the answer is definitely present in the text. Return JSON only:
{{"questions": [{{"id": "q1", "query": "...", "reference_answer": "...", "gold_hint": "key terms"}}]}}

CORPUS (truncated):
{corpus}"""

ANSWER_PROMPT = """Answer the QUERY using ONLY the COMPRESSED corpus below. Be concise (≤120 words).

QUERY: {query}

COMPRESSED CORPUS:
{corpus}"""


@dataclass
class ExamItem:
    question_id: str
    query: str
    reference_answer: str
    gold_hint: str = ""


@dataclass
class QuestionScore:
    question_id: str
    query: str
    reference_answer: str
    candidate_answer: str
    score: float
    missing: str = ""


@dataclass
class ModelExamResult:
    model_family: str
    api_id: str
    mean_score: float
    questions: list[QuestionScore] = field(default_factory=list)
    tokens_full: int = 0
    tokens_compressed: int = 0
    passed: bool = False


@dataclass
class PaperSummaryTeamResult:
    project_id: str
    quality_floor: float
    iterations_run: int
    passed: bool
    compression_pct: float
    min_score_across_models: float
    tokens_full: int
    tokens_compressed: int
    model_results: list[ModelExamResult] = field(default_factory=list)
    pareto_point: ParetoPoint | None = None
    api_mode: str = "offline"
    disclaimer: str = ""
    exam_corpus_dir: str = ""


def _estimate_tokens(text: str) -> int:
    return max(1, len(text.split()))


def corpus_text_from_chunks(chunks: list[Chunk], allowed_ids: set[str] | None = None) -> str:
    parts: list[str] = []
    for chunk in chunks:
        if allowed_ids is not None and chunk.item_id not in allowed_ids:
            continue
        text = chunk.text.strip()
        if text:
            parts.append(text)
    return "\n\n---\n\n".join(parts)


def _offline_reference_answer(query: str, full_text: str, gold_hint: str) -> str:
    from datter.eval.answer import synthesize_answer
    from datter.eval.retrieval import build_index, retrieve_top_k

    df = pd.DataFrame([{"item_id": f"c{i}", "text": t} for i, t in enumerate(full_text.split("\n\n---\n\n"))])
    if df.empty:
        df = pd.DataFrame([{"item_id": "c0", "text": full_text}])
    vectorizer, matrix = build_index(df)
    retrieved = retrieve_top_k(query, df, vectorizer, matrix, k=3)
    return synthesize_answer(query, retrieved) if not retrieved.empty else gold_hint or query


def build_exam(
    corpus_full_text: str,
    model: ModelSpec,
    queries_path: Path | None = None,
    num_questions: int = 6,
) -> list[ExamItem]:
    """FULL-context examiner generates questions + reference answers."""
    if queries_path and queries_path.is_file():
        config = load_queries(queries_path)
        items: list[ExamItem] = []
        for q in config.questions[:num_questions]:
            if has_llm_keys() and model.available:
                ref = _llm_reference_from_corpus(corpus_full_text, q, model)
            else:
                ref = _offline_reference_answer(q.query, corpus_full_text, q.gold_hint)
            items.append(
                ExamItem(
                    question_id=q.id,
                    query=q.query,
                    reference_answer=ref,
                    gold_hint=q.gold_hint,
                )
            )
        return items

    if has_llm_keys() and model.available:
        return _llm_build_exam(corpus_full_text, model, num_questions)

    return [
        ExamItem(
            question_id="q1",
            query="Summarise the main topics in this corpus.",
            reference_answer=_offline_reference_answer(
                "Summarise the main topics in this corpus.",
                corpus_full_text,
                "main topics summary",
            ),
            gold_hint="main topics summary",
        )
    ]


def _llm_reference_from_corpus(corpus: str, question: EvalQuestion, model: ModelSpec) -> str:
    prompt = ANSWER_PROMPT.format(query=question.query, corpus=corpus[:12000])
    try:
        return llm_complete(prompt, model)[:1200]
    except Exception:
        return _offline_reference_answer(question.query, corpus, question.gold_hint)


def _llm_build_exam(corpus: str, model: ModelSpec, n: int) -> list[ExamItem]:
    prompt = EXAM_BUILD_PROMPT.format(n=n, corpus=corpus[:12000])
    try:
        raw = llm_complete(prompt, model)
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start >= 0 and end > start:
            parsed = json.loads(raw[start:end])
            items: list[ExamItem] = []
            for i, q in enumerate(parsed.get("questions", [])[:n]):
                items.append(
                    ExamItem(
                        question_id=str(q.get("id", f"q{i+1}")),
                        query=str(q.get("query", "")),
                        reference_answer=str(q.get("reference_answer", "")),
                        gold_hint=str(q.get("gold_hint", "")),
                    )
                )
            if items:
                return items
    except Exception:
        pass
    return build_exam(corpus, model, queries_path=None, num_questions=n)


def answer_exam(
    corpus_compressed_text: str,
    questions: list[ExamItem],
    model: ModelSpec,
) -> list[str]:
    """COMPRESSED-context examinee answers from optimised corpus only."""
    answers: list[str] = []
    for q in questions:
        if has_llm_keys() and model.available:
            prompt = ANSWER_PROMPT.format(query=q.query, corpus=corpus_compressed_text[:12000])
            try:
                answers.append(llm_complete(prompt, model)[:1200])
                continue
            except Exception:
                pass
        answers.append(
            _offline_reference_answer(q.query, corpus_compressed_text, q.gold_hint)
        )
    return answers


def score_exam(
    questions: list[ExamItem],
    candidate_answers: list[str],
    model: ModelSpec,
) -> tuple[list[QuestionScore], float]:
    """FULL-context examiner (same family) scores compressed answers 0–100."""
    if not has_llm_keys():
        logger.warning(OFFLINE_NOTE)

    scored: list[QuestionScore] = []
    totals: list[float] = []
    for q, cand in zip(questions, candidate_answers):
        if has_llm_keys() and model.available:
            score, missing = llm_judge_answer(
                q.query, q.reference_answer, cand, q.gold_hint, model=model
            )
        else:
            from datter.eval.judge import judge_answer

            score, missing = judge_answer(q.reference_answer, cand, q.gold_hint)
        scored.append(
            QuestionScore(
                question_id=q.question_id,
                query=q.query,
                reference_answer=q.reference_answer[:500],
                candidate_answer=cand[:500],
                score=score,
                missing=missing,
            )
        )
        totals.append(score)
    aggregate = round(sum(totals) / len(totals), 1) if totals else 0.0
    return scored, aggregate


def regenerate_compressed(
    chunks: list[Chunk],
    scores: pd.DataFrame,
    queries_path: Path,
    iteration: int,
    base_reduction: float,
) -> SelectedCorpus:
    """Tighter keep / higher relevance boost / lower reduction step per retry."""
    items_df = chunks_to_dataframe(chunks)
    boost_weight = min(0.95, 0.55 + 0.10 * iteration)
    adj_reduction = max(0.10, base_reduction - 0.05 * iteration)
    boosted = apply_query_relevance_boost(
        scores, items_df, queries_path, boost_weight=boost_weight
    )
    return build_selection(
        chunks,
        boosted,
        target_reduction=adj_reduction,
        queries_path=None,
        items_df=items_df,
    )


def _export_exam_corpus(
    project_path: Path,
    full_text: str,
    compressed_text: str,
    iteration: int,
) -> Path:
    out_dir = project_path / "exam_corpus"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "full_corpus.txt").write_text(full_text, encoding="utf-8")
    (out_dir / f"compressed_iter_{iteration}.txt").write_text(compressed_text, encoding="utf-8")
    manifest = {
        "iteration": iteration,
        "full_tokens": _estimate_tokens(full_text),
        "compressed_tokens": _estimate_tokens(compressed_text),
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return out_dir


def _run_model_exams(
    full_text: str,
    compressed_text: str,
    roster: list[ModelSpec],
    queries_path: Path | None,
    quality_floor: float,
) -> list[ModelExamResult]:
    results: list[ModelExamResult] = []
    floor_pct = quality_floor * 100.0
    tokens_full = _estimate_tokens(full_text)
    tokens_compressed = _estimate_tokens(compressed_text)

    for model in roster:
        exam = build_exam(full_text, model, queries_path=queries_path)
        answers = answer_exam(compressed_text, exam, model)
        scored, aggregate = score_exam(exam, answers, model)
        results.append(
            ModelExamResult(
                model_family=model.family.value,
                api_id=model.api_id,
                mean_score=aggregate,
                questions=scored,
                tokens_full=tokens_full,
                tokens_compressed=tokens_compressed,
                passed=aggregate >= floor_pct,
            )
        )
    return results


def run_team_loop(
    project_path: Path,
    queries_path: Path,
    chunks: list[Chunk],
    scores: pd.DataFrame,
    selection: SelectedCorpus | None = None,
    quality_floor: float = 1.0,
    max_iterations: int = 6,
    project_id: str = "",
) -> PaperSummaryTeamResult:
    """Run multi-model exam loop with compression retry until floor met."""
    if selection is None:
        merged = merge_scores(chunks, scores)
        selection, _ = run_eval_at_quality_floor(chunks, merged, scores, queries_path)

    base_reduction = (
        1.0 - selection.datter_tokens / selection.full_tokens if selection.full_tokens else 0.50
    )
    roster = get_model_roster()
    current_selection = selection
    best_result: PaperSummaryTeamResult | None = None
    last_result: PaperSummaryTeamResult | None = None
    api_mode = "live" if has_llm_keys() else "offline"
    disclaimer = "" if api_mode == "live" else OFFLINE_NOTE

    for iteration in range(max_iterations):
        full_ids = {c.item_id for c in chunks}
        compressed_ids = set(current_selection.datter_chunk_ids)
        full_text = corpus_text_from_chunks(chunks, full_ids)
        compressed_text = corpus_text_from_chunks(chunks, compressed_ids)
        exam_dir = _export_exam_corpus(project_path, full_text, compressed_text, iteration)

        model_results = _run_model_exams(
            full_text, compressed_text, roster, queries_path, quality_floor
        )
        if not model_results:
            raise RuntimeError("Paper Summary Team roster produced no model results")

        min_score = min(r.mean_score for r in model_results)
        compression_pct = round(
            (1.0 - current_selection.datter_tokens / current_selection.full_tokens) * 100, 1
            if current_selection.full_tokens
            else 0.0,
        )
        passed = min_score >= quality_floor * 100.0

        pareto = ParetoPoint(
            token_reduction_pct=compression_pct,
            understanding_pct=round(min_score, 1),
            label=f"Paper Summary Team iter {iteration}",
        )

        result = PaperSummaryTeamResult(
            project_id=project_id or project_path.name,
            quality_floor=quality_floor,
            iterations_run=iteration + 1,
            passed=passed,
            compression_pct=compression_pct,
            min_score_across_models=min_score,
            tokens_full=current_selection.full_tokens,
            tokens_compressed=current_selection.datter_tokens,
            model_results=model_results,
            pareto_point=pareto,
            api_mode=api_mode,
            disclaimer=disclaimer,
            exam_corpus_dir=str(exam_dir),
        )

        last_result = result

        if best_result is None or min_score > best_result.min_score_across_models:
            best_result = result

        if passed:
            break

        current_selection = regenerate_compressed(
            chunks, scores, queries_path, iteration + 1, base_reduction
        )

    assert last_result is not None
    if last_result.passed:
        return last_result
    assert best_result is not None
    best_result.iterations_run = last_result.iterations_run
    best_result.passed = False
    return best_result


def result_to_dict(result: PaperSummaryTeamResult) -> dict:
    """JSON-serialisable summary for exam_results.json."""
    data = asdict(result)
    if result.pareto_point:
        data["pareto_point"] = asdict(result.pareto_point)
    return data


def save_exam_results(project_path: Path, result: PaperSummaryTeamResult) -> Path:
    out = project_path / "exam_results.json"
    out.write_text(json.dumps(result_to_dict(result), indent=2), encoding="utf-8")
    return out


CURSOR_EXAM_PROMPT = """# Paper Summary Team — {cursor_slug}

**Model slot:** `{family}` · **Cursor slug:** `{cursor_slug}`

You are the **examinee** in the Paper Summary Team loop. Answer each question using
**only** the COMPRESSED corpus below (≤120 words per answer). An examiner built
reference answers from the FULL corpus; your answers will be scored against them.

## COMPRESSED CORPUS

```
{compressed}
```

## Questions

{questions_block}

---

## Scoring template (for examiner / orchestrator)

Return JSON after you answer:

```json
{{"answers": [{{"id": "q1", "answer": "..."}}, ...]}}
```
"""


def export_cursor_corpus_aliases(
    exam_dir: Path,
    full_text: str,
    compressed_text: str,
) -> None:
    """Write full.txt / compressed.txt aliases alongside iter exports."""
    exam_dir.mkdir(parents=True, exist_ok=True)
    (exam_dir / "full.txt").write_text(full_text, encoding="utf-8")
    (exam_dir / "compressed.txt").write_text(compressed_text, encoding="utf-8")


def build_exam_prompt_markdown(
    model: ModelSpec,
    exam: list[ExamItem],
    compressed_text: str,
) -> str:
    cursor_slug = cursor_slug_for(model.family)
    blocks: list[str] = []
    for i, item in enumerate(exam, 1):
        blocks.append(
            f"### {item.question_id} ({i}/{len(exam)})\n\n"
            f"**Query:** {item.query}\n\n"
            f"**Reference (FULL corpus — do not peek when answering):** "
            f"{item.reference_answer[:400]}{'…' if len(item.reference_answer) > 400 else ''}\n\n"
            f"**Your answer (COMPRESSED only):**\n"
        )
    return CURSOR_EXAM_PROMPT.format(
        cursor_slug=cursor_slug,
        family=model.family.value,
        compressed=compressed_text[:16000],
        questions_block="\n".join(blocks),
    )


def write_cursor_exam_prompts(
    project_path: Path,
    exam: list[ExamItem],
    compressed_text: str,
    roster: list[ModelSpec] | None = None,
) -> Path:
    """Emit exam_prompts/<family>.md and exam_prompts/<cursor-slug>.md per model."""
    roster = roster or get_model_roster()
    prompts_dir = project_path / "exam_prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    for model in roster:
        content = build_exam_prompt_markdown(model, exam, compressed_text)
        (prompts_dir / f"{model.family.value}.md").write_text(content, encoding="utf-8")
        (prompts_dir / f"{cursor_slug_for(model.family)}.md").write_text(
            content, encoding="utf-8"
        )
    return prompts_dir


def run_cursor_simulated_eval(
    project_path: Path,
    queries_path: Path,
    chunks: list[Chunk],
    scores: pd.DataFrame,
    selection: SelectedCorpus | None = None,
    quality_floor: float = 0.90,
    num_questions: int = 4,
    project_id: str = "",
) -> PaperSummaryTeamResult:
    """Offline multi-slot eval tagged per Cursor model family (orchestrator-simulated)."""
    if selection is None:
        merged = merge_scores(chunks, scores)
        selection, _ = run_eval_at_quality_floor(chunks, merged, scores, queries_path)

    full_ids = {c.item_id for c in chunks}
    compressed_ids = set(selection.datter_chunk_ids)
    full_text = corpus_text_from_chunks(chunks, full_ids)
    compressed_text = corpus_text_from_chunks(chunks, compressed_ids)
    exam_dir = _export_exam_corpus(project_path, full_text, compressed_text, 0)
    export_cursor_corpus_aliases(exam_dir, full_text, compressed_text)

    roster = get_model_roster()
    shared_exam = build_exam(
        full_text, roster[0], queries_path=queries_path, num_questions=num_questions
    )
    write_cursor_exam_prompts(project_path, shared_exam, compressed_text, roster)

    model_results: list[ModelExamResult] = []
    for model in roster:
        answers = answer_exam(compressed_text, shared_exam, model)
        scored, aggregate = score_exam(shared_exam, answers, model)
        model_results.append(
            ModelExamResult(
                model_family=model.family.value,
                api_id=cursor_slug_for(model.family),
                mean_score=aggregate,
                questions=scored,
                tokens_full=_estimate_tokens(full_text),
                tokens_compressed=_estimate_tokens(compressed_text),
                passed=aggregate >= quality_floor * 100.0,
            )
        )

    min_score = min(r.mean_score for r in model_results)
    compression_pct = round(
        (1.0 - selection.datter_tokens / selection.full_tokens) * 100, 1
        if selection.full_tokens
        else 0.0,
    )
    return PaperSummaryTeamResult(
        project_id=project_id or project_path.name,
        quality_floor=quality_floor,
        iterations_run=1,
        passed=min_score >= quality_floor * 100.0,
        compression_pct=compression_pct,
        min_score_across_models=min_score,
        tokens_full=selection.full_tokens,
        tokens_compressed=selection.datter_tokens,
        model_results=model_results,
        pareto_point=ParetoPoint(
            token_reduction_pct=compression_pct,
            understanding_pct=round(min_score, 1),
            label="Cursor multi-model (simulated)",
        ),
        api_mode="cursor_simulated",
        disclaimer=(
            "orchestrator-simulated; for true multi-model run set API keys or "
            "use Cursor chat per exam_prompts/*.md"
        ),
        exam_corpus_dir=str(exam_dir),
    )


def save_cursor_exam_results(project_path: Path, result: PaperSummaryTeamResult) -> Path:
    out = project_path / "exam_results_cursor.json"
    data = result_to_dict(result)
    data["cursor_model_slugs"] = {
        f.value: cursor_slug_for(f) for f in ModelFamily
    }
    out.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return out
