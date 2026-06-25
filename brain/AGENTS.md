# AGENTS.md - Datter Brain Rules

## Scope

This folder is Datter's project-local brain. It is not a general personal vault.

Use it for:

- Datter product memory
- Datter source documents and pitch context
- Data usefulness, compression, curation, deduplication, and token-waste research
- Experiment plans, validation results, and implementation decisions
- Agent handoffs and concrete project requests

Do not use it for:

- Tharm's everyday life/admin memory
- PhD beam-surrogate research details
- Raw private PDFs or confidential third-party data without an explicit handling note

## Start Here

1. `00_System/Datter Brain Manager.md`
2. `00_System/Project Map.md`
3. `00_System/Source Map.md`
4. Target map for the question

## Privacy

Any note with `agent_access: explicit_only` or tag `private` requires an explicit user request before reading or editing.

## Verification

After edits, run:

```bash
python3 brain/scripts/check_brain.py
```

