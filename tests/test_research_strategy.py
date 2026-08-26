from engine.research_strategy import ResearchStrategyEngine, StrategyState

def test_contradictions_are_prioritized():
    state = StrategyState(["causal"], open_subquestions=1, unresolved_claims=1, contradictions=1, source_coverage=.5)
    actions = ResearchStrategyEngine().next_actions(state)
    assert actions[0].action_type == "investigate_contradiction"
