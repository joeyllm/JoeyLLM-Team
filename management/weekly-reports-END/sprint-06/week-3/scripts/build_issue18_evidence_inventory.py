from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(
    "/home/jovyan/chunking_sprint"
)

REPORT_DIR = (
    ROOT
    / "week3/reports"
)

JSON_PATH = (
    REPORT_DIR
    / "issue18_evidence_inventory.json"
)

CSV_PATH = (
    REPORT_DIR
    / "issue18_evidence_inventory.csv"
)

MD_PATH = (
    REPORT_DIR
    / "issue18_evidence_inventory.md"
)

FREEZE_PATH = (
    REPORT_DIR
    / "issue18_reproducibility_freeze.json"
)


REPRESENTATIVE_INPUT = Path(
    "/home/jovyan/hash_output/_audit/"
    "profiling/representative_samples.parquet"
)

WEEK3_INPUT_HASH_FILE = (
    ROOT
    / "week3/configs/"
      "week3_input_sha256.txt"
)

DATASET_MANIFEST = Path(
    "/home/jovyan/hash_output/_audit/"
    "chunking_input_sha256_manifest.txt"
)

DATASET_FREEZE_RECORD = Path(
    "/home/jovyan/hash_output/_audit/"
    "dataset_freeze.md"
)


# ------------------------------------------------------------
# Required high-level evidence
# ------------------------------------------------------------

