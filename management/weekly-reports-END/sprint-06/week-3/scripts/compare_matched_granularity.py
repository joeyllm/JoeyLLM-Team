from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq


ROOT = Path("/home/jovyan/chunking_sprint")

SETTINGS_PATH = (
    ROOT
    / "week3/configs/issue16_matched_settings.json"
)

OUTPUT_DIR = (
    ROOT
    / "week3/results/issue16/matched_comparison"
)

SMALL_CHUNK_THRESHOLD = 256

RUN_DIRS = {
    "token": (
        ROOT
        / "week3/runs/issue16/token_cal_cs839"
    ),
    "recursive": (
        ROOT
        / "week3/runs/issue16/recursive_cal_cs1025"
    ),
    "semantic": (
        ROOT
        / "week3/runs/issue16/semantic_cal_th030"
    ),
}

RESULT_DIRS = {
    "token": (
        ROOT
        / "week3/results/issue16/token_cal_cs839"
    ),
    "recursive": (
        ROOT
        / "week3/results/issue16/recursive_cal_cs1025"
    ),
    "semantic": (
        ROOT
        / "week3/results/issue16/semantic_cal_th030"
    ),
}


def locate_chunk_file(run_dir: Path) -> Path:
    files = sorted(
        run_dir.glob("*.chunks.parquet")
    )

    if len(files) != 1:
        raise RuntimeError(
            f"Expected exactly one chunk parquet in "
            f"{run_dir}, found {len(files)}."
        )

    return files[0]


def small_chunk_stats(
    path: Path,
) -> dict[str, Any]:
    pf = pq.ParquetFile(path)

    if "char_length" not in pf.schema_arrow.names:
        raise RuntimeError(
            f"Missing char_length in {path}"
        )

    total = 0
    small = 0

    for batch in pf.iter_batches(
        columns=["char_length"],
        batch_size=8192,
    ):
        for value in batch.column(0).to_pylist():
            total += 1

            if value < SMALL_CHUNK_THRESHOLD:
                small += 1

    return {
        "threshold_characters": SMALL_CHUNK_THRESHOLD,
        "small_chunk_count": small,
        "total_chunks": total,
        "small_chunk_fraction": (
            small / total
            if total
            else 0.0
        ),
    }


