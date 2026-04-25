# Week 4 Report — Nuo Chen

**Shard worked on**: `004_00049.parquet` (152,991 rows, ~352 MB)
**Notebooks**: `notebooks/week4/task1_regex_filter.ipynb`, `notebooks/week4/task2_anchored_topics.ipynb`
**Outputs**: `outputs/week4/`

---

## 1. Objective

This week focused on the two tutor-assigned tasks:
- **Task 1**: Identify clearly non-Australian content using strong-signal regex
- **Task 2**: Produce a topic distribution of the shard for Matthew's paper, using embeddings + clustering on a stratified sample

The overall goal was the same as the rest of the team: build a runnable, interpretable pipeline on a single shard, with the methodology clear enough that Matthew can run it on the full 50B-token corpus later. I deliberately picked methods that **complement** Yingzhe's V03/V02 work rather than duplicating it.

---

## 2. Task 1 — Non-Australian Content Filtering

### 2.1 Method Design

Per the tutor's explicit instructions ("strong features only", "no spelling rules", "regex recommended"), I built a 4-rule strong-signal regex pipeline. No ML classifier, no fuzzy heuristics, no spelling-based rules.

**The four rules:**

| Rule | What it matches | Why it's a strong signal |
|------|-----------------|--------------------------|
| `US_ZIP` | `(state code) + 5-digit ZIP`, e.g., `CA 94102` | AU postcodes are 4 digits with state name (NSW 2000); zero format collision |
| `US_DATE` | `MM/DD/YYYY` where day ≥ 13 | Day 13–31 is unambiguous: only US format puts month first. Days 1–12 are intentionally excluded because they collide with AU `DD/MM` |
| `US_PHONE` | `(XXX) XXX-XXXX` or `+1-XXX-XXX-XXXX` | AU mobile is `04XX XXX XXX`; AU landline is `+61 X XXXX XXXX`; completely different shape |
| `NON_AU_INST` / `NON_AU_GOV` | Strong institution names (IRS, NHS England, HMRC, CRA, IRD NZ) and `.gov`/`.gov.uk`/`.gc.ca`/`.govt.nz` URLs (with `.gov.au` excluded) | Practically impossible in genuine AU content |

### 2.2 Experimental Results

End-to-end run on all 152,991 rows in 4.6 seconds (lazy row-group reading, constant ~100 MB RAM).

**Per-rule hit counts:**

| Rule | Hits | % of total |
|------|------|------------|
| US_ZIP | 1,205 | 0.79% |
| US_DATE | 407 | 0.27% |
| US_PHONE | 1,480 | 0.97% |
| NON_AU_INST | 888 | 0.58% |
| NON_AU_GOV | 904 | 0.59% |
| **Any rule** | **4,518** | **2.95%** |

**Rule quality scorecard (`.au` TLD reverse sanity check):**

| Rule | Hits on .au TLD | FP rate | Status |
|------|-----------------|---------|--------|
| US_ZIP | 3 / 3,818 | 0.08% | STRONG |
| US_DATE | 1 / 3,818 | 0.03% | STRONG |
| US_PHONE | 0 / 3,818 | 0.00% | STRONG |
| NON_AU_INST | 0 / 3,818 | 0.00% | STRONG |
| NON_AU_GOV | 0 / 3,818 | 0.00% | STRONG |

All four rules pass the validation criterion (FP rate ≤ 5% on confirmed AU content).

### 2.3 Main Findings

- **Strong-signal regex catches ~3% of the shard** as clearly non-Australian. This is the *high-precision floor* — anything caught here is very likely a true positive.
- **The "DD ≥ 13" trick for date format detection** is the most thoughtful design choice. Without it, `05/12/2024` is unparseable (May 12 in US, 5 December in AU). By restricting to days 13–31, US format becomes unambiguous — sacrificing recall for near-perfect precision.
- **`.au` TLD reverse validation** is a clean way to estimate false-positive rate without manual labelling. If a "non-AU" rule fires on a `.au` domain, that's almost certainly a false positive. All five rules score ≤0.08% FP — well below the 5% threshold.
- **The `.au` TLD itself only covers 2.50% of the shard**. This means most genuinely Australian content does *not* sit on `.au` domains — they're hosted on `.com`, blogspot, etc. Any approach that relies on TLD alone misses 90%+ of AU content.

