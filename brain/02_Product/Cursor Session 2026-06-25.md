---
type: session
status: archived
created: 2026-06-25
updated: 2026-06-25
tags:
  - cursor
  - chat
  - handoff
  - datter
agent_access: project
---

# Cursor Session 2026-06-25

Archive of the Cursor planning + implementation session that produced the Datter hackathon MVP and product spine.

## Session arc

1. **Milestone 1 plan** — local Streamlit prototype, folder upload, chunking, dedup, scoring, dashboard
2. **Hackathon context** — Cursor Hands Off London; Datter AI Hands-Off; agent run log; judging criteria
3. **Scorer plugin architecture** — BaseScorer, baseline, Adisorn wrapper, hybrid; models/adisorn/
4. **Compression research (2023–2026)** — informed baseline complexity proxy
5. **MVP implementation** — full repo at `/Users/tharm/dev/datter`
6. **ChatGPT product spine review** — marginal value, task conditioning, proof via reduction curve

## Key decisions

| Decision | Choice | Rationale |
|---|---|---|
| Repo location | `/Users/tharm/dev/datter` | Matches other dev projects |
| UI | Streamlit | Fast, pitchable, local-first |
| Near-dup detection | TF-IDF cosine (sklearn) | No model download for demo |
| Complexity proxy (interim) | Gzip compression ratio | MDL-aligned; no API keys |
| Adisorn integration | Plugin wrapper with graceful fallback | Model format unknown |
| Scorer modes | baseline / adisorn / hybrid | Sidebar selector |
| Product company thesis | Selection engine > dashboard | ChatGPT spine adopted |

## Compression papers referenced (2023–2026)

| Paper | arXiv / venue | Use in Datter |
|---|---|---|
| Measuring Sample Importance in Data Pruning | [2406.14124](https://arxiv.org/abs/2406.14124) | Cross-entropy ≈ MDL; prune low description length |
| ZIP-FIT | [2410.18194](https://arxiv.org/abs/2410.18194) | Gzip NCD for task-aligned selection |
| SoftDedup | [2407.06654](https://arxiv.org/abs/2407.06654) | Reweight vs hard drop |
| PreSelect | ICML 2025 | Compression efficiency predicts downstream value |
| Why Less is More (Sometimes) | [2511.03492](https://arxiv.org/abs/2511.03492) | When curated subsets beat full data |
| Understanding LLM Behaviors via Compression | [2504.09597](https://arxiv.org/html/2504.09597) | Kolmogorov / scaling law framing |
| KoLMogorov Test | [2503.13992](https://arxiv.org/html/2503.13992) | Code-gen as complexity upper bound |
| LMCompress / Understanding is Compression | [2407.07723](https://arxiv.org/pdf/2407.07723) | LLM-based compression paradigm |

Seed notes exist under `brain/01_Research/Papers/`.

## ChatGPT product spine — assessment

**Adopted as north star.** Key upgrades over MVP-only framing:

- Marginal value (not independent chunk scores)
- Task-conditioned usefulness
- Budgeted subset selection (greedy score-per-token)
- Proof via reduction curve + RAG metrics
- Adisorn complexity as one signal, not oracle

**MVP remains valid wedge:** proves structural waste exists before AI spend.

## Files created in this session

```text
app.py
datter/{models,agent,ingest,chunking,dedup,token_cost,report}.py
datter/scorers/{base,baseline,adisorn_complexity,hybrid}.py
models/adisorn/README.md
demo_data/* (6 files)
tests/*
README.md, requirements.txt, pytest.ini, AGENTS.md
brain/ (project memory — pre-existing, extended)
```

## Open questions carried forward

- [ ] Adisorn model format and output semantics
- [ ] Representative queries / task description for task-conditioned scoring
- [ ] RAG eval harness for reduction curve
- [ ] Rename actions to exclude/consolidate vs drop/compress?

## Derived docs in this repo

- [[Product Spine]] — company-level product definition
- [[Scorer Plugin Architecture]] — plugin design
- [[Hackathon MVP Summary]] — what shipped
- [[HANDOFF]] — agent communication log

## Links

- Up: [[Project Map]]
- Product: [[Datter Source Documents]]
- Experiments: [[Experiment Map]]
