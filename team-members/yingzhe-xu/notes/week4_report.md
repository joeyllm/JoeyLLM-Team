Week 4 Report
1. Objective

This week focused on two main tasks:

Task 1: non-Australian content filtering
Task 2: topic distribution analysis on a single shard

The overall goal was to build a runnable, interpretable, and extensible experimental pipeline on a single shard, part_0.parquet, rather than immediately processing the full dataset.

2. Task 1: Non-Australian Content Filtering
2.1 Method Design

For Task 1, a hybrid filtering pipeline was developed. Its main components are:

Tier-A hard filter
high-precision regex rules for strong structured non-Australian signals
such as address templates, postcodes, and government domains
Tier-B / Tier-C heuristic signals
weaker but still informative features used in a weighted manner
such as institutional keywords, country/region references, and geographic clues
Embedding + lightweight classifier
sentence embeddings and a lightweight classifier for borderline cases
intended to add a semantic layer beyond surface rules
2.2 Experimental Results

On a 5,000-document sample from part_0.parquet, the V03 version ran successfully end to end. The main results were:

Tier-A hits: 6
Weakly labeled training set: 506
AU: 500
non-AU: 6
Final decisions:
keep: 4826
unclear: 144
delete: 30
2.3 Main Findings

The experiment showed that:

the pipeline is now fully runnable
Tier-A rules have started to take effect
the system has become more conservative, with more borderline cases moved into unclear

At the same time, several issues remain:

the classifier training set is extremely imbalanced, with too few non-AU samples
some deleted samples still appear to be false positives
the current system tends to learn “foreign-content intensity” rather than a robust boundary for whether a text should be removed from an Australian-content dataset
2.4 Current Conclusion

At this stage, Task 1 is better understood as a:

candidate filtering tool / prototype

rather than a final high-confidence cleaner for large-scale deletion.

3. Task 2: Topic Distribution Analysis
3.1 Method Design

For Task 2, the decision was made to work on a single shard, part_0.parquet, and use:

BERT-family embeddings
BERTopic

to discover topics and estimate content distribution.

Compared with the earlier KMeans-based clustering version, BERTopic was adopted because it can directly produce:

topic words
topic summaries
representative documents
topic distribution charts

which makes it more suitable for corpus profiling.

3.2 Experimental Results

On a 10,000-document sample from part_0.parquet, the BERTopic version ran successfully and produced:

topic_info
topic_summary
topic_words
representative_docs
bar chart / pie chart
parquet / csv / json output files
3.3 Main Findings

The current results show that:

the topic words are significantly better than in the earlier version
they are no longer dominated by stopword-heavy labels such as the_to_and_of
several larger topics already show recognizable directions, such as:
film / music / movie
labor / government / minister
season / club / game / team

However, there are still clear limitations:

Topic -1 is very large, at about 37.65%
this indicates that many texts were not stably assigned to a specific topic
some topic names are still too rough to use directly in a formal report
3.4 Current Conclusion

At this stage, Task 2 already provides:

a usable initial corpus profiling result

but it still requires further tuning and manual interpretation before it can support a more polished topic-distribution analysis for reporting or paper writing.

4. Overall Progress This Week

The three most important outcomes this week are:

a complete prototype pipeline for Task 1
a complete prototype pipeline for Task 2
a full experimental chain on a single shard, covering:
data loading
feature extraction / embeddings
model-based analysis
output saving

This means the work has moved from idea-level discussion into the stage of runnable experimentation.

5. Next Steps
Task 1
collect more reliable positive non-AU samples
continue refining Tier-A rule boundaries
improve handling of texts that are hosted on Australian domains but mainly discuss foreign local content
Task 2
prioritize reducing the size of Topic -1
improve topic representation
manually rename major topics
produce a cleaner and more report-ready topic distribution resul