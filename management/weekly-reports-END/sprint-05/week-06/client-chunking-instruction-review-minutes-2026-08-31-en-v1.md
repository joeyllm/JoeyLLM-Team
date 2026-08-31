# Client Chunking Instruction Review and Team Planning Record (V1)

## 1. Meeting Information

| Field | Details |
| --- | --- |
| Project | Southern-cross AI / JoeyLLM |
| Meeting type | Asynchronous client email instruction review and team execution planning record |
| Sprint / week | Sprint 5; week commencing 31 August 2026 |
| Date | 31 August 2026 |
| Time | Asynchronous email exchange; this record does not represent a synchronous meeting with a start and finish time |
| Channel | Email |
| Client | Matthew Altenburg |
| Team email sender | Yingzhe Xu |
| Minutes prepared by | Nuo Chen |
| Participation | Matthew Altenburg (Client) and Yingzhe Xu participated in the email exchange; Nuo Chen converted the correspondence into this planning record |
| Meeting objective | Record the Client's confirmation of last week's exact-hash deduplication results, close further SimHash/MinHash reduction work, and move this week's priority to understanding and implementing chunking with the open-source Chonkie library |
| Related milestone | Prepare the exact-hash-cleaned data as a cleaned, chunked, vectorisation-ready dataset and provide notebooks that the Client can inspect, reproduce, and continue |
| Document status | Local V1 draft; Sprint, Action owners, common deadline, output directory, and sharing method are confirmed. The cleaned input version and chunking parameters remain subject to execution-stage verification |

### Record Boundary

This document is based on the team's enquiry email and Matthew Altenburg's reply. It records asynchronous written instructions and does not claim that a synchronous meeting occurred or that chunking has already been completed.

The prefix `S5-CH-*` is used for Chunking requirements, decisions, actions, risks, and improvements. This distinguishes the work from existing Sprint 5 Mobile tickets and maintains unique, traceable identifiers across GitHub issues and meeting evidence.

The Client stated that the approximately 70% duplication rate reported last week was consistent with findings from the Ugly Face team and another AI engineer. This is recorded as client-confirmed external validation, but it does not replace the notebook, audit summary, or row-count reconciliation evidence.

The Client explicitly advised that no further dataset reduction using SimHash is required. The focus for this week is to understand the chunking process, attempt chunking with Chonkie, and ensure the Client can access and continue the notebooks.

## 2. Email Background

The team advised the Client that it had planned to continue working on the SimHash and MinHash notebooks and asked whether there were any additional priorities or improvements required for the hash work completed last week.

The Client confirmed that:

1. Last week's work was excellent.
2. No further dataset reduction with SimHash is required.
3. The approximately 70% duplication result was consistent with two external technical sources.
4. This week's main focus should be understanding the chunking process.
5. The open-source Chonkie library should be used to support this work.
6. The team should complete chunking if feasible.
7. If full chunking cannot be completed, the notebooks must still be visible and usable by the Client.

## 3. Review of Previous Work

| Previous work | Previous result | Client feedback | Impact on this week |
| --- | --- | --- | --- |
| Exact-hash deduplication | The team completed hash-based duplicate analysis and reported approximately 70% duplication | The Client accepted the result and advised that the Ugly Face team and another AI engineer observed a similar rate | Do not redesign or unnecessarily rerun the exact-hash analysis; retain the notebook and audit evidence |
| SimHash / MinHash planning | The team originally intended to continue near-duplicate investigation | The Client stated that no additional reduction using SimHash is needed | Do not perform near-duplicate deletion or threshold tuning this week |
| Vector-ready data preparation | The exact-hash-cleaned data still requires chunking | The Client nominated Chonkie and prioritised understanding the chunking process | Establish a chunking research, pilot, execution, validation, and notebook handover workflow |

## 4. Client Requirements and Team Responses

