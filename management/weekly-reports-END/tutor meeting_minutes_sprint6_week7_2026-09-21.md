# Tutor Meeting Minutes

## 1. Meeting information

| Field | Details |
| --- | --- |
| Project | Southern-cross AI |
| Meeting type | Tutor Meeting |
| Sprint / Week | Sprint 6 / Week 7 |
| Date | 21 September 2026 |
| Time | 20 mins |
| Location / Channel | HIVE pod 4 / in-person tutor meeting |
| Chair | Annie Sun|
| Present | Annie Sun; Wen Sun; Yingzhe Xu; Nuo Chen; Xiang Chang; Xingyu Li |
| Apologies / Absent | Matthew (Client) did not respond to the team's meeting email and did not attend the planned 1:00 pm client meeting |
| Meeting objective | Review Sprint 6 progress, confirm final-sprint scope, discuss the client's lack of response, agree on testing/documentation expectations, and prepare for Sprint Review and final handover |
| Related Sprint Goal / Milestone | Sprint 6 — complete the chunk-based duplicate-removal workflow, validate the backend work, and wrap up the project for handover |
| Minutes location | Not yet published |

## 2. Agenda

1. Review previous actions and unresolved decisions.
2. Confirm progress against the Sprint Goal and current backend work.
3. Review the chunk-based duplicate-removal workflow and supporting infrastructure.
4. Discuss client availability, Sprint 6 workload, testing expectations and possible scope changes.
5. Confirm Sprint Review scheduling, Week 10 handover requirements and final-delivery preparation.
6. Record actions, risks and process improvements.

## 3. Review of previous actions

| Previous ID | Action / Deliverable | Accountable owner | Original due date | Current status | Completion evidence | Reason and revised next step if not done |
| --- | --- | --- | --- | --- | --- | --- |
| PA-01 | Improve PBI/task descriptions and acceptance comments based on previous tutor feedback | Team; individual accountable owner not recorded | Not recorded | Done | Tutor explicitly noted good use of descriptions and a large improvement from previous feedback | Continue the same documentation standard in Sprint 6 |
| PA-02 | Build a local web tool for manually marking / comparing dataset records | Team; individual accountable owner not recorded | Not recorded | Implemented | Team reported that the local website had been built and was still working | Keep available as supporting evidence for Sprint 6 review |
| PA-03 | Prepare the required virtual environment on the project server | Team; individual accountable owner not recorded | Not recorded | Implemented | Team reported that the virtual environment had been created and was working on the server | Retain setup information for handover documentation |
| PA-04 | Maintain client communication after the teaching break | Wen Sun / team | 21 September 2026 | In progress | Team emailed the client on the morning of the meeting and invited him to a 1:00 pm meeting, but received no reply | Continue email updates and request clarification on testing, remaining scope and handover |

## 4. Progress and evidence presented

| PBI / Work item | Progress since last meeting | Verified status | Evidence shown | User / stakeholder impact | Remaining gap |
| --- | --- | --- | --- | --- | --- |
| Sprint 6 — chunk-based duplicate-removal workflow | Team decomposed the work into a staged workflow: workflow design first, implementation second, then data runs / feedback | Designed / in progress | Workflow was explained during the tutor meeting | Provides an alternative deduplication method after the earlier hash-based approach and supports the client's research needs | Implementation, evaluation and client feedback are still required |
| Existing deduplication backend | Team clarified that Sprint 6 continues work on the existing system rather than introducing an unrelated new product feature | In progress | Tutor discussion confirmed the work remains primarily backend-focused | Keeps Sprint 6 aligned with project wrap-up rather than expanding scope late | Need to confirm with client that no additional ongoing work is expected |
| Local data-marking website | Local web tool for marking / comparing datasets remains operational | Implemented | Team reported the tool still works | Supports manual inspection and validation of dataset differences | No formal test record was presented |
| Server environment | Required virtual environment is working on the server | Implemented | Team verbally confirmed successful setup | Reduces setup risk for backend experimentation | Handover instructions still need to document access and environment setup |
| Client engagement | Team emailed the client and attempted to hold the planned client meeting | Attempted / unresolved | Email sent; client did not reply or attend | Client feedback is needed to confirm testing expectations and close Sprint 6 cleanly | No client response since before / around the teaching break |

## 5. Discussion, stakeholder feedback and team response

