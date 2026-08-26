# Research Dossier v0.1

`build_dossier(run)` converts a terminal run into an evidence-first output
contract. The orchestrator attaches it automatically as `research_dossier`
when a run completes or reaches its iteration limit.

The dossier contains conclusions with their qualifying contradictions, atomic
claim statuses, an evidence matrix, bibliography, stopping decision, and
research log. All relationships are read directly from the Evidence Graph;
the builder does not infer, summarize, or fabricate scientific claims.
