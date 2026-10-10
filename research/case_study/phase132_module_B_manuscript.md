# Module B: Forest coordinates and primitive coset geometries

## Abstract

We describe a common coordinate construction for several families of flag-transitive incidence geometries. A positively weighted tree determines symmetric groups on its forest components and a laminar family of set stabilizers. Unique paths compute all subgroup intersections, while a single atom-matching argument completes every flag. Unit weights recover the inductively minimal geometries; contraction of a distinguished edge gives the sign-kernel family of maximum-rank symmetric-group geometries; and equal leaf weights on a star give the geometries defined by disjoint subsets and Kneser graphs. We determine their primitive properties, establish the extremal marking correspondence, and compute the parameters and full graph automorphisms of the star family. The relative-generation and Frattini theorems of *Marked groups, kernels and intersections* then give a second coordinate description: every firm residually weakly primitive geometry of a finite p-group is a direct sum of rank-one coordinate geometries. The source statements are recovered with their retained classification inputs and with explicit corrections to the unrestricted infinite Frattini assertion and to three boundary or parameter assertions in the Kneser construction.

## Introduction

The same incidence geometry can be described by subsets, by cosets of stabilizers, or by generators whose omission subgroups are those stabilizers. Each description makes a different part of the structure visible. Subsets make flags concrete; cosets connect the action to subgroup intervals; marked generators reveal the intersection property. The purpose of this paper is to pass between these descriptions through two coordinate systems, rather than to prove their common ingredients anew in every application.

The first coordinate system is a weighted tree. Its edges give cuts of a finite set, and deleting several edges gives a partition. The symmetric groups preserving these partitions have exactly the intersections dictated by the forest. The cuts are laminar, so pairwise compatible subset images have compatible atoms and hence a common permutation representative. Theorem B.F supplies both the subgroup calculation and the geometric flag argument. This distinction matters: a subgroup intersection property alone does not imply that arbitrary pairwise incident cosets have a common point.

Three constructions enter this framework. The unit-weight case supplies the property tests for the inductively minimal geometries studied by Buekenhout and Cara [BC98]. A sign kernel and the contraction of one edge supply the second marking family in Cameron and Cara's maximum-rank classification [CC02]. A weighted star gives, literally, the disjoint-subset geometries studied by Garcia-Colin and Leemans [GL21]. The star specialization shares the entire existence and residue argument with the older forest constructions. Its distance and automorphism assertions require further arguments, which are included here.

The second coordinate system is a quotient vector space. Archer, Cara and Krempa [ACK05] showed that the Frattini subgroup is invisible to firm residually weakly primitive geometries, and used this to classify such geometries for finite p-groups. The general relative-generation, normal-subgroup ladder and coset-transport arguments appear once in the companion paper [U]. Here we verify their geometric hypotheses and obtain the actual coordinate form of every parabolic. The result is a complete classification, rather than only an order or rank bound.

The symmetric-group converse retains two results of Whiston, including the separate omission-subgroup consequence of his classification-dependent argument. The inductively minimal converse retains the earlier Buekenhout–Cara–Dehon classification. These inputs are stated precisely below. The constructions, flag completion, geometric recognition and parameter proofs do not presume the conclusions being recovered.

## 1. Conventions, definitions and retained background

All type sets and forests are finite, as are the domains of the symmetric groups. The normal-quotient bounds and numerical invariants \(\mu,\mu^{\prime}\) are used for finite groups; the relative parabolic-generation formula and the Frattini results explicitly allow arbitrary groups with finite rank where stated. Their coset sets may be infinite. The p-group classification is for finite p-groups. Write \(S_\Omega\) and \(A_\Omega\) for the symmetric and alternating groups on \(\Omega\), and \(S_n=S_{\{1,\ldots,n\}}\). Products of permutation groups on disjoint subsets act trivially outside their indicated supports.

A family \(S=(s_i:i\in I)\) in \(G\) is **independent relative to** \(B\leq G\) if
\[
s_i\notin\langle B,s_j:j\ne i\rangle\qquad(i\in I).
\]
It is a relative generating family if additionally \(\langle B,S\rangle=G\). Let \(\mu(G,B)\) and \(\mu'(G,B)\) be the largest sizes of independent relative generating families and independent relative families respectively. Omit \(B\) when \(B=1\). For a group \(D\) acting on \(N\), a family in \(N\) is **\(D\)-independent** if no member belongs to the subgroup generated by the \(D\)-images of the other members; \(\mu'_D(N)\) is its maximum size. Relative strong independence means
\[
\langle B,s_i:i\in U\rangle\cap\langle B,s_i:i\in V\rangle
 =\langle B,s_i:i\in U\cap V\rangle \quad(U,V\subseteq I).
\tag{1.1}
\]

A typed incidence geometry has a reflexive symmetric incidence relation, with distinct elements of the same type never incident. A flag is a pairwise incident set; a chamber has every type. Every flag of a geometry is required to extend to a chamber. Firmness means that every nonchamber flag extends to at least two chambers. A residue consists of the elements incident with a flag whose types do not occur in that flag. Residual connectedness requires connected incidence graphs in residues of rank at least two. We keep the specified group action as part of the pair. The [BC98]/[CC02] source coset convention includes flag transitivity; for the firm-RWPRI assertions it follows from Lemma B.Flags below.

For subgroups \(H_i\leq G\), put \(H_J=\bigcap_{j\in J}H_j\), \(H_\varnothing=G\), and \(B=H_I\). We use left cosets, acted on by left multiplication; inversion converts this to the right-coset convention of Cameron–Cara. Their source coset criterion, retained here as standard background, is:

* (G1) all \(H_J\), for \(J\subseteq I\), are distinct;
* (G2) \(H_J=\langle H_{J\cup\{k\}}:k\in I\setminus J\rangle\) when \(|I\setminus J|\geq2\);
* (G3) a family of cosets of distinct types with pairwise nonempty intersections has a common element.

These conditions give a firm, residually connected, flag-transitive geometry, with coset intersection as incidence; every such group–geometry pair is represented this way. The residue at the standard flag of type \(J\) is the corresponding coset geometry for \(H_J\) with subgroups \(H_{J\cup\{k\}}\). No general assertion that subgroup intersections alone imply (G3) is used.

For a group acting on a geometry, the pair is **PRI** if its action on every type is primitive, and **WPRI** if its action on at least one type is primitive. The residual versions, applied in each residue including the whole geometry, are RPRI and RWPRI. For flag-transitive coset data these say that every, or at least one, corresponding type stabilizer is maximal; RWPRI is precisely:
\[
\text{(G4)}\qquad J\subsetneq I\Longrightarrow
 \text{some }H_{J\cup\{k\}}\text{ is maximal in }H_J.
\]
For the finite groups in the [BC98] branch, a subgroup is **quasi-maximal** if the interval from it to the ambient group in the subgroup lattice is a chain, equivalently if it has a unique saturated subgroup chain to that group; QPRI requires this for every element stabilizer. Property \((2T)_1\) means that each panel stabilizer is two-transitive on the rank-one residue. Property \((IP)_2\) means that each rank-two residue is either a complete bipartite graph or has at most one common neighbor for each pair of distinct same-type vertices. This last condition concerns geometric incidence, not equation (1.1).

The diagram has one vertex for each type; two vertices are joined when their rank-two residue is not complete bipartite. An **end** of a connected diagram is a vertex whose deletion leaves a connected graph. A **middle** is a vertex whose deletion leaves at least two components, all of equal cardinality. This spells out the source's nonend requirement; in particular a one-vertex diagram has no middle. A finite firm flag-transitive pair of rank \(r\) and connected diagram is **minimal** if \(|G|\leq(r+1)!\), and **inductively minimal** if the pair at every residue with connected diagram is minimal, including the empty flag.

**Lemma B.Flags (residual weak primitivity and flags).** A finite-rank geometry on which a group acts residually weakly primitively is flag-transitive.

