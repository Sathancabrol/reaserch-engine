# Research Lifecycle v0.1

## Purpose

Reference protocol for turning an arbitrary user question into a structured research investigation.

## Phase 1 — Understand

- capture the original question verbatim;
- identify intent;
- detect ambiguity;
- identify domain and context;
- identify temporal and geographic scope;
- identify constraints;
- define what a satisfactory answer would contain.

Output: `ProblemRepresentation`.

## Phase 2 — Decompose

Transform the question into independent sub-questions:

- definitional;
- descriptive;
- comparative;
- causal;
- explanatory;
- predictive;
- evaluative;
- contextual.

Output: `SubQuestion[]`.

## Phase 3 — Plan

For each sub-question determine:

- evidence required;
- source types preferred;
- search queries;
- inclusion/exclusion criteria;
- expected analysis;
- uncertainty risks;
- stopping criteria.

Output: `ResearchPlan`.

## Phase 4 — Search

Search broadly enough to identify the landscape, then narrow toward high-value sources.

Record every meaningful search action and its provenance.

Separate:

- discovery sources;
- primary evidence;
- secondary synthesis;
- contextual sources.

## Phase 5 — Screen

Evaluate candidate sources against relevance and quality criteria before relying on them.

Reject or downgrade:

- irrelevant material;
- duplicate evidence;
- unsupported assertions;
- sources whose methods cannot support the claimed conclusion;
- materially outdated sources when current evidence is required.

## Phase 6 — Extract

Extract atomic claims and the smallest useful evidence units.

For every extracted item preserve:

- source;
- exact location;
- context;
- interpretation;
- limitations.

## Phase 7 — Evaluate

Evaluate separately:

- source quality;
- evidence strength;
- claim confidence.

Do not infer certainty solely from publication venue or source reputation.

## Phase 8 — Analyze

Select the analysis method appropriate to the question and evidence.

Potential modes:

- descriptive;
- comparative;
- correlational;
- causal;
- qualitative;
- quantitative;
- mixed-methods;
- systematic synthesis.

## Phase 9 — Challenge

Actively seek disconfirming evidence.

Ask:

- What would make the current conclusion wrong?
- Which credible sources disagree?
- Are there alternative explanations?
- Are definitions or populations different?
- Is there publication or selection bias?

Output: contradiction and uncertainty map.

## Phase 10 — Synthesize

Construct the strongest answer supported by the evidence.

The synthesis must distinguish:

- established findings;
- strong but incomplete evidence;
- plausible interpretations;
- hypotheses;
- unknowns.

## Phase 11 — Verify

Attempt to verify major claims independently when practical.

Check:

- factual consistency;
- citation-to-claim alignment;
- arithmetic or logical consistency;
- temporal consistency;
- contradiction handling;
- scope of conclusions.

## Phase 12 — Sufficiency

Ask whether further research is likely to materially improve the answer.

Continue if:

- a critical sub-question remains unanswered;
- a major contradiction is unresolved;
- an important claim has weak provenance;
- high-value evidence has not been searched;
- a new search has meaningful expected information gain.

Stop if:

- critical uncertainty is acceptably characterized;
- additional evidence is unlikely to change the conclusion;
- the research budget is exhausted;
- user-defined depth has been reached.

## Phase 13 — Finalize

Return:

1. direct answer;
2. key findings;
3. supporting evidence;
4. important disagreements;
5. confidence / uncertainty;
6. limitations;
7. unresolved questions;
8. sources and provenance;
9. stopping reason.

## Phase 14 — Learn

After completion, record reusable knowledge:

- new concepts;
- source patterns;
- methodological lessons;
- failed search strategies;
- contradiction patterns;
- benchmark cases.

This is the mechanism by which the Research Engine improves between runs without silently changing the evidence of past runs.
