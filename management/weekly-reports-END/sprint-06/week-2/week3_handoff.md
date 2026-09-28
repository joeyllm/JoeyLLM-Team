# Week 3 - Evaluation Handoff

## Objective

Freeze the inputs, configurations, evidence, and constraints required for Week 3 controlled chunking experiments and evaluation.

## 1. Frozen Source Dataset

Primary frozen dataset:

`/home/jovyan/hash_output/part_*.parquet`

Dataset:

- 57 Parquet files
- 6,008,596 documents
- approximately 25 GB
- exact-hash duplicate groups remaining: 0
- SHA256-verified
- immutable during chunking experiments

Text field:

`text`

## 2. Representative Evaluation Set

Representative documents:

`/home/jovyan/hash_output/_audit/profiling/representative_samples.parquet`

Documents:

32

The set includes:

- short documents
- median-length documents
- P90 documents
- P95 documents
- P99 documents
- extreme-length documents
- no-newline documents
- high chars/token cases
- low chars/token cases

## 3. Reproducible Environment

- Python 3.13.15
- Chonkie 1.7.0
- Model2Vec 0.9.0
- PyArrow 25.0.0

Dependency files:

- `requirements.txt`
- `requirements-lock.txt`

## 4. Chunking Pipeline

Main pipeline:

`pipeline/run_chunking.py`

Automated QA:

`pipeline/validate_chunks.py`

Scaled QA:

`pipeline/validate_scaled_part.py`

Week 1 consistency validation:

`pipeline/check_week1_consistency.py`

## 5. Current Chunking Configurations

### TokenChunker

- tokenizer: `character`
- chunk_size: `2048`
- chunk_overlap: `0`

### RecursiveChunker

- tokenizer: `character`
- chunk_size: `2048`
- min_characters_per_chunk: `24`

### SemanticChunker

- embedding_model: `minishlab/potion-base-32M`
- threshold: `0.8`
- chunk_size: `2048`

Semantic embeddings are executed locally with Model2Vec.

No paid model API is required.

## 6. Evaluation Metrics

Metrics are defined in:

`evaluation_metrics.md`

The main dimensions are:

1. output validity
2. chunk granularity
3. boundary behaviour
4. runtime and computational cost
5. robustness across document types

Retrieval evaluation may be added if suitable queries or relevance labels become available.

## 7. Week 2 Validated Outputs

Representative validation outputs:

- `runs/issue10_token/`
- `runs/issue10_recursive/`
- `runs/issue10_semantic/`

Scaled TokenChunker evidence:

- `runs/issue11_token_10k/`
- `runs/issue11_token_part0/`

## 8. Week 3 Comparison Constraint

Raw chunk counts from the current prototype must not be interpreted as direct method-quality results.

TokenChunker and RecursiveChunker use a character tokenizer, while SemanticChunker uses the tokenizer associated with the Model2Vec embedding model.

Week 3 must either:

1. align comparison budgets where technically appropriate; or
2. explicitly preserve and report the tokenizer difference.

## 9. Required Week 3 Work

Week 3 should focus on controlled evaluation rather than pipeline development.

Planned work:

- compare chunk-size distributions
- compare boundary behaviour
- compare behaviour across representative document groups
- measure parameter sensitivity
- compare runtime and resource cost
- investigate the SemanticChunker numerical warning if relevant
- perform retrieval evaluation if suitable labels or queries are available
- produce an evidence-based final comparison

## 10. Reproducibility Rules

Week 3 must:

- keep frozen source data immutable
- preserve provenance
- record exact configurations
- use the automated QA checks
- store experimental outputs separately
- distinguish warnings from failures
- avoid interpreting raw chunk count as quality
- document all changes from the frozen protocol

## Status

Week 3 evaluation inputs and handoff are ready.
