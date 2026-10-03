from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

import pyarrow.parquet as pq


ROOT = Path(
    "/home/jovyan/chunking_sprint"
)

PIPELINE = (
    ROOT
    / "pipeline/run_chunking.py"
)

VALIDATOR = (
    ROOT
    / "pipeline/validate_chunks.py"
)

SOURCE_DIR = Path(
    "/home/jovyan/hash_output"
)

INPUT_MANIFEST = (
    ROOT
    / "week3/inputs/"
      "issue17_long_runtime_inputs.json"
)

RUN_ROOT = (
    ROOT
    / "week3/runs/issue17/"
      "long_runtime"
)

RESULT_ROOT = (
    ROOT
    / "week3/results/issue17/"
      "long_runtime"
)

GROUPS = [
    "length_p95",
    "length_p99",
    "length_max",
]

METHODS = [
    "token",
    "recursive",
    "semantic",
]


def build_pipeline_command(
    method: str,
    input_path: Path,
    output_dir: Path,
) -> list[str]:
    cmd = [
        sys.executable,
        str(PIPELINE),
        "--input",
        str(input_path),
        "--output-dir",
        str(output_dir),
        "--method",
        method,
        "--progress-every",
        "1",
        "--overwrite",
    ]

    if method == "token":
        cmd.extend(
            [
                "--chunk-size",
                "839",
                "--tokenizer",
                "character",
                "--chunk-overlap",
                "0",
            ]
        )

    elif method == "recursive":
        cmd.extend(
            [
                "--chunk-size",
                "1025",
                "--tokenizer",
                "character",
                "--min-characters-per-chunk",
                "24",
            ]
        )

    elif method == "semantic":
        cmd.extend(
            [
                "--chunk-size",
                "2048",
                "--embedding-model",
                "minishlab/potion-base-32M",
                "--threshold",
                "0.30",
            ]
        )

    else:
        raise RuntimeError(
            method
        )

    return cmd


def find_chunk_file(
    run_dir: Path,
) -> Path:
    files = sorted(
        run_dir.glob(
            "*.chunks.parquet"
        )
    )

    if len(files) != 1:
        raise RuntimeError(
            f"{run_dir}: expected exactly "
            f"1 chunk parquet, found "
            f"{len(files)}"
        )

    return files[0]


def run_command(
    cmd: list[str],
    *,
    stdout_path: Path | None = None,
    stderr_path: Path | None = None,
) -> None:
    if stdout_path is None:
        process = subprocess.run(
            cmd,
            text=True,
        )
    else:
        assert stderr_path is not None

        with stdout_path.open(
            "w",
            encoding="utf-8",
        ) as out, stderr_path.open(
            "w",
            encoding="utf-8",
        ) as err:
            process = subprocess.run(
                cmd,
                stdout=out,
                stderr=err,
                text=True,
            )

    if process.returncode != 0:
        raise RuntimeError(
            "Command failed: "
            + " ".join(cmd)
        )


