# Research Engine v0.1 — Scientific Research Protocol

## 0. Status

- Version: 0.1
- Role: normative protocol for the research loop
- Scope: domain-agnostic research and evidence synthesis
- Principle: the protocol defines **what must happen**; implementations define **how it happens**.

---

# 1. Objective

Given an initial user question, produce the most defensible answer that can reasonably be obtained within the available evidence, time, tools and research budget.

The engine must optimize a multi-objective function:

```text
Answer quality = f(
  relevance,
  evidence strength,
  methodological validity,
  coverage,
  contradiction handling,
  uncertainty calibration,
  traceability,
  reproducibility
)
```

Speed is an optimization criterion, but cannot silently override evidence quality.

---

# 2. Fundamental epistemic distinctions

The engine MUST distinguish:

```text
OBSERVATION
    ≠
SOURCE
    ≠
EVIDENCE
    ≠
CLAIM
    ≠
INFERENCE
    ≠
HYPOTHESIS
    ≠
FINDING
    ≠
INTERPRETATION
    ≠
CONCLUSION
```

It must never convert an inference into a fact merely by repeating it.

It must also distinguish:

```text
source quality
    ≠
evidence strength
    ≠
claim confidence
    ≠
truth
```

---

# 3. Master protocol

```text
P0  RECEIVE
 ↓
P1  UNDERSTAND
 ↓
P2  DEFINE / SCOPE
 ↓
P3  DECOMPOSE
 ↓
P4  DESIGN RESEARCH PLAN
 ↓
P5  SEARCH
 ↓
P6  SCREEN SOURCES
 ↓
P7  EXTRACT EVIDENCE
 ↓
P8  BUILD CLAIMS
 ↓
P9  EVALUATE EVIDENCE
 ↓
P10 ANALYZE
 ↓
P11 SEARCH FOR COUNTER-EVIDENCE
 ↓
P12 ANALYZE CONTRADICTIONS
 ↓
P13 SYNTHESIZE
 ↓
P14 CRITIQUE / ATTEMPT FALSIFICATION
 ↓
P15 VERIFY CITATIONS + CLAIMS
 ↓
P16 ASSESS UNCERTAINTY
 ↓
P17 ASSESS SUFFICIENCY
 ├───────────────┐
 │ CONTINUE      │ STOP
 ↓               ↓
P18 NEXT ACTION  P19 FINALIZE
 │               ↓
 └──────→        P20 REPORT
```

Each phase has an input, output, quality gate and failure/retry condition.

---

# 4. P0 — RECEIVE

## Objective

Capture the user's request without prematurely interpreting it.

## Input

- raw user message;
- attached context when available;
- declared constraints.

## Operations

- preserve the original wording;
- identify explicit deliverables;
- identify explicit constraints;
- identify requested depth and format;
- identify whether the user asks for facts, explanation, decision support, design, prediction or creation.

## Output

`RawResearchRequest`

## Quality gate

Nothing important in the request has been silently dropped.

---

# 5. P1 — UNDERSTAND

## Objective

Construct a semantic representation of the request.

## Operations

- identify entities;
- identify relations;
- identify ambiguous terms;
- identify temporal/geographic/domain context;
- identify implicit objectives;
- identify assumptions;
- detect multiple questions hidden in one sentence.

## Output

`ProblemRepresentation`

```text
question
intent
entities
constraints
assumptions
ambiguities
context
expected_answer_type
```

## Failure conditions

- ambiguity changes the answer materially;
- scope cannot be inferred safely.

→ Ask for clarification OR branch into explicit interpretations.

---

# 6. P2 — DEFINE / SCOPE

## Objective

Make the research tractable without distorting the user's intent.

## Scope dimensions

- conceptual;
- temporal;
- geographic;
- population;
- domain;
- evidence type;
- depth;
- exclusions.

## Output

`ResearchScope`

## Quality gate

A third party should be able to understand what is and is not being investigated.

---

# 7. P3 — DECOMPOSE

## Objective

Transform a complex question into answerable sub-questions.

## Rules

Decompose when:

