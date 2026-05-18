# Opinion 04: Preserve Filtering Reasons for Auditability

## Issue

The paper describes several processing stages, including ccTLD extraction, structural refinement, and dataset validation. However, it does not clearly specify whether each retained or removed record keeps a processing trace.

For JoeyLLM, each record should preserve filtering reasons and processing metadata so the dataset can be audited later.

## Recommendation

Add a field-level processing trace for each document.

Suggested metadata fields:

- `source_dataset`
- `source_snapshot`
- `source_file`
- `url`
- `cctld`
- `pipeline_version`
- `processing_stage`
- `matched_rule`
- `geo_signals`
- `quality_score`
- `language_score`
- `token_count`
- `dedup_group_id`
- `removed_reason`
- `final_decision`

## Why This Matters

Keeping filtering reasons helps answer:

- why a document was retained or removed
- which rule or stage affected the document
- whether a filtering rule is too aggressive
- how many records each rule removed
- whether later dataset versions are reproducible

This is especially important for sovereign corpora, where data provenance and regional alignment need to be explainable.

## Suggested Question for the Paper

The paper could clarify:

> Does each processed document retain metadata describing which extraction, refinement, quality, or deduplication rule affected it?

## Suggested Placement

This could be added under:

**Data Transparency and Reproducibility**

or:

**Dataset Schema**
