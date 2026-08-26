"""Bridge between the graph primitives and the ResearchRun context."""

from .evidence_extractor import extract
from .evidence_graph import EvidenceGraph
from .claims import build_claim, attach_evidence, claim_status


class RunBuilder:
    def __init__(self, graph=None):
        self.graph = graph or EvidenceGraph()

    def add_source_result(self, result):
        self.graph.add_node(result.id, "source", title=result.title, url=result.url, source_type=result.source_type)
        evidence = extract(result, f"evidence:{result.id}")
        self.graph.add_node(evidence.id, "evidence", content=evidence.content, source_id=evidence.source_id)
        self.graph.add_edge(evidence.id, "derived_from", result.id)
        return evidence

    def add_claim(self, claim_id, text, evidence_ids=(), importance=1):
        build_claim(self.graph, claim_id, text, importance=importance)
        for evidence_id in evidence_ids:
            attach_evidence(self.graph, claim_id, evidence_id, "supports")
        self.graph.nodes[claim_id].data["status"] = claim_status(self.graph, claim_id)
        return self.graph.nodes[claim_id]

    def snapshot(self):
        return {
            "nodes": [{"id": n.id, "kind": n.kind, "data": n.data} for n in self.graph.nodes.values()],
            "edges": [{"source": e.source, "relation": e.relation, "target": e.target, "data": e.data} for e in self.graph.edges],
        }
