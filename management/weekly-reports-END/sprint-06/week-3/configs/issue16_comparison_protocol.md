# Issue 16 Matched-Granularity Comparison Protocol

## Compared Runs

The comparison uses the frozen matched settings from:

`issue16_matched_settings.json`

No additional chunking runs are required for the primary comparison.

## Same-Document Requirement

All three runs must contain the same frozen 32 representative source
documents.

## Granularity Metrics

Compare:

- total chunks
- chunks per document
- character-length distribution
- token-count distribution

Chunk-level token counts are reported as pipeline outputs, but they must
not be treated as directly equivalent across methods because tokenizer
semantics differ.

## Boundary Metrics

Compare internal-boundary proportions for:

- paragraph_boundary
- newline_boundary
- sentence_boundary
- whitespace_boundary
- other_boundary

`document_end` is excluded from the internal-boundary denominator.

## Fragmentation Metric

A small chunk is frozen as:

`char_length < 256`

The threshold is defined before inspecting matched-run small-chunk
counts.

Report:

- small-chunk count
- small-chunk percentage

The same absolute character threshold is used for all three methods.

## Robustness

Compare matched-run behaviour across every representative
`sample_groups` category.

For each method and group, report:

- documents
- chunks
- mean chunks per document
- median chunk character length
- mean chunk character length
- boundary distribution

## Reliability

Report:

- failed documents
- QA status
- QA hard failures
- warning count
- warning text when present

Warnings remain distinct from hard failures.

## Efficiency

Report:

- elapsed seconds
- documents per second
- chunks per second
- chunk Parquet output size in bytes

## Interpretation

Measurements are descriptive.

The comparison must not:

- assign an overall quality score
- rank methods overall
- treat one metric as overall quality
- treat tokenizer-specific token counts as directly equivalent

Observed evidence and interpretation must be separated explicitly.
