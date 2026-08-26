from engine.planner import AdaptivePlanner


def test_planner_creates_hybrid_plan_with_quality_gates():
    plan = AdaptivePlanner().plan("What is the effect of X on Y?")
    assert plan.research_type == "adaptive_hybrid"
    assert len(plan.subquestions) >= 4
    assert "claim_provenance" in plan.quality_gates
    assert "counter_evidence_check" in plan.quality_gates
