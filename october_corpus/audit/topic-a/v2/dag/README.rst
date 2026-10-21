Topic A: source and replacement arguments
========================================

This packet connects the six admitted Topic A source contracts to the current
common theory, six complete applications, and complete required program appendix.
It adds a portable checker and an offline explorer to the independently accepted
logical-v3 and weighted-v2 records. It adds no mathematical result, source credit,
or new compression claim. The displayed whole-document factors come unchanged
from the separately admitted measurement.

``inputs/logical`` contains the 236 mathematical/documentary nodes and 392 directed
edges. ``inputs/weighted`` contains the exclusive ownership of all 341 selected
text spans, their ten metric coordinates, and the documented dependency unions.
Their independent reviews are copied alongside them. These frozen bytes remain
separate from ``render.py`` and the derived visual files.

Reading the graph
-----------------

Open ``explorer.html`` after publication, or ``visual/explorer.html`` in this
private staging packet. No web service or third-party JavaScript is required.
Choose a source/application pair and click a box for exact locators, paid text,
prerequisites, retained unknown costs, and documentary qualifications. Current
proof links point to the published TeX/PDF files; historical source links are
recorded primary URLs. The measured edition is identified separately when its
title differs from the journal catalogue title.

Solid arrows run from a prerequisite to its use. Comparison and attribution links
are optional dashed arrows and are listed separately from proof prerequisites.
Named-result mode replaces displayed branches with their grouping result, even
when that grouping node itself is not in the fine dependency closure. Expanded
mode retains the original fine graph. Additional paid-text boxes have no invented
mathematical arrows. The complete selected text is paid even when it is outside a
particular result's recorded dependency closure.

Box costs can overlap; totals count each passage once. All four computational
aliases refer to the same complete appendix owner. External proof costs and
unmeasured diagram/image costs remain unknown, never zero. Grouping parents are
not charged again on top of their children. Node categories and granularity differ
between source and replacement arguments; there is no node-count compression
factor. A recorded prerequisite union is not a minimum or complete proof cost.

Conditional application factors prepay both the WHOLE common theory and the WHOLE
complete program appendix. The complete written-topic coordinate charges the full
common theory and applications; the program-inclusive coordinate also charges the
complete appendix. Neither coordinate measures the unextracted scientific image
content or unknown retained external proofs.

Reproduction
------------

Use Python 3 with the bound ``pypdf==6.13.0`` extraction version. From the packet
root (or its published location), run::

  python3 -B -O check.py \
    --sources-root /path/to/private/primary-root \
    --artifacts-root /path/to/public/repository \
    --out /fresh/accounting-replay

The primary root must contain the six exact ``sources/`` PDF paths recorded in
``protocol.json``. No primary PDF, extraction, or raster is distributed here. The
artifact root supplies the current ``papers/topic-a/v2`` TeX, PDFs, and four full
program files. The checker verifies those source editions and current proof
locators, re-extracts all 14 documents, checks exclusive ownership and all 420
measurement cells, and tests seven deliberate corruptions. It does not rerun GAP
or Lean and does not reprove the mathematical implications.

The 93 historical extracted-text evidence spans remain bound reviewed archive
evidence, not freshly replayed text-locator files. The six historical PDF editions
and all measured selected-text ownership spans are freshly checked. The adapter
does not require archived Markdown, private TXT files, or a Git archive worktree.
Original author/reviewer scripts are copied as provenance; use this adapter for
the current-tree replay rather than invoking their old private paths.

To regenerate the derived view and check its interface, use Node.js and Python::

  python3 -B render.py --out /fresh/visual
  node test_explorer.js /fresh/visual/explorer.html /fresh/visual/default_view.svg \
    > /fresh/visual/javascript_checks.json
  python3 -B -O check_visual.py --visual-dir /fresh/visual \
    --out /fresh/visual-report.json

The JavaScript test uses a small DOM harness, not a browser layout engine. It
checks all 12 source/replacement pair views, exact collapsed-route membership,
the A2 parent regression, current proof/source links, logical-versus-comparison
details, all ten cost coordinates, and the complete expanded graph. The separate
projection checker compares the derived data directly with the frozen records
and rejects four corruptions. ``default_view.svg`` is a static export of the
default paired view; ``overview.dot`` is a full named-result Graphviz description.

Publication layout and trust boundary
------------------------------------

``publication_map.json`` explicitly maps the private packet into
``audit/topic-a/v2/dag``. The four visual assets and their two check reports are
flattened from ``visual/`` into that root. In particular, the explorer must be
published at ``audit/topic-a/v2/dag/explorer.html``: its relative proof links assume
that depth. ``inputs/`` and all adapter files keep their relative paths.

The core/input manifest and derived-view manifest can be reviewed separately.
The outer manifest binds both and the explicit publication map. Existing frozen
mathematical and measurement packets are unchanged. Independent review of this
adapter and visual layer is recorded in ``../dag_admission.json``. Original
manifests retain their earlier author-freeze status; the current admission
is separate. ``publication_revision.json`` records the sole status-text
adaptation to the reviewed packet.
