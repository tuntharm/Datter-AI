---
type: source_index
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - product
  - source
  - datter
---

# Datter Source Documents

## Project Sources

| Source | Use |
|---|---|
| Root `README.md` | Public quick start |
| `AGENTS.md` | Agent routing for this repo |
| `app.py` | Streamlit demo UI |
| `datter/agent.py` | Autonomous analysis pipeline |
| `datter/scorers/` | Pluggable scoring (baseline, Adisorn, hybrid) |
| `demo_data/` | Pitch/demo corpus |
| `models/adisorn/README.md` | Research model integration contract |

## Brain / Session Sources

| Note | Use |
|---|---|
| [[Product Spine]] | Company-level product definition (task-conditioned selection) |
| [[Hackathon MVP Summary]] | What M1 shipped and how to run it |
| [[Scorer Plugin Architecture]] | BaseScorer interface and Adisorn wrapper design |
| [[Cursor Session 2026-06-25]] | Full archive of 2026-06-25 Cursor chat |
| [[HANDOFF]] | Agent handoff log |
| [[REQUESTS]] | Active task queue |

## External Project Context

- Everyday-life project note: `/Users/tharm/everyday-life-brain/02_Projects/Datter_AI/Datter AI Home.md`
- Everyday-life source index: `/Users/tharm/everyday-life-brain/02_Projects/Datter_AI/Datter AI Source Documents.md`
- Local project root: `/Users/tharm/dev/datter`

The everyday-life brain should link here for detailed Datter context rather than duplicating the research layer.

## Paper Evidence

| Paper | Why Datter cares |
|---|---|
| [[ZIP-FIT]] | Compression-based task alignment supports usefulness scoring before expensive AI work |
| [[Predictive Data Selection]] | Data that predicts downstream capability is a concrete version of "data that matters" |
| [[SoftDedup]] | Supports graded recommendations such as downweight or compress instead of only delete |
| [[Deduplicating Training Data Makes Language Models Better]] | Foundational deduplication evidence for redundancy cost and memorization risk |
| [[SemDeDup]] | Semantic deduplication baseline Datter should compare against |
| [[Why Less is More Sometimes]] | Theory candidate for when curated subsets beat full datasets |
| [[Understanding LLM Behaviors via Compression]] | Compression-theoretic framing for learnable structure |
| [[Measuring Sample Importance in Data Pruning]] | Entropy-based sample-importance signal; metadata mismatch with old Tan/compression label needs reconciliation |

## Handling Rule

Datter startup and pitch material may be commercially sensitive. Keep detailed product, scoring, and pitch strategy in this repo or explicit private notes unless Tharm asks to publish.

## Links

- Up: [[Project Map]]
- Research: [[Papers Map]]
- Experiments: [[Experiment Map]]

