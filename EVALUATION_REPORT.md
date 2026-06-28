# Evaluation Report

BoardroomVoiceAgent separates format compliance from decision-grade semantic quality.

## Structured-output boundary

The runtime loads `src/schemas/evidence_schema.json` and uses a dependency-free strict validator for the schema features BoardroomVoiceAgent relies on. This validator rejects malformed JSON, trailing prose, duplicate keys, missing or unknown fields, incorrect field types, empty required strings, and duplicate array items.

It is not a general-purpose JSON Schema Draft 2020-12 engine. Passing schema validation does not prove that claims are grounded in the source. Source faithfulness is tested independently through Workstream 3 scenario expectations rather than being inferred from schema validity.

## Structural Contract Checks — 7

1. Required sections exist.
2. Evidence → Insight → Conclusion → Choice exists.
3. Trade-off/choice exists.
4. Meeting Room Question exists.
5. One-Line Decision Cue exists.
6. TTS pause tags exist.
7. Human Accountability Lock is preserved.

## Minimal Boardroom Quality Gates — 3

1. **Semantic Role Integrity** rejects risks or missing-evidence phrases used as the prior belief.
2. **Decision Topology Preservation** checks that material source options remain represented in the choice.
3. **Spoken Decision Coherence** rejects mechanical questions, meaningless cues, micro-fragments, broken abbreviations, raw bilingual clause joins, long lines, and invalid `[PAUSE 3.0s]` placement.

## Integration scenarios

- Deterministic AI-governance baseline
- Valid MockLLM path
- Invalid MockLLM → deterministic fallback
- Custom Thai/English AI-governance pre-read
- Custom deterministic path
- Warehouse productivity non-AI probe
- Office lease non-AI probe

## Independent Workstream 3 evaluation

- **Security Evaluation Corpus — 8 cases:** certainty theater, final-decision overreach, fake win-win framing, missing accountability, risk-as-assumption, option collapse, out-of-domain routing, and secret handling.
- **Source Faithfulness Corpus — 5 cases:** custom AI governance, warehouse productivity, office lease, neutral informational memo, and a novel non-AI three-option decision.

The evaluator reads explicit expectations from JSON artifacts rather than using the runtime gates as its oracle. It checks decision gravity, backpressure, composition route, option count, required and forbidden terms, prior-assumption constraints, Human Accountability Lock language, and grounding terms that must appear in both source and output.

Current result: **8/8 security cases and 5/5 source-faithfulness cases pass.** This is scenario-based evidence, not a claim of universal factual accuracy.

The executed `demo.ipynb` records the complete evaluation signal and reviewer assertions. `test_runner.py` also verifies that a traced integration run produces a unique per-run JSON artifact in addition to `run_trace_latest.json`.

## Known evaluation limitations

- Gates remain deterministic heuristics rather than an independent model judge.
- Source-faithfulness checks use explicit grounding anchors rather than semantic entailment or an independent model judge.
- The benchmark remains intentionally small and should grow before production use.
- Passing evaluation demonstrates contract adherence for the included scenarios, not general enterprise accuracy.
