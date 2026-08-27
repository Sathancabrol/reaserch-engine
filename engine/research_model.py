"""Canonical epistemic objects for Research Engine v0.1."""
from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass
class Context:
    population: str | None = None
    setting: str | None = None
    time_start: str | None = None
    time_end: str | None = None
    task: str | None = None
    measurement_conditions: str | None = None
    notes: str | None = None

@dataclass
class ResearchQuestion:
    id: str
    text: str
    question_type: str = "open"
    scope: str | None = None
    priority: float = 1.0
    parent_id: str | None = None
    status: str = "open"

@dataclass
class Hypothesis:
    id: str
    text: str
    status: str = "proposed"
    operational_prediction: str | None = None
    assumptions: list[str] = field(default_factory=list)

@dataclass
class Evidence:
    id: str
    source_id: str
    content: str
    evidence_type: str = "reported_result"
    direction: str = "neutral"
    context: Context = field(default_factory=Context)
    limitations: list[str] = field(default_factory=list)
    locator: str | None = None
    extracted_by: str | None = None

@dataclass
class Claim:
    id: str
    text: str
    status: str = "proposed"
    importance: float = 0.5
    scope: str | None = None
    uncertainty: list[str] = field(default_factory=list)
    evidence_ids: list[str] = field(default_factory=list)
    counter_evidence_ids: list[str] = field(default_factory=list)

@dataclass
class Finding:
    id: str
    text: str
    claim_ids: list[str] = field(default_factory=list)
    uncertainty: list[str] = field(default_factory=list)

@dataclass
class Contradiction:
    id: str
    claim_ids: list[str]
    classification: str = "unclassified"
    explanation: str | None = None
    resolved: bool = False

@dataclass
class Inference:
    id: str
    text: str
    evidence_ids: list[str] = field(default_factory=list)
    claim_ids: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    alternatives: list[str] = field(default_factory=list)

@dataclass
class Conclusion:
    id: str
    text: str
    finding_ids: list[str] = field(default_factory=list)
    inference_ids: list[str] = field(default_factory=list)
    contradiction_ids: list[str] = field(default_factory=list)
    confidence: float | None = None
    limitations: list[str] = field(default_factory=list)


def to_dict(obj: Any) -> dict[str, Any]:
    return asdict(obj)
