# Research Engine — Hermes Integration Architecture

## Purpose

Research Engine should reuse mature agent infrastructure instead of rebuilding a generic agent runtime. Hermes Agent is treated as a reference/runtime candidate for agent execution, while Research Engine adds the scientific-research control layer.

## Architectural principle

**Do not turn Research Engine into another general-purpose agent framework.**

Separate the system into:

1. **Agent Runtime** — execution, tools, skills, sessions, MCP, model providers.
2. **Research Control Plane** — question decomposition, research planning, evidence collection, verification, stopping criteria, synthesis and evaluation.
3. **Research Knowledge Layer** — claims, sources, entities, relations, provenance, contradictions, temporal state and research history.

## Target architecture

```text
USER QUESTION
      |
      v
+---------------------------+
| QUESTION ANALYZER         |
| intent / domain / scope   |
| complexity / constraints  |
+-------------+-------------+
              |
              v
+---------------------------+
| RESEARCH PLANNER          |
| hypotheses / subquestions |
| search strategy / budget  |
+-------------+-------------+
              |
              v
+------------------------------------------------+
|              AGENT RUNTIME                     |
| Hermes / LangGraph-compatible execution layer |
|                                                |
| tools | skills | MCP | browser | code | APIs |
+----------------------+-------------------------+
                       |
                       v
+------------------------------------------------+
|              EVIDENCE ENGINE                   |
| source ingestion | claims | citations         |
| extraction | provenance | contradiction        |
+----------------------+-------------------------+
                       |
                       v
+------------------------------------------------+
|              RESEARCH GRAPH                    |
|                                                |
| Question <-> Claim <-> Evidence <-> Source    |
| Entity <-> Relation <-> Paper <-> Dataset      |
| Hypothesis <-> Finding <-> Contradiction       |
+----------------------+-------------------------+
                       |
                       v
+---------------------------+
| CRITICAL REVIEW           |
| source quality            |
| evidence coverage         |
| contradiction detection   |
| uncertainty               |
| methodological quality    |
+-------------+-------------+
              |
        enough evidence?
          /          \
        NO            YES
        |              |
        +--> RESEARCH  v
             LOOP    SYNTHESIS
                         |
                         v
                  EVALUATION
                         |
                         v
                    FINAL REPORT
```

## Hermes role

Hermes should be evaluated primarily as the **agent runtime/infrastructure layer**, not as the research methodology itself.

Potentially reusable capabilities:

- agent loop
- model/provider abstraction
- tool execution
- skills
- persistent memory
- session history/search
- MCP integration
- browser/web capabilities
- code execution
- multi-agent/task execution
- evaluation infrastructure

Research Engine should add the missing research-specific semantics above this layer.

## Research-specific state model

Every research run should maintain a durable state similar to:

```text
ResearchRun
├── question
├── objective
├── scope
├── assumptions[]
├── hypotheses[]
├── subquestions[]
├── search_tasks[]
├── sources[]
├── documents[]
├── claims[]
├── evidence[]
├── entities[]
├── relations[]
├── contradictions[]
├── gaps[]
├── decisions[]
├── evaluations[]
├── synthesis
└── stopping_reason
```

## Core loop

```text
ANALYZE
  -> PLAN
  -> SEARCH
  -> READ
  -> EXTRACT
  -> UPDATE GRAPH
  -> VERIFY
  -> IDENTIFY GAPS
  -> SEARCH AGAIN
  -> CRITIQUE
  -> SYNTHESIZE
  -> EVALUATE
  -> STOP or LOOP
```

The stopping decision must be explicit and measurable. Examples of signals:

- evidence coverage
- source quality
- source diversity
- claim verification rate
- contradiction rate
- unresolved gaps
- novelty of additional searches
- confidence/uncertainty
- research budget

## Tool discovery layer

Research Engine should maintain a **Tool Knowledge Graph** rather than a static list.

```text
Tool
├── capability[]
├── input_types[]
├── output_types[]
├── protocols[]
├── APIs[]
├── MCP_support
├── providers[]
├── license
├── language
├── maturity
├── activity
├── benchmarks[]
├── alternatives[]
└── compatibility[]
```

Possible discovery sources:

- GitHub
- MCP registries
- Hugging Face
- package registries
- academic papers
- benchmark repositories
- official documentation

This enables a future loop:

```text
RESEARCH TASK
      |
      v
REQUIRED CAPABILITIES
      |
      v
TOOL DISCOVERY
      |
      v
TOOL RANKING
      |
      v
MCP / API / LIBRARY
      |
      v
EXECUTION
```

## Recommended v0.1 boundaries

### Build

- ResearchRun state model
- Planner
- research task queue
- source/claim/evidence schema
- provenance model
- research loop
- stopping criteria
- evaluation record
- model/provider abstraction

### Reuse rather than rebuild

- generic agent loop
- generic tool calling
- MCP client/server infrastructure
- browser automation
- generic memory/session infrastructure
- provider adapters

### Keep replaceable

Hermes should be an adapter/runtime, not a hard dependency of the research domain model. The Research Engine should be able to swap Hermes for LangGraph, OpenAI Agents SDK, PydanticAI, or another runtime without rewriting the research graph and evidence layer.

## Strategic conclusion

Hermes can substantially reduce the amount of infrastructure Research Engine needs to implement. The differentiator should be the **research control plane + evidence graph + verification loop + measurable stopping criteria**, not another generic agent framework.
