import json
import os
import subprocess
import sys
from pathlib import Path

from src.boardroom_narrator import spoken_decision_coherence
from src.boardroom_narrator import BoardroomVoiceAgentSkill
from src.contracts import DocumentContext
from src.decision_gravity import DecisionGravityClassifier
from src.evidence_chain import EvidenceExtractor
from src.llm_interface import LLMInterface
from src.scenario_evaluation import evaluate_scenario_expectations
from src.schema_validation import StructuredResponseError, parse_and_validate_structured_response
from src.semantic_backpressure import SemanticBackpressureDetector
from src.structured_validation import (
    FALLBACK,
    REPAIR,
    decision_topology_preservation,
    semantic_role_integrity,
    validate_evidence_output,
)


def run_test(name, cmd, expected_markers=(), forbidden_markers=()):
    display_cmd = ["python", *cmd[1:]] if cmd and cmd[0] == sys.executable else cmd
    print("\n======================================")
    print(f"Running Test: {name}")
    print(f"Command: {' '.join(display_cmd)}")
    print("======================================")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    if result.returncode != 0:
        print(f"\n[!] Test Failed: {name}")
        return False
    evaluation_lines = [line for line in result.stdout.splitlines() if line.startswith("Evaluation Result")]
    if not evaluation_lines or "PASSED" not in evaluation_lines[-1]:
        print(f"\n[!] Evaluation Failed in Test: {name}")
        return False
    for marker in expected_markers:
        if marker not in result.stdout:
            print(f"\n[!] Expected routing marker missing in Test: {name}: {marker}")
            return False
    for marker in forbidden_markers:
        if marker in result.stdout:
            print(f"\n[!] Forbidden routing marker found in Test: {name}: {marker}")
            return False
    return True


def run_minimal_gate_regressions():
    print("\n======================================")
    print("Running Test: Minimal Boardroom Quality Gates")
    print("======================================")
    bad_prior = semantic_role_integrity(
        {
            "prior_assumption": "that the unclear accountability risk was " + "fully mitigated",
            "new_baseline": "AI Agent scaling changes the operating model.",
            "risks": ["unclear accountability"],
            "missing_evidence": [],
        }
    )
    collapsed_options = decision_topology_preservation(
        {
            "options": ["Option A", "Option B", "Option C"],
            "choice": "Option A or Option B",
        },
        "Option A: scale. Option B: delay. Option C: targeted pilots.",
    )
    weak_spoken = spoken_decision_coherence(
        "How do we resolve the missing evidence regarding ROI baseline and halt rules before committing?",
        "More discussion is needed.",
        '> “Previously,”\n\n> “Or run a bounded pilot, e.g.”\n\n> “knowledge retrieval.”',
        ["ROI baseline", "halt rules"],
        "High",
        True,
    )
    cases = [
        ("Semantic Role Integrity rejects risk-as-assumption", bad_prior.outcome == FALLBACK),
        ("Decision Topology Preservation rejects collapsed options", collapsed_options.outcome == FALLBACK),
        ("Spoken Decision Coherence routes weak narration to repair", weak_spoken.outcome == REPAIR),
    ]
    for label, passed in cases:
        print(f"[{'PASS' if passed else 'FAIL'}] {label}")
    return all(passed for _, passed in cases)


def _valid_schema_payload():
    return {
        "facts": ["A measured operating fact."],
        "assumptions": ["The current operating path remains viable."],
        "inferences": ["The decision frame has changed."],
        "risks": [],
        "missing_evidence": [],
        "evidence": "A measured operating fact changes the decision baseline.",
        "insight": "The operating choice now requires explicit comparison.",
        "conclusion": "The alternatives must remain distinct for executive review.",
        "choice": "Option A preserves continuity; Option B accepts disruption for lower cost.",
        "prior_assumption": "The current operating path remains viable.",
        "new_baseline": "Executives must now compare continuity and cost.",
        "options": [
            "Option A: preserve continuity.",
            "Option B: accept disruption for lower cost.",
        ],
        "meeting_room_question": "Which operating consequence is the executive team prepared to own?",
        "one_line_decision_cue": "The decision is which operating consequence the organization is prepared to own.",
        "semantic_backpressure_required": False,
        "backpressure_reason": "",
    }


