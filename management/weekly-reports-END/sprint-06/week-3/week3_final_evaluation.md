# Week 3 Final Chunking Evaluation

## Executive Summary

Week 3 evaluated TokenChunker, RecursiveChunker, and SemanticChunker using a frozen 32-document representative sample from the frozen post-deduplication dataset.

The evaluation covered validated baseline behaviour, an 11-configuration parameter-sensitivity matrix, an approximately matched-granularity comparison, robustness across representative document groups, controlled long-document runtime evidence, computational cost, and the existing Week 2 scaled TokenChunker run.

The evidence shows materially different chunking behaviour across methods, but does not support an overall quality winner. Retrieval-relevance labels and downstream task evaluation are not part of the current evidence set.

All canonical report tables are generated from stored experiment outputs. Displayed values may be rounded for readability; the canonical CSV files retain the source numeric values without report-level rounding.

## 1. Experimental Setup

### Frozen Dataset and Representative Input

The frozen dataset pattern is `/home/jovyan/hash_output/part_*.parquet`.

The preserved full-dataset SHA256 manifest contains 57 entries.

Week 3 uses the frozen representative input `/home/jovyan/hash_output/_audit/profiling/representative_samples.parquet` containing 32 documents.

The representative-input SHA256 was checked during Issue #18 reproducibility freeze and matches the stored Week 3 hash:

`3f94e75b152e2cc41cbddf9b5ad7a6a42477b9627b510db08d91d4e5f6a70caf`

Issue #18 does not rehash the complete approximately 25 GiB dataset; it preserves the existing 57-file dataset manifest as the full-dataset integrity evidence.

### Software Environment

| Component | Version |
|---|---|
| Python | 3.13.15 |
| Chonkie | 1.7.0 |
| model2vec | 0.9.0 |
| PyArrow | 25.0.0 |

### Baseline Configurations

| Method | Frozen baseline configuration |
|---|---|
| token | `{"chunk_overlap":0,"chunk_size":2048,"method":"token","tokenizer":"character"}` |
| recursive | `{"chunk_size":2048,"method":"recursive","min_characters_per_chunk":24,"tokenizer":"character"}` |
| semantic | `{"chunk_size":2048,"embedding_model":"minishlab/potion-base-32M","method":"semantic","threshold":0.8}` |

### Evaluation Dimensions

The frozen evaluation specification covers output validity, chunks per document, chunk character length, chunk token count, boundary classification, representative sample groups, runtime, warnings, failures, and QA.

Internal boundaries are classified as `paragraph_boundary`, `newline_boundary`, `sentence_boundary`, `whitespace_boundary`, or `other_boundary`; `document_end` is tracked separately.

Configured chunk sizes are not assumed to be equivalent across methods. Raw chunk count is not treated as a quality metric.

**Evidence:** `week3/configs/environment_snapshot.json`, `week3/configs/baseline_configs.json`, `week3/configs/experimental_constants.json`, `week3/week3_experiment_plan.md`, `week3/configs/evaluation_metric_spec.md`, `week3/reports/issue18_reproducibility_freeze.json`

## 2. Baseline Results

### Results

| Method | Chunks | Mean chunks/doc | Median chars | Mean chars | Newline | Sentence | Whitespace | Other | Seconds | Warnings | QA |
|---|---|---|---|---|---|---|---|---|---|---|---|
| token | 1078 | 33.688 | 2048.000 | 2024.477 | 0.29% | 1.24% | 17.02% | 81.45% | 0.260699 | 0 | pass |
| recursive | 1272 | 39.750 | 1826.000 | 1715.712 | 97.50% | 2.50% | 0.00% | 0.00% | 0.075861 | 0 | pass |
| semantic | 5629 | 175.906 | 257.000 | 387.704 | 42.29% | 57.71% | 0.00% | 0.00% | 3.220511 | 1 | pass |

### Interpretation

TokenChunker at the 2048-character baseline produced fixed-size-like chunks: its median chunk character length was 2048.000, and most internal boundaries were classified as `other_boundary` or `whitespace_boundary`.

