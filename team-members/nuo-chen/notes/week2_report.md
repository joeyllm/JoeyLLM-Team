# FineWeb Data Exploration & Cleaning Notes

## Overview

Explored the FineWeb dataset (Common Crawl web text) provided on JupyterHub at `/data/fineweb/`.
The subset contains **10 parquet files**, totalling ~3.66 GB and ~1.67 million rows.

## Dataset Structure

Each parquet file has 9 columns, all slices share the same schema:

| Column | Type | Purpose |
|---|---|---|
| `text` | string | The main web page content |
| `url` | string | Source URL |
| `date` | string | Crawl timestamp |
| `language` | string | Detected language code |
| `language_score` | double | Language detection confidence (0-1) |
| `token_count` | int64 | Number of tokens in the text |
| `id` | string | Unique record ID (URN UUID) |
| `dump` | string | Common Crawl dump identifier |
| `file_path` | string | S3 path of the source WARC file |

Each file contains ~152-181 row groups of ~1000 rows each.

## Key Findings

### Language Distribution
- The entire sample subset is **100% English** (`en`). No multilingual filtering needed for this batch,
  but this should be re-evaluated when working with the full 60TB dataset.

### Token Count Distribution
- Range: 31 to 62,381 tokens
- Median: 489 tokens, Mean: 775 tokens
- Most content (p25-p75) falls between 238-899 tokens
- Long tail: p95 = 2,317 tokens, max = 62,381 tokens
- Very few extremely short documents (only 4 out of 5,000 sampled rows had < 50 tokens)

### Language Score
- Scores are generally high: median = 0.94, p25 = 0.92
- Minimum observed: 0.65
- The data appears to be **pre-filtered** — FineWeb already applies quality filtering upstream

### Data Quality Issues (from 5,000 sampled rows)
- **High repetition**: 2,885 rows (57.7%) — this is the dominant issue, likely pages with repeated
  navigation elements, footers, or template-heavy content
- **Very long (>10k tokens)**: 7 rows — potential scraping artifacts
- **Boilerplate-heavy**: 5 rows — cookie banners, privacy policy text
- **Very short (<50 tokens)**: 4 rows — navigation fragments or error pages

### Cleaning Results
- With default config (min 50 tokens, min 0.65 lang score, min 100 chars), the **keep rate is ~99.8%**.
- FineWeb is already quite clean — most removals are token count outliers.
- The high repetition rate (57.7%) suggests we need a **character-level repetition filter** as an
  additional cleaning step beyond simple threshold filters.

## Design Decisions

### Memory-Efficient Lazy Loading
The original reader loaded entire 2GB files into memory (~4-6GB with pandas conversion).
I redesigned it to read **one row group at a time** (~1000 rows), keeping RAM usage constant
at ~100MB regardless of file size. This is critical for scaling to the full dataset.

### Cleaning Pipeline Architecture
Cleaning is applied per row group with a configurable dict:
```python
CLEAN_CONFIG = {
    'min_tokens': 50,
    'max_tokens': 50000,
    'min_lang_score': 0.65,
    'min_text_length': 100,
    'languages': None,       # e.g. ['en'] to filter
    'dedup_url': True,
}
```
This makes it easy to experiment with different thresholds and reproduce results.

## Next Steps (Post-Easter)

1. **Repetition filter**: The 57.7% high-repetition rate is the biggest quality issue.
   Need to add character n-gram or line-level deduplication within documents.
2. **Cross-file URL dedup**: Current dedup is within each row group. Need global dedup across all files.
3. **Text-level cleaning**: Strip common boilerplate (cookie banners, navigation menus, footers).
4. **Connect to fine-tuning**: Output cleaned text in format suitable for tokenizer/training pipeline.
5. **Scale testing**: Verify the pipeline works on the full dataset (hundreds of 2GB slices).
