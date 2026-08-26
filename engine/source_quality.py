"""Transparent source classification and quality dimensions."""

SOURCE_TYPES = {
    "primary_study", "systematic_review", "meta_analysis", "institutional_report",
    "academic_book", "academic_record", "thesis", "secondary_source", "opinion", "unverified_web",
}


def classify_source(*, source_type: str, peer_reviewed: bool | None = None,
                    direct_evidence: bool = False, transparent_methods: bool | None = None,
                    relevant: bool = True) -> dict:
    if source_type not in SOURCE_TYPES:
        source_type = "unverified_web"
    return {
        "source_type": source_type,
        "peer_reviewed": peer_reviewed,
        "direct_evidence": direct_evidence,
        "transparent_methods": transparent_methods,
        "relevance": "high" if relevant else "low",
    }


def quality_flags(metadata: dict) -> list[str]:
    flags = []
    if metadata.get("relevance") == "low":
        flags.append("low_relevance")
    if metadata.get("peer_reviewed") is False:
        flags.append("not_peer_reviewed")
    if metadata.get("transparent_methods") is False:
        flags.append("methods_not_transparent")
    return flags
