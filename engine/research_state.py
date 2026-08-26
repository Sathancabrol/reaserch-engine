"""Canonical state carried across autonomous research iterations."""
from dataclasses import dataclass, field
from typing import Any

@dataclass
class ResearchState:
    run_id: str
    question: str
    iteration: int = 0
    phase: str = "planning"
    plan: Any = None
    sources: list[Any] = field(default_factory=list)
    evidence: list[Any] = field(default_factory=list)
    claims: list[Any] = field(default_factory=list)
    contradictions: list[Any] = field(default_factory=list)
    actions: list[Any] = field(default_factory=list)
    findings: list[Any] = field(default_factory=list)
    audit_log: list[dict] = field(default_factory=list)
    stopped: bool = False
    stop_reason: str | None = None

    def log(self, event: str, **data):
        self.audit_log.append({"iteration": self.iteration, "phase": self.phase, "event": event, **data})
