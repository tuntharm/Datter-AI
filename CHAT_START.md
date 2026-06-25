# CHAT_START.md — Read this first in a new Cursor chat

Open this workspace at **`/Users/tharm/dev/datter`**, not home.

This file routes a fresh agent to the right project memory after a chat that started on the home workspace.

## Read order (smallest first)

1. `AGENTS.md` — repo working agreement
2. `brain/HANDOFF.md` — latest decisions and blockers (newest on top)
3. `brain/02_Product/Cursor Session 2026-06-25 Home Workspace Chat.md` — archived home-workspace chat
4. One targeted note based on your question:

| If you are working on… | Read next |
|---|---|
| **Orchestrate multi-agent / hackathon build** | `brain/02_Product/Orchestration/Orchestration Plan.md`, then `brain/REQUESTS.md` |
| CEO / CTO / CPO roles | `brain/02_Product/Orchestration/Agent Team Model.md` |
| Create project / upload UX | `brain/02_Product/Orchestration/Project Model.md` |
| Proof loop / vertical PDF demo | `brain/02_Product/Orchestration/Proof Loop Spec.md` |
| Product / company direction | `brain/02_Product/Product Spine.md` |
| Business / GTM / buyers | `brain/02_Product/Business Strategy.md` |
| Hackathon demo / MVP | `brain/02_Product/Orchestration/Hackathon Win Strategy.md` |
| Scoring / Adisorn plugin | `brain/02_Product/Scorer Plugin Architecture.md` |
| Papers / research | `brain/01_Research/Papers Map.md` |
| Code / app | `README.md`, then `datter/` |

## What the home-workspace chat covered

1. **Business strategy** — who pays, B2B wedge, bank vs AI lab vs datacenter, GTM phases
2. **Obsidian paper layer** — Codex prompt for everyday-life brain (not this repo)
3. **Hackathon tech partners** — Cursor + Manus claim now; Modal/Supabase/PayPal/Wassist later

## Boundaries

- **Datter detail** lives in `brain/` inside this repo.
- **Everyday life / admin** lives in `/Users/tharm/everyday-life-brain/` — link only, do not duplicate.
- **PhD research** lives in the PhD vault/repo — see everyday `PhD Bridge.md`.

## Quick repo state

- Local Streamlit MVP: `streamlit run app.py`
- Tests: `pytest tests/ -q`
- Brain check: `python3 brain/scripts/check_brain.py`

## Cursor chat roles (2026-06-25)

| Tab | Role |
|---|---|
| Datter — CEO | Main; strategy + orchestrate via HANDOFF / REQUESTS |
| Datter — CTO | Build; read Orchestration Plan + REQUESTS |
| Datter — CPO | UX rare; Project Model + Proof Loop Spec |

## Suggested first message in the new chat

**CEO:**
```text
Read brain/HANDOFF.md and brain/02_Product/Orchestration/Orchestration Plan.md. You are CEO — coordinate via HANDOFF and REQUESTS.
```

**CTO:**
```text
Read brain/REQUESTS.md and brain/02_Product/Orchestration/. Implement P0 queue. Baseline scorer only; no Adisorn.
```
