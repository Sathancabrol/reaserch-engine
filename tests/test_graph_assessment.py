from engine.evidence_graph import EvidenceGraph
from engine.graph_assessment import assess_evidence_graph


def test_assessment_exposes_critical_claim_and_unresolved_contradiction():
    graph = EvidenceGraph()
    graph.add_claim("c1", text="Important claim", importance="critical")
    graph.add_claim("c2", text="Counterclaim")
    graph.add_contradiction("k1", claim_ids=["c1", "c2"])

    assessment = assess_evidence_graph(graph)

    assert assessment["weak_critical_claims"] == 1
    assert assessment["critical_claim_ids"] == ["c1"]
    assert assessment["unresolved_major_contradictions"] == 1
