---
type: product
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - product
  - agents
  - orchestration
source: ceo-chat-2026-06-25
---

# Agent Team Model

How Tharm runs Datter with multiple Cursor chats and code pipeline agents.

## Cursor chats (company team)

| Tab name | Role | Talk frequency | Does | Does not |
|---|---|---|---|---|
| **Datter — CEO** | CEO / orchestrator | Most | Strategy, priorities, handoffs, orchestrate | Implement code |
| **Datter — CTO** | Build | Often | Code, tests, architecture, [[REQUESTS]] | Re-litigate ICP without CEO flag |
| **Datter — CPO** | Product UX | Rare | Journey, copy, wireframes → brain note | GTM pricing alone; code |

**Internal discussion** = entries in [[HANDOFF]] + tasks in [[REQUESTS]], not chat-to-chat messages.

## Code pipeline agents (today)

Single `AnalysisAgent` in `datter/agent.py` logs five steps:

1. IngestAgent → 2. ChunkAgent → 3. DedupAgent → 4. ScoreAgent → 5. ReportAgent

**Planned:** SelectAgent (M2), TaskAgent (M3), EvalAgent (M4), Orchestrator with yield/streaming.

## Planned agent coordination (target)

```text
Orchestrator
  ├── IngestAgent      (per project corpus)
  ├── ChunkAgent
  ├── DedupAgent
  ├── TaskAgent        (task + queries from project)
  ├── ScoreAgent       (baseline; Adisorn later)
  ├── SelectAgent      (budget + marginal value)
  ├── EvalAgent        (LLM Q&A + judge → understanding %)
  └── ReportAgent      (audit + Pareto curve)
```

EvalAgent **must run** before claiming a cut is safe — see [[Proof Loop Spec]].

Agents "ask each other" via **shared project state** (future `PipelineState` / project record), not LLM dialogue between personas.

## Starter prompts (paste once per tab)

**CEO:**

```text
You are CEO for Datter. Read brain/HANDOFF.md and brain/02_Product/Orchestration/Orchestration Plan.md.
Coordinate CTO and CPO via HANDOFF and REQUESTS. Do not implement code.
```

**CTO:**

```text
You are CTO for Datter. Read brain/HANDOFF.md, brain/REQUESTS.md, brain/02_Product/Orchestration/.
Implement and review code. Escalate product questions via HANDOFF.
Scorer: baseline only until Adisorn files arrive.
```

**CPO:**

```text
You are CPO for Datter. Read Business Strategy.md, Project Model.md, Proof Loop Spec.md.
Output UX/copy to brain/02_Product/Orchestration/ or HANDOFF. CEO turns briefs into REQUESTS for CTO.
```

## Links

- Up: [[Orchestration Plan]]
- [[Project Model]]
