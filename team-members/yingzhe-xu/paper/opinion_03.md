# Opinion 03: Missing Train / Validation / Test Split Details

## Issue

The paper explains how national corpora are constructed from FineWeb using ccTLD extraction and structural refinement. It also mentions high-quality public samples for each jurisdiction.

However, the paper does not clearly explain how the dataset would be split into:

- training set
- validation set
- test set

This is a gap if the corpus is intended to support JoeyLLM training or evaluation.

## Why This Matters

Without a clear split strategy, it is difficult to know:

- whether train / validation / test leakage is controlled
- whether near-duplicate documents appear across splits
- whether evaluation results would be reliable
- whether each split preserves national and domain-level diversity

## Suggested Question for the Paper

The paper could clarify:

> After constructing the national corpus, how are training, validation, and test splits created, and what steps are used to prevent document or near-duplicate overlap across splits?

## Suggested Placement

This could be added briefly under:

**Data Pipeline Overview**

or:

**Data Transparency and Reproducibility**
