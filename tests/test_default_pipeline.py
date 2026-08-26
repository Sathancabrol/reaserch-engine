from engine.default_pipeline import build_agents
from engine.orchestrator import Orchestrator, ResearchRun
from engine.retrieval import InMemoryRetriever, SearchResult


def test_default_pipeline_registers_retrieved_source_and_evidence_in_run_graph():
    retriever = InMemoryRetriever([
        SearchResult(id="s1", title="Study on X", snippet="X improves the outcome."),
    ])
    run = ResearchRun("run-1", "Does X improve the outcome?")
    run.context["queries"] = ["X outcome"]
    completed = Orchestrator(build_agents(retriever), max_iterations=1).run(run)

    nodes = {node["id"]: node for node in completed.context["evidence_graph_snapshot"]["nodes"]}
    edges = completed.context["evidence_graph_snapshot"]["edges"]
    assert nodes["s1"]["kind"] == "source"
    assert nodes["evidence:s1"]["kind"] == "evidence"
    assert {"source": "s1", "relation": "provides", "target": "evidence:s1", "data": {}} in edges