- the question contains several causal or logical steps;
- different evidence types are required;
- different populations or time periods are involved;
- a conclusion depends on intermediate claims;
- important definitions must be established first.

## Sub-question types

- definitional;
- descriptive;
- comparative;
- causal;
- correlational;
- explanatory;
- predictive;
- evaluative;
- methodological;
- historical;
- normative.

## Output

A dependency graph:

```text
Q0
├── Q1 definition
├── Q2 evidence
│   ├── Q2a
│   └── Q2b
├── Q3 mechanism
└── Q4 limitations
```

## Quality gate

The set of sub-questions must be sufficient to answer the parent question.

---

# 8. P4 — DESIGN RESEARCH PLAN

## Objective

Choose the most appropriate research strategy before collecting evidence.

## Plan components

- research objectives;
- sub-questions;
- search queries;
- source classes;
- inclusion/exclusion criteria;
- preferred evidence hierarchy;
- methods of analysis;
- contradiction strategy;
- verification strategy;
- stopping criteria;
- budget.

## Method selection

```text
Question type → appropriate strategy

Descriptive      → surveys / datasets / reports / observational evidence
Causal           → experiments / quasi-experiments / causal studies
Comparative      → matched comparisons / comparative studies
Qualitative      → interviews / ethnography / thematic analysis
Historical       → primary sources + historiography
Theoretical      → conceptual analysis + literature synthesis
Mixed            → mixed-method design
```

This mapping is a heuristic, not a rigid rule.

## Output

`ResearchPlan vN`

---

# 9. P5 — SEARCH

## Objective

Acquire candidate evidence efficiently and comprehensively.

## Search strategy

Use multiple complementary search modes:

1. broad discovery;
2. precise query;
3. terminology variants;
4. authoritative sources;
5. primary sources;
6. review/meta-analysis sources when appropriate;
7. counter-evidence search;
8. citation chaining;
9. recent evidence search for time-sensitive questions.

## Search diversity

The engine should avoid stopping after the first plausible narrative.

For major claims, seek:

```text
supporting evidence
       +
independent evidence
       +
contradicting evidence
       +
boundary conditions
```

## Output

`CandidateSources[]`

## Quality gate

Search coverage is sufficient for the current iteration's objective.

---

# 10. P6 — SCREEN SOURCES

## Objective

Determine which candidate sources deserve deeper extraction.

## Evaluation dimensions

- relevance;
- authority;
- methodological rigor;
- transparency;
- recency;
- independence;
- conflicts of interest;
- data quality;
- reproducibility;
- directness to the claim.

## Important rule

Do not use a single weighted score as a substitute for judgment. Preserve the dimensions separately.

## Output

`EvaluatedSource[]`

## Gate

Critical claims should preferentially use the strongest available evidence.

---

# 11. P7 — EXTRACT EVIDENCE

## Objective

Extract claim-relevant information from sources without losing provenance.

## Each evidence item records

- source ID;
- exact location;
- surrounding context;
- evidence type;
- observation/result;
- population/sample if relevant;
- method;
- direction: supports / contradicts / contextualizes / neutral;
- limitations;
- extraction confidence.

## Rule

A summary is not automatically evidence. Evidence must be traceable to the source.

## Output

`Evidence[]`

---

# 12. P8 — BUILD CLAIMS

## Objective

Convert evidence into atomic propositions that can be evaluated independently.

## Claim properties

```text
claim_id
text
claim_type
importance
status
confidence
supporting_evidence[]
contradicting_evidence[]
dependencies[]
provenance[]
```

## Claim types

- established fact;
- empirical claim;
- statistical claim;
- causal claim;
- theoretical claim;
- interpretation;
- inference;
- hypothesis;
- prediction;
- normative claim;
- unknown/unresolved.

## Quality gate

A reviewer can determine what evidence would make the claim stronger or weaker.

---

# 13. P9 — EVALUATE EVIDENCE

## Objective

Determine how strongly each evidence item bears on each claim.

## Dimensions