*Proof.* Fix a chamber. Starting with its empty flag, choose a remaining type on which that flag's stabilizer acts primitively, hence transitively. Given any second chamber containing the chosen flag, use that stabilizer to match its element of the chosen type to the fixed chamber's element. Repeat in the residue. At most \(|I|\) steps match any chamber to the fixed chamber. Thus the group is chamber-transitive. Every flag extends to a chamber, so it is transitive on flags of each fixed type. The fixed chamber's element stabilizers then give the usual coset representation: the typewise coset bijections preserve incidence because transitivity on incident pairs supplies a common representative. ∎

Thus the firm-RWPRI results below need no extra assumption of flag transitivity or residual connectedness. For a flag-transitive coset geometry, firmness gives distinct \(H_J\), and RWPRI gives a maximal next intersection at every proper \(J\). To see distinctness explicitly, firmness gives \(H_{I\setminus\{i\}}>B\); choose \(s_i\) in this difference. For \(J\ne K\), a type in one of their differences supplies an \(s_i\) that lies in one intersection and not the other.

The following are the unexpanded mathematical inputs.

**B97 (foundational classification).** Buekenhout–Cara–Dehon, *Inductively minimal flag-transitive geometries* (1997), as recalled in [BC98] Lemma 1 and the following paragraph: an inductively minimal pair of rank \(r\) is thin and residually connected and has group \(S_{r+1}\). Its connected diagram has no induced cycle longer than three, each edge lies in a unique maximal clique, and each vertex lies in one or two maximal cliques. Conversely every such connected diagram determines exactly one inductively minimal pair up to isomorphism. We retain the classification and uniqueness, not the four targeted property conclusions of the 1998 paper.

**W1 (Whiston bound and extremal generation).** An independent family in \(S_m\) has at most \(m-1\) members, and an independent family with \(m-1\) members generates \(S_m\). We use precisely this implication, not a converse asserting that every independent generating family has maximum size.

**W2 (Whiston omission consequence).** If \(n\geq7\) and \((s_i)\) is an independent generating family of \(S_n\) of size \(n-1\), each omission subgroup \(\langle s_j:j\ne i\rangle\) is intransitive, is transitive imprimitive with blocks of size two, or is \(A_n\). This is the separate consequence of Whiston's proof stated on page 4 of the 2002 manuscript. Its dependence on the classification of finite simple groups is retained. W2 is not deduced here from W1.

We also retain Cayley's formula: there are \(m^{m-2}\) trees on a specified labelled \(m\)-element set. Elementary group theory, permutation parity, and the equivalence of primitivity with maximality of a point stabilizer are used throughout. The source references for these inputs are given at the end. None of the declared target conclusions is used as background.



**PΦ (finite-p-group Frattini quotient).** For every finite p-group \(P\), the quotient \(P/\Phi(P)\) is an elementary abelian p-group, hence a finite-dimensional vector space over \(\mathbb F_p\). Here \(\Phi(P)\) is the intersection of the maximal subgroups. We retain this elementary group-theoretic fact in the form recalled in [ACK05], page 174. Zorn's lemma is retained for the explicitly infinite-group maximal-overgroup arguments. Neither input is a classification of p-group geometries.

For the action-isomorphism convention in Theorem B.MaxRank, we retain the classical fact that every automorphism of \(S_n\) is inner for \(n\geq7\). Choosing instead the source's equivalence of conjugate coset data gives the same stated marking correspondence.

