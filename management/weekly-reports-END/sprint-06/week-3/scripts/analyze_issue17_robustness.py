from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import pyarrow.parquet as pq


ROOT = Path("/home/jovyan/chunking_sprint")

OUTPUT_DIR = (
    ROOT
    / "week3/results/issue17"
)

GROUP_SOURCE = (
    ROOT
    / "week3/results/issue16/"
      "matched_comparison/"
      "matched_sample_groups.csv"
)

COMPARISON_SOURCE = (
    ROOT
    / "week3/results/issue16/"
      "matched_comparison/"
      "matched_comparison.json"
)

RUN_DIRS = {
    "token": (
        ROOT
        / "week3/runs/issue16/"
          "token_cal_cs839"
    ),
    "recursive": (
        ROOT
        / "week3/runs/issue16/"
          "recursive_cal_cs1025"
    ),
    "semantic": (
        ROOT
        / "week3/runs/issue16/"
          "semantic_cal_th030"
    ),
}

METHODS = [
    "token",
    "recursive",
    "semantic",
]

EXPECTED_GROUPS = {
    "high_chars_per_token",
    "length_max",
    "length_median",
    "length_min",
    "length_p05",
    "length_p90",
    "length_p95",
    "length_p99",
    "low_chars_per_token",
    "no_newline",
}

LONG_GROUPS = {
    "length_p95",
    "length_p99",
    "length_max",
}

SMALL_CHUNK_THRESHOLD = 256


def chunk_file(run_dir: Path) -> Path:
    files = sorted(
        run_dir.glob(
            "*.chunks.parquet"
        )
    )

    if len(files) != 1:
        raise RuntimeError(
            f"{run_dir}: expected 1 chunk parquet, "
            f"found {len(files)}"
        )

    return files[0]


def parse_groups(
    value: str | None,
) -> list[str]:
    if not value:
        return []

    return [
        part.strip()
        for part in value.split(",")
        if part.strip()
    ]


