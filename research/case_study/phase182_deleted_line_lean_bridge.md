# Literal q=4 residue: source bridge and Lean scope

The file formal/DeletedLineFourResidue.lean verifies the actual 18-vertex
rank-two residue of L092 Construction3 at an original line of
S4 = Γ(AG(2,4))L. It uses the literal equation x = a(y+t), then proves that
the resulting finite graph is the disjoint union of three hexagons.

## Identification with the source objects

Choose coordinates so the first deleted affine line is L:y=0. In S4 the
points are (x,y) with y≠0, and the lines are x=ay+b, with their intersections
with L removed. This is the incidence description on the source's p.568,
derived directly from Construction3 on p.565.

Fix the original line M:x=0 of S4. The residue Γ(S4)M has two types:

* Its point objects are the S4-points nonincident to M. These are precisely
  (x,y) with x,y∈F4*.
* Its other objects are S4-flags ((0,t),N) with N∩M={(0,t)}.
  Here t≠0, and N is uniquely x=a(y+t) for a∈F4*. Conversely every such
  (a,t) gives one flag of this residue.

The first correspondence has 3² objects, as does the second. A point
(x,y) of the first type is different from (0,t), because x≠0.
Construction3 therefore makes the point incident to the displayed flag
exactly when it lies on N, namely x=a(y+t). No further incidence condition
has been dropped.

## The formal arithmetic

F4 is represented by pairs over ZMod2. The pair (r,s) denotes r+sω,
where ω²=ω+1. Addition is componentwise, and the file defines multiplication
by the resulting coefficient formula. The theorem field_table_laws checks
commutativity, associativity, distributivity, the nonzero unit, and the
inverse x² of every nonzero x. The additive group is the existing product
of the two ZMod2 additive groups. The theorem omega_polynomial checks the
displayed quadratic relation.

Exponent coordinates are ZMod3. The map nonzero lists 1,ω,ω², and the file
proves that it is injective and exhausts exactly the nonzero field elements.
It also proves multiplication corresponds to addition of exponents.
Consequently both residue-object identifications above are bijective with
the formal two copies of ZMod3×ZMod3.

Crucially, the formal incidence definition uses the field multiplication
and addition formula, not the claimed component invariant. The theorem
incidence_formula derives

    incident (X,Y) (A,T) ↔ X+Y=A−T and Y≠T.

It follows that every edge preserves the value X+Y on point objects and
A−T on flag objects. Induction on reflexive-transitive reachability proves
that every finite path preserves this value. Two displayed vertices have
different values, giving not_connected.

The file goes further: threeHexagons is an explicit equivalence from
ZMod3×Fin6 to the 18 vertices. In each component its cyclic order is

    L0, R1, L2, R0, L1, R2,

where Lj=(k−j,j) and Rh=(k+h,h). The theorem three_hexagons_adjacency
proves that adjacency is exactly equality of the first coordinate and
consecutive cyclic positions modulo six. Thus the three-hexagon
description itself, not only the failure of connectedness, is verified.

## Scope and trust

The formal connectivity predicate is the usual reflexive-transitive closure
of the symmetric, irreflexive adjacency relation, followed by universal
reachability. It does not import Mathlib's SimpleGraph wrapper; the file
proves symmetry and irreflexivity directly.

Seven printed axiom reports use only propext, Classical.choice and
Quot.sound. The finite arithmetic checks use ordinary kernel-checked
decide. No sorry, custom axiom or native_decide occurs.

The source-to-object isomorphism in the first section is a written proof
from the original definitions. The formal file proves its resulting exact
finite arithmetic graph, its full three-cycle decomposition, and its
disconnection. It does not formalize the entire source's rank-three
construction, the all-q automorphism theorem, the positive q=8 case, or the
uniform corrected theorem. Those scopes remain separate.
