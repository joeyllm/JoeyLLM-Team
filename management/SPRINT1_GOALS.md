# Sprint 1 Goal

## 🎯 Get every member onto the data, and agree on one shared filtering baseline.

That means: **all five members running their own notebook over the FineWeb sample** (10 parquet shards, not the full 60TB), and **one evidence-backed threshold baseline the whole team uses** — so Sprint 2 starts from a common pipeline instead of five different ones.

---

**Window:** 2026-03-16 → 2026-04-05 · **Milestone:** [Sprint 1](https://github.com/joeyllm/JoeyLLM-Team/milestone/2)

- **Week 1** — stand up the team website on GitHub Pages (`docs/`); confirm WireGuard, JupyterHub and repo access for everyone; assign a maintainer to each repo.
- **Week 2** — each member builds a reader over one shard and runs a first filtering pass; compare results side by side and agree on preliminary parameters.
- **Week 3** — cross-validate the rules across all 10 shards, lock the shared thresholds (`language_score ≥ 0.85`, `min_tokens ≥ 50`, `text_length ≥ 200`), standardise output format and make per-stage IO timing mandatory.
