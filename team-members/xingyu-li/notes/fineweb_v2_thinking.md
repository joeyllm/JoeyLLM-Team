# Week 03 FineWeb Filtering & Cleaning Notes

## Task Understanding
This week builds directly on V1 exploration. The stakeholder (Matty) reviewed Week 02 work and asked for three specific improvements: clearer written insights on what worked and what didn't, more repeatable filtering experiments, and stronger notebook annotations and outputs. The overall direction remains the same — continue data exploration and cleaning on the 10-file FineWeb subset, refine filtering approaches, and track IO timing.

## What I Did in V2
In this notebook version, I:
- defined 4 threshold-based filtering rules motivated by V1 findings,
- ran each rule independently to measure its individual impact,
- applied all rules as a combined pipeline with step-by-step removal tracking,
- built a before/after comparison table and distribution charts (token count, language score, text length),
- inspected 10 randomly sampled removed records to check for false positives,
- conducted threshold sensitivity analysis on language_score (0.65–0.95) and min_tokens (10–200),
- applied the full pipeline to all 10 parquet files to verify cross-file consistency,
- output cleaned CSV samples and pipeline summary files,
- tracked IO timing for all read and filter operations.

## Key Findings

### Filter Impact
- R3 (language_score >= 0.85) is the dominant filter, removing 6,126 rows (3.55%) on its own — over 98% of all removals.
- R1 (min tokens >= 50) removed only 74 rows (0.04%), R2 (max tokens <= 50,000) removed 10, and R4 (min text length >= 200 chars) removed 65.
- Combined pipeline: 172,447 → 166,278 rows, total removal rate 3.58%.

### Threshold Sensitivity
- Language score is highly sensitive above 0.85: at 0.90 only 86% kept, at 0.92 only 74%, at 0.95 only 41%. The 0.85 threshold sits at a natural inflection point.
- Min tokens has almost no effect below 50 (the dataset minimum is 31). At 100 the keep rate drops to 96%, at 200 it drops to 81%.
- Current thresholds (lang_score >= 0.85, min_tokens >= 50) are well-positioned — aggressive enough to remove noise, conservative enough to preserve good data.

### Removed Records Quality
- Most removed records are genuinely low quality: mixed-language pages, product spec sheets, SEO spam, e-commerce listings.
- A small number of borderline false positives exist: a children's activity blog (lang_score=0.84), an academic abstract about androgen receptors (lang_score=0.82). These were flagged because technical jargon or informal language lowered the language detection confidence.
- No threshold adjustment recommended at this stage.

### Cross-File Consistency
- Keep rate across all 10 files: 96.33% to 96.49%, standard deviation 0.06%.
- IO timing: read ~0.75s per file, filter ~4.63s per file. Filter time is dominated by the text_length string computation.
- The pipeline generalises perfectly across all shards.

### Before/After Distribution
- Core distributions (p25–p75) are nearly unchanged after filtering.
- Main effects: lower tail of language_score removed (min raised from 0.65 to 0.85), extreme token count outliers capped (max dropped from 103,654 to 46,866).
- The filtering trims noise without distorting the overall dataset shape.

## What Worked
- The repeatable experiment framework made it easy to compare rules and thresholds objectively.
- Sensitivity analysis gave clear evidence for why 0.85 is the right language_score cutoff.
- Cross-file validation confirmed the rules are not overfitting to one shard.
- Outputting cleaned CSV samples makes the work concrete and verifiable.

## What Didn't Work (or Was Surprising)
- R1 and R4 barely removed anything — FineWeb is already pre-filtered for very short documents. These rules are useful as safety nets but have almost zero independent impact.
- The steep drop-off above lang_score 0.85 was more dramatic than expected. Moving to 0.90 would remove 14% of data, which is much more aggressive than it sounds.
- The filter step (~4.6s) is significantly slower than the read step (~0.75s), mainly due to computing text_length via string operations on the text column.

## What Is Still Incomplete
- No content-level quality scoring yet (e.g., alphabetic ratio, sentence length, vocabulary diversity).
- No duplicate detection (text-level or URL-level).
- Borderline false positive cases not yet resolved — may need domain-specific rules.
- No connection to downstream training data preparation yet.

## Next Steps (Post-Easter)
1. Implement the team's proposed content quality scoring system (composite score from multiple linguistic signals).
2. Add deduplication as a complementary filtering step.
3. Investigate whether a slightly lower language_score threshold (e.g., 0.82) better serves specialised content like academic text.
4. Begin connecting the cleaned dataset to training data preparation workflows.
5. Transition from notebook experimentation to reusable Python scripts for production runs.
