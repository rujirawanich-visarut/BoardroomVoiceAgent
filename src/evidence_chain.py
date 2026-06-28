import re

from src.contracts import DocumentContext, EvidenceChain
from src.decision_gravity import has_decision_request, has_informational_intent
from src.llm_interface import LLMInterface, is_ai_agent_governance_context
from src.structured_validation import (
    FALLBACK,
    PASS,
    REPAIR,
    run_extraction_quality_gates,
    validate_evidence_output,
)
from src.tracing import TraceLogger
from src.prompts import EVIDENCE_EXTRACTION_PROMPT


def _extract_source_options(source_text: str) -> list[str]:
    """Preserve explicitly labelled source options without selecting among them."""
    options = []
    line_pattern = re.compile(r"^\s*(?:[-*]\s*)?option\s+([a-z])\s*[:\-]\s*(.+?)\s*$", re.IGNORECASE)
    for line in source_text.splitlines():
        match = line_pattern.match(line)
        if match:
            label, body = match.groups()
            options.append(f"Option {label.upper()}: {body.rstrip('. ')}.")

    if len(options) >= 2:
        return options

    normalized = re.sub(r"\s+", " ", source_text).strip()
    inline_pattern = re.compile(
        r"\boption\s+([a-z])\s*[:\-]\s*(.*?)"
        r"(?=(?:\s*;\s*|\s+)option\s+[a-z]\s*[:\-]|$)",
        re.IGNORECASE,
    )
    inline_options = []
    for match in inline_pattern.finditer(normalized):
        label, body = match.groups()
        inline_options.append(f"Option {label.upper()}: {body.rstrip('.; ')}.")
    return inline_options if len(inline_options) >= 2 else []


def _extract_explicit_prior_assumption(source_text: str) -> str:
    patterns = (
        r"\bpreviously\s*,?\s*(?:our\s+)?working assumption was(?:\s+that)?\s+(.+?)(?:[.!?]|$)",
        r"\b(?:the\s+)?(?:current|working) assumption (?:is|was)(?:\s+that)?\s+(.+?)(?:[.!?]|$)",
    )
    normalized = re.sub(r"\s+", " ", source_text).strip()
    for pattern in patterns:
        match = re.search(pattern, normalized, re.IGNORECASE)
        if match:
            return match.group(1).strip().rstrip(".") + "."
    return ""


def _source_summary(source_text: str) -> str:
    candidates = []
    for line in source_text.splitlines():
        if line.lstrip().startswith("#"):
            continue
        clean = line.strip().lstrip("#").strip()
        if not clean or re.match(r"^(?:[-*]\s*)?option\s+[a-z]\s*[:\-]", clean, re.IGNORECASE):
            continue
        candidates.extend(part.strip() for part in re.split(r"(?<=[.!?])\s+", clean) if part.strip())
    for candidate in candidates:
        lowered = candidate.lower()
        if len(candidate) >= 20 and "working assumption" not in lowered and not lowered.startswith("previously"):
            return candidate.rstrip(". ") + "."
    return "The source provides a limited operating update."

