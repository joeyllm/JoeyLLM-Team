from pathlib import Path
import csv
import time

import pyarrow as pa
import pyarrow.parquet as pq

from chonkie import (
    RecursiveChunker,
    SemanticChunker,
    TokenChunker,
)


INPUT = Path(
    "/home/jovyan/hash_output/_audit/profiling/"
    "representative_samples.parquet"
)

OUTPUT_DIR = Path(
    "/home/jovyan/chunking_sprint/prototypes/full"
)

EXPECTED_DOCUMENTS = 32


def chunk_stats(chunks):
    char_lengths = [len(chunk.text) for chunk in chunks]
    token_counts = [chunk.token_count for chunk in chunks]

    return {
        "chunk_count": len(chunks),
        "min_chunk_chars": min(char_lengths),
        "mean_chunk_chars": sum(char_lengths) / len(char_lengths),
        "max_chunk_chars": max(char_lengths),
        "min_chunk_tokens": min(token_counts),
        "mean_chunk_tokens": sum(token_counts) / len(token_counts),
        "max_chunk_tokens": max(token_counts),
    }


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

records = pq.read_table(INPUT).to_pylist()

if len(records) != EXPECTED_DOCUMENTS:
    raise RuntimeError(
        f"Expected {EXPECTED_DOCUMENTS} representative documents, "
        f"found {len(records)}"
    )


chunkers = {
    "token": TokenChunker(
        tokenizer="character",
        chunk_size=2048,
        chunk_overlap=0,
    ),
    "recursive": RecursiveChunker(
        tokenizer="character",
        chunk_size=2048,
    ),
    "semantic": SemanticChunker(
        embedding_model="minishlab/potion-base-32M",
        threshold=0.8,
        chunk_size=2048,
    ),
}


summary_rows = []
chunk_rows = []

total_runs = len(records) * len(chunkers)
completed = 0
failed = 0
experiment_start = time.perf_counter()


for document_index, document in enumerate(records, start=1):
    text = document["text"]

    for method, chunker in chunkers.items():
        completed += 1

        print(
            f"[{completed:02d}/{total_runs}] "
            f"doc={document_index:02d}/{len(records)} | "
            f"{document['sample_groups']} | "
            f"{method} | "
            f"chars={len(text):,}"
        )

        start = time.perf_counter()

        try:
            chunks = chunker.chunk(text)
            elapsed = time.perf_counter() - start

            if not chunks:
                raise RuntimeError("Chunker returned no chunks")

            stats = chunk_stats(chunks)

            invalid_ranges = 0
            slice_mismatches = 0

            for chunk_index, chunk in enumerate(chunks):
                valid_range = (
                    0 <= chunk.start_index
                    <= chunk.end_index
                    <= len(text)
                )

                if not valid_range:
                    invalid_ranges += 1

                slice_matches = (
                    valid_range
                    and text[
                        chunk.start_index:chunk.end_index
                    ] == chunk.text
                )

                if not slice_matches:
                    slice_mismatches += 1

                chunk_rows.append(
                    {
                        "sample_groups": document["sample_groups"],
                        "source_file": document["source_file"],
                        "file_row_number": document["file_row_number"],
                        "document_id": document["id"],
                        "method": method,
                        "chunk_index": chunk_index,
                        "start_index": chunk.start_index,
                        "end_index": chunk.end_index,
                        "token_count": chunk.token_count,
                        "char_length": len(chunk.text),
                        "slice_matches_source": slice_matches,
                        "text": chunk.text,
                    }
                )

            summary_rows.append(
                {
                    "sample_groups": document["sample_groups"],
                    "source_file": document["source_file"],
                    "file_row_number": document["file_row_number"],
                    "input_chars": len(text),
                    "stored_token_count": document["token_count"],
                    "method": method,
                    "status": "success",
                    "runtime_seconds": elapsed,
                    **stats,
                    "invalid_index_ranges": invalid_ranges,
                    "slice_mismatches": slice_mismatches,
                    "error": "",
                }
            )

            print(
                f"    SUCCESS | "
                f"chunks={stats['chunk_count']} | "
                f"time={elapsed:.4f}s | "
                f"index_errors={invalid_ranges} | "
                f"slice_mismatches={slice_mismatches}"
            )

        except Exception as exc:
            failed += 1
            elapsed = time.perf_counter() - start

            summary_rows.append(
                {
                    "sample_groups": document["sample_groups"],
                    "source_file": document["source_file"],
                    "file_row_number": document["file_row_number"],
                    "input_chars": len(text),
                    "stored_token_count": document["token_count"],
                    "method": method,
                    "status": "failed",
                    "runtime_seconds": elapsed,
                    "chunk_count": "",
                    "min_chunk_chars": "",
                    "mean_chunk_chars": "",
                    "max_chunk_chars": "",
                    "min_chunk_tokens": "",
                    "mean_chunk_tokens": "",
                    "max_chunk_tokens": "",
                    "invalid_index_ranges": "",
                    "slice_mismatches": "",
                    "error": repr(exc),
                }
            )

            print(f"    FAILED | {exc!r}")


experiment_elapsed = time.perf_counter() - experiment_start


summary_path = OUTPUT_DIR / "prototype_summary.csv"

with summary_path.open(
    "w",
    encoding="utf-8",
    newline="",
) as f:
    writer = csv.DictWriter(
        f,
        fieldnames=summary_rows[0].keys(),
    )
    writer.writeheader()
    writer.writerows(summary_rows)


chunks_path = OUTPUT_DIR / "prototype_chunks.parquet"

pq.write_table(
    pa.Table.from_pylist(chunk_rows),
    chunks_path,
)


print()
print("=" * 72)
print("FULL PROTOTYPE COMPLETE")
print(f"Documents: {len(records)}")
print(f"Runs: {total_runs}")
print(f"Successful: {total_runs - failed}")
print(f"Failed: {failed}")
print(f"Elapsed: {experiment_elapsed:.2f}s")
print(f"Summary: {summary_path}")
print(f"Chunks: {chunks_path}")
