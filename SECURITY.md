# Security Features

## 1. Security Philosophy

BoardroomVoiceAgent treats security primarily as **decision integrity**. The project is designed to reduce unsafe executive-communication behavior: false certainty, hidden evidence gaps, collapsed trade-offs, and autonomous strategic decisions presented as if they were human-approved.

The security objective is not to make the agent the decision-maker. It is to preserve evidence boundaries and human accountability while preparing executives to make the decision themselves.

## 2. Security Scope

Implemented protections:

- **Semantic Backpressure** surfaces insufficient evidence, unclear accountability, governance gaps, safety conflicts, and decision-integrity collisions.
- **Human Accountability Lock** prevents the agent from selecting the final strategic pathway for executives.
- **Structured Validation** rejects incomplete or unsafe model payloads before narration.
- **Minimal Boardroom Quality Gates** protect semantic roles, option topology, and spoken decision coherence.
- **Deterministic Fallback** replaces invalid model output with bounded deterministic composition.
- **MockLLM Offline Safety** exercises model-boundary behavior without network calls.
- **No Hardcoded Secrets** keeps the optional provider credential in an environment variable.
- **Trace-Based Observability** records routing, validation, fallback, and backpressure outcomes.
- **Evaluation-Driven Safety Checks** test guardrails as executable regression behavior.

Not implemented or out of scope:

- Production authentication or authorization
- Cloud IAM
- Encryption controls
- External API transport or provider security
- Full prompt-injection defense
- MCP security
- Production deployment hardening
- SIEM integration or production monitoring
- Enterprise compliance certification

## 3. Security Architecture

### 3.1 AGENTS.md — Security Constitution

`AGENTS.md` defines the invariant rules that govern executive-facing output. It prohibits fake certainty, fake win-win framing, unsupported bridges, and autonomous final board decisions. It also requires Semantic Backpressure when evidence, accountability, governance, safety, or compliance boundaries are incomplete.

### 3.2 semantic_backpressure.py — Runtime Halt / Backpressure Enforcement

`src/semantic_backpressure.py` evaluates the source and extracted evidence for decision-integrity risks. It can trigger a Semantic Backpressure brief, identify the governing rule, disclose missing evidence, and preserve the decision boundary. Model output may add backpressure but cannot clear deterministic backpressure.

### 3.3 structured_validation.py — Output Safety Validation

`src/structured_validation.py` implements two extraction-stage gates, with the third gate enforced by the narrator:

- **Semantic Role Integrity** prevents risks or missing-evidence phrases from becoming the prior business belief.
- **Decision Topology Preservation** prevents material source options from being collapsed or silently omitted.
- **Spoken Decision Coherence** in `src/boardroom_narrator.py` rejects mechanical questions, meaningless cues, fragmented narration, broken abbreviations, raw bilingual clause joins, and invalid pause placement.

These are deliberately three composite gates rather than a large checklist of disconnected validators.

Before these semantic gates, `src/schema_validation.py` loads the real `src/schemas/evidence_schema.json` artifact and strictly enforces the schema subset used by BoardroomVoiceAgent. The implementation is dependency-free for offline reproducibility and is not a general-purpose JSON Schema Draft 2020-12 engine. Schema validation cannot establish source faithfulness; Workstream 3 evaluates grounding through independent scenario expectations.

### 3.4 llm_interface.py — LLM Boundary

`src/llm_interface.py` provides an offline MockLLM and an intentionally stubbed provider boundary.

- MockLLM makes no network calls.
- The optional provider credential is read from `LLM_API_KEY`; no API key is hardcoded.
- Provider behavior is not represented as production-ready.
- Invalid MockLLM/model output is rejected and routed to deterministic fallback.
- Unmatched demo inputs return insufficient context rather than fabricated AI-governance evidence.

### 3.5 prompts.py — Prompt-Level Safety Constraints

`src/prompts.py` instructs a future model boundary not to fabricate evidence, make the final strategic decision, hide trade-offs, or suppress missing-evidence disclosure. Prompt instructions complement runtime validation; they do not replace it.

### 3.6 evaluation.py and test_runner.py — Safety Regression

`src/evaluation.py` reports seven structural contracts and the three Minimal Boardroom Quality Gates. `test_runner.py` exercises valid MockLLM output, invalid-output fallback, Semantic Backpressure, Human Accountability Lock, risk-as-assumption rejection, option preservation, spoken coherence, and non-AI routing probes. It also executes all eight cases in `eval/security_eval_cases.json` against independent expectations and runs five source-grounding scenarios from `eval/source_faithfulness_cases.json`.

### 3.7 tracing.py — Auditability

`src/tracing.py` records decision gravity, LLM mode, model-validation status, deterministic fallback, Semantic Backpressure, triggered rule, quality-gate outcomes, and the final gate-protocol outcome. Traces support review; they are not a production SIEM or immutable audit log.

## 4. Security Behaviors Demonstrated

- **Missing accountability:** AI Agent scaling without an accountability owner, auditable ROI baseline, or halt rules triggers Semantic Backpressure and lists the missing controls.
- **Fake certainty:** Requests that exceed the evidence boundary are not converted into settled conclusions.
- **Final-decision requests:** The output frames the choice but does not approve a strategic pathway for the board.
- **Invalid model output:** A MockLLM recommendation that violates human decision ownership is rejected and routed through deterministic fallback.
- **Risk-as-assumption error:** Semantic Role Integrity rejects a risk phrase when it is incorrectly supplied as the prior belief.
- **Scenario-overfit protection:** Warehouse productivity and office-lease probes do not become AI-governance briefings.

## 5. How to Run Security Evaluation

Run the regression suite:

```bash
python test_runner.py
```

Run the primary governance scenario:

```bash
python app.py --input sample_inputs/custom_pre_read.md --output sample_outputs/final_submission_custom_mock_llm.md --mock-llm --trace --strict
```

Validate the reviewer-facing security corpus:

```bash
python -m json.tool eval/security_eval_cases.json
```

## 6. Limitations

- This is a capstone prototype focused on decision-integrity security.
- It does not implement full production infrastructure or application security controls.
- MockLLM exists for offline reproducibility and is not a general security-testing model.
- The provider boundary is stubbed and must be separately designed and reviewed before production use.
- Security expectations are automated, but the corpus remains small and deterministic rather than a substitute for production red-teaming.
- Source-faithfulness checks are anchor-based and do not establish universal factual accuracy.
- Human review remains mandatory for executive use.
