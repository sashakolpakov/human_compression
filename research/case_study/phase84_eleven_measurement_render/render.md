The question addressed here is whether the principal results of specified
research manuscripts can be recovered as short corollaries of a smaller
collection of proved ideas. The candidate intake is N001, N003, N008, L032,
L035, F013, F016, L088, N013, N016 and L108. Their exact versions, corrected scopes
and retained inputs are part of the mathematical contract. An intake list is
not a count of approved replacements, and this draft has no compression factor.

The useful object is a group with a distinguished family of parabolic
subgroups. Its chambers form a torsor when the action is regular: selecting a
base chamber identifies them with the group, and changing the base chamber
changes that identification by translation. Faces are the orbits of specified
parabolics. A finite torsor is representable by permutation matrices, but the
matrices do not eliminate the crucial information: one must retain the
marking, the parabolic partitions and their common-point properties. Ordinary
linear algebra alone neither proves the intersection property nor guarantees
that the resulting incidence system is a geometry.

The first common theorem isolates an exact obstruction. If two marked
subgroups have the correct intersection after applying a homomorphism, their
intersection before applying it is correct precisely when the kernel contains
no additional intersection. This gives both independent cyclic edge extensions
and the chirality-group criterion for a smallest regular cover. The proof is
one elementary lift of an element with prescribed image. Exact coset transport
through a kernel in the chamber stabilizer is another, separately proved,
statement: it preserves the whole geometry. Relative generation and a Frattini
ladder then turn finite p-group geometries into coordinate geometries, and
primitive saturation supplies the same base for the graded two-group argument.

Two further kinds of information remain essential. Forest cuts give actual
intersection partitions and laminar flag completion for symmetric groups;
these markings generally have no Boolean deletion maps. Endpoint conjugation
instead gives a subgroup of index at most two. Its algebraic obstruction is
an overlap and an intersection-closed support family, while a graph double
cover proves the required geometric flag completion. This operation handles
both the odd-endpoint J1 constructions and generalized-cube halving. The
coordinate section identifies the latter's toroidal lattices by a Gray-code
isomorphism of face posets and an exact affine marking, including the square
map's change of lattice basis. It never infers a geometry from its order alone.

A further operation keeps actual subsets of retained objects rather than
labelled copies of walks. The common retained-object theorem identifies its
exact permutation kernel and also supplies the old coset-core identity and
the endpoint operation's faithfulness. Thin Petrials still require their own
residue-cycle and face-shadow proofs; a general matrix change is not a
substitute for these hypotheses.

The full forest recognition, cyclic-core classification, model presentations,
FAP arguments, residue-extension census, local mirror identifications and
minimal-cover proof are printed below. Every required finite program is in an
appendix. Several substantial older inputs remain explicit, including B97,
Whiston's two separate inputs, Burnside, the cyclic core bound, the complete
order-256 and J1 subgroup catalogues, Danzer's general construction, the stated
Coxeter classifications, the geometric extension and oriented-polytope
interfaces, and the older five tight chiral families. None becomes free because
it appears in a shared notation.

The new integration preserves all source corrections: the unrestricted
infinite Frattini converse, F013's auxiliary kernel assertions, diagonal
translation counts, chiral facet embeddings, L088's exchanged figure labels,
N013's rank-three exception and N016's nonidentity-power wording. L108's
Petrial operation is now handled with its exact action kernel: the source's
unconditional embedding is corrected, while its principal obstruction and
valid numbered structural conclusions are proved in Section 23. No open
conjecture, new priority claim, or Lean verification of the complete geometry
is asserted.

The intended reconstruction is explicit: take a source statement in the
contract map, use its displayed corollary and the complete internal lemmas
named there, then retain only the declared background. The appendix programs
are part of that proof. Component reviews do not replace independent review
of this newly integrated text.

## 1. Conventions and all retained inputs

All type sets and forests are finite, as are the domains of the symmetric groups. The normal-quotient bounds and numerical invariants \(\mu,\mu^{\prime}\) are used for finite groups; the relative parabolic-generation formula and the Frattini results explicitly allow arbitrary groups with finite rank where stated. Their coset sets may be infinite. The p-group classification is for finite p-groups. Write \(S_\Omega\) and \(A_\Omega\) for the symmetric and alternating groups on \(\Omega\), and \(S_n=S_{\{1,\ldots,n\}}\). Products of permutation groups on disjoint subsets act trivially outside their indicated supports.

A family \(S=(s_i:i\in I)\) in \(G\) is **independent relative to** \(B\leq G\) if
\[
s_i\notin\langle B,s_j:j\ne i\rangle\qquad(i\in I).
\]
It is a relative generating family if additionally \(\langle B,S\rangle=G\). Let \(\mu(G,B)\) and \(\mu'(G,B)\) be the largest sizes of independent relative generating families and independent relative families respectively. Omit \(B\) when \(B=1\). For a group \(D\) acting on \(N\), a family in \(N\) is **\(D\)-independent** if no member belongs to the subgroup generated by the \(D\)-images of the other members; \(\mu'_D(N)\) is its maximum size. Relative strong independence means
\[
\langle B,s_i:i\in U\rangle\cap\langle B,s_i:i\in V\rangle
 =\langle B,s_i:i\in U\cap V\rangle \quad(U,V\subseteq I).
\tag{A1.1}
\]

A typed incidence geometry has a reflexive symmetric incidence relation, with distinct elements of the same type never incident. A flag is a pairwise incident set; a chamber has every type. Every flag of a geometry is required to extend to a chamber. Firmness means that every nonchamber flag extends to at least two chambers. A residue consists of the elements incident with a flag whose types do not occur in that flag. Residual connectedness requires connected incidence graphs in residues of rank at least two. We keep the specified group action as part of the pair. The N001/N003 source coset convention includes flag transitivity; for the firm-RWPRI assertions it follows from Lemma E0 below.

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
For the finite groups in the N001 branch, a subgroup is **quasi-maximal** if the interval from it to the ambient group in the subgroup lattice is a chain, equivalently if it has a unique saturated subgroup chain to that group; QPRI requires this for every element stabilizer. Property \((2T)_1\) means that each panel stabilizer is two-transitive on the rank-one residue. Property \((IP)_2\) means that each rank-two residue is either a complete bipartite graph or has at most one common neighbor for each pair of distinct same-type vertices. This last condition concerns geometric incidence, not equation (A1.1).

The diagram has one vertex for each type; two vertices are joined when their rank-two residue is not complete bipartite. An **end** of a connected diagram is a vertex whose deletion leaves a connected graph. A **middle** is a vertex whose deletion leaves at least two components, all of equal cardinality. This spells out the source's nonend requirement; in particular a one-vertex diagram has no middle. A finite firm flag-transitive pair of rank \(r\) and connected diagram is **minimal** if \(|G|\leq(r+1)!\), and **inductively minimal** if the pair at every residue with connected diagram is minimal, including the empty flag.

**Lemma E0 (residual weak primitivity and flags).** A finite-rank geometry on which a group acts residually weakly primitively is flag-transitive.

*Proof.* Fix a chamber. Starting with its empty flag, choose a remaining type on which that flag's stabilizer acts primitively, hence transitively. Given any second chamber containing the chosen flag, use that stabilizer to match its element of the chosen type to the fixed chamber's element. Repeat in the residue. At most \(|I|\) steps match any chamber to the fixed chamber. Thus the group is chamber-transitive. Every flag extends to a chamber, so it is transitive on flags of each fixed type. The fixed chamber's element stabilizers then give the usual coset representation: the typewise coset bijections preserve incidence because transitivity on incident pairs supplies a common representative. ∎

Thus the firm-RWPRI results below need no extra assumption of flag transitivity or residual connectedness. For a flag-transitive coset geometry, firmness gives distinct \(H_J\), and RWPRI gives a maximal next intersection at every proper \(J\). To see distinctness explicitly, firmness gives \(H_{I\setminus\{i\}}>B\); choose \(s_i\) in this difference. For \(J\ne K\), a type in one of their differences supplies an \(s_i\) that lies in one intersection and not the other.

The following are the unexpanded mathematical inputs.

**B97 (foundational classification).** Buekenhout–Cara–Dehon, *Inductively minimal flag-transitive geometries* (1997), as recalled in N001 Lemma 1 and the following paragraph: an inductively minimal pair of rank \(r\) is thin and residually connected and has group \(S_{r+1}\). Its connected diagram has no induced cycle longer than three, each edge lies in a unique maximal clique, and each vertex lies in one or two maximal cliques. Conversely every such connected diagram determines exactly one inductively minimal pair up to isomorphism. We retain the classification and uniqueness, not the four targeted property conclusions of the 1998 paper.

**W1 (Whiston bound and extremal generation).** An independent family in \(S_m\) has at most \(m-1\) members, and an independent family with \(m-1\) members generates \(S_m\). We use precisely this implication, not a converse asserting that every independent generating family has maximum size.

**W2 (Whiston omission consequence).** If \(n\geq7\) and \((s_i)\) is an independent generating family of \(S_n\) of size \(n-1\), each omission subgroup \(\langle s_j:j\ne i\rangle\) is intransitive, is transitive imprimitive with blocks of size two, or is \(A_n\). This is the separate consequence of Whiston's proof stated on page 4 of the 2002 manuscript. Its dependence on the classification of finite simple groups is retained. W2 is not deduced here from W1.

We also retain Cayley's formula: there are \(m^{m-2}\) trees on a specified labelled \(m\)-element set. Elementary group theory, permutation parity, and the equivalence of primitivity with maximality of a point stabilizer are used throughout. The source references for these inputs are given at the end. None of the declared target conclusions is used as background.



**PΦ (finite-p-group Frattini quotient).** For every finite p-group \(P\), the quotient \(P/\Phi(P)\) is an elementary abelian p-group, hence a finite-dimensional vector space over \(\mathbb F_p\). Here \(\Phi(P)\) is the intersection of the maximal subgroups. We retain this elementary group-theoretic fact in the form recalled in [ACK05], page 174. Zorn's lemma is retained for the explicitly infinite-group maximal-overgroup arguments. Neither input is a classification of p-group geometries.

For the action-isomorphism convention in Corollary B7, we retain the classical fact that every automorphism of \(S_n\) is inner for \(n\geq7\). Choosing instead the source's equivalence of conjugate coset data gives the same stated marking correspondence.

Two earlier results quoted in [ACK05] remain explicit source imports, not conclusions proved here. Its Theorem 4.1 quotes Gaschütz: if a finite Frattini-free group \(F\) has socle \(S=A\times D\), with \(A\) the product of abelian simple factors and \(D\) the product of nonabelian simple factors, then \(F=A\rtimes K\), where \(D=\operatorname{Inn}(S)\leq K\leq\operatorname{Aut}(S)=\operatorname{Aut}(A)\times\operatorname{Aut}(D)\), and the maximal \(K\)-invariant subgroups of \(A\) have trivial intersection. Its final paragraph quotes Archer's earlier reduction of RPRI geometries that are not direct sums to primitive group actions after removal of the action kernel. These retained results are not used to prove results E0–E5 or any of Corollaries C1–C11; their original proofs are outside this intake.

For a group marked by involutions \(r_i\), \(i\in V\), write
\(G_I=\langle r_i:i\in I\rangle\). Its intersection property (IP) is
\(G_I\cap G_J=G_{I\cap J}\) for all subsets. A string C-group has IP and
\([r_i,r_j]=1\) when \(|i-j|>1\); it is nondegenerate if consecutive
generators do not commute. Its type records their product orders. All marked
isomorphisms preserve the ordered generators. Write
\([x,y]=x^{-1}y^{-1}xy\), \(x^y=y^{-1}xy\), and \(D_8\) for the dihedral
group of order eight. The lower central series is \(\gamma_j(G)\).



We retain the regular-polytope/string-C-group correspondence, its marked
quotient/covering correspondence, and its coset face/stabilizer description.
We also retain Burnside's basis theorem, finite nilpotency of finite
two-groups, the lower-central graded Lie construction and generation in
degree one, and the Euclidean algorithm for Gaussian integers. The cyclic
core bound retained in §12 is stated there exactly. The geometric alternating
assembly and free-extension theorems retained in §15 are also stated exactly.
The amalgam normal-form theorem and completeness of the SmallGroups
order-256 catalogue are retained. The **relation-pattern census derived
from that catalogue** is a separately charged finite verification, not
another unnamed classification assumption. No main target from the four
source papers is accepted as background.

For finite p-groups, the PΦ input is used together with Burnside's basis theorem: irredundant generating markings map to bases of the Frattini quotient. Theorem S proves the required compatibility with every marked subgroup; that compatibility is not an imported classification. Equation labels beginning A or Q and theorem labels beginning Q are unique internal labels in this manuscript. They are not references to another manuscript. All necessary proofs are printed below.



### Oriented geometry and the additional retained inputs

We retain the following standard geometric correspondence, with its actual scope. Set
\[
 W_n=\langle r_0,\ldots,r_{n-1}\mid r_i^2=1,
 [r_i,r_j]=1\ (|i-j|>1)\rangle,
 \qquad U_n=W_n^+=\langle s_1,\ldots,s_{n-1}\rangle,
 \quad s_i=r_{i-1}r_i.
\]
The presentation of \(U_n\) has relations \((s_i\cdots s_j)^2=1\) for \(i<j\). Marked quotients of \(U_n\) satisfying the string \(C^+\) intersection property correspond to chiral or directly regular polytopes. Recursively, a marked quotient of rank at least three is such a group precisely when its facet and vertex-figure subgroups are such groups and their intersection is the medial subgroup. Rank two starts with a nontrivial cyclic group, including the infinite cyclic group; rank one has trivial rotation group. Direct regularity is equivalent to existence of the automorphism induced by conjugation with \(r_0\). Marked epimorphisms correspond to covers. The analogous quotients without the intersection property describe the relevant oriented maniplexes. This standard correspondence is retained, not proved by K.

We also retain the geometric section theorem: the facets of facets and the vertex-figures of vertex-figures of a chiral polytope are directly regular. This is the Schulte–Weiss result cited as Proposition 9 in the source. All sections of a directly regular polytope are directly regular. These are the only geometric ingredients needed to remove the local polytopality assumptions in the cover criterion. In particular, we do **not** retain the target's Proposition 2.2 or Theorem 3.1 as background.


For the operation branch we retain Danzer's regular lattice-polytope
construction and its full semidirect-product group in the exact form stated
in §20, the classical finite/affine/compact-hyperbolic Coxeter classifications,
and the standard convex-polytope orders used there. The particular toroidal
lattices are proved in §9. The J1 branch retains TomLib's complete forty-class
subgroup table and its ambient permutation model, together with exact GAP
group, coset and orbit algorithms; its original geometry census is not an
input. The chiral branch retains the older five classified tight families
and their embedded chirality property, stated exactly in §22.3. All these
are substantial charged inputs. In the general coset sections use left
cosets; the operation certificate uses right cosets. Inversion identifies
the conventions, and every common-point or subgroup assertion is invariant
under that conversion. The scripts use their own explicitly given convention.

## 2. Exact kernels, relative generation and the Frattini ladder

**Theorem K (intersection transport, exact coset transport and retained-object operations).**


**(0) Three-subgroup transport.** Let \(\pi:H\to Q\) be a homomorphism,
\(C\le A\cap B\le H\), and suppose
\(\pi(A)\cap\pi(B)=\pi(C)\). Then
\[
 A\cap B=C\quad\Longleftrightarrow\quad A\cap B\cap\ker\pi\le C.
 \tag{K0}
\]
*Proof of (0).* Only the reverse implication needs proof. Given
\(x\in A\cap B\), choose \(c\in C\) with \(\pi(c)=\pi(x)\).
Then \(xc^{-1}\in A\cap B\cap\ker\pi\le C\), so \(x\in C\).
No finiteness, centrality or global surjectivity is needed. This is the
generic algebraic statement formalized as
`LeemansLift.intersection_of_image_and_kernel`; the complete proof is here.

**(a) Marked intersections.** Let \(\pi:H\twoheadrightarrow Q\) preserve a marking, and suppose the image marking has IP. Put \(K=\ker\pi\), \(H_I=\langle r_i:i\in I\rangle\), and \(K_I=K\cap H_I\). Then the marking in \(H\) has IP if and only if \(K_I\cap K_J=K_{I\cap J}\) for all subsets.

*Proof of (a).* Apply (0) with
\(A=H_I\), \(B=H_J\), \(C=H_{I\cap J}\).
The image hypothesis is the quotient's IP, and the kernel condition is
exactly \(K_I\cap K_J=K_{I\cap J}\), since the reverse inclusion always
holds. This proves both directions. ∎

**(b) Exact coset transport.** If \(N\unlhd G\) and \(N\leq B\), the quotient map induces an isomorphism of typed pregeometries
\[
 gH_i\longmapsto (gN)(H_i/N)
\tag{A6.3}
\]
between the families in \(G\) and \(G/N\). It preserves all coset intersections, flags, chambers, residues, common-point witnesses, firmness, residual connectedness, flag-transitivity, RWPRI and RPRI. Subgroup families containing \(N\) correspond bijectively to quotient subgroup families.


*Proof of (b).* For the quotient homomorphism \(\pi\),
\[
\pi^{-1}\bigl(\pi(g)(H_i/N)\bigr)=gH_i.
\]
Thus corresponding cosets are in bijection and every intersection pattern is preserved, including common points of any family. This proves the incidence and flag claims, also for pregeometries lacking flag-transitivity. The acting groups have the same permutation image on the corresponding cosets. Subgroup correspondence preserves maximality in each interval above \(N\), including all residue intervals, which proves the primitive properties. The usual subgroup correspondence gives the final assertion. ∎


**(c) Retained-object operations and the faithful image.** Let G act on sets X and Y. Suppose there is a G-invariant subset Y₀⊆Y and an equivariant surjection p:Y₀→X. Suppose also that Y admits an injective equivariant encoding into a tagged disjoint union of finite products, each factor being X or its power set, with G fixing the tags. In particular, an element fixing X pointwise fixes every encoding. Then

\[
 N:=\ker(G\curvearrowright Y)=\ker(G\curvearrowright X)
   =\bigcap_{x\in X}G_x.
 \tag{Kc1}
\]

If X is the disjoint union of transitive G-sets with selected stabilizers H\_j, then

\[
 N=\bigcap_j\operatorname{core}_G(H_j)
   =\operatorname{core}_G\!\left(\bigcap_jH_j\right).
 \tag{Kc2}
\]

The induced faithful group is G/N. If it acts by type-preserving automorphisms of a thin residually connected finite-rank geometry on Y and is chamber-transitive, it is the full type-preserving automorphism group. For a chamber D and a panel F⊂D in that geometry, the stabilizers in G satisfy

\[
 G_D=N,\qquad [G_F:N]=2.
 \tag{Kc3}
\]

Thus G\_F of order two forces N=1. No finiteness of G or X is required.

*Proof.* An element fixing Y fixes X by the equivariant surjection. An element fixing X fixes each encoded element/subset and hence each uniquely encoded object of Y. This proves (Kc1). Every stabilizer in a transitive orbit is a conjugate of its selected H\_j. Intersecting those conjugates proves both equalities in (Kc2); the intersection is exactly the largest normal subgroup contained in every H\_j. The quotient is the faithful permutation image by the first isomorphism theorem. The chamber assertion follows from the free chamber action in Lemma O0 below: any automorphism agrees on a base chamber with an element of the transitive image, so their quotient fixes that chamber and is the identity. The preimage of its chamber stabilizer is N. Chamber transitivity makes G\_F transitive on the two chambers containing F, with stabilizer G\_D=N. The orbit–stabilizer bijection proves (Kc3), also for infinite G. ∎

The encoding hypothesis uses actual subsets, not independently labelled copies of the same subset. The theorem identifies a permutation image; it does not say that a changed generator list is a homomorphic image of the old marking.

**Lemma O0 (chamber galleries and residue stabilizers).** A residually connected geometry of finite rank has connected chamber graph. If it is thin, its full type-preserving automorphism group acts freely on chambers. In that thin case, if a subgroup G acts chamber-transitively, it therefore acts regularly and equals the full group. For the unique involution r\_i carrying a base chamber across its i-panel,

\[
 G=\langle r_i:i\in I\rangle,
 \qquad G_F=\langle r_i:i\notin t(F)\rangle
 \tag{O0}
\]

for every subflag F of the base chamber.

*Proof.* Induct on rank. Rank-one chambers are mutually adjacent. At larger rank, chambers containing an object are gallery-connected by induction in its residue. A path in the connected incidence graph, extending each incident pair to a chamber, then joins any two chambers by such galleries. This also applies inside every residue. In the thin case, an automorphism fixing a chamber fixes its unique neighbour across every panel, hence every chamber and every object. This proves freeness. A transitive subgroup exhausts the full free action. Its unique panel-changing element r\_i has square fixing the base chamber, so is a nonidentity involution. Reading an arbitrary gallery as successive panel changes proves generation. Reading a gallery inside the residue of F proves the stabilizer formula, since only types outside F change. ∎

### Marked torsors and geometric recognition


For this recognition interface a marking of a group G is an ordered family of nonidentity involutions r\_i generating G, indexed by a finite set I. For J⊆I write G\_J=⟨r\_j:j∈J⟩. The **intersection property**, abbreviated IP, is

\[
G_J\cap G_K=G_{J\cap K}\qquad(J,K\subseteq I).
\tag{O1}
\]

A marking satisfying (O1) is a C-group marking. Its maximal parabolics are P\_i=G\_(I\{i}). Right cosets P\_i g are objects of type i, with incidence given by nonempty intersection. The common-point property for every pairwise incident family of differently typed cosets will be called **typed Helly**. IP and typed Helly are separate requirements.

**Recognition lemma O1.1.** If a marking has IP and its maximal-parabolic cosets have typed Helly, their incidence system is a thin, residually connected geometry on which G acts regularly; G is its full type-preserving automorphism group.

**Proof.** A common coset point extends every flag to the chamber consisting of its cosets in all types. Translation takes every flag to its base flag. By IP, the stabilizer of a base flag of types S is G\_(I\S), the full chamber stabilizer is trivial, and a panel stabilizer is a group ⟨r\_i⟩ of order two. Thus panels have exactly two chambers. In a residue of rank at least two, its stabilizer G\_(I\S) is generated by its proper maximal parabolics: every remaining marker belongs to one of them. The word expressing an element in their union gives a walk in the residue incidence graph. Hence every such residue is connected. Lemma O0 now identifies the already regular G-action with the full type-preserving automorphism group. ∎

There is a convenient finite certificate for the second requirement. Put

\[
X_{ij}=\{P_i x:x\in P_j\},\qquad P_J=\bigcap_{j\in J}P_j.
\]

**Recognition lemma O1.2.** For a finite group, typed Helly is equivalent to

\[
\left|\bigcap_{j\in J}X_{ij}\right|
 =[P_J:P_J\cap P_i]
\quad(i\notin J,\ |J|\ge2).
\tag{O2}
\]

**Proof.** The cosets represented in P\_J form a subset of the intersection on the left, and their number is the right side. Equality of sizes is therefore equality of sets. Induct on the size of a flag. Normalize all but its last object to base cosets using the common point supplied inductively. The last coset lies in the left side of (O2), so has a representative in the common subgroup of those base cosets. This is a common point for the entire flag. Singletons and pairs start the induction. Conversely, typed Helly applied to such an anchored family gives the set equality and hence (O2). ∎

These lemmas apply to the actual orbit partitions of the regular G-torsor. Replacing each g by its permutation matrix loses no information, provided the distinguished parabolic partitions are retained. Linearity alone proves neither (O1) nor (O2).

**Theorem R (relative-generation core).**

(a) For finite \(G\) and \(N\unlhd G\),
\[
\mu(G)\leq\mu(G/N)+\mu'(N).
\tag{A4.1}
\]
If \(N\) is abelian, conjugation gives the sharper inequality
\[
\mu(G)\leq\mu(G/N)+\mu'_G(N).
\tag{A4.2}
\]

