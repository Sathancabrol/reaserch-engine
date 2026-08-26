"""Sufficiency decision logic for Research Engine v0.1.

This module deliberately uses explicit signals instead of pretending that
research completeness can be reduced to a universal numeric truth score.
"""

from dataclasses import dataclass, field


@dataclass
class SufficiencyInput:
    critical_gaps: int = 0
    weak_critical_claims: int = 0
    unresolved_major_contradictions: int = 0
    unsearched_high_value_categories: int = 0
    verifier_critical_issues: int = 0
    expected_information_gain: float = 0.0
    research_cost: float = 0.0
    budget_remaining: float = 1.0
    evidence_saturation: bool = False
    user_depth_reached: bool = False
    notes: list[str] = field(default_factory=list)


def assess(x: SufficiencyInput) -> dict:
    """Return a transparent stop/continue/blocked decision."""
    if x.verifier_critical_issues > 0:
        return {"decision": "continue", "reason": "critical_verification_issue"}
    if x.critical_gaps > 0 or x.weak_critical_claims > 0:
        return {"decision": "continue", "reason": "critical_evidence_gap"}
    if x.unresolved_major_contradictions > 0:
        return {"decision": "continue", "reason": "major_contradiction_unresolved"}
    if x.unsearched_high_value_categories > 0 and x.budget_remaining > 0:
        return {"decision": "continue", "reason": "high_value_source_class_unsearched"}
    if x.user_depth_reached or x.evidence_saturation:
        return {"decision": "stop", "reason": "depth_or_saturation_reached"}
    if x.expected_information_gain > x.research_cost and x.budget_remaining > 0:
        return {"decision": "continue", "reason": "positive_expected_information_gain"}
    return {"decision": "stop", "reason": "low_marginal_information_gain"}