RecursiveChunker at the same configured chunk size produced a different boundary profile. Its internal boundaries were predominantly newline boundaries, showing that equal configured chunk size does not imply equivalent output structure.

SemanticChunker produced substantially more and shorter chunks on this representative sample. Its internal boundaries were concentrated on sentence and newline boundaries. The baseline SemanticChunker run recorded one numerical warning while still completing with zero processing failures and QA status `pass`.

Because TokenChunker and RecursiveChunker use the character tokenizer while SemanticChunker uses its Model2Vec tokenizer, chunk token-count statistics are not used as direct cross-method quality comparisons.

**Evidence:** `week3/reports/tables/baseline_results.csv`

## 3. Parameter Sensitivity

### Results

| Run | Method | Axis | Chunk size | Threshold | Chunks | Mean chunks/doc | Median chars | Mean chars | Seconds | Warnings | QA |
|---|---|---|---|---|---|---|---|---|---|---|---|
| token_cs1024 | token | chunk_size | 1024 | — | 2144 | 67.000 | 1024.000 | 1017.904 | 0.275721 | 0 | pass |
| token_cs2048 | token | chunk_size | 2048 | — | 1078 | 33.688 | 2048.000 | 2024.477 | 0.260699 | 0 | pass |
| token_cs4096 | token | chunk_size | 4096 | — | 546 | 17.062 | 4096.000 | 3997.044 | 0.261970 | 0 | pass |
| recursive_cs1024 | recursive | chunk_size | 1024 | — | 2879 | 89.969 | 824.000 | 758.036 | 0.096994 | 0 | pass |
| recursive_cs2048 | recursive | chunk_size | 2048 | — | 1272 | 39.750 | 1826.000 | 1715.712 | 0.075861 | 0 | pass |
| recursive_cs4096 | recursive | chunk_size | 4096 | — | 594 | 18.562 | 3844.000 | 3674.051 | 0.066561 | 0 | pass |
| semantic_cs1024 | semantic | chunk_size | 1024 | 0.8 | 5630 | 175.938 | 257.000 | 387.635 | 3.286211 | 1 | pass |
| semantic_cs2048 | semantic | chunk_size | 2048 | 0.8 | 5629 | 175.906 | 257.000 | 387.704 | 3.220511 | 1 | pass |
| semantic_cs4096 | semantic | chunk_size | 4096 | 0.8 | 5629 | 175.906 | 257.000 | 387.704 | 3.144583 | 1 | pass |
| semantic_th070 | semantic | threshold | 2048 | 0.7 | 4930 | 154.062 | 283.000 | 442.675 | 3.322987 | 1 | pass |
| semantic_th090 | semantic | threshold | 2048 | 0.9 | 6325 | 197.656 | 232.000 | 345.041 | 3.140238 | 1 | pass |

### Interpretation

For TokenChunker, increasing `chunk_size` from 1024 to 2048 to 4096 reduced total chunks from 2144 to 1078 to 546, while mean chunk character length increased from 1017.904 to 2024.477 to 3997.044.

RecursiveChunker shows the same directional granularity response to chunk size: total chunks changed from 2879 at 1024 to 1272 at 2048 and 594 at 4096.

SemanticChunker behaved differently on the frozen sample. At threshold 0.8, changing configured chunk size from 1024 to 2048 to 4096 produced 5630, 5629, and 5629 chunks respectively, so chunk-size changes had little observed effect over this range.

Semantic threshold was more influential: at chunk size 2048, threshold 0.7 produced 4930 chunks, threshold 0.8 produced 5629, and threshold 0.9 produced 6325. Mean chunk character length moved in the opposite direction as the threshold increased.

These are within-method parameter effects. They do not establish a cross-method quality ordering.

**Evidence:** `week3/reports/tables/parameter_sensitivity.csv`

## 4. Matched-Granularity Comparison

### Matching Procedure

The selected settings minimize the worst relative spread over three matching metrics: median chunk character length, mean chunk character length, and mean chunks per document. Relative spread is defined as `(max - min) / mean`.

The frozen matching tolerance is 30.0%.

The selected settings achieved a worst observed relative spread of 29.895%.

### Selected Configurations

