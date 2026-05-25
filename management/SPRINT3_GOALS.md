# Sprint 3 Goal

## 🎯 Get the data ready to train next term's 2B Gemma model.

That means: **four 1B and four 5B regional datasets live on Hugging Face** (AU / NZ / CA / UK), and the **50B Australian dataset carries `hash` + `simhash` columns** so we can deduplicate before training.

---

**Window:** 2026-05-14 → 2026-05-31 · **Milestone:** [`Sprint 3`](../../milestone/sprint-3)

- **Week 1** — ship the 4 × 1B datasets on HF (fix the missing AU 1B); lock in weekly notebook commits.
- **Week 2** — build & upload the 4 × 5B datasets; commit training notebooks; review paper data pipeline.
- **Week 3** — augment 50B AU dataset with `hash` + `simhash` columns (text-only, append-only).
