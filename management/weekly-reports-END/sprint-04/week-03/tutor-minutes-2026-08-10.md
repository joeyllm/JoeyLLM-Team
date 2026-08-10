# Tutor Meeting and Sprint Progress Review Minutes

## 1. Meeting information

| Field | Details |
| --- | --- |
| Project | Southern-cross AI / JoeyLLM |
| Meeting type | Tutor Meeting / Sprint Progress Review |
| Sprint / Week | Sprint 4 / Week 3 |
| Date | 10 August 2026 |
| Time | 14:00-15:00 AEST |
| Location / Channel | TechLauncher Tutor meeting |
| Chair | Annie Sun |
| Minute taker | Xingyu Li |
| Present | Annie Sun, Nuo Chen, Wen Sun, Xiang Chang, Xingyu Li, Yingzhe Xu |
| Apologies / Absent | None |
| Meeting objective | Review Sprint 4 delivery, evidence, documentation, tickets, prototype consolidation, system validation, research, and same-day process improvements |
| Related Sprint Goal / Milestone | [Sprint 4 Goal](../../../SPRINT4_GOALS.md) / [Sprint 4 milestone](https://github.com/joeyllm/JoeyLLM-Team/milestone/5) |
| Minutes location | `management/weekly-reports-END/sprint-04/week-03/tutor-minutes-2026-08-10.md` |

## 2. Agenda

1. Review Week 2 actions, Sprint Goal, and open Client clarification.
2. Demonstrate the selected ChatJoey frontend, API integration, and deployment.
3. Present tickets, UX documentation, system validation, and Qdrant research.
4. Record Tutor feedback on professionalism, consistency, target users, and testing.
5. Confirm decisions, completed same-day improvements, accepted limitations, and Sprint close.

## 3. Review of previous actions

| Previous ID | Action / deliverable | Accountable owner | Original due | Current status | Completion evidence | Reason / revised next step |
| --- | --- | --- | --- | --- | --- | --- |
| S4-A05 | Obtain explicit Client confirmation of target users | Wen Sun | 10 August 2026 | Closed as an unresolved Sprint limitation | Client has not explicitly confirmed the audience | Use “people interested in Australian information” only as a documented working assumption based on Semester 1 context; no Client-confirmed claim is made |
| S4-A06 | Produce comparable individual Next.js prototypes | Yingzhe Xu | 7 August 2026 | Done | [PR #1](https://github.com/joeyllm/ChatJoey/pull/1), [PR #2](https://github.com/joeyllm/ChatJoey/pull/2), historical prototype evidence, and [frontend selection record](Meeting%20record%20about%20front-end%20website.pdf) | Historical branches were later removed after convergence; durable evidence is retained through PRs, commits, and the selection record |
| S4-A07 / S4-A12 | Produce Qdrant research evidence and identify unresolved production decisions | Nuo Chen | 10 August 2026 | Done as research | [Qdrant basics](https://github.com/joeyllm/ChatJoey/blob/main/docs/qdrant-basics-en.md), [technical discussion](Vector_Database_Meeting_Minutes_EN.pdf), and [literature review](research/vector-retrieval-literature-review.md) | Qdrant/RAG implementation and benchmark are not claimed in Sprint 4 |
| S4-A08 | Prepare Sprint Review evidence aligned with the goal | Xiang Chang | 10 August 2026 | Done | [Sprint summary](ChatJoey_Sprint_Summary_English.pdf), this week index, implementation and research links | Team confirmation remains required for any statement marked pending in the summary |
| S4-A09 | Compare prototypes and select a shared direction | Yingzhe Xu | 10 August 2026 | Done | [Frontend selection record](Meeting%20record%20about%20front-end%20website.pdf) and [decision log](https://github.com/joeyllm/ChatJoey/blob/main/docs/DECISIONS.md) | None |
| S4-A10 | Consolidate the selected interface | Yingzhe Xu | 10 August 2026 | Done | [PR #4](https://github.com/joeyllm/ChatJoey/pull/4) merged to `main` | Shared implementation is represented in `main` |
| S4-A11 | Validate the deployed shared flow with all members | Nuo Chen | 10 August 2026 | Done | [Live application](https://chat-joey.vercel.app/) and [system validation](system-validation.md) | Automated, load, and security testing remain outside this manual validation claim |

## 4. Progress and evidence presented

| Work item | Progress since last meeting | Verified status | Evidence shown | User / stakeholder impact | Remaining gap |
| --- | --- | --- | --- | --- | --- |
| Shared ChatJoey interface | Separate prototypes were compared and Yingzhe Xu's version was selected as the shared baseline, with suitable team ideas consolidated | Implemented | [PR #4](https://github.com/joeyllm/ChatJoey/pull/4), [decision log](https://github.com/joeyllm/ChatJoey/blob/main/docs/DECISIONS.md), frontend selection PDF | Gives the project one maintainable, responsive, multilingual interface | Automated browser coverage and persistent conversation storage are not implemented |
| Real JoeyLLM API connection | The browser uses a server-side Next.js `/api/chat` boundary and credentials remain server-side | Implemented and manually tested | [Architecture](https://github.com/joeyllm/ChatJoey/blob/main/docs/ARCHITECTURE.md), PR #4, [system validation](system-validation.md) | Enables end-to-end questions and genuine model responses | Production observability and broader failure testing are outside the verified Sprint 4 scope |
| Deployment | The consolidated application is available online | Deployed | [https://chat-joey.vercel.app/](https://chat-joey.vercel.app/) and [deployment guide](https://github.com/joeyllm/ChatJoey/blob/main/docs/DEPLOYMENT.md) | Tutor, Client, and prospective users can review the live interface | No additional production-maintenance outcome is claimed in Sprint 4 |
| Qdrant/vector preparation | The team documented embeddings, collections, payloads, similarity search, HNSW, RAG boundaries, and evaluation variables | Researched | Qdrant documentation, technical discussion PDF, and literature review | Provides an evidence-based technical foundation and identifies unresolved production choices | No collection, embeddings, retrieval pipeline, RAG prompt, or benchmark is implemented |
| Target-user definition | Prior Semester 1 context indicates a broad audience of people interested in Australian information | Working assumption | Semester 1 project context | Provides an interim basis for general accessibility and information-oriented design | The Client has not explicitly confirmed the current target audience |

## 5. Discussion, Tutor feedback and team response

| Feedback ID | Source | Feedback, question or concern | Team response and rationale | Outcome | Linked decision / action / PBI |
| --- | --- | --- | --- | --- | --- |
| S4-F07 | Tutor | Meeting minutes must be formal and structured, including discussion, decisions, actions, responsibility, and follow-up | Accepted. The team adopted one professional template covering previous actions, evidence, feedback responses, rationale, risks, actions, improvement, follow-up readiness, approval, and checklist traceability | Implemented as a process change | S4-D11, S4-A14, S4-I05 |
| S4-F08 | Tutor | Project communication evidence should not focus only on email; meeting outcomes and stakeholder responses must be visible | Accepted. The Sprint index and minutes link communication to decisions, actions, PBIs, and evidence | Implemented in the documentation structure | S4-A14, S4-I05 |
| S4-F09 | Tutor | Ticket names and descriptions should be unique, consistent, and sufficiently detailed | Accepted. The team adopted a rule requiring a unique outcome title, owner, acceptance criteria, evidence, and a closure explanation; Issue #3 is retained as an example of insufficient closure detail | Implemented as a process rule | S4-D12, S4-A19, S4-I06 |
| S4-F10 | Tutor | User stories, personas, scenarios, and design should be mutually consistent and based on target users | Accepted. The broad audience remains a working assumption and no Client-confirmed audience is claimed | Accepted limitation at Sprint close | S4-A05, S4-R10 |
| S4-F11 | Tutor | User testing should use key tasks and usability criteria, and identified problems must become tickets | Accepted. The team consolidated the agreed manual checks and all five member confirmations into one validation record; no defect was reported in the tested flow | Implemented for the agreed Sprint 4 validation scope | S4-A17, S4-I07 |
| S4-F12 | Tutor | The team must show reflection and measurable improvement, not only product progress | Accepted. The team documented root causes and implemented the professional template, accountable-owner rule, ticket rule, and consolidated validation evidence on the same day | Implemented in this record and PR #50 | S4-D13, S4-A14-S4-A19, S4-I05-S4-I07 |

## 6. Decisions and rationale

| Decision ID | Decision | Rationale / evidence considered | Confirmed by | Affected work | Effective date |
| --- | --- | --- | --- | --- | --- |
| S4-D11 | Use the shared professional meeting-minutes template as the sole formal meeting standard | Directly responds to Tutor feedback and creates an auditable feedback/action/decision/improvement chain | Southern-cross AI | All formal minutes and weekly evidence | 10 August 2026 |
| S4-D12 | Require unique ticket titles, acceptance criteria, an evidence link, and a closure explanation before a work item is treated as Done | Issue #3 was closed without sufficient visible outcome evidence | Southern-cross AI | Project issue/PBI governance | 10 August 2026 |
| S4-D13 | Close the Sprint 4 evidence set on 10 August after recording Tutor feedback, root causes, same-day process improvements, and accepted limitations; do not publish minutes for an unheld internal meeting | Preserves factual meeting evidence while still recording measurable reflection and improvement | Southern-cross AI | Sprint 4 documentation close | 10 August 2026 |
| S4-D14 | Keep production Qdrant/RAG, model training, and data/backend experiments outside the Sprint 4 completion claim | The client provides the model framework and the required production choices/access were not available | Southern-cross AI | Sprint 4 scope statement | 10 August 2026 |

## 7. Risks, blockers, delays and scope changes

| ID | Risk / blocker | Impact on Sprint Goal | Mitigation | Accountable owner | Escalation / decision required | Review date | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4-R10 | Client has not explicitly confirmed the target audience | Detailed persona/scenario and usability priorities may rest on an assumption | Retain the broad Australia-information audience as a labelled working assumption and make no Client-confirmed claim | Wen Sun | None within the closed Sprint 4 evidence set | 10 August 2026 | Accepted limitation at Sprint close |
| S4-R11 | Manual tests passed but automated browser, load, security, and forced-failure coverage are not available | The evidence supports the agreed manual flow but not broader quality claims | Preserve the exact manual scope and explicitly exclude unperformed testing | Nuo Chen | None; broader testing was not a Sprint 4 completion criterion | 10 August 2026 | Accepted outside Sprint 4 scope |
| S4-R12 | Qdrant configuration, embedding model, dataset permissions, metadata schema, and hosting are not confirmed | A valid production retrieval implementation cannot be claimed | Record the research conclusions and required technical decisions without claiming implementation | Nuo Chen | None within Sprint 4 | 10 August 2026 | Accepted outside Sprint 4 scope |

## 8. New action items

| Action ID | Action / deliverable | Accountable owner | Contributors | Linked feedback / decision | Due date | Acceptance criteria and evidence location | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4-A14 | Adopt the professional meeting-minutes template and remove weaker formal templates | Xingyu Li | Southern-cross AI | S4-F07, S4-F08, S4-D11 | 10 August 2026 | Template and README committed in `JoeyLLM-Team` | Done |
| S4-A15 | Remove the AI-prompt rule that assumes all members attended and document the approval/file-naming rules | Xingyu Li | Nuo Chen | S4-F07, S4-D11 | 10 August 2026 | Updated `templates/README.md` in PR #50 | Done |
| S4-A17 | Consolidate the agreed manual validation and all five member confirmations into one evidence record | Nuo Chen | Southern-cross AI | S4-F11, S4-R11 | 10 August 2026 | [System validation](system-validation.md) with scope and limitations | Done |
| S4-A19 | Define consistent ticket naming, acceptance, evidence, and closure requirements | Xiang Chang | Southern-cross AI | S4-F09, S4-D12 | 10 August 2026 | Decision S4-D12 and the professional template quality gate | Done |

## 9. Continuous improvement

| Improvement ID | Observed problem and evidence | Root cause | Process change | Accountable owner | Success measure | Review date | Linked PBI / status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4-I05 | Minutes lacked previous-action closure, feedback response, rationale, measurable improvement, and follow-up evidence | No single formal quality standard or reviewer existed | Use the professional template, publish through PR, and require Nuo Chen review | Xingyu Li | Every formal record in PR #50 contains all 12 required sections with no prohibited placeholder or group-only owner | 10 August 2026 | S4-A14-S4-A15 / Done |
| S4-I06 | Issue #3 was closed without visible outcome, links, or acceptance evidence | Ticket closure did not have a Definition of Done | Adopt unique title, owner, acceptance criteria, evidence, and closure-explanation requirements | Xiang Chang | The rule is recorded in S4-D12 and the professional template quality gate | 10 August 2026 | S4-A19 / Done |
| S4-I07 | Manual testing was discussed without one consistent evidence record | Validation was distributed across conversation, PR notes, and individual checks | Maintain one system-validation record with exact scope, results, member confirmation, and limitations | Nuo Chen | Every agreed Sprint 4 manual test has a recorded result and all five members are represented | 10 August 2026 | S4-A17 / Done |

## 10. Sprint close and boundary statement

| Field | Details |
| --- | --- |
| Evidence close date | 10 August 2026 |
| Further Sprint 4 meeting recorded | None |
| Goal evidence completed | Frontend comparison and consolidation, real API integration, live deployment, five-member manual validation, and foundational Qdrant/vector research |
| Same-day process improvements completed | Professional minutes template, safe attendance rule, accountable-owner model, ticket closure rule, consolidated validation record, and three-week evidence index |
| Accepted limitations | Target users are not explicitly Client-confirmed; automated/load/security testing and production Qdrant/RAG were not Sprint 4 completion criteria |
| Boundary | No later meeting, PBI, implementation, or Client decision is claimed as part of this Sprint 4 completion record |

### Sprint close checklist

1. Verified completion states are linked to implementation, deployment, validation, or research evidence.
2. Unperformed work is explicitly excluded rather than presented as planned Sprint 4 work.
3. Tutor feedback has a recorded response, decision, completed action, or accepted limitation.
4. All formal records remain subject to Nuo Chen's final review before merge.

## 11. Meeting close and approval

| Check | Result |
| --- | --- |
| Open actions at close | None within the Sprint 4 evidence set; S4-A05 closed as an unresolved limitation |
| Decisions recorded | S4-D11-S4-D14 |
| Feedback awaiting external response | None claimed within Sprint 4; target-user confirmation remains unconfirmed |
| Risks / limitations at close | S4-R10-S4-R12 recorded as accepted limitations or outside-scope boundaries |
| Minutes prepared by | Xingyu Li |
| Reviewer | Nuo Chen |
| Approval status | Draft pending Nuo Chen review |
| Distributed to | Tutor and Southern-cross AI |
| GitHub location | This document |

## 12. Sprint checklist traceability

| Checklist dimension | Evidence captured | IDs / links |
| --- | --- | --- |
| Stakeholder Engagement | Tutor feedback, explicit responses, Client-confirmation limitation, and same-day action closure | S4-F07-S4-F12, S4-A05, S4-A14-S4-A19 |
| Planning and Organisation | Sprint Goal, closed actions, accountable owners, exact dates, risks, and scope boundaries | S4-D11-S4-D14, S4-R10-S4-R12 |
| Execution and Quality | PR #4, deployment, five-member system validation, research evidence, and accurate implementation boundaries | Progress table, S4-A17 |
| Reflection and Improvement | Tutor feedback, documented root causes, same-day process changes, measurable results, and final review control | S4-D13, S4-I05-S4-I07 |
