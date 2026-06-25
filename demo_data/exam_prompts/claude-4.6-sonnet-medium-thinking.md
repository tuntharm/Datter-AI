# Paper Summary Team — claude-4.6-sonnet-medium-thinking

**Model slot:** `sonnet` · **Cursor slug:** `claude-4.6-sonnet-medium-thinking`

You are the **examinee** in the Paper Summary Team loop. Answer each question using
**only** the COMPRESSED corpus below (≤120 words per answer). An examiner built
reference answers from the FULL corpus; your answers will be scored against them.

## COMPRESSED CORPUS

```
# FNO Surrogate Model for Beam Transient Response

This work develops a Fourier Neural Operator surrogate for predicting transient displacement in Euler-Bernoulli beams subject to moving loads.

Compared to explicit Newmark time integration, our approach achieves roughly 40 times faster inference with L2 error below 2% on held-out velocity conditions.

Main results:
- Combined physics-informed and data-driven training objective
- Generalizes to load speeds not seen during training
- Suitable for real-time structural health monitoring on edge devices

We evaluate on a 12 metre simply supported steel I-beam using 500 training and 100 validation load trajectories with speeds from 5 to 25 metres per second.

---

# Corporate Data Retention Policy

All rights reserved.

Confidential — do not distribute.

This document describes the standard terms and conditions for data retention within the organisation.

Employees must comply with all applicable regulations.

See appendix A for definitions.

See appendix B for escalation procedures.

No action required unless instructed by legal.

This policy may be updated without notice.

Terms and conditions apply to all subsidiaries and contractors.

Lorem ipsum dolor sit amet, consectetur adipiscing elit.

Repeated boilerplate text repeated boilerplate text repeated boilerplate text.

---

Datter Demo: Dense Technical Specification
FNO: 4 Fourier layers, width 64, modes 16.

Loss = L_data + 0.1*L_PDE + 0.05*L_bc
Training: AdamW 1e-3, batch 32, 200 epochs.

Inference: 3.2ms/A100, 18ms Jetson Orin.

OOD generalization: 1.8 percent mean L2 error.

---

Meeting notes — weekly sync

As discussed, we should follow up on the thing from last week.

No action required for now.

Action items: TBD.

We need to circle back and touch base on the roadmap.

Good meeting overall.

Let's take this offline and loop in the team.

Follow up next week.

As discussed previously.

---

# Compression ladder — Structural audit lab

Generated: 2026-06-25 · Mode: **offline**

## Best at quality floor

- **Max safe compression:** 96.0% (target 10%)
- **Min score:** 45.4% (floor 90%)
- **Tokens saved:** 9,722 (10,127 → 405)

## Ladder

| Target | Actual cut | Min score | Passed | Tokens kept |
|-------:|-----------:|----------:|:------:|------------:|
| 10% | 96.0% | 45.4% | ✗ | 405 |

*Offline TF-IDF judge fallback — production claims require live multi-model run.*

---

# Compression ladder — lab project

**Run:** 2026-06-25 · **Quality floor:** 90% · **Judge:** offline TF-IDF fallback (no API keys)

## Summary

| Metric | Value |
|--------|-------|
| Best compression at floor | **None** — no step met 90% min score |
| Best min score observed | 85.9% at 40.9% actual reduction (minimum achievable on demo corpus) |
| Steps run | 1 (stopped early: min_score &lt; floor) |
| API mode | `offline` |

**Judge note:** API required for Paper Summary Team production run — using TF-IDF judge fallback.

**Corpus note:** Ladder evaluated on canonical demo files `01–06` only.

`exam_prompts/*.md` in `demo_data/` are ingested by the lab project but excluded here (they pollute scores when included).

`exam_corpus/` is already skipped by ingest.

## Ladder table

| Step | Target reduction | Actual reduction | Tokens full | Tokens compressed | Min score | Passed |
|------|------------------|------------------|-------------|-------------------|-----------|--------|
| 1 | 10% | 40.9% | 685 | 405 | 85.9% | No |

Steps 2–8 were not run (early stop at step 1).

At targets 10–40%, actual reduction stays at 40.9% (4 non-drop chunks, 405 tokens).

Higher targets increase reduction (55.9% at 50%, 76.4% at 70%) but scores fall further (77.8% → 65.8%).

## Root cause

1.

---

1.

**Baseline scorer drops canonical duplicates:** `01_unique_research_note.md` is `is_canonical=True` but gets `recommended_action=drop` because `redundancy ≥ 0.92` fires before the canonical guard.

Q1 (unique research findings) cannot be answered from compressed corpus.

2.

**Selection skips all `drop` chunks:** Minimum compression on demo corpus is ~41%, not the 10–20% ladder start the experiment intended.

3.

**Offline judge ceiling:** TF-IDF overlap judge scores ~86% max on this corpus even at minimum compression; live multi-model judge needed for production floor checks.

## Compressor recommendation

1.

**Keep canonical chunks** even when redundancy is high — adjust `recommend_action()` in `baseline.py` so `is_canonical` bypasses the `redundancy ≥ 0.92` drop rule.

2.

**Query-relevance boost before cut:** Ensure `apply_query_relevance_boost` lifts query-critical chunks (e.g.

unique note for q1) above drop threshold.

3.

**Exclude eval artifacts from ingest:** Skip `exam_prompts/` (and already `exam_corpus/`) in `ingest_folder` so lab reruns stay clean.

4.

**Re-run ladder with API keys** after scorer fix for authoritative 90% floor measurement.
```

## Questions

### q1 (1/4)

**Query:** What are the key research findings in the unique note?

**Reference (FULL corpus — do not peek when answering):** ```

## Questions

### q1 (1/4)

**Query:** What are the key research findings in the unique note? **Reference (FULL corpus — do not peek when answering):** ```

## Questions

### q1 (1/4)

**Query:** What are the key research findings in the unique note? **Reference (FULL corpus — do not peek when answering):** ```

## Questions

### q1 (1/4)

**Query:** What are the key research findings in the …

**Your answer (COMPRESSED only):**

### q2 (2/4)

**Query:** What policy requirements are documented?

**Reference (FULL corpus — do not peek when answering):** **Reference (FULL corpus — do not peek when answering):** ```

## Questions

### q1 (1/4)

**Query:** What are the key research findings in the …

**Your answer (COMPRESSED only):**

### q2 (2/4)

**Query:** What policy requirements are documented? **Reference (FULL corpus — do not peek when answering):** **Query:** What policy requirements are documented? ```

## Questions

### q1 (1/4)

**Query:…

**Your answer (COMPRESSED only):**

### q3 (3/4)

**Query:** What technical specifications are defined?

**Reference (FULL corpus — do not peek when answering):** **Reference (FULL corpus — do not peek when answering):** **Reference (FULL corpus — do not peek when answering):** ### q2 (2/4)

**Query:** What policy requirements are …

**Your …

**Your answer (COMPRESSED only):**

### q3 (3/4)

**Query:** What technical specifications are defined? **Reference (FULL corpus — do not peek when answering):** **Reference (FULL corpus — do not peek when answering):…

**Your answer (COMPRESSED only):**

### q4 (4/4)

**Query:** Are there duplicate documents in this corpus?

**Reference (FULL corpus — do not peek when answering):** **R…

**Your answer (COMPRESSED only):**

### q4 (4/4)

**Query:** Are there duplicate documents in this corpus? **Reference (FULL corpus — do not peek when answering):** **Query:** Are there duplicate documents in this corpus? **Reference (FULL corpus — do not peek when answering):** **Reference (FULL corpus — do not peek when answeri…

**Your answer (COMPRESSED only):** **Query:** Are there dupl…

**Your answer (COMPRESSED only):**


---

## Scoring template (for examiner / orchestrator)

Return JSON after you answer:

```json
{"answers": [{"id": "q1", "answer": "..."}, ...]}
```
