# Client Instruction Review and Team Planning Minutes (V2)

## 1. Meeting Information

| Field | Details |
| --- | --- |
| Project | Southern-cross AI / JoeyLLM |
| Meeting type | Asynchronous client-instruction review and internal team planning record |
| Sprint / week | Sprint 5 / Week 1; Semester 2 Week 4 |
| Date | 17 August 2026 |
| Time | Asynchronous review on 17 August 2026; this record does not represent a synchronous meeting with a start and end time |
| Location / channel | Local review of the client email; this record does not claim that an online meeting has taken place |
| Chair / instruction source | Matty, author of the client instruction email |
| Minute taker | Chen Nuo |
| Attendance | Chen Nuo completed the document review; no claim is made that other members attended a synchronous meeting |
| Apologies / absences | Not applicable to an asynchronous instruction review |
| Meeting objective | Convert the client's requirements for this week into three GitHub Issues, fifteen verifiable Action Items, and the associated security, branch, and scope controls |
| Related Sprint Goal / milestone | Sprint 5 Goal: Enhance ChatJoey’s cross-platform responsiveness, interaction consistency, and usability across representative phone, tablet, and desktop environments, while complying with the client’s local-only development, no-deployment, and protected-branch constraints. Validate the core chat workflows through systematic functional, compatibility, accessibility, and regression testing, and deliver multiple isolated, independently reviewable UI Modes with distinct visual and interaction styles based on the existing Mode architecture, supported by traceable local test evidence for subsequent client review and integration. |
| Local file location | `D:\COMP8715\semester2\week 4\client-instruction-review-minutes-2026-08-17-v2-en.md` |
| Approved repository location | `management/weekly-reports-END/sprint-05/week-04/client-instruction-review-minutes-2026-08-17.md` in JoeyLLM-Team; this management record is not part of the ChatJoey interface repository |

### Record Boundary

This document records the client's written instructions and the team's planning response. It does not claim that the Teams or Discord catch-up mentioned in the email has already taken place. The client's telephone number is excluded. The three GitHub Issues are the team's organisational structure for this week's development work; until the client lifts the local-only restriction, they remain local task definitions and do not imply that online Issues have already been created or published.

## 2. Agenda

1. Review the relationship between the Sprint 4 deliverables and the new publication-security boundary.
2. Extract and confirm the material requirements in the client email dated 17 August 2026.
3. Record team-proposed improvements for security, mobile readiness, QA, personality isolation, and review evidence.
4. Establish ten decisions defining how the client requirements and team improvements will be implemented together.
5. Restructure the development work into three GitHub Issues and fifteen Action Items.
6. Define the Vercel shutdown, local-only freeze, client catch-up, and vector-work freeze as operational controls.
7. Define the evidence, clarification questions, and Sprint Checklist traceability required for the next meeting.

## 3. Review of Previous Actions

| Previous ID | Action / deliverable | Original owner | Original due date | Current status | Completion evidence | Current impact / follow-up |
| --- | --- | --- | --- | --- | --- | --- |
| S4-A10 | Integrate the selected shared interface | Yingzhe Xu | 10 August 2026 | Completed in Sprint 4 | Shared ChatJoey implementation on `main` and the Sprint 4 evidence set | Serves as the local baseline for this week's mobile implementation; no merge is authorised this week |
| S4-A11 | Validate the deployed shared workflow with all members | Chen Nuo | 10 August 2026 | Completed in Sprint 4; the previous publication method has been superseded by the new instruction | Sprint 4 system-validation record | The old Vercel deployment must be shut down and all new validation must be local; see the common execution constraints in Section 8 |
| S4-A12 | Consolidate Qdrant/vector research and unresolved production decisions | Chen Nuo | 10 August 2026 | Research completed; further work deferred | Sprint 4 literature review and technical notes | Vector work is paused until next week and must not enter ChatJoey; it remains a scope control rather than a development Issue |
| S4-A17 | Consolidate validation evidence from all five members | Chen Nuo | 10 August 2026 | Completed within the Sprint 4 test scope | Sprint 4 system-validation record | The client considers the interface not yet mobile-ready; Issue 2 (S5-A06 to S5-A10) creates a new mobile QA evidence chain |

## 4. Current Progress and Evidence Presented

