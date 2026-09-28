from pathlib import Path

import pyarrow.parquet as pq


WEEK1 = Path(
    "/home/jovyan/chunking_sprint/"
    "prototypes/full/prototype_chunks.parquet"
)

CURRENT = {
    "token": Path(
        "/home/jovyan/chunking_sprint/"
        "runs/issue10_token/"
        "representative_samples.chunks.parquet"
    ),
    "recursive": Path(
        "/home/jovyan/chunking_sprint/"
        "runs/issue10_recursive/"
        "representative_samples.chunks.parquet"
    ),
    "semantic": Path(
        "/home/jovyan/chunking_sprint/"
        "runs/issue10_semantic/"
        "representative_samples.chunks.parquet"
    ),
}


week1_rows = pq.read_table(WEEK1).to_pylist()


def week1_tuple(row):
    return (
        row["source_file"],
        row["file_row_number"],
        row["document_id"],
        row["method"],
        row["chunk_index"],
        row["start_index"],
        row["end_index"],
        row["token_count"],
        row["char_length"],
        row["text"],
    )


def current_tuple(row):
    return (
        row["source_file"],
        row["source_row_number"],
        row["document_id"],
        row["method"],
        row["chunk_index"],
        row["start_index"],
        row["end_index"],
        row["token_count"],
        row["char_length"],
        row["text"],
    )


all_pass = True

for method, path in CURRENT.items():
    expected = [
        week1_tuple(row)
        for row in week1_rows
        if row["method"] == method
    ]

    current_rows = pq.read_table(path).to_pylist()

    actual = [
        current_tuple(row)
        for row in current_rows
    ]

    count_match = len(expected) == len(actual)
    exact_match = expected == actual

    print("=" * 72)
    print("Method:", method)
    print("Week 1 chunks:", len(expected))
    print("Week 2 chunks:", len(actual))
    print("Count match:", count_match)
    print("Exact chunk match:", exact_match)

    if not exact_match:
        all_pass = False

        limit = min(len(expected), len(actual))

        for index in range(limit):
            if expected[index] != actual[index]:
                print(
                    "First mismatch at chunk record:",
                    index,
                )
                print("Expected:", expected[index][:-1])
                print("Actual:  ", actual[index][:-1])
                break


print("=" * 72)

if all_pass:
    print("WEEK 1 CONSISTENCY: PASS")
else:
    print("WEEK 1 CONSISTENCY: FAIL")
    raise SystemExit(1)
