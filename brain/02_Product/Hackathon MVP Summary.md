---
type: product
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - product
  - hackathon
  - mvp
source: cursor-chat-2026-06-25
---

# Hackathon MVP Summary

**Event:** Cursor Hands Off London Hackathon  
**Product name:** Datter AI Hands-Off  
**Tagline:** "We know which data matters."

## What was built

Local-first Streamlit MVP at `/Users/tharm/dev/datter`.

### Features shipped

- [x] Upload or select folder of `.txt`, `.md`, `.pdf` files
- [x] Token-aware chunking (~400 tokens, ~50 overlap)
- [x] Token + embedding cost estimation (`tiktoken`)
- [x] Exact duplicate detection (SHA-256 normalised hash)
- [x] Near-duplicate detection (TF-IDF cosine ≥ 0.85)
- [x] Scoring: redundancy, novelty, density, usefulness, complexity proxy
- [x] Actions: keep / drop / compress / review
- [x] Dashboard KPIs + chunk tables + agent run log
- [x] JSON + Markdown export
- [x] Bundled demo dataset
- [x] Pluggable scorer architecture (baseline / Adisorn / hybrid)

### Demo results (bundled corpus)

| Metric | Value |
|---|---|
| Documents | 6 |
| Avoidable tokens | ~41% |
| Scorer fallback | Works without Adisorn model files |

### Run

```bash
cd /Users/tharm/dev/datter
source .venv/bin/activate
streamlit run app.py
```

### Tests

```bash
pytest tests/ -q   # 5 passed
```

## What MVP proves (wedge)

> Datter can identify low-value, redundant, or compressible AI data before token, embedding, or training cost is committed.

## What MVP does NOT prove yet

- Task-conditioned usefulness
- Marginal selection under budget
- Downstream RAG quality preservation
- Adisorn research model inference

See [[Product Spine]] for the company-level target.

## Milestone sequencing

| Phase | Deliverable |
|---|---|
| **M1 (done)** | Structural audit + cost estimate + agent log demo |
| **M2** | Greedy marginal selector + token budget |
| **M3** | Task description + representative queries |
| **M4** | RAG eval harness + reduction curve |
| **M5** | Adisorn complexity model wired in |

## 60-second pitch script

1. "AI teams pay to tokenise, embed, and train on everything — most of it is redundant."
2. Click **Run demo dataset** — agent log shows autonomous analysis in seconds.
3. Point to **avoidable tokens** and **projected savings**.
4. Show a redundant chunk marked **drop**.
5. "Datter AI — we know which data matters."

## Links

- Code: `app.py`, `datter/agent.py`, `datter/scorers/`
- Demo: `demo_data/`
- Product spine: [[Product Spine]]
- Session archive: [[Cursor Session 2026-06-25]]
