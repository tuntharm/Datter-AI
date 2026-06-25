from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from datter.models import EvalSummary


def load_eval_cache(path: Path) -> EvalSummary | None:
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    from datter.models import EvalQuestionResult, ParetoPoint

    questions = [EvalQuestionResult(**q) for q in data.get("questions", [])]
    pareto = [ParetoPoint(**p) for p in data.get("pareto_points", [])]
    return EvalSummary(
        mean_full_score=data.get("mean_full_score", 100.0),
        mean_datter_score=data.get("mean_datter_score", 0.0),
        mean_random_score=data.get("mean_random_score", 0.0),
        understanding_pct=data.get("understanding_pct", 0.0),
        random_understanding_pct=data.get("random_understanding_pct", 0.0),
        quality_floor=data.get("quality_floor", 0.90),
        target_reduction=data.get("target_reduction", 0.50),
        actual_reduction=data.get("actual_reduction", 0.0),
        max_safe_reduction_pct=data.get("max_safe_reduction_pct", 0.0),
        meets_quality_floor=data.get("meets_quality_floor", False),
        questions=questions,
        pareto_points=pareto,
        disclaimer=data.get("disclaimer", ""),
    )


def save_eval_cache(path: Path, summary: EvalSummary) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "mean_full_score": summary.mean_full_score,
        "mean_datter_score": summary.mean_datter_score,
        "mean_random_score": summary.mean_random_score,
        "understanding_pct": summary.understanding_pct,
        "random_understanding_pct": summary.random_understanding_pct,
        "quality_floor": summary.quality_floor,
        "target_reduction": summary.target_reduction,
        "actual_reduction": summary.actual_reduction,
        "max_safe_reduction_pct": summary.max_safe_reduction_pct,
        "meets_quality_floor": summary.meets_quality_floor,
        "disclaimer": summary.disclaimer,
        "questions": [asdict(q) for q in summary.questions],
        "pareto_points": [asdict(p) for p in summary.pareto_points],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
