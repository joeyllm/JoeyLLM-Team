# Sprint 4 Meeting and Evidence Chain

**Team:** Southern-cross AI  
**Sprint evidence period:** 27 July-10 August 2026  
**Sprint Goal:** [Complete the ChatJoey frontend workstream, connect the real JoeyLLM API, and prepare the team for vector database work](../../SPRINT4_GOALS.md)  
**Canonical minutes template:** [Professional Meeting Minutes Template](../templates/professional-meeting-minutes-template.md)  
**Approval:** Each authoritative meeting record was approved by Nuo Chen on the date of that meeting.

## 1. How to read this evidence set

This README is the entry point to the Sprint 4 evidence. It explains what happened, why each decision was made, which action followed, where the result can be verified, and how the result was closed. A reader should not need prior knowledge of JoeyLLM to follow the chain.

All authoritative meeting minutes use the same professional structure:

1. meeting information and objective;
2. agenda;
3. review of actions created by the previous meeting;
4. progress and evidence presented;
5. stakeholder feedback and the team's response;
6. decisions and rationale;
7. risks, blockers and scope changes;
8. new actions with one accountable owner, a due date and acceptance evidence;
9. measurable process improvement;
10. preparation for the next review, or a final Sprint-close boundary when no later Sprint 4 meeting exists;
11. approval and open-item summary; and
12. Sprint Checklist traceability.

The Week 3 record uses a Sprint-close boundary in Section 10 because Sprint 4 evidence was closed on 10 August and no later meeting is claimed. This is a deliberate final-record adaptation of the common template, not evidence of an unheld meeting.

## 2. Sprint 4 story in plain language

### Week 1 - establish a controlled Sprint

On 27 July, the team and Tutor identified that Sprint 4 needed a clear goal, a reviewable deliverable, professional meeting records and visible repository evidence. The team therefore created the Sprint Goal, assigned accountable owners, established the Client-liaison process and organised the management evidence before detailed technical work continued.

### Week 2 - translate stakeholder direction into accountable work

On 3 August, Matthew instructed the team to develop separate Next.js chat-interface prototypes and learn the foundations of Qdrant while JupyterHub and the server were unavailable. The Tutor added four important controls: confirm target users instead of assuming them, keep the Sprint Goal stable, preserve reviewable research evidence, and communicate unclear requirements professionally.

At the 5 August internal meeting, the team converted that direction into a delivery plan. All members worked on frontend ideas in parallel; the prototypes would then be compared and reduced to one maintained implementation. Qdrant remained a documented research task rather than an unsupported implementation claim. The Client had not explicitly confirmed the target audience, so “people interested in Australian information” remained a labelled working assumption derived from Semester 1 context.

### Week 3 - converge, validate and close

By 10 August, the team had compared the prototypes, selected Yingzhe Xu's design as the shared baseline, consolidated the implementation, connected the real JoeyLLM API through the server-side Next.js boundary, deployed the application, and completed the agreed manual checks with all five members. The team also completed the vector-database literature review and documented the unresolved production choices without claiming that Qdrant or RAG had been implemented.

The Tutor then raised evidence-quality concerns: minutes needed a professional structure, tickets needed clearer closure evidence, user-testing evidence needed to be consolidated, and process improvement needed to be measurable. The team responded on the same day by adopting the canonical template, defining ownership and ticket-quality rules, consolidating the validation record and closing every Sprint 4 action either as completed work or as an explicitly accepted scope limitation.

## 3. Approved authoritative meeting records

| Sequence | Approved record | Role in the evidence chain | Inputs reviewed | Main outputs | Approval |
| --- | --- | --- | --- | --- | --- |
| 1 | [Sprint planning Tutor meeting - 27 July](week-01/tutor-2026-07-27.md) | Established governance, the need for a stable Sprint Goal, Client communication and repository evidence | Semester 1 context and Tutor expectations | Sprint Goal actions, evidence-management actions and initial risks | Approved by Nuo Chen, 27 July 2026 |
| 2 | [Tutor meeting - 3 August](week-02/tutor-minutes-2026-08-03.md) | Reviewed the Week 1 actions and translated Matthew's instruction and Tutor feedback into delivery controls | Goal, repository actions, Client instruction, server unavailability | Target-user clarification, parallel prototypes, Qdrant research and Sprint Review evidence actions | Approved by Nuo Chen, 3 August 2026 |
| 3 | [Internal team meeting - 5 August](week-02/internal-minutes-2026-08-05.md) | Reviewed the Tutor actions and allocated the convergence, validation and research work | Open target-user, prototype, research and review-evidence actions | Prototype comparison, one shared frontend, team validation and research-consolidation actions | Approved by Nuo Chen, 5 August 2026 |
| 4 | [Tutor and Sprint progress review - 10 August](week-03/tutor-minutes-2026-08-10.md) | Verified delivery, recorded Tutor feedback, completed measurable improvements and closed the Sprint evidence | All earlier actions, implementation, deployment, tests, research, risks and documentation | Verified deliverables, accepted limitations, professional documentation rules and final Sprint closure | Approved by Nuo Chen, 10 August 2026 |

