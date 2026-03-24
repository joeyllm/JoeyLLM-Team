# FineWeb Data Cleaning Report

**Author**: Nuo Chen
**Date**: 2026-03-24
**Dataset**: FineWeb (HuggingFace) — Common Crawl web text, CC-MAIN-2025-26

---

## 1. Dataset Overview

| Metric | Value |
|---|---|
| Total files | 10 parquet slices |
| Total size | ~3.66 GB |
| Total rows | ~1.67 million |
| Columns | 9 (text, url, date, language, language_score, token_count, id, dump, file_path) |
| Language | 100% English |
| Token count range | 31 — 62,381 (median: 489) |

FineWeb is a pre-filtered dataset from HuggingFace, already cleaned from raw Common Crawl.
However, our quality assessment revealed that further cleaning is needed before fine-tuning.

## 2. Quality Issues Identified

From profiling 5,000 sampled rows:

| Issue | Count | % | Severity |
|---|---|---|---|
| High character repetition | 2,885 | 57.7% | High |
| Very long text (>10k tokens) | 7 | 0.14% | Low |
| Boilerplate-heavy | 5 | 0.1% | Medium |
| Very short (<50 tokens) | 4 | 0.08% | Low |

**Key finding**: The dominant quality issue is **intra-document repetition** — web pages
containing repeated navigation bars, sidebar links, and footer text. These inflate token
counts and would introduce noisy patterns during fine-tuning.

## 3. Phase 1 Cleaning (Pre-Easter) — Completed

### 3.1 Approach

Three targeted cleaning operations, chosen for high impact and low risk:

**Step 1: Intra-document line deduplication**
- Split each document into lines, count duplicate occurrences
- If >50% of lines are duplicates → discard entire document (broken/template page)
- If >20% of lines are duplicates → remove duplicate lines, keep first occurrence
- Rationale: Directly addresses the 57.7% repetition issue without losing real content

**Step 2: Boilerplate line stripping**
- Pattern-match common web boilerplate: cookie banners, privacy notices,
  navigation links, "subscribe" prompts, copyright notices
- Only remove lines that are *entirely* boilerplate (not partial matches)
- If document becomes <50 chars after stripping → discard (was mostly boilerplate)
- Rationale: Removes non-content text that would teach the model web UI patterns

**Step 3: Cross-file URL deduplication**
- Maintain a global set of seen URLs across all 10 files
- Remove rows where the URL has already been seen in a previous file/row group
- Keep the first occurrence only
- Rationale: Same page can appear in multiple crawl segments

### 3.2 Post-Cleaning Filters

After text-level cleaning, apply threshold filters:
- Minimum 50 tokens
- Minimum 0.65 language score
- Minimum 100 characters of text remaining

### 3.3 Design Decision: Memory Efficiency

Each parquet file is ~380MB with ~173 row groups of ~1000 rows. Loading an entire file
into memory would require 2-4GB RAM. Instead, we process **one row group at a time**,
keeping RAM usage constant at ~100MB regardless of file size. This same approach will
scale to the full 60TB dataset.

## 4. Phase 2 Plan (Post-Easter) — Content Quality Scoring

### 4.1 Motivation

After removing obvious duplicates and boilerplate, the remaining data still varies
significantly in quality. A web page might pass all threshold filters but contain:
- Low-information content (product listings, auto-generated pages)
- Poorly structured text (no paragraph breaks, inconsistent formatting)
- SEO-optimized filler text
- Machine-translated content that scored high on language detection

We need a **content quality scoring system** that evaluates each document on multiple
linguistic signals and assigns a composite score.

### 4.2 Proposed Scoring Dimensions

| Signal | What it measures | How to compute | Expected threshold |
|---|---|---|---|
| **Alphabetic ratio** | Whether content is actual text vs code/numbers/symbols | `sum(c.isalpha()) / len(text)` | > 0.6 |
| **Average sentence length** | Whether text has proper sentence structure | Split on `.!?`, compute mean word count | 8 — 40 words |
| **Punctuation density** | Whether text reads like natural prose | `count(.,;:!?) / len(text)` | > 0.01 |
| **Uppercase ratio** | Detect ALL-CAPS spam or headers-only pages | `sum(c.isupper()) / sum(c.isalpha())` | < 0.3 |
| **Unique word ratio** | Vocabulary diversity, catches repetitive content | `len(set(words)) / len(words)` | > 0.2 |
| **Line length variance** | Detect structured prose vs fragmented lists | `std(line_lengths)` | context-dependent |
| **Stop word ratio** | Natural language has predictable stop word frequency | `count(stop_words) / len(words)` | 0.1 — 0.5 |

### 4.3 Scoring Architecture

```python
def quality_score(text) -> float:
    """Compute composite quality score (0.0 — 1.0) from multiple signals."""
    scores = {
        'alpha_ratio':    score_alpha_ratio(text),      # weight: 0.20
        'sentence_len':   score_sentence_length(text),   # weight: 0.20
        'punct_density':  score_punctuation(text),       # weight: 0.15
        'uppercase':      score_uppercase(text),         # weight: 0.10
        'vocab_diversity': score_vocab_diversity(text),  # weight: 0.15
        'line_variance':  score_line_variance(text),     # weight: 0.10
        'stop_words':     score_stop_words(text),        # weight: 0.10
    }
    weights = [0.20, 0.20, 0.15, 0.10, 0.15, 0.10, 0.10]
    return sum(s * w for s, w in zip(scores.values(), weights))
```

Each sub-scorer returns 0.0 — 1.0. The composite score is a weighted average.
Documents below a tunable threshold (e.g., 0.4) are filtered out.

