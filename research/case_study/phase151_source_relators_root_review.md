# Source relations: independent proof review and admission

Reviewed on 2026-10-10. Root read the complete two Lean sources, their
author scope, the dedicated compilation and control programs, and both
written consumers: the characteristic-two bridge and universal label-four
adapter. This is an independent review of this author's formal package,
not an external peer review or a new reading of the entire source corpus.
The frozen author manifest has SHA-256
`f80ddf889abe6381686d7f10f349658b26269eb9d4832d9eadf5dd51b9bb6575`.

## The actual quadratic theorem

Let Q be a quadratic form over any field of characteristic two and let B
be its polar form. For unit vectors e,f,h satisfying B(e,h)=0 and
B(e,f)=B(f,h), put sigma_u(x)=x+B(x,u)u. The final theorem proves

    ((sigma_f sigma_h)^k (sigma_e sigma_f)^k)^2 = 1

as an equality of linear equivalences of the entire ambient vector space,
for every integer k. There is no dimension or nondegeneracy assumption.
This exactly covers the local extra relation in the written bridge; it is
stronger than checking equality on the span of the three vectors.

The implementation uses Mathlib's actual quadratic forms and their polar
forms. It proves the composition law for the explicit maps

    T_u(x) = x + B(x,z)u + (B(x,u) + Q(u)B(x,z))z

for parameters perpendicular to z, their involutivity, their linear
equivalences, subgroup closure and covariance under isometries fixing z.
It does not assume that the parameterization is injective. The abstract
integer-power lemma separately handles nonnegative and negative powers;
the required normalization by both an element and its inverse is explicit.
In the final application z=e+h, the unit and polar assumptions derive
the singular/perpendicular relations, the product of endpoint symmetries
is the required translation, and normalization and exponent two are
proved. Neither the desired word relation nor normalization is an
unproved premise of the final theorem.

The general translation composition law does not require z to be singular;
the final application proves singularity. Degeneracy of the restricted
three-dimensional form therefore causes no hidden extension step.

## The label-four equivalence

In an arbitrary group, let a,b,c square to one and let a commute with c.
With [x,y]=xyx^-1y^-1, the proof establishes both directions between the
two adjacent fourth-power relations together with the source's three
power relators, and the corresponding adjacent nested commutators and
cross commutator. It derives [a,b]=(ab)^2; the adjacent nested relations
are equivalent to the fourth-power relation, the cross relation is the
second-power relation, and the first- and third-power relations are
redundant. Identity markers are permitted, and no exact order is inferred.

These are equalities and equivalences inside an arbitrary group. The Lean
module does not construct presented groups, identify their normal
closures, or prove a universal presentation isomorphism. The written
unitriangular identification still uses the attributed Biss–Dasgupta
presentation theorem. Its order and intersection arguments are not
silently included in this local formal equivalence.

## Fresh executions and trust

Root freshly executed the frozen dedicated runner with pinned Lean 4.32.2
and the pinned, tracked-clean package checkouts. Both local sources and
the two missing Mathlib modules were rebuilt successfully. The
[root build report](phase151_source_relators_root_build.json) records all
28 printed declaration audits. Root also freshly ran all seven
[input-preservation and rejection controls](phase151_source_relators_root_controls.json).
These controls check the runner, not the mathematical theorem.

The exported sources were compiled again with the public generic runner
in separate fresh output directories. The eight label-four audits use
only `propext`; the twenty quadratic audits use subsets of `propext` and
`Quot.sound`. There are no placeholders, added axioms or native-evaluation
claims. The two rebuilt Mathlib sources are pinned and recorded in the
public dependency reports. The installed compiler and other cached
compiled package objects remain trusted; this is not a rebuild of the
whole dependency chain.

The admitted sources are:

- `LabelFourRelations.lean`, SHA-256
  `6cda4bb1f0bf2f6efb6e7935db0487961ade5bdd6d5d210a8e84aa63f556e5ab`.
- `CharacteristicTwoTranslations.lean`, SHA-256
  `430dc7d20ba40b5f0013b129551d136cf9d97088b91b5ddf0bb5652f510ac1cd`.

Admission covers the two actual formal statements and their correspondence
to the named written arguments. Finite-field parameter selection, the
retained Brooksbank–Ferrara–Leemans generation/intersection theorem,
polytope correspondence, and the retained unitriangular presentation
theorem remain outside these certificates. This adds no full-conjecture
solution, historical-priority assertion, source coverage or measured
compression factor. Earlier frozen pending-review labels remain unchanged;
this review records their subsequent admission.
