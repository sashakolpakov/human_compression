# Independent internal review: Suzuki realization decisions

Date: 2026-10-10. Reviewer: recent_conjectures, independently of the deriving
agent survey_audit. This is an internal mathematical review, not external peer
review or a determination of priority.

## Materials and result

Read the complete companion notes `phase5_suzuki_realization.md` and
`phase5_suzuki_higher.md`, including the revised characteristic-subgroup
argument in the latter. Compared them against the primary full texts:

* L114, *The rank 3 geometries of the simple Suzuki groups Sz(q)*,
  §§2–3, Theorem 5.3, the case analysis before Theorem 5.5, its ten displayed
  shapes, and the final paragraph on printed p.61.
* L110, *The residually weakly primitive pre-geometries of the Suzuki simple
  groups*, the extension notation and maximal-subgroup table on pp.5–6,
  and the R1–R13 restatement on pp.7–9.
* Bray–Bäärnhielm, *A new method for recognising Suzuki groups*,
  equations (1)–(5), for the matrix convention and Bruhat decomposition.

No mathematical gap was found in the reviewed arguments. The exact conclusion
is realization of every Theorem 5.3 embedded subgroup lattice and the following
decisions for Theorem 5.5: shapes 1,2,3,5,9 are impossible as the specified
embedded RWPRI lattices; shapes 4,6,7,8,10 admit the supplied realizations.
The published candidate-list completeness and Theorem 5.4 nonexistence are
retained inputs, not independently rederived here.

## Checks of the difficult steps

The split-dihedral normalizer is self-normalizing, and internal conjugacy of
such dihedrals makes a prescribed subfield group containing it unique. Thus
the simultaneous-coordinate argument excludes every possible embedding of
the first three composite-degree shapes, rather than just a chosen standard
embedding. Restricting the Suzuki automorphism to an odd-degree subfield has
the correct exponent. The intersection at degree gcd one is Sz(2) of order
20. The involution-centralizer argument for shape 5 forces the common commuting
involutions into the intersection field, excluding its required Klein four.

For Theorem 5.3, the trace argument exhausts the odd-element classes. The two
equal-prime cases, including prime 5, are handled by the supplied involution
conjugation; the source permits one parameter to equal 2 but keeps the other
odd. The construction covers that boundary. The affine-complement
irreducibility used for shapes 4 and 6 holds even when the chosen prime
divisor also divides the smaller field's multiplicative-group order.

For shape 9/R12, the first elementary abelian factor really has order q in
the source notation. The normal Sylow-2 subgroup P contains the full center
of an ambient Sylow-2 subgroup. That center is exactly the identity and all
involutions of P, hence is characteristic in P and normal in G1. The shared
simple subfield fixes the standard positions of both larger subfield groups;
the shared Borel fixes the point-stabilizer position. Consequently containment
and orders force G1=Z_q U_t H_t. Adding one F_t-line to either proper central
field subspace gives a strictly intermediate subgroup. Both required
intersections fail maximality in G1, violating RWPRI for J={1}.

For shapes 7 and 8, the field intersection and unique ambient torus give the
precise gcd of the rotation-group orders. This remains valid when a selected
prime divides the smaller torus order: its valuation increases on only one
side. The common torus normalizer is maximal in the common subfield group,
the cyclic extensions have prime index, and all relevant subfield inclusions
have prime relative degree. These facts verify RWPRI at every subset, not
merely at the ambient group. Shape 10 follows from the same prime-degree
inclusions; the source's exponent restriction ensures its smallest Suzuki
group is simple, rather than Sz(2).

## Dependency and scope boundary

Besides the four explicitly enumerated classical facts in the companion
note, the proofs use maximality of the split and nonsplit torus normalizers,
maximality of prime-degree subfield groups, and the standard odd-element
torus/conjugacy description. These are retained Suzuki structure facts, also
used in the source's classification. They should remain explicit dependencies.

The decisions do not classify flag transitivity, all relative positions of
the realizable triples, or isomorphism classes of the resulting geometries.
In particular the shape 9 obstruction is to RWPRI for the exact displayed
lattice, not to existence of its abstract groups or their bare embedding.

## Executable check actually repeated

Inspected `phase5_suzuki_higher_check.py` and reran an unchanged copy in a
temporary directory. It passed, with certified irreducible degree-45 field,
the common degree-3 subfield, and intermediate center dimensions
9 < 12 < 45 and 15 < 18 < 45 over F2. The direct matrix normalizations and
commutations and the four integer torus-parameter checks passed. The original
script and historical JSON were not modified by the run. This finite example
supports the implementation; the uniform conclusions rest on the paper proofs.

Checked script SHA256:
`02a8d329f21e97856685ef1a34bc4a41e656977f106bb976d671a867a206a785`.
