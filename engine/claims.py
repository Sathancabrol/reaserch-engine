"""Claim/evidence operations for the v0.1 epistemic graph."""


def build_claim(graph, claim_id: str, text: str, importance: int = 1, **data):
    graph.add_node(claim_id, "claim", text=text, importance=importance, status="proposed", **data)
    return claim_id


def attach_evidence(graph, claim_id: str, evidence_id: str, direction: str):
    if direction not in {"supports", "contradicts", "neutral", "contextual"}:
        raise ValueError(f"Unsupported evidence direction: {direction}")
    graph.add_edge(claim_id, direction, evidence_id)


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
