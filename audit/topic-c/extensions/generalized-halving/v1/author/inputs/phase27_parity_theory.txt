# Geometric halving through graph covers and parity-compatible shadows

Working original, 10 October 2026. The construction itself and the bipartiteness/index-two equivalence are established in Piedade–Tranchida, [arXiv:2405.19050v1](https://arxiv.org/abs/2405.19050v1), especially Construction 3.6 and Proposition 4.3. This note gives a single double-cover formulation, an exact condition for its residual connectivity, a finite failure of the broader claim in that inspected version, and a reduction of the geometric halving theorem of Montero–Weiss, [arXiv:2001.11082v1](https://arxiv.org/abs/2001.11082v1), §3. Publication priority is not claimed.

The revised 2025 journal article has not been read in full. The explicit source contradiction below is restricted to the inspected 2024 preprint. The [separate current-version audit](phase27_halving_version_status.md) distinguishes those versions.

## 1. Hypotheses and the missing condition

Let Γ be a finite-rank residually connected incidence **geometry**, with types 0,1,…,n−1 and n≥3. A geometry means that every flag extends to a chamber. Assume:

- **B1:** the vertex-edge truncation on types 0 and 1 is the incidence geometry of a simple graph G.
- **B2:** for an edge e and any higher object x, incidence e*x is equivalent to both endpoints of e being incident with x.

No thinness or transitivity assumption is made here. For a flag F consisting only of higher objects, let G_F be the graph whose vertices and edges are incident with every member of F. Write G_x when F={x}, and G_∅=G. B2 makes G_F exactly the subgraph of G induced on the common vertex shadow. Every G_F is connected and contains an edge, by Lemma 1 below and chamber extension.

The additional condition is:

> **PC.** For every nonempty higher-object flag F, if every G_x, x∈F, is nonbipartite, then G_F is nonbipartite.

The converse is automatic, since G_F is a subgraph of every G_x. Thus PC says that intersecting incident higher shadows introduces no new bipartiteness when none of the individual shadows is bipartite. This condition concerns flags of actual objects, not arbitrary intersections of subsets.

**Theorem.** Assume G is nonbipartite. The partitioned construction below is always a geometry. It is residually connected **if and only if PC holds**. Thinness is preserved in both directions. Every chamber-transitive automorphism group of Γ acts faithfully and chamber-transitively on the constructed geometry.

For bipartite G, choose either component of its bipartite double cover. The same construction gives the established bipartition geometry, and residual connectivity is automatic under the original hypotheses. All shadows are then bipartite, so PC is vacuous.

The automorphism assertion means the natural action of an existing faithful group of automorphisms. It does not identify the full automorphism group for arbitrary nonthin geometries, or assert a converse to chamber transitivity. The regular, thin case is treated in §7.

## 2. Connected truncations, with the needed distinction

**Lemma 1.** Every nonempty truncation of a finite-rank residually connected geometry is connected when it has at least two types.

**Proof.** First prove that the chamber graph is connected, allowing adjacency between distinct chambers differing in one object, by induction on rank. In rank one the chamber graph is complete. In larger rank, all chambers containing a fixed object are connected through chambers containing that object: this is the induction hypothesis applied to its residually connected residue. Given arbitrary chambers, choose objects in them and an incidence path joining those objects. Every incident consecutive pair on that path extends to a chamber. The resulting sequence of chambers can be linked inside the appropriate object residues. This proves chamber connectivity.

Now restrict such a chamber gallery to the desired types. Two successive truncated chambers are identical or share every object but one. If at least two types remain, their complete incidence subgraphs are connected and overlap. Every retained object occurs in a chamber. Consequently the retained incidence graph is connected. The argument applies to every residue as well. ∎

For a higher flag F, its residue contains types 0 and 1. The preceding lemma proves that its vertex-edge incidence graph is connected; B1 and B2 identify this with the incidence graph of G_F. A chamber extending F supplies an edge. Importantly, a two-type truncation is generally **not** a residue. We will use the lemma in the necessity direction of the theorem rather than assume that a disconnected truncation already makes its larger residue disconnected.

## 3. One graph double cover for both constructions

For a connected loopless graph Q, define D(Q) on V(Q)×{0,1} by

    (v,s) ~ (w,1−s)  iff  v~w in Q.

Even walks preserve the second coordinate and odd walks reverse it. It follows directly that D(Q) is connected if Q has an odd cycle, and has exactly two components if Q is bipartite. Each component projects onto all vertices of Q; in the bipartite case each base vertex has exactly one lift in each component.

Choose a connected component C of D(G). In the nonbipartite case C=D(G). Define a new incidence system L_C(Γ):

- Type 0 and type 1 objects are the vertices (v,0) and (v,1) lying in C.
- A higher object is (x,C_x), where C_x is a connected component of D(G_x) contained in C.
- A type-0 vertex and a type-1 vertex are incident exactly when adjacent in D(G).
- A lifted vertex is incident with (x,C_x) exactly when it belongs to C_x.
- Two higher objects (x,C_x),(y,C_y) are incident exactly when x*y in Γ and C_x∩C_y is nonempty.

In the nonbipartite case this is literally Piedade–Tranchida Construction 3.6: identify C_x with its type-0 part P_x, an even-walk class in G_x. Its type-1 part is the complementary parity class, or all vertices when G_x is nonbipartite. Nonempty intersection of components is equivalent to nonempty intersection of their type-0 parts. To see the latter implication when the known common lift has type 1, use a neighbor in the connected graph G_{x,y}; its lifted neighbor has type 0 and lies in both components.

If G is bipartite, each D(G_x) has exactly one component in C, so no higher object is duplicated. The two new vertex types are the two color classes of G. This is Construction 3.1/BP in the same source, attributed there to Percsy–Percsy–Leemans.

## 4. The component-intersection lemma

Let Φ={(x,C_x):x∈F} be a flag consisting only of higher objects. Write

    W_Φ = ⋂_{x∈F} C_x  ⊆ D(G_F).

For F empty, W_Φ=C. For nonempty F:

1. If at least one G_x is bipartite, W_Φ is exactly one connected component of D(G_F).
2. If all G_x are nonbipartite, W_Φ is all of D(G_F).

**Proof.** A nonbipartite constituent imposes no restriction on the lifts of vertices in G_F. Suppose G_x is bipartite. Since G_F is a connected subgraph containing an edge, the restriction of C_x to D(G_F) is precisely one of its two components. If G_y is another bipartite constituent, G_{x,y} is connected. The restrictions of C_x and C_y to D(G_{x,y}) are components. They meet by incidence in Φ, so they are equal. Their restrictions to D(G_F) are therefore equal too. All bipartite constituents select the same component, proving 1. Statement 2 follows because each C_x is then the whole D(G_x). ∎

In particular W_Φ is always nonempty and contains an edge, whether or not PC holds. Its connectedness is equivalent to PC for that flag when all individual shadows are nonbipartite.

This is the exact issue in the inspected preprint's Lemmas 3.11–3.12: the common selected set need not be a **single** even-walk class of G_F. Connectedness of all original shadows does not make that conclusion automatic.

## 5. Geometry and the exact residual-connectivity criterion

### Chamber extension

For a flag of higher objects only, choose an edge (v,0)~(w,1) in W_Φ. The original flag F together with v and the edge {v,w} extends to an original chamber. Every extra higher object in that chamber has a unique lifted component containing (v,0), and it also contains (w,1). These choices give a new chamber extending Φ.

For a flag already containing one lifted vertex, extend the corresponding original flag at that vertex to an original chamber. Its incident edge supplies a neighbor lift, which lies in every prescribed C_x. For a flag containing both lifted vertex types, their incidence gives the unique base edge {v,w}; B2 makes this edge incident with all underlying higher objects. Extend that original flag and lift as before. These cases prove that L_C(Γ) is a geometry without PC.

### Residues containing a lifted vertex

The residue of (v,0) is isomorphic to the original residue Γ_v: replace a type-1 neighbor (w,1) by the unique edge {v,w}, and replace (x,C_x) by x. The component C_x is uniquely determined by containing (v,0). B1 and B2 prove bijectivity and preservation of incidence. The type-1 version is identical, with the two new vertex labels exchanged. Restricting this isomorphism handles every residue whose defining flag contains a lifted vertex. When both lifted vertices occur, the corresponding original flag contains v and {v,w}.

### Sufficiency of PC

Take a defining flag Φ with no lifted vertex. By the component-intersection lemma and PC, its {0,1}-truncation W_Φ is connected. Every other object of its residue belongs to a chamber of that residue, by the geometry result. It is therefore incident with a type-0 object in W_Φ. Thus the entire incidence graph of the residue is connected. Residues whose defining flags contain a lifted vertex are connected by the preceding original-residue isomorphisms. This proves residual connectivity. The same argument applies when global G is bipartite: a constituent already selects a unique component, and the empty defining flag uses the chosen component C.

### Necessity of PC

Suppose PC fails at a higher flag F: every G_x is nonbipartite, but G_F is bipartite. Each higher object then has a unique lift, so they form a flag Φ in the new geometry. Its {0,1}-truncation is all D(G_F), which has two components. If the new geometry were residually connected, Lemma 1 applied to its residue at Φ would make this truncation connected. This contradiction proves necessity. This argument does not incorrectly identify the truncation with the full residue when other types remain. ∎

### Full residue transport under PC

The same description gives the stronger residue isomorphism used in diagram calculations. For a higher flag Φ, its residue is the same component construction applied to Γ_F and the selected component W_Φ of D(G_F).

If G_F is bipartite, every remaining object has exactly one compatible lift into W_Φ. If G_F is nonbipartite, all G_x for x∈F are nonbipartite. For any further higher object y incident with F, PC applied to F∪{y} implies that G_{F,y} is nonbipartite exactly when G_y is nonbipartite. Consequently restricting components from D(G_y) to D(G_{F,y}) is a bijection. Applying the same statement to F∪{y,z} shows that these bijections preserve higher-object incidence. Vertex incidence is immediate. This proves the residue isomorphism, not just connectivity.

PC is inherited in the nonbipartite local case: if all singleton shadows G_{F,y} of a local flag are nonbipartite, then all G_y and all constituents of F are nonbipartite, so global PC forces their total intersection to be nonbipartite. The bipartite local case uses the bipartition construction.

## 6. Thinness, natural group actions and rank-two diagrams

Panels containing both lifted vertex types correspond to original panels with the same omitted higher type. A panel omitting one lifted vertex type corresponds instead to an original panel omitting the **edge** type, at the other endpoint. Original panels omitting the original vertex type already have exactly two objects by B1. These correspondences prove thinness in both directions; no type-preservation error is hidden in the correspondence.

For nonbipartite G, an original chamber (v,{v,w},x₂,…,xₙ₋₁) corresponds bijectively to the lifted chamber with (v,0),(w,1) and the unique components through (v,0). Every original automorphism lifts naturally, acting on vertices and components. This action is faithful: fixing all lifted objects fixes all original vertices and higher objects, and B1 then fixes the edges. The chamber bijection proves preservation of chamber transitivity.

For bipartite G, keep the subgroup preserving the chosen color classes. A chamber-transitive original group has an element exchanging these classes because it can map a chamber at v to the chamber with the other endpoint w of the same edge. The color-preserving subgroup has index two and acts faithfully and transitively on the selected lifted chambers.

Under PC, every rank-two residue is now specified by §5: residues containing one of the two new vertex types duplicate the corresponding original vertex residue; residues of two higher types retain their original models; a residue of types {0,1} is a connected component of D(G_F). In the thin case G_F is a finite polygon graph of length m or a bi-infinite path. In the finite case its cover component is a cycle of length m when m is even and of length 2m when m is odd. Its rank-two geometry therefore has gonality m/2 or m respectively. A bi-infinite path has two isomorphic cover components and retains infinite gonality. This gives the usual halved endpoint order and the duplicated adjacent diagram labels.

This description recovers the actual rank-two residue models, rather than relying on a diagram as a substitute for the geometry. Further classification of arbitrary graph gonalities or exceptional iterated leaf conditions is not claimed here.

## 7. Regular markings and the local parity support family

Suppose now that Γ is a regular leaf hypertope, with distinguished involutions a,b,r_i, where a is the vertex-changing marker and commutes with the rest markers r_i. Continue to assume B1 and B2. For a subset J of the rest labels put

    U_J=<a,b,R_J>,  Q_J=<b,R_J>,  H_J=<b,b^a,R_J>.

The connected vertex graph of the corresponding base residue has vertex set U_J/Q_J. It is bipartite if and only if a∉H_J. This is the local version of the established Proposition 4.3 of Piedade–Tranchida, not a new parity theorem. An elementary proof is as follows. H_J is normal of index at most two, contains Q_J, and U_J=H_J<a>. If it is proper, its two cosets color the vertex graph and a crosses colors. Conversely a bipartite connected graph has a canonical action character on its two colors; Q_J fixes the base vertex and a exchanges adjacent vertices, so its character takes a to1 and all b,r_j to0. It kills H_J and excludes a.

When G is globally nonbipartite, let E be the set of rest labels and

    F = {J⊆E : a∈H_J}.

Then E∈F and F is upward closed. A base higher flag with type set S⊆E has common graph corresponding to U_(E\S), while its singleton graph for type i corresponds to U_(E\{i}). Transitivity reduces all higher flags to base flags. PC is therefore equivalent to

    [E\{i}∈F for every i∈S] ⇒ E\S∈F.

This is equivalent to F being closed under intersections. Indeed let T be the set of labels whose coatom E\{i} belongs to F. PC gives E\T∈F. Every J∈F contains E\T, and upward closure then makes F exactly the family of supersets of E\T. Conversely any such principal family has the displayed property. In the globally bipartite case F is empty and PC is automatic.

Thus the geometric parity compatibility is exactly the support-filter obstruction in [the abstract marking theorem](phase26_halving_core.md), once the original object is an actual regular geometry and B2 is available. B1 supplies its other, parabolic-overlap condition as in source Lemma4.5.

Under PC the constructed geometry is thin, residually connected and chamber-transitive. Its standard adjacent-chamber involutions are b^a,b,r_i: b changes the second lifted endpoint, b^a changes the first, and r_i changes the corresponding higher object. A direct check follows by applying a,b,a to the two endpoints of the base edge; component choices are uniquely fixed by the endpoint retained in the chamber. The group generated by these involutions is the full type-preserving automorphism group, since the chamber graph is connected and an automorphism fixing one chamber of a thin residually connected geometry fixes every chamber. Its standard coset geometry is therefore the constructed geometry.

This gives a precise geometric theorem with an exact extra parity condition. It does **not** prove that every regular leaf hypertope satisfying only B1+B2 automatically satisfies PC; that stronger assertion of source Theorem4.4 remains a separate obligation here. The nonthin counterexample below does not decide that restricted assertion.

## 8. A firm counterexample to the broader inspected preprint claim

Let G_m be the complete four-partite graph with four parts of size m, where m is any positive integer. Use its vertices as type0 and its edges as type1. For each of types2 and3 take the four unions of three parts. Vertex and edge incidence with those higher objects is containment; every type2/type3 pair is incident.

This is a geometry: any higher pair has at least two common parts and hence a common edge; a compatible vertex can be extended to such an edge; all other flags then extend by choosing higher objects containing the relevant edge. B1 and B2 hold literally. Here is a direct all-m proof of residual connectivity. A residue whose defining flag contains an edge is complete multipartite: each remaining vertex or higher type has two possible elements, and all cross-type incidences hold. A residue at a vertex v alone has a complete bipartite graph on its two higher types (three objects each); every incident edge attaches to that graph. At a flag {v,x} with one higher object, the opposite-type copy of the same three-part union x is incident with every remaining edge, so this rank-two residue is connected. With no vertex or edge in the defining flag, the possibilities are the empty flag, one higher object, or two higher objects. Their vertex-edge cores are respectively G_m, K_(m,m,m), and K_(m,m,m) or K_(m,m); all are connected, and every remaining higher object attaches to that core. These cases exhaust every residue of rank at least two.

Every individual higher shadow is K_(m,m,m), which contains triangles. Distinct higher objects intersect in K_(m,m), which is bipartite. Construction3.6 consequently leaves every higher object single, but the new residue at a distinct higher pair is D(K_(m,m)), two disjoint copies of K_(m,m). PC fails exactly as predicted.

The family has 48m² chambers and 162m²+64m+25 flags, including the empty flag. For the latter count, flags with no edge contribute 25+64m: there are25 higher-only flags, and each of4m vertices admits16 choices of its optional two higher objects. Each of6m² edges contributes27 flags through the three choices of its optional vertex and three choices for each optional higher type.

There are72m² panels of size2 (missing the vertex or a higher type), 24m panels of size m (missing the edge with two distinct higher shadows), and12m panels of size2m (missing the edge with equal higher shadows). Equal sizes must be aggregated. The geometry is firm for every m≥2. Exactly12 higher pairs have different underlying three-part unions; their transformed residues have two components of size2m. Every other transformed residue is connected, either by the lifted-vertex residue isomorphism or by its connected doubled vertex-edge core.

The m=1 example has251 flags and48 chambers. The m=2 example has801 flags and192 chambers; every panel has size2 or4, so it is firm as well as residually connected. Its transformed geometry has12 disconnected higher-pair residues, each with two components of size4. Neither starting geometry is thin or flag-transitive; equal-shadow versus distinct-shadow higher pairs already distinguish chamber orbits.

[phase27_parity_shadow_check.py](phase27_parity_shadow_check.py) uses explicit incidence and the Python standard library to enumerate every flag, every chamber extension, every relevant residue graph, and B1/B2 in both examples. It reports original panel sizes and every transformed disconnected residue in [its saved report](phase27_parity_shadow_check.json). The construction is built literally from the singleton parity classes, whose nonbipartiteness is checked by an explicit triangle in each shadow.

This contradicts the residual-connectivity assertion in arXiv:2405.19050v1 Proposition3.13, Theorem3.18 and the introductory TheoremA under their stated general hypotheses. It does not, by itself, contradict the thin regular-hypertope theorem, nor an uninspected revised journal statement. No author-motive inference or publication-priority claim follows.

## 9. Geometric halving reduction for lattice polytopes

Apply the preceding construction to a regular abstract polytope whose face poset is a lattice, reversing types first if halving at the last endpoint as in Montero–Weiss. An edge is the join of its two vertices, so two vertices determine at most one edge and an edge lies in a higher face exactly when both endpoints do. Thus B1 and B2 hold. In a higher flag the faces form a chain, their vertex shadows are nested, and their common graph equals the smallest constituent shadow. PC follows immediately.

Sections5–7 now establish, with no alternating semiregular-polytope construction retained:

- the changed marked group has the full intersection property;
- its actual coset incidence system is flag-transitive;
- that system is a regular hypertope with the changed group as its full type-preserving automorphism group;
- its diagram has the two duplicated adjacent labels and endpoint label m/gcd(m,2) for finite m, with infinite endpoint order remaining infinite.

These are the geometric principal conclusions of Montero–Weiss Theorem3.1, Proposition3.2 and Corollary3.3, with their nondegenerate/lattice hypothesis explicitly retained. The graph-cover construction and the original polytope/hypertope correspondence are established ingredients. The reduction replaces the separate parabolic induction and the external alternating semiregular-polytope flag-transitivity bridge with the component lemma and residue transport.

It does not yet rederive their §4 generalized-cube identifications, exact group orders, selected locally spherical examples or hyperbolic-type claims. It does not rederive the Piedade–Tranchida cubic-toroid classification, iterated B1/B2 criteria, or full automorphism groups of arbitrary nonthin geometries. Those are distinct principal/application obligations and receive no completion credit in this note.
