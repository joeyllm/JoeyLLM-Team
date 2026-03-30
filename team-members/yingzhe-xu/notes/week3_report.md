# Week 3 Report — Notebook Upgrades (Data Profiling + Cleaning Iterations)

## 1) Data Exploration Notebook (week2_Data_analysis_en_UPGRADED): Improvements vs. Previous Version

- **From “viewing results” to a reusable, quantitative profile output**
  - The upgraded notebook automatically exports a standardized shard profile (`profile_summary.csv/json`) so results are comparable across shards and across teammates.

- **From `describe()` to a stable metrics system (quantiles + threshold ratios)**
  - Key distributions (e.g., `token_count`, `language_score`) are summarized using fixed quantiles (p25/p50/p75/p90/p95/p99) and ratio-based thresholds (e.g., `<100 tokens`, `<0.9 language_score`) to support before/after comparisons.

- **From outlier-only inspection to stratified sampling**
  - Instead of checking only the shortest/longest/lowest-score examples, the notebook produces bucketed review samples (by length, language-score, and URL-pattern buckets) and exports them for consistent manual auditing.

- **Added IO timing (speed tracking)**
  - The notebook records and exports timings for metadata read, table load, pandas conversion, and feature engineering (`io_timing.csv`), aligning with the requirement to track IO performance.

## 2) Filtering / Cleaning Notebook (week2_filter_draft_001_en_UPGRADED and week3_filter_draft_002_en): Improvements vs. Previous Version

- **From a single pass to 2-round, explainable iterations (v1/v2)**
  - The workflow now supports explicit iteration versions:
    - **v1**: baseline filters (empty/short text, language confidence, weak URL patterns, template-like pages, exact dedup).
    - **v2**: refinement targeting typical “long-but-noisy” web spam/SEO cases (e.g., keyword-based spam heuristics and optional very-long-text controls).

- **Versioned outputs aligned to shard IDs**
  - Output naming is automatically aligned to `SHARD_ID`, and results are organized by version (`cleaning_outputs/<shard>/<version>/...`), preventing mislabeling and enabling clean comparisons.

- **Rule statistics upgraded for interpretability**
  - Rule reporting distinguishes **rule hits** (can overlap) from the **final removed total** (non-overlapping), improving explainability of what caused removals.

- **Before/after metrics standardized and expanded**
  - The cleaning notebook exports consistent evaluation metrics (retention/deletion rates, distribution quantiles/ratios, language-score threshold ratios, weak URL pattern ratios, duplication indicators) that match the profiling summary format.

- **Sampling upgraded: random → stratified**
  - Raw vs. cleaned review samples are bucketed (length / language-score / URL-pattern) and exported with `manual_label` / `manual_notes` columns to close the loop with manual quality checks.

- **Added IO timing for pipeline stages**
  - Timing logs quantify read/transform/write costs, enabling bottleneck identification and supporting “large-scale web dataset cleaning” claims.


## 3) IO Timing Finding (Shard 004_00018, v1)

Using the recorded IO metrics:

- `read_meta_s`: 0.0043 s  
- `load_table_s`: 0.6949 s  
- `to_pandas_s`: 0.0069 s  
- `total_load_s`: 0.7063 s  
- `feature_engineering_s`: 37.8622 s  
- Shard size: 172,447 rows, 173 row groups, 9 columns

**Key takeaway:** Parquet IO is not the bottleneck. Loading the shard into memory takes ~0.71 s, while feature engineering takes ~37.86 s, meaning feature engineering accounts for ~98% of the combined (load + feature) runtime. This indicates that Python-level text/URL parsing and per-row feature computation dominate overall runtime, so performance improvements should prioritize optimizing or reducing feature engineering rather than parquet reading.


## 4) Next-Step Performance Optimizations (Ordered by Expected Impact)

1. **Reduce or defer expensive feature engineering**
   - Compute heavyweight text-derived features (e.g., word counts, average word length) only on stratified samples for auditing, or only after a first-pass filter has removed obvious low-quality records.
   - Keep the full-pass features minimal (e.g., `token_count`, `language_score`, and lightweight URL pattern checks).

2. **Replace Python `apply()` loops with vectorized operations or faster engines**
   - Avoid per-row `apply()` for URL parsing and text processing where possible.
   - Prefer vectorized string operations (e.g., pandas `.str` methods) or move filtering/feature extraction into faster backends such as Polars or DuckDB for columnar execution.

3. **Batch processing**
   - Process the shard in batches (e.g., by row group or fixed-size batches) to reduce memory pressure and isolate the cost of individual steps.
   - This also enables incremental writes and easier recovery if a batch fails.

4. **Minimize repeated regex scans**
   - Pre-compile regex patterns and reduce the number of passes over `text`.
   - Merge multiple pattern checks into a single pass when feasible.

5. **Measure after each change**
   - Re-run IO timing after each optimization and track changes in `feature_engineering_s` to confirm real speedups and identify new bottlenecks.


## One-line Summary
These upgrades move the work from a “working notebook experiment” to a **reproducible, comparable, and iterative pipeline**: standardized profiling outputs + stratified auditing + v1/v2 explainable cleaning iterations + speed/IO tracking.
