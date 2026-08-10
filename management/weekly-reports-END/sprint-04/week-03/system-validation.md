# ChatJoey System Validation Record

**Team:** Southern-cross AI  
**Sprint / Week:** Sprint 4 / Week 3  
**Validation date:** 10 August 2026  
**Application:** [https://chat-joey.vercel.app/](https://chat-joey.vercel.app/)  
**Implementation:** [ChatJoey PR #4](https://github.com/joeyllm/ChatJoey/pull/4)  
**Accountable evidence owner:** Nuo Chen  
**Contributors / testers:** Nuo Chen, Wen Sun, Xiang Chang, Xingyu Li, Yingzhe Xu

## Purpose

Confirm that the consolidated ChatJoey interface is accessible, supports the agreed interaction flow, and communicates with the real JoeyLLM API. This record separates successful technical connectivity from model-answer-quality evaluation, which is outside the verified Sprint 4 scope.

## Shared test results

| Test ID | Test | Expected result | Team-confirmed result | Status | Evidence / limitation |
| --- | --- | --- | --- | --- | --- |
| S4-T01 | Open the production URL | The shared interface loads successfully | Loaded successfully for all members | Passed | Live deployment URL |
| S4-T02 | Submit an empty message | Empty input is rejected without an API request | Empty submission was prevented | Passed | PR #4 browser validation and team check |
| S4-T03 | Submit a normal question | The message reaches the server-side API route | Submission completed without observed error | Passed | Live application and PR #4 API boundary |
| S4-T04 | Receive a real JoeyLLM answer | A genuine model response appears in the chat | Response returned and displayed | Passed | Live application; successful connectivity does not by itself prove answer quality |
| S4-T05 | Switch interface language | UI labels change without breaking the conversation interface | Language switching operated successfully | Passed | Six-language implementation in PR #4 |
| S4-T06 | Use a narrow/mobile-sized window | Layout remains usable and text does not overflow | No usability problem was reported by the team | Passed | Responsive implementation and member checks |
| S4-T07 | Observe normal-use error behaviour | No unexpected error is shown in the tested flow | No unexpected error was observed | Passed for tested normal flow | Forced outage, load, penetration, and recovery testing were not separately performed |

## Member confirmation

| Tester | Scope confirmed | Result | Follow-up defect |
| --- | --- | --- | --- |
| Nuo Chen | Live access, input, response, language, responsive layout | Passed | None reported |
| Wen Sun | Live access, input, response, language, responsive layout | Passed | None reported |
| Xiang Chang | Live access, input, response, language, responsive layout | Passed | None reported |
| Xingyu Li | Live access, input, response, language, responsive layout | Passed | None reported |
| Yingzhe Xu | Live access, input, response, language, responsive layout | Passed | None reported |

## Quality conclusion

The team confirmed that the deployed Sprint 4 flow operated without a reported defect in the agreed manual checks. This supports the status **Deployed and manually tested**. It does not claim automated end-to-end coverage, performance testing, security testing, production observability, Qdrant/RAG integration, or a formal benchmark of model-answer quality.

## Sprint 4 validation boundary

All five members completed the agreed manual validation and no defect was reported in the tested Sprint 4 flow. Automated browser testing, load testing, security testing, and forced-failure testing were not Sprint 4 completion criteria and are not claimed by this record.
