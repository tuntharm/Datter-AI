---
type: session
status: archived
created: 2026-06-25
updated: 2026-06-25
tags:
  - cursor
  - chat
  - handoff
  - datter
  - home-workspace
agent_access: project
---

# Cursor Session 2026-06-25 Home Workspace Chat

Archive of a Cursor chat that ran on the **home workspace** (not `/Users/tharm/dev/datter`). Tharm asked to move continuity to the Datter repo so the next chat can read it.

## Why this note exists

- Home workspace chats do not attach to the project repo by default.
- Durable context from that chat is captured here and in [[Business Strategy]].
- New chats should open **`/Users/tharm/dev/datter`** and start from `CHAT_START.md`.

## Session topics

### 1. Business side / GTM

Discussed who pays, uniqueness, and whether to sell to datacenters vs AI companies vs banks.

**Conclusions captured in [[Business Strategy]]:**

- Wedge = pre-tokenisation / pre-ingestion validation
- First buyer = AI builder / ML engineer (RAG / fine-tuning ingest)
- Datacenter = later channel, not founding ICP
- B2C framing is wrong; PLG B2B is the model
- Uniqueness = economic usefulness layer + learnability + regime model, not dedup alone

### 2. Obsidian 2nd brain — Codex prompt (everyday vault)

Tharm asked for a Codex prompt to build an AI-readable paper/knowledge layer.

**Important boundary:**

- That prompt targets **`/Users/tharm/everyday-life-brain`** (general second brain).
- Datter-specific papers already live in **`/Users/tharm/dev/datter/brain/01_Research/`**.
- Do not merge the two vaults. Everyday brain routes to Datter repo for Datter detail.

The full Codex prompt was delivered in chat. If not yet executed in everyday-life-brain, add a task to `/Users/tharm/everyday-life-brain/REQUESTS.md`.

Everyday brain already has: maps, `AI Brain Manager`, `Linking Standard`, `Reading Log` pattern to mirror for papers.

### 3. Hackathon tech partners

Screenshot: Tech Partners credits page (Cursor Hands Off).

| Partner | Action for Datter MVP |
|---|---|
| **Cursor** | Claim credits from Discord — already building here |
| **Manus AI** | Optional — get QA code if it helps agent-autonomy demo |
| **Modal** | Defer — GPU scoring / Adisorn model later |
| **Supabase** | Defer — persistence / team dashboard later |
| **PayPal** | Skip — billing out of MVP scope |
| **Wassist** | Skip — WhatsApp unrelated to wedge |

Local Streamlit demo does not require cloud partner setup to pitch.

## Related prior session

Implementation + product spine from an earlier session the same day:

- [[Cursor Session 2026-06-25]] — MVP build, scorer plugins, compression papers
- [[Product Spine]] — selection engine north star
- [[Hackathon MVP Summary]] — what shipped

## Open questions still live

- [ ] Execute everyday-vault paper layer Codex prompt (if desired)
- [ ] Claim Cursor hackathon credits
- [ ] Evaluate Manus QA code for demo fit
- [ ] Pick one vertical proof corpus for 30%+ reduction claim
- [ ] Confirm first buyer interviews align with AI-builder wedge

## Links

- Up: [[Project Map]]
- Strategy: [[Business Strategy]]
- Repo entry: `/Users/tharm/dev/datter/CHAT_START.md`
- Everyday router: `/Users/tharm/everyday-life-brain/02_Projects/Datter_AI/Datter AI Home.md`
