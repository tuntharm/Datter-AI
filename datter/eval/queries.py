from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class EvalQuestion:
    id: str
    query: str
    gold_hint: str = ""


@dataclass
class EvalConfig:
    task_description: str
    quality_floor: float
    target_token_reduction: float
    questions: list[EvalQuestion]


def load_queries(path: Path) -> EvalConfig:
    data = json.loads(path.read_text(encoding="utf-8"))
    questions = [
        EvalQuestion(id=q["id"], query=q["query"], gold_hint=q.get("gold_hint", ""))
        for q in data.get("questions", [])
    ]
    return EvalConfig(
        task_description=data.get("task_description", ""),
        quality_floor=float(data.get("quality_floor", 0.90)),
        target_token_reduction=float(data.get("target_token_reduction", 0.50)),
        questions=questions,
    )
