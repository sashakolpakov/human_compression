# Locally injective covers, kernel supports, and finite join-density

Private research manuscript, 10 October 2026. This proves a conditional general join-density theorem and a complete finite cover-interval classification. It does not prove general join-density for monodromy kernels, or solve the general multiple-minimal-cover problem. Earlier phase41 and44 packages are unchanged.

## 1. An exact quotient intersection test

Let H be a group, A,B≤H, C=A∩B, and M normal in H. Write q:H→H/M. Products AB below are products of subsets, not an assertion that AB is a subgroup.

**Lemma1.**

    q(A)∩q(B)=q(C)  iff  M∩AB=(M∩A)(M∩B).

**Proof.** The right-hand product is always contained in M∩AB. Assume the image intersection equality, and write m=ab∈M with a∈A,b∈B. Then q(a)=q(b^−1) belongs to q(C). Choose c∈C with q(c)=q(a). The factors ac^−1∈M∩A and cb∈M∩B have product m, giving the reverse inclusion. Conversely, if q(a)=q(b) for a∈A,b∈B, write ab^−1=m_A m_B with m_A∈M∩A,m_B∈M∩B. Then m_A^−1 a=m_B b∈A∩B=C, and its image equals q(a). This proves the equality. ∎

Now fix a normal subgroup L of H with

    L∩A=L∩B={1},

and define the **defect set** D=L∩AB. For every normal M≤L, Lemma1 becomes

    q(A)∩q(B)=q(C)  iff  M∩D={1}.                 (1)

Thus D controls every intermediate quotient in a single fixed finite cover interval. It need not be normal or a subgroup. This is a quotient form of the shared kernel-intersection mechanism, proved here without importing a source polytopality criterion.

**Size formula.** If the groups in question are finite and π:H→H/L, then

    |D|=[π(A)∩π(B):π(C)].                         (2)

Indeed each x∈π(A)∩π(B) has unique lifts a_x∈A,b_x∈B because π is injective on both ends. The map x↦a_x b_x^−1 takes values in D and is surjective. Its fibers are precisely the left cosets xπ(C): multiplying both lifts on the right by c∈C leaves their product unchanged; conversely equality of the products gives a_y^−1a_x=b_y^−1b_x∈C. This proves (2), without assuming π(C) is normal in the intersection.

## 2. Exact application to regular polytopes

Let H be the marked group of a regular rank-n polytope, n≥3, and let A,B,C be its two end parabolics and common medial subgroup. Suppose π:H→R is a marked epimorphism, with kernel L, that is injective on A and B. All groups may be finite or infinite for this paragraph. The end parabolics in any intermediate quotient H/M, with M normal in H and M≤L, are unchanged marked copies of A and B. The standard recursive string-C recognition criterion therefore gives

    H/M is the group of a regular polytope
       iff M∩D={1},       where D=L∩AB.           (3)

The standard group/polytope correspondence and recursive recognition are retained geometric background. Formula(3) is proved from Lemma1 and the injectivity assumptions. In particular, it is not a claim that arbitrary quotients preserve the local polytopality hypotheses.

There is an oriented version used in the finite example below. Let H be a string C+ group with its mirror automorphism μ, representing a directly regular polytope. Take the end **rotation** parabolics A,B and C=A∩B. If L is normal and μ-invariant, intersects A,B trivially, and M≤L is also normal and μ-invariant, the same proof gives (3) with the C+ recognition theorem; the induced mirror proves direct regularity. In this version, stability must be tested under conjugations by H **and** μ. It is not enough to select arbitrary vector subspaces of L. Equivalently, one can work throughout in the full regular group H⋊⟨μ⟩, while using the rotation parabolics for the C+ test.

Assume further that R is the smallest regular maniplex cover of a finite polytope P. Every intermediate polytopal quotient H/M covers P. A maximal admissible M inside L gives a minimal regular polytope cover of P, even among covers outside the initially chosen interval: every quotient of H/M is also a quotient of H, and any regular cover of P factors through R. Thus any further regular polytopal quotient would correspond to an admissible overgroup of M within L. Conversely, every minimal cover of P that is covered by H arises in this way. This does not assert that all minimal covers of P are covered by H.