def _raises_stage(raw_response, expected_stage):
    try:
        parse_and_validate_structured_response(raw_response, "EvidenceSchema")
    except StructuredResponseError as exc:
        return exc.stage == expected_stage
    return False


def run_schema_boundary_regressions():
    print("\n======================================")
    print("Running Test: Strict Structured Response Boundary")
    print("======================================")
    valid = _valid_schema_payload()
    valid_raw = json.dumps(valid)

    missing_field = dict(valid)
    missing_field.pop("prior_assumption")
    unknown_field = dict(valid)
    unknown_field["unexpected"] = "not allowed"
    wrong_options_type = dict(valid)
    wrong_options_type["options"] = "Option A"
    wrong_boolean_type = dict(valid)
    wrong_boolean_type["semantic_backpressure_required"] = "false"
    unsafe_but_schema_valid = dict(valid)
    unsafe_but_schema_valid["choice"] = "We recommend choosing Option A immediately."

    parsed_unsafe = parse_and_validate_structured_response(
        json.dumps(unsafe_but_schema_valid),
        "EvidenceSchema",
    )
    semantic_valid, semantic_error = validate_evidence_output(parsed_unsafe)

    mock = LLMInterface(mock_llm=True)
    mock_result = mock.generate_structured(
        "prompt",
        "EvidenceSchema",
        "AI Agent adoption requires governance, data access, and an approval gate.",
    )
    schema_invalid_mock = LLMInterface(mock_llm=True)
    schema_invalid_mock._mock_generate = lambda prompt, schema_name, context: {"facts": []}
    schema_invalid_result = schema_invalid_mock.generate_structured("prompt", "EvidenceSchema", "context")

    malformed_provider = LLMInterface(use_llm=True)
    malformed_provider._provider_generate = lambda prompt, schema_name, context: '{"facts": [}'
    malformed_provider_result = malformed_provider.generate_structured("prompt", "EvidenceSchema", "context")

    cases = [
        ("Valid JSON object passes schema", parse_and_validate_structured_response(valid_raw, "EvidenceSchema") == valid),
        ("Non-string model payload is rejected", _raises_stage(valid, "parse")),
        ("Malformed JSON is rejected", _raises_stage('{"facts": [}', "parse")),
        ("Trailing prose is rejected", _raises_stage(valid_raw + " trailing prose", "parse")),
        ("Duplicate JSON keys are rejected", _raises_stage('{"facts": [], "facts": []}', "parse")),
        ("Missing required field is rejected", _raises_stage(json.dumps(missing_field), "schema")),
        ("Unknown field is rejected", _raises_stage(json.dumps(unknown_field), "schema")),
        ("Wrong options type is rejected", _raises_stage(json.dumps(wrong_options_type), "schema")),
        ("String boolean is rejected", _raises_stage(json.dumps(wrong_boolean_type), "schema")),
        (
            "Schema-valid unsafe choice still fails semantic validation",
            not semantic_valid and "Decision Topology Preservation" in semantic_error,
        ),
        (
            "MockLLM crosses parse and schema boundary",
            "error" not in mock_result
            and mock.last_validation["parse_passed"]
            and mock.last_validation["schema_passed"],
        ),
        (
            "Schema-invalid MockLLM payload reports schema failure",
            "error" in schema_invalid_result
            and schema_invalid_mock.last_validation["parse_passed"]
            and not schema_invalid_mock.last_validation["schema_passed"]
            and schema_invalid_mock.last_validation["error_type"] == "schema_validation_error",
        ),
        (
            "Malformed provider payload reports parse failure",
            "error" in malformed_provider_result
            and not malformed_provider.last_validation["parse_passed"]
            and malformed_provider.last_validation["error_type"] == "parse_validation_error",
        ),
    ]
    for label, passed in cases:
        print(f"[{'PASS' if passed else 'FAIL'}] {label}")
    return all(passed for _, passed in cases)


