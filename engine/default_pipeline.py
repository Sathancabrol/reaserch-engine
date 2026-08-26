"""Build the reference v0.1 pipeline from injectable components."""

from .agents import (
    PlannerAgent, ResearcherAgent, EvidenceAnalystAgent,
    ContradictionAnalystAgent, SynthesizerAgent, VerifierAgent, NextActionAgent,
)


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
    return {agent.name: agent.execute for agent in instances}
