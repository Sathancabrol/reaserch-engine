"""Reference provider adapters and boundaries for v0.1."""

from dataclasses import dataclass
from .retrieval import Retriever, SearchRequest, SearchResult


@dataclass
class RetrievalProvider:
    name: str
    retriever: Retriever

    def search(self, request: SearchRequest) -> list[SearchResult]:
        return self.retriever.search(request)


class ProviderRegistry:
    def __init__(self):
        self._providers: dict[str, RetrievalProvider] = {}

    def register(self, provider: RetrievalProvider):
        self._providers[provider.name] = provider

    def get(self, name: str) -> RetrievalProvider:
        try:
            return self._providers[name]
        except KeyError as exc:
            raise KeyError(f"Unknown retrieval provider: {name}") from exc
