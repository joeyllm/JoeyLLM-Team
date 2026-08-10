# Sprint 4 Goal

## 🎯 Complete the ChatJoey frontend workstream, connect the real JoeyLLM API, and prepare the team for vector database work.

That means: **consolidate the separate Next.js frontend prototypes into one shared ChatJoey frontend**, **connect and test the real JoeyLLM API**, and build a **foundational understanding of vector databases and Qdrant** for the next retrieval-focused sprint.

The model framework remains client-provided. Model fine-tuning, post-training, database back-end experiments, and production Qdrant integration are not claimed as Sprint 4 deliverables.

---

**Window:** 2026-07-27 → 2026-08-11 · **Milestone:** [Sprint 4](https://github.com/joeyllm/JoeyLLM-Team/milestone/5)

## Primary Workstreams

- **Frontend consolidation** — compare the individual Next.js frontend prototypes, discuss their strengths and limitations, stop maintaining competing formal versions, and agree on one shared ChatJoey frontend direction.
- **API deployment and testing** — connect the shared frontend to the real JoeyLLM API through the server-side Next.js API boundary, deploy the online system, and have each team member independently test the end-to-end question-and-answer flow.
- **Vector database and Qdrant learning** — study embeddings, vector storage, payload metadata, similarity search, Qdrant concepts, and how a future RAG layer could fit behind the ChatJoey server-side API boundary.

- **Week 1** — confirm Sprint 4 scope, review Semester 1 evidence, identify which outputs are verified versus prototype-only, and prepare the team repository/workflow so website work can begin once Matthew's detailed interface instructions are available.
- **Week 2** — build and publish individual Next.js chat frontend prototypes in separate member branches; explore interface layout, chat interaction, responsive behaviour, mock-response flow, deployment readiness, and a replaceable client-API boundary.
- **Week 2** — begin Qdrant and vector database learning by developing a basic understanding of embeddings, vector storage, similarity search, and Qdrant's role in retrieval-augmented generation.
- **Week 3** — stop separate competing frontend development, compare member prototypes, select one shared frontend direction, and consolidate the final ChatJoey interface using Yingzhe's version as the main template with suitable ideas from other branches.
- **Week 3** — connect the consolidated ChatJoey frontend to the real JoeyLLM API through the server-side API boundary, deploy the system online, and have each member independently test API connectivity and model responses.
- **Week 3** — continue vector database and Qdrant learning, document the current understanding, and identify the decisions needed before future production retrieval work, including embedding model, vector dimension, Qdrant hosting, collection design, metadata schema, and retrieval evaluation.
