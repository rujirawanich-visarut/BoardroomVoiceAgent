from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class DocumentContext:
    raw_text: str
    paragraphs: List[str]

@dataclass
class DecisionGravityResult:
    gravity: str  # "Low", "Medium", "High"
    triggers: List[str]

@dataclass
class EvidenceChain:
    evidence: str
    insight: str
    conclusion: str
    choice: str
    missing_evidence: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    llm_validated: bool = False
    llm_fallback_used: bool = False
    semantic_backpressure_required: bool = False
    backpressure_reason: str = ""
    prior_assumption: str = ""
    new_baseline: str = ""
    options: List[str] = field(default_factory=list)
    meeting_room_question: str = ""
    one_line_decision_cue: str = ""
    gate_outcomes: Dict[str, str] = field(default_factory=dict)
    composition_route: str = "PASS"

@dataclass
class BackpressureResult:
    triggered: bool
    severity: str  # "Low", "Medium", "High"
    rule_triggered: Optional[str]  # e.g., "Rule 1", "Rule 2", "Rule 4"
    reasons: List[str]
    missing_evidence: List[str]
    recommended_next_evidence: List[str]

@dataclass
class BoardroomBrief:
    prior_update: str
    evidence_chain: EvidenceChain
    trade_off: str
    tts_script: str
    clean_read: str
    meeting_room_question: str
    one_line_decision_cue: str
    rhythm_rationale: str
    backpressure: BackpressureResult
