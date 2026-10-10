# The higher-rank Steiner classification as one application

The following is the complete principal classification in L092 Theorem11, deduced from the shared residue and fiber results. The two auxiliary printed statements corrected in phases182–183 are not used. In particular, the subline family is selected by flag transitivity after residual connectivity has been analyzed correctly.

**Theorem C.Classification.** Let S=S(t,k,v) be a finite Steiner system with 3≤t<k, and let G=Aut(S). Then Γ(S) is a firm residually connected geometry on which G is flag-transitive if and only if S is one of the following:

1. the points and affine planes of AG(3,2);
2. the projective GF(4)-subline design on PG(1,16);
3. one of the three large Witt designs S(3,6,22), S(4,7,23), S(5,8,24).

Each resulting geometry also satisfies (IP)₂. In the first case the full design group is AGL(3,2); in the second it is PΓL(2,16). In the last three cases the full design groups contain the indicated native Mathieu groups, and their orders are887,040,10,200,960,244,823,040 respectively.

**Proof.** Suppose first that Γ(S) is firm and G is flag-transitive. The firmness criterion gives k−t+1≥2 and r=(v−t+1)/(k−t+1)≥3. The equivariant chamber bijection C.Fiber makes G t-transitive on the points of S. Kantor's Theorem3, retained with its precise primary-source hypotheses, therefore leaves the binary affine plane family, the projective subline family, and the five Mathieu designs.

For the binary affine plane family S_d, the one-point derivative is PG(d−1,2). The residue theorem makes Γ(S_d) residually connected exactly when its rank-three derived construction is connected. B.ProjectivePlane includes the positive case PG(2,2), while B.SpaceObstruction excludes every projective dimension at least three. Thus d=3. The case d=2 does not satisfy the already necessary condition r≥3. Conversely the explicit affine action in the fiber manuscript is chamber-transitive, and the same residue argument proves residual connectivity when d=3. Preservation of the fourth point of each affine plane proves Aut(S_d)=AGL(d,2), as shown there.

In the projective subline case the parameters are S(3,q+1,qᵉ+1), with e≥2 and q≥3. The derivative at a point is AG(e,q). B.AffinePlane and B.SpaceObstruction, together with the residue theorem, imply residual connectivity exactly when e=2. For this remaining case the independently reviewed phase183 argument proves Aut(S)=PΓL(2,q²). If q=pᶠ, the chamber count is |PGL(2,q²)|q whereas the full group order is |PGL(2,q²)|·2f. Flag transitivity therefore requires q to divide2f.

This divisibility leaves only q=4 in the range q≥3. If f=1, it is impossible. If f≥3, then q≥2ᶠ>2f, also impossible. If f=2, q=p² divides4 only when p=2. At q=4 the phase183 normalization proves transitivity explicitly: the relevant Frobenius action cycles through the four nontrivial direction classes and the scalar action covers the three eligible points in each class. This supplies sufficiency as well as necessity. Firmness and (IP)₂ follow from the uniform Steiner theorems.

For the two small Witt designs the chamber counts from C.Fiber are23,760 and285,120. The literal finite models and full automorphism computations give orders7,920 and95,040. A transitive group cannot have an orbit larger than itself, so neither design gives a flag-transitive construction.

For each large Witt design r=5. The explicit finite maps identify every (t−2)-fold derivative with PG(2,4): one derivative is verified against coordinates, and native t-transitivity transports it to every other derivative. B.ProjectivePlane and the residue theorem give residual connectivity. The parameters give firmness, and C.Intersections gives (IP)₂. The already retained Mathieu fiber computation verifies transitivity of a native subgroup on every stage of the chamber fiber; consequently the full automorphism group is also transitive. This proves sufficiency and completes the classification. ∎

The source's theorem already states this final list. The contribution here is a deduction that separates the common structural proofs, retained classification inputs, and exact finite fibers, and that continues to prove the correct final list after correcting the source's intermediate residual-connectivity assertions. It is not a new classification theorem.

The principal classification is now paid as a written proof with finite computational inputs. Its admission still requires independent review of the new manuscripts and replay of the exact packet. The Lean certificate verifies the three explicit finite coordinate-incidence maps; it does not formalize this classification proof, Kantor's theorem, the all-rank residue theorem, or the completeness of the finite automorphism computations. The historical names of the two earlier rank-five residues remain an additional full-source obligation.
