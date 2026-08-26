"""Minimal dependency-free Research Engine v0.1 orchestrator.

Agents are injected as callables so retrieval/model providers can be added
without coupling the core engine to one vendor.
"""

from dataclasses import dataclass, field
from typing import Any, Callable
from .state_machine import ResearchState, transition
from .sufficiency import SufficiencyInput, assess
from .evidence_graph import EvidenceGraph

Agent = Callable[[dict[str, Any]], dict[str, Any]]


@dataclass
class ResearchRun:
    run_id: str
    question: str
    state: ResearchState = ResearchState.CREATED
    iteration: int = 0
    revision: int = 0
    context: dict[str, Any] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)


class Orchestrator:
    """Coordinates the protocol; it does not contain domain knowledge."""

    def __init__(self, agents: dict[str, Agent], max_iterations: int = 5, store=None):
        self.agents = agents
        self.max_iterations = max_iterations
        self.store = store

    def _checkpoint(self, run: ResearchRun) -> None:
        if self.store is not None:
            self.store.save(run)

    def _run_agent(self, name: str, run: ResearchRun) -> None:
        agent = self.agents.get(name)
        if agent is None:
            raise RuntimeError(f"Missing required agent: {name}")
        result = agent(run.context)
        if result:
            run.context.update(result)
        run.history.append({"iteration": run.iteration, "agent": name, "result_keys": list(result or {})})
        self._checkpoint(run)

    def run(self, run: ResearchRun) -> ResearchRun:
        # The graph belongs to the run context so injected agents can enrich it
        # without the orchestrator needing domain-specific extraction logic.
        run.context.setdefault("evidence_graph", EvidenceGraph())
        run.context.setdefault("run_id", run.run_id)
        run.context.setdefault("question", run.question)
        self._checkpoint(run)
        run.state = transition(run.state, ResearchState.PLANNING)
        self._run_agent("planner", run)

        while run.iteration < self.max_iterations:
            run.iteration += 1
            run.state = transition(run.state, ResearchState.RESEARCHING)
            self._run_agent("researcher", run)
            self._run_agent("evidence_analyst", run)
            self._run_agent("contradiction_analyst", run)

            run.state = transition(run.state, ResearchState.SYNTHESIZING)
            self._run_agent("synthesizer", run)

            run.state = transition(run.state, ResearchState.VERIFYING)
            self._run_agent("verifier", run)

            decision = assess(SufficiencyInput(**run.context.get("sufficiency", {})))
            run.context["stopping_decision"] = decision

            if decision["decision"] == "stop":
                run.state = transition(run.state, ResearchState.SUFFICIENT)
                run.state = transition(run.state, ResearchState.COMPLETED)
                self._checkpoint(run)
                return run

            # Start the next research cycle from the research state.
            run.state = transition(run.state, ResearchState.RESEARCHING)
            self._run_agent("next_action", run)

        run.state = ResearchState.BLOCKED
        run.context["stopping_decision"] = {
            "decision": "blocked",
            "reason": "maximum_iterations_reached",
        }
        self._checkpoint(run)
        return run
