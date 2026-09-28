from pathlib import Path
import json
import time

import pyarrow.parquet as pq


SOURCE = Path("/home/jovyan/hash_output/part_0.parquet")
CHUNKS = Path(
    "/home/jovyan/chunking_sprint/"
    "runs/issue11_token_part0/part_0.chunks.parquet"
)
OUTPUT = Path(
    "/home/jovyan/chunking_sprint/"
    "runs/issue11_token_part0/scaled_qa_summary.json"
)

EXPECTED_SOURCE_FILE = "part_0.parquet"
EXPECTED_METHOD = "token"


def iter_chunk_rows():
    pf = pq.ParquetFile(CHUNKS)

    columns = [
        "source_file",
        "source_row_number",
        "document_id",
        "method",
        "chunker_config",
        "chunk_index",
        "start_index",
        "end_index",
        "token_count",
        "char_length",
        "text",
    ]

    for batch in pf.iter_batches(
        batch_size=8192,
        columns=columns,
    ):
        for row in batch.to_pylist():
            yield row


source_pf = pq.ParquetFile(SOURCE)

chunk_iterator = iter_chunk_rows()
current_chunk = next(chunk_iterator, None)

counts = {
    "documents_checked": 0,
    "chunks_checked": 0,
    "documents_without_chunks": 0,
    "source_file_mismatches": 0,
    "source_row_order_errors": 0,
    "document_id_mismatches": 0,
    "method_mismatches": 0,
    "missing_chunker_config": 0,
    "chunk_index_mismatches": 0,
    "invalid_index_ranges": 0,
    "source_slice_mismatches": 0,
    "empty_chunks": 0,
    "whitespace_only_chunks": 0,
    "zero_token_chunks": 0,
    "char_length_mismatches": 0,
    "extra_chunks": 0,
}

start_time = time.perf_counter()
source_row_number = 0


for batch in source_pf.iter_batches(
    batch_size=2048,
    columns=["id", "text"],
):
    data = batch.to_pydict()

    for document_id, source_text in zip(
        data["id"],
        data["text"],
    ):
        if (
            current_chunk is not None
            and current_chunk["source_row_number"]
            < source_row_number
        ):
            counts["source_row_order_errors"] += 1

        expected_chunk_index = 0
        document_chunk_count = 0

        while (
            current_chunk is not None
            and current_chunk["source_row_number"]
            == source_row_number
        ):
            row = current_chunk

            counts["chunks_checked"] += 1
            document_chunk_count += 1

            if row["source_file"] != EXPECTED_SOURCE_FILE:
                counts["source_file_mismatches"] += 1

            if row["document_id"] != document_id:
                counts["document_id_mismatches"] += 1

            if row["method"] != EXPECTED_METHOD:
                counts["method_mismatches"] += 1

            if row["chunker_config"] is None:
                counts["missing_chunker_config"] += 1

            if row["chunk_index"] != expected_chunk_index:
                counts["chunk_index_mismatches"] += 1

            text = row["text"]

            if text == "":
                counts["empty_chunks"] += 1

            if text.isspace():
                counts["whitespace_only_chunks"] += 1

            if row["token_count"] == 0:
                counts["zero_token_chunks"] += 1

            if row["char_length"] != len(text):
                counts["char_length_mismatches"] += 1

            start_index = row["start_index"]
            end_index = row["end_index"]

            valid_range = (
                0
                <= start_index
                <= end_index
                <= len(source_text)
            )

            if not valid_range:
                counts["invalid_index_ranges"] += 1
            elif (
                source_text[start_index:end_index]
                != text
            ):
                counts["source_slice_mismatches"] += 1

            expected_chunk_index += 1
            current_chunk = next(
                chunk_iterator,
                None,
            )

        if document_chunk_count == 0:
            counts["documents_without_chunks"] += 1

        counts["documents_checked"] += 1
        source_row_number += 1

        if (
            counts["documents_checked"] % 25000
            == 0
        ):
            print(
                f"[{counts['documents_checked']}/"
                f"{source_pf.metadata.num_rows}] "
                f"chunks={counts['chunks_checked']}"
            )


while current_chunk is not None:
    counts["extra_chunks"] += 1
    current_chunk = next(
        chunk_iterator,
        None,
    )


elapsed = time.perf_counter() - start_time

failure_fields = [
    "documents_without_chunks",
    "source_file_mismatches",
    "source_row_order_errors",
    "document_id_mismatches",
    "method_mismatches",
    "missing_chunker_config",
    "chunk_index_mismatches",
    "invalid_index_ranges",
    "source_slice_mismatches",
    "empty_chunks",
    "whitespace_only_chunks",
    "zero_token_chunks",
    "char_length_mismatches",
    "extra_chunks",
]

failure_events = sum(
    counts[field]
    for field in failure_fields
)

summary = {
    "status": (
        "pass"
        if failure_events == 0
        else "fail"
    ),
    **counts,
    "failure_events": failure_events,
    "elapsed_seconds": elapsed,
}

OUTPUT.write_text(
    json.dumps(
        summary,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)

print()
print("=" * 72)
print("SCALED QA")
print("Status:", summary["status"])
print(
    "Documents checked:",
    counts["documents_checked"],
)
print(
    "Chunks checked:",
    counts["chunks_checked"],
)
print(
    "Failure events:",
    failure_events,
)
print(
    "Elapsed seconds:",
    round(elapsed, 2),
)
print("Summary:", OUTPUT)
print("=" * 72)

if failure_events != 0:
    raise SystemExit(1)
