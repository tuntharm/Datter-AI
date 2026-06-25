from pathlib import Path

import pandas as pd

from datter.scorers import get_scorer
from datter.models import ScorerConfig


def _sample_items():
    return pd.DataFrame(
        [
            {"item_id": "a", "text": "Unique neural operator surrogate for beam dynamics with FNO layers.", "token_count": 20, "max_similarity": 0.1, "is_exact_duplicate": False, "is_canonical": True},
            {"item_id": "b", "text": "Unique neural operator surrogate for beam dynamics with FNO layers.", "token_count": 20, "max_similarity": 0.1, "is_exact_duplicate": True, "is_canonical": False},
            {"item_id": "c", "text": "As discussed follow up no action required lorem ipsum boilerplate.", "token_count": 15, "max_similarity": 0.2, "is_exact_duplicate": False, "is_canonical": True},
        ]
    )


def test_baseline_scorer_returns_all_columns():
    scorer = get_scorer("baseline")
    out = scorer.score(_sample_items())
    assert len(out) == 3
    assert out.iloc[1]["recommended_action"] == "drop"


def test_adisorn_graceful_without_model():
    cfg = ScorerConfig(model_path=str(Path(__file__).parent / "missing_models"))
    scorer = get_scorer("adisorn", cfg)
    assert not scorer.is_loaded
    out = scorer.score(_sample_items())
    assert len(out) == 3


def test_hybrid_degrades_without_model():
    cfg = ScorerConfig(model_path=str(Path(__file__).parent / "missing_models"))
    scorer = get_scorer("hybrid", cfg)
    assert not scorer.is_loaded
    out = scorer.score(_sample_items())
    assert len(out) == 3
