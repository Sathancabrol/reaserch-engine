# Run persistence v0.1

`JsonRunStore` is the local persistence boundary for Research Engine v0.1. It
stores one JSON document per run and replaces it atomically after each
checkpoint, avoiding half-written checkpoints after interruption.

Each document preserves the run identifier, question, state-machine state,
iteration, monotonic revision, agent history, context, and the complete
Evidence Graph snapshot. `JsonRunStore.load()` reconstructs the graph so a
caller can inspect it or resume with its own orchestration policy.

The default orchestrator checkpoints after initialization, every agent result,
and a terminal outcome. It intentionally does not silently resume a run: retry
and resume policy remain a future operational layer, where budgets, provider
idempotency and human approval can be defined explicitly.