For the oriented formulation, R denotes the rotation part of the smallest regular maniplex cover; the same statement holds for its full group after adjoining the mirror. Every regular cover of a chiral P is orientable, so its universal kernel lies inside the universal rotation subgroup. No infinite-cover minimality issue occurs when H is finite: its quotients are finite.

## 3. A support theorem for elementary abelian kernels

In the setting of Section2, assume H is finite. Suppose L is elementary abelian of order p^d, written additively as an F_p-vector space. Let Ω be its induced conjugation group; include μ in Ω in the oriented formulation. Assume that, as an Ω-module,

    L=L1⊕⋯⊕Lt,

where the Li are simple and pairwise nonisomorphic. This is an explicit multiplicity-free semisimplicity assumption. We do not assert it for arbitrary elementary abelian covering kernels.

For x∈L define supp(x)={i:the Li-coordinate of x is nonzero}. Form a finite hypergraph on {1,...,t} whose nonempty hyperedges are the supports of elements of D\{0}. Repeated edges can be discarded. Write H_D for this collection. It is harmless to keep only its inclusion-minimal edges.

**Theorem2 (support classification and join-density).** Under these hypotheses:

1. Every admissible intermediate kernel is uniquely L_J=⊕_(i∈J)Li for a subset J containing no hyperedge of H_D.
2. The minimal regular covers of P which are covered by H correspond exactly to the maximal hyperedge-free subsets J.
3. The join of all admissible intermediate kernels equals

       ⊕ {Li : D∩Li={0}}.                        (4)

4. If each D∩Li={0}, then the join equals L. If also R is nonpolytopal, there are at least two different maximal admissible kernels. Their quotients are distinct minimal regular covers of P under rank-preserving isomorphisms, and the join of **all** finite admissible universal kernels is the entire monodromy kernel K.

**Proof of the module assertion.** Every Ω-invariant subspace M of L is a sum of a subset of the Li. To prove this without concealing a classification theorem, choose a simple submodule T of a nonzero M, possible by finite dimension. A nonzero coordinate projection T→Li is an isomorphism by simplicity. There is at most one such coordinate, since the Li are pairwise nonisomorphic. Hence T is exactly that coordinate Li. Subtracting its coordinate gives M=Li⊕(M∩⊕_(j≠i)Lj). Induction on dimension proves the claim. Conversely, every coordinate sum is invariant. Normality (and mirror stability where required) of a subgroup of the elementary abelian L is exactly Ω-invariance.

A vector x is in L_J precisely when supp(x)⊆J. Therefore (3) says that L_J is admissible exactly when J contains no member of H_D. This proves1, and maximality plus Section2 proves2. If D∩Li≠0, the singleton {i} is a hyperedge, so no admissible J contains i. If D∩Li=0, Li itself is admissible, so it appears in the join. This proves3.

For4, the singleton condition makes the join L. Nonpolytopality of R means D≠{0}, by (3) with M=L, so the entire vertex set is not admissible. A unique maximal admissible subset would contain every admissible singleton, hence every vertex, a contradiction. There are at least two maximal admissible subsets. Their quotients are minimal by Section2 and distinct because their marked universal relation kernels differ.

Finally let N0 be the kernel of the universal group W→H and let K be the kernel of W→R. The inverse image of L is K. Every admissible M has inverse image N_M, an admissible finite-index universal kernel containing N0. Inverse image identifies the subgroup interval [1,L] with [N0,K], preserving joins. Thus the join of these N_M is K; the join of all finite admissible kernels is also K. For the oriented version use μ-invariant normals in the universal rotation group, which are precisely the corresponding full W-normal kernels. ∎

This theorem supplies a finite, checkable sufficient condition for global join-density and cover multiplicity. It is not merely the definition of the global join: the condition is a decomposition of one explicit finite covering kernel and an intersection test with each simple constituent.

**Precise obstruction within this interval.** If D meets some simple constituent Li nontrivially, then every admissible intermediate kernel omits Li, and the interval join is proper in L. This obstructs this particular finite witness of global density. It does not prove that the global join is proper: another polytopal cover not covered by H might supply the missing relations.

