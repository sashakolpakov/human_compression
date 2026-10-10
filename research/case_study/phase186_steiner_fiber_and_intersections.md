# The Steiner chamber fiber and rank-two intersections

This extension belongs to the private L092 intake. It retains Construction2 from D. Leemans, *A Generalization of a Construction due to Van Nypelseer* (2005), and the classical Steiner-design facts explicitly named below. It supplements the independently reviewed residue recursion rather than repeating its proof.

The source-reading scope is the complete fourteen-page paper. The common geometry and connectivity argument is the root draft phase182_steiner_residue_recursion.md, independently checked in phase187_residue_recursion_review.md. The review includes the full ordinary-chain necessity argument and all exceptional-type residue cases. The join decomposition and induction are valid: a flag containing an ordinary j-subset reduces to a Boolean factor and Γ of the j-fold derived design; a complete ordinary chain removes the Boolean factors for the converse. The t=2 connectivity base is a retained rank-three question, not an inferred connectivity assertion.

Throughout let S=S(t,k,v), t≥2, k≥t+1, and
\[
r=\frac{v-t+1}{k-t+1}\ge3.
\]
These are exactly the source's firmness parameters. Write Γ(S) for its Construction2.

**Firmness necessity.** The retained residue note proves sufficiency of the displayed conditions. Conversely, if Γ(S) is a firm geometry, extend any marked object (T,E) to a chamber. Removing its copied point leaves a panel with exactly |E|=k−t+1 completions, so k−t+1≥2. Removing its alternative block leaves a panel with exactly r−1 completions, so r−1≥2. Thus the conditions are also necessary, recovering the full iff in L092 Lemma1. If r=1 there is no chamber containing the marked object in the first place.

## 1. A single chamber fiber

A chamber of Γ(S) consists of a full chain of ordinary subsets, a marked pair (T,E), an alternative block B₀ containing T and disjoint from E, and a copied point z∈E. Here |T|=t−1 and B′=T∪E is a block. The ordinary chain together with T uniquely orders its t−1 points: its successive differences are singletons.

**Theorem C.Fiber.** For every G≤Aut(S), there is a G-equivariant bijection
\[
\operatorname{Ch}(\Gamma(S))
\longleftrightarrow
\{((x_1,\ldots,x_t),B_0):
x_i\text{ distinct},\
T=\{x_1,\ldots,x_{t-1}\}\subset B_0,\
x_t\notin B_0\}.
\tag{C1}
\]
Over each ordered t-tuple the fiber contains exactly r−1 blocks. Consequently G is chamber-transitive if and only if:

1. G is t-transitive on the points of S;
2. the stabilizer of one ordered t-tuple is transitive on these r−1 blocks.

In particular,
\[
|\operatorname{Ch}(\Gamma(S))|=(v)_t(r-1),
\tag{C2}
\]
where (v)t=v(v−1)⋯(v−t+1).

**Proof.** From a chamber take x₁,…,x(t−1) in the order determined by its ordinary chain and T, and put x_t=z. The condition B₀∩E=∅ implies z∉B₀.

Conversely, given the right-hand data in (C1), let B′ be the unique block containing the t-set T∪{x_t}. Because x_t∉B₀, the blocks B′ and B₀ differ. Distinct Steiner blocks have at most t−1 common points, so their intersection is exactly T. Put E=B′∖T, take the ordinary chain of initial subsets of the ordered tuple, and use the copied point z=x_t. This reconstructs a chamber. The two constructions are inverse and use only invariant set operations, hence are G-equivariant.

There are r blocks through T and precisely one of them contains x_t, namely B′. Thus the fiber size is r−1. The standard orbit-fiber lemma, retained as U.Orbits, now gives the transitivity criterion: a transitive action on the total set must be transitive on its base and each stabilizer fiber, and these two conditions conversely move any total object to any other. Counting the base and fibers proves (C2). ∎

