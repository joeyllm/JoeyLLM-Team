# Weekly Report 🗂️

**Week:** W02 · **Sprint:** Sprint 4 · **Date:** 2026-08-03  
**Prepared by:** Southern-cross AI

## Sprint goal

Present the completed and published Next.js chat interface, continue dataset-optimisation and training-parameter planning, and undertake the Qdrant learning task next week. The model framework is provided by the client, so the team's technical focus remains data quality and training configuration.

## Sprint criteria

| Criterion | Success criterion | Evidence | Status |
|-----------|-------------------|----------|--------|
| C1 |  |  |  |
| C2 | Every Southern-cross AI member completed Next.js website work in a separate branch; the team website is complete, published and passes the defined quality checks. | [Team repository](https://github.com/joeyllm/ChatJoey) and [member branches](https://github.com/joeyllm/ChatJoey/branches) | Completed |
| C3 | Document Qdrant's role and core concepts, and identify the client decisions needed before production integration; a minimal insert/search spike is desirable but not yet evidenced. | Planned Qdrant note and reproducible local spike | Next week |

## Progress this week

- Every Southern-cross AI member completed website work in a separate branch.
- The team completed and published the Next.js chat website.
- The reviewed team build passed `pnpm lint`, `pnpm typecheck` and `pnpm build` on 3 August 2026.
- A local browser check confirmed the suggestion-to-composer-to-mock-reply flow.
- Semester 1 assets were reviewed. The Australian 1B package and FineWeb profiling have local evidence; 5B training, full training and later outputs are not recorded as completed.

## In progress

- Create a dataset-optimisation experiment plan from the verified Australian 1B baseline.
- Create a controlled training-parameter experiment matrix for the client-provided framework.
- Check server recovery and request the client API contract and Qdrant production settings.

## Blockers

- JupyterHub and the server were unavailable according to Matthew's 3 August email. His hoped-for next-day recovery was an estimate, not a confirmed date.
- The client model API contract is not documented in the reviewed repository, so the real model endpoint and end-to-end response path cannot yet be claimed as validated.
- Qdrant is not active or integrated. The embedding model, vector dimension, distance metric, collection design and hosting plan still require confirmation.

## Evidence

- Team repository: <https://github.com/joeyllm/ChatJoey>
- Different members' work: <https://github.com/joeyllm/ChatJoey/branches>
- Supporting evidence: repository README, validation output and the published team website.

## Next week

- Begin C3: document Qdrant concepts and, if practical, produce a reproducible local insert/search spike.
- Confirm the embedding model, vector dimension, distance metric, hosting approach and client API requirements.
- Update Sprint progress, close or revise open actions, and prepare the next demonstrable result for the Sprint Review.

## Actions

| Action | Owner | Due | Status |
|--------|-------|-----|--------|
| Record the team repository and Branches page in the Sprint evidence index. | Southern-cross AI | 2026-08-03 | Done |
| Write a Qdrant concept note and, if practical, a minimal local insert/search spike. | Data/retrieval workstream | 2026-08-14 | Planned |
| Create a dataset-optimisation experiment plan from the verified Australian 1B baseline. | Dataset workstream | 2026-08-07 | Open |
| Create a training-parameter experiment matrix for the client-provided framework. | Training workstream | 2026-08-07 | Open |
| Check server recovery and request the client API contract and Qdrant production settings. | Client liaison | 2026-08-04 | Open |

🙂
