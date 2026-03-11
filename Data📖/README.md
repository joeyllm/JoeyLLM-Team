# Data 📖

This folder is for dataset documentation and data-related notes used by the project.

## What Goes Here

- dataset descriptions and sources
- licensing or usage constraints
- preprocessing notes
- data dictionaries or schema summaries
- links to storage locations if the data is too large for Git

## Documents

- `fineweb.md`: overview of the FineWeb dataset and project-relevant scale notes
- `loading-data.md`: CPU Pandas and GPU cuDF loading examples
- `gpu-data.md`: VRAM-aware workflows and cuDF OOM prevention notes
- `best-practices.md`: memory management rules, including the subset-first workflow

---

Do not commit large raw datasets unless the team has explicitly agreed to store them in Git. Prefer documenting where the data lives and how to access it.
🙂
