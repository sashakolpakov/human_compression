Global support counting by stabilizer fibers
===========================================

This additive supplement closes the generic global-decomposition boundary
of the first support-counting packet. The new module constructs an actual
bijection between the ambient orbit quotient and the disjoint union of
stabilizer-fiber orbit quotients. It then proves the complete common
Möbius/Burnside count with the actual global quotient on the left.

The strongest final declaration is
``MathCompression.SupportCounting.order_automorphic_admissible_extension_orbit_count``.
It constructs exact-top invariance from support equivariance, chooses
canonical representatives of all base orbits, and proves the sum of
fixed-point sublevel counts. Base orbits outside the image have empty
fibers. The arbitrary-transversal theorem gives the manuscript's exact
indexing by one representative of each orbit in the admissible base image.

The common hypothesis uses the acted-on type X for the manuscript's
invariant admissibility subset R. No source-specific admissibility,
generation, least-field support, geometric recognition or census is
proved by this supplement. UD.Orbits and the other parts of the full
Topic D manuscript are not claimed as newly formalized here.

Reproduction
------------

Supply Lean 4.32.2 and the exact package revisions/cache recorded in
``dependency_manifest.json``::

  python3 -B -O check.py --out /fresh/output \
    --lean /path/to/lean --packages /path/to/.lake/packages

The two local modules are compiled from the bound source into fresh output.
The first module is a byte-identical copy of the separately frozen first
supplement; its original packet is untouched. Absent pinned package
objects are compiled into an isolated overlay. Remaining package objects
are trusted; no full mathlib rebuild or independent kernel implementation
is claimed. No compiled objects are distributed.

The fresh replay passes 28 declaration reports: the original 12 and 16 new
ones, including equivalences and adapter definitions. All use at most
propext, Classical.choice and Quot.sound. No sorry, axiom declaration or
native_decide is used. Ten finite validations/countermodels and seven
rejected proof mutations are recorded. The three new mutations remove
necessary interface hypotheses; their corresponding finite countermodels
show the mathematical failures of injectivity, surjectivity and counting.
These checks supplement the quantified proofs rather than replace them.

``theorem_map.json`` maps manuscript statements and hypotheses to the
actual declarations. ``scope.json`` records the remaining boundaries.
The construction composes classical orbit transport, Möbius inversion and
Burnside counting. It makes no historical priority, source credit,
conjecture credit or compression-rate claim. Independent review is pending.
