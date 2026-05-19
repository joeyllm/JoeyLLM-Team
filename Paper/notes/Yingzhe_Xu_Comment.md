# Yingzhe Xu Comments on the Paper

## 1. Structural Refinement Could Be More Specific

The paper mentions structural refinement, but the current description is still quite general. My notebook `V03_non_au_filter_pipeline_part0_gpu_refined.ipynb` can be used as a prototype for Australian corpus cleaning:

https://github.com/joeyllm/JoeyLLM-Team/blob/main/team-members/yingzhe-xu/notebooks/week4/V03_non_au_filter_pipeline_part0_gpu_refined.ipynb

The main idea is that a document should not be removed simply because it discusses foreign events. It should only be flagged when there is clear structural evidence of non-local content, such as foreign postcodes, foreign address formats, or foreign government domains.

- Tier-A: high-confidence structural rules, which can be used as `delete_candidate`
- Tier-B: medium-strength institutional or structural signals, added to `bc_score` with weights
- Tier-C: weak geographic or semantic signals, used only as low-weight evidence to avoid removing international content written in a local Australian context

## 2. The Paper Does Not Explain the Train / Validation / Test Split

The paper mainly explains how to construct national corpora and high-quality public samples. However, it does not clearly explain how the corpus would be split into training, validation, and test sets if it is used for JoeyLLM training.

This matters because the split strategy affects whether train-test leakage and near-duplicate overlap are controlled.

## 3. Keeping Filtering Reasons Would Improve Auditability

The paper includes a dataset schema, but it could more clearly explain whether each record keeps a processing trace.

When a document is retained or removed, it would be useful to trace the processing stage, triggered rule, and final decision. This would make it easier to inspect and correct a rule if it later turns out to remove valid data.

## 4. Topic Distribution Could Also Use a Pie Chart

The paper already uses a bar chart to show topic distribution. Bar charts are useful for comparing differences between categories, but if the goal is to help readers quickly understand each topic's share of the overall corpus, a pie chart may be more intuitive.

In `V02_Task2_part0_BERTopic_cudf.ipynb`, I produced not only a topic summary and bar chart, but also a pie chart:

https://github.com/joeyllm/JoeyLLM-Team/blob/main/team-members/yingzhe-xu/notebooks/week4/V02_Task2_part0_BERTopic_cudf.ipynb

This suggests that a pie chart could be used as a useful supplement to the bar chart for showing the approximate proportion of each topic or category in the corpus.
