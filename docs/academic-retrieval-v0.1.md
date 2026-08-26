# Academic retrieval v0.1

`CrossrefRetriever` implements the existing retrieval protocol against the
public Crossref Works API. It maps DOI-backed records into `SearchResult`
objects, preserving raw Crossref metadata for later source criticism. It makes
no request until `search()` is called.

`LocalFirstRetriever(local, external)` is the default composition pattern:
results from user-provided or local corpora are returned first; external search
is called only when local retrieval finds nothing. The engine does not treat a
Crossref record as proof—each result still goes through evidence extraction,
quality assessment, and contradiction analysis.
