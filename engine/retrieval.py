"""Provider-agnostic retrieval interfaces for Research Engine v0.1.

The core engine does not perform network I/O. Concrete adapters can implement
this protocol for web search, scholarly APIs, local corpora, or databases.
"""

from dataclasses import dataclass, field
import json
import re
from typing import Protocol
from urllib.parse import urlencode
from urllib.request import Request, urlopen


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


class LocalFirstRetriever:
    """Use local results when available, otherwise delegate to external retrieval."""

    def __init__(self, local: Retriever, external: Retriever):
        self.local = local
        self.external = external

    def search(self, request: SearchRequest) -> list[SearchResult]:
        local_results = self.local.search(request)
        return local_results if local_results else self.external.search(request)


class CrossrefRetriever:
    """Small Crossref works adapter; network access occurs only on ``search``."""

    endpoint = "https://api.crossref.org/works"

    def __init__(self, mailto: str | None = None, http_get=None):
        self.mailto = mailto
        self.http_get = http_get or self._http_get

    @staticmethod
    def _http_get(url: str) -> dict:
        request = Request(url, headers={"User-Agent": "ResearchEngine/0.1 (mailto: unavailable)"})
        with urlopen(request, timeout=15) as response:  # nosec B310: public academic API selected by caller
            return json.loads(response.read().decode("utf-8"))

    @staticmethod
    def _text(value: str | None) -> str:
        return re.sub(r"<[^>]+>", "", value or "").strip()

    def search(self, request: SearchRequest) -> list[SearchResult]:
        params = {"query": request.query, "rows": request.max_results}
        if self.mailto:
            params["mailto"] = self.mailto
        payload = self.http_get(f"{self.endpoint}?{urlencode(params)}")
        results = []
        for item in payload.get("message", {}).get("items", []):
            doi = item.get("DOI")
            if not doi:
                continue
            titles = item.get("title") or [doi]
            authors = [" ".join(filter(None, [author.get("given"), author.get("family")])) for author in item.get("author", [])]
            results.append(SearchResult(
                id=f"doi:{doi.lower()}",
                title=titles[0],
                url=item.get("URL") or f"https://doi.org/{doi}",
                snippet=self._text(item.get("abstract")),
                source_type="primary_study" if item.get("type") == "journal-article" else "academic_record",
                metadata={"doi": doi, "crossref_type": item.get("type"), "authors": authors, "published": item.get("published-print") or item.get("published-online")},
            ))
        return results
