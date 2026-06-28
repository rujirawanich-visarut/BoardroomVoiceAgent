# Threat Model

## 1. System Context

BoardroomVoiceAgent processes executive pre-read text and produces decision-grade briefings with prior updates, an Evidence → Insight → Conclusion → Choice chain, material options, missing-evidence disclosure, a Meeting Room Question, a One-Line Decision Cue, and TTS-ready narration.

This is a lightweight threat model for a capstone prototype. It focuses on decision-integrity and public-repository risks rather than claiming a full STRIDE or production infrastructure assessment.

## 2. Assets to Protect

- Decision integrity
- Human accountability
- Evidence faithfulness
- Trade-off clarity
- Missing-evidence visibility
- Output trustworthiness
- Absence of secret leakage

## 3. Threats Considered

### Threat 1 — Certainty Theater

**Description:** The agent presents uncertain, incomplete, or assumption-heavy evidence as settled truth.

**Mitigation:** Semantic Backpressure, the Missing Evidence Protocol in `AGENTS.md`, structured validation, and explicit evidence-boundary narration.

### Threat 2 — Fake Win-Win Framing

**Description:** The agent hides an unavoidable trade-off and implies that all objectives can be optimized simultaneously.

**Mitigation:** Decision Topology Preservation and the anti-fake-win-win constraints in `AGENTS.md`.

### Threat 3 — Risk-as-Assumption Error

**Description:** The agent uses a risk, governance gap, or missing-evidence phrase as the prior business assumption.

**Mitigation:** Semantic Role Integrity and a dedicated regression case in `test_runner.py`.

### Threat 4 — Autonomous Final Decision

**Description:** The agent chooses or approves the final strategic pathway for the board.

**Mitigation:** Human Accountability Lock, model-output validation, narration checks, and invalid-recommendation fallback testing.

### Threat 5 — Missing Evidence Suppression

**Description:** The agent generates a confident briefing while accountability, ROI baseline, data-access boundaries, approval gates, or halt rules remain incomplete.

**Mitigation:** Semantic Backpressure and the Missing Evidence Protocol.

### Threat 6 — LLM Output Overreach

**Description:** A model returns schema-shaped but semantically unsafe content, including unsupported recommendations or collapsed options.

**Mitigation:** `src/structured_validation.py`, the three Minimal Boardroom Quality Gates, deterministic fallback, and regression testing.

### Threat 7 — Scenario Overfit

**Description:** The agent incorrectly routes an unrelated pre-read into the AI-governance scenario.

**Mitigation:** AI-specific routing signals, a safe insufficient-context fallback, and warehouse/office out-of-domain probes.

### Threat 8 — Secret Leakage / Public Repo Hygiene

**Description:** Credentials, `.env` files, notebook runtime packages, local paths, or compiled caches are accidentally committed or exposed.

**Mitigation:** `.gitignore`, environment-variable credential lookup, no hardcoded API keys, offline MockLLM execution, and pre-submission hygiene scans.

## 4. Threat-to-Control Matrix

| Threat | Risk | Mitigation | Code Evidence | Test Evidence |
|---|---|---|---|---|
| Certainty Theater | Unsupported executive confidence | Semantic Backpressure and missing-evidence disclosure | AGENTS.md; src/semantic_backpressure.py | Custom AI-governance and weak-evidence scenarios |
| Fake Win-Win Framing | Hidden strategic sacrifice | Decision Topology Preservation and invariant constraints | AGENTS.md; src/structured_validation.py | Security case fake_win_win_003; scenario tests |
| Risk-as-Assumption Error | False prior-update logic | Semantic Role Integrity | src/structured_validation.py | Minimal gate regression in test_runner.py |
| Autonomous Final Decision | Loss of human accountability | Human Accountability Lock and recommendation rejection | AGENTS.md; src/structured_validation.py; src/boardroom_narrator.py | Invalid MockLLM fallback test |
| Missing Evidence Suppression | Unsafe commitment without controls | Backpressure and missing-evidence narration | src/semantic_backpressure.py; src/boardroom_narrator.py | Custom AI-governance scenario |
| LLM Output Overreach | Unsafe model content reaches executives | Structured validation and deterministic fallback | src/llm_interface.py; src/evidence_chain.py | Valid/invalid MockLLM paths |
| Scenario Overfit | Unrelated input receives false AI evidence | AI-specific routing and safe unmatched fallback | src/llm_interface.py; src/evidence_chain.py | Warehouse and office probes |
| Secret Leakage / Repo Hygiene | Credentials or local artifacts exposed | Environment variables and repository ignore rules | src/llm_interface.py; .gitignore | Reviewer hygiene scan; security case secret_handling_008 |

All eight security cases are executed by `test_runner.py`. A separate five-case source-faithfulness corpus verifies explicit grounding anchors for representative scenarios; it is not an exhaustive hallucination detector.

## 5. Residual Risks

- No production authentication or authorization is implemented.
- No real deployment or cloud-security controls are implemented.
- Provider mode is stubbed and requires a separate security review before use.
- Out-of-domain generalization requires broader adversarial testing.
- Prompt injection is not comprehensively defended.
- Traces are local observability artifacts, not immutable security logs.
- Human review remains required for executive use.

## 6. Security Review Checklist

- [x] `AGENTS.md` present
- [x] Semantic Backpressure tested
- [x] Human Accountability Lock tested
- [x] MockLLM mode runs offline
- [x] No hardcoded secrets
- [x] No `.env` committed
- [x] `test_runner.py` passes
- [x] Traces generated
- [x] Stale risk-as-assumption sample outputs removed
