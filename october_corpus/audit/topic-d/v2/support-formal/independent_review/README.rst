Independent review of the global support formula
================================================

Both actual Lean modules and their complete checker/control sources were read.
The strongest exported types were inspected from freshly compiled objects.
A new isolated replay passes all 28 declaration reports, seven rejected proof
mutations and ten finite validations. Only standard Lean axioms occur.

The accepted scope is the actual global orbit decomposition, the full generic
UD.AdmissibleExtensions formula and UD.ExactSupportOrbits. The proof constructs
the stabilizer actions, exact-support restrictions and quotient equivalences.
It does not assume the counting conclusion or an abstract equivalent formula.
Classical incidence inversion and Burnside are imported from pinned mathlib;
their relevant source declarations were also inspected and remain attributed.

The invariant admissible subset R is represented by the acted-on type X.
Concrete generation, least-field support, admissibility and geometry hypotheses
remain the responsibility of the applications. Divisor-poset/number-theoretic
Mobius identification, source classifications and finite censuses are not
formalized by this supplement. No source or solved-question credit is added.

Reproduce the fresh compilation using the immutable author packet::

  python3 -B -O PACKET/check.py --out FRESH_DIRECTORY \
    --lean PATH_TO_LEAN --packages PATH_TO_PINNED_PACKAGES

Then compile ReviewTypes.lean against that fresh lib and dependency_lib overlay
to inspect the six principal exported signatures. actual_types.txt is the
recorded output. The source and package requirements are those of PACKET's
scope.json and dependency_manifest.json. Fresh local sources and absent pinned
dependencies are compiled; existing dependency objects remain trusted.

review.json distinguishes this proof/type review from finite controls and
records every boundary. Neither the first supplement nor the written
manuscripts were changed. This is an independent review of the author work;
it is not a second implementation of the Lean kernel or a rebuild of mathlib.
