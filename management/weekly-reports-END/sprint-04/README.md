# Sprint 4 Meeting and Evidence Index

**Team:** Southern-cross AI  
**Sprint window:** 27 July-11 August 2026  
**Sprint goal:** [Complete the ChatJoey frontend workstream, connect the real JoeyLLM API, and prepare the team for vector database work](../../SPRINT4_GOALS.md)  
**Minutes reviewer:** Nuo Chen

## Sprint narrative

Sprint 4 progressed through a connected three-week sequence:

1. **Week 1 - establish the Sprint.** The team reviewed Semester 1 evidence, confirmed the need for a clear Sprint Goal and organised the repository and meeting process while JupyterHub and the server were unavailable.
2. **Week 2 - clarify and execute.** Matthew requested independent Next.js chat-interface work and Qdrant learning. The Tutor confirmed that user identification, research evidence, stable scope, and professional clarification were required. The team converted that feedback into parallel prototype, communication, and research actions.
3. **Week 3 - converge, validate, review, and improve.** The team compared the prototypes, selected Yingzhe Xu's interface as the shared baseline, consolidated it into `ChatJoey/main`, connected the real JoeyLLM API, deployed and tested the application, documented Qdrant learning, received Tutor feedback, and adopted a stronger meeting-minutes process.

The client supplies the model framework. Sprint 4 does not claim model fine-tuning, post-training, production Qdrant integration, or unauthorised backend experiments.

## Authoritative meeting records

| Week | Meeting | Record | Purpose |
| --- | --- | --- | --- |
| 1 | Tutor / Sprint planning, 27 July | [`week-01/tutor-2026-07-27.md`](week-01/tutor-2026-07-27.md) | Establish scope, governance, risks, and preparation actions |
| 2 | Tutor, 3 August | [`week-02/tutor-minutes-2026-08-03.md`](week-02/tutor-minutes-2026-08-03.md) | Confirm UI/research scope and stakeholder expectations |
| 2 | Internal, 5 August | [`week-02/internal-minutes-2026-08-05.md`](week-02/internal-minutes-2026-08-05.md) | Convert feedback into work allocation and evidence requirements |
| 3 | Tutor / progress review, 10 August | [`week-03/tutor-minutes-2026-08-10.md`](week-03/tutor-minutes-2026-08-10.md) | Present verified outcomes and record Tutor feedback |
| 3 | Internal Sprint retrospective, 12 August | [`week-03/internal-retrospective-2026-08-12.md`](week-03/internal-retrospective-2026-08-12.md) | Scheduled close-out of Sprint 4 process learning and Sprint 5 improvements |

## Supporting reports and evidence

| Evidence | Location | Status / use |
| --- | --- | --- |
| Week 2 weekly report | [`week-02/report.md`](week-02/report.md) | Pre-meeting progress summary |
| Week 2 detailed Tutor preparation | [`week-02/tutor-2026-08-03.md`](week-02/tutor-2026-08-03.md) | Pre-meeting report; not post-meeting minutes |
| Sprint summary | [`week-03/ChatJoey_Sprint_Summary_English.pdf`](week-03/ChatJoey_Sprint_Summary_English.pdf) | Supporting Sprint narrative; team confirmation required where indicated |
| Frontend selection record | [`week-03/Meeting record about front-end website.pdf`](week-03/Meeting%20record%20about%20front-end%20website.pdf) | Evidence for the shared frontend decision |
| Vector-database discussion | [`week-03/Vector_Database_Meeting_Minutes_EN.pdf`](week-03/Vector_Database_Meeting_Minutes_EN.pdf) | Technical research evidence |
| System validation | [`week-03/system-validation.md`](week-03/system-validation.md) | Member validation and test-scope record |
| Vector retrieval literature review | [`week-03/research/vector-retrieval-literature-review.md`](week-03/research/vector-retrieval-literature-review.md) | Research evidence and proposed evaluation plan |
| Live application | [ChatJoey on Vercel](https://chat-joey.vercel.app/) | Deployed shared interface |
| Consolidation and API integration | [ChatJoey PR #4](https://github.com/joeyllm/ChatJoey/pull/4) | Implementation, validation, security, and scope evidence |
| Current implementation boundary | [ChatJoey current state](https://github.com/joeyllm/ChatJoey/blob/main/docs/CURRENT_STATE.md) | Implemented and not-yet-implemented states |

## Traceability summary

| Dimension | Evidence chain |
| --- | --- |
| Stakeholder Engagement | Tutor feedback IDs `S4-F01`-`S4-F11`, team responses, linked actions, and next-meeting preparation in the weekly minutes |
| Planning and Organisation | Sprint Goal, workstream allocation, exact dates, owners, risks, and carry-over actions `S4-A01` onwards |
| Execution and Quality | Prototype PRs, shared implementation PR #4, deployment URL, system validation, research evidence, and explicit scope limitations |
| Reflection and Improvement | Week 3 Tutor feedback, adoption of the professional template, scheduled Sprint retrospective, measurable process improvements, and Sprint 5 carry-over PBIs |

## Status conventions

- Minutes and reports are the management source of truth in `JoeyLLM-Team`.
- Code, technical decisions, PRs, and implementation issues remain in `ChatJoey` and are linked rather than duplicated.
- PDFs are supporting evidence. Markdown minutes are the authoritative decision-and-action records.
- A record becomes Approved only after Nuo Chen reviews it.
