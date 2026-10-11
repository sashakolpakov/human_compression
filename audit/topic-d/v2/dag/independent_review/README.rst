Independent Topic D ownership and reader review
================================================

Accepted cost edition v2 (26b1424f) against logical v3 (ca1fa632). The original
cost/graph freezes remain preserved. Four requested corrections are resolved;
all complete-document and owner metric numbers remain unchanged.

This reviewer did not author the cost/reader packet. The review reuses accepted
scientific, glyph, logical and numerical evidence, and does not independently
re-adjudicate the reviewer-authored generic Lean supplement. No mathematical
program or Lean compiler is run by this review.

Independent replay, with the accepted source PDFs available under STUDY::

  python3 -B -O recount.py --study-root STUDY --packet STUDY/topic_D_dag_costs_v2 \
    --logical STUDY/topic_D_logical_dag_v3 \
    --author-pin 26b1424f96d0bb84423f79983f66d1259cd6d3de39d1515cdc6a157a963b998a \
    --out FRESH_DIRECTORY
  python3 -B -O revision_check.py --study-root STUDY \
    --costs STUDY/topic_D_dag_costs_v2 --logical STUDY/topic_D_logical_dag_v3 \
    --out FRESH_DELTA_REPORT
  node ui_check.js STUDY/topic_D_dag_costs_v2 \
    STUDY/topic_D_logical_dag_v3/logical_graph.json FRESH_UI_REPORT

The recount imports only the accepted extraction/calibration interface. It uses
an independent character-state allocator and reverse-adjacency traversal. Its
private output includes full selected-text inspection aids; those files are not
review exports and must not be published. The manifest lists the review exports.

The UI test is a minimal DOM behavior harness, not a browser-layout test. Both
reader pages and the static graph were visually inspected; the final numeric
edge-count change was viewed separately. Current graph routing is fixed by the
v2 manifest/delta and current input_bindings, not the retained v1 reader-provenance
record. Whole-paper factors and source/question credits remain unchanged.
