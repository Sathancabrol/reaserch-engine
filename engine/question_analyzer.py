"""Question analysis and research-design classification for v0.1."""
from dataclasses import dataclass, field

@dataclass
class QuestionAnalysis:
    original: str
    normalized: str
    research_types: list[str] = field(default_factory=list)
    intents: list[str] = field(default_factory=list)
    ambiguities: list[str] = field(default_factory=list)
    constraints: dict = field(default_factory=dict)

class QuestionAnalyzer:
    """Deterministic baseline classifier; an LLM can enrich the result later."""
    def analyze(self, question: str) -> QuestionAnalysis:
        q = " ".join(question.strip().split())
        low = q.lower()
        types = []
        if any(x in low for x in ("compare", "versus", "vs ", "différence", "meilleur")): types.append("comparative")
        if any(x in low for x in ("cause", "causes", "pourquoi", "effect", "impact", "effet")): types.append("causal")
        if any(x in low for x in ("combien", "mesure", "taux", "prévalence", "corrélation")): types.append("quantitative")
        if any(x in low for x in ("comment", "expérience", "test", "évaluer")): types.append("empirical")
        if any(x in low for x in ("histoire", "historique", "évolution", "origine")): types.append("historical")
        if any(x in low for x in ("doit", "devrait", "meilleur", "recommand")): types.append("normative")
        if not types: types.append("exploratory")
        intents = ["answer_question"] if "?" in q else []
        return QuestionAnalysis(q, q, list(dict.fromkeys(types)), intents, [], {})