REQUIRED_FILES = {
    # Week 3 design
    "design.baseline_configs":
        ROOT
        / "week3/configs/"
          "baseline_configs.json",

    "design.parameter_matrix":
        ROOT
        / "week3/configs/"
          "parameter_sensitivity_matrix.csv",

    "design.experimental_constants":
        ROOT
        / "week3/configs/"
          "experimental_constants.json",

    "design.week3_input_sha256":
        WEEK3_INPUT_HASH_FILE,

    "design.environment_snapshot":
        ROOT
        / "week3/configs/"
          "environment_snapshot.json",

    "design.experiment_plan":
        ROOT
        / "week3/"
          "week3_experiment_plan.md",

    # Evaluation metric specification
    "evaluation.metric_spec":
        ROOT
        / "week3/configs/"
          "evaluation_metric_spec.md",

    "evaluation.metric_schema":
        ROOT
        / "week3/configs/"
          "evaluation_metric_schema.json",

    "evaluation.aggregator":
        ROOT
        / "week3/evaluate_chunks.py",

    # Baselines
    "baseline.token.json":
        ROOT
        / "week3/results/"
          "baseline_token/summary.json",

    "baseline.token.csv":
        ROOT
        / "week3/results/"
          "baseline_token/summary.csv",

    "baseline.token.md":
        ROOT
        / "week3/results/"
          "baseline_token/report.md",

    "baseline.recursive.json":
        ROOT
        / "week3/results/"
          "baseline_recursive/summary.json",

    "baseline.recursive.csv":
        ROOT
        / "week3/results/"
          "baseline_recursive/summary.csv",

    "baseline.recursive.md":
        ROOT
        / "week3/results/"
          "baseline_recursive/report.md",

    "baseline.semantic.json":
        ROOT
        / "week3/results/"
          "baseline_semantic/summary.json",

    "baseline.semantic.csv":
        ROOT
        / "week3/results/"
          "baseline_semantic/summary.csv",

    "baseline.semantic.md":
        ROOT
        / "week3/results/"
          "baseline_semantic/report.md",

    # Parameter sensitivity
    "sensitivity.summary_json":
        ROOT
        / "week3/results/"
          "parameter_sensitivity/"
          "parameter_sensitivity_summary.json",

    "sensitivity.summary_csv":
        ROOT
        / "week3/results/"
          "parameter_sensitivity/"
          "parameter_sensitivity_summary.csv",

    "sensitivity.report":
        ROOT
        / "week3/results/"
          "parameter_sensitivity/"
          "parameter_sensitivity_report.md",

    "sensitivity.observations":
        ROOT
        / "week3/results/"
          "parameter_sensitivity/"
          "parameter_sensitivity_observations.md",

    # Issue 16
    "matched.matching_protocol":
        ROOT
        / "week3/configs/"
          "issue16_matching_protocol.md",

    "matched.comparison_protocol":
        ROOT
        / "week3/configs/"
          "issue16_comparison_protocol.md",

    "matched.settings":
        ROOT
        / "week3/configs/"
          "issue16_matched_settings.json",

    "matched.calibration_matrix":
        ROOT
        / "week3/configs/"
          "issue16_calibration_matrix.csv",

    "matched.token_calibration_matrix":
        ROOT
        / "week3/configs/"
          "issue16_token_calibration_matrix.csv",

    "matched.recursive_calibration_matrix":
        ROOT
        / "week3/configs/"
          "issue16_recursive_calibration_matrix.csv",

    "matched.summary_json":
        ROOT
        / "week3/results/issue16/"
          "matched_comparison/"
          "matched_comparison.json",

    "matched.summary_csv":
        ROOT
        / "week3/results/issue16/"
          "matched_comparison/"
          "matched_comparison.csv",

    "matched.groups_csv":
        ROOT
        / "week3/results/issue16/"
          "matched_comparison/"
          "matched_sample_groups.csv",

    "matched.report":
        ROOT
        / "week3/results/issue16/"
          "matched_comparison/"
          "matched_comparison.md",

    "matched.interpretation":
        ROOT
        / "week3/results/issue16/"
          "matched_comparison/"
          "matched_comparison_interpretation.md",

    # Issue 17
    "robustness.protocol":
        ROOT
        / "week3/configs/"
          "issue17_analysis_protocol.md",

    "robustness.long_runtime_protocol":
        ROOT
        / "week3/configs/"
          "issue17_long_runtime_protocol.md",

    "robustness.summary_json":
        ROOT
        / "week3/results/issue17/"
          "robustness_summary.json",

    "robustness.groups_csv":
        ROOT
        / "week3/results/issue17/"
          "robustness_by_group.csv",

    "robustness.cost_csv":
        ROOT
        / "week3/results/issue17/"
          "computational_cost.csv",

    "robustness.report":
        ROOT
        / "week3/results/issue17/"
          "robustness_summary.md",

    "robustness.scaled_json":
        ROOT
        / "week3/results/issue17/"
          "scaled_engineering_evidence.json",

    "robustness.scaled_md":
        ROOT
        / "week3/results/issue17/"
          "scaled_engineering_evidence.md",

    "robustness.long_runtime_json":
        ROOT
        / "week3/results/issue17/"
          "long_runtime/"
          "long_runtime_summary.json",

    "robustness.long_runtime_csv":
        ROOT
        / "week3/results/issue17/"
          "long_runtime/"
          "long_runtime_summary.csv",

    "robustness.long_runtime_md":
        ROOT
        / "week3/results/issue17/"
          "long_runtime/"
          "long_runtime_summary.md",

    "robustness.final_report":
        ROOT
        / "week3/results/issue17/"
          "final_report.md",

    "robustness.final_summary":
        ROOT
        / "week3/results/issue17/"
          "final_summary.json",

    # Week 2 scaled evidence
    "scaled.run_metadata":
        ROOT
        / "runs/issue11_token_part0/"
          "run_metadata.json",

    "scaled.qa":
        ROOT
        / "runs/issue11_token_part0/"
          "scaled_qa_summary.json",

    "scaled.resources":
        ROOT
        / "runs/issue11_token_part0/"
          "resource_usage.txt",

    "scaled.stdout":
        ROOT
        / "runs/issue11_token_part0/"
          "pipeline.stdout.log",

    "scaled.stderr":
        ROOT
        / "runs/issue11_token_part0/"
          "pipeline.stderr.log",

    # Environment files
    "environment.requirements":
        ROOT
        / "requirements.txt",

    "environment.lock":
        ROOT
        / "requirements-lock.txt",

    # Dataset freeze evidence
    "dataset.freeze_manifest":
        DATASET_MANIFEST,

    "dataset.freeze_record":
        DATASET_FREEZE_RECORD,
}


# ------------------------------------------------------------
# Raw run IDs which directly support the final report
# ------------------------------------------------------------