- directness;
- relevance;
- internal validity;
- external validity;
- consistency;
- precision;
- independence;
- methodological limitations;
- replication/convergence when available.

## Output

`EvidenceAssessment[]`

## Rule

Do not infer causal evidence from correlation merely because the narrative is plausible.

---

# 14. P10 — ANALYZE

## Objective

Apply methods appropriate to the evidence and question.

Possible operations:

- descriptive statistics;
- inferential statistics;
- effect-size analysis;
- qualitative coding;
- thematic synthesis;
- comparative analysis;
- causal reasoning;
- temporal analysis;
- theoretical integration;
- sensitivity analysis.

## Output

`AnalysisResults[]`

## Gate

Methods used must be explicit enough to audit the resulting finding.

---

# 15. P11 — SEARCH FOR COUNTER-EVIDENCE

## Objective

Actively challenge the emerging conclusion.

## Required questions

- What would disprove the leading explanation?
- What credible sources disagree?
- Are there null results?
- Are there failed replications?
- Are there alternative mechanisms?
- Are definitions being conflated?
- Are there boundary conditions?

## Output

`CounterEvidence[]`

This phase is mandatory for high-importance claims unless the question is purely procedural or trivial.

---

# 16. P12 — CONTRADICTION ANALYSIS

## Objective

Determine whether apparent disagreement is real.

## Classification

```text
Factual
Population
Contextual
Temporal
Operationalization
Methodological
Statistical
Theoretical
Semantic
Source-quality
Genuine unresolved contradiction
```

## Procedure

```text
Claim A vs Claim B
      ↓
Compare definitions
      ↓
Compare populations
      ↓
Compare methods
      ↓
Compare time/context
      ↓
Compare uncertainty
      ↓
Determine compatibility
```

## Output

`ContradictionAssessment`

---

# 17. P13 — SYNTHESIZE

## Objective

Construct the best-supported explanation or answer from the evaluated evidence.

## Rules

- prioritize critical claims;
- preserve disagreements;
- separate evidence from interpretation;
- state conditions and exceptions;
- do not average incompatible studies blindly;
- do not manufacture consensus;
- do not conceal missing evidence.

## Output

`ProvisionalSynthesis`

---

# 18. P14 — CRITIQUE / ATTEMPT FALSIFICATION

## Objective

Try to break the provisional synthesis.

## Critic checklist

- unsupported claim?
- citation mismatch?
- source overinterpretation?
- causal leap?
- selection bias?
- survivorship bias?
- publication bias?
- confounding?
- base-rate neglect?
- definition drift?
- cherry-picking?
- false consensus?
- outdated evidence?
- missing counterargument?
- overgeneralization?
- uncertainty understated?

## Output

`CritiqueReport`

## Gate

Critical failures must trigger revision or another research cycle.

---

# 19. P15 — VERIFY

## Objective

Verify the factual and provenance layer independently from synthesis.

## Checks

- every major claim has supporting evidence or is explicitly marked uncertain;
- citations actually support the associated claim;
- source metadata are correct;
- quotations are faithful when used;
- conclusions do not exceed study designs;
- contradictory evidence has not disappeared during synthesis.

## Output

`VerificationReport`

---

# 20. P16 — UNCERTAINTY ASSESSMENT

## Objective

Represent what is known, unknown and conditionally known.

Use categories such as:

```text
HIGH CONFIDENCE
MODERATE CONFIDENCE
LOW CONFIDENCE
UNRESOLVED
INSUFFICIENT EVIDENCE
```

Do not imply numerical precision unless the methodology supports calibration.

## Uncertainty sources

- measurement error;
- sampling error;
- model uncertainty;
- conflicting studies;
- sparse evidence;
- outdated evidence;
- ambiguous definitions;
- external validity limitations;
- unknown confounders;
- missing data.

---

# 21. P17 — SUFFICIENCY ASSESSMENT

## Objective

Decide whether another iteration is justified.

Evaluate:

```text
Coverage
Evidence quality
Claim support
Contradiction resolution
Uncertainty
Critical gaps
Expected information gain
Research cost
User-defined depth
```

## Decision rule