| Requirement ID | Client requirement / feedback | Team response and rationale | Outcome | Related items |
| --- | --- | --- | --- | --- |
| S5-CH-CR01 | Last week's work was excellent and the approximately 70% duplication result was accurate | Accept the result and retain the existing deduplication notebook, summary, and validation evidence | The exact-hash result is accepted by the Client | S5-CH-D01, S5-CH-A01, S5-CH-I01 |
| S5-CH-CR02 | No further dataset reduction using SimHash is required | Stop SimHash/MinHash near-duplicate removal and threshold tuning | Near-duplicate reduction is removed from scope | S5-CH-D02, S5-CH-A01, S5-CH-I02 |
| S5-CH-CR03 | The main focus is understanding the chunking process | Define the input unit, chunk boundaries, size, overlap, metadata, and validation before considering a full run | Chunking understanding becomes the first priority | S5-CH-D03, S5-CH-A02, S5-CH-I03 |
| S5-CH-CR04 | Use the open-source Chonkie library | Review the API and environment compatibility, select an appropriate chunker, and then run a pilot | Chonkie is the designated chunking tool | S5-CH-D04, S5-CH-A02, S5-CH-A03, S5-CH-I04 |
| S5-CH-CR05 | Complete chunking if possible | Validate a representative pilot before deciding whether time, storage, and compute resources permit a full run | Full execution depends on successful pilot and preflight checks | S5-CH-D05, S5-CH-A03, S5-CH-A04, S5-CH-I05 |
| S5-CH-CR06 | If chunking cannot be completed, ensure that the Client can see and continue the notebooks | Treat notebook handover as the minimum deliverable regardless of full-run completion | Establish reproducible and client-visible notebook evidence | S5-CH-D06, S5-CH-A05, S5-CH-I06 |

## 5. Decisions and Rationale

| Decision ID | Decision | Rationale / evidence | Confirmed by | Effective date |
| --- | --- | --- | --- | --- |
| S5-CH-D01 | Accept last week's exact-hash deduplication result and do not unnecessarily repeat the analysis | The approximately 70% duplication rate was confirmed by the Client and two external technical sources | Matthew Altenburg / Client | 31 August 2026 |
| S5-CH-D02 | Stop using SimHash or MinHash to further reduce the dataset | The Client explicitly removed this work from the current scope | Matthew Altenburg / Client | 31 August 2026 |
| S5-CH-D03 | Prioritise understanding and documenting the chunking process before pursuing a full-dataset output | The Client identified process understanding as the main focus, and a large-scale run requires validated methods and resources | Client requirement and team execution decision | 31 August 2026 |
| S5-CH-D04 | Use Chonkie for research and pilot testing, but do not process the full dataset with unvalidated parameters | Chunker type, size, overlap, and boundaries directly affect retrieval quality | Client requirement and team safety decision | 31 August 2026 |
| S5-CH-D05 | Run full-dataset chunking only after the preflight, pilot quality review, resource estimate, and output contract pass | An uncontrolled full run could waste time, storage, and compute resources | Team reliability decision | 31 August 2026 |
| S5-CH-D06 | Deliver client-visible, reproducible, and resumable notebooks whether or not full chunking is completed | The Client explicitly identified notebook visibility as the minimum outcome | Matthew Altenburg / Client | 31 August 2026 |

### Scope Controls

- Do not perform SimHash or MinHash near-duplicate deletion this week.
- Do not tune the previous approximately 0.8 near-duplicate threshold unless the Client reopens that scope.
- Do not modify the immutable source dataset.
- Do not run an embedding model or insert vectors into Qdrant.
- Limit this work to chunking research, Chonkie evaluation, pilot/full chunking where feasible, validation, and notebook handover.
- The Client remains responsible for vectorisation and Qdrant ingestion.

## 6. Action Items

### Issue: Understand and implement AUTokens50 chunking with Chonkie

| Action ID | Task | Accountable owner | Main deliverable | Due date | Acceptance criteria | Status |
| --- | --- | --- | --- | --- | --- | --- |
| S5-CH-A01 | Confirm deduplicated input and freeze near-duplicate work | Xiang Chang | Confirm the exact-hash-cleaned input; record its manifest, schema, row count, and deduplication summary; close SimHash/MinHash reduction scope | 1 September 2026 | Input is traceable; the 70% result has notebook/audit evidence; no near-duplicate deletion is performed | Open |
| S5-CH-A02 | Research Chonkie and design the chunking contract | Yingzhe Xu | Evaluate suitable Chonkie chunkers and define chunk unit, size, overlap, boundaries, metadata, stable chunk IDs, provenance, and output schema | 1 September 2026 | A justified parameter recommendation and design note exist; no full run begins with unconfirmed parameters | Open |
| S5-CH-A03 | Build and validate a representative pilot | Xingyu Li | Build a representative sample, generate chunks with candidate Chonkie settings, and inspect boundaries, empty chunks, length outliers, metadata, and traceability | 1 September 2026 | Pilot is reproducible, covers short/long/edge-case content, and passes documented quality checks | Blocked by S5-CH-A01 and S5-CH-A02 |
| S5-CH-A04 | Execute resumable full-dataset chunking if feasible | Nuo Chen | After pilot approval and resource checks, process the cleaned dataset with batching/streaming, checkpoints, partitioned outputs, and safe writes | 1 September 2026 | Source data is unchanged; output can be resumed and read by partition; statistics and failures are recorded; any incomplete run has a documented reason | Blocked by S5-CH-A03 |
| S5-CH-A05 | Prepare client-visible notebooks and handover evidence | Wen Sun | Organise setup, paths, Chonkie configuration, pilot/full-run cells, validation, limitations, resume steps, output manifest, and continuation notes | 1 September 2026 | The Client can use JupyterLab to understand the method, reproduce the pilot, and continue execution without relying on a verbal explanation | Open; minimum required deliverable |