| PBI / work item | Progress since the previous meeting | Verified status | Evidence presented | User / stakeholder impact | Current gap |
| --- | --- | --- | --- | --- | --- |
| S5-PBI01 Client security instruction | The client email has been translated into local-only, no-deploy, no-merge, and repository-scope controls | Client instruction confirmed; execution status still to be verified | Locally retained, redacted summary of the 17 August 2026 client email | Reduces the risk of further public exposure | Vercel shutdown and public endpoint status have not yet been verified |
| S5-PBI02 Issue 1: Mobile-first responsive implementation | Five subtasks have been defined for the navigation drawer, Header, viewport/composer, overflow, and multi-breakpoint behaviour | Planned | S5-A01 to S5-A05 | Makes the core chat interface usable and consistent on phones, tablets, and desktop | No claim is made that the implementation is complete |
| S5-PBI03 Issue 2: Mobile QA and accessibility validation | Target viewports, keyboard/focus behaviour, Mode/chat regression, and final review evidence have been defined | Planned | S5-A06 to S5-A10 | Converts “mobile-ready” into reproducible and reviewable quality evidence | The new test matrix has not yet been executed |
| S5-PBI04 Issue 3: Five Joey personalities | Five isolated Personalities, folders, branches, and a shared implementation contract have been defined | Planned | S5-A11 to S5-A15 | Provides five independently reviewable experiences without destabilising the core Next.js application | Four remaining members still need to be assigned to the other four Personalities |
| S5-PBI05 Vector workstream | Qdrant/vector work is formally paused for this week and excluded from ChatJoey | Client-confirmed deferral | S5-CR10, S5-D10, and the common execution constraints in Section 8 | Prevents scope creep during the interface-focused week | Awaiting client infrastructure direction next week |

## 5. Client Requirements, Discussion, and Team Response

| Requirement ID | Source / topic | Client requirement or concern | Team response and rationale | Outcome | Linked Improvement / Decision / Action or control |
| --- | --- | --- | --- | --- | --- |
| S5-CR01 | Client email / public exposure | Keep all work local today and shut down the Vercel site created last week | Accepted. The team treats this as incident containment, not merely a preference to stop new deployments | Publication-containment control takes immediate effect | S5-I01, S5-D01, and Section 8 common execution constraints |
| S5-CR02 | Client email / protected branches | Do not deploy online and do not push or merge into `main`, `live`, or `beta` | Accepted. All implementation remains on isolated local branches until the client clarifies the later review method | Local-only change freeze adopted | S5-I02, S5-D02, and Section 8 common execution constraints |
| S5-CR03 | Client email / catch-up | Meet through Teams or Discord after 13:00 and provide at least one hour's notice | Accepted. The meeting will be used to obtain security, delivery, and review decisions rather than only report status | Managed as a meeting action, not a development Issue | S5-I03, S5-D03, and Section 10 |
| S5-CR04 | Client email / local development | No API key will be provided this week; everyone must work in local development mode | Accepted. All implementation and QA will use mock/local mode, and final checks must detect secrets or real API dependencies | Included in the common constraints and final QA | S5-I04, S5-D04, S5-A10, and Section 8 common execution constraints |
| S5-CR05 | Client email / mobile first | The first priority is to support phones, larger mobile devices, tablets, and desktop | Accepted. A shared responsive implementation stream will be completed before Personality work begins | Issue 1 established and validated through Issue 2 | S5-I05, S5-D05, S5-A01 to S5-A10 |
| S5-CR06 | Client email / mobile quality | The current interface is not properly mobile-ready | Accepted. Mobile readiness is defined as passing layout, viewport, overflow, interaction, keyboard, and regression checks | Independent QA and accessibility stream established | S5-I06, S5-D06, S5-A06 to S5-A10 |
| S5-CR07 | Client email / branches only | Use separate branches; the team must not merge; the client will review, test, and merge | Accepted. Mobile work uses an isolated branch and each Personality uses its own local branch; the team will not merge | Review-safe branch governance adopted | S5-I07, S5-D07, the branch fields in Section 8, and the common execution constraints |
| S5-CR08 | Client email / Joey personalities | Use the existing modes template, place one Personality on each branch, and avoid unnecessary changes to the main Next.js application | Accepted. The team will produce five configuration-driven and folder-isolated Personalities | Issue 3 established | S5-I08, S5-D08, S5-A11 to S5-A15 |
| S5-CR09 | Client email / repository and AI-tool discipline | Keep ChatJoey interface-only, update the branch README, and maintain `AGENTS.md` where required when using AI tools | Accepted. Every branch requires a concise review package, and final QA will audit diff scope | Added to every branch and the S5-A10 acceptance criteria | S5-I09, S5-D09, S5-A10, and Section 8 common execution constraints |
| S5-CR10 | Client email / vector database | Pause vector-database work until next week and do not add that work or documentation to ChatJoey | Accepted. No related development Issue will be created this week, and research materials will remain outside ChatJoey | Retained as an explicit scope freeze | S5-I10, S5-D10, and Section 8 common execution constraints |

