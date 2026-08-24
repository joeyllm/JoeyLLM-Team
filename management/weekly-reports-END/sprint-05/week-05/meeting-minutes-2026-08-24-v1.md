# Client Mobile Completion and Data-Cleaning Planning Meeting Minutes (V1)

## 1. Meeting Information

| Field | Details |
| --- | --- |
| Project | Southern-cross AI / JoeyLLM |
| Meeting type | Synchronous client meeting and team execution-planning meeting |
| Sprint / week | Sprint 5; Semester 2, Week 5 |
| Date | 24 August 2026 |
| Time | Commenced at 10:10 am AEST and lasted approximately 30 minutes |
| Location / channel | Online meeting; the specific platform was not recorded |
| Chair / instruction owner | Matthew Altenburg, Client |
| Minute taker | Nuo Chen |
| Attendees | Matthew Altenburg (Client), Nuo Chen, Xiang Chang, Yingzhe Xu, Xingyu Li, Wen Sun |
| Apologies / absences | Not recorded; these minutes do not infer the attendance status of anyone not explicitly identified |
| Meeting objective | Complete and validate the Mobile UI; begin planning AUTokens50 exact-hash data cleaning; and clarify responsibilities for near-duplicate validation, chunking, vectorisation, Qdrant, and post-launch support for Joey |
| Related Sprint Goal / milestone | Complete Joey's mobile and production readiness so that Joey is ready to go live and can be tested after launch, while beginning preparation of an Australian dataset that is cleaned, deduplicated, chunked, and ready for vectorisation |
| Document status | Principal Action owners and the Client's Mobile acceptance result have been added; team confirmation of deadlines and remaining technical details is pending |

### Record Boundary

This document is based on the approximately 30-minute Client meeting held on 24 August 2026, the Client's follow-up email, and the team's breakdown of the two principal workstreams. Technical implementation decisions and team process improvements are distinguished from Client decisions. Client decisions capture the priorities and responsibility boundaries confirmed by the Client; team decisions describe the engineering approach adopted to implement those requirements.

The dataset figures `21,087,435`, `6,008,596`, and `15,078,839` are observed baselines from the existing notebook and must still be revalidated by the production pipeline against the current read-only dataset. SimHash and MinHash terminology was used inconsistently during the meeting. These minutes do not treat them as the same algorithm and do not authorise deletion using either approximate-similarity method.

## 2. Agenda

1. Review completion of last week's Joey Modes and Mobile work.
2. Confirm Mobile integration, hamburger navigation, manual responsive testing, and handover requirements.
3. Record the Joey go-live plan and post-launch production-support expectations.
4. Confirm the scope of exact-hash deduplication, the read-only source dataset, and the Scratch output boundary.
5. Divide the exact-hash pipeline into five auditable Actions.
6. Clarify SimHash/MinHash terminology, the approximate `0.8` candidate threshold, and manual sample-validation requirements.
7. Define responsibilities for chunking, vectorisation, and Qdrant.
8. Record team improvements for branch integration, two-layer UI testing, large-data safety, and auditing.
9. Confirm the evidence, risks, dependencies, and materials required for the next Client review.

## 3. Review of Previous Actions

| Previous ID | Action / deliverable | Previous owner | Previous due date | Current status | Completion evidence | Current impact / follow-up |
| --- | --- | --- | --- | --- | --- | --- |
| S5-A01 to S5-A05 | Mobile-first responsive implementation | Mobile team | 21 August 2026 | Integrated and locally validated; final Client acceptance was pending at the time of the earlier review | Unified Mobile implementation, hamburger/drawer, local build, and browser checks | Forms the pre-launch Mobile baseline for Joey |
| S5-A06 to S5-A10 | Mobile QA and accessibility validation | QA team | 21 August 2026 | Executed; the complete automated test result for this cycle was 28/28 passed | Playwright responsive/focus tests, manual Chrome testing, and defect-fix records | Retained as the regression suite for pre-launch and post-launch validation |
| S5-A11 to S5-A15 | Five Joey personalities | Five Personality owners | 21 August 2026 | Reviewed by the Client and merged into `main` | Client email and the Modes merged into `main` | Personality work is complete; only production regressions remain in scope |
| S5-PBI05 | Vector/Qdrant work | Client and Data team | Deferred for further planning this week | Scope clarified | Decisions from this meeting | The team prepares vector-ready data; the Client owns vectorisation and Qdrant |

