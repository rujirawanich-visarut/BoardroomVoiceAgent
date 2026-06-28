from src.contracts import DocumentContext, EvidenceChain, BackpressureResult
from src.decision_gravity import has_decision_request

class SemanticBackpressureDetector:
    def detect(self, context: DocumentContext, evidence: EvidenceChain) -> BackpressureResult:
        # Extractors may add backpressure, but can never clear deterministic backpressure.
        extracted_backpressure = evidence.semantic_backpressure_required
        extracted_reason = evidence.backpressure_reason
        
        # Rule 1 triggers: "critical evidence missing", "human accountability owner unclear", etc.
        text_lower = context.raw_text.lower()
        decision_requested = has_decision_request(context.raw_text)
        
        triggered = False
        reasons = []
        missing = []
        rule = None
        severity = "Low"
        
        governance_gaps_present = bool(evidence.missing_evidence) and any(
            term in " ".join(evidence.risks + evidence.missing_evidence).lower()
            for term in ("accountability", "halt rule", "governance", "approval gate", "data access")
        )
        safety_boundary_present = any(
            term in " ".join(evidence.risks + evidence.missing_evidence + [extracted_reason]).lower()
            for term in ("safety", "thermal limit", "shutdown risk", "operating limit")
        )
        critical_boundary_present = bool(evidence.missing_evidence) or governance_gaps_present or safety_boundary_present

        # Check if human accountability is unclear while a real decision is requested.
        if decision_requested and "human accountability" in text_lower and "not yet mature" in text_lower:
            triggered = True
            rule = "Rule 1"
            severity = "High"
            reasons.append("Human accountability owner unclear for broad deployment.")
            missing.append("Explicit human accountability and governance boundaries.")

        ai_scaling_case = "scale ai agent" in text_lower or "ai agent adoption" in text_lower
        if decision_requested and ai_scaling_case and governance_gaps_present:
            triggered = True
            rule = "Rule 1"
            severity = "High"
            reasons.append("Accountability, evidence, and control boundaries are incomplete for broad AI Agent autonomy.")
            
        # Check for fake win-win
        if decision_requested and "win-win" in text_lower and ("cut" in text_lower or len(evidence.risks) > 0):
            triggered = True
            rule = "Rule 4"
            severity = "High"
            reasons.append("Fake win-win framing detected alongside major trade-offs or risks.")

        # Check for safety vs output collision
        if decision_requested and "safety" in text_lower and "exceeds" in text_lower and "recommend pushing" in text_lower:
            triggered = True
            rule = "Rule 4"
            severity = "High"
            reasons.append("Strategic intent conflicts with operating safety reality.")

        # Check for weak evidence
        if decision_requested and ("roi is not yet fully measured" in text_lower or "data is missing" in text_lower):
            triggered = True
            rule = "Rule 1"
            severity = "Medium"
            reasons.append("Critical evidence missing. Requested conclusion exceeds available evidence.")
            missing.append("ROI measurement and user adoption data.")

        if decision_requested and critical_boundary_present and extracted_backpressure and not triggered:
            triggered = True
            rule = "Rule 1 (Extracted)"
            severity = "High" if governance_gaps_present else "Medium"
            reasons.append(f"Semantic backpressure triggered: {extracted_reason}")

        deduplicated_missing = list(dict.fromkeys(missing + evidence.missing_evidence))
        recommended = []
        if triggered:
            if governance_gaps_present:
                recommended.extend([
                    "Assign human accountability owners",
                    "Establish an auditable value baseline",
                    "Define halt rules and approval gates",
                ])
            elif safety_boundary_present:
                recommended.extend([
                    "Confirm the operating safety boundary",
                    "Assign an accountable owner for any exception",
                ])
            else:
                recommended.append("Complete the missing decision evidence before commitment")
            
        return BackpressureResult(
            triggered=triggered,
            severity=severity,
            rule_triggered=rule,
            reasons=reasons,
            missing_evidence=deduplicated_missing,
            recommended_next_evidence=recommended
        )
