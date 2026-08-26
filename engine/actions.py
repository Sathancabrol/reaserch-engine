"""Research action selection for v0.1."""


def next_best_action(context: dict) -> dict:
    """Select one explicit research action from the current uncertainty state."""
    if context.get("verification", {}).get("critical_issues", 0) > 0:
        return {"type": "verify_claims", "priority": 100, "reason": "critical verification issue"}
    if context.get("critical_gaps", 0) > 0:
        return {"type": "search_missing_evidence", "priority": 90, "reason": "critical evidence gap"}
    if context.get("unresolved_major_contradictions", 0) > 0:
        return {"type": "investigate_contradiction", "priority": 85, "reason": "major contradiction"}
    if context.get("unsearched_high_value_categories", 0) > 0:
        return {"type": "search_new_source_class", "priority": 70, "reason": "high-value source class unsearched"}
    return {"type": "counter_evidence_search", "priority": 50, "reason": "test current synthesis"}
