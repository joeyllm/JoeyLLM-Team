# Week 4 Report 🗂️

**Week:** Week 4  
**Date:** 2026-04-20  
**Attendees:** Xiang Chang, Wen Sun, Xingyu Li, Yingzhe Xu, Nuo Chen  
**Facilitator:** Xiang Chang, Wen Sun, Xingyu Li, Yingzhe Xu, Nuo Chen 
**Prepared by:** Xiang Chang 

---

## Agenda

1. Review progress on Task 1: strong non-AU signal detection rules
2. Review progress on Task 2: topic distribution analysis for the AU subset
3. Discuss data quality issues in `part_0.parquet`, especially duplicated news content
4. Plan refinements for next week, including prototype-based topic classification improvement

## Discussion

This week we focused on two main tasks.

First, for **Task 1**, we continued building and testing rules to identify strong foreign-local signals inside the AU subset. We separated the rules into **Level 1** and **Level 2**. Level 1 focused on very strong signals such as US ZIP/state combinations, Canadian postal codes, UK postcodes, and explicit foreign institutional phrases. Level 2 focused on contextual signals such as the term `ZIP code`, refined US phone-number formats, and unambiguous US-style date formats. During testing, we found that some rules were too broad at first and produced false positives, so we refined them to improve precision.

Second, for **Task 2**, we started building a topic-distribution analysis pipeline for the AU subset. We first designed an Australia-relevant topic taxonomy, then used a TF-IDF baseline with clustering, and later improved the workflow with dimensionality reduction and a prototype-based document classifier. We expanded the taxonomy from 12 to 13 categories by adding **Technology and digital life**, because the clustering results showed that technology-related content formed a meaningful category of its own.

We also found an important data-quality issue in `part_0.parquet`: there appears to be a substantial amount of duplicated or near-duplicated news content. Our current estimate is that duplicated news may account for roughly **20%** of this shard. Even when duplicate pages were crawled around six months apart, the actual textual content often showed little meaningful difference. This may inflate the apparent proportion of news in the dataset and could bias later model training toward over-representing news-style language and topics.

## Decisions

- We will keep the **Level 1 / Level 2** framework for Task 1, because it provides a clear distinction between very strong foreign-local signals and weaker contextual signals.
- For Task 2, we will use the **prototype-based document classifier with uncertainty handling** as the main current result, instead of relying only on cluster-level mapping.
- We will keep the **13-category taxonomy**, including **Technology and digital life**.
- We will explicitly document the duplicated-news issue in `part_0.parquet`, because it may affect both topic-distribution analysis and future training-data balance.

## Action Items

| Action | Owner | Due |
|--------|-------|-----|
| Refine remaining weak Task 1 rules and document false-positive patterns | _To be filled_ | Next meeting |
| Continue improving prototype-based classification for Task 2 | _To be filled_ | Next meeting |
| Investigate duplicated news in `part_0.parquet` more systematically | _To be filled_ | Next meeting |
| Prepare a cleaner summary of topic distribution results for the team | _To be filled_ | Next meeting |

## Progress Summary

This week we made meaningful progress on both filtering and topic analysis. For Task 1, we moved from rough regex ideas to a more structured rule system with manual inspection and refinement. For Task 2, we advanced from a basic TF-IDF clustering baseline to a more interpretable prototype-based topic-classification workflow. We also identified an important duplication issue in the raw shard, which may have significant implications for topic balance and downstream model training.

## Completed This Week

- Built and tested multiple **Level 1** and **Level 2** filtering rules for strong foreign-local signals
- Refined several rules after manual inspection to reduce false positives
- Designed an Australia-relevant topic taxonomy for Task 2
- Expanded the taxonomy from 12 to 13 categories by adding **Technology and digital life**
- Built an initial TF-IDF + clustering topic-analysis baseline
- Improved Task 2 with a prototype-based document classifier and uncertainty handling
- Identified a duplicated-news issue in `part_0.parquet` that may distort topic proportions

## In Progress

- Further refinement of weak topic categories in the prototype-based classifier
- Validation of topic-distribution quality on a broader sample
- Investigation of how duplicated news affects overall corpus balance
- Interpreting how current topic distribution should inform future small-model training

## Blockers

- Some topic categories are still harder to separate cleanly than others, especially categories with overlapping vocabulary
- The current topic analysis is still based on a relatively small working sample
- Duplicated news content in `part_0.parquet` may distort the apparent distribution of topics and bias future training if not handled carefully

## Plan for Next Week

- Continue refining the prototype-based topic classifier, especially weaker categories
- Recheck uncertain or mixed assignments and improve category separation
- Investigate duplicated news content in more detail and consider possible mitigation strategies such as down-weighting or deduplication
- Use the refined topic distribution results to discuss data selection and balancing for the Australian-focused small model
- Start traning the model

## Next Meeting

**Date:** 2026-04-27  
🙂
