from chonkie import SemanticChunker

TEXT = """
Chunking divides long documents into smaller units. Good chunk boundaries
should preserve useful context.

Semantic chunking uses changes in meaning to identify suitable split points.
This differs from purely fixed-size chunking.

The purpose of this test is only to verify that the local semantic chunking
pipeline can load its embedding model and produce chunks without an API.
""".strip()


chunker = SemanticChunker(
    embedding_model="minishlab/potion-base-32M",
    threshold=0.8,
    chunk_size=2048,
)

chunks = chunker.chunk(TEXT)

assert chunks, "SemanticChunker returned no chunks"

print("Chunks:", len(chunks))

for i, chunk in enumerate(chunks, 1):
    print(
        f"{i}: "
        f"start={chunk.start_index}, "
        f"end={chunk.end_index}, "
        f"tokens={chunk.token_count}, "
        f"chars={len(chunk.text)}"
    )

print("SEMANTIC SMOKE TEST: PASS")
