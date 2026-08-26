# Research Engine v0.1 — Architecture

## Purpose

This document defines the reference architecture for Research Engine v0.1.

Research Engine is a closed-loop research orchestrator. Its purpose is not merely to retrieve documents or generate text, but to transform a question into an auditable chain of reasoning:

`question → problem representation → research plan → evidence → evaluation → synthesis → critique → sufficiency decision → iteration or answer`

## Architectural principles

1. Question-first: scope the question before searching.
2. Evidence-first: important claims must have provenance.
3. Atomic claims: claims should be independently assessable.
4. Source criticism: source quality and evidence strength are distinct.
5. Contradiction-aware: disagreement is explicitly represented.
6. Uncertainty-aware: confidence must reflect evidence and limitations.
7. Method-question alignment: choose methods appropriate to the research question.
8. Exploratory/confirmatory separation.
9. Iterative research: use unresolved uncertainty to select the next action.
10. Explicit stopping: every run records why research stopped.
11. Reproducibility: preserve plans, sources, transformations and decisions.
12. Human review: unresolved or high-impact cases may be escalated.

## Logical architecture

```text
┌─────────────────────────────────────────────────────┐
│                    INTERFACE / API                   │
└──────────────────────────┬──────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                      │
│ question router · planner · state machine · loop    │
│ controller · budget · stopping controller            │
└──────────────────────────┬──────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────┐
│                  SPECIALIZED AGENTS                  │
│ problem · researcher · source critic · evidence     │
│ methodology · contradiction · synthesizer · verifier │
└──────────────────────────┬──────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────┐
│             KNOWLEDGE / EVIDENCE GRAPH              │
│ questions · claims · sources · evidence · concepts   │
│ theories · hypotheses · findings · contradictions   │
│ provenance                                           │
└──────────────────────────┬──────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────┐
│                ANALYSIS / SYNTHESIS                  │
│ qualitative · quantitative · comparative · causal   │
│ uncertainty · robustness · synthesis                │
└──────────────────────────┬──────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────┐
│             PERSISTENCE / OBSERVABILITY              │
│ runs · artifacts · logs · versions · metrics        │
└─────────────────────────────────────────────────────┘
```

## Research state machine

```text
RECEIVED
  ↓
UNDERSTANDING
  ↓
SCOPING
  ↓
PLANNING
  ↓
SEARCHING
  ↓
SCREENING
  ↓
EXTRACTING
  ↓
EVALUATING
  ↓
ANALYZING
  ↓
SYNTHESIZING
  ↓
CRITIQUING
  ↓
VERIFYING
  ↓
SUFFICIENCY_CHECK
  ├── CONTINUE → PLANNING
  ├── BLOCKED  → HUMAN_REVIEW
  └── SUFFICIENT → FINALIZING
```

## Core entities

### ResearchRun

The immutable audit envelope for one investigation. It links all plans, iterations, artifacts and decisions.

Minimum fields:

- `run_id`
- `question_id`
- `created_at`
- `status`
- `iteration`
- `scope`
- `plan_versions`
- `sources`
- `claims`
- `evidence`
- `contradictions`
- `findings`
- `analyses`
- `decisions`
- `stopping_reason`
- `final_answer`

### ResearchQuestion

Stores the original question and its normalized, scoped representation.

### SubQuestion

A decomposed question required to answer the parent question reliably.

### ResearchPlan

Contains objectives, sub-questions, hypotheses, search strategy, source strategy, analysis plan, expected evidence and stopping criteria.

### Source

Represents an external information source with provenance and quality dimensions.

### Evidence

Represents a specific extract, result, dataset observation or other support for/against a claim.

### Claim

An atomic proposition that can be evaluated independently.

### Hypothesis

A provisional explanatory proposition with a theoretical basis and testable prediction when applicable.

### Finding

An output of analysis grounded in evidence.

### Contradiction

An explicit relationship between claims or findings that appear inconsistent, plus analysis of whether the conflict is substantive, methodological, contextual or semantic.

### Concept / Theory / Model

Reusable knowledge structures connecting claims and research questions across runs.

