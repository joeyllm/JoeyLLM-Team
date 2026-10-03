from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(
    "/home/jovyan/chunking_sprint"
)

RUN_DIR = (
    ROOT
    / "runs/issue11_token_part0"
)

OUTPUT_DIR = (
    ROOT
    / "week3/results/issue17"
)

METADATA_PATH = (
    RUN_DIR
    / "run_metadata.json"
)

QA_PATH = (
    RUN_DIR
    / "scaled_qa_summary.json"
)

RESOURCE_PATH = (
    RUN_DIR
    / "resource_usage.txt"
)


def parse_resource_file(
    path: Path,
) -> dict[str, object]:
    result = {}

    if not path.exists():
        return result

    for raw_line in path.read_text(
        encoding="utf-8"
    ).splitlines():
        if ":" not in raw_line:
            continue

        key, raw_value = raw_line.split(
            ":",
            1,
        )

        key = key.strip()
        value = raw_value.strip()

        try:
            if "." in value:
                parsed = float(value)
            else:
                parsed = int(value)
        except ValueError:
            parsed = value

        result[key] = parsed

    return result


def main() -> None:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    metadata = json.loads(
        METADATA_PATH.read_text(
            encoding="utf-8"
        )
    )

    qa = json.loads(
        QA_PATH.read_text(
            encoding="utf-8"
        )
    )

    resources = parse_resource_file(
        RESOURCE_PATH
    )

    assert (
        metadata["processed_documents"]
        == 227628
    )

    assert (
        metadata["chunks_written"]
        == 1334973
    )

    assert (
        metadata["failed_documents"]
        == 0
    )

    assert (
        qa["documents_checked"]
        == 227628
    )

    assert (
        qa["chunks_checked"]
        == 1334973
    )

    output_files = metadata[
        "output_files"
    ]

    assert len(output_files) == 1

    chunk_path = Path(
        output_files[0]
    )

    assert chunk_path.exists()

    documents = int(
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

    evidence = {
        "schema_version": 1,
        "evidence_class": (
            "week2_scaled_engineering_run"
        ),
        "run_directory": str(
            RUN_DIR
        ),
        "method": metadata[
            "method"
        ],
        "configuration": metadata[
            "configuration"
        ],
        "status": metadata[
            "status"
        ],
        "processed_documents":
            documents,
        "failed_documents":
            metadata[
                "failed_documents"
            ],
        "chunks_written":
            chunks,
        "elapsed_seconds":
            elapsed,
        "seconds_per_document":
            elapsed / documents,
        "documents_per_second":
            documents / elapsed,
        "chunks_per_second":
            chunks / elapsed,
        "chunk_output_file":
            str(chunk_path),
        "chunk_output_bytes":
            chunk_path.stat().st_size,
        "qa": qa,
        "resource_measurement": {
            "source":
                str(RESOURCE_PATH),
            "values":
                resources,
        },
        "memory_note": (
            "max_rss_kb is reported "
            "exactly as recorded by the "
            "existing resource_usage.txt; "
            "it is not extrapolated to "
            "other methods or runs."
        ),
    }

    json_path = (
        OUTPUT_DIR
        / "scaled_engineering_evidence.json"
    )

    md_path = (
        OUTPUT_DIR
        / "scaled_engineering_evidence.md"
    )

    json_path.write_text(
        json.dumps(
            evidence,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Issue 17 Scaled Engineering Evidence",
        "",
        "## Week 2 TokenChunker Run",
        "",
        f"- Status: `{metadata['status']}`",
        (
            "- Processed documents: "
            f"{documents:,}"
        ),
        (
            "- Generated chunks: "
            f"{chunks:,}"
        ),
        (
            "- Processing failures: "
            f"{metadata['failed_documents']}"
        ),
        (
            "- Pipeline elapsed seconds: "
            f"{elapsed:.6f}"
        ),
        (
            "- Derived seconds/document: "
            f"{elapsed / documents:.9f}"
        ),
        (
            "- Derived documents/second: "
            f"{documents / elapsed:.3f}"
        ),
        (
            "- Derived chunks/second: "
            f"{chunks / elapsed:.3f}"
        ),
        (
            "- Chunk output bytes: "
            f"{chunk_path.stat().st_size}"
        ),
        "",
        "## Streaming QA",
        "",
    ]

    for key in sorted(qa):
        lines.append(
            f"- `{key}`: "
            f"`{qa[key]}`"
        )

    lines.extend(
        [
            "",
            "## Recorded Resource Evidence",
            "",
        ]
    )

    if resources:
        for key in sorted(resources):
            lines.append(
                f"- `{key}`: "
                f"`{resources[key]}`"
            )
    else:
        lines.append(
            "- No resource_usage.txt "
            "measurements were found."
        )

    lines.extend(
        [
            "",
            (
                "Resource measurements apply "
                "only to this scaled TokenChunker "
                "run and are not extrapolated."
            ),
            "",
        ]
    )

    md_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(
        "Processed documents:",
        documents,
    )
    print(
        "Chunks:",
        chunks,
    )
    print(
        "Failures:",
        metadata[
            "failed_documents"
        ],
    )
    print(
        "Elapsed:",
        f"{elapsed:.6f}",
    )
    print(
        "Documents/s:",
        f"{documents / elapsed:.3f}",
    )
    print(
        "Chunks/s:",
        f"{chunks / elapsed:.3f}",
    )
    print(
        "Output bytes:",
        chunk_path.stat().st_size,
    )
    print(
        "QA status:",
        qa.get("status"),
    )
    print(
        "Recorded max_rss_kb:",
        resources.get(
            "max_rss_kb"
        ),
    )
    print()
    print(
        "ISSUE #17 SCALED ENGINEERING "
        "EVIDENCE: PASS"
    )


if __name__ == "__main__":
    main()
