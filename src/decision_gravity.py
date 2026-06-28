import re

from src.contracts import DocumentContext, DecisionGravityResult


NEGATED_DECISION_PATTERNS = (
    r"\bno\s+(?:new\s+)?governance\s+decision\b",
    r"\bno\s+(?:executive\s+)?approval\s+(?:is\s+)?requested\b",
    r"\bnot\s+(?:a|an)\s+safety\s+issue\b",
    r"\bno\s+ai\s+agents?[^.!?\n]{0,80}\bgovernance\s+decision\b",
    r"\bno\s+(?:new\s+)?strategic\s+(?:decision|commitment)(?:\s+is|\s+being)?\s+requested\b",
    r"\bno\s+(?:decision|approval|commitment)\s+(?:is\s+)?requested\b",
)

INFORMATIONAL_INTENT_PATTERNS = (
    r"\binformational\s+(?:operating\s+|performance\s+)?update\b",
    r"\bfor\s+information\s+only\b",
    r"\bno\s+(?:executive\s+)?decision(?:\s+or\s+approval)?\s+(?:is\s+)?requested\b",
    r"\bno\s+(?:new\s+)?strategic\s+commitment(?:\s+is|\s+being)?\s+requested\b",
    r"\bno\s+further\s+action\s+is\s+required\b",
    r"\bno\s+approval\s+(?:is\s+)?requested\b",
    r"ไม่มี[^.!?\n]{0,50}(?:การตัดสินใจ|การอนุมัติ)[^.!?\n]{0,30}(?:ที่ต้องการ|ในวันนี้)",
)

DECISION_REQUEST_PATTERNS = (
    r"\bboard\b",
    r"\bmanagement\s+committee\b",
    r"\bexecutive(?:s|\s+team)?\b[^.!?\n]{0,80}\b(?:decid\w*|decision|choose|approve|approval|direction|commit)\b",
    r"\b(?:needs?|requests?|requires?|seeks?|asks?\s+for)\s+(?:an?\s+)?(?:decision|approval|direction|commitment|alignment|funding)\b",
    r"\bmust\s+(?:decide|choose|approve|commit)\b",
    r"\b(?:scale|deploy)\s+ai\s+agents?\b",
    r"\bpresent\b[^.!?\n]{0,80}\b(?:ai\s+agent\s+scaling|decision|trade-off)\b",
    r"\b(?:print|reveal|expose)\b[^.!?\n]{0,80}\b(?:environment variable|credential|api key)\b",
    r"\boption\s+[a-z]\b",
    r"\bwhether\s+to\b",
    r"(?:ขอ|ต้องการ)[^.!?\n]{0,30}(?:direction|การตัดสินใจ|อนุมัติ)",
    r"(?:ตัดสินใจ|อนุมัติ)[^.!?\n]{0,30}(?:อย่างไร|หรือไม่|scale)",
)


def without_negated_decision_context(text: str) -> str:
    """Remove explicit no-decision phrases before keyword classification."""
    cleaned = text.lower()
    for pattern in NEGATED_DECISION_PATTERNS:
        cleaned = re.sub(pattern, " ", cleaned, flags=re.IGNORECASE)
    return cleaned


def has_informational_intent(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered, re.IGNORECASE) for pattern in INFORMATIONAL_INTENT_PATTERNS)


def has_decision_request(text: str) -> bool:
    if has_informational_intent(text):
        return False
    cleaned = without_negated_decision_context(text)
    return any(re.search(pattern, cleaned, re.IGNORECASE) for pattern in DECISION_REQUEST_PATTERNS)

class DecisionGravityClassifier:
    HIGH_GRAVITY_KEYWORDS = [
        "board", "mc", "c-suite", "investment committee", "capital allocation", 
        "governance", "irreversible commitment", "safety", "risk", "compliance", 
        "ai agent deployment", "operating model redesign", "scale"
    ]
    
    MEDIUM_GRAVITY_KEYWORDS = [
        "alignment", "strategic priority", "priority decision", "direction", "funding phase", "next-step approval"
    ]

    AI_HIGH_GRAVITY_SIGNALS = (
        "accountability",
        "autonomy",
        "governance",
        "halt rule",
        "approval gate",
        "data access",
    )

    @staticmethod
    def _contains_keyword(text: str, keyword: str) -> bool:
        pattern = r"(?<!\w)" + re.escape(keyword) + r"(?!\w)"
        return re.search(pattern, text) is not None

    def classify(self, context: DocumentContext) -> DecisionGravityResult:
        text_lower = without_negated_decision_context(context.raw_text)
        
        triggers = []
        for kw in self.HIGH_GRAVITY_KEYWORDS:
            if self._contains_keyword(text_lower, kw):
                triggers.append(kw)

        if (
            ("ai agent" in text_lower or "ai-agent" in text_lower)
            and any(signal in text_lower for signal in self.AI_HIGH_GRAVITY_SIGNALS)
            and "ai accountability" not in triggers
        ):
            triggers.append("ai accountability")
                
        if len(triggers) > 0:
            return DecisionGravityResult(gravity="High", triggers=triggers)
            
        for kw in self.MEDIUM_GRAVITY_KEYWORDS:
            if self._contains_keyword(text_lower, kw):
                triggers.append(kw)
                
        if len(triggers) > 0:
            return DecisionGravityResult(gravity="Medium", triggers=triggers)
            
        return DecisionGravityResult(gravity="Low", triggers=[])