## Evidence graph

```text
SOURCE ──supports────────→ CLAIM
SOURCE ──contradicts─────→ CLAIM
SOURCE ──describes───────→ STUDY
STUDY ──produces─────────→ FINDING
CLAIM ──depends_on───────→ CLAIM
CLAIM ──derived_from─────→ DATA
CLAIM ──instantiates─────→ CONCEPT
THEORY ──predicts────────→ CLAIM
HYPOTHESIS ──tested_by───→ STUDY
FINDING ──updates────────→ MODEL
CLAIM ──conflicts_with──→ CLAIM
```

## Agent contracts

### Orchestrator

Owns workflow state. It may schedule work, reject incomplete artifacts and trigger iterations. It must not fabricate evidence.

### Problem Analyst

Produces a structured problem representation, assumptions, scope, ambiguity list and sub-question decomposition.

### Researcher

Produces candidate sources and evidence with search provenance. It must distinguish discovery from verification.

### Source Critic

Evaluates relevance, authority, methodological rigor, transparency, recency, independence, conflicts of interest and reproducibility.

### Evidence Analyst

Maps evidence to atomic claims and evaluates relevance, directness, consistency and limitations.

### Methodology Critic

Checks whether the design and analysis of a study justify the interpretation attributed to it.

### Contradiction Analyst

Searches for counter-evidence and classifies disagreement: factual, contextual, population, operationalization, temporal, methodological, statistical, theoretical or semantic.

### Synthesizer

Builds the evidence-weighted synthesis while retaining uncertainty and disagreement.

### Verifier

Attempts to falsify, weaken or find missing evidence for the synthesis.

### Sufficiency Controller

Determines whether another research action has enough expected value to justify another iteration.

## Research loop

Each iteration asks:

1. What do we currently believe?
2. Which major claims support that belief?
3. What evidence contradicts it?
4. What uncertainty remains?
5. Which next action has the highest expected information gain?
6. Would that action materially change the conclusion?

```text
CURRENT STATE
   ↓
UNCERTAINTY MAP
   ↓
RESEARCH GAPS
   ↓
CANDIDATE ACTIONS
   ↓
ACTION SELECTION
   ↓
NEW EVIDENCE
   ↓
GRAPH UPDATE
   ↓
CRITIQUE
   ↓
SUFFICIENCY
```

## Quality gates

1. Question quality
2. Search coverage
3. Evidence quality
4. Claim traceability
5. Methodological validity
6. Contradiction coverage
7. Synthesis validity
8. Sufficiency

A run cannot be considered complete merely because the model can produce fluent prose.

## Stopping criteria

Stopping can be triggered by one or more of:

- critical sub-questions sufficiently answered;
- evidence saturation;
- convergence of independent evidence;
- marginal information gain below threshold;
- remaining uncertainty is not reducible with available sources;
- research budget reached;
- user-defined depth reached;
- human review required.

The stopping decision itself is an auditable artifact.

## Confidence model

Do not collapse all uncertainty into a single source score. Keep at least three dimensions distinct:

`source quality ≠ evidence strength ≠ claim confidence`

Confidence should be accompanied by a rationale and uncertainty description. Numeric calibration can be introduced after v0.1 benchmarks exist.

## Reproducibility

Every run should preserve:

- original question;
- normalized question;
- scope;
- plan versions;
- search actions;
- source identifiers;
- evidence locations;
- transformations;
- analysis configuration;
- agent decisions;
- iteration history;
- stopping decision.

## Security and governance

The architecture must eventually support:

- secret isolation;
- source access permissions;
- prompt/tool boundary enforcement;
- untrusted-content handling;
- provenance preservation;
- data minimization;
- human approval for high-impact actions.

## v0.1 implementation boundary

v0.1 is primarily a **methodological and data-model foundation**. It does not require a fully autonomous production agent system. The repository should first establish stable concepts, schemas, protocols, agent contracts and benchmark cases.

The recommended progression is:

`methodology → schemas → benchmark cases → orchestration → retrieval adapters → persistence → adaptive research`