| Feedback ID | Agenda item / Source | Feedback, question or concern | Team response and rationale | Outcome | Linked decision / action / PBI |
| --- | --- | --- | --- | --- | --- |
| F-01 | Tutor | Sprint 6 is the last active development sprint, so the team should focus on wrapping up rather than accepting open-ended ongoing work | Accepted. Team agreed that the current workload is suitable and should remain focused on the existing backend task | Resolved | D-01, A-01 |
| F-02 | Tutor | Keep a clear one-sentence Sprint Goal even though the task breakdown already exists | Accepted. Team will maintain a concise Sprint Goal alongside detailed task descriptions | Resolved | A-04 |
| F-03 | Tutor | The current task descriptions show a major improvement compared with previous feedback | Accepted. Team will continue the same documentation practice | No further action required | I-01 |
| F-04 | Tutor | The team should discuss workload and any possible maintenance / ongoing work with the client because the team will not continue development after Sprint 6 | Accepted. Team will tell the client that new ongoing work must be handed back or reassigned after this sprint | Pending client response | D-01, A-01 |
| F-05 | Tutor | Consider more systematic testing rather than relying only on casual developer checks | Accepted conditionally. Team will first ask the client whether systematic testing is required; if yes, use a structured table | Pending client response | D-02, A-03 |
| F-06 | Tutor | A systematic test record should include date, tested feature/data/function, expected result, actual result, pass/fail and tester | Accepted. This structure will be used if formal testing is required; otherwise lightweight test notes will still be kept | Resolved | D-02, A-03 |
| F-07 | Tutor | Because the backend refinement may not create a visible frontend change, even casual testing should still be documented with short notes | Accepted. Team will retain brief evidence of checks performed during development | Resolved | A-03, I-02 |
| F-08 | Tutor | Client non-response is a concern in the final sprint; the tutor will contact the support team to make sure the client remains engaged | Accepted. Team will continue emailing progress while the tutor checks the situation | Pending | A-02, R-01 |
| F-09 | Tutor | The client should not return late in Sprint 6 with a large new feature request; the team can push back professionally if scope is unreasonable | Accepted. Team will evaluate any new request against remaining Sprint 6 capacity and final handover needs | Resolved | D-01, R-02 |
| F-10 | Tutor | Week 9 Monday is a public holiday; Sprint Review scheduling must move to Tuesday-Friday. The current tutor is available Tuesday and Wednesday; another tutor may cover Thursday or Friday | Accepted. Team will confirm availability after receiving the tutor's schedule email | Pending scheduling | A-05, R-04 |
| F-11 | Tutor | Week 10 should focus on documentation, user manual, final wrap-up, and handing project access back to the client | Accepted. Team will prepare documentation and remove / return project access as part of final handover | Resolved | D-03, A-06 |
| F-12 | Tutor | Final delivery format is not yet confirmed; it may be a presentation or showcase and students should monitor Canvas after Week 10 | Clarification required. No final format has been announced | Pending | R-03 |

## 6. Decisions and rationale

| Decision ID | Decision | Rationale / Evidence considered | Confirmed by | Affected PBI / Document | Effective date |
| --- | --- | --- | --- | --- | --- |
| D-01 | Keep Sprint 6 focused on the existing chunk-based duplicate-removal backend workflow and project wrap-up; do not accept substantial new ongoing scope without reassessment | Sprint 6 is the final development sprint and the tutor advised avoiding open-ended work or late feature expansion | Tutor and team | Sprint 6 backlog | 21 September 2026 |
| D-02 | Ask the client whether formal systematic testing is required. If yes, use a table containing date, test item, expected result, actual result, pass/fail and tester; otherwise retain concise testing notes | Backend changes may not produce large visible differences, but evidence of validation is still required for Sprint Review | Tutor and team | Testing record / Sprint Review evidence | 21 September 2026 |
| D-03 | Use Week 10 primarily for documentation, user manual, handover and return of project access to the client | The project is approaching final delivery and access should not remain with the student team after handover | Tutor and team | Handover documentation | 21 September 2026 |
| D-04 | Continue proactive written client updates even while waiting for a response | The client has been unavailable and Sprint 6 requires a clear evidence trail of engagement and completed work | Tutor and team | Client communication log | 21 September 2026 |

## 7. Risks, blockers, delays and scope changes