## 6. Decisions and Rationale

| Decision ID | Final decision | Rationale / evidence considered | Confirming body | Affected PBI / document | Effective date |
| --- | --- | --- | --- | --- | --- |
| S5-D01 | Shut down the old Vercel deployment, verify the known public endpoints, and retain verification evidence locally | The client reported that previously public materials may have been copied externally; stopping new deployment alone does not contain the existing risk | Southern-cross AI planning response to S5-CR01 | S5-PBI01 and Sections 7, 8, and 10 | 17 August 2026 |
| S5-D02 | Freeze deployment, remote push, and merges into `main`, `live`, and `beta`; retain all branches locally this week | This satisfies both the client's branches-only instruction and the prohibition on online publication | Southern-cross AI planning response to S5-CR02 | All three Issues and Section 8 common execution constraints | 17 August 2026 |
| S5-D03 | Treat the client catch-up as a decision meeting, provide at least one hour's notice, and record conclusions on branch delivery, Vercel, devices, and Personality review | These decisions are necessary before the team can safely hand over local work | Southern-cross AI planning response to S5-CR03 | Section 10 | 17 August 2026 |
| S5-D04 | Conduct all development and testing in local/mock mode without an API key, real API requests, or committed secrets | The client is not providing an API key, but the interface must remain runnable and testable | Southern-cross AI planning response to S5-CR04 | S5-A01 to S5-A15, with final verification in S5-A10 | 17 August 2026 |
| S5-D05 | Establish one mobile implementation stream containing five independently acceptable subtasks: drawer, Header, viewport/composer, overflow, and tablet/desktop behaviour | This is more maintainable and traceable than unrelated device-specific patches | Southern-cross AI planning response to S5-CR05 | Issue 1: S5-A01 to S5-A05 | 17 August 2026 |
| S5-D06 | Establish an independent QA stream that verifies mobile readiness through defined viewports, keyboard/focus behaviour, chat/Mode regression, and engineering checks | This converts the subjective phrase “mobile-ready” into reproducible evidence | Southern-cross AI planning response to S5-CR06 | Issue 2: S5-A06 to S5-A10 | 17 August 2026 |
| S5-D07 | Limit each local branch to one clear concern; the team will not merge, and the client retains review, test, and merge authority | This reduces review ambiguity and the risk of changing protected branches | Southern-cross AI planning response to S5-CR07 | Section 8 branch design and common execution constraints | 17 August 2026 |
| S5-D08 | Create Outback, Coastal, Study, Sports, and Eco Joey; assign one member to each isolated folder and local branch | This supports parallel work while satisfying the one-Personality-per-member rule | Southern-cross AI planning response to S5-CR08 | Issue 3: S5-A11 to S5-A15 | 17 August 2026 |
| S5-D09 | Update the root README on every branch with purpose, changes, local run steps, tests, limitations, and AI contribution; update `AGENTS.md` where required and add no unrelated documents | This enables the client to reproduce, understand, and safely review each branch | Southern-cross AI planning response to S5-CR09 | All Issues, with final verification in S5-A10 | 17 August 2026 |
| S5-D10 | Do not implement or publish any vector/Qdrant work this week and retain no such documentation in ChatJoey | The client explicitly deferred the relevant infrastructure work until next week | Southern-cross AI planning response to S5-CR10 | S5-PBI05 and Section 8 common execution constraints | 17 August 2026 |

## 7. Risks, Blockers, Deferrals, and Scope Changes

