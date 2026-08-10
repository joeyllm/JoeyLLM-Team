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
| Meeting objective | Review Sprint 4 delivery, evidence, documentation, tickets, prototype consolidation, system validation, research, and preparation for user testing and the next Sprint |
| Related Sprint Goal / Milestone | [Sprint 4 Goal](../../../SPRINT4_GOALS.md) / [Sprint 4 milestone](https://github.com/joeyllm/JoeyLLM-Team/milestone/5) |
| Minutes location | `management/weekly-reports-END/sprint-04/week-03/tutor-minutes-2026-08-10.md` |

## 2. Agenda

1. Review Week 2 actions, Sprint Goal, and open Client clarification.
2. Demonstrate the selected ChatJoey frontend, API integration, and deployment.
3. Present tickets, UX documentation, system validation, and Qdrant research.
4. Record Tutor feedback on professionalism, consistency, target users, and testing.
5. Confirm decisions, improvement actions, Sprint retrospective, and next meeting readiness.

## 3. Review of previous actions

| Previous ID | Action / deliverable | Accountable owner | Original due | Current status | Completion evidence | Reason / revised next step |
| --- | --- | --- | --- | --- | --- | --- |
| S4-A05 | Obtain explicit Client confirmation of target users | Wen Sun | 10 August 2026 | In progress | Client has not explicitly confirmed the audience | Carry to 17 August; use ?people interested in Australian information? only as a documented working assumption based on Semester 1 context |
| S4-A06 | Produce comparable individual Next.js prototypes | Yingzhe Xu | 7 August 2026 | Done | [PR #1](https://github.com/joeyllm/ChatJoey/pull/1), [PR #2](https://github.com/joeyllm/ChatJoey/pull/2), historical prototype evidence, and [frontend selection record](Meeting%20record%20about%20front-end%20website.pdf) | Historical branches were later removed after convergence; durable evidence is retained through PRs, commits, and the selection record |
| S4-A07 / S4-A12 | Produce Qdrant research evidence and future-decision requirements | Nuo Chen | 10 August 2026 | Done as research | [Qdrant basics](https://github.com/joeyllm/ChatJoey/blob/main/docs/qdrant-basics-en.md), [technical discussion](Vector_Database_Meeting_Minutes_EN.pdf), and [literature review](research/vector-retrieval-literature-review.md) | Qdrant/RAG implementation and benchmark remain future work |
| S4-A08 | Prepare Sprint Review evidence aligned with the goal | Xiang Chang | 10 August 2026 | Done | [Sprint summary](ChatJoey_Sprint_Summary_English.pdf), this week index, implementation and research links | Team confirmation remains required for any statement marked pending in the summary |
| S4-A09 | Compare prototypes and select a shared direction | Yingzhe Xu | 10 August 2026 | Done | [Frontend selection record](Meeting%20record%20about%20front-end%20website.pdf) and [decision log](https://github.com/joeyllm/ChatJoey/blob/main/docs/DECISIONS.md) | None |
| S4-A10 | Consolidate the selected interface | Yingzhe Xu | 10 August 2026 | Done | [PR #4](https://github.com/joeyllm/ChatJoey/pull/4) merged to `main` | Shared implementation is represented in `main` |
| S4-A11 | Validate the deployed shared flow with all members | Nuo Chen | 10 August 2026 | Done | [Live application](https://chat-joey.vercel.app/) and [system validation](system-validation.md) | Automated, load, and security testing remain outside this manual validation claim |

## 4. Progress and evidence presented

| Work item | Progress since last meeting | Verified status | Evidence shown | User / stakeholder impact | Remaining gap |
| --- | --- | --- | --- | --- | --- |
| Shared ChatJoey interface | Separate prototypes were compared and Yingzhe Xu's version was selected as the shared baseline, with suitable team ideas consolidated | Implemented | [PR #4](https://github.com/joeyllm/ChatJoey/pull/4), [decision log](https://github.com/joeyllm/ChatJoey/blob/main/docs/DECISIONS.md), frontend selection PDF | Gives the project one maintainable, responsive, multilingual interface | Automated browser coverage and persistent conversation storage are not implemented |
| Real JoeyLLM API connection | The browser uses a server-side Next.js `/api/chat` boundary and credentials remain server-side | Implemented and manually tested | [Architecture](https://github.com/joeyllm/ChatJoey/blob/main/docs/ARCHITECTURE.md), PR #4, [system validation](system-validation.md) | Enables end-to-end questions and genuine model responses | Production observability and broader failure testing remain future work |
| Deployment | The consolidated application is available online | Deployed | [https://chat-joey.vercel.app/](https://chat-joey.vercel.app/) and [deployment guide](https://github.com/joeyllm/ChatJoey/blob/main/docs/DEPLOYMENT.md) | Tutor, Client, and prospective users can review the live interface | Continued configuration and dependency maintenance are required |
| Qdrant/vector preparation | The team documented embeddings, collections, payloads, similarity search, HNSW, RAG boundaries, and evaluation variables | Researched | Qdrant documentation, technical discussion PDF, and literature review | Provides an evidence-based starting point for a retrieval-focused Sprint | No collection, embeddings, retrieval pipeline, RAG prompt, or benchmark is implemented |
| Target-user definition | Prior Semester 1 context indicates a broad audience of people interested in Australian information | Working assumption | Semester 1 project context | Provides an interim basis for general accessibility and information-oriented design | The Client has not explicitly confirmed the current target audience |

## 5. Discussion, Tutor feedback and team response

| Feedback ID | Source | Feedback, question or concern | Team response and rationale | Outcome | Linked decision / action / PBI |
| --- | --- | --- | --- | --- | --- |
| S4-F07 | Tutor | Meeting minutes must be formal and structured, including discussion, decisions, actions, responsibility, and follow-up | Accepted. The team adopted one professional template covering previous actions, evidence, feedback responses, rationale, risks, actions, improvement, next-meeting readiness, approval, and checklist traceability | Implemented as a process change | S4-D11, S4-A14, S4-I05 |
| S4-F08 | Tutor | Project communication evidence should not focus only on email; meeting outcomes and stakeholder responses must be visible | Accepted. The Sprint index and minutes link communication to decisions, actions, PBIs, and evidence | Implemented in the documentation structure | S4-A14, S4-I05 |
| S4-F09 | Tutor | Ticket names and descriptions should be unique, consistent, and sufficiently detailed | Accepted. New issues must state outcome, owner, acceptance criteria, evidence, and related feedback; Issue #3 is retained as an example of insufficient closure detail | Carry into Sprint 5 workflow | S4-D12, S4-A19, S4-I06 |
| S4-F10 | Tutor | User stories, personas, scenarios, and design should be mutually consistent and based on target users | Accepted. Current broad audience remains a working assumption; explicit Client confirmation stays open | Pending Client response | S4-A05, S4-A16, S4-R10 |
| S4-F11 | Tutor | User testing should use key tasks and usability criteria, and identified problems must become tickets | Accepted. The team preserved the manual system validation and will define a formal user-test PBI and convert future failures into uniquely named issues | Partial completion; formal user testing continues | S4-A17-S4-A19 |
| S4-F12 | Tutor | The team must show reflection and measurable improvement, not only product progress | Accepted. Week 3 includes a scheduled internal Sprint retrospective and measurable process improvements | Scheduled | S4-D13, S4-A20, S4-I05-S4-I07 |

## 6. Decisions and rationale

| Decision ID | Decision | Rationale / evidence considered | Confirmed by | Affected work | Effective date |
| --- | --- | --- | --- | --- | --- |
| S4-D11 | Use the shared professional meeting-minutes template as the sole formal meeting standard | Directly responds to Tutor feedback and creates an auditable feedback/action/decision/improvement chain | Southern-cross AI | All formal minutes and weekly evidence | 10 August 2026 |
| S4-D12 | Require unique ticket titles, acceptance criteria, an evidence link, and a closure explanation before a work item is treated as Done | Issue #3 was closed without sufficient visible outcome evidence | Southern-cross AI | Sprint 5 issue/PBI workflow | 10 August 2026 |
| S4-D13 | Hold a distinct internal Sprint retrospective rather than treating the Tutor progress review as the retrospective | External review feedback and internal process reflection answer different Checklist requirements | Southern-cross AI | 12 August internal meeting | 10 August 2026 |
| S4-D14 | Keep production Qdrant/RAG, model training, and data/backend experiments outside the Sprint 4 completion claim | The client provides the model framework and the required production choices/access were not available | Southern-cross AI | Sprint scope and next-Sprint planning | 10 August 2026 |

## 7. Risks, blockers, delays and scope changes

| ID | Risk / blocker | Impact on Sprint Goal | Mitigation | Accountable owner | Escalation / decision required | Review date | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4-R10 | Client has not explicitly confirmed the target audience | Detailed persona/scenario and usability priorities may rest on an assumption | Retain the broad Australia-information audience as a labelled working assumption and seek written confirmation | Wen Sun | Client clarification | 17 August 2026 | Open |
| S4-R11 | Manual tests passed but automated browser, load, security, and forced-failure coverage are not available | Future regressions may not be detected automatically | Create a test-automation PBI and preserve repeatable manual checks | Nuo Chen | Sprint 5 priority decision | 17 August 2026 | Open |
| S4-R12 | Qdrant configuration, embedding model, dataset permissions, metadata schema, and hosting are not confirmed | Retrieval work cannot yet produce a valid production implementation | Carry explicit questions and a controlled experiment plan into the next Sprint | Nuo Chen | Client technical decisions | 17 August 2026 | Open |

## 8. New action items

| Action ID | Action / deliverable | Accountable owner | Contributors | Linked feedback / decision | Due date | Acceptance criteria and evidence location | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4-A14 | Adopt the professional meeting-minutes template and remove weaker formal templates | Xingyu Li | Southern-cross AI | S4-F07, S4-F08, S4-D11 | 10 August 2026 | Template and README committed in `JoeyLLM-Team` | Done |
| S4-A15 | Remove the AI-prompt rule that assumes all members attended and document the approval/file-naming rules | Xingyu Li | Nuo Chen | S4-F07, S4-D11 | 11 August 2026 | Updated `templates/README.md` reviewed by Nuo Chen | In progress |
| S4-A16 | Obtain explicit Client confirmation of target users; otherwise retain the question as open | Wen Sun | Xiang Chang, Xingyu Li | S4-F10, S4-R10 | 17 August 2026 | Written Client response or documented pending item | Open |
| S4-A17 | Preserve the repeatable manual validation record and convert future failures into issues | Nuo Chen | Southern-cross AI | S4-F11, S4-R11 | 17 August 2026 | Updated validation record and linked issues where applicable | Open |
| S4-A18 | Create an automated browser-test PBI with clear acceptance criteria | Nuo Chen | Yingzhe Xu | S4-F11, S4-R11 | 17 August 2026 | ChatJoey issue linked from the next minutes | Open |
| S4-A19 | Define consistent ticket naming and closure requirements for Sprint 5 PBIs | Xiang Chang | Southern-cross AI | S4-F09, S4-D12 | 12 August 2026 | Retrospective decision and sample PBI format | Open |
| S4-A20 | Conduct the internal Sprint retrospective and convert improvement outcomes into Sprint 5 PBIs | Xiang Chang | Southern-cross AI | S4-F12, S4-D13 | 12 August 2026 | Approved retrospective minutes with measurable improvements | Scheduled |

## 9. Continuous improvement

| Improvement ID | Observed problem and evidence | Root cause | Process change | Accountable owner | Success measure | Review date | Linked PBI / status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4-I05 | Minutes lacked previous-action closure, feedback response, rationale, measurable improvement, and next-meeting evidence | No single formal quality standard or reviewer existed | Use the professional template, publish through PR, and require Nuo Chen review | Xingyu Li | Every formal record passes the publication quality gate with no placeholder or group-only owner | 17 August 2026 | S4-A14-S4-A15 / In progress |
| S4-I06 | Issue #3 was closed without visible outcome, links, or acceptance evidence | Ticket closure did not have a Definition of Done | Add unique title, description, owner, acceptance criteria, evidence, and closure comment requirements | Xiang Chang | Every new closed Sprint 5 issue includes evidence and an acceptance statement | 31 August 2026 | S4-A19 / Open |
| S4-I07 | Manual testing was discussed without one consistent evidence record | Validation was distributed across conversation, PR notes, and individual checks | Maintain one system-validation record and link every defect to an issue | Nuo Chen | All planned test cases have a result and every failure has a linked issue | 17 August 2026 | S4-A17-S4-A18 / Open |

## 10. Next meeting readiness

| Field | Details |
| --- | --- |
| Confirmed date / time | 12 August 2026, 20:00 AEST |
| Meeting type | Internal Sprint Retrospective |
| Purpose | Close Sprint 4 process learning and convert review feedback into Sprint 5 PBIs |
| Required completed actions | S4-A14, S4-A15, preparation for S4-A19-S4-A20 |
| Evidence to present | Tutor feedback, professional template commits, issue examples, validation record, research plan, risks, and open Client clarification |
| Decisions required | Meeting governance, ticket Definition of Done, user-testing workflow, and Sprint 5 carry-over priorities |
| Presenters | Xiang Chang (process/PBIs), Nuo Chen (testing/research), Yingzhe Xu (UI evidence), Wen Sun (Client clarification), Xingyu Li (minutes governance) |
| Pre-reading | This Tutor record, system validation, template, and Sprint evidence index |

### Proposed next-meeting agenda

1. Review Tutor feedback and close S4-A14-S4-A15 where evidence is ready.
2. Run the Sprint retrospective: what worked, what did not, root causes, and lessons.
3. Confirm measurable improvements and their owners.
4. Convert product, testing, retrieval, communication, and process follow-up into Sprint 5 PBIs.
5. Confirm evidence and questions for the 17 August Tutor meeting.

## 11. Meeting close and approval

| Check | Result |
| --- | --- |
| Open actions at close | S4-A15-S4-A20; S4-A14 completed |
| Decisions recorded | S4-D11-S4-D14 |
| Feedback awaiting external response | S4-F10 / target-user confirmation |
| Risks requiring escalation / decision | S4-R10-S4-R12 |
| Minutes prepared by | Xingyu Li |
| Reviewer | Nuo Chen |
| Approval status | Draft pending Nuo Chen review |
| Distributed to | Tutor and Southern-cross AI |
| GitHub location | This document |

## 12. Sprint checklist traceability

| Checklist dimension | Evidence captured | IDs / links |
| --- | --- | --- |
| Stakeholder Engagement | Tutor feedback, explicit responses, Client clarification, follow-up actions, and next-meeting preparation | S4-F07-S4-F12, S4-A16 |
| Planning and Organisation | Sprint Goal, action closure, PBIs, owners, dates, risks, and retrospective preparation | S4-A14-S4-A20, S4-R10-S4-R12 |
| Execution and Quality | PR #4, deployment, system validation, accurate implementation boundaries, and test carry-over | Progress table, S4-A17-S4-A18 |
| Reflection and Improvement | Tutor review separated from the internal retrospective; root-cause improvements have measures and review dates | S4-D13, S4-I05-S4-I07 |
