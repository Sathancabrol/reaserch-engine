# Graph assessment v0.1

`assess_evidence_graph(graph)` translates traceable graph state into explicit
verification and sufficiency inputs. It reports weak critical claims,
unresolved contradictions, and low-relevance source identifiers; it does not
assign an opaque composite score.

The default verifier publishes these values into the existing sufficiency
contract. A critical claim is marked by `importance="critical"` or an integer
importance of at least `3`. Consequently, a run with unsupported critical
claims or unresolved contradictions continues rather than stopping from low
marginal information gain.
