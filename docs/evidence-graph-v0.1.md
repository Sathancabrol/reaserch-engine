# Evidence Graph v0.1

## Purpose

The graph is the auditable bridge between retrieval and a research conclusion.
It is an in-memory core object, deliberately independent of a graph database.
Persistence adapters should store its JSON snapshot without changing the
meaning of nodes or edges.

## Canonical chain

```text
Source --provides--> Evidence --supports|contradicts--> Claim
Claim --conflicts_in--> Contradiction --qualifies--> Conclusion
Claim --informs---------------------------------------> Conclusion
```

- A `source` identifies the retrieved material and its metadata.
- An `evidence` record has non-empty extracted content and exactly one source.
- A `claim` is an atomic proposition. Claim status is derived from attached
  supporting and contradicting evidence, not generated prose.
- A `contradiction` refers to at least two existing claims and has an explicit
  classification, such as methodological, contextual or empirical.
- A `conclusion` is linked to the claims that inform it and any contradictions
  that qualify it.

## Orchestration contract

The orchestrator creates one `EvidenceGraph` per `ResearchRun` in its context.
The default evidence analyst registers every retrieved `SearchResult` as a
source and deterministic evidence record. It does not invent claims. Provider
agents can submit structured `claim_drafts`, `contradictions` and a
`conclusion_draft`; only drafts with the required identifiers are linked.

After each graph-aware stage, a JSON-safe `evidence_graph_snapshot` is placed
in the run context. This keeps the injected-agent API compatible while giving
synthesis, verification and sufficiency adapters a stable read model.

## Current boundary

v0.1 does not yet persist graph revisions, compute weighted confidence, or
automatically discover semantic contradictions. Those are the next adapters on
top of this stable provenance model; the sufficiency controller can already use
their resulting unresolved-contradiction and weak-claim counts.
