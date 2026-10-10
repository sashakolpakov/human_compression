## 23. Set-valued Petrials: the exact kernel and thin-case recovery

The operation in this section is that of Bonheure–Buekenhout–Leemans (2001), with equal geometric Petrie sets identified. Its principal theorem and valid numbered structural conclusions are the targets. The unconditional embedding assertion is corrected below. No source conclusion is used as a hypothesis, and neither a finite group nor finite residues are assumed.

Let Γ be a thin regular residually connected rank-three geometry. Label its types vertex, edge and face. At a base chamber C=(v,e,f), let a change the face, b the edge and c the vertex. Lemma O0 gives

\[
 G=\operatorname{Aut}(\Gamma)=\langle a,b,c\rangle,
 \quad G_v=\langle a,b\rangle,\quad G_e=\langle a,c\rangle,
 \quad G_f=\langle b,c\rangle,\quad G_v\cap G_e=\langle a\rangle.
 \tag{P1}
\]

The other two pair intersections are respectively ⟨b⟩ and ⟨c⟩, and the chamber stabilizer is trivial. Any two of a,b,c generate a dihedral group, possibly infinite: a word in two involutions alternates after cancellation and is a power of their product or such a power times one involution. For distinct nonidentity involutions x,y, the intersection ⟨xy⟩∩⟨x⟩ is trivial. Otherwise x is a power of xy and commutes with it, forcing xy=yx and |xy|=2; then x=xy would force y=1. This proves the rotation/reflection fact used below without a finiteness assumption.

### 23.1. Geometric operation and its faithful image

Put w=cab. Starting at a chamber, change vertex, face, then edge; at the base chamber the result is wC. At gC, successive chamber flips act by right multiplication on g, so iteration gives gw^iC. The Petrie face at C is the actual ordered pair

\[
 P(C)=\left(\{w^iv:i\in\mathbb Z\},\{w^ie:i\in\mathbb Z\}\right).
 \tag{P2}
\]

Equal pairs are one face; the vertex–edge incidence induced on these sets is understood. Define ΠΓ by retaining old vertices, edges and their incidence, and adjoining these distinct faces, with incidence to a face given by membership. This is equivariant: P(gC)=gP(C). In particular wP(C)=P(C), and

\[
 wv=cv,\qquad w^{-1}e=be.
 \tag{P3}
\]

Thus a Petrie face contains v and cv at e, and e and be at v. Each pair is distinct because the corresponding old panel change is nontrivial.

**Lemma P1 (connectivity and exact action).** ΠΓ is a residually connected geometry. Its natural automorphism action ρ has kernel

\[
 \ker\rho=\operatorname{core}_G\langle a\rangle
 =\begin{cases}\langle a\rangle,&a\in Z(G),\\1,&a\notin Z(G).\end{cases}
 \tag{P4}
\]

*Proof.* Every incident old vertex–edge pair extends through an old chamber to its Petrie face. For an object belonging to a Petrie face, a step of the defining walk supplies an incident object of the other retained type. These facts extend every flag to a chamber.

Write v_i=w^iv and e_i=w^ie. Equation (P3) says that e_i joins v_i and v_(i+1). The walk therefore connects every object in its face residue; additional induced incidences preserve connectivity. In the old residue at v, replace every two-step path e₁–f–e₂ with distinct edges by e₁–P(v,e₁,f)–e₂. Thinness and (P3) justify the replacement. It connects all retained edges in the new vertex residue, and every new incident face meets one of them. The analogous replacement v₁–f–v₂ proves connectivity of each edge residue. Finally an old path through a face can be replaced by a path in its connected vertex–edge residue. Thus the old vertex–edge truncation, and consequently the new geometry with every face attached, is connected.

For the action apply K(c) with X the disjoint union of old vertices and edges. They are retained in Y, and every new face is uniquely encoded by its two actual subsets of X. Equations (Kc2) and (P1) give the core in (P4). A normal subgroup of ⟨a⟩ is either trivial or all of ⟨a⟩. The latter is normal in G exactly when its unique nonidentity element a is central. This proves the exact formula and constructs the faithful image G/kerρ. ∎

This application uses the same core identity as N008's faithful coset action. It keeps the action kernel that a set-valued construction may lose. It asserts neither chamber transitivity of ΠΓ nor injectivity of ρ without further proof.

For an ordinary map, the three successive changes move across an edge to its other endpoint, change the incident face, and continue along that face. These are exactly the alternating corner choices in the conventional Petrie walk. This proves the walk-definition assertion of source Lemma 3.1; it does not forbid repetitions or replace geometric faces by labelled walks.

### 23.2. The thin obstruction and all conditional conclusions

**Theorem P2 (Petrial obstruction and recovery).** If ΠΓ is thin, then |ab|=2 or |ac|=2. The action ρ is faithful and regular and is the full automorphism group of ΠΓ. Applying Π again recovers Γ by an isomorphism fixing all retained vertices and edges.

