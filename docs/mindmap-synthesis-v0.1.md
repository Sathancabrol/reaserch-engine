# Research Engine v0.1 — Mindmap-derived synthesis

## Purpose

This document captures architectural knowledge recovered from the project's prior mindmaps and related Cognitorium/HCSM work, then translates it into requirements for Research Engine. It is deliberately a synthesis, not a claim that the mindmaps themselves are scientific evidence.

## 1. Core idea

The Research Engine should be understood as a **research control system**, not a chatbot with search attached.

```text
USER QUESTION
      ↓
PROBLEM REPRESENTATION
      ↓
RESEARCH DESIGN
      ↓
EVIDENCE ACQUISITION
      ↓
EVIDENCE ORGANIZATION
      ↓
CRITICAL ANALYSIS
      ↓
INFERENCE / SYNTHESIS
      ↓
VERIFICATION
      ↓
SUFFICIENCY
      ↓
RESEARCH DOSSIER
```

The engine must preserve the distinction between:

```text
knowledge ≠ measurement/observation ≠ evidence ≠ inference ≠ conclusion
```

## 2. Three-graph architecture

The strongest reusable idea from the cognitive-model work is to separate three graph functions.

### A. Knowledge Graph

Represents what is known or defined in the scientific domain:

```text
CONCEPT
 ├── definition
 ├── sub-concepts
 ├── theories
 ├── models
 ├── measures
 ├── tasks
 └── literature
```

### B. Evidence Graph

Represents what sources actually provide:

```text
SOURCE
   ↓ provides
EVIDENCE
   ↓ supports / contradicts / contextualizes
CLAIM
```

### C. Inference Graph

Represents what can be inferred from evidence under explicit assumptions:

```text
EVIDENCE + CONTEXT + ASSUMPTIONS
              ↓
           INFERENCE
          ↙         ↘
 ALTERNATIVE A   ALTERNATIVE B
          \         /
             FINDING
                ↓
            CONCLUSION
```

### Architectural consequence

Research Engine should not collapse these graphs into one undifferentiated knowledge graph. They may share identifiers and edges, but their epistemic roles remain distinct.

## 3. Temporal and contextual reasoning

The HCSM work adds an important general research-engine principle: observations and inferences are often conditional on context and time.

Therefore evidence records should be able to carry, when relevant:

- temporal window;
- population;
- environment/context;
- task/procedure;
- measurement conditions;
- baseline/reference;
- alternative explanations;
- uncertainty.

This is especially important for longitudinal, behavioral, cognitive, medical, organizational and real-world research.

The principle generalizes:

```text
Evidence = observation/result + provenance + context + time + limitations
```

## 4. Multidimensional research objects

The prior cognitive and visualization work suggests that a research object should not be reduced to a scalar confidence value.

For a claim, keep distinct dimensions such as:

```text
CLAIM
├── epistemic status
├── importance
├── supporting evidence
├── contradicting evidence
├── source diversity
├── methodological support
├── population/context scope
├── temporal scope
├── uncertainty
├── alternative explanations
└── provenance
```

Similarly:

```text
source quality ≠ evidence strength ≠ claim confidence ≠ truth
```

## 5. Research hierarchy

The mindmap-derived structure suggests four levels of abstraction:

```text
LEVEL 0 — QUESTION
    What do we want to know?

LEVEL 1 — SUBQUESTIONS
    What must be established to answer it?

LEVEL 2 — EVIDENCE / CLAIMS
    What observations and arguments support or challenge each component?

LEVEL 3 — SYNTHESIS
    What answer survives critical examination?
```

A fifth cross-cutting layer is required:

```text
PROVENANCE + UNCERTAINTY + CONTEXT + TIME
```

These are not merely output metadata; they constrain interpretation.

## 6. Scientific workflow expanded

The engine's methodological backbone should cover:

```text
Observation
→ Problem definition
→ Research question
→ Literature search
→ Literature synthesis
→ Theoretical framework
→ Problematic / research gap
→ Objectives
→ Hypotheses
→ Operational hypotheses
→ Variables / constructs
→ Scope / population
→ Research design
→ Sampling
→ Inclusion / exclusion
→ Instruments
→ Pilot / pre-test when appropriate
→ Validity / reliability
→ Ethics / governance
→ Protocol
→ Data collection
→ Cleaning / coding
→ Analysis
→ Results
→ Interpretation
→ Discussion
→ Hypothesis assessment
→ Limitations
→ Conclusion
→ Perspectives / recommendations
```

This is not a rigid sequence for every question. The planner should select only the stages justified by the research design.

## 7. Research-design taxonomy

The question analyzer should be able to recognize combinations of:

- descriptive;
- exploratory;
- comparative;
- correlational;
- causal;
- experimental;
- quasi-experimental;
- qualitative;
- quantitative;
- mixed-methods;
- historical;
- theoretical/conceptual;
- systematic evidence synthesis;
- evaluative;
- predictive;
- normative/decision-support.

