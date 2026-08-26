# Research Engine v0.1 — Executable Architecture

## Goal

Turn a user question into an auditable research run. The engine must separate orchestration from model providers and retrieval providers, preserve provenance, represent supporting and contradicting evidence, and stop only when explicit sufficiency criteria are met.

## Core loop

```text
Question
  -> Planning
  -> Retrieval
  -> Evidence extraction
  -> Claim construction
  -> Contradiction analysis
  -> Synthesis
  -> Verification
  -> Sufficiency decision
       |-- stop -> final answer
       `-- continue -> next best research action -> next iteration
```

## Components

- `ResearchRun`: persistent state and provenance boundary.
- `state_machine`: legal lifecycle transitions.
- `Orchestrator`: coordinates agents and iterations.
- `retrieval`: provider-neutral search contract.
- `providers`: registry for interchangeable retrieval backends.
- `evidence_graph`: explicit epistemic relationships.
- `evidence_extractor`: converts retrieval results into traceable evidence.
- `claims`: attaches evidence and computes basic claim status.
- `sufficiency`: transparent stopping logic.
- `actions`: next-best-action selection.
- `quality`: measurable quality/gap signals.
- `agents`: structured contracts for LLM-backed implementations.

## Design principles

1. **Provenance first** — every evidence item keeps a source identifier.
2. **Claims are not facts** — a claim has a support state and can be mixed or contradicted.
3. **Contradictions are first-class** — disagreement triggers investigation rather than silent averaging.
4. **Provider independence** — retrieval and model providers are replaceable.
5. **Explicit uncertainty** — unknown is a valid result.
6. **Bounded autonomy** — every run has iteration limits and stopping criteria.
7. **Auditable actions** — each iteration records why the next action was selected.
8. **No fake confidence** — quality signals are separated from truth claims.

## v0.1 boundary

v0.1 provides the core contracts, deterministic primitives, testable orchestration, and provider seams. Production Web/academic retrieval, LLM structured-output adapters, advanced source quality scoring, citation parsing, and persistent storage are intentionally subsequent layers.