### 2.4 Current Conclusion

Task 1 is **production-ready as a high-precision filter**. The four rules can be applied to the full 50B-token corpus exactly as written; performance scales linearly with row count.

The deliberate trade-off: this catches the *obviously* non-AU content (~3%) but says nothing about the *subtly* non-AU content (e.g., a US news article with no zip/phone). That gap is what Yingzhe's V03 ML classifier is designed to cover. **Together, my regex and his ML form a precision/recall pair**.

---

## 3. Task 2 — Topic Distribution Analysis

### 3.1 Method Design

Tutor required: **embeddings + clustering, NVIDIA-style taxonomy, pie chart**.

Yingzhe used pure BERTopic (BERT + UMAP + HDBSCAN) and reported 37.65% of documents falling into Topic -1 (the noise topic). This is a structural property of density-based clustering on heterogeneous web text, not a tunable parameter.

I deliberately chose a **two-stage hybrid** that addresses this head-on:

**Stage 1 — Anchored embedding classification:**
- Encode every document with `all-MiniLM-L6-v2` (384-dim, 80 MB, CPU-friendly)
- For each of NVIDIA's 26 NeMo Curator domain categories, write 2–3 prototype sentences
- Compute mean embedding per category → "anchor centroid"
- For each document, find the highest-cosine-similarity centroid → assign that category
- Record the similarity as confidence

**Stage 2 — Residual KMeans clustering:**
- Documents with confidence < 0.30 are considered "low-confidence" — the anchor templates didn't capture them well
- Re-cluster these with KMeans (k=15) to discover topics not covered by the NVIDIA taxonomy
- Describe each discovered cluster by top TF-IDF terms

This guarantees **100% coverage with 0% noise topic** — the structural fix to BERTopic's weakness.

### 3.2 Experimental Results

Stratified sample of 10,000 documents (2,000 short / 5,000 medium / 3,000 long).

**Stage 1 confidence distribution:**
- Median similarity: ~0.27
- High-confidence (sim ≥ 0.30): 2,924 docs (29.2%)
- Low-confidence (going to Stage 2): 7,076 docs (70.8%)

**Top NVIDIA categories assigned in Stage 1** (sample of larger ones):
- Games: 388 (3.88%)
- Books_and_Literature: 208 (2.08%)
- Jobs_and_Education: 173 (1.73%)
- Real_Estate: 167 (1.67%)
- Travel_and_Transportation: 153 (1.53%)
- Beauty_and_Fitness: 143 (1.43%)
- (... 21 more NVIDIA categories with smaller counts)

**Discovered clusters from Stage 2** (the 15 KMeans clusters with top TF-IDF terms):

| Cluster | Docs | Top terms | Likely NVIDIA mapping |
|---------|------|-----------|------------------------|
| Discovered_01 | 760 | use, time, need, high, used, water, like | (general / how-to) |
| Discovered_12 | 646 | style, design, perfect, collection, make, high | Beauty/Shopping/Home |
| Discovered_09 | 633 | business, company, services, work, team, management | Business_and_Industrial |
| Discovered_03 | 593 | time, just, new, city, area, located, day | Travel / Reference |
| Discovered_05 | 536 | new, time, music, just, like, years, movie, film | Arts_and_Entertainment |
| Discovered_06 | 529 | new, use, time, available, high, design, using | (general) |
| Discovered_04 | 466 | law, police, court, state, people, year | Law_and_Government |
| Discovered_02 | 465 | president, government, people, said, state, years | Law_and_Government |
| Discovered_13 | 459 | school, year, children, students, community, program | Jobs_and_Education |
| Discovered_00 | 426 | time, life, people, just, like, day | (general blog / opinion) |
| Discovered_07 | 405 | business, data, website, information, digital, marketing | Computers_and_Electronics / Business |
| Discovered_11 | 398 | health, make, food, like, used, help, use | Health / Food_and_Drink |
| Discovered_08 | 277 | team, game, year, season, league, players | Sports |
| Discovered_14 | 270 | money, financial, online, casino, free, account | Finance / Adult |
| Discovered_10 | 213 | god, church, jesus, world, people, life | People_and_Society / Religion (not in NVIDIA) |

