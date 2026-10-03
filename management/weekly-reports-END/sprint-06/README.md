# Sprint 06 — Three-Week Chunking Research and Evaluation Report

## 1. Summary

Sprint 06 investigated how to turn a large, deduplicated corpus into a reproducible and evidence-driven chunking pipeline that can support the project's chunk-based duplicate-removal workflow and future retrieval-oriented processing.

The work was organized as a three-week progression:

- **Week 1 — Design and Exploration:** freeze and profile the post-deduplication dataset, build a reproducible Chonkie environment, define evaluation criteria, and prototype three chunking strategies.
- **Week 2 — Development and Validation:** convert the prototypes into a reusable provenance-aware batch pipeline, add automated QA, verify consistency, and test engineering-scale execution.
- **Week 3 — Controlled Evaluation:** perform parameter sensitivity studies, construct approximately matched-granularity settings, compare boundary behaviour and fragmentation, test robustness across document groups, measure runtime cost, and consolidate the evidence into reproducible canonical tables and audits.

The three evaluated methods were:

1. **TokenChunker** — fixed-size chunking using a character tokenizer.
2. **RecursiveChunker** — structure-aware recursive splitting using character-budget constraints.
3. **SemanticChunker** — embedding-based semantic splitting using local Model2Vec embeddings.

The sprint did **not** attempt to declare a universal “best” chunker. The central result is that the methods exhibit different and measurable trade-offs in granularity control, structural boundary use, fragmentation, runtime, and robustness. Retrieval-quality labels were not available, so the evidence supports engineering and segmentation conclusions rather than a downstream retrieval ranking.

---

## 2. Research Motivation and Literature Basis

Chunking is not merely a preprocessing detail. It determines the retrieval unit, controls how much context is packaged together, affects the number and size of indexed units, and changes the boundaries at which information can be retrieved.

The broader motivation comes from retrieval-augmented language modelling. Lewis et al. introduced Retrieval-Augmented Generation (RAG), where a model accesses external non-parametric memory through retrieval rather than relying only on parameters [1]. In such systems, the unit that is indexed and retrieved becomes an important design decision.

This sprint was informed by several lines of research:

| Research work | Main idea relevant to this sprint | Influence on the Sprint 06 design |
| --- | --- | --- |
| Lewis et al., 2020, **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** [1] | Retrieval provides explicit external context to language models. | Motivates treating chunk construction as an important upstream retrieval-system design problem. |
| Hearst, 1997, **TextTiling** [2] | Text can be segmented into coherent subtopic passages using discourse/lexical structure rather than fixed lengths alone. | Motivates measuring whether chunk boundaries align with natural structural boundaries such as sentences and newlines. |
| Pevzner & Hearst, 2002, **A Critique and Improvement of an Evaluation Metric for Text Segmentation** [3] | Segmentation quality should be evaluated through boundary behaviour rather than simplistic counts. | Motivates explicit boundary analysis and avoiding “number of chunks” as a standalone quality metric. |
| Chen et al., 2024, **Dense X Retrieval: What Retrieval Granularity Should We Use?** [4] | Retrieval granularity materially affects retrieval and downstream QA; fine-grained units can behave differently from passage-level units. | Directly motivates parameter-sensitivity analysis and the matched-granularity comparison used in Week 3. |
| Sarthi et al., 2024, **RAPTOR** [5] | Recursive organization of text can preserve information at multiple levels of abstraction. | Supports investigating recursive/structure-aware chunking rather than relying exclusively on fixed-size splitting. |
| Günther et al., 2024, **Late Chunking** [6] | Encoding chunks independently can lose surrounding context; chunking strategy interacts with representation quality. | Reinforces the limitation that segmentation alone does not establish retrieval quality and motivates future contextual-embedding evaluation. |

### Core research idea

The sprint therefore used the following principle:

> **A fair chunking comparison should separate output correctness, effective granularity, boundary behaviour, robustness, and computational cost rather than comparing methods only by configured chunk size or raw chunk count.**

