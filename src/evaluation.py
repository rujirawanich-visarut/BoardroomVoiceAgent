from src.boardroom_narrator import spoken_decision_coherence
from src.contracts import BoardroomBrief
from src.structured_validation import (
    BACKPRESSURE,
    DECISION_TOPOLOGY_PRESERVATION,
    FALLBACK,
    PASS,
    REPAIR,
    SEMANTIC_ROLE_INTEGRITY,
    SPOKEN_DECISION_COHERENCE,
    decision_topology_preservation,
    semantic_role_integrity,
)


class Evaluator:
    def __init__(self):
        self.protocol_outcome = PASS
        self.composition_route = PASS
        self.decision_boundary = "CLEAR"
        self.pipeline_outcome = PASS

    def _report_check(self, label: str, passed: bool) -> int:
        print(f"[{'PASS' if passed else 'FAIL'}] {label}")
        return int(passed)

    def _composition_route(self, brief: BoardroomBrief) -> str:
        outcomes = brief.evidence_chain.gate_outcomes.values()
        if brief.evidence_chain.composition_route == FALLBACK:
            return FALLBACK
        if brief.evidence_chain.composition_route == REPAIR:
            return REPAIR
        if brief.evidence_chain.llm_fallback_used or FALLBACK in outcomes:
            return FALLBACK
        if REPAIR in outcomes:
            return REPAIR
        return PASS

    @staticmethod
    def _pipeline_outcome(composition_route: str, decision_boundary: str) -> str:
        if decision_boundary == BACKPRESSURE:
            if composition_route == PASS:
                return BACKPRESSURE
            return f"{composition_route} -> {BACKPRESSURE}"
        return composition_route

    def evaluate(
        self,
        brief: BoardroomBrief,
        context_text: str,
        trace: bool = False,
        llm_mode: bool = False,
        gravity: str = "Low",
    ) -> bool:
        chain = brief.evidence_chain

        print("\nStructural Contract Checks")
        structural_results = [
            ("Required sections present.", bool(brief.prior_update and brief.tts_script and brief.clean_read)),
            ("Evidence -> Insight -> Conclusion -> Choice present.", bool(chain.evidence and chain.insight and chain.conclusion and chain.choice)),
            ("Trade-off statement present.", bool(brief.trade_off)),
            ("Meeting Room Question present.", bool(brief.meeting_room_question)),
            ("One-Line Decision Cue present.", bool(brief.one_line_decision_cue)),
            ("TTS pause tags present.", "[PAUSE" in brief.tts_script),
            (
                "Human Accountability Lock preserved.",
                not any(
                    term in brief.tts_script.lower()
                    for term in ("we recommend choosing", "the final decision is", "we will proceed with")
                ),
            ),
        ]
        structural_passed = sum(self._report_check(label, passed) for label, passed in structural_results)

        semantic_data = {
            "prior_assumption": chain.prior_assumption,
            "new_baseline": chain.new_baseline,
            "risks": chain.risks,
            "missing_evidence": chain.missing_evidence,
            "options": chain.options,
            "choice": chain.choice,
        }
        has_real_trade_off = len(chain.options) >= 2 or any(
            marker in chain.choice.lower() for marker in (" or ", "option a", "at the cost of")
        )
        final_gate_results = [
            semantic_role_integrity(semantic_data, context_text),
            decision_topology_preservation(semantic_data, context_text),
            spoken_decision_coherence(
                brief.meeting_room_question,
                brief.one_line_decision_cue,
                brief.tts_script,
                brief.backpressure.missing_evidence,
                gravity,
                has_real_trade_off,
                chain.choice,
            ),
        ]

        print("\nMinimal Boardroom Quality Gates")
        quality_passed = 0
        for result in final_gate_results:
            final_passed = result.outcome == PASS
            routed_outcome = chain.gate_outcomes.get(result.name, PASS)
            print(f"[{'PASS' if final_passed else 'FAIL'}] {result.name} | Outcome: {routed_outcome}")
            if result.reasons:
                print(f"       {result.reasons[0]}")
            quality_passed += int(final_passed)

        self.composition_route = self._composition_route(brief)
        self.decision_boundary = BACKPRESSURE if brief.backpressure.triggered else "CLEAR"
        self.pipeline_outcome = self._pipeline_outcome(self.composition_route, self.decision_boundary)
        self.protocol_outcome = self.pipeline_outcome
        print("\nGate Outcome Protocol")
        print("PASS = acceptable | REPAIR = deterministic composition | FALLBACK = invalid model output | BACKPRESSURE = decision-integrity boundary")
        print(f"Composition Route: {self.composition_route}")
        print(f"Decision Boundary: {self.decision_boundary}")
        print(f"Pipeline Outcome: {self.pipeline_outcome}")

        total_passed = structural_passed + quality_passed
        total_checks = len(structural_results) + len(final_gate_results)
        success = total_passed == total_checks
        print(f"\nStructural Contract Result: {structural_passed}/{len(structural_results)}")
        print(f"Minimal Boardroom Quality Gate Result: {quality_passed}/{len(final_gate_results)}")
        print(f"Evaluation Result: {'PASSED' if success else 'FAILED'} ({total_passed}/{total_checks})")
        return success
