# Nuo Chen — Comments on the JoeyLLM Paper

## 1. Tokenizer Adaptation for Australian Vocabulary

The paper uses `cl100k_base` throughout, which was trained on general English web text. It may be worth considering whether an Australian-specific tokenizer — or at least an evaluation of tokenization efficiency on Australian vocabulary — would better serve the project's goals. Australian-specific terms such as Indigenous place names, local institutions, and colloquial expressions may be split into more subword tokens than necessary, which could affect model efficiency and downstream representation quality.

## 2. Quantitative Evaluation of the Data Pipeline and Model

The paper provides a thorough description of the data pipeline and the BabyJoey prototype, but does not include quantitative downstream evaluations — for example, perplexity on a held-out Australian test set or task-level comparisons against models trained on non-Australian text. Including such benchmarks in a future version would help readers assess whether the Australian-specific training data produces measurable improvements in Australian-domain performance.

## 3. Concrete Implementation of Indigenous Data Governance

The paper acknowledges the importance of ethical handling of Indigenous Australian content, which is commendable. To further strengthen this commitment, future versions could point to established frameworks — such as the CARE Principles for Indigenous Data Governance or the AIATSIS Code of Ethics — and describe any community consultation undertaken, as well as specific mechanisms for identifying and handling culturally sensitive material.

## 4. Cross-Country Validation of Australian Content Distinctiveness

The paper describes a set of country-attribution signals (ccTLD, URL patterns, content heuristics) for identifying Australian content. A cross-country comparison — examining vocabulary overlap, named-entity distributions, or topic profiles relative to UK, Canadian, or New Zealand English web text — could help demonstrate that the resulting corpus is meaningfully distinctive, and that the attribution pipeline isolates Australian-specific content rather than primarily removing obvious US signals.

## 5. Domain Gap Between BabyJoey's Training Corpus and the Target Web Corpus

BabyJoey (§4.1) was trained on Project Gutenberg Australia, which predominantly comprises literary works predating 1954. While this is a practical choice for an initial prototype, it would be helpful to discuss how this starting domain might affect training stability or transfer when the model is later adapted to modern, web-crawled Australian text, and whether any domain-bridging steps are planned to address this gap.
