# AI Prompt for Meeting Minutes

Use this prompt when asking an AI assistant to generate JoeyLLM-Team meeting minutes. The raw notes may be written in Chinese or English, but the final meeting minutes should be generated in English.

```text
请为 JoeyLLM-Team 生成一份正式的英文 Meeting Minutes。

请先从 GitHub 读取对应模板：
Repository: joeyllm/JoeyLLM-Team
Folder: management/weekly-reports-END/templates

根据会议类型选择模板：
- Tutor Meeting: Tutormeeting.md
- Client Meeting: Clientmeeting.md
- Quick Sync / Internal Meeting: Quicksync.md
- Weekly Report: Weeklyreporttemplate.md

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

会议基本信息：
- Meeting type: [Tutor Meeting / Client Meeting / Quick Sync / Weekly Report]
- Date: [YYYY-MM-DD]
- Sprint / Week: [S__ / W__]
- Next meeting date: [YYYY-MM-DD，如果知道]

要求：
- 最终输出必须是英文。
- 严格按照 GitHub 模板结构生成。
- 使用正式的大学项目文档语气。
- 清楚区分 completed work、in-progress work、planned work 和 untested assumptions。
- 按模板要求写清楚 feedback、decisions、action items、owner、due date、status、improvements/follow-up 和 next meeting focus。
- 不要编造成果、决定或已完成事项。
- 如果会议没有做出最终决定，请写：`No final decision was made. This will be followed up.`
- 如果没有 blocker，请写：`No major blockers were identified.`

原始会议记录：
[在这里粘贴会议记录，可以是中文或英文]
```
