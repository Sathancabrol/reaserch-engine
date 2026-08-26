import pytest
from engine.evidence_graph import EvidenceGraph
from engine.claims import claim_status


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


def test_full_epistemic_chain_is_provenance_preserving():
    graph = EvidenceGraph()
    graph.add_source("s1", title="Controlled study")
    graph.add_evidence("e1", source_id="s1", content="The outcome improved.", direction="supports")
    graph.add_claim("c1", text="X improves the outcome")
    graph.add_claim("c2", text="X has no effect")
    graph.link_evidence("e1", "c1", "supports")
    graph.add_contradiction("k1", claim_ids=["c1", "c2"], classification="empirical")
    graph.add_conclusion("z1", text="The effect remains uncertain.", claim_ids=["c1", "c2"], contradiction_ids=["k1"])

    assert graph.provenance("e1") == ["s1"]
    assert graph.supporting_evidence("c1") == ["e1"]
    assert claim_status(graph, "c1") == "supported"
    assert graph.neighbors("c1", "conflicts_in") == ["k1"]
    assert graph.neighbors("k1", "qualifies") == ["z1"]


def test_typed_relationships_reject_invalid_provenance():
    graph = EvidenceGraph()
    with pytest.raises(KeyError):
        graph.add_evidence("e1", source_id="missing", content="Observation")
    graph.add_source("s1", title="Source")
    with pytest.raises(ValueError):
        graph.add_evidence("e1", source_id="s1", content="   ")