## 4. Current Progress and Evidence Presented

| PBI / work item | Current progress | Validated status | Evidence presented / available | Stakeholder impact | Current gap |
| --- | --- | --- | --- | --- | --- |
| S5-PBI01 Mobile integration | Mobile work previously distributed across several branches has been consolidated into one implementation using a hamburger menu and drawer on mobile | Team local validation completed; Client acceptance result: "Meets expectations" | Mobile branch, commit history, build, Playwright report, and Chrome viewport screenshots | Removes the principal UI blocker before Joey goes live | Continue retaining regression evidence until launch |
| S5-PBI02 Mobile visual regression | Manual testing identified and resolved Sydney speech-bubble overflow and Coastal wave artwork covering text | 28/28 tests passed after the fixes, with manual checks completed | Before/after screenshots and targeted regression tests | Improves readability of different Joey Modes on narrow screens | Real-device and user-feedback validation remains necessary after launch |
| S5-PBI03 Exact-hash data cleaning | The team divided the notebook's 15 stages into five responsibility-based Actions | Planned; the full production pipeline has not yet run | `AUTokens50_global_exact_hash_dedup_v2.ipynb` design and five Action definitions | Produces cleaner data for later chunking and vector-database preparation | Paths, capacity, schema, baseline, and ownership details require formal verification |
| S5-PBI04 Near-duplicate validation | The Client proposed an approximate `0.8` similarity threshold and required manual sampling | Deferred pending completion of exact-hash processing | Sampling plan recorded in these minutes | Reduces the risk of false deletion during similarity deduplication | The actual similarity algorithm and later threshold-review method are provisional |
| S5-PBI05 Chunking and vector handover | Responsibility boundary confirmed: the team prepares cleaned/chunked data; the Client performs vectorisation and Qdrant insertion | Scope confirmed; implementation not started | Client email and meeting decisions | Prevents duplication of work or unauthorised server-side vector processing | Chunk size, boundaries, overlap, metadata, and output contract require discussion |
| S5-PBI06 Joey go-live readiness | The Client expects Joey to go live on 31 August 2026, with possible external or media promotion approximately two weeks later | The launch date is an estimate; actual deployment has not been recorded | Client email / meeting statement | Moves the project into production-readiness and maintenance | Monitoring, incident ownership, and conversation-logging validation remain to be confirmed |

## 5. Client Requirements, Discussion, and Team Response