BASELINE_RUNS = {
    "token":
        ROOT
        / "runs/issue10_token",
    "recursive":
        ROOT
        / "runs/issue10_recursive",
    "semantic":
        ROOT
        / "runs/issue10_semantic",
}

ISSUE15_RUN_IDS = [
    "token_cs1024",
    "token_cs4096",
    "recursive_cs1024",
    "recursive_cs4096",
    "semantic_cs1024",
    "semantic_cs4096",
    "semantic_th070",
    "semantic_th090",
]

ISSUE16_MATCHED_RUN_IDS = [
    "token_cal_cs839",
    "recursive_cal_cs1025",
    "semantic_cal_th030",
]

ISSUE17_LONG_RUN_IDS = [
    "length_p95__token",
    "length_p95__recursive",
    "length_p95__semantic",
    "length_p99__token",
    "length_p99__recursive",
    "length_p99__semantic",
    "length_max__token",
    "length_max__recursive",
    "length_max__semantic",
]


# ------------------------------------------------------------
# Frozen / derived inputs
# ------------------------------------------------------------

DERIVED_INPUTS = [
    ROOT
    / "week3/inputs/"
      "issue17_long_documents.parquet",

    ROOT
    / "week3/inputs/"
      "issue17_length_p95.parquet",

    ROOT
    / "week3/inputs/"
      "issue17_length_p99.parquet",

    ROOT
    / "week3/inputs/"
      "issue17_length_max.parquet",

    ROOT
    / "week3/inputs/"
      "issue17_long_runtime_inputs.json",
]


HASH_LIMIT = (
    128
    * 1024
    * 1024
)


def sha256_file(
    path: Path,
) -> str:
    digest = hashlib.sha256()

    with path.open(
        "rb"
    ) as f:
        while True:
            block = f.read(
                1024 * 1024
            )

            if not block:
                break

            digest.update(
                block
            )

    return digest.hexdigest()


def relative_display(
    path: Path,
) -> str:
    try:
        return str(
            path.relative_to(
                ROOT
            )
        )
    except ValueError:
        return str(path)


def record_file(
    key: str,
    category: str,
    path: Path,
    *,
    force_hash: bool = False,
) -> dict:
    assert path.exists(), (
        f"Missing required evidence: "
        f"{key}: {path}"
    )

    assert path.is_file(), (
        f"Expected file: {path}"
    )

    size = path.stat().st_size

    should_hash = (
        force_hash
        or size <= HASH_LIMIT
    )

    return {
        "key": key,
        "category": category,
        "path": str(path),
        "display_path":
            relative_display(path),
        "bytes": size,
        "sha256": (
            sha256_file(path)
            if should_hash
            else None
        ),
        "hash_status": (
            "computed"
            if should_hash
            else "skipped_large_non_input"
        ),
    }


def parse_sha256_manifest(
    path: Path,
) -> list[dict]:
    records = []

    pattern = re.compile(
        r"^([0-9a-fA-F]{64})"
        r"\s+\*?(.*?)\s*$"
    )

    for line_number, raw in enumerate(
        path.read_text(
            encoding="utf-8",
            errors="replace",
        ).splitlines(),
        start=1,
    ):
        text = raw.strip()

        if (
            not text
            or text.startswith("#")
        ):
            continue

        match = pattern.match(
            text
        )

        if match:
            records.append(
                {
                    "line":
                        line_number,
                    "sha256":
                        match.group(1).lower(),
                    "path":
                        match.group(2),
                    "raw":
                        raw,
                }
            )

    return records


def read_json(
    path: Path,
):
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def check_qa(
    path: Path,
    label: str,
) -> dict:
    assert path.exists(), (
        f"Missing QA summary: "
        f"{label}: {path}"
    )

    qa = read_json(
        path
    )

    assert (
        qa.get("status")
        == "pass"
    ), (
        label,
        qa.get("status"),
    )

    assert (
        qa.get(
            "hard_failure_events",
            0,
        )
        == 0
    ), (
        label,
        qa.get(
            "hard_failure_events"
        ),
    )

    return {
        "label": label,
        "path": str(path),
        "status":
            qa.get("status"),
        "documents_checked":
            qa.get(
                "documents_checked"
            ),
        "chunks_checked":
            qa.get(
                "chunks_checked"
            ),
        "warning_count":
            qa.get(
                "warning_count"
            ),
        "hard_failure_events":
            qa.get(
                "hard_failure_events"
            ),
    }


