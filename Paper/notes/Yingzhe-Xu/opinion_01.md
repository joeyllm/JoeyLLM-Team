# Report: Structural Refinement Method for the Paper

## 1. Summary

This report reviews whether `V03_non_au_filter_pipeline_part0_gpu_refined.ipynb`(https://github.com/joeyllm/JoeyLLM-Team/blob/main/team-members/yingzhe-xu/notebooks/week4/V03_non_au_filter_pipeline_part0_gpu_refined.ipynb) can support the paper's data processing section.

The notebook can be used to support a **secondary structural refinement method** after ccTLD extraction. Its main contribution is a rule-based and weighted-scoring approach for detecting non-local artifacts in the Australian corpus.

This method should be added to the paper under:

**Data Cleaning and Filtering / Structural Refinement**

Suggested subsection title:

**Structural Refinement for Non-local Artifacts**

## 2. Fit with the Paper

The method is consistent with the paper's principle:

> do not remove documents simply because they discuss foreign topics or international events.

Instead, the method focuses on structural evidence, such as postal codes, address formats, government domains, institutional terms, and local-context signals.

This is important because Australian news, government documents, education pages, or local commentary may discuss international events while still being valid Australian-context content.

## 3. Proposed Method

After extracting Australian candidate documents using ccTLD filtering, apply a second-stage structural refinement filter.

The filter has three levels:

1. Tier-A: high-confidence structural rules
2. Tier-B: medium-strength non-AU institutional and structural signals
3. Tier-C: weak semantic and geographic signals

The output should be one of:

- `keep`
- `delete_candidate`
- `unclear`

## 4. Tier-A: High-Confidence Structural Rules

Tier-A contains strong non-AU structural indicators. These can push a document into `delete_candidate`.

Examples from the notebook:

- US city + state + ZIP pattern, e.g. `Albany, NY 12207`
- US street address format
- Canadian postcode
- UK postcode
- foreign government domains, e.g. `.gov.uk`, `.gc.ca`, `.govt.nz`
- foreign government domain plus government-page context, e.g. ministry, department, parliament

These rules are suitable for the paper because they are based on structural mismatch rather than topic or meaning.

## 5. Tier-B: Medium-Strength Weighted Signals

Tier-B uses the notebook's `BC_WEIGHTS` idea. These signals are weaker than Tier-A but still useful for estimating non-local artifact risk.

Tier-B signals add positive weight to `bc_score`.

Examples:

- `USD` / `US$`
- `IRS`
- `ZIP code`
- `Social Security`
- US-style date format, e.g. `MM/DD/YYYY`
- foreign city-region pairs, e.g. `Toronto, ON`, `Sacramento, CA`
- North American phone number with contact context
- foreign institutional terms, e.g. `Internal Revenue Service`, `HM Revenue`, `National Insurance Number`
- foreign country context, e.g. United States, United Kingdom, Canada, New Zealand
- foreign local context, e.g. California, Ontario, New York, Toronto, Vancouver, Auckland

Tier-B should not delete a document by itself. It should raise the risk score and help decide whether a document should become `unclear` or support a Tier-A deletion candidate.

## 6. Tier-C: Weak Semantic and Geographic Signals

Tier-C captures weak and ambiguous signals.

Its purpose is to avoid deleting Australian-context documents just because they discuss international events. These signals should have low weight.

Examples:

- weak geography: California, Texas, Ontario, Toronto, London, New York, British Columbia, Auckland, Quebec, Manchester
- international public or cultural context: Wall Street, Hollywood, Broadway, US election, White House, Downing Street

Tier-C is useful for scoring and review, but it must not become a direct deletion rule.

## 7. `bc_score` Weighted Scoring

The notebook computes a weighted score using non-AU signals and AU-positive signals:

```text
bc_score = sum(non_au_signal * positive_weight)
           + sum(au_signal * negative_weight)
```

Recommended use:

- Tier-B signals receive stronger positive weights.
- Tier-C signals receive weaker positive weights.
- AU-positive signals receive negative weights.
- High `bc_score` means higher non-local artifact risk.
- `bc_score` should support structural filtering, not replace Tier-A evidence.

## 8. AU-Positive Signals

AU-positive signals help reduce false deletion.

Examples:

- `.gov.au`
- `abc.net.au`
- `smh.com.au`
- `theage.com.au`
- Australian Government
- Parliament of Australia
- NSW / VIC / QLD / ACT / WA / SA / TAS / NT
- Canberra, Sydney, Melbourne, Brisbane

If a document has AU source or AU local context and only discusses foreign events, it should usually be kept or marked as `unclear`, not deleted.

## 9. Decision Logic

| Condition | Decision |
| --- | --- |
| Tier-A structural signal, no strong AU context | `delete_candidate` |
| Tier-A structural signal, but strong AU context | `unclear` |
| No Tier-A, but high `bc_score` | `unclear` |
| Only foreign topic or foreign place names | `keep` |
| AU source/context and no structural conflict | `keep` |

## 10. Suggested Paper Text

> After ccTLD-based extraction, we applied a secondary structural refinement stage to reduce residual non-local artifacts in the Australian corpus. The refinement stage combines high-confidence structural rules with a weighted scoring mechanism. Strong indicators such as foreign postcode formats, address templates, and government domains are treated as deletion candidates, while weaker signals such as foreign institutions, currency markers, and regional references contribute to a weighted risk score. Australian source and context signals are assigned negative weights to reduce false removals. This design avoids excluding documents solely because they discuss foreign countries or international events, preserving locally framed international content.

## 11. Limitations

This notebook should be presented as a prototype, not final production evidence.

Current limitations:

- It was tested only on `part_0.parquet`.
- Some notebook markdown statistics do not match the code outputs.
- The full-output stage does not show final complete statistics.
- It does not prove ccTLD extraction, FineWeb deduplication, multi-country generalization, or topic-distribution validation.

## 12. Conclusion

The notebook can support the paper's data cleaning section if framed correctly.

The strongest usable contribution is the **Tier-A structural filtering plus Tier-B/Tier-C weighted scoring mechanism**. The method should be described as a structural refinement prototype designed to remove obvious non-local artifacts while preserving Australian-context documents that discuss international content.
