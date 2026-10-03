from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(
    "/home/jovyan/chunking_sprint"
)

REPORT_DIR = (
    ROOT
    / "week3/reports"
)

TABLE_DIR = (
    REPORT_DIR
    / "tables"
)

REPORT_PATH = (
    REPORT_DIR
    / "week3_final_evaluation.md"
)

INDEX_PATH = (
    REPORT_DIR
    / "final_comparison_tables.md"
)

TRACE_PATH = (
    REPORT_DIR
    / "report_traceability.json"
)

CANONICAL_PATH = (
    TABLE_DIR
    / "week3_canonical_summary.json"
)

INVENTORY_PATH = (
    REPORT_DIR
    / "issue18_evidence_inventory.json"
)

FREEZE_PATH = (
    REPORT_DIR
    / "issue18_reproducibility_freeze.json"
)

ROBUSTNESS_SOURCE = (
    ROOT
    / "week3/results/issue17/"
      "robustness_summary.json"
)

LONG_RUNTIME_SOURCE = (
    ROOT
    / "week3/results/issue17/"
      "long_runtime/"
      "long_runtime_summary.json"
)

SENSITIVITY_SOURCE = (
    ROOT
    / "week3/results/"
      "parameter_sensitivity/"
      "parameter_sensitivity_summary.json"
)

MATCHED_SOURCE_JSON = (
    ROOT
    / "week3/results/issue16/"
      "matched_comparison/"
      "matched_comparison.json"
)

MATCHED_SOURCE_CSV = (
    ROOT
    / "week3/results/issue16/"
      "matched_comparison/"
      "matched_comparison.csv"
)

SCALED_SOURCE = (
    ROOT
    / "week3/results/issue17/"
      "scaled_engineering_evidence.json"
)

