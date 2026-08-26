"""Dependency-free JSON checkpoints for reproducible research runs."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from enum import Enum
import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from .evidence_graph import EvidenceGraph
from .state_machine import ResearchState


def _json_value(value: Any) -> Any:
    if isinstance(value, EvidenceGraph):
        return {"__type__": "EvidenceGraph", "snapshot": value.snapshot()}
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return _json_value(asdict(value))
    if isinstance(value, dict):
        return {key: _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    return value


def _restore_value(value: Any) -> Any:
    if isinstance(value, dict):
        if value.get("__type__") == "EvidenceGraph":
            return EvidenceGraph.from_snapshot(value["snapshot"])
        return {key: _restore_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_restore_value(item) for item in value]
    return value


class JsonRunStore:
    """A local checkpoint store using atomic file replacement."""

    def __init__(self, directory: str | Path):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _path(self, run_id: str) -> Path:
        if not run_id or Path(run_id).name != run_id:
            raise ValueError("run_id must be a non-empty filename, not a path")
        return self.directory / f"{run_id}.json"

    def save(self, run) -> Path:
        run.revision += 1
        payload = {
            "run_id": run.run_id,
            "question": run.question,
            "state": run.state.value,
            "iteration": run.iteration,
            "revision": run.revision,
            "context": _json_value(run.context),
            "history": _json_value(run.history),
        }
        target = self._path(run.run_id)
        with NamedTemporaryFile("w", encoding="utf-8", dir=self.directory, delete=False) as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
            temporary = Path(handle.name)
        temporary.replace(target)
        return target

    def load(self, run_id: str):
        from .orchestrator import ResearchRun

        with self._path(run_id).open(encoding="utf-8") as handle:
            payload = json.load(handle)
        return ResearchRun(
            run_id=payload["run_id"],
            question=payload["question"],
            state=ResearchState(payload["state"]),
            iteration=payload["iteration"],
            revision=payload.get("revision", 0),
            context=_restore_value(payload.get("context", {})),
            history=_restore_value(payload.get("history", [])),
        )
