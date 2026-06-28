from src.contracts import BoardroomBrief


FINAL_DECISION_TERMS = (
    "we recommend choosing",
    "the final decision is",
    "we will proceed with",
    "approve option a now",
    "approval statement confirming",
)


def _output_surface(brief: BoardroomBrief) -> str:
    chain = brief.evidence_chain
    return " ".join(
        [
            chain.prior_assumption,
            chain.new_baseline,
            chain.evidence,
            chain.insight,
            chain.conclusion,
            chain.choice,
            *chain.risks,
            *chain.missing_evidence,
            *chain.options,
            brief.meeting_room_question,
            brief.one_line_decision_cue,
            brief.tts_script,
        ]
    ).lower()


def evaluate_scenario_expectations(
    case: dict,
    source_text: str,
    gravity: str,
    brief: BoardroomBrief,
) -> list[tuple[str, bool]]:
    """Independent scenario assertions; this is an evaluation corpus, not a runtime gate."""
    chain = brief.evidence_chain
    output = _output_surface(brief)
    source = source_text.lower()
    checks = [
        ("decision gravity", gravity == case["expected_decision_gravity"]),
        ("semantic backpressure", brief.backpressure.triggered == case["expected_backpressure"]),
        ("composition route", chain.composition_route == case["expected_composition_route"]),
        ("option count", len(chain.options) == case.get("expected_option_count", len(chain.options))),
        (
            "human accountability lock",
            not any(term in output for term in FINAL_DECISION_TERMS),
        ),
    ]

    for term in case.get("required_output_terms", []):
        checks.append((f"required output term: {term}", term.lower() in output))
    for term in case.get("forbidden_output_terms", []):
        checks.append((f"forbidden output term: {term}", term.lower() not in output))

    prior = chain.prior_assumption.lower()
    for term in case.get("required_prior_terms", []):
        checks.append((f"required prior term: {term}", term.lower() in prior))
    for term in case.get("forbidden_prior_terms", []):
        checks.append((f"forbidden prior term: {term}", term.lower() not in prior))

    for term in case.get("grounding_terms", []):
        normalized = term.lower()
        checks.append((f"source contains grounding term: {term}", normalized in source))
        checks.append((f"output preserves grounding term: {term}", normalized in output))

    return checks
