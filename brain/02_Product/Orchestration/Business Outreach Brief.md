---
type: product
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - product
  - gtm
  - outreach
  - hackathon
source: ceo-orchestration-2026-06-25
---

# Business Outreach Brief — 2026-06-25

**Tonight's goal:** three parallel conversations — design partner, seed investor, plugin partner.  
**Product anchor:** max token cut at customer quality floor; same understanding for AI, fewer tokens.

Business team uses this doc + [[CEO Pitch Meeting 2026-06-25]] + hackathon Loom link.

---

## Who to reach (prioritized)

| Track | Who | Why tonight | Success signal |
|---|---|---|---|
| **A — Client** | **AI lab / RAG team lead** (priority for [[Paper Summary Team]]) | Phase 1 ICP; multi-model exam proves compression before embed | Pilot + `exam_results.json` review |
| **A — Client** | ML engineer pre-embedding | Token waste pain | 15-min call + corpus pilot offer |
| **B — Investor** | Pre-seed / seed AI infra, dev-tools, data-quality angels | Input-gate ROI + agent-company story | Intro call + deck + demo link |
| **C — Partner** | Vector DB, RAG framework, embedding API, scorer plugin authors | Distribution + proof harness integration | Technical intro + plugin spec share |

**Do not lead with:** datacenter channel, training-accuracy ML-lab pitch, or absolute "92% understanding" without disclaimer.

---

## Track A — AI lab / RAG team (design partner)

### Target profile

- Team embedding PDFs / docs into Pinecone, Weaviate, pgvector, etc.  
- 500k–10M+ tokens/month in embeddings + retrieval context  
- Has (or will write) 5–10 eval questions for their bot  
- Pain: cost, latency, noisy retrieval — not "we need another ETL tool"

### Where to find tonight

- Hackathon attendees building RAG / agent apps  
- London AI engineer meetups, Cursor community, company Slack #rag #llm  
- LinkedIn: "RAG", "vector database", "knowledge base", "support bot" + eng title  

### Talk track (60 seconds)

> "You're about to embed a corpus. Much of it won't help your bot answer anything. Datter runs seven hands-off agents — ingest through export — and finds the **maximum token cut** that still meets **your** quality floor on your eval questions. Our **Paper Summary Team** runs the same exam across gpt, opus, sonnet, and composer — full corpus vs compressed — so you see score vs compression on the models you actually use. We prove Datter vs random at the same budget. Free local audit tonight; paid tier is max cut @ 90–99% floor."

### Email template — design partner (AI lab)

**Subject:** Cut RAG tokens before you embed — 15 min?

Hi {Name},

Saw you're building {RAG / support bot / internal KB} — quick one.

We built **Datter AI Hands-Off**: autonomous agents audit a doc corpus *before* embedding and find the **largest safe token reduction** at a quality floor you choose (e.g. 90% understanding on your test questions). Proof tab compares our cut vs random at the same token budget.

Hackathon demo (2 min): {LOOM_URL}

We also run a **Paper Summary Team** eval — multi-model exam on full vs compressed corpus (see `exam_results.json` on pilot).

If you're embedding PDFs in the next few weeks, we'd love a 15-min call and a pilot on one corpus — free audit export included.

{Your name}

---

## Track B — Seed investor (AI infra / dev tools)

### Target profile

- Pre-seed / seed; thesis in dev tools, AI infra, data quality, cost optimization  
- Comfortable with "building demo" + research flywheel  
- Cares about **input-gate** economics, not another dashboard

### Talk track (60 seconds)

> "AI spend compounds at the data layer before training or RAG. Datter is a **selection engine** — customer picks quality floor, we maximise token drop with eval proof. SKU is max safe reduction % at floor. Research (scorers, task-conditioned selection) pushes the Pareto frontier. Agent-company delivery: hands-off pipeline, audit trail, export. Wedge is RAG teams; expand to regulated KB. Tonight: working demo on real PDFs; production LLM judge next."

### Email template — investor intro

**Subject:** Datter — max token cut at quality floor (Hands-Off demo)

Hi {Name},

**Datter** sits at the input gate before embedding/training spend compounds. We're a **selection engine**, not dedup: the customer sets a quality floor (e.g. 90% understanding on eval Q&A); we find the **maximum token reduction** that preserves it — proven vs random cut at the same budget.

Built for Cursor Hands-Off London — seven autonomous agents, real PDF corpora, audit + export. Research flywheel (Adisorn scorer, task-conditioned selection) lifts max cut at the same floor.

2-min demo: {LOOM_URL}  
Deck / one-pager: [[Executive Finance Report]] (internal)

Open to a 20-min intro this week if AI infra / cost-at-data-layer fits your thesis.

{Your name}

---

## Track C — Plugin / partner (distribution + proof)

### Target profile

| Partner type | Examples | Integration angle |
|---|---|---|
| **Vector / RAG platform** | LangChain, LlamaIndex, vector DB vendors | Pre-ingestion audit step; export optimised chunks |
| **Embedding API** | OpenAI, Voyage, Cohere | "$ saved" ROI tied to their $/M |
| **Scorer / eval** | Custom rerankers, LLM-judge tools | Plugin slot in `datter/scorers/`; joint proof harness |

### Talk track (60 seconds)

> "Datter is the step **before** your stack embeds. We export an optimised corpus + JSON audit. Partners win on lower embed bills and cleaner retrieval. We're scorer-plugin shaped — baseline today, hybrid/Adisorn next. Looking for one integration partner to co-demo: ingest → Datter cut → your index."

### Email template — partner / plugin

**Subject:** Pre-embedding audit plugin — co-demo?

Hi {Name},

We built **Datter** — hands-off agents that audit a corpus and output the **max token cut** at a customer quality floor, with eval proof vs random baseline.

Natural fit: **before** {your product} indexes chunks — fewer tokens, same downstream Q&A quality. We export optimised corpus + manifest; scorer architecture is plugin-based (`baseline`, hybrid, research scorers).

Hackathon demo: {LOOM_URL}

Interested in a technical intro to explore a co-demo or scorer plugin slot?

{Your name}

---

## Outreach ops (tonight)

1. **Personalize** `{Name}`, `{RAG / support bot}`, `{LOOM_URL}` — paste from `HACKATHON.md` when uploaded  
2. **Send 3–5 emails per track** — quality over volume  
3. **Log replies** in [[HANDOFF]] or Slack — design partner > investor > partner for CEO sync  
4. **Never claim** production LLM judge accuracy; say "building demo — offline proxy; production harness on roadmap"  
5. **Strongest demo corpus for skeptics:** **Lab** project (~41% avoidable); **Government** for real-world PDF story  

---

## Objection quick answers

| Objection | Response |
|---|---|
| "We already dedup" | Dedup removes bytes; we optimise for **downstream understanding** at your floor |
| "50% cut is scary" | You pick the floor; we find **max** cut that meets it — not a fixed 50% |
| "How do you measure understanding?" | Project-scoped eval Q&A; tonight offline proxy, production LLM judge ([[Proof Loop Spec]]) |
| "Why not just use smaller chunks?" | Smaller chunks ≠ fewer tokens; we select **minimum sufficient subset** under budget |

---

## Links

- [[CEO Pitch Meeting 2026-06-25]]
- [[Business Model & Finance]]
- [[Business Strategy]]
- [[Hackathon Win Strategy]]
- [[HANDOFF]]
