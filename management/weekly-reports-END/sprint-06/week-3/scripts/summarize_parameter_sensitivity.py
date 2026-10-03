from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path("/home/jovyan/chunking_sprint")

MATRIX = (
    ROOT
    / "week3/configs/parameter_sensitivity_matrix.csv"
)

OUTPUT_DIR = (
    ROOT
    / "week3/results/parameter_sensitivity"
)

BASELINE_RESULT_DIRS = {
    "token_cs2048": (
        ROOT
        / "week3/results/baseline_token"
    ),
    "recursive_cs2048": (
        ROOT
        / "week3/results/baseline_recursive"
    ),
    "semantic_cs2048": (
        ROOT
        / "week3/results/baseline_semantic"
    ),
}


def result_dir_for(run_id: str) -> Path:
    if run_id in BASELINE_RESULT_DIRS:
        return BASELINE_RESULT_DIRS[run_id]

    return (
        ROOT
        / "week3/results/issue15"
        / run_id
    )


def load_summary(run_id: str) -> dict[str, Any]:
    path = (
        result_dir_for(run_id)
        / "summary.json"
    )

    if not path.exists():
        raise SystemExit(
            f"Missing summary for {run_id}: {path}"
        )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def pct(
    numerator: float,
    denominator: float,
) -> float | None:
    if denominator == 0:
        return None

    return (
        (numerator - denominator)
        / denominator
        * 100.0
    )


