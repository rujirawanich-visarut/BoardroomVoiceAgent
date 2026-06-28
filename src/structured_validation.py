import re
from dataclasses import dataclass, field


PASS = "PASS"
REPAIR = "REPAIR"
FALLBACK = "FALLBACK"
BACKPRESSURE = "BACKPRESSURE"

SEMANTIC_ROLE_INTEGRITY = "Semantic Role Integrity"
DECISION_TOPOLOGY_PRESERVATION = "Decision Topology Preservation"
SPOKEN_DECISION_COHERENCE = "Spoken Decision Coherence"

RISK_AS_ASSUMPTION_PATTERNS = (
    "unclear accountability",
    "missing evidence",
    "halt rule",
    "ความรับผิดชอบคลุมเครือ",
)

OPTION_STOPWORDS = {
    "option", "the", "and", "or", "with", "without", "for", "from", "into", "until",
    "can", "we", "accept", "protect", "current", "explicit", "resulting", "such", "than",
}


@dataclass(frozen=True)
class GateResult:
    name: str
    outcome: str
    reasons: list[str] = field(default_factory=list)


def _normalise(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def _meaningful_tokens(value: str) -> set[str]:
    tokens = re.findall(r"[a-z0-9]+|[\u0E00-\u0E7F]+", _normalise(value))
    return {token for token in tokens if len(token) > 2 and token not in OPTION_STOPWORDS}


def _explicitly_stated_as_prior(assumption: str, source_text: str) -> bool:
    source = _normalise(source_text)
    needle = _normalise(assumption)
    index = source.find(needle)
    if index < 0:
        return False
    lead_in = source[max(0, index - 120):index]
    return any(marker in lead_in for marker in ("previously", "working assumption", "until now", "เดิม", "สมมติฐาน"))


def semantic_role_integrity(data: dict, source_text: str = "") -> GateResult:
    """Gate 1: keep prior belief, changed baseline, risks, and missing evidence in their proper roles."""
    assumption = _normalise(data.get("prior_assumption", ""))
    baseline = _normalise(data.get("new_baseline", ""))
    risks = {_normalise(item) for item in data.get("risks", [])}
    missing = {_normalise(item) for item in data.get("missing_evidence", [])}

    if not assumption or not baseline:
        return GateResult(
            SEMANTIC_ROLE_INTEGRITY,
            REPAIR,
            ["Prior assumption or changed baseline requires deterministic composition."],
        )

    risk_pattern = any(pattern in assumption for pattern in RISK_AS_ASSUMPTION_PATTERNS) or bool(
        re.search(r"\brisk\b.{0,60}\b(?:mitigat\w*|resolv\w*|eliminat\w*|controlled)\b", assumption)
    )
    role_values = risks | missing
    role_collision = assumption == baseline or any(
        assumption == value
        or (len(value) >= 12 and value in assumption)
        or (len(assumption) >= 12 and assumption in value)
        for value in role_values
    )
    if (risk_pattern and not _explicitly_stated_as_prior(assumption, source_text)) or role_collision:
        return GateResult(
            SEMANTIC_ROLE_INTEGRITY,
            FALLBACK,
            ["A risk, missing-evidence item, or changed baseline was used as the prior business belief."],
        )

    return GateResult(SEMANTIC_ROLE_INTEGRITY, PASS)


def _source_has_three_paths(source_text: str) -> bool:
    source = _normalise(source_text)
    explicit = set(re.findall(r"\boption\s+([abc])\b", source)) == {"a", "b", "c"}
    ai_scale_paths = (
        ("scale ai agent" in source or "ai agent" in source)
        and "targeted pilot" in source
        and ("หยุดรอ governance" in source or "delay" in source or "wait for governance" in source)
    )
    return explicit or ai_scale_paths


def decision_topology_preservation(data: dict, source_text: str = "") -> GateResult:
    """Gate 2: preserve the material executive paths without choosing one for the board."""
    choice = _normalise(data.get("choice", ""))
    options = data.get("options", []) or []
    final_decision_terms = (
        "we recommend choosing",
        "the final decision is",
        "we will proceed with",
        "recommend proceeding with",
    )
    if not choice or any(term in choice for term in final_decision_terms):
        return GateResult(
            DECISION_TOPOLOGY_PRESERVATION,
            FALLBACK,
            ["The choice is missing or makes the final strategic decision for executives."],
        )

    expects_three = _source_has_three_paths(source_text) or len(options) >= 3
    labelled_choice = all(f"option {label}" in choice for label in ("a", "b", "c"))
    option_coverage = []
    choice_tokens = _meaningful_tokens(choice)
    for option in options[:3]:
        option_tokens = _meaningful_tokens(option)
        required_overlap = min(2, len(option_tokens))
        option_coverage.append(required_overlap > 0 and len(option_tokens & choice_tokens) >= required_overlap)
    preserves_three = len(options) >= 3 and (labelled_choice or all(option_coverage))
    if expects_three and not preserves_three:
        return GateResult(
            DECISION_TOPOLOGY_PRESERVATION,
            FALLBACK,
            ["Three material paths in the source were collapsed or omitted."],
        )

    return GateResult(DECISION_TOPOLOGY_PRESERVATION, PASS)


def run_extraction_quality_gates(data: dict, source_text: str = "") -> list[GateResult]:
    return [
        semantic_role_integrity(data, source_text),
        decision_topology_preservation(data, source_text),
    ]


def validate_evidence_output(data: dict, source_text: str = "") -> tuple[bool, str]:
    if "error" in data:
        return False, data["error"]

    for field_name in ("evidence", "insight", "conclusion", "choice"):
        if not data.get(field_name):
            return False, f"Missing required field: {field_name}"

    for result in run_extraction_quality_gates(data, source_text):
        # REPAIR is valid for deterministic composition, but an LLM response that
        # needs semantic repair is routed through the deterministic fallback.
        if result.outcome != PASS:
            reason = result.reasons[0] if result.reasons else "Gate did not pass."
            return False, f"{result.name} -> {result.outcome}: {reason}"

    return True, ""