| Requirement ID | Source / topic | Client requirement or concern | Team response and rationale | Outcome | Related Decision / Action / Improvement |
| --- | --- | --- | --- | --- | --- |
| S5-CR01 | Mobile priority | Mobile work had to be consolidated into one complete implementation rather than remain distributed across branches | Accepted. The team established a unified Mobile integration and a single handover point | Mobile was completed as the first priority | S5-D01, S5-A01, S5-I01 |
| S5-CR02 | Mobile navigation | The complete sidebar must not remain permanently visible on small screens; it must use a three-dot or standard hamburger/drawer menu | Accepted. A standard three-line hamburger and overlay drawer were adopted | Mobile navigation implemented and tested | S5-D02, S5-A02, S5-I02 |
| S5-CR03 | Manual UI validation | The website must be opened and visually checked at different Chrome sizes; Playwright alone is insufficient | Accepted. A two-layer automated and manual acceptance process was established | Target viewports were tested and personality-specific problems were fixed | S5-D03, S5-A03, S5-I03 |
| S5-CR04 | Integrated Definition of Done | Completion of individual branches does not mean that the complete Mobile feature is finished | Accepted. Final acceptance applies to the integrated branch, build, automated tests, and manual checks | A unified Mobile DoD was established | S5-D04, S5-A04, S5-I04 |
| S5-CR05 | Go-live readiness | Joey will enter formal launch preparation after Mobile is completed | Accepted. Pre-launch regression and handover evidence are retained | Mobile delivery is connected to production readiness | S5-D05, S5-A05, S5-I05 |
| S5-CR06 | Exact duplicates | Existing exact hashes must be used first to identify and remove exact duplicates | Accepted. The 57 Parquet files will be scanned globally as one logical dataset | A five-stage exact-hash pipeline was defined | S5-D06, S5-A06, S5-I06 |
| S5-CR07 | Immutable source / Scratch | The original dataset is locked/immutable, and cleaned output must be written to Scratch | Accepted. Production writes and audit artifacts remain within Scratch during processing | Path, snapshot, and fail-closed controls were established | S5-D07, S5-A07, S5-I07 |
| S5-CR08 | Near-duplicate threshold | The approximate `0.8` similarity threshold must not be trusted without manual sampling | Accepted. Exact-hash and near-duplicate processing remain separate | MinHash/SimHash deletion remains frozen | S5-D08, S5-A08, S5-I08 |
| S5-CR09 | Vector-database boundary | The team is not responsible for running embeddings or inserting vectors into Qdrant | Accepted. The team will deliver a cleaned, deduplicated, chunked, vector-ready dataset | The Client retains ownership of vectorisation and Qdrant | S5-D09, S5-A09, S5-I09 |
| S5-CR10 | Production support | After launch, the final Sprint is likely to focus on production testing, bug fixing, and user feedback | Accepted. A production issue/evidence workflow will be established | Maintenance work is included in subsequent planning | S5-D10, S5-A10, S5-I10 |

## 6. Decisions and Rationale

### 6.1 Mobile UI Decisions

| Decision ID | Final decision | Rationale / evidence considered | Confirming party | Impacted scope | Effective date |
| --- | --- | --- | --- | --- | --- |
| S5-D01 | All Mobile work must be consolidated into a unified Mobile branch based on the latest `main` | Distributed branches cannot represent one complete and reviewable experience | Client requirement; confirmed through team implementation | Mobile integration | 24 August 2026 |
| S5-D02 | The Mobile sidebar remains closed by default and is opened by a standard hamburger button | Small screens must return the available width to the core chat experience | Client requirement; confirmed through team implementation | Navigation, header, and focus | 24 August 2026 |
| S5-D03 | Mobile acceptance must include both Playwright and manual responsive checks in Chrome | Automation cannot fully detect visual obstruction, layering, and readability defects | Client requirement and Sydney/Coastal defect evidence | QA and review evidence | 24 August 2026 |
| S5-D04 | Different Joey Modes must be included in personality-specific mobile regression testing | Each Mode has different mascot, background, and speech-bubble structures | Team improvement decision based on observed defects | A07 and visual regression | 24 August 2026 |
| S5-D05 | Mobile can be marked feature-complete only after integration, build, automated testing, manual testing, and the review package are complete | Completion of individual tasks does not prove that the integrated version is production-ready | Client requirement and team DoD | Joey go-live gate | 24 August 2026 |

### 6.2 Exact-Hash Data-Cleaning Decisions

