from __future__ import annotations

import argparse
import csv
import glob
import json
from collections import Counter
from pathlib import Path

import pyarrow.parquet as pq


REQUIRED_FIELDS = [
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


def resolve_chunk_files(pattern: str) -> list[Path]:
    paths = [
        Path(path).resolve()
        for path in sorted(glob.glob(pattern))
    ]

    if not paths:
        raise FileNotFoundError(
            f"No chunk files matched: {pattern}"
        )

    return paths


class SourceReader:
    def __init__(self, source_dir: Path):
        self.source_dir = source_dir
        self.parquet_files = {}
        self.records = {}

    def read(self, source_file: str, row_number: int):
        key = (source_file, row_number)

        if key in self.records:
            return self.records[key]

        path = self.source_dir / source_file

        if not path.is_file():
            raise FileNotFoundError(
                f"Source file not found: {path}"
            )

        if source_file not in self.parquet_files:
            self.parquet_files[source_file] = (
                pq.ParquetFile(path)
            )

        parquet_file = self.parquet_files[source_file]

        if row_number < 0:
            raise IndexError(
                f"Negative source row: {row_number}"
            )

        start = 0

        for row_group_index in range(
            parquet_file.metadata.num_row_groups
        ):
            row_count = (
                parquet_file.metadata
                .row_group(row_group_index)
                .num_rows
            )

            end = start + row_count

            if start <= row_number < end:
                offset = row_number - start

                table = parquet_file.read_row_group(
                    row_group_index,
                    columns=["id", "text"],
                )

                record = (
                    table.slice(offset, 1)
                    .to_pylist()[0]
                )

                self.records[key] = record
                return record

            start = end

        raise IndexError(
            f"Source row {row_number} is outside "
            f"{source_file}"
        )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Validate chunk integrity, provenance, "
            "and source-text correspondence."
        )
    )

    parser.add_argument(
        "--chunks",
        required=True,
        help="Chunk Parquet file or glob pattern.",
    )
    parser.add_argument(
        "--source-dir",
        required=True,
        help="Directory containing frozen part_*.parquet files.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory for QA outputs.",
    )
    parser.add_argument(
        "--run-metadata",
        default=None,
    )
    parser.add_argument(
        "--stderr-log",
        default=None,
    )

    args = parser.parse_args()

    chunk_files = resolve_chunk_files(
        args.chunks
    )

    source_dir = Path(
        args.source_dir
    ).resolve()

    output_dir = Path(
        args.output_dir
    ).resolve()

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    source_reader = SourceReader(
        source_dir
    )

    counts = Counter()
    document_chunk_counts = Counter()
    failures = []

    def record_failure(row, check, details):
        failures.append(
            {
                "source_file": row.get(
                    "source_file"
                ),
                "source_row_number": row.get(
                    "source_row_number"
                ),
                "document_id": row.get(
                    "document_id"
                ),
                "method": row.get(
                    "method"
                ),
                "chunk_index": row.get(
                    "chunk_index"
                ),
                "check": check,
                "details": details,
            }
        )

    for chunk_file in chunk_files:
        parquet_file = pq.ParquetFile(
            chunk_file
        )

        columns = set(
            parquet_file.schema_arrow.names
        )

        missing_columns = [
            name
            for name in REQUIRED_FIELDS
            if name not in columns
        ]

        if missing_columns:
            raise RuntimeError(
                f"{chunk_file} missing required "
                f"columns: {missing_columns}"
            )

        for batch in parquet_file.iter_batches(
            batch_size=4096
        ):
            rows = batch.to_pylist()

            for row in rows:
                counts["chunks_checked"] += 1

                missing_fields = [
                    field
                    for field in REQUIRED_FIELDS
                    if row.get(field) is None
                ]

                if missing_fields:
                    counts[
                        "missing_required_fields"
                    ] += 1

                    record_failure(
                        row,
                        "missing_required_fields",
                        ",".join(missing_fields),
                    )

                    continue

                text = row["text"]

                if text == "":
                    counts["empty_chunks"] += 1

                    record_failure(
                        row,
                        "empty_chunk",
                        "Chunk text is empty.",
                    )

                if text.isspace():
                    counts[
                        "whitespace_only_chunks"
                    ] += 1

                    record_failure(
                        row,
                        "whitespace_only_chunk",
                        "Chunk contains only whitespace.",
                    )

                if row["token_count"] == 0:
                    counts[
                        "zero_token_chunks"
                    ] += 1

                    record_failure(
                        row,
                        "zero_token_chunk",
                        "Chunk token_count is zero.",
                    )

                if row["char_length"] != len(text):
                    counts[
                        "char_length_mismatches"
                    ] += 1

                    record_failure(
                        row,
                        "char_length_mismatch",
                        (
                            f"stored={row['char_length']} "
                            f"actual={len(text)}"
                        ),
                    )

                document_key = (
                    row["source_file"],
                    row["source_row_number"],
                    row["document_id"],
                    row["method"],
                )

                document_chunk_counts[
                    document_key
                ] += 1

                try:
                    source = source_reader.read(
                        row["source_file"],
                        row["source_row_number"],
                    )

                except Exception as exc:
                    counts[
                        "source_lookup_failures"
                    ] += 1

                    record_failure(
                        row,
                        "source_lookup_failure",
                        repr(exc),
                    )

                    continue

                if (
                    source["id"]
                    != row["document_id"]
                ):
                    counts[
                        "document_id_mismatches"
                    ] += 1

                    record_failure(
                        row,
                        "document_id_mismatch",
                        (
                            f"source={source['id']!r} "
                            f"chunk={row['document_id']!r}"
                        ),
                    )

                source_text = source["text"]

                start_index = row["start_index"]
                end_index = row["end_index"]

                valid_range = (
                    0
                    <= start_index
                    <= end_index
                    <= len(source_text)
                )

                if not valid_range:
                    counts[
                        "invalid_index_ranges"
                    ] += 1

                    record_failure(
                        row,
                        "invalid_index_range",
                        (
                            f"start={start_index} "
                            f"end={end_index} "
                            f"source_length="
                            f"{len(source_text)}"
                        ),
                    )

                    continue

                if (
                    source_text[
                        start_index:end_index
                    ]
                    != text
                ):
                    counts[
                        "source_slice_mismatches"
                    ] += 1

                    record_failure(
                        row,
                        "source_slice_mismatch",
                        "Chunk text does not match source slice.",
                    )

    run_failed_documents = 0

    if args.run_metadata:
        metadata_path = Path(
            args.run_metadata
        )

        metadata = json.loads(
            metadata_path.read_text(
                encoding="utf-8"
            )
        )

        run_failed_documents = int(
            metadata.get(
                "failed_documents",
                0,
            )
        )

    warning_lines = []

    if args.stderr_log:
        stderr_path = Path(
            args.stderr_log
        )

        if stderr_path.is_file():
            for line in stderr_path.read_text(
                encoding="utf-8",
                errors="replace",
            ).splitlines():
                if (
                    "RuntimeWarning" in line
                    or "Warning:" in line
                ):
                    warning_lines.append(
                        line.strip()
                    )

    hard_failure_keys = [
        "missing_required_fields",
        "empty_chunks",
        "whitespace_only_chunks",
        "zero_token_chunks",
        "char_length_mismatches",
        "source_lookup_failures",
        "document_id_mismatches",
        "invalid_index_ranges",
        "source_slice_mismatches",
    ]

    hard_failure_events = (
        sum(
            counts[key]
            for key in hard_failure_keys
        )
        + run_failed_documents
    )

    status = (
        "pass"
        if hard_failure_events == 0
        else "fail"
    )

    summary = {
        "status": status,
        "chunk_files": [
            str(path)
            for path in chunk_files
        ],
        "chunks_checked": counts[
            "chunks_checked"
        ],
        "documents_checked": len(
            document_chunk_counts
        ),
        "run_failed_documents": (
            run_failed_documents
        ),
        "missing_required_fields": counts[
            "missing_required_fields"
        ],
        "empty_chunks": counts[
            "empty_chunks"
        ],
        "whitespace_only_chunks": counts[
            "whitespace_only_chunks"
        ],
        "zero_token_chunks": counts[
            "zero_token_chunks"
        ],
        "char_length_mismatches": counts[
            "char_length_mismatches"
        ],
        "source_lookup_failures": counts[
            "source_lookup_failures"
        ],
        "document_id_mismatches": counts[
            "document_id_mismatches"
        ],
        "invalid_index_ranges": counts[
            "invalid_index_ranges"
        ],
        "source_slice_mismatches": counts[
            "source_slice_mismatches"
        ],
        "warning_count": len(
            warning_lines
        ),
        "warnings": warning_lines,
        "hard_failure_events": (
            hard_failure_events
        ),
    }

    summary_path = (
        output_dir
        / "qa_summary.json"
    )

    summary_path.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    failures_path = (
        output_dir
        / "qa_failures.csv"
    )

    with failures_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        fieldnames = [
            "source_file",
            "source_row_number",
            "document_id",
            "method",
            "chunk_index",
            "check",
            "details",
        ]

        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(failures)

    counts_path = (
        output_dir
        / "chunk_counts.csv"
    )

    with counts_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        fieldnames = [
            "source_file",
            "source_row_number",
            "document_id",
            "method",
            "chunk_count",
        ]

        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for (
            source_file,
            source_row_number,
            document_id,
            method,
        ), chunk_count in sorted(
            document_chunk_counts.items()
        ):
            writer.writerow(
                {
                    "source_file": (
                        source_file
                    ),
                    "source_row_number": (
                        source_row_number
                    ),
                    "document_id": (
                        document_id
                    ),
                    "method": method,
                    "chunk_count": (
                        chunk_count
                    ),
                }
            )

    report_path = (
        output_dir
        / "qa_report.md"
    )

    report_lines = [
        "# Chunk QA Report",
        "",
        f"- Status: **{status.upper()}**",
        (
            f"- Documents checked: "
            f"{len(document_chunk_counts)}"
        ),
        (
            f"- Chunks checked: "
            f"{counts['chunks_checked']}"
        ),
        (
            f"- Pipeline document failures: "
            f"{run_failed_documents}"
        ),
        (
            f"- Missing required fields: "
            f"{counts['missing_required_fields']}"
        ),
        (
            f"- Empty chunks: "
            f"{counts['empty_chunks']}"
        ),
        (
            f"- Whitespace-only chunks: "
            f"{counts['whitespace_only_chunks']}"
        ),
        (
            f"- Zero-token chunks: "
            f"{counts['zero_token_chunks']}"
        ),
        (
            f"- Character-length mismatches: "
            f"{counts['char_length_mismatches']}"
        ),
        (
            f"- Source lookup failures: "
            f"{counts['source_lookup_failures']}"
        ),
        (
            f"- Document ID mismatches: "
            f"{counts['document_id_mismatches']}"
        ),
        (
            f"- Invalid index ranges: "
            f"{counts['invalid_index_ranges']}"
        ),
        (
            f"- Source-slice mismatches: "
            f"{counts['source_slice_mismatches']}"
        ),
        (
            f"- Recorded warnings: "
            f"{len(warning_lines)}"
        ),
        (
            f"- Hard failure events: "
            f"{hard_failure_events}"
        ),
        "",
        "## Warning Log",
        "",
    ]

    if warning_lines:
        for warning in warning_lines:
            report_lines.append(
                f"- `{warning}`"
            )
    else:
        report_lines.append(
            "No recorded warnings."
        )

    report_path.write_text(
        "\n".join(report_lines)
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("CHUNK QA")
    print(f"Status: {status}")
    print(
        "Documents checked:",
        len(document_chunk_counts),
    )
    print(
        "Chunks checked:",
        counts["chunks_checked"],
    )
    print(
        "Pipeline failures:",
        run_failed_documents,
    )
    print(
        "Invalid index ranges:",
        counts["invalid_index_ranges"],
    )
    print(
        "Source slice mismatches:",
        counts["source_slice_mismatches"],
    )
    print(
        "Empty chunks:",
        counts["empty_chunks"],
    )
    print(
        "Zero-token chunks:",
        counts["zero_token_chunks"],
    )
    print(
        "Missing provenance:",
        counts["missing_required_fields"],
    )
    print(
        "Warnings:",
        len(warning_lines),
    )
    print(
        "Hard failure events:",
        hard_failure_events,
    )
    print(
        f"Summary: {summary_path}"
    )
    print(
        f"Report: {report_path}"
    )
    print("=" * 72)

    if status != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