| ID | Risk / blocker / change | Impact on Sprint Goal | Current mitigation | Accountable owner | Required clarification / decision | Due / review date | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S5-R01 | Previously public Joey Chat material may have been copied externally | Further publication could increase competitive and reputational risk | Apply Vercel shutdown, local-only, and no-deploy controls | To be assigned | Verify Vercel shutdown and known public endpoints | 17 August 2026 | Open |
| S5-R02 | The client requires branch review while also prohibiting online publication | An unclear handover method could cause an accidental push or prevent review | Keep S5-A01 to S5-A15 on local branches and clarify the later transfer method in the client meeting | To be assigned | How will the client receive the local branches? | 17 August 2026 | Open |
| S5-R03 | The team has not confirmed who has Vercel shutdown permission | The public site may remain accessible | Confirm the authorised person internally without exposing credentials in the minutes | To be assigned | Who will shut down and verify the old deployment? | 17 August 2026 | Open |
| S5-R04 | No API key or real API access is available | Model connectivity cannot be validated this week | Use mock/local mode for all Actions; S5-A10 checks secrets and network dependencies | QA team (accountable name to be added) | No escalation unless the client changes scope | 21 August 2026 | Monitoring |
| S5-R05 | Drawer, viewport, and overflow fixes may affect one another across breakpoints | One viewport may pass while another layout regresses | S5-A01 to S5-A05 use shared responsive rules; S5-A06 to S5-A10 validate independently | Mobile team and QA team (accountable names to be added) | Does the client have a priority physical device? | 21 August 2026 | Monitoring |
| S5-R06 | A visual-only accessibility review may miss focus traps or focusable hidden controls | The mobile UI may appear correct but remain unusable with keyboards or assistive technology | S5-A08 defines explicit keyboard and focus acceptance criteria | QA team (accountable name to be added) | None | 21 August 2026 | Monitoring |
| S5-R07 | Four Personality owner names remain unassigned | Duplicate work or an unowned Personality may result | Complete the one-to-one allocation before S5-A12 to S5-A15 begin | Chen Nuo (coordination; remaining owners to be added) | Confirm the mapping of the other four members to the four remaining Personalities | 17 August 2026 | Open |
| S5-R08 | Personality branches may modify core `app/page.tsx` or another member's Mode | Integration conflict and review risk would increase | S5-A11 to S5-A15 follow the common Personality contract and isolated folder boundary | Five Personality owners (four names still to be added) | None | 21 August 2026 | Monitoring |
| S5-R09 | README, AI-contribution, or diff-scope evidence may be insufficient | The client may be unable to understand the changes or may find unrelated files | Every branch updates README; S5-A10 performs final scope, secret, and AI-contribution checks | QA team (accountable name to be added) | Does actual AI contribution require an `AGENTS.md` update? | 21 August 2026 | Monitoring |
| S5-R10 | Vector infrastructure decisions have been deferred | Retrieval work cannot continue this week | Exclude vector work from the three Issues and ChatJoey pending next week's client direction | To be assigned | Client infrastructure direction is required next week | 21 August 2026 | Deferred |

## 8. New Action Items

### Issue 1: Mobile-first responsive implementation

| Action ID | GitHub Issue / subtask | Accountable owner | Local branch | Primary deliverable | Due date | Acceptance criteria | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S5-A01 | Issue 1 / Implement the mobile navigation drawer | Chen Nuo | `codex/mobile-drawer-responsive` | Keep the mobile sidebar closed by default; add a menu button, overlay drawer, and backdrop; support backdrop and Escape closing; close after Joey Mode selection; prevent the sidebar from permanently consuming mobile chat width | 21 August 2026 | At phone widths, the drawer opens through the menu and closes through the backdrop, Escape, or Mode selection; after closing, the full chat width is usable | Open |
| S5-A02 | Issue 1 / Optimise the mobile Header and status display |Yingzhe Xu | `codex/mobile-drawer-responsive` | Simplify the mobile Header; preserve Joey branding; display compact Ready, Thinking, Demo, and Error states; align menu, brand, and status; provide primary touch targets of approximately 44px or more | 21 August 2026 | All four states remain identifiable without overflow; menu, brand, and status align correctly; primary touch targets are approximately 44px or larger | Open |
| S5-A03 | Issue 1 / Fix the chat viewport and composer | Yingzhe Xu | `codex/mobile-drawer-responsive` | Use `100dvh`; make the conversation area independently scrollable; keep the composer at the dynamic viewport bottom; support iPhone safe areas; handle mobile landscape and the software keyboard | 21 August 2026 | At target portrait and landscape phone sizes, messages scroll independently and the composer is not permanently hidden by browser chrome, safe areas, or the software keyboard | Open |
| S5-A04 | Issue 1 / Fix narrow-screen content overflow | Xingyu Li| `codex/mobile-drawer-responsive` | Prevent mascot and speech-bubble overflow; constrain message widths; handle long URLs and unbroken strings; give code blocks and Markdown tables local horizontal scrolling | 21 August 2026 | The page has no unintended horizontal scrolling; long text, URLs, code blocks, and tables remain readable, with local scrolling only where required | Open |
| S5-A05 | Issue 1 / Preserve tablet and desktop responsive behaviour |  Xingyu Li | `codex/mobile-drawer-responsive` | Define phone, tablet, and desktop breakpoints; validate the 768px boundary; preserve desktop sidebar collapse, resize, Mode tooltips, and desktop layout | 21 August 2026 | Behaviour is correct on both sides of 768px; desktop sidebar collapse/resize and Mode tooltips do not regress; tablet and desktop have no page overflow | Open |

