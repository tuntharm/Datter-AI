from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd

SCORE_COLUMNS = [
    "item_id",
    "complexity_score",
    "usefulness_score",
    "redundancy_score",
    "novelty_score",
    "information_density_score",
    "recommended_action",
    "explanation",
]

ACTIONS = ("keep", "drop", "compress", "review")


class BaseScorer(ABC):
    name: str = "base"

    def __init__(self, config=None):
        from datter.models import ScorerConfig

        self.config = config or ScorerConfig()

    @abstractmethod
    def fit(self, data: pd.DataFrame) -> BaseScorer:
        ...

    @abstractmethod
    def score(self, items: pd.DataFrame) -> pd.DataFrame:
        ...

    @property
    def is_loaded(self) -> bool:
        return True

    @property
    def status_message(self) -> str:
        return f"{self.name} ready"

    @staticmethod
    def clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
        return max(lo, min(hi, value))

    @staticmethod
    def empty_scores(items: pd.DataFrame) -> pd.DataFrame:
        return pd.DataFrame({col: [] for col in SCORE_COLUMNS})
