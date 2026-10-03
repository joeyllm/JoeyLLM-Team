# Week 3 Evaluation Metric Specification

## Purpose

This document freezes the metric definitions used by the Week 3
evaluation aggregator.

All Week 3 experimental runs must use the same definitions unless a
change is explicitly documented.

## Input Sources

The aggregator reads:

1. one `.chunks.parquet` output
2. the corresponding `run_metadata.json`
3. the corresponding `pipeline.stderr.log` when available
4. QA summary files when available

## Document Identity

A source document is identified using:

- `source_file`
- `source_row_number`
- `document_id`

The aggregator must not infer document identity from chunk text.

## Run-Level Metrics

For each run, report:

- method
- configuration
- processed documents
- failed documents
- total chunks
- elapsed seconds
- documents per second
- chunks per second
- warning count
- QA status when available

## Chunks Per Document

For each document, count the number of generated chunks.

Report:

- minimum
- mean
- median
- P90
- P95
- P99
- maximum

## Chunk Character Length

Use the existing `char_length` field.

Report:

- minimum
- mean
- median
- P90
- P95
- P99
- maximum

The aggregator must verify that:

`char_length == len(text)`

before using the value in final statistics.

## Chunk Token Count

Use the existing chunk-level `token_count` field.

Report:

- minimum
- mean
- median
- P90
- P95
- P99
- maximum

This value is distinct from:

`source_token_count`

which is the stored token count of the original source document.

The two fields must not be mixed.

## Boundary Classification

Boundary behaviour is classified using the end of each chunk.

Classification precedence is fixed as follows.

### 1. document_end

If:

`end_index == source_char_length`

the chunk is classified as:

`document_end`

This represents the natural end of the source document rather than an
internal chunking decision.

### 2. paragraph_boundary

For a non-final chunk, classify as `paragraph_boundary` if the chunk
text ends with:

- `\n\n`
- `\r\n\r\n`

### 3. newline_boundary

For a non-final chunk, classify as `newline_boundary` if the chunk text
ends with:

- `\n`
- `\r`

### 4. sentence_boundary

For a non-final chunk, remove trailing horizontal whitespace
(space and tab only).

Classify as `sentence_boundary` if the remaining text ends with one of:

- `.`
- `!`
- `?`

Sentence-ending punctuation followed by common closing quote or bracket
characters should also be treated as a sentence boundary.

### 5. whitespace_boundary

For a non-final chunk, classify as `whitespace_boundary` if the final
character is whitespace and none of the higher-priority rules matched.

### 6. other_boundary

All remaining non-final chunk boundaries are classified as:

`other_boundary`

## Boundary Percentages

Report:

1. counts across all chunks
2. percentages across all chunks
3. percentages across internal boundaries only

`document_end` must be excluded from the internal-boundary denominator.

This avoids treating the unavoidable final boundary of every document
as evidence about chunker boundary behaviour.

## Representative Sample Groups

The `sample_groups` field may contain multiple comma-separated group
names.

Example:

`length_min,low_chars_per_token`

The aggregator must:

1. split on commas
2. trim surrounding whitespace
3. ignore empty components
4. retain membership in every listed group

A document may therefore contribute to more than one group.

Group-level statistics should report:

- documents
- chunks
- mean chunks per document
- median chunk character length
- mean chunk character length
- boundary distribution
- failures or warnings when attributable

Overlapping groups must not be summed to estimate the total number of
unique documents.

## Percentiles

Use deterministic linear percentile interpolation.

The same percentile implementation must be used for every run.

Report:

- P90
- P95
- P99

## Missing Values

The aggregator must not silently replace missing values with invented
defaults.

If a required metric field is missing, the run must report the problem.

Optional source metadata may remain null.

## Warning Handling

Warnings are distinct from hard failures.

Warning counts must not change a successful run into a failed run unless
the existing QA logic classifies the event as a hard failure.

## Output Formats

Each evaluated run must produce:

- JSON summary
- CSV summary
- Markdown report

The three outputs must be generated from the same in-memory metric
results.

## Interpretation Rule

The aggregator produces descriptive measurements.

It must not:

- rank methods
- assign quality scores
- declare a method superior
- interpret raw chunk count as quality

Interpretation is performed separately in later Week 3 issues.

## Status

Week 3 metric definitions frozen.
