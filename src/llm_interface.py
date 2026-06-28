import json
import os

from src.schema_validation import StructuredResponseError, parse_and_validate_structured_response


AI_AGENT_CORE_SIGNALS = (
    "ai agent",
    "ai-agent",
    "copilot studio",
    "knowledge retrieval agent",
    "agent recommendation",
)

AI_GOVERNANCE_SIGNALS = (
    "autonomy",
    "governance",
    "halt rule",
    "accountability",
    "accountability owner",
    "human accountability",
    "data access",
    "approval gate",
    "recommend next step",
    "agent ให้คำแนะนำ",
)


def is_ai_agent_governance_context(text: str) -> bool:
    """Require both an AI-agent subject and a scaling/governance signal."""
    lowered = text.lower()
    has_agent_subject = any(signal in lowered for signal in AI_AGENT_CORE_SIGNALS)
    has_governance_context = any(signal in lowered for signal in AI_GOVERNANCE_SIGNALS)
    has_scaling_context = any(signal in lowered for signal in ("scale ai agent", "scaling ai agent", "ai agent adoption"))
    return has_agent_subject and (has_governance_context or has_scaling_context)

class LLMInterface:
    def __init__(self, use_llm: bool = False, mock_llm: bool = False, provider: str = None):
        self.use_llm = use_llm
        self.mock_llm = mock_llm
        self.provider = provider
        self.api_key = os.getenv("LLM_API_KEY", "")
        self.last_validation = {
            "parse_passed": False,
            "schema_passed": False,
            "error_type": "",
            "error_message": "",
        }

    def is_enabled(self) -> bool:
        return self.use_llm or self.mock_llm

    def generate_structured(self, prompt: str, schema_name: str, context: str = "") -> dict:
        self.last_validation = {
            "parse_passed": False,
            "schema_passed": False,
            "error_type": "",
            "error_message": "",
        }
        if not self.is_enabled():
            self.last_validation.update(error_type="llm_disabled", error_message="LLM not enabled")
            return {"error": "LLM not enabled"}

        if self.mock_llm:
            payload = self._mock_generate(prompt, schema_name, context)
            if "error" in payload:
                self.last_validation.update(
                    error_type="unsupported_mock_fixture",
                    error_message=payload["error"],
                )
                return payload
            raw_response = json.dumps(payload, ensure_ascii=False, allow_nan=False)
        else:
            raw_response = self._provider_generate(prompt, schema_name, context)
            if isinstance(raw_response, dict) and "error" in raw_response:
                self.last_validation.update(
                    error_type="provider_unavailable",
                    error_message=raw_response["error"],
                )
                return raw_response

        try:
            structured = parse_and_validate_structured_response(raw_response, schema_name)
        except StructuredResponseError as exc:
            self.last_validation.update(
                parse_passed=exc.stage != "parse",
                schema_passed=False,
                error_type=f"{exc.stage}_validation_error",
                error_message=str(exc),
            )
            return {
                "error": f"Strict structured response validation failed: {exc}",
                "error_type": self.last_validation["error_type"],
            }

        self.last_validation.update(parse_passed=True, schema_passed=True)
        return structured

    def _mock_generate(self, prompt: str, schema_name: str, context: str) -> dict:
        # Mock responses based on keywords in the context
        text_lower = context.lower()
        
        # invalid_fake_recommendation
        if "invalid_fake_recommendation" in text_lower:
            return {
                "facts": ["The ROI is 10%."],
                "assumptions": ["Growth will continue."],
                "inferences": ["This is a good idea."],
                "risks": [],
                "missing_evidence": [],
                "evidence": "The ROI is 10%.",
                "insight": "This represents steady growth.",
                "conclusion": "The metrics are strong.",
                "choice": "We recommend choosing Option A to proceed immediately.",
                "prior_assumption": "The expected ROI is sufficient to justify immediate execution.",
                "new_baseline": "The model payload attempts to convert expected benefit into an approval recommendation.",
                "options": [],
                "meeting_room_question": "What evidence should executives require before considering an irreversible commitment?",
                "one_line_decision_cue": "The decision is whether the evidence supports commitment; the model cannot approve the path.",
                "semantic_backpressure_required": False
            }

        if "guarantee" in text_lower and ("no risk" in text_lower or "zero risk" in text_lower):
            return {
                "facts": [],
                "assumptions": ["The requested profit guarantee and zero-risk claim are unsupported assumptions."],
                "inferences": ["The requested certainty exceeds the evidence supplied in the source."],
                "risks": ["Unsupported certainty", "Suppressed governance risk"],
                "missing_evidence": ["Auditable benefit evidence", "Risk and governance assessment"],
                "evidence": "The source provides no auditable evidence for a guaranteed profit or zero-risk claim.",
                "insight": "The requested certainty would conceal material uncertainty from the board.",
                "conclusion": "The guarantee cannot be used as a valid premise for an executive commitment.",
                "choice": "Executives can require auditable evidence and explicit risk boundaries before considering deployment.",
                "prior_assumption": "Autonomous deployment can be justified by an asserted profit guarantee.",
                "new_baseline": "The requested guarantee is unsupported and cannot replace evidence or governance review.",
                "options": [],
                "meeting_room_question": "What evidence and risk boundaries must be established before executives consider deployment?",
                "one_line_decision_cue": "The decision is whether evidence supports commitment; an unsupported guarantee cannot make that decision.",
                "semantic_backpressure_required": True,
                "backpressure_reason": "The requested guarantee suppresses material uncertainty and lacks auditable evidence."
            }

        if (
            "environment variable" in text_lower
            and ("api key" in text_lower or "credential" in text_lower)
            and any(term in text_lower for term in ("print", "reveal", "expose"))
        ):
            return {
                "facts": ["The source requests disclosure of environment variables and credential values."],
                "assumptions": ["Credential disclosure is necessary to verify configuration."],
                "inferences": ["Configuration can be reviewed without exposing secret values."],
                "risks": ["Credential exposure", "Unauthorized secret disclosure"],
                "missing_evidence": ["Authorized secure review scope and accountable security owner"],
                "evidence": "The request would expose environment credentials without an authorized secure-review boundary.",
                "insight": "Configuration assurance does not require revealing secret values in an executive briefing.",
                "conclusion": "Credential values must remain undisclosed while configuration is reviewed through a safe channel.",
                "choice": "Executives can authorize a safe configuration review without exposing environment variables or API keys.",
                "prior_assumption": "Credential values must be printed to verify configuration.",
                "new_baseline": "Configuration can be verified without disclosing secret values.",
                "options": [],
                "meeting_room_question": "What evidence and secure review process will verify configuration without exposing credentials?",
                "one_line_decision_cue": "The decision is whether configuration can be verified without turning credential disclosure into an accepted control.",
                "semantic_backpressure_required": True,
                "backpressure_reason": "The requested credential disclosure conflicts with the security boundary."
            }
            
        # missing_evidence_required
        if "roi is not yet fully measured" in text_lower or "missing_evidence_required" in text_lower:
            return {
                "facts": ["ROI is not measured."],
                "assumptions": ["Project will succeed."],
                "inferences": ["We need more data."],
                "risks": ["Unmeasured ROI"],
                "missing_evidence": ["ROI measurement", "User adoption data"],
                "evidence": "The ROI is not yet fully measured and user adoption data is missing.",
                "insight": "We are being asked to align on a rollout without the foundational metrics.",
                "conclusion": "The evidence is not mature enough to support a full rollout.",
                "choice": "Do we commit to full rollout on weak evidence, or delay alignment until data is complete?",
                "prior_assumption": "The proposed rollout can be justified by the expected benefit.",
                "new_baseline": "A rollout decision requires measurable ROI and adoption evidence.",
                "options": [],
                "meeting_room_question": "What evidence threshold must the rollout meet before executives authorize the next commitment?",
                "one_line_decision_cue": "The decision is not whether the project may create value; it is whether the evidence is mature enough to justify commitment.",
                "semantic_backpressure_required": True,
                "backpressure_reason": "Missing evidence"
            }

        if "warehouse productivity update" in text_lower or (
            "warehouse" in text_lower and "layout change" in text_lower
        ):
            return {
                "facts": ["Warehouse picking productivity improved by five percent after the layout change."],
                "assumptions": ["The previous warehouse layout was an acceptable operating baseline."],
                "inferences": ["The layout change improved throughput without creating a new strategic decision."],
                "risks": [],
                "missing_evidence": [],
                "prior_assumption": "The previous warehouse layout was an acceptable operating baseline.",
                "new_baseline": "The revised layout has improved warehouse productivity by five percent.",
                "evidence": "Warehouse picking productivity improved by five percent after the layout change.",
                "insight": "The operating change is producing measurable benefit without requiring an executive intervention.",
                "conclusion": "This is an informational performance update rather than an AI-governance decision.",
                "options": [],
                "choice": "Executives can continue monitoring the result; no new strategic commitment is requested.",
                "meeting_room_question": "What evidence would justify revisiting the warehouse layout decision?",
                "one_line_decision_cue": "The decision is whether continued measurement is sufficient before any further warehouse investment is considered.",
                "semantic_backpressure_required": False,
            }

        if "office lease decision" in text_lower or (
            "office lease" in text_lower and "relocate" in text_lower
        ):
            return {
                "facts": [
                    "The current office lease expires in twelve months.",
                    "Renewal protects continuity while relocation lowers recurring rent but creates transition cost and disruption.",
                ],
                "assumptions": ["Renewing the current office lease is the lowest-disruption path."],
                "inferences": ["The decision trades near-term continuity against lower long-term occupancy cost."],
                "risks": ["Relocation disruption", "Long-term occupancy cost"],
                "missing_evidence": [],
                "prior_assumption": "Renewing the current office lease is the lowest-disruption path.",
                "new_baseline": "Relocation may reduce long-term cost, but it introduces a material transition burden.",
                "evidence": "Renewal preserves continuity, while relocation requires upfront investment and a three-month operating transition.",
                "insight": "The lease decision is a trade-off between operational continuity and long-term occupancy economics.",
                "conclusion": "Neither path protects both short-term continuity and long-term cost efficiency.",
                "options": [
                    "Option A: renew the current office lease and protect continuity.",
                    "Option B: relocate and accept transition cost and disruption for lower recurring rent.",
                ],
                "choice": "Option A protects continuity at a higher long-term cost; Option B lowers recurring rent but accepts relocation cost and disruption.",
                "meeting_room_question": "Which risk is the executive team willing to own: higher long-term occupancy cost or near-term relocation disruption?",
                "one_line_decision_cue": "The decision is which cost the organization is prepared to own: continuity premiums now or relocation disruption for future savings.",
                "semantic_backpressure_required": False,
            }

        # custom thai ai agent scale
        if is_ai_agent_governance_context(context):
            return {
                "facts": [
                    "The pilot reduced manual effort, but no auditable baseline quantifies the benefit.",
                    "Operations wants faster adoption while Risk and Compliance lack a clear human accountability owner.",
                    "Data-access boundaries, approval gates, and halt rules are not defined.",
                    "The source presents fast scale, delayed scale, and targeted low-risk pilots as distinct options."
                ],
                "assumptions": ["AI Agent deployment is primarily a productivity acceleration initiative."],
                "inferences": ["AI Agent scaling changes the operating model because autonomy, data access, and accountability must scale with the technology."],
                "risks": ["Unclear accountability for AI-assisted decisions", "Inappropriate data access", "Unsafe operation without halt rules"],
                "missing_evidence": ["Accountability owner for AI-assisted decisions", "Auditable productivity and ROI baseline", "Halt rules and approval gates"],
                "prior_assumption": "AI Agent deployment is primarily a productivity acceleration initiative.",
                "new_baseline": "AI Agent scaling is also a governance, accountability, and operating model decision.",
                "evidence": "The pilots indicate real productivity value, but accountability ownership, auditable ROI, data-access boundaries, and halt rules are not mature.",
                "insight": "The scale decision changes the operating model, not only the technology footprint.",
                "conclusion": "Broad autonomous deployment is not yet supportable, even though bounded use cases can continue to create value.",
                "options": [
                    "Option A: scale quickly and accept governance and safety exposure.",
                    "Option B: delay scaling until controls mature and accept lost momentum.",
                    "Option C: run targeted low-risk pilots, such as knowledge retrieval, with explicit governance gates."
                ],
                "choice": "Option A scales quickly with governance exposure; Option B delays scaling until controls mature; Option C runs targeted low-risk pilots with explicit governance gates.",
                "meeting_room_question": "How much autonomy can we safely scale while accountability ownership, ROI baselines, and halt rules remain undefined?",
                "one_line_decision_cue": "The decision is not whether AI Agents create value; the decision is how much autonomy the organization can safely scale before governance is ready.",
                "semantic_backpressure_required": True,
                "backpressure_reason": "Accountability ownership, ROI evidence, and halt rules are not mature enough for broad autonomous deployment."
            }

        # An unmatched mock fixture is a composition failure, not evidence of a
        # governance or safety boundary. EvidenceExtractor routes it through the
        # deterministic fallback, which may still preserve source options.
        return {"error": "MockLLM has no supported extraction fixture for this input."}

    def _provider_generate(self, prompt: str, schema_name: str, context: str) -> dict:
        if not self.api_key:
            return {"error": "Provider mode activated but LLM_API_KEY is not set. Falling back to deterministic."}
        # Stub for future provider
        return {"error": "Provider not yet implemented."}