| Method | Run | Configuration |
|---|---|---|
| token | token_cal_cs839 | `{"chunk_overlap":0,"chunk_size":839,"method":"token","run_id":"token_cal_cs839","tokenizer":"character"}` |
| recursive | recursive_cal_cs1025 | `{"chunk_size":1025,"method":"recursive","min_characters_per_chunk":24,"run_id":"recursive_cal_cs1025","tokenizer":"character"}` |
| semantic | semantic_cal_th030 | `{"chunk_size":2048,"embedding_model":"minishlab/potion-base-32M","method":"semantic","run_id":"semantic_cal_th030","threshold":0.3}` |

### Results

| Method | Chunks | Mean chunks/doc | Median chars | Mean chars | Small <256 | Newline | Sentence | Whitespace | Other | Seconds | Warnings | QA |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| token | 2623 | 81.969 | 839.000 | 832.019 | 0.76% | 0.35% | 1.04% | 16.83% | 81.78% | 0.288113 | 0 | pass |
| recursive | 2871 | 89.719 | 827.000 | 760.148 | 4.46% | 88.66% | 11.31% | 0.00% | 0.04% | 0.110693 | 0 | pass |
| semantic | 2141 | 66.906 | 612.000 | 1019.330 | 26.53% | 47.46% | 52.54% | 0.00% | 0.00% | 3.056384 | 1 | pass |

### Interpretation

Approximate aggregate granularity matching does not remove structural differences. TokenChunker remains dominated by `other_boundary` and whitespace endings, RecursiveChunker remains predominantly newline-aligned, and SemanticChunker remains split between sentence and newline boundaries.

Under the frozen `char_length < 256` fragmentation definition, the matched runs also retain different very-small-chunk frequencies. These values are descriptive fragmentation evidence rather than a direct quality score.

All three matched runs processed all 32 source documents with zero processing failures and QA status `pass`. The matched SemanticChunker run retained one warning.

**Evidence:** `week3/configs/issue16_matched_settings.json`, `week3/reports/tables/matched_granularity.csv`

## 5. Robustness

### Representative-Group Results

The representative sample contains ten overlapping profiling groups. Group overlap is preserved rather than deduplicated.