### Shared Execution Constraints

- Centralise and validate all input paths at the beginning of the notebook.
- Never overwrite the source or cleaned dataset.
- Write generated chunks to `Scratch/AUTokens50_chunked_chonkie/`.
- Do not load the entire dataset into pandas at once.
- Do not start a full run before the pilot passes.
- A full run must support checkpoint/resume and clearly distinguish partial and completed output.
- Notebooks must retain Markdown explanations, code, summaries, and known limitations.
- Share notebooks and supporting evidence with the Client through JupyterLab.
- Action S5-CH-A05 remains mandatory even if the full run cannot be completed.

## 7. Questions the Chunking Work Must Answer

| Area | Question | Expected evidence |
| --- | --- | --- |
| Input | Which exact-hash-cleaned dataset is used, what fields does it contain, and how many records are present? | Input manifest, schema, and deduplication summary |
| Chunker | Which Chonkie strategy is suitable for the corpus? | Comparison and selection rationale |
| Size | Is chunk size measured in tokens, characters, or another unit? | Distribution, examples, and retrieval-oriented rationale |
| Boundaries | Are paragraph, sentence, and document boundaries preserved? | Boundary examples and edge cases |
| Overlap | Is overlap required, and if so, by what amount? | Context-continuity and output-expansion assessment |
| Metadata | Which source fields must remain attached to each chunk? | Output schema and sample chunk record |
| Identity | How are stable, unique, traceable chunk IDs generated? | ID rule and uniqueness validation |
| Quality | How are empty, duplicate, short, long, or corrupted chunks detected? | Validation report and failure samples |
| Scale | What time, storage, and memory does a full run require? | Pilot throughput and resource estimate |
| Handover | How can the Client rerun, resume, or change parameters? | Notebook, instructions, run state, and output manifest |

## 8. Risks and Blockers

| Risk ID | Risk / blocker | Impact | Mitigation | Owner | Required decision | Status |
| --- | --- | --- | --- | --- | --- | --- |
| S5-CH-R01 | Chonkie API, version, or dependencies are not yet verified | Notebook may not run in JupyterLab | Complete package/version preflight and document installation | Yingzhe Xu | Confirm permitted installation method | Open |
| S5-CH-R02 | Chunk size, overlap, and boundary strategy are unconfirmed | Output may not suit retrieval | Compare designs with a representative pilot before full execution | Yingzhe Xu / Xingyu Li | Determine whether Client approval is required before full run | Open |
| S5-CH-R03 | Dataset scale may exceed Scratch capacity or the available execution window | Full run may stop or remain incomplete | Estimate expansion and use batches, partitions, and checkpoints | Nuo Chen | Confirm Scratch quota, retention, and runtime limits | Open |
| S5-CH-R04 | Overlap may reintroduce substantial duplicated text | Increased vectorisation cost and storage | Report overlap expansion ratio and chunk counts in the pilot | Xingyu Li | Agree on acceptable continuity/cost trade-off | Open |
| S5-CH-R05 | Metadata or source provenance may be lost | Chunks cannot be traced to their source records | Require source ID, row/part reference, and chunk index in the output contract | Yingzhe Xu / Xingyu Li | Confirm required metadata | Open |
| S5-CH-R06 | Pursuing a full run may leave insufficient time for handover | Client cannot continue the next stage | Keep S5-CH-A05 independent of S5-CH-A04 and share through JupyterLab | Wen Sun | Confirm Client JupyterLab access | Open |
| S5-CH-R07 | The approximately 70% result may lack consolidated linked evidence | Sprint evidence is less traceable | Link the dedup summary, audit evidence, and Client email from the handover notebook | Xiang Chang / Wen Sun | Confirm the evidence location | Monitoring |

## 9. Continuous Improvements