### Issue 2: Mobile QA and accessibility validation

| Action ID | GitHub Issue / subtask | Accountable owner | Local branch | Primary deliverable | Due date | Acceptance criteria | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S5-A06 | Issue 2 / Test phone portrait layouts | Chen Nuo | Same as the corresponding mobile implementation branch | Test 320×568, 375×667, 390×844, and 430×932; cover the drawer, composer, overflow, and Mode selection | 21 August 2026 | At all four portrait phone sizes, a user can open navigation, select a Mode, type, send, and read a response in a complete chat flow | Open |
| S5-A07 | Issue 2 / Test phone landscape and tablet layouts | Xiang Chang | Same as the corresponding mobile implementation branch | Test 667×375, 844×390, 768×1024, and 1024×768; cover breakpoints, sidebar behaviour, and page overflow | 21 August 2026 | Both landscape phone and both tablet sizes render correctly, breakpoint behaviour is consistent, core controls work, and the page has no unintended overflow | Open |
| S5-A08 | Issue 2 / Validate keyboard and focus behaviour | Xiang Chang | Same as the corresponding mobile implementation branch | Verify that Tab reaches the menu; Enter/Space opens the drawer; Escape closes it; focus returns after closing; hidden drawer controls cannot receive focus | 21 August 2026 | The drawer is fully keyboard operable; focus order is predictable; focus returns to the trigger after closing; hidden content is absent from the focus order | Open |
| S5-A09 | Issue 2 / Test chat and Joey Mode interactions | Wen Sun  | Same as the corresponding mobile implementation branch | Test New Chat, Little/Evil/Sydney Joey switching, Enter/Shift+Enter, mock/thinking/error states, long messages, and Markdown | 21 August 2026 | Core chat and existing Mode functions do not regress on target devices; every failure has reproducible steps and local evidence | Open |
| S5-A10 | Issue 2 / Run final checks and prepare review evidence | Wen Sun  | Same as the corresponding mobile implementation branch | Run ESLint and TypeScript; inspect the console, Git diff, secrets, and unrelated files; update README with changes, tests, limitations, and AI-tool contribution | 21 August 2026 | ESLint and TypeScript pass; no unexplained console error exists; the diff contains no secrets or unrelated files; README enables local reproduction and client review | Open |

### Issue 3: Five Joey personalities