def run_independent_scenario_corpus(name, corpus_path):
    print("\n======================================")
    print(f"Running Test: {name}")
    print("======================================")
    with open(corpus_path, "r", encoding="utf-8") as handle:
        cases = json.load(handle)

    all_passed = True
    for case in cases:
        if "input_file" in case:
            with open(case["input_file"], "r", encoding="utf-8") as source_handle:
                source_text = source_handle.read()
        else:
            source_text = case["input"]

        context = DocumentContext(raw_text=source_text, paragraphs=[source_text])
        gravity = DecisionGravityClassifier().classify(context)
        evidence = EvidenceExtractor(LLMInterface(mock_llm=True)).extract(context)
        backpressure = SemanticBackpressureDetector().detect(context, evidence)
        brief = BoardroomVoiceAgentSkill().generate_brief(evidence, backpressure, gravity.gravity)
        checks = evaluate_scenario_expectations(
            case,
            source_text,
            gravity.gravity,
            brief,
        )
        passed = all(result for _, result in checks)
        print(f"[{'PASS' if passed else 'FAIL'}] {case['case_id']} ({sum(result for _, result in checks)}/{len(checks)})")
        if not passed:
            for label, result in checks:
                if not result:
                    print(f"       [FAIL] {label}")
        all_passed = all_passed and passed
    return all_passed


def probe_excludes_ai_governance(output_path):
    with open(output_path, "r", encoding="utf-8") as handle:
        output = handle.read().lower()
    forbidden = (
        "human accountability boundaries",
        "ai agent scaling",
        "halt rules are not mature",
    )
    passed = not any(term in output for term in forbidden)
    print(f"[{'PASS' if passed else 'FAIL'}] Non-AI probe stays outside AI-governance routing: {output_path}")
    return passed


def probe_preserves_three_options(output_path):
    with open(output_path, "r", encoding="utf-8") as handle:
        output = handle.read().lower()
    passed = all(f"option {label}" in output for label in ("a", "b", "c"))
    print(f"[{'PASS' if passed else 'FAIL'}] Three source options preserved: {output_path}")
    return passed


def verify_trace_artifacts():
    latest_path = Path("logs/run_trace_latest.json")
    if not latest_path.exists():
        print("[FAIL] Latest trace JSON exists")
        return False
    with latest_path.open("r", encoding="utf-8") as handle:
        trace = json.load(handle)
    artifact_path = Path(trace.get("trace_artifact_json", ""))
    checks = [
        ("Latest trace JSON exists", latest_path.exists()),
        ("Trace has unique run ID", bool(trace.get("run_id"))),
        ("Per-run trace JSON exists", artifact_path.is_file()),
        ("Trace records composition route", trace.get("composition_route") in {"PASS", "REPAIR", "FALLBACK"}),
        ("Trace records decision boundary", trace.get("decision_boundary") in {"CLEAR", "BACKPRESSURE"}),
    ]
    for label, passed in checks:
        print(f"[{'PASS' if passed else 'FAIL'}] {label}")
    return all(passed for _, passed in checks)


