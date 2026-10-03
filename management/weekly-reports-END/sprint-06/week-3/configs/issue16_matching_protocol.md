# Issue 16 Matched-Granularity Protocol

## Objective

Compare TokenChunker, RecursiveChunker, and SemanticChunker at
approximately comparable observed output granularity.

Configured chunk_size values are not assumed to be directly comparable
across methods.

## Matching Metrics

Matching uses three observed metrics:

1. median chunk character length
2. mean chunk character length
3. mean chunks per document

For each metric:

relative_spread = (maximum - minimum) / mean

across the three selected methods.

## Selection Rule

For each three-method combination:

1. calculate relative spread for all three matching metrics
2. calculate the worst relative spread
3. calculate the mean relative spread

Select configurations by:

1. minimizing worst relative spread
2. breaking ties using mean relative spread

## Matching Target

The target tolerance is:

relative spread <= 30%

for each of the three matching metrics.

The tolerance is frozen before calibration results are inspected.

If the target cannot be achieved, the residual mismatch must be
reported explicitly rather than redefining the tolerance after seeing
the results.

## Initial Anchor

The first calibration stage keeps:

- TokenChunker: token_cs1024
- RecursiveChunker: recursive_cs1024

These settings are used because they are the existing Token and
Recursive settings closest in output scale to the SemanticChunker
range tested so far.

## Semantic Calibration

Only SemanticChunker threshold is changed.

Fixed:

- chunk_size = 2048
- embedding_model = minishlab/potion-base-32M

Coarse calibration thresholds:

- 0.30
- 0.40
- 0.50

The existing threshold 0.70, 0.80, and 0.90 results remain available
from Issue 15.

If the coarse scan brackets a substantially better match but does not
meet the frozen tolerance, a finer threshold scan may be performed.

## Dataset

All calibration and comparison runs use the same frozen 32-document
representative sample:

/home/jovyan/hash_output/_audit/profiling/representative_samples.parquet

## Interpretation Constraint

Matching is used only to reduce output-scale confounding.

It does not imply that matched methods have equivalent quality, semantic
content, or retrieval performance.

## Stage 2 Calibration Amendment

The frozen Semantic coarse scan at thresholds 0.30, 0.40, and 0.50
did not satisfy the three-metric 30% tolerance.

The best coarse Semantic setting was threshold 0.30.

At this setting, RecursiveChunker `recursive_cs1024` and
SemanticChunker `semantic_cal_th030` are already close to the frozen
30% tolerance across:

- median chunk character length
- mean chunk character length
- mean chunks per document

Therefore the second calibration stage keeps fixed:

- RecursiveChunker: `recursive_cs1024`
- SemanticChunker: `semantic_cal_th030`

and performs a narrow TokenChunker calibration.

Only TokenChunker `chunk_size` is changed.

Fixed TokenChunker settings:

- tokenizer = `character`
- chunk_overlap = `0`

The tested TokenChunker chunk sizes are frozen before execution as:

- 836
- 837
- 838
- 839
- 840

The same original matching rule remains unchanged:

1. minimize worst relative spread
2. break ties using mean relative spread
3. target every matching metric at relative spread <= 30%

The 30% tolerance is not changed.

## Stage 3 Minimal Recursive Calibration

After the Stage 2 Token calibration, the best observed combination was:

- TokenChunker: `token_cal_cs839`
- RecursiveChunker: `recursive_cs1024`
- SemanticChunker: `semantic_cal_th030`

The resulting relative spreads were:

- median chunk character length: 29.934066%
- mean chunk character length: 30.040878%
- mean chunks per document: 28.967683%

Only mean chunk character length exceeded the frozen 30% tolerance.

The RecursiveChunker mean chunk character length was 758.036124,
while the feasible lower bound was 758.359511, a residual difference
of only 0.323387 characters.

Therefore the next calibration uses the smallest possible integer
increase in RecursiveChunker chunk_size:

- chunk_size = 1025

Fixed:

- tokenizer = `character`
- min_characters_per_chunk = `24`

The original matching rule and 30% tolerance remain unchanged.

If chunk_size 1025 does not satisfy the frozen tolerance, subsequent
calibration will be determined from the observed result rather than
from an unbounded parameter sweep.

## Final Matched Settings

The frozen 30% matching tolerance was achieved.

Selected runs:

### TokenChunker

- run_id: `token_cal_cs839`
- chunk_size: `839`
- tokenizer: `character`
- chunk_overlap: `0`

### RecursiveChunker

- run_id: `recursive_cal_cs1025`
- chunk_size: `1025`
- tokenizer: `character`
- min_characters_per_chunk: `24`

### SemanticChunker

- run_id: `semantic_cal_th030`
- chunk_size: `2048`
- embedding_model: `minishlab/potion-base-32M`
- threshold: `0.30`

## Final Matching Evidence

Observed matching metrics:

| Metric | Token | Recursive | Semantic | Relative spread |
|---|---:|---:|---:|---:|
| Median chunk characters | 839.000000 | 827.000000 | 612.000000 | 29.894644% |
| Mean chunk characters | 832.019062 | 760.148380 | 1019.330220 | 29.773931% |
| Mean chunks/document | 81.968750 | 89.718750 | 66.906250 | 28.683694% |

Worst relative spread:

`29.894644%`

Frozen tolerance:

`30.000000%`

Status:

`MATCHED`