| Group | Method | Docs | Chunks/doc | Median chars | Small <256 | Newline | Sentence | Whitespace | Other |
|---|---|---|---|---|---|---|---|---|---|
| high_chars_per_token | token | 4 | 11.500 | 839.000 | 4.35% | 2.38% | 0.00% | 9.52% | 88.10% |
| length_max | token | 3 | 704.333 | 839.000 | 0.09% | 0.33% | 1.18% | 16.68% | 81.80% |
| length_median | token | 3 | 9.000 | 839.000 | 11.11% | 0.00% | 0.00% | 16.67% | 83.33% |
| length_min | token | 3 | 2.333 | 839.000 | 14.29% | 0.00% | 0.00% | 0.00% | 100.00% |
| length_p05 | token | 3 | 6.000 | 839.000 | 0.00% | 0.00% | 0.00% | 20.00% | 80.00% |
| length_p90 | token | 3 | 20.000 | 839.000 | 5.00% | 0.00% | 0.00% | 21.05% | 78.95% |
| length_p95 | token | 3 | 30.000 | 839.000 | 3.33% | 1.15% | 1.15% | 20.69% | 77.01% |
| length_p99 | token | 3 | 71.000 | 839.000 | 0.00% | 0.00% | 0.48% | 16.19% | 83.33% |
| low_chars_per_token | token | 4 | 3.750 | 839.000 | 13.33% | 0.00% | 0.00% | 18.18% | 81.82% |
| no_newline | token | 4 | 9.000 | 839.000 | 11.11% | 0.00% | 0.00% | 21.88% | 78.12% |
| high_chars_per_token | recursive | 4 | 12.500 | 807.000 | 10.00% | 78.26% | 21.74% | 0.00% | 0.00% |
| length_max | recursive | 3 | 781.000 | 819.000 | 4.40% | 90.68% | 9.32% | 0.00% | 0.00% |
| length_median | recursive | 3 | 8.667 | 845.500 | 3.85% | 95.65% | 4.35% | 0.00% | 0.00% |
| length_min | recursive | 3 | 2.000 | 859.000 | 0.00% | 100.00% | 0.00% | 0.00% | 0.00% |
| length_p05 | recursive | 3 | 6.333 | 712.000 | 5.26% | 93.75% | 6.25% | 0.00% | 0.00% |
| length_p90 | recursive | 3 | 20.000 | 860.000 | 3.33% | 92.98% | 7.02% | 0.00% | 0.00% |
| length_p95 | recursive | 3 | 28.000 | 906.000 | 0.00% | 100.00% | 0.00% | 0.00% | 0.00% |
| length_p99 | recursive | 3 | 80.000 | 830.000 | 5.83% | 77.64% | 21.94% | 0.00% | 0.42% |
| low_chars_per_token | recursive | 4 | 3.250 | 887.000 | 7.69% | 22.22% | 77.78% | 0.00% | 0.00% |
| no_newline | recursive | 4 | 8.000 | 912.000 | 3.12% | 0.00% | 100.00% | 0.00% | 0.00% |
| high_chars_per_token | semantic | 4 | 10.250 | 808.000 | 12.20% | 43.24% | 56.76% | 0.00% | 0.00% |
| length_max | semantic | 3 | 554.000 | 622.000 | 26.11% | 47.38% | 52.62% | 0.00% | 0.00% |
| length_median | semantic | 3 | 8.000 | 409.000 | 29.17% | 61.90% | 38.10% | 0.00% | 0.00% |
| length_min | semantic | 3 | 3.000 | 412.000 | 22.22% | 100.00% | 0.00% | 0.00% | 0.00% |
| length_p05 | semantic | 3 | 6.000 | 723.500 | 22.22% | 40.00% | 60.00% | 0.00% | 0.00% |
| length_p90 | semantic | 3 | 24.333 | 394.000 | 36.99% | 52.86% | 47.14% | 0.00% | 0.00% |
| length_p95 | semantic | 3 | 34.333 | 393.000 | 36.89% | 68.00% | 32.00% | 0.00% | 0.00% |
| length_p99 | semantic | 3 | 55.667 | 725.000 | 23.95% | 42.07% | 57.93% | 0.00% | 0.00% |
| low_chars_per_token | semantic | 4 | 3.500 | 644.500 | 35.71% | 10.00% | 90.00% | 0.00% | 0.00% |
| no_newline | semantic | 4 | 8.000 | 616.000 | 21.88% | 0.00% | 100.00% | 0.00% | 0.00% |

### Long-Document Behaviour

| Group | Method | Chunks/doc | Median chars | Mean chars | Small <256 |
|---|---|---|---|---|---|
| length_p95 | token | 30.000 | 839.000 | 813.167 | 3.33% |
| length_p95 | recursive | 28.000 | 906.000 | 871.250 | 0.00% |
| length_p95 | semantic | 34.333 | 393.000 | 710.534 | 36.89% |
| length_p99 | token | 71.000 | 839.000 | 835.577 | 0.00% |
| length_p99 | recursive | 80.000 | 830.000 | 741.575 | 5.83% |
| length_p99 | semantic | 55.667 | 725.000 | 1065.737 | 23.95% |
| length_max | token | 704.333 | 839.000 | 838.322 | 0.09% |
| length_max | recursive | 781.000 | 819.000 | 756.029 | 4.40% |
| length_max | semantic | 554.000 | 622.000 | 1065.809 | 26.11% |

### Controlled Long-Document Runtime

