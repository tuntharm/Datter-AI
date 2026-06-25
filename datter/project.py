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


def _upload_specs(uploads: list) -> list[tuple[str, int]]:
    specs: list[tuple[str, int]] = []
    for upload in uploads:
        name = Path(upload.name).name.lower()
        if Path(name).suffix.lower() not in {".pdf", ".txt", ".md"}:
            continue
        size = getattr(upload, "size", None)
        if size is None:
            size = len(upload.getvalue())
        specs.append((name, int(size)))
    return specs


def _project_fingerprints(project: Project) -> set[tuple[str, int]]:
    fps: set[tuple[str, int]] = set()
    for name in project.pdf_files:
        path = project.corpus_path / name
        if path.is_file():
            fps.add((name.lower(), path.stat().st_size))
    return fps


def _project_for_unique_pdf_size(size: int, root: Path | None = None) -> Project | None:
    matches: list[Project] = []
    for project in load_projects(root):
        if any(pdf_size == size for _, pdf_size in _project_fingerprints(project)):
            matches.append(project)
    if len(matches) == 1:
        return matches[0]
    return None


def match_upload_to_project(uploads: list, root: Path | None = None) -> Project | None:
    """Match uploaded files to a known sample project by filename or byte fingerprint."""
    specs = _upload_specs(uploads)
    if not specs:
        return None

    upload_names = {name for name, _ in specs}
    upload_fps = set(specs)

    for project in load_projects(root):
        project_names = {name.lower() for name in project.pdf_files}
        project_fps = _project_fingerprints(project)

        if upload_names == project_names:
            return project
        if len(specs) == 1 and specs[0][0] in project_names:
            return project
        if project_fps and upload_fps == project_fps:
            return project
        if len(specs) == 1 and specs[0] in project_fps:
            return project

    if len(specs) == 1:
        return _project_for_unique_pdf_size(specs[0][1], root)

    return None
