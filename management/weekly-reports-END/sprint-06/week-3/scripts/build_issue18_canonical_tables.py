from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(
    "/home/jovyan/chunking_sprint"
)

OUTPUT_DIR = (
    ROOT
    / "week3/reports/tables"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ---------------------------------------------------------------------
# Source paths
# ---------------------------------------------------------------------

BASELINE_PATHS = {
    method: (
        ROOT
        / "week3/results"
        / f"baseline_{method}"
        / "summary.json"
    )
    for method in [
        "token",
        "recursive",
        "semantic",
    ]
}

SENSITIVITY_PATH = (
    ROOT
    / "week3/results/"
      "parameter_sensitivity/"
      "parameter_sensitivity_summary.json"
)

MATCHED_JSON_PATH = (
    ROOT
    / "week3/results/issue16/"
      "matched_comparison/"
      "matched_comparison.json"
)

MATCHED_CSV_PATH = (
    ROOT
    / "week3/results/issue16/"
      "matched_comparison/"
      "matched_comparison.csv"
)

ROBUSTNESS_PATH = (
    ROOT
    / "week3/results/issue17/"
      "robustness_summary.json"
)

LONG_RUNTIME_PATH = (
    ROOT
    / "week3/results/issue17/"
      "long_runtime/"
      "long_runtime_summary.json"
)

SCALED_PATH = (
    ROOT
    / "week3/results/issue17/"
      "scaled_engineering_evidence.json"
)

INVENTORY_PATH = (
    ROOT
    / "week3/reports/"
      "issue18_evidence_inventory.json"
)


# ---------------------------------------------------------------------
# Output paths
# ---------------------------------------------------------------------

BASELINE_OUT = (
    OUTPUT_DIR
    / "baseline_results.csv"
)

SENSITIVITY_OUT = (
    OUTPUT_DIR
    / "parameter_sensitivity.csv"
)

MATCHED_OUT = (
    OUTPUT_DIR
    / "matched_granularity.csv"
)

ROBUSTNESS_OUT = (
    OUTPUT_DIR
    / "robustness_summary.csv"
)

LONG_RUNTIME_OUT = (
    OUTPUT_DIR
    / "long_document_runtime.csv"
)

COST_OUT = (
    OUTPUT_DIR
    / "computational_cost.csv"
)

RELIABILITY_OUT = (
    OUTPUT_DIR
    / "reliability_qa.csv"
)

SCALED_OUT = (
    OUTPUT_DIR
    / "scaled_engineering_evidence.csv"
)

SUMMARY_OUT = (
    OUTPUT_DIR
    / "week3_canonical_summary.json"
)


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def load_json(
    path: Path,
):
    assert path.exists(), path

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def read_csv(
    path: Path,
):
    assert path.exists(), path

    with path.open(
        newline="",
        encoding="utf-8",
    ) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = list(
            reader.fieldnames or []
        )

    return fields, rows


def write_csv(
    path: Path,
    rows: list[dict],
    fields: list[str] | None = None,
):
    assert rows, (
        f"No rows for {path}"
    )

    if fields is None:
        fields = list(
            rows[0].keys()
        )

    expected = set(fields)

    for index, row in enumerate(rows):
        assert (
            set(row.keys())
            == expected
        ), (
            f"Schema mismatch in "
            f"{path.name} row {index}"
        )

    with path.open(
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


def json_text(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def display_path(
    path: Path,
) -> str:
    return str(
        path.relative_to(ROOT)
    )


def sha256_file(
    path: Path,
) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as f:
        while True:
            block = f.read(
                1024 * 1024
            )

            if not block:
                break

            digest.update(block)

    return digest.hexdigest()


# ---------------------------------------------------------------------
# 1. Baseline table
# ---------------------------------------------------------------------

baseline_rows = []

for method, path in (
    BASELINE_PATHS.items()
):
    data = load_json(path)

    run = data["run"]
    metrics = data["metrics"]

    char_length = (
        metrics["char_length"]
    )

    chunks_per_document = (
        metrics[
            "chunks_per_document"
        ]
    )

    boundaries = (
        metrics[
            "boundaries"
        ][
            "percentages_internal_only"
        ]
    )

    assert (
        run["method"]
        == method
    )

    assert (
        run["processed_documents"]
        == 32
    )

    assert (
        run["failed_documents"]
        == 0
    )

    assert (
        run["qa_status"]
        == "pass"
    )

    assert (
        data["validation"][
            "char_length_mismatches"
        ]
        == 0
    )

    assert (
        data["validation"][
            "required_columns_present"
        ]
        is True
    )

    baseline_rows.append(
        {
            "method":
                method,
            "processed_documents":
                run[
                    "processed_documents"
                ],
            "failed_documents":
                run[
                    "failed_documents"
                ],
            "total_chunks":
                run[
                    "total_chunks"
                ],
            "mean_chunks_per_document":
                chunks_per_document[
                    "mean"
                ],
            "median_chunks_per_document":
                chunks_per_document[
                    "median"
                ],
            "mean_chunk_char_length":
                char_length["mean"],
            "median_chunk_char_length":
                char_length["median"],
            "p90_chunk_char_length":
                char_length["p90"],
            "p95_chunk_char_length":
                char_length["p95"],
            "p99_chunk_char_length":
                char_length["p99"],
            "paragraph_boundary_internal":
                boundaries[
                    "paragraph_boundary"
                ],
            "newline_boundary_internal":
                boundaries[
                    "newline_boundary"
                ],
            "sentence_boundary_internal":
                boundaries[
                    "sentence_boundary"
                ],
            "whitespace_boundary_internal":
                boundaries[
                    "whitespace_boundary"
                ],
            "other_boundary_internal":
                boundaries[
                    "other_boundary"
                ],
            "elapsed_seconds":
                run[
                    "elapsed_seconds"
                ],
            "documents_per_second":
                run[
                    "documents_per_second"
                ],
            "chunks_per_second":
                run[
                    "chunks_per_second"
                ],
            "warning_count":
                run[
                    "warning_count"
                ],
            "failed_qa_events":
                run[
                    "qa_hard_failure_events"
                ],
            "qa_status":
                run[
                    "qa_status"
                ],
            "configuration_json":
                json_text(
                    run[
                        "configuration"
                    ]
                ),
            "source_summary":
                display_path(path),
        }
    )

write_csv(
    BASELINE_OUT,
    baseline_rows,
)


# ---------------------------------------------------------------------
# 2. Parameter sensitivity table
# ---------------------------------------------------------------------

sensitivity = load_json(
    SENSITIVITY_PATH
)

sensitivity_records = (
    sensitivity["records"]
)

assert (
    sensitivity[
        "configuration_count"
    ]
    == 11
)

assert (
    len(
        sensitivity_records
    )
    == 11
)

source_fields = list(
    sensitivity_records[0].keys()
)

source_field_set = set(
    source_fields
)

for row in sensitivity_records:
    assert (
        set(row.keys())
        == source_field_set
    )

sensitivity_rows = []

for row in (
    sensitivity_records
):
    new_row = {
        key: value
        for key, value
        in row.items()
    }

    new_row[
        "source_summary"
    ] = display_path(
        SENSITIVITY_PATH
    )

    sensitivity_rows.append(
        new_row
    )

write_csv(
    SENSITIVITY_OUT,
    sensitivity_rows,
    source_fields
    + ["source_summary"],
)


# ---------------------------------------------------------------------
# 3. Matched-granularity table
# ---------------------------------------------------------------------

matched_json = load_json(
    MATCHED_JSON_PATH
)

matched_fields, matched_rows_raw = (
    read_csv(
        MATCHED_CSV_PATH
    )
)

assert len(
    matched_rows_raw
) == 3

assert (
    matched_json[
        "source_documents"
    ]
    == 32
)

assert (
    len(
        matched_json[
            "methods"
        ]
    )
    == 3
)

matched_config = {
    row["method"]:
        row["configuration"]
    for row in (
        matched_json[
            "methods"
        ]
    )
}

assert set(
    matched_config
) == {
    "token",
    "recursive",
    "semantic",
}

matched_rows = []

for row in (
    matched_rows_raw
):
    method = row["method"]

    assert (
        method
        in matched_config
    )

    new_row = dict(row)

    new_row[
        "configuration_json"
    ] = json_text(
        matched_config[
            method
        ]
    )

    new_row[
        "matching_tolerance"
    ] = matched_json[
        "matching"
    ]["tolerance"]

    new_row[
        "worst_relative_spread"
    ] = matched_json[
        "matching"
    ][
        "worst_relative_spread"
    ]

    new_row[
        "source_csv"
    ] = display_path(
        MATCHED_CSV_PATH
    )

    new_row[
        "source_json"
    ] = display_path(
        MATCHED_JSON_PATH
    )

    matched_rows.append(
        new_row
    )

write_csv(
    MATCHED_OUT,
    matched_rows,
    matched_fields
    + [
        "configuration_json",
        "matching_tolerance",
        "worst_relative_spread",
        "source_csv",
        "source_json",
    ],
)


# ---------------------------------------------------------------------
# 4. Robustness table
# ---------------------------------------------------------------------

robustness = load_json(
    ROBUSTNESS_PATH
)

robustness_rows_raw = (
    robustness[
        "robustness_by_group"
    ]
)

assert len(
    robustness_rows_raw
) == 30

assert (
    robustness[
        "source_documents"
    ]
    == 32
)

assert (
    robustness[
        "group_overlap"
    ]
    is True
)

robustness_fields = list(
    robustness_rows_raw[
        0
    ].keys()
)

robustness_schema = set(
    robustness_fields
)

robustness_rows = []

for row in (
    robustness_rows_raw
):
    assert (
        set(row.keys())
        == robustness_schema
    )

    new_row = dict(row)

    new_row[
        "small_chunk_threshold"
    ] = robustness[
        "small_chunk_definition"
    ]["threshold"]

    new_row[
        "group_overlap"
    ] = robustness[
        "group_overlap"
    ]

    new_row[
        "source_summary"
    ] = display_path(
        ROBUSTNESS_PATH
    )

    robustness_rows.append(
        new_row
    )

assert {
    row["method"]
    for row in robustness_rows
} == {
    "token",
    "recursive",
    "semantic",
}

assert len({
    row["group"]
    for row in robustness_rows
}) == 10

write_csv(
    ROBUSTNESS_OUT,
    robustness_rows,
    robustness_fields
    + [
        "small_chunk_threshold",
        "group_overlap",
        "source_summary",
    ],
)


# ---------------------------------------------------------------------
# 5. Long-document runtime table
# ---------------------------------------------------------------------

long_runtime = load_json(
    LONG_RUNTIME_PATH
)

assert (
    long_runtime[
        "run_count"
    ]
    == 9
)

assert (
    long_runtime[
        "measurement_class"
    ]
    == "single_run_descriptive"
)

runtime_records = (
    long_runtime["records"]
)

assert len(
    runtime_records
) == 9

runtime_fields = [
    key
    for key in (
        runtime_records[
            0
        ].keys()
    )
    if key != "warnings"
]

runtime_rows = []

for row in runtime_records:
    assert (
        row[
            "failed_documents"
        ]
        == 0
    )

    assert (
        row[
            "qa_hard_failure_events"
        ]
        == 0
    )

    assert (
        row["qa_status"]
        == "pass"
    )

    new_row = {
        key: row[key]
        for key in runtime_fields
    }

    new_row[
        "warnings_json"
    ] = json_text(
        row["warnings"]
    )

    new_row[
        "measurement_class"
    ] = long_runtime[
        "measurement_class"
    ]

    new_row[
        "source_summary"
    ] = display_path(
        LONG_RUNTIME_PATH
    )

    runtime_rows.append(
        new_row
    )

assert {
    (
        row["group"],
        row["method"],
    )
    for row in runtime_rows
} == {
    (group, method)
    for group in [
        "length_p95",
        "length_p99",
        "length_max",
    ]
    for method in [
        "token",
        "recursive",
        "semantic",
    ]
}

write_csv(
    LONG_RUNTIME_OUT,
    runtime_rows,
    runtime_fields
    + [
        "warnings_json",
        "measurement_class",
        "source_summary",
    ],
)


# ---------------------------------------------------------------------
# 6. Computational-cost table
# ---------------------------------------------------------------------

cost_rows_raw = (
    robustness[
        "computational_cost"
    ]
)

assert len(
    cost_rows_raw
) == 3

cost_fields = list(
    cost_rows_raw[
        0
    ].keys()
)

cost_schema = set(
    cost_fields
)

cost_rows = []

for row in cost_rows_raw:
    assert (
        set(row.keys())
        == cost_schema
    )

    assert (
        row[
            "failed_documents"
        ]
        == 0
    )

    assert (
        row["qa_status"]
        == "pass"
    )

    new_row = dict(row)

    new_row[
        "source_summary"
    ] = display_path(
        ROBUSTNESS_PATH
    )

    cost_rows.append(
        new_row
    )

write_csv(
    COST_OUT,
    cost_rows,
    cost_fields
    + ["source_summary"],
)


# ---------------------------------------------------------------------
# 7. Reliability / QA table
# ---------------------------------------------------------------------

inventory = load_json(
    INVENTORY_PATH
)

raw_evidence = (
    inventory[
        "raw_run_evidence"
    ]
)

qa_records = (
    raw_evidence["qa"]
)

metadata_records = (
    raw_evidence[
        "metadata"
    ]
)

assert len(
    qa_records
) == 24

assert len(
    metadata_records
) == 24

qa_by_label = {
    row["label"]: row
    for row in qa_records
}

metadata_by_label = {
    row["label"]: row
    for row in metadata_records
}

assert (
    set(qa_by_label)
    == set(
        metadata_by_label
    )
)

reliability_rows = []

for label in sorted(
    qa_by_label
):
    qa = qa_by_label[
        label
    ]

    metadata = (
        metadata_by_label[
            label
        ]
    )

    assert (
        qa["status"]
        == "pass"
    )

    assert (
        metadata["status"]
        == "completed"
    )

    assert (
        metadata[
            "failed_documents"
        ]
        == 0
    )

    reliability_rows.append(
        {
            "evidence_label":
                label,
            "processed_documents":
                metadata[
                    "processed_documents"
                ],
            "chunks_written":
                metadata[
                    "chunks_written"
                ],
            "failed_documents":
                metadata[
                    "failed_documents"
                ],
            "elapsed_seconds":
                metadata[
                    "elapsed_seconds"
                ],
            "warning_count":
                qa.get(
                    "warning_count"
                ),
            "qa_hard_failure_events":
                qa.get(
                    "hard_failure_events"
                ),
            "qa_documents_checked":
                qa.get(
                    "documents_checked"
                ),
            "qa_chunks_checked":
                qa.get(
                    "chunks_checked"
                ),
            "qa_status":
                qa[
                    "status"
                ],
            "run_status":
                metadata[
                    "status"
                ],
            "configuration_json":
                json_text(
                    metadata[
                        "configuration"
                    ]
                ),
            "qa_source":
                display_path(
                    Path(
                        qa["path"]
                    )
                ),
            "metadata_source":
                display_path(
                    Path(
                        metadata[
                            "path"
                        ]
                    )
                ),
        }
    )

write_csv(
    RELIABILITY_OUT,
    reliability_rows,
)


# ---------------------------------------------------------------------
# 8. Week 2 scaled engineering table
# ---------------------------------------------------------------------

scaled = load_json(
    SCALED_PATH
)

assert (
    scaled["status"]
    == "completed"
)

assert (
    scaled[
        "failed_documents"
    ]
    == 0
)

assert (
    scaled[
        "processed_documents"
    ]
    == 227628
)

assert (
    scaled[
        "chunks_written"
    ]
    == 1334973
)

assert (
    scaled[
        "qa"
    ]["status"]
    == "pass"
)

resource_values = (
    scaled[
        "resource_measurement"
    ]["values"]
)

max_rss_kb = (
    resource_values.get(
        "max_rss_kb"
    )
)

assert (
    max_rss_kb
    is not None
)

assert (
    max_rss_kb
    > 0
)

scaled_row = {
    "evidence_class":
        scaled[
            "evidence_class"
        ],
    "method":
        scaled["method"],
    "processed_documents":
        scaled[
            "processed_documents"
        ],
    "chunks_written":
        scaled[
            "chunks_written"
        ],
    "failed_documents":
        scaled[
            "failed_documents"
        ],
    "elapsed_seconds":
        scaled[
            "elapsed_seconds"
        ],
    "seconds_per_document":
        scaled[
            "seconds_per_document"
        ],
    "documents_per_second":
        scaled[
            "documents_per_second"
        ],
    "chunks_per_second":
        scaled[
            "chunks_per_second"
        ],
    "chunk_output_bytes":
        scaled[
            "chunk_output_bytes"
        ],
    "qa_documents_checked":
        scaled[
            "qa"
        ].get(
            "documents_checked"
        ),
    "qa_chunks_checked":
        scaled[
            "qa"
        ].get(
            "chunks_checked"
        ),
    "qa_status":
        scaled[
            "qa"
        ]["status"],
    "qa_warning_count":
        scaled[
            "qa"
        ].get(
            "warning_count"
        ),
    "max_rss_kb":
        max_rss_kb,
    "configuration_json":
        json_text(
            scaled[
                "configuration"
            ]
        ),
    "resource_values_json":
        json_text(
            resource_values
        ),
    "memory_note":
        scaled[
            "memory_note"
        ],
    "source_summary":
        display_path(
            SCALED_PATH
        ),
}

write_csv(
    SCALED_OUT,
    [scaled_row],
)


# ---------------------------------------------------------------------
# Canonical summary manifest
# ---------------------------------------------------------------------

table_specs = {
    "baseline_results": {
        "path":
            BASELINE_OUT,
        "rows":
            len(
                baseline_rows
            ),
        "sources": [
            display_path(path)
            for path in (
                BASELINE_PATHS.values()
            )
        ],
    },
    "parameter_sensitivity": {
        "path":
            SENSITIVITY_OUT,
        "rows":
            len(
                sensitivity_rows
            ),
        "sources": [
            display_path(
                SENSITIVITY_PATH
            )
        ],
    },
    "matched_granularity": {
        "path":
            MATCHED_OUT,
        "rows":
            len(
                matched_rows
            ),
        "sources": [
            display_path(
                MATCHED_JSON_PATH
            ),
            display_path(
                MATCHED_CSV_PATH
            ),
        ],
    },
    "robustness_summary": {
        "path":
            ROBUSTNESS_OUT,
        "rows":
            len(
                robustness_rows
            ),
        "sources": [
            display_path(
                ROBUSTNESS_PATH
            )
        ],
    },
    "long_document_runtime": {
        "path":
            LONG_RUNTIME_OUT,
        "rows":
            len(
                runtime_rows
            ),
        "sources": [
            display_path(
                LONG_RUNTIME_PATH
            )
        ],
    },
    "computational_cost": {
        "path":
            COST_OUT,
        "rows":
            len(
                cost_rows
            ),
        "sources": [
            display_path(
                ROBUSTNESS_PATH
            )
        ],
    },
    "reliability_qa": {
        "path":
            RELIABILITY_OUT,
        "rows":
            len(
                reliability_rows
            ),
        "sources": [
            display_path(
                INVENTORY_PATH
            )
        ],
    },
    "scaled_engineering_evidence": {
        "path":
            SCALED_OUT,
        "rows": 1,
        "sources": [
            display_path(
                SCALED_PATH
            )
        ],
    },
}

for spec in (
    table_specs.values()
):
    path = spec["path"]

    assert path.exists()
    assert (
        path.stat().st_size
        > 0
    )

    spec[
        "path"
    ] = display_path(path)

    spec[
        "sha256"
    ] = sha256_file(path)


canonical_summary = {
    "schema_version": 1,
    "purpose": (
        "Canonical machine-readable "
        "tables for the Week 3 "
        "final evaluation report."
    ),
    "generation_policy": {
        "new_chunking_runs":
            False,
        "source_only_transformation":
            True,
        "numeric_rounding":
            False,
        "unsupported_overall_ranking":
            False,
    },
    "table_row_counts": {
        "baseline_results": 3,
        "parameter_sensitivity": 11,
        "matched_granularity": 3,
        "robustness_summary": 30,
        "long_document_runtime": 9,
        "computational_cost": 3,
        "reliability_qa": 24,
        "scaled_engineering_evidence": 1,
    },
    "tables":
        table_specs,
    "semantic_notes": {
        "small_chunk_definition": (
            robustness[
                "small_chunk_definition"
            ]
        ),
        "representative_group_overlap":
            robustness[
                "group_overlap"
            ],
        "matched_run_memory_measurement_status":
            robustness[
                "matched_run_memory_measurement_status"
            ],
        "long_runtime_measurement_class":
            long_runtime[
                "measurement_class"
            ],
        "scaled_memory_measurement": {
            "max_rss_kb":
                max_rss_kb,
            "scope": (
                "Week 2 scaled "
                "TokenChunker run only"
            ),
            "extrapolated":
                False,
        },
        "tokenizer_comparability_note": (
            "TokenChunker and RecursiveChunker "
            "baseline/matched configurations use "
            "the character tokenizer, while "
            "SemanticChunker uses its local "
            "Model2Vec tokenizer. Token-count "
            "statistics are therefore not treated "
            "as directly comparable quality units."
        ),
    },
}

SUMMARY_OUT.write_text(
    json.dumps(
        canonical_summary,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)


# ---------------------------------------------------------------------
# Final console validation
# ---------------------------------------------------------------------

expected_counts = {
    "baseline_results.csv": 3,
    "parameter_sensitivity.csv": 11,
    "matched_granularity.csv": 3,
    "robustness_summary.csv": 30,
    "long_document_runtime.csv": 9,
    "computational_cost.csv": 3,
    "reliability_qa.csv": 24,
    "scaled_engineering_evidence.csv": 1,
}

for filename, expected in (
    expected_counts.items()
):
    path = (
        OUTPUT_DIR
        / filename
    )

    _, rows = read_csv(
        path
    )

    assert len(rows) == expected, (
        filename,
        len(rows),
        expected,
    )

print("=" * 96)
print(
    "ISSUE #18 CANONICAL FINAL SUMMARY TABLES"
)
print("=" * 96)

for filename, expected in (
    expected_counts.items()
):
    print(
        f"{filename:<38} "
        f"{expected:>3} rows"
    )

print()
print(
    "Scaled max_rss_kb:",
    max_rss_kb,
)

print(
    "Scaled QA warning count:",
    scaled["qa"].get(
        "warning_count"
    ),
)

print(
    "Canonical summary:",
    SUMMARY_OUT,
)

print()
print(
    "ISSUE #18 STEP 2 CANONICAL TABLE BUILD: PASS"
)