| Group | Method | Docs | Input chars | Chunks | Seconds | Seconds/doc | Warnings | QA |
|---|---|---|---|---|---|---|---|---|
| length_p95 | token | 3 | 73185 | 90 | 0.017351 | 0.005784 | 0 | pass |
| length_p95 | recursive | 3 | 73185 | 84 | 0.009500 | 0.003167 | 0 | pass |
| length_p95 | semantic | 3 | 73185 | 103 | 0.130052 | 0.043351 | 0 | pass |
| length_p99 | token | 3 | 177978 | 213 | 0.030785 | 0.010262 | 0 | pass |
| length_p99 | recursive | 3 | 177978 | 240 | 0.016151 | 0.005384 | 0 | pass |
| length_p99 | semantic | 3 | 177978 | 167 | 0.270322 | 0.090107 | 0 | pass |
| length_max | token | 3 | 1771375 | 2113 | 0.235517 | 0.078506 | 0 | pass |
| length_max | recursive | 3 | 1771375 | 2343 | 0.078265 | 0.026088 | 0 | pass |
| length_max | semantic | 3 | 1771375 | 1662 | 2.395008 | 0.798336 | 0 | pass |

### Interpretation

The representative groups show that aggregate matching does not imply subgroup matching. Document length, newline structure, and chars-per-stored-token profile remain associated with different output patterns.

The `no_newline` cases are particularly useful for separating newline-dependent behaviour from other boundary mechanisms: RecursiveChunker cannot rely on newline boundaries in those documents, while sentence-boundary behaviour becomes more visible.

P95, P99, and maximum-length controlled runs all completed with zero processing failures and QA status `pass`. Runtime increases on larger inputs, but these are single-run descriptive pipeline measurements, not statistically repeated benchmarks.

**Evidence:** `week3/reports/tables/robustness_summary.csv`, `week3/reports/tables/long_document_runtime.csv`

## 6. Computational Cost

### Matched 32-Document Runs

| Method | Docs | Chunks | Seconds | Seconds/doc | Docs/s | Chunks/s | Output bytes | Warnings |
|---|---|---|---|---|---|---|---|---|
| token | 32 | 2623 | 0.288113 | 0.009004 | 111.068 | 9104.079 | 855496 | 0 |
| recursive | 32 | 2871 | 0.110693 | 0.003459 | 289.088 | 25936.585 | 883148 | 0 |
| semantic | 32 | 2141 | 3.056384 | 0.095512 | 10.470 | 700.501 | 874593 | 1 |

### Week 2 Scaled TokenChunker Evidence

| Method | Docs | Chunks | Failures | Seconds | Docs/s | Chunks/s | Output bytes | Max RSS KB | QA |
|---|---|---|---|---|---|---|---|---|---|
| token | 227628 | 1334973 | 0 | 344.772837 | 660.226 | 3872.036 | 1104574318 | 1512640 | pass |

### Interpretation

The matched 32-document runs show substantial differences in observed pipeline runtime and throughput. SemanticChunker uses the local `minishlab/potion-base-32M` embedding path and has higher observed elapsed time in these experiments.

These timings are pipeline-level engineering measurements. They should not be decomposed into pure algorithmic cost, model-loading cost, or I/O cost without additional instrumentation.

Memory was not measured for the three matched Issue #16 runs or the Issue #17 controlled long-document runs.

The directly recorded Week 2 scaled TokenChunker resource measurement is `max_rss_kb=1512640`. That value applies only to the scaled TokenChunker run and is not extrapolated to other methods.

The Week 2 scaled run also uses a different TokenChunker configuration from the Issue #16 matched run, so it is supporting engineering-scale evidence rather than a matched-method comparison.

**Evidence:** `week3/reports/tables/computational_cost.csv`, `week3/reports/tables/scaled_engineering_evidence.csv`

## 7. Reliability and QA

### Results

The canonical reliability table contains 24 stored run records. Every inventoried run metadata record has `status=completed`, every run has zero processing failures, and every associated QA summary has status `pass`.

The standard QA records report zero hard-failure events where that field is present. The Week 2 scaled QA uses a different validation schema, so missing fields are not silently converted to zero.

Across records with an explicit warning count, 6 warning event(s) were recorded.

| Evidence | Warnings | Failures | QA |
|---|---|---|---|
| baseline.semantic | 1 | 0 | pass |
| issue15.semantic_cs1024 | 1 | 0 | pass |
| issue15.semantic_cs4096 | 1 | 0 | pass |
| issue15.semantic_th070 | 1 | 0 | pass |
| issue15.semantic_th090 | 1 | 0 | pass |
| issue16.semantic_cal_th030 | 1 | 0 | pass |