| Decision ID | Final decision | Rationale / evidence considered | Confirming party | Impacted scope | Effective date |
| --- | --- | --- | --- | --- | --- |
| S5-D06 | Before any scan, complete a preflight covering paths, schemas, 57 files, DuckDB row numbering, and an immutable-source snapshot | The dataset exceeds 100 GB; an incorrect path or row mapping would create a high-cost error | Team safety design implementing the Client's immutable-source requirement | Data Action 1 | 24 August 2026 |
| S5-D07 | Use the persisted `hash` column to perform global exact-duplicate discovery across all 57 Parquet files; do not infer or recompute the hash algorithm | Duplicates across parts cannot be found through per-file deduplication | Client exact-hash requirement and team engineering design | Data Action 2 | 24 August 2026 |
| S5-D08 | For each repeated hash, select one survivor by lower `part_number` and then lower `file_row_number`; stop automatic deletion for same-hash/different-text anomalies | Ensures reproducibility, traceability, and protection against collision/anomaly deletion | Team provenance and fail-closed decision | Data Action 3 | 24 August 2026 |
| S5-D09 | Rewrite data using per-part removal indexes, PyArrow batches, bounded concurrency, and `.partial` safe writes, applying row filtering only | Prevents out-of-memory failures, incomplete files appearing valid, and schema changes | Team reliability decision | Data Action 4 | 24 August 2026 |
| S5-D10 | Mark the pipeline `completed` only when row conservation, hash uniqueness, schema preservation, and source immutability all pass | File existence or the absence of runtime errors does not prove correctness | Team audit decision | Data Action 5 | 24 August 2026 |

### 6.3 Scope Decisions

- No record will be deleted using SimHash, MinHash, embedding similarity, or LLM judgement during this stage.
- Approximately `0.8` is only a candidate near-duplicate threshold. The Client must confirm it after manual inspection of 10–20 pairs near the threshold, or up to approximately 50 pairs where practical.
- Chunk size, overlap, paragraph/document boundaries, metadata, and output structure will be discussed after the exact-hash pipeline is complete.
- The team will not run the embedding model or write vectors to Qdrant. The Client owns server-side vectorisation and Qdrant setup.
- `Scratch` is a working directory and not reliable permanent storage. The target persistent archive for important outputs is the `JoeyLLM_Data` directory. Because that directory is currently read-only, final transfer requires Client/administrator action or explicit write authorisation. The team must not bypass the read-only control.

## 7. Risks, Blockers, Deferrals, and Scope Changes

| ID | Risk / blocker / change | Impact on objectives | Current mitigation | Accountable owner | Clarification / decision required | Review date | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S5-R01 | Mobile automation can pass while visual obstruction remains | Mode-specific UI defects may appear after launch | Manual Chrome testing and personality regression tests | Xiang Chang | Whether the Client has priority physical devices | Next Client review | Monitoring |
| S5-R02 | The expected 31 August 2026 go-live date is close | The review and defect-fix window is short | Retain the full regression suite, manual checklist, and rapid rollback evidence | Xiang Chang | Actual go-live completion and go/no-go owner | Before 31 August 2026 | Open |
| S5-R03 | Notebook design paths and Jupyter UI paths differ | The wrong directory could be read or data could be written outside Scratch | Action 1 must resolve absolute paths and validate output containment | Yingzhe Xu | Actual mapping among `/data/...`, `JoeyLLM_Data/...`, and Scratch | Before the data run | Open |
| S5-R04 | Scratch may be non-persistent and its capacity is unconfirmed | Long-running rewrite output may be lost or exhaust storage | Check `df`/quota before execution, use partitioned output and run state, then archive important output to the designated `JoeyLLM_Data` location | Yingzhe Xu | Confirm Client/administrator transfer process or `JoeyLLM_Data` write authorisation | Before the data run | Open |
| S5-R05 | The 57 files exceed 100 GB | A full pandas load may cause OOM or kernel failure | DuckDB column pruning, PyArrow batches, and bounded concurrency | Yingzhe Xu | CPU, RAM, I/O, and worker calibration | After dry run | Monitoring |
| S5-R06 | Incorrect `file_row_number` base or filename mapping | Incorrect rows could be deleted | Synthetic probe and exact filename-mapping gate | Yingzhe Xu | None; this gate must pass before continuation | At completion of Action 1 | Open |
| S5-R07 | The same hash may map to different stored text | Automatic deduplication could delete non-identical content | Exact stored-text validation and STOP on anomaly | Yingzhe Xu | Client treatment of anomaly groups | Escalate immediately if observed | Monitoring |
| S5-R08 | SimHash and MinHash terminology was mixed during the meeting | The wrong algorithm or threshold could be adopted | Keep exact and near-duplicate pipelines separate | Yingzhe Xu / Client | Actual near-duplicate algorithm and later threshold-review method remain provisional | After exact deduplication | Deferred |
| S5-R09 | Current notebook baselines may differ from the current dataset version | Expected row counts may be wrong | Recalculate every value from the current input and use the baseline for comparison only | Yingzhe Xu | Dataset version and file snapshot | After Action 2 | Open |
| S5-R10 | Availability, UI, response-quality, or offensive-content incidents may occur after launch | Production incidents may interrupt final-Sprint work | Production issue log, severity, reproduction, and regression workflow | Team and Client, ownership to be divided | Client incident channel, SLA, and ownership | Before launch | Open |

