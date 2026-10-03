from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(
    "/home/jovyan/chunking_sprint"
)

RESULT_DIR = (
    ROOT
    / "week3/results/issue17"
)

ROBUSTNESS_PATH = (
    RESULT_DIR
    / "robustness_summary.json"
)

SCALED_PATH = (
    RESULT_DIR
    / "scaled_engineering_evidence.json"
)

LONG_RUNTIME_PATH = (
    RESULT_DIR
    / "long_runtime/"
      "long_runtime_summary.json"
)

LONG_INPUT_PATH = (
    ROOT
    / "week3/inputs/"
      "issue17_long_runtime_inputs.json"
)

REPORT_PATH = (
    RESULT_DIR
    / "final_report.md"
)

SUMMARY_PATH = (
    RESULT_DIR
    / "final_summary.json"
)


METHODS = [
    "token",
    "recursive",
    "semantic",
]

GROUPS = [
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
]

LENGTH_GROUPS = [
    "length_min",
    "length_p05",
    "length_median",
    "length_p90",
    "length_p95",
    "length_p99",
    "length_max",
]

LONG_GROUPS = [
    "length_p95",
    "length_p99",
    "length_max",
]


def load(path: Path):
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def pct(value: float) -> str:
    return (
        f"{value * 100:.2f}%"
    )


def find_row(
    rows,
    method,
    group,
):
    matches = [
        row
        for row in rows
        if (
            row["method"] == method
            and row["group"] == group
        )
    ]

    if len(matches) != 1:
        raise RuntimeError(
            f"Expected one row for "
            f"{method}/{group}, "
            f"found {len(matches)}."
        )

    return matches[0]


def extrema(
    rows,
    key,
):
    low = min(
        rows,
        key=lambda x: x[key],
    )

    high = max(
        rows,
        key=lambda x: x[key],
    )

    return low, high


