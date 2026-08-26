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

See `docs/product-requirements-v0.1.md` and `docs/research-output-spec-v0.1.md` for the product and output contracts.