## 8. New Action Items

### Issue 1: Complete and Validate the Unified Mobile Implementation

| Action ID | Subtask | Accountable owner | Branch / environment | Principal deliverable | Due date | Acceptance criteria | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S5-A01 | Consolidate all Mobile work | Xiang Chang | Unified `mobile` branch | Integrate navigation, header, 100dvh/composer, overflow, tablet/desktop behaviour, and A07/A08 tests on the latest `main` | Completed | One branch contains the complete Mobile experience, with no direct changes to `main`, `beta`, or `live` | Completed |
| S5-A02 | Implement hamburger navigation and drawer | Xiang Chang | Unified `mobile` branch | Standard three-line trigger; drawer closed by default; close through backdrop, Escape, and Mode selection; focus trap and focus return | Completed | The sidebar is not permanently visible on small screens; full keyboard and touch operation is available | Completed |
| S5-A03 | Execute automated and manual responsive QA | Xiang Chang | Local Chrome and Playwright | Test 667×375, 844×390, 768×1024, 1024×768, the 768px breakpoint, keyboard/focus, and the core chat flow; manually resize Chrome | Completed | Complete result is 28/28 passed and the manual viewport checklist is complete | Completed |
| S5-A04 | Fix personality-specific mobile regressions | Xiang Chang | Unified `mobile` branch | Fix Sydney speech-bubble overflow and Coastal wave artwork covering text; add 390×844 regression tests | Completed | Sydney text remains inside the viewport; Coastal text remains above the wave artwork; the full suite continues to pass | Completed |
| S5-A05 | Prepare Client handover and go-live evidence | Xiang Chang | GitHub `mobile` branch | Organise branch, commits, README/run steps, reports, screenshots, known limitations, and Client checkout instructions | Completed | Client can check out and reproduce the result; Client acceptance result is "Meets expectations" | Completed / Accepted |

#### Shared Mobile Execution Constraints

- Do not directly modify `main`, `beta`, or `live`.
- Automated testing does not replace manual visual testing in Chrome.
- Add a corresponding regression test after every defect found through manual testing.
- The Mobile Definition of Done requires integration, build, automated QA, manual QA, and Client-reviewable evidence.
- Run the complete regression suite again before launch and record the actual Client go-live decision.

### Issue 2: Global Exact-Hash Deduplication of AUTokens50