def main() -> None:
    robustness = load(
        ROBUSTNESS_PATH
    )

    scaled = load(
        SCALED_PATH
    )

    long_runtime = load(
        LONG_RUNTIME_PATH
    )

    long_inputs = load(
        LONG_INPUT_PATH
    )

    robustness_rows = (
        robustness[
            "robustness_by_group"
        ]
    )

    cost_rows = (
        robustness[
            "computational_cost"
        ]
    )

    runtime_rows = (
        long_runtime[
            "records"
        ]
    )

    assert (
        robustness[
            "source_documents"
        ]
        == 32
    )

    assert len(
        robustness_rows
    ) == 30

    assert len(
        cost_rows
    ) == 3

    assert len(
        runtime_rows
    ) == 9

    assert (
        long_inputs[
            "unique_documents_across_groups"
        ]
        == 9
    )

    by_method_cost = {
        row["method"]: row
        for row in cost_rows
    }

    assert (
        set(by_method_cost)
        == set(METHODS)
    )

    runtime_map = {
        (
            row["method"],
            row["group"],
        ): row
        for row in runtime_rows
    }

    assert (
        len(runtime_map)
        == 9
    )

    lines = [
        "# Issue 17 — Robustness and Computational Cost",
        "",
        "## Scope",
        "",
        (
            "This report evaluates robustness and "
            "operational behaviour for the frozen "
            "matched-granularity TokenChunker, "
            "RecursiveChunker, and SemanticChunker "
            "configurations."
        ),
        "",
        (
            "The primary robustness evidence uses "
            "the same frozen 32-document representative "
            "sample used in Issue 16."
        ),
        "",
        (
            "Computational cost is reported separately "
            "from chunk-quality interpretation. "
            "No overall chunk-quality ranking is assigned."
        ),
        "",
        "## Evidence Base",
        "",
        (
            "The analysis combines four evidence classes: "
            "the 32-document matched runs, representative-"
            "group output statistics, controlled "
            "P95/P99/maximum-length runtime runs, and "
            "the existing Week 2 scaled TokenChunker run."
        ),
        "",
        "## Representative-Group Robustness",
        "",
        (
            "A very small chunk retains the frozen "
            "Issue 16 definition `char_length < 256`."
        ),
        "",
        (
            "| Group | Method | Docs | Chunks/doc | "
            "Median chars | Mean chars | Small % | "
            "Paragraph | Newline | Sentence | "
            "Whitespace | Other |"
        ),
        (
            "|---|---|---:|---:|---:|---:|---:|"
            "---:|---:|---:|---:|---:|"
        ),
    ]

    for group in GROUPS:
        for method in METHODS:
            row = find_row(
                robustness_rows,
                method,
                group,
            )

            lines.append(
                f"| {group} "
                f"| {method} "
                f"| {row['documents']} "
                f"| {row['mean_chunks_per_document']:.3f} "
                f"| {row['median_chunk_char_length']:.3f} "
                f"| {row['mean_chunk_char_length']:.3f} "
                f"| {pct(row['small_chunk_fraction'])} "
                f"| {pct(row['paragraph_boundary_internal'])} "
                f"| {pct(row['newline_boundary_internal'])} "
                f"| {pct(row['sentence_boundary_internal'])} "
                f"| {pct(row['whitespace_boundary_internal'])} "
                f"| {pct(row['other_boundary_internal'])} |"
            )

    lines.extend(
        [
            "",
            "## Document-Length Sensitivity",
            "",
            (
                "The table below summarizes the observed "
                "range across the seven frozen "
                "length-labelled groups. These ranges "
                "describe variation; they are not quality "
                "scores."
            ),
            "",
            (
                "| Method | Chunks/doc range | "
                "Median-char range | Small-chunk range |"
            ),
            "|---|---|---|---|",
        ]
    )

    length_sensitivity = {}

    for method in METHODS:
        rows = [
            find_row(
                robustness_rows,
                method,
                group,
            )
            for group in LENGTH_GROUPS
        ]

        cpd_lo, cpd_hi = extrema(
            rows,
            "mean_chunks_per_document",
        )

        med_lo, med_hi = extrema(
            rows,
            "median_chunk_char_length",
        )

        small_lo, small_hi = extrema(
            rows,
            "small_chunk_fraction",
        )

        length_sensitivity[
            method
        ] = {
            "chunks_per_document": {
                "min_group":
                    cpd_lo["group"],
                "min":
                    cpd_lo[
                        "mean_chunks_per_document"
                    ],
                "max_group":
                    cpd_hi["group"],
                "max":
                    cpd_hi[
                        "mean_chunks_per_document"
                    ],
            },
            "median_chunk_char_length": {
                "min_group":
                    med_lo["group"],
                "min":
                    med_lo[
                        "median_chunk_char_length"
                    ],
                "max_group":
                    med_hi["group"],
                "max":
                    med_hi[
                        "median_chunk_char_length"
                    ],
            },
            "small_chunk_fraction": {
                "min_group":
                    small_lo["group"],
                "min":
                    small_lo[
                        "small_chunk_fraction"
                    ],
                "max_group":
                    small_hi["group"],
                "max":
                    small_hi[
                        "small_chunk_fraction"
                    ],
            },
        }

        lines.append(
            f"| {method} "
            f"| {cpd_lo['mean_chunks_per_document']:.3f}"
            f" ({cpd_lo['group']}) – "
            f"{cpd_hi['mean_chunks_per_document']:.3f}"
            f" ({cpd_hi['group']}) "
            f"| {med_lo['median_chunk_char_length']:.3f}"
            f" ({med_lo['group']}) – "
            f"{med_hi['median_chunk_char_length']:.3f}"
            f" ({med_hi['group']}) "
            f"| {pct(small_lo['small_chunk_fraction'])}"
            f" ({small_lo['group']}) – "
            f"{pct(small_hi['small_chunk_fraction'])}"
            f" ({small_hi['group']}) |"
        )

    lines.extend(
        [
            "",
            "## Newline-Structure Sensitivity",
            "",
            (
                "The `no_newline` representative group "
                "provides the direct frozen evidence for "
                "documents without newline structure."
            ),
            "",
            (
                "| Method | Docs | Chunks/doc | "
                "Median chars | Small % | Newline | "
                "Sentence | Whitespace | Other |"
            ),
            (
                "|---|---:|---:|---:|---:|"
                "---:|---:|---:|---:|"
            ),
        ]
    )

    for method in METHODS:
        row = find_row(
            robustness_rows,
            method,
            "no_newline",
        )

        lines.append(
            f"| {method} "
            f"| {row['documents']} "
            f"| {row['mean_chunks_per_document']:.3f} "
            f"| {row['median_chunk_char_length']:.3f} "
            f"| {pct(row['small_chunk_fraction'])} "
            f"| {pct(row['newline_boundary_internal'])} "
            f"| {pct(row['sentence_boundary_internal'])} "
            f"| {pct(row['whitespace_boundary_internal'])} "
            f"| {pct(row['other_boundary_internal'])} |"
        )

    lines.extend(
        [
            "",
            "## Chars-per-Stored-Token Sensitivity",
            "",
            (
                "The high and low "
                "`chars_per_stored_token` groups are "
                "reported side by side. Stored token "
                "counts are provenance data and are not "
                "treated as a common tokenizer definition "
                "for all chunkers."
            ),
            "",
            (
                "| Method | High docs | High median chars | "
                "High small % | Low docs | "
                "Low median chars | Low small % |"
            ),
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )

    for method in METHODS:
        high = find_row(
            robustness_rows,
            method,
            "high_chars_per_token",
        )

        low = find_row(
            robustness_rows,
            method,
            "low_chars_per_token",
        )

        lines.append(
            f"| {method} "
            f"| {high['documents']} "
            f"| {high['median_chunk_char_length']:.3f} "
            f"| {pct(high['small_chunk_fraction'])} "
            f"| {low['documents']} "
            f"| {low['median_chunk_char_length']:.3f} "
            f"| {pct(low['small_chunk_fraction'])} |"
        )

    lines.extend(
        [
            "",
            "## Very-Long-Document Output Behaviour",
            "",
            (
                "P95, P99, and maximum-length groups "
                "are shown explicitly."
            ),
            "",
            (
                "| Group | Method | Docs | Chunks/doc | "
                "Median chars | Mean chars | Small % |"
            ),
            "|---|---|---:|---:|---:|---:|---:|",
        ]
    )

    for group in LONG_GROUPS:
        for method in METHODS:
            row = find_row(
                robustness_rows,
                method,
                group,
            )

            lines.append(
                f"| {group} "
                f"| {method} "
                f"| {row['documents']} "
                f"| {row['mean_chunks_per_document']:.3f} "
                f"| {row['median_chunk_char_length']:.3f} "
                f"| {row['mean_chunk_char_length']:.3f} "
                f"| {pct(row['small_chunk_fraction'])} |"
            )

    lines.extend(
        [
            "",
            "## Very-Long-Document Runtime",
            "",
            (
                "Each group/method pair below is one "
                "controlled pipeline run. The measurements "
                "are descriptive, not repeated benchmark "
                "estimates."
            ),
            "",
            (
                "| Group | Method | Docs | Input chars | "
                "Chunks | Seconds | Seconds/doc | "
                "Docs/s | Chunks/s | Output bytes | "
                "Warnings | Failures | QA |"
            ),
            (
                "|---|---|---:|---:|---:|---:|---:|"
                "---:|---:|---:|---:|---:|---|"
            ),
        ]
    )

    for group in LONG_GROUPS:
        for method in METHODS:
            row = runtime_map[
                (method, group)
            ]

            lines.append(
                f"| {group} "
                f"| {method} "
                f"| {row['input_documents']} "
                f"| {row['input_total_characters']} "
                f"| {row['generated_chunks']} "
                f"| {row['elapsed_seconds']:.6f} "
                f"| {row['seconds_per_document']:.6f} "
                f"| {row['documents_per_second']:.3f} "
                f"| {row['chunks_per_second']:.3f} "
                f"| {row['output_bytes']} "
                f"| {row['warning_count']} "
                f"| {row['failed_documents']} "
                f"| {row['qa_status']} |"
            )

    lines.extend(
        [
            "",
            "## Long-Input Runtime Scaling",
            "",
            (
                "For each method, the following ratios "
                "compare the maximum-length group with "
                "the P95 group. Input-character and "
                "elapsed-time ratios are arithmetic "
                "derivations from the measured runs."
            ),
            "",
            (
                "| Method | P95 input chars | "
                "Max input chars | Input-char ratio | "
                "P95 seconds | Max seconds | "
                "Elapsed ratio |"
            ),
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )

    runtime_scaling = {}

    for method in METHODS:
        p95 = runtime_map[
            (method, "length_p95")
        ]

        maximum = runtime_map[
            (method, "length_max")
        ]

        char_ratio = (
            maximum[
                "input_total_characters"
            ]
            / p95[
                "input_total_characters"
            ]
        )

        elapsed_ratio = (
            maximum[
                "elapsed_seconds"
            ]
            / p95[
                "elapsed_seconds"
            ]
        )

        runtime_scaling[
            method
        ] = {
            "input_character_ratio":
                char_ratio,
            "elapsed_ratio":
                elapsed_ratio,
        }

        lines.append(
            f"| {method} "
            f"| {p95['input_total_characters']} "
            f"| {maximum['input_total_characters']} "
            f"| {char_ratio:.3f}× "
            f"| {p95['elapsed_seconds']:.6f} "
            f"| {maximum['elapsed_seconds']:.6f} "
            f"| {elapsed_ratio:.3f}× |"
        )

    lines.extend(
        [
            "",
            (
                "These ratios include fixed batch "
                "initialization and I/O overhead. "
                "SemanticChunker pipeline invocations "
                "also include local embedding-model "
                "initialization, so the ratios must not "
                "be interpreted as pure algorithmic "
                "per-document complexity."
            ),
            "",
            "## Matched-Run Computational Cost",
            "",
            (
                "The following cost measurements come "
                "from the 32-document Issue 16 matched "
                "runs."
            ),
            "",
            (
                "| Method | Documents | Chunks | "
                "Seconds | Seconds/doc | Docs/s | "
                "Chunks/s | Output bytes | "
                "Warnings | Failures | QA |"
            ),
            (
                "|---|---:|---:|---:|---:|---:|"
                "---:|---:|---:|---:|---|"
            ),
        ]
    )

    for method in METHODS:
        row = by_method_cost[
            method
        ]

        lines.append(
            f"| {method} "
            f"| {row['processed_documents']} "
            f"| {row['total_chunks']} "
            f"| {row['elapsed_seconds']:.6f} "
            f"| {row['seconds_per_document']:.9f} "
            f"| {row['documents_per_second']:.3f} "
            f"| {row['chunks_per_second']:.3f} "
            f"| {row['output_bytes']} "
            f"| {row['warning_count']} "
            f"| {row['failed_documents']} "
            f"| {row['qa_status']} |"
        )

    scaled_qa = (
        scaled["qa"]
    )

    resource_values = (
        scaled[
            "resource_measurement"
        ]["values"]
    )

    max_rss = (
        resource_values.get(
            "max_rss_kb"
        )
    )

    scaled_warning = (
        scaled_qa.get(
            "warning_count"
        )
    )

    lines.extend(
        [
            "",
            "## Week 2 Scaled Engineering Evidence",
            "",
            (
                "The existing Week 2 scaled run is "
                "supporting engineering evidence for "
                "TokenChunker. It used its recorded "
                "Week 2 configuration and is not the "
                "Issue 16 matched TokenChunker "
                "`chunk_size=839` run."
            ),
            "",
            (
                f"Recorded configuration: "
                f"`{json.dumps(scaled['configuration'], sort_keys=True)}`."
            ),
            "",
            (
                "| Documents | Chunks | Failures | "
                "Elapsed (s) | Docs/s | Chunks/s | "
                "Output bytes | QA |"
            ),
            "|---:|---:|---:|---:|---:|---:|---:|---|",
            (
                f"| {scaled['processed_documents']} "
                f"| {scaled['chunks_written']} "
                f"| {scaled['failed_documents']} "
                f"| {scaled['elapsed_seconds']:.6f} "
                f"| {scaled['documents_per_second']:.3f} "
                f"| {scaled['chunks_per_second']:.3f} "
                f"| {scaled['chunk_output_bytes']} "
                f"| {scaled_qa.get('status')} |"
            ),
            "",
            "## Memory and Resource Evidence",
            "",
            (
                "The three Issue 16 matched runs did not "
                "record a memory measurement. The "
                "controlled Issue 17 long-document runs "
                "also do not introduce a memory claim."
            ),
            "",
            (
                "The Week 2 scaled TokenChunker run did "
                "record resource usage. Its existing "
                f"`max_rss_kb` value is `{max_rss}`. "
                "This measurement applies only to that "
                "scaled run and is not extrapolated to "
                "RecursiveChunker, SemanticChunker, or "
                "the matched configurations."
            ),
            "",
            "## Warnings and Failures",
            "",
            (
                "| Evidence | Method | Failures | "
                "Warnings | QA |"
            ),
            "|---|---|---:|---:|---|",
        ]
    )

    for method in METHODS:
        row = by_method_cost[
            method
        ]

        lines.append(
            f"| Matched 32-doc run "
            f"| {method} "
            f"| {row['failed_documents']} "
            f"| {row['warning_count']} "
            f"| {row['qa_status']} |"
        )

    for method in METHODS:
        method_long = [
            row
            for row in runtime_rows
            if row["method"] == method
        ]

        lines.append(
            f"| Long-document controlled runs "
            f"| {method} "
            f"| {sum(r['failed_documents'] for r in method_long)} "
            f"| {sum(r['warning_count'] for r in method_long)} "
            f"| "
            + (
                "pass"
                if all(
                    r["qa_status"] == "pass"
                    for r in method_long
                )
                else "not-all-pass"
            )
            + " |"
        )

    lines.append(
        f"| Week 2 scaled run "
        f"| token "
        f"| {scaled['failed_documents']} "
        f"| "
        + (
            str(scaled_warning)
            if scaled_warning is not None
            else "not recorded"
        )
        + f" | {scaled_qa.get('status')} |"
    )

    lines.extend(
        [
            "",
            (
                "Warnings are kept separate from "
                "processing failures. In the matched "
                "32-document evidence, the SemanticChunker "
                "run recorded one warning while still "
                "passing QA; this is not converted into "
                "a processing failure."
            ),
            "",
            "## Observed Robustness Interpretation",
            "",
            (
                "The evidence shows that approximate "
                "aggregate granularity matching does not "
                "eliminate group-specific differences. "
                "The representative-group tables retain "
                "variation in chunks per document, "
                "chunk-length distributions, small-chunk "
                "frequency, and boundary-class behaviour."
            ),
            "",
            (
                "Document length is associated with "
                "substantial changes in chunks per "
                "document, while chunk-shape and "
                "fragmentation behaviour remain "
                "method-dependent across the frozen "
                "length groups."
            ),
            "",
            (
                "The `no_newline` group provides direct "
                "evidence that removing newline structure "
                "changes the available boundary pattern. "
                "The high/low chars-per-stored-token "
                "groups likewise show that unusual source "
                "character/token ratios should be retained "
                "as a separate robustness dimension."
            ),
            "",
            (
                "For P95, P99, and maximum-length inputs, "
                "the controlled runtime measurements show "
                "that elapsed pipeline time changes as "
                "input size increases. Because each group "
                "contains a small representative sample "
                "and each timing is a single run, these "
                "measurements support descriptive "
                "engineering conclusions rather than "
                "stable benchmark estimates."
            ),
            "",
            "## Limitations",
            "",
            (
                "Representative groups contain only a "
                "small number of documents and may "
                "overlap. Group-level statistics are "
                "therefore descriptive rather than "
                "population estimates."
            ),
            "",
            (
                "The 32-document matched sample was also "
                "used during matched-setting calibration, "
                "so the resulting observations should "
                "not automatically be generalized to the "
                "entire frozen corpus."
            ),
            "",
            (
                "Aggregate matching does not imply "
                "subgroup-level matching. Residual "
                "granularity differences remain across "
                "representative groups."
            ),
            "",
            (
                "Tokenizer semantics differ across "
                "methods. Stored source token counts and "
                "chunk token counts are therefore not "
                "treated as universally equivalent units."
            ),
            "",
            (
                "Matched and long-document runtime "
                "measurements are single-run pipeline "
                "measurements. They include initialization "
                "and I/O overhead and are not repeated "
                "statistical benchmarks."
            ),
            "",
            (
                "Memory evidence is available only for "
                "the existing Week 2 scaled TokenChunker "
                "run. It is not extrapolated to runs where "
                "memory was not measured."
            ),
            "",
            (
                "The Week 2 scaled TokenChunker run uses "
                "a different TokenChunker configuration "
                "from the Issue 16 matched setting, so it "
                "serves as engineering-scale evidence "
                "rather than a matched-method comparison."
            ),
            "",
            (
                "No downstream retrieval relevance labels "
                "or end-task quality judgments are part of "
                "this issue. Computational cost, boundary "
                "behaviour, and fragmentation statistics "
                "must not individually be interpreted as "
                "overall chunk quality."
            ),
            "",
            "## Conclusion",
            "",
            (
                "Issue 17 now contains representative-group "
                "robustness evidence, explicit P95/P99/"
                "maximum-length output and runtime analysis, "
                "matched-run computational-cost evidence, "
                "warning/failure separation, measured "
                "Week 2 scaled engineering evidence, and "
                "the available resource measurement."
            ),
            "",
            (
                "The evidence is retained as a set of "
                "method- and document-structure-specific "
                "observations. No overall chunk-quality "
                "ranking is assigned."
            ),
            "",
        ]
    )

    REPORT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    final_summary = {
        "schema_version": 1,
        "status":
            "ready_for_acceptance_audit",
        "representative_sample": {
            "documents": 32,
            "groups": GROUPS,
            "methods": METHODS,
            "robustness_rows":
                len(robustness_rows),
            "small_chunk_threshold":
                robustness[
                    "small_chunk_definition"
                ]["threshold"],
            "group_overlap":
                robustness[
                    "group_overlap"
                ],
        },
        "length_sensitivity":
            length_sensitivity,
        "long_document_analysis": {
            "groups": LONG_GROUPS,
            "unique_union_documents":
                long_inputs[
                    "unique_documents_across_groups"
                ],
            "controlled_runs":
                len(runtime_rows),
            "measurement_class":
                long_runtime[
                    "measurement_class"
                ],
            "runtime_scaling":
                runtime_scaling,
            "all_qa_pass":
                all(
                    row["qa_status"]
                    == "pass"
                    for row in runtime_rows
                ),
            "total_failures":
                sum(
                    row[
                        "failed_documents"
                    ]
                    for row
                    in runtime_rows
                ),
            "total_warnings":
                sum(
                    row[
                        "warning_count"
                    ]
                    for row
                    in runtime_rows
                ),
        },
        "matched_cost_runs":
            cost_rows,
        "scaled_engineering_evidence": {
            "method":
                scaled["method"],
            "configuration":
                scaled[
                    "configuration"
                ],
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
            "qa_status":
                scaled_qa.get(
                    "status"
                ),
            "recorded_max_rss_kb":
                max_rss,
        },
        "memory_evidence": {
            "matched_runs":
                "not_measured",
            "long_runtime_runs":
                "not_measured",
            "scaled_token_run_max_rss_kb":
                max_rss,
            "extrapolated":
                False,
        },
        "artifacts": {
            "final_report":
                str(REPORT_PATH),
            "robustness_summary":
                str(ROBUSTNESS_PATH),
            "scaled_evidence":
                str(SCALED_PATH),
            "long_runtime_summary":
                str(LONG_RUNTIME_PATH),
        },
    }

    SUMMARY_PATH.write_text(
        json.dumps(
            final_summary,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "Representative robustness rows:",
        len(robustness_rows),
    )

    print(
        "Long runtime records:",
        len(runtime_rows),
    )

    print(
        "Long runtime failures:",
        final_summary[
            "long_document_analysis"
        ]["total_failures"],
    )

    print(
        "Long runtime warnings:",
        final_summary[
            "long_document_analysis"
        ]["total_warnings"],
    )

    print(
        "Scaled documents:",
        scaled[
            "processed_documents"
        ],
    )

    print(
        "Scaled chunks:",
        scaled[
            "chunks_written"
        ],
    )

    print(
        "Scaled max_rss_kb:",
        max_rss,
    )

    print(
        "Report:",
        REPORT_PATH,
    )

    print(
        "Summary:",
        SUMMARY_PATH,
    )

    print()
    print(
        "ISSUE #17 FINAL REPORT BUILD: PASS"
    )


if __name__ == "__main__":
    main()
