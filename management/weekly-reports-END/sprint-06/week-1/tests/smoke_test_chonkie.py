from importlib.metadata import version

from chonkie import RecursiveChunker, TokenChunker


TEXT = """
Chunking divides a document into smaller units while preserving useful context.

A reproducible pipeline should use fixed software versions and explicit
configuration. This smoke test verifies that the installed Chonkie package
can instantiate local chunkers and process text without any external API.
""".strip()


def test_recursive_chunker():
    chunker = RecursiveChunker(
        tokenizer="character",
        chunk_size=80,
    )

    chunks = chunker.chunk(TEXT)

    assert isinstance(chunks, list)
    assert len(chunks) > 0

    print("RecursiveChunker:")
    print("  chunks:", len(chunks))
    print("  first chunk type:", type(chunks[0]).__name__)
    print("  first chunk:", repr(chunks[0]))


def test_token_chunker():
    chunker = TokenChunker(
        tokenizer="character",
        chunk_size=80,
        chunk_overlap=0,
    )

    chunks = chunker.chunk(TEXT)

    assert isinstance(chunks, list)
    assert len(chunks) > 0

    print("TokenChunker:")
    print("  chunks:", len(chunks))
    print("  first chunk type:", type(chunks[0]).__name__)
    print("  first chunk:", repr(chunks[0]))


if __name__ == "__main__":
    print("Chonkie version:", version("chonkie"))
    print()

    test_recursive_chunker()
    print()

    test_token_chunker()
    print()

    print("SMOKE TEST: PASS")
