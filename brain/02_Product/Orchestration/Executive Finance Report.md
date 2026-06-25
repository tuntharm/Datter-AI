---
type: product
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - product
  - finance
  - executive
source: orchestration-plan-2026-06-25
---

# Executive Finance Report

One-page executive summary for the Datter AI Hands-Off demo. CTO renders this in the **Executive** tab.

## Input-gate ROI (why this matters)

```text
Storage ($27k) → Labeling ($150k) → GPU/training ($400k+)
```

Datter sits **before** that chain compounds. Every token embedded into RAG without audit is prepaid waste.

> Move from "Is the data clean?" to "Is the data worth AI spend?"

## Per-project economics (template)

| Metric | Source |
|---|---|
| Corpus tokens analysed | Pipeline report |
| Avoidable tokens | keep/drop/compress recommendations |
| Token + embedding cost (full) | User cost assumptions |
| Projected savings | Avoidable tokens × blended $/M |
| Understanding retained | EvalAgent offline proxy (see disclaimer) |
| Quality floor | Project `queries.json` (default 90%) |

**Executive sentence:**

> "This project contains **{total_tokens}** tokens. Datter identifies **{avoidable_tokens}** ({pct_removable}%) as avoidable before embedding, saving **${avoidable_cost_usd}** at current rates, while retaining **{understanding_pct}%** understanding on the eval set at a **{quality_floor}%** floor."

## Quality-floor pricing tiers (conceptual)

| Tier | Quality floor | Use case | Price unit |
|---|---|---|---|
| **Audit** | N/A (structural only) | Free wedge / hackathon | Free local |
| **Standard** | 90% understanding | RAG teams, support bots | $/M tokens analysed |
| **Assured** | 95% understanding | Regulated internal KB | $/project/month |
| **Governed** | 99% understanding | Banks, audit trail required | Enterprise + VPC |

Product sells **max token cut at customer's quality floor**, not a fixed 50% for all data. See [[Business Model & Finance]] for the Pareto flywheel and research reinvestment loop.

## Key SKU metric: max safe reduction

> At quality floor **{quality_floor}%**, max safe cut **{max_safe_reduction_pct}%** — understanding **{understanding_pct}%** (random **{random_understanding_pct}%** at same budget).

North star: raise max cut toward **100% token drop** at **100% understanding** via research (Adisorn, M2, M3).

## Hackathon disclaimer (required in UI)

**Building demo — offline understanding proxy.**

Tonight's understanding % uses TF-IDF retrieval + token-overlap judge on fixed eval questions. This is **not** a production accuracy claim. Production eval uses the developed LLM answer + judge harness (see [[Proof Loop Spec]]).

Do not tell judges "92% understanding" unless EvalAgent ran and the disclaimer is visible.

## CFO recommendation for Loom

1. Lead with **avoidable tokens + $ saved** (concrete, believable tonight).
2. Show **understanding % vs random cut** on Proof tab (relative win, not absolute truth).
3. Close with **quality floor pricing** — "You pick the floor; we find the max cut."

## Links

- Up: [[Orchestration Plan]]
- GTM: [[Business Strategy]]
- Proof: [[Proof Loop Spec]]
