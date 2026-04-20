# Week 3 Report 🗂️

**Week:** Week 3
**Date:** 2026-03-30
**Attendees:** Wen Sun, Xiang Chang, Xingyu Li, Nuo Chen, Yingzhe Xu
**Facilitator:** Xingyu Li
**Prepared by:** Nuo Chen

---

## Agenda

1. Cross-compare individual Week 2 filtering results — identify which rules are consistently effective across shards vs. shard-specific
2. Align on shared filtering thresholds and discuss the gap between threshold filtering and deeper content cleaning
3. Review IO performance findings and discuss pipeline scalability for the full 60TB dataset
4. Finalise pre-Easter deliverables: each member's upgraded notebook, outputs, and documentation

## Discussion

> This week's meeting opened with each member presenting their filtering results side by side. A clear pattern emerged: across all five notebooks, `language_score` filtering dominated all other rules, accounting for >95% of row removals. Rules targeting short text, long text, and URL patterns were useful as safety nets but had minimal independent impact — confirming that FineWeb is already well pre-filtered for basic quality.
>
> The team identified a significant gap between what threshold filters can achieve (~3–4% removal) and the deeper quality issues revealed by profiling (~57.7% of documents contain repeated template lines). This led to a key decision: rather than pushing thresholds higher (which risks removing legitimate content), the team should pursue content-level cleaning — specifically intra-document line deduplication and boilerplate stripping — as the next priority.
>
> IO performance was another major discussion point. Yingzhe's profiling revealed that feature engineering accounts for ~98% of total processing time (37.86s vs. 0.71s for parquet loading), and Xiang's per-operation timing confirmed that non-alphanumeric ratio checks (18.4s) and low-information keyword checks (6.3s) are the most expensive operations. The team agreed that future pipeline design should minimise per-row Python `apply()` calls and explore vectorised alternatives.
>
> Finally, the team discussed how to standardise outputs across members — consistent CSV column names, quantile-based profiling metrics, and stratified sampling for manual review — to enable meaningful cross-comparison and reproducibility.

## Decisions

