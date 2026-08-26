from engine.question_analyzer import QuestionAnalyzer

def test_classifies_comparative_causal_question():
    a = QuestionAnalyzer().analyze("Quelle est la différence et l'effet de X ?")
    assert "comparative" in a.research_types
    assert "causal" in a.research_types