def main():
    os.makedirs("sample_outputs", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    tests = [
        {
            "name": "Deterministic Baseline",
            "cmd": [sys.executable, "app.py", "--input", "sample_inputs/ai_agent_adoption_pre_read.md", "--output", "sample_outputs/test_deterministic.md"],
            "expected_markers": ("Composition Route: PASS", "Decision Boundary: BACKPRESSURE"),
        },
        {
            "name": "Mock LLM Valid Path",
            "cmd": [sys.executable, "app.py", "--input", "sample_inputs/ai_agent_adoption_pre_read.md", "--output", "sample_outputs/test_mock_valid.md", "--mock-llm", "--trace", "--strict"],
            "expected_markers": ("Composition Route: PASS", "Decision Boundary: BACKPRESSURE"),
        },
        {
            "name": "Mock LLM Invalid Fallback Path",
            "cmd": [sys.executable, "app.py", "--input", "sample_inputs/invalid_fake_recommendation.md", "--output", "sample_outputs/test_mock_invalid.md", "--mock-llm", "--trace", "--strict"],
            "expected_markers": ("Composition Route: FALLBACK", "Decision Boundary: CLEAR"),
        },
        {
            "name": "Custom Pre-read Mock LLM Boardroom Quality",
            "cmd": [sys.executable, "app.py", "--input", "sample_inputs/custom_pre_read.md", "--output", "sample_outputs/custom_decision_briefing.md", "--mock-llm", "--trace", "--strict"],
            "expected_markers": ("Composition Route: PASS", "Decision Boundary: BACKPRESSURE"),
        },
        {
            "name": "Custom Pre-read Deterministic Boardroom Quality",
            "cmd": [sys.executable, "app.py", "--input", "sample_inputs/custom_pre_read.md", "--output", "sample_outputs/custom_decision_briefing_deterministic.md", "--strict"],
            "expected_markers": ("Composition Route: PASS", "Decision Boundary: BACKPRESSURE"),
        },
        {
            "name": "Warehouse Productivity Non-AI Probe",
            "cmd": [sys.executable, "app.py", "--input", "sample_inputs/warehouse_productivity_update.md", "--output", "sample_outputs/warehouse_productivity_update_briefing.md", "--mock-llm", "--trace", "--strict"],
            "expected_markers": ("Decision Gravity: Low", "Composition Route: PASS", "Decision Boundary: CLEAR"),
            "forbidden_markers": ("SEMANTIC BACKPRESSURE TRIGGERED",),
        },
        {
            "name": "Office Lease Non-AI Probe",
            "cmd": [sys.executable, "app.py", "--input", "sample_inputs/office_lease_decision.md", "--output", "sample_outputs/office_lease_decision_briefing.md", "--mock-llm", "--trace", "--strict"],
            "expected_markers": ("Composition Route: PASS", "Decision Boundary: CLEAR"),
            "forbidden_markers": ("SEMANTIC BACKPRESSURE TRIGGERED",),
        },
        {
            "name": "Neutral Informational Memo Routing",
            "cmd": [sys.executable, "app.py", "--input", "sample_inputs/neutral_informational_memo.md", "--output", "sample_outputs/neutral_informational_memo_briefing.md", "--mock-llm", "--trace", "--strict"],
            "expected_markers": ("Decision Gravity: Low", "Composition Route: PASS", "Decision Boundary: CLEAR", "Pipeline Outcome: PASS"),
            "forbidden_markers": ("SEMANTIC BACKPRESSURE TRIGGERED",),
        },
        {
            "name": "Novel Three-Option Non-AI Fallback",
            "cmd": [sys.executable, "app.py", "--input", "sample_inputs/novel_three_option_non_ai_decision.md", "--output", "sample_outputs/novel_three_option_non_ai_decision_briefing.md", "--mock-llm", "--trace", "--strict"],
            "expected_markers": ("Composition Route: FALLBACK", "Decision Boundary: CLEAR", "Pipeline Outcome: FALLBACK"),
            "forbidden_markers": ("SEMANTIC BACKPRESSURE TRIGGERED",),
        },
    ]
    failures = 0
    if not run_schema_boundary_regressions():
        failures += 1
    if not run_minimal_gate_regressions():
        failures += 1
    if not run_independent_scenario_corpus(
        "Security Evaluation Corpus",
        "eval/security_eval_cases.json",
    ):
        failures += 1
    if not run_independent_scenario_corpus(
        "Source Faithfulness Corpus",
        "eval/source_faithfulness_cases.json",
    ):
        failures += 1
    for test in tests:
        if not run_test(
            test["name"],
            test["cmd"],
            test.get("expected_markers", ()),
            test.get("forbidden_markers", ()),
        ):
            failures += 1
    for probe_output in (
        "sample_outputs/warehouse_productivity_update_briefing.md",
        "sample_outputs/office_lease_decision_briefing.md",
        "sample_outputs/neutral_informational_memo_briefing.md",
        "sample_outputs/novel_three_option_non_ai_decision_briefing.md",
    ):
        if not probe_excludes_ai_governance(probe_output):
            failures += 1
    if not probe_preserves_three_options("sample_outputs/novel_three_option_non_ai_decision_briefing.md"):
        failures += 1
    if not verify_trace_artifacts():
        failures += 1
    print("\n======================================")
    if failures == 0:
        print("Strict schema boundary, independent scenario evaluation, structural contracts, and three minimal quality gates passed.")
    else:
        print(f"{failures} Test(s) Failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