This principle is especially important because the three methods do not share identical tokenizer semantics. TokenChunker and RecursiveChunker were configured with a character tokenizer, while SemanticChunker uses the tokenizer associated with the local Model2Vec embedding model. Equal configured values therefore do not imply equal effective chunk granularity.

The evaluation strategy was consequently designed around **observed output behaviour**, not nominal parameter equality.

---

## 3. Dataset and Experimental Foundation

The starting point was the frozen post-deduplication dataset:

- **57 Parquet files**
- **6,008,596 documents**
- approximately **25 GB**
- text field: `text`
- exact-hash duplicate groups remaining: **0**
- source dataset treated as immutable during chunking experiments

A **32-document representative evaluation set** was created to support controlled experiments. It includes typical and extreme cases across:

- minimum-length documents
- median-length documents
- P90, P95, and P99 length regions
- maximum-length documents
- documents without newlines
- high chars-per-stored-token cases
- low chars-per-stored-token cases

The environment was frozen as:

- Python 3.13.15
- Chonkie 1.7.0
- Model2Vec 0.9.0
- PyArrow 25.0.0

Semantic embeddings were executed locally using `minishlab/potion-base-32M`; no paid model API was required.

---

## 4. Three-Week Work

## Week 1 — Design and Exploration

Week 1 established the experimental foundation before attempting scale or comparison.

### Work completed

- froze and documented the post-deduplication input dataset;
- profiled all 6,008,596 documents;
- created the 32-document representative sample;
- created and pinned the Chonkie environment;
- prototyped TokenChunker, RecursiveChunker, and SemanticChunker;
- executed all three prototypes on all 32 representative documents;
- defined evaluation metrics and reproducibility rules;
- finalized the experiment protocol.

### Prototype validation

The prototype stage produced:

- **96 total method-document runs**
- **96 successful runs**
- **0 failed runs**
- **0 invalid index ranges**
- **0 source-slice mismatches**

The purpose of Week 1 was not to choose a method. It was to establish that all three approaches could be executed reproducibly and that their chunks could be traced exactly back to source text.

See: [week-1/](./week-1/)

---

## Week 2 — Development and Validation

Week 2 converted exploratory prototypes into a reusable engineering pipeline.

### Pipeline work

A configurable batch chunking CLI was implemented in `pipeline/run_chunking.py`. It preserves source provenance and records:

- input/source file;
- source row;
- document ID;
- source metadata;
- chunking method and exact configuration;
- chunk index;
- start/end indices;
- token count;
- character length;
- chunk text;
- runtime, warnings, and failures.

Automated QA was implemented in `pipeline/validate_chunks.py`, including checks for:

- required provenance;
- empty/whitespace-only chunks;
- zero-token chunks;
- character-length consistency;
- valid index ranges;
- source lookup;
- document ID consistency;
- exact source-slice equality;
- pipeline failures;
- warning capture.

### Representative validation

On the 32 representative documents:

| Method | Documents | Chunks | Processing failures | QA |
| --- | ---: | ---: | ---: | --- |
| TokenChunker | 32 | 1,078 | 0 | PASS |
| RecursiveChunker | 32 | 1,272 | 0 | PASS |
| SemanticChunker | 32 | 5,629 | 0 | PASS |

SemanticChunker generated one recorded Model2Vec numerical runtime warning, but this did not create a processing failure or QA failure.

### Consistency with Week 1

Week 2 outputs exactly matched the Week 1 prototypes for chunk counts, order, source identity, indices, token counts, character lengths, and chunk text.

Result:

`WEEK 1 CONSISTENCY: PASS`

### Scaled engineering validation

TokenChunker was then executed on a complete frozen Parquet file containing **227,628 documents**.

Results:

- **1,334,973 chunks**
- **0 processing failures**
- pipeline elapsed time: **344.773 s**
- wall time: **345.354 s**
- throughput: approximately **660.226 documents/s**
- maximum RSS: **1,512,640 KB**
- output size: approximately **1.1 GB**
- streaming QA: **PASS**
- QA validation failure events: **0**

This established that the pipeline could move beyond the 32-document experimental sample without modifying the frozen source.

