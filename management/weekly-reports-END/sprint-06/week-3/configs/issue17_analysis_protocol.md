# Issue 17 Robustness and Computational-Cost Analysis Protocol

## Objective

Evaluate the robustness and operational behaviour of the frozen
matched-granularity TokenChunker, RecursiveChunker, and SemanticChunker
configurations.

This issue does not assign an overall chunk-quality ranking.

## Primary Configurations

Reuse the frozen Issue 16 matched settings:

- TokenChunker: `token_cal_cs839`
- RecursiveChunker: `recursive_cal_cs1025`
- SemanticChunker: `semantic_cal_th030`

No configuration is changed for the primary robustness analysis.

## Representative Sample

Use the same frozen 32-document representative sample used in Issue 16.

The analysis covers all representative sample groups:

- high_chars_per_token
- length_max
- length_median
- length_min
- length_p05
- length_p90
- length_p95
- length_p99
- low_chars_per_token
- no_newline

Groups are not mutually exclusive where the frozen sample assigns more
than one group to a source document.

## Robustness Metrics

For each method and representative group, record where available:

- document count
- chunk count
- mean chunks per document
- median chunk character length
- mean chunk character length
- very-small-chunk frequency
- internal boundary-class distribution
- failures
- warnings

## Small-Chunk Definition

Reuse the definition frozen before the Issue 16 matched comparison:

`char_length < 256`

The definition must not be changed after inspecting Issue 17 results.

## Long-Document Analysis

Explicitly analyze:

- `length_p95`
- `length_p99`
- `length_max`

Compare their observed granularity and fragmentation with the other
representative groups.

Runtime behaviour for long documents must only be reported when actual
timing measurements exist.

## Computational Cost

Record measured evidence for:

- total runtime
- runtime per document when measured or directly derivable
- documents per second
- chunks per second
- chunk-output size
- warnings
- failures

## Memory Evidence

Memory use may only be reported if an existing run or a new controlled
measurement explicitly recorded a memory metric.

Memory use must not be estimated, inferred from file size, or fabricated.

## Scaled Engineering Evidence

Incorporate the existing Week 2 TokenChunker scaled run.

Expected identifying evidence from the project history is:

- 227,628 processed documents
- 1,334,973 generated chunks
- 0 processing failures
- full streaming QA pass

The exact artifact paths and metadata must be located and verified
before these values are copied into the final Issue 17 results.

No full-dataset rerun is required unless the existing evidence cannot be
verified.

## Runtime Interpretation

Existing single-run elapsed times are descriptive measurements.

Do not claim statistically stable runtime differences from single-run
timings.

If additional timing experiments are required for long-document
behaviour, their protocol must be documented before execution.

## Evidence Separation

The final report must distinguish:

1. directly measured evidence
2. derived arithmetic quantities
3. interpretation

Computational cost alone must not be interpreted as chunk quality.

## Limitations

The final analysis must document:

- representative-group sample sizes
- group overlap
- aggregate matching does not imply subgroup matching
- tokenizer differences
- absence of memory evidence where applicable
- limitations of single-run runtime measurements
- limits on generalizing from the 32-document sample