## 4. End-to-end evidence chains

Each chain below uses **descriptive name (record ID)** so that readers can understand both the event and its traceable identifier.

### 4.1 Professional minutes and repository governance

The Tutor first stated the **formal meeting-record requirement (S4-FW1-01)** and the **organised repository-evidence requirement (S4-FW1-04)**. The team responded with the **shared repository minutes decision (S4-D01)** and assigned the **organise repository and meeting evidence action (S4-A01)**. The 3 August minutes reviewed that action as completed.

On 10 August, the Tutor identified the more specific **professional minutes requirement (S4-F07)** and **visible communication-evidence requirement (S4-F08)**. The team made the **one canonical minutes template decision (S4-D11)**, completed the **apply the professional template action (S4-A14)** and the **remove unsafe attendance assumptions action (S4-A15)**, and measured the result through the **professional minutes quality improvement (S4-I05)**. The four records listed above are the resulting approved evidence.

**Chain:** Formal meeting-record requirement (S4-FW1-01) → Shared repository minutes decision (S4-D01) → Organise repository and meeting evidence (S4-A01) → Professional minutes requirement (S4-F07) → One canonical template decision (S4-D11) → Apply template and publication controls (S4-A14, S4-A15) → Professional minutes quality improvement completed (S4-I05).

### 4.2 Stable Sprint Goal and reviewable delivery

The Tutor raised the **clear Sprint Goal and reviewable deliverable requirement (S4-FW1-02)**. The team made the **activate Sprint 4 with a presentable goal decision (S4-D02)** and completed the **define and communicate the Sprint Goal action (S4-A02)**. The initial **prepare a reviewable deliverable action (S4-A04)** was refined after Matthew's detailed instruction into the **prepare Sprint Review evidence action (S4-A08)**. The 10 August record closes the product deliverable through the deployed ChatJoey interface and closes the review-evidence package through the Sprint summary, implementation links, validation and research records.

The Tutor also issued the **keep the Sprint Goal stable feedback (S4-F03)**, which became the **stable Sprint Goal decision (S4-D05)**. No later work changed the agreed Goal.

**Chain:** Clear Goal and deliverable requirement (S4-FW1-02) → Active Sprint and presentable Goal decision (S4-D02) → Define Sprint Goal (S4-A02) + Prepare reviewable deliverable (S4-A04) → Keep Goal stable feedback (S4-F03) → Stable Goal decision (S4-D05) → Sprint Review evidence package (S4-A08) → Deployed and evidenced Sprint Goal result.

### 4.3 Target-user clarification and honest scope control

The Tutor raised the **confirm target users before design feedback (S4-F01)** and **avoid unsupported assumptions feedback (S4-F06)**. The team made the **target-user clarification decision (S4-D04)** and assigned the **obtain explicit Client target-user confirmation action (S4-A05)** to Wen Sun.

At the internal meeting, the team confirmed the **working-audience-only decision (S4-D08)**: prior Semester 1 evidence suggested people interested in Australian information, but that description could not be presented as Client-confirmed. On 10 August, the **user-story and persona consistency feedback (S4-F10)** was accepted, while the absent Client confirmation was recorded as the **unconfirmed target-audience limitation (S4-R10)**. The clarification action was therefore closed as an unresolved Sprint limitation, not falsely marked as Client-confirmed.

**Chain:** Confirm target users (S4-F01) + Avoid assumptions (S4-F06) → Target-user clarification decision (S4-D04) → Obtain Client confirmation (S4-A05) → Working-audience-only decision (S4-D08) → User-story consistency feedback (S4-F10) → Unconfirmed target-audience limitation accepted at Sprint close (S4-R10).

### 4.4 Parallel prototypes to one deployed frontend