This proves and sharpens the organization of L092 Theorem9. The source's Property(*) uses three successive choices: a chamber of Construction1, an alternative block, then a point of its complement. The bijection (C1) combines the last point with the ordered tuple and pays only one final fiber. The underlying theorem and construction remain attributed to the source; the explicit one-fiber organization is the present reusable deduction.

The number of objects of each type is also uniform:
\[
n_i=\binom vi\ (1\le i\le t-2),\qquad
n_{\rm block}=\frac{\binom vt}{\binom kt},\qquad
n_{\rm marked}=n_{\rm block}\binom{k}{t-1},\qquad
n_{\rm copy}=v.
\tag{C3}
\]
The marked count follows by choosing B′ and then T⊂B′. Together with the already proved panel sizes 2, k−t+2, r−1 and k−t+1, these formulas recover the object counts and local orders in the source's design diagrams. Stabilizer isomorphism types are additional data; an orbit size alone does not prove them.

## 2. The intersection property is uniform

A rank-two geometry satisfies the source's intersection property when it is a partial linear space or a generalized digon. The following statement supplies this condition for every firm Steiner construction; it is not an extra classification assumption.

**Theorem C.Intersections.** Under the displayed parameter assumptions, Γ(S) satisfies (IP)₂.

**Proof.** Begin with t=2, so S is a linear space and Γ(S) is Construction3. Its residue at a flag (x,M) is the complete bipartite incidence between M∖{x} and the other lines through x. At an original point p, each remaining flag (x,M) is determined by x, since M is the unique line through p and x. The other remaining objects are lines avoiding p, and the residual incidence is x∈L. This is a subincidence structure of S, so two such point objects lie on at most one residual line. At an original line L, a remaining flag (x,M) is determined by M, because x is its unique intersection with L. The residual incidence with the points outside L is again a subincidence structure of S. Thus both these residues are partial linear spaces.

Induct on t. A rank-two residue whose defining flag contains an ordinary subset is a residue of a join B(X)*Γ(S_X). Residues of a join are joins of the factor residues. If two positive-rank factors remain, both have rank one and their join is a generalized digon. If only the derived factor remains, apply the inductive hypothesis. If only a Boolean factor remains, its rank-two residues have the same elementary form: either a join of two rank-one intervals, or the incidence of singletons and two-element subsets of a three-element set. These are respectively generalized digons and partial linear spaces.

It remains to consider a rank-two residue defined using only exceptional types: marked pair, block, copied point. Its defining flag has size t−1, so t≤4.

For t=4 the flag uses all three exceptional types. The remaining ordinary objects are the nonempty proper subsets of the marked three-set T. Their two ranks give the usual three-point, three-line triangle incidence.

For t=3 the defining flag has two exceptional objects. A marked pair together with a block leaves the two ordinary points in T and the copied points of E, with complete cross-incidence. A marked pair together with a copied point similarly leaves the two points in T and all alternative blocks, again with complete cross-incidence. A block B₀ together with a copied point z leaves ordinary points of B₀ and marked pairs indexed by its two-subsets: the unique block through such a two-subset and z determines the marked pair. Incidence is containment. The point/two-subset geometry on B₀ is a partial linear space.

These exhaust the exceptional cases. The t=2 case was already proved, so the induction is complete. ∎

The Boolean argument requires the full interval decomposition, not a blanket claim that every rank-two truncation of a Boolean lattice is a partial linear space. For example arbitrary nonconsecutive selected subset sizes are not the residues used here. The complete-chain geometry supplies exactly the interval factors described in the proof.

## 3. The affine binary family

Let S_d consist of points and affine planes of AG(d,2), d≥3. Every three distinct points are affinely independent over F₂ and lie in a unique affine plane, so this is S(3,4,2^d). Deriving at the origin identifies the remaining points with nonzero vectors. A derived block is {u,v,u+v}, precisely a projective line in PG(d−1,2). Thus the derived design is PG(d−1,2).