BASELINE_SOURCES = {
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

TABLES = {
    "baseline_results":
        TABLE_DIR
        / "baseline_results.csv",

    "parameter_sensitivity":
        TABLE_DIR
        / "parameter_sensitivity.csv",

    "matched_granularity":
        TABLE_DIR
        / "matched_granularity.csv",

    "robustness_summary":
        TABLE_DIR
        / "robustness_summary.csv",

    "long_document_runtime":
        TABLE_DIR
        / "long_document_runtime.csv",

    "computational_cost":
        TABLE_DIR
        / "computational_cost.csv",

    "reliability_qa":
        TABLE_DIR
        / "reliability_qa.csv",

    "scaled_engineering_evidence":
        TABLE_DIR
        / "scaled_engineering_evidence.csv",
}

AUDIT_JSON = (
    REPORT_DIR
    / "issue18_final_audit.json"
)

AUDIT_MD = (
    REPORT_DIR
    / "issue18_final_audit.md"
)


def load_json(path):
    assert path.exists(), path

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def read_csv(path):
    assert path.exists(), path

    with path.open(
        newline="",
        encoding="utf-8",
    ) as f:
        return list(
            csv.DictReader(f)
        )


def sha256(path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        while True:
            block = f.read(
                1024 * 1024
            )

            if not block:
                break

            h.update(block)

    return h.hexdigest()


def rel(path):
    return str(
        path.relative_to(ROOT)
    )


def scalar(value):
    if value is None:
        return ""

    return str(value)


def json_text(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def assert_scalar(
    actual,
    expected,
    context,
):
    expected_text = scalar(
        expected
    )

    assert actual == expected_text, (
        f"{context}: "
        f"{actual!r} != "
        f"{expected_text!r}"
    )


checks = []


def passed(name):
    checks.append(
        {
            "check": name,
            "status": "pass",
        }
    )


canonical = load_json(
    CANONICAL_PATH
)

inventory = load_json(
    INVENTORY_PATH
)

freeze = load_json(
    FREEZE_PATH
)

trace = load_json(
    TRACE_PATH
)

report = REPORT_PATH.read_text(
    encoding="utf-8"
)


# ================================================================
# 1. Canonical table manifest hashes and row counts
# ================================================================

expected_counts = {
    "baseline_results": 3,
    "parameter_sensitivity": 11,
    "matched_granularity": 3,
    "robustness_summary": 30,
    "long_document_runtime": 9,
    "computational_cost": 3,
    "reliability_qa": 24,
    "scaled_engineering_evidence": 1,
}

assert (
    canonical[
        "table_row_counts"
    ]
    == expected_counts
)

for name, expected_count in (
    expected_counts.items()
):
    spec = (
        canonical[
            "tables"
        ][name]
    )

    path = (
        ROOT
        / spec["path"]
    )

    rows = read_csv(path)

    assert (
        len(rows)
        == expected_count
    )

    assert (
        sha256(path)
        == spec["sha256"]
    )

passed(
    "canonical_table_hashes_and_row_counts"
)


# ================================================================
# 2. Baseline source -> canonical exact consistency
# ================================================================

baseline_rows = read_csv(
    TABLES[
        "baseline_results"
    ]
)

baseline_by_method = {
    row["method"]: row
    for row in baseline_rows
}

for method, source_path in (
    BASELINE_SOURCES.items()
):
    source = load_json(
        source_path
    )

    out = baseline_by_method[
        method
    ]

    run = source["run"]

    metrics = source[
        "metrics"
    ]

    char = metrics[
        "char_length"
    ]

    cpd = metrics[
        "chunks_per_document"
    ]

    boundary = metrics[
        "boundaries"
    ][
        "percentages_internal_only"
    ]

    expected = {
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
            cpd["mean"],
        "median_chunks_per_document":
            cpd["median"],
        "mean_chunk_char_length":
            char["mean"],
        "median_chunk_char_length":
            char["median"],
        "p90_chunk_char_length":
            char["p90"],
        "p95_chunk_char_length":
            char["p95"],
        "p99_chunk_char_length":
            char["p99"],
        "paragraph_boundary_internal":
            boundary[
                "paragraph_boundary"
            ],
        "newline_boundary_internal":
            boundary[
                "newline_boundary"
            ],
        "sentence_boundary_internal":
            boundary[
                "sentence_boundary"
            ],
        "whitespace_boundary_internal":
            boundary[
                "whitespace_boundary"
            ],
        "other_boundary_internal":
            boundary[
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
            rel(
                source_path
            ),
    }

    for key, value in (
        expected.items()
    ):
        assert_scalar(
            out[key],
            value,
            f"baseline.{method}.{key}",
        )

passed(
    "baseline_source_to_canonical"
)


# ================================================================
# 3. Parameter-sensitivity source -> canonical
# ================================================================

sensitivity_source = load_json(
    SENSITIVITY_SOURCE
)

sensitivity_rows = read_csv(
    TABLES[
        "parameter_sensitivity"
    ]
)

assert (
    sensitivity_source[
        "configuration_count"
    ]
    == 11
)

source_records = {
    row["run_id"]: row
    for row in (
        sensitivity_source[
            "records"
        ]
    )
}

output_records = {
    row["run_id"]: row
    for row in (
        sensitivity_rows
    )
}

assert (
    set(source_records)
    == set(output_records)
)

for run_id, source in (
    source_records.items()
):
    out = output_records[
        run_id
    ]

    for key, value in (
        source.items()
    ):
        assert_scalar(
            out[key],
            value,
            (
                "sensitivity."
                f"{run_id}.{key}"
            ),
        )

    assert (
        out[
            "source_summary"
        ]
        == rel(
            SENSITIVITY_SOURCE
        )
    )

passed(
    "parameter_sensitivity_source_to_canonical"
)


# ================================================================
# 4. Matched comparison source -> canonical
# ================================================================

matched_json = load_json(
    MATCHED_SOURCE_JSON
)

matched_source_rows = read_csv(
    MATCHED_SOURCE_CSV
)

matched_rows = read_csv(
    TABLES[
        "matched_granularity"
    ]
)

source_by_method = {
    row["method"]: row
    for row in matched_source_rows
}

out_by_method = {
    row["method"]: row
    for row in matched_rows
}

config_by_method = {
    row["method"]:
        row["configuration"]
    for row in (
        matched_json[
            "methods"
        ]
    )
}

assert (
    set(source_by_method)
    == set(out_by_method)
    == {
        "token",
        "recursive",
        "semantic",
    }
)

for method, source in (
    source_by_method.items()
):
    out = out_by_method[
        method
    ]

    for key, value in (
        source.items()
    ):
        assert (
            out[key]
            == value
        ), (
            method,
            key,
            out[key],
            value,
        )

    assert (
        out[
            "configuration_json"
        ]
        == json_text(
            config_by_method[
                method
            ]
        )
    )

    assert_scalar(
        out[
            "matching_tolerance"
        ],
        matched_json[
            "matching"
        ]["tolerance"],
        (
            "matched."
            f"{method}."
            "matching_tolerance"
        ),
    )

    assert_scalar(
        out[
            "worst_relative_spread"
        ],
        matched_json[
            "matching"
        ][
            "worst_relative_spread"
        ],
        (
            "matched."
            f"{method}."
            "worst_relative_spread"
        ),
    )

passed(
    "matched_source_to_canonical"
)


# ================================================================
# 5. Robustness source -> canonical
# ================================================================

robustness_source = load_json(
    ROBUSTNESS_SOURCE
)

robustness_rows = read_csv(
    TABLES[
        "robustness_summary"
    ]
)

source_robustness = {
    (
        row["group"],
        row["method"],
    ): row
    for row in (
        robustness_source[
            "robustness_by_group"
        ]
    )
}

out_robustness = {
    (
        row["group"],
        row["method"],
    ): row
    for row in (
        robustness_rows
    )
}

assert (
    set(source_robustness)
    == set(out_robustness)
)

assert (
    len(
        source_robustness
    )
    == 30
)

for key, source in (
    source_robustness.items()
):
    out = out_robustness[
        key
    ]

    for field, value in (
        source.items()
    ):
        assert_scalar(
            out[field],
            value,
            (
                "robustness."
                f"{key}.{field}"
            ),
        )

    assert_scalar(
        out[
            "small_chunk_threshold"
        ],
        robustness_source[
            "small_chunk_definition"
        ]["threshold"],
        (
            "robustness."
            f"{key}."
            "small_chunk_threshold"
        ),
    )

    assert_scalar(
        out[
            "group_overlap"
        ],
        robustness_source[
            "group_overlap"
        ],
        (
            "robustness."
            f"{key}."
            "group_overlap"
        ),
    )

passed(
    "robustness_source_to_canonical"
)


# ================================================================
# 6. Long runtime source -> canonical
# ================================================================

runtime_source = load_json(
    LONG_RUNTIME_SOURCE
)

runtime_rows = read_csv(
    TABLES[
        "long_document_runtime"
    ]
)

source_runtime = {
    row["run_id"]: row
    for row in (
        runtime_source[
            "records"
        ]
    )
}

out_runtime = {
    row["run_id"]: row
    for row in runtime_rows
}

assert (
    set(source_runtime)
    == set(out_runtime)
)

assert (
    len(source_runtime)
    == 9
)

for run_id, source in (
    source_runtime.items()
):
    out = out_runtime[
        run_id
    ]

    for field, value in (
        source.items()
    ):
        if field == "warnings":
            continue

        assert_scalar(
            out[field],
            value,
            (
                "long_runtime."
                f"{run_id}.{field}"
            ),
        )

    assert (
        out[
            "warnings_json"
        ]
        == json_text(
            source["warnings"]
        )
    )

    assert (
        out[
            "measurement_class"
        ]
        == runtime_source[
            "measurement_class"
        ]
    )

passed(
    "long_runtime_source_to_canonical"
)


# ================================================================
# 7. Cost source -> canonical
# ================================================================

cost_rows = read_csv(
    TABLES[
        "computational_cost"
    ]
)

source_cost = {
    row["method"]: row
    for row in (
        robustness_source[
            "computational_cost"
        ]
    )
}

out_cost = {
    row["method"]: row
    for row in cost_rows
}

assert (
    set(source_cost)
    == set(out_cost)
)

for method, source in (
    source_cost.items()
):
    out = out_cost[
        method
    ]

    for field, value in (
        source.items()
    ):
        assert_scalar(
            out[field],
            value,
            (
                "cost."
                f"{method}.{field}"
            ),
        )

passed(
    "computational_cost_source_to_canonical"
)


# ================================================================
# 8. Reliability inventory -> canonical
# ================================================================

reliability_rows = read_csv(
    TABLES[
        "reliability_qa"
    ]
)

raw = inventory[
    "raw_run_evidence"
]

qa_by_label = {
    row["label"]: row
    for row in raw["qa"]
}

meta_by_label = {
    row["label"]: row
    for row in raw[
        "metadata"
    ]
}

out_reliability = {
    row[
        "evidence_label"
    ]: row
    for row in (
        reliability_rows
    )
}

assert (
    set(qa_by_label)
    == set(meta_by_label)
    == set(out_reliability)
)

assert (
    len(out_reliability)
    == 24
)

for label, out in (
    out_reliability.items()
):
    qa = qa_by_label[
        label
    ]

    meta = meta_by_label[
        label
    ]

    expected = {
        "evidence_label":
            label,
        "processed_documents":
            meta[
                "processed_documents"
            ],
        "chunks_written":
            meta[
                "chunks_written"
            ],
        "failed_documents":
            meta[
                "failed_documents"
            ],
        "elapsed_seconds":
            meta[
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
            qa["status"],
        "run_status":
            meta["status"],
        "configuration_json":
            json_text(
                meta[
                    "configuration"
                ]
            ),
        "qa_source":
            rel(
                Path(
                    qa["path"]
                )
            ),
        "metadata_source":
            rel(
                Path(
                    meta[
                        "path"
                    ]
                )
            ),
    }

    for field, value in (
        expected.items()
    ):
        assert_scalar(
            out[field],
            value,
            (
                "reliability."
                f"{label}.{field}"
            ),
        )

passed(
    "reliability_inventory_to_canonical"
)


# ================================================================
# 9. Scaled evidence source -> canonical
# ================================================================

scaled_source = load_json(
    SCALED_SOURCE
)

scaled_rows = read_csv(
    TABLES[
        "scaled_engineering_evidence"
    ]
)

assert len(
    scaled_rows
) == 1

out = scaled_rows[0]

resource_values = (
    scaled_source[
        "resource_measurement"
    ]["values"]
)

expected_scaled = {
    "evidence_class":
        scaled_source[
            "evidence_class"
        ],
    "method":
        scaled_source[
            "method"
        ],
    "processed_documents":
        scaled_source[
            "processed_documents"
        ],
    "chunks_written":
        scaled_source[
            "chunks_written"
        ],
    "failed_documents":
        scaled_source[
            "failed_documents"
        ],
    "elapsed_seconds":
        scaled_source[
            "elapsed_seconds"
        ],
    "seconds_per_document":
        scaled_source[
            "seconds_per_document"
        ],
    "documents_per_second":
        scaled_source[
            "documents_per_second"
        ],
    "chunks_per_second":
        scaled_source[
            "chunks_per_second"
        ],
    "chunk_output_bytes":
        scaled_source[
            "chunk_output_bytes"
        ],
    "qa_documents_checked":
        scaled_source[
            "qa"
        ].get(
            "documents_checked"
        ),
    "qa_chunks_checked":
        scaled_source[
            "qa"
        ].get(
            "chunks_checked"
        ),
    "qa_status":
        scaled_source[
            "qa"
        ]["status"],
    "qa_warning_count":
        scaled_source[
            "qa"
        ].get(
            "warning_count"
        ),
    "max_rss_kb":
        resource_values[
            "max_rss_kb"
        ],
    "configuration_json":
        json_text(
            scaled_source[
                "configuration"
            ]
        ),
    "resource_values_json":
        json_text(
            resource_values
        ),
    "memory_note":
        scaled_source[
            "memory_note"
        ],
    "source_summary":
        rel(
            SCALED_SOURCE
        ),
}

for field, value in (
    expected_scaled.items()
):
    assert_scalar(
        out[field],
        value,
        (
            "scaled."
            f"{field}"
        ),
    )

assert (
    out[
        "qa_warning_count"
    ]
    == ""
)

passed(
    "scaled_source_to_canonical"
)


# ================================================================
# 10. Frozen representative input integrity
# ================================================================

rep = freeze[
    "representative_input"
]

rep_path = Path(
    rep["path"]
)

assert (
    sha256(rep_path)
    == rep[
        "expected_sha256"
    ]
    == rep[
        "current_sha256"
    ]
)

assert (
    rep["status"]
    == "match"
)

assert (
    freeze[
        "full_dataset_freeze"
    ][
        "manifest_entries"
    ]
    == 57
)

passed(
    "frozen_input_integrity"
)


# ================================================================
# 11. Traceability manifest current hashes
# ================================================================

assert (
    trace[
        "report_sha256"
    ]
    == sha256(
        REPORT_PATH
    )
)

assert (
    trace[
        "comparison_table_index_sha256"
    ]
    == sha256(
        INDEX_PATH
    )
)

assert (
    trace[
        "canonical_summary_sha256"
    ]
    == sha256(
        CANONICAL_PATH
    )
)

assert len(
    trace[
        "sections"
    ]
) == 9

for section, records in (
    trace[
        "sections"
    ].items()
):
    assert records, section

    for record in records:
        path = (
            ROOT
            / record["path"]
        )

        assert path.exists(), path

        assert (
            path.stat().st_size
            == record["bytes"]
        ), (
            section,
            record["path"],
            "byte count changed",
        )

        assert (
            sha256(path)
            == record[
                "sha256"
            ]
        ), (
            section,
            record["path"],
            "SHA256 changed",
        )

passed(
    "report_traceability_hashes"
)


# ================================================================
# 12. QA / failures / warnings semantics
# ================================================================

assert all(
    row[
        "qa_status"
    ]
    == "pass"
    for row in (
        reliability_rows
    )
)

assert all(
    row[
        "run_status"
    ]
    == "completed"
    for row in (
        reliability_rows
    )
)

assert all(
    row[
        "failed_documents"
    ]
    == "0"
    for row in (
        reliability_rows
    )
)

known_warning_rows = [
    row
    for row in reliability_rows
    if (
        row[
            "warning_count"
        ]
        != ""
    )
]

unknown_warning_rows = [
    row
    for row in reliability_rows
    if (
        row[
            "warning_count"
        ]
        == ""
    )
]

known_warning_total = sum(
    int(
        float(
            row[
                "warning_count"
            ]
        )
    )
    for row in (
        known_warning_rows
    )
)

assert (
    known_warning_total
    == 6
)

assert (
    len(
        unknown_warning_rows
    )
    == 1
)

passed(
    "qa_failures_and_warning_semantics"
)


# ================================================================
# 13. Final report required structure / limitations
# ================================================================

required_sections = [
    "## 1. Experimental Setup",
    "## 2. Baseline Results",
    "## 3. Parameter Sensitivity",
    "## 4. Matched-Granularity Comparison",
    "## 5. Robustness",
    "## 6. Computational Cost",
    "## 7. Reliability and QA",
    "## 8. Limitations",
    "## 9. Conclusions",
    "## Reproducibility and Evidence Paths",
]

for heading in (
    required_sections
):
    assert heading in report

required_limitations = [
    "Tokenizer semantics differ",
    "The representative set is small",
    "Matched granularity is approximate",
    "Retrieval relevance labels are absent",
    "SemanticChunker numerical warnings",
    "Full-scale cross-method testing is limited",
    "Runtime evidence is descriptive",
    "Memory evidence is incomplete",
    "The Git repository currently has an unborn HEAD",
]

for phrase in (
    required_limitations
):
    assert phrase in report, phrase

assert (
    "does not support an overall quality winner"
    in report
)

assert (
    "method-specific trade-offs rather than an overall winner"
    in report
)

assert (
    "Stronger chunk-quality conclusions would require"
    in report
)

passed(
    "report_structure_and_limitations"
)


# ================================================================
# 14. Generation-policy invariants
# ================================================================

policy = canonical[
    "generation_policy"
]

assert (
    policy[
        "new_chunking_runs"
    ]
    is False
)

assert (
    policy[
        "source_only_transformation"
    ]
    is True
)

assert (
    policy[
        "numeric_rounding"
    ]
    is False
)

assert (
    policy[
        "unsupported_overall_ranking"
    ]
    is False
)

report_policy = trace[
    "report_generation"
]

assert (
    report_policy[
        "new_chunking_runs"
    ]
    is False
)

assert (
    report_policy[
        "canonical_tables_only_for_experiment_numbers"
    ]
    is True
)

assert (
    report_policy[
        "canonical_numeric_rounding"
    ]
    is False
)

assert (
    report_policy[
        "unsupported_overall_winner"
    ]
    is False
)

passed(
    "generation_policy_invariants"
)


# ================================================================
# Final audit outputs
# ================================================================

audit = {
    "schema_version": 1,
    "status": "pass",
    "check_count": len(checks),
    "checks": checks,
    "canonical_row_counts":
        expected_counts,
    "known_warning_events":
        known_warning_total,
    "qa_records_with_warning_count_unrecorded":
        len(
            unknown_warning_rows
        ),
    "representative_input_sha256":
        rep[
            "current_sha256"
        ],
    "full_dataset_manifest_entries":
        freeze[
            "full_dataset_freeze"
        ][
            "manifest_entries"
        ],
    "report_sha256":
        sha256(
            REPORT_PATH
        ),
    "comparison_table_index_sha256":
        sha256(
            INDEX_PATH
        ),
    "canonical_summary_sha256":
        sha256(
            CANONICAL_PATH
        ),
    "conclusion": (
        "Stored source evidence, canonical "
        "tables, report traceability, QA, "
        "and final report are internally "
        "consistent."
    ),
}

AUDIT_JSON.write_text(
    json.dumps(
        audit,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)

md = [
    "# Issue 18 Final Audit",
    "",
    "**Status:** PASS",
    "",
    (
        f"Checks passed: "
        f"{len(checks)}"
    ),
    "",
]

for item in checks:
    md.append(
        "- PASS — "
        + item["check"]
    )

md.extend(
    [
        "",
        (
            "Known warning events: "
            f"{known_warning_total}"
        ),
        "",
        (
            "QA records with warning count "
            "unrecorded: "
            f"{len(unknown_warning_rows)}"
        ),
        "",
        (
            "Full-dataset manifest entries: "
            f"{freeze['full_dataset_freeze']['manifest_entries']}"
        ),
        "",
        (
            "Final report SHA256: `"
            + audit[
                "report_sha256"
            ]
            + "`"
        ),
        "",
        (
            "**Final result:** all stored "
            "source evidence, canonical "
            "tables, QA evidence, and report "
            "artifacts are internally "
            "consistent."
        ),
        "",
    ]
)

AUDIT_MD.write_text(
    "\n".join(md),
    encoding="utf-8",
)

print("=" * 100)
print(
    "ISSUE #18 FINAL CROSS-ARTIFACT AUDIT"
)
print("=" * 100)

for item in checks:
    print(
        "PASS |",
        item["check"],
    )

print()
print(
    "Checks passed:",
    len(checks),
)

print(
    "Known warning events:",
    known_warning_total,
)

print(
    "QA records with warning count unrecorded:",
    len(
        unknown_warning_rows
    ),
)

print(
    "Final report SHA256:",
    audit[
        "report_sha256"
    ],
)

print(
    "Audit JSON:",
    AUDIT_JSON,
)

print(
    "Audit Markdown:",
    AUDIT_MD,
)

print()
print(
    "ISSUE #18 FINAL CROSS-ARTIFACT AUDIT: PASS"
)
