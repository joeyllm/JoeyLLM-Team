## Data exploration: ##
Inspected a FineWeb parquet shard (one row = one web document) and reviewed key fields (text, url, date, language, language_score, token_count, id). Observed mixed quality: article-like pages plus thin/template/navigation pages; URL patterns also indicate weak-content pages (e.g., tag/category/author/page).

## Cleaning workflow: Built an interpretable, rule-based filter:##
- remove empty/near-empty and very short texts (token_count),
- filter by language confidence (language, language_score),
- filter weak-content URL patterns,
- remove template-like text,
- exact dedup by id/url/text,
- with logging of removal reasons.

## Evaluation: ##
Compared before vs after using retention rate, length distribution, language-score distribution, duplication rate, source/URL-pattern changes, plus small manual sample checks.