*Proof.* Set P=P(C). Suppose first that bP≠P. Both P and bP contain e and be at v, so the vertex residue of ΠΓ contains the four-cycle e–P–be–bP–e. A finite cycle in a connected graph of degree two is the entire graph: its vertices already have their two neighbours, so no path can leave it. Lemma P1 therefore says that precisely two old edges are incident with v. In the old thin connected vertex residue both edges have degree two, and each incident face meets both. It is also a four-cycle. Its regular dihedral group ⟨a,b⟩ has four chambers, so |ab|=2.

Suppose instead that bP=P. Since w fixes P, ca=wb fixes P and e. By Lemma O0, the automorphism group of the thin ΠΓ acts freely on chambers. Its edge–face panel stabilizer embeds in the permutation group on that panel's two completions, so ρ(ca)^2=1. Equation (P4) puts (ca)^2 in ⟨a⟩. The rotation/reflection intersection in ⟨a,c⟩ is trivial, hence (ca)^2=1. Since c≠a, this gives |ac|=2. This proves the obstruction without presuming that b always fixes P or that the new action is regular.

Interchanging vertex and edge interchanges b,c and changes cab to bac=w^(-1), preserving the same Petrie sets after that type interchange. We may consequently assume [a,c]=1. Then bwb=w^(-1), bv=v and be=w^(-1)e, so bP=P. The subgroup ⟨b,w⟩=⟨b,ca⟩ is transitive on the incident vertex–edge pairs of P: its elements give (v_i,e_i) and (v_i,e_(i−1)) for every i. These are distinct pairs, and thinness makes them all pairs at v_i. Every object of P occurs in the walk. The original chamber-transitive G is transitive on the faces P(gC), so its induced action on ΠΓ is chamber-transitive. K(c) identifies its image with the full regular automorphism group. The preimage of the new panel stabilizing (v,e) is exactly G_v∩G_e=⟨a⟩. Equation (Kc3) forces kerρ=1.

At (v,e,P), the new panel involutions are therefore a,b,ca: the last fixes (e,P) and sends v to cv; b fixes (v,P) and changes e; a exchanges the two faces at (v,e). The new generators generate the same group since c=(ca)a. Their geometric marking is established by this action, not by assuming a homomorphism from the old marking. Their second Petrie step is (ca)ab=cb. The cb-orbits of v and e exhaust exactly the old face's vertex–edge shadow: use the alternating normal form in its residue group ⟨b,c⟩ from (P1).

Those old face shadows are distinct. Otherwise let f≠f′ have the same shadow and choose (v,e) in it, moving the base chamber if needed. Thinness gives f′=af. Both f,f′ meet e and be at v. Their four-cycle exhausts the old vertex residue, as above, forcing [a,b]=1. Together with [a,c]=1 this makes a central in G, and (P4) contradicts kerρ=1. Thus old faces correspond bijectively to the second Petrie faces, with precisely their original incidences. This proves the required isomorphism. The vertex–edge-swapped case gives the same conclusion. ∎

The commuting pair is the source's linear-diagram conclusion. Theorem P2 proves its Theorem 1 and the thin-only formulation in its abstract, together with Lemma 3.2(iii),(iv). Lemma P1 gives Lemma 3.2(i). No finite-residue assumption occurs in the walk, connected-cycle, dihedral or gallery arguments.

### 23.3. Corrected assertions and exact controls

The unconditional Lemma 3.2(ii) must be read as the natural homomorphism with kernel (P4), not as an embedding. Indeed take the complete tripartite geometry with two objects of each type. Its full type-preserving group is C₂³, regularly permuting eight chambers. Let a,b,c independently change the face, edge and vertex coordinates. The element cab changes all three, so every Petrie face consists of both vertices and both edges. Deduplication leaves one face. Thus ΠΓ is the complete tripartite geometry with type sizes (2,2,1), its full group is C₂², and the kernel is ⟨a⟩. An order-eight group cannot embed in this order-four automorphism group. This also gives a commuting-pair diagram with nonthin Petrial, so the principal implication has no converse in this diagram convention.

The unnumbered geometric length/order equality also cannot be unconditional. Take C₂×S₃, with a generating its central C₂ and b,c distinct transpositions generating S₃. The coset geometry with stabilizers in (P1) is a six-cycle on three vertices and three edges, joined to two faces. It is thin, residually connected and regular: its twelve chambers form the regular C₂×S₃ action. On retained objects, cab acts as cb, a rotation of order three, while cab itself has order six. Its geometric Petrie face has three vertices and three edges, not length six. This assertion is unnecessary for every proof above.

The optional finite controls construct these examples, a tetrahedron and its vertex–edge interchange, a nonlinear star-transposition S₄ geometry, and two cube markings from explicit permutations. They use the literal chamber changes and deduplicate vertex–edge sets; no changed-marking or faithfulness conclusion is assumed. Their full standard-library program is charged in Appendix E. The two counterexamples above are proved directly, and the infinite theorems do not follow from finite sampling. No source atlas classification, external map-classification theorem, new open-conjecture solution, priority claim or complete Lean certificate is asserted.