The hypothesis cannot be weakened to “L is elementary abelian; all its subspaces are candidate regular kernels”. Invariance under Ω is essential. The concrete example in Section6 disproves that replacement.

## 4. Central kernels: an exact count of minimal covers

A second general case admits a closed formula without a multiplicity-free assumption. Retain the finite locally injective setup of Section3 and assume L is central and elementary abelian of order p^d. In the oriented version, assume additionally that μ acts as a scalar on L (so every subspace is mirror-invariant).

**Theorem3.** The defect set D is a vector subspace of L. Put e=dim(D). The maximal admissible intermediate kernels are exactly the vector-space complements to D, and there are

    p^(e(d−e))

of them. Every corresponding minimal cover has degree p^e over R. If 0<e<d and R is a finite-polytope monodromy quotient as in Section2, then global join-density holds and P has at least p^(e(d−e)) distinct finite minimal regular polytope covers.

**Proof.** Use the lift map f(x)=a_x b_x^−1 from the proof of(2), for x∈π(A)∩π(B). Its values lie in central L. For x,y in that intersection, uniqueness of the lifts gives

    f(xy)=a_x a_y b_y^−1 b_x^−1
         =a_x f(y)b_x^−1=f(y)f(x)=f(x)f(y).

Thus f is a homomorphism with image D and kernel π(C). In particular D is a subgroup, hence an F_p-subspace. Every subspace of L is normal, and in the oriented case the scalar mirror preserves it. By(3), admissible subspaces are exactly those disjoint from D. Every such subspace extends to a complement of D by extending a basis of its image in L/D. Therefore the maximal admissible ones are precisely the complements.

Fix one complement F. Every complement is the graph of a unique linear map F→D, and conversely each such graph is a complement. There are p^(e(d−e)) such maps. Each complement M has dimension d−e, so |L/M|=p^e. Section2 proves global minimality of each quotient among regular covers of P; distinct complements give distinct marked kernels and therefore nonisomorphic regular polytopes under rank-preserving isomorphisms. No identification by permutations of the ranks is intended.

If 0<e<d, choose 0≠v∈F. For any x∈D, a linear map F→D taking v to x gives a complement containing v+x. The reference complement contains v; hence the join of all complements contains x. It also contains F, so this join is L. Pulling back to universal kernels proves global join-density exactly as in Theorem2. ∎

The endpoint cases are explicit: if e=0, the largest admissible kernel is L and R is already polytopal. If e=d, the only admissible kernel is0 and H is the unique minimal quotient **within this interval**; this says nothing about covers not covered by H. The central hypothesis cannot be replaced by abelianity: Section6 has an abelian noncentral L and a nonnormal defect. The complete count above is conditional on the stated central/scalar action assumptions and is not asserted for that example.

## 5. A finite algorithm certificate

For any finite marked polytopal H and kernel L which is injective on the two ends, a complete certificate for this interval consists of:

1. Exact marked group operations; normality of L; trivial intersections L∩A,L∩B; and the original recursive intersection properties.
2. The finite set D=L∩AB, computed by exact multiplication, or through the lift-coset bijection in (2).
3. A complete list of Ω-invariant subgroups of L, with the test M∩D={1} on each; and the inclusion-maximal successful subgroups.

Theorem2 replaces item3 by finite linear algebra and a hypergraph computation when its module hypothesis is verified. The proof above certifies completeness of the resulting list of normal kernels. If a decomposition is supplied explicitly, its verification requires that each Li be invariant, simple, pairwise nonisomorphic, and sum directly to L. For one-dimensional distinct characters these are immediate once the generator action table is checked.

Neither (2) nor matching subgroup orders alone certifies subgroup equality; the executable example checks the actual subgroups, the actual set D, all quotient maps, and the explicit actions.

## 6. Complete interval for Cunningham's finite chiral example