See: [week-2/](./week-2/)

---

## Week 3 — Controlled Evaluation

Week 3 shifted from implementation to controlled comparison.

### Experimental structure

The final evaluation contained:

- **11 parameter-sensitivity configurations**
- **3 approximately matched-granularity methods**
- **10 representative profiling groups**
- **9 controlled long-document runtime runs**
- **24 stored QA/run records**
- **61 required evidence artifacts accounted for**
- **14/14 final cross-artifact audit checks passed**

### Parameter sensitivity

For TokenChunker and RecursiveChunker, configured chunk size had a strong and predictable effect on output granularity.

For example:

- TokenChunker total chunks changed from **2,144 → 1,078 → 546** as chunk size increased **1024 → 2048 → 4096**.
- RecursiveChunker total chunks changed from **2,879 → 1,272 → 594** over the same configured sizes.

SemanticChunker behaved differently:

- at threshold 0.8, chunk sizes **1024, 2048, and 4096** produced **5,630, 5,629, and 5,629** chunks respectively;
- changing semantic threshold had a much stronger effect: thresholds **0.7, 0.8, 0.9** produced **4,930, 5,629, 6,325** chunks.

This shows that nominal `chunk_size` is not equally influential across the three methods.

### Matched-granularity comparison

Because equal configuration values were not directly comparable, Week 3 selected settings that minimized the worst relative spread across:

- median chunk character length;
- mean chunk character length;
- mean chunks per document.

The frozen tolerance was **30%**, and the selected settings achieved a worst relative spread of approximately **29.895%**.

Selected settings:

| Method | Selected setting |
| --- | --- |
| TokenChunker | `chunk_size=839`, character tokenizer, overlap 0 |
| RecursiveChunker | `chunk_size=1025`, character tokenizer, min characters 24 |
| SemanticChunker | `chunk_size=2048`, threshold 0.30, `minishlab/potion-base-32M` |

Observed results:

| Method | Chunks | Chunks/doc | Median chars | Mean chars | Small chunks <256 | Runtime | QA |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| TokenChunker | 2,623 | 81.969 | 839 | 832.019 | 0.76% | 0.288 s | PASS |
| RecursiveChunker | 2,871 | 89.719 | 827 | 760.148 | 4.46% | 0.111 s | PASS |
| SemanticChunker | 2,141 | 66.906 | 612 | 1,019.330 | 26.53% | 3.056 s | PASS |

### Boundary behaviour

The most important qualitative distinction remained after approximate granularity matching:

- **TokenChunker:** boundaries were dominated by whitespace and positions classified as other/non-structural boundaries.
- **RecursiveChunker:** boundaries were predominantly aligned with newlines, with some sentence endings.
- **SemanticChunker:** boundaries were primarily split between sentence and newline endings.

This supports the literature-informed idea that equal-sized chunks are not structurally equivalent.

### Robustness

The three methods were compared across ten document groups. Aggregate matching did not imply subgroup matching.

Document length, newline availability, and chars-per-stored-token profile all changed observed behaviour.

The `no_newline` group was particularly informative:

- RecursiveChunker could no longer rely on newline boundaries;
- sentence-boundary behaviour became more visible;
- SemanticChunker remained sentence-oriented;
- TokenChunker retained predominantly fixed-size/non-structural boundary behaviour.

### Long-document runtime

Controlled P95, P99, and maximum-length runs all completed with:

- zero processing failures;
- QA status PASS.

On the maximum-length subset:

| Method | Docs | Input chars | Chunks | Seconds | Seconds/doc |
| --- | ---: | ---: | ---: | ---: | ---: |
| TokenChunker | 3 | 1,771,375 | 2,113 | 0.236 | 0.079 |
| RecursiveChunker | 3 | 1,771,375 | 2,343 | 0.078 | 0.026 |
| SemanticChunker | 3 | 1,771,375 | 1,662 | 2.395 | 0.798 |

These are descriptive single-run pipeline measurements, not repeated statistical benchmarks.

See: [week-3/](./week-3/)

---

## 5. System Structure