Matthew's Next.js instruction and the Tutor's **research-before-development workflow feedback (S4-F02)** and **valid offline frontend work feedback (S4-F04)** led to the **continue achievable frontend work decision (S4-D06)** and the **produce comparable member prototypes action (S4-A06)**. All five members contributed frontend work in parallel on separate branches.

The internal meeting then made the **continue parallel work through comparison decision (S4-D07)** and the **select one maintained frontend decision (S4-D09)**. The team completed the **compare prototypes action (S4-A09)** and the **consolidate the selected interface action (S4-A10)**. Yingzhe Xu's interface was selected as the shared baseline, with suitable ideas from the team's parallel work incorporated into the maintained implementation.

**Chain:** Next.js instruction + Research-before-development workflow (S4-F02) + Valid frontend work during server outage (S4-F04) → Continue achievable frontend work (S4-D06) → Produce parallel prototypes (S4-A06) → Compare before convergence (S4-D07) → Select one maintained frontend (S4-D09) → Compare prototypes (S4-A09) → Consolidate shared interface (S4-A10) → [Frontend selection evidence](week-03/Meeting%20record%20about%20front-end%20website.pdf) + [ChatJoey PR #4](https://github.com/joeyllm/ChatJoey/pull/4).

### 4.5 Real API connection, deployment and validation

After the frontend was consolidated, the team connected it to the real JoeyLLM API through a server-side Next.js route and deployed the shared application. The internal meeting's **validate the deployed shared flow action (S4-A11)** required all five members to check live access, message submission, model response, language switching and responsive behaviour.

The Tutor's **task-based user-testing evidence feedback (S4-F11)** led to the **consolidate five-member validation evidence action (S4-A17)** and the **single validation-record improvement (S4-I07)**. All agreed manual checks passed without a reported defect. Automated browser, load, security and forced-failure testing were recorded as the **broader-testing scope limitation (S4-R11)** rather than claimed as completed.

**Chain:** Consolidated frontend (S4-A10) → Validate deployed shared flow (S4-A11) → Task-based testing evidence feedback (S4-F11) → Consolidate five-member validation evidence (S4-A17) → Single validation-record improvement completed (S4-I07) → [System validation record](week-03/system-validation.md) + [Live ChatJoey deployment](https://chat-joey.vercel.app/).

### 4.6 Qdrant learning without an unsupported implementation claim

Matthew requested a basic understanding of Qdrant. The Tutor's **reviewable vector-research evidence feedback (S4-F05)** led to the **document research without backend claims decision (S4-D06)** and the **produce Qdrant research evidence action (S4-A07)**. The internal meeting reaffirmed the boundary through the **research-not-implementation decision (S4-D10)** and the **consolidate vector research and production decisions action (S4-A12)**.

By 10 August, the team had documented embeddings, dense retrieval, similarity search, HNSW, Qdrant collections and payloads, RAG boundaries and evaluation requirements. The work was closed as research. Missing embedding, hosting, dataset, schema and evaluation decisions were recorded as the **production retrieval configuration limitation (S4-R12)**. No Qdrant collection, retrieval pipeline or RAG benchmark was claimed.

**Chain:** Qdrant learning request → Reviewable research evidence feedback (S4-F05) → Research-without-backend-claims decision (S4-D06) → Produce Qdrant evidence (S4-A07) → Research-not-implementation decision (S4-D10) → Consolidate research and unresolved decisions (S4-A12) → [Qdrant basics](https://github.com/joeyllm/ChatJoey/blob/main/docs/qdrant-basics-en.md) + [Vector retrieval literature review](week-03/research/vector-retrieval-literature-review.md) → Production retrieval limitation recorded (S4-R12).

### 4.7 Ticket quality and measurable process improvement

On 10 August, the Tutor raised the **specific and consistent ticket evidence feedback (S4-F09)** and the **measurable reflection requirement (S4-F12)**. The team responded with the **ticket Definition of Done decision (S4-D12)**, requiring a unique outcome title, one accountable owner, acceptance criteria, an evidence link and a closure explanation. The team completed the **define ticket-quality requirements action (S4-A19)** and recorded the result through the **ticket closure quality improvement (S4-I06)**.

The team also made the **same-day Sprint evidence closure decision (S4-D13)**. This closed the professional-minutes improvement (S4-I05), ticket-quality improvement (S4-I06) and validation-record improvement (S4-I07) with observable success measures rather than leaving them as discussion points.

**Chain:** Ticket evidence feedback (S4-F09) + Measurable reflection requirement (S4-F12) → Ticket Definition of Done decision (S4-D12) + Same-day evidence closure decision (S4-D13) → Define ticket-quality requirements (S4-A19) → Professional minutes, ticket quality and validation-record improvements completed (S4-I05-S4-I07).

## 5. Action closure register

This register prevents an action from disappearing between meetings. “Refined into” means that the original action retained its purpose but was made more specific after new stakeholder information became available.

| Named action (ID) | Created in | Reviewed or refined in | Final result and evidence | Final status |
| --- | --- | --- | --- | --- |
| Organise repository and meeting evidence (S4-A01) | 27 July Tutor meeting | 3 August Tutor meeting | Weekly evidence structure and professionalised records | Done |
| Define and communicate Sprint 4 Goal (S4-A02) | 27 July Tutor meeting | 3 August Tutor meeting | [Sprint 4 Goal](../../SPRINT4_GOALS.md) | Done |
| Obtain and circulate Client instruction (S4-A03) | 27 July Tutor meeting | 3 August Tutor meeting | Matthew's 3 August Next.js and Qdrant instruction recorded in the minutes | Done |
| Prepare a reviewable Sprint deliverable (S4-A04) | 27 July Tutor meeting | Refined into Sprint Review evidence (S4-A08) on 3 August | Shared frontend, deployment, Sprint summary, validation and research evidence | Done |
| Obtain explicit target-user confirmation (S4-A05) | 3 August Tutor meeting | 5 August internal meeting and 10 August Tutor review | Client did not explicitly confirm; the limitation is recorded in unconfirmed target-audience risk (S4-R10) | Closed as unresolved Sprint limitation |
| Produce comparable member prototypes (S4-A06) | 3 August Tutor meeting | 5 August internal meeting | [Prototype PR #1](https://github.com/joeyllm/ChatJoey/pull/1), [prototype PR #2](https://github.com/joeyllm/ChatJoey/pull/2) and frontend selection evidence | Done |
| Produce Qdrant research evidence (S4-A07) | 3 August Tutor meeting | Extended by research consolidation (S4-A12) | Qdrant basics, technical discussion and literature review | Done as research |
| Prepare Sprint Review evidence (S4-A08) | 3 August Tutor meeting | 5 and 10 August reviews | Sprint summary, implementation, deployment, validation, risks and research evidence | Done |
| Compare member prototypes (S4-A09) | 5 August internal meeting | 10 August Tutor review | Frontend selection record and decision log | Done |
| Consolidate selected frontend (S4-A10) | 5 August internal meeting | 10 August Tutor review | [ChatJoey PR #4](https://github.com/joeyllm/ChatJoey/pull/4) merged to `main` | Done |
| Validate deployed shared flow (S4-A11) | 5 August internal meeting | 10 August Tutor review | [Five-member system validation](week-03/system-validation.md) | Done |
| Consolidate vector research and unresolved production decisions (S4-A12) | 5 August internal meeting | 10 August Tutor review | [Vector retrieval literature review](week-03/research/vector-retrieval-literature-review.md) and implementation boundary | Done as research |
| Apply professional minutes template (S4-A14) | 10 August Tutor review | Closed in the same record | Canonical template and four standardised minutes | Done |
| Remove unsafe attendance assumptions (S4-A15) | 10 August Tutor review | Closed in the same record | [Publication rules](../templates/README.md) | Done |
| Consolidate five-member validation evidence (S4-A17) | 10 August Tutor review | Closed in the same record | [System validation record](week-03/system-validation.md) | Done |
| Define ticket-quality requirements (S4-A19) | 10 August Tutor review | Closed in the same record | Ticket Definition of Done decision (S4-D12) and template publication gate | Done |

Action identifiers are preserved exactly as used in the authoritative minutes. Unused numbers do not represent unrecorded or missing actions.

## 6. Sprint Checklist evidence matrix

| Checklist dimension | What the Checklist expects | Named evidence chain | Direct evidence | Final status |
| --- | --- | --- | --- | --- |
| Stakeholder Engagement | Regular meetings, clear progress/risks, feedback, response, accountable actions and follow-up | Formal meeting-record requirement (S4-FW1-01); target-user clarification (S4-F01, S4-A05); professional minutes requirement (S4-F07); all feedback responses (S4-F01-S4-F12 and S4-FW1-01-S4-FW1-04) | Four approved minutes in Section 3; action closure register in Section 5 | Covered; target-user confirmation accurately closed as a limitation |
| Planning and Organisation | Goal/work-item alignment, work allocation, owners, deadlines, risks and trackable PBIs | Active Sprint decision (S4-D02); stable Goal decision (S4-D05); actions (S4-A01-S4-A19 where assigned); risks (S4-R01-S4-R12) | [Sprint Goal](../../SPRINT4_GOALS.md), [nine closed Sprint 4 work items](https://github.com/joeyllm/JoeyLLM-Team/issues?q=is%3Aissue%20milestone%3A%22Sprint%204%22%20is%3Aclosed), approved minutes and action closure register | Covered through named owners, exact dates, risks and evidence links |
| Execution and Quality | Version control, review, testing, blocker/scope response and demonstrated impact | Parallel prototype action (S4-A06); frontend selection (S4-A09); consolidation (S4-A10); deployment validation (S4-A11, S4-A17); testing limitation (S4-R11) | [PR #1](https://github.com/joeyllm/ChatJoey/pull/1), [PR #2](https://github.com/joeyllm/ChatJoey/pull/2), [PR #4](https://github.com/joeyllm/ChatJoey/pull/4), [live deployment](https://chat-joey.vercel.app/), [system validation](week-03/system-validation.md) | Implemented, deployed and manually tested within the stated scope |
| Reflection and Improvement | Review outcomes, feedback responses, root cause, measurable process changes and closed improvement actions | Evidence-discipline improvement (S4-I01-S4-I04); professional minutes improvement (S4-I05); ticket-quality improvement (S4-I06); validation-record improvement (S4-I07); same-day closure decision (S4-D13) | [10 August Tutor and Sprint progress review](week-03/tutor-minutes-2026-08-10.md), Sections 5, 8, 9 and 10 | Completed; no separate unheld retrospective is claimed |

Sprint 4 used named owners and exact due dates rather than claiming unrecorded Planning Poker or velocity measurements. Vercel deployment and pull-request evidence are used where applicable; no unsupported CI, automated-test or production-retrieval result is claimed.

The Sprint 4 tracking set contains nine closed issues and no open issue. The link above therefore opens the closed-item view directly instead of relying on GitHub's default open-item view.

## 7. Supporting product and research evidence

| Evidence | Purpose | Evidence status |
| --- | --- | --- |
| [Week 2 weekly report](week-02/report.md) | Pre-meeting progress summary | Supporting report, not minutes |
| [Week 2 detailed Tutor preparation](week-02/tutor-2026-08-03.md) | Questions and evidence prepared before the 3 August meeting | Supporting report, not minutes |
| [Sprint summary](week-03/ChatJoey_Sprint_Summary_English.pdf) | Three-week delivery and scope summary | Supporting PDF |
| [Frontend selection record](week-03/Meeting%20record%20about%20front-end%20website.pdf) | Prototype comparison and selected frontend rationale | Supporting decision evidence |
| [Vector-database discussion](week-03/Vector_Database_Meeting_Minutes_EN.pdf) | Shared technical discussion of vector-database concepts | Supporting research evidence |
| [Vector retrieval literature review](week-03/research/vector-retrieval-literature-review.md) | Literature-based retrieval and evaluation understanding | Research complete; implementation not claimed |
| [System validation](week-03/system-validation.md) | Test scope, results and all five member confirmations | Team-confirmed manual validation |
| [ChatJoey PR #4](https://github.com/joeyllm/ChatJoey/pull/4) | Consolidated frontend, API integration and implementation review | Merged implementation evidence |
| [Live ChatJoey](https://chat-joey.vercel.app/) | Reviewable deployed system | Deployed and manually tested |
| [Current implementation state](https://github.com/joeyllm/ChatJoey/blob/main/docs/CURRENT_STATE.md) | Implemented and excluded functionality | Scope boundary evidence |

## 8. Evidence authority and status rules

- The approved Markdown minutes are the authoritative records for meetings, feedback, decisions, actions, risks and improvements.
- Product code, technical decisions, pull requests and implementation issues remain in `ChatJoey` and are linked from the minutes and this README.
- PDFs, reports and research notes support the authoritative minutes; they do not create additional meetings.
- `Done`, `Tested`, `Deployed` and `Client-confirmed` are different evidence states. A stronger state is never inferred from a weaker one.
- Client-provided model architecture remains outside team ownership. Sprint 4 does not claim model fine-tuning, post-training, production Qdrant/RAG integration or unauthorised backend experiments.
- Sprint 4 has no open action in this evidence set. The unconfirmed target audience, broader automated testing and production retrieval configuration are recorded as accepted scope limitations rather than hidden or misreported as completed work.
