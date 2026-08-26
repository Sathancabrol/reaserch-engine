"""Bridge between the graph primitives and the ResearchRun context."""

from .evidence_extractor import extract
from .evidence_graph import EvidenceGraph
from .claims import build_claim, attach_evidence, claim_status
from .source_quality import classify_source


class RunBuilder:
    def __init__(self, graph=None):
        self.graph = graph or EvidenceGraph()

    def add_source_result(self, result):
        if result.id not in self.graph.nodes:
            metadata = result.metadata or {}
            self.graph.add_source(
                result.id, title=result.title, url=result.url, source_type=result.source_type,
                metadata=metadata,
                quality=classify_source(
                    source_type=result.source_type,
                    peer_reviewed=metadata.get("peer_reviewed"),
                    direct_evidence=result.source_type == "primary_study",
                    transparent_methods=metadata.get("transparent_methods"),
                ),
            )
        evidence = extract(result, f"evidence:{result.id}")
        if evidence.id not in self.graph.nodes:
            self.graph.add_evidence(evidence.id, source_id=evidence.source_id, content=evidence.content,
                                    direction=evidence.direction, evidence_type=evidence.evidence_type,
                                    location=evidence.location, confidence=evidence.confidence,
                                    limitations=evidence.limitations or [])
        return evidence

    def add_claim(self, claim_id, text, evidence_ids=(), importance=1, direction="supports"):
        if claim_id not in self.graph.nodes:
            build_claim(self.graph, claim_id, text, importance=importance)
        for evidence_id in evidence_ids:
            attach_evidence(self.graph, claim_id, evidence_id, direction)
        self.graph.nodes[claim_id].data["status"] = claim_status(self.graph, claim_id)
        return self.graph.nodes[claim_id]

    def add_contradiction(self, contradiction_id, claim_ids, **data):
        if contradiction_id not in self.graph.nodes:
            return self.graph.add_contradiction(contradiction_id, claim_ids=claim_ids, **data)
        return self.graph.nodes[contradiction_id]

    def add_conclusion(self, conclusion_id, text, claim_ids=(), contradiction_ids=(), **data):
        if conclusion_id not in self.graph.nodes:
            return self.graph.add_conclusion(conclusion_id, text=text, claim_ids=claim_ids,
                                             contradiction_ids=contradiction_ids, **data)
        return self.graph.nodes[conclusion_id]

    def snapshot(self):
        return self.graph.snapshot()
