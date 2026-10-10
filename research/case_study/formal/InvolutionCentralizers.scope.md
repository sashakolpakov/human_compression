# Scope of the involution-centralizer rank certificate

10 October 2026. Fresh Lean compilation **PASS**, exit code zero.
Source SHA256: cd7c62c97fd09f9c14f4cf6bcb9c5ab972cd40e1fa6a30585fabd580b8e47072.
Private successful report SHA256: 7f51f13f7f53ea76b5d325d0347bdb01cf4ae1ecee28025d3bcd3f0f4ce01f7a.

The source proves two versions of one abstract theorem. In any group
with trivial center, suppose that whenever nonidentity involutions b,c
both commute with a nonidentity involution a, they commute with each
other. A sequence of nonidentity involutions indexed by Fin n, satisfying
string commutations and generating the group, then has n<=3.

The first version expresses trivial center as: an element commuting
with every group element is one. The second uses Subgroup.center G=bot.
Generation is expressed as Subgroup.closure (Set.range rho)=top, not as
a hypothesis that already asserts the desired rank bound.

If n>=4, rho3 commutes with rho0 and rho1 by the string relations.
For every index j>=2, both rho3 and rhoj commute with rho0, so the
centralizer hypothesis makes them commute. Closure induction extends
this commutation from all generators to every group element. Thus rho3
is central, contradicting its nonidentity.

The certificate does not require that the group is finite, that the
generators are distinct, or that the intersection property holds. These
extra hypotheses are unnecessary for this obstruction. It also does not
assume commutativity of the entire involution centralizer, only of its
nonidentity involutions.

To apply it to Suzuki groups, the structural group-theoretic inputs
remain written: trivial center and the fact that involutions commuting
with a fixed nonidentity involution commute with each other. The Lean
file does not define Suzuki groups, prove their centralizer structure,
or establish rank-three existence. Consequently it formalizes the
general rank obstruction, not an entire Suzuki classification.

Both theorem reports list only propext, Classical.choice and Quot.sound.
No sorryAx or additional axiom appears. The compile used the pinned
private dependency checkout through verify_lean.py; the public portable
runner may independently compile the same frozen source. No existing
runner, dependency source, public file or historical certificate was
edited.
