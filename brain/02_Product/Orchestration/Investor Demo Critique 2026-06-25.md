---
type: product
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - product
  - orchestration
  - investor
  - demo
  - critique
source: cpo-orchestration-2026-06-25
---

# Investor Demo Critique — 2026-06-25

CPO assessment for CEO/investor Loom and outreach. Inputs: [[Executive Finance Report]], [[Business Outreach Brief]], [[CEO Review Meeting 2026-06-25]], live `app.py` results panels.

---

## CEO verdict: would an investor like it?

**Yes — with caveats.** The *story* is investable tonight; the *proof* is not yet fundable.

| What lands | What hurts |
|---|---|
| **Input-gate ROI** — spend compounds before embed/train | **Complexity score gauge** — wrong hero metric; confuses structural noise with eval proof |
| **Selection engine framing** — max cut @ customer quality floor, not blind dedup | **Ugly UI** — Streamlit mockup reads hackathon, not enterprise; gauge + regime cards feel like a dashboard, not a decision |
| **Hands-off agent pipeline** — seven steps, real PDFs, export artifact | **Offline proxy eval** — TF-IDF judge ties Datter vs random on all five projects; one skeptical question kills seed diligence |
| **Government vertical** — 50% cut @ 90.1% on *Managing Public Money* | **Lab misses floor** — 85.9% @ 40.9% undermines "you pick the floor" promise on messy data |
| **Quality-floor pricing tiers** — SKU maps to Assured/Governed upsell | **No delta vs random** — "why pay you?" objection unanswered in numbers |

**Investor temperature:** *Conditional interest* (matches [[CEO Review Meeting 2026-06-25]]). A pre-seed AI-infra angel will take the intro call if we lead with economics + honest disclaimer. They will **not** wire on "92% understanding" from an offline proxy.

**Decision:** Drop **complexity score** from the Loom hero. Lead **compression @ floor → understanding retained → export → $ ROI**.

---

## What to highlight on Loom (ordered)

Record in this sequence. Skip Panel A (complexity gauge) on camera unless asked.

| # | Beat | Screen | Say |
|---|---|---|---|
| **1** | **Compression @ floor** | ROI panel — "Corpus compressed by **X%**" + avoidable tokens | "You pick a 90% quality floor. Datter finds the **maximum token cut** that still meets it — **50% on this Treasury PDF**, not a fixed 50% for everyone." |
| **2** | **Understanding retained** | Advanced → proof table *or* Executive tab understanding % + disclaimer | "At that cut, **90.1% understanding** on our eval questions. Building demo — offline proxy tonight; production LLM judge on roadmap. We show Datter vs random at the **same token budget**." |
| **3** | **Export / audit** | Download **Compress — optimised corpus** + JSON manifest | "You don't just get a score — you get an **optimised corpus zip**, markdown audit, and JSON discard log. Drop straight into your embed pipeline." |
| **4** | **$ ROI** | Embedding savings ($) + input-gate chain | "**$X embedding savings** on this corpus alone. We sit **before** storage → labeling → GPU spend compounds." |

**Corpus pick:** **Government** for story (real PDF, 50% cut). **Lab** only if you need speed (~2s) — call out eval floor miss honestly.

**Do not lead with:** complexity gauge, Core-Set / Ghost Data regime cards, absolute accuracy without disclaimer.

---

## Persona reactions (simulated)

### 1 · RAG / ML engineer at startup

| Field | Reaction |
|---|---|
| **First 10 sec** | "Upload → agents run → 50% fewer tokens? Okay, that's my embed bill." |
| **How they'd use it** | Pre-embed audit on support-bot PDFs; export optimised zip into Pinecone/pgvector; keep `queries.json` aligned with bot eval |
| **Objection** | "Random cut at the same budget scores the same on your chart — why not `numpy.random`?" |
| **What wins them** | Beat-random delta on **their** corpus + LLM judge on **their** 5–10 questions; one-click export that drops into existing ingest |

### 2 · MLOps / platform lead

| Field | Reaction |
|---|---|
| **First 10 sec** | "Seven agents, audit JSON — could be a CI gate before index refresh." |
| **How they'd use it** | Wire as pre-ingestion step in deploy pipeline; block embed if floor not met; store manifest in object storage for rollback |
| **Objection** | "Streamlit demo isn't an API. Where's the SLA, idempotency, and VPC deploy?" |
| **What wins them** | Headless CLI/API, project-scoped config, Pareto artifact in S3, **Governed tier** with on-prem option |

### 3 · CFO / finance

| Field | Reaction |
|---|---|
| **First 10 sec** | "Avoidable tokens and dollar savings — finally someone talking before the $400k GPU line." |
| **How they'd use it** | Approve RAG pilot spend only after Datter audit; tie embedding line item to **max safe cut @ floor** tier |
| **Objection** | "Savings assume your understanding metric is real. What's the audit trail for the board?" |
| **What wins them** | Executive sentence from [[Executive Finance Report]] + conservative $/M assumptions + **quality-floor pricing** ("you pick 90/95/99%, we price to floor") |

### 4 · AI lab research director

| Field | Reaction |
|---|---|
| **First 10 sec** | "Paper Summary Team — multi-model exam on full vs compressed. That's interesting." |
| **How they'd use it** | Run `exam_results.json` across gpt/opus/sonnet/composer before publishing internal paper summaries; treat as compression benchmark harness |
| **Objection** | "Selection quality is only as good as your scorer. Adisorn/hybrid isn't shipped." |
| **What wins them** | Open scorer plugin slot, Pareto frontier iteration story, design-partner co-auth on **task-conditioned selection** (M2/M3) |

### 5 · Regulated enterprise — bank / gov compliance buyer

| Field | Reaction |
|---|---|
| **First 10 sec** | "Managing Public Money PDF — they understand our world. Export + discard log — good." |
| **How they'd use it** | Audit internal policy KB before citizen-facing RAG; require manifest proving which chunks were dropped and why, per eval question |
| **Objection** | "90.1% on four hackathon questions isn't compliance sign-off. Offline TF-IDF won't pass InfoSec." |
| **What wins them** | **Governed tier** — 99% floor, VPC, LLM judge + human review queue, immutable audit trail, no training on customer data |

---

## Selling loop — company pitch sequence

Four-step loop for design partner → paid tier → expand. Repeat per account.

```text
1. HOOK — Input gate
   "You're about to embed {N}M tokens. Much won't help your bot answer anything."

2. PROVE — Max cut @ their floor
   Run hands-off audit on one corpus + their eval questions.
   Show: compression %, understanding retained, Datter vs random (same budget).

3. SHIP — Optimised export
   They embed the zip, not the raw dump. Manifest + discard log for audit.

4. EXPAND — Floor tier + frontier
   Start Standard (90%) → Assured (95%) → Governed (99%) as trust grows.
   Research flywheel lifts max cut at same floor → more savings, same SKU.
```

**Close line:** "You pick the quality floor. We find the max cut — and keep pushing that cut up as scoring improves."

---

## Links

- Up: [[Orchestration Plan]]
- Prior review: [[CEO Review Meeting 2026-06-25]]
- Loom: [[Loom Script]]
- GTM: [[Business Outreach Brief]]
- Finance: [[Executive Finance Report]]
