# Tutor Meeting Minutes

## 1. Meeting information

| Field | Details |
| --- | --- |
| Project | Southern-cross AI / JoeyLLM |
| Meeting type | Tutor Meeting |
| Sprint / Week | Sprint 4 / Week 2 |
| Date | 3 August 2026 |
| Time | 14:07-14:40 AEST |
| Location / Channel | TechLauncher Hive |
| Chair | Annie Sun |
| Minute taker | Xingyu Li |
| Present | Annie Sun, Nuo Chen, Wen Sun, Xiang Chang, Xingyu Li, Yingzhe Xu |
| Apologies / Absent | None |
| Meeting objective | Confirm Sprint 4 scope, target-user requirements, productive work during the server outage, and evidence expected for the Sprint Review |
| Related Sprint Goal / Work items | [Sprint 4 Goal](../../../SPRINT4_GOALS.md) / [Nine closed Sprint 4 issues](https://github.com/joeyllm/JoeyLLM-Team/issues?q=is%3Aissue%20milestone%3A%22Sprint%204%22%20is%3Aclosed) |
| Minutes location | `management/weekly-reports-END/sprint-04/week-02/tutor-minutes-2026-08-03.md` |

## 2. Agenda

1. Review Week 1 preparation actions.
2. Confirm the Sprint Goal and Matthew's latest instructions.
3. Review the UI prototype scope and target-user question.
4. Confirm productive work while JupyterHub and the server are unavailable.
5. Agree on research evidence, communication, and Sprint Review preparation.

## 3. Review of previous actions

| Previous ID | Action / deliverable | Accountable owner | Original due | Current status | Completion evidence | Reason / next step |
| --- | --- | --- | --- | --- | --- | --- |
| S4-A01 | Review and organise the team repository and minutes evidence | Xingyu Li | 3 August 2026 | Done | [Sprint 4 weekly-report structure](../) | Continue improving minutes quality throughout the Sprint |
| S4-A02 | Define and communicate the Sprint 4 Goal and three-week plan | Xiang Chang | 3 August 2026 | Done | [Sprint 4 Goal](../../../SPRINT4_GOALS.md) | Keep the agreed goal stable |
| S4-A03 | Obtain and circulate the Client's Sprint 4 instruction | Wen Sun | 3 August 2026 | Done | Matthew's 3 August email instructed Next.js interface work and Qdrant learning | Convert the instruction into workstream actions |
| S4-A04 | Prepare a reviewable Sprint deliverable or work plan | Yingzhe Xu | 10 August 2026 | In progress | UI prototype scope and team repository | Continue to Sprint Review evidence |

## 4. Progress and evidence presented

| PBI / work item | Progress since last meeting | Verified status | Evidence shown | Stakeholder impact | Remaining gap |
| --- | --- | --- | --- | --- | --- |
| Sprint 4 Goal | Goal was defined and communicated to the Tutor | Confirmed | [Sprint 4 Goal](../../../SPRINT4_GOALS.md) | Gives the Sprint Review a stable assessment baseline | Evidence must remain aligned with the goal |
| Next.js interface | Current work was scoped as a ChatGPT/Gemini-style interface prototype | Planned / beginning implementation | [Week 2 report](report.md) and [Tutor preparation](tutor-2026-08-03.md) | Provides a visible user-facing deliverable while backend access is limited | Target users and final shared design were not yet confirmed |
| Qdrant learning | Matthew asked the team to explore Qdrant and understand vector-database concepts | Researched work planned | Client instruction and planned notes | Prepares the next retrieval-focused Sprint | No Qdrant collection, embedding pipeline, or retrieval benchmark existed |
| Runtime access | JupyterHub and the server were unavailable during maintenance | Blocked dependency | Client instruction and team status | Prevented authorised model/data/backend experiments | Continue independent work and recheck access later |

## 5. Discussion, Tutor feedback and team response

| Feedback ID | Source | Feedback, question or concern | Team response and rationale | Outcome | Linked decision / action |
| --- | --- | --- | --- | --- | --- |
| S4-F01 | Tutor | Confirm target users with the Client before further design decisions; possible audiences include researchers, government staff, the general public, or another group | Accepted. The team would seek explicit Client confirmation and avoid presenting an inferred audience as Client-confirmed | Pending Client clarification | S4-D04, S4-A05 |
| S4-F02 | Tutor | Use the workflow requirements confirmation -> user identification -> research -> prototype -> Client confirmation -> development | Accepted. User research and prototype evidence would be linked rather than treated as separate unsupported activities | Incorporated into work plan | S4-D04, S4-A05, S4-A06 |
| S4-F03 | Tutor | Keep the agreed Sprint Goal stable because the Sprint Review will assess against it | Accepted. The team would preserve the goal and distinguish completed, researched, and out-of-scope work | Resolved as a working rule | S4-D05, S4-A08 |
| S4-F04 | Tutor | UI design, research, planning, and documentation remain valid work while the server is unavailable | Accepted. The team would prioritise work that did not require unavailable infrastructure | Resolved | S4-D06, S4-A06, S4-A07 |
| S4-F05 | Tutor | Qdrant and vector-database learning counts as Sprint work only when reviewable evidence is maintained | Accepted. The team would produce Markdown research evidence and clearly avoid implementation claims | Action required | S4-D06, S4-A07 |
| S4-F06 | Tutor | Avoid assumptions and follow up professionally when requirements are unclear | Accepted. Client liaison members would record questions and responses | Ongoing practice | S4-A05 |

## 6. Decisions and rationale

| Decision ID | Decision | Rationale / evidence considered | Confirmed by | Affected work | Effective date |
| --- | --- | --- | --- | --- | --- |
| S4-D04 | Treat target-user identification as an open Client clarification while using prior project context only as a documented working assumption | The Client had not explicitly confirmed the current audience | Tutor and Southern-cross AI | UI research, personas, scenarios, and accessibility | 3 August 2026 |
| S4-D05 | Keep the Sprint 4 Goal stable unless a necessary change is formally agreed | The Sprint Review is assessed against the agreed goal | Tutor and Southern-cross AI | Sprint plan and review evidence | 3 August 2026 |
| S4-D06 | Continue independent frontend, research, planning, and documentation work without claiming unavailable backend experiments | These outputs are achievable without JupyterHub or server access and match Matthew's instruction | Tutor and Southern-cross AI | UI and Qdrant workstreams | 3 August 2026 |

## 7. Risks, blockers, delays and scope changes

| ID | Risk / blocker | Impact on Sprint Goal | Mitigation | Accountable owner | Escalation / decision required | Review date | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4-R04 | Client has not explicitly confirmed target users | UI requirements could be based on an assumption | Ask the Client and label the interim audience as a working assumption | Wen Sun | Client clarification | 10 August 2026 | Open |
| S4-R05 | JupyterHub and server unavailable | Prevents model, training, dataset, and backend experiments | Deliver frontend and research work; do not claim unavailable work | Xiang Chang | Client access update | 10 August 2026 | Monitoring |
| S4-R06 | Parallel prototypes may diverge without comparison criteria | Could create competing versions and weak integration evidence | Agree on comparison criteria and one convergence decision | Yingzhe Xu | Team selection decision | 10 August 2026 | Open |

## 8. New action items

| Action ID | Action / deliverable | Accountable owner | Contributors | Linked feedback / decision | Due date | Acceptance criteria and evidence location | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4-A05 | Ask the Client to confirm the intended target users and record the answer | Wen Sun | Xiang Chang, Xingyu Li | S4-F01, S4-F06, S4-D04 | 10 August 2026 | Written Client response or documented open clarification | Open |
| S4-A06 | Produce comparable Next.js interface prototypes in separate member branches | Yingzhe Xu | Southern-cross AI | S4-F02, S4-F04, S4-D06 | 7 August 2026 | Prototype evidence, branch/PR/preview references, and comparison inputs | In progress |
| S4-A07 | Produce reviewable Qdrant and vector-database research evidence | Nuo Chen | Southern-cross AI | S4-F05, S4-D06 | 10 August 2026 | Markdown/PDF research evidence with implementation limits | In progress |
| S4-A08 | Prepare Sprint Review evidence aligned with the stable Sprint Goal | Xiang Chang | Southern-cross AI | S4-F03, S4-D05 | 10 August 2026 | Demonstration, evidence links, risks, and status distinctions | In progress |

## 9. Continuous improvement

| Improvement ID | Observed problem | Root cause | Process change | Accountable owner | Success measure | Review date | Linked item / status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4-I02 | Research and UI activity could be difficult to assess if only described verbally | Evidence requirements were not embedded in each action | Attach an acceptance condition and evidence location to each Sprint action | Xingyu Li | Every action due at the review has direct evidence or a documented reason | 10 August 2026 | S4-A06-S4-A08 / In progress |

## 10. Next meeting readiness

| Field | Details |
| --- | --- |
| Confirmed date / time | 10 August 2026, 14:00 AEST |
| Meeting type | Tutor Meeting / Sprint progress review |
| Purpose | Present consolidated Sprint outcomes, evidence, risks, and open Client clarification |
| Required completed actions | S4-A05-S4-A08 |
| Evidence to present | Prototype comparison, selected shared direction, deployed/validated implementation if complete, Qdrant research, tickets, and documentation |
| Decisions / clarifications requested | Whether the demonstrated evidence and improvement actions satisfy the Sprint expectations |
| Presenters | Southern-cross AI workstream representatives |
| Pre-reading / material to send | Sprint summary and repository links |

### Proposed next-meeting agenda

1. Close or explain S4-A05-S4-A08.
2. Demonstrate the shared frontend and verified system state.
3. Present Qdrant research and state what is not implemented.
4. Review risks, stakeholder clarification, tickets, and documentation.
5. Record Tutor feedback, improvement actions, and Sprint close-out preparation.

## 11. Meeting close and approval

| Check | Result |
| --- | --- |
| Open actions at close | 4: S4-A05-S4-A08 |
| Decisions recorded | 3: S4-D04-S4-D06 |
| Feedback items awaiting external response | S4-F01 / target-user confirmation |
| Risks requiring monitoring | S4-R04-S4-R06 |
| Minutes prepared by | Xingyu Li |
| Reviewer | Nuo Chen |
| Approval status | Approved by Nuo Chen on 3 August 2026 |
| Distributed to | Tutor and Southern-cross AI |
| GitHub location | This document |

## 12. Sprint checklist traceability

| Checklist dimension | Evidence captured | Direct IDs / links |
| --- | --- | --- |
| Stakeholder Engagement | Tutor feedback, explicit responses, Client clarification, actions, and next meeting | S4-F01-S4-F06, S4-A05 |
| Planning and Organisation | Stable goal, workstreams, ownership, dates, risks, and review plan | S4-D04-S4-D06, S4-A05-S4-A08, S4-R04-S4-R06 |
| Execution and Quality | Accurate status separation and evidence-based acceptance conditions | Progress table, S4-I02 |
| Reflection and Improvement | Measurable evidence discipline carried into the Sprint Review | S4-I02 |
