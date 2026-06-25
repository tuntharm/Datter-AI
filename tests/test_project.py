from pathlib import Path

from datter.project import default_project_id, get_project, load_projects

ROOT = Path(__file__).parent.parent


def test_load_projects_includes_lab():
    projects = load_projects(ROOT)
    ids = {p.id for p in projects}
    assert "lab" in ids


def test_government_project_when_pdf_present():
    gov = get_project("government", ROOT)
    if gov is None:
        return  # skip if PDF not downloaded
    assert gov.primary_pdf == "managing_public_money.pdf"
    assert gov.question_count >= 6


def test_default_project_is_government_when_available():
    projects = load_projects(ROOT)
    if any(p.id == "government" for p in projects):
        assert default_project_id(ROOT) == "government"