| ID | Risk / Blocker / Change | Impact on Sprint Goal | Current mitigation | Accountable owner | Escalation or decision required | Due / Review date | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R-01 | Client has not responded to emails or attended the planned meeting | Delays confirmation of testing expectations, workload and final handover requirements | Continue progress emails; tutor to contact support team | Solomon | Confirm whether client contact can be restored | 21 September 2026 | Open |
| R-02 | Client may request substantial new work late in Sprint 6 | Could create scope, schedule and handover risk | Evaluate any new request against final-sprint capacity and push back professionally if unreasonable | Wen Sun, acting as team contact | Client confirmation of remaining scope | Before Sprint Review | Monitoring |
| R-03 | Final delivery format is still unknown | Team cannot fully prepare presentation / showcase materials yet | Monitor Canvas and tutor announcements after Week 10 | Wen Sun | Course staff clarification | After Week 10 announcement | Monitoring |
| R-04 | Week 9 Monday public holiday changes Sprint Review scheduling | May affect tutor availability and review preparation | Select Tuesday or Wednesday with Solomon where possible; Thursday/Friday may use another tutor | Wen Sun | Confirm team availability after tutor email | Before Week 9 | Open |
| R-05 | Formal testing expectations are not yet confirmed | Risk of insufficient evidence at Sprint Review | Ask client; regardless of response, keep lightweight testing notes during development | Wen Sun, acting as team contact | Client clarification preferred | Before Sprint Review | Monitoring |

## 8. New action items

| Action ID | Action / Deliverable | Accountable owner | Contributors | Linked feedback / decision / PBI | Due date | Acceptance criteria and evidence location | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A-01 | Send the client a follow-up covering Sprint 6 progress, remaining workload, possible ongoing work, testing expectations and handover | Wen Sun | Team | F-01, F-04, D-01, D-04, R-01 | 22 September 2026 | Email sent and retained in the project communication record | Open |
| A-02 | Contact the project support team regarding the client's lack of response and confirm whether escalation is needed | Solomon | None | F-08, R-01 | 21 September 2026 | Support contact completed and outcome communicated to the team | In progress |
| A-03 | Maintain a testing record for Sprint 6; use the structured table if formal testing is requested, otherwise record concise test notes with evidence | Wen Sun | Yingzhe Xu; Nuo Chen; Xiang Chang; Xingyu Li | F-05, F-06, F-07, D-02, R-05 | Before Sprint Review | Test record contains date, tested item, expected/actual result where applicable, pass/fail and tester; linked from Sprint Review evidence | Open |
| A-04 | Add / retain a one-sentence Sprint 6 Goal in the project management record | Wen Sun | Team | F-02 | 22 September 2026 | Sprint Goal visible in the Sprint 6 board / documentation | Open |
| A-05 | Confirm Week 9 Sprint Review availability after receiving Solomon's schedule email | Wen Sun | Team | F-10, R-04 | 25 September 2026 | Review day confirmed with tutor; replacement tutor identified if Thursday/Friday is selected | Open |
| A-06 | Prepare Week 10 handover package including documentation, user manual, environment/setup notes and access-return checklist | Wen Sun | Yingzhe Xu; Nuo Chen; Xiang Chang; Xingyu Li | F-11, D-03 | 9 October 2026 | Handover package complete; client access ownership restored; team access removed or transferred as required | Open |
| A-07 | Continue implementation and evaluation of the chunk-based deduplication workflow without expanding into unrelated new features | Wen Sun | Yingzhe Xu; Nuo Chen; Xiang Chang; Xingyu Li | D-01, Sprint 6 Goal | Before Sprint Review | Working implementation, run evidence and concise comparison / findings ready for review | In progress |

## 9. Continuous improvement

| Improvement ID | Observed problem and evidence | Likely root cause | Improvement experiment / Process change | Accountable owner | Success measure | Review date | Linked PBI / Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| I-01 | Earlier tutor feedback indicated the team's task descriptions and professional documentation needed improvement; the tutor now noted a significant improvement | Previous records were not sufficiently explicit or professionally structured | Continue using descriptive PBIs, completion comments and concise Sprint Goals | Wen Sun | Sprint Review contains clear descriptions, statuses and evidence with no ambiguous task naming | Sprint Review | In progress |
| I-02 | Backend work may be tested informally but leave little reviewable evidence | Validation happens during development but is not consistently recorded | Add a lightweight testing log throughout Sprint 6 even if formal test cases are not required | Wen Sun | Every meaningful backend validation has a dated note and identifiable tester / result | Sprint Review | Open |
| I-03 | Client availability has become unreliable near the end of the project | Communication depends too heavily on synchronous meetings | Use written progress emails as the default evidence trail and escalate non-response early | Wen Sun | No Sprint 6 decision or deliverable is blocked solely because a meeting did not occur | 25 September 2026 | Open |

