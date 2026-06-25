from datter.scorers.base import SCORE_COLUMNS, BaseScorer
from datter.scorers.baseline import BaselineScorer
from datter.scorers.adisorn_complexity import AdisornComplexityScorer
from datter.scorers.hybrid import HybridScorer

SCORER_MODES = {
    "baseline": BaselineScorer,
    "adisorn": AdisornComplexityScorer,
    "hybrid": HybridScorer,
}


def get_scorer(mode: str, config=None):
    from datter.models import ScorerConfig

    cfg = config or ScorerConfig()
    if mode == "hybrid":
        return HybridScorer(cfg)
    cls = SCORER_MODES.get(mode, BaselineScorer)
    return cls(cfg)


__all__ = [
    "SCORE_COLUMNS",
    "BaseScorer",
    "BaselineScorer",
    "AdisornComplexityScorer",
    "HybridScorer",
    "get_scorer",
    "SCORER_MODES",
]