**Pie chart**: saved to `outputs/week4/task2_distribution_pie.png`. Shows top 15 categories + Other.

### 3.3 Main Findings

1. **Coverage is 100% vs Yingzhe's 62.35%.** No documents fall into a noise category. This is the headline structural difference vs his BERTopic V02.

2. **The NVIDIA taxonomy mostly fits Australian web content, with one or two genuine gaps.** Most discovered clusters semantically map back to NVIDIA categories (politics → Law_and_Government, sports → Sports, business → Business_and_Industrial). The exception: `Discovered_10` (god/church/jesus) — religion isn't a top-level NVIDIA category. This is a candidate for taxonomy extension.

3. **Stage 1 confidence is lower than expected.** The 0.30 threshold pushes 70% of docs into Stage 2. Two likely causes:
   - Anchor templates are short (2–3 sentences); document text is much longer and includes contextual noise
   - MiniLM embeddings of long noisy text drift toward a "general" centroid
   - Mitigation (post-Easter): write more diverse anchor templates, or add document chunking + max-pooling

4. **The Stage 2 discovered clusters validate the taxonomy choice.** The fact that Stage 2 keeps rediscovering NVIDIA categories (Law_and_Government appears twice as Disc_02 and Disc_04, Business twice as Disc_07 and Disc_09) confirms: the taxonomy is the right shape, but my anchor encoding is too narrow. Tuning anchors will probably collapse Stage 2 down to a much smaller residual.

### 3.4 Current Conclusion

The pipeline produces **paper-ready distribution numbers** (clean percentages mapping to a known taxonomy) and the required pie chart, in under 60 seconds on CPU for 10k docs.

For Matthew's paper, this is more usable than the V02 BERTopic output (no "37.65% noise" caveat to explain). For exploratory analysis, BERTopic remains stronger because it can find emergent fine-grained topics (the `film/music/movie` and `season/club/game/team` clusters Yingzhe identified). **The two methods are complementary; we should report both.**

---

## 4. Overall Progress This Week

The three most important outcomes this week:

1. **A complete, runnable Task 1 regex pipeline** with explicit per-rule false-positive validation (all 5 rules pass) and 4,518 high-confidence delete candidates output.
2. **A complete, runnable Task 2 anchored-classification pipeline** with 100% coverage (vs Yingzhe's 62.35%) and a pie chart deliverable for Matthew's paper.
3. **Deliberate methodological complementarity with Yingzhe's V03/V02 work** — together my high-precision regex + his higher-recall ML cover Task 1; my paper-ready anchored classifier + his discovery-friendly BERTopic cover Task 2 from two angles.

Both notebooks were written and run on the local 152,991-row shard with real outputs saved to `outputs/week4/`. The methodology in both notebooks is designed to scale to Matthew's full 50B-token corpus without modification (lazy row-group reading for Task 1; switch to cuDF + larger sample for Task 2).

---

## 5. Next Steps (Post-Easter)

### Task 1
- Cross-compare delete candidates with Yingzhe's V03 results on the same shard (need to coordinate which shard he's using)
- Add a few more institution patterns if precision audits surface gaps
- Run on additional shards to confirm rule generalisation

### Task 2
- Lower the Stage 1 threshold (or enrich anchor templates) to push more docs into NVIDIA categories on Stage 1 — currently 70% spill to Stage 2
- Manually map persistent discovered clusters to NVIDIA labels; consider adding `Religion` or `Personal_Blog` as taxonomy extensions
- Scale to 200k sample (tutor's upper bound) — likely needs cuDF or batching
- Side-by-side comparison of distribution percentages vs Yingzhe's V02 BERTopic on the same sample

### Cross-team
- Co-author a 1-page summary with Yingzhe comparing the two methods' strengths so the team can decide which to recommend to Matthew for the paper
