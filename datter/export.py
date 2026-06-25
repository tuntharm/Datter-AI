from __future__ import annotations

import io
import json
import zipfile
from dataclasses import dataclass, field

import pandas as pd

from datter.models import Chunk, SelectedCorpus


@dataclass
class ExportManifestEntry:
    item_id: str
    filename: str
    action: str
    token_count: int
    export_path: str


@dataclass
class OptimisedCorpus:
    entries: list[ExportManifestEntry] = field(default_factory=list)
    total_tokens: int = 0
    file_count: int = 0


def _trim_text(text: str, action: str) -> str:
    if action == "compress":
        half = max(1, len(text) // 2)
        return text[:half].strip()
    return text.strip()


def build_optimised_corpus(
    chunks: list[Chunk],
    scores: pd.DataFrame,
    selected_ids: list[str],
) -> OptimisedCorpus:
    lookup = {c.item_id: c for c in chunks}
    idx = scores.set_index("item_id") if not scores.empty else pd.DataFrame().set_index(pd.Index([]))
    entries: list[ExportManifestEntry] = []
    total_tokens = 0

    for i, cid in enumerate(selected_ids):
        if cid not in lookup:
            continue
        chunk = lookup[cid]
        action = str(idx.loc[cid, "recommended_action"]) if cid in idx.index else "keep"
        if action == "drop":
            continue
        text = _trim_text(chunk.text, action)
        token_count = max(1, len(text.split()))
        export_name = f"chunk_{i:04d}_{chunk.filename}.txt"
        entries.append(
            ExportManifestEntry(
                item_id=cid,
                filename=chunk.filename,
                action=action,
                token_count=token_count,
                export_path=export_name,
            )
        )
        total_tokens += token_count

    return OptimisedCorpus(entries=entries, total_tokens=total_tokens, file_count=len(entries))


def export_zip(
    chunks: list[Chunk],
    scores: pd.DataFrame,
    selection: SelectedCorpus,
) -> bytes:
    optimised = build_optimised_corpus(chunks, scores, selection.datter_chunk_ids)
    lookup = {c.item_id: c for c in chunks}
    idx = scores.set_index("item_id") if not scores.empty else pd.DataFrame().set_index(pd.Index([]))

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for entry in optimised.entries:
            chunk = lookup.get(entry.item_id)
            if not chunk:
                continue
            action = str(idx.loc[entry.item_id, "recommended_action"]) if entry.item_id in idx.index else "keep"
            text = _trim_text(chunk.text, action)
            zf.writestr(entry.export_path, text)

        manifest = {
            "corpus_type": "datter_optimised",
            "total_tokens": optimised.total_tokens,
            "chunk_count": optimised.file_count,
            "entries": [entry.__dict__ for entry in optimised.entries],
        }
        zf.writestr("manifest.json", json.dumps(manifest, indent=2))

    return buf.getvalue()
