import pytest
from engine.evidence_graph import EvidenceGraph


def test_traceable_support_and_contradiction():
    graph = EvidenceGraph()
    graph.add_node("c1", "claim")
    graph.add_node("e1", "evidence")
    graph.add_node("e2", "evidence")
    graph.add_edge("c1", "supports", "e1")
    graph.add_edge("c1", "contradicts", "e2")
    assert graph.supporting_evidence("c1") == ["e1"]
    assert graph.contradicting_evidence("c1") == ["e2"]


def test_edge_requires_existing_nodes():
    graph = EvidenceGraph()
    graph.add_node("c1", "claim")
    with pytest.raises(KeyError):
        graph.add_edge("c1", "supports", "missing")