| Action ID | GitHub Issue / subtask | Accountable owner | Local branch | Primary deliverable | Due date | Acceptance criteria | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S5-A11 | Issue 3 / Member 1: Outback Joey | Chen Nuo | `chen-nuo/outback-joey` | Create a calm, practical Personality with restrained Australian humour in `modes/outback-joey/`, using outback, desert, and sunset colours | 21 August 2026 | Meets the common Personality acceptance criteria below and can be selected and demonstrated independently in local mock mode | Open |
| S5-A12 | Issue 3 / Member 2: Coastal Joey | Xiang Chang | `<member-2>/coastal-joey` | Create a relaxed, friendly Personality for everyday conversation in `modes/coastal-joey/`, using ocean, beach, and light-blue styling | 21 August 2026 | Meets the common Personality acceptance criteria below and can be selected and demonstrated independently in local mock mode | Open |
| S5-A13 | Issue 3 / Member 3: Study Joey | Yingzhe Xu | `<member-3>/study-joey` | Create a patient, clear Personality that explains tasks step by step in `modes/study-joey/`, using soft blue-purple and study elements | 21 August 2026 | Meets the common Personality acceptance criteria below and can be selected and demonstrated independently in local mock mode | Open |
| S5-A14 | Issue 3 / Member 4: Sports Joey | Xingyu Li | `<member-4>/sports-joey` | Create an energetic and encouraging teamwork-oriented Personality in `modes/sports-joey/`, using a green-and-gold sports theme | 21 August 2026 | Meets the common Personality acceptance criteria below and can be selected and demonstrated independently in local mock mode | Open |
| S5-A15 | Issue 3 / Member 5: Eco Joey | Wen Sun | `<member-5>/eco-joey` | Create a calm, environmentally focused Personality in `modes/eco-joey/`, using forest-green and earth-tone styling | 21 August 2026 | Meets the common Personality acceptance criteria below and can be selected and demonstrated independently in local mock mode | Open |

#### Common Issue 3 Personality Acceptance Criteria

- Each of the five members owns one Personality, with no duplication or omission.
- Each Personality uses its own folder and isolated local branch.
- Each is created from `modes/template/` and defines an independent `name`, `description`, `prompt`, `theme`, and SVG icon.
- The Little Joey mascot may be reused, but the visual and conversational style must remain distinguishable.
- Each is registered in `modes/index.ts` and validated in local mock mode.
- No member modifies `app/page.tsx`, an API, or another member's Mode.
- ESLint and TypeScript checks pass.

#### Common Execution Constraints

- Mobile work (Issues 1 and 2) takes priority over Personality work (Issue 3).
- No API key is used; development and validation use local mock/development mode.
- Nothing is deployed to Vercel or another online platform; the old Vercel deployment is shut down and its verification is retained locally.
- Nothing is pushed or merged into `main`, `live`, or `beta`, and work branches are not published online.
- All implementation remains on isolated local branches; the client retains final review, test, and merge authority.
- No Qdrant, RAG, research notes, meeting records, or unrelated technical documentation is added to ChatJoey; vector work is paused this week.
- Every branch updates the root README with purpose, changes, local run steps, tests, limitations, and AI contribution.
- When AI tools are actually used, `AGENTS.md` is maintained in accordance with the existing instructions.
- Vercel shutdown, the local-only change freeze, client catch-up, and vector-work freeze are operational controls, meeting actions, or scope constraints, not additional GitHub development Issues.
- All S5-A01 to S5-A15 Action Items are due on 21 August 2026 and begin with Open status.

## 9. Continuous Improvement