The shared algebraic results used below are U.RelativeBound, U.Relative, U.Maximal, U.FrattiniTransport, U.FrattiniLadder and U.Coset in [U]. Their proofs are not repeated. We identify their hypotheses at each use; their notation \(m(G,B),i(G,B)\) is our \(\mu(G,B),\mu'(G,B)\). U.Coset is stated for right cosets. Taking inverses converts its coset bijection and intersection assertions to our left-coset convention.

## 2. A common forest and flag theorem

Let \(T\) be a tree with vertex set \(V\) and edge set \(E\). Give each vertex a nonempty block \(B_v\), with the blocks pairwise disjoint, and put \(\Omega=\bigsqcup_vB_v\). For \(F\subseteq E\), let
\[
K_F=\prod_C S_{\bigcup_{v\in C}B_v},
\tag{2.1}
\]
where \(C\) runs over the components of the forest \((V,F)\). Root \(T\), and let \(A_e\subseteq\Omega\) be the union of blocks on the side of \(T-e\) away from the root. Set \(H_e=K_{E\setminus\{e\}}=S_{A_e}\times S_{\Omega\setminus A_e}\).

**Theorem B.F (forest intersections and flag completion).** The following hold.

1. \(K_F\cap K_D=K_{F\cap D}\). Moreover \(K_F\) is generated by \(K_\varnothing\) together with the groups \(K_{\{e\}}\), \(e\in F\).
2. The coset system of the \(H_e\) is a firm, residually connected, flag-transitive geometry. Its type-\(e\) elements identify with the \(|A_e|\)-subsets of \(\Omega\), and distinct types satisfy
   \[
   X_e\mathrel{*}X_f\quad\Longleftrightarrow\quad
   |X_e\cap X_f|=|A_e\cap A_f|.
   \tag{2.2}
   \]
3. Its Borel subgroup is \(K_\varnothing=\prod_vS_{B_v}\). The residue whose remaining types are \(F\) is the join of the same constructions on the nontrivial components of \((V,F)\). Its acting group is \(K_F\); components with no edges contribute only a kernel on this residue.

*Proof.* A permutation belongs to both groups in (1) exactly when it preserves every intersection of their component blocks. Two vertices lie in a common block of both forests precisely when their unique tree path belongs to both edge sets. Thus the common refinement is the component partition for \(F\cap D\). Transpositions inside the blocks, together with transpositions joining adjacent blocks along retained edges, connect each component; they generate its full symmetric group. This proves (1).

The coset \(gH_e\) maps to \(gA_e\). Two pairs of subsets are conjugate under \(S_\Omega\) exactly when their four Boolean atoms have the same sizes, giving (2.2). The sets \(A_e\) are laminar: any two are nested or disjoint. Equation (2.2) forces the identical nesting and disjointness relations on any pairwise incident family \((X_e)\). Add \(\Omega\) as a top container. From each selected container subtract its maximal selected proper subcontainers. These differences partition \(\Omega\), and the corresponding differences for the \(A_e\) and \(X_e\) have equal sizes. Bijections between these atoms combine into a single permutation sending every selected \(A_e\) to \(X_e\). This proves (G3) for every partial flag.

Repeated use of (1) gives \(H_J=K_{E\setminus J}\). Different edge sets give different component partitions and different groups, since every block is nonempty and adding an edge allows a transposition between its two sides. Thus (G1) holds. If at least two edge types remain, the groups obtained by deleting each remaining edge collectively contain \(K_\varnothing\) and each remaining one-edge group, proving (G2). The coset criterion gives the geometry assertions. Its residue group and its subgroups factor over the forest components; all elements from different components are incident, which gives the stated join and the kernel convention. ∎

For unit blocks \(B_v=\{v\}\), write \(\tau_e\) for the endpoint transposition of \(e\). The theorem says
\[
K_F=\langle\tau_e:e\in F\rangle
 =\prod_C S_C,\qquad K_\varnothing=1.
\tag{2.3}
\]
This is the unweighted model used for [BC98]. The weighted formulation also supplies the parity construction after an edge contraction and the disjoint-subset construction after a star specialization.

**Theorem B.P (sign-kernel extension).** Let the blocks be singletons and distinguish an edge \(d\), with \(s=\tau_d\). For \(e\ne d\), choose \(\epsilon_e\in\{1,-1\}\) and put
\[
r_d=s,\qquad r_e=(s\tau_e)^{\epsilon_e}.
\tag{2.4}
\]
For \(U\subseteq E\), set \(F(U)=\{d\}\cup(U\setminus\{d\})\). Then
\[
\langle r_e:e\in U\rangle=
\begin{cases}
K_{F(U)},&d\in U,\\
K_{F(U)}\cap A_\Omega,&d\notin U.
\end{cases}
\tag{2.5}
\]
Both the ordinary marking \((\tau_e)\) and (2.4) generate \(S_\Omega\), are independent, and satisfy the full subset intersection property (1.1) with \(B=1\).

*Proof.* Inverting an individual generator leaves its cyclic subgroup unchanged. If \(s\) is included, \(s\) and \(s\tau_e\) recover \(\tau_e\), proving the first case. The sign kernel of \(K_F\), for \(d\in F\), is generated by the \(s\tau_e\), \(e\in F\setminus\{d\}\): every even word in edge transpositions is a product of pairs, and
\[
\tau_e\tau_f=(s\tau_e)^{-1}(s\tau_f),\qquad s\tau_d=1.
\]
This proves the second case, including the empty set, since \(K_{\{d\}}\cap A_\Omega=1\). Intersect (2.5) using Theorem B.F and the sign condition. Since \(F(U)\cap F(V)=F(U\cap V)\), the result is exactly the subgroup for \(U\cap V\). The same conclusion for ordinary markings follows from (2.3). Omitting an ordinary edge or a twisted label \(e\ne d\) leaves its cut invariant; the omitted generator crosses that cut. Omitting \(r_d\) leaves only even permutations, whereas \(r_d\) is odd. These observations prove independence and the generation assertions. ∎

## 3. Overgroups and the inductively minimal property tests

**Lemma B.Overgroups (two-block overgroups).** Let \(\Omega=A\sqcup C\), with \(a=|A|\), \(c=|C|\) positive, and put \(H=S_A\times S_C\). If \(a\ne c\), or \(a=c=1\), then \(H\) is maximal in \(S_\Omega\). If \(a=c\geq2\), its only proper strict overgroup is the unordered two-block stabilizer
\[
W=(S_A\times S_C)\rtimes C_2,
\]
which is maximal and satisfies \([W:H]=2\). In all cases the subgroup interval \([H,S_\Omega]\) is a chain. A positive weighted tree has at most one edge whose two sides have equal total weight.

*Proof.* The case \(a=c=1\) is immediate. The group \(H\) contains the transpositions within each of its two blocks. If an overgroup element does not preserve their unordered partition, its conjugates of these transpositions include one crossing the original blocks. Together with the original within-block transpositions the support graph is connected, so these transpositions generate \(S_\Omega\). This remains valid when one block is a singleton: a permutation moving that singleton produces a cross-block conjugate from the other block. Thus a proper overgroup must preserve the unordered partition. That stabilizer equals \(H\) when the sizes differ and has index two over it when they agree. Its only further overgroup is \(S_\Omega\), by the same argument.

If an edge bisects the total weight, the side of any other edge away from it is a proper positive-weight subset of one of its halves. It has strictly less than half the total weight and cannot be a bisecting side. ∎

**Proposition B.Minimal (unweighted tree property profile).** For a tree \(T\) on \(N\geq2\) vertices, the geometry of Theorem B.F with unit blocks has rank \(N-1\), group \(S_N\), and diagram \(L(T)\), the line graph of \(T\). It is inductively minimal, satisfies RWPRI, \((2T)_1\), and \((IP)_2\), and has the following exact properties:

* PRI holds if no edge bisects \(N\), with the additional primitive case \(N=2\).
* Every element stabilizer is quasi-maximal. Failure of PRI is equivalent to a middle in \(L(T)\).
* RPRI holds exactly when \(T\) is a star, equivalently when \(L(T)\) is complete.

*Proof.* Equation (2.3) gives trivial chamber stabilizer and two elements in each panel; the panel group is \(S_2\), proving thinness and \((2T)_1\). A two-edge forest consists either of a three-vertex path or of two disjoint edges. The corresponding rank-two residue is respectively a six-cycle or a complete bipartite graph \(K_{2,2}\). Consequently the diagram is \(L(T)\) and \((IP)_2\) holds.

Each connected remaining edge set with \(m\) edges is a subtree with \(m+1\) vertices; its residue group is \(S_{m+1}\), while all other vertices are isolated and contribute trivial factors. This verifies inductive minimality. In any nonempty forest residue choose a leaf of a nontrivial component. Its edge cut gives a point stabilizer in that component's symmetric group. This is maximal, and multiplying by the other factors preserves maximality. Thus RWPRI holds.

Lemma B.Overgroups gives the global PRI and quasi-maximality tests. Removing the vertex \(e\) from \(L(T)\) leaves the line graphs of the two sides of \(T-e\), with respective cardinalities \(a-1\) and \(N-a-1\); an empty side of this diagram corresponds to a leaf cut. A middle therefore exists exactly when an edge has \(a=N-a\geq2\), which is exactly failure of PRI. For \(N=2\) there is no middle and the pair is primitive.

Every nontrivial subtree of a star is again a star, and every edge cut of a star is a leaf cut, so its residues are PRI. A nonstar tree contains a three-edge path. The residue on those three edges is an \(S_4\) geometry with a \(2+2\) middle cut; its stabilizer \(S_2\times S_2\) is not maximal by Lemma B.Overgroups. Thus RPRI fails. Finally, a tree has pairwise adjacent edges exactly when it is a star, proving the line-graph formulation. ∎

**Lemma B.Diagram (diagram recognition).** Every connected graph satisfying the three diagram conditions in B97 is the line graph of a tree, unique up to isomorphism. Hence B97 identifies every inductively minimal pair with one of Proposition B.Minimal.

*Proof.* For a diagram with at least two vertices, make a vertex for each maximal clique. A diagram vertex in two maximal cliques gives an edge between the corresponding clique vertices; a diagram vertex in one maximal clique gives an edge from its clique vertex to a new leaf. Two distinct maximal cliques meet in at most one vertex, since a shared edge would violate the unique-clique condition. Thus the resulting graph has no loops or parallel edges. It is connected, and its edge labels are the original diagram vertices, with exactly their original adjacencies.

A shortest cycle of length at least four in this graph would give an induced cycle of that length on its edge labels in the diagram. A triangle would give three pairwise adjacent edge labels, which extend to a maximal clique; its three pairwise edges would then violate uniqueness of the maximal cliques already represented at the three cycle vertices. Both cases are impossible. The constructed graph is therefore a tree. Conversely the maximal cliques in the line graph of a tree are its nontrivial edge stars, so this construction recovers the tree. A one-vertex diagram corresponds separately to the one-edge tree. Proposition B.Minimal constructs an inductively minimal pair for every such diagram; the uniqueness in B97 identifies it with the given pair. ∎

## 4. Relative generation and extremal markings

**Proposition B.RelativeApplication.** For finite \(G\) and \(N\unlhd G\),
\[
\mu(G)\leq\mu(G/N)+\mu'(N),\qquad
\mu(G)\leq\mu(G/N)+\mu'_G(N)\quad\text{if }N\text{ is abelian}.
\tag{4.1}
\]
A finite-group coset geometry of rank \(r\) and Borel \(B\) has \(r\leq\mu'(G,B)\). If a finite-rank firm geometry is RWPRI, its group may be infinite, and any choices
\[
s_i\in H_{I\setminus\{i\}}\setminus H_i
\tag{4.2}
\]
satisfy
\[
H_J=\langle B,s_i:i\notin J\rangle\quad(J\subseteq I).
\tag{4.3}
\]
They form a strongly independent relative generating family. For finite \(G\), this gives \(r\leq\mu(G,B)\).

*Proof.* The first bounds are U.RelativeBound applied to the indicated finite group and its normal subgroup. For a source coset geometry, flag transitivity is part of the coset criterion; for a general firm RWPRI geometry it follows from B.Flags. In either case firmness gives distinct intersections and the nonempty panel differences (4.2). Every \(s_j\), \(j\ne i\), and \(B\) lie in \(H_i\), whereas \(s_i\) does not. Thus the panel choices are relatively independent, proving the first rank bound even without RWPRI. Under RWPRI, each proper \(H_J\) has a maximal next intersection by (G4). These are exactly the hypotheses of U.Relative, which supplies (4.3), generation and every relative intersection identity. No finiteness or separate residual-connectedness hypothesis is used in this last application. ∎

**Lemma B.Blocks (the two-point-block obstruction).** If \(m\geq4\) and \(H\leq C_2\wr S_m\) is transitive on its \(2m\) points, then \(H\) cannot have an independent generating family of size \(2m-2\).

*Proof.* Let \(N\) be the block kernel, a subspace of \(\mathbb F_2^m\), and let \(P=H/N\leq S_m\) be the transitive block action. W1 bounds \(\mu(P)\leq m-1\). We first have \(\mu'_H(N)\leq m-1\). This is automatic if \(N\) is proper. If \(N=\mathbb F_2^m\) and an \(H\)-independent family had \(m\) elements, it would be a vector-space basis. For each omitted basis vector, the span of the orbits of the others is proper but contains their hyperplane, so that hyperplane is invariant. Intersecting these hyperplanes shows that every basis line is invariant. Over \(\mathbb F_2\) every such line is pointwise fixed, contradicting the nontrivial transitive block action.

If an independent generating family of size \(2m-2\) existed, Proposition B.RelativeApplication would give
\[
2m-2\leq\mu(H)\leq\mu(P)+\mu'_H(N)\leq2m-2.
\]
Equality forces \(\mu(P)=m-1\); applying W1 to that family in \(S_m\) gives \(P=S_m\). Every nonconstant vector \(v\) in an \(S_m\)-invariant subspace generates a submodule containing the even-weight space: for coordinates with different entries, \(v+(ij)v=e_i+e_j\), and the orbit of this vector spans the even-weight space. That space has codimension one. Therefore an \(S_m\)-independent family containing \(v\) can have at most one further member; a family of constant vectors has at most one member. Consequently \(\mu'_H(N)\leq2\), and (4.1) now gives \(2m-2\leq m+1\), contradicting \(m\geq4\). ∎

**Theorem B.Extremal (extremal recognition).** Assume \(n\geq7\). Every independent family of \(n-1\) elements of \(S_n\) is an ordinary tree marking (2.3) or a sign-kernel marking (2.4). If the family is independent relative to \(B\leq S_n\), then \(B=1\).

*Proof.* By W1 the family generates \(S_n\). For its omission groups \(G_i\), W2 and Lemma B.Blocks exclude the two-point-block case: in that case \(n=2m\geq8\), and the remaining \(n-2\) generators are an independent generating family for \(G_i\). At most one \(G_i\) is \(A_n\), because its omitted generator must be the unique odd member. Label a possible exception by \(1\).

For each \(i>1\), choose an edge \(e_i=\{x,s_i(x)\}\) crossing two \(G_i\)-orbits. Such an edge exists, since otherwise every generator would preserve those orbits. Choose \(e_1\) from any moved point of \(s_1\). If all the omission groups are intransitive, choose \(e_1\) crossing its own omission orbits as well. For \(j\ne i\), the edge \(e_j\) lies inside a \(G_i\)-orbit because \(s_j\in G_i\). In particular the chosen edges are distinct: a repeated edge with a label \(i>1\) would both cross and stay inside the \(G_i\)-orbits. Thus a cycle cannot contain \(e_i\) for \(i>1\): the remaining edges would give a path within a \(G_i\)-orbit between its endpoints. A cycle cannot consist of \(e_1\) alone. The \(n-1\) edges therefore form a tree on the \(n\) points.

Deleting \(e_i\), for \(i>1\), leaves two connected sets each contained in a \(G_i\)-orbit; intransitivity makes them exactly its two orbits. Hence \(s_j\) preserves this cut whenever \(j\ne i\). Intersect these cut stabilizers using Theorem B.F. It follows that \(s_1\in K_{\{e_1\}}\), so \(s_1=\tau_{e_1}\), and that \(s_i\in K_{\{e_1,e_i\}}\). If every omission group is intransitive, include the first cut too to obtain \(s_i=\tau_{e_i}\) for every \(i\). Otherwise \(G_1=A_n\), and all other generators are nonidentity even elements of the two-edge group. For adjacent edges that group is \(S_3\), whose nonidentity even elements are the two inverse three-cycles; for disjoint edges it is \(C_2\times C_2\), with a unique nonidentity even element. These are precisely \((s_1\tau_{e_i})^{\pm1}\), giving (2.4).

Now suppose the original family is independent relative to \(B\). It is independent in the ordinary sense, so the preceding classification applies. By Theorems B.F and B.P its omission groups are the tree-cut stabilizers, except that in the sign-kernel case the distinguished omission group is \(A_n\). At each maximal omission group independence forces \(B\leq G_i\); otherwise \(\langle B,G_i\rangle=S_n\). A pendant edge different from the distinguished edge exists and yields a point stabilizer, so \(B\) fixes a point. At a nonmaximal cut, Lemma B.Overgroups forces \(B\) into the unordered two-block stabilizer. Its elements outside the ordered stabilizer interchange the halves and fix no point. Thus \(B\leq G_i\) here also. Strong independence from Theorems B.F and B.P gives \(B\leq\bigcap_iG_i=1\). ∎

**Corollary B.Count (the three counting conventions).** For \(n\geq7\), the number of actual unordered generating sets of the first form is \(n^{n-2}\). The number of actual unordered sets of the second form is \((n-1)n^{n-2}\). If a three-cycle and its inverse are identified independently in such a set, the second number becomes
\[
\binom n2(n-1)^{n-3}.
\]

*Proof.* Ordinary sets recover their unique edge trees, so Cayley's formula gives the first count. A twisted set has a unique odd member \(s=(a\ b)\). Multiplying each of its other actual members \(h\) by \(s\) recovers a transposition. If \(h=(s\tau_e)^{-1}\), the recovered edge is the conjugate \(s\tau_es\); for an adjacent edge this switches its attachment from \(a\) to \(b\), and for a disjoint edge it changes nothing. Contracting \(\{a,b\}\) gives the same tree before and after any switches. Every such independent switch therefore preserves the tree property. Consequently actual twisted sets are in bijection with trees having one distinguished edge, via the canonical set \(\{s\}\cup\{s\tau_e:e\ne d\}\). This gives \((n-1)n^{n-2}\). Modulo inversion of the three-cycles, the data are exactly the pair \(\{a,b\}\) and a labelled tree on the \(n-1\) blocks obtained by contracting it. Cayley's formula gives the last count. ∎

## 5. From markings to every geometry of maximum rank

**Theorem B.MaxRank (geometry recognition).** For \(n\geq7\), each marking in Theorem B.Extremal gives an RWPRI coset geometry with its omission subgroups. Conversely every source coset geometry of \(S_n\) of rank \(n-1\) is one of these, and has trivial Borel subgroup. Among RWPRI geometries the correspondence is bijective after simultaneous conjugation and independent inversion of the marking generators; sets are unordered, so type renaming is understood.

*Proof of existence.* Strong independence and generation give (G1) and (G2). Theorem B.F supplies (G3) for ordinary markings, and the leaf argument of Proposition B.Minimal supplies (G4).

For a sign-kernel marking, contract \(d\) to a vertex of weight two. Its other omission groups are precisely the cut stabilizers of this weighted tree, while the distinguished omission group is \(A_n\). Theorem B.F gives a common representative for the cut types of any flag. Every intersection of these cut stabilizers contains the odd transposition \(s\). Multiplying the representative on the right by \(s\) changes its parity without changing any of its cut cosets, so it can satisfy the parity coset too. This proves (G3).

To prove (G4), if parity is not yet fixed, choose that type: the even subgroup has index two in the residue group, because the latter contains \(s\). If parity is fixed, the residue group is the even part of a product of forest symmetric groups, and the component containing \(d\) still contains that edge. If another component has an edge, choose a leaf cut there. Projection from the residue group onto that component's symmetric group is surjective, since the \(d\)-component supplies an odd correction. The new stabilizer is the inverse image of a maximal point stabilizer, so is maximal. If only the \(d\)-component is nontrivial and a type remains, it has at least three vertices and a leaf other than the two endpoints considered together as the distinguished block. More explicitly, every tree with at least three vertices has a leaf not belonging to a specified edge's two endpoints unless that edge is the whole tree; such a leaf supplies a remaining cut. The group on this component is its alternating group. Its natural action is primitive: for degree at least four it is two-transitive (adjust the parity of a map of an ordered pair by swapping two remaining points), and \(A_3\) is regular of prime degree. The leaf stabilizer is again maximal. This proves (G4).

*Proof of uniqueness in the RWPRI case.* Proposition B.RelativeApplication and then Theorem B.Extremal give \(B=1\), a classified marking, and equality (4.3) for all parabolics. Each panel group is cyclic of order two or three. A generator of it is therefore unique up to inversion. Moving the chosen chamber conjugates all stabilizers and generators together; renaming types reorders the set. Conversely those operations give the same group–geometry pair. Here isomorphisms intertwine the specified \(S_n\)-action, up to an automorphism of \(S_n\); for \(n\geq7\) all such automorphisms are inner, an elementary symmetric-group fact retained for this formulation. Equivalently one may use the source convention of conjugate coset data throughout.

*Proof for arbitrary maximum-rank geometries.* This step does not assume (G4). Choose \(s_i\) as in (4.2); they are independent relative to \(B\). W1 gives ordinary generation and Theorem B.Extremal gives \(B=1\) and the two marking families. Let \(G_i=\langle s_j:j\ne i\rangle\). Then
\[
G_i\leq H_i<S_n.
\]
Lemma B.Overgroups and the maximality of \(A_n\) show that \(H_i=G_i\), except possibly at one balanced cut \(k\), where \(H_k\) might be its unordered stabilizer \(W_k\). Every other tree edge has a nonempty cut side wholly in one \(k\)-half. Its stabilizer cannot interchange those halves, so
\[
W_k\cap G_j\leq G_k
\tag{5.1}
\]
for every such cut type \(j\ne k\).

Consider a panel intersection \(\bigcap_{j\ne i}H_j\). If it omits \(k\), it is already the corresponding intersection of the \(G_j\). If it contains \(k\), it also contains another cut type \(j\ne i,k\), since there are \(n-1\geq6\) types and at most one is a parity type. Equation (5.1) again lets us replace \(W_k\) by \(G_k\). All panels therefore coincide with those of the marking and equal \(\langle s_i\rangle\). Starting from panels and using (G2) downwards now gives \(H_J=\langle s_i:i\notin J\rangle\) for every \(J\). In particular every \(H_i=G_i\); the geometry is one already proved RWPRI. ∎


## 6. Frattini kernels and primitive coordinates

The groups in this section may be infinite, with finite type set, except where a finite p-group is expressly specified. Put \(\Phi(G)=\bigcap\{M:M\text{ maximal in }G\}\), with an empty intersection equal to \(G\).

**Theorem B.FrattiniApplication.** For a finite-rank firm RWPRI geometry with Borel \(B\),
\[
\Phi(G)\leq B\leq H_i\quad(i\in I).
\tag{6.1}
\]
The geometry is isomorphic, with the same permutation action, to the coset geometry of \(G/\Phi(G)\) and the subgroups \(H_i/\Phi(G)\). More generally this coset correspondence holds for any normal subgroup \(N\leq B\), even for a pregeometry without flag transitivity. The full action kernel is
\[
\operatorname{core}_G(B)=\bigcap_i\operatorname{core}_G(H_i).
\tag{6.2}
\]
Quotienting by it makes the action faithful.

*Proof.* By B.Flags and firmness all indexed intersections are distinct. Repeatedly choosing a maximal next intersection under (G4) supplies a chain from \(G\) to \(B\), every step maximal. The subgroup \(\Phi(G)\) is characteristic and lies in every maximal subgroup of \(G\). Thus all hypotheses of U.FrattiniLadder hold, proving (6.1), including for infinite \(G\). U.Coset now applies because the normal subgroup lies in every type stabilizer. Its coset bijection preserves all intersection patterns and maximal subgroup intervals, hence the geometry, residues and primitive properties.

An element acts trivially on every type precisely when it lies in the core of every \(H_i\). Intersecting all conjugates commutes with the finite intersection defining \(B\), proving (6.2). This is the largest normal subgroup contained in \(B\), and U.Coset gives the faithful quotient. ∎

The quotient \(G/\Phi(G)\) is Frattini free: its maximal subgroups correspond to the maximal subgroups of \(G\), with intersection \(\Phi(G)\). If there are no maximal subgroups then the quotient is trivial, and the conclusion is the same. In particular every firm RWPRI geometry has a realization for a Frattini-free group. Pullback and quotient give a bijection of indexed subgroup families with the quotient map fixed. This does not assert that automorphisms of the quotient lift, or identify orbit counts under different automorphism groups.

For relative generating families, U.FrattiniTransport says that a finite family generates \(G\) irredundantly relative to \(B\) if and only if its image does so in \(G/\Phi(G)\), provided every proper overgroup of \(B\) is contained in a maximal subgroup. This hypothesis holds for finite groups. It also follows from U.Maximal when \(G\) is finitely generated relative to \(B\). The unrestricted infinite converse printed in [ACK05, Theorem 2.1] requires this correction. Indeed let \(D=C_{p^\infty}\) and \(G=D\times C_2\). A maximal subgroup of this abelian group has a cyclic quotient of prime order. Divisibility makes the image of \(D\) in every such quotient trivial; the only maximal subgroup is therefore \(D\times1=\Phi(G)\). The generator of the second factor generates \(G/\Phi(G)\) but not \(G\). This counterexample does not restrict Theorem B.FrattiniApplication: its maximal-overgroup argument is already furnished by the finite maximal chain in U.FrattiniLadder.

**Theorem B.Coordinates.** Let \(P\) be a finite p-group acting on a firm RWPRI geometry of rank \(r\), with Borel \(B\). Then \(B\unlhd P\), \(P/B\cong\mathbb F_p^r\), and there is a basis \((v_i)_{i\in I}\) such that
\[
H_J/B=\operatorname{span}\{v_i:i\notin J\}\quad(J\subseteq I).
\tag{6.3}
\]
The geometry is the direct sum of \(r\) primitive rank-one geometries of \(p\) points. It is RPRI, and its faithful group \(P/B\) is regular on chambers.

*Proof.* B.FrattiniApplication gives \(\Phi(P)\leq B\). The retained finite-p-group fact PΦ identifies \(P/\Phi(P)\) with a vector space. Consequently \(B/\Phi(P)\) is normal, \(B\unlhd P\), and \(P/B\) is a vector space. Apply B.RelativeApplication: the images \(v_i=s_iB\) span \(P/B\). A nonzero linear dependence expresses one \(s_i\) modulo \(B\) in terms of the other generators, contrary to relative independence. Thus they form a basis, and (4.3) becomes (6.3).

The cosets of \(H_i/B\) are exactly the \(p\) possible values of coordinate \(i\). Assignments to distinct coordinates always have a common vector. Hence every choice of one element of each type is a chamber, with all distinct types completely incident. Fixing one more coordinate in any residue has index \(p\), and is a maximal subgroup inclusion. This proves RPRI and the primitive direct-sum description. Since \(B\) is normal it is the action kernel in (6.2); translations of \(P/B\) are regular on the set of complete coordinate assignments. ∎

Conversely every family of \(r\) independent functionals on \(P/\Phi(P)\) yields such a geometry by pulling back their kernels. The coordinate argument proves firmness, flag transitivity, residual connectedness and RPRI. Theorem B.Coordinates shows there are no other indexed subgroup families. Writing \(d=\dim P/\Phi(P)\), their number is
\[
\frac{\prod_{j=0}^{r-1}(p^d-p^j)}{(p-1)^r},\qquad 1\leq r\leq d,
\tag{6.4}
\]
since one chooses independent ordered functionals and divides by the independent nonzero rescalings that preserve their kernels. This counts indexed subgroup families, not automorphism orbits.

Two subsidiary assertions of [ACK05] follow directly in these coordinates. For arbitrary subgroups \(H_1,H_2\), the cosets \(gH_1,hH_2\) meet precisely when \(g^{-1}h\in H_1H_2\). Thus their rank-two pregeometry is a direct sum exactly when \(H_1H_2=G\). If \(U,W<\mathbb F_p^k\), with \(U\) a hyperplane, \(U\cap W\) a hyperplane of \(U\), and \(W\not\subseteq U\), then \(W\) has one-dimensional image in \(\mathbb F_p^k/U\). It follows that \(\dim W=(k-2)+1=k-1\), as asserted in the source's maximal-subspace lemma.

Finally, every residue gives its own necessary Frattini test. At a flag of type \(J\), its stabilizer is \(H_J\); its type subgroups are \(H_J\cap H_i\), \(i\notin J\), and their common intersection is still \(B\). B.Flags, firmness and residual weak primitivity hold within this residue. Applying U.FrattiniLadder to these actual subgroups gives
\[
\Phi(H_J)\leq B\leq H_J\cap H_i\quad(i\notin J).
\tag{6.5}
\]
This is a necessary rejection test, not a sufficiency criterion. It does not rely on the generally false inclusion \(\Phi(H_J)\leq\Phi(G)\).

## 7. Weighted stars and Kneser geometries

Let \(r\geq2\), \(k\geq1\), and \(N>rk\) be integers. On a star with \(r\) labelled leaves give each leaf a block of size \(k\), and give the central vertex a block of size \(N-rk\). Root the star at its center. Its edge cuts are precisely the leaf blocks. Theorem B.F therefore gives a geometry \(\mathcal K(N,k,r)\) whose type set is \(\{1,\ldots,r\}\), with
\[
\{\text{type-}i\text{ elements}\}=\binom{[N]}k,
\qquad (i,A)*(j,B)\iff i\ne j\text{ and }A\cap B=\varnothing
\tag{7.1}
\]
for distinct elements. This is exactly Construction 1.1 of [GL21], on setting
\[
N=n+k(r-2),\qquad n\geq2k+1.
\tag{7.2}
\]
The case \(k=1,n=3\) is the unit-star geometry of Proposition B.Minimal, so the two constructions overlap at the level of their actual cosets and actions.

**Theorem B.Star (the weighted-star specialization).** The geometry \(\mathcal K(N,k,r)\) is firm, residually connected and flag-transitive under \(S_N\). A flag of \(s\) elements has residue \(\mathcal K(N-sk,k,r-s)\), on the complement of its subsets, with the evident rank-zero and rank-one conventions. Each type has \(\binom Nk\) elements, and each panel has
\[
\binom{N-(r-1)k}{k}=\binom{n-k}{k}
\tag{7.3}
\]
elements. It is thick except when \(k=1,n=3\), when it is thin. The incidence graph is \(KG(N,k)\otimes K_r\); its vertex links are \(KG(N-k,k)\otimes K_{r-1}\). The group \(S_N\) is transitive on its maximal cliques.

*Proof.* All positive-weight and laminar-cut hypotheses of B.F hold for the displayed star, so firmness, residual connectedness, flag completion and flag transitivity follow from that theorem. Explicitly, a flag is a family of disjoint \(k\)-subsets assigned to distinct types. Its residue uses the unused points and types, proving the residue identity. It also gives (7.3). If \(k=1\), this number is \(n-1\), which is two only for \(n=3\) and is at least three otherwise. If \(k\geq2\), then \(n-k\geq k+1\), so it is at least \(\binom{k+1}k=k+1\geq3\). This proves the exact thin boundary without an additional parameter restriction.

Equation (7.1) is the tensor-product adjacency relation. Fixing \((i,A)\) leaves the other \(r-1\) types and the \(N-k\) points outside \(A\), proving the link formula. Every maximal clique is a chamber by flag completion. A bijection between the \(r\) disjoint subsets of two chambers extends to a permutation of their complements, proving the stated transitivity. ∎

Here \(\otimes\) denotes the categorical, or tensor, graph product: both coordinates must be adjacent. For \(r=2\), its link formula is simply an edgeless graph on the neighbors, as \(K_1\) has no edges. The rank-two residues are the bipartite doubles of \(KG(n,k)\). We compute their distances without invoking a classification of distance-regular graphs.

**Proposition B.Distance (replacement distances).** Put \(s=n-2k>0\), and let \(A,B\) be \(k\)-subsets of \([n]\), with \(c=|A\cap B|\). In the bipartite double of \(KG(n,k)\), the distances between copies in the same and in opposite parts are respectively
\[
d_{\mathrm{even}}(A,B)=2\left\lceil\frac{k-c}{s}\right\rceil,
\qquad
d_{\mathrm{odd}}(A,B)=2\left\lceil\frac{c}{s}\right\rceil+1.
\tag{7.4}
\]
Its diameter, from either part, is \(2\lceil k/s\rceil+1\). Its gonality is three for \(n=2k+1\) and two for \(n\geq2k+2\). The odd girth of \(KG(n,k)\) is \(2\lceil k/s\rceil+1\).

*Proof.* If \(A,C,D\) are successive vertices of a disjointness walk, then \(A\cup D\) lies in the complement of \(C\), of size \(n-k=k+s\). Thus \(|A\setminus D|\leq s\): two steps change at most \(s\) entries. Conversely, if two \(k\)-sets differ in at most \(s\) entries, their union has size at most \(k+s\), leaving at least \(k\) points from which to choose a common disjoint set. Every such replacement is realizable in two steps.

An even walk from \(A\) to \(B\) must replace the \(k-c\) elements of \(A\setminus B\), so needs at least \(2\lceil(k-c)/s\rceil\) steps. Partition those elements and the corresponding new elements of \(B\setminus A\) into matching batches of size at most \(s\). Replace one batch at a time and use the common disjoint set just constructed. This realizes the bound, including distance zero when \(A=B\).

For an odd walk, let \(C\) be its penultimate set; then \(C\cap B=\varnothing\), so \(|A\cap C|\leq k-c\). Its even initial segment has length at least \(2\lceil c/s\rceil\). Equality is achievable: take all of \(A\setminus B\), and fill \(C\) with \(c\) points outside \(A\cup B\). There are \(s+c\) available such points. Use the even construction from \(A\) to \(C\), then the edge to \(B\). This proves (7.4). Both parity distances are finite, so the double is connected. Their largest value is the asserted odd distance between the two copies of a single set.

The number of common neighbors of two distinct sets with intersection size \(c\) is
\[
\binom{n-2k+c}{k},
\tag{7.5}
\]
with the binomial coefficient zero if its upper argument is smaller than \(k\). For \(n=2k+1\), distinct sets have \(c\leq k-1\), so (7.5) is at most one. There is no four-cycle. To exhibit a six-cycle, take three \(k\)-sets \(S\cup\{x\},S\cup\{y\},S\cup\{z\}\), where \(|S|=k-1\) and \(x,y,z\) are distinct outside \(S\). In the other part take the complements of the unions of each consecutive pair. Each complement has size \(k\); the three complements are distinct, and they yield a six-cycle. This works also for \(k=1\). If \(n\geq2k+2\), choose two sets differing in one entry. Formula (7.5) is at least \(\binom{k+1}k\geq2\), giving a four-cycle. These facts give the gonalities.

Finally, (7.4) with \(A=B\) gives the minimum length of an odd closed walk in the Kneser graph. Every odd closed walk contains an odd cycle: if it repeats a vertex internally, splitting it at that vertex leaves an odd closed subwalk, and induction removes repetitions. Therefore the minimum odd closed walk is itself an odd cycle, proving the odd-girth assertion. ∎

It follows that the Buekenhout diagram is complete, with each edge labelled \(d-g-d\), where \(d=2\lceil k/(n-2k)\rceil+1\) and \(g\) is as in B.Distance. No rank-two residue is a generalized digon: the two copies of the same \(k\)-set are not incident. Thus the geometric property \((IP)_2\) holds exactly for \(n=2k+1\). The order at each diagram vertex is the panel size minus one, namely \(\binom{n-k}{k}-1\).

### 7.1. Recovering the permutation action

**Lemma B.Johnson.** If \(N>2k\), every automorphism of the Johnson graph \(J(N,k)\) is induced by a unique permutation of \([N]\).

*Proof.* The vertices are the \(k\)-sets, with adjacency when their intersection has size \(k-1\). For \(k=1\) this is the complete graph on \([N]\), so the assertion holds. Assume \(k\geq2\). For each \((k-1)\)-set \(C\), the family of \(k\)-sets containing \(C\) is a clique, called its star. For each \((k+1)\)-set \(D\), the family of \(k\)-sets contained in \(D\) is a clique, called its top.

These are all maximal cliques. To see this, take two adjacent vertices \(A=C\cup\{a\}\), \(B=C\cup\{b\}\). Any further vertex adjacent to both either contains \(C\), or has the form \((C\setminus\{x\})\cup\{a,b\}\) for some \(x\in C\). In the latter case it is contained in \(D=C\cup\{a,b\}\). A vertex \(C\cup\{z\}\) with \(z\notin D\) meets such a latter vertex in only \(k-2\) points, so cannot occur in the same clique. Consequently a clique through \(A,B\) lies entirely in their star or their top, and maximality gives the whole star or top. Both displayed families are maximal by the same observation.

Stars have size \(N-k+1\), larger than the top size \(k+1\); hence every automorphism preserves stars. Two distinct stars intersect if and only if their \((k-1)\)-sets differ in one point, so the induced action on stars is an automorphism of \(J(N,k-1)\). Induction identifies it with a permutation of \([N]\), since \(N>2(k-1)\). A \(k\)-set is determined by the stars containing it, namely its \((k-1)\)-subsets. The action on stars therefore determines the original action, proving existence and uniqueness. ∎

**Proposition B.TypedAut.** The type-preserving automorphism group of \(\mathcal K(N,k,r)\) is \(S_N\), and the group allowed to permute its types is \(S_N\times S_r\).

*Proof.* Within one type, count the common neighbors of two distinct vertices in a fixed other type. Formula (7.5), now with ambient size \(N\), is strictly largest exactly when their intersection has size \(k-1\): its upper argument there is \(N-k-1\geq k\), and decreasing the intersection either strictly decreases the binomial coefficient or makes it zero. Thus the incidence relation reconstructs the Johnson adjacency in each type. By B.Johnson a type-preserving automorphism acts on type \(i\) by a permutation \(\pi_i\) of \([N]\).

These permutations are all equal. For two types \(i\ne j\), compose with \(\pi_i^{-1}\) on the ground set. The resulting permutation fixes every vertex of type \(i\), and sends a type-\(j\) set \(B\) to \(\pi_i^{-1}\pi_j B\) with the same disjointness neighborhood. Distinct \(k\)-sets have distinct such neighborhoods: if \(x\in B\setminus B'\), choose a \(k\)-set containing \(x\) in the complement of \(B'\); it meets \(B\) but is disjoint from \(B'\). This is possible because \(N-k\geq k\). Hence every \(B\) is fixed, and faithfulness of the action on \(k\)-sets gives \(\pi_i=\pi_j\). The diagonal \(S_N\) acts, so it is exactly the type-preserving group.

Every permutation of the \(r\) types acts independently and commutes with the diagonal \(S_N\). Composing any type-permuting automorphism with the inverse of its type permutation reduces to the type-preserving case. The two actions have trivial intersection, giving the direct product. ∎

### 7.2. Recovering the types from the uncolored graph

The automorphism group of a typed geometry need not be the full group of its incidence graph: a graph automorphism could conceivably mix the type classes. We exclude this possibility for (7.1) by identifying the type classes intrinsically as the maximum independent sets.

Let \(\mathscr V=\binom{[N]}k\), \(v=|\mathscr V|\), and let \(K\) be its disjointness matrix. Its row sum is \(d=\binom{N-k}{k}\). For a subset \(T\) of size \(j\leq k\), put \(f_T(A)=1\) if \(T\subseteq A\), and zero otherwise. Let \(V_j\) be the span of the \(f_T\) with \(|T|=j\). The spaces form an increasing filtration: for \(|S|=j-1\),
\[
\sum_{\substack{T\supset S\\ |T|=j}} f_T=(k-j+1)f_S.
\tag{7.6}
\]
Also \(V_0\) consists of constants and \(V_k=\mathbb R^{\mathscr V}\), because the latter indicators are the individual vertex indicators.

For \(|T|=j\), direct counting and inclusion–exclusion give
\[
(Kf_T)(A)=\binom{N-k-j}{k-j}\,1_{A\cap T=\varnothing}
=\binom{N-k-j}{k-j}\sum_{S\subseteq T}(-1)^{|S|}f_S(A).
\tag{7.7}
\]
Thus \(K\) preserves the filtration and acts on \(V_j/V_{j-1}\) by
\[
\lambda_j=(-1)^j\binom{N-k-j}{k-j}.
\tag{7.8}
\]
Choosing bases adapted to the filtration shows that every eigenvalue is one of these values; any zero-dimensional quotient simply contributes none. As \(K\) is real symmetric, it is diagonalizable. For \(j\geq1\),
\[
|\lambda_j|\leq\binom{N-k-1}{k-1}
=\frac{k}{N-k}\,d<d.
\tag{7.9}
\]
The inequality follows successively from \(\binom{a-1}{b-1}/\binom ab=b/a<1\). In particular \(d\) occurs only on the constant subspace.

The graph adjacency matrix is \(M=(J_r-I_r)\otimes K\). The two eigenvalues of \(J_r-I_r\) are \(r-1\) on constants and \(-1\) on their orthogonal complement. Tensor products of eigenbases give all eigenvectors of \(M\). Since \(N>rk\),
\[
(r-1)\frac{k}{N-k}<1.
\tag{7.10}
\]
It follows from (7.9) that the least eigenvalue of \(M\) is exactly \(-d\). Its eigenspace consists precisely of vectors constant on each type, with the \(r\) constants summing to zero.

**Theorem B.Aut (the full incidence-graph group).** The maximum independent sets of the graph of \(\mathcal K(N,k,r)\) are exactly its \(r\) type classes. Its full graph automorphism group is \(S_N\times S_r\).

*Proof.* The graph has \(rv\) vertices and valency \(t=(r-1)d\). If an independent set has size \(a\), write its indicator as \(x=\alpha\mathbf1+z\), where \(\alpha=a/(rv)\) and \(z\perp\mathbf1\). Then \(\|z\|^2=rv\alpha(1-\alpha)\). Independence gives \(x^TMx=0\), hence
\[
z^TMz=-t\,rv\alpha^2.
\]
The least-eigenvalue inequality \(z^TMz\geq-d\|z\|^2\) therefore gives \(t\alpha\leq d(1-\alpha)\), or \(\alpha\leq1/r\). Thus \(a\leq v\), attained by each type class.

If \(a=v\), equality holds in the eigenvalue inequality. Expanding \(z\) in an orthonormal eigenbasis shows that every component on a larger eigenvalue is zero. Thus \(z\), and therefore \(x\), is constant on each type. Since \(x\) is a zero-one indicator of size exactly \(v\), it is the indicator of one type class. Graph automorphisms preserve maximum independent sets and hence permute the types. Proposition B.TypedAut now gives the full group. ∎

For \(k=2,n=5,r=3\), the graph has \(3\binom72=63\) vertices and each link is the bipartite double of the Petersen graph \(KG(5,2)\), the Desargues incidence graph. Explicitly, complementing the sets in one part identifies its incidence with containment between the two-subsets and three-subsets of a five-element set, the classical Desargues \(10_3\) configuration. Its full group is \(S_7\times S_3\), of order \(30240\). The source's displayed Corollary 5.1 names only \(S_7\); that is the type-preserving subgroup. Theorem B.Aut establishes the larger full graph group without relying on a finite enumeration.

## 8. Source results as corollaries

The preceding arguments give the following four applications. The references in their proofs specify which common construction or quotient theorem supplies each conclusion.

**Corollary B.BC98 (inductively minimal pairs).** For every finite inductively minimal pair of positive rank:

1. RWPRI, \((2T)_1\) and \((IP)_2\) hold.
2. Even rank implies PRI.
3. Every type stabilizer is quasi-maximal; failure of PRI is equivalent to a middle in the connected diagram.
4. RPRI holds if and only if the diagram is complete.

*Proof.* The retained B97 classification and B.Diagram identify the pair with a unit-weight tree geometry. B.Minimal gives the first, third and fourth conclusions. For the second, an even number of edges gives an odd number of vertices, so no edge cut is balanced; B.Overgroups gives maximality of every type stabilizer. These are all four clauses of [BC98, Theorem 1]. The stronger wording in clause 3 avoids an ambiguity in the source: its phrase “this is the case” characterizes failure of PRI, not QPRI alone. The one-vertex diagram has no middle and is included. ∎

**Corollary B.CC02 (extremal symmetric-group generators and geometries).** For \(n\geq7\), the independent generating sets of \(S_n\) of size \(n-1\) are exactly the ordinary and sign-kernel tree markings of B.F and B.P. They are strongly independent and have the three counts in B.Count. A relative independent generating family of that size forces its relative subgroup to be trivial. Independent generating sets, modulo conjugation and independent inversion of generators, correspond bijectively to RWPRI coset geometries of rank \(n-1\), with type renaming understood. Every source coset geometry of this rank is RWPRI. The general finite-group normal-quotient and geometric rank bounds are those of B.RelativeApplication.

*Proof.* B.Extremal gives the classification and triviality of the relative subgroup; B.F and B.P give every intersection and both construction converses. B.Count distinguishes actual sets from sets modulo three-cycle inversion. B.MaxRank proves the geometry correspondence and, by its separate arbitrary-parabolic argument, the automatic RWPRI assertion. B.RelativeApplication is U.RelativeBound together with the verified coset hypotheses of U.Relative. This recovers [CC02, Theorems 1.1, 2.1, 3.1, 3.2 and Corollaries 2.2–2.4, 3.3], with finite-group scope for the numerical invariants. The small-degree exceptions mentioned after Corollary 2.4 are not included in this \(n\geq7\) classification. ∎

**Corollary B.ACK05 (primitive geometries and Frattini quotients).** A finite-rank firm RWPRI geometry, including one for an infinite group, has its Frattini subgroup inside every type stabilizer and is exactly the corresponding coset geometry of the Frattini quotient. Normal subgroups of the Borel can be removed without changing even the pregeometry; removing its core makes the action faithful. The quotient group is Frattini free. For a finite p-group, RWPRI is equivalent to RPRI, and the geometry is a direct sum of primitive rank-one geometries, with its complete coordinate classification given by B.Coordinates. Every residue satisfies (6.5). Relative irredundant generating families correspond through the Frattini quotient under U.FrattiniTransport's maximal-overgroup hypothesis, in particular for finite groups.

*Proof.* These are B.FrattiniApplication, B.Coordinates and the residue application of U.FrattiniLadder. They give [ACK05, Theorems 3.1, 3.4, 3.8, Proposition 3.2, Corollary 3.3, Proposition 3.7 and §§4.2–4.3]. The coset-product and subspace calculations following B.Coordinates give Proposition 3.5 and Lemma 3.6. U.FrattiniTransport with the explicitly checked maximal-overgroup hypothesis gives Theorem 2.1 in the corrected scope; §6 gives the counterexample to its unrestricted infinite converse. This correction does not narrow the infinite geometric containment theorem. ∎

**Corollary B.GL21 (disjoint-subset geometries and locally Kneser graphs).** For \(r\geq2\), \(k\geq1\), \(n\geq2k+1\), the geometry of [GL21, Construction 1.1] is the weighted star (7.1)–(7.2). It has all the existence, residue and clique-transitivity properties in B.Star, the complete diagram and distance parameters in B.Distance, and the type-preserving and full graph groups in B.TypedAut and B.Aut. It satisfies \((IP)_2\) exactly when \(n=2k+1\).

*Proof.* The star has positive central weight \(n-2k\), so B.F gives B.Star. Its rank-two residues are the bipartite doubles of B.Distance; they are never digons, and their four-cycle criterion gives \((IP)_2\). B.TypedAut and B.Aut prove the two action assertions and exclude extra uncolored graph automorphisms. These establish [GL21, Theorem 1.2 and Corollaries 1.3, 1.4, 4.8, 5.1] with three explicit corrections: the diagram order is \(\binom{n-k}{k}-1\); the case \(k=1,n=3\) is thin while every other allowed case is thick; and the locally Desargues example has full group \(S_7\times S_3\). ∎

## References and retained inputs

[U] *Marked groups, kernels and intersections*, companion manuscript, version 2. Results used here: U.Coset, U.RelativeBound, U.Relative, U.Maximal, U.FrattiniTransport and U.FrattiniLadder. Their statements and proofs form the shared algebraic dependency of this paper.

[BC98] F. Buekenhout and P. Cara, *Some properties of inductively minimal geometries*, Bulletin of the Belgian Mathematical Society–Simon Stevin **5** (1998), 213–219, DOI 10.36045/bbms/1103409005. The consulted complete authored text is the browser-rendered author upload; its diagram and formula rendering is imperfect. No identity with an unacquired PDF is assumed.

[BCD97] F. Buekenhout, P. Cara and M. Dehon, *Inductively minimal flag-transitive geometries*, in N. L. Johnson (ed.), *Mostly Finite Geometries*, Marcel Dekker, 1997, 185–190. B97 is retained in the exact form recalled in [BC98, Lemma 1 and the following paragraph]; the original chapter's proof is not reproduced or claimed independently read here.

[CC02] P. J. Cameron and P. Cara, *Independent generating sets and geometries for symmetric groups*, Journal of Algebra **258** (2002), 641–650, DOI 10.1016/S0021-8693(02)00550-1. The consulted source is the complete twelve-page author manuscript. Its source coset correspondence (G1)–(G3) is retained from pp. 7–8, with the references there to the general theory of Tits, Buekenhout and Hermand.

[W00] J. Whiston, *Maximal independent generating sets of the symmetric group*, Journal of Algebra **232** (2000), 255–268. W1 and the separate W2 are retained as stated in [CC02, pp. 3–4]; their original proofs and classification inputs are not rederived. Cayley's labelled-tree formula and the innerness of automorphisms of \(S_n\) for \(n\geq7\) are the other classical inputs used in the enumeration and action-isomorphism statements.

[ACK05] C. Archer, P. Cara and J. Krempa, *Using the Frattini Subgroup and Independent Generating Sets to Study RWPRI Geometries*, Beiträge zur Algebra und Geometrie **46**(1) (2005), 169–177. The complete published nine-page PDF is the consulted source. Its elementary finite-p-group Frattini quotient fact is retained from p. 174. U.Maximal uses Zorn's lemma in the infinite-group setting.

[GL21] N. Garcia-Colin and D. Leemans, *An infinite family of locally X graphs based on incidence geometries*, Art of Discrete and Applied Mathematics **4** (2021), #P3.01, DOI 10.26493/2590-9770.1328.902. The consulted institutional revised author manuscript is titled *An infinite family of incidence geometries whose incidence graphs are locally X*. Its Theorem 1.2 and Corollaries 1.3, 1.4, 4.8 and 5.1 provide the numbering used here; the earlier arXiv version has different numbering. No identity of the institutional PDF with the publisher's typeset text is presumed.

[Gas53] W. Gaschütz, *Über die Φ-Untergruppe endlicher Gruppen*, Math. Z. **58** (1953), 160–170. The structural theorem quoted in [ACK05, Theorem 4.1] remains an earlier input: a finite Frattini-free group with socle \(A\times D\), where \(A\) is the product of abelian simple factors and \(D\) of nonabelian simple factors, has form \(A\rtimes K\), with \(D=\operatorname{Inn}(A\times D)\leq K\leq\operatorname{Aut}(A\times D)\), and the maximal \(K\)-invariant subgroups of \(A\) have trivial intersection. This quoted result is not needed for any proof above and is not claimed as a new corollary.

[Arc04] C. Archer, *Direct sum decomposition of geometries based on maximal subgroups*, Journal of Geometry **79** (2004), 12–18. The primitive-group reduction quoted at the end of [ACK05, §4.3] remains earlier work: after removal of the action kernel, an RPRI geometry that is not a direct sum is reduced to a primitive-group action. It is neither a new target here nor an input used to obtain B.Coordinates.
