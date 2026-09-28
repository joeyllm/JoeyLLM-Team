# Week 2 - Chunking Development and Validation Report

## Objective

Week 2 converted the Week 1 Chonkie prototypes into a reusable, provenance-aware, validated batch chunking pipeline and tested its behaviour at larger scale.

## 1. Batch Pipeline

A configurable batch chunking pipeline was implemented:

`pipeline/run_chunking.py`

The pipeline supports:

- TokenChunker
- RecursiveChunker
- SemanticChunker

Configuration is provided through CLI arguments, including:

- input path
- output directory
- chunking method
- chunk size
- tokenizer
- overlap
- RecursiveChunker minimum character setting
- SemanticChunker embedding model and threshold
- batch size
- maximum number of documents

The pipeline records:

- processing progress
- runtime
- failures
- chunk count
- run configuration
- execution metadata

Frozen source files are never modified.

## 2. Provenance and Metadata

Chunk outputs preserve source provenance.

Each chunk records:

- input file
- original source file
- original source row number
- document ID
- available source metadata
- chunking method
- exact chunker configuration
- chunk index
- start index
- end index
- chunk token count
- chunk character length
- chunk text

Representative-sample provenance was verified against the original frozen dataset.

Validation confirmed:

- document ID match: PASS
- source text slice match: PASS
- URL match: PASS
- file path match: PASS
- stored token count match: PASS

## 3. Automated QA

Automated QA was implemented in:

`pipeline/validate_chunks.py`

Checks include:

- required provenance fields
- empty chunks
- whitespace-only chunks
- zero-token chunks
- character-length consistency
- source lookup
- document ID consistency
- valid start/end indices
- source-slice equality
- pipeline document failures
- warning capture

Machine-readable and human-readable outputs are generated.

## 4. Representative-Set Validation

The final Week 2 pipeline was validated on all 32 representative documents using all three methods.

### TokenChunker

- Documents: 32
- Chunks: 1,078
- Pipeline failures: 0
- Hard QA failures: 0
- QA status: PASS

### RecursiveChunker

- Documents: 32
- Chunks: 1,272
- Pipeline failures: 0
- Hard QA failures: 0
- QA status: PASS

### SemanticChunker

- Documents: 32
- Chunks: 5,629
- Pipeline failures: 0
- Hard QA failures: 0
- QA status: PASS
- Recorded Model2Vec runtime warnings: 1

The SemanticChunker warning was recorded separately from hard failures and did not affect chunk integrity.

## 5. Week 1 Consistency

Week 2 outputs were compared against the Week 1 prototype outputs.

For all three methods:

- chunk counts matched
- chunk order matched
- source identity matched
- chunk indices matched
- start/end indices matched
- token counts matched
- character lengths matched
- chunk text matched

Result:

`WEEK 1 CONSISTENCY: PASS`

## 6. Scaled Processing

Scaled processing was performed using TokenChunker on frozen dataset file:

`/home/jovyan/hash_output/part_0.parquet`

The file contains:

- 227,628 documents
- approximately 1.0 GiB source data

### 10,000-Document Pilot

- Documents processed: 10,000
- Failures: 0
- Chunks generated: 57,165
- Pipeline time: 13.775 s
- Wall time: 14.296 s
- Maximum RSS: 762,856 KB
- Output size: approximately 46 MB

### Full part_0 Run

- Documents processed: 227,628
- Failures: 0
- Chunks generated: 1,334,973
- Pipeline time: 344.773 s
- Wall time: 345.354 s
- Maximum RSS: 1,512,640 KB
- Output size: approximately 1.1 GB

## 7. Scaled QA

The complete `part_0` output was validated using streaming QA.

Results:

- Documents checked: 227,628
- Chunks checked: 1,334,973
- Validation failure events: 0
- QA status: PASS
- QA elapsed time: 30.98 s

## 8. Frozen Input Integrity

The original frozen input was re-verified after scaled processing.

Result:

`part_0.parquet: OK`

The source dataset remained unchanged.

## 9. Known Limitations

### Tokenizer Semantics

The current prototype configurations are not directly equivalent in chunk-size semantics.

TokenChunker and RecursiveChunker use:

`tokenizer="character"`

SemanticChunker uses the tokenizer associated with:

`minishlab/potion-base-32M`

Therefore raw chunk counts must not be interpreted as a direct quality ranking.

### Semantic Warning

Model2Vec produced one numerical runtime warning during representative-set SemanticChunker processing:

`RuntimeWarning: invalid value encountered in divide`

The warning did not result in pipeline failures or QA failures.

### Full Dataset Scale

The complete 57-file frozen dataset was not chunked during Week 2.

Scaled validation instead progressed from:

- 32 representative documents
- 10,000 frozen documents
- one complete 227,628-document frozen Parquet file

This provides sufficient engineering evidence for larger-scale feasibility analysis.

## Status

Week 2 development and validation complete.
