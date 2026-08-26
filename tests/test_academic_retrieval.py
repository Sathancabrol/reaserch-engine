from engine.retrieval import CrossrefRetriever, InMemoryRetriever, LocalFirstRetriever, SearchRequest, SearchResult


def test_crossref_retriever_maps_works_without_network():
    observed_urls = []

    def fake_get(url):
        observed_urls.append(url)
        return {"message": {"items": [{
            "DOI": "10.1000/Example", "title": ["A study"], "type": "journal-article",
            "abstract": "<jats:p>Observed <b>effect</b>.</jats:p>",
            "author": [{"given": "Ada", "family": "Lovelace"}],
        }]}}

    results = CrossrefRetriever(mailto="research@example.test", http_get=fake_get).search(SearchRequest("effect", max_results=3))

    assert "rows=3" in observed_urls[0]
    assert results[0].id == "doi:10.1000/example"
    assert results[0].snippet == "Observed effect."
    assert results[0].metadata["authors"] == ["Ada Lovelace"]


def test_local_first_avoids_external_retrieval_when_local_evidence_exists():
    local = InMemoryRetriever([SearchResult("local-1", "Effect study", snippet="Observed effect")])

    class External:
        def search(self, request):
            raise AssertionError("external retrieval should not run")

    results = LocalFirstRetriever(local, External()).search(SearchRequest("effect"))
    assert [result.id for result in results] == ["local-1"]