def check_metadata(
    path: Path,
    label: str,
) -> dict:
    assert path.exists(), (
        f"Missing run metadata: "
        f"{label}: {path}"
    )

    data = read_json(
        path
    )

    assert (
        data.get("status")
        == "completed"
    ), (
        label,
        data.get("status"),
    )

    assert (
        data.get(
            "failed_documents"
        )
        == 0
    ), (
        label,
        data.get(
            "failed_documents"
        ),
    )

    return {
        "label": label,
        "path": str(path),
        "status":
            data.get("status"),
        "processed_documents":
            data.get(
                "processed_documents"
            ),
        "chunks_written":
            data.get(
                "chunks_written"
            ),
        "failed_documents":
            data.get(
                "failed_documents"
            ),
        "elapsed_seconds":
            data.get(
                "elapsed_seconds"
            ),
        "configuration":
            data.get(
                "configuration"
            ),
    }


def git_snapshot() -> dict:
    result = {
        "available": False,
        "repository_toplevel": None,
        "head_available": False,
        "head": None,
        "head_error": None,
        "branch": None,
        "working_tree_lines": [],
    }

    try:
        toplevel = subprocess.run(
            [
                "git",
                "rev-parse",
                "--show-toplevel",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )

    except (
        FileNotFoundError,
        subprocess.CalledProcessError,
    ):
        return result

    result["available"] = True
    result["repository_toplevel"] = (
        toplevel.stdout.strip()
    )

    head = subprocess.run(
        [
            "git",
            "rev-parse",
            "HEAD",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    if head.returncode == 0:
        result["head_available"] = True
        result["head"] = (
            head.stdout.strip()
        )
    else:
        result["head_error"] = (
            head.stderr.strip()
        )

    branch = subprocess.run(
        [
            "git",
            "branch",
            "--show-current",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    status = subprocess.run(
        [
            "git",
            "status",
            "--porcelain",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    result["branch"] = (
        branch.stdout.strip()
    )

    result[
        "working_tree_lines"
    ] = [
        line
        for line
        in status.stdout.splitlines()
        if line
    ]

    return result

def main() -> None:
    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    inventory = []

    # --------------------------------------------------------
    # High-level evidence
    # --------------------------------------------------------

    for key, path in (
        REQUIRED_FILES.items()
    ):
        category = key.split(
            ".",
            1,
        )[0]

        inventory.append(
            record_file(
                key,
                category,
                path,
            )
        )

    # --------------------------------------------------------
    # Validate Week 3 representative input hash
    # --------------------------------------------------------

    assert (
        REPRESENTATIVE_INPUT.exists()
    )

    rep_current_hash = (
        sha256_file(
            REPRESENTATIVE_INPUT
        )
    )

    week3_hash_entries = (
        parse_sha256_manifest(
            WEEK3_INPUT_HASH_FILE
        )
    )

    assert week3_hash_entries, (
        "No parseable SHA256 entry in "
        f"{WEEK3_INPUT_HASH_FILE}"
    )

    matching_entries = [
        entry
        for entry
        in week3_hash_entries
        if Path(
            entry["path"]
        ).name
        == REPRESENTATIVE_INPUT.name
    ]

    if not matching_entries:
        assert (
            len(
                week3_hash_entries
            )
            == 1
        ), (
            "Could not identify "
            "representative input entry "
            "in week3_input_sha256.txt"
        )

        matching_entries = [
            week3_hash_entries[0]
        ]

    assert (
        len(matching_entries)
        == 1
    )

    expected_rep_hash = (
        matching_entries[0][
            "sha256"
        ]
    )

    assert (
        rep_current_hash
        == expected_rep_hash
    ), (
        "Representative sample "
        "SHA256 mismatch."
    )

    representative_freeze = {
        "path":
            str(
                REPRESENTATIVE_INPUT
            ),
        "bytes":
            REPRESENTATIVE_INPUT
            .stat()
            .st_size,
        "expected_sha256":
            expected_rep_hash,
        "current_sha256":
            rep_current_hash,
        "status":
            "match",
        "hash_manifest":
            str(
                WEEK3_INPUT_HASH_FILE
            ),
        "hash_manifest_line":
            matching_entries[0][
                "line"
            ],
    }

    inventory.append(
        record_file(
            "input.representative_sample",
            "input",
            REPRESENTATIVE_INPUT,
            force_hash=True,
        )
    )

    # --------------------------------------------------------
    # Freeze Issue 17 derived inputs
    # --------------------------------------------------------

    derived_freeze = []

    for path in DERIVED_INPUTS:
        assert path.exists(), (
            f"Missing derived input: "
            f"{path}"
        )

        entry = record_file(
            "input."
            + path.stem,
            "input",
            path,
            force_hash=True,
        )

        inventory.append(
            entry
        )

        derived_freeze.append(
            {
                "path":
                    str(path),
                "bytes":
                    path.stat()
                    .st_size,
                "sha256":
                    entry["sha256"],
            }
        )

    # --------------------------------------------------------
    # Existing full-dataset freeze evidence
    # --------------------------------------------------------

    dataset_entries = (
        parse_sha256_manifest(
            DATASET_MANIFEST
        )
    )

    assert (
        len(dataset_entries)
        == 57
    ), (
        "Expected 57 entries in "
        "dataset freeze manifest; "
        f"found {len(dataset_entries)}"
    )

    dataset_freeze = {
        "manifest_path":
            str(DATASET_MANIFEST),
        "manifest_entries":
            len(dataset_entries),
        "manifest_sha256":
            sha256_file(
                DATASET_MANIFEST
            ),
        "freeze_record_path":
            str(
                DATASET_FREEZE_RECORD
            ),
        "freeze_record_sha256":
            sha256_file(
                DATASET_FREEZE_RECORD
            ),
        "note": (
            "The existing 57-file "
            "dataset SHA256 manifest "
            "is preserved as the "
            "full frozen-dataset "
            "integrity evidence. "
            "Issue 18 does not rehash "
            "the approximately 25 GiB "
            "dataset."
        ),
    }

    # --------------------------------------------------------
    # Raw baseline QA + metadata
    # --------------------------------------------------------

    qa_records = []
    metadata_records = []

    for method, run_dir in (
        BASELINE_RUNS.items()
    ):
        qa_records.append(
            check_qa(
                run_dir
                / "qa/"
                  "qa_summary.json",
                f"baseline.{method}",
            )
        )

        metadata_records.append(
            check_metadata(
                run_dir
                / "run_metadata.json",
                f"baseline.{method}",
            )
        )

    # --------------------------------------------------------
    # Issue 15 non-baseline sensitivity raw runs
    # --------------------------------------------------------

    for run_id in (
        ISSUE15_RUN_IDS
    ):
        run_dir = (
            ROOT
            / "week3/runs/issue15"
            / run_id
        )

        qa_records.append(
            check_qa(
                run_dir
                / "qa/"
                  "qa_summary.json",
                f"issue15.{run_id}",
            )
        )

        metadata_records.append(
            check_metadata(
                run_dir
                / "run_metadata.json",
                f"issue15.{run_id}",
            )
        )

    # --------------------------------------------------------
    # Issue 16 matched raw runs
    # --------------------------------------------------------

    for run_id in (
        ISSUE16_MATCHED_RUN_IDS
    ):
        run_dir = (
            ROOT
            / "week3/runs/issue16"
            / run_id
        )

        qa_records.append(
            check_qa(
                run_dir
                / "qa/"
                  "qa_summary.json",
                f"issue16.{run_id}",
            )
        )

        metadata_records.append(
            check_metadata(
                run_dir
                / "run_metadata.json",
                f"issue16.{run_id}",
            )
        )

    # --------------------------------------------------------
    # Issue 17 long-document raw runs
    # --------------------------------------------------------

    for run_id in (
        ISSUE17_LONG_RUN_IDS
    ):
        run_dir = (
            ROOT
            / "week3/runs/issue17/"
              "long_runtime"
            / run_id
        )

        qa_records.append(
            check_qa(
                run_dir
                / "qa/"
                  "qa_summary.json",
                f"issue17.{run_id}",
            )
        )

        metadata_records.append(
            check_metadata(
                run_dir
                / "run_metadata.json",
                f"issue17.{run_id}",
            )
        )

    # --------------------------------------------------------
    # Week 2 scaled run
    # --------------------------------------------------------

    scaled_metadata_path = (
        ROOT
        / "runs/issue11_token_part0/"
          "run_metadata.json"
    )

    scaled_qa_path = (
        ROOT
        / "runs/issue11_token_part0/"
          "scaled_qa_summary.json"
    )

    metadata_records.append(
        check_metadata(
            scaled_metadata_path,
            "week2.scaled_token",
        )
    )

    scaled_qa = read_json(
        scaled_qa_path
    )

    assert (
        scaled_qa.get("status")
        == "pass"
    )

    assert (
        scaled_qa[
            "documents_checked"
        ]
        == 227628
    )

    assert (
        scaled_qa[
            "chunks_checked"
        ]
        == 1334973
    )

    qa_records.append(
        {
            "label":
                "week2.scaled_token",
            "path":
                str(
                    scaled_qa_path
                ),
            "status":
                scaled_qa.get(
                    "status"
                ),
            "documents_checked":
                scaled_qa.get(
                    "documents_checked"
                ),
            "chunks_checked":
                scaled_qa.get(
                    "chunks_checked"
                ),
            "warning_count":
                scaled_qa.get(
                    "warning_count"
                ),
            "hard_failure_events":
                scaled_qa.get(
                    "hard_failure_events"
                ),
        }
    )

    # --------------------------------------------------------
    # Validate summary-level counts
    # --------------------------------------------------------

    baseline_summaries = []

    for method in [
        "token",
        "recursive",
        "semantic",
    ]:
        path = (
            ROOT
            / "week3/results"
            / f"baseline_{method}"
            / "summary.json"
        )

        data = read_json(
            path
        )

        assert (
            data["run"][
                "processed_documents"
            ]
            == 32
        )

        assert (
            data["run"][
                "failed_documents"
            ]
            == 0
        )

        assert (
            data["run"][
                "qa_status"
            ]
            == "pass"
        )

        baseline_summaries.append(
            {
                "method":
                    method,
                "processed_documents":
                    data["run"][
                        "processed_documents"
                    ],
                "total_chunks":
                    data["run"][
                        "total_chunks"
                    ],
                "warning_count":
                    data["run"][
                        "warning_count"
                    ],
                "qa_status":
                    data["run"][
                        "qa_status"
                    ],
            }
        )

    sensitivity = read_json(
        ROOT
        / "week3/results/"
          "parameter_sensitivity/"
          "parameter_sensitivity_summary.json"
    )

    assert (
        sensitivity[
            "configuration_count"
        ]
        == 11
    )

    assert (
        len(
            sensitivity[
                "records"
            ]
        )
        == 11
    )

    matched = read_json(
        ROOT
        / "week3/results/issue16/"
          "matched_comparison/"
          "matched_comparison.json"
    )

    assert (
        matched[
            "source_documents"
        ]
        == 32
    )

    assert (
        len(
            matched["methods"]
        )
        == 3
    )

    issue17 = read_json(
        ROOT
        / "week3/results/issue17/"
          "final_summary.json"
    )

    assert (
        issue17[
            "representative_sample"
        ]["documents"]
        == 32
    )

    assert (
        issue17[
            "long_document_analysis"
        ]["controlled_runs"]
        == 9
    )

    assert (
        issue17[
            "long_document_analysis"
        ]["all_qa_pass"]
        is True
    )

    # --------------------------------------------------------
    # QA totals
    # --------------------------------------------------------

    assert (
        len(qa_records)
        == (
            3
            + 8
            + 3
            + 9
            + 1
        )
    )

    assert all(
        record["status"]
        == "pass"
        for record
        in qa_records
    )

    assert all(
        (
            record[
                "hard_failure_events"
            ]
            in (
                None,
                0,
            )
        )
        for record
        in qa_records
    )

    assert all(
        record[
            "failed_documents"
        ]
        == 0
        for record
        in metadata_records
    )

    # --------------------------------------------------------
    # Git snapshot
    # --------------------------------------------------------

    git = git_snapshot()

    # --------------------------------------------------------
    # Inventory deterministic ordering
    # --------------------------------------------------------

    inventory = sorted(
        inventory,
        key=lambda item: (
            item["category"],
            item["key"],
        ),
    )

    # --------------------------------------------------------
    # Reproducibility freeze
    # --------------------------------------------------------

    freeze = {
        "schema_version": 1,
        "issue": 18,
        "representative_input":
            representative_freeze,
        "derived_issue17_inputs":
            derived_freeze,
        "full_dataset_freeze":
            dataset_freeze,
        "environment": {
            "environment_snapshot":
                str(
                    ROOT
                    / "week3/configs/"
                      "environment_snapshot.json"
                ),
            "environment_snapshot_sha256":
                sha256_file(
                    ROOT
                    / "week3/configs/"
                      "environment_snapshot.json"
                ),
            "requirements":
                str(
                    ROOT
                    / "requirements.txt"
                ),
            "requirements_sha256":
                sha256_file(
                    ROOT
                    / "requirements.txt"
                ),
            "requirements_lock":
                str(
                    ROOT
                    / "requirements-lock.txt"
                ),
            "requirements_lock_sha256":
                sha256_file(
                    ROOT
                    / "requirements-lock.txt"
                ),
        },
        "git": git,
    }

    FREEZE_PATH.write_text(
        json.dumps(
            freeze,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # Evidence inventory JSON
    # --------------------------------------------------------

    output = {
        "schema_version": 1,
        "issue": 18,
        "purpose":
            "Final Week 3 evidence inventory",
        "required_artifacts":
            inventory,
        "required_artifact_count":
            len(inventory),
        "baseline_summaries":
            baseline_summaries,
        "parameter_sensitivity": {
            "configuration_count":
                sensitivity[
                    "configuration_count"
                ],
            "record_count":
                len(
                    sensitivity[
                        "records"
                    ]
                ),
        },
        "matched_comparison": {
            "source_documents":
                matched[
                    "source_documents"
                ],
            "method_count":
                len(
                    matched[
                        "methods"
                    ]
                ),
            "worst_relative_spread":
                matched[
                    "matching"
                ][
                    "worst_relative_spread"
                ],
        },
        "issue17": {
            "representative_documents":
                issue17[
                    "representative_sample"
                ]["documents"],
            "representative_groups":
                len(
                    issue17[
                        "representative_sample"
                    ]["groups"]
                ),
            "long_runtime_runs":
                issue17[
                    "long_document_analysis"
                ][
                    "controlled_runs"
                ],
            "long_runtime_all_qa_pass":
                issue17[
                    "long_document_analysis"
                ][
                    "all_qa_pass"
                ],
            "scaled_documents":
                issue17[
                    "scaled_engineering_evidence"
                ][
                    "processed_documents"
                ],
            "scaled_chunks":
                issue17[
                    "scaled_engineering_evidence"
                ][
                    "chunks_written"
                ],
        },
        "raw_run_evidence": {
            "qa_summary_count":
                len(
                    qa_records
                ),
            "run_metadata_count":
                len(
                    metadata_records
                ),
            "qa":
                qa_records,
            "metadata":
                metadata_records,
        },
        "reproducibility_freeze":
            str(FREEZE_PATH),
    }

    JSON_PATH.write_text(
        json.dumps(
            output,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # Inventory CSV
    # --------------------------------------------------------

    with CSV_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "key",
                "category",
                "display_path",
                "bytes",
                "sha256",
                "hash_status",
            ],
        )

        writer.writeheader()

        for row in inventory:
            writer.writerow(
                {
                    key:
                        row[key]
                    for key in [
                        "key",
                        "category",
                        "display_path",
                        "bytes",
                        "sha256",
                        "hash_status",
                    ]
                }
            )

    # --------------------------------------------------------
    # Human-readable inventory report
    # --------------------------------------------------------

    categories = {}

    for row in inventory:
        categories.setdefault(
            row["category"],
            [],
        ).append(
            row
        )

    lines = [
        "# Issue 18 — Final Evidence Inventory",
        "",
        "## Reproducibility Freeze",
        "",
        (
            "- Representative sample SHA256: "
            f"`{rep_current_hash}`"
        ),
        "- Representative sample hash match: `PASS`",
        (
            "- Full dataset freeze-manifest entries: "
            f"{len(dataset_entries)}"
        ),
        (
            "- Full dataset manifest SHA256: "
            f"`{dataset_freeze['manifest_sha256']}`"
        ),
        (
            "- Issue 17 derived inputs frozen: "
            f"{len(derived_freeze)}"
        ),
        "",
        "## Evidence Coverage",
        "",
        (
            "- Baseline methods: "
            f"{len(baseline_summaries)}"
        ),
        (
            "- Parameter-sensitivity configurations: "
            f"{sensitivity['configuration_count']}"
        ),
        (
            "- Matched-comparison methods: "
            f"{len(matched['methods'])}"
        ),
        (
            "- Representative robustness groups: "
            f"{len(issue17['representative_sample']['groups'])}"
        ),
        (
            "- Long-document controlled runs: "
            f"{issue17['long_document_analysis']['controlled_runs']}"
        ),
        (
            "- Raw QA summaries verified: "
            f"{len(qa_records)}"
        ),
        (
            "- Raw run metadata records verified: "
            f"{len(metadata_records)}"
        ),
        "",
        "## Required Artifacts",
        "",
    ]

    for category in sorted(
        categories
    ):
        lines.extend(
            [
                f"### {category}",
                "",
                "| Key | Path | Bytes | SHA256 status |",
                "|---|---|---:|---|",
            ]
        )

        for row in categories[
            category
        ]:
            lines.append(
                f"| `{row['key']}` "
                f"| `{row['display_path']}` "
                f"| {row['bytes']} "
                f"| {row['hash_status']} |"
            )

        lines.append("")

    lines.extend(
        [
            "## Git Snapshot",
            "",
            (
                "- Git available: "
                f"`{git['available']}`"
            ),
        ]
    )

    if git["available"]:
        lines.extend(
            [
                (
                    "- HEAD: "
                    f"`{git['head']}`"
                ),
                (
                    "- Branch: "
                    f"`{git['branch']}`"
                ),
                (
                    "- Working-tree entries: "
                    f"{len(git['working_tree_lines'])}"
                ),
            ]
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            (
                "This inventory records evidence locations "
                "and reproducibility metadata only. It does "
                "not introduce new experimental results or "
                "method rankings."
            ),
            "",
        ]
    )

    MD_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # Console summary
    # --------------------------------------------------------

    print("=" * 96)
    print(
        "ISSUE #18 FINAL EVIDENCE INVENTORY"
    )
    print("=" * 96)

    print(
        "Required artifacts:",
        len(inventory),
    )

    print(
        "Representative sample hash:",
        "PASS",
    )

    print(
        "Full dataset manifest entries:",
        len(dataset_entries),
    )

    print(
        "Baseline summaries:",
        len(baseline_summaries),
    )

    print(
        "Parameter configurations:",
        sensitivity[
            "configuration_count"
        ],
    )

    print(
        "Matched methods:",
        len(
            matched["methods"]
        ),
    )

    print(
        "Robustness groups:",
        len(
            issue17[
                "representative_sample"
            ]["groups"]
        ),
    )

    print(
        "Long runtime runs:",
        issue17[
            "long_document_analysis"
        ]["controlled_runs"],
    )

    print(
        "Raw QA summaries verified:",
        len(qa_records),
    )

    print(
        "Raw run metadata verified:",
        len(metadata_records),
    )

    print(
        "All raw QA status:",
        "PASS",
    )

    print(
        "All raw processing failures:",
        "0",
    )

    print(
        "Git snapshot available:",
        git["available"],
    )

    print()
    print(
        "Inventory JSON:",
        JSON_PATH,
    )

    print(
        "Inventory CSV:",
        CSV_PATH,
    )

    print(
        "Inventory Markdown:",
        MD_PATH,
    )

    print(
        "Reproducibility freeze:",
        FREEZE_PATH,
    )

    print()
    print(
        "ISSUE #18 STEP 1 EVIDENCE "
        "INVENTORY BUILD: PASS"
    )


if __name__ == "__main__":
    main()
