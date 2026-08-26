from engine import JsonRunStore, Orchestrator, ResearchRun
from engine.evidence_graph import EvidenceGraph


def test_checkpoint_round_trip_restores_graph_and_run_metadata(tmp_path):
    graph = EvidenceGraph()
    graph.add_source("s1", title="Study")
    graph.add_evidence("e1", source_id="s1", content="Observed outcome")
    run = ResearchRun("run-1", "Question?", context={"evidence_graph": graph})

    store = JsonRunStore(tmp_path)
    store.save(run)
    restored = store.load("run-1")

    assert restored.revision == 1
    assert restored.context["evidence_graph"].provenance("e1") == ["s1"]


def test_orchestrator_checkpoints_agent_progress(tmp_path):
    agents = {
        "planner": lambda _: {}, "researcher": lambda _: {}, "evidence_analyst": lambda _: {},
        "contradiction_analyst": lambda _: {}, "synthesizer": lambda _: {},
        "verifier": lambda _: {"sufficiency": {"evidence_saturation": True}}, "next_action": lambda _: {},
    }
    store = JsonRunStore(tmp_path)
    run = Orchestrator(agents, store=store).run(ResearchRun("run-2", "Question?"))

    restored = store.load("run-2")
    assert restored.state.value == "completed"
    assert restored.revision == run.revision
    assert len(restored.history) == len(run.history)
