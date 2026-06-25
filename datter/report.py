from __future__ import annotations

import json

import pandas as pd

from datter.models import AnalysisReport, Chunk, EvalSummary, SelectedCorpus
from datter.token_cost import (
    DEFAULT_EMBEDDING_COST_PER_M,
    DEFAULT_TOKEN_COST_PER_M,
    estimate_embedding_cost,
    estimate_token_cost,
)


def chunks_to_dataframe(chunks: list[Chunk]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "item_id": c.item_id,
                "doc_id": c.doc_id,
                "filename": c.filename,
                "text": c.text,
                "token_count": c.token_count,
                "max_similarity": c.max_similarity,
                "is_exact_duplicate": c.is_exact_duplicate,
                "is_canonical": c.is_canonical,
                "exact_dup_group": c.exact_dup_group,
                "near_dup_group": c.near_dup_group,
            }
            for c in chunks
        ]
    )


def merge_scores(chunks: list[Chunk], scores: pd.DataFrame) -> pd.DataFrame:
    base = chunks_to_dataframe(chunks)
    merged = base.merge(scores, on="item_id", how="left")
    merged["text_preview"] = merged["text"].str.slice(0, 200)
    return merged


def compute_avoidable_tokens(merged: pd.DataFrame) -> int:
    avoidable = 0
    for _, row in merged.iterrows():
        action = row.get("recommended_action", "review")
        tokens = int(row.get("token_count", 0))
        if action == "drop":
            avoidable += tokens
        elif action == "compress":
            avoidable += int(tokens * 0.5)
    return avoidable


def build_report(
    documents,
    chunks: list[Chunk],
    scores: pd.DataFrame,
    agent_log,
    scorer_name: str,
    scorer_loaded: bool,
    scorer_status: str,
    token_cost_per_m: float = DEFAULT_TOKEN_COST_PER_M,
    embedding_cost_per_m: float = DEFAULT_EMBEDDING_COST_PER_M,
    project_id: str = "",
    project_name: str = "",
    selection: SelectedCorpus | None = None,
    eval_summary: EvalSummary | None = None,
    optimised_corpus_tokens: int = 0,
) -> AnalysisReport:
    merged = merge_scores(chunks, scores)
    total_tokens = int(merged["token_count"].sum()) if not merged.empty else 0
    token_cost = estimate_token_cost(total_tokens, token_cost_per_m)
    embedding_cost = estimate_embedding_cost(total_tokens, embedding_cost_per_m)
    avoidable_tokens = compute_avoidable_tokens(merged)
    avoidable_cost = estimate_token_cost(avoidable_tokens, token_cost_per_m) + estimate_embedding_cost(
        avoidable_tokens, embedding_cost_per_m
    )
    pct_removable = (avoidable_tokens / total_tokens * 100) if total_tokens else 0.0

    from datter.dedup import duplicate_stats

    exact_pct, near_pct = duplicate_stats(chunks)

    rec_counts = (
        merged["recommended_action"].value_counts().to_dict()
        if "recommended_action" in merged.columns and not merged.empty
        else {}
    )

    top_useful = (
        merged.sort_values("usefulness_score", ascending=False).head(10)
        if not merged.empty
        else merged
    )
    most_redundant = (
        merged.sort_values("redundancy_score", ascending=False).head(10)
        if not merged.empty
        else merged
    )

    return AnalysisReport(
        documents=documents,
        chunks=chunks,
        scores=merged,
        total_tokens=total_tokens,
        total_documents=len(documents),
        total_chunks=len(chunks),
        token_cost_usd=token_cost,
        embedding_cost_usd=embedding_cost,
        total_cost_usd=token_cost + embedding_cost,
        avoidable_tokens=avoidable_tokens,
        avoidable_cost_usd=avoidable_cost,
        pct_removable=pct_removable,
        exact_dup_pct=exact_pct * 100,
        near_dup_pct=near_pct * 100,
        recommendation_counts=rec_counts,
        top_useful=top_useful,
        most_redundant=most_redundant,
        agent_log=agent_log,
        scorer_name=scorer_name,
        scorer_loaded=scorer_loaded,
        scorer_status=scorer_status,
        project_id=project_id,
        project_name=project_name,
        selection=selection,
        eval_summary=eval_summary,
        optimised_corpus_tokens=optimised_corpus_tokens,
    )


def report_to_markdown(report: AnalysisReport) -> str:
    lines = [
        "# Datter AI — Usefulness Report",
        "",
        f"**Scorer:** {report.scorer_name} ({report.scorer_status})",
        "",
        "## Summary",
        f"- Documents analysed: **{report.total_documents}**",
        f"- Chunks analysed: **{report.total_chunks}**",
        f"- Total tokens: **{report.total_tokens:,}**",
        f"- Estimated token cost: **${report.token_cost_usd:.4f}**",
        f"- Estimated embedding cost: **${report.embedding_cost_usd:.4f}**",
        f"- Avoidable tokens: **{report.avoidable_tokens:,}** ({report.pct_removable:.1f}%)",
        f"- Projected savings: **${report.avoidable_cost_usd:.4f}**",
        f"- Exact duplicate chunks: **{report.exact_dup_pct:.1f}%**",
        f"- Near-duplicate chunks: **{report.near_dup_pct:.1f}%**",
        "",
        "## Recommendations",
    ]
    for action, count in sorted(report.recommendation_counts.items()):
        lines.append(f"- {action}: {count}")

    lines.extend(["", "## Agent Run Log", ""])
    for entry in report.agent_log:
        lines.append(f"- [{entry.timestamp.strftime('%H:%M:%S')}] **{entry.agent}** ({entry.status}): {entry.message}")

    return "\n".join(lines)


def report_to_json(report: AnalysisReport) -> str:
    payload = {
        "summary": {
            "total_documents": report.total_documents,
            "total_chunks": report.total_chunks,
            "total_tokens": report.total_tokens,
            "token_cost_usd": report.token_cost_usd,
            "embedding_cost_usd": report.embedding_cost_usd,
            "avoidable_tokens": report.avoidable_tokens,
            "avoidable_cost_usd": report.avoidable_cost_usd,
            "pct_removable": report.pct_removable,
            "exact_dup_pct": report.exact_dup_pct,
            "near_dup_pct": report.near_dup_pct,
            "scorer_name": report.scorer_name,
            "scorer_status": report.scorer_status,
        },
        "recommendation_counts": report.recommendation_counts,
        "chunks": report.scores.to_dict(orient="records"),
        "agent_log": [
            {
                "agent": e.agent,
                "status": e.status,
                "message": e.message,
                "metrics": e.metrics,
                "timestamp": e.timestamp.isoformat(),
            }
            for e in report.agent_log
        ],
    }
    return json.dumps(payload, indent=2)
