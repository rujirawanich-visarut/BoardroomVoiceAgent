import re
import textwrap

from src.contracts import EvidenceChain, BackpressureResult, BoardroomBrief
from src.structured_validation import (
    PASS,
    REPAIR,
    SPOKEN_DECISION_COHERENCE,
    GateResult,
    semantic_role_integrity,
)


MAX_TTS_LINE_LENGTH = 180
MAX_SPOKEN_TEXT_LENGTH = MAX_TTS_LINE_LENGTH - 4
ABBREVIATIONS = ("e.g.", "i.e.", "etc.", "mr.", "mrs.", "ms.", "dr.", "vs.")


def _question_is_coherent(question: str, missing_evidence: list[str]) -> bool:
    value = re.sub(r"\s+", " ", question.strip().lower())
    if len(value) < 35 or not value.endswith("?"):
        return False
    if "how do we resolve the missing evidence regarding" in value:
        return False
    exact_missing = sum(1 for item in missing_evidence if item.lower() in value)
    if exact_missing >= 2 and " and " in value:
        return False
    return any(
        term in value
        for term in (
            "what level", "which", "whether", "how much", "what risk", "what decision", "what evidence",
            "ระดับใด", "เลือก", "ยอมรับความเสี่ยง", "ตัดสินใจ",
        )
    )


def _cue_is_coherent(cue: str) -> bool:
    value = re.sub(r"\s+", " ", cue.strip().lower())
    has_decision_frame = "decision" in value or "การตัดสินใจ" in value
    return 45 <= len(value) <= 220 and has_decision_frame and any(
        term in value for term in (
            "not whether", "risk", "how much", "trade-off", "whether", "which",
            "ความเสี่ยง", "ระดับ", "เลือก",
        )
    )


def spoken_decision_coherence(
    question: str,
    cue: str,
    tts_script: str,
    missing_evidence: list[str],
    gravity: str,
    has_real_trade_off: bool,
    decision_text: str = "",
) -> GateResult:
    """Gate 3: validate the assembled spoken artifact as one coherent decision."""
    reasons = []
    if not _question_is_coherent(question, missing_evidence):
        reasons.append("Meeting Room Question is mechanical or not decision-ready.")
    if not _cue_is_coherent(cue):
        reasons.append("One-Line Decision Cue does not connect conclusion and trade-off.")
    if not tts_script or any(len(line) > MAX_TTS_LINE_LENGTH for line in tts_script.splitlines()):
        reasons.append("TTS rendering is empty or contains a line over 180 characters.")
    spoken_lines = re.findall(r'^> “(.*)”$', tts_script, re.MULTILINE)
    if any(len(line.strip()) < 12 or line.rstrip().endswith((",", ":")) for line in spoken_lines):
        reasons.append("TTS rendering contains a micro-fragment rather than a complete spoken unit.")
    if any(re.search(r"(?:\be\.g\.|\bi\.e\.)$", line.strip(), re.IGNORECASE) for line in spoken_lines):
        reasons.append("TTS rendering splits an abbreviation from the phrase it qualifies.")
    awkward_patterns = (
        r"The latest evidence changes that:\s*[\u0E00-\u0E7F]",
        r"The systemic insight is clear:\s*[\u0E00-\u0E7F]",
        r"Missing elements:\s*-",
    )
    if any(re.search(pattern, tts_script, re.IGNORECASE) for pattern in awkward_patterns):
        reasons.append("TTS rendering mechanically concatenates raw or mixed-language fields.")
    combined_decision_text = " ".join((tts_script, question, cue, decision_text))
    if re.search(r"[A-Za-z][^.!?\n]{0,160},\s*หรือ", combined_decision_text):
        reasons.append("Decision language contains raw bilingual clause concatenation.")
    pause_3_count = tts_script.count("[PAUSE 3.0s]")
    if (
        pause_3_count > 1
        or (pause_3_count == 1 and not (gravity == "High" and has_real_trade_off))
        or (gravity == "High" and has_real_trade_off and pause_3_count != 1)
    ):
        reasons.append("The decision-gravity pause is not tied to a real high-gravity trade-off.")
    if any(term in tts_script.lower() for term in ("we recommend choosing", "the final decision is", "we will proceed with")):
        reasons.append("The narration makes the final strategic choice for executives.")
    return GateResult(SPOKEN_DECISION_COHERENCE, REPAIR if reasons else PASS, reasons)


