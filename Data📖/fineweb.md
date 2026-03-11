# FineWeb Dataset Notes

## Overview

FineWeb is a large-scale web text dataset intended for language-model pretraining and large corpus analysis. For this project, the important point is scale: the full dataset is on the order of tens of terabytes, so it must be treated as a distributed or streamed data source rather than a file you load into local memory.

## Scale Considerations

- Treat the full FineWeb corpus as roughly `60 TB` class data for planning purposes.
- Full-dataset processing is not realistic on a laptop or a single mid-range workstation.
- Storage format, compression, and selected subset will change the actual bytes on disk.
- Data transfer time is a serious bottleneck and should be part of experiment planning.

## Practical Implications

- Start with a small subset before touching the full corpus.
- Prefer columnar formats and partitioned storage when available.
- Avoid converting entire splits into one local CSV or one in-memory dataframe.
- Keep preprocessing steps incremental so jobs can resume after failure.

## Recommended Workflow

1. Identify the exact split or shard needed for the experiment.
2. Load only the columns required for that task.
3. Sample or subset first to validate schema and code paths.
4. Scale up gradually while measuring RAM, VRAM, disk, and runtime.

## Documentation Checklist

When working with FineWeb, document:

- source location
- exact split or version used
- storage format
- subset size
- filtering steps
- output artifacts produced by preprocessing
