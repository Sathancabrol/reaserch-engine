from engine.agents import PlannerAgent, ResearcherAgent
from engine.retrieval import InMemoryRetriever, SearchResult


def test_planner_returns_structured_plan():
    result = PlannerAgent().execute(type("C", (), {"question": "Q"})())
    assert "research_plan" in result
    assert result["research_plan"]["question"] == "Q"


def test_researcher_uses_injected_retriever():
    retriever = InMemoryRetriever([SearchResult("s1", "Q evidence", snippet="Q")])
    context = type("C", (), {"question": "Q", "state": {"queries": ["Q"]}})()
    result = ResearcherAgent(retriever).execute(context)
    assert result["search_results"][0].id == "s1"
