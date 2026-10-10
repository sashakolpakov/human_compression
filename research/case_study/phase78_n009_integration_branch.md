## 24. Central quotients and the complete order-1024 classification

This branch concerns the principal nondegenerate classification in Gomi–Loyola–De Las Peñas [GLP18], with the marking retained. Its equivalence sends the distinguished generator set onto the other set. For a connected string diagram this permits precisely the two orders related by reversal. It does not identify arbitrary markings of an abstractly isomorphic group. The rank-two case is the unique dihedral marking of order 1024. The three higher-rank totals below are 125, 105 and 8; all stated types, facets and universal orders are part of the conclusion.

The specifically retained prior results in this branch are the standard string intersection criteria quoted as [GLP18] Lemmas 2.2–2.4, the universal geometric interpretation quoted as its Theorem 4.2, the finite smooth square-quotient classification quoted as its Lemma 5.1, and the exceptional infinite universal decomposition quoted as its Theorem 5.3. Their relevant precise forms are stated below. Exact finite-group and complete coset-enumeration algorithms in GAP, and NQ's universal nilpotent quotient algorithm, are computational inputs. The Atlas supplies definitions of named marked presentations, all printed in Appendix G; neither its completeness nor a SmallGroups catalogue is assumed.

### 24.1. Preliminary adapters and exact quotient intersections

**Proposition N1 (endpoint cosets).** A finite string C-group of rank d and adjacent orders m₁,…,m_(d−1) has order at least 2∏mᵢ. In particular, a nondegenerate string two-group of order 1024 has rank at most five.

*Proof.* Put a=r₀, b=r₁ and H=⟨r₁,…,r_(d−1)⟩. IP gives H∩⟨a,b⟩=⟨b⟩. If H(ab)ⁱ=H(ab)ʲ, then (ab)^(i−j) lies in the intersection of the rotation subgroup with ⟨b⟩, which is trivial. The m₁ such cosets, with 0≤i<m₁, are therefore distinct. Iterating gives the bound. Each mᵢ is at least four in the stated two-group case, so 2^(2d−1)≤1024, forcing d≤5. ∎

The smooth Coxeter quotient assertion in source Theorem 2.7 is the homomorphism from the string Coxeter presentation sending each distinguished generator to its marked involution; the specified adjacent orders make it smooth. A disconnected string diagram yields a direct product of its component subgroups: they commute and IP makes each meet the subgroup on the other components trivially. This gives the source's preliminary reduction; a separate census of every degenerate product is not added to the principal contract. Source Lemma 2.8 is the coordinate-character consequence of Burnside's basis theorem: an irredundant generating list of a finite two-group maps to a basis of G/Φ(G), and every binary assignment extends to a homomorphism to C₂. No infinite-group assertion is made here.

For rank three write L=⟨a,b⟩ and R=⟨b,c⟩. The retained rank-three criterion says that these two rank-two marked string C-groups, together with [a,c]=1 and L∩R=⟨b⟩, give full IP. Precisely, for d=4 or 5, the versions quoted in source Lemmas 2.3–2.4 require the prefix H=⟨r₀,…,r_(d−2)⟩ to have IP and each equality H∩⟨rⱼ,…,r_(d−1)⟩=⟨rⱼ,…,r_(d−2)⟩ for j=1,…,d−1, with the final right side trivial. These are respectively all four and all five source hypotheses. All finite certificates below instead test every subset pair directly.

If N◁G and N∩RL=1, Theorem K(d) says the quotient facets have exactly their old intersection and both embed; their product orders are unchanged. This is source Lemma 3.1. If N≤L and the displayed images of a,b still give a rank-two marking on L/N, then N∩R≤⟨b⟩ and b∉N, so R embeds. The last clause of K(d) gives the same facet intersection and the rank-three criterion gives IP. This is source Lemma 3.2, including its symmetric case. An unrelated marking on the abstract quotient L/N would not suffice.

### 24.2. A safe central quotient and the three complete lift patterns

Assume throughout this subsection that G is a finite marked string two-group ⟨a,b,c⟩, with m=|ab|≥4 and n=|bc|≥4. Put x=(ab)^(m/2) and y=(bc)^(n/2).

**Lemma N2 (central elements in an end product).**

\[
Z(G)\cap RL\subseteq\{1,x,y,yx,ybx\}.
\tag{N1}
\]

If yx is central, x and y are separately central. The element ybx is never central.

