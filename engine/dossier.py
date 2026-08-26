"""Build an audit-ready research dossier from a completed research run."""

from __future__ import annotations

from .claims import claim_status


def _graph(run):
    return run.context.get("evidence_graph")


def _nodes_of_kind(graph, kind):
    return [node for node in graph.nodes.values() if node.kind == kind]


def _claim_ids_for_evidence(graph, evidence_id):
    return [edge.target for edge in graph.edges if edge.source == evidence_id and edge.relation in {"supports", "contradicts", "neutral", "contextual"}]


def _evidence_ids_for_claim(graph, claim_id, direction):
    return [edge.source for edge in graph.edges if edge.target == claim_id and edge.relation == direction]


def build_dossier(run) -> dict:
    """Return only traceable material; this function never invents a conclusion."""
    graph = _graph(run)
    if graph is None:
        raise ValueError("Cannot build a dossier without an evidence graph")

    claims = []
    for node in _nodes_of_kind(graph, "claim"):
        claims.append({
            "id": node.id,
            "text": node.data["text"],
            "status": claim_status(graph, node.id),
            "importance": node.data.get("importance"),
            "supporting_evidence": _evidence_ids_for_claim(graph, node.id, "supports"),
            "contradicting_evidence": _evidence_ids_for_claim(graph, node.id, "contradicts"),
        })

    evidence_matrix = []
    for node in _nodes_of_kind(graph, "evidence"):
        source_ids = graph.provenance(node.id)
        evidence_matrix.append({
            "id": node.id,
            "source_id": source_ids[0] if source_ids else None,
            "content": node.data["content"],
            "direction": node.data.get("direction", "neutral"),
            "claim_ids": _claim_ids_for_evidence(graph, node.id),
            "limitations": node.data.get("limitations", []),
        })

    contradictions = []
    for node in _nodes_of_kind(graph, "contradiction"):
        contradictions.append({
            "id": node.id,
            "classification": node.data.get("classification", "unclassified"),
            "claim_ids": [edge.source for edge in graph.edges if edge.target == node.id and edge.relation == "conflicts_in"],
            "status": node.data.get("status", "unresolved"),
        })

    conclusions = []
    for node in _nodes_of_kind(graph, "conclusion"):
        conclusions.append({
            "id": node.id,
            "text": node.data["text"],
            "claim_ids": [edge.source for edge in graph.edges if edge.target == node.id and edge.relation == "informs"],
            "contradiction_ids": [edge.source for edge in graph.edges if edge.target == node.id and edge.relation == "qualifies"],
        })

    bibliography = [
        {"id": node.id, "title": node.data["title"], "url": node.data.get("url"), "source_type": node.data.get("source_type")}
        for node in _nodes_of_kind(graph, "source")
    ]
    return {
        "run_id": run.run_id,
        "question": run.question,
        "status": run.state.value,
        "revision": run.revision,
        "conclusions": conclusions,
        "claims": claims,
        "evidence_matrix": evidence_matrix,
        "contradictions": contradictions,
        "bibliography": bibliography,
        "stopping_decision": run.context.get("stopping_decision"),
        "research_log": list(run.history),
    }
