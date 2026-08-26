"""Reference agent contracts for Research Engine v0.1.

Agents are deliberately thin orchestration components. A production LLM
adapter should implement these contracts while returning structured data.
"""

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass
class AgentContext:
    run_id: str
    question: str
    state: dict[str, Any]


class Agent(Protocol):
    name: str

    def execute(self, context: AgentContext) -> dict[str, Any]: ...


class PlannerAgent:
    name = "planner"

    def execute(self, context: AgentContext) -> dict[str, Any]:
        return {"research_plan": {"question": context.question, "subquestions": []}}


class ResearcherAgent:
    name = "researcher"

    def __init__(self, retriever):
        self.retriever = retriever

    def execute(self, context: AgentContext) -> dict[str, Any]:
        from .retrieval import SearchRequest
        queries = context.state.get("queries", [context.question])
        results = []
        for query in queries:
            results.extend(self.retriever.search(SearchRequest(query=query)))
        return {"search_results": results}


class EvidenceAnalystAgent:
    name = "evidence_analyst"

    def execute(self, context: AgentContext) -> dict[str, Any]:
        return {"evidence_analysis": {"status": "pending", "results": context.state.get("search_results", [])}}


class ContradictionAnalystAgent:
    name = "contradiction_analyst"

    def execute(self, context: AgentContext) -> dict[str, Any]:
        return {"contradictions": []}


class SynthesizerAgent:
    name = "synthesizer"

    def execute(self, context: AgentContext) -> dict[str, Any]:
        return {"synthesis": {"status": "draft", "based_on": context.state.get("claims", [])}}


class VerifierAgent:
    name = "verifier"

    def execute(self, context: AgentContext) -> dict[str, Any]:
        return {"verification": {"critical_issues": 0}}


class NextActionAgent:
    name = "next_action"

    def execute(self, context: AgentContext) -> dict[str, Any]:
        from .actions import next_best_action
        return {"next_action": next_best_action(context.state)}
