from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq


REQUIRED_COLUMNS = {
    "source_file",
    "source_row_number",
    "document_id",
    "source_char_length",
    "sample_groups",
    "method",
    "chunk_index",
    "end_index",
    "token_count",
    "char_length",
    "text",
}

BOUNDARY_CLASSES = [
    "document_end",
    "paragraph_boundary",
    "newline_boundary",
    "sentence_boundary",
    "whitespace_boundary",
    "other_boundary",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Aggregate Week 3 chunking evaluation metrics "
            "from a validated pipeline run."
        )
    )

    parser.add_argument(
        "--run-dir",
        required=True,
        type=Path,
        help="Pipeline run directory.",
    )

    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for JSON, CSV, and Markdown reports.",
    )

    return parser.parse_args()


def percentile_linear(
    values: list[float | int],
    percentile: float,
) -> float:
    if not values:
        raise ValueError(
            "Cannot calculate percentile of an empty sequence."
        )

    ordered = sorted(values)

    if len(ordered) == 1:
        return float(ordered[0])

    position = (
        (len(ordered) - 1)
        * percentile
        / 100.0
    )

    lower = math.floor(position)
    upper = math.ceil(position)

    if lower == upper:
        return float(ordered[lower])

    weight = position - lower

    return float(
        ordered[lower]
        + (
            ordered[upper]
            - ordered[lower]
        )
        * weight
    )


def distribution(
    values: list[float | int],
) -> dict[str, float]:
    if not values:
        raise ValueError(
            "Cannot summarize an empty sequence."
        )

    return {
        "min": float(min(values)),
        "mean": float(sum(values) / len(values)),
        "median": percentile_linear(values, 50),
        "p90": percentile_linear(values, 90),
        "p95": percentile_linear(values, 95),
        "p99": percentile_linear(values, 99),
        "max": float(max(values)),
    }


def split_sample_groups(
    value: str | None,
) -> list[str]:
    if value is None:
        return []

    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]


def classify_boundary(
    text: str,
    end_index: int,
    source_char_length: int,
) -> str:
    if end_index == source_char_length:
        return "document_end"

    if (
        text.endswith("\r\n\r\n")
        or text.endswith("\n\n")
    ):
        return "paragraph_boundary"

    if (
        text.endswith("\n")
        or text.endswith("\r")
    ):
        return "newline_boundary"

    trimmed = text.rstrip(" \t")

    closing_characters = "\"'”’)]}"

    while (
        trimmed
        and trimmed[-1] in closing_characters
    ):
        trimmed = trimmed[:-1]

    if (
        trimmed.endswith(".")
        or trimmed.endswith("!")
        or trimmed.endswith("?")
    ):
        return "sentence_boundary"

    if text and text[-1].isspace():
        return "whitespace_boundary"

    return "other_boundary"


def boundary_summary(
    boundaries: list[str],
) -> dict[str, Any]:
    counts = Counter(boundaries)

    total = len(boundaries)

    all_percentages = {
        name: (
            counts[name] / total
            if total
            else 0.0
        )
        for name in BOUNDARY_CLASSES
    }

    internal_total = (
        total
        - counts["document_end"]
    )

    internal_percentages = {}

    for name in BOUNDARY_CLASSES:
        if name == "document_end":
            continue

        internal_percentages[name] = (
            counts[name] / internal_total
            if internal_total
            else 0.0
        )

    return {
        "counts": {
            name: counts[name]
            for name in BOUNDARY_CLASSES
        },
        "percentages_all_chunks": (
            all_percentages
        ),
        "internal_boundary_count": (
            internal_total
        ),
        "percentages_internal_only": (
            internal_percentages
        ),
    }


def read_warning_fallback(
    stderr_path: Path,
) -> list[str]:
    if not stderr_path.exists():
        return []

    warnings = []

    for line in stderr_path.read_text(
        encoding="utf-8",
        errors="replace",
    ).splitlines():
        if (
            "RuntimeWarning:" in line
            or "Warning:" in line
        ):
            warnings.append(line.strip())

    return warnings


