The isolated order-768 example
=============================

Root-authored verification, awaiting distinct review. The source is L003,
the retained 2018 edition, physical pages 18--19. Read order768.pdf for
the complete two-page argument and the literal four permutation generators.

The exact universal presentation has order 768. Its 128-element facet
group is the square torus with period (4,0); its 48-element vertex group
is the Petrie quotient {4,6}_3. Every one of the 256 subgroup-intersection
equalities is checked. The vertex figure has counts (4,12,6), Euler
characteristic -2, and an odd closed walk in its flag graph, hence is
nonorientable of genus four. The finite permutation image alone is not
used as an upper bound on the universal presentation.

Reproduction::

  python -B -O check.py --out FRESH --render

Required mathematics consists of the whole verify.g program and the
ordinary string C-group recognition theorem and affine square reflection
description used in the manuscript. GAP exact finite presentation and
permutation-group algorithms are trusted. check.py is a replay/build
driver. No earlier census or table calculation is repeated. This is not
a new Lean proof. Any manuscript comparison excludes software on both
sides and charges the complete written note in its assigned application.

The original group-order and genus claims belong to the source authors.
This packet supplies their verification; it adds no conjecture answer,
historical priority claim or whole-original admission. An initial local
run stopped at GAP's reserved name E after the group calculations; the
variable was renamed Ctwo before the successful runs and this freeze.
That failed run is not mathematical evidence.
