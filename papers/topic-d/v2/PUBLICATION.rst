Stabilizers, support and geometry enumeration
============================================

This edition contains a complete common paper and three applications. The
`independent review <../../../audit/topic-d/v2/independent_review/review.json>`_
accepts all 37 source rows with their retained inputs, corrections and
exclusions. The `admission <../../../audit/topic-d/v2/admission.json>`_ binds
the exact edition and review. The frozen author files retain their earlier
pending-review labels; this publication record supersedes those labels.

Read the `common theory <umbrella.pdf>`_ (6 pages), followed by:

* `Commuting involutions and six-point polyhedra
  <commuting-involutions.pdf>`_ (5 pages): Kiefer and Leemans, 2013;
  all-degree pair counts and the exceptional degree-six classification.
* `Suzuki polyhedra in field coordinates <suzuki-polyhedra.pdf>`_ (6 pages):
  Kiefer and Leemans, 2010, in the bound twelve-page author edition dated
  27 September 2011; both uniform counting formulas, generation,
  intersection, rank and duality.
* `The Hall–Janko census <hall-janko-geometries.pdf>`_ (2 pages): Leemans,
  2002; eight rank-two, nineteen rank-three and three rank-four geometries,
  with no higher ranks, under the stated complete subgroup catalogue.

The common theorem combines the stabilizer action on an extension fiber
with a condition on its support. Möbius inversion isolates exact support;
fixed-point counting then counts its orbits. The support sublevel sets
need not themselves be invariant. A further common lemma about odd-order
actions supplies both Suzuki freeness arguments. The local subfield,
generation and geometry hypotheses are proved in the applications or
retained explicitly. The common paper also contains the full coset
recognition and exhaustive augmentation proofs for a possibly nontrivial
chamber stabilizer.

Orbit–stabilizer, Burnside counting, Möbius inversion and the action
classification are classical. The earlier project proof bank supplies
reviewed extension, recognition and augmentation arguments. The source
results retain their authors' attribution; this edition claims no new
historical classification or solved conjecture. Its exact scope is in
`scope.json <scope.json>`_. In particular, L104's printed diagrams, full
automorphism and correlation groups, and doubling relation are excluded
from the recovered principal census contract. No M22 result is included.

Complete computations
---------------------

The `twelve-page appendix <program-appendix.pdf>`_ prints all eight
mathematical programs. Five are required computations: the exceptional
degree-six census and four Hall–Janko programs. Three complete formula,
field and matrix diagnostics are conservatively retained. Two complete
execution drivers are inventoried separately. No program has been pruned.

Independent execution exhausted all 146 Hall–Janko subgroup anchors and
4,072 augmentation candidates, and checked all thirty final geometries.
The subgroup catalogue and exact GAP algorithms remain retained inputs.
A separate semantic comparison verified equality of all 170 resulting
panel and parabolic subgroups, even when GAP printed different generating
lists. Small field computations are diagnostics for the Suzuki formulas;
their all-parameter proofs are written in the application.

Lean coverage and replay
------------------------

The two Lean files have ten freshly checked declarations. Eight prove
the actual orbit correspondence in a selected stabilizer fiber and the
odd-period action argument; two reused declarations prove an abstract
rank obstruction under explicit centralizer hypotheses. Only standard
Lean axioms occur. Read `formal/scope.json <formal/scope.json>`_ for the
exact correspondence and remaining written obligations.

This edition does not claim that Lean verifies the complete source results,
support-count formula, geometric recognition, classical Suzuki structure,
subgroup catalogue or GAP programs. The later support-count formalization
is a separate supplement awaiting independent review. It is not included
in these ten declarations or this admission.

From the repository root, with Python and pypdf 6.13.0::

  python3 -B -O papers/topic-d/v2/check.py --out FRESH_DIRECTORY

This verifies the frozen proofs, source-row map, complete code inclusion
and seven integrity controls. To repeat the complete computations, formal
checks and five PDF renders, add::

  --programs --formal --render --gap PATH_TO_GAP --xelatex PATH_TO_XELATEX \
  --lean PATH_TO_LEAN --packages PATH_TO_PINNED_PACKAGES

Use GAP 4.15.1 with TomLib 1.2.11 and Lean 4.32.2 with the package revisions
in `formal/dependency_manifest.json <formal/dependency_manifest.json>`_.
The formal runner builds the local sources and missing dependency objects
privately; it trusts the remaining pinned package caches. It does not
rebuild all of mathlib. The standard catalogue builder can render the four
scientific papers; the command above also renders the complete code appendix.

Primary PDFs and the previous proof-bank files are not redistributed.
Supplying ``--study-root PATH`` additionally checks their exact bytes.
Without it, the program reports those external byte checks as unperformed;
the retained mathematical inputs remain necessary.

Measurement follows separately. Each combined written comparison must
charge this whole common paper once and all three complete applications.
The complete program cost is a separate comparison; individual application
factors require the common theory and required programs to be acquired.
No numerical compression factor is assigned by this proof admission.
