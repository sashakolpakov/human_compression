# The retained-object interface for halving and Petrials

Author planning lemma, 10 October 2026. This is a bounded mathematical attachment for the proposed module *Halving and Petrial operations on regular geometries*. It is not a completed module or an independent admission. It uses the exact theorem U.Action in the frozen third edition of *Marked groups, kernels and intersections*. No earlier file is altered.

## 1. Graph halving detects the original action

Let Γ be a finite-rank incidence geometry of rank at least three, with designated vertex and edge types. Suppose its vertex–edge truncation Q is a connected simple graph, every edge has its two endpoints, and the nonempty vertex–edge shadow Q_x of every object x of higher type is connected. Assume the graph-halving incidence construction has been defined as follows. Write D(Q) for the bipartite double cover, with vertices (v,ε), ε∈{0,1}, and edges between (v,0) and (w,1) when {v,w} is an edge of Q. Choose one connected component C of D(Q). The new object set Y consists of its vertices, separated into types by ε, and the objects (x,C_x), where C_x is a connected component of D(Q_x) contained in C. The usual halving incidence is preserved by the induced action described below.

Let G≤Aut_type(Γ), and let K be the subgroup whose induced action preserves C. Put X equal to the disjoint union of the old vertices and all old objects of higher type. The projection

\[
(v,\varepsilon)\longmapsto v,\qquad (x,C_x)\longmapsto x
\]

is a K-equivariant surjection Y→X. Indeed, if Q is nonbipartite, D(Q) is connected, so C=D(Q). Every old vertex has both lifts in C, and every Q_x has a component in C. If Q is bipartite, each component of D(Q) contains exactly one lift of each old vertex. Since Q_x is connected, its intersection with C is exactly one of the two components of D(Q_x). Thus every old higher object also has a lift. The parity-of-walk argument proving these assertions works for infinite connected graphs as well.

The object (v,ε) is encoded by the fixed type tag ε and v. Encode (x,C_x) by its old type, x and the two subsets

\[
V_\varepsilon(C_x)=\{v:(v,\varepsilon)\in C_x\}\subseteq X
\qquad(\varepsilon=0,1).
\]

This is an injective equivariant encoding of Y by tagged finite tuples of elements and subsets of X. A component is determined by its vertex set, and the old object x is retained in the encoding even when different objects have equal shadows. All hypotheses of U.Action are therefore discharged, and

\[
\ker(K\curvearrowright Y)=\ker(K\curvearrowright X)=1.
\tag{C.A1}
\]

For the last equality, an element fixing X fixes every old vertex and higher object. Simplicity of Q makes an old edge uniquely determined by its two endpoints, so that element also fixes every edge and hence every object of Γ. As K is a subgroup of its automorphism group, the element is the identity.

This proves faithfulness only. It does not prove that Y with the proposed incidence is a geometry, residually connected, thin or chamber-transitive. Those conclusions still require the graph-halving proof, including its shadow compatibility condition. Once that proof gives a thin residually connected geometry and chamber transitivity of K, U.Geometry identifies K with the full type-preserving group. Under old chamber transitivity, K=G for nonbipartite Q; for bipartite Q, the old panel move interchanging the endpoints of an edge exchanges colors, so K has index two in G. The index assertion is not needed to establish (C.A1).

## 2. A Petrial retains a smaller faithful quotient

Let Γ be a thin regular residually connected rank-three geometry with base chamber (v,e,f). Let a change the face, b the edge and c the vertex. The standard gallery argument gives

\[
G=\langle a,b,c\rangle,
\quad G_v=\langle a,b\rangle,
\quad G_e=\langle a,c\rangle,
\quad G_v\cap G_e=\langle a\rangle.
\]

Take X to be the disjoint union of its vertices and edges. A geometric Petrie face is the actual pair of subsets obtained by the walk w=cab; equal pairs are identified. The new geometry retains X, and every new face is encoded by its two subsets of X. Thus U.Action applies with Y₀=X and projection the identity, giving

\[
\ker(G\curvearrowright\Pi\Gamma)
=\operatorname{core}_G\langle a\rangle
=\begin{cases}
\langle a\rangle,&a\in Z(G),\\
1,&a\notin Z(G).
\end{cases}
\tag{C.A2}
\]

The last equality uses only that a is a nonidentity involution: its order-two subgroup is normal precisely when a is central. The operation therefore supplies the faithful image G/core_G⟨a⟩, not an unconditional embedding of G.

The existing thin-Petrial proof must still show that the induced action is chamber-transitive and that the preimage of its vertex–edge panel stabilizer is ⟨a⟩. U.Action then gives [⟨a⟩:ker]=2 and hence a trivial kernel. Establishing those premises requires the two-case thin-residue obstruction and the actual new panel marking; they are not consequences of the kernel formula alone. No finite-group assumption is involved.

## 3. The exact common use and its limit

Equations (C.A1) and (C.A2) use the same theorem with two verified encodings. In graph halving, the retained vertices and higher objects reconstruct the omitted edges. In a geometric Petrial, omitted faces need not be reconstructible from the retained vertex–edge sets, so their pointwise kernel must be kept. This explains the differing faithfulness conclusions without changing the definition of either operation.

Neither use constructs a homomorphism carrying the old distinguished generator list to the changed one. In particular, U.Compare, U.K and U.SK cannot be substituted for the endpoint overlap/support proof or the Petrial thinness proof without additional, presently absent hypotheses. The proposed module will cite U.Action and U.Geometry once per verified application and retain the separate operation-specific arguments in full.

Attribution: U.Action reproduces the elementary retained-object/core argument already proved in the repository's reviewed Petrial integration. The graph-halving construction and parity interpretation follow the previously attributed geometric halving literature; the explicit attachment above reorganizes their faithfulness proof. This planning note makes no historical novelty, conjecture-resolution, complete Lean or length claim.
