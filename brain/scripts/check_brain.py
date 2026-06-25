#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
BRAIN = ROOT / "brain"
PAPERS = BRAIN / "01_Research" / "Papers"

REQUIRED = [
    "AGENTS.md",
    "brain/AGENTS.md",
    "brain/README.md",
    "brain/HANDOFF.md",
    "brain/REQUESTS.md",
    "brain/00_System/Datter Brain Manager.md",
    "brain/00_System/Project Map.md",
    "brain/00_System/Source Map.md",
    "brain/01_Research/Papers Map.md",
    "brain/01_Research/Paper Queue.md",
    "brain/01_Research/Paper Intake Protocol.md",
    "brain/02_Product/Datter Source Documents.md",
    "brain/03_Experiments/Experiment Map.md",
    "brain/Templates/Paper Note.md",
    "brain/Templates/Paper Deep Notes.md",
]

PAPER_REQUIRED_KEYS = ["type", "title", "status", "tags"]
PAPER_REQUIRED_SECTIONS = [
    "## One-line thesis",
    "## Why it matters to Datter",
    "## Links",
]

WIKILINK = re.compile(r"\[\[([^\]|#]+)")


def all_markdown_files() -> list[Path]:
    return [p for p in BRAIN.rglob("*.md")]


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    try:
        _, block, _ = text.split("---\n", 2)
    except ValueError:
        return {}
    data = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data


def note_stems() -> set[str]:
    stems = {p.stem for p in all_markdown_files()}
    stems.update({"README", "AGENTS", "HANDOFF", "REQUESTS"})
    return stems


def main() -> int:
    errors = []

    for rel in REQUIRED:
        if not (ROOT / rel).exists():
            errors.append(f"Missing required file: {rel}")

    stems = note_stems()
    for path in all_markdown_files():
        text = path.read_text(encoding="utf-8")
        for match in WIKILINK.findall(text):
            target = match.strip()
            if target and target not in stems:
                errors.append(f"Unresolved wikilink in {path.relative_to(ROOT)}: [[{target}]]")

    notes = sorted(PAPERS.glob("*.md"))
    if not notes:
        errors.append("No paper notes found in brain/01_Research/Papers")

    for path in notes:
        text = path.read_text(encoding="utf-8")
        meta = frontmatter(text)

        for key in PAPER_REQUIRED_KEYS:
            if key not in meta:
                errors.append(f"{path.relative_to(ROOT)} missing frontmatter key: {key}")

        if meta.get("type") != "paper":
            errors.append(f"{path.relative_to(ROOT)} has type {meta.get('type')!r}, expected 'paper'")

        for section in PAPER_REQUIRED_SECTIONS:
            if section not in text:
                errors.append(f"{path.relative_to(ROOT)} missing section: {section}")

    if errors:
        print("Datter brain check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Datter brain check passed: {len(all_markdown_files())} brain markdown files, {len(notes)} paper notes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