## 10. Next meeting readiness

| Field | Details |
| --- | --- |
| Confirmed date / time | Week 9; exact day/time pending tutor email. Solomon is available Tuesday and Wednesday; another tutor may cover Thursday or Friday |
| Meeting type | Sprint Review |
| Purpose | Review Sprint 6 outcomes, evidence, testing, client communication, risks and readiness for Week 10 handover |
| Required completed actions | A-01, A-03, A-04, A-05; substantial progress on A-07 |
| Evidence to present | Chunk-based dedup workflow / implementation; run results; local marking tool; environment evidence; testing log; client email trail; Sprint Goal; current backlog and risks |
| Decisions / Clarifications requested | Whether the client requires systematic testing; confirmation of any remaining client-requested scope; Sprint Review schedule; final-delivery format when available |
| Presenter(s) | Team presenters to be assigned before Sprint Review |
| Pre-reading / Material to send | Updated Sprint 6 board, testing record and client communication summary |

### Proposed next-meeting agenda

1. Verify the status and evidence for every Sprint 6 action due before the review.
2. Demonstrate the chunk-based deduplication workflow and explain its purpose relative to the earlier hash-based approach.
3. Present testing / validation evidence and any client feedback received.
4. Review client communication status, unresolved risks and any late scope requests.
5. Confirm Week 10 documentation, handover and access-return tasks.
6. Confirm final delivery preparation once course staff publish the format.

## 11. Meeting close and approval

| Check | Result |
| --- | --- |
| Open actions at close | 6 open / in-progress actions: A-01, A-02, A-03, A-04, A-05, A-06, plus ongoing development A-07 |
| Decisions recorded | 4: D-01 to D-04 |
| Feedback items awaiting response | F-05 / F-08 / F-10 / F-12 depend on client, tutor scheduling or course-staff clarification |
| Risks requiring escalation | R-01 — client non-response |
| Minutes drafted by / date | Wen Sun, 21 September 2026 |
| Minutes reviewed by / date | Not yet reviewed |
| Distributed to | Team / Tutor after review |
| GitHub commit / document link | Not yet published |

## 12. Sprint checklist traceability

| Checklist dimension | Evidence captured in these minutes | Direct links / IDs |
| --- | --- | --- |
| Stakeholder Engagement | Client non-response, tutor escalation, team follow-up, testing clarification and handover communication | F-04 to F-08; D-04; A-01; A-02; R-01 |
| Planning and Organisation | Sprint 6 scope, one-sentence Sprint Goal, workload control, review scheduling and handover plan | F-01, F-02, F-09, F-10, F-11; D-01, D-03; A-04 to A-07 |
| Execution and Quality | Chunk-based dedup workflow, local marking tool, server environment, testing expectations and evidence requirements | Section 4; F-05 to F-07; D-02; A-03; A-07 |
| Reflection and Improvement | Improved task descriptions, systematic testing records and written client communication process | I-01 to I-03 |

## Publication quality gate

Before publishing, confirm all boxes:

- [x] Metadata, attendees, objective, Sprint Goal and location are recorded; exact meeting time was not available in the transcript.
- [x] Previous actions discussed in the meeting have a current status and evidence / limitation note.
- [x] Work claims are distinguished as designed, implemented, in progress or unresolved.
- [x] Material tutor feedback has a recorded team response.
- [x] Final decisions include rationale and affected actions.
- [x] New actions have one named accountable owner or explicitly identify where the meeting did not confirm individual ownership.
- [x] Blockers include impact, mitigation, owner and escalation path.
- [x] Process improvements include a success measure and review point.
- [x] Next-meeting preparation identifies actions, evidence and required clarification.
- [x] Work-item titles are specific and tied to the relevant Sprint 6 outcome.
- [ ] Add direct GitHub / email / issue links before publication.
- [ ] Confirm attendee list and exact meeting time before publication if required by the course.
- [ ] Confirm Sprint Review date after Solomon's availability email.
- [ ] Have the team / tutor review the minutes before final publication.
