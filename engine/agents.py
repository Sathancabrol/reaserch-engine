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
        from .run_builder import RunBuilder

        graph = context.state.get("evidence_graph")
        builder = RunBuilder(graph)
        records = []
        for result in context.state.get("search_results", []):
            records.append(builder.add_source_result(result))
        # Claim drafts are optional structured agent output. Keeping them
        # separate from final claims prevents the core from inventing claims.
        for draft in context.state.get("claim_drafts", []):
            if isinstance(draft, dict) and {"id", "text"} <= draft.keys():
                builder.add_claim(
                    draft["id"], draft["text"], draft.get("evidence_ids", ()),
                    draft.get("importance", 1), draft.get("direction", "supports"),
                )
        return {
            "evidence": records,
            "evidence_analysis": {"status": "complete", "records": records},
            "evidence_graph_snapshot": builder.snapshot(),
        }


class ContradictionAnalystAgent:
    name = "contradiction_analyst"

    def execute(self, context: AgentContext) -> dict[str, Any]:
        from .run_builder import RunBuilder

        builder = RunBuilder(context.state.get("evidence_graph"))
        contradictions = context.state.get("contradictions", [])
        for item in contradictions:
            if isinstance(item, dict) and {"id", "claim_ids"} <= item.keys():
                data = {key: value for key, value in item.items() if key not in {"id", "claim_ids"}}
                builder.add_contradiction(item["id"], item["claim_ids"], **data)
        return {"contradictions": contradictions, "evidence_graph_snapshot": builder.snapshot()}


class SynthesizerAgent:
    name = "synthesizer"

    def execute(self, context: AgentContext) -> dict[str, Any]:
        from .run_builder import RunBuilder

        synthesis = {"status": "draft", "based_on": context.state.get("claims", [])}
        builder = RunBuilder(context.state.get("evidence_graph"))
        # A provider may explicitly return a conclusion draft. It is only added
        # when a claim provenance list accompanies it.
        draft = context.state.get("conclusion_draft")
        if isinstance(draft, dict) and {"id", "text"} <= draft.keys():
            builder.add_conclusion(draft["id"], draft["text"], draft.get("claim_ids", ()),
                                   draft.get("contradiction_ids", ()))
            synthesis["conclusion_id"] = draft["id"]
        return {"synthesis": synthesis, "evidence_graph_snapshot": builder.snapshot()}


class VerifierAgent:
    name = "verifier"

    def execute(self, context: AgentContext) -> dict[str, Any]:
        from .graph_assessment import assess_evidence_graph

        graph = context.state.get("evidence_graph")
        assessment = assess_evidence_graph(graph) if graph is not None else {}
        return {
            "verification": {"critical_issues": 0, "graph_assessment": assessment},
            "sufficiency": {
                "weak_critical_claims": assessment.get("weak_critical_claims", 0),
                "unresolved_major_contradictions": assessment.get("unresolved_major_contradictions", 0),
            },
        }


class NextActionAgent:
    name = "next_action"

    def execute(self, context: AgentContext) -> dict[str, Any]:
        from .actions import next_best_action
        return {"next_action": next_best_action(context.state)}