| Improvement ID | Observed problem and evidence | Possible root cause | Improvement / process change | Accountable owner | Success criterion | Review date | Linked Issue / Action / control |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S5-I01 | Previously deployed material was publicly accessible and may have been copied externally | Publication lacked a sufficient containment and approval gate | Add old-deployment shutdown, endpoint verification, and local-only incident evidence | To be assigned | No known production endpoint serves the application, and local verification is retained | 17 August 2026 | Section 8 common execution constraints / Open |
| S5-I02 | “Use branches” could be misread as permission to push public remote branches | Branch review and publication boundaries were unclear | Separate local development from remote delivery and prohibit remote writes until the client gives explicit permission | To be assigned | All three Issues remain on local branches and protected branches remain unchanged | 21 August 2026 | Section 8 common execution constraints / Open |
| S5-I03 | A status-only catch-up would not resolve delivery and security ambiguity | The meeting lacks explicit required decisions | Use a decision agenda and record conclusions on publication, delivery, devices, and Personality review | To be assigned | Every key clarification becomes a decision or a clearly recorded open question | 17 August 2026 | Section 10 / Open |
| S5-I04 | Previous interface validation may have relied on real integration | No formal offline-safe UI boundary existed | Use mock/local mode for all development and QA, and include no-secret/no-real-network checks in final validation | QA team (accountable name to be added) | The interface can be demonstrated without an API key or real request, and the diff contains no secret | 21 August 2026 | All Actions, especially S5-A10 / Open |
| S5-I05 | Independent device patches could produce inconsistent responsive behaviour | Shared mobile-first design rules were missing | Put navigation, Header, viewport, overflow, and desktop preservation into one implementation stream | Mobile team (accountable name to be added) | All five implementation subtasks pass the Issue 2 device matrix | 21 August 2026 | Issue 1: S5-A01 to S5-A05 / Open |
| S5-I06 | “Mobile-ready” is too subjective | Reproducible task, viewport, and accessibility evidence was missing | Establish five QA layers: phone portrait, landscape/tablet, keyboard/focus, chat/Mode regression, and engineering checks | QA team (accountable name to be added) | Every QA item has a result and every failure has reproducible steps | 21 August 2026 | Issue 2: S5-A06 to S5-A10 / Open |
| S5-I07 | Parallel branches can overlap in scope or affect protected branches | Branch purpose and merge authority were not sufficiently explicit | Use one concern per branch, local-only work, descriptive branch names, and client-only merge authority | To be assigned | Each branch has one review purpose and `main`, `live`, and `beta` remain unchanged | 21 August 2026 | Section 8 branch fields and common execution constraints / Open |
| S5-I08 | Personality experiments could spread into the core application | A shared Mode contract and owner isolation were missing | Give each of five members an isolated folder and branch and build a configuration-driven Personality from the template | Five Personality owners (four names still to be added) | Five Personalities can be selected, distinguished, and reviewed independently without unrelated core changes | 21 August 2026 | Issue 3: S5-A11 to S5-A15 / Open |
| S5-I09 | The client may be unable to infer modifications, testing, or AI contribution from code diff alone | Standard branch handover evidence was missing | Update the root README on every branch, update `AGENTS.md` where necessary, and audit scope and secrets during final checks | QA team (accountable name to be added) | The client can reproduce locally from README; AI contribution is visible; no unrelated files are present | 21 August 2026 | All branches, especially S5-A10 / Open |
| S5-I10 | Simply pausing vector work could allow scope to recur or documentation to enter the wrong repository | Deferral was not expressed as an explicit control | Exclude vector/Qdrant work entirely from the three Issues and ChatJoey pending next week's client instruction | To be assigned | ChatJoey has zero vector/Qdrant diff this week | 21 August 2026 | Section 8 common execution constraints / Deferred |

## 10. Preparation for the Next Meeting

| Field | Details |
| --- | --- |
| Known date / time | 17 August 2026 after 13:00 AEST; exact time awaits team confirmation and must be communicated to the client at least one hour in advance |
| Meeting type | Teams or Discord client catch-up |
| Purpose | Confirm Vercel shutdown, the local-only boundary, local branch handover, target-device priority, expectations for reviewing five Personalities, and evidence format |
| Workstream and owner structure | One mobile implementation stream (S5-A01 to S5-A05, with Chen Nuo accountable for S5-A01), one QA stream (S5-A06 to S5-A10, with Chen Nuo accountable for S5-A06), and five Personality owners (S5-A11 to S5-A15, with Chen Nuo accountable for S5-A11); remaining names must still be assigned |
| Pre-meeting operational actions | Confirm the Vercel shutdown owner and status; maintain the local-only freeze; choose a meeting time and notify the client at least one hour in advance |
| Evidence to present | Local responsive-implementation status, QA matrix, five-Personality branch plan, README template, and Vercel shutdown status; no new online deployment may be shown |
| Required decisions / clarifications | How the client will receive local branches; who verifies Vercel shutdown; priority physical devices; whether all five Personalities enter review; the expected `AGENTS.md` detail for AI contributions |
| Presenter(s) | Mobile team, QA team, five Personality owners, and the representative responsible for operational controls; remaining names to be assigned |
| Pre-read material | Redacted client-email summary, three Issues / fifteen Actions, local risk record, and decision questions; no client telephone number |

### Proposed Agenda for the Next Meeting

1. Security and publication controls: confirm that the old Vercel deployment is shut down and that no new online publication exists.
2. Local handover: define how the client will receive and review isolated local branches.
3. Issue 1 — Mobile implementation: present the implementation status and material changes for S5-A01 to S5-A05.
4. Issue 2 — Mobile QA: present target viewports, keyboard/focus, chat/Mode regression, and engineering-check evidence.
5. Issue 3 — Five Joey personalities: confirm five owners, five folders/branches, and the common acceptance criteria.
6. Next steps: record client decisions, remaining risks, owners, and the review-handover method.

## 11. Meeting Close and Approval

