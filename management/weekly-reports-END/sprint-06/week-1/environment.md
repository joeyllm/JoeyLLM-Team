# Chonkie Environment

## Project

- Project directory: `/home/jovyan/chunking_sprint`
- Purpose: Reproducible environment for the 3-week chunking sprint

## Python Environment

- Virtual environment: `/home/jovyan/chunking_sprint/chonkie`
- Python version: 3.13.15
- Python executable: `/home/jovyan/chunking_sprint/chonkie/bin/python`

## Chonkie

- Chonkie version: 1.7.0
- Installation: isolated local virtual environment
- Direct dependency: `chonkie==1.7.0`
- Full resolved dependencies: `requirements-lock.txt`

## Verified Local Chunkers

The installed Chonkie 1.7.0 package exposes:

- `TokenChunker`
- `RecursiveChunker`
- `SentenceChunker`
- `SemanticChunker`
- `CodeChunker`
- `TableChunker`
- `FastChunker`
- `LateChunker`
- `NeuralChunker`
- `SlumberChunker`
- `TeraflopAIChunker`

## Verification

Local smoke tests were created for:

- `RecursiveChunker`
- `TokenChunker`

The smoke tests use the local `character` tokenizer and require no external model or API.

See:

- `tests/smoke_test_chonkie.py`
- `smoke_test.log`