def main() -> None:
    manifest = json.loads(
        INPUT_MANIFEST.read_text(
            encoding="utf-8"
        )
    )

    assert (
        manifest[
            "unique_documents_across_groups"
        ]
        == 9
    )

    RUN_ROOT.mkdir(
        parents=True,
        exist_ok=True,
    )

    RESULT_ROOT.mkdir(
        parents=True,
        exist_ok=True,
    )

    records = []

    total_runs = (
        len(GROUPS)
        * len(METHODS)
    )

    completed = 0

    for group in GROUPS:
        group_info = (
            manifest[
                "groups"
            ][group]
        )

        input_path = Path(
            group_info[
                "input_path"
            ]
        )

        input_table = (
            pq.read_table(
                input_path,
                columns=[
                    "char_length",
                ],
            )
        )

        input_documents = (
            input_table.num_rows
        )

        input_total_chars = sum(
            input_table[
                "char_length"
            ].to_pylist()
        )

        for method in METHODS:
            run_id = (
                f"{group}__{method}"
            )

            run_dir = (
                RUN_ROOT
                / run_id
            )

            qa_dir = (
                run_dir
                / "qa"
            )

            run_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            qa_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            stdout_path = (
                run_dir
                / "pipeline.stdout.log"
            )

            stderr_path = (
                run_dir
                / "pipeline.stderr.log"
            )

            print()
            print(
                "=" * 88
            )

            print(
                f"RUN "
                f"{completed + 1}/{total_runs}: "
                f"{run_id}"
            )

            print(
                "=" * 88
            )

            pipeline_cmd = (
                build_pipeline_command(
                    method,
                    input_path,
                    run_dir,
                )
            )

            run_command(
                pipeline_cmd,
                stdout_path=
                    stdout_path,
                stderr_path=
                    stderr_path,
            )

            metadata_path = (
                run_dir
                / "run_metadata.json"
            )

            assert (
                metadata_path.exists()
            )

            chunk_path = (
                find_chunk_file(
                    run_dir
                )
            )

            qa_cmd = [
                sys.executable,
                str(VALIDATOR),
                "--chunks",
                str(chunk_path),
                "--source-dir",
                str(SOURCE_DIR),
                "--output-dir",
                str(qa_dir),
                "--run-metadata",
                str(metadata_path),
                "--stderr-log",
                str(stderr_path),
            ]

            run_command(
                qa_cmd
            )

            qa_path = (
                qa_dir
                / "qa_summary.json"
            )

            metadata = json.loads(
                metadata_path.read_text(
                    encoding="utf-8"
                )
            )

            qa = json.loads(
                qa_path.read_text(
                    encoding="utf-8"
                )
            )

            processed = int(
                metadata[
                    "processed_documents"
                ]
            )

            chunks = int(
                metadata[
                    "chunks_written"
                ]
            )

            elapsed = float(
                metadata[
                    "elapsed_seconds"
                ]
            )

            failures = int(
                metadata[
                    "failed_documents"
                ]
            )

            assert (
                processed
                == input_documents
            )

            assert failures == 0

            assert (
                qa[
                    "documents_checked"
                ]
                == processed
            )

            assert (
                qa[
                    "chunks_checked"
                ]
                == chunks
            )

            assert (
                qa["status"]
                == "pass"
            )

            record = {
                "group": group,
                "method": method,
                "run_id": run_id,
                "input_documents":
                    input_documents,
                "input_total_characters":
                    input_total_chars,
                "input_mean_characters":
                    (
                        input_total_chars
                        / input_documents
                    ),
                "generated_chunks":
                    chunks,
                "elapsed_seconds":
                    elapsed,
                "seconds_per_document":
                    (
                        elapsed
                        / processed
                    ),
                "documents_per_second":
                    (
                        processed
                        / elapsed
                    ),
                "chunks_per_second":
                    (
                        chunks
                        / elapsed
                    ),
                "output_bytes":
                    chunk_path.stat().st_size,
                "failed_documents":
                    failures,
                "warning_count":
                    qa[
                        "warning_count"
                    ],
                "warnings":
                    qa["warnings"],
                "qa_status":
                    qa["status"],
                "qa_hard_failure_events":
                    qa[
                        "hard_failure_events"
                    ],
            }

            records.append(
                record
            )

            completed += 1

            print(
                f"COMPLETED "
                f"{completed}/{total_runs}"
            )

            print(
                "  documents:",
                processed,
            )

            print(
                "  chunks:",
                chunks,
            )

            print(
                "  elapsed:",
                f"{elapsed:.6f}",
            )

            print(
                "  warnings:",
                record[
                    "warning_count"
                ],
            )

            print(
                "  QA:",
                record[
                    "qa_status"
                ],
            )

    assert len(records) == 9

    json_path = (
        RESULT_ROOT
        / "long_runtime_summary.json"
    )

    csv_path = (
        RESULT_ROOT
        / "long_runtime_summary.csv"
    )

    md_path = (
        RESULT_ROOT
        / "long_runtime_summary.md"
    )

    output = {
        "schema_version": 1,
        "run_count": len(records),
        "measurement_class":
            "single_run_descriptive",
        "records": records,
    }

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
        key
        for key in records[0]
        if key != "warnings"
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

        for record in records:
            writer.writerow(
                {
                    key: value
                    for key, value
                    in record.items()
                    if key != "warnings"
                }
            )

    lines = [
        "# Issue 17 Long-Document Runtime",
        "",
        (
            "These are single-run descriptive "
            "pipeline measurements."
        ),
        "",
        (
            "| Group | Method | Docs | "
            "Input chars | Chunks | Seconds | "
            "Seconds/doc | Docs/s | Chunks/s | "
            "Output bytes | Warnings | QA |"
        ),
        (
            "|---|---|---:|---:|---:|---:|"
            "---:|---:|---:|---:|---:|---|"
        ),
    ]

    for r in records:
        lines.append(
            f"| {r['group']} "
            f"| {r['method']} "
            f"| {r['input_documents']} "
            f"| {r['input_total_characters']} "
            f"| {r['generated_chunks']} "
            f"| {r['elapsed_seconds']:.6f} "
            f"| {r['seconds_per_document']:.6f} "
            f"| {r['documents_per_second']:.3f} "
            f"| {r['chunks_per_second']:.3f} "
            f"| {r['output_bytes']} "
            f"| {r['warning_count']} "
            f"| {r['qa_status']} |"
        )

    lines.extend(
        [
            "",
            (
                "Pipeline timings include "
                "batch initialization and I/O "
                "overhead."
            ),
            "",
            (
                "Semantic timings also include "
                "local embedding-model "
                "initialization for each pipeline "
                "invocation."
            ),
            "",
            (
                "No overall chunk-quality ranking "
                "is implied by runtime."
            ),
            "",
        ]
    )

    md_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print()
    print(
        "=" * 88
    )

    print(
        "Runs completed:",
        completed,
    )

    print(
        "JSON:",
        json_path,
    )

    print(
        "CSV:",
        csv_path,
    )

    print(
        "Markdown:",
        md_path,
    )

    print()
    print(
        "ISSUE #17 LONG RUNTIME "
        "EXPERIMENT: PASS"
    )


if __name__ == "__main__":
    main()
