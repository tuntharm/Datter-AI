from __future__ import annotations

import io
import re
from pathlib import Path

from pypdf import PdfReader

from datter.models import Document

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}


def normalize_text(text: str) -> str:
    text = text.replace("\x00", "")
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def read_pdf_bytes(data: bytes) -> str:
    reader = PdfReader(io.BytesIO(data))
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return normalize_text("\n".join(parts))


def read_file_bytes(filename: str, data: bytes) -> str:
    ext = Path(filename).suffix.lower()
    if ext == ".pdf":
        return read_pdf_bytes(data)
    return normalize_text(data.decode("utf-8", errors="replace"))


def read_file_path(path: Path) -> Document:
    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported extension: {ext}")

    if ext == ".pdf":
        text = read_pdf_bytes(path.read_bytes())
    else:
        text = normalize_text(path.read_text(encoding="utf-8", errors="replace"))

    return Document(
        doc_id=path.stem,
        filename=path.name,
        extension=ext,
        source=str(path),
        raw_text=text,
        char_count=len(text),
    )


def ingest_folder(folder_path: str | Path) -> list[Document]:
    root = Path(folder_path)
    if not root.is_dir():
        raise FileNotFoundError(f"Folder not found: {root}")

    docs: list[Document] = []
    for path in sorted(root.rglob("*")):
        if "exam_corpus" in path.parts:
            continue
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS and path.name.lower() != "readme.md":
            docs.append(read_file_path(path))
    return docs


def ingest_uploads(uploads: list) -> list[Document]:
    docs: list[Document] = []
    for i, upload in enumerate(uploads):
        name = upload.name
        ext = Path(name).suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            continue
        text = read_file_bytes(name, upload.getvalue())
        stem = Path(name).stem
        docs.append(
            Document(
                doc_id=f"{stem}_{i}",
                filename=name,
                extension=ext,
                source="upload",
                raw_text=text,
                char_count=len(text),
            )
        )
    return docs
