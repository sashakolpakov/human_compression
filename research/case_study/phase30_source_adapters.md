# Nested shadows, generalized cubes, and two complete halved presentations

Private source-bound extension, 10 October 2026. This note applies the already reviewed [graph-cover recognition theorem](phase28_voltage_shadow_theory.md). It does not claim that the constructions, covering-space facts, or endpoint halving are new. The new scope of this package is the arbitrary-cover nested-shadow corollary, the explicit generalized-cube applications in N013 §4, and complete presentations for F015 Propositions 11 and 13. N013 §3 was already recovered in [phase27 §9](phase27_parity_theory.md) and receives no additional coverage credit here.

## 1. Primary sources and the bounded access result

**L111.** C. Lefèvre-Percsy, N. Percsy and D. Leemans, *New geometries for finite groups and polytopes*, Bull. Belg. Math. Soc. Simon Stevin **7** (2000), 583–610, DOI [10.36045/bbms/1103055618](https://doi.org/10.36045/bbms/1103055618). The original complete body remains unavailable in this audit. ResearchGate exposes authored indexed excerpts but direct retrieval returned 429; a new publisher full-page route did not retrieve the body. Exact-title searches found no new accessible author-hosted copy. The indexed passages identify two constructions and applications, but are not sufficient to certify all hypotheses or proofs. No L111 theorem is claimed recovered. Earlier phase26 access limitations remain valid.

**N013.** A. Montero and A. Ivić Weiss, *Locally Spherical Hypertopes from Generalised Cubes*, [arXiv:2001.11082v1](https://arxiv.org/abs/2001.11082v1), 29 January 2020, §4, printed pp. 8–10. The cached primary manuscript was read through all of §4. The targets are its unnumbered Danzer-family applications, including the rank-four and rank-five hyperbolic examples. The later journal version is not substituted for this manuscript's numbering.

**F015.** C. A. Piedade, *Infinite Families of Hypertopes from Centrally Symmetric Polytopes*, [EJC 30(2) (2023), P2.20](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v30i2p20/pdf/), §§2.2–2.4 and 3.1–3.2. The exact targets are Propositions 11 and 13, including their defining presentations, regularity and group orders. The underlying extension results quoted as Theorem 5, Lemma 7, and Corollaries 9 and 12 remain explicit inputs.

The source summaries above specify scope; all arguments below are written independently. This is not a whole-paper reduction of L111 or F015, and no current-open/priority claim is made.

## 2. The arbitrary-cover consequence of nested shadows

Let Γ be a finite-rank residually connected geometry satisfying B1/B2 of phase28. Suppose every nonempty higher flag F has a member x₀ such that its common vertex-edge shadow equals Xₓ₀ and Xₓ₀ is contained in every Xₓ, x∈F. For example, this holds for the incidence geometry of a lattice polytope: a higher flag is a chain and its smallest face supplies the common shadow.

For **every connected regular graph cover** Y→X, the phase28 conditions H and M hold. Indeed, at a common base vertex, Hₓ₀≤Hₓ for all x∈F and H_F=Hₓ₀. This proves M. Given pairwise-intersecting cosets gₓHₓ, the coset belonging to x₀ meets each other one and is contained in it: after choosing a point of intersection, this is the elementary inclusion of cosets of nested subgroups. Its entire coset therefore lies in the total intersection, proving H. The empty flag uses connectedness of Y.

Consequently the graph-incidence lift is a residually connected geometry; it is thin whenever Γ is thin. If Y is bipartite, its compression is also a thin residually connected geometry. This statement permits nonabelian deck groups and infinite covers, exactly as in phase28. Transitivity still requires liftability of the chosen base action. It does not follow from connectedness alone.

For a lattice polytope, B1/B2 follow directly from joins. An edge is the join of its two vertices: there cannot be two edges with those same endpoints, and any face containing both endpoints contains their join. Thus its graph is simple and its face shadows are induced graphs. The arbitrary-cover statement does not assert preservation of the face-lattice property. The finite diagnostic below includes a tetrahedral cover with two lifted faces having a disconnected intersection, so this distinction is substantive.

In the identity-cover case of a bipartite graph all subgroups are trivial. The compression simply makes the two vertex colors into two types and retains the higher faces. A regular action on the original polytope restricts to its index-two color-preserving subgroup, which acts regularly on the compressed chambers. Each compressed chamber corresponds to the unique original chamber whose vertex has the selected first color. The full type-preserving automorphism group is this subgroup: a thin residually connected geometry has trivial chamber stabilizers, by propagation along chamber galleries.

## 3. Generalized cubes: an exact coordinate reduction of N013 §4

Let K be a finite regular lattice polytope with m vertices, and put P=2^K in Danzer's construction. Retain the standard Danzer fact that this face construction is a regular lattice polytope with group

    G = F₂^m ⋊ Aut(K).

Vertices are binary vectors, and its graph is the m-cube. An i-face, i≥1, is a coordinate subcube F(x), where F is an (i−1)-face of K and the freely varying coordinates are the vertices of F. These descriptions make the graph parity and all face shadows explicit. The identity-cover result in §2 gives a regular hypertope Δ with

    Aut_I(Δ) = E_m ⋊ Aut(K),
    E_m = {x∈F₂^m : Σ x_i=0},
    |Aut_I(Δ)| = 2^(m−1)|Aut(K)|.                         (1)

Here the natural permutations of the coordinates preserve parity. To identify the actual halving marking, write a for the flip at the base vertex of K and b, r₂,… for its standard polytope generators. The compressed marking is

    (aba, b, r₂,…).

The element aba·b flips the two endpoints of the base edge of K. Conjugating by Aut(K) gives all its edge vectors. Since the graph of K is connected, its edge vectors span E_m: along a path, their sum is the vector at its two endpoints. Hence the displayed marking generates exactly the group in (1), not an unidentified subgroup of the correct order.

The source uses the dual convention P̂=(2^(K*))* and halves the final endpoint. Apply the preceding statement to K* and reverse types. Thus m in the source is the number of facets of K. No change of source convention or new assumption is hidden in (1).

### Polygon inputs

For K a p-gon, p≥3, Δ becomes a regular self-dual map of type {p,p} after ordering its types as (color 0, old face, color 1). Its counts are

    V = F = 2^(p−1),     E = p·2^(p−2),     |Aut| = p·2^p.

These follow by counting coordinate subcubes: each polygon edge gives 2^(p−2) squares of P. The original coordinate flip a interchanges the new vertex colors and conjugates the two fork generators, furnishing the duality. The map is orientable: the reflection-sign character of D_p, extended trivially across E_m, takes each distinguished generator to −1. The standard flag-orientation criterion then applies. Euler's formula gives

    genus = 1 + 2^(p−3)(p−4).                            (2)

In particular p=3 gives the tetrahedron and p=4 gives the square toroidal case. Identification of that torus with the conventional lattice label {4,4}_(2,2) is the standard square-grid identification, rather than a consequence of the order alone.

### Locally spherical inputs and the two hyperbolic examples

For the source's K of type {p,3,…,3}, use its dual L=K* in the coordinate construction. The relevant L are the simplex, cross-polytope, icosahedron and 600-cell. Every proper face of these L is a simplex.

Residues at either new vertex type are L. At an old j-face of 2^L, j≥2, write F for its corresponding (j−1)-face of L. The lower and upper sections are independent: the residue is the product of the compressed cube 2^F with the section L/F. Since F is a simplex on j vertices, the first factor has the standard even-sign permutation group E_j⋊S_j and the D_j Coxeter marking. Its order 2^(j−1)j! equals the order of the finite D_j Coxeter group, so this is the universal spherical D_j geometry, with D₂=A₁×A₁ and D₃=A₃. The second factor is a spherical section of the convex regular L. This gives the **actual** spherical maximal residues, not merely a finite-looking diagram. Thus all these examples are locally spherical.

Their diagrams are the fork diagrams obtained by duplicating the first node adjacent to the initial label 3 of L. The standard finite/affine/compact-hyperbolic Coxeter diagram classifications identify respectively D_(r+1), affine B_r, and the rank-four/rank-five hyperbolic forks, where r=rank L. This diagram classification remains a named input; it is not proved by group orders.

The source's two exceptional finite examples now have the exact groups and orders

    K=dodecahedron: E_12 ⋊ Aut(K),   2^11·120 = 245760;
    K=120-cell:    E_120 ⋊ Aut(K),  2^119·14400.          (3)

Here E_m denotes the even subspace of F₂^m, of dimension m−1. The other source rows follow uniformly from m=r+1 and |Aut(simplex)|=(r+1)!, or m=2r and |Aut(cube)|=2^r r!.

The restrictions on the locally spherical inputs also have a short diagram proof. A new vertex residue is L itself, so L must be universal spherical. Retain the classical list of finite string Coxeter groups. If the output rank is at least four, its proper three-node fork [q,q], with q the first label of L, is spherical only for q=3 (all labels are at least three in a lattice polytope). At output rank five, the remaining finite-list candidate F₄={3,4,3} is excluded because its proper four-node fork is affine, not spherical. The finite list now leaves exactly the simplex/cross-polytope and the icosahedral/600-cell cases just described. At output ranks at least six only the first two remain. This is a reduction relative to the classical finite Coxeter list, not a new classification of finite Coxeter groups or arbitrary regular polytopes. Conventional toroidal lattice labels in §4 are retained rather than inferred from their orders.

## 4. A complete index-two presentation lemma

This is elementary Reidemeister–Schreier rewriting, with both Schreier conjugates retained until shown redundant. Suppose an old presentation has involution generators a,b,c₂,…,c_r, relations [a,c_i]=1, (ab)^4=1, the remaining string Coxeter relations, and additional relators of the form

    (a w)^2e=1,       w a word in b,c₂,…,c_r.             (4)

All defining relators have even a-parity. The parity kernel has generators d=aba, b,c₂,…,c_r. Its Coxeter part is the fork obtained from the original string by replacing a with d: d and b commute; the d–c₂ order equals the b–c₂ order; d commutes with c_i for i≥3. No extra relation is omitted: apply the transversal {1,a}; a² removes its associated Schreier generator, and the conjugates of each old relation produce exactly these fork relations.

Let θ replace every b in a word by d and fix the c_i. Then a w a=θ(w), and

    (a w)^2 = θ(w)w =: R_w.

Relation (4) contributes R_w^e=1. Its a-conjugate is redundant because

    a R_w a = w θ(w) = w R_w w^−1.                     (5)

Therefore the fork Coxeter presentation plus precisely the relations R_w^e gives the whole parity kernel. This is a presentation theorem, not only a verification that particular words vanish in the known finite group. The same proof works with several relations (4), and with no finiteness assumption.

## 5. F015 Proposition 11: the full polygon-family statement

Retain the original matching-dihedral extension, as stated in F015 Corollary 9 and Proposition 10: for integers p,s≥2 it is a regular lattice polytope with

    G = D_s^p ⋊ D_(2p),       |G|=(2s)^p·4p,

where D_t has order 2t. Its marked presentation has type {4,2p} and extra relators

    [a b(cb)^(j−1)]^4=1  (2≤j≤p−1),
    [a b(cb)^(p−1)]^(2s)=1.                             (6)

The a-parity character is surjective. On the matching Coxeter group it is total reflection parity and on the old polytope group it is trivial. The vertex graph, a Cayley graph of D_s^p in its standard reflection generators, is therefore bipartite. Its identity-cover compression is a regular hypertope with full group the parity kernel; in rank three the fork is a string after reordering, hence a regular map of type {2p,2p}. Its order is (2s)^p·2p.

Apply §4 to w=b(cb)^(j−1). The exact rewritten word is

    R_j=(dc)^(j−1) d b(cb)^(j−1).

Thus the full defining presentation is the Coxeter group [2p,2p] on the reordered generators d,c,b, with

    R_j²=1 (2≤j≤p−1),       R_p^s=1.                  (7)

These are precisely Proposition 11's extra relations. Their sufficiency follows from (5); no unchecked omitted conjugate relation is required. For p=2 the familiar square-grid lattice gives {4,4}_(s,s), as in the source. The original extension theorem and that lattice notation remain inputs; all new halved presentation, regularity and order assertions follow above.

## 6. F015 Proposition 13: the full orthoplex-family statement

Retain Corollary 12: for n≥3 and integer s≥2, the original extension is the cubical regular toroid {4,3^(n−2),4}_(2s,0,…,0), with group order (4s)^n n! and presentation consisting of that string Coxeter group and

    [a b c₂···c_(n−1)c_n c_(n−1)···c₂ b]^(2s)=1.     (8)

Its matching-dihedral model is D_s^n⋊Aut(n-orthoplex); total reflection parity again proves bipartiteness. Hence compression gives a regular hypertope with full group order

    (4s)^n n!/2 = (4s)^(n−1)(2s)n!.

The fork diagram is Proposition 13's affine B_n diagram. In §4 take w=b c₂···c_n···c₂ b. Write t=c₂···c_n···c₂. Since θ changes only the two endpoint b's, θ(w)w=dtdbtb; using db=bd gives

    R_w = [d c₂···c_n···c₂ b]².

Consequently the complete extra defining relation of the parity kernel is

    [d c₂···c_n···c₂ b]^(2s)=1,                        (9)

exactly the source's relation. This proves completeness of its presentation and all its group/geometry assertions from the retained original toroid. More explicitly, in the original affine Coxeter group the word aw is a coordinate translation. The translation lattice of the stated toroid is generated by conjugates of (aw)^(2s); each has even a-parity. The entire lattice therefore lies in the parity kernel. The halved group is the affine fork reflection group modulo this same translation lattice, so it is a toroidal hypertope. The source's lattice name fixes the original geometric realization. Merely having the displayed finite order would not prove this assertion.

## 7. Scope and executable checks

The uniform proofs above do not depend on finite tests. The [coordinate checker](phase30_source_geometry_check.py) checks the four polygon inputs p=3,4,5,6, the rank-four cube compression, and nontrivial C₃ covers of the tetrahedron and tesseract (the latter also compressed). Its [report](phase30_source_geometry_check.json) records 10,580 flags, 3,060 residues of rank at least two, and 4,896 thin panels, all checked directly. The rank-four cover includes 132 incident higher-component pairs, all verified nested. The tetrahedral cover has two face shadows meeting in three disjoint edges, an exact control showing that the face-lattice property need not survive.

The [raw-presentation GAP checker](phase30_source_presentations_check.g) uses the complete displayed presentations in (7)/(9), establishes their actual orders, and then checks every marked subgroup intersection. The [log](phase30_source_presentations_check.log) and [report](phase30_source_presentations_check.json) give orders 64,144,384,1296 for (p,s)=(2,2),(2,3),(3,2),(3,3), and orders 1536,5184 for (n,s)=(3,2),(3,3). All 768 subgroup meets pass. These checks are finite diagnostics, not the uniform presentation proof.

No new paper-level credit is asserted here. N013's already recovered §3 is not counted again. This note adds its explicit §4 family derivations with retained Coxeter classifications/lattice labels, and complete selected principal propositions of F015. L111 remains an access gap. Arbitrary cover classification, automatic liftability, preservation of face lattices, and the remaining F015 presentations are outside scope.

## 8. Literal N013 numbered-statement and principal-application ledger

This ledger distinguishes principal-result coverage from a claim that every sentence or attribution in the manuscript has been proved anew.

| Source target | Status and exact boundary |
| --- | --- |
| Proposition 2.1, Tits coset construction | Quoted background retained. The coset incidence definition and rank≤2 flag transitivity are also established directly in the workspace torsor notes; no separate theorem credit. |
| Theorem 2.2, C-group plus flag transitivity ⇒ regular hypertope | Quoted background retained; our geometric proof establishes geometry/thinness/RC directly. |
| Proposition 2.3, maximal-parabolic IP criterion | Quoted background retained; not needed by the phase27 geometric replacement. |
| Lemma 2.4, direct products of C-groups | Recovered by the one-line product-intersection calculation below. |
| Theorem 3.1 | Already recovered in phase27 §9: all nondegenerate regular polytopes, not only the examples of the current note. |
| Proposition 3.2 | Already recovered in phase27 §9: full flag transitivity of the resulting coset geometry, not merely generation or subgroup IP. |
| Corollary 3.3 | Already recovered in phase27 §9: regular hypertope and full type-preserving group. |
| Remark 4.1, Pellicer extensions | The quoted construction of P_s is retained, not rederived. The blanket non-local-sphericity sentence needs a rank qualification; see below. |
| §4, generalized-cube group and size | §3, equation (1), retaining the original Danzer polytope construction. |
| §4, polygon counts, self-duality and genus | §3, equation (2), with the classical square-torus label retained. |
| §4, spherical/Euclidean/hyperbolic families in ranks 4 and 5 | §3: explicit groups, actual maximal residues, diagrams, and equation (3); classical Coxeter recognition retained. |
| §4, all-rank simplex/cube families and restriction for ranks≥6 | §3, relative to the finite string Coxeter classification; standard toroidal lattice names retained. |
| Comparison with examples in reference [9] | Not independently checked. No novelty or uniqueness relative to that list is claimed. |
| End of §3, identification of the auxiliary semiregular S(P) with P | Not a new target here; the source's Monson–Schulte input/identification is retained. It is unnecessary to the replacement proof. |

For Lemma 2.4, a marked subgroup in G×H is G_S×H_T. Hence

    (G_S×H_T) ∩ (G_U×H_V)
      = (G_S∩G_U) × (H_T∩H_V)
      = G_(S∩U) × H_(T∩V),

which is the required full IP, with the two disjoint marking alphabets understood.

For the precise boundary in Remark 4.1, assume its stated extension is a nondegenerate regular P_s to which the halving theorem applies, with finite Schläfli entries and n≥3. At rank three, the halved geometry has only finite dihedral rank-two proper residues; it is therefore locally spherical under the manuscript's own definition, even for s≥3. At rank n≥4, the proper three-node fork has labels (p,p,s) with p,s≥3 and is not a finite Coxeter diagram, since 2/p+1/s≤1. Thus the intended non-local-sphericity conclusion does follow in those ranks. We record this rank distinction without claiming a new correction or independently rederiving Pellicer's extension theorem. It is one reason to avoid a literal whole-document truth claim.