class BoardroomVoiceAgentSkill:
    def _is_ai_agent_case(self, evidence: EvidenceChain) -> bool:
        semantic_text = " ".join(
            [evidence.evidence, evidence.insight, evidence.conclusion, evidence.choice]
            + evidence.options
        ).lower()
        return "ai agent" in semantic_text or "autonomy" in semantic_text

    def _resolve_prior_assumption(self, evidence: EvidenceChain) -> str:
        candidate = evidence.prior_assumption.strip()
        role_result = semantic_role_integrity(
            {
                "prior_assumption": candidate,
                "new_baseline": evidence.new_baseline or "A changed decision baseline.",
                "risks": evidence.risks,
                "missing_evidence": evidence.missing_evidence,
            }
        )
        if candidate and role_result.outcome == PASS:
            return candidate
        if self._is_ai_agent_case(evidence):
            return "AI Agent deployment is primarily a productivity acceleration initiative."
        return "The status quo can continue to deliver the intended business outcome."

    def _resolve_new_baseline(self, evidence: EvidenceChain) -> str:
        if evidence.new_baseline.strip():
            return evidence.new_baseline.strip()
        if self._is_ai_agent_case(evidence):
            return "AI Agent scaling is also a governance, accountability, and operating model decision."
        return evidence.insight.strip() or "The decision must now account for a changed operating reality."

    def _meeting_room_question(self, evidence: EvidenceChain) -> str:
        if evidence.meeting_room_question.strip():
            return evidence.meeting_room_question.strip()
        if self._is_ai_agent_case(evidence):
            return (
                "What level of AI Agent autonomy are we willing to scale now, given that accountability "
                "ownership, ROI baseline, and halt rules are not yet mature?"
            )
        return f"Which risk are executives willing to own when choosing among these paths: {evidence.choice.rstrip('?')}?"

    def _decision_cue(self, evidence: EvidenceChain) -> str:
        if evidence.one_line_decision_cue.strip():
            return evidence.one_line_decision_cue.strip()
        if self._is_ai_agent_case(evidence):
            return (
                "The decision is not whether AI Agents create value; the decision is how much autonomy "
                "the organization can safely scale before governance is ready."
            )
        conclusion = evidence.conclusion.rstrip(". ")
        return f"{conclusion}; the decision is which risk the organization is prepared to own."

    @staticmethod
    def _protect_abbreviations(text: str) -> str:
        protected = text
        for abbreviation in ABBREVIATIONS:
            protected = re.sub(
                re.escape(abbreviation),
                lambda match: match.group(0).replace(".", "<DOT>"),
                protected,
                flags=re.IGNORECASE,
            )
        return protected

    @staticmethod
    def _balanced_chunks(text: str) -> list[str]:
        if len(text) <= MAX_SPOKEN_TEXT_LENGTH:
            return [text]
        parts = [part.strip() for part in re.split(r"(?<=[,;:])\s+", text) if part.strip()]
        if len(parts) == 1:
            return textwrap.wrap(
                text,
                width=MAX_SPOKEN_TEXT_LENGTH,
                break_long_words=False,
                break_on_hyphens=False,
            )
        chunks = []
        current = ""
        for part in parts:
            candidate = f"{current} {part}".strip()
            if not current or len(candidate) <= 140:
                current = candidate
            else:
                chunks.append(current)
                current = part
        if current:
            if chunks and len(current) < 30 and len(chunks[-1]) + len(current) + 1 <= MAX_SPOKEN_TEXT_LENGTH:
                chunks[-1] = f"{chunks[-1]} {current}"
            else:
                chunks.append(current)
        return chunks

    def _spoken_blocks(self, text: str) -> list[str]:
        """Render one spoken idea per quoted line, respecting natural linguistic boundaries."""
        clean = re.sub(r"\s+", " ", text.strip())
        if not clean:
            return []
        
        protected = self._protect_abbreviations(clean)
        ideas = [idea.replace("<DOT>", ".") for idea in re.split(r"(?<=[.!?])\s+", protected)]
        blocks = []
        for idea in ideas:
            idea = idea.strip()
            if not idea:
                continue
            
            blocks.extend(f"> “{part}”" for part in self._balanced_chunks(idea))
        return blocks

    def _append_idea(self, blocks: list[str], text: str) -> None:
        blocks.extend(self._spoken_blocks(text))

    def generate_brief(self, evidence: EvidenceChain, backpressure: BackpressureResult, gravity: str) -> BoardroomBrief:
        question_needed_repair = not _question_is_coherent(
            evidence.meeting_room_question,
            backpressure.missing_evidence,
        )
        cue_needed_repair = not _cue_is_coherent(evidence.one_line_decision_cue)
        prior_assumption = self._resolve_prior_assumption(evidence)
        new_baseline = self._resolve_new_baseline(evidence)
        evidence.prior_assumption = prior_assumption
        evidence.new_baseline = new_baseline

        if backpressure.triggered:
            baseline_status = "The decision baseline must shift before any broad or irreversible commitment."
        elif gravity == "High":
            baseline_status = "We need to rebuild the decision from this new baseline."
        else:
            baseline_status = "This updates the operating baseline."

        prior_update = "\n".join(
            [
                f"Previous assumption: {prior_assumption}",
                f"New evidence: {evidence.evidence}",
                f"New baseline: {new_baseline}",
                f"Decision implication: {baseline_status}",
            ]
        )

        trade_off = evidence.choice.strip()
        meeting_room_question = self._meeting_room_question(evidence)
        one_line_cue = self._decision_cue(evidence)
        evidence.meeting_room_question = meeting_room_question
        evidence.one_line_decision_cue = one_line_cue

        blocks: list[str] = []
        self._append_idea(blocks, f"Previously, our working assumption was: {prior_assumption}")
        blocks.append("[PAUSE 0.5s]")
        self._append_idea(blocks, "The latest evidence changes that baseline.")
        self._append_idea(blocks, new_baseline)
        blocks.append("[PAUSE 1.5s]")
        self._append_idea(blocks, evidence.evidence)
        self._append_idea(blocks, evidence.insight)
        self._append_idea(blocks, evidence.conclusion)
        blocks.append("[PAUSE 1.5s]")

        if evidence.options:
            self._append_idea(blocks, "The options are not equal.")
            for option in evidence.options:
                self._append_idea(blocks, option)
        elif gravity == "Low" and any(
            marker in trade_off.lower() for marker in ("informational", "no new strategic commitment", "continue monitoring")
        ):
            self._append_idea(blocks, "This is an informational update; no executive trade-off is required today.")
            self._append_idea(blocks, trade_off)
        else:
            self._append_idea(blocks, "Executives must now decide which risk they are willing to own.")
            self._append_idea(blocks, trade_off)

        has_real_trade_off = len(evidence.options) >= 2 or any(
            marker in trade_off.lower() for marker in (" or ", "option a", "at the cost of")
        )
        if gravity == "High" and has_real_trade_off:
            blocks.append("[PAUSE 3.0s]")
            self._append_idea(blocks, "That is the decision behind the evidence.")

        if backpressure.triggered:
            blocks.append("[PAUSE 1.5s]")
            self._append_idea(blocks, "The evidence is not yet sufficient for a final broad-scale decision.")
            self._append_idea(
                blocks,
                "The decision today is whether to authorize bounded learning while the missing controls and evidence are completed.",
            )
            for missing_item in dict.fromkeys(backpressure.missing_evidence):
                self._append_idea(blocks, f"Still required: {missing_item.rstrip('.')}.")

        tts_script = "\n\n".join(blocks)
        clean_read = "\n\n".join(block for block in blocks if not block.startswith("[PAUSE"))
        final_spoken_gate = spoken_decision_coherence(
            meeting_room_question,
            one_line_cue,
            tts_script,
            backpressure.missing_evidence,
            gravity,
            has_real_trade_off,
            trade_off,
        )
        if final_spoken_gate.outcome == PASS and (question_needed_repair or cue_needed_repair):
            evidence.gate_outcomes[SPOKEN_DECISION_COHERENCE] = REPAIR
        else:
            evidence.gate_outcomes[SPOKEN_DECISION_COHERENCE] = final_spoken_gate.outcome
        if (
            evidence.composition_route == PASS
            and evidence.gate_outcomes[SPOKEN_DECISION_COHERENCE] == REPAIR
        ):
            evidence.composition_route = REPAIR
        if gravity == "High" and has_real_trade_off:
            rhythm_rationale = (
                "The script uses complete spoken units, marks major logic transitions, and reserves "
                "[PAUSE 3.0s] for the material high-gravity trade-off."
            )
        else:
            rhythm_rationale = (
                "The script uses complete spoken units and short transition pauses. It does not apply "
                "a three-second decision-gravity pause because no high-gravity trade-off is present."
            )

        return BoardroomBrief(
            prior_update=prior_update,
            evidence_chain=evidence,
            trade_off=trade_off,
            tts_script=tts_script,
            clean_read=clean_read,
            meeting_room_question=meeting_room_question,
            one_line_decision_cue=one_line_cue,
            rhythm_rationale=rhythm_rationale,
            backpressure=backpressure,
        )