The projective base theorem in phase186_linear_space_bases.md and the retained residue recursion show:
\[
\Gamma(S_d)\text{ is residually connected}\iff d=3.
\tag{C4}
\]
This proves L092 Lemma4 without repeating an obstruction at every rank. The positive base PG(2,2) is included explicitly; the source's Theorem3 excludes q=2, so one must not cite that restricted statement alone for this application.

The full affine group is chamber-transitive for every d≥3. To apply C.Fiber, note first that AGL(d,2) is transitive on ordered triples of distinct points: translate the first point to zero, then send the two independent difference vectors to prescribed independent vectors. Normalize a triple to (0,e₁,e₂). The unique block on it is ⟨e₁,e₂⟩. Alternative planes through the line ⟨e₁⟩ correspond to nonzero vectors in
\[
\mathbb F_2^d/\langle e_1\rangle
\]
other than the vector represented by e₂. The stabilizer fixing e₁,e₂ induces the full stabilizer of that nonzero vector in GL(d−1,2). This group is transitive on the remaining nonzero vectors: any ordered pair of independent vectors extends to a basis. C.Fiber proves chamber transitivity.

At d=3 the type sizes are 8 ordinary points, 84 marked objects, 14 blocks and 8 copied points; the panel sizes are 2,3,2,2 in that type order. There are (8)₃·2=672 chambers. The group AGL(3,2), of order1344, has chamber stabilizer of order2. These statements pay the numerical positive case used in Theorem11. The full design group is exactly AGL(d,2). Indeed, after translating the image of zero back to zero, a design automorphism preserves the unique fourth point x+y of the affine plane through 0,x,y whenever x,y are distinct nonzero vectors. It therefore preserves addition in this case; equal vectors or a zero vector give the same identity immediately in characteristic two. Hence it is linear. This proves the full-group identification directly, while chamber transitivity already follows from the explicit subgroup exhibited above.

## 4. Mathieu applications and the remaining named inputs

For S(4,5,11) and S(5,6,12), formula (C2) gives respectively 23,760 and 285,120 chambers. The literal finite computation phase186_witt_derived_check.g constructs their forced native block systems, verifies the Steiner property and computes full automorphism groups of orders7,920 and95,040. Neither group can therefore be transitive: the chamber count is three times the full group order. No search over putative chamber orbits is necessary.

For S(3,6,22), S(4,7,23) and S(5,8,24), the common value is r=5 and the final fiber has size4. Their chamber counts are respectively36,960,850,080 and20,401,920. The root's independent phase182_mathieu_fibers.g constructs the actual block designs, verifies the Steiner property over every t-subset, and checks the stabilizer orbits supplying the source's Property(*). That computation is retained; it is not duplicated here.

Their (t−2)-fold derived design is PG(2,4). This is now established by explicit coordinate-incidence maps, described in phase186_witt_group_identifications.md and checked by GAP, independent coefficient arithmetic, and the finite Lean certificate WittDerivedPlanes. The bridge from the original native Witt blocks to each displayed derived incidence table remains checked in GAP and Python. The residue recursion, C.Intersections and the projective base theorem then prove geometry, firmness, residual connectivity and (IP)₂, while the retained fiber computation proves chamber transitivity.

For the rank-six M24 construction, the ordinary-point residue is Γ(S(4,7,23)), with type sizes23,253,8,855,253,23. The residue of an octad block has type sizes8,28,56,280,16: its ordinary subsets have sizes1,2,3; a marked object chooses a four-subset of the octad and one of four alternative octads; and its copied points lie outside the octad. These two type-size multisets prove that the displayed rank-five residues are not isomorphic. The Figure3 subgroup labels are now proved by explicit finite kernels, complements and transported actions in the group-identification note. The object-level identifications with the named earlier Pasini geometries remain source-specific obligations.
