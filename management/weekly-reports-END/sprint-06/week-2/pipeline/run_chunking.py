from __future__ import annotations

import argparse
import glob
import json
import re
import sys
import time
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from chonkie import RecursiveChunker, SemanticChunker, TokenChunker


OUTPUT_SCHEMA = pa.schema(
    [
        ("input_file", pa.large_string()),
        ("source_file", pa.large_string()),
        ("source_row_number", pa.int64()),
        ("document_id", pa.large_string()),

        ("source_dump", pa.large_string()),
        ("source_url", pa.large_string()),
        ("source_date", pa.large_string()),
        ("source_file_path", pa.large_string()),
        ("source_language", pa.large_string()),
        ("source_language_score", pa.float64()),
        ("source_token_count", pa.int64()),
        ("source_hash", pa.large_string()),
        ("source_simhash", pa.uint64()),

        ("source_char_length", pa.int64()),
        ("source_newline_count", pa.int64()),
        ("source_chars_per_stored_token", pa.float64()),
        ("sample_groups", pa.large_string()),

        ("method", pa.string()),
        ("chunker_config", pa.large_string()),

        ("chunk_index", pa.int64()),
        ("start_index", pa.int64()),
        ("end_index", pa.int64()),
        ("token_count", pa.int64()),
        ("char_length", pa.int64()),
        ("text", pa.large_string()),
    ]
)


SOURCE_COLUMNS = [
    "id",
    "text",

    "source_file",
    "file_row_number",

    "dump",
    "url",
    "date",
    "file_path",
    "language",
    "language_score",
    "token_count",
    "hash",
    "simhash",

    "char_length",
    "newline_count",
    "chars_per_stored_token",
    "sample_groups",
]


def natural_key(path: str):
    return [
        int(piece) if piece.isdigit() else piece
        for piece in re.split(r"(\d+)", Path(path).name)
    ]


def resolve_inputs(pattern: str) -> list[Path]:
    paths = [
        Path(path).resolve()
        for path in sorted(glob.glob(pattern), key=natural_key)
    ]

    if not paths:
        raise FileNotFoundError(
            f"No input Parquet files matched: {pattern}"
        )

    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(path)

    return paths


def get_value(data, name, offset):
    column = data.get(name)

    if column is None:
        return None

    return column[offset]


def build_chunker(args):
    if args.method == "token":
        config = {
            "tokenizer": args.tokenizer,
            "chunk_size": args.chunk_size,
            "chunk_overlap": args.chunk_overlap,
        }

        chunker = TokenChunker(
            tokenizer=args.tokenizer,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
        )

    elif args.method == "recursive":
        config = {
            "tokenizer": args.tokenizer,
            "chunk_size": args.chunk_size,
            "min_characters_per_chunk": (
                args.min_characters_per_chunk
            ),
        }

        chunker = RecursiveChunker(
            tokenizer=args.tokenizer,
            chunk_size=args.chunk_size,
            min_characters_per_chunk=(
                args.min_characters_per_chunk
            ),
        )

    elif args.method == "semantic":
        config = {
            "embedding_model": args.embedding_model,
            "threshold": args.threshold,
            "chunk_size": args.chunk_size,
        }

        chunker = SemanticChunker(
            embedding_model=args.embedding_model,
            threshold=args.threshold,
            chunk_size=args.chunk_size,
        )

    else:
        raise ValueError(
            f"Unsupported method: {args.method}"
        )

    return chunker, config