*Proof.* Every element of RL has a unique expression h(ab)ʲ with h∈R and 0≤j<m. Equality of two expressions would put a rotation in L∩R=⟨b⟩. Conjugation by b negates j, so centrality implies j=0 or m/2. The former case gives an element of Z(R)={1,y}. In the latter case write z=hx; since x commutes with b, h lies in C_R(b)={1,b,y,yb}. The choice h=b fails because the reflection bx does not commute with a when m≥4. This proves (N1).

If yx commutes with a, then y does, because x already does; commuting with c similarly makes x commute with c. Thus both half-rotations are central. Finally x,y∈Φ(G), since they are even powers of rotations. If z=ybx were central, then a,z,c would have the same Frattini basis as a,b,c and would generate G. A central z is an involution here: z∈C_G(x) implies y commutes with x, and y,b,x are commuting involutions. Thus a,z,c are three commuting involutions, contradicting |ab|≥4. ∎

**Theorem N3 (central descent with IP).** G has a central order-two subgroup N such that the displayed images of a,b,c give a rank-three string C-group on G/N. Successive such descents, allowing degenerate intermediate markings, stop at C₂³.

*Proof.* If x is central, take N=⟨x⟩. The marked dihedral quotient L/N has rotation order m/2≥2 and R embeds because N∩R=1. The N≤L clause of K(d) proves the quotient intersection. The same reasoning applies to central y. If neither half-rotation is central, choose any central involution z, which exists in every nontrivial finite two-group. Lemma N2 puts z outside RL; now the injective-ends clause of K(d) proves IP and preserves both end groups. A degenerate rank-three marking is C₂ times a dihedral marking. Unless it is C₂³, the central rotation involution of its nonabelian dihedral factor can be factored out while preserving rank three. Orders strictly decrease by two, so this process terminates exactly at C₂³. ∎

This proves source Corollary 3.3, Lemmas 3.4–3.5 and Theorem 3.6. The bottom boundary is necessary in source Corollary 3.7: a rank-three order-eight group cannot have a rank-three order-four quotient. Its literal unrestricted wording is not asserted.

**Theorem N4 (three lift patterns with complete presentations).** Let Q be a finite rank-three marked string C-group with a complete presentation in its involutions a₀,b₀,c₀, including Coxeter relations and additional relators R₁,…,Rₜ. Let G=⟨a,b,c⟩ be a central extension with kernel ⟨z⟩ of order two, mapping those involutions respectively to a₀,b₀,c₀. Suppose the lifts are involutions, [a,c]=1 and G has IP. Exactly three order patterns are possible: the left adjacent order doubles, the right adjacent order doubles, or neither doubles. In each case a complete presentation is obtained by adjoining central z with z²=1, each defining Coxeter word of Q set equal to its actual value 1 or z (in particular (ab)^p=z when its quotient order p doubles), and equations Rᵢ=z^(εᵢ), εᵢ∈{0,1}. At least one relation expresses z as a word in a,b,c, so z can be eliminated.

*Proof.* Each adjacent order is unchanged or doubled. If both doubled, z would be the halfway rotation in both L and R and hence in their intersection ⟨b⟩, impossible for a nontrivial dihedral rotation. Every defining word of Q lifts to 1 or z. The indicated presentation P maps onto G and has P/⟨z⟩=Q; centrality and z²=1 imply |P|≤2|Q|=|G|, proving that map an isomorphism. When an adjacent order doubles, its half-power is z. If neither does and every additional relator lifted to 1, the generating tuple would define a surjection Q→G, contradicting the orders. ∎

This is source Theorem 3.8 and Table 1. It classifies successful extensions; it does not assert that every binary lift choice has the required order or IP. Those properties and equality of ordered markings must still be checked.

### 24.3. One exhaustive computation for both the seed and all three ranks

Apply Theorems Q5.5–Q5.6 to the path on d vertices with k=log₂|G|−(2d−1). Appendix A is a single parameterized program for the four cases in the following table. NQ computes the universal nilpotent quotient of class k+2. The original generators are transported through its epimorphism and pc isomorphism; they are never replaced by an arbitrary generating list. Every normal kernel in the invariant ladder is generated, with only equal subgroups deduplicated. The binary canonical subgroup key is used only after all ambient relative pc orders have been checked to be two.

| d | k | Order of U | Order of γ₃(U) | Terminal kernels | Ordered IP markings | Reversal-fixed | Classes | Direct IP meets |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 3 | 2¹⁸ | 2¹³ | 61 | 37 | 3 | 20 | 3904 |
| 3 | 5 | 2³⁸ | 2³³ | 401 | 235 | 15 | 125 | 25664 |
| 4 | 3 | 2³⁴ | 2²⁷ | 1483 | 199 | 11 | 105 | 379648 |
| 5 | 1 | 2¹⁶ | 2⁷ | 127 | 15 | 1 | 8 | 130048 |

