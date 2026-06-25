from datter.dedup import deduplicate_chunks, exact_hash
from datter.models import Chunk


def test_exact_duplicate_detection():
    chunks = [
        Chunk("a::0", "a", "a.txt", "hello world", 0, 2),
        Chunk("b::0", "b", "b.txt", "hello world", 0, 2),
        Chunk("c::0", "c", "c.txt", "unique content here", 0, 3),
    ]
    deduplicate_chunks(chunks)
    assert chunks[0].is_exact_duplicate and chunks[1].is_exact_duplicate
    assert exact_hash("Hello, World!") == exact_hash("hello world")
