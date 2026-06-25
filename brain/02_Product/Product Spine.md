---
type: product
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - product
  - strategy
  - datter
source: cursor-chat-2026-06-25
---

# Product Spine

## One-line definition

**Datter compiles a raw corpus into the smallest dataset that preserves downstream AI performance under a cost budget.**

## What the company actually is

The **selection engine** is the company. Dashboard, agents, and token calculators are packaging.

Datter is not merely deduplication or token counting. It is a **task-conditioned dataset optimisation engine**.

## Core technical objective

Maximise downstream quality per unit of data cost.

Usefulness is **relational and task-dependent**. The value of an item depends on:

- the downstream objective (task T)
- what information is already present in the selected set (S)

## Utility model

For every document or chunk *i*, conditioned on task T and already-selected data S:

```text
Value(i|S,T) =
  α·Relevance
+ β·Marginal Coverage
+ γ·Information Density
+ η·Structured Complexity
− δ·Redundancy
− μ·Noise
```

Then:

```text
Value per Cost(i) = Value(i|S,T) / (tokens, embedding cost, labelling cost, or GPU cost)
```

**Marginal value** is the key phrase. A paragraph may be useful once; the twentieth copy adds almost nothing.

## How Datter decomposes data

```text
Corpus
  → Documents
    → Sections
      → Semantic chunks
        → Features and embeddings
          → Similarity clusters
            → Selected minimum-sufficient subset
```

Score at three levels:

| Level | Signals |
|---|---|
| Document | source, age, authority, duplicates, overall relevance |
| Chunk | redundancy, task relevance, density, noise |
| Corpus | topic coverage, diversity, missing concepts, repeated clusters |

## Scoring dimensions

| Signal | Practical baseline (MVP) |
|---|---|
| Validity | parsing success, malformed text, empty content |
| Exact redundancy | normalised text hash |
| Semantic redundancy | TF-IDF / embedding similarity |
| Task relevance | similarity to task description and representative queries *(future)* |
| Novelty | distance from already-selected content *(future)* |
| Coverage | new topics/clusters covered by selection *(future)* |
| Information density | meaningful content per token; boilerplate penalties |
| Noise | OCR corruption, symbol spam, fragments *(future)* |
| Structured complexity | Adisorn research model *(plugin)* |
| Cost | tokens, embeddings, storage, labelling |

Do not collapse these into one mysterious number. Show component scores, confidence, and reasoning.

## Actions (product output)

Datter does not delete customer data. It produces an **optimised dataset and audit trail**.

| Condition | Action |
|---|---|
| Exact duplicate | Drop duplicate; retain canonical source |
| Very high semantic overlap | Consolidate cluster |
| Relevant but verbose/repetitive | Compress or rechunk |
| Low relevance and low novelty | Exclude from current pipeline |
| Novel but noisy or uncertain | Human review |
| High relevance and unique coverage | Keep |
| Rare edge-case content | Protect from automatic removal |

Prefer **extractive consolidation** over generative summarisation early (provenance, no hallucination).

## Selection algorithm (target — not MVP yet)

Do not independently keep everything above 0.7. That produces repetitive high-scoring piles.

Instead solve:

> **Maximise task coverage and useful information under a token or cost budget.**

Greedy hackathon-grade algorithm:

```python
selected = []
remaining = all_chunks

while token_budget_remaining:
    for chunk in remaining:
        marginal_value = (
            task_relevance(chunk)
            + new_topic_coverage(chunk, selected)
            + information_density(chunk)
            - semantic_overlap(chunk, selected)
            - noise(chunk)
        )
        score_per_token = marginal_value / token_count(chunk)

    choose chunk with highest score_per_token
    add to selected; remove from remaining
```

This is closer to **core-set selection / budgeted coverage optimisation** than basic data cleaning.

## What the user gives Datter (strong version)

```text
1. Raw document corpus
2. Task description
3. Representative questions or queries
4. Optional token/cost budget
5. Optional quality benchmark
```

Without task or queries, Datter can only estimate **structural quality**, not true usefulness.

## What Datter returns

```text
Original corpus:         1,240,000 tokens
Exact duplicates:         96,000 tokens
Near-duplicate content:    214,000 tokens
Boilerplate/noise:          61,000 tokens
Recommended corpus:        887,000 tokens
Reduction:                   28.5%
Retrieval quality delta:     -0.3%
Estimated annual saving:     £X
```

Plus: selected corpus, excluded corpus, duplicate clusters, action codes, reason codes, confidence, rollback manifest.

## How to prove the cut is valid

A score alone is not proof. For RAG, compare original vs reduced:

- retrieval recall@k
- mean reciprocal rank
- answer accuracy / faithfulness
- citation quality
- latency, embedded tokens, total cost

Run a **reduction curve** (0%, 10%, 20%, 30%, 40% cut) and find the Pareto point:

> Maximum cost reduction within agreed quality-loss tolerance.

Defensible claim:

> "Datter reduced corpus size by 31% while retrieval quality remained within 1% of baseline."

Not:

> "Datter knows this data is useless."

## Where Adisorn's model fits

Adisorn Panasawatwong's data-driven complexity score is **one component**:

```text
Datter utility =
  task relevance
+ marginal coverage
+ information density
+ structural complexity   ← Adisorn
− redundancy
− noise
− cost
```

Complexity alone cannot determine commercial usefulness. The moat:

> **Complexity science + task-conditioned marginal utility + measurable downstream ROI.**

## First wedge

```text
Raw corpus → Datter → minimum-sufficient corpus → embeddings / vector DB
```

First defensible milestone:

> **X% fewer embedded tokens with no material loss in retrieval quality.**

## Links

- Session archive: [[Cursor Session 2026-06-25]]
- Scorer plugins: [[Scorer Plugin Architecture]]
- MVP built: [[Hackathon MVP Summary]]
- Up: [[Project Map]]