The ladder sizes are respectively (7,23,61), (7,23,61,147,401), (31,267,1483) and (127). These are computed outputs, never candidate filters. All 539264 subset-pair intersections are tested, including every candidate rejected by the kernel-profile criterion, and the two IP decisions agree for every candidate. Burnside's orbit formula gives (ordered+fixed)/2 reversal classes. The four ordered type-{4,8} markings in the first case satisfy the four distinct word rows in §13, one each; this is the same finite input used in the eight-family completeness proof. The last three cases prove the classification at order 1024, with the rank bound in Proposition N1 proving that no further nondegenerate rank is omitted.

For rank three the twelve type counts, up to reversal, are:

| Type | Count | Type | Count |
|---|---:|---|---:|
| {4,4} | 1 | {8,8} | 22 |
| {4,8} | 8 | {8,16} | 40 |
| {4,16} | 14 | {8,32} | 8 |
| {4,32} | 4 | {8,64} | 4 |
| {4,64} | 2 | {16,16} | 10 |
| {4,128} | 2 | {16,32} | 10 |

These are exactly source Table 5. The complete presentations defining all named facets, and the full 107 rows of Table 6, appear as literal mathematical data in Appendix G. For every one of the 199 rank-four and 15 rank-five ordered markings, Appendix F reconstructs the quotient from its exact new kernel key and proves unique generator-preserving isomorphisms from both named end groups: 428 exact facet identifications. It computes dual names from reversed generators, rather than assuming that equal-looking types or letter suffixes are self-dual. Under reversal a facet pair (A,B) becomes (dual(B),dual(A)). Counts are compared after this operation for each of the 99 rank-four and eight rank-five rows individually.

The four printed type-{4,16,4} rows in Table 6 have right-hand type {4,16}; their ordered vertex-figure markings necessarily have type {16,4}. The data use precisely these duals, preserving every letter suffix and count. This qualification was checked on printed page 16; it is not an inferred change to class counts.

For each of the 106 finite rows, the complete universal presentation is the union of the two complete facet presentations, shifted to overlapping generator lists, together with the distant-end commutation relation. Completed Todd–Coxeter enumeration at the trivial subgroup gives 101 orders of 1024 and five orders of 2048. The finite checker also verifies actual IP and both exact facet embeddings. The remaining row is the explicitly retained infinite universal of §24.6; it is never sent to an unbounded finite-order test.

### 24.4. Every printed rank-three presentation and its corrections

The complete finite-presentation protocol in Appendix F takes the bare displayed relators, performs complete trivial-subgroup Todd–Coxeter enumeration, and checks that the resulting permutation action has the table's full order. It evaluates every relator, proves generation by the specified marked involutions, and tests all 4^d marked-subgroup intersections. Thus its order bounds concern the raw presented groups, not just finite images or nilpotent truncations.

Write C(p,q) for the rank-three Coxeter relations of type {p,q}. In source Table 2, adjoin to C(4,8) the following pairs, set equal to 1:

| Name | R₁ | R₂ |
|---|---|---|
| 512a | (abcb)⁴ | (ca(bc)³ab)² |
| 512b | (cab)⁸ | (a(bc)³b)² |
| 512c | (c(abcb)²)² | (ca(bc)³ab)² |
| 512d | (a(bc)³b)² | (cab)⁵c(ba)²(cb)²ab |

All four raw groups have order 512 and are pairwise inequivalent as ordered markings; their complete primary Atlas presentations are identified exactly. Class I of source Example 3.9 would require an order-512 quotient of C(2,8), whose order is 32, so contributes none. Class II uses C(4,4) with (abcb)⁸=1, of order 512; its two lifts have central τ=(bc)⁴ and (abcb)⁸=1 or τ. They define the two distinct targets called 1024a and 1024b. For each Table 2 row, the three Class III choices (R₁,R₂)=(τ,1),(1,τ),(τ,τ), with central τ²=1, yield exactly:

| Base | (τ,1) | (1,τ) | (τ,τ) |
|---|---|---|---|
| 512a | 1024c | 1024d | 1024e |
| 512b | 1024a | 1024c | 1024f |
| 512c | 1024c | 1024g | 1024h |
| 512d | 512d | 1024a | 512d |

