from engine import Orchestrator, ResearchRun, ResearchState


def agent(**result):
    return lambda context: result


def test_engine_reaches_completed_when_sufficient():
    agents = {
        "planner": agent(plan={"steps": []}),
        "researcher": agent(sources=["s1"], evidence=["e1"]),
        "evidence_analyst": agent(claims=["c1"]),
        "contradiction_analyst": agent(contradictions=[]),
        "synthesizer": agent(synthesis={"answer": "supported"}),
        "verifier": agent(verification={"critical_issues": 0}, sufficiency={"evidence_saturation": True}),
        "next_action": agent(),
    }
    run = Orchestrator(agents).run(ResearchRun("r1", "Does X affect Y?"))
    assert run.state == ResearchState.COMPLETED
    assert run.context["stopping_decision"]["decision"] == "stop"


def test_engine_stops_after_iteration_budget():
    agents = {name: agent() for name in [
        "planner", "researcher", "evidence_analyst", "contradiction_analyst",
        "synthesizer", "verifier", "next_action"
    ]}
    agents["verifier"] = agent(sufficiency={"critical_gaps": 1})
    run = Orchestrator(agents, max_iterations=1).run(ResearchRun("r2", "Open question"))
    assert run.state == ResearchState.BLOCKED
    assert run.context["stopping_decision"]["reason"] == "maximum_iterations_reached"
