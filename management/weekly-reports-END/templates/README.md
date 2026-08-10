# Meeting Minutes Templates

This folder contains the shared professional meeting-minutes template and weekly report template for Southern-cross AI / JoeyLLM-Team.

## Templates

| Purpose | Template |
| --- | --- |
| Tutor, client, Sprint Review, retrospective, and formal internal meeting minutes | `professional-meeting-minutes-template.md` |
| Weekly report | `Weeklyreporttemplate.md` |

## Publication rules

- Use `professional-meeting-minutes-template.md` for every assessed or formal meeting.
- Use English and remove every instructional comment and placeholder before publication.
- List only attendees confirmed by the meeting notes, recording, calendar, or participants. Never assume attendance.
- Keep unconfirmed attendance or facts marked `To be confirmed` and keep the document in Draft status.
- Use one accountable owner per action. Other team members may be listed as contributors.
- Use exact dates, direct evidence links, and the status vocabulary defined by the template.
- `Done`, `Tested`, `Deployed`, and `Client-confirmed` require evidence appropriate to that status.
- Minutes are Approved only after Nuo Chen, the nominated reviewer, has checked names, dates, links, decisions, actions, and evidence status.

## File naming

| Record | Filename |
| --- | --- |
| Tutor meeting minutes | `tutor-minutes-YYYY-MM-DD.md` |
| Client meeting minutes | `client-minutes-YYYY-MM-DD.md` |
| Formal internal meeting | `internal-minutes-YYYY-MM-DD.md` |
| Sprint retrospective | `internal-retrospective-YYYY-MM-DD.md` |
| Weekly report | `report.md` |

Legacy filenames remain in their existing week folders so that historical links do not break. Each week README identifies the authoritative meeting record.

## AI prompt

```text
Please generate formal English meeting minutes for Southern-cross AI / JoeyLLM-Team.

Read and follow:
management/weekly-reports-END/templates/professional-meeting-minutes-template.md

Rules:
- Do not invent attendance, work, decisions, evidence, test results, deployment status, or client confirmation.
- Distinguish Planned, Researched, Implemented, Tested, Deployed, and Client-confirmed.
- Give each action a unique ID, one accountable owner, an exact due date, acceptance criteria, and an evidence location.
- Record the team response and outcome for every material Tutor, Client, or team feedback item.
- Record rationale and affected PBIs/documents for every final decision.
- Record impact, mitigation, owner, review date, and status for each risk or blocker.
- Record root cause, process change, success measure, owner, review date, and linked PBI for each improvement.
- Produce a concise decision-and-action record, not a transcript.

Raw meeting notes:
[Paste verified notes here]
```
