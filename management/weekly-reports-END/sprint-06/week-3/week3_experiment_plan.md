# Week 3 - Controlled Chunking Evaluation Plan

## Objective

Week 3 performs controlled evaluation of the validated Chonkie
chunking pipeline developed during Weeks 1 and 2.

The evaluation focuses on:

1. baseline behaviour
2. parameter sensitivity
3. matched-granularity comparison
4. robustness across document types
5. computational cost

The frozen source data must not be modified.

## Experimental Input

Representative evaluation set:

`/home/jovyan/hash_output/_audit/profiling/representative_samples.parquet`

The representative set contains 32 documents.

Frozen source dataset:

`/home/jovyan/hash_output/part_*.parquet`

The representative set and pipeline inputs are checksum-frozen before
Week 3 experiments begin.

## Environment

The Week 3 environment is recorded in:

`week3/configs/environment_snapshot.json`

Dependency specifications are also retained in:

- `requirements.txt`
- `requirements-lock.txt`

## Baseline Configurations

Baseline configurations are frozen in:

`week3/configs/baseline_configs.json`

### TokenChunker

- method: `token`
- tokenizer: `character`
- chunk_size: `2048`
- chunk_overlap: `0`

### RecursiveChunker

- method: `recursive`
- tokenizer: `character`
- chunk_size: `2048`
- min_characters_per_chunk: `24`

### SemanticChunker

- method: `semantic`
- embedding_model: `minishlab/potion-base-32M`
- threshold: `0.8`
- chunk_size: `2048`

## Parameter-Sensitivity Matrix

The frozen experiment matrix is stored in:

`week3/configs/parameter_sensitivity_matrix.csv`

There are 11 unique planned configurations.

### TokenChunker

Chunk-size sensitivity:

- 1024
- 2048
- 4096

Fixed settings:

- tokenizer = `character`
- chunk_overlap = `0`

### RecursiveChunker

Chunk-size sensitivity:

- 1024
- 2048
- 4096

Fixed settings:

- tokenizer = `character`
- min_characters_per_chunk = `24`

### SemanticChunker

Chunk-size sensitivity:

- 1024
- 2048
- 4096

with:

- threshold = `0.8`

Threshold sensitivity:

- 0.7
- 0.8
- 0.9

with:

- chunk_size = `2048`

The baseline SemanticChunker configuration
`chunk_size=2048, threshold=0.8` is executed only once.

## Experiment A - Baseline Behaviour

Evaluate the three validated baseline configurations on the same
32 representative documents.

Measure:

- total chunks
- chunks per document
- chunk character-length distribution
- chunk token-count distribution
- boundary behaviour
- runtime
- warnings
- failures
- QA status

The baseline experiment is descriptive.

Raw chunk count must not be interpreted as a standalone quality metric.

## Experiment B - Parameter Sensitivity

Run the 11 configurations defined in the frozen parameter matrix.

For each run:

1. preserve the same source documents
2. record the exact configuration
3. write output to a separate run directory
4. run automated QA
5. generate evaluation statistics
6. retain warnings separately from hard failures

Parameter sensitivity should first be interpreted within each method.

## Experiment C - Matched-Granularity Comparison

The three methods use different tokenizer semantics.

TokenChunker and RecursiveChunker use:

`tokenizer="character"`

SemanticChunker uses the tokenizer associated with the local Model2Vec
embedding model.

Therefore equal configured `chunk_size` values do not imply equivalent
effective granularity.

Cross-method comparison must use observed output behaviour.

The matching stage should consider:

- median chunk character length
- mean chunk character length
- chunks per document

After selecting approximately matched configurations, compare:

- chunk-size distribution
- boundary behaviour
- fragmentation
- robustness
- runtime
- warnings
- failures

Residual differences in granularity must be reported.

## Evaluation Dimensions

### 1. Output Validity

Check:

- empty chunks
- whitespace-only chunks
- zero-token chunks
- invalid index ranges
- source-slice mismatches
- provenance mismatches

### 2. Granularity

Measure:

- total chunks
- chunks per document
- character-length distribution
- token-count distribution

### 3. Boundary Behaviour

Use deterministic boundary classes defined by the Week 3 evaluation
aggregator.

The rules must be documented before final interpretation.

### 4. Robustness

Analyze behaviour across the representative sample groups already
stored in `sample_groups`.

### 5. Computational Cost

Measure available evidence for:

- runtime
- documents per second
- chunks per second where useful
- output size
- warnings
- failures
- memory use where it was actually recorded

## Retrieval Evaluation

Retrieval evaluation is not required for the core Week 3 experiment.

It should only be added if suitable queries and relevance labels are
available through a defensible protocol.

No relevance labels should be invented solely to force a retrieval
metric.

## Experimental Rules

1. Keep frozen source data immutable.
2. Use the same representative documents for comparable runs.
3. Record exact configuration for every run.
4. Preserve source provenance.
5. Run automated QA before interpreting results.
6. Separate warnings from hard failures.
7. Do not use raw chunk count as a standalone quality metric.
8. Do not assume equal configured chunk sizes mean equal effective
   granularity across methods.
9. Store every experimental run separately.
10. Preserve machine-readable evidence for reported results.
11. Document deviations from this protocol before interpreting them.
12. Distinguish measured results from interpretation.

## Planned Week 3 Workflow

1. Freeze experimental design.
2. Build the evaluation aggregator.
3. Run parameter-sensitivity experiments.
4. Select approximately matched-granularity configurations.
5. Perform cross-method comparison.
6. Analyze robustness and computational cost.
7. Produce the final Week 3 evaluation report.

## Frozen Artifacts

The experimental design depends on:

- `week3/configs/baseline_configs.json`
- `week3/configs/parameter_sensitivity_matrix.csv`
- `week3/configs/experimental_constants.json`
- `week3/configs/environment_snapshot.json`
- `week3/configs/week3_input_sha256.txt`
- `week3/week3_experiment_plan.md`

## Status

Week 3 experimental design frozen.
