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

## One-line Summary
These upgrades move the work from a “working notebook experiment” to a **reproducible, comparable, and iterative pipeline**: standardized profiling outputs + stratified auditing + v1/v2 explainable cleaning iterations + speed/IO tracking.
