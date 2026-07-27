# Sprint 2 Goal

## 🎯 Turn the raw AU shards into a region-verified, topic-profiled subset.

That means: **a rule-based non-Australian signal filter (Level 1 / Level 2) and a 13-category AU topic distribution** over the Australian subset, plus **a deduplicated pipeline fast enough to run on full shards** — so Sprint 3 can build the 1B and 5B regional datasets on top of it.

---

**Window:** 2026-04-20 → 2026-05-10 · **Milestone:** [Sprint 2](https://github.com/joeyllm/JoeyLLM-Team/milestone/3)

- **Week 1** — build Task 1 (Level 1 / Level 2 foreign-signal rules) and the Task 2 baseline (AU topic taxonomy + TF-IDF clustering); refine rules against false positives found by manual inspection.
- **Week 2** — replace cluster mapping with the prototype-based classifier with uncertainty handling; quantify and deduplicate the repeated-news content in `part_0.parquet` (~20% of the shard).
- **Week 3** — scale the pipeline off per-row `apply()` onto vectorised / GPU execution so it runs shard-wide; produce the first 1B-token regional samples and document the pipeline for the paper.
