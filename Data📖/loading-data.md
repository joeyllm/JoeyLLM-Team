# Loading Data

## CPU with Pandas

Use Pandas when the subset is small enough to fit comfortably in system RAM.

```python
import pandas as pd

columns = ["text", "language", "token_count"]

df = pd.read_parquet(
    "data/fineweb/sample.parquet",
    columns=columns,
)

print(df.head())
print(df.memory_usage(deep=True).sum() / 1024**2, "MB")
```

### When to Use Pandas

- schema inspection
- small samples
- debugging preprocessing code
- CPU-only environments

## GPU with cuDF

Use cuDF when the dataset chunk fits in VRAM and the preprocessing work benefits from GPU acceleration.

```python
import cudf

columns = ["text", "language", "token_count"]

gdf = cudf.read_parquet(
    "data/fineweb/sample.parquet",
    columns=columns,
)

print(gdf.head())
print(gdf.memory_usage(deep=True).sum() / 1024**2, "MB")
```

### When to Use cuDF

- repeated dataframe transforms
- filtering large batches
- string operations that benefit from GPU execution
- workflows already running on a GPU machine

## Basic Rule

If the first sample does not fit comfortably in RAM or VRAM, reduce the subset size before doing anything else.
