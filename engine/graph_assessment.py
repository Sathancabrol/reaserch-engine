"""Transparent graph-derived inputs for verification and stopping decisions."""

from .claims import claim_status


def _is_critical(importance) -> bool:
    return importance == "critical" or (isinstance(importance, int) and importance >= 3)


def assess_evidence_graph(graph) -> dict:
    """Return counts, not opaque scores, so the sufficiency decision is auditable."""
    claims = [node for node in graph.nodes.values() if node.kind == "claim"]
    contradictions = [node for node in graph.nodes.values() if node.kind == "contradiction"]
    weak_critical_claims = [
        node.id for node in claims
        if _is_critical(node.data.get("importance")) and claim_status(graph, node.id) != "supported"
    ]
    unresolved = [
        node.id for node in contradictions if node.data.get("status", "unresolved") == "unresolved"
    ]
    source_nodes = [node for node in graph.nodes.values() if node.kind == "source"]
    low_quality_sources = [
        node.id for node in source_nodes
        if node.data.get("quality", {}).get("relevance") == "low"
    ]
    return {
        "weak_critical_claims": len(weak_critical_claims),
        "unresolved_major_contradictions": len(unresolved),
        "critical_claim_ids": weak_critical_claims,
        "unresolved_contradiction_ids": unresolved,
        "low_quality_source_ids": low_quality_sources,
    }
