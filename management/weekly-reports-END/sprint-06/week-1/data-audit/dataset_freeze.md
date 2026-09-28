# Dataset Freeze Record

## Purpose

This dataset is the fixed input for the 3-week chunking sprint.

## Dataset

- Path: `/home/jovyan/hash_output/part_*.parquet`
- Format: Parquet
- File count: 57
- Row count: 6,008,596
- Total size: 26,791,040,341 bytes

## Schema

| Field | Type |
|---|---|
| text | large_string |
| id | large_string |
| dump | large_string |
| url | large_string |
| date | large_string |
| file_path | large_string |
| language | large_string |
| language_score | double |
| token_count | int64 |
| hash | large_string |
| simhash | uint64 |

All 57 Parquet files use the same schema.

The text field used for the chunking stage is `text`.

## Provenance

- Previous input dataset: `/data/joeyllm_data/AUTokens50_with_hash_simhash`
- Previous input rows: 21,087,435
- Deduplicated output rows: 6,008,596
- Duplicate rows removed: 15,078,839
- Deduplication status: Completed
- Deduplication contract validation: Pass
- Remaining duplicate hash groups: 0

## Integrity

- SHA256 manifest: `/home/jovyan/hash_output/_audit/chunking_input_sha256_manifest.txt`
- SHA256 verification record: `/home/jovyan/hash_output/_audit/chunking_input_sha256_check.txt`
- Verified files: 57/57

## Validation Environment

- Python executable: `/opt/conda/bin/python`
- Python version: 3.13.15
- PyArrow version: 25.0.0

## Freeze Policy

The dataset must not be modified in place during the chunking sprint.

All Week 1, Week 2, and Week 3 chunking experiments must use this frozen dataset as input.

All chunking outputs must be written to a separate location.

Any modification to the frozen dataset requires a new dataset version and a new freeze record.
