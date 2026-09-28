# Issue 5 - Chunking Evaluation Metrics

## Goal

Define the metrics that will be used to compare chunking methods in later controlled experiments.

## 1. Output Validity

For every chunking run:

- successful / failed run
- invalid index ranges
- source-slice mismatches
- empty chunks
- zero-token chunks

A valid chunk must map back to the original source text using its recorded start and end indices.

## 2. Chunk Granularity

For each method and document:

- number of chunks
- minimum chunk length
- mean chunk length
- median chunk length
- maximum chunk length
- chunk length distribution

Both character length and the chunker's reported token count will be recorded.

## 3. Boundary Behaviour

Evaluate where chunk boundaries occur relative to document structure.

Record whether boundaries occur around:

- paragraph breaks
- sentence boundaries
- headings
- lists
- other visible structural separators

Representative documents will be used for manual boundary inspection where required.

## 4. Efficiency

For each method:

- runtime per document
- total runtime
- mean runtime per document

External API usage and model cost will also be recorded if any method requires them.

## 5. Robustness

Compare behaviour across the representative sample groups, including:

- short documents
- median-length documents
- long documents
- extreme-length documents
- documents without newlines
- high chars/token cases
- low chars/token cases

The objective is to identify methods that remain stable across different document structures and lengths.

## 6. Comparison Rule

Chunk count or runtime alone will not determine which method is better.

The methods must be evaluated using a combination of:

- output validity
- chunk granularity
- boundary quality
- robustness
- computational cost

The current prototype configurations use different tokenizer semantics, so prototype chunk sizes must not be treated as directly equivalent. Controlled experiments should align the comparison settings where possible, or explicitly report the difference.

## 7. Retrieval Evaluation

If a suitable retrieval task, query set, or relevance labels become available, retrieval-quality metrics can be added later.

Retrieval evaluation is not required for the initial chunking comparison.

## Status

Evaluation metrics defined for the controlled chunking experiments.
