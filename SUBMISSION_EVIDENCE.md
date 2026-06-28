# BoardroomVoiceAgent — Submission Evidence Index

This index points reviewers to reproducible repository evidence. It does not claim capabilities outside the implemented prototype.

## Verified commands

```bash
python -m pip install -r requirements.txt
python test_runner.py
python app.py --input sample_inputs/custom_pre_read.md --output sample_outputs/final_submission_custom_mock_llm.md --mock-llm --trace --strict
```

The offline CLI uses the Python standard library and performs no network calls in deterministic or MockLLM mode.

## Reviewer evidence map

| Claim | Evidence | Verification |
|---|---|---|
| Pre-decision clarity rather than generic summarization | `CAPSTONE_WRITEUP.md`; custom briefing output | Inspect Prior Update and Evidence → Insight → Conclusion → Choice |
| Three Minimal Boardroom Quality Gates | `src/structured_validation.py`; `src/boardroom_narrator.py` | Run `python test_runner.py` |
| Strict structured-output boundary | `src/schema_validation.py`; `src/schemas/evidence_schema.json` | Review strict-boundary regressions in `test_runner.py` |
| Semantic Backpressure and Human Accountability Lock | `AGENTS.md`; `src/semantic_backpressure.py` | Run the custom and invalid-recommendation scenarios |
| Independent security evaluation | `eval/security_eval_cases.json` | Confirm 8/8 cases in `test_runner.py` output |
| Scenario-based source faithfulness | `eval/source_faithfulness_cases.json`; `src/scenario_evaluation.py` | Confirm 5/5 cases in `test_runner.py` output |
| Reproducible notebook | `demo.ipynb` | Inspect the committed executed outputs or rerun the notebook |
| Per-run observability | `src/tracing.py`; executed notebook trace summary | Confirm `run_id` and `logs/runs/<run-id>-<scenario>.json` |
| Antigravity planning and Human Vibe Diff | `implementation_plan01.md`; `submission_evidence/antigravity/01-plan-review-and-hardening-patch.png` | Inspect the plan-first pause and the start of the human pre-code patch |
| Wave 1 result review and bounded continuation | `submission_evidence/antigravity/02-wave1-walkthrough-wave11-approval.png` | Confirm the walkthrough/diff, deterministic-MVP acceptance, and `Wave 1.1 only` instruction |
| Artifact-based IDE handoff and readiness gate | `submission_evidence/antigravity/03-ide-handoff-wave1-exit-review.png` | Confirm the transferred invariant context, `Do NOT implement Wave 2 yet`, and `READY AFTER MINOR PATCHES` verdict |

## Historical Antigravity evidence

The committed screenshots are copies of project-author-supplied historical evidence. Together with the author's chronology, they establish the following sequence:

```text
implementation plan
→ pre-code hardening patch
→ Wave 1 build and walkthrough
→ human acceptance of the deterministic MVP
→ authorization for Wave 1.1 only
→ reported five-scenario hardening
→ artifact-based handoff to Antigravity IDE
→ independent Wave 1 Exit Review
→ READY AFTER MINOR PATCHES
→ corrective implementation and verification
```

This sequence is a human-orchestrated sequential specialist-agent workflow. Platform-level reasoning supported macro-architecture and initial scaffolding, while the IDE provided stronger repository-level inspection, code-detail review, and corrective implementation. The screenshots do not independently prove the full patch text, authorship of every code line, exact historical terminal commands, or the complete scope of later IDE activity. `python test_runner.py` proves the current repository behavior, not historical tool attribution. See `submission_evidence/antigravity/README.md` for the evidence boundary.

## Notebook execution evidence

`demo.ipynb` is committed with six executed code cells and zero execution errors. It records:

- Python and environment information without exposing an absolute local path
- dependency verification
- strict schema, security, source-faithfulness, and integration results
- custom AI-governance routing and evaluation
- schema and semantic validation status
- a unique per-run trace reference
- reviewer assertions for option preservation, Human Accountability Lock, and TTS line length

The notebook uses `sys.executable` rather than a machine-specific Python command. Locally it discovers the repository root. On Kaggle it can copy an attached read-only repository into `/kaggle/working` before executing.

## Trace behavior

Each traced run writes both:

```text
logs/run_trace_latest.md
logs/run_trace_latest.json
```

and unique per-run artifacts:

```text
logs/runs/<run-id>-<scenario>.md
logs/runs/<run-id>-<scenario>.json
```

The `logs/` directory remains ignored because traces are generated runtime artifacts. The executed notebook contains reviewer-visible trace evidence without requiring generated logs to be committed.

## Scope boundary

Provider integration, PDF/PPTX ingestion, generated audio, sessions, persistent memory, real multi-agent orchestration, production UI, and deployment infrastructure are not implemented. Human review remains mandatory. Official submission requirements must be checked again when the final competition rules are available.
