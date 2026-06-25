---
type: paper
status: skimmed
created: 2026-06-25
updated: 2026-06-25
title: "ZIP-FIT: Embedding-Free Data Selection via Compression-Based Alignment"
authors:
  - Elyas Obbad
  - Iddah Mlauzi
  - Brando Miranda
  - Rylan Schaeffer
  - Kamal Obbad
  - Suhana Bedi
  - Sanmi Koyejo
year: 2024
venue: arXiv
arxiv: "2410.18194"
doi: "10.48550/arXiv.2410.18194"
url: "https://arxiv.org/abs/2410.18194"
source_pdf: definition_pending
tags:
  - paper
  - compression
  - data-selection
projects:
  - datter
read_depth: skim
confidence: medium
agent_access: default
aliases:
  - ZIP FIT
  - Embedding-Free Data Selection via Compression-Based Alignment
---

# ZIP-FIT

## One-line thesis

Gzip-based compression alignment can select task-relevant training data without embeddings.

## Why it matters to Datter

This is one of the cleanest public references for Datter's claim that compression can expose which data is worth using before more expensive AI work begins.

## Problem

Data selection often ignores the target task or depends on noisy proxies such as hashed n-grams or embeddings that may not capture task alignment.

## Method (5 bullets max)

- Compare candidate training data against a target task distribution.
- Use gzip compression as the alignment signal.
- Select data that compresses well with the target distribution.
- Evaluate on task-specific adaptation settings.
- Compare against baselines including DSIR and D4.

## Key results (5 bullets max)

- The abstract reports lower cross-entropy loss up to 85.1 percent faster than baselines.
- Selection is reported as up to 65.8 percent faster than DSIR.
- It is reported as two orders of magnitude faster than D4.
- Smaller, better-aligned data can outperform larger but less targeted data.

## Limitations

- Abstract-level note only.
- Evidence is centered on specific tasks such as autoformalization and Python code generation.
- Gzip alignment may not directly solve noisy enterprise-document settings.

## Datter implications

- Prototype a target-aware compression score.
- Compare it against the current generic gzip complexity proxy in `datter/scorers/baseline.py`.

## Mechanisms / equations worth remembering

- Compression-based alignment between target distribution and candidate data.
- Task-aware data selection without embedding generation.

## Quotes or numbers to cite

- arXiv: `2410.18194`
- Abstract numbers: 85.1 percent faster to lowest cross-entropy loss; 65.8 percent faster selection than DSIR.

## Related papers

- [[Predictive Data Selection]]
- [[Understanding LLM Behaviors via Compression]]
- [[Why Less is More Sometimes]]

## Open questions

- Can this be adapted to pre-tokenization document triage for RAG?
- What does the score look like for mixed PDFs, markdown, and noisy enterprise documents?

## Links

- Up: [[Papers Map]]
- Experiments: [[Experiment Map]]
- Source: https://arxiv.org/abs/2410.18194

