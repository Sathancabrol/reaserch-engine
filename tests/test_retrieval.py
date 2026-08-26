from engine.retrieval import InMemoryRetriever, SearchRequest, SearchResult


def test_in_memory_retrieval_is_deterministic():
    retriever = InMemoryRetriever([
        SearchResult("1", "Cognitive science methods", snippet="experimental methods"),
        SearchResult("2", "Unrelated topic", snippet="cooking"),
    ])
    results = retriever.search(SearchRequest("cognitive methods", max_results=5))
    assert [r.id for r in results] == ["1"]
