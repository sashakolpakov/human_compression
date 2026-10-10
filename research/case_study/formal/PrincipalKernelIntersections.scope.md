# Principal-kernel intersection certificate

This new module kernel-checks the quotient-to-actual-IP step used in
phase17_k1_classification.md. It imports the pinned mathlib environment
already used by the existing certificates; no prior module is changed.

`intersection_eq_of_image_and_kernel` proves a general subgroup lemma.
If C lies in A and B, every common image under a homomorphism lifts
from C, and the common kernel contributes no elements outside C, then
A intersect B equals C. The proof uses an explicit quotient-kernel
correction x*y^(-1), rather than a finite order argument.

`intersection_property_of_principal_kernel` specializes this to a
monotone family P(S) indexed by arbitrary vertex subsets. Its explicit
assumptions are: exact intersections of the subgroup images; every
kernel element is 1 or a fixed z; and z belongs to P(S) precisely
when a fixed support J is contained in S. It concludes the full
intersection property P(S) intersect P(T)=P(S intersect T). Neither
finiteness nor centrality is needed for this transport lemma.

The actual central extension, isolated seed-kernel words, parabolic
kernel membership formula, canonical-quotient input, necessity of the
least active support, and all-rank 5d−10 count remain written proofs.
This is not an end-to-end formalization of that classification.

The supplied check report records successful Lean 4.32.2 compilation.
Both theorems use only Lean's standard `propext` and `Quot.sound`
axioms. There is no `sorry`, `sorryAx`, or new axiom declaration.

Reproduce with the existing portable public runner, supplying the
same pinned built package directory:

    python3 verify_lean.py --packages /path/to/pinned/.lake/packages PrincipalKernelIntersections.lean

The private development runner has machine-local defaults; those
defaults are not a new dependency or exported source of this module.
