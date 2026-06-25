---
type: standard
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - paper
  - intake
  - standard
  - datter
---

# Paper Intake Protocol

Use this when adding a new paper, PDF, arXiv link, DOI, or Datter-relevant research source.

## Route First

| Paper Type | Durable Home |
|---|---|
| Datter data-usefulness / compression / dedup / token-waste paper | `brain/01_Research/Papers/` |
| Product-specific source or deck evidence | [[Datter Source Documents]] |
| PhD beam-surrogate / structural dynamics paper | PhD brain via `/Users/tharm/.codex/brain_router.md` |
| General life or non-Datter learning | Everyday-life brain |

## Intake Steps

1. Read [[Papers Map]] and [[Paper Queue]].
2. Decide whether the paper belongs in this Datter brain or another brain.
3. If a PDF is provided, store it under `brain/attachments/papers/<slug>.pdf`.
4. Create `brain/01_Research/Papers/<Short Title>.md` from [[Paper Note]].
5. Fill metadata from arXiv, DOI, venue page, or the PDF front page.
6. Keep the first note short: thesis, why it matters, method, results, limits, relevance, links.
7. Mark unknown fields as `definition_pending`; do not guess.
8. Add or update a row in [[Paper Queue]].
9. Add implementation implications to [[Experiment Map]] only when there is a real test to run.
10. Run `python3 brain/scripts/check_brain.py`.

## Depth Levels

| Depth | Use |
|---|---|
| `none` | Metadata stub only |
| `skim` | Abstract-level structured note with uncertainty |
| `full` | Deep read with claims, equations, results, and critique |

If the note grows beyond 150 lines, create `<Short Title> - Deep Notes.md` using [[Paper Deep Notes]] and link it from the main note.

## Links

- Up: [[Papers Map]]
- Queue: [[Paper Queue]]
- Project: [[Project Map]]