(b) A source coset geometry for finite \(G\), of rank \(r\) and Borel subgroup \(B\), has \(r\leq\mu'(G,B)\). More generally, for any finite-rank firm RWPRI geometry with specified group \(G\), possibly infinite, choose any
\[
s_i\in H_{I\setminus\{i\}}\setminus H_i.
\tag{A4.3}
\]
Then for every \(J\subseteq I\),
\[
H_J=\langle B,s_i:i\notin J\rangle.
\tag{A4.4}
\]
The family is strongly independent relative to \(B\). When \(G\) is finite, this also gives \(r\leq\mu(G,B)\).

*Proof.* For (a), take an independent generating family \(S\) and a subset \(T\subseteq S\) whose images minimally generate \(G/N\). For each \(s\in S\setminus T\), choose a word \(w_s\) in \(T\) with \(sN=w_sN\). The elements \(v_s=sw_s^{-1}\in N\) are independent: an expression for one in terms of the others would express \(s\) in terms of \(S\setminus\{s\}\). This proves (A4.1). If \(N\) is abelian, its conjugation action by \(G=N\langle T\rangle\) equals the action by \(\langle T\rangle\). The same substitution applies to expressions in conjugates of the other \(v_s\), proving \(G\)-independence and (A4.2).

For (b), (G1) makes the difference in (A4.3) nonempty, since its intersection with \(H_i\) is \(B\). For a general finite-rank firm RWPRI geometry, Lemma E0 gives flag transitivity and distinct intersections, so the same panel choices exist. Every other \(s_j\), as well as \(B\), lies in \(H_i\), so the family is independent relative to \(B\). This proves the first rank bound. Under (G4), prove (A4.4) downwards from \(J=I\). Choose \(k\notin J\) for which \(H_{J\cup\{k\}}\) is maximal in \(H_J\). The inductive hypothesis supplies its generators, while \(s_k\) belongs to \(H_J\) and not to that maximal subgroup. Adjoining it generates \(H_J\), proving (A4.4). Finally \(H_J\cap H_K=H_{J\cup K}\) becomes (A1.1), establishing strong relative independence. This part of the proof uses firmness and residual maximality, with no finiteness of \(G\) or separate assumption (G2). ∎

**Lemma E1 (relative finite generation supplies maximal overgroups).** Suppose \(G=\langle B,t_1,\ldots,t_r\rangle\) with finite \(r\). Every proper subgroup \(H\geq B\) is contained in a maximal subgroup of \(G\).

*Proof.* For finite \(G\), choose a proper overgroup of largest order. In general, order the proper overgroups of \(H\) by inclusion. The union of a chain is a subgroup; if that union were \(G\), a single member would contain the finitely many \(t_j\), and hence all of \(G\), a contradiction. Every chain therefore has a proper upper bound, and Zorn's lemma gives a maximal element. ∎

Let \(\Phi(G)\) denote the intersection of all maximal subgroups of \(G\), with the intersection equal to \(G\) if there are none. It is characteristic and hence normal. If every proper overgroup of \(B\) lies in a maximal subgroup, then
\[
\Phi(G)H=G,\ H\geq B\quad\Longrightarrow\quad H=G.\tag{A6.1}
\]
Indeed a maximal subgroup containing a proper \(H\) also contains \(\Phi(G)\). This hypothesis holds for finite \(G\), and more generally under Lemma E1. It is important to supply it when \(G\) is infinite.

### Containment and quotient actions

**Theorem E2 (normal-subgroup ladder).** Suppose all intersections \(H_J\), \(J\subseteq I\), are distinct and that some ordering of the types gives a maximal subgroup chain
\[
G=K_0>K_1>\cdots>K_r=B,\qquad K_j=H_{\{1,\ldots,j\}}.
\tag{A6.2}
\]
If \(N\unlhd G\) lies in every maximal subgroup of \(G\), then \(N\leq B\). The group may be infinite.

*Proof.* Choose \(t_j\in K_{j-1}\setminus K_j\). Each maximal inclusion gives \(K_{j-1}=\langle K_j,t_j\rangle\), so backwards induction gives \(G=\langle B,t_1,\ldots,t_r\rangle\). Lemma E1 implies that \(NH_i=G\) is impossible for a proper \(H_i\): a maximal overgroup of \(H_i\) would contain both factors.

Suppose \(N\not\leq B\), and let \(k\) be the first index with \(N\not\leq K_k\). Then \(N\leq K_{k-1}\), and normality and maximality give
\[
K_{k-1}=N(K_{k-1}\cap H_k).
\]
Suppose, in an upward step with \(1\leq j<k\), that \(K_j=N(K_j\cap H_k)\). Since \(N\leq K_{j-1}\),
\[
K_j\leq N(K_{j-1}\cap H_k)\leq K_{j-1}.
\]
Maximality permits only the endpoints. Equality with the lower endpoint would imply \(K_{j-1}\cap H_k\leq K_j\), and consequently
\[
K_{j-1}\cap H_k=K_j\cap H_k.
\]
These are different indexed intersections, because \(j<k\), contradicting distinctness. Thus equality with the upper endpoint holds. Repeating this step reaches \(G=NH_k\), the contradiction established in the first paragraph. ∎

RWPRI supplies (A6.2) by choosing a maximal next intersection repeatedly. Lemma E0 and firmness supply distinctness. With \(N=\Phi(G)\), Theorem E2 proves \(\Phi(G)\leq B\) for every finite-rank firm RWPRI geometry, including infinite \(G\). Its infinite proof does not assume that the whole Frattini subgroup is always superfluous.

**Corollary E3 (exact coset-kernel transport).** All assertions of Theorem K(b) apply whenever the normal subgroup lies in the Borel. This is the coset-geometry specialization of the common kernel theorem, including pregeometries and infinite groups.

The quotient by \(\Phi(G)\) is Frattini free: its maximal subgroups correspond to the maximal subgroups of \(G\), whose intersection is \(\Phi(G)\). If \(G\) has no maximal subgroups, then \(\Phi(G)=G\) and the quotient is trivial, giving the same conclusion. Applying K(c) with X=Y the typed coset objects gives the kernel
\[
\bigcap_i\operatorname{core}_G(H_i)
 =\operatorname{core}_G(B).
\tag{A6.4}
\]
It is the core from (Kc2); K(b) transports through it to the faithful action. Theorem E2 puts \(\Phi(G)\) inside this kernel.

The bijection here concerns indexed subgroup families with the quotient map fixed. It is not a claim that all automorphisms of \(G/\Phi(G)\) lift to \(G\), or that their respective automorphism orbits have equal counts. The source's stated incidence isomorphisms and its quotient-family correspondence are fully recovered without that extra assertion.

### Relative generators and the corrected infinite scope

**Theorem E4 (Frattini transport of relative generators).** Suppose every proper subgroup containing \(B\) is contained in a maximal subgroup of \(G\). For a finite indexed family \((s_i)\), it is an independent generating family of \(G\) relative to \(B\) if and only if its image is an independent generating family of \(G/\Phi(G)\) relative to \(B\Phi(G)/\Phi(G)\). In particular this holds for finite groups and for groups finitely generated relative to \(B\).

*Proof.* For \(H=\langle B,s_i:i\in I\rangle\), generation in the quotient means \(\Phi(G)H=G\), equivalent to \(H=G\) by (A6.1). Under generation, independence means that every deletion subgroup \(H_i'=\langle B,s_j:j\ne i\rangle\) is proper. Apply the same equivalence to each \(H_i'\): it is proper precisely when its image is proper in the quotient. This is exactly quotient independence. ∎

The unqualified printed infinite converse of N008 Theorem 2.1 is false. Let \(D=C_{p^\infty}\) be a Prüfer group and \(G=D\times C_2\). Every maximal subgroup of this abelian group has a cyclic prime-order quotient. Divisibility forces every homomorphism from \(D\) to such a quotient to be trivial. Hence \(D\times1\) is the unique maximal subgroup and equals \(\Phi(G)\). The one element generating the second factor generates \(G/\Phi(G)\), but does not generate \(G\). Taking \(B=1\) gives the advertised failure even for a one-element family.

This is a source-scope correction, not a new-priority claim. Theorem E4 gives the required finite version and a precise sufficient infinite hypothesis. If a finite family is already known to generate \(G\) relative to \(B\), Lemma E1 supplies the maximal-overgroup hypothesis, so its independence equivalence also survives for infinite \(G\). The independent proof of Theorem E2 remains valid in full infinite geometric scope.



## 3. One primitive-coordinate theorem and its geometry specialization

**Theorem S (primitive saturation and relative coordinates).** Let a finite p-group \(P\) have an irredundant generating marking \((r_i:i\in V)\), with \(|V|=d\), and put \(F=\Phi(P)\). For \(P_U=\langle r_i:i\in U\rangle\),
\[
 \Phi(P_U)=P_U\cap F,\qquad
 P_UF=\pi^{-1}\operatorname{span}(\bar r_i:i\in U),
 \quad [P:P_UF]=p^{d-|U|}.                           \tag{S.1}
\]
These saturated parabolics intersect according to intersection of label sets. Each omission subgroup has the unique maximal overgroup \(M_i=P_{V\setminus\{i\}}F\). Its coset action is the unique primitive coarsening of that omission action; all such actions together give the complete d-partite geometry with p elements of each type and faithful chamber-regular group \(P/F\).

More generally, if \(B\lhd P\), \(F\le B\), and \((s_i:i\in I)\) generates \(P\) irredundantly relative to \(B\), then \(P/B\) has basis \((s_iB)\) and
\[
 \langle B,s_i:i\in U\rangle/B
      =\operatorname{span}(s_iB:i\in U).                \tag{S.2}
\]
Its omission geometry is the complete \(|I|\)-partite p-point geometry. Finally, if the original marking consists of involutions and \(p=2\), then \(F=P'\), and \(\Phi(P_U)=P_U'\) for every parabolic.

*Proof.* Burnside's basis theorem makes \((\bar r_i)\) a basis of \(P/F\). The image of \(P_U\) has dimension \(|U|\), so its elementary abelian quotient has kernel \(P_U\cap F\) and order \(p^{|U|}\). It follows that \(\Phi(P_U)\le P_U\cap F\). Since \(P_U\) has \(|U|\) generators, Burnside gives \([P_U:\Phi(P_U)]\le p^{|U|}\); equality of the two bounds proves the kernel identity. The inverse-image, intersection and index assertions follow from coordinate subspaces. Every maximal subgroup contains \(F\) and has index p; containing an omission subgroup therefore forces equality with the preimage of its coordinate hyperplane. This proves uniqueness and primitivity. Cosets prescribe independent coordinate values; every assignment extends to a vector. Their intersection kernel is \(F\), and the quotient translations act regularly on chambers.

For the relative assertion, \(P/B\) is elementary abelian because \(B\ge F\). The images span, and a nontrivial linear relation would express one \(s_i\) modulo \(B\) in terms of the others, contrary to irredundancy. They therefore form a basis, proving (S.2) and the same coordinate-geometry statements. For involution generators, the abelianization is elementary abelian of exponent two. Thus \(P'\le\Phi(P)\), while the elementary abelian quotient by \(P'\) gives \(\Phi(P)\le P'\). The same argument applies to each parabolic. ∎


**Theorem E5 (the coordinate specialization of (A4.4)).** Let \(P\) be a finite p-group and let a firm RWPRI coset geometry for \(P\) have rank \(r\) and Borel \(B\). Then \(B\unlhd P\), \(P/B\cong\mathbb F_p^r\), and in a suitable basis \((v_i)\) of \(P/B\),
\[
H_J/B=\operatorname{span}\{v_i:i\notin J\}
\qquad(J\subseteq I).
\tag{A6.5}
\]
Consequently every type has \(p\) elements, every choice of one element of each type is a chamber, the geometry is RPRI, and it is the direct sum of \(r\) primitive rank-one geometries. Its faithful group \(P/B\) acts regularly on chambers.

*Proof.* The normal-subgroup ladder E2 gives \(\Phi(P)\le B\). Since \(P/\Phi(P)\) is abelian, \(B\) is normal. Theorem R(b) supplies the irredundant relative marking and every parabolic formula. Apply the relative clause (S.2) of Theorem S: it gives the stated basis and all coordinate cosets. Every assignment is a chamber; fixing a further coordinate has index p, hence is maximal. Therefore the geometry is RPRI and a direct sum of primitive p-point geometries. Its action kernel is \(B\) by normality and Theorem K(b), and the quotient translations act regularly on chambers. ∎

Conversely, writing \(d=\dim P/\Phi(P)\), any \(r\) independent linear functionals on that vector space, each considered up to nonzero scalar, give the full collection of examples of rank \(1\leq r\leq d\) by pulling back their kernels. Indeed a basis of \(P/B\) in E5 supplies exactly those quotient coordinate functionals. Every resulting family is firm, flag-transitive, residually connected and RPRI by coordinate assignments. For clarity this also gives the exact number of **indexed subgroup families**, not automorphism orbits:
\[
\frac{\prod_{j=0}^{r-1}(p^d-p^j)}{(p-1)^r}.
\tag{A6.6}
\]
The numerator chooses independent ordered functionals; independent rescaling does not change their kernels. This converse and count are useful extra consequences of the common theory, not extra source targets or an asserted new result.

Two subsidiary source statements need only elementary arguments. For two subgroups \(H_1,H_2\), every left coset of one intersects every left coset of the other exactly when \(H_1H_2=G\), since \(gH_1\cap hH_2\ne\varnothing\) is equivalent to \(g^{-1}h\in H_1H_2\). This is the rank-two direct-sum criterion. If \(U,W<V=\mathbb F_p^k\), with \(U\) a hyperplane, \(U\cap W\) a hyperplane of \(U\), and \(W\not\subseteq U\), then the image of \(W\) in \(V/U\) is one-dimensional. Therefore \(\dim W=(k-2)+1=k-1\), giving the source's maximal-subspace lemma.

### Every residue supplies a Frattini test

For every proper \(J\subsetneq I\), apply E2 inside the residue group \(H_J\). The Borel of that residue is still \(B\), since
\[
\bigcap_{i\notin J}(H_J\cap H_i)=B.
\]
Thus every firm RWPRI geometry satisfies
\[
\Phi(H_J)\leq B\leq H_{J\cup\{i\}}
\qquad(i\notin J).
\tag{A6.7}
\]
This is a necessary rejection test on candidate residue groups. It neither asserts sufficiency nor assumes \(\Phi(H_J)\leq\Phi(G)\). No runtime improvement for a particular enumeration follows from the proof alone.

## 4. Symmetric groups from forest cuts and laminar flags

Let \(T\) be a tree with vertex set \(V\) and edge set \(E\). Give each vertex a nonempty block \(B_v\), with the blocks pairwise disjoint, and put \(\Omega=\bigsqcup_vB_v\). For \(F\subseteq E\), let
\[
K_F=\prod_C S_{\bigcup_{v\in C}B_v},
\tag{A2.1}
\]
where \(C\) runs over the components of the forest \((V,F)\). Root \(T\), and let \(A_e\subseteq\Omega\) be the union of blocks on the side of \(T-e\) away from the root. Set \(H_e=K_{E\setminus\{e\}}=S_{A_e}\times S_{\Omega\setminus A_e}\).

**Theorem F (forest intersections and flag completion).** The following hold.

1. \(K_F\cap K_D=K_{F\cap D}\). Moreover \(K_F\) is generated by \(K_\varnothing\) together with the groups \(K_{\{e\}}\), \(e\in F\).
2. The coset system of the \(H_e\) is a firm, residually connected, flag-transitive geometry. Its type-\(e\) elements identify with the \(|A_e|\)-subsets of \(\Omega\), and distinct types satisfy
   \[
   X_e\mathrel{*}X_f\quad\Longleftrightarrow\quad
   |X_e\cap X_f|=|A_e\cap A_f|.
   \tag{A2.2}
   \]
3. Its Borel subgroup is \(K_\varnothing=\prod_vS_{B_v}\). The residue whose remaining types are \(F\) is the join of the same constructions on the nontrivial components of \((V,F)\). Its acting group is \(K_F\); components with no edges contribute only a kernel on this residue.

*Proof.* A permutation belongs to both groups in (1) exactly when it preserves every intersection of their component blocks. Two vertices lie in a common block of both forests precisely when their unique tree path belongs to both edge sets. Thus the common refinement is the component partition for \(F\cap D\). Transpositions inside the blocks, together with transpositions joining adjacent blocks along retained edges, connect each component; they generate its full symmetric group. This proves (1).

The coset \(gH_e\) maps to \(gA_e\). Two pairs of subsets are conjugate under \(S_\Omega\) exactly when their four Boolean atoms have the same sizes, giving (A2.2). The sets \(A_e\) are laminar: any two are nested or disjoint. Equation (A2.2) forces the identical nesting and disjointness relations on any pairwise incident family \((X_e)\). Add \(\Omega\) as a top container. From each selected container subtract its maximal selected proper subcontainers. These differences partition \(\Omega\), and the corresponding differences for the \(A_e\) and \(X_e\) have equal sizes. Bijections between these atoms combine into a single permutation sending every selected \(A_e\) to \(X_e\). This proves (G3) for every partial flag.

Repeated use of (1) gives \(H_J=K_{E\setminus J}\). Different edge sets give different component partitions and different groups, since every block is nonempty and adding an edge allows a transposition between its two sides. Thus (G1) holds. If at least two edge types remain, the groups obtained by deleting each remaining edge collectively contain \(K_\varnothing\) and each remaining one-edge group, proving (G2). The coset criterion gives the geometry assertions. Its residue group and its subgroups factor over the forest components; all elements from different components are incident, which gives the stated join and the kernel convention. ∎

For unit blocks \(B_v=\{v\}\), write \(\tau_e\) for the endpoint transposition of \(e\). The theorem says
\[
K_F=\langle\tau_e:e\in F\rangle
 =\prod_C S_C,\qquad K_\varnothing=1.
\tag{A2.3}
\]
This is the unweighted model used for N001. The weighted formulation costs only a change of notation and will also supply the flag completion for the parity construction.

**Theorem P (sign-kernel extension).** Let the blocks be singletons and distinguish an edge \(d\), with \(s=\tau_d\). For \(e\ne d\), choose \(\epsilon_e\in\{1,-1\}\) and put
\[
r_d=s,\qquad r_e=(s\tau_e)^{\epsilon_e}.
\tag{A2.4}
\]
For \(U\subseteq E\), set \(F(U)=\{d\}\cup(U\setminus\{d\})\). Then
\[
\langle r_e:e\in U\rangle=
\begin{cases}
K_{F(U)},&d\in U,\\
K_{F(U)}\cap A_\Omega,&d\notin U.
\end{cases}
\tag{A2.5}
\]
Both the ordinary marking \((\tau_e)\) and (A2.4) generate \(S_\Omega\), are independent, and satisfy the full subset intersection property (A1.1) with \(B=1\).

*Proof.* Inverting an individual generator leaves its cyclic subgroup unchanged. If \(s\) is included, \(s\) and \(s\tau_e\) recover \(\tau_e\), proving the first case. The sign kernel of \(K_F\), for \(d\in F\), is generated by the \(s\tau_e\), \(e\in F\setminus\{d\}\): every even word in edge transpositions is a product of pairs, and
\[
\tau_e\tau_f=(s\tau_e)^{-1}(s\tau_f),\qquad s\tau_d=1.
\]
This proves the second case, including the empty set, since \(K_{\{d\}}\cap A_\Omega=1\). Intersect (A2.5) using Theorem F and the sign condition. Since \(F(U)\cap F(V)=F(U\cap V)\), the result is exactly the subgroup for \(U\cap V\). The same conclusion for ordinary markings follows from (A2.3). Omitting an ordinary edge or a twisted label \(e\ne d\) leaves its cut invariant; the omitted generator crosses that cut. Omitting \(r_d\) leaves only even permutations, whereas \(r_d\) is odd. These observations prove independence and the generation assertions. ∎

## 5. Two-block overgroups and inductively minimal property tests

**Lemma O (two-block overgroups).** Let \(\Omega=A\sqcup C\), with \(a=|A|\), \(c=|C|\) positive, and put \(H=S_A\times S_C\). If \(a\ne c\), or \(a=c=1\), then \(H\) is maximal in \(S_\Omega\). If \(a=c\geq2\), its only proper strict overgroup is the unordered two-block stabilizer
\[
W=(S_A\times S_C)\rtimes C_2,
\]
which is maximal and satisfies \([W:H]=2\). In all cases the subgroup interval \([H,S_\Omega]\) is a chain. A positive weighted tree has at most one edge whose two sides have equal total weight.

*Proof.* The case \(a=c=1\) is immediate. The group \(H\) contains the transpositions within each of its two blocks. If an overgroup element does not preserve their unordered partition, its conjugates of these transpositions include one crossing the original blocks. Together with the original within-block transpositions the support graph is connected, so these transpositions generate \(S_\Omega\). This remains valid when one block is a singleton: a permutation moving that singleton produces a cross-block conjugate from the other block. Thus a proper overgroup must preserve the unordered partition. That stabilizer equals \(H\) when the sizes differ and has index two over it when they agree. Its only further overgroup is \(S_\Omega\), by the same argument.

If an edge bisects the total weight, the side of any other edge away from it is a proper positive-weight subset of one of its halves. It has strictly less than half the total weight and cannot be a bisecting side. ∎

**Proposition I (unweighted tree property profile).** For a tree \(T\) on \(N\geq2\) vertices, the geometry of Theorem F with unit blocks has rank \(N-1\), group \(S_N\), and diagram \(L(T)\), the line graph of \(T\). It is inductively minimal, satisfies RWPRI, \((2T)_1\), and \((IP)_2\), and has the following exact properties:

* PRI holds if no edge bisects \(N\), with the additional primitive case \(N=2\).
* Every element stabilizer is quasi-maximal. Failure of PRI is equivalent to a middle in \(L(T)\).
* RPRI holds exactly when \(T\) is a star, equivalently when \(L(T)\) is complete.

*Proof.* Equation (A2.3) gives trivial chamber stabilizer and two elements in each panel; the panel group is \(S_2\), proving thinness and \((2T)_1\). A two-edge forest consists either of a three-vertex path or of two disjoint edges. The corresponding rank-two residue is respectively a six-cycle or a complete bipartite graph \(K_{2,2}\). Consequently the diagram is \(L(T)\) and \((IP)_2\) holds.

Each connected remaining edge set with \(m\) edges is a subtree with \(m+1\) vertices; its residue group is \(S_{m+1}\), while all other vertices are isolated and contribute trivial factors. This verifies inductive minimality. In any nonempty forest residue choose a leaf of a nontrivial component. Its edge cut gives a point stabilizer in that component's symmetric group. This is maximal, and multiplying by the other factors preserves maximality. Thus RWPRI holds.

Lemma O gives the global PRI and quasi-maximality tests. Removing the vertex \(e\) from \(L(T)\) leaves the line graphs of the two sides of \(T-e\), with respective cardinalities \(a-1\) and \(N-a-1\); an empty side of this diagram corresponds to a leaf cut. A middle therefore exists exactly when an edge has \(a=N-a\geq2\), which is exactly failure of PRI. For \(N=2\) there is no middle and the pair is primitive.

Every nontrivial subtree of a star is again a star, and every edge cut of a star is a leaf cut, so its residues are PRI. A nonstar tree contains a three-edge path. The residue on those three edges is an \(S_4\) geometry with a \(2+2\) middle cut; its stabilizer \(S_2\times S_2\) is not maximal by Lemma O. Thus RPRI fails. Finally, a tree has pairwise adjacent edges exactly when it is a star, proving the line-graph formulation. ∎

**Lemma D (diagram recognition).** Every connected graph satisfying the three diagram conditions in B97 is the line graph of a tree, unique up to isomorphism. Hence B97 identifies every inductively minimal pair with one of Proposition I.

*Proof.* For a diagram with at least two vertices, make a vertex for each maximal clique. A diagram vertex in two maximal cliques gives an edge between the corresponding clique vertices; a diagram vertex in one maximal clique gives an edge from its clique vertex to a new leaf. Two distinct maximal cliques meet in at most one vertex, since a shared edge would violate the unique-clique condition. Thus the resulting graph has no loops or parallel edges. It is connected, and its edge labels are the original diagram vertices, with exactly their original adjacencies.

A shortest cycle of length at least four in this graph would give an induced cycle of that length on its edge labels in the diagram. A triangle would give three pairwise adjacent edge labels, which extend to a maximal clique; its three pairwise edges would then violate uniqueness of the maximal cliques already represented at the three cycle vertices. Both cases are impossible. The constructed graph is therefore a tree. Conversely the maximal cliques in the line graph of a tree are its nontrivial edge stars, so this construction recovers the tree. A one-vertex diagram corresponds separately to the one-edge tree. Proposition I constructs an inductively minimal pair for every such diagram; the uniqueness in B97 identifies it with the given pair. ∎

## 6. Extremal symmetric markings

**Lemma M (the two-point-block obstruction).** If \(m\geq4\) and \(H\leq C_2\wr S_m\) is transitive on its \(2m\) points, then \(H\) cannot have an independent generating family of size \(2m-2\).

*Proof.* Let \(N\) be the block kernel, a subspace of \(\mathbb F_2^m\), and let \(P=H/N\leq S_m\) be the transitive block action. W1 bounds \(\mu(P)\leq m-1\). We first have \(\mu'_H(N)\leq m-1\). This is automatic if \(N\) is proper. If \(N=\mathbb F_2^m\) and an \(H\)-independent family had \(m\) elements, it would be a vector-space basis. For each omitted basis vector, the span of the orbits of the others is proper but contains their hyperplane, so that hyperplane is invariant. Intersecting these hyperplanes shows that every basis line is invariant. Over \(\mathbb F_2\) every such line is pointwise fixed, contradicting the nontrivial transitive block action.

If an independent generating family of size \(2m-2\) existed, Theorem R would give
\[
2m-2\leq\mu(H)\leq\mu(P)+\mu'_H(N)\leq2m-2.
\]
Equality forces \(\mu(P)=m-1\); applying W1 to that family in \(S_m\) gives \(P=S_m\). Every nonconstant vector \(v\) in an \(S_m\)-invariant subspace generates a submodule containing the even-weight space: for coordinates with different entries, \(v+(ij)v=e_i+e_j\), and the orbit of this vector spans the even-weight space. That space has codimension one. Therefore an \(S_m\)-independent family containing \(v\) can have at most one further member; a family of constant vectors has at most one member. Consequently \(\mu'_H(N)\leq2\), and (A4.2) now gives \(2m-2\leq m+1\), contradicting \(m\geq4\). ∎

**Theorem E (extremal recognition).** Assume \(n\geq7\). Every independent family of \(n-1\) elements of \(S_n\) is an ordinary tree marking (A2.3) or a sign-kernel marking (A2.4). If the family is independent relative to \(B\leq S_n\), then \(B=1\).

*Proof.* By W1 the family generates \(S_n\). For its omission groups \(G_i\), W2 and Lemma M exclude the two-point-block case: in that case \(n=2m\geq8\), and the remaining \(n-2\) generators are an independent generating family for \(G_i\). At most one \(G_i\) is \(A_n\), because its omitted generator must be the unique odd member. Label a possible exception by \(1\).

For each \(i>1\), choose an edge \(e_i=\{x,s_i(x)\}\) crossing two \(G_i\)-orbits. Such an edge exists, since otherwise every generator would preserve those orbits. Choose \(e_1\) from any moved point of \(s_1\). If all the omission groups are intransitive, choose \(e_1\) crossing its own omission orbits as well. For \(j\ne i\), the edge \(e_j\) lies inside a \(G_i\)-orbit because \(s_j\in G_i\). Thus a cycle cannot contain \(e_i\) for \(i>1\): the remaining edges would give a path within a \(G_i\)-orbit between its endpoints. A cycle cannot consist of \(e_1\) alone. The \(n-1\) edges therefore form a tree on the \(n\) points.

Deleting \(e_i\), for \(i>1\), leaves two connected sets each contained in a \(G_i\)-orbit; intransitivity makes them exactly its two orbits. Hence \(s_j\) preserves this cut whenever \(j\ne i\). Intersect these cut stabilizers using Theorem F. It follows that \(s_1\in K_{\{e_1\}}\), so \(s_1=\tau_{e_1}\), and that \(s_i\in K_{\{e_1,e_i\}}\). If every omission group is intransitive, include the first cut too to obtain \(s_i=\tau_{e_i}\) for every \(i\). Otherwise \(G_1=A_n\), and all other generators are nonidentity even elements of the two-edge group. For adjacent edges that group is \(S_3\), whose nonidentity even elements are the two inverse three-cycles; for disjoint edges it is \(C_2\times C_2\), with a unique nonidentity even element. These are precisely \((s_1\tau_{e_i})^{\pm1}\), giving (A2.4).

Now suppose the original family is independent relative to \(B\). It is independent in the ordinary sense, so the preceding classification applies. By Theorems F and P its omission groups are the tree-cut stabilizers, except that in the sign-kernel case the distinguished omission group is \(A_n\). At each maximal omission group independence forces \(B\leq G_i\); otherwise \(\langle B,G_i\rangle=S_n\). A pendant edge different from the distinguished edge exists and yields a point stabilizer, so \(B\) fixes a point. At a nonmaximal cut, Lemma O forces \(B\) into the unordered two-block stabilizer. Its elements outside the ordered stabilizer interchange the halves and fix no point. Thus \(B\leq G_i\) here also. Strong independence from Theorems F and P gives \(B\leq\bigcap_iG_i=1\). ∎

## 7. Recognition of all maximum-rank symmetric geometries

**Theorem G (geometry recognition).** For \(n\geq7\), each marking in Theorem E gives an RWPRI coset geometry with its omission subgroups. Conversely every source coset geometry of \(S_n\) of rank \(n-1\) is one of these, and has trivial Borel subgroup. Among RWPRI geometries the correspondence is bijective after simultaneous conjugation and independent inversion of the marking generators; sets are unordered, so type renaming is understood.

*Proof of existence.* Strong independence and generation give (G1) and (G2). Theorem F supplies (G3) for ordinary markings, and the leaf argument of Proposition I supplies (G4).

For a sign-kernel marking, contract \(d\) to a vertex of weight two. Its other omission groups are precisely the cut stabilizers of this weighted tree, while the distinguished omission group is \(A_n\). Theorem F gives a common representative for the cut types of any flag. Every intersection of these cut stabilizers contains the odd transposition \(s\). Multiplying the representative on the right by \(s\) changes its parity without changing any of its cut cosets, so it can satisfy the parity coset too. This proves (G3).

To prove (G4), if parity is not yet fixed, choose that type: the even subgroup has index two in the residue group, because the latter contains \(s\). If parity is fixed, the residue group is the even part of a product of forest symmetric groups, and the component containing \(d\) still contains that edge. If another component has an edge, choose a leaf cut there. Projection from the residue group onto that component's symmetric group is surjective, since the \(d\)-component supplies an odd correction. The new stabilizer is the inverse image of a maximal point stabilizer, so is maximal. If only the \(d\)-component is nontrivial and a type remains, it has at least three vertices and a leaf other than the two endpoints considered together as the distinguished block. More explicitly, every tree with at least three vertices has a leaf not belonging to a specified edge's two endpoints unless that edge is the whole tree; such a leaf supplies a remaining cut. The group on this component is its alternating group. Its natural action is primitive: for degree at least four it is two-transitive (adjust the parity of a map of an ordered pair by swapping two remaining points), and \(A_3\) is regular of prime degree. The leaf stabilizer is again maximal. This proves (G4).

*Proof of uniqueness in the RWPRI case.* Theorem R and then Theorem E give \(B=1\), a classified marking, and equality (A4.4) for all parabolics. Each panel group is cyclic of order two or three. A generator of it is therefore unique up to inversion. Moving the chosen chamber conjugates all stabilizers and generators together; renaming types reorders the set. Conversely those operations give the same group–geometry pair. Here isomorphisms intertwine the specified \(S_n\)-action, up to an automorphism of \(S_n\); for \(n\geq7\) all such automorphisms are inner, an elementary symmetric-group fact retained for this formulation. Equivalently one may use the source convention of conjugate coset data throughout.

*Proof for arbitrary maximum-rank geometries.* This step does not assume (G4). Choose \(s_i\) as in (A4.3); they are independent relative to \(B\). W1 gives ordinary generation and Theorem E gives \(B=1\) and the two marking families. Let \(G_i=\langle s_j:j\ne i\rangle\). Then
\[
G_i\leq H_i<S_n.
\]
Lemma O and the maximality of \(A_n\) show that \(H_i=G_i\), except possibly at one balanced cut \(k\), where \(H_k\) might be its unordered stabilizer \(W_k\). Every other tree edge has a nonempty cut side wholly in one \(k\)-half. Its stabilizer cannot interchange those halves, so
\[
W_k\cap G_j\leq G_k
\tag{A5.1}
\]
for every such cut type \(j\ne k\).

Consider a panel intersection \(\bigcap_{j\ne i}H_j\). If it omits \(k\), it is already the corresponding intersection of the \(G_j\). If it contains \(k\), it also contains another cut type \(j\ne i,k\), since there are \(n-1\geq6\) types and at most one is a parity type. Equation (A5.1) again lets us replace \(W_k\) by \(G_k\). All panels therefore coincide with those of the marking and equal \(\langle s_i\rangle\). Starting from panels and using (G2) downwards now gives \(H_J=\langle s_i:i\notin J\rangle\) for every \(J\). In particular every \(H_i=G_i\); the geometry is one already proved RWPRI. ∎

## 8. Deletion maps, compatible products and cyclic edge kernels

**Lemma Q2.2 (Boolean deletion).** Suppose every assignment
\(e_S(r_i)=r_i\) for \(i\in S\), \(e_S(r_i)=1\) otherwise, extends to an
endomorphism. Then \(G\) has IP,
\(e_Se_T=e_{S\cap T}\), and
\[
 G=\ker(e_S)\rtimes G_S,
 \qquad \ker(e_S)=\langle\!\langle r_i:i\notin S\rangle\!\rangle.
\]

**Proof.** Endomorphisms agreeing on the generators agree everywhere. The
image and fixed subgroup of \(e_S\) are \(G_S\). For
\(x\in G_S\cap G_T\), \(x=e_S(x)\in e_S(G_T)=G_{S\cap T}\). The kernel
contains the displayed normal closure. Quotienting by that closure leaves
the retained generators, and the induced retraction fixes them; hence its
kernel is trivial. Splitting follows because \(e_S|_{G_S}=1\). ∎

The FAP at a face or coface is precisely the corresponding split product
with the normal closure of a final or initial interval of generators. Thus
Boolean deletion implies every such FAP, including those in the contract.

**Theorem Q2.3 (compatible products).** Let \(A,B\) have Boolean deletions,
with label sets overlapping in \(S\), and identify their \(S\)-parabolics
by the marking as \(C\). Their deletion maps give \(p_A:A\to C\) and
\(p_B:B\to C\). Then
\[
 P=A\times_C B=\{(a,b):p_A(a)=p_B(b)\}
   =(\ker p_A\times\ker p_B)\rtimes C
\]
is generated by the common diagonal generators and the exclusive
generators in their respective coordinates. It has Boolean deletions,
embeds both marked factors, and, if finite,
\( |P|=|A||B|/|C|\). Two generators appearing together in neither factor
commute.

**Proof.** The indicated generators include the section
\(a\mapsto(a,p_A(a))\), its analogue for \(B\), and therefore all
\((1,bp_B(b)^{-1})\). Equivalently the exclusive generators normally
generate each kernel, by Lemma Q2.2. They generate the displayed semidirect
product. Coordinatewise deletion preserves compatibility: both separator
images are deleted on exactly \(S\cap I\). Lemma Q2.2 gives IP, and the
sections, order formula and commutation assertions are immediate. ∎

We will also use a non-split variant with cyclic kernels. Let \(B\) have
IP and retractions to chosen two-generator subgroups
\(B_e=\langle b_i,b_j\rangle\), killing all other markers. Suppose
\(q_e=|b_ib_j|\) is even. For each chosen pair choose a multiple \(m_e\)
and a dihedral group \(D_e=\langle u_e,v_e\rangle\) of order \(2m_e\),
mapping by its reflections to \(B_e\). Form the simultaneous fiber product
of \(B\) and the \(D_e\) over these maps, with the evident marked tuples.

**Theorem Q2.4 (independent edge inflation).** These tuples generate the
whole fiber product \(H\), with
\[
 |H|=|B|\prod_e(m_e/q_e),\qquad
 K=\ker(H\to B)=\prod_e C_{m_e/q_e},\qquad
 K\cap H_I=\prod_{e\subseteq I}C_{m_e/q_e}.                 \tag{Q2.1}
\]
It has IP. Chosen pair orders become \(m_e\), and all other pair orders
remain their base values. Thus string diagrams give string C-groups.

**Proof.** The word \((r_i r_j)^{q_e}\) is a generator of the \(e\)-kernel
and trivial in every other coordinate: another chosen pair contains at
most one of its endpoints, so evenness kills that reflection. These words
generate the entire kernel, while the tuples project onto \(B\). The
same word lies in \(H_I\) when \(e\subseteq I\). Otherwise its coordinate
in \(H_I\) is at most a single reflection subgroup and meets the rotation
kernel trivially. This proves (Q2.1); its coordinate intersection law and
Theorem K(a) prove IP. For an unchosen pair, a coordinate projection is a
base pair, a single reflection, or the identity. Its order divides the
base pair order because its projection onto \(B_e\) has that same order.
An odd-order base pair cannot meet a chosen edge at exactly one endpoint,
since the retraction would map its product to an involution. Hence the
extra coordinates cannot increase an unchosen pair order. ∎

Finally, if a marked presentation \(P\) has finite normal subgroups
\(A_1,\ldots,A_h\) of orders at most \(a_i\), and its quotient by their
product has at most \(b\) elements, then
\( |P|\le b\prod_i a_i\). A constructed marked quotient of exactly that
order identifies the presentation itself. The proof uses successive
product cardinalities; it does not assume the normal factors commute or
intersect trivially. We call this the **order comparison principle**.

## 9. The common square-lattice seed

Let
\[
 a(x,y)=(-x,y),\quad b(x,y)=(y,x),\quad c(x,y)=(x,1-y).
\]
These generate \(W=\mathbb Z^2\rtimes D_8\), of type \(\{4,4\}\), with
\(ac=ca\). Its presentation is
\[
 W=\langle a,b,c\mid a^2=b^2=c^2=(ab)^4=(bc)^4=(ac)^2=1\rangle. \tag{Q3.1}
\]
Here is an algebraic normal-form proof. Put \(d=bab\), \(y_0=cd\), and
\(x_0=by_0b\). The relations give \([a,d]=1\), \([a,y_0]=1\),
\(dy_0d=y_0^{-1}\), \(ax_0a=x_0^{-1}\), and conjugation by \(b\) swaps
\(x_0,y_0\). Substitution of \(bc=x_0ab\) makes \((bc)^4=1\) equivalent
to \([x_0,y_0]=1\). Thus every word collects to \(x_0^u y_0^v M\),
\(M\in\langle a,b\rangle=D_8\). In the affine model \(x_0,y_0\) are the
unit translations, so these forms are distinct. This proves (Q3.1).

For \(n\ge5\), define the invariant lattice
\[
 \Lambda_n=\begin{cases}
  2^e\mathbb Z^2,&n=2e+3,\\
  2^e\langle(1,1),(1,-1)\rangle,&n=2e+4,
 \end{cases}\qquad e\ge1,
\]
and put \(H_n=W/\Lambda_n\). Its order is \(2^n\); the full linear
\(D_8\) coordinate is retained, even if its action on the vertex quotient
is not faithful. Its pair orders are \(4,4,2\).

Write \(T=abcb\), \(U=cbab\), translations by \((-1,0)\), \((0,1)\).
The extra relators for \(H_n\) can be taken as \(T^{2^e},U^{2^e}\) in
the square case, and \(T^{2^e}U^{2^e},T^{2^e}U^{-2^e}\) in the diagonal
case. After deleting any marker, both \(T,U\) have order at most two:
deleting \(a\) leaves conjugates of \(c\), deleting \(c\) leaves
conjugates of \(a\), and deleting \(b\) leaves \(ac,ca\). Therefore
every lattice relator survives every deletion. The even Coxeter relators
also survive. Thus \(H_n\) has Boolean deletions and IP by Lemma Q2.2.

Moreover,
\[
 \gamma_3(W)=2\mathbb Z^2,
 \qquad \gamma_3(H_n)=2\mathbb Z^2/\Lambda_n,
 \qquad |\gamma_3(H_n)|=2^{n-5}.                         \tag{Q3.2}
\]
Indeed reduction modulo \(2\mathbb Z^2\) makes the adjacent squares
central; conversely \([[a,b],c]\) and \([[b,c],a]\) give the two doubled
unit translations, up to signs. Thus \(H_5\) is class two of order 32.
The squared translations are not always independent cyclic subgroups:
in \(H_6\) they coincide and have order two. Formula (Q3.2) uses a lattice
index and does not make the false independence assertion.

**Lemma Q3.1 (square-map recognition).** Every finite two-group string
C-group of type \(\{4,4\}\) and order \(2^n\) is marked-isomorphic to
\(H_n\); necessarily \(n\ge5\).

**Proof.** The two dihedral parabolics have orders eight and intersect in
order two, so their product already has 32 elements. The universal group
(Q3.1) maps onto the given group. IP gives irredundancy, so Theorem S gives elementary abelianization of rank three. Hence word parity is a
homomorphism onto \(C_2\), and the kernel of (Q3.1) lies in the subgroup
of orientation-preserving plane isometries. It contains no nonidentity
torsion: a finite-order plane isometry fixes a point; the square tiling
moves that point into a closed fundamental right triangle; its stabilizer
is a subgroup of a vertex dihedral parabolic or an edge reflection group.
Each embeds by the prescribed pair orders and IP. An orientation-preserving
plane isometry without finite order is a translation. Thus the kernel is
a \(D_8\)-invariant sublattice of \(\mathbb Z^2\) of index \(2^{n-3}\).
Identifying the lattice with an ideal of \(\mathbb Z[i]\), its generator
has norm a power of two. Unique factorization (from the Euclidean
algorithm) makes it a unit times a power of \(1+i\). Even powers give
the square lattice and odd powers the diagonal lattice displayed above.
There is exactly one such ideal at each index, proving the assertion. ∎


### An oriented square model for the later cover criterion

**Lemma L1 (the square linear-part quotient).** In the square tessellation
with vertices \(\mathbb Z[i]\), the rotations
\(u:z\mapsto iz\), \(v:z\mapsto iz+1\) are rotations about a vertex and
an adjacent face centre. Their centre coordinates are \(0\) and
\((1+i)/2\), respectively, and \((uv)^2=1\). They generate the full
orientation-preserving grid group: their quotient supplies a unit
translation, and conjugation by the quarter-turn supplies the other unit
translation. For a nonzero ideal \(J=(b+ic)\), the marked quotient is
\((\mathbb Z[i]/J)\rtimes C_4\). It is the usual square-map model whenever
the source parameters specify such a map. The geometric interpretation is
the literal quotient of the tessellation, not an inference from its order.

The linear-part map \(\ell\) sends both marked generators to \(i\), and
is injective on each of their cyclic subgroups: both generators have fourth
power one and linear part of exact order four. If the universal mirror
sends \((u,v)\) to \((u^{-1},u^2v)\), then \(\ell\mu\) is inversion
composed with \(\ell\). Thus both the relation kernel and its mirror lie
in the universal kernel of \(\ell\); the chirality subgroup is contained
in the translation subgroup. In particular it meets \(\langle v\rangle\)
trivially. Here the chirality subgroup is the image of the product of the
relation kernel and its mirror, as defined precisely in §22.1. The argument
uses only the regular marked quotient \(C_4\), and does not claim that a
one-cell quotient is an abstract polytope. ∎

### Cubical and halved lattices in every dimension


Let r≥2 and let L be the r-dimensional cross-polytope with vertices labelled
+e\_i,−e\_i, 1≤i≤r. A proper face of L chooses at most one vertex from each
antipodal pair. Write Q\_r for the cubical tessellation of R^r whose vertices are
Z^r and whose cells are products of unit intervals and integer singletons.
The quotient Q\_r/4Z^r has a formal least and greatest face adjoined when viewed
as an abstract polytope. These formal faces are also understood below.

For each pair of binary coordinates belonging to +e\_i,−e\_i, use the Gray map

    (0,0) ↦ 0,   (1,0) ↦ 1,   (1,1) ↦ 2,   (0,1) ↦ 3     in Z/4Z.   (T1)

**Lemma T1.** The product of these maps is a rank-preserving face-poset
isomorphism 2^L ≅ Q\_r/4Z^r. Binary weight modulo two becomes
∑\_i x\_i modulo two in the cubical coordinates.

**Proof.** In Danzer's construction a proper face of 2^L allows the bits indexed
by a face of L to vary, and fixes every other bit. Thus in any antipodal pair
either both bits are fixed or exactly one bit varies. Under (T1), varying a
single bit describes precisely one edge of the four-cycle: its four possible
edges arise from the two choices of varying bit and the two values of the fixed
bit. A face therefore becomes a product of four-cycle vertices and edges.
Conversely every such product uniquely specifies the varying bit in each free
pair and the remaining fixed bits. Its dimension is the number of free pairs.
Inclusion is preserved and reflected coordinatewise, and formal faces match.
These products are exactly the cubical cells modulo 4Z^r, with their incidence.
The four cases of (T1) have binary parities 0,1,0,1 respectively, proving the
last assertion. ∎

This is a face-poset identification, rather than an inference from orders.
It also handles the dual in the target source explicitly. For a cubical face
F with free coordinate set S, write its free intervals as [m\_i,m\_i+1] for
i∈S and its fixed coordinates as m\_j for j∉S. The dual face F\* has fixed
coordinate m\_i+1/2 for i∈S and free interval [m\_j−1/2,m\_j+1/2] for j∉S.
This reverses containment: whenever an endpoint is fixed in a subface of F,
the corresponding free interval of the dual contains the fixed midpoint of
F\*. It is a bijection onto the shifted cubical tessellation, with dimensions
adding to r. Subtracting (1/2,…,1/2) identifies that tessellation with Q\_r.
The construction commutes with translations by 4Z^r, and consequently induces
an order-reversing bijection on the quotient. Thus for the r-cube K=L\*, the
source's polytope (2^{K\*})* is indeed the cubical toroid
{4,3^(r−2),4}\_(4,0,…,0). The string is {4,4} when r=2.
Reversing the source marking moves its last-end halving to first-end halving
of 2^L. Type reversal is kept explicit; no unproved compatibility of a chosen
self-duality with halving is needed.

### The marking and the exact affine quotient

Use the following reflections of R^r:

    a(x_1,x_2,…,x_r) = (1−x_1,x_2,…,x_r),
    b_i swaps x_i and x_(i+1)                         (1≤i<r),
    c(x_1,…,x_(r−1),x_r) = (x_1,…,x_(r−1),−x_r).      (T2)

They generate W=Z^r⋊B\_r, where B\_r is the signed permutation group. Indeed the
b\_i,c generate B\_r, including the reflection x\_1↦−x\_1; its product with a is
translation by ±e\_1. Signed permutations then supply every integer translation.
The simplex 1/2≥x\_1≥x\_2≥⋯≥x\_r≥0 is a fundamental chamber. One way to verify
this without a presentation theorem is to translate each coordinate to
[−1/2,1/2], make it nonnegative, and order the coordinates; a point with strict
inequalities has a unique such representative. Its reflected walls are the
displayed generators. Its vertices are the barycentres of a nested flag of
cubical faces, so its chamber system is the barycentric subdivision of Q\_r.

The marking in (T2) also agrees with Danzer's marking under (T1). Flipping the
+e\_1 bit induces x\_1↦1−x\_1 modulo four; interchanging antipodal pairs induces
the b\_i; swapping the two bits in the last pair induces x\_r↦−x\_r. These are
the usual base vertex/base flag generators of 2^L. Hence the isomorphism of
Lemma T1 identifies the marked action, not only the unmarked face poset.
The action of W on Q\_r/4Z^r has kernel exactly Λ=4Z^r: an affine signed
permutation acting trivially on all vertices has translation zero modulo
four, and its linear part is the identity modulo four; testing the unit
vectors forces that signed permutation to be the identity.

Put b=b\_1 and replace a by

    d=aba: (x_1,x_2,x_3,…,x_r)
            ↦(1−x_2,1−x_1,x_3,…,x_r).              (T3)

Let E={v∈Z^r : ∑v\_i is even}.

**Lemma T2.** H=⟨d,b\_1,…,b\_(r−1),c⟩ is exactly E⋊B\_r. It has index two
in W and contains Λ. Its fundamental chamber is

    x_1≥x_2≥⋯≥x_r≥0,   x_1+x_2≤1.                (T4)

Its chamber system is the halved cubical geometry, and the marked finite
halving group and geometry are H/Λ and the quotient of that chamber system
by Λ, respectively.

**Proof.** Every displayed generator preserves the parity of an integral
vertex's coordinate sum, so H≤E⋊B\_r. It contains B\_r. The product of d with
the B\_r-reflection (x\_1,x\_2)↦(−x\_2,−x\_1) is translation by e\_1+e\_2.
Conjugating by B\_r gives every ±e\_i±e\_j. These span E: subtract multiples of
e\_i−e\_r, i<r, to leave an even multiple of e\_r, and use
2e\_r=(e\_r+e\_1)+(e\_r−e\_1). This works also for r=2. Thus equality holds and
the index is two. Since every 4e\_i is in E, Λ≤H.

The region (T4) is the union of the preceding W chamber and its reflection
in the a-wall x\_1=1/2. On their common wall the two chambers glue; the other
wall x\_1=x\_2 is paired with its a-image x\_1+x\_2=1. All other walls agree.
Because W=H⊔Ha and the interiors of W chambers are disjoint, these doubled
chambers tile R^r under H, each once. Their wall reflections are exactly
d,b\_1,…,b\_(r−1),c. Equivalently, their chamber labels are the old cubical
flags with the initial vertex chosen in one parity class, pairing the two
old flags differing only at that vertex. The two ends of the old edge
become the two new vertex types; the higher faces retain their type. This
is precisely the graph-halving construction of §18.

Finally, translations in Λ preserve both vertex colors and take cubical
faces to cubical faces. The same flag pairing therefore commutes with Λ.
Every finite chamber has a lift, and two lifts yield the same finite chamber
exactly when they differ by Λ. Wall adjacencies are the marked reflections
modulo Λ. The maximal parabolics are the images of the corresponding wall
subgroups, so the typed coset geometry also agrees. Regularity, thinness and
residual connectedness of the finite geometry follow from the already proved
halving theorem; they are not inferred solely from being a group quotient. ∎

For r≥3, the walls (T4) have the affine fork diagram B̃\_r: d and b\_1 commute;
both meet b\_2 with product order three, successive b\_i have order three, and
b\_(r−1)c has order four. All other distinct wall pairs commute. This follows
directly from (T2)–(T3), or from their mirror angles. Thus its rank-(r+1)
quotient has the source's type {4,3^(r−3),3/3}. Here the quotient lattice is
exactly 4Z^r in the original coordinates; the subscript (4,0,…,0) denotes
the lattice generated by that vector's signed-permutation orbit. This proves
the source's all-rank toroidal identification, including the marking. Its
group order is [E:4Z^r]|B\_r|=(4^r/2)2^r r!=2^(3r−1)r!, agreeing with the
separate parity-module calculation. The order is a check, not the proof.

The coordinate convention can be checked directly against Ens's primary
paper: its equations (3.1), (4.1) are (T2), (T3) for r=3; its §2 definition of
Λ\_s uses the signed-permutation orbit of s, and Theorem 4.3 denotes the
corresponding Coxeter-complex quotient by that lattice. Thus s=(4,0,0) here
is literally the same parameter. The target extends this convention to
larger r. No classification theorem about all invariant lattices is needed.
[Ens, *Rank 4 toroidal hypertopes*, pp.70–75](https://www.researchgate.net/publication/325538081\_Rank\_4\_toroidal\_hypertopes).

### The rank-three square map and its changed lattice basis

When r=2, reorder the halved types as (even vertex, old square, odd vertex).
An old unit square joins its two even corners as an edge of the new map;
the four even neighbors of an old odd vertex bound a new square face.
This describes the ordinary square tessellation with vertex lattice E and
edge directions

    f_1=(1,1),     f_2=(−1,1).                       (T5)

Every even vertex has four such incident edges, every displayed quadrilateral
is a face, and the incidences are exactly those of halving. Thus this is an
isomorphism of maps, not a comparison of their counts. In this basis

    4e_1=2f_1−2f_2,      4e_2=2f_1+2f_2.

The quotient lattice has basis (2,−2),(2,2) in square coordinates. Negating
the first vector gives the customary pair (−2,2),(2,2), so the map is
{4,4}\_(2,2). Lemma T1 and the explicit duality already identify the original
map as {4,4}\_(4,0). This completes both p=4 names in the N013 polygon contract.

## 10. Prescribed rank, order and type

**Corollary Q4.1 (L032 1.2 and L035 1.2).** For \(d\ge3\), \(n\ge5\), and \(k_i\ge2\) with \(\sum_{i=1}^{d-1}k_i\le n-1\), there is a string C-group of exact order \(2^n\) and type \(\{2^{k_1},\ldots,2^{k_{d-1}}\}\). In rank three this includes all \(n\ge10\) parameters of L035 Theorem 1.2.

**Proof.** Put \(\delta=n-1-\sum_i k_i\ge0\) and use the Boolean seed
\(B=C_2^{d-3}\times H_{\delta+5}\), with the independent \(C_2\)
markers first. Its consecutive orders are two until the last two, which
are four. Inflate consecutive pair \(i\) to \(2^{k_i}\) by Theorem Q2.4.
The resulting group has IP, the required string type, and order
\[
 2^{d-3+\delta+5}
 \prod_{i=1}^{d-3}2^{k_i-1}
 \prod_{i=d-2}^{d-1}2^{k_i-2}
 =2^{\delta+1+\sum_i k_i}=2^n.
\]
The rank-three specialization covers every parameter in L035 1.2. ∎

This proves existence with an explicit model; L032's particular higher-rank
presentation is not itself a principal target. To identify the rank-three
presentation used in L035's proof as well, add
\([(ab)^4,c]=[a,(bc)^4]=1\) to the type relations. The two edge-power
subgroups are cyclic normal of orders at most \(2^{s-2}\) and
\(2^{t-2}\). Modulo their product one obtains (Q3.1). In its affine model
\([(ab)^2,c]\) is a doubled unit translation and
\([(ab)^2,(bc)^2]\) is a diagonal doubled translation, up to signs.
For even \(\delta=n-1-s-t\), the additional relation
\([(ab)^2,c]^{2^{\delta/2}}=1\) kills exactly the square lattice
\(\Lambda_{\delta+5}\) by conjugation; for odd \(\delta\), use
\([(ab)^2,(bc)^2]^{2^{(\delta-1)/2}}=1\), killing exactly its diagonal
lattice. The edge-inflation model satisfies these relations since the
displayed commutators vanish in every two-generator coordinate. The order
comparison principle identifies the presentation with that model. Thus no
source presentation-order assertion has been smuggled into the seed.

## 11. The canonical class-two quotient from graded support

**Lemma Q5.1 (descending lift).** Let \(G\) be finite nilpotent and let
\(A\cap B=1\). Put \(D_j=\gamma_j(G)\), \(A_j=A\cap D_j\),
\(B_j=B\cap D_j\). If the images of \(A_j,B_j\) generate
\(D_j/D_{j+1}\) for every \(j\ge m\), then \(D_j=A_jB_j\) for
every \(j\ge m\).

**Proof.** Descend from a trivial term. Assuming
\(D_{j+1}=A_{j+1}B_{j+1}\), if \(a\in A_j,b\in B_j\) have equal
images in the next quotient, write \(ab^{-1}=a'b'\) with
\(a'\in A_{j+1},b'\in B_{j+1}\). Then \(a'^{-1}a=b'b\in A\cap B\),
so both images are trivial. Their images therefore form an internal
direct sum in the abelian quotient. Counting gives
\(|D_j|=|A_j||B_j|=|A_jB_j|\), proving equality as sets. No prior
normality or permutability of \(A,B\) is assumed. ∎

**Lemma Q5.2 (graded support).** Let a positively graded Lie algebra be
generated in degree one by disjoint sets \(X,Y\), with subalgebras
\(L_X,L_Y\). If \([x,y]\in L_Y\) for \(x\in X,y\in Y\), then
\(L=L_X+L_Y\), degree by degree.

**Proof.** The derivation \(\operatorname{ad}x\) preserves \(L_Y\)
because it does so on its generators. Iterated brackets of those
derivations also preserve \(L_Y\), by Jacobi. Hence
\([L_X,L_Y]\subseteq L_Y\), and \(L_X+L_Y\) is a Lie subalgebra
containing all generators. The argument holds in characteristic two. ∎

**Theorem Q5.3 (forest quotient).** Suppose \(G\) is a finite two-group generated by involutions \(r_i\), with marked IP, and its noncommuting pairs form a forest \(T\) on
\(d\) vertices and \(m\) edges. Then edge commutators are independent
in \(G'/\gamma_3(G)\), and \(G/\gamma_3(G)\) is the marked group
\[
 (v,z)(w,t)=(v+w,z+t+\beta(v,w)),\quad
 v,w\in\mathbb F_2^d,\ z,t\in\mathbb F_2^m,               \tag{Q5.1}
\]
where, after orienting each edge, its component of \(\beta\) is
\(v_{\rm head}w_{\rm tail}\). Its order is \(2^{d+m}\).

**Proof.** IP gives irredundancy. Theorem S gives \(G/G'=C_2^d\) and \(G'\cap\langle r_i\rangle=1\).
The lower-central graded Lie ring is generated by these degree-one
elements; all its graded components are \(\mathbb F_2\)-spaces by
bilinearity. Edge commutators span degree two. If they satisfy a nonzero
linear relation, root each forest component and choose a participating
edge whose child endpoint has maximal depth in its component. Removing
it separates the descendant set \(X\) from all other vertices \(Y\),
and no other participating edge is internal to \(X\). The relation
therefore writes the only nonzero cross bracket as a sum of brackets
internal to \(Y\). Lemma Q5.2 shows every graded component is generated
by pure \(X\)- and pure \(Y\)-brackets. Their representatives lie in
\(G_X\cap\gamma_j(G)\) and \(G_Y\cap\gamma_j(G)\).

Actual IP gives \(G_X\cap G_Y=1\), so Lemma Q5.1 gives
\(G'=(G'\cap G_X)(G'\cap G_Y)\). For the crossing endpoints
\(x\in X,y\in Y\), write \([r_x,r_y]=uv\) accordingly. Then
\(u\in G_X\cap G_{\{x\}\cup Y}=\langle r_x\rangle\), whence
\(u=1\); next \([r_x,r_y]\in G_Y\cap G_{\{x,y\}}=\langle r_y\rangle\),
so it too is one. This contradicts that the edge is noncommuting.
Independence follows.

Bilinearity makes (Q5.1) associative; its coordinate markers are
involutions with independent central edge commutators. It is generated
by those markers, and its parabolic on \(I\) consists exactly of vertex
coordinates supported on \(I\) and edge coordinates supported on edges
internal to \(I\). Thus it has IP. Collection in the corresponding
class-two presentation gives at most \(2^{d+m}\) elements, and this
coordinate model attains the bound. Independence in \(G'/\gamma_3(G)\)
gives the same order for \(G/\gamma_3(G)\); hence the marked map is an
isomorphism. ∎

**Corollary Q5.4 (F013 1.1–1.2).** For every finite nondegenerate two-group
string C-group of rank \(d\ge2\),
\(G/\gamma_3(G)\cong G(C_d)\), of order \(2^{2d-1}\); the associated
polytope covers \(C_d\).

**Proof.** Its diagram is a path, so \(m=d-1\). Conder's marked
presentation has involutions, distant commutation, adjacent order four,
and adjacent squares central. The model (Q5.1) realizes that presentation
with the maximal collected order, identifying it with \(G(C_d)\).
The retained marked covering correspondence gives the geometric assertion.
This also proves uniqueness of the minimal object in the declared finite
nondegenerate class. ∎

Notice that no intermediate quotient was assumed to retain IP. Lemma Q5.1
is the step that prevents that circular assumption.

## 12. Bounded cyclic cores and all binary extension models

We now prove the additional classification needed by L035. This section is
source-specific work, sharing its square quotient and kernel transport with
the earlier construction; its length must remain in the replacement.

The retained **cyclic core theorem of Lucchini** says: if a cyclic proper
subgroup \(M\) of a finite group \(H\) has core \(K\), then
\(|M:K|<|H:M|\). Here \(K\) is the largest normal subgroup of \(H\)
contained in \(M\). We use the form recorded in Isaacs, *Finite Group
Theory*, Theorem 2.20, also stated as L035 Proposition 2.9.

**Theorem Q6.1 (bounded cyclic quotient).** Let \((G;a,b,c)\) be a
rank-three string C-group of order \(2^{t+s}\), type \(\{4,2^t\}\),
with \(s\ge3\) and \(t\ge s-2\). Put
\[
 r=bc,\quad m=2^t,\quad d_0=(ab)^2,\quad
 A=\langle r^{2^{s-2}}\rangle.
\]
Then \(A\lhd G\), and \(G/A\) is a string C-group of order
\(2^{2s-2}\) and type \(\{4,2^{s-2}\}\).

**Proof.** The even-word subgroup \(H=\langle ab,bc\rangle\) has
index at most two. IP and Theorem S give \(G/G'=C_2^3\), where its image
has dimension two, so the index is exactly two. For \(M=\langle r\rangle\),
the cyclic core theorem gives \(|M:\operatorname{Core}_H M|<2^{s-1}\),
hence at most \(2^{s-2}\). Thus \(A\) is the subgroup of the cyclic
core of its prescribed order, so is characteristic there and normal in
\(H\). The involution \(b\) inverts \(r\); consequently \(A\lhd G\).
It meets \(\langle a,b\rangle\) trivially by IP and lies in
\(\langle b,c\rangle\). Their quotient parabolics still intersect in
\(\langle bA\rangle\): equality of cosets gives membership in the
original right parabolic, after multiplication by an element of \(A\).
The left parabolic embeds and the right has its stated dihedral order.
This proves IP, independence, type and order in the quotient. ∎

Since \(\operatorname{Aut}(A)\) is abelian, every commutator centralizes
\(A\). In particular \([d_0,r^{2^{s-2}}]=1\). If \(A\ne1\), its unique
involution \(z=r^{m/2}\) is central in \(G\). The universal identities
\[
 r^a=d_0r,\quad d_0^a=d_0,\quad r^c=r^{-1},\quad d_0^c=d_0^r       \tag{Q6.1}
\]
follow from the involution, string and order-four relations.

Hereafter \(s\in\{3,4,5\}\), \(n=t+s\ge10\), so \(m\) is divisible
by 32. The following eight models will realize every class. Let \(z\) be
a distinguished central involution of the finite group \(D\):

| Branch | Group \(D\) | Right-conjugation automorphism \(T\), fixing \(z\) |
|---|---|---|
| \(s=3\) | \(\langle d_0,z\rangle=C_2^2\) | \(T(d_0)=d_0z^\epsilon\) |
| \(s=4\) | \(\langle d_0,d_1,z\rangle=C_2^3\) | \(T(d_0)=d_1,\ T(d_1)=d_0z^\epsilon\) |
| \(s=5\) | Four involutions \(d_0,d_1,d_2,z\), \(z\) central, \([d_0,d_2]=1\), \([d_0,d_1]=[d_1,d_2]=z^\beta\) | \(T(d_0)=d_1,\ T(d_1)=d_2,\ T(d_2)=d_0d_1d_2z^\nu\) |

Here \(\epsilon\in\{0,1\}\), or \((\beta,\nu)\in\{0,1\}^2\).
For the last row an explicit group law on four binary coordinates is
\[
 (u,v,w,e)(u',v',w',e')=
 (u+u',v+v',w+w',e+e'+\beta(vu'+wv')).                    \tag{Q6.2}
\]
Its bilinear final term proves associativity and gives all sixteen
normal forms \(d_0^u d_1^v d_2^w z^e\). Thus the three \(D\)-orders
are four, eight and sixteen. The displayed maps preserve their involution
and commutator relations and have fourth power one. For example in the
last row the two nontrivial commutator contributions cancel in
\((d_0d_1d_2)^2\), and applying \(T\) four times to \(d_0\) returns
\(d_0\); its orbit generates \(D\) together with \(z\).

Adjoin a cyclic \(r\) of order \(m\), with \(x^r=T(x)\), and take the
central quotient
\[
 N=(D\rtimes\langle r\rangle)/\langle zr^{-m/2}\rangle.       \tag{Q6.3}
\]
The identified subgroup has order two and meets both \(D\) and
\(\langle r\rangle\) trivially, since \(T^{m/2}=1\). Hence \(D\)
embeds, \(r\) retains order \(m\), and \(|N|=|D|m/2\).

Define automorphisms \(\mathcal A,\mathcal C\) by
\[
 \mathcal A(r)=d_0r,\quad \mathcal A(d_0)=d_0,\qquad
 \mathcal C(r)=r^{-1},\quad
 \mathcal C(d_i)=T^{1-i}(d_0),\quad\mathcal C(z)=z.
\]
In the first two rows \(\mathcal A\) fixes \(D\); in the third it fixes
\(d_0,d_1,z\) and sends \(d_2\) to \(d_2z^\beta\). For an explicit
verification, substituting the listed generator images into the defining
involutions and commutators of \(D\) preserves each relation. On its
generators the compatibility equalities are
\[
 \mathcal A(Tx)=T(\mathcal A(x)^{d_0}),\qquad
 \mathcal C(Tx)=T^{-1}\mathcal C(x).
\]
They express precisely preservation of \(x^r=T(x)\). Collection gives
\((d_0r)^4=r^4\) in the first two rows and \(r^4z^\nu\) in the last.
Since eight divides \(m/2\), this preserves \(r^m=1\) and
\(r^{m/2}=z\). Finally \(\mathcal A^2=\mathcal C^2=1\) and
\(\mathcal A\mathcal C=\mathcal C\mathcal A\) on \(r,d_0\), which
generate \(N\). For instance both composites send \(r\) to
\(r^{-1}d_0\). These checks prove the automorphism assertions for every
admissible \(m\), not only for a computational sample.

Set \(G=N\rtimes\langle a,c\rangle\), where \(a,c\) are commuting
involutions inducing these automorphisms, and put \(b=rc\). Then
\(a,b,c\) are involutions, \([a,c]=1\), \(bc=r\), and
\((ab)^2=d_0\). They generate \(G\), of order \(2^s m\), with pair
orders \(4,m,2\). In \(G/N\), the images of \(a,b\) are independent
whereas the right parabolic has image \(\langle cN\rangle\). Hence the
only candidates for their intersection are \(1,b,d_0,d_0b\). The normal
form (Q6.3) gives \(d_0\notin\langle r\rangle\), leaving exactly
\(\langle b\rangle\). The three generators are independent (already
\(a\notin\langle b,c\rangle\), and the pair orders exclude the others),
so this proves rank-three IP. Direct substitution yields
\[
 \begin{array}{ll}
 s=3:&[d_0,c]=z^\epsilon,\\
 s=4:&[d_0,r^2]=z^\epsilon,\\
 s=5:&[a,r^2]^2=z^\beta,\qquad[a,r^4]=z^\nu.
 \end{array}                                                   \tag{Q6.4}
\]
They are invariant words of the ordered marking and distinguish the two,
two and four models within their branches.

## 13. Completeness and exact presentation recognition

The eight source presentations have common relations
\[
 a^2=b^2=c^2=(ac)^2=(ab)^4=r^m=1,\qquad r=bc,
\]
and the following additional relations, with \(z=r^{m/2}\):

| Source name | \(m\) | Extra relations |
|---|---|---|
| \(G_1,G_2\) | \(2^{n-3}\) | \([d_0,c]=z^\epsilon\), \(\epsilon=0,1\) respectively |
| \(G_3,G_4\) | \(2^{n-4}\) | \([d_0,r^2]=z^\epsilon\), \(\epsilon=0,1\) respectively |
| \(G_5,G_6,G_7,G_8\) | \(2^{n-5}\) | \([a,r^2]^2=z^\beta,\ [a,r^4]=z^\nu\), with \((\beta,\nu)=(0,0),(1,0),(0,1),(1,1)\) |

**Theorem Q7.1 (high-type completeness).** Every group in the three
classes of L035 Theorem 1.3 is exactly one of the marked models of §12;
each displayed source presentation defines that model.

**Proof, first branch.** For \(s=3\), Theorem Q6.1 gives a quotient of
type \(\{4,2\}\) and order sixteen, necessarily \(D_8\times C_2\).
Thus \(h=[d_0,r]\in A=\langle r^2\rangle\). Since it commutes with
\(r\), and \(d_0\) centralizes \(A\),
\(h^2=[d_0,r^2]=1\). Hence \(h=1\) or \(z\), and (Q6.1) makes this
exactly \([d_0,c]=z^\epsilon\). The conjugates of \(d_0\) obey
\(d_1=d_0z^\epsilon\); (Q6.1) forces all the first model's actions and
normal forms. The resulting surjection from that model onto the actual
group is between groups of the same order, hence an isomorphism.

**Second branch.** For \(s=4\), the quotient of order 64 and type
\(\{4,4\}\) is \(H_6\), by Lemma Q3.1. In that affine quotient
\([d_0,r^2]=1\), so upstairs \(h=[d_0,r^2]\in\langle r^4\rangle\).
Again \(h^2=[d_0,r^4]=1\), giving \(d_2=d_0z^\epsilon\), where
\(d_i=d_0^{r^i}\). Conjugation by \(a\) fixes \(d_0,d_1\).
Applying it to the equation for \(d_2\), with \(z\) central, gives
\(d_2^a=(d_1^{d_0})^r=d_2\), so \([d_0,d_1]=1\).
All second-model relations follow, and the same order comparison proves
uniqueness.

**The bounded seed for the third branch.** A finite computation from the
complete SmallGroups catalogue establishes the following explicit fact:
every order-256 marked string C-group of type \(\{4,8\}\), with
\(r=bc,d_0=(ab)^2\), satisfies exactly one row of this table.

| Row | Relation pattern | Anchored triples | SmallGroup identifier |
|---|---|---:|---|
| I | \([a,r^2]^2=1,\ [a,r^4]=1\) | 64 | \([256,5078]\) |
| II | \([a,r^2]^2=r^4,\ [a,r^4]=1\) | 4 | \([256,6665]\) |
| III | \([d_0,r^2]=r^4\) | 16 | \([256,6661]\) |
| IV | \([(r^2)^a,r]=r^4\) | 8 | \([256,6665]\) |

Here “anchored” is only an enumeration convention, not a count of
isomorphism classes. The finite proof and its executable are charged in
Appendix A. Its exhaustiveness is as follows. Burnside restricts the
catalogue to abelianization \(C_2^3\). Choose \(r\) from every conjugacy
class of order-eight elements outside \(\Phi(G)\); choose \(c\) from
every centralizer orbit of involutions inverting \(r\), independent
from it modulo \(\Phi(G)\). Put \(b=rc\). Then choose **every**
involution \(a\) commuting with \(c\), outside their Frattini plane,
with \(|ab|=4\), and test that the dihedral parabolics intersect in
order two. The basis theorem proves generation and the test proves IP.
Conjugacy and centralizer choices lose no possible marking. The code
tests all four words and rejects an unclassified or overlapping row.
Thus this is a finite proof conditional on the complete catalogue and
the correctness of the exact computation, not an appeal to L035's
classification.

**Third-branch lifts.** For \(s=5\), Theorem Q6.1 gives
\(A=\langle r^8\rangle\) and the table applies to \(G/A\).
In row III we would have \([d_0,r^2]=r^e\), \(e\equiv4\pmod8\).
It commutes with \(r\), so \([d_0,r^8]=r^{4e}=1\), impossible for
\(m\ge32\), since \(v_2(4e)=4\).
In row IV put \(x=(r^2)^a\). The relation would give
\([x,r]=r^e\), \(e\equiv4\pmod8\), hence \(r^x=r^{1-e}\).
The unit \(1-e\equiv5\pmod8\) has order \(m/4\) modulo \(m\):
successive squaring gives
\(v_2((1-e)^{2^j}-1)=j+2\). But
\(x^{m/8}=(r^{m/4})^a\in A\), by normality, so it centralizes \(r\),
contradicting that order. Thus III and IV cannot lift.

In I and II, \([a,r^4]\in A\), so \(a\) maps \(r^4\) to an odd power
of itself and \(M=\langle r^4\rangle\lhd G\). Quotienting gives a
marked \(\{4,4\}\) group of order 128, hence \(H_7=W/4\mathbb Z^2\).
Let \(N=\langle d_0,r\rangle\). Equations (Q6.1) make it normal, with
index four: modulo \(N\), \(a,c\) commute, and their independence follows
in the rank-three Frattini quotient, where \(N\) has the one-dimensional
image spanned by \(r\). The cyclic normal subgroup \(M\) is central
in \(N\), because \(d_0\) is a commutator and \(r\) centralizes its
own powers.

In \(H_7\), the conjugates \(d_i\), \(0\le i\le3\), have linear part
\(-I\) and translation parts \((0,0),(0,2),(2,2),(2,0)\), up to the
choice of coordinate directions. They generate \(C_2^3\), with
\(d_3=d_0d_1d_2\). Upstairs, every \([d_i,d_j]\) is in central \(M\)
and has order at most two. Put \([d_0,d_1]=z^\beta\); conjugating by
\(r\) gives \([d_1,d_2]=z^\beta\). Write
\(d_3=d_0d_1d_2u\) with \(u\in M\). Conjugation invariance gives
\[
 [d_1,d_2]=[d_2,d_3]=[d_2,d_0][d_2,d_1],
\]
so \([d_0,d_2]=1\). Consequently \((d_0d_1d_2)^2=1\); because \(d_3\)
is an involution, \(u^2=1\), giving \(u=z^\nu\). One further
conjugation gives \(d_4=d_0\). These are precisely the final row of
the table in §12, and (Q6.1) forces the actions of the commuting complement
\(\langle a,c\rangle\). The model maps onto \(G\) and has its order
\(32m\), so is isomorphic. This proves completeness of the eight models.

It remains to recognize the **bare presentations**, where the target
order cannot yet be assumed. Let \(P\) be one of them and
\(z=r^{m/2}\), initially of order at most two. For \(G_1,G_2\), if
\(\epsilon=1\), \(a\) centralizes \(z=[d_0,c]\) since it centralizes
\(d_0,c\); \(b,c\) centralize it since they invert \(r\). If
\(\epsilon=0\), \(d_0\) is central; (Q6.1) and the evenness of \(m/2\)
then make \(z\) central too. Collection gives at most \(8m\) normal
forms, attained by the first model.

For \(G_3,G_4\), \(d_2=d_0z^\epsilon\). If \(\epsilon=0\), applying
\(a\) as in the second-branch argument gives \([d_0,d_1]=1\), after
which the model relations and centrality of \(z\) follow. If
\(\epsilon=1\), \([d_0,r^2]=z\) implies that conjugation by \(d_0\)
inverts \(z\); as \(z^2=1\), it centralizes \(z\). Thus \(z\)
commutes with \(r\) and all \(d_i\). Write \(j=[d_0,d_1]\).
Applying \(a\) to the equation for \(d_2\), and using (Q6.1), gives
\(z^a=jz\). Since \(a\) fixes \(d_0,d_1\), it fixes \(j\), and
\(a^2=1\) gives \(j^2=1\). Hence \(d_0,d_1\) centralize \(j\).
Also \(j^r=[d_1,d_2]=[d_1,d_0z]=j^{-1}=j\), and \(c\) exchanges
\(d_0,d_1\), so \(j\) is central. Collection yields
\((d_0r)^4=j r^4\). Since \(m/8\) is even,
\(z^a=(d_0r)^{m/2}=z\), so \(j=1\). The second model relations now
give at most \(16m\) forms, all attained by that model.

For \(G_5\)–\(G_8\), put \(w=[a,r^2]\). If \(\beta=1\), conjugation
by \(a\) inverts \(w\), and so fixes \(z=w^2\). If \(\nu=1\), it
inverts \([a,r^4]=z\), again fixing \(z\). If both are zero, \(a\)
centralizes \(r^4\) and therefore \(z\). Thus \(z\) is central in
every case, and \([a,r^4]=z^\nu\) makes \(M=\langle r^4\rangle\)
normal of order at most \(m/4\). Modulo \(M\), the presentation is
\(W\) with the extra relation \([a,r^2]^2=1\). In the affine model
\([a,r^2]\) is a doubled unit translation, so its square and conjugates
kill precisely \(4\mathbb Z^2\). Thus the quotient has order 128, and
\(|P|\le128(m/4)=32m\). The constructed model attains this bound and
satisfies every relator, so the order comparison principle identifies
\(P\) with it. This completes presentation recognition and the theorem. ∎

The preceding theorem proves the full marked interpretation of L035
Theorem 1.3; the listed word invariants distinguish all the declared
families. It does not classify arbitrary two-groups of order \(2^n\),
other types, or the source's unnumbered exceptional \(n<10\) discussion.

## 14. Prescribed square sections and their universal presentation

For \(d\ge3\) and \(n_3,\ldots,n_d\ge5\), place \(H_{n_{i+3}}\)
on the label bag \(\{i,i+1,i+2\}\), \(0\le i\le d-3\). Glue the
successive bags over their shared \(D_8\) using Theorem Q2.3. At each
step the previous group and the new seed embed, with their given
markings. Thus all adjacent orders remain four, distant markers
commute, every deletion exists, and the group \(G(n_3,\ldots,n_d)\)
has IP. Its exact order is
\[
 |G(n_3,\ldots,n_d)|
 =\frac{\prod_{j=3}^d2^{n_j}}{8^{d-3}}
 =2^{\sum_{j=3}^d n_j-3(d-3)}.                           \tag{Q8.1}
\]
The common regular-polytope correspondence gives a finite regular
\(d\)-polytope with precisely the specified consecutive triple sections.

For \(d\ge4\), let \(A\) be its final facet subgroup, on
\(\{0,\ldots,d-2\}\), and let \(B\) be its last triple subgroup,
on \(\{d-3,d-2,d-1\}\). The compatible product decomposition gives
\(G=BA\). The stabilizer of the base \((d-4)\)-face contains \(B\).
The coset incidence criterion therefore makes every \((d-4)\)-face
incident with every facet. Every vertex lies on a \((d-4)\)-face
(including the rank-zero case), so the polytope is flat. Boolean
deletion gives FAP for every initial or final cut, hence all three
cuts required by F016 5.1(d). For \(d=3\), the co-\((-1)\)-face
cut, if included in that notation, is the tautological whole-polytope
cut; the vertex-figure and facet cuts are genuine seed retractions.
This proves every clause of **F016 Theorem 5.1**.

The same construction connects directly to the canonical quotient:
\[
 \gamma_3(G)=\prod_{j=3}^d\gamma_3(H_{n_j}),\qquad
 |\gamma_3(G)|=2^{\sum_{j=3}^d(n_j-5)},\qquad
 G/\gamma_3(G)=G(C_d).                                  \tag{Q8.2}
\]
Indeed realize the group as compatible tuples of seed coordinates.
An element of the third lower-central subgroup of one embedded triple
projects trivially into every other bag: the overlap has at most two
markers and its image lies in a dihedral group of class at most two.
It occupies exactly its own coordinate, so these kernels are independent
normal factors. On quotienting by their product, each consecutive triple
is class two. Every edge commutator then commutes with its endpoints,
its nearest outside markers, and by string commutation with the remaining
markers. Hence the entire quotient is class two. This proves equality
with \(\gamma_3(G)\), and (Q8.1) gives the canonical quotient order.
Thus (Q8.2) is one construction meeting the bound in Theorem Q5.3 at every
rank, rather than an unrelated counting trick.

We next prove that this construction has the exact additional presentation
claimed in **F016 Theorem 5.3**. The only extra identity needed is local.

**Lemma Q8.1 (four-marker centralization).** Suppose \(a,b,c,d\) are
involutions with \([a,c]=[a,d]=[b,d]=1\) and
\([ (ab)^2,(cd)^2]=1\). Then \(d\) commutes with
\((cbab)^2\) and \((abcb)^2\).

**Proof.** Put \(x=bab\), \(E=(ab)^2=ax\), \(F=(cd)^2\).
The element \(a\) commutes with \(F\), so \([E,F]=1\) implies
\([x,F]=1\). Also \([x,d]=1\), hence \([x,Fd]=[x,cdc]=1\).
Conjugating by \(c\) gives \([cxc,d]=1\). Both factors of
\((cbab)^2=(cxc)x\) commute with \(d\). Finally
\(abcb=b(cbab)^{-1}b\), and \(b\) commutes with \(d\), proving
the second assertion. ∎

First let \(P_0\) have the string \([4,\ldots,4]\) relations and every
prescribed triple presentation from §9. All its defining relators are
stable under every deletion assignment: the string Coxeter relators have
even exponents, and the local lattice relators survive every deletion of
their three markers by §9. Thus the assignments define endomorphisms of
\(P_0\), and Lemma Q2.2 proves its IP without assuming finiteness. The
constructed quotient \(G\) shows that each local triple embeds with its
exact prescribed marking and that every generator is nontrivial. Hence
\(P_0\) itself is a string C-group of the required local type. Every
marked string C-group of that local type satisfies its defining relators,
so is its quotient. The standard marked covering correspondence therefore
constructs the universal regular polytope of that type directly. No
separate assumption about a universal polytope's presentation or existence
is needed.

Now let \(Q\) be the quotient of \(P_0\) by
\[
 [(r_i r_{i+1})^2,(r_{i+2}r_{i+3})^2]=1
 \quad(0\le i\le d-4).                                  \tag{Q8.3}
\]
The constructed group satisfies these relations. For (Q8.3), no tuple
coordinate contains both disjoint edges; the edge missing one endpoint
has square one in that coordinate. Hence \(Q\twoheadrightarrow G\).
Each triple embeds in \(Q\), since its map onward to the embedded
triple in \(G\) is injective. Its third lower-central subgroup \(K_i\)
is generated by its two squared translations and has order
\(2^{n_{i+3}-5}\), by (Q3.2). Lemma Q8.1 and its reversed version show
that the nearest outside markers centralize \(K_i\), while the farther
markers do so by string commutation. Thus every \(K_i\lhd Q\).
Their product \(K\) is finite of order at most
\(2^{\sum_j(n_j-5)}\). Modulo it all triples are class two; the same
local-to-global centralization argument used for (Q8.2) makes \(Q/K\)
class two. Collecting markers and central edge commutators gives
\( |Q/K|\le2^{2d-1}\). Therefore
\[
 |Q|\le2^{\sum_j(n_j-5)+2d-1}
      =2^{\sum_j n_j-3(d-3)}=|G|.
\]
The order comparison principle identifies \(Q=G\) as marked groups.
Since \(P_0\) is the universal type group just constructed, this is
exactly its quotient by (Q8.3). The finite group presentation, the
universal group and both intersection properties have all been proved
using the same deletion calculus.

## 15. Alternating assembly and infinite extensions

The additional geometry required for the semiregular conclusions is
retained with the following precise forms; no target theorem of F016
is used to justify them.

**Assembly input.** If regular \((d-1)\)-polytopes \(P,Q\) have an
identified common facet \(K\) and FAP retractions
\(\Gamma(P)=N_P\rtimes\Gamma(K)\),
\(\Gamma(Q)=N_Q\rtimes\Gamma(K)\), the tail-triangle group
\((N_P\times N_Q)\rtimes\Gamma(K)\), with distinct final markers,
gives an alternating semiregular \(d\)-polytope with these two facets.
Its full automorphism group is that group when \(P\not\cong Q\), and
its extension by the branch-swapping \(C_2\) when \(P=Q\); the latter
polytope is regular. This is the construction and full-automorphism
criterion of Monson–Schulte, *The assembly problem for alternating
semiregular polytopes* (2020), Theorem 5.3, in the FAP case needed here.

Apply §14 to the two lists
\((n_3,\ldots,n_{d-2},n_{d-1})\) and
\((n_3,\ldots,n_{d-2},m_{d-1})\). Their common facet \(K\) has list
\((n_3,\ldots,n_{d-2})\), or is the square if \(d=4\). Theorem Q2.3
gives their tail-triangle fiber product, with
\[
 |\Gamma(K)|=2^{\sum_{j=3}^{d-2}n_j-3(d-5)},\quad
 |N_P|=2^{n_{d-1}-3},\quad |N_Q|=2^{m_{d-1}-3}.
\]
The first expression gives eight when \(d=4\), with the sum empty.
The assembly input supplies the polytope, while these formulas give
exactly its contracted order. Equal last parameters give identical
marked constructions, hence the branch swap; unequal last parameters
give different facet orders and exclude isomorphism. This proves both
clauses of **F016 Theorem 6.1**, including the precise doubling case.
Its type prescribes all the listed rank-three sections of facets; it
does not assert an independently prescribed co-\((d-4)\)-face.

For the infinite statements we retain the following previously established
**free-extension identifications**, including their geometric existence,
universality and symmetry conclusions. All input ranks here satisfy the
source's standing convention \(d\ge3\):

1. If \(K\) is regular with facet \(F\), its free extension is regular,
   of rank one higher, with group
   \(\Gamma(K)*_{\Gamma(F)}(\Gamma(F)\times C_2)\).
2. If \(K\) is oriented chiral with directly regular facets \(F\), its
   free extension is oriented chiral, of rank one higher, with group
   \(\Gamma(K)*_{\Gamma^+(F)}\Gamma(F)\), where
   \(\Gamma(F)=\Gamma^+(F)\rtimes C_2\).
3. If regular \(d\)-polytopes \(P,Q\) have isomorphic facets \(K\),
   their universal alternating semiregular \((d+1)\)-polytope has group
   \(\Gamma(P)*_{\Gamma(K)}\Gamma(Q)\), with an additional
   branch-swapping \(C_2\) precisely if \(P\cong Q\).

The first is the standard regular free-extension construction; the
second is Schulte–Weiss, *Free extensions of chiral polytopes* (1995);
the third is the universal alternating construction of Monson–Schulte
(2012, 2021). The embeddings are the indicated face or facet-rotation
subgroups, not an assumed embedding of a full facet group in a chiral
automorphism group.

**Lemma Q9.1 (torsion and amalgams).** Let “two-primary torsion” mean that
every element of finite order has two-power order. This property passes
to subgroups, to extensions by finite two-groups, and to amalgamated
free products. If the amalgamated subgroup is proper in both factors,
the free product is infinite. If the factors are finitely generated,
so is the amalgam.

**Proof.** In an extension, a finite cyclic subgroup has two-group
intersection with the kernel and two-group image, hence two-power
order. For an amalgam, its normal-form theorem conjugates any element
either into a factor or to a cyclically reduced word of length at least
two. Powers of such a word stay reduced with increasing length and
cannot have finite order. Thus torsion is conjugate into a factor.
If \(a,b\) lie outside the common subgroup in their respective factors,
\((ab)^h\) is reduced of length \(2h\), proving infinitude. Finite
generation follows by taking generators of both factors. ∎

In each of the three free-extension identifications the common subgroup
is proper in both factors, as the face/flag action or the new reflection
shows. In the second factor of the first two constructions its index
is two. Every factor has two-primary torsion: in the chiral case the
**rotation subgroup** of the facet embeds in \(\Gamma(K)\), and its
extension by \(C_2\) suffices to prove the property for \(\Gamma(F)\).
All factors are finitely generated by their finite marked sets. Lemma Q9.1
and, when needed, its finite-extension clause prove exactly **F016
Theorems 7.1, 7.2 and 7.3**, including infinite input groups. No assertion
that all elements have finite order is made.

## 16. Corrections and exclusions in the two-group branch

The F013 common-quotient theorem is recovered by a different kernel. Its
specified auxiliary subgroup is false in general. We include the proof
of the correction so that no false historical claim is counted as a
corollary of this manuscript.

In the path model (Q5.1), name the central edge coordinates
\(c_1,\ldots,c_{d-1}\), and put
\[
 \sigma_i=r_{i-1}r_i,\quad
 A_i=\langle\sigma_1,\ldots,\sigma_{i-1},\sigma_i^2,
                  \sigma_{i+1},\ldots,\sigma_{d-1}\rangle,
 \quad C=\bigcap_i\Phi(A_i).                              \tag{Q10.1}
\]
These are exactly the source's equations (7)–(9), and \(\sigma_i^2=c_i\).
The vertex images of the rotations are independent and span the
even-weight subspace. Each \(A_i\) contains all central coordinates,
with vertex-image dimension \(d-2\). Thus \(|A_i|=2^{2d-3}\).
Squaring a collected class-two word shows its square subgroup is
generated by the squares and pair commutators of the generators;
Burnside identifies it with \(\Phi(A_i)\). The endpoint computations
give
\[
 \Phi(A_1)=\langle c_2,\ldots,c_{d-1}\rangle,\qquad
 \Phi(A_{d-1})=\langle c_1,\ldots,c_{d-2}\rangle.
\]
All listed coordinates are squares; no missing endpoint coordinate can
arise because every remaining rotation has the missing endpoint vertex
coordinate zero. For an internal \(i\), all coordinates except \(c_i\)
are squares, and \([\sigma_{i-1},\sigma_{i+1}]=c_i\). Hence
\(\Phi(A_i)=\langle c_1,\ldots,c_{d-1}\rangle\) internally and
\[
 C=\langle c_2,\ldots,c_{d-2}\rangle,\qquad |C|=2^{d-3}
 \quad(d\ge3).                                          \tag{Q10.2}
\]
For \(d=2\), separately, \(C=1\). For every \(d\ge4\), this model
has order \(2^{2d-1}\) but \(C\ne1=\gamma_3(G)\). It contradicts
F013 v1 Theorem 4.2(c)'s kernel order, (d)'s quotient order and prescribed
identification, and (e)'s equality with \(\gamma_3(G)\). The actual
quotient order is \(2^{d+2}\); it still has IP, with interior adjacent
orders two. Thus this counterexample does not refute the separate main
common-quotient existence conclusion, nor every clause of 4.2(d).

Two F016 proof repairs also remain explicit. In a diagonal square-map
quotient the perpendicular squared translation subgroups can coincide,
so their orders cannot be multiplied as in its page-11 argument; (Q3.2)
uses the correct lattice index. In its chiral extension proof the full
facet automorphism group need not embed in the chiral group; §15 only
uses its rotation subgroup and a finite index-two extension.

Outside the declared main-result contract are the four papers' open
questions, historical discussion, unnumbered small-order lists and
examples, F016's separate power-polytope recollections, and assertions
about absolute minimum flag counts among all regular polytopes. The
source's known power constructions have displayed semidirect groups
\(C_2^v\rtimes H\) and \((D_{2^m})^{v/2}\rtimes H\), where here
the latter dihedral notation means order \(2^{m+1}\). Conditional on
those retained constructions, their order formulas are immediate, but
their geometric construction is not rederived or counted as another
target here. The order-1024 census N009 is excluded entirely.

The proved core supplies short final source corollaries, but its cyclic
classification, lattice recognition, finite census and retained
semiregular geometry have real costs. The two-group source contracts require the full preceding text and bound finite certificate; their inherited review does not certify this changed assembly. This integration requires its own independent review; no factor is assigned.

## 17. A single endpoint theorem

Let (G;a,b,(r\_i)\_(i∈E)) be a C-group marking, with [a,r\_i]=1 for all i∈E. No string diagram, finite group, or underlying geometry is assumed. Define

\[
a'=aba,\quad R_J=\langle r_j:j\in J\rangle,\quad
U_J=\langle a,b,R_J\rangle,\quad H_J=\langle a',b,R_J\rangle,
\]
\[
P=\langle b,R_E\rangle,\quad H=H_E,\quad
\mathcal F=\{J\subseteq E:a\in H_J\}.
\tag{O3}
\]

Conjugation by a exchanges b and a′ and fixes R\_J pointwise. Consequently

\[
H_J\trianglelefteq U_J=H_J\langle a\rangle,
\qquad [U_J:H_J]\le2.
\tag{O4}
\]

**Endpoint theorem O2.1.** The new marking (H;a′,b,(r\_i)) has IP if and only if

\[
P\cap P^a=R_E,
\qquad \mathcal F\text{ is closed under intersections}.
\tag{O5}
\]

The group H is normal of index at most two in G. It is G precisely when ℱ is nonempty. Since E is finite, a nonempty intersection-closed ℱ is precisely the family of supersets of one least support S⊆E.

**Proof.** The family ℱ is upward closed. Any new marked subgroup is of one of the forms

\[
A_{\epsilon,J}=\langle b^\epsilon,R_J\rangle\ (\epsilon=0,1),
\qquad H_J,\qquad Q_J^a\text{ with }Q_J=\langle b,R_J\rangle,
\tag{O6}
\]

where b⁰ means that b is omitted. These correspond to omitting a′, using both endpoint labels, or using a′ but omitting b. Intersections of two A's are old marked intersections. Also

\[
A_{\epsilon,I}\cap H_J
\le A_{\epsilon,I}\cap U_J=A_{\epsilon,I\cap J};
\]

all generators on the right belong to H\_J, so equality holds. Intersections of two Q^a's follow by conjugating old IP. Conjugation by a normalizes H\_I, so an H-with-Q^a intersection reduces to the just proved H-with-A case. For an A-with-Q^a intersection, the first condition in (O5) confines it to R\_E. Intersecting there and using that a centralizes R\_E gives R\_(I∩J).

It remains to intersect H\_I and H\_J. Put K=I∩J. Old IP gives

\[
H_K\le H_I\cap H_J\le U_I\cap U_J=U_K.
\tag{O7}
\]

If a∈H\_K then H\_K=U\_K. Otherwise H\_K has index two in U\_K, so the middle subgroup is either H\_K or U\_K. The latter case occurs exactly when a belongs to both H\_I and H\_J, and intersection closure excludes it. This proves all new marked intersections. Necessity of the first condition follows by intersecting the two endpoint-deleted new parabolics; necessity of the second follows by intersecting H\_I,H\_J. The generators are involutions and the proved IP supplies independence. Equation (O4) with J=E gives the group and index assertions. A finite nonempty upward intersection-closed family contains its total intersection S, giving the least-support description. ∎

**Corollary O2.2 (odd endpoint and proper halving).** If m=|ab| is odd, the only test in (O5) is the overlap P∩P^a=R\_E, and H=G. If H is proper in G, the only test is again the overlap, and [G:H]=2. In either case the endpoint product has order m/gcd(m,2) for finite m; infinite m remains infinite.

Indeed a′b=(ab)², and for odd m,

\[
a=(a'b)^{(m+1)/2}b\in H_\varnothing.
\]

Thus ℱ is respectively all subsets or empty. An even endpoint order by itself does not imply that H is proper; the least-support alternative in Theorem O2.1 cannot be discarded.

**Lemma O2.3 (central twist).** Suppose b,c are involutions with |bc|=m odd and m≥3, and w is a nonidentity involution centralizing b,c. Replacing b by wb preserves the generated group and changes |bc| to 2m, provided w belonged to the original group.

**Proof.** The commuting factors w and bc have coprime orders, so (wbc)^m=w and |wbc|=2m. Hence the new generators recover w and b. The new marker wb is a nonidentity involution: wb=1 would make b=w commute with c, contrary to m≥3 odd. ∎

A parabolic containing w,b,c is unchanged by this twist; one omitting b is unchanged. Other intersections and typed Helly still require proof. Lemma O2.3 is the auxiliary operation needed in the finite application below, not a blanket geometric preservation theorem.

## 18. The geometric meaning of the support condition

Let Γ be a finite-rank residually connected incidence geometry, of rank n≥3. Designate types 0 and 1 as vertices and edges. Assume their truncation is a simple graph Q, and that an edge is incident with a higher object exactly when both its endpoints are incident with that object. For a flag F of higher objects, let Q\_F be its common vertex-edge shadow. All Q\_F are connected and contain an edge.

Lemma O0 supplies connected chamber galleries in every residue. Restricting a gallery to any set of at least two types shows that its truncation is connected, since successive complete incidence subgraphs overlap. Apply this inside the residue at F; chamber extension supplies an edge. The edge-shadow hypothesis says Q\_F is the induced graph on its common vertices.

For a connected graph Q, its bipartite double cover D(Q) has vertices (v,ε), ε∈{0,1}, with (v,ε) adjacent to (w,1−ε) when v is adjacent to w. It is connected when Q has an odd cycle, and has two components otherwise: parity of walks proves both assertions. Choose a component C of D(Q). Define L\_C(Γ) as follows. Its first two types are (v,0) and (v,1) in C. A higher object is a pair (x,C\_x), where C\_x is a component of D(Q\_x) contained in C. Incidence of the first two types is adjacency, incidence with a higher object is membership in C\_x, and two higher objects are incident when their old objects are incident and their chosen components meet.

The precise compatibility requirement is

\[
\text{if every }Q_x\ (x\in F)\text{ is nonbipartite, then }Q_F
\text{ is nonbipartite},
\tag{PC}
\]

for every nonempty higher flag F. It is automatic if the higher shadows of every flag are nested, or if Q is bipartite.

**Geometric theorem O3.1.** The system L\_C(Γ) is always a geometry. It is residually connected exactly when (PC) holds. It is thin exactly when Γ is thin. A chamber-transitive automorphism group of Γ acts faithfully and chamber-transitively on L\_C(Γ) when Q is nonbipartite; when Q is bipartite its index-two color-preserving subgroup does so.

**Proof.** For a flag Φ={(x,C\_x):x∈F} of higher lifts, write W=∩C\_x. If any Q\_x is bipartite, restriction of C\_x to D(Q\_F) is one component. Any two such restrictions agree: incidence makes them meet over the connected Q\_(x,y), and hence select the same parity class there and over Q\_F. Nonbipartite constituents impose no restriction. Thus W is one component if any constituent is bipartite, and all of D(Q\_F) otherwise. In particular W always contains an edge, and is connected exactly under (PC) for this flag. For F empty use W=C.

An edge of W and a chamber of Γ extending its base edge and F give a chamber extending Φ. Every additional higher object has a unique component containing the chosen lift of that edge. The same extension works for a flag already containing one lifted vertex. If it contains both, their base edge is unique by simplicity and incident with all the old higher objects by the shadow condition. This proves the geometry axiom.

The residue at (v,0) is the old residue Γ\_v: a neighbour (w,1) corresponds to the unique edge {v,w}, and the component for an incident higher object is uniquely specified by (v,0). Simplicity and the shadow condition preserve all incidences. The other color is identical. Hence residues of flags containing a lifted vertex are connected. For a flag of higher objects only, its two-type truncation is W; when W is connected, every other residual object attaches to it through a chamber. This proves residual connectivity under (PC). If (PC) fails, choose its higher flag; all constituents have unique lifts but W has two components. Were the resulting geometry residually connected, the truncation lemma inside its residue would make W connected. This proves necessity without treating a truncation as a residue.

Panels containing both new vertex types correspond to old panels missing the same higher type. A panel missing one new vertex type corresponds to an old panel missing the edge type, at the retained endpoint. Old panels missing the vertex type already have two objects by simplicity. These correspondences prove both directions of thinness.

If Q is nonbipartite, an old chamber (v,{v,w},x₂,…,x\_(n−1)) corresponds bijectively to the new chamber with (v,0),(w,1) and the components containing them. Old automorphisms act naturally on this bijection. If Q is bipartite, the same bijection uses the old chambers whose chosen vertex is in one fixed color class. A chamber-transitive group contains a color-exchanging element, since it exchanges the endpoints of a base edge through a chamber move. Its color-preserving subgroup therefore has index two and is transitive on the selected chambers.

For faithfulness apply K(c) to this actual acting group, retaining X consisting of old vertices and all old higher objects. A new vertex is encoded by its old vertex and its color; (x,C\_x) is encoded by x and the two old-vertex subsets of C\_x. These data determine the component, because the double-cover graph is fixed. Forgetting the color or component maps onto X: when Q is nonbipartite all lifts lie in C, while in the bipartite case C has one lift of every old vertex and one compatible component of every connected Q\_x. Thus the encoding and surjection hypotheses hold. An element fixing X fixes every old edge by simplicity, so acts trivially on Γ and is the identity. K(c) therefore proves faithfulness. ∎

Suppose now Γ is regular and thin, with vertex-changing marker a, edge-changing marker b, and higher markers r\_i; assume a commutes with the higher markers. Under (PC), Theorem O3.1 produces a regular thin residually connected geometry. Directly on a base edge, its panel involutions are b^a,b,r\_i: b changes one endpoint, aba changes the other, and each r\_i changes its higher object. Lemma O1.1's chamber argument identifies their group as the full type-preserving group H. Conversely, walking within residues identifies the stabilizer of a base flag with the subgroup generated by its missing-type markers, giving IP and identifying the actual coset incidence with L\_C(Γ).

There is also an exact correspondence between the two parity conditions. In the base residue with group U\_J from (O3), the vertex stabilizer is Q\_J=⟨b,R\_J⟩. Its vertex graph is bipartite precisely when a∉H\_J. If H\_J is proper, its two cosets give a coloring, since Q\_J≤H\_J and a crosses colors. Conversely the action on the two colors supplies a character killing b and all r\_j and sending a to the nontrivial element, so it excludes a from H\_J. In a globally nonbipartite geometry, higher flags reduce by transitivity to base flags with shadows U\_(E\S). Condition (PC) says

\[
[E\setminus\{i\}\in\mathcal F\text{ for all }i\in S]
\Longrightarrow E\setminus S\in\mathcal F.
\tag{O8}
\]

An upward family containing E satisfies (O8) exactly when it is principal: let T be the set of i whose complementary coatom belongs to ℱ; (O8) gives E\T∈ℱ, and every member of ℱ contains E\T. Thus geometric parity compatibility is the least-support condition of Theorem O2.1. The mixed overlap in that theorem has a different role: it says the two adjacent vertices determine one edge. Indeed P and P^a stabilize the endpoints; their intersection is the edge's pointwise stabilizer R\_E exactly when no other edge has those endpoints, using transitivity on panels and the regular chamber identification.

## 19. All lattice-polytope halvings

**Corollary O4.1.** Let P be a regular rank-n abstract polytope, n≥3, whose face poset is a lattice. Replacing one endpoint marker a by aba gives a C-group H normal of index at most two in Aut(P). Its maximal-parabolic coset system is a regular hypertope, with full type-preserving group H. The diagram duplicates the edge labels from b to the remaining markers, and the a′–b label is m/gcd(m,2) for m=|ab| finite, or infinity for infinite m. The index is two exactly when the corresponding vertex graph is bipartite; for a final-end operation use the dual graph on facets.

**Proof.** In a lattice polytope an edge is the join of its two distinct vertices. Thus two vertices determine at most one edge, and that edge belongs to a higher face exactly when both vertices do. Higher faces of a flag form a chain, so their shadows are nested and (PC) is automatic. Theorem O3.1 and the panel-marker identification prove the asserted geometry, full group, and IP without an alternating-semiregular-polytope theorem. Equation (O4) and the coloring argument give the index. Finally a′b=(ab)² and a commutes with all r\_i, so a′r\_i is conjugate to br\_i; all other products are unchanged. ∎

This is N013 Theorem 3.1, Proposition 3.2 and Corollary 3.3, after reversing their final-end convention. Their term *non-degenerate* is used in the lattice-face-poset sense, as explicitly explained by the later primary halving manuscript cited in the references; a general abstract polytope with simple diagram is not substituted for that hypothesis. N013's auxiliary direct-product Lemma 2.4 follows at once because a marked subgroup of a product with disjoint factor markings is the product of the corresponding marked subgroups, and intersections are coordinatewise. Its quoted Propositions 2.1 and 2.3 are background; the latter is not needed. Recognition lemma O1.1 supplies the content needed from N013's quoted Theorem 2.2.

## 20. Generalized cubes: one parity module gives every principal application

Retain the following Danzer construction. If K is a finite regular lattice polytope with m vertices, 2^K has binary vertex set V=F₂^m. A face associated with a face F of K and x∈V allows exactly the coordinates indexed by the vertices of F to vary. These coordinate subcubes, ordered by inclusion with their improper faces, form a regular lattice polytope of one higher rank, with vertex figures K and automorphism group

\[
\operatorname{Aut}(2^K)=V\rtimes\operatorname{Aut}(K).
\tag{O9}
\]

The coordinate action is the natural vertex permutation action. This construction theorem is a substantial retained input; neither its polytopality nor the identification of the full group in (O9) is inferred solely from an order calculation.

**Corollary O5.1.** Halving 2^K at its vertex endpoint gives the exact group

\[
E_m\rtimes\operatorname{Aut}(K),\qquad
E_m=\{x\in\mathbf F_2^m:\sum x_i=0\},
\tag{O10}
\]

of order 2^(m−1)|Aut(K)|, acting as the full type-preserving group of the regular hypertope in Corollary O4.1.

**Proof.** The vertex graph of 2^K is the m-cube, bipartitioned by coordinate parity. Its color-preserving subgroup of (O9) is exactly (O10), so Corollary O4.1 identifies the whole halving group. Alternatively, let a flip the coordinate of a base vertex v of K and let b be its first distinguished reflection, carrying v to an adjacent vertex v′. The product a′b=(aba)b is translation by e\_v+e\_v′. The unchanged reflections generate Aut(K). Their conjugates give every edge difference in the connected vertex graph of K; along paths, these span E\_m. This independently proves generation of the displayed subgroup. ∎

N013 uses the dual convention P̂=(2^(K\*))*. Consequently m in its formulas is the number of facets of K, and reversing all types converts (O10) exactly to its construction.

**Corollary O5.2 (polygon inputs).** For a p-gon K, p≥3, the result is a self-dual orientable regular map of type {p,p}, with

\[
V=F=2^{p-1},\qquad E=p2^{p-2},\qquad
|\operatorname{Aut}|=p2^p,\qquad
g=1+2^{p-3}(p-4).
\tag{O11}
\]

**Proof.** The two vertex colors give V and F after ordering the map types as (color 0, old square, color 1). Each edge of the p-gon specifies 2^(p−2) coordinate squares, giving E. The fork diagram becomes {p,p}. A single coordinate flip conjugates the two new endpoint reflections and exchanges the colors, supplying the duality. Extend the reflection-sign character of the dihedral Aut(K) trivially over E\_m. Each of the three new distinguished reflections has sign −1, so the chamber orientation is well defined and reverses across every adjacency. This proves orientability. Euler's formula V−E+F=2−2g gives (O11). ∎

For p=3 the map is the tetrahedron: the group is E₃⋊S₃ of order 24 with the spherical A₃ marking and its universal Coxeter geometry. For p=4 it is the square toroid {4,4}\_(2,2). The Gray-code face-poset proof, explicit cubical duality and lattice basis change in §9 prove this identification and identify the original dual generalized cube as {4,4}\_(4,0).

**Corollary O5.3 (all locally spherical inputs and exceptional orders).** In output rank n≥4, the locally spherical cases of N013's dual generalized-cube construction are obtained from K equal to the (n−1)-simplex or (n−1)-cube, and additionally the dodecahedron for n=4 and the 120-cell for n=5. Their types are respectively spherical D\_n, affine B̃\_(n−1), and the rank-four/rank-five compact-hyperbolic forks. The last two finite groups have orders

\[
2^{11}\cdot120=245760,
\qquad 2^{119}\cdot14400.
\tag{O12}
\]

**Proof.** Put L=K\* to use the coordinate model. Each of its two new vertex residues is L itself. If the output is locally spherical, L must therefore be a universal spherical polytope. Retain the classical finite string-Coxeter list. In rank at least four a proper three-node fork with equal labels q,q is spherical only for q=3, where q is the first label of L. In rank five, the remaining candidate F₄={3,4,3} is excluded because its proper four-node fork is affine. The finite list leaves exactly the simplex, cross-polytope, icosahedron and 600-cell, the last two only in their respective ranks. For rank at least six only the first two remain.

Conversely, all proper faces of these L are simplices. At an old j-face of 2^L, j≥2, let F be its associated (j−1)-face of L. The lower and upper sections vary independently. After halving, the maximal residue is the product of the compressed cube 2^F with the spherical section L/F. As F has j vertices, the first factor has group E\_j⋊S\_j and its D\_j marking; its order 2^(j−1)j! equals that of the finite Coxeter group D\_j, proving equality with the universal spherical geometry. Here D₂=A₁×A₁ and D₃=A₃. Vertex residues are L, so all maximal residues, and consequently all proper residues, are genuinely spherical geometries. A diagram alone is not used as a substitute for those residues.

The new global diagrams follow from Corollary O4.1. The retained finite, affine and compact-hyperbolic Coxeter classifications identify them as stated. Formula (O10), with m=12 or 120 and the classical orders |Aut(dodecahedron)|=120 and |Aut(120-cell)|=14400, gives (O12). For the simplex m=n and |Aut(K)|=n!, giving D\_n order 2^(n−1)n!. For the (n−1)-cube, m=2(n−1) and |Aut(K)|=2^(n−1)(n−1)!, giving 2^(3n−4)(n−1)!. The finite hyperbolic examples are proper hypertopes because the fork diagrams have a vertex of degree three. ∎

The source's toroidal notation for cube input is {4,3^(n−4),3/3}\_(4,0,…,0). Section 9 identifies the original cubical toroid and its halving as actual marked face/chamber quotients by 4Z^(n−1), proving the lattice names in addition to the exact group, order and residue assertions above. N013's claim that its rank-four hyperbolic example differs from every example in its reference [9] is not used or independently verified. Its auxiliary identification with an alternating semiregular polytope is likewise unnecessary and retained as background rather than counted as a new corollary.

There is a scope correction to N013 Remark 4.1. Retaining Pellicer's extension construction, the halved diagram for endpoint 2s has a three-node fork triangle with labels (p,p,s). For output rank at least four and p,s≥3, this proper rank-three diagram is not finite, since 2/p+1/s≤1; thus the stated non-local-sphericity follows in those ranks. In rank three all proper residues are finite dihedral for finite parameters, so the blanket non-local-sphericity wording is not valid under the source's own definition. Neither this remark nor its correction is a new open-problem claim.

## 21. Six finite constructions from one marking

The second application takes the odd branch of Corollary O2.2. Retain the GAP TomLib J1 permutation model, of order 175560. Appendix B constructs a marking (a,b,c,d) within that model with

\[
|ab|,|ac|,|ad|,|bc|,|bd|,|cd|=(5,2,2,3,2,5),
\]
\[
(abc)^5=((dcb)^5a)^3=1.
\tag{O13}
\]

It also completes a Todd–Coxeter calculation for the literal presentation with the four involution relations and (O13): the index over ⟨b,c,d⟩ is 1463. That subgroup is a quotient of the finite Coxeter group [3,5] of order 120, so the presented group has order at most 1463·120=175560. The found generating tuple in the TomLib model supplies a quotient of that order; hence this is the source presentation of J1. A valid permutation action alone would not prove the upper bound: the completed exact coset enumeration is a charged computational input.

Set w=(bcd)^5. The certificate proves that w is a nonidentity central involution of ⟨b,c,d⟩. The six source-defined markings and their exact invariants are:

| Geometry | Marking | Pair orders ab,ac,ad,bc,bd,cd in that marking | Maximal-parabolic orders |
|---|---|---|---|
| Γ1 | (a,b,c,d) | 5,2,2,3,2,5 | 120,20,20,60 |
| Γ2 | (a,wb,c,d) | 5,2,2,6,2,5 | 120,20,20,660 |
| Γ3 | (a,b,c,c^d) | 5,2,2,3,3,5 | 120,20,60,60 |
| Γ4 | (b^a,b,c,d) | 5,3,2,3,2,5 | 120,120,20,60 |
| Γ5 | (b^a,b,c,c^d) | 5,3,3,3,3,5 | 120,120,60,60 |
| Γ6 | ((wb)^a,wb,c,d) | 5,6,2,6,2,5 | 120,120,20,660 |

Order-120 parabolics are C2×A5, order-20 ones are D20=C2×D10, order-60 ones A5 and order-660 ones PSL₂(11); D10 here has order ten. Structure identifications use the retained exact GAP algorithms and named group models.

**Corollary O6.1.** Each of these six marked coset systems is a thin regular residually connected rank-four geometry with full type-preserving group J1. They are pairwise nonisomorphic, even allowing type permutations. These are L088 Theorems 3.2, 4.2, 5.2, 5.4, 6.2 and 7.2, including their generation lemmas.

**Proof.** Lemma O2.3 gives the central twist Γ1→Γ2 and preserves its first parabolic. Every endpoint operation has odd endpoint order five, so Corollary O2.2 recovers the same group. Appendix B verifies the two actual subgroup equalities

\[
\langle b,c,d\rangle\cap\langle b,c,d\rangle^a=\langle c,d\rangle,
\qquad
\langle a,b,c\rangle\cap\langle a,b,c\rangle^d=\langle a,b\rangle.
\tag{O14}
\]

They have order ten. The second gives Γ3, the first Γ4. In Γ3, ⟨b,c,c^d⟩=⟨b,c,d⟩ because |cd|=5, and ⟨c,c^d⟩=⟨c,d⟩; hence the same first equality gives Γ5. In Γ2 its first parabolic is unchanged by the twist, so that equality gives Γ6. Thus after the seed and twist cases, four IP proofs reduce to the two meets (O14). Appendix B additionally verifies all 256 ordered marked-subset meets for each of the six markings, so the finite result does not depend on a mistaken reuse of a subgroup identity.

For each marking it checks all sixteen equalities (O2), without presuming that a C-group with a nonstring diagram is a geometry. Recognition lemmas O1.1–O1.2 now give all the geometric conclusions. The six multisets of maximal-parabolic orders in the table are distinct, so no type-permuting isomorphism identifies two geometries. ∎

The definition of Γ3 in L088 §5 duplicates an A5 parabolic, whereas its printed figure labelled Γ3 duplicates C2×A5; the definition of Γ4 has the reverse discrepancy. The source figure labels Γ3 and Γ4 are therefore transposed relative to its definitions. The table follows the definitions. This is a source correction, not a seventh construction.

The two source-mentioned failures also follow from the same certificate. The markings (a,wb,c,c^d) and (a,b,c,wd) still generate J1 and satisfy typed Helly, but each has eight failing ordered IP meets; their panel orders are respectively (2,4,2,2) and (2,2,2,4). Therefore they are not thin. These failures demonstrate why neither endpoint generation nor flag transitivity is a substitute for IP.

### 21.1. Exhaustiveness by a general residue-extension theorem

The original geometry census can be replaced by a short complete search on proper residues. The required group data are the complete TomLib table of J1 subgroup-conjugacy classes, not a list of its geometries.

**Residue-extension theorem O6.2.** Let G be finite and let M₁,…,M\_s represent all conjugacy classes of maximal proper subgroups. For each M\_j enumerate, up to M\_j-conjugation, all unordered k-element sets of involutions whose markings satisfy IP and typed Helly. Append every involution of G outside the subgroup generated by each retained set and apply the same tests. This finds every rank-(k+1) thin regular residually connected geometry whose full type-preserving group is a subgroup of G. To restrict to group G, retain exactly the extensions generating G.

**Proof.** For any such rank-(k+1) geometry, its distinguished marking consists of independent involutions. Omitting one gives a proper subgroup P of its full group and hence of G, so P lies in a conjugate of one M\_j. Its marked coset geometry is the corresponding rank-k residue, thus satisfies both IP and typed Helly. Conjugation into M\_j and then within M\_j puts its unordered markers in the enumerated list. Its omitted involution lies outside P and occurs in the extension loop. Conversely, the tested IP and Helly conditions give exactly the asserted geometries by Lemma O1.1. Ordering the marker set merely orders the type labels. ∎

For completeness, the residue statement used here requires no extension of arbitrary residue automorphisms to G. The base-flag stabilizer acts transitively and freely on the residue's chambers, and the residue is thin and connected. Its full type-preserving group also acts freely, so the stabilizer already is that full group. Walking inside the residue identifies its panel generators. Thus local Helly is a necessary condition for these genuine residues, not an arbitrary extra filter.

**Corollary O6.3.** Up to isomorphism allowing a permutation of types, the six geometries in Corollary O6.1 are all the thin regular residually connected rank-four geometries with group J1. There are none of rank at least five.

**Proof.** Appendix C executes Theorem O6.2 for k=3 and k=4. The retained complete table has forty subgroup classes. Its nonzero containment entries determine seven maximal classes of orders 660,168,120,114,110,60,42. The local counts are:

| Maximal subgroup order | Involutions | Triple orbits | Quadruple orbits | Regular triple orbits | Regular quadruple orbits |
|---:|---:|---:|---:|---:|---:|
|660|55|60|588|42|6|
|168|7|3|3|2|0|
|120|31|108|616|45|7|
|114|19|12|42|0|0|
|110|11|2|4|0|0|
|60|23|58|221|6|2|
|42|7|2|2|0|0|
|Total|—|245|1476|95|15|

The conjugation permutation action on involutions need not be faithful; its image nevertheless has exactly the required orbits on subsets. No local generated subgroup is required to equal its containing maximal subgroup. The 95 retained triples reduce to 70 J1-conjugacy classes. All 100016 possible outside-involution extensions are tested; forty pass with generated group J1, collapsing to precisely six classes. Their maximal-parabolic order multisets are the six distinct ones in Corollary O6.1, which already supplies six pairwise nonisomorphic constructions.

Here is the exact conjugacy test, so equality of numerical invariants is not mistaken for isomorphism. There is one class of 1463 involutions in J1, with centralizer order120. Fix a₀. For each x in an unordered marker set T choose g\_x with x^g\_x=a₀, enumerate T^(g\_xc) for every c∈C\_G(a₀), and take the least sorted tuple of involution indices. These are exactly the conjugates of T containing a₀: every conjugator carrying x to a₀ differs from g\_x on the right by such a c. Consequently keys agree exactly for inner-conjugate unordered markings. There is no assumption that all automorphisms of J1 are inner. The six different parabolic-order multisets prevent any further isomorphism from merging those classes, while the complete six-class upper bound prevents any additional geometry.

For k=4, the fifteen local regular quadruple classes remain fifteen after J1-conjugacy deduplication. All 21352 extensions by an involution outside their generated subgroup fail the full regular-geometry tests. This stage does not discard proper-subgroup targets. If a regular geometry of rank r≥5 existed for J1, fixing r−5 objects of a base chamber would yield a rank-five regular residue with group contained in J1; Theorem O6.2 would have found it. Thus all higher ranks are excluded. This does not assert nonexistence of C-group markings that fail typed Helly. ∎

The source's successful central modifications in §8, when they generate J1 and yield a thin regular geometry, are consequently covered by the same exhaustive classification. The two displayed failures were checked separately above. Appendix B also verifies the incidental source equality N\_G(⟨a,b,c⟩)=⟨a,b,c⟩. Its initial vertex figure is the universal spherical [3,5] geometry, since that parabolic has the full Coxeter order120; its facet is the antipodal hemi-dodecahedral quotient of [5,3], since the A5 quotient has order60 and kernel the unique central order-two subgroup of C2×A5. These conventional spherical identifications use the named classical Coxeter models.

## 22. Mirror covers and their exact kernel obstruction

### 22.1. Mirror, mix, and local kernels

Write an oriented polytope group as \(\Gamma=U_n/N\). Conjugation by \(r_0\) induces the involutory automorphism \(\mu\) of \(U_n\) given by
\[
 \mu(s_1)=s_1^{-1},\qquad \mu(s_2)=s_1^2s_2,
 \qquad \mu(s_i)=s_i\quad(i>2).
\]
Put \(\overline N=\mu(N)\), \(\overline\Gamma=U_n/\overline N\), and
\[
 \Lambda=\operatorname{im}\bigl(U_n\longrightarrow
             \Gamma\times\overline\Gamma\bigr).
\]
This is the marked mix: its generators are the pairs of corresponding generators. It is \(U_n/(N\cap\overline N)\). The isomorphism \(\overline\Gamma\to\Gamma\), induced by \(\mu\), identifies its marking with
\((\sigma_1^{-1},\sigma_1^2\sigma_2,\sigma_3,\ldots)\).

**Universal cover assertion.** \(\Lambda\) is the rotation group of the smallest regular maniplex covering the given oriented polytope.

**Proof.** Its relation kernel \(N\cap\overline N\) is \(\mu\)-invariant and contained in \(N\), so it is a regular cover. If a regular marked quotient \(U_n/J\) covers \(\Gamma\), then \(J\le N\) and \(\mu(J)=J\), whence \(J\le\overline N\). Thus \(J\le N\cap\overline N\), giving the asserted factorization. This proves smallestness in the marked cover order. A regular cover of a chiral polytope is orientable: pull back the two-coloring of its flag graph. Thus the argument includes all regular polytope covers of interest.

Define the chirality subgroup by
\[
 X(\Gamma)=(N\overline N)/N\le U_n/N.
\]
It is trivial exactly when \(N=\overline N\), equivalently when the oriented object is directly regular. The product \(N\overline N\) is the least \(\mu\)-invariant normal subgroup containing \(N\).

**Kernel identity.** Under the first-coordinate identification,
\[
 X(\Gamma)=\{g\in\Gamma:(g,1)\in\Lambda\}.             \tag{V1}
\]
**Proof.** Elements in the right side are exactly images in \(U_n/N\) of words in \(\overline N\). Their image is \(N\overline N/N\). This proves the identity and the chirality interpretation without any counting argument.

Let \(A=\Lambda_{n-1}\), \(B=\Lambda_0\), and \(C=\Lambda_{0,n-1}\) denote the subgroups generated respectively by the first \(n-2\), last \(n-2\), and middle \(n-3\) paired generators. Let \(K,L,M\) be the correspondingly marked facet, vertex-figure, and medial section of the original polytope. For \(\pi:\Lambda\to\overline\Gamma\), the identities needed below are
\[
 A\cap\ker\pi=X(K)\times1,\quad
 B\cap\ker\pi=X(L)\times1,\quad
 C\cap\ker\pi=X(M)\times1.                       \tag{V2}
\]
Here the chirality groups are embedded in the **same** ambient first factor \(\Gamma\) with its fixed base flag. Merely knowing their abstract isomorphism types is insufficient.

For clarity, the local mirror convention in (V2) is not an unmentioned automorphism of a chiral group. On the facet universal subgroup, \(\mu\) is precisely its intrinsic mirror. On the vertex universal subgroup generated by \(s_2,\ldots,s_{n-1}\), the intrinsic mirror is conjugation by \(r_1\). Since \(r_0=s_1r_1\), global conjugation by \(r_0\) is intrinsic conjugation by \(r_1\), followed by conjugation by \(s_1\). Conjugating the second coordinate by the image of \(s_1^{-1}\) therefore identifies the local paired subgroup with the intrinsic mirror mix, without changing its first-coordinate kernel. The same argument applies to the medial subgroup. Formula (V1), applied to those local universal subgroups, proves (V2). It also identifies the end subgroups of \(\Lambda\) with the smallest regular covers of \(K\) and \(L\).


### 22.2. One-line criterion and its local prerequisites

**Lemma V3.1 (regular end).** An oriented rotary polytope having directly regular facets or directly regular vertex-figures has a polytopal smallest regular cover.

**Proof.** Induct on rank; the polygon and directly regular cases are immediate. Suppose the facets \(K\) are directly regular. Their mixes are graph subgroups and hence are isomorphic marked copies of their rotation groups, so \(A\) is polytopal and \(A\cap\ker\pi=1\). A vertex-figure \(L\) has directly regular facets, since these are vertex-figures of \(K\); by induction its mirror mix \(B\) is polytopal. The original mirrored polytope has the intersection property, giving \(\pi(A)\cap\pi(B)=\pi(C)\). The kernel condition in K is automatic because \(A\cap\ker\pi=1\). Hence \(A\cap B=C\), and the recursive correspondence gives polytopality of \(\Lambda\). Duality handles directly regular vertex-figures. This proves, rather than imports, source Proposition 2.2.

For an arbitrary chiral polytope, the two end groups \(A,B\) are polytopal: apply Lemma V3.1 to its facets and vertex-figures using the depth-two regularity theorem. It follows that \(\Lambda\) is polytopal exactly when \(A\cap B=C\). This proves source Proposition 2.3, including its local prerequisites.

**Theorem V3.2 (chiral-cover adapter).** For a chiral polytope \(P\) with compatibly marked sections \(K,L,M\),
\[
 \text{the smallest regular cover of }P\text{ is polytopal}
 \quad\Longleftrightarrow\quad X(K)\cap X(L)\le X(M).       \tag{V3}
\]
**Proof.** The mirrored polytope gives \(\pi(A)\cap\pi(B)=\pi(C)\). By (V2), the kernel condition in K is exactly \(X(K)\cap X(L)\le X(M)\). The preceding paragraph converts \(A\cap B=C\) into polytopality. This proves both directions of source Theorem 3.1.

The following consequences contain all the general conclusions in its Section 3.

1. If either end section is regular, its chirality subgroup is trivial, and (V3) holds. This recovers Remark 3.2 consistently with Lemma V3.1.
2. If the medial section is regular, its chirality subgroup is trivial, so the criterion is \(X(K)\cap X(L)=1\). Since this intersection already lies in \(\Gamma_{n-1}\cap\Gamma_0=\Gamma_{0,n-1}\), this is exactly Corollary 3.3's condition that its intersection with the medial subgroup is trivial.
3. In rank four the medial section is a polygon and its group is \(\langle\sigma_2\rangle\). Thus the criterion says that \(X(K)\cap X(L)\) contains no **nonidentity** power of \(\sigma_2\). This is the logically correct reading of Corollary 3.4; the identity belongs to every subgroup.
4. If the facet and vertex-figure are totally chiral, their chirality groups are their full rotation groups. Their intersection is \(\Gamma_{0,n-1}\), so (V3) holds precisely when \(X(M)=\Gamma_{0,n-1}\), which is total chirality of \(M\). This proves Proposition 3.6.
5. Suppose a chiral facet \(K\) satisfies \(X(K)\cap\Gamma_0(K)=1\). In every chiral extension having these facets, the intersection \(X(K)\cap X(L)\) lies in \(X(K)\cap\Gamma_{0,n-1}=X(K)\cap\Gamma_0(K)=1\). This proves Corollary 3.7 for every such extension, without assuming the existence of extensions of arbitrary rank.


### 22.3. The two infinite-family applications and their exact retained cost

**Square torus maps.** For the chiral maps {4,4}\_(b,c)
in the source's standard parameter convention, bc(b−c)≠0, Lemma L1 gives
X(K)∩⟨v⟩=1. Consequence 5 in §22.2 therefore proves source Example 3.8
for every such extension. No negative or noncanonical parameters are added
to the source contract; no degenerate one-cell map is needed.

**Five tight families.** Here the retained input is substantial and explicit. Cunningham–Pellicer, *Tight chiral polytopes*, J. Algebraic Combin. **54** (2021), 837–878, [DOI](https://doi.org/10.1007/s10801-021-01023-z), constructs the five chiral-facet/chiral-vertex rows of its Table 4. Its published Proposition 11 is cited by the target; the checked [arXiv author version](https://arxiv.org/pdf/2009.04566) calls the corresponding result Proposition 4.2 (printed page 20). For an atomic tight chiral rank-four polytope with both ends chiral it gives
\[
 X(P)=\langle\sigma_2^{q'}\rangle,\qquad q/q'\text{ prime},
 \qquad X(K)=X(L)=X(P)
\]
as embedded subgroups. Although part (b)'s sentence uses “isomorphic”, its proof and the immediately following arguments identify these embedded groups. Alternatively, local chirality is contained in global chirality by (V2), and its nontriviality together with global prime order gives equality. Thus no inference from abstract isomorphism alone is being made.

The retained families and the resulting nonidentity obstruction are:

| Type | Parameter range and choices in the classified family | Element in both local chirality subgroups |
|---|---|---|
| \(\{2m,m^\alpha,2m\}\) | \(m\) odd prime, \(\alpha\ge2\), \(1\le k\le m-1\) | \(\sigma_2^{m^{\alpha-1}}\), order \(m\) |
| \(\{8,2^\beta,8\}\) | \(\beta\ge5\), \(\epsilon_1,\epsilon_2\in\{\pm1\}\) | \(\sigma_2^{2^{\beta-1}}\), order 2 |
| \(\{2^{\beta-1},2^\beta,2^{\beta-1}\}\) | same \(\beta,\epsilon_1,\epsilon_2\) range | same |
| \(\{8,2^\beta,2^{\beta-1}\}\) | same range | same |
| \(\{2^{\beta-1},2^\beta,8\}\) | same range | same |

The parameters refer to the marked groups in that table, not to every polytope sharing the same Schläfli type. Existence, atomicity and the chirality statement are retained from that older work; none of its all-parameter classification is replaced by sampling. The displayed obstruction and consequence 3 immediately prove the target's Example 3.5 for every parameter in those families. The classification of all tight chiral polytopes is neither a new target nor claimed as compressed here.


### 22.4. Two distinct minimal regular polytope covers

Use \(a,b,c\) for the three rotation generators and impose
\[
 (ab)^2=(bc)^2=(abc)^2=1.                         \tag{V4}
\]
Let \(P\) be given by (V4) together with
\[
 a^6=b^9=c^6=1,\quad ba^2=a^2b^4,\quad c^2b=b^4c^2. \tag{V5}
\]
Let \(T\) be given by (V4) and
\[
 a^6=b^9=c^2=1,\quad (ab^{-2})^2=1,
 \quad ab^2a(ab^{-1}a)^2=1,                         \tag{V6}
\]
and let \(T^\delta\) be given by (V4) and
\[
 a^2=b^9=c^6=1,\quad(c^{-1}b^2)^2=1,
 \quad bc^2b(c^{-1}bc^{-1})^2=1.                    \tag{V7}
\]
These are the three literal presentations in the source, not extra quotients chosen to fit its order claims. Put
\[
 R=P\diamond\overline P,\qquad Q=R\diamond T,
 \qquad Q'=R\diamond T^\delta,
\]
where the mirror marking is \((a^{-1},a^2b,c)\).

The complete program in Appendix D starts from the bare finitely presented groups (V5)–(V7), obtains GAP isomorphisms to finite permutation groups, and constructs every mix as the subgroup generated by paired generators in a direct product. Exact GAP group algorithms are retained for this finite proof. RAMP, a group catalogue, random sampling, and the source's output are not dependencies. The checker asserts the following full table; all orders are rotation-group orders.

| Group | Order | Orders of \(a,b,c\) | Facet, vertex orders | End intersection | Mirror automorphism |
|---|---:|---|---|---:|---|
| \(P\) | 324 | 6,9,6 | 54,54 | 9 | no |
| \(T\) | 324 | 6,9,2 | 162,18 | 9 | yes |
| \(T^\delta\) | 324 | 2,9,6 | 18,162 | 9 | yes |
| \(R\) | 972 | 6,9,6 | 162,162 | 27 | yes |
| \(Q\) | 2916 | 6,9,6 | 162,162 | 9 | yes |
| \(Q'\) | 2916 | 6,9,6 | 162,162 | 9 | yes |

In each row \(\langle b\rangle\) has order nine, \(\langle a\rangle\cap\langle b\rangle=\langle b\rangle\cap\langle c\rangle=1\), and (V4) holds. The check tests subgroup equality, not merely numerical resemblance, for the successful end intersections. Thus the retained \(C^+\) correspondence proves that \(P\) is chiral, \(T,T^\delta,Q,Q'\) are directly regular polytopes, and \(R\) is not a polytope. The mirror maps are verified automorphisms; chirality of \(P\) is verified by the failure of the specified generator assignment to define a homomorphism.

The first-coordinate images of the second-projection kernels in the two end subgroups are both exactly \(\langle b^3\rangle\le\Gamma(P)\), of order three, as the checker also asserts. Thus K identifies the same nonpolytopality obstruction directly: the medial polygon has trivial chirality while its nonidentity element \(b^3\) lies in both end chirality groups.

The checker additionally verifies the marked facet isomorphism between \(T\) and \(R\), and the dual isomorphism \((a,b,c)_T\mapsto(c^{-1},b^{-1},a^{-1})_{T^\delta}\). Since \(T\) has two facets, it is the trivial extension of that facet in the source's sense. The maps \(R\to P\), \(Q\to R\), and \(Q'\to R\) are marked epimorphisms, each with kernel order three. Multiplying rotation orders by two gives exactly the source's 648, 1944, and 5832 flags.

For nonisomorphism there is an explicit short certificate:
\[
 w=(bc^{-1})^2ac^2a^{-1},\qquad
 \operatorname{ord}_Q(w)=1,\quad\operatorname{ord}_{Q'}(w)=3.       \tag{V8}
\]
Hence the marked relation kernels differ. An isomorphism of regular polytopes can be composed with a target automorphism to match any chosen base flags, and would then preserve their marked relations. Therefore (V8) excludes an unbased polytope isomorphism as well. This assertion concerns isomorphisms preserving face ranks; it does not assert nonduality.

**Minimality proof.** Any regular polytope cover of \(P\) factors through its smallest regular maniplex \(R\), by §22.1. An intermediate regular polytope between \(Q\) and \(P\) therefore gives an intermediate quotient between \(Q\) and \(R\). The latter map has prime degree three, so its kernel has no intermediate subgroup: the quotient is \(Q\) or \(R\). The second is not a polytope, so \(Q\) is minimal. The same argument proves minimality of \(Q'\). Equation (V8) proves there are at least two different minimal regular polytope covers. This establishes every numerical and structural assertion about the example in source Section 4.

More generally, if the smallest regular maniplex is polytopal, its universal property makes it the unique minimal regular polytope cover. This implication requires no finite hypothesis. Its converse, and the proposed analogous multiplicity for all five tight families, are **not** consequences of K or of this finite example.


### 22.5. Relation to the 2025 general mix criterion and current boundaries

Cunningham–Hubard, *Polytopality criteria for the mix of polytopes and maniplexes*, [arXiv:2506.19334](https://arxiv.org/abs/2506.19334), explicitly recovers this chiral criterion in Corollary 6.17. Its Theorem 6.3 treats a polytope mixed with a premaniplex under the stated symmetry-type admissibility hypotheses: local facet and vertex-figure mixes must be polytopal, and a variance-group intersection inclusion must hold at every relevant flag. Section transitivity can reduce the multiple flag checks. The two-orbit specialization has additional hypotheses, including medial-section transitivity and the specified orbit class with the two end colors excluded. Chiral polytopes satisfy that specialization. Thus the later paper already records the extension; no priority or novelty claim is made here.

Both criteria express the obstruction to polytopality of a specified smallest mixed cover. Neither, by itself, constructs or classifies larger minimal regular polytope covers when that cover fails the intersection condition. §22.4 adds precisely such a construction in one finite case. It does not turn the 2025 criterion into a solution of the target's Section 4 conjectures.

As of 10 October 2026, the arXiv record for 2506.19334 shows only v1, submitted 24 June 2025, and no journal reference. This is a statement about the checked primary record, not a claim that no other publication exists. A bounded current search for the chiral unique/multiple-minimal-cover question, inspection of the full 2025 paper's concluding questions, and a text search of Hubard–Schulte's 2026 *Two-Orbit Polytopes* did not locate a resolution of the two multiplicity conjectures. That absence is not a proof of their current open status. We leave them unproved and make no novelty claim about them.


### 22.6. Version corrections and compression claim

The source extraction prints “no power” in Corollary 3.4 and Example 3.8; this manuscript explicitly says “no nonidentity power”. Definition 2.1's extracted rank-one base case is incompatible with the displayed \(U_1\); we use the standard rank-two cyclic base case. The source's unconditional wording for a mix “polytope” is read as a mix object, which is polytopal only after checking the intersection property. Lost overbars in web extraction are restored using the universal mirror convention, not interpreted as equality of marked copies. The publisher acknowledgement mentions an earlier error in Corollary 3.3; we use and prove the author version's stated condition through (V3), and do not certify the text of an unacquired publisher PDF.


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

Write v\_i=w^iv and e\_i=w^ie. Equation (P3) says that e\_i joins v\_i and v\_(i+1). The walk therefore connects every object in its face residue; additional induced incidences preserve connectivity. In the old residue at v, replace every two-step path e₁–f–e₂ with distinct edges by e₁–P(v,e₁,f)–e₂. Thinness and (P3) justify the replacement. It connects all retained edges in the new vertex residue, and every new incident face meets one of them. The analogous replacement v₁–f–v₂ proves connectivity of each edge residue. Finally an old path through a face can be replaced by a path in its connected vertex–edge residue. Thus the old vertex–edge truncation, and consequently the new geometry with every face attached, is connected.

For the action apply K(c) with X the disjoint union of old vertices and edges. They are retained in Y, and every new face is uniquely encoded by its two actual subsets of X. Equations (Kc2) and (P1) give the core in (P4). A normal subgroup of ⟨a⟩ is either trivial or all of ⟨a⟩. The latter is normal in G exactly when its unique nonidentity element a is central. This proves the exact formula and constructs the faithful image G/kerρ. ∎

This application uses the same core identity as N008's faithful coset action. It keeps the action kernel that a set-valued construction may lose. It asserts neither chamber transitivity of ΠΓ nor injectivity of ρ without further proof.

For an ordinary map, the three successive changes move across an edge to its other endpoint, change the incident face, and continue along that face. These are exactly the alternating corner choices in the conventional Petrie walk. This proves the walk-definition assertion of source Lemma 3.1; it does not forbid repetitions or replace geometric faces by labelled walks.

### 23.2. The thin obstruction and all conditional conclusions

**Theorem P2 (Petrial obstruction and recovery).** If ΠΓ is thin, then |ab|=2 or |ac|=2. The action ρ is faithful and regular and is the full automorphism group of ΠΓ. Applying Π again recovers Γ by an isomorphism fixing all retained vertices and edges.

*Proof.* Set P=P(C). Suppose first that bP≠P. Both P and bP contain e and be at v, so the vertex residue of ΠΓ contains the four-cycle e–P–be–bP–e. A finite cycle in a connected graph of degree two is the entire graph: its vertices already have their two neighbours, so no path can leave it. Lemma P1 therefore says that precisely two old edges are incident with v. In the old thin connected vertex residue both edges have degree two, and each incident face meets both. It is also a four-cycle. Its regular dihedral group ⟨a,b⟩ has four chambers, so |ab|=2.

Suppose instead that bP=P. Since w fixes P, ca=wb fixes P and e. By Lemma O0, the automorphism group of the thin ΠΓ acts freely on chambers. Its edge–face panel stabilizer embeds in the permutation group on that panel's two completions, so ρ(ca)^2=1. Equation (P4) puts (ca)^2 in ⟨a⟩. The rotation/reflection intersection in ⟨a,c⟩ is trivial, hence (ca)^2=1. Since c≠a, this gives |ac|=2. This proves the obstruction without presuming that b always fixes P or that the new action is regular.

Interchanging vertex and edge interchanges b,c and changes cab to bac=w^(-1), preserving the same Petrie sets after that type interchange. We may consequently assume [a,c]=1. Then bwb=w^(-1), bv=v and be=w^(-1)e, so bP=P. The subgroup ⟨b,w⟩=⟨b,ca⟩ is transitive on the incident vertex–edge pairs of P: its elements give (v\_i,e\_i) and (v\_i,e\_(i−1)) for every i. These are distinct pairs, and thinness makes them all pairs at v\_i. Every object of P occurs in the walk. The original chamber-transitive G is transitive on the faces P(gC), so its induced action on ΠΓ is chamber-transitive. K(c) identifies its image with the full regular automorphism group. The preimage of the new panel stabilizing (v,e) is exactly G\_v∩G\_e=⟨a⟩. Equation (Kc3) forces kerρ=1.

At (v,e,P), the new panel involutions are therefore a,b,ca: the last fixes (e,P) and sends v to cv; b fixes (v,P) and changes e; a exchanges the two faces at (v,e). The new generators generate the same group since c=(ca)a. Their geometric marking is established by this action, not by assuming a homomorphism from the old marking. Their second Petrie step is (ca)ab=cb. The cb-orbits of v and e exhaust exactly the old face's vertex–edge shadow: use the alternating normal form in its residue group ⟨b,c⟩ from (P1).

Those old face shadows are distinct. Otherwise let f≠f′ have the same shadow and choose (v,e) in it, moving the base chamber if needed. Thinness gives f′=af. Both f,f′ meet e and be at v. Their four-cycle exhausts the old vertex residue, as above, forcing [a,b]=1. Together with [a,c]=1 this makes a central in G, and (P4) contradicts kerρ=1. Thus old faces correspond bijectively to the second Petrie faces, with precisely their original incidences. This proves the required isomorphism. The vertex–edge-swapped case gives the same conclusion. ∎

The commuting pair is the source's linear-diagram conclusion. Theorem P2 proves its Theorem 1 and the thin-only formulation in its abstract, together with Lemma 3.2(iii),(iv). Lemma P1 gives Lemma 3.2(i). No finite-residue assumption occurs in the walk, connected-cycle, dihedral or gallery arguments.

### 23.3. Corrected assertions and exact controls

The unconditional Lemma 3.2(ii) must be read as the natural homomorphism with kernel (P4), not as an embedding. Indeed take the complete tripartite geometry with two objects of each type. Its full type-preserving group is C₂³, regularly permuting eight chambers. Let a,b,c independently change the face, edge and vertex coordinates. The element cab changes all three, so every Petrie face consists of both vertices and both edges. Deduplication leaves one face. Thus ΠΓ is the complete tripartite geometry with type sizes (2,2,1), its full group is C₂², and the kernel is ⟨a⟩. An order-eight group cannot embed in this order-four automorphism group. This also gives a commuting-pair diagram with nonthin Petrial, so the principal implication has no converse in this diagram convention.

The unnumbered geometric length/order equality also cannot be unconditional. Take C₂×S₃, with a generating its central C₂ and b,c distinct transpositions generating S₃. The coset geometry with stabilizers in (P1) is a six-cycle on three vertices and three edges, joined to two faces. It is thin, residually connected and regular: its twelve chambers form the regular C₂×S₃ action. On retained objects, cab acts as cb, a rotation of order three, while cab itself has order six. Its geometric Petrie face has three vertices and three edges, not length six. This assertion is unnecessary for every proof above.

The optional finite controls construct these examples, a tetrahedron and its vertex–edge interchange, a nonlinear star-transposition S₄ geometry, and two cube markings from explicit permutations. They use the literal chamber changes and deduplicate vertex–edge sets; no changed-marking or faithfulness conclusion is assumed. Their full standard-library program is charged in Appendix E. The two counterexamples above are proved directly, and the infinite theorems do not follow from finite sampling. No source atlas classification, external map-classification theorem, new open-conjecture solution, priority claim or complete Lean certificate is asserted.

## 24. Every source result as an explicit corollary

The labels below preserve the complete Unified source contracts. The operation
contracts are already explicit in Corollaries O4.1, O5.1–O5.3, O6.1 and O6.3;
the mirror-cover contract is Theorem V3.2 with its five consequences, classified
applications and the complete finite minimality proof in §22. A1–A4 recover the four 1998 theorem clauses, B1–B8 the eight numbered 2002 results in the declared scope, and C1–C11 the stated 2005 consequences, with its false unrestricted infinite converse labeled as corrected. Each proof uses only common results proved above and the explicit retained background.

**Corollary A1 — N001 Theorem 1(1).** Every inductively minimal pair satisfies RWPRI, \((2T)_1\), and \((IP)_2\).

*Proof.* B97 and Lemma D identify it with an unweighted tree geometry. Apply Proposition I, including its leaf argument in every residue and its explicit two-edge residues. ∎

**Corollary A2 — N001 Theorem 1(2).** An inductively minimal pair of even rank is PRI.

*Proof.* Its tree has one more vertex than its rank, hence an odd number of vertices. No edge cut is balanced, so Proposition I applies. ∎

**Corollary A3 — N001 Theorem 1(3).** If an inductively minimal pair is not PRI, it is QPRI; failure of PRI occurs exactly when its diagram has a middle. In fact every inductively minimal pair is QPRI.

*Proof.* Proposition I translates a middle into a balanced nonleaf cut, and Lemma O gives the unique chain from that stabilizer to the full group. All other stabilizers are maximal, so their intervals are chains too. This also disambiguates the source's phrase “this is the case”: the middle characterizes failure of PRI, not QPRI by itself. ∎

**Corollary A4 — N001 Theorem 1(4).** An inductively minimal pair is RPRI if and only if its diagram is complete.

*Proof.* Proposition I gives RPRI exactly for stars, whose line graphs are exactly the complete diagrams. ∎

**Corollary B1 — N003 Theorem 1.1, finite-group scope.** For \(N\unlhd G\), \(\mu(G)\leq\mu(G/N)+\mu'(N)\); if \(N\) is abelian, \(\mu(G)\leq\mu(G/N)+\mu'_G(N)\).

*Proof.* Apply Theorem R(a). The finiteness restriction is part of this intake contract; no assertion about infinite maxima is added. ∎

**Corollary B2 — N003 Theorem 2.1.** If \(n\geq7\), every independent generating set \(S\) of \(S_n\) of size \(n-1\) has, for some tree \(T\) on \(\{1,\ldots,n\}\), one of the forms
\[
S=S(T)=\{\tau_e:e\in E(T)\},\qquad
S=\{s\}\cup\{(s\tau_e)^{\epsilon_e}:e\ne d\},
\quad s=\tau_d,\quad\epsilon_e\in\{1,-1\}.
\]
Conversely every displayed set is an independent generating set.

*Proof.* Theorem E is the forward direction; Theorems F and P give generation and independence in both converse directions. ∎

**Corollary B3 — N003 Corollary 2.2.** For \(n\geq7\), the number of actual unordered generating sets of the first form is \(n^{n-2}\). The number of actual unordered sets of the second form is \((n-1)n^{n-2}\). If a three-cycle and its inverse are identified independently in such a set, the second number becomes
\[
\binom n2(n-1)^{n-3}.
\]

*Proof.* Ordinary sets recover their unique edge trees, so Cayley's formula gives the first count. A twisted set has a unique odd member \(s=(a\ b)\). Multiplying each of its other actual members \(h\) by \(s\) recovers a transposition. If \(h=(s\tau_e)^{-1}\), the recovered edge is the conjugate \(s\tau_es\); for an adjacent edge this switches its attachment from \(a\) to \(b\), and for a disjoint edge it changes nothing. Contracting \(\{a,b\}\) gives the same tree before and after any switches. Every such independent switch therefore preserves the tree property. Consequently actual twisted sets are in bijection with trees having one distinguished edge, via the canonical set \(\{s\}\cup\{s\tau_e:e\ne d\}\). This gives \((n-1)n^{n-2}\). Modulo inversion of the three-cycles, the data are exactly the pair \(\{a,b\}\) and a labelled tree on the \(n-1\) blocks obtained by contracting it. Cayley's formula gives the last count. ∎

**Corollary B4 — N003 Corollary 2.3.** Every independent generating set of \(S_n\) of size \(n-1\), for \(n\geq7\), is strongly independent.

*Proof.* Use Theorem E to recognize the marking and Theorems F and P for all subset intersections, including the empty subset. ∎

**Corollary B5 — N003 Corollary 2.4.** If \(n\geq7\), \(B\leq S_n\), and \(\mu(S_n,B)=n-1\), then \(B=1\).

*Proof.* Theorem E proves the stronger conclusion from \(\mu'(S_n,B)=n-1\); W1 bounds either invariant by \(n-1\). ∎

**Corollary B6 — N003 Theorem 3.1 and its stated strong-independence consequence, finite-group scope.** A coset geometry for \(G\) with Borel subgroup \(B\) has rank at most \(\mu'(G,B)\). If it is RWPRI, its rank is at most \(\mu(G,B)\), and the panel choices (A4.3) give a strongly independent relative generating family.

*Proof.* This is Theorem R(b), including equality (A4.4) for every parabolic. ∎

**Corollary B7 — N003 Theorem 3.2.** For \(n\geq7\), independent generating sets of size \(n-1\), modulo conjugation and inversion of individual generators, correspond bijectively to RWPRI coset geometries of rank \(n-1\) for \(S_n\), with the specified action and type renaming understood.

*Proof.* Apply the existence and uniqueness parts of Theorem G. Triviality of the Borel follows from Theorem E; cyclic panels of orders two or three give exactly the stated inversion ambiguity. ∎

**Corollary B8 — N003 Corollary 3.3.** Every source coset geometry for \(S_n\) of rank \(n-1\), with \(n\geq7\), is RWPRI.

*Proof.* Apply the arbitrary-parabolic part of Theorem G. Its balanced-cut and panel argument is needed: merely classifying an extracted independent marking does not identify an arbitrary geometry's original parabolics. ∎


**Corollary C1 — N008 Theorem 2.1, finite specialization and corrected infinite converse.** Relative independent generating families in a finite group descend to and lift from its Frattini quotient, relative to the image of \(B\). This is E4. Its printed unrestricted infinite converse is replaced by E4's explicit additional hypothesis and the preceding counterexample.

**Corollary C2 — N008 Theorem 3.1.** In any finite-rank firm RWPRI coset geometry, \(\Phi(G)\leq H_i\) for every type, including infinite groups. Lemma E0 and firmness give the lattice hypotheses, and E2 yields the stronger \(\Phi(G)\leq B\).

**Corollary C3 — N008 Proposition 3.2.** A coset pregeometry whose type subgroups contain \(N\unlhd G\) is isomorphic to the pregeometry of their images in \(G/N\). This is E3 without any flag-transitivity assumption.

**Corollary C4 — N008 Corollary 3.3.** Every firm RWPRI coset geometry is isomorphic to its Frattini-quotient coset geometry. Combine C2 with E3.

**Corollary C5 — N008 Theorem 3.4.** Every firm RWPRI geometry is isomorphic to one for a Frattini-free group. Apply C4 and the maximal-subgroup correspondence following E3. Quotient and pullback give the fixed-indexed-family bijection motivating the paper.

**Corollary C6 — N008 Proposition 3.5.** A rank-two coset pregeometry is a direct sum exactly when \(H_1H_2=G\). This is the coset-product calculation after E5, with no finiteness or normality assumption.

**Corollary C7 — N008 Lemma 3.6.** If \(U,W<\mathbb F_p^k\), \(W\not\subseteq U\), \(U\) is maximal and \(U\cap W\) is maximal in \(U\), then \(W\) is maximal in \(\mathbb F_p^k\). This is the dimension calculation after E5.

**Corollary C8 — N008 Proposition 3.7.** A firm coset geometry of a finite p-group is RWPRI if and only if it is RPRI. E5 proves the nontrivial implication; the converse is immediate from the definitions.

**Corollary C9 — N008 Theorem 3.8, finite-p-group context.** Every firm RWPRI coset geometry of a finite p-group is a direct sum of primitive geometries of rank one. This is E5; each summand has exactly \(p\) points.

**Corollary C10 — N008 §4.2.** For each standard flag of type \(J\), \(\Phi(H_J)\) must lie in every \(H_J\cap H_i\), \(i\notin J\). This is (A6.7), derived by applying E2 in each residue.

**Corollary C11 — N008 §4.3, action-kernel assertion.** The largest normal subgroup of \(G\) contained in the Borel is \(\operatorname{core}_G(B)=\bigcap_i\operatorname{core}_G(H_i)\). Quotienting by it preserves the geometry and makes the action faithful; for firm RWPRI geometries it contains \(\Phi(G)\). This is (A6.4), E3 and E2.

**Corollary D1 — L032 Theorem 1.2.** For every \(d\ge3\), \(n\ge5\) and \(k_1,\ldots,k_{d-1}\ge2\) with \(\sum_i k_i\le n-1\), there is a regular rank-\(d\) polytope with automorphism group of exact order \(2^n\) and type \(\{2^{k_1},\ldots,2^{k_{d-1}}\}\).

*Proof.* Corollary Q4.1 constructs its marked string C-group using the single square seed and independent cyclic edge kernels. Apply the retained regular-polytope correspondence. ∎

**Corollary D2 — L035 Theorem 1.2.** For \(n\ge10\), \(s,t\ge2\) and \(s+t\le n-1\), there is a regular rank-three polytope of order \(2^n\) and type \(\{2^s,2^t\}\).

*Proof.* Set \(d=3\) in D1. The construction and proof are shared, with no second seed. ∎

**Corollary D3 — L035 Theorem 1.3, all three parts and eight presentations.** Let \(n\ge10\). Every marked rank-three string C-group of order \(2^n\) and type \(\{4,2^{n-s}\}\), for \(s\in\{3,4,5\}\), is exactly one of the following marked presentations. Put \(m=2^{n-s}\), \(r=bc\), \(d_0=(ab)^2\), and \(z=r^{m/2}\). All have common relations
\[
a^2=b^2=c^2=(ac)^2=(ab)^4=r^m=1.
\]
For \(s=3\), add \([d_0,c]=z^\epsilon\), with \(\epsilon=0,1\), giving \(G_1,G_2\). For \(s=4\), add \([d_0,r^2]=z^\epsilon\), with \(\epsilon=0,1\), giving \(G_3,G_4\). For \(s=5\), add
\[
[a,r^2]^2=z^\beta,\qquad [a,r^4]=z^\nu,
\]
with \((\beta,\nu)=(0,0),(1,0),(0,1),(1,1)\), giving \(G_5,G_6,G_7,G_8\), respectively. Conversely each bare presentation has the stated exact order, type and IP; the alternatives are distinct as marked string C-groups.

*Proof.* Theorem Q6.1 gives the bounded cyclic quotient. The explicit models and invariant relations in §12 construct and distinguish every listed marking. Theorem Q7.1 gives completeness, excludes the nonlifting order-256 relation patterns and identifies every bare presentation by its order bound. The complete finite relation computation and its exhaustiveness proof are in Appendix A. Thus the converse does not assume the presented group already has the desired order or IP. ∎

**Corollary D4 — F013 Theorem 1.1.** Every finite nondegenerate two-group string C-group of rank \(d\ge2\) admits a marked epimorphism onto the canonical string C-group \(G(C_d)\) of order \(2^{2d-1}\).

*Proof.* Its noncommuting diagram is a path. Theorem Q5.3 identifies its quotient by \(\gamma_3(G)\) with the explicit vertex-and-edge model. Corollary Q5.4 identifies that model with \(G(C_d)\). The Frattini/basis input is the common Theorem S, and the graded support proof is included in §11. ∎

**Corollary D5 — F013 Theorem 1.2.** Every finite nondegenerate regular rank-\(d\) polytope with two-group automorphism group, \(d\ge2\), covers \(C_d\).

*Proof.* Apply D4 and the retained marked quotient/cover correspondence. The false auxiliary source kernel is not needed; §16 proves its precise failure. ∎

**Corollary D6 — F016 Theorem 5.1(a–d).** For \(d\ge3\) and \(n_3,\ldots,n_d\ge5\), there is a finite regular rank-\(d\) polytope whose consecutive rank-three sections are exactly \(\{4,4\}_{(n_3)},\ldots,\{4,4\}_{(n_d)}\), where each square map has automorphism group of order \(2^{n_j}\). Its group has order \(2^{\sum_{j=3}^d n_j-3(d-3)}\). For \(d\ge4\) it is \((d-4,d-1)\)-flat and hence flat. It has FAP with respect to its co-\((d-4)\)-faces, co-\((d-3)\)-faces and facets, with the rank-three co-\((-1)\)-face interpreted as the whole-polytope cut.

*Proof.* The square recognition theorem and compatible product Q2.3 give the exact local sections. Equation (Q8.1) gives the order. The last product factorization gives flatness through the retained coset-face criterion, and Q2.2 supplies the actual deletion retractions and all FAP cuts. These arguments, including the rank-three convention, are all in §14. ∎

**Corollary D7 — F016 Theorem 5.3.** The automorphism group in D6 is precisely the quotient of the universal regular polytope group of generalized type \(\{\{4,4\}_{(n_3)},\ldots,\{4,4\}_{(n_d)}\}\) by
\[
[(r_ir_{i+1})^2,(r_{i+2}r_{i+3})^2]=1
\quad(0\le i\le d-4).
\]

*Proof.* Section 14 proves Boolean deletions and IP for the bare local presentation, so the universal regular polytope exists by the ordinary C-group correspondence. Lemma Q8.1 makes the third-lower-central triple kernels normal. The local lattice indices, global class-two bound and order comparison identify the quotient with the actual product construction. This retains the source's entire presentation claim and repairs the diagonal-translation order step. ∎

**Corollary D8 — F016 Theorem 6.1(a–b).** Let \(d\ge4\), \(n_3,\ldots,n_{d-1}\ge5\), and \(m_{d-1}\ge5\). There is an alternating semiregular rank-\(d\) polytope with regular facet types
\[
(n_3,\ldots,n_{d-2},n_{d-1}),\qquad
(n_3,\ldots,n_{d-2},m_{d-1}).
\]
Its full automorphism group has order
\[
2^{\sum_{j=3}^{d-2}n_j+n_{d-1}+m_{d-1}-3(d-3)}
\]
if the last parameters differ, and twice this order if they agree. At \(d=4\), the shared list is empty and the common facet of the two facets is a square. The remaining co-\((d-4)\)-section is not separately prescribed.

*Proof.* Use D6 for the two facet groups, Q2.3 for the branched compatible product, and the exact retained Monson–Schulte assembly/full-automorphism input in §15. The orders there give the displayed formula, while unequal facet orders exclude an interchange and equal marked constructions admit it. ∎

**Corollary D9 — F016 Theorem 7.1.** For a regular input polytope of rank \(d\ge3\) whose group is a finite or infinite two-group in the source's convention, its free regular extension has rank \(d+1\) and finitely generated infinite automorphism group with every finite-order element of two-power order.

*Proof.* The retained regular free-extension theorem gives the geometry and its amalgam. Lemma Q9.1 proves infinitude, finite generation and the finite-torsion assertion, including infinite input. ∎

**Corollary D10 — F016 Theorem 7.2.** For an oriented chiral input polytope of rank \(d\ge3\) with directly regular facets and finite or infinite two-group automorphism group, its free oriented chiral extension has rank \(d+1\) and a finitely generated infinite two-group in the same convention.

*Proof.* The retained Schulte–Weiss theorem gives the geometry and amalgam over the facet rotation group. That rotation group embeds in the input group; its full facet group is an index-two extension, so Lemma Q9.1 transfers the torsion property and proves the extension conclusions. No full-facet embedding in the chiral group is assumed. ∎

**Corollary D11 — F016 Theorem 7.3.** Let two regular rank-\(d\) polytopes, \(d\ge3\), have isomorphic facets and finite or infinite two-group automorphism groups. Their universal alternating semiregular extension has rank \(d+1\) and finitely generated infinite two-group automorphism group, with the additional branch swap precisely when the two facets of the extension are isomorphic.

*Proof.* The retained universal alternating-extension theorem gives the group amalgam and possible index-two extension. Lemma Q9.1 gives all three group properties in both cases. ∎


**Corollary Z1 — N013's toroidal labels.** For the r-cube input, r≥3, the
dual generalized cube is {4,3^(r−2),4}\_(4,0,…,0), and its halving is the
affine fork toroidal hypertope {4,3^(r−3),3/3}\_(4,0,…,0). For r=2 the
two maps are {4,4}\_(4,0) and {4,4}\_(2,2). The complete face-poset,
marking and lattice proofs are Lemmas T1–T2 and the rank-three basis change
in §9, with regularity supplied by Corollary O4.1. ∎

**Corollary Z2 — N016's proved conclusions.** With the exact author-version
scope and retained inputs stated in §1 and §22, source Propositions
2.2–2.4, Theorem 3.1, Corollaries 3.3–3.4 and 3.7, Proposition 3.6,
Examples 3.5 and 3.8, the uniqueness implication and the finite pair of
minimal regular covers all follow from Theorem K(0), the local mirror
identities, the proved regular-end induction, Lemma L1, the retained
five-family input, and the exact Appendix D calculation. Each implication
and the prime-degree minimality argument is written in §22; the two
source multiplicity conjectures remain unproved. ∎

**Corollary Z3 — L108's corrected principal contract.** A thin regular residually connected rank-three geometry with thin Petrial has a commuting pair in its diagram. Its Petrial is residually connected; under thinness it has the same full regular automorphism group and its second Petrial recovers the original geometry. The map walk is the usual Petrie walk. Unconditionally the natural action has kernel core\_G(⟨a⟩), rather than necessarily being an embedding.

*Proof.* Lemma P1 supplies residual connectivity and the exact kernel through K(c). Theorem P2 proves the obstruction, faithfulness and biduality without finite-group assumptions. The explicit three-step walk in §23.1 proves source Lemma 3.1. Section 23.3 proves why the unconditional source inclusion and length/order equality cannot be counted as literal rederivations. These are Theorem 1 and the valid numbered conclusions of Lemma 3.2, with its part (ii) expressly corrected. ∎

## 25. Shared proof, retained costs and source boundaries

Theorem K(0) replaces the two copies of the same image-lifting proof;
K(a) is its marked corollary. K(b) retains its distinct exact-coset proof.
Lemma L1 presents the square affine model and its linear-part obstruction
once, beside the full square-seed normal-form proof. The Gray-code bridge
adds a necessary proof previously retained as a lattice identification.
The relative-generation and primitive-coordinate core remains shared by
the finite-p and two-group branches. Endpoint conjugation shares geometric
recognition with the J1 census and generalized-cube applications, but is
not assumed to be a homomorphic image of the old marking.

The laminar forest proof cannot be deleted: adjacent tree transpositions
satisfy an odd braid relation that Boolean deletion would destroy. The
cyclic-model proof, its catalogue-relative order-256 census, all FAP cuts,
the complete J1 residue census and all mirror/local-polytopality arguments
also remain. No theorem of this manuscript claims to replace their
distinct hypotheses by a generic matrix computation. The newer marked
parabolic comparison theorem is not used: no application-specific product
injectivity has been established that would shorten the endpoint proof.

The necessary finite programs are printed in full in Appendices A–D. The optional Petrial controls are also fully charged in Appendix E; their finite output is not a substitute for the uniform proof.
Appendix A uses the complete SmallGroups order-256 catalogue; Appendices
B–C use the complete TomLib J1 subgroup table and exact algorithms;
Appendix D starts from bare finite presentations and uses exact GAP
algorithms without a finite-group catalogue. Existing exact-hash component
replays certify those unchanged programs; extraction and any new runner
are checked separately. Runtime versions, data hashes, logs and output
certificates remain charged audit artifacts. No new Lean formalization of
the complete arguments is claimed. A future common measurement must count
all proof prose and code, charge wrappers/outputs consistently and declare
the retained background. There is no numerical ratio in this draft.

L108's set-valued operation is included with the exact K(c) kernel and the corrected §23 contract; its former exclusion in the ten-source assembly remains part of that earlier frozen record. The current branch uses no atlas or map classification. Ens's full
toroidal classification, the older tight-family classification, N009's
order-1024 census, and the phase46 minimal-cover exploration are not new
intake entries. N013's comparison with every example in its reference [9]
and its unused alternating-semiregular identification remain unproved
auxiliary assertions. Its Remark 4.1 is retained only with the rank
qualification proved in §20. The component ledgers retain every other
literal-versus-corrected boundary.

Exact source versions are the complete rendered N001 authored text,
twelve-page N003 author manuscript, nine-page N008 journal PDF, revised
L032 author PDF dated 8 November 2019, L035 arXiv:1802.08947v2,
F013 arXiv:2605.20691v1, F016 arXiv:2512.15511v1, L088's ten-page
journal PDF and N013 arXiv:2001.11082v1. N016 is the eight-page author
manuscript headed 25 July 2023; its 2024 journal publication is confirmed,
but the publisher full text was not acquired. L108 uses the complete seven-page authored browser rendering corresponding to its 2001 publication, without a primary PDF. This extension freshly read that complete text and the complete phase25 proof, checker, contract and independent review; it inherits unchanged earlier source readings. Component approval does not approve this altered assembly.

## Appendix A. The finite completeness calculation, fully specified

The following GAP algorithm is part of the proof cost in §13. The only
classification supplied to it is the complete catalogue of groups of
order 256. All arithmetic, Frattini groups, conjugacy classes,
centralizers and intersections are exact finite group operations.

```gap
# Fresh Compress_B replay. Exact census code retained and charged in manuscript Appendix A.
# Exhaustive marked {4,8}, order256 census using the GAP SmallGroups library.
# The three involutions must have independent images in G/Phi(G), so the
# abelianization is exactly C2^3. Conjugacy representatives for r=b*c and
# centralizer orbits for c lose no marked generating triples.
SetInfoLevel(InfoWarning,0);
Main:=function()
local started,ids,total,active,hits,counts,id,g,phi,rs,invs,hom,found,r,
 candidates,cr,c,b,plane,aas,right,a,d,z,matches;
started:=Runtime();;
ids:=IdsOfAllSmallGroups(256,AbelianInvariants,[[2,2,2]]);;
Print("GAP ",GAPInfo.Version," SmallGroups ",PackageInfo("smallgrp")[1].Version,
 " eligible_groups=",Length(ids),"\n");
total:=0;; active:=0;; hits:=[];; counts:=[0,0,0,0];;
for id in ids do
 g:=SmallGroup(id);;
 phi:=FrattiniSubgroup(g);;
 rs:=Filtered(List(ConjugacyClasses(g),Representative),x->Order(x)=8 and not x in phi);;
 if Length(rs)=0 then continue;fi;
 active:=active+1;
 invs:=Filtered(Elements(g),x->Order(x)=2);;
 hom:=NaturalHomomorphismByNormalSubgroup(g,phi);;
 found:=[];;
 for r in rs do
  candidates:=Set(Filtered(invs,c->r^c=r^-1 and not Image(hom,c) in Group(Image(hom,r))));;
  cr:=Elements(Centralizer(g,r));;
  while Length(candidates)>0 do
   c:=candidates[1];;
   candidates:=Difference(candidates,Set(cr,x->c^x));;
   b:=r*c;; plane:=Group(Image(hom,r),Image(hom,c));;
   aas:=Filtered(invs,a->not Image(hom,a) in plane and a*c=c*a and Order(a*b)=4);;
   right:=Group(b,c);;
   for a in aas do
    if Size(Intersection(Group(a,b),right))<>2 then continue;fi;
    total:=total+1;; d:=(a*b)^2;; z:=r^4;;
    matches:=[];;
    if Comm(a,r^2)^2=One(g) and Comm(a,r^4)=One(g) then Add(matches,1);fi;
    if Comm(a,r^2)^2=z and Comm(a,r^4)=One(g) then Add(matches,2);fi;
    if Comm(d,r^2)=z then Add(matches,3);fi;
    if Comm((r^2)^a,r)=z then Add(matches,4);fi;
    if Length(matches)<>1 then
     Print("UNEXPECTED ",id," matches=",matches," tuple=",[a,b,c],"\n");
     QUIT_GAP(1);
    fi;
    counts[matches[1]]:=counts[matches[1]]+1;;
    AddSet(found,matches[1]);;
   od;
  od;
 od;
 if Length(found)>0 then
  Add(hits,[id,found]);;
  Print("HIT ",id," patterns=",found," cumulative=",total," ms=",Runtime()-started,"\n");
 fi;
od;
Print("PASS groups=",Length(ids)," active=",active," triples=",total,
 " pattern_counts=",counts," hits=",hits," ms=",Runtime()-started,"\n");
end;
Main();
QUIT;
```

The excluded catalogue groups cannot have the required marking by
Burnside. For the included groups, \(r,c,a\) pass a basis test in the
Frattini quotient, and \(a,b,c\) are recovered by the invertible change
\(b=rc\); generation follows. The normalizations by conjugation never
lose a word relation or parabolic-intersection outcome. Conversely any
admissible marking normalizes to one examined in the loops. The program records the row identifiers in §13; only the exhaustive relation implications, not those identifiers or anchored multiplicities, enter the infinite-parameter proof. Source and output hashes, runtime versions and fresh-run status
belong to the ledger. No computation of groups above order 256 is used
in the completeness argument.



## Appendix B. Complete finite construction certificate

The following code is part of this manuscript, not an excluded implementation appendix. It searches for its own source marking in the retained ambient group, rather than reading an earlier geometry census or a hard-coded witness. It then verifies the presentation upper bound, every marked intersection and all required typed-Helly equalities.

```gap
# Entire finite certificate for Compress_C. No geometry census is read.
LoadPackage("tomlib");;
SizeScreen([100000,24]);;
CheckC:=function(test,msg) if not test then Error(msg);fi;end;;
G:=UnderlyingGroup(TableOfMarks("J1"));;
CheckC(Size(G)=175560,"ambient J1 order");;
FindSeedC:=function(K)
 local a,b,c,d,iv,bs;
 a:=GeneratorsOfGroup(K)[1];
 CheckC(Order(a)=2,"ambient first generator");
 iv:=Filtered(Elements(Centralizer(K,a)),x->Order(x)=2);
 for d in iv do
  if d=a then continue;fi;
  bs:=Filtered(Elements(Centralizer(K,d)),x->Order(x)=2 and Order(a*x)=5);
  for c in iv do
   if Order(c*d)<>5 then continue;fi;
   for b in bs do
    if Order(b*c)=3 and (a*b*c)^5=One(K)
      and ((d*c*b)^5*a)^3=One(K) and Group(a,b,c,d)=K then
     return [a,b,c,d];
    fi;
   od;
  od;
 od;
 Error("no source seed");
end;;
s:=FindSeedC(G);;
pairs:=Combinations([1..4],2);;
CheckC(List(pairs,p->Order(s[p[1]]*s[p[2]]))=[5,2,2,3,2,5],"seed pairs");;
CheckC(Normalizer(G,Group(s{[1,2,3]}))=Group(s{[1,2,3]}),"seed facet normalizer");;
# Exact upper bound for the literal source presentation.
F:=FreeGroup("a","b","c","d");; u:=GeneratorsOfGroup(F);;
rels:=Concatenation(List(u,x->x^2),List([1..6],i->
 (u[pairs[i][1]]*u[pairs[i][2]])^[5,2,2,3,2,5][i]),
 [(u[1]*u[2]*u[3])^5,((u[4]*u[3]*u[2])^5*u[1])^3]);;
Q:=F/rels;; q:=GeneratorsOfGroup(Q);;
ct:=CosetTable(Q,Subgroup(Q,q{[2,3,4]}));;
CheckC(Length(ct[1])=1463,"presentation coset index");;
CheckC(Size(Group(List([1,3,5,7],i->PermList(ct[i]))))=175560,"presentation image");;
w:=(s[2]*s[3]*s[4])^5;;
CheckC(Order(w)=2 and ForAll(s{[2,3,4]},x->Comm(w,x)=()),"twist center");;
marks:=[s,[s[1],w*s[2],s[3],s[4]],
 [s[1],s[2],s[3],s[3]^s[4]],
 [s[2]^s[1],s[2],s[3],s[4]],
 [s[2]^s[1],s[2],s[3],s[3]^s[4]],
 [(w*s[2])^s[1],w*s[2],s[3],s[4]]];;
CheckC(Intersection(Group(s{[2,3,4]}),Group(s{[2,3,4]})^s[1])
 =Group(s{[3,4]}),"left overlap");;
CheckC(Intersection(Group(s{[1,2,3]}),Group(s{[1,2,3]})^s[4])
 =Group(s{[1,2]}),"right overlap");;
VerifyC:=function(t)
 local ss,subs,a,b,ip,pars,i,j,J,rows,T,common,expected,h,pan;
 ss:=Combinations([1..4]);
 subs:=List(ss,J->Group(Concatenation([()],t{J})));
 ip:=0;
 for a in [1..16] do for b in [1..16] do
  if Intersection(subs[a],subs[b])<>subs[Position(ss,Intersection(ss[a],ss[b]))]
   then ip:=ip+1;fi;
 od;od;
 pars:=List([1..4],i->Group(t{Difference([1..4],[i])}));
 h:=[];
 for i in [1..4] do
  rows:=[];
  for j in Difference([1..4],[i]) do
   T:=Intersection(pars[i],pars[j]);
   rows[j]:=Set(List(RightTransversal(pars[j],T),x->RightCoset(pars[i],x)));
  od;
  for J in Combinations(Difference([1..4],[i])) do
   if Length(J)<2 then continue;fi;
   common:=Length(Intersection(rows{J})); T:=Intersection(pars{J});
   expected:=Index(T,Intersection(T,pars[i]));
   Add(h,[i,J,common,expected]);
  od;
 od;
 pan:=List([1..4],i->Size(Intersection(pars{Difference([1..4],[i])})));
 return rec(order:=Size(Group(t)),pairs:=List(pairs,p->Order(t[p[1]]*t[p[2]])),
  parabolics:=List(pars,Size),types:=List(pars,StructureDescription),
  ip_failures:=ip,helly:=h,borel:=Size(Intersection(pars)),panels:=pan);
end;;
expectedP:=[[120,20,20,60],[120,20,20,660],[120,20,60,60],
 [120,120,20,60],[120,120,60,60],[120,120,20,660]];;
expectedPairs:=[[5,2,2,3,2,5],[5,2,2,6,2,5],[5,2,2,3,3,5],
 [5,3,2,3,2,5],[5,3,3,3,3,5],[5,6,2,6,2,5]];;
for i in [1..6] do
 CheckC(ForAll(marks[i],x->Order(x)=2),"marker orders");
 r:=VerifyC(marks[i]);
 CheckC(r.order=175560 and r.ip_failures=0,"generation and IP");
 CheckC(r.parabolics=expectedP[i] and r.pairs=expectedPairs[i],"source tables");
 CheckC(r.types=List(r.parabolics,o->["C2 x A5","D20","A5","PSL(2,11)"]
  [Position([120,20,60,660],o)]),"parabolic isomorphism types");
 CheckC(r.borel=1 and r.panels=[2,2,2,2],"thinness");
 CheckC(ForAll(r.helly,z->z[3]=z[4]),"typed Helly");
 Print("GEOMETRY ",i," PAIRS ",r.pairs," PARABOLICS ",r.parabolics,
  " TYPES ",r.types," IP_MEETS 256 HELLY_ROWS ",Length(r.helly)," PASS\n");
od;
CheckC(Length(Set(List(expectedP,SortedList)))=6,"pairwise nonisomorphism");;
bad:=[[s[1],w*s[2],s[3],s[3]^s[4]],[s[1],s[2],s[3],w*s[4]]];;
for i in [1..2] do
 r:=VerifyC(bad[i]);
 CheckC(r.order=175560 and r.ip_failures=8 and r.borel=1,"negative scope");
 CheckC(r.panels=[[2,4,2,2],[2,2,2,4]][i],"negative panel");
 CheckC(ForAll(r.helly,z->z[3]=z[4]),"negative Helly");
 Print("NEGATIVE ",i," IP_FAILURES ",r.ip_failures," PANELS ",r.panels," PASS\n");
od;
Print("COMPRESS_C_J1_PASS\n");
QUIT;
```


## Appendix C. Complete exhaustive residue-extension certificate

This program reads no geometry representative list. It derives the maximal-subgroup classes from the complete group table, enumerates local unordered marker orbits, tests full IP and typed Helly, and extends every retained proper residue by all possible outside involutions. Early rejection only uses failure of the necessary irredundance condition. All six rank-four classes and the absence of rank-five residues are outputs of the search; their asserted final counts are checked after enumeration.

```gap
# Complete finite J1 geometry census by proper-residue extension.
# Relative to the complete TomLib J1 subgroup table, not a geometry census.
LoadPackage("tomlib");;
SizeScreen([100000,24]);;
tom:=TableOfMarks("J1");;G:=UnderlyingGroup(tom);;
ids:=MaximalSubgroupsTom(tom)[1];;
ns:=Length(OrdersTom(tom));; incidence:=SubsTom(tom);;
derived:=Filtered([1..ns-1],i->not ForAny([i+1..ns-1],j->i in incidence[j]));;
if derived<>SortedList(ids) or ns<>40 then Error("maximal subgroup catalogue");fi;
Print("MAXIMAL_CLASSES ",derived," ORDERS ",List(ids,i->Size(RepresentativeTom(tom,i))),"\n");;
CheckCensus:=function(t)
 local n,I,i,j,k,K,L,ss,subs,P,rows,J,common,T;
 n:=Length(t); I:=[1..n];
 # Irredundance is necessary for IP and rejects most global extensions.
 for i in I do
  K:=Group(t{Difference(I,[i])});
  if t[i] in K then return fail;fi;
 od;
 ss:=Combinations(I);
 subs:=List(ss,J->Group(Concatenation([()],t{J})));
 for i in [1..Length(ss)] do for j in [i+1..Length(ss)] do
  if Intersection(subs[i],subs[j])<>subs[Position(ss,Intersection(ss[i],ss[j]))]
   then return fail;fi;
 od;od;
 P:=List(I,i->Group(t{Difference(I,[i])}));
 for i in I do
  rows:=[];
  for j in Difference(I,[i]) do
   K:=Intersection(P[i],P[j]);
   rows[j]:=Set(List(RightTransversal(P[j],K),x->RightCoset(P[i],x)));
  od;
  for J in Combinations(Difference(I,[i])) do
   if Length(J)<2 then continue;fi;
   T:=Intersection(P{J});
   if Length(Intersection(rows{J}))<>Index(T,Intersection(T,P[i]))
    then return fail;fi;
  od;
 od;
 return rec(marking:=t,order:=Size(Group(t)),parabolics:=List(P,Size));
end;;
localReps:=rec();;
for k in [3,4] do
 localReps.(String(k)):=[];
 for id in ids do
  M:=RepresentativeTom(tom,id);
  iv:=Filtered(Elements(M),x->Order(x)=2);
  A:=Image(ActionHomomorphism(M,iv,OnPoints));
  oo:=OrbitsDomain(A,Combinations([1..Length(iv)],k),OnSets);
  count:=0;
  for o in oo do
   t:=iv{o[1]}; r:=CheckCensus(t);
   if r<>fail then Add(localReps.(String(k)),t);count:=count+1;fi;
  od;
  Print("LOCAL ",k," MAXIMAL ",id," ORDER ",Size(M)," ORBITS ",Length(oo)," REGULAR ",count,"\n");
 od;
 Print("LOCAL_TOTAL ",k," ",Length(localReps.(String(k))),"\n");
od;
Print("LOCAL_ENUMERATION_DONE\n");
involClasses:=Filtered(ConjugacyClasses(G),c->Order(Representative(c))=2);;
if Length(involClasses)<>1 then Error("single involution class required");fi;
ivG:=SortedList(Elements(involClasses[1]));;
if Length(ivG)<>1463 then Error("involution count");fi;
a0:=ivG[1];; C0:=Elements(Centralizer(G,a0));;
if Length(C0)<>120 then Error("involution centralizer");fi;
conjCache:=[];;
CanonicalCensus:=function(t)
 local ans,x,p,g,c,key;
 ans:=fail;
 for x in t do
  p:=PositionSorted(ivG,x);
  if not IsBound(conjCache[p]) then
   g:=RepresentativeAction(G,x,a0);
   if g=fail or x^g<>a0 then Error("involution conjugator");fi;
   conjCache[p]:=g;
  fi;
  g:=conjCache[p];
  for c in C0 do
   key:=SortedList(List(t,y->PositionSorted(ivG,y^(g*c))));
   if ans=fail or key<ans then ans:=key;fi;
  od;
 od;
 return ans;
end;;
globalClasses:=[];;fiveClasses:=[];;classParabolics:=[];;
for k in [3,4] do
 keys:=[];unique:=[];
 for t in localReps.(String(k)) do
  key:=CanonicalCensus(t);
  if not key in keys then Add(keys,key);Add(unique,t);fi;
 od;
 Print("GLOBAL_LOCAL_ORBITS ",k," ",Length(unique),"\n");
 tested:=0;passed:=0;start:=Runtime();
 for i in [1..Length(unique)] do
  t:=unique[i];K:=Group(t);
  for x in ivG do
   if x in K then continue;fi;
   tested:=tested+1;
   r:=CheckCensus(Concatenation(t,[x]));
   if r=fail then continue;fi;
   if k=3 and r.order<>175560 then continue;fi;
   passed:=passed+1;
   key:=CanonicalCensus(r.marking);
   if k=3 and not key in globalClasses then
    Add(globalClasses,key);Add(classParabolics,SortedList(r.parabolics));
    Print("NEW_RANK4 ",key," PARABOLICS ",SortedList(r.parabolics),"\n");
   elif k=4 and not key in fiveClasses then
    Add(fiveClasses,key);
    Print("NEW_RANK5 ",key," GROUP_ORDER ",r.order," PARABOLICS ",r.parabolics,"\n");
   fi;
  od;
  Print("EXTENSION ",k+1," LOCAL ",i,"/",Length(unique)," TESTED ",tested,
   " PASSED ",passed," SECONDS ",(Runtime()-start)/1000,"\n");
 od;
 Print("STAGE_TOTAL ",k+1," TESTED ",tested," ACCEPTED ",passed,"\n");
od;
Print("RANK4_CLASSES ",Length(globalClasses)," RANK5_CLASSES ",Length(fiveClasses),"\n");
if Length(globalClasses)<>6 or Length(fiveClasses)<>0 then Error("geometry classification");fi;
expected:=[[20,20,60,120],[20,20,120,660],[20,60,60,120],
 [20,60,120,120],[60,60,120,120],[20,120,120,660]];;
if SortedList(classParabolics)<>SortedList(expected) then Error("six distinct types");fi;
PrintTo("phase40_compress_operations_exhaustive_classes.json",
 [globalClasses,fiveClasses,classParabolics],"\n");;
Print("COMPRESS_C_EXHAUSTIVE_PASS\n");
QUIT;
```
## Appendix D. Complete chiral-cover finite certificate

This complete program begins with the literal source presentations,
constructs their mirror mixes, checks every relevant C+ intersection and
marked cover, verifies local chirality, and supplies the distinguishing
word. The abstract universal-property and minimality proofs are in §22.
Its bytes are identical to the frozen phase41 program.

```gap
# All source presentations are literal. GAP's exact finitely presented/permutation
# group algorithms are retained; this is not a Lean kernel certificate.
SetInfoLevel(InfoWarning,0);;
check:=function(ok,label) if not ok then Print("FAIL ",label,"\n");QUIT_GAP(1);fi;end;;
F:=FreeGroup("a","b","c");; a:=F.1;; b:=F.2;; c:=F.3;;
base:=[(a*b)^2,(b*c)^2,(a*b*c)^2];;
prs:=rec(P:=Concatenation([a^6,b^9,c^6],base,[b*a^2*(a^2*b^4)^-1,c^2*b*(b^4*c^2)^-1]),T:=Concatenation([a^6,b^9,c^2],base,[(a*b^-2)^2,a*b^2*a*(a*b^-1*a)^2]),Td:=Concatenation([a^2,b^9,c^6],base,[(c^-1*b^2)^2,b*c^2*b*(c^-1*b*c^-1)^2]));;
make:=function(name)
 local fp,iso,g,s;
 fp:=F/prs.(name);iso:=IsomorphismPermGroup(fp);g:=Image(iso);
 check(IsBijective(iso),Concatenation(name," fp isomorphism"));
 s:=List(GeneratorsOfGroup(fp),x->Image(iso,x));
 check(ForAll(prs.(name),w->MappedWord(w,GeneratorsOfGroup(F),s)=One(g)),Concatenation(name," literal relators"));
 return rec(g:=g,s:=s);
end;;
mix:=function(A,B)
 local d,e1,e2,s;
 d:=DirectProduct(A.g,B.g);e1:=Embedding(d,1);e2:=Embedding(d,2);
 s:=List([1..3],i->Image(e1,A.s[i])*Image(e2,B.s[i]));
 return rec(g:=Group(s),s:=s);
end;;
P:=make("P");;T:=make("T");;Td:=make("Td");;
Pm:=rec(g:=P.g,s:=[P.s[1]^-1,P.s[1]^2*P.s[2],P.s[3]]);;
R:=mix(P,Pm);;Q:=mix(R,T);;Qd:=mix(R,Td);;
expected:=rec(P:=[324,[6,9,6],[54,54],9,false],T:=[324,[6,9,2],[162,18],9,true],Td:=[324,[2,9,6],[18,162],9,true],R:=[972,[6,9,6],[162,162],27,true],Q:=[2916,[6,9,6],[162,162],9,true],Qd:=[2916,[6,9,6],[162,162],9,true]);;
A:=P;;
for name in ["P","T","Td","R","Q","Qd"] do
 A:=ValueGlobal(name);f:=Group(A.s{[1,2]});v:=Group(A.s{[2,3]});m:=Group([A.s[2]]);
 reg:=GroupHomomorphismByImages(A.g,A.g,A.s,[A.s[1]^-1,A.s[1]^2*A.s[2],A.s[3]]);
 row:=[Size(A.g),List(A.s,Order),[Size(f),Size(v)],Size(Intersection(f,v)),reg<>fail];
 check(row=expected.(name),Concatenation(name," exact row"));
 check(Size(m)=9,Concatenation(name," medial"));
 check(Intersection(Group([A.s[1]]),m)=TrivialSubgroup(A.g),Concatenation(name," facet IP"));
 check(Intersection(Group([A.s[3]]),m)=TrivialSubgroup(A.g),Concatenation(name," vertex IP"));
 check(ForAll(base,w->MappedWord(w,GeneratorsOfGroup(F),A.s)=One(A.g)),Concatenation(name," rotation relations"));
 if reg<>fail then check(IsBijective(reg),Concatenation(name," mirror automorphism"));fi;
 if name<>"R" then check(Intersection(f,v)=m,Concatenation(name," end IP"));else check(Intersection(f,v)<>m,"R fails IP");fi;
 Print("ROW ",name," ",row,"\n");
od;
for pair in [[R,P],[Q,R],[Qd,R]] do
 cov:=GroupHomomorphismByImages(pair[1].g,pair[2].g,pair[1].s,pair[2].s);
 check(cov<>fail and IsSurjective(cov),"marked cover");
 check(Size(Kernel(cov))=3,"degree three");
od;
p1:=GroupHomomorphismByImages(R.g,P.g,R.s,P.s);;
p2:=GroupHomomorphismByImages(R.g,P.g,R.s,Pm.s);;
check(p1<>fail and p2<>fail,"two mirror projections");
Xf:=Image(p1,Intersection(Group(R.s{[1,2]}),Kernel(p2)));;
Xv:=Image(p1,Intersection(Group(R.s{[2,3]}),Kernel(p2)));;
check(Xf=Group([P.s[2]^3]) and Xv=Xf,"local chirality obstruction b^3");
Print("CHIRALITY facet=vertex=<b^3> ORDER 3\n");
faciso:=GroupHomomorphismByImages(Group(T.s{[1,2]}),Group(R.s{[1,2]}),T.s{[1,2]},R.s{[1,2]});;
check(faciso<>fail and IsBijective(faciso),"T facet is R facet");
dualiso:=GroupHomomorphismByImages(T.g,Td.g,T.s,[Td.s[3]^-1,Td.s[2]^-1,Td.s[1]^-1]);;
check(dualiso<>fail and IsBijective(dualiso),"Td is literal dual of T");
w:=(b*c^-1)^2*a*c^2*a^-1;;
check(List([Q,Qd],A->Order(MappedWord(w,GeneratorsOfGroup(F),A.s)))=[1,3],"nonisomorphism witness");
Print("DISTINGUISH (b*c^-1)^2*a*c^2*a^-1 ORDERS [1,3]\n");
Print("PASS GAP ",GAPInfo.Version," six exact groups, all maps, IP, regularity, duality, witness\n");
QUIT_GAP(0);
```

## Appendix E. Complete Petrial operation and kernel controls

This standard-library program constructs the geometry and its actual set-valued Petrial from explicit permutations. It checks all finite incidence/residue conditions, both branches of the face-stabilizer split, the exact action kernel against the intersection of conjugates, the central-involution criterion and thin-case bidual shadows. The two source boundaries and every general theorem already have full proofs in §23. The program is a strengthened, fully charged version of the phase25 checker; its seven examples are not a census.

```python
#!/usr/bin/env python3
"""Finite controls for the source-defined Petrial and exact retained-object kernel.

Standard library only. The operation acts on chambers of incidence structures,
not on a presumed replacement generating set. Original examples use explicit
permutations, without a group catalogue or external presentation library.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def mul(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def inv(p):
    out = [0] * len(p)
    for i, v in enumerate(p):
        out[v] = i
    return tuple(out)


def cyc(n, *cycles):
    out = list(range(n))
    for cycle in cycles:
        for a, b in zip(cycle, cycle[1:] + cycle[:1]):
            out[a] = b
    return tuple(out)


def closure(gens):
    one = tuple(range(len(gens[0])))
    seen, queue = {one}, [one]
    for g in queue:
        for s in gens:
            h = mul(g, s)
            if h not in seen:
                seen.add(h)
                queue.append(h)
    return frozenset(seen)


def order(p):
    return len(closure([p]))


def connected(vertices, adjacent):
    if not vertices:
        return False
    seen, queue = {vertices[0]}, [vertices[0]]
    for v in queue:
        for w in vertices:
            if w not in seen and adjacent(v, w):
                seen.add(w)
                queue.append(w)
    return len(seen) == len(vertices)


class Geometry:
    def __init__(self, sizes, pairs):
        self.sizes = sizes
        self.pairs = {k: frozenset(v) for k, v in pairs.items()}
        self.vertices = [(i, j) for i, s in enumerate(sizes) for j in range(s)]
        self.chambers = tuple(c for c in itertools.product(*map(range, sizes))
                              if all((c[i], c[j]) in self.pairs[i, j]
                                     for i, j in ((0, 1), (0, 2), (1, 2))))
        self.panels = {}
        for c in self.chambers:
            for i in range(3):
                key = (i, tuple(c[j] for j in range(3) if j != i))
                self.panels.setdefault(key, []).append(c)

    def adjacent(self, x, y):
        i, a = x
        j, b = y
        if i == j:
            return a == b
        if i > j:
            i, j, a, b = j, i, b, a
        return (a, b) in self.pairs[i, j]

    def properties(self):
        geometry = bool(self.chambers)
        for i, s in enumerate(self.sizes):
            geometry &= all(any(c[i] == a for c in self.chambers) for a in range(s))
        for (i, j), edges in self.pairs.items():
            geometry &= all(any(c[i] == a and c[j] == b for c in self.chambers)
                            for a, b in edges)
        thin = geometry and all(len(v) == 2 for v in self.panels.values())
        rc = connected(self.vertices, self.adjacent)
        for v in self.vertices:
            residue = [w for w in self.vertices if w[0] != v[0] and self.adjacent(v, w)]
            rc &= connected(residue, self.adjacent)
        return {'geometry': bool(geometry), 'thin': bool(thin),
                'residually_connected': bool(rc), 'type_sizes': list(self.sizes),
                'chambers': len(self.chambers)}

    def flip(self, c, i):
        key = (i, tuple(c[j] for j in range(3) if j != i))
        choices = self.panels[key]
        assert len(choices) == 2 and c in choices
        return choices[choices[0] == c]

    def petrial(self):
        assert self.properties()['thin']
        successors = {}
        for c in self.chambers:
            d = c
            for i in (0, 2, 1):
                d = self.flip(d, i)
            successors[c] = d
        assert len(set(successors.values())) == len(successors)
        remaining = set(self.chambers)
        faces, by_chamber, cycles = set(), {}, []
        while remaining:
            start = min(remaining)
            walk, c = [], start
            while c not in walk:
                walk.append(c)
                c = successors[c]
            assert c == start
            remaining.difference_update(walk)
            face = (frozenset(c[0] for c in walk), frozenset(c[1] for c in walk))
            faces.add(face)
            for c in walk:
                by_chamber[c] = face
            cycles.append({'chambers': len(walk), 'vertices': len(face[0]),
                           'edges': len(face[1])})
        faces = tuple(sorted(faces, key=lambda f: (sorted(f[0]), sorted(f[1]))))
        pairs = {(0, 1): self.pairs[0, 1],
                 (0, 2): {(v, f) for f, face in enumerate(faces) for v in face[0]},
                 (1, 2): {(e, f) for f, face in enumerate(faces) for e in face[1]}}
        return Geometry((self.sizes[0], self.sizes[1], len(faces)), pairs), faces, by_chamber, cycles


def coset_geometry(gens):
    a, b, c = gens
    G = closure(gens)
    subgroups = [closure([a, b]), closure([a, c]), closure([b, c])]
    cosets = []
    for H in subgroups:
        cs = {frozenset(mul(g, h) for h in H) for g in G}
        cosets.append(tuple(sorted(cs, key=lambda x: sorted(x))))
    lookups = [{C: j for j, C in enumerate(cs)} for cs in cosets]
    actions = {g: tuple(tuple(lookups[i][frozenset(mul(g, h) for h in C)]
                             for C in cs) for i, cs in enumerate(cosets)) for g in G}
    pairs = {(i, j): {(x, y) for x, X in enumerate(cosets[i]) for y, Y in enumerate(cosets[j]) if X & Y}
             for i, j in ((0, 1), (0, 2), (1, 2))}
    geom = Geometry(tuple(map(len, cosets)), pairs)
    base = tuple(lookups[i][H] for i, H in enumerate(subgroups))
    return G, geom, base, actions


def run_case(name, generators, expected_thin):
    G, geom, base, actions = coset_geometry(generators)
    prop = geom.properties()
    assert prop['geometry'] and prop['thin'] and prop['residually_connected']
    assert len(geom.chambers) == len(G)
    assert {tuple(actions[g][i][base[i]] for i in range(3)) for g in G} == set(geom.chambers)
    new, faces, by_chamber, cycles = geom.petrial()
    new_prop = new.properties()
    assert new_prop['geometry'] and new_prop['residually_connected']
    assert new_prop['thin'] == expected_thin
    P = by_chamber[base]
    a, b, c = generators
    bP = (frozenset(actions[b][0][v] for v in P[0]), frozenset(actions[b][1][e] for e in P[1]))
    kernel = [g for g in G if all(actions[g][i] == tuple(range(geom.sizes[i])) for i in (0, 1))]
    # Compute the core independently from actual conjugates, then compare the
    # literal retained-object kernel with both forms of the uniform theorem.
    A = closure([a])
    core = set(A)
    for g in G:
        core.intersection_update(mul(mul(g, h), inv(g)) for h in A)
    assert set(kernel) == core
    central = all(mul(a, g) == mul(g, a) for g in G)
    one = tuple(range(len(a)))
    assert core == ({one, a} if central else {one})
    induced = set()
    face_lookup = {P: i for i, P in enumerate(faces)}
    for g in G:
        face_action = tuple(face_lookup[(frozenset(actions[g][0][v] for v in P[0]),
                                        frozenset(actions[g][1][e] for e in P[1]))] for P in faces)
        act = actions[g][:2] + (face_action,)
        induced.add(act)
        assert all(tuple(act[i][C[i]] for i in range(3)) in new.chambers for C in new.chambers)
    out = {'name': name, 'generators_zero_based': list(map(list, generators)),
           'group_order': len(G), 'pair_orders_ab_ac_bc': [order(mul(a, b)), order(mul(a, c)), order(mul(b, c))],
           'original': prop, 'petrial': new_prop, 'action_kernel_order': len(kernel),
           'induced_action_order': len(induced), 'base_face_fixed_by_b': bP == P,
           'computed_core_order': len(core), 'face_marker_central': central,
           'petrie_cycles': sorted(cycles, key=lambda x: (x['chambers'], x['vertices'], x['edges']))}
    if new_prop['thin']:
        assert len(kernel) == 1
        base_new = base[:2] + (face_lookup[P],)
        orbit = {tuple(act[i][base_new[i]] for i in range(3)) for act in induced}
        assert orbit == set(new.chambers)
        second, second_faces, _, _ = new.petrial()
        old_shadows = tuple((frozenset(v for v, f0 in geom.pairs[0, 2] if f0 == f),
                             frozenset(e for e, f0 in geom.pairs[1, 2] if f0 == f))
                            for f in range(geom.sizes[2]))
        assert len(set(old_shadows)) == len(old_shadows)
        assert set(second_faces) == set(old_shadows)
        assert second.properties()['thin'] and second.properties()['residually_connected']
        out['bidual_face_shadows_exact'] = True
        out['induced_action_chamber_regular'] = True
        assert 2 in out['pair_orders_ab_ac_bc'][:2]
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path(__file__).with_suffix('.json'))
    args = parser.parse_args()
    cases = [
        ('C2_cubed', [cyc(6, (0, 1)), cyc(6, (2, 3)), cyc(6, (4, 5))], False),
        ('C2_times_S3', [cyc(5, (0, 1)), cyc(5, (2, 3)), cyc(5, (3, 4))], False),
        ('S4_tetrahedron', [cyc(4, (2, 3)), cyc(4, (1, 2)), cyc(4, (0, 1))], True),
        ('S4_tetrahedron_vertex_edge_swap', [cyc(4, (2, 3)), cyc(4, (0, 1)), cyc(4, (1, 2))], True),
        ('S4_star', [cyc(4, (0, 1)), cyc(4, (0, 2)), cyc(4, (0, 3))], False),
        ('B3_cube', [cyc(6, (2, 4), (3, 5)), cyc(6, (0, 2), (1, 3)), cyc(6, (0, 1))], True),
        ('B3_cube_vertex_edge_swap', [cyc(6, (2, 4), (3, 5)), cyc(6, (0, 1)), cyc(6, (0, 2), (1, 3))], True),
    ]
    results = [run_case(*case) for case in cases]
    assert results[0]['action_kernel_order'] == results[1]['action_kernel_order'] == 2
    assert results[0]['petrial']['type_sizes'] == [2, 2, 1]
    assert results[2]['base_face_fixed_by_b'] and not results[3]['base_face_fixed_by_b']
    report = {'status': 'PASS', 'scope': 'Seven explicit finite examples; no exhaustion or uniform proof claim.',
              'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'cases': results, 'summary': {'examples': len(results),
                 'original_chambers': sum(x['original']['chambers'] for x in results),
                 'thin_petrials': sum(x['petrial']['thin'] for x in results),
                 'nonfaithful_petrial_actions': sum(x['action_kernel_order'] > 1 for x in results)}}
    with args.output.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report['summary'], sort_keys=True))
    print('PASS')


if __name__ == '__main__':
    main()
```

## References and exact source versions


[BC98] F. Buekenhout and P. Cara, *Some properties of inductively minimal geometries*, Bulletin of the Belgian Mathematical Society–Simon Stevin **5** (1998), 213–219, DOI [10.36045/bbms/1103409005](https://doi.org/10.36045/bbms/1103409005). Target version: complete authored text rendered at the [author-uploaded Academia entry](https://www.academia.edu/54639280/Some\_properties\_of\_inductively\_minimal\_geometries), locally recorded with displayed lines 181–220. No PDF-version identity is inferred.

[CC02] P. J. Cameron and P. Cara, *Independent generating sets and geometries for symmetric groups*, Journal of Algebra **258** (2002), 641–650, DOI [10.1016/S0021-8693(02)00550-1](https://doi.org/10.1016/S0021-8693(02)00550-1). Target version: the twelve-page [author manuscript](https://maths.qmul.ac.uk/~pjc/preprints/igsgsn.pdf); result page references in the ledger refer to that manuscript rather than the journal pagination.

[BCD97] F. Buekenhout, P. Cara and M. Dehon, *Inductively minimal flag-transitive geometries*, in N. L. Johnson (ed.), *Mostly Finite Geometries*, Marcel Dekker, 1997, 185–190. Retained in the precise form restated in [BC98], Lemma 1 and its following paragraph; the original 1997 chapter was not independently acquired in this assembly.

[W00] J. Whiston, *Maximal independent generating sets of the symmetric group*, Journal of Algebra **232** (2000), 255–268. W1 and W2 are retained in the forms recited in [CC02], pages 3–4; the original proof and its classification inputs are not reproved or newly source-audited here.

[Coset] The (G1)–(G4) conventions and general coset correspondence are those stated in [CC02], pages 7–8, with its references to F. Buekenhout, *Foundations of incidence geometry*, in *Handbook of Incidence Geometry* (1995), 63–105; F. Buekenhout and M. Hermand, *On flag-transitive geometries and groups* (1991), 45–78; and J. Tits, *Buildings of Spherical Type and Finite BN-Pairs* (1974).


[ACK05] C. Archer, P. Cara and J. Krempa, *Using the Frattini Subgroup and Independent Generating Sets to Study RWPRI Geometries*, Beiträge zur Algebra und Geometrie **46**(1) (2005), 169–177. Target version: complete published nine-page PDF, identically retrieved from the [GWDG EMIS mirror](https://ftp.gwdg.de/pub/EMIS/journals/BAG/vol.46/no.1/b46h1car.pdf) and the [Masaryk EMIS mirror](https://emis.muni.cz/journals/BAG/vol.46/no.1/b46h1car.pdf). The finite-p-group background is recalled on page 174; all target statements, scope corrections and the imported theorem inventory are version-bound in the companion contract.

[Gas53] W. Gaschütz, *Über die Φ-Untergruppe endlicher Gruppen*, Math. Z. **58** (1953), 160–170. Retained only in the structural form quoted as [ACK05] Theorem 4.1; the original proof was not independently acquired for this assembly.

[Arc04] C. Archer, *Direct sum decomposition of geometries based on maximal subgroups*, J. Geometry **79** (2004), 12–18. The primitive-group reduction quoted in [ACK05] §4.3 is retained as earlier work, not proved or used to establish the new Frattini/coordinate core.

[HFLa] D.-D. Hou, Y.-Q. Feng and D. Leemans, *On regular polytopes of 2-power order*, revised author PDF dated 8 November 2019, journal 2020, DOI 10.1007/s00454-019-00119-5. Exact retained primary file: `sources/catalogue_L032.pdf`.

[HFLb] D.-D. Hou, Y.-Q. Feng and D. Leemans, *Existence of regular 3-polytopes of order 2^n*, arXiv:1802.08947v2, 22 January 2019; journal catalogue title *2-groups behaving as automorphism groups of regular 3-polytopes*. Exact retained primary file: `sources/catalogue_L035.pdf`.

[HS26] D.-D. Hou and E. Schulte, *String C-groups of 2-power order project onto a common string C-group*, arXiv:2605.20691v1, submitted 20 May 2026, PDF dated 21 May. Exact retained primary file: `sources/catalogue_F013.pdf`.

[CFHS25] G. Cunningham, Y.-Q. Feng, D.-D. Hou and E. Schulte, *Symmetric polytopes whose automorphism groups are 2-groups*, arXiv:2512.15511v1, submitted 17 December 2025, PDF dated 18 December. Exact retained primary file: `sources/symmetric_2groups2025.pdf`.

### Operations and covers


1. M. I. Hartley and D. Leemans, *On the thin regular geometries of rank four for the Janko group J1*, Innovations in Incidence Geometry **1** (2005), 181–190. [Journal primary PDF](https://msp.org/iig/2005/1-1/iig-v1-n1-p08-s.pdf). Main construction targets: Theorems 3.2, 4.2, 5.2, 5.4, 6.2, 7.2. Its introductory exhaustive classification is recovered in Corollary O6.3.
2. A. Montero and A. Ivić Weiss, *Locally Spherical Hypertopes from Generalised Cubes*, [arXiv:2001.11082v1](https://arxiv.org/abs/2001.11082v1), 29 January 2020. Targets: Theorem 3.1, Proposition 3.2, Corollary 3.3, and the principal applications in §4. Later journal numbering is not substituted.
3. C. A. Piedade and P. Tranchida, *Constructing new geometries: a generalized approach to halving for hypertopes*, [arXiv:2405.19050v1](https://arxiv.org/abs/2405.19050v1), especially its introduction and §2.3 on lattice nondegeneracy, its graph constructions, and the established bipartiteness/index-two interpretation. This is attribution and terminology support, not an additional compressed manuscript or an import of its broader geometric conclusion without (PC).
4. L. Danzer, *Regular incidence-complexes and dimensionally unbounded sequences of such. I\*, North-Holland Mathematics Studies **87** (1984), 115–127; P. McMullen and E. Schulte, *Abstract Regular Polytopes* (2002), especially the generalized-cube construction and standard coordinate models. The construction theorem in (O9) and standard convex-polytope orders remain retained; the particular toroidal lattice identifications are proved in §9.
5. The classical finite/affine/compact-hyperbolic Coxeter classifications, and the GAP 4.15.1 exact permutation-group/coset algorithms with TomLib 1.2.11's complete J1 subgroup catalogue and permutation model, are the other substantial inputs. The execution manifest binds the actual installed versions and data.


[Cun24] G. Cunningham, *Chiral polytopes whose smallest regular cover is a
polytope*, Journal of Combinatorial Theory, Series A 204 (2024), 105839,
DOI [10.1016/j.jcta.2023.105839](https://doi.org/10.1016/j.jcta.2023.105839).
Target: [author manuscript headed 25 July 2023](https://gabrielcunningham.com/WhichChiralPolytopes.pdf),
eight pages; publisher full text unacquired.

[CP21] G. Cunningham and D. Pellicer, *Tight chiral polytopes*, Journal of
Algebraic Combinatorics 54 (2021), 837–878. The five rows and embedded
chirality input retained in §22.3 were checked in arXiv:2009.04566,
Proposition 4.2 and Table 4; this older classification is not replaced.

[Ens18] E. Ens, *Rank 4 toroidal hypertopes*, Ars Mathematica Contemporanea
15 (2018), 67–79. The selected definitions, equations (3.1), (4.1) and
Theorem 4.3 were read to match the lattice convention in §9; the full
classification is neither assumed to prove that quotient nor counted.



[BBL01] D. Bonheure, F. Buekenhout and D. Leemans, *On the Petrials of thin rank 3 geometries*, Journal of Geometry **71** (2001), 19–25, DOI 10.1007/s00022-001-8548-2. Target version: complete seven-page authored rendering hosted at the coauthor-linked Academia article; primary PDF unavailable. The source operation and targets are attributed to this work. Its unconditional embedding and length/order assertions are corrected in §23, without a historical-priority claim.

The new retained-object interface K(c) and its coset/endpoint/Petrial applications are explicit integration arguments; no claim of historical originality is made for the elementary ingredients. The two-branch corrected Petrial proof was developed and independently reviewed in the earlier phase25 component and is reproved here using the common interface. The phase45 reference erratum is incorporated in this new manuscript: the citation after O4.1 is to N013's quoted Theorem 2.2. No frozen predecessor is altered.
