---
type: map
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - map
  - project
  - datter
---

# Project Map

## Definition

Datter AI is the data usefulness layer for AI.

**Company thesis:** Datter compiles a raw corpus into the smallest dataset that preserves downstream AI performance under a cost budget.

The selection engine is the product; dashboard and agents are packaging.

Full product definition: [[Product Spine]].

## Current Repo State

| Area | Current Surface |
|---|---|
| App | `app.py` Streamlit dashboard |
| Pipeline | `datter/agent.py` |
| Ingestion | `datter/ingest.py` |
| Chunking | `datter/chunking.py` |
| Deduplication | `datter/dedup.py` |
| Scoring | `datter/scorers/` |
| Reporting | `datter/report.py` |
| Demo data | `demo_data/` |
| Vertical proof corpus | `demo_verticals/` — see [[Vertical Demo Corpus]] |
| Tests | `tests/` |
| Project brain | `brain/` |
| Orchestration | `brain/02_Product/Orchestration/` — [[Orchestration Plan]] |

## Current Wedge

Pre-ingestion validation for AI pipelines.

First commercial pain: token, embedding, and retrieval waste in local document workflows.

## MVP Claim (M1 — shipped)

Datter can identify low-value, redundant, or compressible AI data before expensive AI work is committed.

Demo: ~41% avoidable tokens on bundled corpus. Details: [[Hackathon MVP Summary]].

## Milestones

| # | Goal | Status |
|---|---|---|
| M1 | Structural audit + cost estimate + agent demo | Done |
| M2 | Greedy marginal selector under token budget | Pending |
| M3 | Task description + representative queries | Pending |
| M4 | RAG eval harness + reduction curve | Pending |
| M5 | Adisorn complexity model wired in | Blocked on model files |

## Near-Term Proofs Needed

- **Hackathon P0:** LLM judge proof on vertical PDFs — [[Proof Loop Spec]] (≥90% understanding @ ~50% cut).
- Project-scoped corpus + eval set — [[Project Model]].
- Reduction curve / Pareto: quality vs % tokens removed (see [[Product Spine]]).
- Marginal selection beats independent thresholding (M2).
- Task-conditioned relevance when queries provided (M3).
- Adisorn complexity integrated as one utility component (M5 — blocked).

## Links

- Manager: [[Datter Brain Manager]]
- Source map: [[Source Map]]
- Product source docs: [[Datter Source Documents]]
- Research: [[Papers Map]]
- Experiments: [[Experiment Map]]
- Requests: [[REQUESTS]]
- Handoff: [[HANDOFF]]
- Product spine: [[Product Spine]]
- Cursor session: [[Cursor Session 2026-06-25]]
- Home-workspace chat: [[Cursor Session 2026-06-25 Home Workspace Chat]]
- Business / GTM: [[Business Strategy]]
- New chat entry: `CHAT_START.md` (repo root)
- Scorer plugins: [[Scorer Plugin Architecture]]
- MVP summary: [[Hackathon MVP Summary]]
- Orchestration: [[Orchestration Plan]]
- Agent roles: [[Agent Team Model]]
- Project UX: [[Project Model]]
- Proof spec: [[Proof Loop Spec]]
- Demo PDFs: [[Vertical Demo Corpus]]
- CEO archive: [[CEO Discussion Archive 2026-06-25]]

