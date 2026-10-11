The corrected locally projective quotient census
===============================================

This is an author proof packet for the complete two-page Hartley–Leemans 2006
erratum L084. Independent root review and principal admission are still pending.
It does not claim recovery of the separate original L095 or any new conjecture.
No public repository files have been changed.

Read ``semisparse-quotient-census.pdf`` (four pages), then the five-page
``corrected-census.pdf`` and four-page ``required-programs.pdf``. The original
source tables remain literal in ``source_tables.json``. The three known arXiv
column/label inconsistencies are explicitly recorded; they are not assigned to
the unseen journal edition. The exact named source editions and old marking
search are bound in ``source_bindings.json``; no primary PDF or source raster is
exported.

What is proved and retained
---------------------------

A subgroup avoids a forbidden set in every conjugate exactly when it avoids the
ambient element classes meeting that set. This elementary reduction, the facet
orbit count, and the maximality argument are proved completely. The required
finite computation starts with every subgroup conjugacy class of the actual
marked group: 1,262 classes, 137 survivors, 349 containment edges, 26 maximal
classes, and the eight literal deleted labels. It recovers 66 section-regular,
65 original-local-type and 71 mixed quotients. All 137 normalizer quotient
columns are reconciled. The saved group generators determine actual embedded
subgroups; abbreviated structure strings need not determine a semidirect action.

The marked universal-group theorem, exact semisparse criterion and quotient/local
section correspondence are retained from the related complete arXiv original.
Its erroneous census is not a premise. GAP's exact subgroup and element-class
algorithms, its structure descriptions and TomLib's named J1 model remain
computational premises; they are not Lean-certified. The old unavailable g.txt
file is never read. The complete reused marking-search code is present, so no
old umbrella manuscript is an undeclared logical input. There are no Lean claims.

Reproduction
------------

Use Python with NetworkX 3.6.1 and pypdf, GAP 4.15.1 with TomLib 1.2.11, and,
for rendering, XeLaTeX with STIXGeneral, STIX Two Math and Menlo. The exact named
model data and selected standard algorithm files are pinned in
``computational_inputs.json``. This is an explicit computational trust boundary,
not a hash claim about the entire transitive GAP installation.

From any working directory::

    python3 -B -O /path/to/packet/check.py --out /fresh/output \
      --gap /path/to/gap --render --xelatex /path/to/xelatex

Optionally add ``--study-root /path/to/research/leemans`` to verify the original
private source and reused-code bindings. Primary files are not needed to execute
the census. The output path must not exist. A full replay normally takes several
minutes. It reconstructs the marked group, verifies every presentation relator,
enumerates all subgroup classes, filters all element classes, reconstructs the
entire containment graph and local counts, reconciles the historical tables,
checks every printed result row, and replays all eight literal witnesses. Ten
census/table corruptions and sixteen altered actual witnesses must be rejected.
All explicit assertions remain active under Python -O.

The three GAP files and ``accounting.py`` are the complete required program
boundary; ``source_tables.json`` is full required historical data. ``check.py``
is the separately supplied full orchestration/control/render driver. The program
PDF includes all four code files, with a full-file extraction check. The output
``computed_subgroups.g`` contains all 1,262 concrete representatives; the eight
witness files specify actual permutations. These output files are bound under
``evidence/`` but are never used as the input to the exhaustive computation.
No workspaces, cached group objects, primary documents or build products are
exported.

Scope and review
----------------

``source_ledger.json`` records eighteen distinct mathematical/context/edition
clauses, including the eight deletions individually. ``proof_map.json`` binds six
written contexts and the required programs. ``scope.json`` states all retained
inputs and exact formal limits. ``visual_review.json`` distinguishes complete
primary text reading, source-table visual checks and all thirteen own pages.
The manifest binds the exact author edition; later corrections require an
additive successor. Author replay is not independent mathematical acceptance.
