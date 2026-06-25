from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    import pandas as pd

InputType = Literal["text", "embedding", "feature_vector", "time_series"]
DeviceType = Literal["cpu", "cuda", "mps"]
ScorerMode = Literal["baseline", "adisorn", "hybrid"]
ActionType = Literal["keep", "drop", "compress", "review"]


@dataclass
class Document:
    doc_id: str
    filename: str
    extension: str
    source: str
    raw_text: str
    char_count: int


@dataclass
class Chunk:
    item_id: str
    doc_id: str
    filename: str
    text: str
    chunk_index: int
    token_count: int = 0
    max_similarity: float = 0.0
    is_exact_duplicate: bool = False
    is_canonical: bool = True
    exact_dup_group: str | None = None
    near_dup_group: str | None = None


@dataclass
class ScorerConfig:
    model_path: str = "models/adisorn"
    input_type: InputType = "text"
    device: DeviceType = "cpu"
    batch_size: int = 32
    baseline_weight: float = 0.5
    research_weight: float = 0.5


@dataclass
class AgentLogEntry:
    agent: str
    status: str
    message: str
    metrics: dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ParetoPoint:
    token_reduction_pct: float
    understanding_pct: float
    label: str


@dataclass
class EvalQuestionResult:
    question_id: str
    query: str
    full_answer: str
    datter_answer: str
    random_answer: str
    datter_score: float
    random_score: float
    missing_points: str = ""


@dataclass
class EvalSummary:
    mean_full_score: float = 100.0
    mean_datter_score: float = 0.0
    mean_random_score: float = 0.0
    understanding_pct: float = 0.0
    random_understanding_pct: float = 0.0
    quality_floor: float = 0.90
    target_reduction: float = 0.50
    actual_reduction: float = 0.0
    max_safe_reduction_pct: float = 0.0
    meets_quality_floor: bool = False
    questions: list[EvalQuestionResult] = field(default_factory=list)
    pareto_points: list[ParetoPoint] = field(default_factory=list)
    disclaimer: str = ""


@dataclass
class SelectedCorpus:
    full_tokens: int = 0
    datter_tokens: int = 0
    random_tokens: int = 0
    target_reduction: float = 0.50
    datter_chunk_ids: list[str] = field(default_factory=list)
    random_chunk_ids: list[str] = field(default_factory=list)


@dataclass
class AnalysisReport:
    documents: list[Document]
    chunks: list[Chunk]
    scores: pd.DataFrame
    total_tokens: int
    total_documents: int
    total_chunks: int
    token_cost_usd: float
    embedding_cost_usd: float
    total_cost_usd: float
    avoidable_tokens: int
    avoidable_cost_usd: float
    pct_removable: float
    exact_dup_pct: float
    near_dup_pct: float
    recommendation_counts: dict[str, int]
    top_useful: pd.DataFrame
    most_redundant: pd.DataFrame
    agent_log: list[AgentLogEntry]
    scorer_name: str
    scorer_loaded: bool
    scorer_status: str
    project_id: str = ""
    project_name: str = ""
    selection: SelectedCorpus | None = None
    eval_summary: EvalSummary | None = None
    optimised_corpus_tokens: int = 0
