"""Evidence graph primitives for Research Engine v0.1.

The graph is deliberately small: nodes represent epistemic objects and edges
represent traceable relationships. It is independent from any graph database.
"""

from dataclasses import dataclass, field


@dataclass
class GraphNode:
    id: str
    kind: str
    data: dict = field(default_factory=dict)


@dataclass
class GraphEdge:
    source: str
    relation: str
    target: str
    data: dict = field(default_factory=dict)


class EvidenceGraph:
    def __init__(self):
        self.nodes: dict[str, GraphNode] = {}
        self.edges: list[GraphEdge] = []

    def add_node(self, node_id: str, kind: str, **data):
        if node_id in self.nodes:
            raise ValueError(f"Duplicate graph node: {node_id}")
        self.nodes[node_id] = GraphNode(node_id, kind, data)
        return self.nodes[node_id]

    def add_edge(self, source: str, relation: str, target: str, **data):
        if source not in self.nodes or target not in self.nodes:
            raise KeyError("Both edge endpoints must exist")
        edge = GraphEdge(source, relation, target, data)
        self.edges.append(edge)
        return edge

    def neighbors(self, node_id: str, relation: str | None = None):
        return [
            e.target for e in self.edges
            if e.source == node_id and (relation is None or e.relation == relation)
        ]

    def supporting_evidence(self, claim_id: str):
        return self.neighbors(claim_id, "supports")

    def contradicting_evidence(self, claim_id: str):
        return self.neighbors(claim_id, "contradicts")

    def provenance(self, node_id: str):
        return [e.source for e in self.edges if e.target == node_id and e.relation == "derived_from"]
