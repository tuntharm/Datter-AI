from __future__ import annotations

import re

from datter.models import Chunk, Document
from datter.token_cost import count_tokens

CHUNK_SIZE = 400
CHUNK_OVERLAP = 50


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n{2,}", text)
    return [p.strip() for p in parts if p.strip()]


def chunk_document(doc: Document, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[Chunk]:
    if not doc.raw_text:
        return []

    sentences = split_sentences(doc.raw_text)
    chunks: list[Chunk] = []
    current: list[str] = []
    current_tokens = 0
    idx = 0

    def flush():
        nonlocal idx, current, current_tokens
        if not current:
            return
        text = "\n\n".join(current).strip()
        if not text:
            current = []
            current_tokens = 0
            return
        chunks.append(
            Chunk(
                item_id=f"{doc.doc_id}::chunk_{idx}",
                doc_id=doc.doc_id,
                filename=doc.filename,
                text=text,
                chunk_index=idx,
                token_count=count_tokens(text),
            )
        )
        idx += 1
        if overlap > 0 and len(current) > 1:
            current = current[-1:]
            current_tokens = count_tokens("\n\n".join(current))
        else:
            current = []
            current_tokens = 0

    for sentence in sentences:
        sent_tokens = count_tokens(sentence)
        if sent_tokens > chunk_size:
            flush()
            chunks.append(
                Chunk(
                    item_id=f"{doc.doc_id}::chunk_{idx}",
                    doc_id=doc.doc_id,
                    filename=doc.filename,
                    text=sentence,
                    chunk_index=idx,
                    token_count=sent_tokens,
                )
            )
            idx += 1
            continue

        if current_tokens + sent_tokens > chunk_size and current:
            flush()
        current.append(sentence)
        current_tokens += sent_tokens

    flush()
    return chunks


def chunk_documents(documents: list[Document]) -> list[Chunk]:
    all_chunks: list[Chunk] = []
    for doc in documents:
        all_chunks.extend(chunk_document(doc))
    return all_chunks
