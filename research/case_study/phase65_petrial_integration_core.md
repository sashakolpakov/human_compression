**(c) Retained-object operations and the faithful image.** Let G act on sets X and Y. Suppose there is a G-invariant subset Y₀⊆Y and an equivariant surjection p:Y₀→X. Suppose also that Y admits an injective equivariant encoding into a tagged disjoint union of finite products, each factor being X or its power set, with G fixing the tags. In particular, an element fixing X pointwise fixes every encoding. Then

\[
 N:=\ker(G\curvearrowright Y)=\ker(G\curvearrowright X)
   =\bigcap_{x\in X}G_x.
 \tag{Kc1}
\]

If X is the disjoint union of transitive G-sets with selected stabilizers H_j, then

\[
 N=\bigcap_j\operatorname{core}_G(H_j)
   =\operatorname{core}_G\!\left(\bigcap_jH_j\right).
 \tag{Kc2}
\]

The induced faithful group is G/N. If it acts by type-preserving automorphisms of a thin residually connected finite-rank geometry on Y and is chamber-transitive, it is the full type-preserving automorphism group. For a chamber D and a panel F⊂D in that geometry, the stabilizers in G satisfy

\[
 G_D=N,\qquad [G_F:N]=2.
 \tag{Kc3}
\]

Thus G_F of order two forces N=1. No finiteness of G or X is required.

*Proof.* An element fixing Y fixes X by the equivariant surjection. An element fixing X fixes each encoded element/subset and hence each uniquely encoded object of Y. This proves (Kc1). Every stabilizer in a transitive orbit is a conjugate of its selected H_j. Intersecting those conjugates proves both equalities in (Kc2); the intersection is exactly the largest normal subgroup contained in every H_j. The quotient is the faithful permutation image by the first isomorphism theorem. The chamber assertion follows from the free chamber action in Lemma O0 below: any automorphism agrees on a base chamber with an element of the transitive image, so their quotient fixes that chamber and is the identity. The preimage of its chamber stabilizer is N. Chamber transitivity makes G_F transitive on the two chambers containing F, with stabilizer G_D=N. The orbit–stabilizer bijection proves (Kc3), also for infinite G. ∎

The encoding hypothesis uses actual subsets, not independently labelled copies of the same subset. The theorem identifies a permutation image; it does not say that a changed generator list is a homomorphic image of the old marking.

**Lemma O0 (chamber galleries and residue stabilizers).** A residually connected geometry of finite rank has connected chamber graph. If it is thin, its full type-preserving automorphism group acts freely on chambers. In that thin case, if a subgroup G acts chamber-transitively, it therefore acts regularly and equals the full group. For the unique involution r_i carrying a base chamber across its i-panel,

\[
 G=\langle r_i:i\in I\rangle,
 \qquad G_F=\langle r_i:i\notin t(F)\rangle
 \tag{O0}
\]

for every subflag F of the base chamber.

*Proof.* Induct on rank. Rank-one chambers are mutually adjacent. At larger rank, chambers containing an object are gallery-connected by induction in its residue. A path in the connected incidence graph, extending each incident pair to a chamber, then joins any two chambers by such galleries. This also applies inside every residue. In the thin case, an automorphism fixing a chamber fixes its unique neighbour across every panel, hence every chamber and every object. This proves freeness. A transitive subgroup exhausts the full free action. Its unique panel-changing element r_i has square fixing the base chamber, so is a nonidentity involution. Reading an arbitrary gallery as successive panel changes proves generation. Reading a gallery inside the residue of F proves the stabilizer formula, since only types outside F change. ∎
