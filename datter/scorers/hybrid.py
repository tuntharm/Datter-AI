from __future__ import annotations

import pandas as pd

from datter.scorers.adisorn_complexity import AdisornComplexityScorer
from datter.scorers.base import SCORE_COLUMNS, BaseScorer
from datter.scorers.baseline import recommend_action


class HybridScorer(BaseScorer):
    name = "hybrid"

    def __init__(self, config=None):
        super().__init__(config)
        from datter.scorers.baseline import BaselineScorer

        self._baseline = BaselineScorer(config)
        self._adisorn = AdisornComplexityScorer(config)

    @property
    def is_loaded(self) -> bool:
        return self._adisorn.is_loaded

    @property
    def status_message(self) -> str:
        if self._adisorn.is_loaded:
            return (
                f"Hybrid scorer: baseline ({self.config.baseline_weight:.0%}) + "
                f"Adisorn ({self.config.research_weight:.0%})"
            )
        return "Research scorer not loaded — hybrid using baseline only"

    def fit(self, data: pd.DataFrame) -> HybridScorer:
        self._baseline.fit(data)
        self._adisorn.fit(data)
        return self

    def score(self, items: pd.DataFrame) -> pd.DataFrame:
        if items.empty:
            return self.empty_scores(items)

        base_df = self._baseline.score(items)
        adisorn_df = self._adisorn.score(items)

        bw = self.config.baseline_weight
        rw = self.config.research_weight if self._adisorn.is_loaded else 0.0
        total = bw + rw
        if total <= 0:
            bw, rw, total = 1.0, 0.0, 1.0
        bw /= total
        rw /= total

        rows = []
        for i, (_, row) in enumerate(items.iterrows()):
            b = base_df.iloc[i]
            a = adisorn_df.iloc[i]
            usefulness = BaseScorer.clamp(
                bw * float(b["usefulness_score"]) + rw * float(a["complexity_score"])
            )
            redundancy = float(b["redundancy_score"])
            density = float(b["information_density_score"])
            novelty = BaseScorer.clamp(bw * float(b["novelty_score"]) + rw * float(a["novelty_score"]))
            complexity = BaseScorer.clamp(bw * float(b["complexity_score"]) + rw * float(a["complexity_score"]))

            action, expl = recommend_action(usefulness, redundancy, density, row)
            if not self._adisorn.is_loaded:
                explanation = f"Hybrid (baseline-only): {expl}"
            else:
                explanation = f"Hybrid blend ({bw:.0%} baseline, {rw:.0%} Adisorn): {expl}"

            rows.append(
                {
                    "item_id": row["item_id"],
                    "complexity_score": round(complexity, 4),
                    "usefulness_score": round(usefulness, 4),
                    "redundancy_score": round(redundancy, 4),
                    "novelty_score": round(novelty, 4),
                    "information_density_score": round(density, 4),
                    "recommended_action": action,
                    "explanation": explanation,
                }
            )

        return pd.DataFrame(rows, columns=SCORE_COLUMNS)
