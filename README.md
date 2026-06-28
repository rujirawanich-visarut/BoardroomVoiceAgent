# BoardroomVoiceAgent

BoardroomVoiceAgent converts executive pre-reads into decision-grade spoken briefings. It is not a generic summarizer; it is a **Pre-Decision Clarity Layer** that surfaces changed assumptions, evidence gaps, material options, and the question executives must resolve.

## Why it exists

When a presenter is absent, a chronological summary does not carry enough judgment. BoardroomVoiceAgent restructures source material as:

`Prior Update → Evidence → Insight → Conclusion → Choice`

It preserves human decision ownership and triggers Semantic Backpressure when evidence, accountability, governance, or safety boundaries are incomplete.

## Architecture

The offline pipeline separates:

1. Markdown ingestion
2. Decision-gravity classification
3. Evidence-chain extraction
4. Three Minimal Boardroom Quality Gates
5. Semantic Backpressure
6. Boardroom/TTS narration
7. Evaluation and tracing

`AGENTS.md` is the invariant harness. `Skills/script_tts_ready_skill_v3_0.md` defines the Boardroom Voice procedural skill contract implemented by the runtime.

## Minimal Boardroom Quality Gates

- **Semantic Role Integrity** — keeps prior beliefs distinct from risks and missing evidence.
- **Decision Topology Preservation** — preserves material options without choosing for executives.
- **Spoken Decision Coherence** — requires an executive-ready question, meaningful cue, complete spoken units, and disciplined pause placement.

Gate outcomes are `PASS`, `REPAIR`, `FALLBACK`, and `BACKPRESSURE`. Quality repair is not mislabeled as Semantic Backpressure.

## Strict structured-output boundary

MockLLM and future provider responses cross the runtime boundary as serialized JSON. The dependency-free validator loads the real schema at `src/schemas/evidence_schema.json` and enforces the exact subset used by BoardroomVoiceAgent: required and additional properties, object/array/string/boolean types, non-empty strings, unique array items, and local schema references. It also rejects malformed JSON, trailing prose, duplicate keys, and non-standard constants.

This validator is purpose-built for BoardroomVoiceAgent. It is **not** a general-purpose JSON Schema Draft 2020-12 engine. Schema validation checks response shape and types; it does not establish source faithfulness. Source-grounding behavior is evaluated separately in the Workstream 3 scenario corpus.

## Run locally

Python 3.10+ is recommended. The offline CLI uses the standard library only.

### Verify dependencies

```bash
python -m pip install -r requirements.txt
```

### Run the complete evaluation

```bash
python test_runner.py
```

### Run the custom AI-governance demo

```bash
python app.py --input sample_inputs/custom_pre_read.md --output sample_outputs/final_submission_custom_mock_llm.md --mock-llm --trace --strict
```

### Run the non-AI routing probes

```bash
python app.py --input sample_inputs/warehouse_productivity_update.md --output sample_outputs/warehouse_productivity_update_briefing.md --mock-llm --trace --strict
python app.py --input sample_inputs/office_lease_decision.md --output sample_outputs/office_lease_decision_briefing.md --mock-llm --trace --strict
```

## Key Concepts Demonstrated

This project maps the following capstone concepts:

- Key Concept 4 — Security Features
- Key Concept 6 — Agent Skills / Agent
- Key Concept — Antigravity

Evidence and reviewer mapping:

- [Key Concepts Mapping](KEY_CONCEPTS_MAPPING.md)
- [Architectural Execution Trace with Antigravity](Architectural_Execution_Trace_with_Antigravity_BoardroomVoiceAgent.md) — historical orchestration evidence supplied by the project author
- [Antigravity Historical Evidence](submission_evidence/antigravity/README.md) — committed screenshots and explicit evidence boundaries

Antigravity is demonstrated as a **human-orchestrated sequential specialist-agent workflow with artifact-based context handoff and an independent readiness gate**. Platform-level reasoning supported macro-architecture and initial scaffolding. After the human reviewed Wave 1 and authorized Wave 1.1 only, the IDE received the invariant files, repository state, and prior-work summary. It was prohibited from starting Wave 2 and first returned `READY AFTER MINOR PATCHES` from an independent Wave 1 Exit Review. The IDE then provided stronger repository-level inspection, code-detail review, and corrective implementation.

Current tests prove runtime behavior; they do not independently prove historical tool identity. This is not a claim that the BoardroomVoiceAgent runtime uses ADK, MCP, dynamic skill loading, persistent memory, deployment infrastructure, or a real autonomous multi-agent runtime.

Agentic concepts explicitly demonstrated include:
- Multi-stage agentic workflow with explicit handoffs
- Context engineering through an invariant harness and specialized skill
- Structured model-output validation and deterministic fallback
- Semantic Backpressure and Human Accountability Lock
- Traceable routing outcomes
- Structural and semantic evaluation
- Independent security expectations across eight adversarial cases
- Source-faithfulness anchors across five representative enterprise scenarios
- Offline MockLLM execution without network calls

## Security Features

This project demonstrates decision-integrity security through Semantic Backpressure, Human Accountability Lock, structured validation, deterministic fallback, and offline MockLLM execution.

Reviewer artifacts:

- `SECURITY.md`
- `THREAT_MODEL.md`
- `eval/security_eval_cases.json`

## Scope and limitations

This is a capstone reference prototype, not a production deployment.

- Input ingestion currently supports UTF-8 text/Markdown, not PDF or PPTX.
- Deterministic reasoning supports documented scenarios and safely returns insufficient context for unmatched material.
- MockLLM uses local fixtures and is not a general language model.
- Provider mode is intentionally stubbed.
- No sessions, persistent memory, real multi-agent orchestration, audio synthesis, UI, or deployment stack is implemented.
- Human review remains mandatory.

## Repository guide

- `ARCHITECTURE.md` — component boundaries and routing
- `CAPSTONE_WRITEUP.md` — problem, solution, evidence, and limitations
- `DEMO.md` / `demo.ipynb` — reproducible walkthrough
- `EVALUATION_REPORT.md` — current 7 structural + 3 quality-gate model
- `SECURITY.md` / `THREAT_MODEL.md` — implemented controls, threats, and residual risks
- `eval/security_eval_cases.json` — reviewer-facing adversarial security cases
- `eval/source_faithfulness_cases.json` — independent source/output grounding expectations
- `SCENARIOS.md` — expected behavior by scenario
- `FINAL_READINESS_CHECKLIST.md` — pre-upload checks
- `SUBMISSION_EVIDENCE.md` — reviewer verification index and reproducibility evidence