Start from the three exact presentations and the groups P,R,Q,Q' in the frozen phase41 package. Let H=Q⋄Q' denote the marked rotational mix. The phase46 certificate rebuilds those groups from their bare presentations, leaving every frozen file untouched. It verifies that H has order8748 and that its end rotation parabolics A,B both have order162, intersect in C=⟨b⟩ of order9, and satisfy the two local cyclic intersection conditions. The interval-square rotation relations hold and the mirror assignment is an automorphism. Thus H is the rotation group of a directly regular polytope, by the retained C+ correspondence.

The marked map H→R has kernel L of order9 and exponent3, intersecting A and B trivially. Define the two literal rotation words in H

    u=(b c^−1)^2 a c^2 a^−1,
    v=(b^−1 a)^2 c^−1 a^−2 c.

They commute, each has order3, and L=⟨u⟩×⟨v⟩. The first is the kernel generator of H→Q and the second is the kernel generator of H→Q'. The exact conjugation/mirror action is:

| operator | u | v |
|---|---|---|
| conjugation by a | u | v^−1 |
| conjugation by b | u | v |
| conjugation by c | u^−1 | v |
| mirror μ | u | v^−1 |

The action image is therefore C2×C2, and the two axes are distinct one-dimensional simple F3-characters. This verifies the multiplicity-free hypothesis directly. In particular, L is not central.

The defect set is exactly

    D={1,uv,u²v²}=⟨uv⟩.

Thus the support hypergraph has the single edge {1,2}. The only Ω-invariant subgroups are 1,⟨u⟩,⟨v⟩,L. The first three avoid D nontrivially, and L does not. The two maximal admissible kernels are exactly ⟨u⟩ and ⟨v⟩. Their quotients are the original Q and Q', so these are exactly the two minimal regular covers of P among the regular covers that are quotients of H. This supplies a complete finite interval classification, not a classification of all minimal covers of P.

Theorem2 gives global join-density for this example and recovers multiplicity. Here it agrees with the distinct-prime-index proof in phase44, but additionally explains the obstruction and proves the interval list complete.

There are four one-dimensional subspaces of L. The two diagonal lines are not Ω-invariant. The line ⟨uv⟩ is the defect; the other diagonal line also avoids D but cannot be used as a normal regular quotient kernel. This is an actual example inside the target monodromy-cover setting showing why abelianity of L does not permit replacing invariant-subspace enumeration by all-subspace enumeration. It also disproves the assertion that D must be normal, even though in this example it happens to be a subgroup.

## 7. A small counterexample to a different stronger claim

Even with a polytopal source and injectivity on both ends, D need not be a subgroup. Take the tetrahedral string C-group S4 with r0=(12),r1=(23),r2=(34), A=⟨r0,r1⟩, B=⟨r1,r2⟩, and the normal Klein four subgroup L. Both A and B meet L trivially. Direct multiplication gives

    D=L∩AB={1,(12)(34),(13)(24)}.

The product of the two nonidentity elements is (14)(23), which is absent, so D is not a subgroup. This verifies that subset products and support sets, rather than automatic subgroup quotients, are needed in the general algebraic criterion. The quotient S4/L identifies the nonadjacent marked involutions r0 and r2, so it is **not** a proper maniplex or a monodromy group of a polytope in this rank. This small example is not claimed as a counterexample to the cover conjecture, nor as proof that D can fail to be a subgroup under every stronger monodromy hypothesis.

## 8. What remains open in this investigation

The general problem is unchanged: for an arbitrary finite-polytope monodromy kernel K, must the join of all finite admissible universal kernels be K, or at least give a nonpolytopal quotient whenever W/K is nonpolytopal? Theorems2 and3 prove this under explicit additional hypotheses on one finite cover. It does not prove that every P admits such a cover or such a module decomposition. The five infinite tight families in the source have not been checked here.

The older geometric recognition theorems and stock GAP exact group algorithms are retained. No new Lean component is claimed. The primary-source status search and its limitations are in frozen phase44: Cunningham–Pellicer2018 Problem5 asks whether unique minimal regular polytopal covers can occur with non-string-C monodromy; the2024 chiral paper gives the single finite example; F0052025 provides mix-polytopality criteria, not the missing join existence theorem. None of these sources is assumed to assert Theorem2, and no priority/novelty claim is made for the elementary quotient test or module facts.
