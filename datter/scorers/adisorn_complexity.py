from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from datter.scorers.base import SCORE_COLUMNS, BaseScorer
from datter.scorers.baseline import BaselineScorer, gzip_complexity, recommend_action


class AdisornComplexityScorer(BaseScorer):
    """Wrapper for Adisorn Panasawatwong's research complexity model.

    Supports future loading from .pt, .pkl, .onnx, or score_fn.py.
    Until model files are provided, uses a gzip compression proxy.
    """

    name = "adisorn"

    def __init__(self, config=None):
        super().__init__(config)
        self._model = None
        self._manifest: dict | None = None
        self._format: str | None = None
        self._loaded = False
        self._baseline = BaselineScorer(config)
        self._try_load_model()

    def _model_dir(self) -> Path:
        return Path(self.config.model_path)

    def _try_load_model(self) -> None:
        model_dir = self._model_dir()
        manifest_path = model_dir / "manifest.json"
        if manifest_path.exists():
            self._manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            model_file = self._manifest.get("model_file")
            if model_file:
                path = model_dir / model_file
                if path.exists():
                    self._format = self._manifest.get("format")
                    self._model = self._load_by_format(path, self._format)
                    if self._model is not None:
                        self._loaded = True
                        return

        for pattern, fmt in [
            ("*.pt", "pytorch"),
            ("*.pkl", "sklearn"),
            ("*.joblib", "sklearn"),
            ("*.onnx", "onnx"),
        ]:
            matches = list(model_dir.glob(pattern))
            if matches:
                self._format = fmt
                self._model = self._load_by_format(matches[0], fmt)
                if self._model is not None:
                    self._loaded = True
                    return

        score_fn = model_dir / "score_fn.py"
        if score_fn.exists():
            # TODO: dynamic import of user-provided score_batch(items)
            self._format = "python"
            self._loaded = False

    def _load_by_format(self, path: Path, fmt: str | None):
        fmt = (fmt or path.suffix.lstrip(".")).lower()
        try:
            if fmt in {"pytorch", "pt"}:
                import torch  # noqa: F401

                # TODO: wire Adisorn model architecture once format is known
                return torch.load(path, map_location=self.config.device, weights_only=True)
            if fmt in {"sklearn", "pkl", "joblib"}:
                import joblib

                return joblib.load(path)
            if fmt == "onnx":
                import onnxruntime as ort

                return ort.InferenceSession(str(path))
        except Exception:
            return None
        return None

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    @property
    def status_message(self) -> str:
        if self._loaded:
            return f"Adisorn research scorer loaded ({self._format})"
        return "Research scorer not loaded — using compression proxy"

    def fit(self, data: pd.DataFrame) -> AdisornComplexityScorer:
        self._baseline.fit(data)
        # TODO: corpus-level normalization stats for complexity scores
        return self

    def _placeholder_complexity(self, text: str) -> float:
        return gzip_complexity(text)

    def _predict_complexity_batch(self, texts: list[str]) -> list[float]:
        if not self._loaded or self._model is None:
            return [self._placeholder_complexity(t) for t in texts]

        # TODO: implement inference for each supported format once Adisorn delivers model
        return [self._placeholder_complexity(t) for t in texts]

    def score(self, items: pd.DataFrame) -> pd.DataFrame:
        if items.empty:
            return self.empty_scores(items)

        baseline_df = self._baseline.score(items)
        complexities = self._predict_complexity_batch(items["text"].astype(str).tolist())

        rows = []
        for i, (_, row) in enumerate(items.iterrows()):
            base = baseline_df.iloc[i]
            complexity = BaseScorer.clamp(complexities[i])
            redundancy = float(base["redundancy_score"])
            density = float(base["information_density_score"])
            novelty = BaseScorer.clamp(1.0 - redundancy + 0.2 * complexity)
            usefulness = BaseScorer.clamp(0.35 * complexity + 0.35 * novelty + 0.30 * density - 0.30 * redundancy)

            action, base_expl = recommend_action(usefulness, redundancy, density, row)
            if self._loaded:
                explanation = f"Adisorn complexity={complexity:.2f}. {base_expl}"
            else:
                explanation = f"Placeholder: awaiting Adisorn model at {self.config.model_path}. {base_expl}"

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