def locate_chunk_file(
    run_dir: Path,
) -> Path:
    files = sorted(
        run_dir.glob("*.chunks.parquet")
    )

    if len(files) != 1:
        raise RuntimeError(
            "Expected exactly one "
            f"*.chunks.parquet file in {run_dir}, "
            f"found {len(files)}."
        )

    return files[0]


def load_rows(
    chunk_path: Path,
) -> tuple[list[dict[str, Any]], set[str]]:
    pf = pq.ParquetFile(chunk_path)

    actual_columns = set(
        pf.schema_arrow.names
    )

    missing = (
        REQUIRED_COLUMNS
        - actual_columns
    )

    if missing:
        raise RuntimeError(
            "Missing required chunk fields: "
            + ", ".join(sorted(missing))
        )

    columns = sorted(
        REQUIRED_COLUMNS
    )

    rows = []

    for batch in pf.iter_batches(
        batch_size=8192,
        columns=columns,
    ):
        rows.extend(
            batch.to_pylist()
        )

    return rows, actual_columns


def main() -> None:
    args = parse_args()

    run_dir = args.run_dir.resolve()
    output_dir = args.output_dir.resolve()

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    metadata_path = (
        run_dir
        / "run_metadata.json"
    )

    if not metadata_path.exists():
        raise SystemExit(
            f"Missing metadata: {metadata_path}"
        )

    metadata = json.loads(
        metadata_path.read_text(
            encoding="utf-8"
        )
    )

    chunk_path = locate_chunk_file(
        run_dir
    )

    rows, actual_columns = load_rows(
        chunk_path
    )

    if not rows:
        raise SystemExit(
            "Chunk output contains zero rows."
        )

    method = metadata.get("method")

    if method is None:
        raise SystemExit(
            "run_metadata.json is missing 'method'."
        )

    configuration = metadata.get(
        "configuration"
    )

    if not isinstance(
        configuration,
        dict,
    ):
        raise SystemExit(
            "run_metadata.json contains no valid "
            "'configuration' object."
        )

    chunk_methods = {
        row["method"]
        for row in rows
    }

    if chunk_methods != {method}:
        raise SystemExit(
            "Chunk method values do not match "
            f"run metadata: {chunk_methods} vs {method}"
        )

    char_length_mismatches = 0

    for row in rows:
        text = row["text"]

        if text is None:
            raise SystemExit(
                "Encountered null chunk text."
            )

        if (
            row["char_length"]
            != len(text)
        ):
            char_length_mismatches += 1

    if char_length_mismatches:
        raise SystemExit(
            "char_length validation failed for "
            f"{char_length_mismatches} chunks."
        )

    document_chunks = defaultdict(int)

    document_groups = {}

    boundaries = []

    char_lengths = []
    token_counts = []

    group_rows = defaultdict(list)

    for row in rows:
        identity = (
            row["source_file"],
            row["source_row_number"],
            row["document_id"],
        )

        document_chunks[identity] += 1

        groups = split_sample_groups(
            row["sample_groups"]
        )

        previous_groups = (
            document_groups.get(identity)
        )

        current_groups = tuple(groups)

        if (
            previous_groups is not None
            and previous_groups
            != current_groups
        ):
            raise SystemExit(
                "Inconsistent sample_groups "
                f"within document {identity}."
            )

        document_groups[
            identity
        ] = current_groups

        boundary = classify_boundary(
            text=row["text"],
            end_index=row["end_index"],
            source_char_length=(
                row["source_char_length"]
            ),
        )

        boundaries.append(boundary)
        char_lengths.append(
            row["char_length"]
        )
        token_counts.append(
            row["token_count"]
        )

        enriched = {
            **row,
            "_identity": identity,
            "_boundary": boundary,
        }

        for group in groups:
            group_rows[group].append(
                enriched
            )

    unique_documents = len(
        document_chunks
    )

    processed_documents = metadata.get(
        "processed_documents"
    )

    if (
        processed_documents
        is not None
        and unique_documents
        != processed_documents
    ):
        raise SystemExit(
            "Unique document count does not match "
            "processed_documents: "
            f"{unique_documents} vs "
            f"{processed_documents}. "
            "The aggregator will not silently omit "
            "zero-chunk documents."
        )

    chunks_per_document = list(
        document_chunks.values()
    )

    qa_path = (
        run_dir
        / "qa"
        / "qa_summary.json"
    )

    qa = None

    if qa_path.exists():
        qa = json.loads(
            qa_path.read_text(
                encoding="utf-8"
            )
        )

        warning_count = qa.get(
            "warning_count"
        )

        warnings = qa.get(
            "warnings"
        )

        if not isinstance(
            warning_count,
            int,
        ):
            raise SystemExit(
                "QA summary contains no valid "
                "warning_count."
            )

        if not isinstance(
            warnings,
            list,
        ):
            raise SystemExit(
                "QA summary contains no valid "
                "warnings list."
            )

        qa_status = qa.get("status")
        qa_hard_failures = qa.get(
            "hard_failure_events"
        )

    else:
        warnings = read_warning_fallback(
            run_dir
            / "pipeline.stderr.log"
        )

        warning_count = len(
            warnings
        )

        qa_status = None
        qa_hard_failures = None

    elapsed_seconds = metadata.get(
        "elapsed_seconds"
    )

    if (
        not isinstance(
            elapsed_seconds,
            (int, float),
        )
        or elapsed_seconds <= 0
    ):
        raise SystemExit(
            "Invalid elapsed_seconds in run metadata."
        )

    total_chunks = len(rows)

    documents_per_second = (
        unique_documents
        / elapsed_seconds
    )

    chunks_per_second = (
        total_chunks
        / elapsed_seconds
    )

    groups_summary = {}

    for group in sorted(group_rows):
        rows_for_group = (
            group_rows[group]
        )

        identities = {
            row["_identity"]
            for row in rows_for_group
        }

        group_document_counts = (
            Counter(
                row["_identity"]
                for row in rows_for_group
            )
        )

        group_char_lengths = [
            row["char_length"]
            for row in rows_for_group
        ]

        group_boundaries = [
            row["_boundary"]
            for row in rows_for_group
        ]

        groups_summary[group] = {
            "documents": len(
                identities
            ),
            "chunks": len(
                rows_for_group
            ),
            "chunks_per_document": (
                distribution(
                    list(
                        group_document_counts.values()
                    )
                )
            ),
            "char_length": (
                distribution(
                    group_char_lengths
                )
            ),
            "boundaries": (
                boundary_summary(
                    group_boundaries
                )
            ),
        }

    summary = {
        "schema_version": 1,
        "run": {
            "run_directory": str(
                run_dir
            ),
            "chunk_file": str(
                chunk_path
            ),
            "method": method,
            "configuration": (
                configuration
            ),
            "status": metadata.get(
                "status"
            ),
            "processed_documents": (
                processed_documents
            ),
            "unique_documents_in_chunks": (
                unique_documents
            ),
            "failed_documents": (
                metadata.get(
                    "failed_documents"
                )
            ),
            "total_chunks": (
                total_chunks
            ),
            "elapsed_seconds": (
                float(
                    elapsed_seconds
                )
            ),
            "documents_per_second": (
                documents_per_second
            ),
            "chunks_per_second": (
                chunks_per_second
            ),
            "warning_count": (
                warning_count
            ),
            "warnings": warnings,
            "qa_status": qa_status,
            "qa_hard_failure_events": (
                qa_hard_failures
            ),
        },
        "validation": {
            "required_columns_present": True,
            "char_length_mismatches": (
                char_length_mismatches
            ),
            "actual_columns": sorted(
                actual_columns
            ),
        },
        "metrics": {
            "chunks_per_document": (
                distribution(
                    chunks_per_document
                )
            ),
            "char_length": (
                distribution(
                    char_lengths
                )
            ),
            "token_count": (
                distribution(
                    token_counts
                )
            ),
            "boundaries": (
                boundary_summary(
                    boundaries
                )
            ),
        },
        "sample_groups": (
            groups_summary
        ),
    }

    json_path = (
        output_dir
        / "summary.json"
    )

    csv_path = (
        output_dir
        / "summary.csv"
    )

    markdown_path = (
        output_dir
        / "report.md"
    )

    json_path.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    csv_rows = []

    def add_csv(
        scope: str,
        group: str,
        metric: str,
        value: Any,
    ) -> None:
        csv_rows.append(
            {
                "scope": scope,
                "group": group,
                "metric": metric,
                "value": value,
            }
        )

    run_metrics = {
        "method": method,
        "processed_documents": (
            processed_documents
        ),
        "failed_documents": (
            metadata.get(
                "failed_documents"
            )
        ),
        "total_chunks": (
            total_chunks
        ),
        "elapsed_seconds": (
            elapsed_seconds
        ),
        "documents_per_second": (
            documents_per_second
        ),
        "chunks_per_second": (
            chunks_per_second
        ),
        "warning_count": (
            warning_count
        ),
        "qa_status": (
            qa_status
        ),
        "qa_hard_failure_events": (
            qa_hard_failures
        ),
        "configuration_json": (
            json.dumps(
                configuration,
                sort_keys=True,
            )
        ),
    }

    for metric, value in (
        run_metrics.items()
    ):
        add_csv(
            "run",
            "",
            metric,
            value,
        )

    for metric_name in [
        "chunks_per_document",
        "char_length",
        "token_count",
    ]:
        for statistic, value in (
            summary["metrics"][
                metric_name
            ].items()
        ):
            add_csv(
                "overall",
                "",
                (
                    f"{metric_name}."
                    f"{statistic}"
                ),
                value,
            )

    boundaries_summary = (
        summary["metrics"][
            "boundaries"
        ]
    )

    for name, value in (
        boundaries_summary[
            "counts"
        ].items()
    ):
        add_csv(
            "overall",
            "",
            f"boundary.count.{name}",
            value,
        )

    for name, value in (
        boundaries_summary[
            "percentages_all_chunks"
        ].items()
    ):
        add_csv(
            "overall",
            "",
            (
                "boundary."
                "percentage_all."
                f"{name}"
            ),
            value,
        )

    for name, value in (
        boundaries_summary[
            "percentages_internal_only"
        ].items()
    ):
        add_csv(
            "overall",
            "",
            (
                "boundary."
                "percentage_internal."
                f"{name}"
            ),
            value,
        )

    for group, values in (
        groups_summary.items()
    ):
        add_csv(
            "sample_group",
            group,
            "documents",
            values["documents"],
        )

        add_csv(
            "sample_group",
            group,
            "chunks",
            values["chunks"],
        )

        for statistic, value in (
            values[
                "chunks_per_document"
            ].items()
        ):
            add_csv(
                "sample_group",
                group,
                (
                    "chunks_per_document."
                    f"{statistic}"
                ),
                value,
            )

        for statistic, value in (
            values[
                "char_length"
            ].items()
        ):
            add_csv(
                "sample_group",
                group,
                (
                    "char_length."
                    f"{statistic}"
                ),
                value,
            )

        for name, value in (
            values[
                "boundaries"
            ]["counts"].items()
        ):
            add_csv(
                "sample_group",
                group,
                (
                    "boundary.count."
                    f"{name}"
                ),
                value,
            )

        for name, value in (
            values[
                "boundaries"
            ][
                "percentages_internal_only"
            ].items()
        ):
            add_csv(
                "sample_group",
                group,
                (
                    "boundary."
                    "percentage_internal."
                    f"{name}"
                ),
                value,
            )

    with csv_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "scope",
                "group",
                "metric",
                "value",
            ],
        )

        writer.writeheader()
        writer.writerows(
            csv_rows
        )

    def pct(value: float) -> str:
        return f"{value * 100:.2f}%"

    lines = [
        "# Week 3 Chunking Evaluation Report",
        "",
        "## Run",
        "",
        f"- Method: `{method}`",
        (
            "- Configuration: `"
            + json.dumps(
                configuration,
                sort_keys=True,
            )
            + "`"
        ),
        (
            "- Processed documents: "
            f"{processed_documents}"
        ),
        (
            "- Failed documents: "
            f"{metadata.get('failed_documents')}"
        ),
        f"- Total chunks: {total_chunks}",
        (
            "- Elapsed seconds: "
            f"{elapsed_seconds:.6f}"
        ),
        (
            "- Documents/second: "
            f"{documents_per_second:.3f}"
        ),
        (
            "- Chunks/second: "
            f"{chunks_per_second:.3f}"
        ),
        f"- Warning count: {warning_count}",
        f"- QA status: `{qa_status}`",
        (
            "- QA hard failures: "
            f"{qa_hard_failures}"
        ),
        "",
        "## Overall Distributions",
        "",
        "| Metric | Min | Mean | Median | P90 | P95 | P99 | Max |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for label, key in [
        (
            "Chunks/document",
            "chunks_per_document",
        ),
        (
            "Chunk characters",
            "char_length",
        ),
        (
            "Chunk token count",
            "token_count",
        ),
    ]:
        values = (
            summary["metrics"][key]
        )

        lines.append(
            "| "
            + label
            + " | "
            + " | ".join(
                f"{values[name]:.3f}"
                for name in [
                    "min",
                    "mean",
                    "median",
                    "p90",
                    "p95",
                    "p99",
                    "max",
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Boundary Behaviour",
            "",
            "| Boundary | Count | All chunks | Internal only |",
            "|---|---:|---:|---:|",
        ]
    )

    for name in BOUNDARY_CLASSES:
        count = (
            boundaries_summary[
                "counts"
            ][name]
        )

        all_pct = (
            boundaries_summary[
                "percentages_all_chunks"
            ][name]
        )

        if name == "document_end":
            internal_pct = "N/A"
        else:
            internal_pct = pct(
                boundaries_summary[
                    "percentages_internal_only"
                ][name]
            )

        lines.append(
            f"| {name} | "
            f"{count} | "
            f"{pct(all_pct)} | "
            f"{internal_pct} |"
        )

    lines.extend(
        [
            "",
            "## Representative Groups",
            "",
            "| Group | Documents | Chunks | Mean chunks/document | Median chunk chars | Mean chunk chars |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )

    for group, values in (
        groups_summary.items()
    ):
        lines.append(
            f"| {group} | "
            f"{values['documents']} | "
            f"{values['chunks']} | "
            f"{values['chunks_per_document']['mean']:.3f} | "
            f"{values['char_length']['median']:.3f} | "
            f"{values['char_length']['mean']:.3f} |"
        )

    if warnings:
        lines.extend(
            [
                "",
                "## Warnings",
                "",
            ]
        )

        for warning in warnings:
            lines.append(
                f"- `{warning}`"
            )

    lines.extend(
        [
            "",
            "## Interpretation Constraint",
            "",
            (
                "This report contains descriptive "
                "measurements only. Raw chunk count "
                "or configured chunk size must not be "
                "treated as a standalone quality ranking."
            ),
            "",
        ]
    )

    markdown_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("=" * 72)
    print("WEEK 3 EVALUATION AGGREGATOR")
    print("Run:", run_dir)
    print("Method:", method)
    print("Documents:", unique_documents)
    print("Chunks:", total_chunks)
    print("Warnings:", warning_count)
    print("QA status:", qa_status)
    print("JSON:", json_path)
    print("CSV:", csv_path)
    print("Markdown:", markdown_path)
    print("=" * 72)


if __name__ == "__main__":
    main()
