"""Research Engine v0.1 state machine.

Pure orchestration state transitions; no model or network dependency.
"""

from enum import Enum


class ResearchState(str, Enum):
    CREATED = "created"
    PLANNING = "planning"
    RESEARCHING = "researching"
    SYNTHESIZING = "synthesizing"
    VERIFYING = "verifying"
    SUFFICIENT = "sufficient"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"


_ALLOWED = {
    ResearchState.CREATED: {ResearchState.PLANNING, ResearchState.FAILED},
    ResearchState.PLANNING: {ResearchState.RESEARCHING, ResearchState.BLOCKED, ResearchState.FAILED},
    ResearchState.RESEARCHING: {ResearchState.SYNTHESIZING, ResearchState.BLOCKED, ResearchState.FAILED},
    ResearchState.SYNTHESIZING: {ResearchState.VERIFYING, ResearchState.RESEARCHING, ResearchState.FAILED},
    ResearchState.VERIFYING: {ResearchState.SUFFICIENT, ResearchState.RESEARCHING, ResearchState.BLOCKED, ResearchState.FAILED},
    ResearchState.SUFFICIENT: {ResearchState.COMPLETED},
    ResearchState.BLOCKED: {ResearchState.PLANNING, ResearchState.COMPLETED, ResearchState.FAILED},
    ResearchState.COMPLETED: set(),
    ResearchState.FAILED: set(),
}


def transition(current: ResearchState, target: ResearchState) -> ResearchState:
    """Validate and return a legal next state."""
    if target not in _ALLOWED[current]:
        raise ValueError(f"Illegal research transition: {current.value} -> {target.value}")
    return target
