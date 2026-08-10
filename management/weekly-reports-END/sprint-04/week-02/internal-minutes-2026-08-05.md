# Internal Team Meeting Minutes

## 1. Meeting information

| Field | Details |
| --- | --- |
| Project | Southern-cross AI / JoeyLLM |
| Meeting type | Weekly Internal Team Meeting |
| Sprint / Week | Sprint 4 / Week 2 |
| Date | 5 August 2026 |
| Time | 20:00 AEST; end time not separately recorded |
| Location / Channel | Online team meeting |
| Chair | Xiang Chang |
| Minute taker | Xingyu Li |
| Present | Nuo Chen, Wen Sun, Xiang Chang, Xingyu Li, Yingzhe Xu |
| Apologies / Absent | None |
| Meeting objective | Convert Matthew's instruction and Tutor feedback into a coordinated frontend, Client liaison, research, and evidence plan |
| Related Sprint Goal / Work items | [Sprint 4 Goal](../../../SPRINT4_GOALS.md) / [Nine closed Sprint 4 issues](https://github.com/joeyllm/JoeyLLM-Team/issues?q=is%3Aissue%20milestone%3A%22Sprint%204%22%20is%3Aclosed) |
| Minutes location | `management/weekly-reports-END/sprint-04/week-02/internal-minutes-2026-08-05.md` |

## 2. Agenda

1. Review actions and feedback from the 3 August Tutor meeting.
2. Confirm parallel frontend work and comparison evidence.
3. Confirm Client liaison and target-user clarification.
4. Define Qdrant research outputs and implementation boundaries.
5. Agree on Week 3 convergence, testing, and Sprint Review preparation.

## 3. Review of previous actions

| Previous ID | Action / deliverable | Accountable owner | Original due | Current status | Evidence / progress | Reason / next step |
| --- | --- | --- | --- | --- | --- | --- |
| S4-A05 | Obtain explicit target-user confirmation | Wen Sun | 10 August 2026 | In progress | Client liaison workstream established | Keep the audience labelled as a working assumption until confirmed |
| S4-A06 | Produce comparable Next.js prototypes | Yingzhe Xu | 7 August 2026 | In progress | Member branches, previews, [PR #1](https://github.com/joeyllm/ChatJoey/pull/1), and [PR #2](https://github.com/joeyllm/ChatJoey/pull/2) | Complete comparison evidence and preserve stable references |
| S4-A07 | Produce Qdrant research evidence | Nuo Chen | 10 August 2026 | In progress | Vector-database study underway | Consolidate concepts, sources, and implementation limits |
| S4-A08 | Prepare Sprint Review evidence | Xiang Chang | 10 August 2026 | In progress | Sprint Goal and reports available | Add selected UI, deployment/test status, research, risks, and feedback response |

## 4. Progress and evidence presented

| Work item | Progress | Verified status | Evidence shown | Impact | Remaining gap |
| --- | --- | --- | --- | --- | --- |
| Individual frontend exploration | All members were contributing to separate Next.js interface versions to explore different layouts and interactions | Implemented as parallel prototypes | Member branch/preview evidence and prototype screenshots | Provides alternatives before convergence | Not all historical branches would remain permanent; stable PR/commit/PDF references were needed |
| UI/UX documentation | Product definition, user research, personas, scenarios, stories, and Figma work were being compiled | Researched / documented | [Issue #3](https://github.com/joeyllm/ChatJoey/issues/3) and design materials | Links interface decisions to intended users and tasks | Issue #3 lacked detailed closure evidence and required stronger follow-up documentation |
| Qdrant learning | The team was developing a shared understanding of embeddings, chunking, metadata, similarity search, HNSW, and RAG | Researched | Research notes and planned technical record | Prepares future retrieval work around the client-provided model framework | No production Qdrant/RAG implementation was claimed |

## 5. Discussion and team response

| Feedback ID | Source | Feedback / concern | Team response and rationale | Outcome | Linked decision / action |
| --- | --- | --- | --- | --- | --- |
| S4-IF01 | Tutor / Matthew | Develop the Next.js chat interface while maintaining visible evidence | Accepted. Each member would work in a separate branch before a shared selection | Agreed | S4-D07, S4-A06, S4-A09 |
| S4-IF02 | Tutor | Do not design around an unconfirmed target audience | Accepted. Prior Semester 1 context would support an interim broad audience interested in Australian information, explicitly marked as a working assumption | Pending Client confirmation | S4-D08, S4-A05 |
| S4-IF03 | Team | Maintaining multiple formal products would create integration and maintenance cost | Accepted. Parallel prototypes were a comparison stage, not the final repository state | Agreed | S4-D09, S4-A09, S4-A10 |
| S4-IF04 | Tutor / team | Qdrant learning needs reviewable evidence and should not be confused with implementation | Accepted. The team would produce a technical record and literature-based next-step plan | Agreed | S4-D10, S4-A12 |

## 6. Decisions and rationale

| Decision ID | Decision | Rationale / evidence considered | Confirmed by | Affected work | Effective date |
| --- | --- | --- | --- | --- | --- |
| S4-D07 | Continue parallel prototype work in separate branches through the comparison stage | Preserves independent design exploration and avoids overwriting shared main | All five members | S4-A06 and frontend evidence | 5 August 2026 |
| S4-D08 | Use “people interested in Australian information” only as an interim audience derived from Semester 1 context, not as Client-confirmed scope | The Client had not explicitly answered the current target-user question | All five members | User research, personas, and S4-A05 | 5 August 2026 |
| S4-D09 | Compare prototypes and select one shared frontend direction before final integration | A single maintained implementation is more reviewable and deployable than competing formal versions | All five members | S4-A09, S4-A10 | 5 August 2026 |
| S4-D10 | Treat vector-database work as research and feasibility preparation in Sprint 4 | Server/data access and production decisions were unavailable, and Matthew requested foundational learning | All five members | S4-A12 and Sprint scope | 5 August 2026 |

## 7. Risks, blockers, delays and scope changes

| ID | Risk / blocker | Impact | Mitigation | Accountable owner | Decision required | Review date | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4-R07 | Historical member branches may later be deleted after consolidation | Could weaken evidence for the parallel-prototype claim | Preserve PRs, commit references, screenshots, and the comparison record | Yingzhe Xu | None | 10 August 2026 | Monitoring |
| S4-R08 | Target audience remains an inference rather than explicit Client confirmation | Could affect detailed UI requirements | Keep the audience labelled accurately and close Sprint 4 with this limitation recorded | Wen Sun | None within Sprint 4 | 10 August 2026 | Accepted limitation |
| S4-R09 | No production retrieval environment or confirmed embedding/Qdrant configuration | Prevents an evidence-based implementation claim | Complete research evidence and state the implementation boundary explicitly | Nuo Chen | None within Sprint 4 | 10 August 2026 | Accepted limitation |

## 8. New action items

| Action ID | Action / deliverable | Accountable owner | Contributors | Linked item | Due date | Acceptance criteria and evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4-A09 | Compare the member prototypes using layout, interaction, responsiveness, accessibility, differentiation, and integration feasibility | Yingzhe Xu | Southern-cross AI | S4-D07, S4-D09 | 10 August 2026 | Recorded comparison and final selection decision | Open |
| S4-A10 | Consolidate the selected interface into one shared ChatJoey implementation | Yingzhe Xu | Southern-cross AI | S4-D09 | 10 August 2026 | Merged implementation with architecture and decision evidence | Open |
| S4-A11 | Validate the deployed shared flow with all five members and preserve the results | Nuo Chen | Southern-cross AI | S4-D09 | 10 August 2026 | Deployment URL, repeatable test cases, member results, and issues for any failure | Open |
| S4-A12 | Consolidate Qdrant/vector research and identify the unresolved production decisions | Nuo Chen | Southern-cross AI | S4-D10 | 10 August 2026 | Technical record and literature review with no unsupported implementation claim | Open |
| S4-A05 | Seek target-user clarification; if the Client does not explicitly answer, record the limitation without presenting the inferred audience as confirmed | Wen Sun | Xiang Chang, Xingyu Li | S4-D08 | 10 August 2026 | Client response or an explicit unconfirmed-audience limitation in the Sprint close record | In progress |

## 9. Continuous improvement

| Improvement ID | Observed problem | Root cause | Process change | Accountable owner | Success measure | Review date | Linked item / status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4-I03 | Parallel work could be described as complete without stable evidence for each version | Branches and previews can be temporary | Preserve durable PR, commit, screenshot, and decision links before consolidation | Yingzhe Xu | Every material selection claim has a durable reference | 10 August 2026 | S4-A09 / Open |
| S4-I04 | Shared ownership made it difficult to identify who must close an action | Collaborative delivery had been confused with accountability | Keep all members as contributors but assign one evidence owner per action | Xiang Chang | No open action has `Team` as its only owner | 10 August 2026 | Applied to S4-A05-S4-A12 |

## 10. Next meeting readiness

| Field | Details |
| --- | --- |
| Confirmed date / time | 10 August 2026, 14:00 AEST |
| Meeting type | Tutor Meeting / Sprint progress review |
| Purpose | Demonstrate convergence, deployment/test status, research, limitations, and process evidence |
| Required completed actions | S4-A06-S4-A12, except S4-A05 may remain pending with an explicit reason |
| Evidence to present | Comparison record, PR/commit, deployment, system validation, Qdrant research, risks, and status distinctions |
| Decisions requested | Tutor feedback on documentation, tickets, user testing, and next-Sprint preparation |
| Presenters | Workstream evidence owners |
| Pre-reading | Sprint summary and repository links |

### Proposed next-meeting agenda

1. Review action closure and remaining Client clarification.
2. Present the selected and consolidated ChatJoey frontend.
3. Present deployment and team-validation evidence.
4. Present Qdrant research and unresolved production decisions.
5. Record Tutor feedback and measurable process improvements.

## 11. Meeting close and approval

| Check | Result |
| --- | --- |
| Open actions at close | S4-A05, S4-A09-S4-A12 |
| Decisions recorded | S4-D07-S4-D10 |
| Feedback awaiting response | Target-user clarification only |
| Risks requiring monitoring | S4-R07-S4-R09 |
| Minutes prepared by | Xingyu Li |
| Reviewer | Nuo Chen |
| Approval status | Approved by Nuo Chen on 5 August 2026 |
| Distributed to | Southern-cross AI |
| GitHub location | This document |

## 12. Sprint checklist traceability

| Checklist dimension | Evidence captured | IDs / links |
| --- | --- | --- |
| Stakeholder Engagement | Tutor/Client instructions, team response, target-user clarification, and follow-up | S4-IF01-S4-IF04, S4-A05 |
| Planning and Organisation | Workstreams, prototype convergence plan, owners, dates, risks, and review preparation | S4-D07-S4-D10, S4-A09-S4-A12 |
| Execution and Quality | Durable branch/PR evidence, selection criteria, deployment validation plan, and implementation boundaries | S4-R07, S4-A09-S4-A12 |
| Reflection and Improvement | Evidence preservation and accountable-owner process changes | S4-I03, S4-I04 |