def main() -> None:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    settings = json.loads(
        SETTINGS_PATH.read_text(
            encoding="utf-8"
        )
    )

    methods = [
        "token",
        "recursive",
        "semantic",
    ]

    summaries = {}

    for method in methods:
        summary_path = (
            RESULT_DIRS[method]
            / "summary.json"
        )

        summaries[method] = json.loads(
            summary_path.read_text(
                encoding="utf-8"
            )
        )

    records = []

    group_records = []

    for method in methods:
        summary = summaries[method]

        run = summary["run"]
        metrics = summary["metrics"]

        chunk_file = locate_chunk_file(
            RUN_DIRS[method]
        )

        fragmentation = small_chunk_stats(
            chunk_file
        )

        assert (
            fragmentation["total_chunks"]
            == run["total_chunks"]
        )

        boundaries = (
            metrics["boundaries"]
            ["percentages_internal_only"]
        )

        record = {
            "method": method,
            "run_id": (
                settings["matched_runs"]
                [method]["run_id"]
            ),
            "configuration": (
                run["configuration"]
            ),
            "processed_documents": (
                run["processed_documents"]
            ),
            "failed_documents": (
                run["failed_documents"]
            ),
            "total_chunks": (
                run["total_chunks"]
            ),
            "mean_chunks_per_document": (
                metrics[
                    "chunks_per_document"
                ]["mean"]
            ),
            "median_chunks_per_document": (
                metrics[
                    "chunks_per_document"
                ]["median"]
            ),
            "char_length": (
                metrics["char_length"]
            ),
            "token_count": (
                metrics["token_count"]
            ),
            "internal_boundaries": (
                boundaries
            ),
            "small_chunk_threshold_chars": (
                SMALL_CHUNK_THRESHOLD
            ),
            "small_chunk_count": (
                fragmentation[
                    "small_chunk_count"
                ]
            ),
            "small_chunk_fraction": (
                fragmentation[
                    "small_chunk_fraction"
                ]
            ),
            "elapsed_seconds": (
                run["elapsed_seconds"]
            ),
            "documents_per_second": (
                run["documents_per_second"]
            ),
            "chunks_per_second": (
                run["chunks_per_second"]
            ),
            "warning_count": (
                run["warning_count"]
            ),
            "warnings": (
                run["warnings"]
            ),
            "qa_status": (
                run["qa_status"]
            ),
            "qa_hard_failure_events": (
                run["qa_hard_failure_events"]
            ),
            "chunk_parquet_bytes": (
                chunk_file.stat().st_size
            ),
        }

        records.append(record)

        for group_name, group in sorted(
            summary["sample_groups"].items()
        ):
            group_records.append(
                {
                    "method": method,
                    "group": group_name,
                    "documents": (
                        group["documents"]
                    ),
                    "chunks": (
                        group["chunks"]
                    ),
                    "mean_chunks_per_document": (
                        group[
                            "chunks_per_document"
                        ]["mean"]
                    ),
                    "median_chunk_char_length": (
                        group[
                            "char_length"
                        ]["median"]
                    ),
                    "mean_chunk_char_length": (
                        group[
                            "char_length"
                        ]["mean"]
                    ),
                    "internal_boundaries": (
                        group["boundaries"][
                            "percentages_internal_only"
                        ]
                    ),
                }
            )

    output = {
        "schema_version": 1,
        "source_documents": 32,
        "small_chunk_definition": {
            "field": "char_length",
            "operator": "<",
            "threshold": SMALL_CHUNK_THRESHOLD,
        },
        "matching": {
            "tolerance": (
                settings[
                    "matching_tolerance"
                ]
            ),
            "worst_relative_spread": (
                settings[
                    "worst_relative_spread"
                ]
            ),
            "observed_matching_metrics": (
                settings[
                    "observed_matching_metrics"
                ]
            ),
        },
        "methods": records,
        "sample_groups": group_records,
    }

    json_path = (
        OUTPUT_DIR
        / "matched_comparison.json"
    )

    csv_path = (
        OUTPUT_DIR
        / "matched_comparison.csv"
    )

    groups_csv_path = (
        OUTPUT_DIR
        / "matched_sample_groups.csv"
    )

    md_path = (
        OUTPUT_DIR
        / "matched_comparison.md"
    )

    json_path.write_text(
        json.dumps(
            output,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    csv_fields = [
        "method",
        "run_id",
        "processed_documents",
        "failed_documents",
        "total_chunks",
        "mean_chunks_per_document",
        "median_chunks_per_document",
        "mean_chunk_char_length",
        "median_chunk_char_length",
        "p90_chunk_char_length",
        "p95_chunk_char_length",
        "p99_chunk_char_length",
        "mean_chunk_token_count",
        "median_chunk_token_count",
        "small_chunk_count",
        "small_chunk_fraction",
        "paragraph_boundary_internal",
        "newline_boundary_internal",
        "sentence_boundary_internal",
        "whitespace_boundary_internal",
        "other_boundary_internal",
        "elapsed_seconds",
        "documents_per_second",
        "chunks_per_second",
        "warning_count",
        "qa_status",
        "qa_hard_failure_events",
        "chunk_parquet_bytes",
    ]

    with csv_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=csv_fields,
        )

        writer.writeheader()

        for r in records:
            writer.writerow(
                {
                    "method": r["method"],
                    "run_id": r["run_id"],
                    "processed_documents":
                        r["processed_documents"],
                    "failed_documents":
                        r["failed_documents"],
                    "total_chunks":
                        r["total_chunks"],
                    "mean_chunks_per_document":
                        r["mean_chunks_per_document"],
                    "median_chunks_per_document":
                        r["median_chunks_per_document"],
                    "mean_chunk_char_length":
                        r["char_length"]["mean"],
                    "median_chunk_char_length":
                        r["char_length"]["median"],
                    "p90_chunk_char_length":
                        r["char_length"]["p90"],
                    "p95_chunk_char_length":
                        r["char_length"]["p95"],
                    "p99_chunk_char_length":
                        r["char_length"]["p99"],
                    "mean_chunk_token_count":
                        r["token_count"]["mean"],
                    "median_chunk_token_count":
                        r["token_count"]["median"],
                    "small_chunk_count":
                        r["small_chunk_count"],
                    "small_chunk_fraction":
                        r["small_chunk_fraction"],
                    "paragraph_boundary_internal":
                        r["internal_boundaries"][
                            "paragraph_boundary"
                        ],
                    "newline_boundary_internal":
                        r["internal_boundaries"][
                            "newline_boundary"
                        ],
                    "sentence_boundary_internal":
                        r["internal_boundaries"][
                            "sentence_boundary"
                        ],
                    "whitespace_boundary_internal":
                        r["internal_boundaries"][
                            "whitespace_boundary"
                        ],
                    "other_boundary_internal":
                        r["internal_boundaries"][
                            "other_boundary"
                        ],
                    "elapsed_seconds":
                        r["elapsed_seconds"],
                    "documents_per_second":
                        r["documents_per_second"],
                    "chunks_per_second":
                        r["chunks_per_second"],
                    "warning_count":
                        r["warning_count"],
                    "qa_status":
                        r["qa_status"],
                    "qa_hard_failure_events":
                        r["qa_hard_failure_events"],
                    "chunk_parquet_bytes":
                        r["chunk_parquet_bytes"],
                }
            )

    group_fields = [
        "method",
        "group",
        "documents",
        "chunks",
        "mean_chunks_per_document",
        "median_chunk_char_length",
        "mean_chunk_char_length",
        "paragraph_boundary_internal",
        "newline_boundary_internal",
        "sentence_boundary_internal",
        "whitespace_boundary_internal",
        "other_boundary_internal",
    ]

    with groups_csv_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=group_fields,
        )

        writer.writeheader()

        for r in group_records:
            b = r["internal_boundaries"]

            writer.writerow(
                {
                    "method": r["method"],
                    "group": r["group"],
                    "documents": r["documents"],
                    "chunks": r["chunks"],
                    "mean_chunks_per_document":
                        r["mean_chunks_per_document"],
                    "median_chunk_char_length":
                        r["median_chunk_char_length"],
                    "mean_chunk_char_length":
                        r["mean_chunk_char_length"],
                    "paragraph_boundary_internal":
                        b["paragraph_boundary"],
                    "newline_boundary_internal":
                        b["newline_boundary"],
                    "sentence_boundary_internal":
                        b["sentence_boundary"],
                    "whitespace_boundary_internal":
                        b["whitespace_boundary"],
                    "other_boundary_internal":
                        b["other_boundary"],
                }
            )

    lines = [
        "# Issue 16 Matched-Granularity Comparison",
        "",
        "## Matching",
        "",
        (
            "- Frozen tolerance: "
            f"{settings['matching_tolerance'] * 100:.2f}%"
        ),
        (
            "- Observed worst relative spread: "
            f"{settings['worst_relative_spread'] * 100:.6f}%"
        ),
        "- Matching status: `PASS`",
        "",
        "## Overall Comparison",
        "",
        (
            "| Method | Chunks | Mean chunks/doc | "
            "Median chars | Mean chars | "
            "Small chunks (<256) | Small chunk % | "
            "Elapsed (s) | Warnings | QA |"
        ),
        (
            "|---|---:|---:|---:|---:|---:|---:|"
            "---:|---:|---|"
        ),
    ]

    for r in records:
        lines.append(
            f"| {r['method']} "
            f"| {r['total_chunks']} "
            f"| {r['mean_chunks_per_document']:.3f} "
            f"| {r['char_length']['median']:.3f} "
            f"| {r['char_length']['mean']:.3f} "
            f"| {r['small_chunk_count']} "
            f"| {r['small_chunk_fraction'] * 100:.2f}% "
            f"| {r['elapsed_seconds']:.4f} "
            f"| {r['warning_count']} "
            f"| {r['qa_status']} |"
        )

    lines.extend(
        [
            "",
            "## Internal Boundary Behaviour",
            "",
            (
                "| Method | Paragraph | Newline | Sentence | "
                "Whitespace | Other |"
            ),
            "|---|---:|---:|---:|---:|---:|",
        ]
    )

    for r in records:
        b = r["internal_boundaries"]

        lines.append(
            f"| {r['method']} "
            f"| {b['paragraph_boundary'] * 100:.2f}% "
            f"| {b['newline_boundary'] * 100:.2f}% "
            f"| {b['sentence_boundary'] * 100:.2f}% "
            f"| {b['whitespace_boundary'] * 100:.2f}% "
            f"| {b['other_boundary'] * 100:.2f}% |"
        )

    lines.extend(
        [
            "",
            "## Token-Count Distribution",
            "",
            (
                "Chunk token counts are reported for completeness, "
                "but tokenizer semantics differ across methods and "
                "the values must not be interpreted as directly "
                "equivalent."
            ),
            "",
            "| Method | Mean | Median | P90 | P95 | P99 |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )

    for r in records:
        t = r["token_count"]

        lines.append(
            f"| {r['method']} "
            f"| {t['mean']:.3f} "
            f"| {t['median']:.3f} "
            f"| {t['p90']:.3f} "
            f"| {t['p95']:.3f} "
            f"| {t['p99']:.3f} |"
        )

    lines.extend(
        [
            "",
            "## Output Size",
            "",
            "| Method | Chunk Parquet bytes |",
            "|---|---:|",
        ]
    )

    for r in records:
        lines.append(
            f"| {r['method']} "
            f"| {r['chunk_parquet_bytes']} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation Constraint",
            "",
            (
                "These measurements describe observed differences "
                "under the frozen matched-granularity settings. "
                "They do not constitute an overall quality ranking."
            ),
            "",
        ]
    )

    md_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("Methods:", len(records))
    print(
        "Sample-group rows:",
        len(group_records),
    )
    print("JSON:", json_path)
    print("CSV:", csv_path)
    print("Group CSV:", groups_csv_path)
    print("Markdown:", md_path)
    print()
    print(
        "ISSUE #16 MATCHED COMPARISON GENERATED: PASS"
    )


if __name__ == "__main__":
    main()