Conceptually:

```text
Continue if:
Expected information gain × importance
    >
Research cost + diminishing returns
```

This is a decision heuristic, not a literal universal equation.

## Continue when

- a critical claim remains weak;
- an important contradiction is unresolved;
- a high-value source class has not been searched;
- a plausible alternative explanation has not been tested;
- new evidence could materially change the conclusion.

## Stop when

- critical sub-questions are adequately covered;
- major claims are traceable;
- major counter-evidence has been examined;
- residual uncertainty is explicit;
- expected improvement is low;
- budget/depth constraints are reached.

## Output

`SufficiencyDecision`

---

# 22. P18 — NEXT BEST RESEARCH ACTION

If continuing, select the action with the highest expected value.

Candidate actions:

- search a new source class;
- find primary evidence;
- search a contradictory result;
- verify a citation;
- investigate a mechanism;
- narrow the population/context;
- test an alternative hypothesis;
- retrieve newer evidence;
- perform deeper methodological analysis.

The next action must target a known uncertainty or research gap.

---

# 23. P19 — FINALIZE

The final answer must contain, where relevant:

1. direct answer;
2. key findings;
3. evidence basis;
4. confidence/uncertainty;
5. important contradictions;
6. limitations;
7. unresolved questions;
8. methodology summary;
9. provenance / references.

The answer should not expose internal chain-of-thought. It should expose **auditable research artifacts and concise reasoning summaries** instead.

---

# 24. P20 — REPORT

Every completed run should be exportable as:

```text
Research Report
├── Question
├── Scope
├── Research objectives
├── Sub-questions
├── Method
├── Search strategy
├── Sources
├── Evidence map
├── Claims
├── Contradictions
├── Findings
├── Synthesis
├── Verification
├── Uncertainty
├── Limitations
├── Stopping reason
└── Final answer
```

---

# 25. Iteration protocol

A new iteration must not simply repeat the previous search.

```text
ITERATION N
    ↓
What remains uncertain?
    ↓
What could change the conclusion?
    ↓
Which evidence would resolve it?
    ↓
Which search/action obtains that evidence?
    ↓
ITERATION N+1
```

Each iteration records:

- objective;
- starting uncertainty;
- actions;
- new evidence;
- changed claims;
- changed confidence;
- newly discovered contradictions;
- decision.

---

# 26. Failure modes the engine must detect

- hallucinated source;
- citation mismatch;
- unsupported inference;
- premature closure;
- confirmation bias;
- search-engine ranking bias;
- source monoculture;
- duplicate evidence treated as independent;
- review article treated as primary evidence;
- correlation/causation confusion;
- outdated evidence;
- false precision;
- contradictory evidence omitted;
- scope drift;
- definition drift;
- overgeneralization;
- authority bias;
- publication bias;
- survivorship bias;
- selection bias;
- model-induced consensus.

---

# 27. Minimum viable implementation

A v0.1 implementation is considered protocol-compliant if it can execute:

```text
question
→ scope
→ subquestions
→ plan
→ search
→ source evaluation
→ evidence extraction
→ claim graph
→ contradiction search
→ synthesis
→ verification
→ sufficiency decision
→ final report
```

And persist the artifacts needed to reproduce the decision.

---

# 28. Test philosophy

The engine should eventually be evaluated not only on final-answer correctness, but on:

- evidence recall;
- evidence precision;
- citation correctness;
- claim-evidence alignment;
- contradiction recall;
- calibration;
- robustness to misleading sources;
- reproducibility;
- stopping quality;
- resistance to confirmation bias;
- improvement between iterations.

A research engine that produces a correct answer for the wrong reasons is not considered fully reliable.

---

# 29. Research Engine's central invariant

```text
NO IMPORTANT CONCLUSION
WITHOUT
TRACEABLE EVIDENCE

NO STRONG CONFIDENCE
WITHOUT
ADEQUATE SUPPORT

NO FINALIZATION
WITHOUT
SUFFICIENCY ASSESSMENT
```

This invariant is the core methodological contract of Research Engine v0.1.
