# Issue 17 Long-Document Runtime Protocol

## Objective

Measure descriptive runtime behaviour separately for the frozen
representative groups:

- length_p95
- length_p99
- length_max

The purpose is to determine whether operational behaviour changes across
increasingly long representative inputs.

## Input

Start from the frozen 32-document representative sample.

Create one input Parquet for each target group.

Group membership is determined by exact comma-separated membership in
`sample_groups`.

Documents may occur in more than one group if the frozen representative
sample assigns overlapping labels. Group overlap must be reported rather
than removed.

The union of the three target groups must match the already frozen
9-document long-document subset.

## Methods

Use the Issue 16 matched configurations exactly.

### TokenChunker

- chunk_size = 839
- tokenizer = character
- chunk_overlap = 0

### RecursiveChunker

- chunk_size = 1025
- tokenizer = character
- min_characters_per_chunk = 24

### SemanticChunker

- chunk_size = 2048
- embedding_model = minishlab/potion-base-32M
- threshold = 0.30

## Runs

Execute exactly nine controlled runs:

- length_p95 × token
- length_p95 × recursive
- length_p95 × semantic
- length_p99 × token
- length_p99 × recursive
- length_p99 × semantic
- length_max × token
- length_max × recursive
- length_max × semantic

Each run uses the existing batch pipeline and automated chunk QA.

No runtime repetition is required. These measurements are descriptive
single-run engineering evidence rather than statistically stable
benchmarks.

## Runtime Metrics

For each run record:

- input documents
- input total characters
- generated chunks
- elapsed seconds
- seconds per document
- documents per second
- chunks per second
- output Parquet bytes
- failures
- warning count
- QA status

## Interpretation

Pipeline runtime includes batch-level overhead such as initialization
and I/O.

In particular, SemanticChunker timing includes local embedding-model
initialization within each pipeline invocation.

Therefore seconds/document must not be interpreted as pure algorithmic
per-document compute time.

Computational cost must remain separate from chunk-quality conclusions.

## Memory

Do not infer memory use for these runs.

The directly measured Week 2 scaled TokenChunker resource evidence is
reported separately.
