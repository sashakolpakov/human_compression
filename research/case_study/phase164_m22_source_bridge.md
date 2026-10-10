# Additive source-to-coset bridge for the M22 checkpoint

This note supplements the frozen `phase164_m22_core_checkpoint01_manifest.json` (SHA256 `4c6b9b3432011119f100694dddc28caf14dbac0afd7e67c02d034ffbb0ada6e1`). It does not modify that checkpoint or resolve its source-table gap. The explicit source-interface obligation was identified in the independent review by `/root/review_unified_seven`.

**Lemma E.CosetRealization.** Let a group $G$ act type-preservingly and flag-transitively on an incidence geometry of finite rank, and let $(x_i)_{i\in I}$ be a base chamber. Write $H_i=\operatorname{Stab}_G(x_i)$ and use a right action. Then
\[
H_i g\longmapsto x_i^g
\]
is a type-preserving $G$-equivariant isomorphism from the subgroup coset system to the given geometry.

**Proof.** Transitivity on one-object flags makes the map onto each type. It is well defined and injective because $x_i^g=x_i^h$ holds exactly when $gh^{-1}\in H_i$, which is equivalent to $H_i g=H_i h$. If two cosets share a representative $k$, their images are $x_i^k,x_j^k$ and are incident, as the base objects are incident. Conversely, if two images are incident, transitivity on flags of their two types supplies a $k$ carrying the base pair to them. The injective object correspondence then writes both cosets with that common representative. The map therefore preserves and reflects incidence. ∎

The right-action coset convention is the same as in E.PrimitiveTriples and in the finite programs. It does not assert that an arbitrary isomorphism of incidence structures must normalize the distinguished acting group.

**Lemma E.DistinctMaximals.** In a residually connected rank-three flag-transitive geometry whose three object stabilizers are maximal proper subgroups of $G$, the stabilizers of a base chamber are pairwise distinct.

**Proof.** Apply E.CosetRealization. If all three stabilizers equal $H$, cosets of different types are incident exactly when their underlying right cosets are equal. The whole incidence graph is a disjoint union of three-vertex complete graphs indexed by $H\backslash G$. Since $H$ is proper there are at least two components, contrary to residual connectedness at the empty flag.

Otherwise suppose $H_1=H_2=H$ and $H_3=K\ne H$. In the residue of the base third-type object $K$, the objects of either remaining type are precisely the cosets $Hk$ with $k\in K$. Two of opposite types are incident exactly when their underlying cosets coincide. The residue is therefore a disjoint union of edges indexed by $(H\cap K)\backslash K$. Distinct maximality implies $K\nsubseteq H$, so the index is at least two. The residue has rank two and is disconnected, again a contradiction. Every equality among two of the three stabilizers falls under one of these cases. ∎

Together these lemmas prove that every source geometry occurs among the distinct maximal-subgroup coset systems enumerated in the checkpoint. E.PrimitiveTriples proves the converse admissibility, and U.ExtensionOrbits proves that the finite traversal exhausts their automorphism/type classes. The numerical conclusions still retain the complete group catalogue and exact algorithms, and the refined source-table comparison remains incomplete.
