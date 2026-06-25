from pathlib import Path

from datter.project import (
    default_project_id,
    get_project,
    load_projects,
    match_upload_to_project,
)

ROOT = Path(__file__).parent.parent


class _UploadStub:
    def __init__(self, name: str, data: bytes):
        self.name = name
        self.size = len(data)
        self._data = data

    def getvalue(self) -> bytes:
        return self._data


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


def test_match_upload_by_government_pdf_filename():
    gov = get_project("government", ROOT)
    if gov is None:
        return
    pdf_path = gov.corpus_path / gov.primary_pdf
    if not pdf_path.is_file():
        return
    upload = _UploadStub(gov.primary_pdf, pdf_path.read_bytes())
    matched = match_upload_to_project([upload], ROOT)
    assert matched is not None
    assert matched.id == "government"


def test_match_upload_by_byte_fingerprint():
    gov = get_project("government", ROOT)
    if gov is None:
        return
    pdf_path = gov.corpus_path / gov.primary_pdf
    if not pdf_path.is_file():
        return
    upload = _UploadStub("renamed_copy.pdf", pdf_path.read_bytes())
    matched = match_upload_to_project([upload], ROOT)
    assert matched is not None
    assert matched.id == "government"


def test_match_upload_unknown_returns_none():
    upload = _UploadStub("unknown.pdf", b"not a sample corpus")
    assert match_upload_to_project([upload], ROOT) is None
