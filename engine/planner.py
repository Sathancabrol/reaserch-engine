"""Adaptive research planner for Research Engine v0.1."""

from dataclasses import dataclass, field


@dataclass
class SubQuestion:
    id: str
    text: str
    objective: str
    priority: int = 50
    status: str = "open"
    source_types: list[str] = field(default_factory=list)


@dataclass
class ResearchPlan:
    question: str
    research_type: str
    subquestions: list[SubQuestion]
    quality_gates: list[str]


class AdaptivePlanner:
    """Create a transparent baseline plan; an LLM may enrich, not bypass, it."""

    def plan(self, question: str, *, domain: str | None = None) -> ResearchPlan:
        q = question.strip()
        subquestions = [
            SubQuestion("sq1", f"What exactly is being asked by: {q}?", "define_scope", 100),
            SubQuestion("sq2", "What does the strongest existing evidence show?", "state_of_evidence", 95),
            SubQuestion("sq3", "What credible evidence contradicts or qualifies the leading conclusion?", "counter_evidence", 90),
            SubQuestion("sq4", "What are the limitations, uncertainties and unresolved gaps?", "uncertainty", 85),
        ]
        return ResearchPlan(q, "adaptive_hybrid", subquestions, [
            "source_classification", "claim_provenance", "counter_evidence_check",
            "contradiction_review", "uncertainty_statement", "stopping_criterion",
        ])
