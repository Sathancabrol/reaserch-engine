"""Transparent quality signals for research runs."""


def assess_claims(claims):
    total = len(claims)
    supported = sum(c.get("status") in {"supported", "verified"} for c in claims)
    contradicted = sum(c.get("status") == "contradicted" for c in claims)
    mixed = sum(c.get("status") == "mixed" for c in claims)
    return {
        "claim_count": total,
        "supported_count": supported,
        "contradicted_count": contradicted,
        "mixed_count": mixed,
        "support_ratio": supported / total if total else 0.0,
    }


def identify_gaps(subquestions, claims):
    answered = {c.get("subquestion_id") for c in claims if c.get("status") in {"supported", "verified"}}
    return [q for q in subquestions if q.get("id") not in answered and q.get("status") != "blocked"]
