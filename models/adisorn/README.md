# Adisorn Complexity Model — Integration Guide

Private research model slot for **Adisorn Panasawatwong**'s data-driven complexity scorer.

Datter loads this model as a scoring plugin. The app runs without these files — baseline scoring continues automatically.

## Where to place files

```
models/adisorn/
├── manifest.json          # recommended — declares format and semantics
├── complexity_model.pt    # OR .pkl / .onnx / score_fn.py
└── README.md
```

## manifest.json template

```json
{
  "model_file": "complexity_model.pt",
  "format": "pytorch",
  "input_type": "text",
  "output_key": "complexity",
  "higher_is_more_complex": true,
  "normalization": {"min": 0.0, "max": 1.0}
}
```

## Supported formats

| Format | Extension | Loader |
|--------|-----------|--------|
| PyTorch | `.pt` | `torch.load` — TODO: wire architecture |
| sklearn | `.pkl`, `.joblib` | `joblib.load` |
| ONNX | `.onnx` | `onnxruntime.InferenceSession` |
| Python hook | `score_fn.py` | must expose `score_batch(items) -> list[float]` |

## Configuration (Streamlit sidebar)

- `model_path` — default `models/adisorn`
- `input_type` — `text` | `embedding` | `feature_vector` | `time_series`
- `device` — `cpu` | `cuda` | `mps`
- `batch_size` — inference batch size

## Information needed from Adisorn

1. Model file(s) and format
2. What the raw output means (higher = more complex or more useful?)
3. Normalization range for mapping to 0–1
4. Input preprocessing (tokenization, feature extraction)
5. Max sequence length / feature dimensions
6. Optional: custom `score_fn.py` for rapid integration

## Fallback behaviour

If no model is found, `AdisornComplexityScorer` uses a **gzip compression proxy** (MDL-inspired placeholder) and the dashboard shows:

> Research scorer not loaded — baseline scoring active

## Research background

Recent work (2023–2026) links data value to compressibility / description length:

- Tan et al. 2024 — cross-entropy as MDL proxy for LLM data pruning
- Obbad et al. 2024 — ZIP-FIT gzip alignment for data selection
- Shum et al. 2025 — PreSelect compression-efficiency scoring

The placeholder proxy aligns with this literature until Adisorn's model is integrated.
