"""Deterministic evidence extraction primitives.

LLM adapters may enrich these records later; the core always preserves
source provenance and explicit uncertainty.
"""

from dataclasses import dataclass


@dataclass
class EvidenceRecord:
    id: str
    source_id: str
    content: str
    location: str | None = None
    evidence_type: str = "unspecified"
    direction: str = "neutral"
    limitations: list[str] | None = None
    confidence: str = "unknown"


def extract(result, evidence_id: str, *, direction="neutral", evidence_type="search_result"):
    return EvidenceRecord(
        id=evidence_id,
        source_id=result.id,
        content=result.snippet or result.title,
        evidence_type=evidence_type,
        direction=direction,
    )