Quotienting by the actual τ subgroup recovers the named base marking in every case. In the two order-512 outcomes τ=1. All eight order-1024 targets are pairwise inequivalent as ordered markings and match the eight type-{4,8} quotients in the unfiltered census bijectively, proving completeness independent of any source table assertion.

Separately evaluating every literal Table 4 row gives the ordered-label map

\[
(a,b,c,d,e,f,g,h)_{\mathrm{printed}}
\longmapsto(a,b,c,d,c,a,g,c)_{\mathrm{Table\,3}}.
\tag{N2}
\]

To obtain its intended eight targets, the second displayed additional relation in each of printed rows e,f,h must have right-hand side τ instead of 1. These are exactly the already checked (τ,τ) lifts of Table 2 rows a,b,c. No other row or count changes. Printed page 10 was inspected visually; the diagnosis is about the literal source, without claiming priority or unique editorial intent for the repair.

### 24.5. Universal presentations and all finite examples

For source Definition 4.1 use the combined facet presentation described in §24.3. The retained geometric universal principle, source Theorem 4.2, states that a nonempty class of regular polytopes with those specified facet and vertex-figure groups has that marked universal string C-group and every member is its smooth quotient. At the group-presentation level the epimorphism is immediate from the defining words; the abstract-polytope interpretation remains an explicit background input.

The bare presentations in Examples 4.3–4.5 give:

| Object | Raw order | Type | Ordered end labels |
|---|---:|---|---|
| Example 4.3 universal | 512 | {4,4,4} | {4,4}*32, {4,4}*128 |
| Example 4.4 universal | 1024 | {4,4,4} | {4,4}*32, {4,4}*256 |
| Example 4.5 universal | 2048 | {4,4,8} | {4,4}*64, {4,8}*128a |
| Example 4.5 first quotient | 1024 | {4,4,8} | same two labels |
| Example 4.5 second quotient | 1024 | {4,4,8} | same two labels |
| Example 4.5 third quotient | 1024 | {4,4,4} | not in the prescribed smooth class |

The first two universal presentations add (abcb)²=(bcdc)⁴=1 and (abcb)²=(dbc)⁸=1 respectively to the type-{4,4,4} Coxeter relations. The third adds

\[
(cab)^4=1,\qquad dbcd(cb)^2(dc)^2bc=1
\tag{N3}
\]

to the type-{4,4,8} relations. The complete named facet words in Appendix G differ, where necessary, only by cyclic conjugation from these displayed source words. Their exact generator-preserving isomorphisms and the full raw order/IP tests verify each row above.

For the order-2048 group the three printed central-involution words are

\[
bcdcbab(dc)^2dba,\qquad(bcdcba)^2,\qquad(cd)^4.
\tag{N4}
\]

The checker independently enumerates all central involutions and obtains exactly these three distinct elements. Adding each as a raw relator gives the three quotient rows above. The first two are inequivalent marked groups, with unchanged type and end markings. Every normal order-two subgroup is central, so these three exhaust all order-1024 quotients of this universal, and exactly two belong to the prescribed smooth class. Example 4.3 has no quotient of order 1024; Example 4.4 has only itself. These statements concern these exact orders and do not extrapolate centrality to larger kernels.

### 24.6. Square-lattice centers and the exceptional infinite row

Retain the finite smooth square-quotient classification quoted in source Lemma 5.1: a finite smooth quotient of [4,4] lies in one of the two families obtained by adding (abcb)^s=1, of order 8s², or (abc)^(2s)=1, of order 16s², for a positive integer s. The former has |abcb|=s and |abc|=2s; the latter has |abcb|=2s and |abc|=2s. The retained decompositions are (⟨a,c^b⟩×⟨c,a^b⟩)⋊⟨b⟩ in the first case, and (⟨b,b^a⟩×⟨b^c,b^(ac)⟩)⋊⟨a,c⟩ in the second. Each displayed factor is dihedral of order 2s; the complements have orders two and four respectively. These structural identifications are part of the quoted prior theorem, rather than inferred from the orders. Only the finite scope is used; the infinite Coxeter group itself is not asserted to admit such an s.

Use the common affine model of §9, in coordinates

\[
a(x,y)=(1-x,y),\quad b(x,y)=(y,x),\quad c(x,y)=(x,-y).
\tag{N5}
\]

Its group is W=ℤ²⋊D₈; t=abcb translates by (1,0), (abc)² translates by (1,1), (bc)² is (0,−I), and (ab)² is ((1,1),−I). The two finite families are W/sℤ² and W/L_s, where L_s=⟨(s,s),(s,−s)⟩. The §9 affine normal forms establish these identifications; equivalently the displayed source relations give surjections onto these affine images of the stated orders, hence isomorphisms.

