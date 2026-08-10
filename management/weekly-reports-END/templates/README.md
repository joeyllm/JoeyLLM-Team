# Meeting Minutes Templates

This folder contains the shared professional meeting minutes template and weekly report template for JoeyLLM-Team.

## Templates

| Purpose | Template |
|---|---|
| Tutor, client, Sprint Review, retrospective, and formal internal meeting minutes | `professional-meeting-minutes-template.md` |
| Weekly report | `Weeklyreporttemplate.md` |

## AI Prompt

Team members can copy the prompt below into an AI assistant. The raw notes may be written in Chinese or English, but the final meeting minutes should be generated in English.

```text
请为 JoeyLLM-Team 生成一份正式的英文 Meeting Minutes。

请先从 GitHub 读取通用会议纪要模板：
Repository: joeyllm/JoeyLLM-Team
Template path: management/weekly-reports-END/templates/professional-meeting-minutes-template.md

默认项目信息：
- Project: JoeyLLM / ChatJoey
- Client: Matthew Altenburg
- Tutor: Annie Sun
- 默认组员：
  - Nuo Chen
  - Wen Sun
  - Xiang Chang
  - Xingyu Li
  - Yingzhe Xu

如果我没有特别说明缺席人员，就默认以上五位组员全部出席。
如果是 Tutor Meeting，默认 Tutor 是 Annie Sun。
如果是 Client Meeting，默认 Client 是 Matthew Altenburg。

会议基本信息：
- Meeting type: [Tutor Meeting / Client Meeting / Internal Meeting / Sprint Review / Retrospective]
- Date: [YYYY-MM-DD]
- Time: [HH:MM-HH:MM, timezone，如果知道]
- Sprint / Week: [Sprint X / Week XX]
- Location / Channel: [Classroom / Online / Email / Teams / Zoom / GitHub, 如果知道]
- Chair: [Name，如果知道]
- Minute taker: [Name，如果知道]
- Next meeting date/time: [YYYY-MM-DD HH:MM，如果知道]

要求：
- 最终输出必须是英文。
- 严格按照 GitHub 上的 `professional-meeting-minutes-template.md` 结构生成。
- 使用正式的大学项目文档语气。
- 删除模板中的 instructional comments，并替换所有 placeholders。
- 使用准确日期、具体会议类型和具体人员姓名。
- 不要编造成果、决定、证据链接或已完成事项。
- 清楚区分 Planned、Researched、Implemented、Tested、Deployed 和 Client-confirmed 等状态。
- 每个 action item 必须有唯一 ID、具体 deliverable、一个 accountable owner、due date、status 和 acceptance evidence/location。
- 每个 material tutor/client/team feedback 都要记录 team response 和 outcome。
- 每个 final decision 都要包含 rationale 和 affected PBI/document。
- 每个 risk/blocker 都要包含 impact、mitigation、owner、review date 和 status。
- 每个 improvement 都要包含 observed problem、root cause、process change、success measure 和 review date。
- 如果没有最终决定，请在 Decisions section 写明 pending，并创建 action 去 follow up。
- 如果没有 blocker，请写：`No major blockers were identified.`
- 如果没有可用 evidence link，请写：`Evidence link to be added after publication.`，不要编造链接。
- 输出应是 concise decision-and-action record，不要写成逐字 transcript。

原始会议记录：
[在这里粘贴会议记录，可以是中文或英文]
```
