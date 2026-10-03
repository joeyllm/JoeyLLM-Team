# Week 3 Final Comparison Tables

These CSV files are the canonical machine-readable tables used to generate the final Week 3 report.

The canonical CSV values are retained without report-level numeric rounding.

| Table | Path | Rows | SHA256 | Source evidence |
|---|---|---|---|---|
| baseline_results | `week3/reports/tables/baseline_results.csv` | 3 | `2fa9fcad81124400981faa3ff7a7431e2040a06387d5eb8ca88b194a6dd52226` | `week3/results/baseline_token/summary.json`, `week3/results/baseline_recursive/summary.json`, `week3/results/baseline_semantic/summary.json` |
| computational_cost | `week3/reports/tables/computational_cost.csv` | 3 | `cd7c7c547117c1d6f31769bd878ca2bf2a0f712eee2a5d778f49acec931eaf8e` | `week3/results/issue17/robustness_summary.json` |
| long_document_runtime | `week3/reports/tables/long_document_runtime.csv` | 9 | `3a4da8c576cdb3eaecd8c4fce9e44c815e51f0e35cedc39ac9e5c882d27e9954` | `week3/results/issue17/long_runtime/long_runtime_summary.json` |
| matched_granularity | `week3/reports/tables/matched_granularity.csv` | 3 | `c58d750b09fe67e205d2c1bda73e4cd0529010c0c2c92854a7b26aad341135a9` | `week3/results/issue16/matched_comparison/matched_comparison.json`, `week3/results/issue16/matched_comparison/matched_comparison.csv` |
| parameter_sensitivity | `week3/reports/tables/parameter_sensitivity.csv` | 11 | `55a3cd7825ca61f9d8c988d10092038eb4fb20568b837db8e95a00ecb5e3c039` | `week3/results/parameter_sensitivity/parameter_sensitivity_summary.json` |
| reliability_qa | `week3/reports/tables/reliability_qa.csv` | 24 | `addcb5df6b8ac224135749f4aaf466ea2ee5730239d6ef1725d24be8feb689e2` | `week3/reports/issue18_evidence_inventory.json` |
| robustness_summary | `week3/reports/tables/robustness_summary.csv` | 30 | `fd76986d1e7dcce6dd588fef910977ba46f8caa5ce9626c6bdf1f22aa33d8b5f` | `week3/results/issue17/robustness_summary.json` |
| scaled_engineering_evidence | `week3/reports/tables/scaled_engineering_evidence.csv` | 1 | `4ebfe5021730af14fc114e6958c89460826c3e572db60dbf38bdb4a226c06a48` | `week3/results/issue17/scaled_engineering_evidence.json` |

## Key Matched Comparison

| Method | Chunks | Chunks/doc | Median chars | Mean chars | Small <256 | Seconds | Warnings | QA |
|---|---|---|---|---|---|---|---|---|
| token | 2623 | 81.969 | 839.000 | 832.019 | 0.76% | 0.288113 | 0 | pass |
| recursive | 2871 | 89.719 | 827.000 | 760.148 | 4.46% | 0.110693 | 0 | pass |
| semantic | 2141 | 66.906 | 612.000 | 1019.330 | 26.53% | 3.056384 | 1 | pass |

## Scaled Engineering Evidence

| Method | Docs | Chunks | Seconds | Output bytes | Max RSS KB | QA |
|---|---|---|---|---|---|---|
| token | 227628 | 1334973 | 344.772837 | 1104574318 | 1512640 | pass |
