# Chonkie Chunking Exploration Notes - 2026-08-31

Suggested GitHub path:

```text
team-members/xingyu-li/notes/chonkie-chunking-exploration-notes-2026-08-31.md
```

## Context

Matthew's 2026-08-31 email confirmed that last week's SimHash/MinHash duplication result was accurate and that we do not need to further reduce the dataset with SimHash this week.

The focus for this work is to understand the chunking process and use the open source Chonkie library. Matthew also noted that if we can chunk the data, that is useful; if not, the notebook should still be visible so the work can be reviewed and taken to the next step.

## Notebook

Notebook prepared and tested:

```text
AUTokens50_chonkie_chunking_exploration.ipynb
```

The notebook is a bounded preview/exploration notebook. It is designed to run in the online Jupyter environment where the AUTokens50 parquet data is available.

## Work Completed

- Created a Chonkie chunking exploration notebook for AUTokens50.
- Ran the notebook in the online Jupyter environment.
- Installed and used Chonkie successfully in the notebook environment.
- Confirmed the notebook can locate the real dataset path:

```text
/home/jovyan/JoeyLLM_Data/AUTokens50_with_hash_simhash
```

- Confirmed the dataset contains `57` parquet part files.
- Loaded a bounded preview sample from the parquet dataset:
  - sampled files: `2`
  - sampled documents: `20`
- Tested three Chonkie chunkers:
  - `TokenChunker`
  - `SentenceChunker`
  - `RecursiveChunker`
- Generated `328` preview chunks.
- Saved preview outputs to:

```text
/home/jovyan/Scratch/AUTokens50_chonkie_chunk_preview/
```

## Preview Results

| Chunker | Documents | Chunks | Average Chunks per Document | Average Chunk Characters |
|---|---:|---:|---:|---:|
| RecursiveChunker | 20 | 112 | 5.6 | 1657.29 |
| SentenceChunker | 20 | 108 | 5.4 | 1768.31 |
| TokenChunker | 20 | 108 | 5.4 | 1822.97 |

## Initial Observations

- All three Chonkie chunkers ran successfully on sampled AUTokens50 text.
- `TokenChunker` creates fixed-size chunks and may split in the middle of words or sentences.
- `SentenceChunker` and `RecursiveChunker` appear more useful for review because they better preserve text boundaries.
- `RecursiveChunker` produced slightly more chunks with a smaller average chunk size, which may be useful for later retrieval and vector database preparation.
- The preview used the `character` tokenizer so the notebook can run reliably without needing to download external tokenizer assets.

## Output Files From Preview Run

The online preview run wrote:

```text
/home/jovyan/Scratch/AUTokens50_chonkie_chunk_preview/chonkie_chunk_preview.parquet
/home/jovyan/Scratch/AUTokens50_chonkie_chunk_preview/chonkie_chunk_preview.csv
/home/jovyan/Scratch/AUTokens50_chonkie_chunk_preview/chonkie_chunk_preview_summary.json
```

The CSV is useful for quick review because it stores compact metadata and previews. The parquet output keeps the fuller chunk records for later inspection.

## Scope Boundary

This note records a Chonkie chunking preview and notebook-based exploration only.

This work does not claim:

- the full AUTokens50 corpus has been chunked;
- embeddings have been generated;
- vector database integration has been completed;
- the chunked output is production-ready.

## Next Steps

- Review the preview chunks and confirm the preferred chunking strategy.
- Decide whether the full chunking run should use the original hash/simhash dataset or the exact-hash deduplicated output.
- After chunking strategy and chunk size are approved, prepare a separate full-corpus chunking run.
