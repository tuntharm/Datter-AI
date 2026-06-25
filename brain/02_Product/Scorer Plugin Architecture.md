---
type: product
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - product
  - architecture
  - scoring
  - adisorn
source: cursor-chat-2026-06-25
---

# Scorer Plugin Architecture

## Goal

Clean plugin interface supporting:

1. Baseline scoring methods **now**
2. Adisorn's research model **later**
3. Other scorers in the **future**

The app must run even if Adisorn model files are missing.

## Interface

```python
class BaseScorer:
    name: str

    def fit(self, data: pd.DataFrame) -> BaseScorer: ...
    def score(self, items: pd.DataFrame) -> pd.DataFrame: ...
```

Each scorer returns a DataFrame with:

| Column | Description |
|---|---|
| `item_id` | chunk identifier |
| `complexity_score` | structural complexity (0–1) |
| `usefulness_score` | composite utility (0–1) |
| `redundancy_score` | overlap with corpus (0–1) |
| `novelty_score` | inverse redundancy + unique content |
| `information_density_score` | content per token |
| `recommended_action` | keep / drop / compress / review |
| `explanation` | human-readable reason |

## Code layout

```text
datter/scorers/
  base.py                 # BaseScorer ABC + SCORE_COLUMNS
  baseline.py             # heuristics + gzip complexity proxy
  adisorn_complexity.py   # research model wrapper (placeholder)
  hybrid.py               # blends baseline + Adisorn
  __init__.py             # get_scorer(mode, config) factory

models/adisorn/
  README.md               # integration contract
  manifest.json           # optional format declaration
  *.pt / *.pkl / *.onnx   # gitignored model files
  score_fn.py             # optional Python hook
```

## Scorer modes (Streamlit sidebar)

| Mode | Behaviour |
|---|---|
| **Baseline** | Always available; gzip complexity proxy |
| **Adisorn research** | Loads model if present; else placeholder + warning banner |
| **Hybrid** | Blends baseline + Adisorn; degrades to baseline-only if model missing |

## AdisornComplexityScorer — design rules

- Do **not** hardcode assumptions about the research model
- Do **not** break baseline scorer
- Support future loading from: `.pt`, `.pkl`, `.onnx`, `score_fn.py`
- Configuration: `model_path`, `input_type`, `device`, `batch_size`
- If missing: dashboard shows **"Research scorer not loaded"** and continues with baseline

## Placeholder (until Adisorn delivers model)

Uses gzip compression ratio as MDL-inspired complexity proxy (see [[Measuring Sample Importance in Data Pruning]], [[ZIP-FIT]]).

## Information needed from Adisorn

1. Model file(s) and format
2. Output semantics (higher = more complex or more useful?)
3. Normalization range for 0–1 mapping
4. Input preprocessing requirements
5. Max sequence length / feature dimensions
6. Optional custom `score_fn.py`

## Links

- Integration guide: `models/adisorn/README.md`
- Product spine: [[Product Spine]]
- Up: [[Datter Source Documents]]
