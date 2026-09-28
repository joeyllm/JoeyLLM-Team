# Chunk Provenance Schema

## Goal

Every generated chunk must be traceable to the exact source document and the configuration that produced it.

## Source Identity

Each chunk must record:

- `source_file`
- `source_row_number`
- `document_id`

These fields identify the original source document.

## Source Metadata

Where available from the frozen dataset, preserve:

- `source_dump`
- `source_url`
- `source_date`
- `source_file_path`
- `source_language`
- `source_language_score`
- `source_token_count`
- `source_hash`
- `source_simhash`

Source metadata must be copied from the original document and must not be recomputed by the chunking pipeline.

## Chunking Metadata

Each chunk must record:

- `method`
- `chunker_config`

These fields identify the chunking method and exact configuration used.

## Chunk Identity and Location

Each chunk must record:

- `chunk_index`
- `start_index`
- `end_index`
- `token_count`
- `char_length`
- `text`

`chunk_index` is stable within one source document and one chunking run.

`start_index` and `end_index` refer to positions in the original source text.

## Representative Samples

When processing `representative_samples.parquet`, provenance from the original frozen dataset must be preserved rather than replacing it with the representative-sample container filename and row number.

## Validation Requirement

A sampled output chunk must be traceable back to:

1. the original source Parquet file;
2. the original source row;
3. the source document ID;
4. the corresponding source text range;
5. the chunking method and configuration.

## Status

Chunk provenance contract defined.
