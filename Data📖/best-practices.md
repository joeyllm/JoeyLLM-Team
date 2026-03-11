# Best Practices

## Subset First

Always start with a subset. This is the default rule for FineWeb-scale data.

Why:

- it validates schema assumptions early
- it exposes memory issues before a long run fails
- it shortens the debug loop
- it makes performance tuning measurable

## Memory Management

- read only the columns needed for the task
- process data in shards or batches
- write intermediate outputs instead of keeping everything in memory
- delete temporary objects after use
- monitor RAM and VRAM during early runs

## Operational Guidance

1. Run a tiny sample to verify code correctness.
2. Run a larger subset to estimate memory and runtime.
3. Scale to production-sized shards only after the first two steps succeed.

## Anti-Patterns

- loading the full dataset to "see what happens"
- converting many shards into one giant dataframe
- mixing debugging and full-scale execution in the same run
- assuming GPU memory pressure behaves like CPU memory pressure
