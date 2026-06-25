---
type: product
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - product
  - ux
  - demo
source: input-gate-redesign-2026-06-25
---

# Demo UX Spec

CTO implements these rules literally in [app.py](../../app.py).

## Default experience (Input Gate)

1. **Upload-first** — main page is a single two-column layout; no project cards on main stage
2. **Idle state** — right column shows empty prompt until scan completes
3. **Auto-scan on upload** — new files trigger pipeline automatically
4. **Sample corpora** — sidebar **Try sample** only (Government, Social, Engineering, Science, Lab)
5. **Sidebar expanded** on load so samples are discoverable

## Layout

| Column | Content |
|---|---|
| **Left (~35%)** | THE INPUT GATE — upload zone, S3/SQL/Kafka chips (coming soon), structural scan progress |
| **Right (~65%)** | Results panels A/B/C or empty state |

## Structural scan (left column)

- Title: `Structural Scan`
- `st.progress()` driven by 7 agent steps (Ingest → Report)
- Status line from latest agent log entry

## Results panels (right column)

Investor order: **compress → quality → savings → export**. See [[Investor Demo Critique 2026-06-25]].

### A · Compression

- Hero: max safe cut % (compression on optimised export)
- Token flow: full corpus → optimised tokens
- Stats: avoidable tokens, redundant %, total corpus size

### B · Quality retained

- Hero: `eval_summary.understanding_pct` when eval ran
- Fallback: structural proxy + disclaimer when no `queries.json`
- Never lead with a "complexity score" gauge

### C · ROI / savings

- Hero: `avoidable_cost_usd` (green)
- Stats: token cut %, full vs optimised corpus cost

## Download actions (primary CTAs)

| Button | Action |
|---|---|
| Download optimised corpus (.zip) | Optimised export |
| Download audit report (.md) | Full audit markdown |

Inline **Report preview (Markdown)** expander below downloads.

## Advanced (collapsed)

`Advanced audit & proof` expander:

- Regime labeling (Core-Set / Edge / Ghost by token %)
- JSON audit log download
- Proof disclaimer + Q&A table (when eval ran)
- Pareto chart (when available)
- Chunk audit tables

## Copy

- Page title: "Pre-embedding corpus audit"
- Sub: "Upload → scan → compress → report"
- Footer: model-agnostic density scan before RAG/embed spend

## Links

- Up: [[Orchestration Plan]]
- Finance: [[Executive Finance Report]]
- Proof: [[Proof Loop Spec]]
