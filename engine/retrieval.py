"""Provider-agnostic retrieval interfaces for Research Engine v0.1.

The core engine does not perform network I/O. Concrete adapters can implement
this protocol for web search, scholarly APIs, local corpora, or databases.
"""

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class SearchRequest:
    query: str
    subquestion_id: str | None = None
    source_types: list[str] = field(default_factory=list)
    max_results: int = 10
    recency_days: int | None = None


@dataclass
class SearchResult:
    id: str
    title: str
    url: str | None = None
    snippet: str = ""
    source_type: str = "unknown"
    metadata: dict = field(default_factory=dict)


class Retriever(Protocol):
    def search(self, request: SearchRequest) -> list[SearchResult]: ...


class InMemoryRetriever:
    """Deterministic retriever useful for tests and local experiments."""

    def __init__(self, documents: list[SearchResult] | None = None):
        self.documents = documents or []

    def search(self, request: SearchRequest) -> list[SearchResult]:
        terms = {term.lower() for term in request.query.split() if len(term) > 2}
        ranked = []
        for doc in self.documents:
            haystack = f"{doc.title} {doc.snippet}".lower()
            score = sum(term in haystack for term in terms)
            if score:
                ranked.append((score, doc))
        ranked.sort(key=lambda item: item[0], reverse=True)
        return [doc for _, doc in ranked[:request.max_results]]
