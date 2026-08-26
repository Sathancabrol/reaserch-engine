# Research Engine

Research Engine v0.1 is an autonomous research-assistant core designed to turn one natural-language input into a rigorous, documented research dossier.

## Design principles

- **Local-first evidence**: inspect user/local sources before expanding externally when available.
- **Hybrid methodology**: fixed scientific-quality gates + adaptive strategy based on question type, evidence gaps, contradictions and expected information gain.
- **Evidence over fluency**: the LLM is a reasoning component; the engine owns research state, provenance, verification and stopping logic.
- **Auditability**: important conclusions should be traceable through claims, evidence and sources.
- **Explicit uncertainty**: mixed or insufficient evidence must remain visible.
- **Autonomous iteration**: search → evidence → claims → contradiction analysis → synthesis → verification → sufficiency → next action.

## Current v0.1 core

```text
User input
  -> Question analysis
  -> Research planning
  -> Adaptive strategy
  -> Research agents/tools
  -> Evidence + claims
  -> Contradiction analysis
  -> Synthesis
  -> Verification
  -> Sufficiency / stopping
  -> Final research dossier
```

Core modules include the state machine, dependency-injected orchestrator, adaptive planner/strategy components, source-quality model, sufficiency gates and tests.

## Evidence graph increment

The v0.1 core now records an inspectable chain:

```text
Source --provides--> Evidence --supports|contradicts--> Claim
Claim --conflicts_in--> Contradiction --qualifies--> Conclusion
```

`EvidenceGraph` validates endpoints and preserves the source of each evidence
record. The default pipeline adds retrieved sources and extracted evidence to
the run graph; provider agents may add explicit claim, contradiction and
conclusion drafts. A JSON-safe snapshot is published as
`run.context["evidence_graph_snapshot"]` for dossiers and persistence adapters.

## Checkpointing

`JsonRunStore` saves atomic, JSON-readable checkpoints of a research run,
including the graph and agent history. Pass it to `Orchestrator(..., store=...)`
to checkpoint the initialized run, each completed agent step, and the final
decision. This makes interrupted runs inspectable and recoverable without a
database dependency.

See `docs/product-requirements-v0.1.md` and `docs/research-output-spec-v0.1.md` for the product and output contracts.
