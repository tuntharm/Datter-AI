---
type: ai_manager
status: active
created: 2026-06-25
updated: 2026-06-25
tags:
  - ai
  - system
  - datter
---

# Datter Brain Manager

This note tells Codex, Claude, and future agents how to route Datter work.

## Question Type Routing

| Question Type | Read First | Durable Output Belongs |
|---|---|---|
| Multi-agent orchestration / hackathon run | [[Orchestration Plan]], [[REQUESTS]], [[HANDOFF]] | [[Orchestration Plan]] sub-notes or [[HANDOFF]] |
| CEO / CTO / CPO chat roles | [[Agent Team Model]], [[CEO Discussion Archive 2026-06-25]] | [[HANDOFF]] |
| Project UX / create project first | [[Project Model]] | [[Project Model]] or [[REQUESTS]] |
| Proof demo / LLM judge / vertical PDFs | [[Proof Loop Spec]], [[Vertical Demo Corpus]] | [[Proof Loop Spec]] or code + `demo_verticals/` |
| Hackathon judging / demo script | [[Hackathon Win Strategy]] | [[Hackathon Win Strategy]] or [[HANDOFF]] |
| New Cursor chat / continuing from home workspace | `CHAT_START.md`, [[HANDOFF]], [[Cursor Session 2026-06-25 Home Workspace Chat]] | This repo only |
| What is Datter and what is current state? | [[Project Map]], then root `README.md` | [[Project Map]] or root `README.md` |
| Business model / GTM / who pays | [[Business Strategy]] | [[Business Strategy]] |
| What source/code files matter? | [[Source Map]] | Code, tests, or source map update |
| What papers do we know about X? | [[Papers Map]], then [[Paper Queue]] | Paper note in `brain/01_Research/Papers/` |
| Add/process a new paper | [[Paper Intake Protocol]] | New paper note and [[Paper Queue]] |
| What should we test next? | [[Experiment Map]], then [[Paper Queue]] if research-driven | Experiment note or `REQUESTS.md` |
| What does the MVP currently prove? | [[Experiment Map]], root `README.md`, `demo_data/README.md` | Experiment summary or README |
| What should Codex build? | `REQUESTS.md`, [[Source Map]] | Code/tests plus `REQUESTS.md` completion note |
| What should Claude think through? | `HANDOFF.md`, [[Project Map]], [[Papers Map]] | Handoff entry or project note |
| Is this everyday/life/admin context? | `/Users/tharm/everyday-life-brain/00_System/AI Brain Manager.md` | Everyday-life brain only |
| Is this PhD beam-surrogate context? | `/Users/tharm/.codex/brain_router.md`, then PhD bridge | PhD vault/repo only |

## Agent Workflow

1. Classify the request.
2. Read the smallest map that routes the request.
3. Open only targeted notes, code files, or paper notes.
4. Update the durable note or code file that owns the result.
5. Add a handoff entry if another agent needs context.
6. Run `python3 brain/scripts/check_brain.py` after brain edits.

## Memory Placement

- Product direction and source context: `brain/02_Product/`
- Papers and research synthesis: `brain/01_Research/`
- Experiment plans and result summaries: `brain/03_Experiments/`
- Agent coordination: `brain/HANDOFF.md` and `brain/REQUESTS.md`
- Implementation: root app files, `datter/`, `tests/`, `demo_data/`

## Do Not

- Do not bulk-read `brain/01_Research/Papers/`.
- Do not duplicate detailed Datter research into the everyday-life brain.
- Do not import PhD beam-surrogate notes here.
- Do not leave durable project decisions only in chat.

