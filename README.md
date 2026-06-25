# Datter AI Hands-Off

**We know which data matters.**

Datter AI is the data usefulness layer for AI. It audits datasets before teams spend money on tokenisation, embedding, labelling, fine-tuning, or training.

This hackathon MVP runs fully local as a Streamlit app with a pluggable scoring engine.

**Project memory:** strategy, session archive, paper notes, and handoffs live in [`brain/`](brain/). Start with [`brain/02_Product/Product Spine.md`](brain/02_Product/Product%20Spine.md).

## Project brain

Datter-specific project memory lives in [`brain/`](brain/). Start with [`brain/00_System/Datter Brain Manager.md`](brain/00_System/Datter%20Brain%20Manager.md) before changing product direction, paper notes, experiments, or source routing.

## Quick start

```bash
cd /Users/tharm/dev/datter
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Click **Run demo dataset** for a 2-minute pitch.

## What it does

1. Upload or select `.txt`, `.md`, `.pdf` files
2. Autonomous agent pipeline: ingest → chunk → dedup → score → report
3. Dashboard shows tokens, costs, duplicates, recommendations, agent log
4. Export JSON / Markdown action plan

## Scoring engines

| Mode | Description |
|------|-------------|
| **Baseline** | Heuristic redundancy/novelty/density + gzip complexity proxy |
| **Adisorn research** | Wrapper for Adisorn Panasawatwong's complexity model (placeholder until model files added) |
| **Hybrid** | Blends baseline + Adisorn when model loaded |

See [`models/adisorn/README.md`](models/adisorn/README.md) for model integration.

## Architecture

```
app.py                 Streamlit dashboard
datter/
  agent.py             Autonomous pipeline + run log
  ingest.py            File/folder ingestion
  chunking.py          Token-aware chunking
  dedup.py             Exact + near-duplicate detection
  token_cost.py        tiktoken + cost estimates
  report.py            Aggregations + exports
  scorers/
    base.py            BaseScorer interface
    baseline.py        Default heuristic scorer
    adisorn_complexity.py  Research model wrapper
    hybrid.py          Combined scoring
demo_data/             Bundled pitch dataset
```

## Compression research (2023–2026)

Baseline complexity proxy is informed by recent data-compression literature:

| Paper | Insight for Datter |
|-------|-------------------|
| [Kim & Baek 2024](https://arxiv.org/abs/2406.14124) | Entropy-based sample importance; low-info samples are pruning candidates |
| [ZIP-FIT 2024](https://arxiv.org/abs/2410.18194) | Gzip NCD for task-aligned selection |
| [PreSelect 2025](https://proceedings.mlr.press/v267/shum25a.html) | Compression efficiency predicts downstream value |
| [SoftDedup 2024](https://arxiv.org/abs/2407.06654) | Reweight vs hard-drop for near-duplicates |

## 60-second pitch

1. "AI teams pay to process everything — most of it is redundant."
2. Click **Run demo dataset** — agent log shows autonomous analysis.
3. Point to **avoidable tokens** and **projected savings**.
4. Show a redundant chunk marked **drop**.
5. "Datter AI — we know which data matters."

## Tests

```bash
pytest tests/ -q
```

## Out of scope (MVP)

Auth, billing, enterprise deployment, LLM API calls, persistent database.
