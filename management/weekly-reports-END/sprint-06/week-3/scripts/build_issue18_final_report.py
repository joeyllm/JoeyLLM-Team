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

TABLE_INDEX_PATH = (
    REPORT_DIR
    / "final_comparison_tables.md"
)

TRACE_PATH = (
    REPORT_DIR
    / "report_traceability.json"
)

CANONICAL_SUMMARY_PATH = (
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

ENV_PATH = (
    ROOT
    / "week3/configs/"
      "environment_snapshot.json"
)

BASELINE_CONFIG_PATH = (
    ROOT
    / "week3/configs/"
      "baseline_configs.json"
)

CONSTANTS_PATH = (
    ROOT
    / "week3/configs/"
      "experimental_constants.json"
)

MATCHED_SETTINGS_PATH = (
    ROOT
    / "week3/configs/"
      "issue16_matched_settings.json"
)

PLAN_PATH = (
    ROOT
    / "week3/"
      "week3_experiment_plan.md"
)

METRIC_SPEC_PATH = (
    ROOT
    / "week3/configs/"
      "evaluation_metric_spec.md"
)


TABLE_PATHS = {
    "baseline":
        TABLE_DIR
        / "baseline_results.csv",

    "sensitivity":
        TABLE_DIR
        / "parameter_sensitivity.csv",

    "matched":
        TABLE_DIR
        / "matched_granularity.csv",

    "robustness":
        TABLE_DIR
        / "robustness_summary.csv",

    "long_runtime":
        TABLE_DIR
        / "long_document_runtime.csv",

    "cost":
        TABLE_DIR
        / "computational_cost.csv",

    "reliability":
        TABLE_DIR
        / "reliability_qa.csv",

    "scaled":
        TABLE_DIR
        / "scaled_engineering_evidence.csv",
}


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
) -> list[dict]:
    assert path.exists(), path

    with path.open(
        newline="",
        encoding="utf-8",
    ) as f:
        return list(
            csv.DictReader(f)
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


def rel(
    path: Path,
) -> str:
    return str(
        path.relative_to(ROOT)
    )


def fnum(
    value,
    digits=3,
):
    if value is None:
        return "not recorded"

    if isinstance(
        value,
        str,
    ):
        if value == "":
            return "not recorded"

    return f"{float(value):.{digits}f}"


def fint(
    value,
):
    if value is None:
        return "not recorded"

    if isinstance(
        value,
        str,
    ):
        if value == "":
            return "not recorded"

    return str(
        int(float(value))
    )


def pct_fraction(
    value,
    digits=2,
):
    return (
        f"{float(value) * 100:.{digits}f}%"
    )


def pct_value(
    value,
    digits=2,
):
    return (
        f"{float(value):.{digits}f}%"
    )


def markdown_table(
    headers: list[str],
    rows: list[list[str]],
) -> list[str]:
    output = [
        "| "
        + " | ".join(headers)
        + " |",
        "|"
        + "|".join(
            "---"
            for _ in headers
        )
        + "|",
    ]

    for row in rows:
        assert len(row) == len(headers)

        output.append(
            "| "
            + " | ".join(
                str(value)
                for value in row
            )
            + " |"
        )

    return output


def find_one(
    rows,
    **conditions,
):
    matches = [
        row
        for row in rows
        if all(
            row[key]
            == str(value)
            for key, value
            in conditions.items()
        )
    ]

    if len(matches) != 1:
        raise RuntimeError(
            "Expected exactly one row for "
            f"{conditions}; got "
            f"{len(matches)}"
        )

    return matches[0]


def append_source(
    lines,
    *paths,
):
    lines.append("")

    lines.append(
        "**Evidence:** "
        + ", ".join(
            f"`{rel(path)}`"
            for path in paths
        )
    )

    lines.append("")


# ------------------------------------------------------------------
# Load frozen source evidence
# ------------------------------------------------------------------

environment = load_json(
    ENV_PATH
)

baseline_configs = load_json(
    BASELINE_CONFIG_PATH
)

constants = load_json(
    CONSTANTS_PATH
)

matched_settings = load_json(
    MATCHED_SETTINGS_PATH
)

canonical = load_json(
    CANONICAL_SUMMARY_PATH
)

inventory = load_json(
    INVENTORY_PATH
)

freeze = load_json(
    FREEZE_PATH
)

baseline = read_csv(
    TABLE_PATHS["baseline"]
)

sensitivity = read_csv(
    TABLE_PATHS["sensitivity"]
)

matched = read_csv(
    TABLE_PATHS["matched"]
)

robustness = read_csv(
    TABLE_PATHS["robustness"]
)

long_runtime = read_csv(
    TABLE_PATHS["long_runtime"]
)

cost = read_csv(
    TABLE_PATHS["cost"]
)

reliability = read_csv(
    TABLE_PATHS["reliability"]
)

scaled = read_csv(
    TABLE_PATHS["scaled"]
)


# ------------------------------------------------------------------
# Hard source validation before writing report
# ------------------------------------------------------------------

assert len(baseline) == 3
assert len(sensitivity) == 11
assert len(matched) == 3
assert len(robustness) == 30
assert len(long_runtime) == 9
assert len(cost) == 3
assert len(reliability) == 24
assert len(scaled) == 1

assert {
    row["method"]
    for row in baseline
} == {
    "token",
    "recursive",
    "semantic",
}

assert {
    row["method"]
    for row in matched
} == {
    "token",
    "recursive",
    "semantic",
}

assert len({
    row["run_id"]
    for row in sensitivity
}) == 11

assert len({
    row["group"]
    for row in robustness
}) == 10

assert all(
    row["qa_status"] == "pass"
    for row in baseline
)

assert all(
    row["qa_status"] == "pass"
    for row in sensitivity
)

assert all(
    row["qa_status"] == "pass"
    for row in matched
)

assert all(
    row["qa_status"] == "pass"
    for row in long_runtime
)

assert all(
    row["qa_status"] == "pass"
    for row in cost
)

assert all(
    row["qa_status"] == "pass"
    for row in reliability
)

assert all(
    row["failed_documents"] == "0"
    for row in reliability
)

assert (
    freeze[
        "representative_input"
    ]["status"]
    == "match"
)

assert (
    freeze[
        "full_dataset_freeze"
    ]["manifest_entries"]
    == 57
)

assert (
    canonical[
        "generation_policy"
    ][
        "new_chunking_runs"
    ]
    is False
)


# ------------------------------------------------------------------
# Convenient lookups
# ------------------------------------------------------------------

baseline_by_method = {
    row["method"]: row
    for row in baseline
}

matched_by_method = {
    row["method"]: row
    for row in matched
}

cost_by_method = {
    row["method"]: row
    for row in cost
}

scaled_row = scaled[0]


# ------------------------------------------------------------------
# Derived parameter-sensitivity observations
# ------------------------------------------------------------------

token_1024 = find_one(
    sensitivity,
    run_id="token_cs1024",
)

token_2048 = find_one(
    sensitivity,
    run_id="token_cs2048",
)

token_4096 = find_one(
    sensitivity,
    run_id="token_cs4096",
)

recursive_1024 = find_one(
    sensitivity,
    run_id="recursive_cs1024",
)

recursive_2048 = find_one(
    sensitivity,
    run_id="recursive_cs2048",
)

recursive_4096 = find_one(
    sensitivity,
    run_id="recursive_cs4096",
)

semantic_1024 = find_one(
    sensitivity,
    run_id="semantic_cs1024",
)

semantic_2048 = find_one(
    sensitivity,
    run_id="semantic_cs2048",
)

semantic_4096 = find_one(
    sensitivity,
    run_id="semantic_cs4096",
)

semantic_070 = find_one(
    sensitivity,
    run_id="semantic_th070",
)

semantic_090 = find_one(
    sensitivity,
    run_id="semantic_th090",
)


# ------------------------------------------------------------------
# Reliability observations
# ------------------------------------------------------------------

known_warning_rows = []

unknown_warning_rows = []

for row in reliability:
    raw = row[
        "warning_count"
    ]

    if raw == "":
        unknown_warning_rows.append(
            row
        )

    elif int(
        float(raw)
    ) > 0:
        known_warning_rows.append(
            row
        )

known_warning_total = sum(
    int(
        float(
            row[
                "warning_count"
            ]
        )
    )
    for row
    in known_warning_rows
)


# ------------------------------------------------------------------
# Final report
# ------------------------------------------------------------------

lines = [
    "# Week 3 Final Chunking Evaluation",
    "",
    "## Executive Summary",
    "",
    (
        "Week 3 evaluated TokenChunker, "
        "RecursiveChunker, and SemanticChunker "
        "using a frozen 32-document representative "
        "sample from the frozen post-deduplication "
        "dataset."
    ),
    "",
    (
        "The evaluation covered validated baseline "
        "behaviour, an 11-configuration parameter-"
        "sensitivity matrix, an approximately "
        "matched-granularity comparison, robustness "
        "across representative document groups, "
        "controlled long-document runtime evidence, "
        "computational cost, and the existing Week 2 "
        "scaled TokenChunker run."
    ),
    "",
    (
        "The evidence shows materially different "
        "chunking behaviour across methods, but does "
        "not support an overall quality winner. "
        "Retrieval-relevance labels and downstream "
        "task evaluation are not part of the current "
        "evidence set."
    ),
    "",
    (
        "All canonical report tables are generated "
        "from stored experiment outputs. Displayed "
        "values may be rounded for readability; "
        "the canonical CSV files retain the source "
        "numeric values without report-level rounding."
    ),
    "",
    "## 1. Experimental Setup",
    "",
    "### Frozen Dataset and Representative Input",
    "",
    (
        f"The frozen dataset pattern is "
        f"`{constants['frozen_dataset_pattern']}`."
    ),
    "",
    (
        "The preserved full-dataset SHA256 manifest "
        f"contains "
        f"{freeze['full_dataset_freeze']['manifest_entries']} "
        "entries."
    ),
    "",
    (
        "Week 3 uses the frozen representative input "
        f"`{constants['representative_input']}` containing "
        f"{constants['representative_document_count']} "
        "documents."
    ),
    "",
    (
        "The representative-input SHA256 was checked "
        "during Issue #18 reproducibility freeze and "
        "matches the stored Week 3 hash:"
    ),
    "",
    (
        "`"
        + freeze[
            "representative_input"
        ][
            "current_sha256"
        ]
        + "`"
    ),
    "",
    (
        "Issue #18 does not rehash the complete "
        "approximately 25 GiB dataset; it preserves "
        "the existing 57-file dataset manifest as "
        "the full-dataset integrity evidence."
    ),
    "",
    "### Software Environment",
    "",
]

lines.extend(
    markdown_table(
        [
            "Component",
            "Version",
        ],
        [
            [
                "Python",
                environment["python"],
            ],
            [
                "Chonkie",
                environment["chonkie"],
            ],
            [
                "model2vec",
                environment["model2vec"],
            ],
            [
                "PyArrow",
                environment["pyarrow"],
            ],
        ],
    )
)

lines.extend(
    [
        "",
        "### Baseline Configurations",
        "",
    ]
)

baseline_config_rows = []

for method in [
    "token",
    "recursive",
    "semantic",
]:
    cfg = baseline_configs[
        method
    ]

    baseline_config_rows.append(
        [
            method,
            "`"
            + json.dumps(
                cfg,
                sort_keys=True,
                separators=(",", ":"),
            )
            + "`",
        ]
    )

lines.extend(
    markdown_table(
        [
            "Method",
            "Frozen baseline configuration",
        ],
        baseline_config_rows,
    )
)

lines.extend(
    [
        "",
        "### Evaluation Dimensions",
        "",
        (
            "The frozen evaluation specification "
            "covers output validity, chunks per "
            "document, chunk character length, chunk "
            "token count, boundary classification, "
            "representative sample groups, runtime, "
            "warnings, failures, and QA."
        ),
        "",
        (
            "Internal boundaries are classified as "
            "`paragraph_boundary`, `newline_boundary`, "
            "`sentence_boundary`, `whitespace_boundary`, "
            "or `other_boundary`; `document_end` is "
            "tracked separately."
        ),
        "",
        (
            "Configured chunk sizes are not assumed "
            "to be equivalent across methods. "
            "Raw chunk count is not treated as a "
            "quality metric."
        ),
    ]
)

append_source(
    lines,
    ENV_PATH,
    BASELINE_CONFIG_PATH,
    CONSTANTS_PATH,
    PLAN_PATH,
    METRIC_SPEC_PATH,
    FREEZE_PATH,
)


# ------------------------------------------------------------------
# Baseline section
# ------------------------------------------------------------------

lines.extend(
    [
        "## 2. Baseline Results",
        "",
        "### Results",
        "",
    ]
)

baseline_table_rows = []

for method in [
    "token",
    "recursive",
    "semantic",
]:
    row = baseline_by_method[
        method
    ]

    baseline_table_rows.append(
        [
            method,
            fint(
                row[
                    "total_chunks"
                ]
            ),
            fnum(
                row[
                    "mean_chunks_per_document"
                ]
            ),
            fnum(
                row[
                    "median_chunk_char_length"
                ]
            ),
            fnum(
                row[
                    "mean_chunk_char_length"
                ]
            ),
            pct_fraction(
                row[
                    "newline_boundary_internal"
                ]
            ),
            pct_fraction(
                row[
                    "sentence_boundary_internal"
                ]
            ),
            pct_fraction(
                row[
                    "whitespace_boundary_internal"
                ]
            ),
            pct_fraction(
                row[
                    "other_boundary_internal"
                ]
            ),
            fnum(
                row[
                    "elapsed_seconds"
                ],
                6,
            ),
            fint(
                row[
                    "warning_count"
                ]
            ),
            row[
                "qa_status"
            ],
        ]
    )

lines.extend(
    markdown_table(
        [
            "Method",
            "Chunks",
            "Mean chunks/doc",
            "Median chars",
            "Mean chars",
            "Newline",
            "Sentence",
            "Whitespace",
            "Other",
            "Seconds",
            "Warnings",
            "QA",
        ],
        baseline_table_rows,
    )
)

lines.extend(
    [
        "",
        "### Interpretation",
        "",
        (
            "TokenChunker at the 2048-character baseline "
            "produced fixed-size-like chunks: its median "
            "chunk character length was "
            f"{fnum(token_2048['median_chunk_char_length'])}, "
            "and most internal boundaries were classified "
            "as `other_boundary` or `whitespace_boundary`."
        ),
        "",
        (
            "RecursiveChunker at the same configured "
            "chunk size produced a different boundary "
            "profile. Its internal boundaries were "
            "predominantly newline boundaries, showing "
            "that equal configured chunk size does not "
            "imply equivalent output structure."
        ),
        "",
        (
            "SemanticChunker produced substantially more "
            "and shorter chunks on this representative "
            "sample. Its internal boundaries were "
            "concentrated on sentence and newline "
            "boundaries. The baseline SemanticChunker "
            "run recorded one numerical warning while "
            "still completing with zero processing "
            "failures and QA status `pass`."
        ),
        "",
        (
            "Because TokenChunker and RecursiveChunker "
            "use the character tokenizer while "
            "SemanticChunker uses its Model2Vec tokenizer, "
            "chunk token-count statistics are not used as "
            "direct cross-method quality comparisons."
        ),
    ]
)

append_source(
    lines,
    TABLE_PATHS["baseline"],
)


# ------------------------------------------------------------------
# Sensitivity section
# ------------------------------------------------------------------

lines.extend(
    [
        "## 3. Parameter Sensitivity",
        "",
        "### Results",
        "",
    ]
)

sensitivity_table_rows = []

for row in sensitivity:
    sensitivity_table_rows.append(
        [
            row["run_id"],
            row["method"],
            row[
                "experiment_axis"
            ],
            (
                row["chunk_size"]
                if row[
                    "chunk_size"
                ] != ""
                else "—"
            ),
            (
                row["threshold"]
                if row[
                    "threshold"
                ] != ""
                else "—"
            ),
            fint(
                row[
                    "total_chunks"
                ]
            ),
            fnum(
                row[
                    "mean_chunks_per_document"
                ]
            ),
            fnum(
                row[
                    "median_chunk_char_length"
                ]
            ),
            fnum(
                row[
                    "mean_chunk_char_length"
                ]
            ),
            fnum(
                row[
                    "elapsed_seconds"
                ],
                6,
            ),
            fint(
                row[
                    "warning_count"
                ]
            ),
            row[
                "qa_status"
            ],
        ]
    )

lines.extend(
    markdown_table(
        [
            "Run",
            "Method",
            "Axis",
            "Chunk size",
            "Threshold",
            "Chunks",
            "Mean chunks/doc",
            "Median chars",
            "Mean chars",
            "Seconds",
            "Warnings",
            "QA",
        ],
        sensitivity_table_rows,
    )
)

lines.extend(
    [
        "",
        "### Interpretation",
        "",
        (
            "For TokenChunker, increasing `chunk_size` "
            "from 1024 to 2048 to 4096 reduced total "
            "chunks from "
            f"{fint(token_1024['total_chunks'])} to "
            f"{fint(token_2048['total_chunks'])} to "
            f"{fint(token_4096['total_chunks'])}, while "
            "mean chunk character length increased from "
            f"{fnum(token_1024['mean_chunk_char_length'])} "
            "to "
            f"{fnum(token_2048['mean_chunk_char_length'])} "
            "to "
            f"{fnum(token_4096['mean_chunk_char_length'])}."
        ),
        "",
        (
            "RecursiveChunker shows the same directional "
            "granularity response to chunk size: total "
            "chunks changed from "
            f"{fint(recursive_1024['total_chunks'])} "
            "at 1024 to "
            f"{fint(recursive_2048['total_chunks'])} "
            "at 2048 and "
            f"{fint(recursive_4096['total_chunks'])} "
            "at 4096."
        ),
        "",
        (
            "SemanticChunker behaved differently on the "
            "frozen sample. At threshold 0.8, changing "
            "configured chunk size from 1024 to 2048 to "
            "4096 produced "
            f"{fint(semantic_1024['total_chunks'])}, "
            f"{fint(semantic_2048['total_chunks'])}, and "
            f"{fint(semantic_4096['total_chunks'])} "
            "chunks respectively, so chunk-size changes "
            "had little observed effect over this range."
        ),
        "",
        (
            "Semantic threshold was more influential: "
            "at chunk size 2048, threshold 0.7 produced "
            f"{fint(semantic_070['total_chunks'])} chunks, "
            "threshold 0.8 produced "
            f"{fint(semantic_2048['total_chunks'])}, and "
            "threshold 0.9 produced "
            f"{fint(semantic_090['total_chunks'])}. "
            "Mean chunk character length moved in the "
            "opposite direction as the threshold "
            "increased."
        ),
        "",
        (
            "These are within-method parameter effects. "
            "They do not establish a cross-method quality "
            "ordering."
        ),
    ]
)

append_source(
    lines,
    TABLE_PATHS["sensitivity"],
)


# ------------------------------------------------------------------
# Matched granularity
# ------------------------------------------------------------------

lines.extend(
    [
        "## 4. Matched-Granularity Comparison",
        "",
        "### Matching Procedure",
        "",
        (
            "The selected settings minimize the worst "
            "relative spread over three matching metrics: "
            "median chunk character length, mean chunk "
            "character length, and mean chunks per "
            "document. Relative spread is defined as "
            "`(max - min) / mean`."
        ),
        "",
        (
            "The frozen matching tolerance is "
            f"{matched_settings['matching_tolerance'] * 100:.1f}%."
        ),
        "",
        (
            "The selected settings achieved a worst "
            "observed relative spread of "
            f"{matched_settings['worst_relative_spread'] * 100:.3f}%."
        ),
        "",
        "### Selected Configurations",
        "",
    ]
)

matched_setting_rows = []

for method in [
    "token",
    "recursive",
    "semantic",
]:
    item = (
        matched_settings[
            "matched_runs"
        ][method]
    )

    matched_setting_rows.append(
        [
            method,
            item["run_id"],
            "`"
            + json.dumps(
                item,
                sort_keys=True,
                separators=(",", ":"),
            )
            + "`",
        ]
    )

lines.extend(
    markdown_table(
        [
            "Method",
            "Run",
            "Configuration",
        ],
        matched_setting_rows,
    )
)

lines.extend(
    [
        "",
        "### Results",
        "",
    ]
)

matched_table_rows = []

for method in [
    "token",
    "recursive",
    "semantic",
]:
    row = matched_by_method[
        method
    ]

    matched_table_rows.append(
        [
            method,
            fint(
                row[
                    "total_chunks"
                ]
            ),
            fnum(
                row[
                    "mean_chunks_per_document"
                ]
            ),
            fnum(
                row[
                    "median_chunk_char_length"
                ]
            ),
            fnum(
                row[
                    "mean_chunk_char_length"
                ]
            ),
            pct_fraction(
                row[
                    "small_chunk_fraction"
                ]
            ),
            pct_fraction(
                row[
                    "newline_boundary_internal"
                ]
            ),
            pct_fraction(
                row[
                    "sentence_boundary_internal"
                ]
            ),
            pct_fraction(
                row[
                    "whitespace_boundary_internal"
                ]
            ),
            pct_fraction(
                row[
                    "other_boundary_internal"
                ]
            ),
            fnum(
                row[
                    "elapsed_seconds"
                ],
                6,
            ),
            fint(
                row[
                    "warning_count"
                ]
            ),
            row[
                "qa_status"
            ],
        ]
    )

lines.extend(
    markdown_table(
        [
            "Method",
            "Chunks",
            "Mean chunks/doc",
            "Median chars",
            "Mean chars",
            "Small <256",
            "Newline",
            "Sentence",
            "Whitespace",
            "Other",
            "Seconds",
            "Warnings",
            "QA",
        ],
        matched_table_rows,
    )
)

lines.extend(
    [
        "",
        "### Interpretation",
        "",
        (
            "Approximate aggregate granularity matching "
            "does not remove structural differences. "
            "TokenChunker remains dominated by "
            "`other_boundary` and whitespace endings, "
            "RecursiveChunker remains predominantly "
            "newline-aligned, and SemanticChunker remains "
            "split between sentence and newline "
            "boundaries."
        ),
        "",
        (
            "Under the frozen `char_length < 256` "
            "fragmentation definition, the matched runs "
            "also retain different very-small-chunk "
            "frequencies. These values are descriptive "
            "fragmentation evidence rather than a direct "
            "quality score."
        ),
        "",
        (
            "All three matched runs processed all "
            "32 source documents with zero processing "
            "failures and QA status `pass`. The matched "
            "SemanticChunker run retained one warning."
        ),
    ]
)

append_source(
    lines,
    MATCHED_SETTINGS_PATH,
    TABLE_PATHS["matched"],
)


# ------------------------------------------------------------------
# Robustness
# ------------------------------------------------------------------

lines.extend(
    [
        "## 5. Robustness",
        "",
        "### Representative-Group Results",
        "",
        (
            "The representative sample contains ten "
            "overlapping profiling groups. Group overlap "
            "is preserved rather than deduplicated."
        ),
        "",
    ]
)

robustness_table_rows = []

for row in robustness:
    robustness_table_rows.append(
        [
            row[
                "group"
            ],
            row[
                "method"
            ],
            fint(
                row[
                    "documents"
                ]
            ),
            fnum(
                row[
                    "mean_chunks_per_document"
                ]
            ),
            fnum(
                row[
                    "median_chunk_char_length"
                ]
            ),
            pct_fraction(
                row[
                    "small_chunk_fraction"
                ]
            ),
            pct_fraction(
                row[
                    "newline_boundary_internal"
                ]
            ),
            pct_fraction(
                row[
                    "sentence_boundary_internal"
                ]
            ),
            pct_fraction(
                row[
                    "whitespace_boundary_internal"
                ]
            ),
            pct_fraction(
                row[
                    "other_boundary_internal"
                ]
            ),
        ]
    )

lines.extend(
    markdown_table(
        [
            "Group",
            "Method",
            "Docs",
            "Chunks/doc",
            "Median chars",
            "Small <256",
            "Newline",
            "Sentence",
            "Whitespace",
            "Other",
        ],
        robustness_table_rows,
    )
)

lines.extend(
    [
        "",
        "### Long-Document Behaviour",
        "",
    ]
)

long_output_rows = []

for group in [
    "length_p95",
    "length_p99",
    "length_max",
]:
    for method in [
        "token",
        "recursive",
        "semantic",
    ]:
        row = find_one(
            robustness,
            group=group,
            method=method,
        )

        long_output_rows.append(
            [
                group,
                method,
                fnum(
                    row[
                        "mean_chunks_per_document"
                    ]
                ),
                fnum(
                    row[
                        "median_chunk_char_length"
                    ]
                ),
                fnum(
                    row[
                        "mean_chunk_char_length"
                    ]
                ),
                pct_fraction(
                    row[
                        "small_chunk_fraction"
                    ]
                ),
            ]
        )

lines.extend(
    markdown_table(
        [
            "Group",
            "Method",
            "Chunks/doc",
            "Median chars",
            "Mean chars",
            "Small <256",
        ],
        long_output_rows,
    )
)

lines.extend(
    [
        "",
        "### Controlled Long-Document Runtime",
        "",
    ]
)

long_runtime_rows = []

for row in long_runtime:
    long_runtime_rows.append(
        [
            row["group"],
            row["method"],
            fint(
                row[
                    "input_documents"
                ]
            ),
            fint(
                row[
                    "input_total_characters"
                ]
            ),
            fint(
                row[
                    "generated_chunks"
                ]
            ),
            fnum(
                row[
                    "elapsed_seconds"
                ],
                6,
            ),
            fnum(
                row[
                    "seconds_per_document"
                ],
                6,
            ),
            fint(
                row[
                    "warning_count"
                ]
            ),
            row[
                "qa_status"
            ],
        ]
    )

lines.extend(
    markdown_table(
        [
            "Group",
            "Method",
            "Docs",
            "Input chars",
            "Chunks",
            "Seconds",
            "Seconds/doc",
            "Warnings",
            "QA",
        ],
        long_runtime_rows,
    )
)

lines.extend(
    [
        "",
        "### Interpretation",
        "",
        (
            "The representative groups show that aggregate "
            "matching does not imply subgroup matching. "
            "Document length, newline structure, and "
            "chars-per-stored-token profile remain "
            "associated with different output patterns."
        ),
        "",
        (
            "The `no_newline` cases are particularly useful "
            "for separating newline-dependent behaviour "
            "from other boundary mechanisms: RecursiveChunker "
            "cannot rely on newline boundaries in those "
            "documents, while sentence-boundary behaviour "
            "becomes more visible."
        ),
        "",
        (
            "P95, P99, and maximum-length controlled runs "
            "all completed with zero processing failures "
            "and QA status `pass`. Runtime increases on "
            "larger inputs, but these are single-run "
            "descriptive pipeline measurements, not "
            "statistically repeated benchmarks."
        ),
    ]
)

append_source(
    lines,
    TABLE_PATHS["robustness"],
    TABLE_PATHS["long_runtime"],
)


# ------------------------------------------------------------------
# Cost
# ------------------------------------------------------------------

lines.extend(
    [
        "## 6. Computational Cost",
        "",
        "### Matched 32-Document Runs",
        "",
    ]
)

cost_table_rows = []

for method in [
    "token",
    "recursive",
    "semantic",
]:
    row = cost_by_method[
        method
    ]

    cost_table_rows.append(
        [
            method,
            fint(
                row[
                    "processed_documents"
                ]
            ),
            fint(
                row[
                    "total_chunks"
                ]
            ),
            fnum(
                row[
                    "elapsed_seconds"
                ],
                6,
            ),
            fnum(
                row[
                    "seconds_per_document"
                ],
                6,
            ),
            fnum(
                row[
                    "documents_per_second"
                ],
                3,
            ),
            fnum(
                row[
                    "chunks_per_second"
                ],
                3,
            ),
            fint(
                row[
                    "output_bytes"
                ]
            ),
            fint(
                row[
                    "warning_count"
                ]
            ),
        ]
    )

lines.extend(
    markdown_table(
        [
            "Method",
            "Docs",
            "Chunks",
            "Seconds",
            "Seconds/doc",
            "Docs/s",
            "Chunks/s",
            "Output bytes",
            "Warnings",
        ],
        cost_table_rows,
    )
)

lines.extend(
    [
        "",
        "### Week 2 Scaled TokenChunker Evidence",
        "",
    ]
)

lines.extend(
    markdown_table(
        [
            "Method",
            "Docs",
            "Chunks",
            "Failures",
            "Seconds",
            "Docs/s",
            "Chunks/s",
            "Output bytes",
            "Max RSS KB",
            "QA",
        ],
        [
            [
                scaled_row[
                    "method"
                ],
                scaled_row[
                    "processed_documents"
                ],
                scaled_row[
                    "chunks_written"
                ],
                scaled_row[
                    "failed_documents"
                ],
                fnum(
                    scaled_row[
                        "elapsed_seconds"
                    ],
                    6,
                ),
                fnum(
                    scaled_row[
                        "documents_per_second"
                    ],
                    3,
                ),
                fnum(
                    scaled_row[
                        "chunks_per_second"
                    ],
                    3,
                ),
                scaled_row[
                    "chunk_output_bytes"
                ],
                scaled_row[
                    "max_rss_kb"
                ],
                scaled_row[
                    "qa_status"
                ],
            ]
        ],
    )
)

lines.extend(
    [
        "",
        "### Interpretation",
        "",
        (
            "The matched 32-document runs show substantial "
            "differences in observed pipeline runtime and "
            "throughput. SemanticChunker uses the local "
            "`minishlab/potion-base-32M` embedding path and "
            "has higher observed elapsed time in these "
            "experiments."
        ),
        "",
        (
            "These timings are pipeline-level engineering "
            "measurements. They should not be decomposed "
            "into pure algorithmic cost, model-loading cost, "
            "or I/O cost without additional instrumentation."
        ),
        "",
        (
            "Memory was not measured for the three matched "
            "Issue #16 runs or the Issue #17 controlled "
            "long-document runs."
        ),
        "",
        (
            "The directly recorded Week 2 scaled "
            "TokenChunker resource measurement is "
            f"`max_rss_kb={scaled_row['max_rss_kb']}`. "
            "That value applies only to the scaled "
            "TokenChunker run and is not extrapolated to "
            "other methods."
        ),
        "",
        (
            "The Week 2 scaled run also uses a different "
            "TokenChunker configuration from the Issue #16 "
            "matched run, so it is supporting engineering-"
            "scale evidence rather than a matched-method "
            "comparison."
        ),
    ]
)

append_source(
    lines,
    TABLE_PATHS["cost"],
    TABLE_PATHS["scaled"],
)


# ------------------------------------------------------------------
# Reliability
# ------------------------------------------------------------------

lines.extend(
    [
        "## 7. Reliability and QA",
        "",
        "### Results",
        "",
        (
            f"The canonical reliability table contains "
            f"{len(reliability)} stored run records. "
            "Every inventoried run metadata record has "
            "`status=completed`, every run has zero "
            "processing failures, and every associated "
            "QA summary has status `pass`."
        ),
        "",
        (
            "The standard QA records report zero "
            "hard-failure events where that field is "
            "present. The Week 2 scaled QA uses a "
            "different validation schema, so missing "
            "fields are not silently converted to zero."
        ),
        "",
        (
            f"Across records with an explicit warning "
            f"count, {known_warning_total} warning event(s) "
            "were recorded."
        ),
        "",
    ]
)

if known_warning_rows:
    warning_rows = []

    for row in (
        known_warning_rows
    ):
        warning_rows.append(
            [
                row[
                    "evidence_label"
                ],
                row[
                    "warning_count"
                ],
                row[
                    "failed_documents"
                ],
                row[
                    "qa_status"
                ],
            ]
        )

    lines.extend(
        markdown_table(
            [
                "Evidence",
                "Warnings",
                "Failures",
                "QA",
            ],
            warning_rows,
        )
    )

    lines.append("")

if unknown_warning_rows:
    lines.append(
        (
            "Warning count is not recorded in the "
            "QA schema for: "
            + ", ".join(
                "`"
                + row[
                    "evidence_label"
                ]
                + "`"
                for row in (
                    unknown_warning_rows
                )
            )
            + "."
        )
    )

    lines.append("")

lines.extend(
    [
        "### Source and Provenance Integrity",
        "",
        (
            "QA validates stored chunk outputs against "
            "source provenance. Across the accepted "
            "evidence, source-slice integrity, document "
            "identity, required provenance, and index "
            "validation pass according to the stored QA "
            "summaries."
        ),
        "",
        (
            "The representative sample hash remains "
            "unchanged from the frozen Week 3 input hash. "
            "The complete post-deduplication dataset is "
            "covered by the preserved 57-entry SHA256 "
            "manifest."
        ),
    ]
)

append_source(
    lines,
    TABLE_PATHS["reliability"],
    INVENTORY_PATH,
    FREEZE_PATH,
)


# ------------------------------------------------------------------
# Limitations
# ------------------------------------------------------------------

lines.extend(
    [
        "## 8. Limitations",
        "",
        (
            "1. **Tokenizer semantics differ across "
            "methods.** TokenChunker and RecursiveChunker "
            "use the character tokenizer in the tested "
            "configurations, whereas SemanticChunker uses "
            "its local Model2Vec tokenizer. Token-count "
            "statistics therefore are not directly "
            "comparable quality units."
        ),
        "",
        (
            "2. **The representative set is small.** "
            "Most profiling groups contain only a few "
            "documents, and groups may overlap. Group-level "
            "statistics are descriptive rather than "
            "population estimates."
        ),
        "",
        (
            "3. **Matched granularity is approximate.** "
            "The frozen tolerance is 30%, and the selected "
            "settings still retain measurable residual "
            "differences at both aggregate and subgroup "
            "levels."
        ),
        "",
        (
            "4. **Retrieval relevance labels are absent "
            "from the current canonical evidence.** "
            "Therefore the study does not establish which "
            "method produces better retrieval or downstream "
            "task quality."
        ),
        "",
        (
            "5. **SemanticChunker numerical warnings are "
            "present in several stored runs.** They are "
            "recorded separately from processing failures; "
            "the affected runs still pass QA."
        ),
        "",
        (
            "6. **Full-scale cross-method testing is "
            "limited.** The available 227,628-document "
            "scaled evidence is for TokenChunker only. "
            "RecursiveChunker and SemanticChunker were not "
            "run over the same scaled corpus during this "
            "sprint."
        ),
        "",
        (
            "7. **Runtime evidence is descriptive.** "
            "The principal runtime measurements are "
            "single pipeline runs, not repeated benchmark "
            "distributions. Pipeline timings also combine "
            "multiple operational costs."
        ),
        "",
        (
            "8. **Memory evidence is incomplete across "
            "methods.** A recorded maximum RSS is available "
            "for the Week 2 scaled TokenChunker run only."
        ),
        "",
        (
            "9. **The Git repository currently has an "
            "unborn HEAD.** The reproducibility freeze "
            f"records branch "
            f"`{freeze['git']['branch']}`, "
            "the working-tree state, and the absence of "
            "a resolvable commit hash rather than "
            "inventing one."
        ),
    ]
)

append_source(
    lines,
    CANONICAL_SUMMARY_PATH,
    FREEZE_PATH,
)


# ------------------------------------------------------------------
# Conclusions
# ------------------------------------------------------------------

lines.extend(
    [
        "## 9. Conclusions",
        "",
        "### Evidence-Supported Trade-offs",
        "",
        (
            "**TokenChunker:** chunk size provides a "
            "direct and predictable granularity control "
            "under the character-tokenizer configuration. "
            "Its tested boundaries frequently terminate "
            "at whitespace or positions classified as "
            "`other_boundary`, reflecting its fixed-size "
            "behaviour."
        ),
        "",
        (
            "**RecursiveChunker:** chunk size also strongly "
            "controls granularity, while the method makes "
            "much greater use of newline structure in the "
            "tested corpus. Its output therefore differs "
            "structurally from TokenChunker even when the "
            "configured or observed granularity is similar."
        ),
        "",
        (
            "**SemanticChunker:** configured chunk size "
            "between 1024 and 4096 had little observed "
            "granularity effect at threshold 0.8 on the "
            "representative sample, whereas threshold "
            "changes materially altered chunk count and "
            "chunk length. The method more often ended "
            "chunks on sentence/newline boundaries, "
            "produced more very small chunks under the "
            "matched setting, and incurred higher observed "
            "pipeline runtime in the collected evidence."
        ),
        "",
        (
            "Across all three methods, long-document and "
            "representative-group results show that "
            "aggregate statistics alone are insufficient "
            "to characterize robustness. Document "
            "structure changes the observed behaviour."
        ),
        "",
        (
            "The evidence therefore supports a set of "
            "method-specific trade-offs rather than an "
            "overall winner."
        ),
        "",
        "### Evidence Required for Stronger Claims",
        "",
        (
            "Stronger chunk-quality conclusions would "
            "require retrieval-relevance labels or "
            "downstream task evaluation, larger and "
            "independent representative samples, repeated "
            "runtime/resource measurements, and scaled "
            "processing evidence for RecursiveChunker and "
            "SemanticChunker under comparable conditions."
        ),
        "",
        "## Reproducibility and Evidence Paths",
        "",
        (
            "Canonical report tables are stored under "
            "`week3/reports/tables/`."
        ),
        "",
        (
            "The final evidence inventory is "
            "`week3/reports/issue18_evidence_inventory.json`."
        ),
        "",
        (
            "The reproducibility freeze is "
            "`week3/reports/issue18_reproducibility_freeze.json`."
        ),
        "",
        (
            "The human-readable comparison-table index is "
            "`week3/reports/final_comparison_tables.md`."
        ),
        "",
        (
            "The report traceability manifest is "
            "`week3/reports/report_traceability.json`."
        ),
        "",
        (
            "**Status:** Week 3 evidence consolidated; "
            "ready for final reproducibility and report "
            "consistency audit."
        ),
        "",
    ]
)

REPORT_PATH.write_text(
    "\n".join(lines),
    encoding="utf-8",
)


# ------------------------------------------------------------------
# Final comparison-table index
# ------------------------------------------------------------------

index_lines = [
    "# Week 3 Final Comparison Tables",
    "",
    (
        "These CSV files are the canonical machine-readable "
        "tables used to generate the final Week 3 report."
    ),
    "",
    (
        "The canonical CSV values are retained without "
        "report-level numeric rounding."
    ),
    "",
]

index_rows = []

for table_name, spec in (
    canonical["tables"].items()
):
    index_rows.append(
        [
            table_name,
            f"`{spec['path']}`",
            str(
                spec["rows"]
            ),
            "`"
            + spec["sha256"]
            + "`",
            ", ".join(
                "`"
                + source
                + "`"
                for source
                in spec[
                    "sources"
                ]
            ),
        ]
    )

index_lines.extend(
    markdown_table(
        [
            "Table",
            "Path",
            "Rows",
            "SHA256",
            "Source evidence",
        ],
        index_rows,
    )
)

index_lines.extend(
    [
        "",
        "## Key Matched Comparison",
        "",
    ]
)

index_lines.extend(
    markdown_table(
        [
            "Method",
            "Chunks",
            "Chunks/doc",
            "Median chars",
            "Mean chars",
            "Small <256",
            "Seconds",
            "Warnings",
            "QA",
        ],
        [
            [
                method,
                matched_by_method[
                    method
                ][
                    "total_chunks"
                ],
                fnum(
                    matched_by_method[
                        method
                    ][
                        "mean_chunks_per_document"
                    ]
                ),
                fnum(
                    matched_by_method[
                        method
                    ][
                        "median_chunk_char_length"
                    ]
                ),
                fnum(
                    matched_by_method[
                        method
                    ][
                        "mean_chunk_char_length"
                    ]
                ),
                pct_fraction(
                    matched_by_method[
                        method
                    ][
                        "small_chunk_fraction"
                    ]
                ),
                fnum(
                    matched_by_method[
                        method
                    ][
                        "elapsed_seconds"
                    ],
                    6,
                ),
                matched_by_method[
                    method
                ][
                    "warning_count"
                ],
                matched_by_method[
                    method
                ][
                    "qa_status"
                ],
            ]
            for method in [
                "token",
                "recursive",
                "semantic",
            ]
        ],
    )
)

index_lines.extend(
    [
        "",
        "## Scaled Engineering Evidence",
        "",
    ]
)

index_lines.extend(
    markdown_table(
        [
            "Method",
            "Docs",
            "Chunks",
            "Seconds",
            "Output bytes",
            "Max RSS KB",
            "QA",
        ],
        [
            [
                scaled_row[
                    "method"
                ],
                scaled_row[
                    "processed_documents"
                ],
                scaled_row[
                    "chunks_written"
                ],
                fnum(
                    scaled_row[
                        "elapsed_seconds"
                    ],
                    6,
                ),
                scaled_row[
                    "chunk_output_bytes"
                ],
                scaled_row[
                    "max_rss_kb"
                ],
                scaled_row[
                    "qa_status"
                ],
            ]
        ],
    )
)

index_lines.append("")

TABLE_INDEX_PATH.write_text(
    "\n".join(
        index_lines
    ),
    encoding="utf-8",
)


# ------------------------------------------------------------------
# Traceability manifest
# ------------------------------------------------------------------

section_sources = {
    "1.experimental_setup": [
        ENV_PATH,
        BASELINE_CONFIG_PATH,
        CONSTANTS_PATH,
        PLAN_PATH,
        METRIC_SPEC_PATH,
        FREEZE_PATH,
    ],
    "2.baseline_results": [
        TABLE_PATHS[
            "baseline"
        ],
    ],
    "3.parameter_sensitivity": [
        TABLE_PATHS[
            "sensitivity"
        ],
    ],
    "4.matched_granularity": [
        MATCHED_SETTINGS_PATH,
        TABLE_PATHS[
            "matched"
        ],
    ],
    "5.robustness": [
        TABLE_PATHS[
            "robustness"
        ],
        TABLE_PATHS[
            "long_runtime"
        ],
    ],
    "6.computational_cost": [
        TABLE_PATHS[
            "cost"
        ],
        TABLE_PATHS[
            "scaled"
        ],
    ],
    "7.reliability_qa": [
        TABLE_PATHS[
            "reliability"
        ],
        INVENTORY_PATH,
        FREEZE_PATH,
    ],
    "8.limitations": [
        CANONICAL_SUMMARY_PATH,
        FREEZE_PATH,
    ],
    "9.conclusions": [
        TABLE_PATHS[
            "baseline"
        ],
        TABLE_PATHS[
            "sensitivity"
        ],
        TABLE_PATHS[
            "matched"
        ],
        TABLE_PATHS[
            "robustness"
        ],
        TABLE_PATHS[
            "long_runtime"
        ],
        TABLE_PATHS[
            "cost"
        ],
        TABLE_PATHS[
            "scaled"
        ],
    ],
}

trace_sections = {}

for section, paths in (
    section_sources.items()
):
    trace_sections[
        section
    ] = [
        {
            "path":
                rel(path),
            "sha256":
                sha256_file(
                    path
                ),
            "bytes":
                path.stat()
                .st_size,
        }
        for path in paths
    ]

trace = {
    "schema_version": 1,
    "report":
        rel(
            REPORT_PATH
        ),
    "report_sha256":
        sha256_file(
            REPORT_PATH
        ),
    "comparison_table_index":
        rel(
            TABLE_INDEX_PATH
        ),
    "comparison_table_index_sha256":
        sha256_file(
            TABLE_INDEX_PATH
        ),
    "canonical_summary":
        rel(
            CANONICAL_SUMMARY_PATH
        ),
    "canonical_summary_sha256":
        sha256_file(
            CANONICAL_SUMMARY_PATH
        ),
    "report_generation": {
        "new_chunking_runs":
            False,
        "canonical_tables_only_for_experiment_numbers":
            True,
        "report_display_rounding":
            True,
        "canonical_numeric_rounding":
            False,
        "unsupported_overall_winner":
            False,
    },
    "sections":
        trace_sections,
}

TRACE_PATH.write_text(
    json.dumps(
        trace,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)


# ------------------------------------------------------------------
# Console output
# ------------------------------------------------------------------

print("=" * 100)
print(
    "ISSUE #18 FINAL WEEK 3 REPORT BUILD"
)
print("=" * 100)

print(
    "Report:",
    REPORT_PATH,
)

print(
    "Report bytes:",
    REPORT_PATH.stat().st_size,
)

print(
    "Report SHA256:",
    sha256_file(
        REPORT_PATH
    ),
)

print(
    "Comparison-table index:",
    TABLE_INDEX_PATH,
)

print(
    "Traceability manifest:",
    TRACE_PATH,
)

print()
print(
    "Baseline rows consumed:",
    len(baseline),
)

print(
    "Sensitivity rows consumed:",
    len(sensitivity),
)

print(
    "Matched rows consumed:",
    len(matched),
)

print(
    "Robustness rows consumed:",
    len(robustness),
)

print(
    "Long-runtime rows consumed:",
    len(long_runtime),
)

print(
    "Cost rows consumed:",
    len(cost),
)

print(
    "Reliability rows consumed:",
    len(reliability),
)

print(
    "Scaled rows consumed:",
    len(scaled),
)

print()
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

print()
print(
    "ISSUE #18 STEP 3 FINAL REPORT BUILD: PASS"
)
