from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Union

from datter.chunking import chunk_documents
from datter.dedup import deduplicate_chunks
from datter.eval.cache import load_eval_cache, save_eval_cache
from datter.eval.pareto import run_eval_at_quality_floor
from datter.export import build_optimised_corpus
from datter.ingest import ingest_folder, ingest_uploads
from datter.models import AgentLogEntry, AnalysisReport, ScorerConfig
from datter.report import build_report, chunks_to_dataframe, merge_scores
from datter.scorers import get_scorer
from datter.selection import build_selection
from datter.token_cost import DEFAULT_EMBEDDING_COST_PER_M, DEFAULT_TOKEN_COST_PER_M

StreamEvent = Union[list[AgentLogEntry], AnalysisReport]


class AnalysisAgent:
    def __init__(
        self,
        scorer_mode: str = "baseline",
        scorer_config: ScorerConfig | None = None,
        token_cost_per_m: float = DEFAULT_TOKEN_COST_PER_M,
        embedding_cost_per_m: float = DEFAULT_EMBEDDING_COST_PER_M,
        project_id: str = "",
        project_name: str = "",
        queries_path: Path | None = None,
        target_token_reduction: float = 0.50,
        eval_cache_path: Path | None = None,
    ):
        self.scorer_mode = scorer_mode
        self.scorer_config = scorer_config or ScorerConfig()
        self.token_cost_per_m = token_cost_per_m
        self.embedding_cost_per_m = embedding_cost_per_m
        self.project_id = project_id
        self.project_name = project_name
        self.queries_path = queries_path
        self.target_token_reduction = target_token_reduction
        self.eval_cache_path = eval_cache_path

    def _record(self, agent: str, status: str, message: str, metrics: dict | None = None) -> None:
        self.log.append(
            AgentLogEntry(
                agent=agent,
                status=status,
                message=message,
                metrics=metrics or {},
            )
        )

    def stream_from_folder(self, folder_path: str) -> Iterator[StreamEvent]:
        self.log = []
        self._record("IngestAgent", "started", f"Scanning folder: {folder_path}")
        documents = ingest_folder(folder_path)
        self._record(
            "IngestAgent",
            "completed",
            f"Ingested {len(documents)} documents",
            {"documents": len(documents)},
        )
        yield self.log.copy()
        yield from self._stream_pipeline(documents)

    def stream_from_uploads(self, uploads: list) -> Iterator[StreamEvent]:
        self.log = []
        self._record("IngestAgent", "started", "Processing uploaded files")
        documents = ingest_uploads(uploads)
        self._record(
            "IngestAgent",
            "completed",
            f"Ingested {len(documents)} documents",
            {"documents": len(documents)},
        )
        yield self.log.copy()
        yield from self._stream_pipeline(documents)

    def run_from_folder(self, folder_path: str) -> AnalysisReport:
        report: AnalysisReport | None = None
        for event in self.stream_from_folder(folder_path):
            if isinstance(event, AnalysisReport):
                report = event
        if report is None:
            raise RuntimeError("Pipeline did not produce a report")
        return report

    def run_from_uploads(self, uploads: list) -> AnalysisReport:
        report: AnalysisReport | None = None
        for event in self.stream_from_uploads(uploads):
            if isinstance(event, AnalysisReport):
                report = event
        if report is None:
            raise RuntimeError("Pipeline did not produce a report")
        return report

    def _stream_pipeline(self, documents) -> Iterator[StreamEvent]:
        self._record("ChunkAgent", "started", "Splitting documents into token-aware chunks")
        chunks = chunk_documents(documents)
        total_tokens = sum(c.token_count for c in chunks)
        self._record(
            "ChunkAgent",
            "completed",
            f"Created {len(chunks)} chunks ({total_tokens:,} tokens)",
            {"chunks": len(chunks), "tokens": total_tokens},
        )
        yield self.log.copy()

        self._record("DedupAgent", "started", "Detecting exact and near-duplicates")
        deduplicate_chunks(chunks)
        exact = sum(1 for c in chunks if c.is_exact_duplicate)
        near = sum(1 for c in chunks if c.near_dup_group)
        self._record(
            "DedupAgent",
            "completed",
            f"Found {exact} exact-dup and {near} near-dup chunks",
            {"exact_duplicates": exact, "near_duplicates": near},
        )
        yield self.log.copy()

        scorer = get_scorer(self.scorer_mode, self.scorer_config)
        self._record("ScoreAgent", "started", f"Scoring with {scorer.name} scorer")
        items_df = chunks_to_dataframe(chunks)
        scorer.fit(items_df)
        scores = scorer.score(items_df)

        if not scorer.is_loaded and self.scorer_mode in {"adisorn", "hybrid"}:
            self._record("ScoreAgent", "warning", scorer.status_message)
        self._record(
            "ScoreAgent",
            "completed",
            f"Scored {len(scores)} chunks",
            {"scorer": scorer.name, "loaded": scorer.is_loaded},
        )
        yield self.log.copy()

        merged = merge_scores(chunks, scores)
        queries = self.queries_path if self.queries_path and self.queries_path.is_file() else None

        eval_summary = None
        selection = build_selection(
            chunks,
            scores,
            target_reduction=self.target_token_reduction,
            queries_path=queries,
            items_df=items_df,
        )

        if self.queries_path and self.queries_path.is_file():
            if self.eval_cache_path and self.eval_cache_path.is_file():
                eval_summary = load_eval_cache(self.eval_cache_path)
                if eval_summary and eval_summary.max_safe_reduction_pct == 0:
                    eval_summary = None
                cut = (
                    eval_summary.max_safe_reduction_pct / 100.0
                    if eval_summary.max_safe_reduction_pct
                    else eval_summary.actual_reduction or self.target_token_reduction
                )
                selection = build_selection(
                    chunks, scores, target_reduction=cut, queries_path=queries, items_df=items_df
                )
                self._record(
                    "SelectAgent",
                    "completed",
                    f"Loaded cached max cut: {cut:.1%} ({selection.datter_tokens:,} tokens kept)",
                    {"cached": True},
                )
            else:
                self._record(
                    "SelectAgent",
                    "started",
                    "Finding max token cut at quality floor (Pareto scan)",
                )
                selection, eval_summary = run_eval_at_quality_floor(
                    chunks, merged, scores, self.queries_path
                )
                actual_cut = (
                    1.0 - selection.datter_tokens / selection.full_tokens if selection.full_tokens else 0.0
                )
                self._record(
                    "SelectAgent",
                    "completed",
                    f"Max safe cut: {actual_cut:.1%} ({selection.datter_tokens:,} tokens kept)",
                    {
                        "max_safe_reduction_pct": eval_summary.max_safe_reduction_pct,
                        "meets_quality_floor": eval_summary.meets_quality_floor,
                    },
                )
        else:
            self._record(
                "SelectAgent",
                "completed",
                f"Structural cut: {selection.datter_tokens:,} tokens",
                {"full_tokens": selection.full_tokens},
            )
        yield self.log.copy()

        if self.queries_path and self.queries_path.is_file():
            self._record("EvalAgent", "started", "Proof at quality floor")
            if eval_summary and self.eval_cache_path:
                save_eval_cache(self.eval_cache_path, eval_summary)
            if eval_summary:
                self._record(
                    "EvalAgent",
                    "completed",
                    f"Understanding {eval_summary.understanding_pct:.1f}% at {eval_summary.max_safe_reduction_pct:.1f}% max safe cut",
                    {
                        "understanding_pct": eval_summary.understanding_pct,
                        "meets_quality_floor": eval_summary.meets_quality_floor,
                    },
                )
            yield self.log.copy()
        else:
            self._record("EvalAgent", "warning", "No queries.json — skipping proof loop")
            yield self.log.copy()

        optimised = build_optimised_corpus(chunks, scores, selection.datter_chunk_ids)

        self._record("ReportAgent", "started", "Building usefulness report")
        report = build_report(
            documents=documents,
            chunks=chunks,
            scores=scores,
            agent_log=self.log.copy(),
            scorer_name=scorer.name,
            scorer_loaded=scorer.is_loaded,
            scorer_status=scorer.status_message,
            token_cost_per_m=self.token_cost_per_m,
            embedding_cost_per_m=self.embedding_cost_per_m,
            project_id=self.project_id,
            project_name=self.project_name,
            selection=selection,
            eval_summary=eval_summary,
            optimised_corpus_tokens=optimised.total_tokens,
        )
        self._record(
            "ReportAgent",
            "completed",
            f"Report ready — {report.pct_removable:.1f}% avoidable, {eval_summary.understanding_pct if eval_summary else 'N/A'}% understanding",
            {
                "avoidable_tokens": report.avoidable_tokens,
                "pct_removable": round(report.pct_removable, 2),
            },
        )
        report.agent_log = self.log.copy()
        yield self.log.copy()
        yield report