| Action ID | Subtask | Accountable owner | Notebook cells | Principal deliverable | Due date | Acceptance criteria | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S5-A06 | Dataset Safety & Preflight | Yingzhe Xu | Cells 1–5 | Validate actual paths, Scratch containment, 57 files, schema, `text/hash/simhash`, DuckDB row-number base, filename mapping, pre-run snapshot, and run state | To be confirmed | Read-only input; separate input/output; all file, schema, and path-mapping gates pass; audit artifacts completed | Open |
| S5-A07 | Global Duplicate Discovery | Yingzhe Xu | Cells 6–7 | Globally scan hash integrity and generate duplicate hashes and statistics without deleting data | To be confirmed | All 57 files form one dataset; NULL/empty hash handling is explicit; every `COUNT(*) > 1` group is recorded | Blocked by S5-A06 |
| S5-A08 | Survivor & Removal Planning | Yingzhe Xu | Cells 8–9 | Select survivors by part/row order, generate removed rows, verify exact stored text, and STOP on anomaly | To be confirmed | One survivor per group; removed rows are fully traceable; same-hash/different-text records are not automatically deleted | Blocked by S5-A07 |
| S5-A09 | Parallel Dataset Rewrite | Yingzhe Xu | Cells 10–11 | Build per-part removal indexes and use PyArrow batches, bounded parallelism, and `.partial` safe writes to generate cleaned parts | To be confirmed | 57 outputs; schema, metadata, and values preserved; correct per-part row relationships; source unchanged | Blocked by S5-A08 |
| S5-A10 | Validation & Audit | Yingzhe Xu | Cells 12–15 | Perform per-file/global validation, row/hash conservation, post-run source snapshot, SHA-256 immutability proof, and summary | To be confirmed | Zero remaining duplicate groups; one output row per hash; schema preserved; source unchanged; mark completed only after all checks pass | Blocked by S5-A09 |

#### Shared Data Execution Constraints

- Use the actual input path resolved by the Jupyter preflight; the current UI displays `JoeyLLM_Data/AUTokens50_with_hash_simhash`.
- All processing writes must remain under `Scratch`; the proposed root is `Scratch/AUTokens50_exact_hash_dedup/`.
- Do not modify, rename, delete, or overwrite any file in `JoeyLLM_Data`.
- Do not load the complete dataset into pandas at once.
- Do not recompute or modify `hash`, `simhash`, `text`, or any other source field.
- Do not perform SimHash/MinHash deletion, chunking, embedding, or Qdrant insertion in this pipeline.
- Production execution follows S5-A06 → S5-A07 → S5-A08 → S5-A09 → S5-A10. Later-stage logic may be developed in parallel using synthetic data.
- Scratch is not the only long-term copy. Important output is targeted for persistent archiving in `JoeyLLM_Data`; because it is currently read-only, the Client/administrator must transfer it or grant explicit write authorisation.

## 9. Continuous Improvement

### 9.1 Mobile Improvements

| Improvement ID | Observed issue and evidence | Possible root cause | Improvement / process change | Accountable owner | Success criterion | Review date | Related Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S5-I01 | Mobile work was distributed across several branches | No integration owner or merge order was established early in the Sprint | Establish an integration branch, owner, dependency map, and DoD when related tasks begin | Xiang Chang | No set of branches is described as complete while remaining impossible to review together | Next UI Sprint | S5-A01 |
| S5-I02 | The sidebar permanently occupied chat width on small screens | The desktop navigation model was carried directly into Mobile | Adopt a mobile-first navigation contract covering hamburger, drawer, backdrop, and focus management | Xiang Chang | Core chat width remains usable on phones and the drawer is accessible | Client review | S5-A02 |
| S5-I03 | Automation did not detect the Sydney/Coastal visual defects | QA covered structure and overflow but not layering/readability | Establish two-layer automated/manual QA and a personality test matrix | Xiang Chang | Every Mode is checked for bubble, mascot, heading, composer, and stacking | Before launch | S5-A03, S5-A04 |
| S5-I04 | Visual defects could recur after being fixed | Manual findings were not converted into persistent tests | Use the flow: discover → fix → regression test → full suite | Xiang Chang | Every confirmed defect has reproduction steps or automated coverage | Continuous | S5-A04 |
| S5-I05 | Feature completion was previously judged branch by branch | No integrated delivery standard existed | Use a unified Mobile DoD and Client handover checklist | Xiang Chang | Client can check out, run, test, and issue a review decision | Client review | S5-A05 |

### 9.2 Data Improvements

