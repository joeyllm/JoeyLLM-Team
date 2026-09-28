# Week 1 - Design and Exploration

Week 1 focused on understanding and freezing the deduplicated dataset, profiling document characteristics, establishing a reproducible Chonkie environment, and prototyping multiple chunking strategies.

## Completed Work

- Frozen and documented the deduplicated input dataset.
- Profiled 6,008,596 documents across 57 Parquet files.
- Created a 32-document representative evaluation set.
- Set up a reproducible Chonkie 1.7.0 environment.
- Prototyped TokenChunker, RecursiveChunker, and SemanticChunker.
- Completed 96/96 prototype runs successfully.
- Verified zero invalid index ranges and zero source-slice mismatches.
- Defined chunking evaluation metrics.
- Finalized the Week 1 experiment protocol.

## Main Artifacts

- `environment.md`
- `evaluation_metrics.md`
- `week1_experiment_protocol.md`
- `data-audit/`
- `tests/`
- `prototypes/`
