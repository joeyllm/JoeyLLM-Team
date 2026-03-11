# GPU Data Handling

## VRAM Management

GPU data processing fails quickly when batches are oversized. cuDF is fast, but it is still constrained by device memory, allocator fragmentation, and temporary buffers created during transforms.

## OOM Prevention

- load smaller partitions instead of one large file
- select only required columns
- avoid unnecessary copies
- free intermediate dataframes as soon as they are no longer needed
- prefer batch processing over full-dataset loading

## Example Pattern

```python
import gc
import cudf

columns = ["text", "language"]
paths = [
    "data/fineweb/shard-000.parquet",
    "data/fineweb/shard-001.parquet",
]

for path in paths:
    gdf = cudf.read_parquet(path, columns=columns)
    filtered = gdf[gdf["language"] == "en"]

    # Write or hand off results here before loading the next shard.
    filtered.to_parquet(path.replace(".parquet", "-filtered.parquet"))

    del filtered
    del gdf
    gc.collect()
```

## Practical Notes

- String-heavy columns can consume much more VRAM than expected.
- Groupby, joins, and sort operations often need extra temporary memory.
- A job that barely fits is unstable; leave safety margin in VRAM.
- Test with one shard first, then increase throughput carefully.
