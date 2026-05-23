# WEN SUN — Comments on the JoeyLLM Paper

The paper presents a practical and scalable pipeline for extracting national corpora from FineWeb, and the use of embedding-based semantic analysis is a valuable direction for validating corpus coherence at scale. The cross-country comparison across Australia, the United Kingdom, Canada, and New Zealand also helps show that the proposed pipeline is not limited to a single national context.

However, the validation methodology could be described in more detail to improve reproducibility and reliability.

## 1. Specify the Embedding Model and Preprocessing Details

First, the paper does not specify which embedding model was used for semantic projection and semantic anchor matching. Since different embedding models may produce different clustering patterns, topic assignments, and cross-country differences, the paper should report the following details:

- Exact embedding model name
- Model version
- Embedding dimension
- Chunk length
- Truncation strategy for long documents
- Whether embeddings were normalized
- Whether cosine similarity or Euclidean distance was used for anchor matching

These details are important because the main validation figures and topic distribution results depend on the embedding representation.

## 2. Add a Small-Scale Human Audit

Second, the validation appears to rely mainly on automatic methods, such as embedding projections and topic distributions. These methods are useful for large-scale analysis, but a small human audit would make the validation more convincing.

For example, the authors could manually inspect a random sample of retained documents and removed documents to estimate:

- The regional precision of the ccTLD extraction
- The false positive rate of the structural refinement stage
- The false negative rate of the structural refinement stage

This could include checking whether retained documents genuinely reflect the target national context, and whether documents removed by structural refinement were correctly identified as non-local structural artifacts.

## Overall Suggestion

Adding these details would make the evaluation more transparent and would help readers better assess whether the observed semantic coherence comes from the actual corpus structure rather than from model choice, sampling decisions, or projection artifacts.