The Sprint 06 workflow can be summarized as:

```text
Frozen post-deduplication corpus
        |
        v
Dataset audit and profiling
        |
        v
Representative 32-document sample
        |
        v
+-------------------------------+
| Three chunking strategies     |
| - TokenChunker                |
| - RecursiveChunker            |
| - SemanticChunker             |
+-------------------------------+
        |
        v
Provenance-aware batch pipeline
        |
        v
Automated QA / source validation
        |
        v
Controlled experiments
        |
        +--> parameter sensitivity
        +--> matched granularity
        +--> boundary analysis
        +--> robustness groups
        +--> long-document runtime
        +--> scaled engineering evidence
        |
        v
Canonical evidence tables
        |
        v
Final report + reproducibility audit
```

The repository structure mirrors this progression:

```text
sprint-06/
├── README.md                         # this three-week synthesis
├── tutor meeting_minutes_...md
├── week-1/
│   ├── README.md
│   ├── data-audit/
│   ├── prototypes/
│   ├── tests/
│   └── week1_experiment_protocol.md
├── week-2/
│   ├── README.md
│   ├── pipeline/
│   ├── evidence/
│   ├── week2_report.md
│   └── week3_handoff.md
└── week-3/
    ├── README.md
    ├── week3_experiment_plan.md
    ├── week3_final_evaluation.md
    ├── final_comparison_tables.md
    ├── configs/
    ├── tables/
    ├── audit/
    └── scripts/
```

Large generated Parquet outputs and the frozen source dataset are intentionally excluded from GitHub.

---

## 6. Analysis and Main Findings

### 6.1 Granularity must be measured, not assumed

The strongest methodological finding is that configured chunk size is not a common unit across all chunkers.

This is consistent with the broader retrieval literature showing that retrieval-unit granularity materially affects system behaviour [4]. For that reason, Week 3 used observed character lengths and chunks-per-document to construct an approximate cross-method match before comparing structural behaviour.

### 6.2 Fixed-size and structure-aware chunking produce fundamentally different boundaries

TokenChunker provides predictable size control, but its boundaries frequently do not coincide with sentence or paragraph structure.

RecursiveChunker makes extensive use of source structure, especially newline boundaries.

SemanticChunker produces a higher proportion of sentence/newline boundaries, which is conceptually aligned with discourse-segmentation research such as TextTiling [2]. However, semantic boundary alignment alone is **not** evidence of superior retrieval quality.

### 6.3 SemanticChunker is controlled more strongly by threshold than by chunk size in this sample

Within the tested range, SemanticChunker's configured `chunk_size` had almost no effect at threshold 0.8, while threshold changes materially altered chunk count and mean chunk length.

This is important operationally: parameter sensitivity should be measured for each algorithm rather than assuming that similarly named parameters have comparable effects.

### 6.4 Structure-aware behaviour comes with different fragmentation profiles

Under the Week 3 definition `char_length < 256`, the matched SemanticChunker run produced a larger fraction of very small chunks than the other two methods.

This is not automatically “bad”: fine-grained units may improve retrieval precision in some settings, as suggested by Dense X Retrieval [4]. At the same time, very small independent chunks may lose surrounding context, a concern highlighted by Late Chunking [6].

The present sprint therefore reports fragmentation as a trade-off rather than converting it into a quality score.

### 6.5 Runtime and retrieval quality are separate dimensions

In the matched 32-document experiment, RecursiveChunker had the lowest observed elapsed time and SemanticChunker the highest.

However, runtime alone cannot determine the better chunker. Likewise, boundary coherence alone cannot determine retrieval effectiveness.

A complete downstream decision would require retrieval labels, query sets, or task-level evaluation. Those were outside the available Sprint 06 evidence.

### 6.6 Reproducibility was treated as part of the result

The final study preserved:

- frozen input hashes;
- exact configurations;
- source provenance;
- warning/failure separation;
- QA summaries;
- canonical machine-readable tables;
- report traceability;
- deterministic final report generation.

The final Week 3 audit passed **14/14 checks**, and the final evaluation report SHA256 is:

`9f3c2f9177d3adabc8e98042f27ae01c7a42a188b8afa0f4211efe70f95ec14f`

---

## 7. Limitations

The conclusions should be interpreted within the scope of the collected evidence.

1. The representative sample contains only 32 documents; subgroup results are descriptive rather than population estimates.
2. Retrieval relevance labels and downstream QA labels were not available, so the sprint does not establish retrieval accuracy.
3. The three methods use different tokenizer semantics.
4. Matched granularity is approximate rather than exact.
5. SemanticChunker produced recorded numerical warnings in several representative runs, although the runs still passed integrity QA.
6. Full engineering-scale evidence is available only for TokenChunker; RecursiveChunker and SemanticChunker were not run over the same 227,628-document corpus.
7. Runtime measurements are primarily single pipeline executions rather than repeated benchmark distributions.
8. Memory measurements are available for the scaled TokenChunker run, but not for the three matched Week 3 runs.

---

## 8. Future Work

The next research stage should move from segmentation behaviour to downstream utility.

A stronger evaluation would add:

- a query/relevance-labelled retrieval benchmark;
- recall@k / precision@k / MRR or task-specific retrieval metrics;
- downstream QA or generation quality;
- repeated runtime and memory benchmarks;
- full-scale RecursiveChunker and SemanticChunker execution;
- contextual embedding experiments inspired by Late Chunking [6];
- hierarchical retrieval experiments inspired by RAPTOR [5];
- human or gold-standard boundary labels, enabling segmentation metrics such as WindowDiff [3].

This would allow the current engineering evidence to be connected to actual retrieval utility rather than using chunk shape as a proxy.

---

## 9. Key Sprint 06 Artifacts

- [Week 1 — Design and Exploration](./week-1/)
- [Week 2 — Development and Validation](./week-2/)
- [Week 3 — Controlled Chunking Evaluation](./week-3/)
- [Week 2 detailed report](./week-2/week2_report.md)
- [Week 3 experiment plan](./week-3/week3_experiment_plan.md)
- [Week 3 final evaluation](./week-3/week3_final_evaluation.md)
- [Week 3 final comparison tables](./week-3/final_comparison_tables.md)
- [Week 3 canonical tables](./week-3/tables/)
- [Week 3 audit evidence](./week-3/audit/)
- [Week 3 reproducibility scripts](./week-3/scripts/)

---

## 10. References

[1] Patrick Lewis et al. **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.** NeurIPS 2020.  
https://arxiv.org/abs/2005.11401

[2] Marti A. Hearst. **TextTiling: Segmenting Text into Multi-Paragraph Subtopic Passages.** Computational Linguistics, 23(1), 1997.  
https://aclanthology.org/J97-1003/

[3] Lev Pevzner and Marti A. Hearst. **A Critique and Improvement of an Evaluation Metric for Text Segmentation.** Computational Linguistics, 28(1), 2002.  
https://aclanthology.org/J02-1002/

[4] Tong Chen, Hongwei Wang, Sihao Chen, Wenhao Yu, Kaixin Ma, Xinran Zhao, Hongming Zhang, and Dong Yu. **Dense X Retrieval: What Retrieval Granularity Should We Use?** EMNLP 2024.  
https://aclanthology.org/2024.emnlp-main.845/

[5] Parth Sarthi, Salman Abdullah, Aditi Tuli, Shubh Khanna, Anna Goldie, and Christopher D. Manning. **RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval.** ICLR 2024.  
https://proceedings.iclr.cc/paper_files/paper/2024/hash/8a2acd174940dbca361a6398a4f9df91-Abstract-Conference.html

[6] Michael Günther, Isabelle Mohr, Daniel James Williams, Bo Wang, and Han Xiao. **Late Chunking: Contextual Chunk Embeddings Using Long-Context Embedding Models.** arXiv:2409.04701, 2024.  
https://arxiv.org/abs/2409.04701

---

## Status

**Sprint 06 three-week chunking research, engineering validation, controlled evaluation, and reproducibility packaging are complete.**