def main() -> None:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with MATRIX.open(
        newline="",
        encoding="utf-8",
    ) as f:
        matrix = list(
            csv.DictReader(f)
        )

    if len(matrix) != 11:
        raise SystemExit(
            f"Expected 11 frozen configurations, "
            f"found {len(matrix)}."
        )

    summaries = {}

    for row in matrix:
        run_id = row["run_id"]
        summaries[run_id] = (
            load_summary(run_id)
        )

    expected_run_ids = {
        row["run_id"]
        for row in matrix
    }

    if set(summaries) != expected_run_ids:
        raise SystemExit(
            "Loaded run IDs do not match "
            "the frozen matrix."
        )

    baseline_for = {
        "token": "token_cs2048",
        "recursive": "recursive_cs2048",
        "semantic": "semantic_cs2048",
    }

    records = []

    for row in matrix:
        run_id = row["run_id"]
        summary = summaries[run_id]

        run = summary["run"]
        metrics = summary["metrics"]

        baseline_id = (
            baseline_for[row["method"]]
        )

        baseline = (
            summaries[baseline_id]
        )

        baseline_run = baseline["run"]
        baseline_metrics = (
            baseline["metrics"]
        )

        char_stats = (
            metrics["char_length"]
        )

        chunk_doc_stats = (
            metrics["chunks_per_document"]
        )

        boundaries = (
            metrics["boundaries"]
        )

        internal = (
            boundaries[
                "percentages_internal_only"
            ]
        )

        record = {
            "run_id": run_id,
            "method": row["method"],
            "experiment_axis": (
                row["experiment_axis"]
            ),
            "is_baseline": (
                row["is_baseline"] == "true"
            ),
            "chunk_size": (
                int(row["chunk_size"])
                if row["chunk_size"]
                else None
            ),
            "threshold": (
                float(row["threshold"])
                if row["threshold"]
                else None
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
                chunk_doc_stats["mean"]
            ),
            "median_chunks_per_document": (
                chunk_doc_stats["median"]
            ),
            "mean_chunk_char_length": (
                char_stats["mean"]
            ),
            "median_chunk_char_length": (
                char_stats["median"]
            ),
            "p90_chunk_char_length": (
                char_stats["p90"]
            ),
            "p95_chunk_char_length": (
                char_stats["p95"]
            ),
            "p99_chunk_char_length": (
                char_stats["p99"]
            ),
            "paragraph_boundary_internal_pct": (
                internal[
                    "paragraph_boundary"
                ]
            ),
            "newline_boundary_internal_pct": (
                internal[
                    "newline_boundary"
                ]
            ),
            "sentence_boundary_internal_pct": (
                internal[
                    "sentence_boundary"
                ]
            ),
            "whitespace_boundary_internal_pct": (
                internal[
                    "whitespace_boundary"
                ]
            ),
            "other_boundary_internal_pct": (
                internal[
                    "other_boundary"
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
            "qa_status": (
                run["qa_status"]
            ),
            "baseline_run_id": (
                baseline_id
            ),
            "delta_chunks_vs_method_baseline": (
                run["total_chunks"]
                - baseline_run["total_chunks"]
            ),
            "delta_chunks_pct_vs_method_baseline": (
                pct(
                    run["total_chunks"],
                    baseline_run[
                        "total_chunks"
                    ],
                )
            ),
            "delta_mean_chunk_chars_vs_method_baseline": (
                char_stats["mean"]
                - baseline_metrics[
                    "char_length"
                ]["mean"]
            ),
            "delta_elapsed_seconds_vs_method_baseline": (
                run["elapsed_seconds"]
                - baseline_run[
                    "elapsed_seconds"
                ]
            ),
        }

        records.append(record)

    json_output = {
        "schema_version": 1,
        "configuration_count": (
            len(records)
        ),
        "baseline_reuse": {
            "token": "token_cs2048",
            "recursive": (
                "recursive_cs2048"
            ),
            "semantic": (
                "semantic_cs2048"
            ),
        },
        "records": records,
        "axes": {
            "chunk_size": {
                "token": [
                    "token_cs1024",
                    "token_cs2048",
                    "token_cs4096",
                ],
                "recursive": [
                    "recursive_cs1024",
                    "recursive_cs2048",
                    "recursive_cs4096",
                ],
                "semantic": [
                    "semantic_cs1024",
                    "semantic_cs2048",
                    "semantic_cs4096",
                ],
            },
            "semantic_threshold": [
                "semantic_th070",
                "semantic_cs2048",
                "semantic_th090",
            ],
        },
    }

    json_path = (
        OUTPUT_DIR
        / "parameter_sensitivity_summary.json"
    )

    csv_path = (
        OUTPUT_DIR
        / "parameter_sensitivity_summary.csv"
    )

    md_path = (
        OUTPUT_DIR
        / "parameter_sensitivity_report.md"
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

    fieldnames = list(
        records[0].keys()
    )

    with csv_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(records)

    by_id = {
        record["run_id"]: record
        for record in records
    }

    lines = [
        "# Week 3 Parameter Sensitivity Summary",
        "",
        "## Scope",
        "",
        (
            "This report summarizes the 11 frozen "
            "Week 3 configurations."
        ),
        "",
        (
            "The three validated 2048 baseline runs "
            "are reused rather than recomputed."
        ),
        "",
        (
            "Measurements are descriptive only. "
            "No method ranking or quality score is assigned."
        ),
        "",
        "## Chunk-Size Sensitivity",
        "",
    ]

    for method, run_ids in (
        json_output["axes"]["chunk_size"].items()
    ):
        lines.extend(
            [
                f"### {method}",
                "",
                (
                    "| Run | Chunk size | Chunks | "
                    "Mean chunks/doc | Mean chunk chars | "
                    "Internal sentence boundary | "
                    "Internal whitespace boundary | "
                    "Internal other boundary | "
                    "Elapsed (s) | Warnings | QA |"
                ),
                (
                    "|---|---:|---:|---:|---:|---:|---:|"
                    "---:|---:|---:|---|"
                ),
            ]
        )

        for run_id in run_ids:
            r = by_id[run_id]

            lines.append(
                f"| {run_id} "
                f"| {r['chunk_size']} "
                f"| {r['total_chunks']} "
                f"| {r['mean_chunks_per_document']:.3f} "
                f"| {r['mean_chunk_char_length']:.3f} "
                f"| {r['sentence_boundary_internal_pct'] * 100:.2f}% "
                f"| {r['whitespace_boundary_internal_pct'] * 100:.2f}% "
                f"| {r['other_boundary_internal_pct'] * 100:.2f}% "
                f"| {r['elapsed_seconds']:.4f} "
                f"| {r['warning_count']} "
                f"| {r['qa_status']} |"
            )

        lines.append("")

    lines.extend(
        [
            "## Semantic Threshold Sensitivity",
            "",
            (
                "| Run | Threshold | Chunks | "
                "Mean chunks/doc | Mean chunk chars | "
                "Internal sentence boundary | "
                "Internal whitespace boundary | "
                "Internal other boundary | "
                "Elapsed (s) | Warnings | QA |"
            ),
            (
                "|---|---:|---:|---:|---:|---:|---:|"
                "---:|---:|---:|---|"
            ),
        ]
    )

    threshold_values = {
        "semantic_th070": 0.7,
        "semantic_cs2048": 0.8,
        "semantic_th090": 0.9,
    }

    for run_id in (
        json_output[
            "axes"
        ]["semantic_threshold"]
    ):
        r = by_id[run_id]

        lines.append(
            f"| {run_id} "
            f"| {threshold_values[run_id]:.1f} "
            f"| {r['total_chunks']} "
            f"| {r['mean_chunks_per_document']:.3f} "
            f"| {r['mean_chunk_char_length']:.3f} "
            f"| {r['sentence_boundary_internal_pct'] * 100:.2f}% "
            f"| {r['whitespace_boundary_internal_pct'] * 100:.2f}% "
            f"| {r['other_boundary_internal_pct'] * 100:.2f}% "
            f"| {r['elapsed_seconds']:.4f} "
            f"| {r['warning_count']} "
            f"| {r['qa_status']} |"
        )

    lines.extend(
        [
            "",
            "## Baseline-Relative Measurements",
            "",
            (
                "| Run | Baseline | Δ chunks | "
                "Δ chunks (%) | Δ mean chunk chars | "
                "Δ elapsed (s) |"
            ),
            "|---|---|---:|---:|---:|---:|",
        ]
    )

    for r in records:
        pct_value = (
            r[
                "delta_chunks_pct_vs_method_baseline"
            ]
        )

        pct_text = (
            "N/A"
            if pct_value is None
            else f"{pct_value:.3f}%"
        )

        lines.append(
            f"| {r['run_id']} "
            f"| {r['baseline_run_id']} "
            f"| {r['delta_chunks_vs_method_baseline']} "
            f"| {pct_text} "
            f"| {r['delta_mean_chunk_chars_vs_method_baseline']:.3f} "
            f"| {r['delta_elapsed_seconds_vs_method_baseline']:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation Constraint",
            "",
            (
                "Configured chunk size is not directly "
                "comparable across all three methods because "
                "their chunking mechanisms and tokenizer "
                "behaviour differ."
            ),
            "",
            (
                "These results describe parameter sensitivity "
                "within the frozen representative sample. "
                "They do not by themselves establish retrieval "
                "quality or an overall method ranking."
            ),
            "",
        ]
    )

    md_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(
        "Configurations:",
        len(records),
    )
    print("JSON:", json_path)
    print("CSV:", csv_path)
    print("Markdown:", md_path)
    print()
    print(
        "ISSUE #15 PARAMETER SUMMARY GENERATED: PASS"
    )


if __name__ == "__main__":
    main()