| Improvement ID | Observed issue and evidence | Possible root cause | Improvement / process change | Accountable owner | Success criterion | Review date | Related Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S5-I06 | Notebook design paths differ from the Jupyter UI, and the dataset exceeds 100 GB | Hard-coded paths and environmental assumptions were not centrally validated | Centralise configuration, path containment, dependency/resource checks, immutable snapshot, and resumable run state | Yingzhe Xu | Fail closed before read/write operations when paths or resources are invalid | S5-A06 | S5-A06 |
| S5-I07 | Per-file deduplication would miss duplicates across parts | Partition files were treated as separate datasets | Use DuckDB column pruning to scan hashes globally across 57 files, separating discovery from deletion | Yingzhe Xu | Duplicate report covers cross-file groups and discovery performs zero deletion | S5-A07 | S5-A07 |
| S5-I08 | Non-deterministic survivors or hash collisions could cause unexplained deletion | No deterministic policy or provenance | Persist survivor/removal plans, verify exact stored text, and STOP on anomaly | Yingzhe Xu | Every deletion traces to a survivor and anomalies are not silently deleted | S5-A08 | S5-A08 |
| S5-I09 | A large rewrite may OOM, stop midway, or leave apparently valid incomplete files | Whole-dataset reads, unbounded concurrency, and non-atomic writes | Calibrate batches/workers on samples; use per-part indexes, `.partial` safe writes, checkpoints, and resume | Yingzhe Xu | Failure affects only the current part and completed output is distinguishable from partial output | S5-A09 | S5-A09 |
| S5-I10 | Generated files do not prove correct deduplication | Validation was coupled to generation, without conservation or immutability proof | Independent Validation & Audit, fail-closed completion, and actual-versus-expected summary | Yingzhe Xu | `status: completed` appears only after all invariants pass | S5-A10 | S5-A10 |

## 10. Preparation for the Next Meeting

| Field | Details |
| --- | --- |
| Date / time | To be confirmed by the Client and team; expected go-live date is 31 August 2026 |
| Meeting type | Mobile final review and Data pipeline checkpoint |
| Purpose | Record Mobile Client acceptance; review paths, schema, resources, and the actual duplicate baseline from Data Actions 1–2; confirm the timing of near-duplicate and chunking decisions |
| Pre-meeting Mobile evidence | `mobile` branch, latest-`main` ancestry, README/run steps, 28/28 report, Chrome screenshots, Sydney/Coastal regression evidence, and known limitations |
| Pre-meeting Data evidence | Actual absolute paths, Scratch quota, 57-file manifest, schema comparison, DuckDB calibration, source snapshot, hash-integrity summary, and duplicate-discovery summary if available |
| Decisions / clarifications required | Data Action deadlines; actual go-live completion; administrator transfer/write authorisation for persistent `JoeyLLM_Data` archiving; provisional near-duplicate algorithm and threshold-review method; chunking workshop timing; production incident channel |
| Presenters | Xiang Chang (Mobile), Yingzhe Xu (Data), and other team members as required by the agenda |

### Proposed Agenda for the Next Meeting

1. Mobile final review: Client checkout, hamburger/drawer, target viewports, and personality regressions.
2. Go-live gate: confirm launch date, post-launch testing, conversation logging, and incident ownership.
3. Data preflight: confirm actual paths, Scratch, 57 files, schemas, resources, and immutable snapshot.
4. Exact-duplicate baseline: compare current actual statistics with notebook observations.
5. Pipeline gate: confirm whether discovery may proceed to survivor/removal planning.
6. Near-duplicate planning: confirm terminology, candidate-threshold sampling format, and Client review method.
7. Chunking preparation: arrange discussion of chunk size, boundaries, metadata, and output contract.

## 11. Meeting Close and Approval