- **Shared threshold baseline**: adopt `language_score >= 0.85` (based on Xingyu's sensitivity analysis showing a natural inflection point), `min_tokens >= 50`, `min_text_length >= 100–200 chars` as safety-net filters
- **Next cleaning priority**: intra-document line deduplication and boilerplate stripping, not higher thresholds — threshold-only filtering misses the dominant quality issue (repeated template text within documents)
- **Output standardisation**: all members export profiling summaries with fixed quantiles (p25/p50/p75/p90/p95/p99), before/after comparison tables, rule hit counts (distinguishing overlapping hits from final unique removals), and stratified review samples in CSV format
- **IO timing mandatory**: all notebooks must record and export timing for each pipeline stage to identify bottlenecks early and support scalability analysis
- **Version-tracked iterations**: filtering notebooks should label experiment versions (v1 baseline, v2 refinement) with shard-aligned output naming to prevent result mislabelling

## Action Items

| Action | Owner | Due |
|--------|-------|-----|
| Build three-step content cleaning pipeline (line dedup + boilerplate strip + cross-file URL dedup) | Nuo Chen | 2026-04-06 |
| Complete V2 filtering with threshold sensitivity analysis and full 10-file cross-validation | Xingyu Li | 2026-04-06 |
| Upgrade profiling to standardised quantile metrics + stratified sampling; build 2-round cleaning with versioned outputs | Yingzhe Xu | 2026-04-06 |
| Extend filtering pipeline with low-info keyword check, suspicious URL patterns, repeated-line ratio, HTML residual detection, and domain frequency analysis; record per-operation IO timing | Xiang Chang | 2026-04-06 |
| Build filtering evaluation framework with before/after distribution comparison, per-rule hit analysis, noise-signal metrics, and three-tier sample inspection (cleaned/dropped/borderline) | Wen Sun | 2026-04-06 |

## Progress Summary

> All five team members completed substantial upgrades this week, shifting from Week 2's initial exploration to structured, repeatable experiments with quantitative outputs. The focus was threefold: (1) refining filtering rules with evidence from threshold sensitivity analysis, (2) developing deeper content-level inspection and cleaning beyond basic thresholds, and (3) building evaluation frameworks to objectively compare results. Cross-file validation confirmed that filtering rules generalise well across all 10 parquet shards (keep rate std dev = 0.06%), giving the team confidence in the robustness of the current approach. A key insight emerged from the collective work: the gap between what threshold filters achieve (removing ~3–4% of rows) and what content-level cleaning can achieve (addressing the 57.7% intra-document repetition issue) defines the team's post-Easter roadmap.

## Completed This Week

### Nuo Chen — Content-Level Cleaning Pipeline

Built `cleaner.ipynb`, a three-step cleaning pipeline that goes beyond threshold filtering to address the dominant quality issue: intra-document text repetition.

**Step 1 — Intra-document line deduplication:**
- Split each document into lines and count duplicate occurrences
- If >50% of lines are duplicates → discard entire document (broken or template-only page)
- If 20–50% of lines are duplicates → remove duplicate lines, keep first occurrence
- Rationale: directly targets the 57.7% high-repetition finding from Week 2 profiling

**Step 2 — Boilerplate line stripping:**
- Regex-based pattern matching for common web boilerplate: cookie banners ("accept all cookies", "manage cookies"), privacy notices, navigation links ("skip to content", "toggle menu"), copyright notices ("© 2024", "all rights reserved"), subscription prompts ("subscribe to newsletter")
- Only removes lines that are *entirely* boilerplate — partial matches are preserved to avoid false positives
- If a document becomes <50 characters after stripping → discard (was predominantly boilerplate)

**Step 3 — Cross-file URL deduplication:**
- Maintains a global `URLDeduplicator` set across all files using a streaming approach
- Removes rows where the URL has already been seen in a previous file or row group
- Keeps first occurrence only; prevents the same page appearing across multiple Common Crawl segments

**Result on first 3 files:** 525,214 → 524,934 rows (99.9% keep rate, 280 rows removed). The high keep rate is expected — this pipeline targets specific quality issues (repeated lines, boilerplate, duplicate URLs) rather than broad threshold filtering. The removed rows were confirmed as genuinely low quality through manual spot-checking.

Also wrote `cleaning_report.md` documenting the four-phase roadmap: Phase 1 (line dedup + boilerplate + URL dedup, completed), Phase 2 (content quality scoring with 7 weighted dimensions), Phase 3 (MinHash/LSH near-duplicate detection), Phase 4 (fine-tuning format conversion). Fixed a JupyterHub issue where ipywidgets outputs were not persisted in downloaded .ipynb files by rewriting the notebook to use pure `print()` output.

---

### Xingyu Li — Threshold Sensitivity Analysis & Cross-File Validation

Developed V2 filtering notebook with a rigorous experimental framework: 4 independent threshold rules tested individually before being combined, with full sensitivity analysis and cross-file validation.

**Four independent rules tested:**
| Rule | Description | Rows removed (individual) | Impact |
|------|-------------|--------------------------|--------|
| R1 | `token_count >= 50` | 74 (0.04%) | Negligible — FineWeb already pre-filters short docs |
| R2 | `token_count <= 50,000` | 10 (0.006%) | Negligible — very few extreme outliers |
| R3 | `language_score >= 0.85` | 6,126 (3.55%) | **Dominant** — accounts for >98% of all removals |
| R4 | `text_length >= 200` | 65 (0.04%) | Negligible as safety net |

**Threshold sensitivity analysis (key finding):**
- `language_score` exhibits a steep cliff above 0.85: at 0.90 only 86% of data is retained, at 0.92 only 74%, at 0.95 only 41%
- This confirms 0.85 as a natural inflection point — aggressive enough to remove noise (mixed-language pages, SEO spam, product spec sheets), conservative enough to preserve legitimate content
- `min_tokens` has almost no effect below 50 (dataset minimum is 31); at 100 the keep rate drops to 96%, at 200 it drops to 81%
- The team adopted these findings as the shared threshold baseline

**Cross-file validation:**
- Applied the combined pipeline to all 10 parquet files: keep rate ranges 96.33–96.49%, std dev only 0.06%
- IO timing: ~0.75s read per file, ~4.63s filter per file
- Conclusion: the pipeline generalises perfectly across shards with no overfitting

**Removed records quality inspection:**
- Most removed records are genuinely low quality: mixed-language pages, product spec sheets, SEO spam, e-commerce listings
- Small number of borderline false positives identified: a children's activity blog (lang_score=0.84) and an academic abstract about androgen receptors (lang_score=0.82), flagged because technical jargon lowered language detection confidence
- No threshold adjustment recommended at this stage — these edge cases will be better handled by Phase 2 content quality scoring

Exported: `filtering_summary.csv`, `io_timing.csv`, `cleaned_sample_metadata_200.csv`, `cleaned_sample_with_text_50.csv`, `before_after_distributions.png`, `threshold_sensitivity.png`. Documented all findings in `fineweb_v2_thinking.md`.

---

### Yingzhe Xu — Profiling Framework Upgrade & IO Performance Analysis

Upgraded both the profiling notebook and the filtering notebook from Week 2's exploratory approach to a **reproducible, versioned, quantitatively comparable** framework.

**Profiling notebook upgrades:**
- Replaced basic `describe()` calls with a standardised shard profile system: fixed quantiles (p25/p50/p75/p90/p95/p99) and ratio-based threshold metrics (e.g., `<100 tokens`, `<0.9 language_score`), exported as `profile_summary.csv` and `profile_summary.json` for cross-shard and cross-member comparison
- Replaced outlier-only inspection with **stratified sampling**: review samples are bucketed by text length, language score, and URL pattern, then exported with `manual_label` / `manual_notes` columns to close the loop between automated filtering and manual quality checks

**Cleaning notebook upgrades:**
- Introduced 2-round explainable iterations: **v1** (baseline filters: empty/short text, language confidence, weak URL patterns, template-like pages, exact dedup) and **v2** (refinement targeting long-but-noisy web spam and keyword-based SEO detection)
- Rule reporting now distinguishes **rule hits** (can overlap — a single row may trigger multiple rules) from **final removed total** (non-overlapping count), improving interpretability: "language_score_too_low hit 24,048 rows, but the total unique removed was 30,131" — this tells us how many removals are attributable to multiple issues simultaneously
- Versioned output naming aligned to shard IDs (`cleaning_outputs/<shard>/<version>/...`), preventing mislabelling and enabling clean A/B comparisons

**Critical IO performance finding:**
- On shard `004_00018` (172,447 rows): `read_meta` 0.004s → `load_table` 0.695s → `to_pandas` 0.007s → `feature_engineering` **37.86s**
- Parquet IO is not the bottleneck — it accounts for only **~2% of total runtime**. Feature engineering (Python-level text/URL parsing and per-row computation) accounts for **~98%**
- Implication for scalability: optimising parquet read performance is irrelevant; the team should prioritise reducing per-row Python `apply()` calls, using vectorised string operations, or exploring faster backends (Polars, DuckDB) for the production pipeline

---

### Xiang Chang — Multi-Dimensional Content Inspection & Domain Analysis

Extended the Week 2 pipeline with six new content inspection dimensions, each with per-operation IO timing, providing the most granular view of what "noise" actually looks like in FineWeb data.

**Week 2 baseline (reproduced):**
- English-only filter: 172,447 → 172,447 (0 removed — dataset is 100% English)
- `language_score >= 0.9`: 172,447 → 148,399 (24,048 removed, 13.9%) — note: used a more aggressive threshold (0.9) than the team baseline (0.85), providing useful comparison data
- `text_length >= 200`: 148,399 → 148,391 (8 removed)
- URL dedup: 13 duplicates found; text dedup: 0 exact duplicates found

**Week 3 new inspections:**
| Check | IO time (s) | Key observation |
|-------|-------------|-----------------|
| Low-info keyword check | 6.32s | Pages containing "privacy policy", "cookie policy", "terms of use" — often in otherwise-good content as footer text, not standalone junk pages |
| Suspicious URL patterns | 0.24s | URLs containing "utm_", "tracking", "redirect" — mostly legitimate marketing pages, not necessarily low quality content |
| Very long text (>10k chars) | 0.35s | Mix of genuine long-form content and scraping artefacts |
| Non-alphanumeric ratio >0.3 | **18.43s** | Most expensive check — HTML residuals, code snippets, symbol-heavy pages |
| Repeated line ratio | 1.92s | Corroborates the 57.7% repetition finding — template-heavy pages with nav bars and footers |
| HTML/code residual | 5.51s | Pages with `<div>`, `<script>`, `function()` artefacts — FineWeb's upstream cleaning missed some |
| Domain frequency | 0.31s | Long-tail distribution — no single domain dominates |

**Domain analysis:**
- Exported top 1000 domains before and after filtering, plus 50-row samples from the highest-frequency domain
- Domain distribution follows a long tail — the top domain accounts for a small fraction of total rows, confirming the dataset is not dominated by any single source
- This analysis provides a foundation for domain-based filtering in future phases (e.g., removing known spam domains)

**IO timing insight:**
- Non-alphanumeric ratio check (18.43s) is by far the most expensive operation — consistent with Yingzhe's finding that per-character Python operations dominate runtime
- Keyword and URL pattern checks are cheap (<6.5s combined); domain extraction is nearly free (0.31s)

---

### Wen Sun — Filtering Evaluation Framework

Built a comprehensive evaluation framework (`Filtering_Evaluation.ipynb`) that focuses not just on *what* the filters remove, but on *whether the removals are correct* — providing the team's first systematic quality assurance layer.

**Framework structure:**
1. **Full scan with rule-based classification**: reads the parquet file batch-by-batch, evaluates each row against multiple rules, and classifies every row into cleaned / dropped / borderline categories
2. **Before/after distribution comparison**: side-by-side statistics for `language_score`, `token_count`, and `text_length` across all quantiles — confirming that filtering trims noise without distorting the overall dataset shape
3. **Rule hit analysis**: ranked breakdown showing `language_score < 0.85` dominates (6,126 hits), followed by `token_count > 10,000` (326), `url path blocked` (250), `token_count < 50` (74), `text_length < 200` (65)
4. **Noise-signal comparison**: before/after metrics for boilerplate document ratio (6.06% → 5.97%) and HTML residue ratio (0.05% → 0.04%) — filtering reduces noise but doesn't eliminate it, confirming the need for content-level cleaning
5. **Three-tier sample inspection**: 20 rows each from cleaned, dropped, and borderline (lang_score 0.85–0.90) sets, exported for manual review — this is the team's first structured approach to evaluating false positive / false negative rates

**Key findings:**
- Total filtering result: 172,447 → 165,738 rows (96.11% keep rate, 3.89% dropped)
- Median `language_score` shifted from 0.943 to 0.944 — minimal impact on the core distribution
- Median `token_count` shifted from 487 to 500.5 — filtering preferentially removes shorter, lower-quality documents
- Boilerplate and HTML residue ratios barely changed after threshold filtering — **confirming that these issues require content-level cleaning, not higher thresholds**

Exported 10 output files: `basic_filtering_results.csv`, `before_after_core_stats.csv`, `rule_hit_counts.csv`, `noise_signal_comparison.csv`, `top_domains_before.csv`, `top_domains_after.csv`, `cleaned_samples.csv`, `dropped_samples.csv`, `borderline_samples.csv`, `short_summary.txt`.

---

## Cross-Team Findings Summary

Comparing results across all five members reveals consistent patterns:

| Finding | Confirmed by |
|---------|-------------|
| `language_score` filtering accounts for >95% of row removals | Xingyu, Wen, Xiang, Yingzhe |
| Basic threshold filtering removes only 3–4% of rows | All members |
| FineWeb is 100% English in this subset — no multilingual filtering needed | Xiang, Nuo |
| Intra-document repetition (repeated template lines) is the dominant quality issue | Nuo (57.7%), Xiang (repeated_line_ratio check) |
| Feature engineering dominates runtime (~98%), not Parquet IO | Yingzhe (37.86s vs 0.71s), Xiang (18.43s for non-alnum ratio alone) |
| Filtering trims noise without distorting core distributions | Xingyu (before/after charts), Wen (quantile comparison) |
| No exact text duplicates found; URL duplicates are rare (13 in 148k rows) | Xiang, Yingzhe |

## In Progress

- Consolidating individual filtering thresholds into a shared team configuration based on this week's evidence
- Investigating content-level quality scoring (alphabetic ratio, sentence structure, vocabulary diversity) for Phase 2
- Exploring deduplication strategies beyond URL-level: text-level exact matching and MinHash near-duplicate detection
- Transitioning from individual notebook experimentation toward shared, reusable Python scripts

## Blockers

> The central challenge this week was the gap between what threshold filters can achieve and what the data actually needs. Threshold filtering (primarily `language_score >= 0.85`) removes 3–4% of rows, but the dominant quality issue — 57.7% of documents containing repeated template text — is untouched by thresholds. Raising `language_score` to 0.90 would remove 14% of data but also catch legitimate specialised content (academic text, technical writing). The team's decision to pursue content-level cleaning (line dedup, boilerplate stripping) rather than higher thresholds resolves this, but introduces new implementation complexity: pattern-based cleaning requires careful regex design and per-document processing, which is significantly more expensive computationally than simple column-based threshold filters.
>
> A secondary challenge is IO performance: feature engineering accounts for ~98% of processing time. At 30–40 seconds per shard for feature computation alone, processing the full 60TB dataset (thousands of 2GB shards) at this speed would take days. The team needs to optimise or reduce feature engineering before scaling up.

## Plan for Next Week

- Easter break (2026-04-06 ~ 2026-04-19); Week 4 resumes 2026-04-20
- **Task 1 — Non-Australian signal detection**: design and implement rule-based filters to identify strong foreign-local signals in the Australian subset. Adopt a Level 1 / Level 2 framework — Level 1 for unambiguous signals (e.g., US state + ZIP code combinations, Canadian/UK postcodes, explicit foreign institutional phrases), Level 2 for contextual signals (e.g., `ZIP code` keyword, refined US phone number formats, unambiguous American date formats)
- **Task 2 — Topic distribution analysis**: build a topic classification pipeline for the Australian subset. Start with a TF-IDF + clustering baseline, then improve with dimensionality reduction and prototype-based document classifiers. Design an Australia-relevant topic taxonomy covering areas such as government, health, education, environment, sport, Indigenous affairs, etc.
- Investigate near-duplicate and repeated news content across shards — initial observations suggest significant repetition that could distort topic distributions and bias future model training
- Continue optimising pipeline performance — replace Python `apply()` loops with vectorised operations to address the ~98% feature engineering bottleneck identified this week

## Next Meeting

**Date:** 2026-04-20
🙂
