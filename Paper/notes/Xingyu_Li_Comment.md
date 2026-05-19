# Xingyu Li Comments on the Paper

## Suggestion: Specify Common Crawl Snapshot Versions and Time Range

The paper reports scanning 60TB of data and retaining 1.3T tokens, but does not specify which Common Crawl snapshots, or which FineWeb release, the input corresponds to. I suggest adding this information.

### Suggested Location

**End of Section 3.3 (Storage and Scale)**, after the 60TB / 3.81TB / 1.3T tokens figures.

### Suggested Content

1. The specific FineWeb release version (or HuggingFace dataset commit hash) used.
2. The range of Common Crawl snapshots covered, e.g. `CC-MAIN-2019-XX` through `CC-MAIN-2024-XX`.
3. A histogram showing the temporal distribution of retained `.au` documents across years.

### Reasoning

- **Temporal anchoring**: FineWeb is built from Common Crawl snapshots accumulated between 2013 and 2024. If most retained documents come from 2018–2020, the claim of "reflecting current Australian cultural context" is actually anchored 5–7 years in the past.
- **Snapshot sensitivity**: Different years differ in crawl depth and coverage, which may influence the topic distribution observed in Section 6.
- **Reproducibility**: FineWeb is continuously updated. Citing "FineWeb" without specifying a version means replicating this work at different times would produce different input data.

### Implementation Note

Each FineWeb record already contains a `dump` field (e.g. `CC-MAIN-2024-10`). A `groupby("dump").count()` over the retained parquet files is sufficient to generate the snapshot distribution; no additional crawling or reprocessing is required. The FineWeb release version is available directly from the HuggingFace dataset card.
