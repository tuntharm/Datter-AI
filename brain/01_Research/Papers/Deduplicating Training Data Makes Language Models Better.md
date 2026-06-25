---
type: paper
status: skimmed
created: 2026-06-25
updated: 2026-06-25
title: "Deduplicating Training Data Makes Language Models Better"
authors:
  - Katherine Lee
  - Daphne Ippolito
  - Andrew Nystrom
  - Chiyuan Zhang
  - Douglas Eck
  - Chris Callison-Burch
  - Nicholas Carlini
year: 2022
venue: ACL 2022
arxiv: "2107.06499"
doi: "10.48550/arXiv.2107.06499"
url: "https://arxiv.org/abs/2107.06499"
source_pdf: definition_pending
tags:
  - paper
  - deduplication
  - language-models
  - data-quality
projects:
  - datter
read_depth: skim
confidence: medium
agent_access: default
aliases:
  - Lee et al. 2022 deduplication
---

# Deduplicating Training Data Makes Language Models Better

## One-line thesis

Near-duplicate training data increases memorization and train-test overlap; deduplication can improve efficiency and evaluation quality.

## Why it matters to Datter

This is a foundational baseline for Datter's redundancy story: duplicate data wastes compute and can create model-risk problems beyond simple storage cost.

## Problem

Language-model datasets contain near-duplicates and repetitive substrings that affect training, generation, memorization, and evaluation.

## Method (5 bullets max)

- Identify near-duplicate examples and repetitive substrings in language-model datasets.
- Build tools for dataset deduplication.
- Measure memorized text generation.
- Measure train-test overlap.
- Compare training efficiency and model accuracy after deduplication.

## Key results (5 bullets max)

- The abstract reports over 1 percent of unprompted outputs copied verbatim from training data before deduplication.
- It reports a 10x reduction in memorized text emission after deduplication.
- It reports train-test overlap affecting over 4 percent of standard validation data.
- It reports fewer training steps for same or better accuracy.

## Limitations

- Abstract-level note only.
- This is hard/near deduplication, not general usefulness scoring.
- It does not directly score novelty or downstream task value.

## Datter implications

- Use as baseline evidence for the cost and risk of redundant data.
- Current `datter/dedup.py` should remain transparent and test-covered.

## Mechanisms / equations worth remembering

- Near-duplicate detection.
- Repetitive substring detection.
- Train-test overlap measurement.

## Quotes or numbers to cite

- arXiv: `2107.06499`
- Accepted to ACL 2022 according to arXiv comments.
- Abstract numbers: over 1 percent copied outputs; 10x less memorized emission; over 4 percent validation overlap.

## Related papers

- [[SemDeDup]]
- [[SoftDedup]]
- [[ZIP-FIT]]

## Open questions

- Which deduplication primitive should Datter implement first for local document folders?
- How should Datter distinguish harmful duplication from useful repetition?

## Links

- Up: [[Papers Map]]
- Experiments: [[Experiment Map]]
- Source: https://arxiv.org/abs/2107.06499

