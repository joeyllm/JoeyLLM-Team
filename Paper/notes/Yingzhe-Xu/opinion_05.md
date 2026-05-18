# Opinion 05: Add Corpus Categorization and Topic Analysis

## Issue

The paper discusses dataset validation through topic distribution and semantic structure, but it does not clearly explain a concrete data categorization or topic-analysis workflow for the corpus.

For JoeyLLM, this is important because after building a national corpus, we need to understand what kinds of content are inside it, not only how large it is.

## Team Work

I implemented an initial topic-distribution analysis in:

`V02_Task2_part0_BERTopic_cudf.ipynb` (https://github.com/joeyllm/JoeyLLM-Team/blob/main/team-members/yingzhe-xu/notebooks/week4/V02_Task2_part0_BERTopic_cudf.ipynb)

The notebook uses:

- `part_0.parquet`
- a 10,000-document sample
- BERT-family sentence embeddings
- BERTopic
- `CountVectorizer(stop_words="english", ngram_range=(1, 2), min_df=5)`
- `KeyBERTInspired()` for improved topic representation

The notebook produces:

- topic summary
- topic words
- representative documents
- topic distribution table
- bar chart / pie chart
- parquet / csv / json outputs

## Findings

The current result already shows some readable topic directions, such as:

- film / music / movie
- labor / government / minister
- season / club / game / team
- health / school / education
- police / court / murder
- asylum / Australia / Indonesia
- cricket / sport

This suggests that topic modeling can help describe the internal composition of the Australian corpus.

## Limitations

This analysis is still only a prototype.

Current limitations:

- It only uses one shard: `part_0.parquet`.
- It only samples 10,000 documents.
- Topic `-1` is very large: about 37.65% of the sample.
- A large Topic `-1` means many texts were not stably assigned to a clear topic.
- Some topic names are still too rough for direct paper use, such as `baby_just_time_know`.
- Texts were truncated to 1500 characters, so topic signals may be biased toward the beginning of documents.
- The current topic labels still need manual interpretation and cleanup.

## Suggested Paper Improvement

The paper could add a clearer corpus characterization step:

> After structural refinement, we apply topic modeling or embedding-based clustering to profile the internal composition of each national corpus. This step helps identify major content groups, estimate topic distribution, and inspect whether the corpus is dominated by a small number of source types or maintains broad domain coverage.

## Suggested Question

The paper could clarify:

> How are the extracted national corpora categorized or analyzed internally before release or training use?

## Suggested Placement

This could be added under:

**Dataset Characterization**

or:

**Domain Substructure within National Corpora**

## Conclusion

The notebook provides a useful first-pass topic analysis method, but it should be presented as an initial corpus profiling prototype rather than a final validation result.

The main value is showing that JoeyLLM can move beyond corpus construction and begin analyzing what types of content the national dataset actually contains.
