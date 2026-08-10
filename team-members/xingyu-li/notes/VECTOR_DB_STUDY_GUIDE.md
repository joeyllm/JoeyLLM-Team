# Vector Database and Qdrant Learning Notes

These notes summarise my current understanding of vector databases, Qdrant, and how retrieval could fit into the JoeyLLM project. The focus is on the core concepts and the expected workflow rather than a production deployment.

## Core Idea

A vector database is designed for semantic search.

Traditional keyword search checks whether the same words appear in the text. Vector search compares meaning. For example, if a user asks:

```text
How can we reduce duplicate training data?
```

a vector database should still be able to retrieve passages about hash, simhash, deduplication, or data cleaning, even if the exact wording is different.

## Why Text Is Converted Into Vectors

Computers do not directly understand that two passages have similar meanings. An embedding model converts text into a list of numbers:

```text
"deduplicate Australian data"
-> [0.12, -0.44, 0.08, ...]
```

This list of numbers is called an embedding vector. Texts with similar meaning should usually have vectors that are close to each other in vector space.

## Basic Retrieval Workflow

### 1. Chunking

Long documents are split into smaller pieces called chunks.

This is necessary because:

- a full document can be too long to search or pass into a model
- one document may contain several unrelated topics
- language models have a limited context window

### 2. Embedding

Each chunk is converted into a vector using an embedding model.

In a real system, this should be done with the embedding model selected for the project. In a local learning spike, a simple deterministic embedding can be used only to demonstrate the workflow.

### 3. Indexing

The vectors are stored in a vector database such as Qdrant. Each stored item should also include useful metadata.

Example payload:

```json
{
  "region": "AU",
  "source": "fineweb",
  "hash": "...",
  "simhash": "...",
  "tokens": 320
}
```

### 4. Retrieval

When a user asks a question, the question is also converted into a vector. The vector database then searches for the chunks with the closest vectors.

### 5. Context Assembly

The retrieved chunks are added to the model prompt or request context before calling the JoeyLLM API.

Example:

```text
User question:
How should we handle duplicate Australian data?

Retrieved context:
[1] Hash and simhash fields help identify duplicate and near-duplicate text.
[2] Australian FineWeb data should be cleaned and deduplicated before training or retrieval.

Instruction to model:
Use the retrieved context to answer the user's question.
```

## RAG

RAG stands for Retrieval-Augmented Generation.

The idea is:

- Retrieval: search for relevant information first
- Augmentation: provide that information to the model as context
- Generation: let the model generate an answer using the question and retrieved context

The key point is that the model does not need to store all project knowledge in its weights. It can look up relevant external information before answering.

## What Qdrant Does

Qdrant is a vector database. It stores embedding vectors and supports fast similarity search.

A useful comparison is:

```text
PostgreSQL:
  table -> row -> columns

Qdrant:
  collection -> point -> vector + payload
```

## Qdrant Terminology

| Term | Meaning | JoeyLLM Example |
| --- | --- | --- |
| Collection | A named group of vector records | `joeyllm_chunks` |
| Point | One stored vector record | One text chunk |
| Vector | Numeric representation of text | Embedding output |
| Payload | Metadata stored with the vector | region/source/hash/simhash |
| Distance | Similarity calculation method | cosine |
| Upsert | Insert or update a point | Store a new chunk |
| Query/Search | Retrieve similar vectors | Find chunks related to a user question |
| Filter | Restrict search using metadata | Search only AU data |

## Why A Normal Database Is Not Enough

A normal database is good at exact filtering:

```sql
WHERE region = 'AU'
```

However, it is not designed to answer a semantic search request such as:

```text
Find passages that are closest in meaning to "how to reduce duplicate training data".
```

A vector database is better suited for this type of similarity search.

In practice, both approaches can be combined:

- vector similarity finds semantically related text
- payload filters restrict the results by region, source, dataset, or other metadata

## Connection To Previous Data Work

The hash and simhash work from the previous sprint is relevant to vector database indexing.

- hash can identify exact duplicate text
- simhash can identify near-duplicate text
- repeated content can reduce retrieval quality
- duplicate or near-duplicate chunks can be removed before indexing
- hash and simhash can also be stored as Qdrant payload fields

This means the earlier data cleaning and deduplication work can support a cleaner retrieval layer.

## How This Fits Into JoeyLLM

The vector database should sit between the ChatJoey server-side API route and the JoeyLLM model API.

Suggested flow:

```text
ChatJoey frontend
  -> server-side API route
  -> embed user query
  -> search Qdrant for relevant chunks
  -> build context from top-k results
  -> call JoeyLLM API with user question and retrieved context
  -> return answer to frontend
```

The browser should not directly access Qdrant. API keys, Qdrant endpoints, embedding endpoints, and raw dataset details should stay on the server side.

## Current Understanding

At this stage, the important points are:

- a vector database supports semantic retrieval
- Qdrant stores vectors with payload metadata
- user questions and dataset chunks must use the same embedding model
- retrieval results are ranked by similarity score
- retrieved chunks can be passed to JoeyLLM as context
- production integration requires decisions about embedding model, vector dimension, Qdrant hosting, chunking, metadata schema, and retrieval evaluation

## Short Explanation

Vector database lets JoeyLLM search relevant dataset chunks before answering. We split documents into chunks, embed each chunk into a vector, store those vectors and metadata in Qdrant, then embed the user's question and retrieve the most similar chunks. The retrieved chunks are passed as context to the JoeyLLM API. This supports retrieval-based answering without forcing all knowledge into the model weights.

## Suggested Next Steps

1. Select the embedding model and confirm vector dimension.
2. Decide whether Qdrant will run locally, self-hosted, or in the cloud.
3. Define the collection name and payload schema.
4. Index a small sample of verified AU/NZ data.
5. Run several retrieval test questions.
6. Record the top-k retrieved chunks and similarity scores.
7. Compare model responses with and without retrieval context.

## References

- Qdrant overview: https://qdrant.tech/documentation/overview/
- Collections: https://qdrant.tech/documentation/manage-data/collections/
- Points: https://qdrant.tech/documentation/manage-data/points/
- Payload: https://qdrant.tech/documentation/concepts/payload/
- Search: https://qdrant.tech/documentation/search/search/
