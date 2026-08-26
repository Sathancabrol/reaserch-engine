# Research Engine v0.1 — Product Requirements

## Vision
Research Engine is an autonomous research assistant. A user provides an input/question; the engine independently determines the appropriate research methodology, conducts the research with available tools and evidence, iterates until the evidence is sufficiently complete, and returns the equivalent of a scientifically rigorous research study plus its documentation.

## Core principle
Optimize the **research process and evidential reliability**, not merely answer fluency.

## User contract
Input: natural-language research request, constraints, desired depth if supplied.

Output: a documented research product containing:
- research question and interpretation;
- scope and assumptions;
- methodology selected and rationale;
- research plan and subquestions;
- literature/source landscape;
- evidence and provenance;
- claims and their support/contradiction;
- synthesis and competing explanations;
- uncertainty and limitations;
- verification/audit report;
- conclusion answering the original request;
- references.

If evidence is insufficient, the engine must say so and identify what remains unknown rather than fabricate certainty.

## Methodology
Hybrid methodology:
1. fixed scientific-quality gates and provenance rules;
2. adaptive planning according to question type, domain, evidence availability, contradictions and information gain.

The engine should emulate the useful behaviors of an expert human researcher: decomposition, source prioritization, triangulation, criticism, counter-evidence search, iterative refinement and stopping when marginal information gain is low or critical uncertainty is acceptably bounded.

## Source policy
Local sources have priority. The engine should first inspect user-provided/local corpora when available, then expand to external sources when necessary. Sources must be classified (e.g. primary study, systematic review, meta-analysis, institutional source, secondary source, opinion, unverified web source).

## Epistemic requirements
- Every material claim should have provenance where evidence exists.
- Contradictory evidence must be preserved and surfaced.
- Source quality and relevance must be distinguished from agreement with the current hypothesis.
- The engine must separate evidence, inference and conclusion.
- Uncertainty must be explicit.
- No universal numeric "truth score" should replace qualitative scientific judgment.

## Autonomy target
End state: one input → one autonomous research run → final documented study, with no need for the user to manually orchestrate searches between iterations, assuming required tools/data access are available.

## v0.1 non-goals
- perfect scientific truth;
- autonomous real-world experiments;
- unrestricted access to paywalled/private databases;
- replacing domain experts in high-stakes decisions;
- claiming peer review or publication status that did not occur.

## Architecture implication
The LLM is an interchangeable reasoning component, not the source of truth. The engine owns state, provenance, evidence graph, quality gates, iteration and stopping logic.
