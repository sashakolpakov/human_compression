# Rank-three factorization: formal scope

The theorem `RankThreeFactorization.common_point_of_factorization` is a
group-theoretic Helly statement. Let A,B,C be subgroups of any group, with
every element of A expressible as a product of an element of A∩B and an
element of A∩C. Then every B-coset and C-coset meeting a given A-coset
have a common point in that A-coset. The theorem assumes neither finiteness
nor an additional incidence between the B- and C-cosets.

For three marked types this supplies the common point in each flag. Partial
flags of one or two types extend directly by a point in their coset
intersection. Hence the ordinary rank-three coset system is flag-transitive.
The Lean theorem proves the common-point implication; the interpretation as
a geometry and its flag action is stated here in writing.

The [successful fresh report](RankThreeFactorization.check.json) uses pinned
Lean/mathlib dependencies and prints only `propext` in the theorem's axiom
list. It has no `sorryAx`. The explicit Suzuki matrices, their finite-field
membership, intersection orders, factorization hypothesis and primitivity
are supplied by separate computations and written group theory. They are
not formalized by this module.
