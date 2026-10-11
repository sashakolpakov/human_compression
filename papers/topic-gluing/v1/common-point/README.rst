Gluing permutation markings through a common point
=================================================

This is a bounded author packet for a complete general theorem and its tree
iteration. It is not a complete recovery of L010 or a classification at fixed
degree minus rank. Independent mathematical acceptance is pending. No source,
question or numerical-compression credit is attached to it.

Start with common_point_gluing.pdf, then scope.json and source_map.json.
The written argument proves all subset intersections and retains the actual
supported symmetric-group hypothesis. Pure leaf transpositions discharge it
in the literal first construction of L010. The tree corollary also specifies
all attachment points, the preserved hypotheses and the exact degree/rank
formula. The source's impure-label example is explicitly attributed.

RootOrbitIntersection.lean verifies six genuine permutation-subgroup lemmas;
its scope does not include the complete gluing theorem. The complete GAP file
is diagnostic only: twelve paired gluings, two iterated examples and four
countermodels to weakened assumptions. All source-specific conclusions in the
bounded contract have written proofs; no finite census is a premise.

Replay in a fresh output directory::

  python -B -O check.py --study-root /path/to/research/leemans \
    --out /fresh/path --render

Optional --lean, --packages, --gap and --xelatex select the pinned local tools.
The source PDF is an external prerequisite under sources/gluing2026.pdf.
The runner checks its exact edition; the copyrighted primary is not exported.
Mathlib source revisions and standard Lean axioms are checked, while the pinned
cached library objects are trusted as in the existing formal protocol.

The new proposed common formulation uses standard permutation facts proved in
full here. Historical priority is not claimed. L010 Section 4 and the structural
converse needed for a finite-core classification remain separate obligations.
The frozen unified B edition is unchanged.
