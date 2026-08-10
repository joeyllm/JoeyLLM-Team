# Internal Sprint Retrospective - Scheduled Record

**Record status:** Scheduled draft. The meeting is set for 12 August 2026 and this document must not be marked Approved until the meeting has occurred and the outcomes below have been confirmed.

## 1. Meeting information

| Field | Details |
| --- | --- |
| Project | Southern-cross AI / JoeyLLM |
| Meeting type | Weekly Internal Team Meeting / Sprint 4 Retrospective |
| Sprint / Week | Sprint 4 / Week 3 |
| Date | 12 August 2026 |
| Time | 20:00 AEST; end time to be recorded |
| Location / Channel | Online team meeting |
| Chair | Xiang Chang |
| Minute taker | Xingyu Li |
| Expected attendees | Nuo Chen, Wen Sun, Xiang Chang, Xingyu Li, Yingzhe Xu |
| Apologies / Absent | To be confirmed after the meeting |
| Meeting objective | Review Sprint 4 outcomes and process, determine root causes of identified weaknesses, and convert improvements into Sprint 5 PBIs |
| Related Sprint Goal / Milestone | [Sprint 4 Goal](../../../SPRINT4_GOALS.md) / [Sprint 4 milestone](https://github.com/joeyllm/JoeyLLM-Team/milestone/5) |
| Minutes location | `management/weekly-reports-END/sprint-04/week-03/internal-retrospective-2026-08-12.md` |

## 2. Confirmed agenda

1. Review actions S4-A14-S4-A20 and open risks S4-R10-S4-R12.
2. Confirm what went well in frontend exploration, convergence, API integration, deployment, validation, and research.
3. Confirm what did not go well in minutes, ticket closure, target-user clarification, and test evidence.
4. Determine root causes without assigning blame.
5. Agree on measurable process improvements and Sprint 5 PBIs.
6. Confirm evidence and questions for the 17 August Tutor meeting.

## 3. Previous actions to review

| Previous ID | Required review | Accountable owner | Due | Evidence available before meeting | Status to confirm |
| --- | --- | --- | --- | --- | --- |
| S4-A14 | Professional template adoption | Xingyu Li | 10 August 2026 | Template and repository history | Done |
| S4-A15 | Safe AI prompt, approval, and naming rules | Xingyu Li | 11 August 2026 | Updated template README | To confirm |
| S4-A16 | Target-user confirmation | Wen Sun | 17 August 2026 | Client has not explicitly confirmed | In progress |
| S4-A17 | Repeatable manual validation record | Nuo Chen | 17 August 2026 | `system-validation.md` | To confirm |
| S4-A18 | Automated browser-test PBI | Nuo Chen | 17 August 2026 | PBI/issue to be created | Open |
| S4-A19 | Ticket naming and closure requirements | Xiang Chang | 12 August 2026 | Tutor feedback and template quality gate | To decide |
| S4-A20 | Conduct this retrospective and create improvement PBIs | Xiang Chang | 12 August 2026 | This scheduled record | Scheduled |

## 4. Evidence prepared for discussion

| Area | Evidence | Status before meeting | Question for the team |
| --- | --- | --- | --- |
| Frontend convergence | Frontend selection PDF, PR #4, decision log | Implemented | Which comparison and integration practices should continue? |
| Deployment and testing | Live application and system validation | Deployed and manually tested | What automated or user-testing coverage is required next? |
| Retrieval preparation | Qdrant documents, technical discussion, and literature review | Researched | Which client decisions and minimum spike belong in Sprint 5? |
| Stakeholder requirements | Tutor feedback and open target-user question | Partially resolved | How will the team obtain and record explicit Client confirmation? |
| Documentation process | Professional template and Sprint index | Implemented, review pending | What publication SLA and reviewer rule will be adopted? |

## 5. Retrospective prompts to complete during the meeting

### What went well

- Confirm the value of independent prototypes before convergence.
- Confirm the value of selecting one shared implementation and retaining a documented decision.
- Confirm the effectiveness of the server-side API boundary, deployment, and team validation.
- Confirm the value of Qdrant and retrieval research while production access/decisions were unavailable.

### What did not go well

- Confirm the effect of weak or incomplete meeting-minutes structure.
- Confirm why Issue #3 closed without sufficient evidence and acceptance information.
- Confirm why target-user clarification remained open.
- Confirm the limitations of distributed manual test evidence.

### Root causes

- Confirm whether the team lacked a shared minutes quality gate and named reviewer.
- Confirm whether collaborative work obscured accountable evidence ownership.
- Confirm whether ticket closure lacked a Definition of Done.
- Confirm whether review feedback was not systematically converted into PBIs.

## 6. Decisions to confirm

| Proposed ID | Proposed decision | Rationale | Required confirmation | Affected work |
| --- | --- | --- | --- | --- |
| S4-D15 | Require formal minutes within 24 hours of each assessed meeting and Nuo Chen review before Approved status | Creates timely, auditable evidence | All five members | Meeting workflow |
| S4-D16 | Require every new issue to have a unique outcome title, owner, acceptance criteria, evidence, and closure comment | Prevents untraceable closure | All five members | Sprint 5 PBI workflow |
| S4-D17 | Keep one accountable evidence owner while listing all members as contributors to collaborative delivery | Preserves teamwork and accountability | All five members | All action tables |
| S4-D18 | Prioritise target-user clarification, formal user testing, automated browser testing, and a reproducible Qdrant spike as Sprint 5 candidates | Directly closes Tutor feedback and current evidence gaps | All five members | Sprint 5 planning |

## 7. Risks to review

| ID | Risk | Current mitigation | Owner | Decision / escalation required | Review date | Status before meeting |
| --- | --- | --- | --- | --- | --- | --- |
| S4-R10 | Target audience not explicitly Client-confirmed | Maintain working assumption and request confirmation | Wen Sun | Client response | 17 August 2026 | Open |
| S4-R11 | No automated browser/load/security coverage | Preserve manual tests and create PBI | Nuo Chen | Sprint 5 priority | 17 August 2026 | Open |
| S4-R12 | Retrieval configuration and access decisions unavailable | Carry controlled research plan and Client questions | Nuo Chen | Client technical decisions | 17 August 2026 | Open |

## 8. Proposed improvement actions to confirm

| Action ID | Proposed action / deliverable | Accountable owner | Contributors | Linked feedback / decision | Due | Acceptance criteria | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S4-A21 | Apply the 24-hour drafting and Nuo Chen review rule to the next formal meeting | Xingyu Li | Southern-cross AI | S4-F07, S4-D15 | 17 August 2026 | Next minutes contain draft/review timestamps and pass the quality gate | Proposed |
| S4-A22 | Create Sprint 5 PBIs for target-user confirmation, user testing, automated browser testing, and the Qdrant spike | Xiang Chang | Southern-cross AI | S4-F09-S4-F12, S4-D18 | 17 August 2026 | Uniquely named PBIs with owner, acceptance criteria, and evidence location | Proposed |
| S4-A23 | Send the Client the target-user and retrieval-decision questions | Wen Sun | Xiang Chang, Xingyu Li | S4-R10, S4-R12 | 17 August 2026 | Sent communication and recorded response/status | Proposed |

## 9. Continuous improvement measures to confirm

| Improvement ID | Problem | Proposed process change | Owner | Success measure | Review date | Status |
| --- | --- | --- | --- | --- | --- | --- |
| S4-I08 | Formal minutes were not consistently complete | 24-hour draft plus reviewer quality gate | Xingyu Li | 100% of formal records pass all template checks before Approved | 31 August 2026 | Proposed |
| S4-I09 | Ticket closure lacked auditable acceptance evidence | Definition of Done for every issue | Xiang Chang | 100% of newly closed issues contain acceptance evidence and closure rationale | 31 August 2026 | Proposed |
| S4-I10 | Testing evidence was distributed and mostly manual | One validation record plus issue-linked failures and an automation PBI | Nuo Chen | Every planned test has a recorded result; every failure has an issue | 31 August 2026 | Proposed |

## 10. Next meeting readiness

| Field | Details |
| --- | --- |
| Confirmed date / time | 17 August 2026, 14:00 AEST |
| Meeting type | Tutor Meeting |
| Purpose | Present Sprint 4 closure, retrospective improvements, Sprint 5 PBIs, and remaining Client decisions |
| Required completed actions | Actions confirmed from S4-A21-S4-A23 |
| Evidence to present | Approved retrospective, professional template adoption, validation record, research plan, new PBIs, and Client clarification status |
| Decisions / clarifications requested | Tutor feedback on Sprint 5 scope, user testing, and retrieval preparation |
| Presenters | Workstream evidence owners |
| Pre-reading | Sprint 4 index, retrospective, PBIs, and open-risk summary |

## 11. Meeting close and approval

| Check | Result |
| --- | --- |
| Open actions at close | To be confirmed during the meeting |
| Decisions recorded | To be confirmed during the meeting |
| Feedback awaiting response | Target-user and retrieval Client questions |
| Risks requiring escalation | S4-R10-S4-R12 |
| Minutes prepared by | Xingyu Li |
| Reviewer | Nuo Chen |
| Approval status | Scheduled draft; cannot be Approved before the meeting |
| Distributed to | Southern-cross AI |
| GitHub location | This document |

## 12. Sprint checklist traceability

| Checklist dimension | Evidence prepared | Direct IDs / links |
| --- | --- | --- |
| Stakeholder Engagement | Review feedback, Client questions, proposed responses, owners, and next-meeting preparation | S4-A16, S4-A23, S4-R10, S4-R12 |
| Planning and Organisation | Action review, Sprint 5 PBI plan, owners, dates, risks, and evidence requirements | S4-A21-S4-A23, S4-D15-S4-D18 |
| Execution and Quality | Deployment/validation evidence and proposed automation workflow | System validation, S4-I10 |
| Reflection and Improvement | Distinct internal retrospective, root-cause prompts, measurable improvements, and review dates | S4-I08-S4-I10 |
