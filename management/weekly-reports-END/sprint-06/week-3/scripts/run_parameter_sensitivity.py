from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path("/home/jovyan/chunking_sprint")

MATRIX = (
    ROOT
    / "week3/configs/parameter_sensitivity_matrix.csv"
)

INPUT = Path(
    "/home/jovyan/hash_output/_audit/profiling/"
    "representative_samples.parquet"
)

SOURCE_DIR = Path(
    "/home/jovyan/hash_output"
)

PIPELINE = (
    ROOT
    / "pipeline/run_chunking.py"
)

VALIDATOR = (
    ROOT
    / "pipeline/validate_chunks.py"
)

AGGREGATOR = (
    ROOT
    / "week3/evaluate_chunks.py"
)

RUN_ROOT = (
    ROOT
    / "week3/runs/issue15"
)

RESULT_ROOT = (
    ROOT
    / "week3/results/issue15"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the frozen Week 3 parameter-sensitivity "
            "experiments."
        )
    )

    mode = parser.add_mutually_exclusive_group(
        required=True
    )

    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned commands without executing them.",
    )

    mode.add_argument(
        "--execute",
        action="store_true",
        help="Execute all non-baseline runs.",
    )

    parser.add_argument(
        "--run-id",
        help=(
            "Optionally restrict execution to one frozen "
            "non-baseline run_id."
        ),
    )

    return parser.parse_args()


def load_matrix() -> list[dict[str, str]]:
    with MATRIX.open(
        newline="",
        encoding="utf-8",
    ) as f:
        rows = list(
            csv.DictReader(f)
        )

    if len(rows) != 11:
        raise SystemExit(
            f"Expected 11 frozen configurations, "
            f"found {len(rows)}."
        )

    run_ids = [
        row["run_id"]
        for row in rows
    ]

    if len(run_ids) != len(set(run_ids)):
        raise SystemExit(
            "Duplicate run_id detected in frozen matrix."
        )

    return rows


def build_pipeline_command(
    row: dict[str, str],
    output_dir: Path,
) -> list[str]:
    method = row["method"]

    cmd = [
        sys.executable,
        str(PIPELINE),
        "--input",
        str(INPUT),
        "--output-dir",
        str(output_dir),
        "--method",
        method,
        "--chunk-size",
        row["chunk_size"],
        "--progress-every",
        "8",
        "--overwrite",
    ]

    if method == "token":
        cmd.extend(
            [
                "--tokenizer",
                row["tokenizer"],
                "--chunk-overlap",
                row["chunk_overlap"],
            ]
        )

    elif method == "recursive":
        cmd.extend(
            [
                "--tokenizer",
                row["tokenizer"],
                "--min-characters-per-chunk",
                row["min_characters_per_chunk"],
            ]
        )

    elif method == "semantic":
        cmd.extend(
            [
                "--embedding-model",
                row["embedding_model"],
                "--threshold",
                row["threshold"],
            ]
        )

    else:
        raise SystemExit(
            f"Unsupported frozen method: {method}"
        )

    return cmd


def find_chunk_file(
    run_dir: Path,
) -> Path:
    files = sorted(
        run_dir.glob("*.chunks.parquet")
    )

    if len(files) != 1:
        raise RuntimeError(
            f"Expected exactly one chunk file in "
            f"{run_dir}, found {len(files)}."
        )

    return files[0]


def run_command(
    cmd: list[str],
    stdout_path: Path | None = None,
    stderr_path: Path | None = None,
) -> None:
    print("$", " ".join(cmd))

    if stdout_path is None:
        process = subprocess.run(
            cmd,
            text=True,
        )
    else:
        with stdout_path.open(
            "w",
            encoding="utf-8",
        ) as stdout_file, stderr_path.open(
            "w",
            encoding="utf-8",
        ) as stderr_file:
            process = subprocess.run(
                cmd,
                stdout=stdout_file,
                stderr=stderr_file,
                text=True,
            )

    if process.returncode != 0:
        raise SystemExit(
            f"Command failed with return code "
            f"{process.returncode}: "
            + " ".join(cmd)
        )


def execute_run(
    row: dict[str, str],
) -> None:
    run_id = row["run_id"]

    run_dir = (
        RUN_ROOT
        / run_id
    )

    result_dir = (
        RESULT_ROOT
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

    result_dir.mkdir(
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

    pipeline_cmd = (
        build_pipeline_command(
            row,
            run_dir,
        )
    )

    print()
    print("=" * 72)
    print("RUN:", run_id)
    print("=" * 72)

    run_command(
        pipeline_cmd,
        stdout_path,
        stderr_path,
    )

    chunk_file = (
        find_chunk_file(
            run_dir
        )
    )

    metadata_path = (
        run_dir
        / "run_metadata.json"
    )

    if not metadata_path.exists():
        raise SystemExit(
            f"Missing run metadata: {metadata_path}"
        )

    qa_cmd = [
        sys.executable,
        str(VALIDATOR),
        "--chunks",
        str(chunk_file),
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

    aggregator_cmd = [
        sys.executable,
        str(AGGREGATOR),
        "--run-dir",
        str(run_dir),
        "--output-dir",
        str(result_dir),
    ]

    run_command(
        aggregator_cmd
    )

    summary_path = (
        result_dir
        / "summary.json"
    )

    summary = json.loads(
        summary_path.read_text(
            encoding="utf-8"
        )
    )

    run = summary["run"]

    print()
    print(
        f"COMPLETED {run_id}: "
        f"documents={run['processed_documents']} "
        f"chunks={run['total_chunks']} "
        f"warnings={run['warning_count']} "
        f"qa={run['qa_status']}"
    )


def main() -> None:
    args = parse_args()

    rows = load_matrix()

    rows = [
        row
        for row in rows
        if row["is_baseline"] != "true"
    ]

    if args.run_id:
        rows = [
            row
            for row in rows
            if row["run_id"]
            == args.run_id
        ]

        if not rows:
            raise SystemExit(
                "Requested run_id is not a frozen "
                "non-baseline configuration."
            )

    print(
        "Frozen non-baseline runs:",
        len(rows),
    )

    if args.dry_run:
        for row in rows:
            run_dir = (
                RUN_ROOT
                / row["run_id"]
            )

            cmd = build_pipeline_command(
                row,
                run_dir,
            )

            print()
            print(
                row["run_id"]
            )
            print(
                "  method:",
                row["method"],
            )
            print(
                "  axis:",
                row["experiment_axis"],
            )
            print(
                "  command:",
                " ".join(cmd),
            )

        print()
        print(
            "ISSUE #15 LAUNCHER DRY RUN: PASS"
        )

        return

    completed = 0

    for row in rows:
        execute_run(row)
        completed += 1

    print()
    print("=" * 72)
    print(
        "ISSUE #15 EXECUTION COMPLETE"
    )
    print(
        "New runs completed:",
        completed,
    )
    print("=" * 72)


if __name__ == "__main__":
    main()
