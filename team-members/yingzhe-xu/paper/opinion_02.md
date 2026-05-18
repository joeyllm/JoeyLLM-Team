# Report: Add a Post-extraction Deduplication Stage

## 1. Summary

This report proposes adding a clearer deduplication stage to the paper's data processing pipeline.

The current paper mentions that FineWeb already performs large-scale deduplication. However, after ccTLD-based extraction and structural refinement, the national corpora may still contain exact duplicates, near-duplicates, repeated templates, mirrored pages, syndicated news, and train-test overlap.

Therefore, the paper should add a **post-extraction deduplication stage** after country-level extraction.

Suggested paper section:

**Data Cleaning and Filtering / Deduplication**

Suggested subsection title:

**Post-extraction Deduplication for Sovereign Corpora**

## 2. Motivation

The reference paper **Deduplicating Training Data Makes Language Models Better** supports the need for deduplication in language model training data.

Its main findings are relevant to JoeyLLM:

- Large language-model datasets contain many near-duplicate examples and long repeated substrings.
- Deduplication can reduce memorized text generation by about 10x.
- Deduplication can reduce train-test overlap, making evaluation more reliable.
- Deduplicated datasets can require fewer training steps while maintaining similar or better performance.
- Near-duplicates are common in web-crawled corpora, especially where templates, news reposting, and repeated boilerplate occur.

This is directly relevant to sovereign corpora because national web subsets may contain many repeated pages from government sites, media syndication, commercial templates, event listings, legal disclaimers, and mirrored content.

## 3. Why FineWeb Deduplication Is Not Enough

FineWeb deduplication is useful as an upstream global cleaning layer, but the paper should not rely on it as the only deduplication step.

Reasons:

- ccTLD extraction changes the corpus boundary, so duplicates should be checked again within each national subset.
- National corpora may contain repeated local templates that are not obvious at global scale.
- The same article may appear across multiple Australian domains or media partners.
- Similar pages may differ only by dates, locations, navigation text, or small template fields.
- Train / validation / test splits can still overlap unless deduplication is applied before splitting.

The paper should distinguish:

- **Upstream deduplication**: already performed by FineWeb.
- **Downstream sovereign deduplication**: applied after ccTLD extraction and structural refinement.

## 4. Proposed Method

The deduplication stage can be simple and practical:

1. Normalize document text.
2. Remove exact duplicate documents.
3. Detect exact repeated substrings.
4. Detect near-duplicate documents using MinHash / LSH.
5. Deduplicate before train / validation / test splitting.
6. Record deduplication statistics for transparency.

## 5. Exact Deduplication

Exact deduplication should remove identical documents after basic normalization.

Recommended normalization:

- lowercasing only if appropriate for hash comparison
- trimming whitespace
- collapsing repeated whitespace
- removing boilerplate separators if consistently present
- preserving the original text in the final dataset

Recommended keys:

- normalized text hash
- normalized URL hash
- canonical URL where available

This catches exact repeated pages, duplicated rows, repeated crawls, and simple mirror copies.

## 6. Exact Substring Deduplication

The reference paper also discusses exact substring deduplication, where long repeated token spans are identified and removed or used to flag repeated content.

For JoeyLLM, this can be used to detect:

- repeated legal disclaimers
- navigation boilerplate
- cookie banners
- repeated footers
- repeated government or company templates
- copied blocks across many pages

The paper does not need to implement a complex suffix-array system immediately, but it can propose long-substring matching as a future or optional refinement.

## 7. Near-duplicate Detection with MinHash / LSH

The reference paper proposes approximate matching with MinHash for web-crawled data. It represents documents as sets of n-grams and estimates Jaccard similarity:

```text
Jaccard(A, B) = |A ∩ B| / |A ∪ B|
```

The second reference, **Similarity Estimation Techniques from Rounding Algorithms**, supports the theoretical basis of locality-sensitive hashing. It explains that LSH can create compact sketches of objects so that similarity can be estimated efficiently, and that min-wise hashing estimates Jaccard similarity for sets.

For JoeyLLM, this means:

- represent each document as a set of word or token n-grams
- compute MinHash signatures
- use LSH buckets to find likely near-duplicate pairs
- confirm duplicates using Jaccard similarity or edit similarity
- cluster near-duplicates and keep one representative document

This is suitable for large corpora because comparing every document pair directly is too expensive.

## 8. Suggested Thresholds

Initial thresholds can be conservative:

| Step | Suggested Setting |
| --- | --- |
| n-gram type | 5-gram tokens or word shingles |
| near-duplicate threshold | Jaccard similarity >= 0.8 |
| stricter production threshold | Jaccard similarity >= 0.9 |
| keep strategy | keep highest quality score or earliest canonical URL |
| split protection | remove near-duplicates across train / validation / test |

The exact values should be tuned on Australian sample data.

## 9. Placement in the Pipeline