def flush_rows(writer, rows):
    if not rows:
        return

    table = pa.Table.from_pylist(
        rows,
        schema=OUTPUT_SCHEMA,
    )

    writer.write_table(table)
    rows.clear()


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Configurable provenance-aware "
            "Chonkie batch chunking pipeline."
        )
    )

    parser.add_argument(
        "--input",
        required=True,
    )
    parser.add_argument(
        "--output-dir",
        required=True,
    )
    parser.add_argument(
        "--method",
        required=True,
        choices=[
            "token",
            "recursive",
            "semantic",
        ],
    )

    parser.add_argument(
        "--chunk-size",
        type=int,
        default=2048,
    )
    parser.add_argument(
        "--tokenizer",
        default="character",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=0,
    )
    parser.add_argument(
        "--min-characters-per-chunk",
        type=int,
        default=24,
    )
    parser.add_argument(
        "--embedding-model",
        default="minishlab/potion-base-32M",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.8,
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=256,
    )
    parser.add_argument(
        "--write-buffer-size",
        type=int,
        default=5000,
    )
    parser.add_argument(
        "--max-documents",
        type=int,
        default=None,
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=100,
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
    )

    args = parser.parse_args()

    if args.chunk_size <= 0:
        raise ValueError(
            "--chunk-size must be positive"
        )

    if args.batch_size <= 0:
        raise ValueError(
            "--batch-size must be positive"
        )

    if args.write_buffer_size <= 0:
        raise ValueError(
            "--write-buffer-size must be positive"
        )

    if (
        args.max_documents is not None
        and args.max_documents <= 0
    ):
        raise ValueError(
            "--max-documents must be positive"
        )

    input_paths = resolve_inputs(args.input)

    output_dir = Path(
        args.output_dir
    ).resolve()

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    chunker, config = build_chunker(args)

    config_json = json.dumps(
        config,
        sort_keys=True,
        separators=(",", ":"),
    )

    total_input_rows = sum(
        pq.ParquetFile(path).metadata.num_rows
        for path in input_paths
    )

    target_documents = total_input_rows

    if args.max_documents is not None:
        target_documents = min(
            target_documents,
            args.max_documents,
        )

    run_start = time.perf_counter()

    processed_documents = 0
    failed_documents = 0
    chunks_written = 0
    output_files = []

    print("=" * 72)
    print("CHONKIE BATCH PIPELINE")
    print(f"Method: {args.method}")
    print(f"Input files: {len(input_paths)}")
    print(
        f"Input rows available: "
        f"{total_input_rows}"
    )
    print(
        f"Documents targeted: "
        f"{target_documents}"
    )
    print(
        f"Output directory: "
        f"{output_dir}"
    )
    print(
        f"Configuration: "
        f"{config_json}"
    )
    print("=" * 72)

    stop_requested = False

    for file_number, input_path in enumerate(
        input_paths,
        start=1,
    ):
        if stop_requested:
            break

        parquet_file = pq.ParquetFile(
            input_path
        )

        available_columns = set(
            parquet_file.schema_arrow.names
        )

        required_columns = {
            "id",
            "text",
        }

        missing_columns = (
            required_columns
            - available_columns
        )

        if missing_columns:
            raise RuntimeError(
                f"{input_path} is missing "
                f"required columns: "
                f"{sorted(missing_columns)}"
            )

        read_columns = [
            name
            for name in SOURCE_COLUMNS
            if name in available_columns
        ]

        output_path = (
            output_dir
            / f"{input_path.stem}.chunks.parquet"
        )

        temporary_path = Path(
            str(output_path) + ".tmp"
        )

        if (
            output_path.exists()
            and not args.overwrite
        ):
            raise FileExistsError(
                f"Output already exists: "
                f"{output_path}. "
                "Use --overwrite to replace it."
            )

        if temporary_path.exists():
            temporary_path.unlink()

        print()
        print(
            f"[FILE {file_number}/"
            f"{len(input_paths)}] "
            f"{input_path}"
        )
        print(
            "Source columns: "
            + ", ".join(read_columns)
        )

        writer = pq.ParquetWriter(
            temporary_path,
            OUTPUT_SCHEMA,
            compression="zstd",
        )

        row_buffer = []
        source_row_number = 0

        try:
            for batch in parquet_file.iter_batches(
                batch_size=args.batch_size,
                columns=read_columns,
            ):
                data = batch.to_pydict()

                ids = data["id"]
                texts = data["text"]

                for offset, text in enumerate(
                    texts
                ):
                    if (
                        args.max_documents
                        is not None
                        and processed_documents
                        >= args.max_documents
                    ):
                        stop_requested = True
                        break

                    document_id = ids[offset]

                    container_row_number = (
                        source_row_number
                        + offset
                    )

                    preserved_source_file = (
                        get_value(
                            data,
                            "source_file",
                            offset,
                        )
                    )

                    if (
                        preserved_source_file
                        is None
                    ):
                        preserved_source_file = (
                            input_path.name
                        )

                    preserved_source_row = (
                        get_value(
                            data,
                            "file_row_number",
                            offset,
                        )
                    )

                    if (
                        preserved_source_row
                        is None
                    ):
                        preserved_source_row = (
                            container_row_number
                        )

                    try:
                        if text is None:
                            raise ValueError(
                                "Source text is null"
                            )

                        chunks = chunker.chunk(
                            text
                        )

                        for (
                            chunk_index,
                            chunk,
                        ) in enumerate(chunks):
                            row_buffer.append(
                                {
                                    "input_file": (
                                        input_path.name
                                    ),
                                    "source_file": (
                                        preserved_source_file
                                    ),
                                    "source_row_number": (
                                        preserved_source_row
                                    ),
                                    "document_id": (
                                        document_id
                                    ),

                                    "source_dump": (
                                        get_value(
                                            data,
                                            "dump",
                                            offset,
                                        )
                                    ),
                                    "source_url": (
                                        get_value(
                                            data,
                                            "url",
                                            offset,
                                        )
                                    ),
                                    "source_date": (
                                        get_value(
                                            data,
                                            "date",
                                            offset,
                                        )
                                    ),
                                    "source_file_path": (
                                        get_value(
                                            data,
                                            "file_path",
                                            offset,
                                        )
                                    ),
                                    "source_language": (
                                        get_value(
                                            data,
                                            "language",
                                            offset,
                                        )
                                    ),
                                    "source_language_score": (
                                        get_value(
                                            data,
                                            "language_score",
                                            offset,
                                        )
                                    ),
                                    "source_token_count": (
                                        get_value(
                                            data,
                                            "token_count",
                                            offset,
                                        )
                                    ),
                                    "source_hash": (
                                        get_value(
                                            data,
                                            "hash",
                                            offset,
                                        )
                                    ),
                                    "source_simhash": (
                                        get_value(
                                            data,
                                            "simhash",
                                            offset,
                                        )
                                    ),

                                    "source_char_length": (
                                        get_value(
                                            data,
                                            "char_length",
                                            offset,
                                        )
                                    ),
                                    "source_newline_count": (
                                        get_value(
                                            data,
                                            "newline_count",
                                            offset,
                                        )
                                    ),
                                    "source_chars_per_stored_token": (
                                        get_value(
                                            data,
                                            "chars_per_stored_token",
                                            offset,
                                        )
                                    ),
                                    "sample_groups": (
                                        get_value(
                                            data,
                                            "sample_groups",
                                            offset,
                                        )
                                    ),

                                    "method": (
                                        args.method
                                    ),
                                    "chunker_config": (
                                        config_json
                                    ),

                                    "chunk_index": (
                                        chunk_index
                                    ),
                                    "start_index": (
                                        chunk.start_index
                                    ),
                                    "end_index": (
                                        chunk.end_index
                                    ),
                                    "token_count": (
                                        chunk.token_count
                                    ),
                                    "char_length": (
                                        len(chunk.text)
                                    ),
                                    "text": (
                                        chunk.text
                                    ),
                                }
                            )

                            chunks_written += 1

                        processed_documents += 1

                    except Exception as exc:
                        processed_documents += 1
                        failed_documents += 1

                        print(
                            "DOCUMENT FAILURE | "
                            f"source_file="
                            f"{preserved_source_file} | "
                            f"source_row="
                            f"{preserved_source_row} | "
                            f"error={exc!r}"
                        )

                    if (
                        len(row_buffer)
                        >= args.write_buffer_size
                    ):
                        flush_rows(
                            writer,
                            row_buffer,
                        )

                    if (
                        processed_documents
                        % args.progress_every
                        == 0
                        or processed_documents
                        == target_documents
                    ):
                        elapsed = (
                            time.perf_counter()
                            - run_start
                        )

                        print(
                            f"[{processed_documents}/"
                            f"{target_documents}] "
                            f"chunks="
                            f"{chunks_written} | "
                            f"failures="
                            f"{failed_documents} | "
                            f"elapsed="
                            f"{elapsed:.2f}s"
                        )

                source_row_number += len(
                    texts
                )

                if stop_requested:
                    break

            flush_rows(
                writer,
                row_buffer,
            )

        finally:
            writer.close()

        if output_path.exists():
            if args.overwrite:
                output_path.unlink()
            else:
                raise FileExistsError(
                    output_path
                )

        temporary_path.replace(
            output_path
        )

        output_files.append(
            str(output_path)
        )

        print(
            f"Output: {output_path}"
        )

    elapsed = (
        time.perf_counter()
        - run_start
    )

    status = (
        "completed"
        if failed_documents == 0
        else "completed_with_failures"
    )

    metadata = {
        "status": status,
        "method": args.method,
        "configuration": config,
        "input_pattern": args.input,
        "input_files": [
            str(path)
            for path in input_paths
        ],
        "input_file_count": (
            len(input_paths)
        ),
        "input_rows_available": (
            total_input_rows
        ),
        "max_documents": (
            args.max_documents
        ),
        "processed_documents": (
            processed_documents
        ),
        "failed_documents": (
            failed_documents
        ),
        "chunks_written": (
            chunks_written
        ),
        "elapsed_seconds": elapsed,
        "output_files": output_files,
        "output_schema_fields": (
            OUTPUT_SCHEMA.names
        ),
        "source_identity_policy": {
            "representative_samples": (
                "Preserve source_file and "
                "file_row_number from input."
            ),
            "frozen_dataset": (
                "Use input Parquet filename "
                "and zero-based row number."
            ),
        },
        "python_executable": (
            sys.executable
        ),
        "command": sys.argv,
    }

    metadata_path = (
        output_dir
        / "run_metadata.json"
    )

    metadata_path.write_text(
        json.dumps(
            metadata,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print()
    print("=" * 72)
    print("RUN COMPLETE")
    print(f"Status: {status}")
    print(
        "Documents: "
        f"{processed_documents}/"
        f"{target_documents}"
    )
    print(
        f"Failures: "
        f"{failed_documents}"
    )
    print(
        f"Chunks: "
        f"{chunks_written}"
    )
    print(
        f"Elapsed: "
        f"{elapsed:.2f}s"
    )
    print(
        f"Metadata: "
        f"{metadata_path}"
    )
    print("=" * 72)


if __name__ == "__main__":
    main()
