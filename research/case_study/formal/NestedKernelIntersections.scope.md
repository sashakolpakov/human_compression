# Nested-kernel intersection transport certificate

New private phase-nineteen module, 10 October 2026. The frozen
`PrincipalKernelIntersections.lean` is imported and unchanged.

The module certifies the actual-IP adapter used for the noncentral
excess-two constructions. It works with arbitrary groups G,Q, a
homomorphism f:G→Q, and a subgroup family P(S) indexed by arbitrary
sets of markers. It does not assume that the groups are finite, that
the kernel is central or abelian, or that f is surjective onto Q.

## Explicit nested profile

For subgroups L≤K and supports E⊆T, `nestedKernel L K E T S` is

- K when T⊆S;
- L when E⊆S but T is not contained in S;
- the trivial subgroup otherwise.

`mem_nestedKernel` gives an equivalent membership description;
`nestedKernel_mono` proves monotonicity in S; and
`nestedKernel_meet` proves the exact subgroup identity

    nestedKernel(S) ∩ nestedKernel(U) = nestedKernel(S ∩ U).

The main theorem `intersection_property_of_nested_kernel` assumes:

1. P is monotone with respect to inclusion of marker sets.
2. The subgroup images under f have exact intersections:
   f(P(S)) ∩ f(P(U)) = f(P(S∩U)).
3. The **actual** parabolic kernel is the displayed nested profile:
   P(S) ∩ ker(f) = nestedKernel(S) for every S.
4. L≤K and E⊆T.

It concludes P(S)∩P(U)=P(S∩U) for all S,U. It invokes the existing
`intersection_eq_of_image_and_kernel` theorem, lifting a common
image and correcting its difference inside the common kernel.
No implication from image IP alone to actual IP is asserted.

In the elementary-abelian excess-two application, K is γ₃ of order
four, L=⟨z⟩ has order two, T is the unique noncentral triple support,
and E is its possible active edge. If there is no active edge, the
same certificate applies with L trivial and E empty. The cyclic
kernel application is obtained with T=E. These are mathematical
instantiations described here; the module does not construct the
seed groups or establish their kernel profiles from matrices or
presentations.

## Arbitrary chains of supports

`intersection_property_of_chain_kernel` is a separate generalization.
Let `levels i` be arbitrary subgroups and `support i` be marker sets.
Assume that every pair of supports is nested, and that for every
kernel element x,

    x ∈ P(S) iff there exists i with
      x ∈ levels(i) and support(i) ⊆ S.

Together with the same monotonicity and image-IP assumptions, this
implies actual IP. The index type need not be finite. The level
subgroups need not be explicitly assumed nested: membership at the
smaller of two supports already supplies the needed witness. In a
usual finite-chain application they may of course form a subgroup
chain; a trivial level with empty support accounts for the identity.
The membership profile itself remains an explicit hypothesis.

## Verification and boundary

All five printed theorems compiled under **Lean 4.32.2**, using the
existing pinned mathlib packages and the unchanged principal-kernel
module. The new `NestedKernelIntersections.check.json` records the
source hash, command result and exact axiom output. Each theorem
uses only `propext`, `Classical.choice` and `Quot.sound`; none uses
`sorryAx` or any newly declared axiom.

The following remain written mathematics: the forest quotient,
the noncentral affine/dihedral seeds, fiber generation, the effect of
central identifications on parabolic kernels, verification of the
profile for each constructed group, all necessity arguments, marked
uniqueness, and the all-rank excess-two enumeration. This is not an
end-to-end formalization of the classification or of a concrete
noncentral group.

Reproduction with the existing runner and pinned built packages:

    python3 verify_lean.py --packages /path/to/pinned/.lake/packages NestedKernelIntersections.lean

The import `PrincipalKernelIntersections` must be compiled with the
same toolchain and on LEAN_PATH. The private development run used
`/Users/sasha/bogachev/formal/.lake/packages`; this machine-local path
is not part of the mathematical statement. Compiling this new source
writes only its own `.olean` and `.check.json`. Historical source and
check-report bytes were not changed.