**Proposition N5 (all source center formulas).** For s=2^m, in W/sℤ² the center is ⟨(ab)²,(bc)²⟩ when m=1 and ⟨(abc)^s⟩ when m≥2. In W/L_s it is ⟨ac,(ab)²,(bc)²⟩ when m=0 and ⟨(abcb)^s⟩ when m≥1.

*Proof.* In a central affine pair (v,M), commutation with all translations forces M to act trivially on T=ℤ²/L. If the signed-permutation action on T is faithful, M=I and the center is T^(D₈).

For L=sℤ², s≥4, faithfulness is immediate on the two coordinate vectors. Invariance gives 2x=2y=0 and x=y modulo s, leaving precisely 0 and (s/2,s/2). For s=2, the action kernel is the diagonal sign subgroup; to commute also with the linear D₈ subgroup, M must lie in {I,−I} and v in {0,(1,1)}. This gives the first exceptional center. No first-family formula at m=0 is claimed in the source or here.

For L=L_s with s≥2, a nontrivial diagonal sign change cannot act trivially, since (2,0) and (0,2) do not lie in L_s. A signed swap cannot act trivially because its difference on a coordinate vector has a coordinate ±1, not divisible by s. A fixed translation satisfies (2x,0),(0,2y)∈L_s, hence s divides both x,y; modulo L_s its class is 0 or (s,0), both swap-invariant. For s=1 the lattice consists of vectors with even coordinate sum, so T=C₂ with trivial D₈ action and the group is C₂×D₈. Here ac=(t,−I), (bc)²=(0,−I), and (ab)²=(bc)² in the quotient, giving exactly the claimed generating set. Its three displayed generators are not independent. ∎

For the sole infinite row of Table 6 retain the exact source Theorem 5.3, attributed there to McMullen–Schulte: the universal type-{4,4,4} group with extra relations (abcb)⁴=(bcd)⁴=1 has

\[
U=(W_1\times W_2)\rtimes\langle b,d\rangle,
\quad \langle b,d\rangle\cong C_2^2,\quad
W_1=\langle c^{bd},a,c^b\rangle\cong[4,4],\quad
W_2=\langle c,a^b,c^d\rangle=W_1^b.
\tag{N6}
\]

In particular it is infinite. This theorem, including its marked decomposition, is retained and is not a result of finite coset enumeration.

**Proposition N6 (the exceptional kernel location).** If π:U→G is a marked epimorphism to a finite string two-group with IP, then kerπ≤W₁×W₂ and

\[
G\cong ((W_1\times W_2)/\ker\pi)\rtimes\langle\pi(b),\pi(d)\rangle.
\tag{N7}
\]

*Proof.* IP makes the four marked generators irredundant. Their images form a basis of G/Φ(G). The b- and d-coordinate characters, composed with π, agree on every generator with the projection U→C₂² in (N6): the displayed Wᵢ generators have even b- and d-parities. Thus every element of kerπ lies in W₁×W₂. The image of ⟨b,d⟩ still has order four by these same coordinate characters and meets the image of W₁×W₂ trivially, proving the split quotient formula. ∎

This proves source Lemma 5.4 without assuming quotients preserve IP. At order 1024 the first factor in (N7) has order 256. Finally the two source Theorem 5.5 presentations share the type-{4,4,4} Coxeter relators and (abcb)⁴=(bcd)⁴=1. The first adds (dcbabdc)²=1. The second adds

\[
(bdcdba)^2(cbab)^2=1,\qquad(abcb)^2(babdcd)^2=1.
\tag{N8}
\]

Appendix F proves directly that these two raw groups have order 1024 and full IP, and identifies them with the two and only two census markings whose ordered ends are {4,4}*128 and {4,4}*64. Unequal end orders rule out their becoming equal under reversal. This proves the exact exceptional classification without repeating the source's separate case analysis or presuming its presentations finite.

The finite execution in Appendix F totals 214 complete presentations and 43840 actual IP meets: 72 defining Atlas models, 34 source example/literal-table presentations, the two exceptional presentations, and 106 finite universal presentations. Its distinct logical role from Appendix A is preserved: the universal-kernel proof gives exhaustion, while complete raw coset tables and exact marked isomorphisms give presentation and name recognition. All code and mathematical data are printed. These are exact finite computations conditional on the stated algorithms, not Lean proofs or experimental extrapolations. The concluding source suggestion about geometric realizations, a separate classification of all degenerate products, and historical novelty of the corrections are outside the contract.