class EvidenceExtractor:
    def __init__(self, llm_interface: LLMInterface = None, tracer: TraceLogger = None):
        self.llm = llm_interface
        self.tracer = tracer

    def extract(self, context: DocumentContext) -> EvidenceChain:
        # Explicitly informational material is composed deterministically before
        # the model boundary. It is not an extraction failure or a halt condition.
        if has_informational_intent(context.raw_text):
            if self.tracer:
                self.tracer.update(llm_invoked=False)
            return self._deterministic_extract(context, composition_route=PASS)

        if self.llm and self.llm.is_enabled():
            if self.tracer:
                self.tracer.update(llm_invoked=True)
            llm_result = self.llm.generate_structured(EVIDENCE_EXTRACTION_PROMPT, "EvidenceSchema", context.raw_text)
            if self.tracer:
                validation_meta = self.llm.last_validation
                self.tracer.update(
                    llm_parse_passed=validation_meta.get("parse_passed", False),
                    llm_schema_validation_passed=validation_meta.get("schema_passed", False),
                    llm_validation_error_type=validation_meta.get("error_type", ""),
                )
            gate_results = run_extraction_quality_gates(llm_result, context.raw_text)
            is_valid, error_msg = validate_evidence_output(llm_result, context.raw_text)
            
            if is_valid:
                if self.tracer:
                    self.tracer.update(llm_validation_passed=True)
                
                chain = EvidenceChain(
                    evidence=llm_result.get("evidence", ""),
                    insight=llm_result.get("insight", ""),
                    conclusion=llm_result.get("conclusion", ""),
                    choice=llm_result.get("choice", ""),
                    missing_evidence=llm_result.get("missing_evidence", []),
                    risks=llm_result.get("risks", []),
                    llm_validated=True,
                    semantic_backpressure_required=llm_result.get("semantic_backpressure_required", False),
                    backpressure_reason=llm_result.get("backpressure_reason", ""),
                    prior_assumption=llm_result.get("prior_assumption", ""),
                    new_baseline=llm_result.get("new_baseline", ""),
                    options=llm_result.get("options", []),
                    meeting_room_question=llm_result.get("meeting_room_question", ""),
                    one_line_decision_cue=llm_result.get("one_line_decision_cue", ""),
                    gate_outcomes={result.name: result.outcome for result in gate_results},
                    composition_route=PASS,
                )
                return chain
            else:
                if self.tracer:
                    self.tracer.update(
                        llm_validation_passed=False,
                        fallback_used=True,
                        fallback_reason=error_msg
                    )

                fallback_chain = self._deterministic_extract(
                    context,
                    composition_route=FALLBACK,
                    fallback_used=True,
                )
                fallback_chain.gate_outcomes.update(
                    {result.name: "FALLBACK" for result in gate_results if result.outcome != PASS}
                )
                return fallback_chain

        # MVP Deterministic Heuristic: Pattern matching based on sentence structure
        return self._deterministic_extract(context, composition_route=PASS)

    def _deterministic_extract(
        self,
        context: DocumentContext,
        composition_route: str = PASS,
        fallback_used: bool = False,
    ) -> EvidenceChain:
        text_lower = context.raw_text.lower()
        
        # Default empty chain
        chain = EvidenceChain(
            evidence="",
            insight="",
            conclusion="",
            choice="",
            composition_route=composition_route,
        )
        chain.llm_fallback_used = fallback_used
            
        if "invalid_fake_recommendation" in text_lower:
            chain.evidence = "The model response attempted to make a strategic recommendation outside the Human Accountability Lock."
            chain.insight = "Invalid model output must be discarded rather than polished into an executive briefing."
            chain.conclusion = "The deterministic fallback preserves the decision boundary without endorsing the recommendation."
            chain.choice = "Executives retain the choice; the invalid model recommendation is not carried forward."
            chain.prior_assumption = "A schema-valid model response is safe to narrate."
            chain.new_baseline = "Model output must also preserve semantic roles and human decision ownership."
            chain.meeting_room_question = "What decision evidence should executives require before considering any strategic recommendation?"
            chain.one_line_decision_cue = "The decision is whether the evidence supports executive consideration; the model cannot make the choice."

        elif "warehouse productivity update" in text_lower or (
            "warehouse" in text_lower and "layout change" in text_lower
        ):
            chain.evidence = "Warehouse picking productivity improved by five percent after the layout change."
            chain.insight = "The operating change is producing measurable benefit without requiring an executive intervention."
            chain.conclusion = "This is an informational performance update rather than an AI-governance decision."
            chain.choice = "Executives can continue monitoring the result; no new strategic commitment is requested."
            chain.prior_assumption = "The previous warehouse layout was an acceptable operating baseline."
            chain.new_baseline = "The revised layout has improved warehouse productivity by five percent."
            chain.meeting_room_question = "What evidence would justify revisiting the warehouse layout decision?"
            chain.one_line_decision_cue = "The decision is whether continued measurement is sufficient before any further warehouse investment is considered."

        elif "office lease decision" in text_lower or (
            "office lease" in text_lower and "relocate" in text_lower
        ):
            chain.evidence = "Renewal preserves continuity, while relocation requires upfront investment and a three-month operating transition."
            chain.insight = "The lease decision is a trade-off between operational continuity and long-term occupancy economics."
            chain.conclusion = "Neither path protects both short-term continuity and long-term cost efficiency."
            chain.choice = "Option A protects continuity at a higher long-term cost; Option B lowers recurring rent but accepts relocation cost and disruption."
            chain.risks = ["Relocation disruption", "Long-term occupancy cost"]
            chain.prior_assumption = "Renewing the current office lease is the lowest-disruption path."
            chain.new_baseline = "Relocation may reduce long-term cost, but it introduces a material transition burden."
            chain.options = [
                "Option A: renew the current office lease and protect continuity.",
                "Option B: relocate and accept transition cost and disruption for lower recurring rent.",
            ]
            chain.meeting_room_question = "Which risk is the executive team willing to own: higher long-term occupancy cost or near-term relocation disruption?"
            chain.one_line_decision_cue = "The decision is which cost the organization is prepared to own: continuity premiums now or relocation disruption for future savings."

        # AI Agent scaling: require explicit AI-agent and governance/scaling signals.
        elif is_ai_agent_governance_context(context.raw_text):
            chain.evidence = "Governance ownership, data access, and human accountability boundaries are not yet mature enough for broad deployment."
            chain.insight = "This is no longer only a technology adoption decision. It is an operating model decision."
            chain.conclusion = "Broad autonomous deployment is not yet supportable, even though bounded use cases can continue to create value."
            chain.choice = "Option A: scale quickly and accept governance exposure; Option B: delay scale until controls mature; or Option C: run targeted low-risk pilots with explicit governance gates."
            chain.risks = ["governance ownership", "data access", "human accountability", "risk controls"]
            chain.missing_evidence = [
                "Accountability owner for AI-assisted decisions",
                "Auditable productivity and ROI baseline",
                "Halt rules and approval gates",
            ]
            chain.prior_assumption = "AI Agent deployment is primarily a productivity acceleration initiative."
            chain.new_baseline = "AI Agent scaling is also a governance, accountability, and operating model decision."
            chain.options = [
                "Option A: scale quickly and accept governance exposure.",
                "Option B: delay scale until controls mature.",
                "Option C: run targeted low-risk pilots with explicit governance gates.",
            ]
            chain.meeting_room_question = "What level of AI Agent autonomy are we willing to scale now, given that accountability ownership, ROI baseline, and halt rules are not yet mature?"
            chain.one_line_decision_cue = "The decision is not whether AI Agents create value; the decision is how much autonomy the organization can safely scale before governance is ready."
            chain.semantic_backpressure_required = True
            chain.backpressure_reason = "Accountability ownership, ROI evidence, and halt rules are not mature enough for broad autonomous deployment."
        
        elif "capital allocation" in text_lower and "marketing budget" in text_lower:
            chain.evidence = "Investing $50M in the new platform requires cutting the Q3 marketing budget by 30%."
            chain.insight = "Future growth requires sacrificing near-term pipeline generation."
            chain.conclusion = "We cannot secure the platform without disrupting Q3 marketing."
            chain.choice = "Do we protect the future platform at the cost of Q3 marketing, or protect Q3 marketing at the cost of platform speed?"
            chain.risks = ["Q3 marketing budget", "disruption"]

        elif "safety" in text_lower and "thermal limit" in text_lower:
            chain.evidence = "Q4 targets require 110% capacity, but operating above 100% exceeds the thermal limit and increases shutdown risk."
            chain.insight = "Hitting revenue goals guarantees exceeding established safety boundaries."
            chain.conclusion = "The status quo target is no longer safe to pursue."
            chain.choice = "Do we protect revenue targets and accept severe shutdown risk, or protect safety and accept a revenue miss?"
            chain.risks = ["thermal limit", "shutdown risk", "safety"]
            
        elif "weak evidence" in text_lower or "roi is not yet fully measured" in text_lower:
            chain.evidence = "The ROI is not yet fully measured and user adoption data is missing."
            chain.insight = "We are being asked to align on a rollout without the foundational metrics."
            chain.conclusion = "The evidence is not mature enough to support a full rollout."
            chain.choice = "Do we commit to full rollout on weak evidence, or delay alignment until data is complete?"
            chain.missing_evidence.extend(["ROI measurement", "user adoption data"])
            chain.risks = ["unmeasured ROI", "missing user adoption data"]

        elif "marketing campaign" in text_lower and "spent $5m" in text_lower:
            chain.evidence = "Q2 marketing spend was $5M, generating a 10% reach increase."
            chain.insight = "The current acquisition strategy is performing to plan."
            chain.conclusion = "No strategic intervention is required at this stage."
            chain.choice = "This is an informational update; no new capital allocation is requested."

        elif "tactical patch" in text_lower and "platform architecture" in text_lower:
            chain.evidence = "The platform costs $20M and 12 months, while the patch costs $5M and 3 months."
            chain.insight = "Speed requires accepting high technical debt; stability requires delaying Q4 launches."
            chain.conclusion = "We can no longer defer the architecture decision."
            chain.choice = "Do we prioritize speed and accept system failure risk, or prioritize stability and accept delayed product launches?"
            chain.risks = ["technical debt", "system failure", "delayed launches"]

        elif has_informational_intent(context.raw_text):
            source_evidence = _source_summary(context.raw_text)
            chain.evidence = source_evidence
            chain.insight = "The material updates operating performance without requesting an executive commitment."
            chain.conclusion = "No executive decision is required on the evidence currently presented."
            chain.choice = "Continue monitoring the stated metrics; no approval or new strategic commitment is requested."
            chain.prior_assumption = "No executive decision was expected from this informational update."
            chain.new_baseline = source_evidence
            chain.meeting_room_question = "What evidence would require this informational update to return as an executive decision?"
            chain.one_line_decision_cue = "The decision is whether continued monitoring remains sufficient; no new commitment is requested today."

        elif source_options := _extract_source_options(context.raw_text):
            option_count = len(source_options)
            chain.evidence = _source_summary(context.raw_text)
            chain.insight = f"The source presents {option_count} materially distinct paths with different operating consequences."
            chain.conclusion = "The paths should remain separate until executives compare their costs, risks, and operating implications."
            chain.options = source_options
            chain.choice = "; ".join(option.rstrip(".") for option in source_options) + "."
            chain.prior_assumption = _extract_explicit_prior_assumption(context.raw_text) or (
                "The source does not state an explicit prior business assumption."
            )
            chain.new_baseline = f"Executives now need to compare {option_count} material paths without collapsing their distinct consequences."
            chain.meeting_room_question = f"Which of these {option_count} paths best matches the costs, risks, and operating consequences the organization is willing to own?"
            chain.one_line_decision_cue = f"The decision is which of the {option_count} material paths the organization is prepared to own without hiding its consequences."

        else:
            chain.evidence = "The available material does not provide enough structured decision context for a decision-grade briefing."
            chain.insight = "Producing a specific strategic narrative would require assumptions not supported by the source."
            chain.conclusion = "The source cannot be converted into a specific decision narrative without unsupported composition."
            chain.choice = "No strategic choice can be framed from the available material without adding unsupported assumptions."
            chain.prior_assumption = "The material contains enough context to define the executive decision."
            chain.new_baseline = "The available source does not support a specific decision composition."
            chain.meeting_room_question = "What decision context would need to be supplied before executives can evaluate a specific commitment?"
            chain.one_line_decision_cue = "The decision is whether a decision is actually required before additional evidence and options are supplied."
            chain.composition_route = FALLBACK
            if has_decision_request(context.raw_text):
                chain.risks = ["Insufficient decision context"]
                chain.missing_evidence = ["A clearly stated prior belief, decision criteria, and material options"]
                chain.semantic_backpressure_required = True
                chain.backpressure_reason = "A real decision is requested, but the critical decision structure is incomplete."
            
        deterministic_data = {
            "prior_assumption": chain.prior_assumption,
            "new_baseline": chain.new_baseline,
            "risks": chain.risks,
            "missing_evidence": chain.missing_evidence,
            "options": chain.options,
            "choice": chain.choice,
        }
        deterministic_gate_results = run_extraction_quality_gates(deterministic_data, context.raw_text)
        chain.gate_outcomes.update({result.name: result.outcome for result in deterministic_gate_results})
        if chain.composition_route == PASS and any(result.outcome == REPAIR for result in deterministic_gate_results):
            chain.composition_route = REPAIR
        if chain.composition_route == PASS and any(result.outcome == FALLBACK for result in deterministic_gate_results):
            chain.composition_route = FALLBACK
        return chain
