from engine import Orchestrator, ResearchRun
from engine.evidence_graph import EvidenceGraph


def test_terminal_run_contains_traceable_dossier():
    graph = EvidenceGraph()
    graph.add_source("s1", title="Controlled study", url="https://example.test/study")
    graph.add_evidence("e1", source_id="s1", content="Outcome improved")
    graph.add_claim("c1", text="X improves outcome")
    graph.link_evidence("e1", "c1", "supports")
    graph.add_claim("c2", text="X has no effect")
    graph.add_contradiction("k1", claim_ids=["c1", "c2"])
    graph.add_conclusion("z1", text="Evidence is mixed", claim_ids=["c1", "c2"], contradiction_ids=["k1"])
    agents = {
        "planner": lambda _: {}, "researcher": lambda _: {}, "evidence_analyst": lambda _: {},
        "contradiction_analyst": lambda _: {}, "synthesizer": lambda _: {},
        "verifier": lambda _: {"sufficiency": {"evidence_saturation": True}}, "next_action": lambda _: {},
    }

    run = Orchestrator(agents).run(ResearchRun("r1", "Does X work?", context={"evidence_graph": graph}))
    dossier = run.context["research_dossier"]

    assert dossier["status"] == "completed"
    assert dossier["claims"][0]["supporting_evidence"] == ["e1"]
    assert dossier["contradictions"][0]["claim_ids"] == ["c1", "c2"]
    assert dossier["conclusions"][0]["contradiction_ids"] == ["k1"]
