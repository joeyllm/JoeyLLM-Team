# Issue 6 - Week 1 Experiment Protocol

## Objective

Freeze the experimental setup that will be used for the Week 2 controlled chunking experiments.

## 1. Frozen Input Dataset

Primary dataset:

`/home/jovyan/hash_output/part_*.parquet`

Dataset properties:

- Files: 57
- Rows: 6,008,596
- Text field: `text`
- Exact-hash duplicates remaining: 0
- Frozen input must not be modified in place

Representative prototype dataset:

`/home/jovyan/hash_output/_audit/profiling/representative_samples.parquet`

- Representative documents: 32
- Includes typical and extreme document cases

## 2. Environment

Project directory:

`/home/jovyan/chunking_sprint`

Environment:

- Python 3.13.15
- Chonkie 1.7.0
- Model2Vec 0.9.0
- PyArrow 25.0.0

Dependencies are recorded in:

- `requirements.txt`
- `requirements-lock.txt`

## 3. Chunking Methods

### TokenChunker

- tokenizer: `character`
- chunk_size: `2048`
- chunk_overlap: `0`

### RecursiveChunker

- tokenizer: `character`
- chunk_size: `2048`

### SemanticChunker

- embedding_model: `minishlab/potion-base-32M`
- threshold: `0.8`
- chunk_size: `2048`
- embedding execution: local Model2Vec

## 4. Prototype Evidence

The three methods were tested on all 32 representative documents.

- Total runs: 96
- Successful runs: 96
- Failed runs: 0
- Invalid index ranges: 0
- Source-slice mismatches: 0

Prototype artifacts:

- `prototypes/full/prototype.log`
- `prototypes/full/prototype_summary.csv`
- `prototypes/full/prototype_chunks.parquet`
- `prototypes/full/prototype_report.md`

## 5. Evaluation Metrics

Controlled experiments will evaluate:

1. Output validity
2. Chunk granularity
3. Boundary behaviour
4. Runtime and computational cost
5. Robustness across document types

Metric definitions are recorded in:

`evaluation_metrics.md`

## 6. Experimental Procedure

For each selected document:

1. Load the original `text`.
2. Run each configured chunking method.
3. Preserve source document provenance.
4. Record chunk text, start index, end index, token count, and character length.
5. Validate that chunk indices map back to the original source text.
6. Record runtime and failures.
7. Aggregate results by method and document group.
8. Compare boundary behaviour and chunk-size distributions using the defined metrics.

## 7. Comparison Constraint

The current prototype settings do not provide directly equivalent chunk-size budgets.

TokenChunker and RecursiveChunker use the character tokenizer, while SemanticChunker uses the tokenizer associated with the Model2Vec embedding model.

Therefore:

- prototype chunk counts must not be interpreted as a direct quality ranking;
- controlled experiments should align comparison settings where possible;
- any remaining tokenizer difference must be explicitly reported.

## 8. Robustness Groups

The representative set includes cases covering:

- short documents
- median-length documents
- P90/P95/P99 documents
- extreme-length documents
- documents without newlines
- high chars/token cases
- low chars/token cases

Results should be reported separately where these groups show materially different behaviour.

## 9. Retrieval Evaluation

Retrieval-quality evaluation may be added if a suitable query set or relevance labels become available.

It is not required for the initial controlled chunking comparison.

## 10. Reproducibility Rules

- Do not modify the frozen source dataset.
- Store experimental outputs separately.
- Record all parameter changes.
- Pin dependency versions.
- Preserve source-file and row provenance.
- Validate chunk-to-source mappings.
- Record warnings and failures rather than silently discarding them.

## 11. Cost

The current TokenChunker, RecursiveChunker, and SemanticChunker pipeline uses no paid model API.

Semantic embeddings are produced locally with Model2Vec.

## Status

Week 1 chunking experiment protocol finalized.