Research type is therefore a **set of design requirements**, not a single label.

## 8. Hypothesis discipline

The engine should distinguish:

```text
QUESTION
  ↓
HYPOTHESIS
  ↓
PREDICTION / OPERATIONALIZATION
  ↓
EVIDENCE
  ↓
TEST / ANALYSIS
  ↓
RESULT
```

It must not invent a hypothesis when the research question is descriptive or purely exploratory. Conversely, causal and confirmatory questions should expose the assumptions and predictions needed to test the proposed explanation.

## 9. Exploratory vs confirmatory

These modes must remain explicit:

```text
EXPLORATORY
→ discover patterns
→ generate hypotheses
→ map the evidence landscape

CONFIRMATORY
→ test pre-specified claims/hypotheses
→ evaluate predictions
→ control analytic flexibility
```

A single research run may contain both, but the transition must be recorded.

## 10. Evidence triangulation

For important claims, the engine should seek multiple dimensions of support:

```text
DIRECT EVIDENCE
      +
INDEPENDENT EVIDENCE
      +
COUNTER-EVIDENCE
      +
BOUNDARY CONDITIONS
      +
METHODOLOGICAL CRITIQUE
```

Repeated copies of the same source are not independent confirmation.

## 11. Uncertainty as a first-class object

The engine should represent uncertainty as a structured object rather than a vague disclaimer.

```text
UNCERTAINTY
├── source limitations
├── measurement uncertainty
├── sampling uncertainty
├── model uncertainty
├── conflicting evidence
├── missing evidence
├── contextual uncertainty
├── temporal uncertainty
└── inference uncertainty
```

The final report should state which uncertainty could still change the conclusion.

## 12. Research stopping as an epistemic decision

Stopping is not simply a token or time limit.

```text
CURRENT CONCLUSION
      ↓
WHAT COULD CHANGE IT?
      ↓
WHAT EVIDENCE WOULD RESOLVE THAT?
      ↓
CAN WE OBTAIN IT?
      ↓
EXPECTED INFORMATION GAIN
      ↓
STOP / CONTINUE
```

If a critical uncertainty remains and accessible evidence could materially reduce it, the engine should continue.

If uncertainty is irreducible with available evidence, it should stop **and document that irreducibility**.

## 13. Cognition as a benchmark domain

The cognitive-science work should be used as a demanding benchmark for Research Engine, not hard-coded into the generic core.

A cognition research run may require:

```text
CONSTRUCTS
↓
THEORIES / MODELS
↓
TASKS / MEASURES
↓
OBSERVATIONS
↓
CONTEXT
↓
INFERENCE
↓
ALTERNATIVE EXPLANATIONS
↓
COGNITIVE STATE / FINDING
```

The generic engine should support this structure through extensible entities and relations.

## 14. Cognitorium integration boundary

Cognitorium can later consume Research Engine outputs as evidence-backed knowledge.

```text
Research Engine
    ↓
validated claims / findings / provenance
    ↓
Cognitorium knowledge layer
    ↓
concepts / competencies / trajectories / representations
```

Research Engine should not depend on Cognitorium to function. The dependency direction should remain:

```text
Research Engine → produces auditable knowledge
Cognitorium     → consumes / represents / contextualizes it
```

## 15. Implementation priorities derived from the mindmaps

1. Keep the three epistemic layers distinct: knowledge, evidence, inference.
2. Make context/time first-class where the domain requires it.
3. Make hypotheses and operationalization explicit rather than implicit.
4. Preserve exploratory/confirmatory status.
5. Represent alternatives and counter-evidence.
6. Preserve multidimensional uncertainty rather than one opaque score.
7. Make the research plan adaptive but auditable.
8. Treat cognition/HCSM as a benchmark domain and extensibility test.
9. Keep provenance through every transformation.
10. Make the final dossier reconstructible from the underlying graph and research log.

## 16. Target architecture

```text
                         USER
                          │
                          ▼
                  QUESTION ANALYZER
                          │
                          ▼
                   RESEARCH DESIGN
                          │
                          ▼
                    PLAN / BUDGET
                          │
                          ▼
                 AUTONOMOUS RESEARCH LOOP
                          │
          ┌───────────────┼────────────────┐
          ▼               ▼                ▼
    KNOWLEDGE GRAPH   EVIDENCE GRAPH   INFERENCE GRAPH
          │               │                │
          └───────────────┼────────────────┘
                          ▼
                  CRITICAL REVIEW
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
          UNCERTAINTY             CONTRADICTIONS
              └───────────┬───────────┘
                          ▼
                    SUFFICIENCY
                      /      \
                 CONTINUE      STOP
                    │           │
                    ▼           ▼
              NEXT ACTION    DOSSIER
```

## Status

This synthesis is an architectural input derived from prior project work. It must itself remain open to criticism and should not be treated as scientific evidence merely because it came from a mindmap or previous design discussion.
