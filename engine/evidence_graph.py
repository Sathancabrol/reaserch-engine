"""In-memory, provenance-preserving evidence graph for Research Engine v0.1.

The graph is intentionally storage-agnostic. It gives the orchestration loop
one canonical chain: source -> evidence -> claim -> contradiction -> conclusion.
"""

from dataclasses import dataclass, field
from typing import Any, Iterable


EVIDENCE_DIRECTIONS = {"supports", "contradicts", "neutral", "contextual"}


@dataclass
class GraphNode:
    id: str
    kind: str
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class GraphEdge:
    source: str
    relation: str
    target: str
    data: dict[str, Any] = field(default_factory=dict)


class EvidenceGraph:
    def __init__(self):
        self.nodes: dict[str, GraphNode] = {}
        self.edges: list[GraphEdge] = []

    def add_node(self, node_id: str, kind: str, **data: Any) -> GraphNode:
        if node_id in self.nodes:
            raise ValueError(f"Duplicate graph node: {node_id}")
        self.nodes[node_id] = GraphNode(node_id, kind, data)
        return self.nodes[node_id]

    def add_edge(self, source: str, relation: str, target: str, **data: Any) -> GraphEdge:
        if source not in self.nodes or target not in self.nodes:
            raise KeyError("Both edge endpoints must exist")
        edge = GraphEdge(source, relation, target, data)
        self.edges.append(edge)
        return edge

    def add_source(self, source_id: str, *, title: str, **metadata: Any) -> GraphNode:
        return self.add_node(source_id, "source", title=title, **metadata)

    def add_evidence(self, evidence_id: str, *, source_id: str, content: str,
                     direction: str = "neutral", **metadata: Any) -> GraphNode:
        if direction not in EVIDENCE_DIRECTIONS:
            raise ValueError(f"Unsupported evidence direction: {direction}")
        if not content.strip():
            raise ValueError("Evidence content cannot be empty")
        if self.nodes.get(source_id) is None or self.nodes[source_id].kind != "source":
            raise KeyError(f"Evidence source must be an existing source: {source_id}")
        node = self.add_node(evidence_id, "evidence", content=content, direction=direction, **metadata)
        self.add_edge(source_id, "provides", evidence_id)
        return node

    def add_claim(self, claim_id: str, *, text: str, **metadata: Any) -> GraphNode:
        if not text.strip():
            raise ValueError("Claim text cannot be empty")
        return self.add_node(claim_id, "claim", text=text, status="proposed", **metadata)

    def link_evidence(self, evidence_id: str, claim_id: str, direction: str) -> GraphEdge:
        if direction not in EVIDENCE_DIRECTIONS:
            raise ValueError(f"Unsupported evidence direction: {direction}")
        if self.nodes.get(evidence_id, GraphNode("", "")).kind != "evidence":
            raise KeyError(f"Expected evidence node: {evidence_id}")
        if self.nodes.get(claim_id, GraphNode("", "")).kind != "claim":
            raise KeyError(f"Expected claim node: {claim_id}")
        return self.add_edge(evidence_id, direction, claim_id)

    def add_contradiction(self, contradiction_id: str, *, claim_ids: Iterable[str],
                          classification: str = "unclassified", **metadata: Any) -> GraphNode:
        claim_ids = list(claim_ids)
        if len(claim_ids) < 2:
            raise ValueError("A contradiction requires at least two claims")
        for claim_id in claim_ids:
            if self.nodes.get(claim_id, GraphNode("", "")).kind != "claim":
                raise KeyError(f"Contradiction references a missing claim: {claim_id}")
        node = self.add_node(contradiction_id, "contradiction", classification=classification, **metadata)
        for claim_id in claim_ids:
            self.add_edge(claim_id, "conflicts_in", contradiction_id)
        return node

    def add_conclusion(self, conclusion_id: str, *, text: str, claim_ids: Iterable[str] = (),
                       contradiction_ids: Iterable[str] = (), **metadata: Any) -> GraphNode:
        if not text.strip():
            raise ValueError("Conclusion text cannot be empty")
        node = self.add_node(conclusion_id, "conclusion", text=text, **metadata)
        for claim_id in claim_ids:
            if self.nodes.get(claim_id, GraphNode("", "")).kind != "claim":
                raise KeyError(f"Conclusion references a missing claim: {claim_id}")
            self.add_edge(claim_id, "informs", conclusion_id)
        for contradiction_id in contradiction_ids:
            if self.nodes.get(contradiction_id, GraphNode("", "")).kind != "contradiction":
                raise KeyError(f"Conclusion references a missing contradiction: {contradiction_id}")
            self.add_edge(contradiction_id, "qualifies", conclusion_id)
        return node

    def neighbors(self, node_id: str, relation: str | None = None) -> list[str]:
        return [
            e.target for e in self.edges
            if e.source == node_id and (relation is None or e.relation == relation)
        ]

    def supporting_evidence(self, claim_id: str) -> list[str]:
        """Support both the legacy claim->evidence and canonical reverse direction."""
        incoming = [e.source for e in self.edges if e.target == claim_id and e.relation == "supports"]
        return incoming + self.neighbors(claim_id, "supports")

    def contradicting_evidence(self, claim_id: str) -> list[str]:
        incoming = [e.source for e in self.edges if e.target == claim_id and e.relation == "contradicts"]
        return incoming + self.neighbors(claim_id, "contradicts")

    def provenance(self, node_id: str) -> list[str]:
        return [e.source for e in self.edges if e.target == node_id and e.relation in {"provides", "derived_from"}]

    def snapshot(self) -> dict[str, list[dict[str, Any]]]:
        return {
            "nodes": [{"id": n.id, "kind": n.kind, "data": n.data} for n in self.nodes.values()],
            "edges": [{"source": e.source, "relation": e.relation, "target": e.target, "data": e.data} for e in self.edges],
        }

    @classmethod
    def from_snapshot(cls, snapshot: dict[str, list[dict[str, Any]]]) -> "EvidenceGraph":
        """Restore a graph snapshot while enforcing the usual endpoint checks."""
        graph = cls()
        for node in snapshot.get("nodes", []):
            graph.add_node(node["id"], node["kind"], **node.get("data", {}))
        for edge in snapshot.get("edges", []):
            graph.add_edge(edge["source"], edge["relation"], edge["target"], **edge.get("data", {}))
        return graph
