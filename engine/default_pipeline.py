"""Build the reference v0.1 pipeline from injectable components."""

from .agents import (
    PlannerAgent, ResearcherAgent, EvidenceAnalystAgent,
    ContradictionAnalystAgent, SynthesizerAgent, VerifierAgent, NextActionAgent,
)
from .agents import AgentContext


def build_agents(retriever):
    instances = [
        PlannerAgent(),
        ResearcherAgent(retriever),
        EvidenceAnalystAgent(),
        ContradictionAnalystAgent(),
        SynthesizerAgent(),
        VerifierAgent(),
        NextActionAgent(),
    ]
    def invoke(execute):
        def wrapped(state):
            return execute(AgentContext(
                run_id=state.get("run_id", "unknown"),
                question=state.get("question", ""),
                state=state,
            ))
        return wrapped

    return {agent.name: invoke(agent.execute) for agent in instances}