### 4.4 Calibration Strategy

1. Manually label ~200 documents as "high quality" / "low quality" / "borderline"
2. Compute quality scores on all 200
3. Tune weights and thresholds to maximize agreement with manual labels
4. Apply to full dataset and spot-check results

This avoids over-fitting to any single heuristic and produces interpretable scores.

## 5. Phase 3 Plan — MinHash Near-Duplicate Detection

### 5.1 Motivation

URL deduplication only catches exact same pages. In practice, many web pages are
**near-duplicates**: slightly different versions of the same content (e.g., same article
on different subdomains, cached copies, syndicated content with minor edits).

Training on near-duplicates wastes compute and can bias the model toward over-represented content.

### 5.2 Approach: MinHash + LSH

**MinHash** (Min-wise Independent Permutations) is the standard technique for
large-scale near-duplicate detection:

1. **Shingling**: Convert each document into a set of character n-grams (e.g., 5-grams)
2. **MinHash signature**: Compute a fixed-size signature (e.g., 128 hash values) that
   approximates the Jaccard similarity between any two documents
3. **LSH (Locality-Sensitive Hashing)**: Hash signatures into buckets so that similar
   documents land in the same bucket with high probability
4. **Cluster & deduplicate**: Within each bucket, compute exact Jaccard similarity.
   Keep one representative document per cluster.

### 5.3 Why MinHash over Exact Hashing

| Method | Catches | Misses | Scalability |
|---|---|---|---|
| Exact hash (MD5/SHA) | Byte-identical copies | Any edit breaks the hash | Excellent |
| URL dedup | Same-URL duplicates | Different URLs, same content | Excellent |
| **MinHash + LSH** | Near-duplicates (>80% similar) | Low-similarity paraphrases | Good (sublinear) |
| Embedding similarity | Semantic duplicates | — | Poor (O(n^2) or approximate) |

MinHash is the right trade-off: it catches the near-duplicates that matter for training
data quality, while remaining computationally feasible for millions of documents.

### 5.4 Implementation Plan

```python
# Using the datasketch library
from datasketch import MinHash, MinHashLSH

lsh = MinHashLSH(threshold=0.8, num_perm=128)  # 80% Jaccard similarity

for doc_id, text in iterate_all_docs():
    mh = MinHash(num_perm=128)
    for shingle in ngrams(text, n=5):
        mh.update(shingle.encode('utf-8'))

    # Check for near-duplicates
    duplicates = lsh.query(mh)
    if not duplicates:
        lsh.insert(doc_id, mh)  # keep this document
    # else: skip (near-duplicate of an existing document)
```

### 5.5 Expected Impact

Based on similar work on Common Crawl data (e.g., the C4 dataset paper, RefinedWeb),
near-duplicate removal typically reduces dataset size by **5-15%** while significantly
improving training efficiency and model quality.

## 6. Phase 4 Plan — Fine-Tuning Pipeline Integration

### 6.1 Overview

The goal is to connect cleaned data directly to a training pipeline:

```
Raw Parquet → Phase 1 (dedup/boilerplate) → Phase 2 (quality scoring)
→ Phase 3 (MinHash dedup) → Tokenization → Training Data Loader
```

### 6.2 Output Format

For fine-tuning, the cleaned text needs to be in a format the training framework expects.
Common options:

| Format | Use case | Tool support |
|---|---|---|
| JSONL (one doc per line) | Most flexible, HuggingFace compatible | `datasets` library |
| Arrow/Parquet | Efficient for large datasets | `datasets`, `pyarrow` |
| Tokenized binary | Pre-tokenized, fastest loading | Framework-specific |

We will likely use **JSONL** for maximum compatibility:
```json
{"text": "cleaned document text here..."}
{"text": "another document..."}
```

### 6.3 Integration with HuggingFace

```python
from datasets import Dataset

# Load cleaned parquet files directly
dataset = Dataset.from_parquet('cleaned/*.parquet')

# Or from JSONL
dataset = Dataset.from_json('cleaned/*.jsonl')

# Tokenize
tokenized = dataset.map(
    lambda x: tokenizer(x['text'], truncation=True, max_length=2048),
    batched=True,
)
```

### 6.4 Key Decisions Still Ahead

- **Model selection**: Which base model to fine-tune (size, architecture)
- **Tokenizer**: Use pre-trained tokenizer or train a custom one on our data
- **Sequence length**: How to handle documents longer than the model's context window
  (truncate vs. chunk vs. sliding window)
- **Data mixing**: If we combine FineWeb with other data sources, what ratios to use

## 7. Timeline

| Phase | Scope | Status | Timeline |
|---|---|---|---|
| Phase 1 | Line dedup + boilerplate + URL dedup | Done | Pre-Easter |
| Phase 2 | Content quality scoring | Planned | Week after Easter |
| Phase 3 | MinHash near-duplicate detection | Planned | Week after Easter |
| Phase 4 | Fine-tuning pipeline integration | Planned | Following weeks |

## 8. References

- [FineWeb: 15T Tokens of High-Quality Web Data](https://huggingface.co/datasets/HuggingFaceFW/fineweb) — HuggingFace
- [Deduplicating Training Data Makes Language Models Better](https://arxiv.org/abs/2107.06499) — Lee et al., 2022
- [RefinedWeb: Outperforming Curated Corpora](https://arxiv.org/abs/2306.01116) — Penedo et al., 2023
- [datasketch: MinHash LSH](https://ekzhu.com/datasketch/) — implementation library
