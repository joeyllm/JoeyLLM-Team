# Issue 4 - Chunking Prototype Results

## Scope

Three Chonkie chunking methods were tested on the 32 representative documents:

- TokenChunker
- RecursiveChunker
- SemanticChunker

Total runs: 96.

## Validation

- Successful runs: 96/96
- Failed runs: 0
- Invalid index ranges: 0
- Source slice mismatches: 0

Semantic output validation:

- Total semantic chunks: 5,629
- Empty chunks: 0
- Zero-token chunks: 0
- Non-matching source slices: 0

## Prototype Results

| Method | Total chunks | Mean chunks/document | Mean runtime/document |
|---|---:|---:|---:|
| TokenChunker | 1,078 | 33.6875 | 0.006858 s |
| RecursiveChunker | 1,272 | 39.7500 | 0.000943 s |
| SemanticChunker | 5,629 | 175.9063 | 0.102390 s |

## Observations

SemanticChunker produced substantially finer segmentation than TokenChunker and RecursiveChunker under the current prototype configurations.

The current configurations are not directly comparable as a controlled benchmark because TokenChunker and RecursiveChunker use the character tokenizer while SemanticChunker uses the tokenizer associated with the Model2Vec embedding model.

One Model2Vec runtime warning was observed during semantic processing, but all runs completed successfully and all output chunks passed index and source-slice validation.

The smallest observed semantic chunk contained 22 characters, so `min_characters_per_sentence=24` should not be interpreted as a minimum final chunk length.

## Artifacts

- `prototype.log`
- `prototype_summary.csv`
- `prototype_chunks.parquet`

## Status

Issue 4 prototype complete.
- `prototype_chunks.parquet`

## Status

Issue 4 prototype complete.
