"""Claim/evidence operations for the v0.1 epistemic graph."""


def build_claim(graph, claim_id: str, text: str, importance: int = 1, **data):
    graph.add_claim(claim_id, text=text, importance=importance, **data)
    return claim_id


def attach_evidence(graph, claim_id: str, evidence_id: str, direction: str):
    if direction not in {"supports", "contradicts", "neutral", "contextual"}:
        raise ValueError(f"Unsupported evidence direction: {direction}")
    graph.link_evidence(evidence_id, claim_id, direction)


def claim_status(graph, claim_id: str) -> str:
    support = len(graph.supporting_evidence(claim_id))
    contradiction = len(graph.contradicting_evidence(claim_id))
    if support and contradiction:
        return "mixed"
    if support:
        return "supported"
    if contradiction:
        return "contradicted"
    return "unknown"