Recommended order:

1. FineWeb input
2. ccTLD extraction
3. structural refinement
4. post-extraction deduplication
5. train / validation / test split
6. dataset characterization

Deduplication should happen before splitting to reduce leakage between train, validation, and test sets.

## 10. Metadata to Record

The paper should recommend storing deduplication metadata:

- `text_hash`
- `url_hash`
- `dedup_method`
- `duplicate_cluster_id`
- `cluster_size`
- `kept_document_id`
- `jaccard_similarity`
- `dedup_stage`
- `removed_reason`

This improves reproducibility and makes the dataset easier to audit.

## 11. Suggested Paper Text

> Although the underlying FineWeb corpus already includes upstream deduplication, we recommend adding a downstream deduplication stage after country-level extraction. This step addresses duplicate and near-duplicate content that may emerge within national subsets, including repeated templates, syndicated news articles, mirrored pages, and repeated boilerplate. Exact duplicates can be removed using normalized text and URL hashes, while near-duplicates can be detected using MinHash signatures over document n-grams and confirmed using Jaccard similarity. Applying this step before train-validation-test splitting reduces leakage and improves the reliability of downstream evaluation.

## 12. Reference Evidence

The recommendation above is supported by the following reference statements.

### 12.1 Why deduplication matters

From **Deduplicating Training Data Makes Language Models Better**:

> We find that existing language modeling datasets contain many near-duplicate examples and long repetitive substrings.

This supports the claim that large LM training corpora can contain substantial duplicated or near-duplicated text.

The same paper states:

> Deduplication allows us to train models that emit memorized text ten times less frequently and require fewer training steps to achieve the same or better accuracy.

This supports the argument that deduplication can reduce memorization and improve training efficiency.

It also states:

> We can also reduce train-test overlap, which affects over 4% of the validation set of standard datasets, thus allowing for more accurate evaluation.

This supports applying deduplication before train / validation / test splitting.

### 12.2 Exact substring and MinHash methods

From **Deduplicating Training Data Makes Language Models Better**:

> We introduce two complementary methods for performing deduplication. First, using a suffix array ... Second, we use MinHash ...

This supports the proposed combination of exact substring deduplication and approximate near-duplicate detection.

The paper further explains:

> We use MinHash ... for estimating the n-gram similarity between all pairs of examples in a corpus.

This supports the proposed use of document n-grams and MinHash signatures.

For web-crawled data, it states:

> NEARDUP ... is a good complement to the exact substring matching, especially for web crawl text ...

This supports using MinHash-style near-duplicate detection for FineWeb / Common Crawl derived corpora.

### 12.3 Jaccard similarity and thresholds

From **Deduplicating Training Data Makes Language Models Better**:

```text
Jaccard(di, dj) = |di ∩ dj| / |di ∪ dj|
```

The paper also reports using Jaccard and edit-similarity thresholds:

> Document pairs with edit similarity higher than 0.8 were identified as duplicates.

And for a stricter setting:

> filtering to document pairs with Jaccard index of at least 0.9 and edit similarity of at least 0.9.

This supports using 0.8 as an initial threshold and 0.9 as a stricter production threshold, subject to validation on JoeyLLM data.

### 12.4 LSH and compact similarity sketches

From **Similarity Estimation Techniques from Rounding Algorithms**:

> Such a scheme leads to a compact representation of objects so that similarity of objects can be estimated from their compact sketches.

This supports using sketch-based methods for scalable similarity estimation.

The same paper states:

> Min-wise independent permutations provide ... a locality sensitive hashing scheme ... with the set similarity measure sim(A, B) = |A ∩ B| / |A ∪ B|.

This supports using min-wise hashing / LSH as the theoretical basis for estimating Jaccard-style set similarity.

## 13. Limitations

This proposal is a pipeline improvement suggestion, not evidence that the current paper has already run post-extraction deduplication.

Current limitations:

- The paper currently attributes deduplication mainly to FineWeb.
- There is no clear evidence that national subsets were deduplicated again after ccTLD extraction.
- Thresholds need to be validated on JoeyLLM's actual Australian corpus.
- Aggressive deduplication may remove legitimate repeated public-interest text, such as laws, quotations, or official notices.

## 14. Conclusion

The paper should add a short post-extraction deduplication stage to make the data pipeline stronger and more defensible.

The strongest recommendation is:

**Use FineWeb deduplication as the upstream baseline, then apply a national-subset deduplication pass using exact hashing and MinHash/LSH near-duplicate detection before dataset splitting.**

## 15. Reference URLs

- Lee et al., **Deduplicating Training Data Makes Language Models Better**: https://aclanthology.org/2022.acl-long.577.pdf
- Charikar, **Similarity Estimation Techniques from Rounding Algorithms**: https://www.cs.princeton.edu/courses/archive/spring04/cos598B/bib/CharikarEstim.pdf
