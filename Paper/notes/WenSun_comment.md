# WEN SUN — Comments on the JoeyLLM Paper

The paper presents a practical and scalable pipeline for extracting national corpora from FineWeb. The ccTLD-based extraction and structural refinement stages are useful for JoeyLLM because they provide a clear way to build country-specific datasets from a larger web corpus.

However, the data cleaning and filtering pipeline could be made more transparent in two ways:

## 1. Add a small human audit for retained and removed documents

The current pipeline appears to rely mainly on automatic checks. Manually reviewing a small sample of retained and removed documents would help estimate whether the filtering rules correctly keep relevant national content and remove non-local structural artifacts.

## 2. Adapt this audit process for JoeyLLM

A similar small-scale audit could help verify the quality of the 5B Australian dataset before scaling or release. This would be especially useful for checking whether the ccTLD extraction and structural refinement rules work correctly on the JoeyLLM data pipeline.

Overall, these additions would make the data processing pipeline more reproducible, transparent, and easier to adapt for JoeyLLM.
