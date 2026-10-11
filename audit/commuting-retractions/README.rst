Compatible pairs of commuting retractions
========================================

The Lean file constructs the subgroup of pairs ``(x,y)`` fixed by two
commuting idempotent endomorphisms ``e`` and ``f``, with ``f(x)=e(y)``.
The actual homomorphism ``g |-> (e(g),f(g))`` is surjective: a compatible
pair has the explicit preimage ``x * e(y)^(-1) * y``. Its kernel is exactly
the intersection of the two kernels. When that intersection is trivial,
the same formula is the inverse of the constructed group isomorphism.
No finiteness, commutativity or generation hypothesis on the group is used.

The common paper uses this argument for Boolean deletion maps in UA.Mix.
It removes that proof's appeal to generation of a compatible product.
Each application must still establish the actual deletion maps and their
trivial common kernel. The separate semidirect-product description remains
needed elsewhere in the volume.

The independent reviewer read the written and formal statements and
compiled the exact source afresh with Lean 4.32.2 and the pinned mathlib
revision. The eleven printed declarations use only the recorded standard
axioms. External cached library objects remain trusted. The preserved
author and independent manifests describe those original checks; the
admission record binds the unchanged canonical source and current build.

This is a generic formal proof, not a formalization of the full six-paper
source contracts, their concrete presentations or their geometry. It adds
no source recovery, solved conjecture, historical priority or length factor.
The earlier 99 modules and their reports retain their bytes. Only this
module and one entry in the default build are added.

The repository's ``scripts/check_lean.py`` can rebuild the full library
from an explicit pinned package cache; ``lake build`` includes this module.
The published evidence combines the prior 96-module run with four separately
checked additions. It is not a claim of one new 100-module compilation.
