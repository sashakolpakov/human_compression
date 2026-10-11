Topic F: odd kernels and cyclotomic polyhedra
===========================================

This is a private author edition of an already admitted principal-results
contract. It requires independent review before canonical publication. It
does not change the source or question counts and asserts no compression
ratio. The exact source is Hou--Feng--Leemans--Qu,
``arXiv:2407.10388v1`` (15 July 2024), 12 pages; no later edition is
silently substituted.

Complete papers
---------------

``umbrella.tex/pdf`` proves the common subgroup, orbit, character and
cyclotomic arguments. ``odd-kernel-polyhedra.tex/pdf`` gives the complete
application: the structural theorem, both directions of the abelian/tight
classification, every odd-prime nonabelian construction, the exact named
presentation, its automorphisms and auxiliary identities. Their TeX inputs
are the preamble and the eight files under ``sections/``; the two documents
are separate papers, with the entire common paper paid within this topic.
No old combined manuscript is a hidden mathematical premise.

``scope.json`` maps all 25 inherited source/audit records to 16 exact
current TeX spans. It preserves the accepted correction of the literal
Theorem 1.2 marking, the retained tight-classification converse and the
excluded introductory census and general Hughes classification. The old
author/reviewer/admission bindings are historical evidence, not substitutes
for the complete local proofs. ``inventory.json`` is the earlier planning
snapshot; the final scope governs this edition.

Retained input and formal limits
-------------------------------

Cunningham--Pellicer Theorem 1.1(b),(c) is retained only for the odd/even
tightness converse and uniqueness, with the exceptional even parameter
four excluded. Its primary theorem was read in the previous accepted
audit. No local complete PDF, hash or complete-text cost is available,
and none was acquired in this closed-corpus task. The classical
polyhedron/string-C-group correspondence, Sylow and Lagrange theorems,
finite abelian arithmetic, Eisenstein criterion and determinant norm are
explicit retained background. All lattice deductions are proved here.

``formal/OddKernelIntersection.lean`` is byte-identical to the accepted
five-declaration module. Its scope is exactly two subgroup intersection
theorems and three group identities. The all-parameter Sylow, character,
cyclotomic, construction and presentation arguments are written, not Lean
theorems. The standard axioms are reported for each declaration. Cached
pinned dependency objects are trusted, and missing objects may be rebuilt
privately; no full mathlib rebuild is claimed.

Complete validation boundary
----------------------------

The three complete mathematical programs are printed once in
``program-appendix.tex/pdf`` and supplied byte-identically under
``programs/``. They validate seven cyclotomic models, four abelian models
and five independent literal source presentations, checking all 64 subset
intersections for each marking. The uniform written proofs do not depend
on those bounded outputs. Any later validation-cost comparison must retain
all three complete programs, including comments and negative controls;
their raw executable text is an alternative to the printed appendix,
not an additional duplicate charge.

Both complete historical operational checkers are retained under
``drivers/``. The canonical runner stages and executes the first without
modifying it. The second is preserved as historical operational evidence;
it requires the full original phase236/248 layout. Its independent
mathematical GAP program is run directly by the canonical runner.
No file is pruned because it is diagnostic. The two full drivers are a
separate operational boundary.

Portable replay
---------------

Use Python with pypdf, GAP, the pinned Lean 4.32.2 compiler and package
checkout, and XeLaTeX with STIXGeneral, STIX Two Math and Menlo::

    python3 -B -O check.py --out /fresh/output \
      --programs --formal --render \
      --gap /path/to/gap --xelatex /path/to/xelatex \
      --lean /path/to/lean --packages /path/to/pinned/packages

Optional ``--study-root`` and ``--public-root`` verify the external exact
primary and prior-admission bindings. They are unnecessary for a copied
packet's validation, formal and render replay. The original source PDF,
cached full text and page images are not exported.

All outputs must be fresh. The runner verifies local hashes, all 25 rows,
all proof spans, all complete programs and exact code inclusion in the PDF.
Eight integrity mutations must be rejected. ``--programs`` invokes the
historical driver's three semantic controls plus the independent
composite-index counterexample and also compiles the same five Lean
declarations. ``--formal`` independently recompiles those five sources
through the current scoped adapter and checks two omitted-hypothesis
countermodels. These are five distinct declarations, never ten.

The three mathematical program hashes and Lean sources are unchanged
from the accepted recovery. Final render-only replay after typography
corrections is distinguished from the full earlier program/formal replay.
Neither a successful runner nor the page extent replaces independent
mathematical and source review.