| Check | Result |
| --- | --- |
| Mobile Actions | S5-A01 to S5-A05 completed; Client acceptance result: "Meets expectations" |
| Data Actions | S5-A06 to S5-A10 defined and currently Open / Blocked according to their dependencies |
| Decisions recorded | Ten principal decisions, S5-D01 to S5-D10, plus near-duplicate, chunking, and vector-ownership scope controls |
| Improvements recorded | Ten improvements, S5-I01 to S5-I10 |
| Feedback pending | Data Action deadlines, actual go-live completion, persistent `JoeyLLM_Data` archive permission/transfer method, provisional near-duplicate algorithm and threshold-review method, and chunking decisions |
| Risks requiring escalation | S5-R02, S5-R03, S5-R04, S5-R07, S5-R08, S5-R10 |
| Minutes drafted by / date | Nuo Chen, 24 August 2026 |
| Review status | Local V1 draft; awaiting Southern-cross AI team review and confirmation of Client decisions |
| Distribution | Southern-cross AI team; after team review, it may be used as Sprint / TechLauncher evidence |
| GitHub commit / document link | To be decided by the team; the meeting minutes must not be added to the ChatJoey product repository |

## 12. Sprint Checklist Traceability

| Checklist dimension | Evidence provided by these minutes | Direct IDs / sections |
| --- | --- | --- |
| Stakeholder Engagement | Ten Client requirements, Joey go-live plan, manual near-duplicate validation, vector/Qdrant ownership, and next-meeting questions | S5-CR01 to S5-CR10; Sections 5, 6, and 10 |
| Planning and Organisation | Two principal Issues, ten Actions, explicit dependencies, statuses, acceptance criteria, and scope controls | S5-A01 to S5-A10; Sections 7 and 8 |
| Execution and Quality | Mobile integration, hamburger/drawer, manual Chrome testing, 28/28 automation result, Sydney/Coastal fixes, and regression tests | S5-PBI01, S5-PBI02, S5-A01 to S5-A05 |
| Data Safety and Auditability | Read-only source, Scratch containment, global discovery, deterministic survivor, safe rewrite, and independent audit | S5-D06 to S5-D10, S5-A06 to S5-A10 |
| Reflection and Improvement | Ten improvements derived from branch fragmentation, automation blind spots, large-data path/memory risks, provenance, safe writes, and validation | S5-I01 to S5-I10; Section 9 |
| Evidence Traceability | Requirement → Decision → Action → acceptance criteria → Improvement → next-meeting evidence | Sections 5, 6, 8, 9, 10, and 12 |

## Local Draft Quality Check

- [x] Records the date, start time, and approximate 30-minute duration.
- [x] Records only the confirmed attendees and does not infer unrecorded attendance.
- [x] Divides both Mobile and exact-hash data cleaning into five Actions.
- [x] Mobile Actions cover unified integration, hamburger/drawer, automated and manual QA, Sydney/Coastal fixes, and Client handover.
- [x] Data Actions correspond to the five responsibility modules across Notebook Cells 1–15.
- [x] Distinguishes Exact Hash, SimHash, MinHash, embedding, and Qdrant scope.
- [x] Keeps the source dataset immutable and limits processing output to Scratch.
- [x] Labels notebook row-count figures as observed baselines rather than formal results from this meeting.
- [x] Clarifies Client ownership of vectorisation/Qdrant and team responsibility for vector-ready data.
- [x] Records Joey go-live and production support as plans and risks rather than claiming that launch has occurred.
- [x] Confirms the Sprint number as Sprint 5.
- [x] Records Xiang Chang as owner of the Mobile Actions and Yingzhe Xu as owner of the Data Actions.
- [ ] Data Action deadlines still need to be determined.
- [x] Records the Client's acceptance of the `mobile` branch as "Meets expectations".
- [x] Records the expected Joey go-live date as 31 August 2026; actual completion must be confirmed at that time.
- [x] Records `JoeyLLM_Data` as the target for persistent archiving of important output; administrator transfer or write authorisation remains required because the directory is read-only.
- [x] Marks the actual near-duplicate algorithm and subsequent threshold-review method as provisional.

