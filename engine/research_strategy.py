"""Adaptive strategy selection for autonomous research."""
from dataclasses import dataclass, field

@dataclass
class ResearchAction:
    action_type: str
    target: str
    reason: str
    priority: int
    expected_information_gain: float = 0.0
    source_types: list[str] = field(default_factory=list)

@dataclass
class StrategyState:
    question_type: list[str]
    open_subquestions: int = 0
    unresolved_claims: int = 0
    contradictions: int = 0
    source_coverage: float = 0.0
    confidence: float = 0.0

class ResearchStrategyEngine:
    """Choose the next research action from the current epistemic state."""
    def next_actions(self, state: StrategyState) -> list[ResearchAction]:
        actions = []
        if state.open_subquestions:
            actions.append(ResearchAction("search", "highest-priority open subquestion", "close an unresolved research objective", 100, .9, ["systematic_review", "meta_analysis", "primary_study"]))
        if state.contradictions:
            actions.append(ResearchAction("investigate_contradiction", "conflicting claims", "resolve or characterize disagreement", 98, .95, ["primary_study", "systematic_review"]))
        if state.unresolved_claims:
            actions.append(ResearchAction("verify_claims", "unsupported material claims", "increase claim provenance", 95, .8, ["primary_study", "institutional_report"]))
        if state.source_coverage < .7:
            actions.append(ResearchAction("expand_source_classes", "underrepresented evidence classes", "reduce source-selection bias", 75, .7, ["academic_book", "thesis", "institutional_report"]))
        actions.sort(key=lambda a: (a.priority, a.expected_information_gain), reverse=True)
        return actions