def main() -> None:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    comparison = json.loads(
        COMPARISON_SOURCE.read_text(
            encoding="utf-8"
        )
    )

    assert (
        comparison[
            "small_chunk_definition"
        ]["threshold"]
        == SMALL_CHUNK_THRESHOLD
    )

    run_info = {
        row["method"]: row
        for row in comparison["methods"]
    }

    assert set(run_info) == set(METHODS)

    with GROUP_SOURCE.open(
        newline="",
        encoding="utf-8",
    ) as f:
        base_rows = list(
            csv.DictReader(f)
        )

    assert len(base_rows) == 30

    base = {}

    for row in base_rows:
        key = (
            row["method"],
            row["group"],
        )

        assert key not in base
        base[key] = row

    observed = {}

    for method in METHODS:
        path = chunk_file(
            RUN_DIRS[method]
        )

        pf = pq.ParquetFile(path)

        required = {
            "document_id",
            "sample_groups",
            "char_length",
        }

        missing = (
            required
            - set(
                pf.schema_arrow.names
            )
        )

        if missing:
            raise RuntimeError(
                f"{path}: missing "
                f"{sorted(missing)}"
            )

        chunk_counts = defaultdict(int)
        small_counts = defaultdict(int)
        documents = defaultdict(set)

        total_chunks = 0

        for batch in pf.iter_batches(
            columns=[
                "document_id",
                "sample_groups",
                "char_length",
            ],
            batch_size=8192,
        ):
            ids = (
                batch.column(0)
                .to_pylist()
            )

            groups_col = (
                batch.column(1)
                .to_pylist()
            )

            lengths = (
                batch.column(2)
                .to_pylist()
            )

            for (
                document_id,
                group_value,
                char_length,
            ) in zip(
                ids,
                groups_col,
                lengths,
            ):
                total_chunks += 1

                groups = parse_groups(
                    group_value
                )

                for group in groups:
                    if (
                        group
                        not in EXPECTED_GROUPS
                    ):
                        raise RuntimeError(
                            "Unexpected group: "
                            f"{group}"
                        )

                    chunk_counts[group] += 1

                    documents[group].add(
                        document_id
                    )

                    if (
                        char_length
                        < SMALL_CHUNK_THRESHOLD
                    ):
                        small_counts[
                            group
                        ] += 1

        assert (
            total_chunks
            == run_info[method][
                "total_chunks"
            ]
        )

        for group in EXPECTED_GROUPS:
            key = (method, group)

            assert key in base

            expected_chunks = int(
                base[key]["chunks"]
            )

            expected_docs = int(
                base[key]["documents"]
            )

            assert (
                chunk_counts[group]
                == expected_chunks
            ), (
                method,
                group,
                chunk_counts[group],
                expected_chunks,
            )

            assert (
                len(documents[group])
                == expected_docs
            ), (
                method,
                group,
                len(documents[group]),
                expected_docs,
            )

            observed[key] = {
                "small_chunk_count":
                    small_counts[group],
                "small_chunk_fraction": (
                    small_counts[group]
                    / chunk_counts[group]
                    if chunk_counts[group]
                    else 0.0
                ),
            }

    rows = []

    for method in METHODS:
        for group in sorted(
            EXPECTED_GROUPS
        ):
            key = (method, group)

            source = base[key]
            extra = observed[key]

            rows.append(
                {
                    "method": method,
                    "group": group,
                    "documents": int(
                        source["documents"]
                    ),
                    "chunks": int(
                        source["chunks"]
                    ),
                    "mean_chunks_per_document":
                        float(
                            source[
                                "mean_chunks_per_document"
                            ]
                        ),
                    "median_chunk_char_length":
                        float(
                            source[
                                "median_chunk_char_length"
                            ]
                        ),
                    "mean_chunk_char_length":
                        float(
                            source[
                                "mean_chunk_char_length"
                            ]
                        ),
                    "small_chunk_count":
                        extra[
                            "small_chunk_count"
                        ],
                    "small_chunk_fraction":
                        extra[
                            "small_chunk_fraction"
                        ],
                    "paragraph_boundary_internal":
                        float(
                            source[
                                "paragraph_boundary_internal"
                            ]
                        ),
                    "newline_boundary_internal":
                        float(
                            source[
                                "newline_boundary_internal"
                            ]
                        ),
                    "sentence_boundary_internal":
                        float(
                            source[
                                "sentence_boundary_internal"
                            ]
                        ),
                    "whitespace_boundary_internal":
                        float(
                            source[
                                "whitespace_boundary_internal"
                            ]
                        ),
                    "other_boundary_internal":
                        float(
                            source[
                                "other_boundary_internal"
                            ]
                        ),
                    "run_failed_documents":
                        run_info[method][
                            "failed_documents"
                        ],
                    "run_warning_count":
                        run_info[method][
                            "warning_count"
                        ],
                    "warnings_group_attributable":
                        False,
                }
            )

    cost_rows = []

    for method in METHODS:
        run = run_info[method]

        elapsed = float(
            run["elapsed_seconds"]
        )

        documents = int(
            run["processed_documents"]
        )

        cost_rows.append(
            {
                "method": method,
                "run_id": run["run_id"],
                "processed_documents":
                    documents,
                "failed_documents":
                    run[
                        "failed_documents"
                    ],
                "total_chunks":
                    run["total_chunks"],
                "elapsed_seconds":
                    elapsed,
                "seconds_per_document":
                    (
                        elapsed
                        / documents
                    ),
                "documents_per_second":
                    run[
                        "documents_per_second"
                    ],
                "chunks_per_second":
                    run[
                        "chunks_per_second"
                    ],
                "output_bytes":
                    run[
                        "chunk_parquet_bytes"
                    ],
                "warning_count":
                    run[
                        "warning_count"
                    ],
                "qa_status":
                    run["qa_status"],
                "memory_measurement":
                    None,
            }
        )

    json_output = {
        "schema_version": 1,
        "source_documents": 32,
        "small_chunk_definition": {
            "field": "char_length",
            "operator": "<",
            "threshold":
                SMALL_CHUNK_THRESHOLD,
        },
        "matched_run_memory_measurement_status":
            "not_measured",
        "warning_attribution": (
            "Warnings are run-level "
            "and are not attributable "
            "to representative groups."
        ),
        "group_overlap": True,
        "robustness_by_group": rows,
        "computational_cost": cost_rows,
    }

    json_path = (
        OUTPUT_DIR
        / "robustness_summary.json"
    )

    csv_path = (
        OUTPUT_DIR
        / "robustness_by_group.csv"
    )

    cost_path = (
        OUTPUT_DIR
        / "computational_cost.csv"
    )

    md_path = (
        OUTPUT_DIR
        / "robustness_summary.md"
    )

    json_path.write_text(
        json.dumps(
            json_output,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    fields = list(
        rows[0].keys()
    )

    with csv_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fields,
        )

        writer.writeheader()
        writer.writerows(rows)

    with cost_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=list(
                cost_rows[0].keys()
            ),
        )

        writer.writeheader()
        writer.writerows(
            cost_rows
        )

    lines = [
        "# Issue 17 Robustness Evidence",
        "",
        "## Group-Level Robustness",
        "",
        (
            "| Group | Method | Docs | "
            "Chunks/doc | Median chars | "
            "Mean chars | Small chunks | "
            "Small % |"
        ),
        (
            "|---|---|---:|---:|---:|"
            "---:|---:|---:|"
        ),
    ]

    for row in rows:
        lines.append(
            f"| {row['group']} "
            f"| {row['method']} "
            f"| {row['documents']} "
            f"| {row['mean_chunks_per_document']:.3f} "
            f"| {row['median_chunk_char_length']:.3f} "
            f"| {row['mean_chunk_char_length']:.3f} "
            f"| {row['small_chunk_count']} "
            f"| {row['small_chunk_fraction'] * 100:.2f}% |"
        )

    lines.extend(
        [
            "",
            "## Long-Document Groups",
            "",
            (
                "| Group | Method | "
                "Chunks/doc | Median chars | "
                "Mean chars | Small % |"
            ),
            (
                "|---|---|---:|---:|"
                "---:|---:|"
            ),
        ]
    )

    for row in rows:
        if (
            row["group"]
            not in LONG_GROUPS
        ):
            continue

        lines.append(
            f"| {row['group']} "
            f"| {row['method']} "
            f"| {row['mean_chunks_per_document']:.3f} "
            f"| {row['median_chunk_char_length']:.3f} "
            f"| {row['mean_chunk_char_length']:.3f} "
            f"| {row['small_chunk_fraction'] * 100:.2f}% |"
        )

    lines.extend(
        [
            "",
            "## Computational Cost",
            "",
            (
                "| Method | Seconds | "
                "Seconds/doc | Docs/s | "
                "Chunks/s | Output bytes | "
                "Warnings | Failures |"
            ),
            (
                "|---|---:|---:|---:|"
                "---:|---:|---:|---:|"
            ),
        ]
    )

    for row in cost_rows:
        lines.append(
            f"| {row['method']} "
            f"| {row['elapsed_seconds']:.6f} "
            f"| {row['seconds_per_document']:.9f} "
            f"| {row['documents_per_second']:.3f} "
            f"| {row['chunks_per_second']:.3f} "
            f"| {row['output_bytes']} "
            f"| {row['warning_count']} "
            f"| {row['failed_documents']} |"
        )

    lines.extend(
        [
            "",
            "## Measurement Notes",
            "",
            (
                "Memory was not measured for "
                "the three matched Issue 16 runs. "
                "Week 2 scaled TokenChunker resource "
                "evidence is recorded separately."
            ),
            "",
            (
                "Warnings are recorded at run "
                "level and are not attributed "
                "to individual representative "
                "groups."
            ),
            "",
            (
                "Runtime measurements above are "
                "single-run descriptive evidence, "
                "not repeated benchmark estimates."
            ),
            "",
        ]
    )

    md_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(
        "Robustness rows:",
        len(rows),
    )
    print(
        "Cost rows:",
        len(cost_rows),
    )
    print(
        "Long-document rows:",
        sum(
            row["group"]
            in LONG_GROUPS
            for row in rows
        ),
    )
    print(
        "JSON:",
        json_path,
    )
    print(
        "Group CSV:",
        csv_path,
    )
    print(
        "Cost CSV:",
        cost_path,
    )
    print(
        "Markdown:",
        md_path,
    )
    print()
    print(
        "ISSUE #17 ROBUSTNESS "
        "EVIDENCE BUILD: PASS"
    )


if __name__ == "__main__":
    main()
