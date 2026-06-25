from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERTICALS_ROOT = ROOT / "demo_verticals"
LAB_ROOT = ROOT / "demo_data"

VERTICAL_META = {
    "government": {
        "name": "Treasury compliance RAG",
        "domain": "Government",
        "description": "UK public finance handbook — Managing Public Money",
    },
    "social": {
        "name": "WHO social connection RAG",
        "domain": "Social",
        "description": "WHO report on social connection and health",
    },
    "engineering": {
        "name": "Seismic SMF design RAG",
        "domain": "Engineering",
        "description": "NIST seismic design guide for steel special moment frames",
    },
    "science": {
        "name": "Paleoclimate research RAG",
        "domain": "Science",
        "description": "CLIMBER-X paleoclimate modeling paper",
    },
}

LAB_META = {
    "name": "Structural audit lab",
    "domain": "Lab",
    "description": "Mixed corpus with duplicates and boilerplate — strong savings signal",
}


@dataclass
class Project:
    id: str
    name: str
    domain: str
    description: str
    corpus_path: Path
    queries_path: Path
    task_description: str = ""
    quality_floor: float = 0.90
    target_token_reduction: float = 0.50
    pdf_files: list[str] = field(default_factory=list)
    total_pdf_bytes: int = 0
    question_count: int = 0

    @property
    def primary_pdf(self) -> str | None:
        return self.pdf_files[0] if self.pdf_files else None


def _load_queries(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _scan_pdfs(folder: Path) -> tuple[list[str], int]:
    pdfs = sorted(p.name for p in folder.glob("*.pdf") if p.stat().st_size > 0)
    total = sum((folder / name).stat().st_size for name in pdfs)
    return pdfs, total


def _build_project(project_id: str, folder: Path, meta: dict) -> Project | None:
    pdfs, total_bytes = _scan_pdfs(folder)
    if not pdfs:
        return None
    queries_path = folder / "queries.json"
    queries = _load_queries(queries_path)
    questions = queries.get("questions", [])
    return Project(
        id=project_id,
        name=meta["name"],
        domain=meta["domain"],
        description=meta["description"],
        corpus_path=folder,
        queries_path=queries_path,
        task_description=queries.get("task_description", meta["description"]),
        quality_floor=float(queries.get("quality_floor", 0.90)),
        target_token_reduction=float(queries.get("target_token_reduction", 0.50)),
        pdf_files=pdfs,
        total_pdf_bytes=total_bytes,
        question_count=len(questions),
    )


def load_projects(root: Path | None = None) -> list[Project]:
    root = root or ROOT
    verticals = root / "demo_verticals"
    projects: list[Project] = []

    if verticals.is_dir():
        for sub in sorted(verticals.iterdir()):
            if not sub.is_dir():
                continue
            meta = VERTICAL_META.get(sub.name)
            if not meta:
                continue
            project = _build_project(sub.name, sub, meta)
            if project:
                projects.append(project)

    lab_folder = root / "demo_data"
    if lab_folder.is_dir() and any(lab_folder.glob("*")):
        lab = _build_project("lab", lab_folder, LAB_META)
        if lab:
            projects.append(lab)

    return projects


def get_project(project_id: str, root: Path | None = None) -> Project | None:
    for p in load_projects(root):
        if p.id == project_id:
            return p
    return None


def default_project_id(root: Path | None = None) -> str:
    projects = load_projects(root)
    for preferred in ("government", "social", "engineering", "science", "lab"):
        if any(p.id == preferred for p in projects):
            return preferred
    return projects[0].id if projects else "lab"
