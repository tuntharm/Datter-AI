---
type: map
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - paper
  - research
  - map
  - datter
---

# Papers Map

## Purpose

This is the routing layer for Datter's AI-readable paper notes.

Use it for data usefulness, compression, data curation, deduplication, pretraining data selection, and token-waste research that directly informs Datter.

## Folder Layout

| Path | Use |
|---|---|
| `brain/01_Research/Papers/` | Structured markdown paper notes |
| `brain/attachments/papers/` | Optional PDFs supplied by Tharm |
| `brain/01_Research/Paper Queue.md` | What to read, skim, deepen, cite, or park |
| `brain/01_Research/Paper Intake Protocol.md` | Steps for adding a new paper |
| `brain/Templates/Paper Note.md` | Standard paper note template |
| `brain/Templates/Paper Deep Notes.md` | Optional overflow notes |

## Agent Routing Rules

- Start here before opening individual paper notes.
- Open [[Paper Queue]] when deciding what to read next.
- Open [[Paper Intake Protocol]] before processing a new PDF or arXiv link.
- Read only the paper notes directly relevant to the current question.
- Do not bulk-read `brain/01_Research/Papers/` or `brain/attachments/papers/`.
- Treat markdown notes as the agent-readable source of truth; PDFs are attachments.

## Topic Index

### Compression / data selection / curation

| Paper | Status | Why it matters |
|---|---|---|
| [[ZIP-FIT]] | skimmed | Compression-based task alignment for data selection |
| [[Predictive Data Selection]] | skimmed | Uses predictiveness of model losses as a data-value signal |
| [[Why Less is More Sometimes]] | to_read | Theory for when curated subsets outperform full datasets |
| [[Measuring Sample Importance in Data Pruning]] | to_read | Entropy-based sample importance for pruning language-model data |
| [[Understanding LLM Behaviors via Compression]] | to_read | Compression-theoretic view of scaling, knowledge, and hallucination |

### Deduplication / redundancy

| Paper | Status | Why it matters |
|---|---|---|
| [[SoftDedup]] | skimmed | Reweights duplicated/common data instead of hard deletion |
| [[Deduplicating Training Data Makes Language Models Better]] | skimmed | Baseline evidence for deduplication, memorization, and train-test overlap |
| [[SemDeDup]] | skimmed | Embedding-based semantic duplicate removal at web scale |

## Datter Implementation Links

| Concept | Current Code Surface |
|---|---|
| Gzip complexity proxy | `datter/scorers/baseline.py` |
| Exact duplicate handling | `datter/dedup.py` |
| Near duplicate handling | `datter/dedup.py` |
| Keep/drop/compress/review | `datter/scorers/baseline.py` |
| Avoidable token calculation | `datter/report.py` |
| Research scorer slot | `datter/scorers/adisorn_complexity.py`, `models/adisorn/README.md` |

## Links

- Up: [[Datter Brain Manager]]
- Queue: [[Paper Queue]]
- Intake: [[Paper Intake Protocol]]
- Product: [[Datter Source Documents]]
- Experiments: [[Experiment Map]]