| Check | Result |
| --- | --- |
| Development Actions open at close | 15: S5-A01 to S5-A15 across three Issues |
| Operational controls / meeting actions | Vercel shutdown, local-only change freeze, client catch-up with at least one hour's notice, and vector-work freeze |
| Decisions recorded | 10: S5-D01 to S5-D10 |
| Feedback awaiting response | Local branch handover method, Vercel shutdown owner, priority devices, and review scope for the five Personalities |
| Risks requiring escalation | S5-R01, S5-R02, S5-R03, and S5-R07 |
| Minutes drafted by / date | Chen Nuo, 17 August 2026 |
| Minutes review status | English V2 approved by Chen Nuo for publication in the JoeyLLM-Team management repository; remaining owner allocations are explicitly recorded as open and are not represented as complete |
| Distribution | Southern-cross AI through `management/weekly-reports-END/sprint-05/week-04/`; this record is not added to the ChatJoey interface repository |
| GitHub document link | [Sprint 5 / Week 4 client instruction review minutes](https://github.com/joeyllm/JoeyLLM-Team/blob/main/management/weekly-reports-END/sprint-05/week-04/client-instruction-review-minutes-2026-08-17.md) |

## 12. Sprint Checklist Traceability

| Checklist dimension | Evidence provided by these minutes | Direct IDs / location |
| --- | --- | --- |
| Stakeholder Engagement | Ten client requirements, ten decisions, the one-hour client notification requirement, clarification questions, and a structured Agenda | S5-CR01 to S5-CR10, S5-D01 to S5-D10, and Sections 5, 6, and 10 |
| Planning and Organisation | Explicit Sprint Goal, continuity from previous Actions, three Issues, fifteen Actions, consistent due dates, branch and owner roles, risks, and operational controls | S5-A01 to S5-A15, S5-R01 to S5-R10, and Sections 1, 3, 7, and 8 |
| Execution and Quality | Issue 1 defines five mobile implementation tasks; Issue 2 defines viewport, accessibility, regression, and engineering validation; Issue 3 defines five isolated Personalities and a common contract | S5-A01 to S5-A15 and Sections 4 and 8 |
| Reflection and Improvement | Ten process improvements are derived from public exposure, subjective mobile readiness, branch overlap, Personality scope, and review evidence, and linked to the correct Issue, Action, or control | S5-I01 to S5-I10 and Section 9 |
| Evidence Traceability | A continuous chain from Requirement to Decision to Issue/Action or operational control, then to acceptance criteria and next-meeting evidence | Sections 5, 6, 8, 9, 10, and 12 |

## Local Draft Quality Check

- [x] The client email is accurately treated as an asynchronous written instruction; no unheld synchronous meeting is claimed.
- [x] Section 8 contains three GitHub Issues, each with exactly five Action Items.
- [x] Action IDs run continuously from S5-A01 to S5-A15 with no duplicate or missing ID.
- [x] Issue 1 maps to S5-A01 to S5-A05; Issue 2 maps to S5-A06 to S5-A10; Issue 3 maps to S5-A11 to S5-A15.
- [x] S5-A01, S5-A06, and S5-A11 identify Chen Nuo as the accountable owner.
- [x] Five Personalities are reserved for five members and use five isolated folders and local branches; the other four member names remain explicit placeholders.
- [x] Every Action is due on 21 August 2026 and has Open status.
- [x] Vercel shutdown, the local-only freeze, client catch-up, and vector freeze remain operational controls, meeting actions, or scope constraints rather than incorrectly defined development Issues.
- [x] Sections 7, 9, 10, 11, and 12 are synchronised with the three-Issue, fifteen-Action structure.
- [x] The client's telephone number is excluded, and the record does not claim that code has been deployed, pushed, merged, or completed.
- [ ] Accountable owner names for S5-A02 to S5-A05 and S5-A07 to S5-A10 still need to be assigned.
- [ ] Four remaining team members must be assigned one-to-one to Coastal, Study, Sports, and Eco Joey, and their branch placeholders must be replaced with actual prefixes.
- [ ] The owners of Vercel shutdown, client-meeting notification, and vector-work scope control must be confirmed.
- [ ] The exact client catch-up time, meeting outcomes, and client decisions must be added after the meeting.
- [x] Chen Nuo authorised publication of this English management record in the JoeyLLM-Team Sprint 5 / Week 4 directory; this does not authorise publication of ChatJoey implementation branches.