| Improvement ID | Observation | Process improvement | Success criterion | Related Action |
| --- | --- | --- | --- | --- |
| S5-CH-I01 | External validation and internal evidence are distributed across locations | Place the Client confirmation, dedup summary, input snapshot, and final counts in one handover index | The Client can trace the 70% result from one entry point | S5-CH-A01, S5-CH-A05 |
| S5-CH-I02 | The team planned to continue SimHash/MinHash before the Client changed the scope | Add a client scope-confirmation gate at the start of each week | No out-of-scope near-duplicate deletion code or outputs are created | S5-CH-A01 |
| S5-CH-I03 | Beginning implementation immediately could bypass process understanding | Define the chunking contract, build a pilot, and only then decide on the full run | Parameters, boundaries, and metadata have documented rationale | S5-CH-A02, S5-CH-A03 |
| S5-CH-I04 | A new open-source dependency may be difficult to reproduce | Pin the Chonkie and runtime versions and document setup and fallback steps | The Client can reproduce the pilot in the same Jupyter environment | S5-CH-A02, S5-CH-A05 |
| S5-CH-I05 | Large runs can stop and leave ambiguous partial output | Use partitions, checkpoints, run state, partial naming, and a completion manifest | Interrupted work can be resumed and valid outputs can be identified | S5-CH-A04 |
| S5-CH-I06 | Treating only a completed full run as success overlooks handover needs | Define a readable, reproducible, and continuable notebook as an independent Definition of Done | The Client can continue even when the full run is incomplete | S5-CH-A05 |

## 10. Minimum Delivery Package

Regardless of whether full-dataset chunking is completed, the team must provide:

1. An accessible Chonkie chunking notebook.
2. Environment and dependency versions.
3. Confirmed input path, schema, and manifest.
4. An explanation of strategy, size, overlap, boundaries, and metadata.
5. A runnable representative pilot.
6. Pilot samples and a validation summary.
7. Full-run code or clear continuation steps.
8. Checkpoint and resume instructions.
9. Known limitations and unresolved decisions.
10. JupyterLab access to the notebooks, outputs, and evidence in `Scratch/AUTokens50_chunked_chonkie/`.

## 11. Closure and Approval

| Check | Result |
| --- | --- |
| Previous hash work | The Client rated the work highly and confirmed that the approximately 70% duplication rate matched external observations |
| SimHash / MinHash | No longer used for dataset reduction in the current scope |
| First priority | Understand chunking and use Chonkie for pilot implementation |
| Minimum deliverable | Client-visible, understandable, reproducible, and continuable notebooks |
| Full-run expectation | Complete if methods, resources, and time permit; otherwise document limitations and continuation steps |
| Actions | S5-CH-A01 to S5-CH-A05 |
| Decisions | S5-CH-D01 to S5-CH-D06 |
| Improvements | S5-CH-I01 to S5-CH-I06 |
| Owners / deadline | Xiang Chang, Yingzhe Xu, Xingyu Li, Nuo Chen, and Wen Sun; common due date: 1 September 2026 |
| Output / sharing | `Scratch/AUTokens50_chunked_chonkie/`; notebooks and evidence shared through JupyterLab |
| Minutes prepared by / date | Nuo Chen, 31 August 2026 |
| Review status | Local V1 draft; Sprint, owners, deadline, output, and sharing are confirmed; technical parameters remain subject to execution-stage verification |
| Distribution | Southern-cross AI team; may be retained as Sprint / TechLauncher evidence after team review |

## Local Draft Quality Check

- [x] The correspondence is accurately identified as an asynchronous Client instruction rather than a synchronous meeting.
- [x] The Client's positive assessment and validation of the approximately 70% duplication result are recorded.
- [x] SimHash/MinHash reduction is removed from scope.
- [x] Chonkie and chunking-process understanding are identified as the priority.
- [x] Full execution is separated from the minimum notebook handover.
- [x] The record does not claim that chunking, embedding, or Qdrant insertion is complete.
- [x] Immutable-source and no-vectorisation boundaries are retained.
- [x] Sprint 5 uses the unique `S5-CH-*` prefix to avoid duplicate ticket names.
- [x] All owners and the common due date are recorded.
- [x] The output directory and JupyterLab sharing method are recorded.
- [ ] Confirm the exact cleaned input path and version.
- [ ] Confirm Chonkie version, chunker, size, overlap, boundaries, and metadata.
- [ ] Confirm Scratch quota, retention, and long-term archival arrangements.
