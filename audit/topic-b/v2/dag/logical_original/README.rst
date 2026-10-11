Topic B: paired logical proof routes
====================================

This is an authored dependency graph awaiting independent edge review. It
does not change any admitted mathematical statement. The fixed boundary is
the thirty clauses from N001, N003, N008 and the revised institutional L030
edition, matched to the complete common paper and four applications published
at commit 769322e67042671b404917b7a6249e1a5de4ef18. The corrected C10/C11 map
is authoritative.

``logical_graph.json`` contains historical and new nodes, exact source and
TeX locators, retained inputs and prerequisite-to-use arrows. Named results
are subdivided where one name would hide several substantial proof steps.
In particular, weighted-forest intersections and flag completion, the
extremal-marking converse, the Frattini maximal-chain argument, and the
spectral reconstruction have separate proof branches. These branches expose
the arguments; their number is not a measure of research quality or a
node-count compression factor.

``coverage.json`` preserves every exact accepted clause, original source
span, corrected new-owner reference, and its two proof routes. Historical
routes record identifiable uses in the printed argument. They are not a
claim that every original inference is fully expanded or independently
certified. Existing source corrections and unexpanded steps are flagged.
The historical source graph is bounded by these targets; it does not claim
to include every reference, remark, question or auxiliary example.

N001 uses the bound authored browser rendering, with its displayed line
numbers. Its original PDF remains unavailable. Browser spans are not an
invented PDF numerator. The other three sources bind both their primary PDFs
and the existing exact extractions used for documentary locators. None of
those primary texts, PDFs or rasters is exported by this packet.

Definitions and checked hypotheses are prerequisites. External classification
inputs are explicitly named and have unknown cost, never zero. Source
attribution, the six scoped Lean components, and finite validation evidence
are separate edge kinds; they are not silently used as premises of the new
written proofs. No mathematical enumeration is required by this volume.
The separate Lean module proves subgroup-generation components, not the
complete geometric applications.

There are no assigned text weights. The frozen measurement candidate is
recorded for coordination, but this graph neither adopts its metrics nor
computes a ratio. A later weighted layer must use the adopted extraction,
cover every selected character exactly once, and charge full documents.
Semantic parent and branch locators can overlap; adding their lengths would
double-count text. Per-output closures need not be minimal and do not replace
the complete-manuscript denominator. All new proof nodes occur in at least
one complete-application route.

Reproduce the generated graph in a fresh directory::

  python -B -O build.py --sources-root PRIVATE_RESEARCH_ROOT \
    --public-root PUBLIC_CHECKOUT --out FRESH_GRAPH_DIR

Check exact bindings, clauses, spans, closures, acyclicity and controls::

  python -B -O check.py --packet GRAPH_DIR \
    --sources-root PRIVATE_RESEARCH_ROOT --public-root PUBLIC_CHECKOUT \
    --out FRESH_REPORT_JSON

The checker rejects a missing source clause, altered span, dependency cycle,
zero substituted for unknown cost, invented N001 PDF coordinate, obsolete
C10 mapping, attribution presented as a proof premise, and stale counts.
Those controls validate the interface; an independent reviewer must
still review the authored edge choices before admission.