Warning count is not recorded in the QA schema for: `week2.scaled_token`.

### Source and Provenance Integrity

QA validates stored chunk outputs against source provenance. Across the accepted evidence, source-slice integrity, document identity, required provenance, and index validation pass according to the stored QA summaries.

The representative sample hash remains unchanged from the frozen Week 3 input hash. The complete post-deduplication dataset is covered by the preserved 57-entry SHA256 manifest.

**Evidence:** `week3/reports/tables/reliability_qa.csv`, `week3/reports/issue18_evidence_inventory.json`, `week3/reports/issue18_reproducibility_freeze.json`

## 8. Limitations

1. **Tokenizer semantics differ across methods.** TokenChunker and RecursiveChunker use the character tokenizer in the tested configurations, whereas SemanticChunker uses its local Model2Vec tokenizer. Token-count statistics therefore are not directly comparable quality units.

2. **The representative set is small.** Most profiling groups contain only a few documents, and groups may overlap. Group-level statistics are descriptive rather than population estimates.

3. **Matched granularity is approximate.** The frozen tolerance is 30%, and the selected settings still retain measurable residual differences at both aggregate and subgroup levels.

4. **Retrieval relevance labels are absent from the current canonical evidence.** Therefore the study does not establish which method produces better retrieval or downstream task quality.

5. **SemanticChunker numerical warnings are present in several stored runs.** They are recorded separately from processing failures; the affected runs still pass QA.

6. **Full-scale cross-method testing is limited.** The available 227,628-document scaled evidence is for TokenChunker only. RecursiveChunker and SemanticChunker were not run over the same scaled corpus during this sprint.

7. **Runtime evidence is descriptive.** The principal runtime measurements are single pipeline runs, not repeated benchmark distributions. Pipeline timings also combine multiple operational costs.

8. **Memory evidence is incomplete across methods.** A recorded maximum RSS is available for the Week 2 scaled TokenChunker run only.

9. **The Git repository currently has an unborn HEAD.** The reproducibility freeze records branch `main`, the working-tree state, and the absence of a resolvable commit hash rather than inventing one.

**Evidence:** `week3/reports/tables/week3_canonical_summary.json`, `week3/reports/issue18_reproducibility_freeze.json`

## 9. Conclusions

### Evidence-Supported Trade-offs

**TokenChunker:** chunk size provides a direct and predictable granularity control under the character-tokenizer configuration. Its tested boundaries frequently terminate at whitespace or positions classified as `other_boundary`, reflecting its fixed-size behaviour.

**RecursiveChunker:** chunk size also strongly controls granularity, while the method makes much greater use of newline structure in the tested corpus. Its output therefore differs structurally from TokenChunker even when the configured or observed granularity is similar.

**SemanticChunker:** configured chunk size between 1024 and 4096 had little observed granularity effect at threshold 0.8 on the representative sample, whereas threshold changes materially altered chunk count and chunk length. The method more often ended chunks on sentence/newline boundaries, produced more very small chunks under the matched setting, and incurred higher observed pipeline runtime in the collected evidence.

Across all three methods, long-document and representative-group results show that aggregate statistics alone are insufficient to characterize robustness. Document structure changes the observed behaviour.

The evidence therefore supports a set of method-specific trade-offs rather than an overall winner.

### Evidence Required for Stronger Claims

Stronger chunk-quality conclusions would require retrieval-relevance labels or downstream task evaluation, larger and independent representative samples, repeated runtime/resource measurements, and scaled processing evidence for RecursiveChunker and SemanticChunker under comparable conditions.

## Reproducibility and Evidence Paths

Canonical report tables are stored under `week3/reports/tables/`.

The final evidence inventory is `week3/reports/issue18_evidence_inventory.json`.

The reproducibility freeze is `week3/reports/issue18_reproducibility_freeze.json`.

The human-readable comparison-table index is `week3/reports/final_comparison_tables.md`.

The report traceability manifest is `week3/reports/report_traceability.json`.

**Status:** Week 3 evidence consolidated; ready for final reproducibility and report consistency audit.
