# Module A: Construction and classification of two-group polytopes and hypertopes

## Abstract

We develop construction and classification methods for regular polytopes and hypertopes whose automorphism groups have two-power order. A forest of noncommuting generators determines a canonical class-two quotient. Its square-lattice sections provide local kernels that can be attached independently by the supported-kernel theorem of *Marked groups, kernels and intersections*. This yields prescribed edge orders, square sections and three-generator hypertope types, with exact orders and complete presentations. Conversely, a fixed class-two quotient reduces bounded-order classification to an exhaustive invariant-kernel problem. We combine this reduction with cyclic-core and central-descent arguments to recover the high-type rank-three families and the full order-1024 classification, including named facets and corrected presentations. The same local models also support regular, chiral and alternating extensions. Source conclusions, retained geometric inputs and corrections are stated explicitly.

## Introduction

Local sections serve two complementary purposes in finite incidence geometry. One may prescribe them and construct a marked group realizing those prescriptions, or constrain their orders and classify every group that can occur. The same kernel coordinates can organize both tasks. In the construction direction, a local quotient is attached to a subset of the marker labels. In the classification direction, a canonical nilpotent quotient confines the search to normal subgroups of one finite group.

The starting point is a vertex-and-edge model for a forest diagram. The intersection property forces independent edge commutators in degree two, so every finite marked two-group with that diagram has the same class-two quotient (§2). The affine square group supplies exact local kernels and two useful quotient decompositions (§3). The supported-kernel theorem of the companion paper [U] then assembles prescribed edge orders and consecutive square sections. Its coordinate-kernel Helly theorem upgrades three dihedral attachments to an actual regular hypertope. A separate sharp order bound identifies the source's complete presentation (§4).

The reverse direction begins with a bounded cyclic core, reducing the high-type rank-three problem to eight explicit models (§5). Central descent and complete binary lifting link the bounded quotients (§6). One invariant-kernel census, followed by complete presentation and marked-isomorphism checks, yields the order-1024 classification (§7). Finally, free geometric extensions use the amalgam theorem of [U] and precisely stated earlier constructions (§8).

The six applications are the prescribed-order theorem of Hou, Feng and Leemans [HFLa], their high-type rank-three classification [HFLb], their three-generator hypertope construction [HFLh], the common-quotient theorem of Hou and Schulte [HS26], the square-section and extension theorems of Cunningham, Feng, Hou and Schulte [CFHS25], and the order-1024 classification of Gomi, Loyola and De Las Peñas [GLP18]. Their original results retain that attribution. The general algebraic proofs occur once in [U]; this paper supplies the actual marked maps, local injectivity, geometric hypotheses and source-presentation identifications needed to use them. Earlier cyclic-core, geometric-assembly and infinite-decomposition theorems remain explicit retained inputs. All finite classification data and the complete certificate interface are specified in Appendix C.

## 1. Markings, geometric inputs and the interface to U

A marking is an ordered generating family of nonidentity involutions
\(r_i\), indexed by a finite set \(I\). Write
\(G_J=\langle r_j:j\in J\rangle\). The intersection property is
\(G_J\cap G_K=G_{J\cap K}\) for every pair of subsets. A string
C-group also has \([r_i,r_j]=1\) for \(|i-j|>1\); nondegeneracy
means that consecutive generators do not commute. The type is their consecutive
product orders. A regular hypertope is a thin, residually connected incidence geometry with a chamber-transitive type-preserving automorphism group. It need not have a string diagram; its rank-three type here records all three pair-product orders. Use \([x,y]=x^{-1}y^{-1}xy\), \(x^y=y^{-1}xy\),
and \(D_8\) for the dihedral group of order eight. Ordered marked
isomorphisms preserve every generator. The [GLP18] census instead identifies
generator sets; for a nondegenerate string this adds precisely reversal.

We retain the regular-polytope/string-C-group correspondence, the marked
epimorphism/cover correspondence and the coset description of faces and
stabilizers. A deletion sends selected markers to themselves and all others
to one. Its geometric interpretation gives the flat amalgamation property
(FAP) at the corresponding initial or final cut. Flatness itself is a separate
incidence conclusion: a factorization of the group by two relevant face
stabilizers makes every face of the first kind incident with every face of the
second kind. It is never inferred merely from IP.

The general facts used from U are listed with their exact interfaces.
Their complete proofs occur once in U; each application below verifies the stated hypotheses.

* **U.K**: if a marked epimorphism \(G\to B\) has kernel \(N\)
  and the base has IP, then G has IP exactly when the profiles
  \(N\cap G_J\) have the same subset-intersection property.
* **U.Q**: for a quotient \(q:G\to G/N\),
  \(q(A)\cap q(B)=q(A\cap B)\) holds exactly when
  \(N\cap BA=(N\cap B)(N\cap A)\). In particular
  \(N\cap BA=1\) preserves the
  intersection and embeds both ends; if \(N\le A\), then
  \(q(A)\cap q(B)=q(A\cap B)\). The latter still requires checking
  that the displayed quotient marking on A is valid.
* **U.D**: a full Boolean family of genuine deletions implies IP and
  split parabolic retractions, including infinite groups.
* **U.SK**: exact base deletions and epimorphisms \(E_S\to B_S\)
  injective on every proper-support parabolic give the full supported fiber
  group, with kernel profile
  \(\ker\pi\cap H_J=\prod_{S\subseteq J}\ker(E_S\to B_S)\).
  It has IP, inherits Boolean deletions, and has the resulting parabolic
  order formula. Antichain supports embed their full local groups. If every
  local kernel is \(\gamma_c(E_S)\) and B has class below c, the
  global kernel is \(\gamma_c(H)\). A supported separator gives
  \(H=H_JH_K\) when \(B=B_JB_K\).
* **U.SK.Helly/U.SK.Geometry**: a marked quotient with base IP and an exact direct-product coordinate profile transfers typed coset Helly from the base. If the base is a regular hypertope and every local marker is an involution, U.SK therefore gives a regular hypertope with the constructed full type-preserving group. In the pair-support case local involutivity also follows from proper-singleton injectivity.

* **U.Nilpotent/U.Ladder**: for an involutory finitely generated presentation F with
  deletions, its class-two quotient Q inherits deletions and IP. Finite marked quotients with
  that same Q and order \(|Q|2^k\) are classified by suitable kernels
  inside \(\gamma_3(F/\gamma_{k+3}(F))\). Their IP is the exact
  all-parabolic kernel-profile condition. Every invariant index-two step is
  a hyperplane preimage in \(M/(\Phi(M)[M,U])\), and iterating k
  steps exhausts every index-\(2^k\) invariant kernel.
* **U.Phi**: an irredundant generating marking of a finite two-group maps to
  a basis of its Frattini quotient; every binary coordinate assignment gives
  a character. All marked parabolics have the corresponding coordinate images.
* **U.Amalgam**: p-primary finite torsion is preserved by subgroups, finite
  p-group extensions and amalgamated free products. Proper embeddings in both
  factors make an amalgam infinite; finitely generated factors generate it.
* **U.Order**: finite normal factors and a finite quotient-index bound give
  the product upper bound; a marked finite quotient attaining that bound
  identifies the complete presentation.

U retains Burnside's basis theorem, lower-central graded Lie theory, finite
nilpotency of finite two-groups and amalgam normal forms. Here we additionally
retain the Gaussian-integer Euclidean algorithm, the precise cyclic-core theorem
in §5 and the geometric assembly/extension theorems in §§4 and 8. The standard
low-rank string-IP criteria, smooth square-quotient classification, universal
geometric interpretation and exceptional infinite decomposition quoted by
[GLP18] are stated where used. Exact GAP group and coset algorithms and NQ's
universal nilpotent quotient algorithm are computational inputs. No finite
classification catalogue supplies search completeness.

## 2. A canonical quotient and one finite classification problem

The application-specific bridge to U is a rigidity statement: a forest diagram
forces independent edge commutators in degree two. Its proof uses actual IP in
G; no intermediate quotient is presumed to retain IP.

**Lemma A2.1 (descending lift).** Let \(G\) be finite nilpotent and let
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

**Lemma A2.2 (graded support).** Let a positively graded Lie algebra be
generated in degree one by disjoint sets \(X,Y\), with subalgebras
\(L_X,L_Y\). If \([x,y]\in L_Y\) for \(x\in X,y\in Y\), then
\(L=L_X+L_Y\), degree by degree.

**Proof.** The derivation \(\operatorname{ad}x\) preserves \(L_Y\)
because it does so on its generators. Iterated brackets of those
derivations also preserve \(L_Y\), by Jacobi. Hence
\([L_X,L_Y]\subseteq L_Y\), and \(L_X+L_Y\) is a Lie subalgebra
containing all generators. The argument holds in characteristic two. ∎

**Theorem A2.3 (forest quotient).** Suppose \(G\) is a finite two-group generated by involutions \(r_i\), with marked IP, and its noncommuting pairs form a forest \(T\) on
\(d\) vertices and \(m\) edges. Then edge commutators are independent
in \(G'/\gamma_3(G)\), and \(G/\gamma_3(G)\) is the marked group
\[
 (v,z)(w,t)=(v+w,z+t+\beta(v,w)),\quad
 v,w\in\mathbb F_2^d,\ z,t\in\mathbb F_2^m,               \tag{A-F}
\]
where, after orienting each edge, its component of \(\beta\) is
\(v_{\rm head}w_{\rm tail}\). Its order is \(2^{d+m}\).

**Proof.** IP gives irredundancy. U.Phi gives \(G/G'=C_2^d\) and \(G'\cap\langle r_i\rangle=1\).
The lower-central graded Lie ring is generated by these degree-one
elements; all its graded components are \(\mathbb F_2\)-spaces by
bilinearity. Edge commutators span degree two. If they satisfy a nonzero
linear relation, root each forest component and choose a participating
edge whose child endpoint has maximal depth in its component. Removing
it separates the descendant set \(X\) from all other vertices \(Y\),
and no other participating edge is internal to \(X\). The relation
therefore writes the only nonzero cross bracket as a sum of brackets
internal to \(Y\). Lemma A2.2 shows every graded component is generated
by pure \(X\)- and pure \(Y\)-brackets. Their representatives lie in
\(G_X\cap\gamma_j(G)\) and \(G_Y\cap\gamma_j(G)\).

Actual IP gives \(G_X\cap G_Y=1\), so Lemma A2.1 gives
\(G'=(G'\cap G_X)(G'\cap G_Y)\). For the crossing endpoints
\(x\in X,y\in Y\), write \([r_x,r_y]=uv\) accordingly. Then
\(u\in G_X\cap G_{\{x\}\cup Y}=\langle r_x\rangle\), whence
\(u=1\); next \([r_x,r_y]\in G_Y\cap G_{\{x,y\}}=\langle r_y\rangle\),
so it too is one. This contradicts that the edge is noncommuting.
Independence follows.

Bilinearity makes (A-F) associative; its coordinate markers are
involutions with independent central edge commutators. It is generated
by those markers, and its parabolic on \(I\) consists exactly of vertex
coordinates supported on \(I\) and edge coordinates supported on edges
internal to \(I\). Thus it has IP. Collection in the corresponding
class-two presentation gives at most \(2^{d+m}\) elements, and this
coordinate model attains the bound. Independence in \(G'/\gamma_3(G)\)
gives the same order for \(G/\gamma_3(G)\); hence the marked map is an
isomorphism. ∎

**Corollary A2.4 (F013 1.1–1.2).** For every finite nondegenerate two-group
string C-group of rank \(d\ge2\),
\(G/\gamma_3(G)\cong G(C_d)\), of order \(2^{2d-1}\); the associated
polytope covers \(C_d\).

**Proof.** Its diagram is a path, so \(m=d-1\). Conder's marked
presentation has involutions, distant commutation, adjacent order four,
and adjacent squares central. The model (A-F) realizes that presentation
with the maximal collected order, identifying it with \(G(C_d)\).
The retained marked covering correspondence gives the geometric assertion.
This also proves uniqueness of the minimal object in the declared finite
nondegenerate class. ∎

Notice that no intermediate quotient was assumed to retain IP. Lemma A2.1
is the step that prevents that circular assumption.


**Corollary A2.5 (rank and excess classify the finite search).** Let T be a
specified forest on d vertices and m edges, and let k≥0. Set

\[
 F_T=\langle x_i\mid x_i^2=1,\ [x_i,x_j]=1\text{ for nonedges}\rangle,
 \quad U_{T,k}=F_T/\gamma_{k+3}(F_T),\quad K=\gamma_3(U_{T,k}).
\]

The ordered IP markings with graph T and order \(2^{d+m+k}\) are exactly
the quotients \(U_{T,k}/N\), where N is normal, contained in K,
\([K:N]=2^k\), and the images
\((N(K\cap(U_{T,k})_J))/N\) have IP for every pair J,L.
Generator-set equivalence is exactly the action of Aut(T) on these kernels.

*Proof.* Killing any set of generators preserves every defining relator of
\(F_T\). Collection in its class-two quotient gives at most d+m binary
coordinates, and (A-F) realizes all of them, so this quotient is precisely
the marked model \(Q_T\). Every target has that same quotient by A2.3.
These are exactly U.Nilpotent's hypotheses. Its all-parabolic condition and U.Ladder
give the stated bijection and exhaustive search. An ordered isomorphism must
commute with the generating map, hence has the same kernel. A permutation
of the generator set preserves the noncommutation graph and extends to an
automorphism of \(F_T\) and \(U_{T,k}\); this proves the last claim. ∎

This is used twice below: the order-256 seed has (d,k)=(3,3), while all
nondegenerate order-1024 markings have (d,k)=(3,5),(4,3),(5,1). Their actual
terminal counts require the complete computation in Appendix C. The parameter
theorem proves exhaustion and termination, not those output values.

## 3. The affine square seed

Let
\[
 a(x,y)=(-x,y),\quad b(x,y)=(y,x),\quad c(x,y)=(x,1-y).
\]
These generate \(W=\mathbb Z^2\rtimes D_8\), of type \(\{4,4\}\), with
\(ac=ca\). Its presentation is
\[
 W=\langle a,b,c\mid a^2=b^2=c^2=(ab)^4=(bc)^4=(ac)^2=1\rangle. \tag{A-S1}
\]
Here is an algebraic normal-form proof. Put \(d=bab\), \(y_0=cd\), and
\(x_0=by_0b\). The relations give \([a,d]=1\), \([a,y_0]=1\),
\(dy_0d=y_0^{-1}\), \(ax_0a=x_0^{-1}\), and conjugation by \(b\) swaps
\(x_0,y_0\). Substitution of \(bc=x_0ab\) makes \((bc)^4=1\) equivalent
to \([x_0,y_0]=1\). Thus every word collects to \(x_0^u y_0^v M\),
\(M\in\langle a,b\rangle=D_8\). In the affine model \(x_0,y_0\) are the
unit translations, so these forms are distinct. This proves (A-S1).

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
also survive. Thus \(H_n\) has Boolean deletions and IP by U.D.

Moreover,
\[
 \gamma_3(W)=2\mathbb Z^2,
 \qquad \gamma_3(H_n)=2\mathbb Z^2/\Lambda_n,
 \qquad |\gamma_3(H_n)|=2^{n-5}.                         \tag{A-S2}
\]
Indeed reduction modulo \(2\mathbb Z^2\) makes the adjacent squares
central; conversely \([[a,b],c]\) and \([[b,c],a]\) give the two doubled
unit translations, up to signs. Thus \(H_5\) is class two of order 32.
The squared translations are not always independent cyclic subgroups:
in \(H_6\) they coincide and have order two. Formula (A-S2) uses a lattice
index and does not make the false independence assertion.

**Lemma A3.1 (square-map recognition).** Every finite two-group string
C-group of type \(\{4,4\}\) and order \(2^n\) is marked-isomorphic to
\(H_n\); necessarily \(n\ge5\).

**Proof.** The two dihedral parabolics have orders eight and intersect in
order two, so their product already has 32 elements. The universal group
(A-S1) maps onto the given group. IP gives irredundancy, so U.Phi gives elementary abelianization of rank three. Hence word parity is a
homomorphism onto \(C_2\), and the kernel of (A-S1) lies in the subgroup
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



The quotient \(q_n:H_n\to H_5\) fixes the three named generators.
Its kernel is \(\gamma_3(H_n)\). Every proper marked parabolic has
at most two generators, and its type is respectively 4,4 or2 both upstairs
and downstairs. Each is the identical dihedral or order-four group; singleton
and empty parabolics likewise embed. This verifies U.SK's full proper-support
condition, rather than merely checking three involutions.

### 3.1. Complete square quotients and their decompositions

For \(\delta\ge0\), set
\[
 Q_\delta=
 \begin{cases}
 W/q\mathbb Z^2,&\delta\text{ even},\quad q=2^{(\delta+2)/2},\\
 W/q\langle(1,1),(1,-1)\rangle,&\delta\text{ odd},\quad q=2^{(\delta+1)/2}.
 \end{cases}
 \tag{A-S3}
\]
Thus \(Q_\delta=H_{\delta+5}\), and its order is \(2^{\delta+5}\). It is a string C-group of type \(\{4,4\}\), has all Boolean deletions, and its maximal-parabolic cosets have typed Helly by the retained regular-polytope correspondence.

The two words needed in the source are, in these affine coordinates,
\[
 [(ab)^2,c]=(0,-2;1),\qquad
 [(ab)^2,(bc)^2]=(-2,-2;1),
 \tag{A-S4}
\]
where \((v;1)\) denotes translation by v. Indeed \((ab)^2\) is the half-turn \(x\mapsto-x\), while \((bc)^2\) is the half-turn \(x\mapsto(1,1)-x\); composing these with c gives the first formula, and composing the two half-turns twice gives the second. The normal closure in W of a translation consists of the lattice generated by its signed-permutation orbit. Therefore adjoining respectively
\[
 [(ab)^2,c]^{2^{\delta/2}}=1
 \quad\text{or}\quad
 [(ab)^2,(bc)^2]^{2^{(\delta-1)/2}}=1
 \tag{A-S5}
\]
to (A-S1) gives exactly (A-S3), not just a quotient of the stated order.

**Proposition A3.2 (the two square decompositions).** The source presentations \(M_2\) and \(M_1\) have the decompositions displayed below. They hold in the same affine model for every integer \(q\ge1\), not only the powers of two in (A-S3). We use \(D_{2q}\) for the dihedral group of order \(2q\), including \(D_2=C_2\) and \(D_4=C_2^2\). The source's presentations \(M_2\) and \(M_1\) adjoin respectively \((bcba)^q=1\) and \((cba)^{2q}=1\) to (A-S1). 

*Proof.* Here bcba is translation by \((1,0)\), and \((cba)^2\) is translation by \((1,1)\). Their signed-permutation orbits therefore generate exactly the square and diagonal lattices in (A-S6)–(A-S7). This identifies those complete presentations with the indicated lattice quotients.

In the square case, \(\langle a,c^b\rangle\) acts on the first coordinate and \(\langle a^b,c\rangle\) on the second. Their translations have order q; each is \(D_{2q}\), since its reflection has nonidentity linear part, also when q=1. They commute and intersect trivially. The reflection b interchanges the two factors and lies outside their product. They and b generate all three original generators. Hence
\[
 W/q\mathbb Z^2\cong(D_{2q}\times D_{2q})\rtimes C_2.
 \tag{A-S6}
\]

In the diagonal case, put \(A_0=\langle b^a,b^c\rangle\) and \(B_0=\langle b,b^{ac}\rangle\). Their reflecting axes are respectively \(x+y=0,1\) and \(x-y=0,-1\). The first factor has translations along \((1,1)\), the second along \((1,-1)\), of order q in each case. Each reflection retains its nonidentity linear part, so the two factors have order 2q also at q=1. All cross-generators commute. Their linear parts show that an element of their intersection must be a translation; the independence of the two diagonal translations modulo the defining lattice then makes that intersection trivial. Thus \(A_0B_0\cong D_{2q}\times D_{2q}\).

Both a and c exchange the two factors by conjugation, so normalize their product. The two individual reflections a,c do not belong to the product by their linear parts. The only remaining possible nontrivial intersection with \(\langle a,c\rangle\) is ac. Every translation part of an element of \(A_0B_0\) with linear part \(-1\) has coordinates of the same parity, whereas ac has translation part \((0,1)\). The diagonal lattice preserves this parity condition, so ac is also outside the product. Finally b already lies in \(B_0\), so the two factors and \(\langle a,c\rangle\) generate the full group. Consequently
\[
 W/q\langle(1,1),(1,-1)\rangle
 \cong(D_{2q}\times D_{2q})\rtimes(C_2\times C_2).
 \tag{A-S7}
\]
These arguments specify the actions by the original affine generators and prove the decompositions, rather than only equality of orders. \(\square\)

## 4. Prescribed local sections from supported kernels

**Theorem A4.1 (edge inflation and exact orders).** Let B have Boolean
deletions and select pairs S={i,j} whose product orders \(q_S\) are even. For
\(m_S\) divisible by \(q_S\), attach the marked dihedral map
\(D_{2m_S}\to B_S=D_{2q_S}\). The resulting supported fiber group
has IP, all deletions and

\[
 |H_J|=|B_J|\prod_{S\subseteq J}(m_S/q_S).
\]

Every selected pair has product order \(m_S\) and every unselected pair retains
its old order. If the base marking gives a regular hypertope, so does the constructed marking, with full type-preserving group H.

*Proof.* The dihedral quotient is injective on its proper parabolics, which
are trivial or a single reflection. U.SK applies and its antichain clause
identifies each selected local group. On an unselected pair every extra
coordinate is a reflection or one; a base pair of odd order cannot have a
single-reflection deletion. Thus the extra coordinates do not increase its
base product order. For the geometric assertion the local dihedral markers are involutions, and the supports are pairs. Thus the corrected U.SK.Geometry applies to the regular base and proves the required flag property as well as IP. ∎

For d≥3, n≥5, k_i≥2 and \(\sum k_i\le n-1\), set
\(\delta=n-1-\sum k_i\) and
\(B=C_2^{d-3}\times H_{\delta+5}\), with the elementary factors first.
Its initial d−3 consecutive pair orders are 2 and its final two are 4.
Attach \(m_i=2^{k_i}\). The seed supplies all deletions, so A4.1 gives

\[
 |H|=2^{d-3+\delta+5}
       \prod_{i\le d-3}2^{k_i-1}
       \prod_{i>d-3}2^{k_i-2}=2^n.
\]

Distant markers commute in every coordinate, so the marking is string.
The geometric correspondence proves **[HFLa] Theorem 1.2**. Taking d=3
proves **[HFLb] Theorem 1.2**, including its stated n≥10 range, without
another construction. These existence results do not imply the classification
of §5.

### Three-generator hypertopes

Fix integers \(n\ge10\), \(s,t\ge2\), \(\ell\ge1\), with \(\delta=n-s-t-\ell\ge0\). Let \(P=P(n,s,t,\ell)\) have generators a,b,c and relations
\[
 a^2=b^2=c^2=(ab)^{2^s}=(bc)^{2^t}=(ac)^{2^\ell}=1,
\]
\[
 [(ab)^4,c]=[a,(bc)^4]=[(ac)^2,b]=1,
 \tag{A-H1}
\]
together with the appropriate parity relation (A-S5). This is the exact defining presentation in [HFLh, Theorem 3.2], with the source markers renamed a,b,c.

**Theorem A.H (three-generator hypertope presentation).** P has order \(2^n\), its three pair-product orders are exactly \(2^s,2^t,2^\ell\), and its maximal-parabolic coset system is a regular rank-three hypertope with full type-preserving automorphism group P. Moreover the three normal subgroups
\[
 K_{01}=\langle(ab)^4\rangle,\quad
 K_{12}=\langle(bc)^4\rangle,\quad
 K_{02}=\langle(ac)^2\rangle
\]
form an internal direct product
\[
 K\cong C_{2^{s-2}}\times C_{2^{t-2}}\times C_{2^{\ell-1}},
 \qquad P/K\cong Q_\delta.
 \tag{A-H2}
\]
The factors of order one are permitted. With the extension dot making no splitting assertion, the corrected structural conclusion is
\[
 P\cong K\mathbin{.}
 \begin{cases}
 (D_{2^{(\delta+4)/2}}\times D_{2^{(\delta+4)/2}})\rtimes C_2,
     &\delta\text{ even},\\
 (D_{2^{(\delta+3)/2}}\times D_{2^{(\delta+3)/2}})\rtimes(C_2\times C_2),
     &\delta\text{ odd}.
 \end{cases}
 \tag{A-H3}
\]

*Proof.* Apply A4.1 to \(Q_\delta=H_{\delta+5}\), with all three pair supports and target orders \(2^s,2^t,2^\ell\). The base pair orders are \(4,4,2\); the attached maps are therefore \(D_{2^{s+1}}\to D_8\), \(D_{2^{t+1}}\to D_8\) and \(D_{2^{\ell+1}}\to D_4\). Section 3 supplies the base deletions and its regular string-polytope geometry. Each local marking consists of dihedral reflections, so A4.1's geometric clause applies. It constructs a regular hypertope with group H and the exact three pair orders, with
\[
 |H|=2^{\delta+5}\,2^{s-2}\,2^{t-2}\,2^{\ell-1}=2^n.
\]
The local orders and proper-parabolic injections used here are precisely those checked in A4.1; no independent second assembly proof is needed.

The marked tuple in H satisfies every relator of P. The pair-power relations have just been checked. For each commutator in (A-H1), the relevant power is trivial in the base and in every local factor other than its own support, while in that support the third marker is one. For either word in (A-S5), the base satisfies it by (A-S4)–(A-S5). In the \(\{0,1\}\) coordinate c is one; in the \(\{1,2\}\) coordinate a is one; in the \(\{0,2\}\) coordinate b is one. Thus each commutator word is trivial in every local coordinate. There is a marked epimorphism \(P\to H\).

It remains to prove that this map has no kernel. In P each \(K_{ij}\) is normal: its two endpoints invert the pair-product power, and the third marker centralizes it by (A-H1). Their cyclic orders are at most \(2^{s-2}\), \(2^{t-2}\) and \(2^{\ell-1}\). Their normal product K is therefore finite of order at most \(2^{s+t+\ell-5}\); neither commutation nor independence of the factors is being assumed for this bound. After quotienting by K, all remaining pair-power and commutator relations reduce exactly to (A-S1) and (A-S5). Section 3 identifies that quotient with \(Q_\delta\), of order \(2^{\delta+5}\). Hence P is finite and
\[
 |P|\le2^{s+t+\ell-5}2^{\delta+5}=2^n=|H|.
\]
The epimorphism is an isomorphism, by U.Order. This recognizes the bare source presentation and transfers the hypertope conclusion.

In H, the word \((ab)^4\) is trivial in the base and all coordinates except support \(\{0,1\}\), where it generates exactly the kernel of \(D_{2^{s+1}}\to D_8\). The corresponding statements hold for \((bc)^4\) and \((ac)^2\). Thus the displayed three subgroups are precisely the pure coordinate factors in U.SK. This proves the direct product and the exact quotient in (A-H2). Equations (A-S6)–(A-S7) now give (A-H3), including its action and parity. \(\square\)

The bound \(n\ge10\) was not needed in the proof, but it is retained in the statement to match the declared source contract. No nonexistence assertion for \(n<s+t+\ell\) follows from this construction.

### Prescribed square sections

**Theorem A4.2 (square kernels on a forest).** Let T be a forest and choose
distinct induced three-vertex paths S, with parameters \(n_S\)≥5. Attach
\(H_{n_S}\to H_5=(Q_T)_S\) to the model (A-F). Then

\[
 |H_J|=2^{|J|+|E(T[J])|+\sum_{S\subseteq J}(n_S-5)},\qquad
 \gamma_3(H)=\prod_S\gamma_3(H_{n_S}),\qquad H/\gamma_3(H)=Q_T.
 \tag{A-P}
\]

It has Boolean deletions and IP, and each selected triple is exactly \(H_{n_S}\).

*Proof.* Deleting coordinates in (A-F) gives all base deletions and its
parabolic order \(2^{|J|+|E(T[J])|}\). Section3 verifies every
proper-support injection and the local γ3 kernel. U.SK, including its
antichain and lower-central clauses, gives every assertion. ∎

For the d-vertex path, take all consecutive triples with parameters
\(n_3\),…,\(n_d\). Equation (A-P) gives the exact group order
\(2^{\sum n_j-3(d-3)}\), all prescribed square sections and all FAP
cuts. To prove flatness when d≥4, let L={0,…,d−2} and
M={d−3,d−2,d−1}. Every support lies on one side. The vertex-and-edge
counts in (A-F), together with IP, give \(Q_T=(Q_T)_L(Q_T)_M\).
U.SK therefore gives \(H=H_LH_M\). The stabilizer of the base (d−4)-face
contains \(H_M\), while \(H_L\) is a facet stabilizer; taking inverses also gives
\(H=H_MH_L\). The coset face criterion proves (d−4,d−1)-flatness and hence
flatness. The co-(−1)-face cut at d=3 is the tautological whole-polytope
cut; the other two cuts are genuine seed deletions. This proves all clauses
of **[CFHS25] Theorem 5.1**.

### The universal presentation is a separate conclusion

Write G for the group H constructed in the path case above. The supported
fiber group is not an arbitrary amalgam. To prove the source's
universal-presentation claim, a further local normalization argument is needed.

**Lemma A4.3 (four-marker centralization).** Suppose \(a,b,c,d\) are
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
prescribed triple presentation from §3. All its defining relators are
stable under every deletion assignment: the string Coxeter relators have
even exponents, and the local lattice relators survive every deletion of
their three markers by §3. Thus the assignments define endomorphisms of
\(P_0\), and U.D proves its IP without assuming finiteness. The
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
 \quad(0\le i\le d-4).                                  \tag{A-U}
\]
The constructed group satisfies these relations. For (A-U), no tuple
coordinate contains both disjoint edges; the edge missing one endpoint
has square one in that coordinate. Hence \(Q\twoheadrightarrow G\).
Each triple embeds in \(Q\), since its map onward to the embedded
triple in \(G\) is injective. Its third lower-central subgroup \(K_i\)
is generated by its two squared translations and has order
\(2^{n_{i+3}-5}\), by (A-S2). Lemma A4.3 and its reversed version show
that the nearest outside markers centralize \(K_i\), while the farther
markers do so by string commutation. Thus every \(K_i\lhd Q\).
Their product \(K\) is finite of order at most
\(2^{\sum_j(n_j-5)}\). Modulo it all triples are class two; each edge commutator commutes with its endpoints and nearest outside markers,
and with farther markers by string commutation. Thus \(Q/K\) is
class two. Collecting markers and central edge commutators gives
\( |Q/K|\le2^{2d-1}\). Therefore
\[
 |Q|\le2^{\sum_j(n_j-5)+2d-1}
      =2^{\sum_j n_j-3(d-3)}=|G|.
\]
U.Order, applied to the finite normal factors and the displayed quotient bound, identifies \(Q=G\) as marked groups.
Since \(P_0\) is the universal type group just constructed, this is
exactly its quotient by (A-U). The finite group presentation, the
universal group and both intersection properties have all been proved
using the same deletion calculus.


This proves **[CFHS25] Theorem 5.3**. No assertion about the order of the
universal group P_0 itself is required.

### Alternating assembly

We retain the following precise FAP case of Monson–Schulte's assembly theorem.
If regular (d−1)-polytopes P,Q have a common facet K and FAP retractions
\(\Gamma(P)=N_P\rtimes\Gamma(K)\) and
\(\Gamma(Q)=N_Q\rtimes\Gamma(K)\), the tail-triangle group
\((N_P\times N_Q)\rtimes\Gamma(K)\), with distinct final markers,
gives an alternating semiregular d-polytope with these facets. Its full
automorphism group is that group if P and Q are not isomorphic, and its
extension by branch-swapping C2 when P=Q; in that case the polytope is regular.
This is a retained geometric theorem, not a consequence of IP alone.

Apply A4.2 to the tree with common prefix and two final leaves, attaching the
two lists \((n_3,\ldots,n_{d-2},n_{d-1})\) and
\((n_3,\ldots,n_{d-2},m_{d-1})\). Write L,M for the facet label sets
and C=L∩M. The two deletions map H into \(H_L\times_{H_C}H_M\).
They are jointly injective: every vertex coordinate, edge coordinate and
supported kernel coordinate lies on one side and is detected there. Their
image is the full fiber product, since (A-P) gives its order
\(|H_L||H_M|/|H_C|\). Split deletions identify it with the exact
tail-triangle group in the retained theorem. For d=4 the common facet is a
square; otherwise it has list \((n_3,\ldots,n_{d-2})\). Its order is
\(2^{\sum_{j=3}^{d-2}n_j-3(d-5)}\), including 8 for the empty list.
The two facet kernels have orders \(2^{n_{d-1}-3}\) and
\(2^{m_{d-1}-3}\). Thus the full automorphism order is

\[
 2^{\sum_{j=3}^{d-2}n_j+n_{d-1}+m_{d-1}-3(d-3)}
\]

when the final parameters differ, and twice that order when they agree.
Unequal parameters give unequal facet orders and rule out an interchange;
equal parameters give identical marked facets and their branch swap.
These are exactly **[CFHS25] Theorem 6.1(a–b)**. No additional mixed
co-(d−4)-section is prescribed.

## 5. Bounded cyclic cores and the eight high-type families

The supported constructions solve existence. Completeness at the high
dihedral boundary needs a different local invariant, the cyclic core. Its
bounded quotient is nevertheless recognized by the same square model, and
its only finite seed is generated by the same U.Nilpotent/U.Ladder search as order 1024.

The retained **cyclic core theorem of Lucchini** says: if a cyclic proper
subgroup \(M\) of a finite group \(H\) has core \(K\), then
\(|M:K|<|H:M|\). Here \(K\) is the largest normal subgroup of \(H\)
contained in \(M\). We use the form recorded in Isaacs, *Finite Group
Theory*, Theorem 2.20, also stated as L035 Proposition 2.9.

**Theorem A5.1 (bounded cyclic quotient).** Let \((G;a,b,c)\) be a
rank-three string C-group of order \(2^{t+s}\), type \(\{4,2^t\}\),
with \(s\ge3\) and \(t\ge s-2\). Put
\[
 r=bc,\quad m=2^t,\quad d_0=(ab)^2,\quad
 A=\langle r^{2^{s-2}}\rangle.
\]
Then \(A\lhd G\), and \(G/A\) is a string C-group of order
\(2^{2s-2}\) and type \(\{4,2^{s-2}\}\).

**Proof.** The even-word subgroup \(H=\langle ab,bc\rangle\) has
index at most two. IP and U.Phi give \(G/G'=C_2^3\), where its image
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
 r^a=d_0r,\quad d_0^a=d_0,\quad r^c=r^{-1},\quad d_0^c=d_0^r       \tag{A-C1}
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
 (u+u',v+v',w+w',e+e'+\beta(vu'+wv')).                    \tag{A-C2}
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
 N=(D\rtimes\langle r\rangle)/\langle zr^{-m/2}\rangle.       \tag{A-C3}
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
form (A-C3) gives \(d_0\notin\langle r\rangle\), leaving exactly
\(\langle b\rangle\). The three generators are independent (already
\(a\notin\langle b,c\rangle\), and the pair orders exclude the others),
so this proves rank-three IP. Direct substitution yields
\[
 \begin{array}{ll}
 s=3:&[d_0,c]=z^\epsilon,\\
 s=4:&[d_0,r^2]=z^\epsilon,\\
 s=5:&[a,r^2]^2=z^\beta,\qquad[a,r^4]=z^\nu.
 \end{array}                                                   \tag{A-C4}
\]
They are invariant words of the ordered marking and distinguish the two,
two and four models within their branches.

### Completeness and bare presentation recognition

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

**Theorem A5.2 (high-type completeness).** Every group in the three
classes of L035 Theorem 1.3 is exactly one of the marked models of §5;
each displayed source presentation defines that model.

**Proof, first branch.** For \(s=3\), Theorem A5.1 gives a quotient of
type \(\{4,2\}\) and order sixteen, necessarily \(D_8\times C_2\).
Thus \(h=[d_0,r]\in A=\langle r^2\rangle\). Since it commutes with
\(r\), and \(d_0\) centralizes \(A\),
\(h^2=[d_0,r^2]=1\). Hence \(h=1\) or \(z\), and (A-C1) makes this
exactly \([d_0,c]=z^\epsilon\). The conjugates of \(d_0\) obey
\(d_1=d_0z^\epsilon\); (A-C1) forces all the first model's actions and
normal forms. The resulting surjection from that model onto the actual
group is between groups of the same order, hence an isomorphism.

**Second branch.** For \(s=4\), the quotient of order 64 and type
\(\{4,4\}\) is \(H_6\), by Lemma A3.1. In that affine quotient
\([d_0,r^2]=1\), so upstairs \(h=[d_0,r^2]\in\langle r^4\rangle\).
Again \(h^2=[d_0,r^4]=1\), giving \(d_2=d_0z^\epsilon\), where
\(d_i=d_0^{r^i}\). Conjugation by \(a\) fixes \(d_0,d_1\).
Applying it to the equation for \(d_2\), with \(z\) central, gives
\(d_2^a=(d_1^{d_0})^r=d_2\), so \([d_0,d_1]=1\).
All second-model relations follow, and the same order comparison proves
uniqueness.

**The bounded seed for the third branch.** The same universal-kernel theorem used for the order-1024 classification gives the following finite fact: every order-256 marked string C-group of type \(\{4,8\}\), with \(r=bc,d_0=(ab)^2\), satisfies exactly one row.

| Row | Relation pattern | Ordered marked classes |
|---|---|---:|
| I | \([a,r^2]^2=1,\ [a,r^4]=1\) | 1 |
| II | \([a,r^2]^2=r^4,\ [a,r^4]=1\) | 1 |
| III | \([d_0,r^2]=r^4\) | 1 |
| IV | \([(r^2)^a,r]=r^4\) | 1 |

Apply U.Nilpotent and U.Ladder, as specialized in A2.5 with d=3 and k=3. The universal class-five group has order 2¹⁸ and third lower-central subgroup of order 2¹³. Its invariant index-two ladder has 7, 23 and 61 kernels. Testing all 64 subset pairs for each final candidate gives 37 ordered IP markings, four with the indicated orientation of type {4,8}. The census program in Appendix C evaluates every displayed word on all four and verifies that each belongs to exactly one row, one marking per row. Section 7 states the complete output and the shared finite-search proof. Thus this bounded input is now conditional on exact GAP/NQ algorithms, with no abstract-group catalogue. No SmallGroups identifier or catalogue multiplicity enters these relation implications.

**Third-branch lifts.** For \(s=5\), Theorem A5.1 gives
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
Let \(N=\langle d_0,r\rangle\). Equations (A-C1) make it normal, with
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
the table in §5, and (A-C1) forces the actions of the commuting complement
\(\langle a,c\rangle\). The model maps onto \(G\) and has its order
\(32m\), so is isomorphic. This proves completeness of the eight models.

It remains to recognize the **bare presentations**, where the target
order cannot yet be assumed. Let \(P\) be one of them and
\(z=r^{m/2}\), initially of order at most two. For \(G_1,G_2\), if
\(\epsilon=1\), \(a\) centralizes \(z=[d_0,c]\) since it centralizes
\(d_0,c\); \(b,c\) centralize it since they invert \(r\). If
\(\epsilon=0\), \(d_0\) is central; (A-C1) and the evenness of \(m/2\)
then make \(z\) central too. Collection gives at most \(8m\) normal
forms, attained by the first model.

For \(G_3,G_4\), \(d_2=d_0z^\epsilon\). If \(\epsilon=0\), applying
\(a\) as in the second-branch argument gives \([d_0,d_1]=1\), after
which the model relations and centrality of \(z\) follow. If
\(\epsilon=1\), \([d_0,r^2]=z\) implies that conjugation by \(d_0\)
inverts \(z\); as \(z^2=1\), it centralizes \(z\). Thus \(z\)
commutes with \(r\) and all \(d_i\). Write \(j=[d_0,d_1]\).
Applying \(a\) to the equation for \(d_2\), and using (A-C1), gives
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


## 6. Central descent and complete binary lifts

This branch concerns the principal nondegenerate classification in Gomi–Loyola–De Las Peñas [GLP18], with the marking retained. Its equivalence sends the distinguished generator set onto the other set. For a connected string diagram this permits precisely the two orders related by reversal. It does not identify arbitrary markings of an abstractly isomorphic group. The rank-two case is the unique dihedral marking of order 1024. The three higher-rank totals below are 125, 105 and 8; all stated types, facets and universal orders are part of the conclusion.

The specifically retained prior results in this branch are the standard string intersection criteria quoted as [GLP18] Lemmas 2.2–2.4, the universal geometric interpretation quoted as its Theorem 4.2, the finite smooth square-quotient classification quoted as its Lemma 5.1, and the exceptional infinite universal decomposition quoted as its Theorem 5.3. Their relevant precise forms are stated below. Exact finite-group and complete coset-enumeration algorithms in GAP, and NQ's universal nilpotent quotient algorithm, are computational inputs. The Atlas supplies definitions of named marked presentations, all included in the defining-data appendix; neither its completeness nor a SmallGroups catalogue is assumed.

### 6.1. Preliminary adapters and exact quotient intersections

**Proposition N1 (endpoint cosets).** A finite string C-group of rank d and adjacent orders m₁,…,m_(d−1) has order at least 2∏mᵢ. In particular, a nondegenerate string two-group of order 1024 has rank at most five.

*Proof.* Put a=r₀, b=r₁ and H=⟨r₁,…,r_(d−1)⟩. IP gives H∩⟨a,b⟩=⟨b⟩. If H(ab)ⁱ=H(ab)ʲ, then \((ab)^{i-j}\) lies in the intersection of the rotation subgroup with ⟨b⟩, which is trivial. The m₁ such cosets, with 0≤i<m₁, are therefore distinct. Iterating gives the bound. Each mᵢ is at least four in the stated two-group case, so \(2^{2d-1}\)≤1024, forcing d≤5. ∎

The smooth Coxeter quotient assertion in source Theorem 2.7 is the homomorphism from the string Coxeter presentation sending each distinguished generator to its marked involution; the specified adjacent orders make it smooth. A disconnected string diagram yields a direct product of its component subgroups: they commute and IP makes each meet the subgroup on the other components trivially. This gives the source's preliminary reduction; a separate census of every degenerate product is not added to the principal contract. Source Lemma 2.8 is the coordinate-character consequence of Burnside's basis theorem: an irredundant generating list of a finite two-group maps to a basis of G/Φ(G), and every binary assignment extends to a homomorphism to C₂. No infinite-group assertion is made here.

For rank three write L=⟨a,b⟩ and R=⟨b,c⟩. The retained rank-three criterion says that these two rank-two marked string C-groups, together with [a,c]=1 and L∩R=⟨b⟩, give full IP. Precisely, for d=4 or 5, the versions quoted in source Lemmas 2.3–2.4 require the prefix H=⟨r₀,…,r_(d−2)⟩ to have IP and each equality H∩⟨rⱼ,…,r_(d−1)⟩=⟨rⱼ,…,r_(d−2)⟩ for j=1,…,d−1, with the final right side trivial. These are respectively all four and all five source hypotheses. All finite certificates below instead test every subset pair directly.

If N◁G and N∩RL=1, U.Q says the quotient facets have exactly their old intersection and both embed; their product orders are unchanged. This is source Lemma 3.1. If N≤L and the displayed images of a,b still give a rank-two marking on L/N, then N∩R≤⟨b⟩ and b∉N, so R embeds. The last clause of U.Q gives the same facet intersection and the rank-three criterion gives IP. This is source Lemma 3.2, including its symmetric case. An unrelated marking on the abstract quotient L/N would not suffice.

### 6.2. A safe central quotient and the three complete lift patterns

Assume throughout this subsection that G is a finite marked string two-group ⟨a,b,c⟩, with m=|ab|≥4 and n=|bc|≥4. Put x=\((ab)^{m/2}\) and y=\((bc)^{n/2}\).

**Lemma N2 (central elements in an end product).**

\[
Z(G)\cap RL\subseteq\{1,x,y,yx,ybx\}.
\tag{N1}
\]

If yx is central, x and y are separately central. The element ybx is never central.

*Proof.* Every element of RL has a unique expression h(ab)ʲ with h∈R and 0≤j<m. Equality of two expressions would put a rotation in L∩R=⟨b⟩. Conjugation by b negates j, so centrality implies j=0 or m/2. The former case gives an element of Z(R)={1,y}. In the latter case write z=hx; since x commutes with b, h lies in C_R(b)={1,b,y,yb}. The choice h=b fails because the reflection bx does not commute with a when m≥4. This proves (N1).

If yx commutes with a, then y does, because x already does; commuting with c similarly makes x commute with c. Thus both half-rotations are central. Finally x,y∈Φ(G), since they are even powers of rotations. If z=ybx were central, then a,z,c would have the same Frattini basis as a,b,c and would generate G. A central z is an involution here: z∈C_G(x) implies y commutes with x, and y,b,x are commuting involutions. Thus a,z,c are three commuting involutions, contradicting |ab|≥4. ∎

**Theorem N3 (central descent with IP).** G has a central order-two subgroup N such that the displayed images of a,b,c give a rank-three string C-group on G/N. Successive such descents, allowing degenerate intermediate markings, stop at C₂³.

*Proof.* If x is central, take N=⟨x⟩. The marked dihedral quotient L/N has rotation order m/2≥2 and R embeds because N∩R=1. The N≤L clause of U.Q proves the quotient intersection. The same reasoning applies to central y. If neither half-rotation is central, choose any central involution z, which exists in every nontrivial finite two-group. Lemma N2 puts z outside RL; now the injective-ends clause of U.Q proves IP and preserves both end groups. A degenerate rank-three marking is C₂ times a dihedral marking. Unless it is C₂³, the central rotation involution of its nonabelian dihedral factor can be factored out while preserving rank three. Orders strictly decrease by two, so this process terminates exactly at C₂³. ∎

This proves source Corollary 3.3, Lemmas 3.4–3.5 and Theorem 3.6. The bottom boundary is necessary in source Corollary 3.7: a rank-three order-eight group cannot have a rank-three order-four quotient. Its literal unrestricted wording is not asserted.

**Theorem N4 (three lift patterns with complete presentations).** Let Q be a finite rank-three marked string C-group with a complete presentation in its involutions a₀,b₀,c₀, including Coxeter relations and additional relators R₁,…,Rₜ. Let G=⟨a,b,c⟩ be a central extension with kernel ⟨z⟩ of order two, mapping those involutions respectively to a₀,b₀,c₀. Suppose the lifts are involutions, [a,c]=1 and G has IP. Exactly three order patterns are possible: the left adjacent order doubles, the right adjacent order doubles, or neither doubles. In each case a complete presentation is obtained by adjoining central z with z²=1, each defining Coxeter word of Q set equal to its actual value 1 or z (in particular \((ab)^{p}\)=z when its quotient order p doubles), and equations Rᵢ=\(z^{\epsilon _i}\), εᵢ∈{0,1}. At least one relation expresses z as a word in a,b,c, so z can be eliminated.

*Proof.* Each adjacent order is unchanged or doubled. If both doubled, z would be the halfway rotation in both L and R and hence in their intersection ⟨b⟩, impossible for a nontrivial dihedral rotation. Every defining word of Q lifts to 1 or z. The indicated presentation P maps onto G and has P/⟨z⟩=Q; centrality and z²=1 imply |P|≤2|Q|=|G|, proving that map an isomorphism. When an adjacent order doubles, its half-power is z. If neither does and every additional relator lifted to 1, the generating tuple would define a surjection Q→G, contradicting the orders. ∎

This is source Theorem 3.8 and Table 1. It classifies successful extensions; it does not assert that every binary lift choice has the required order or IP. Those properties and equality of ordered markings must still be checked.


## 7. Exhaustive bounded classification and named objects

Apply A2.5 (U.Nilpotent/U.Ladder) to the path on d vertices with k=log₂|G|−(2d−1). The census program of Appendix C is a single parameterized program for the four cases in the following table. NQ computes the universal nilpotent quotient of class k+2. The original generators are transported through its epimorphism and pc isomorphism; they are never replaced by an arbitrary generating list. Every normal kernel in the invariant ladder is generated, with only equal subgroups deduplicated. The binary canonical subgroup key is used only after all ambient relative pc orders have been checked to be two.

| d | k | Order of U | Order of γ₃(U) | Kernels | IP | Fixed | Classes | Meets |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 3 | 2¹⁸ | 2¹³ | 61 | 37 | 3 | 20 | 3904 |
| 3 | 5 | 2³⁸ | 2³³ | 401 | 235 | 15 | 125 | 25664 |
| 4 | 3 | 2³⁴ | 2²⁷ | 1483 | 199 | 11 | 105 | 379648 |
| 5 | 1 | 2¹⁶ | 2⁷ | 127 | 15 | 1 | 8 | 130048 |

Here Kernels counts terminal normal subgroups, IP counts ordered markings satisfying every intersection test, Fixed counts reversal-fixed markings, and Meets counts actual subgroup-intersection checks. The ladder sizes are respectively (7,23,61), (7,23,61,147,401), (31,267,1483) and (127). These are computed outputs, never candidate filters. All 539264 subset-pair intersections are tested, including every candidate rejected by the kernel-profile criterion, and the two IP decisions agree for every candidate. Burnside's orbit formula gives (ordered+fixed)/2 reversal classes. The four ordered type-{4,8} markings in the first case satisfy the four distinct word rows in §5, one each; this is the same finite input used in the eight-family completeness proof. The last three cases prove the classification at order 1024, with the rank bound in Proposition N1 proving that no further nondegenerate rank is omitted.

For rank three the twelve type counts, up to reversal, are:

| Type | Count | Type | Count |
|---|---:|---|---:|
| {4,4} | 1 | {8,8} | 22 |
| {4,8} | 8 | {8,16} | 40 |
| {4,16} | 14 | {8,32} | 8 |
| {4,32} | 4 | {8,64} | 4 |
| {4,64} | 2 | {16,16} | 10 |
| {4,128} | 2 | {16,32} | 10 |

These are exactly source Table 5. The complete presentations defining all named facets, and the full 107 rows of Table 6, appear as literal mathematical data in the complete defining-data artifact of Appendix C. For every one of the 199 rank-four and 15 rank-five ordered markings, the presentation checker of Appendix C reconstructs the quotient from its exact new kernel key and proves unique generator-preserving isomorphisms from both named end groups: 428 exact facet identifications. It computes dual names from reversed generators, rather than assuming that equal-looking types or letter suffixes are self-dual. Under reversal a facet pair (A,B) becomes (dual(B),dual(A)). Counts are compared after this operation for each of the 99 rank-four and eight rank-five rows individually.

The four printed type-{4,16,4} rows in Table 6 have right-hand type {4,16}; their ordered vertex-figure markings necessarily have type {16,4}. The data use precisely these duals, preserving every letter suffix and count. This qualification was checked on printed page 16; it is not an inferred change to class counts.

For each of the 106 finite rows, the complete universal presentation is the union of the two complete facet presentations, shifted to overlapping generator lists, together with the distant-end commutation relation. Completed Todd–Coxeter enumeration at the trivial subgroup gives 101 orders of 1024 and five orders of 2048. The finite checker also verifies actual IP and both exact facet embeddings. The remaining row is the explicitly retained infinite universal of §7.4; it is never sent to an unbounded finite-order test.

### 7.2. Every printed rank-three presentation and its corrections

The complete finite-presentation protocol in the presentation checker of Appendix C takes the bare displayed relators, performs complete trivial-subgroup Todd–Coxeter enumeration, and checks that the resulting permutation action has the table's full order. It evaluates every relator, proves generation by the specified marked involutions, and tests all \(4^{d}\) marked-subgroup intersections. Thus its order bounds concern the raw presented groups, not just finite images or nilpotent truncations.

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

### 7.3. Universal presentations and all finite examples

For source Definition 4.1 use the combined facet presentation described in §7. The retained geometric universal principle, source Theorem 4.2, states that a nonempty class of regular polytopes with those specified facet and vertex-figure groups has that marked universal string C-group and every member is its smooth quotient. At the group-presentation level the epimorphism is immediate from the defining words; the abstract-polytope interpretation remains an explicit background input.

The bare presentations in Examples 4.3–4.5 give:

| Object | Raw order | Type | Ordered end labels |
|---|---:|---|---|
| Example 4.3 universal | 512 | {4,4,4} | {4,4}\*32, {4,4}\*128 |
| Example 4.4 universal | 1024 | {4,4,4} | {4,4}\*32, {4,4}\*256 |
| Example 4.5 universal | 2048 | {4,4,8} | {4,4}\*64, {4,8}\*128a |
| Example 4.5 first quotient | 1024 | {4,4,8} | same two labels |
| Example 4.5 second quotient | 1024 | {4,4,8} | same two labels |
| Example 4.5 third quotient | 1024 | {4,4,4} | not in the prescribed smooth class |

The first two universal presentations add (abcb)²=(bcdc)⁴=1 and (abcb)²=(dbc)⁸=1 respectively to the type-{4,4,4} Coxeter relations. The third adds

\[
(cab)^4=1,\qquad dbcd(cb)^2(dc)^2bc=1
\tag{N3}
\]

to the type-{4,4,8} relations. The complete named facet words in the complete defining-data artifact of Appendix C differ, where necessary, only by cyclic conjugation from these displayed source words. Their exact generator-preserving isomorphisms and the full raw order/IP tests verify each row above.

For the order-2048 group the three printed central-involution words are

\[
bcdcbab(dc)^2dba,\qquad(bcdcba)^2,\qquad(cd)^4.
\tag{N4}
\]

The checker independently enumerates all central involutions and obtains exactly these three distinct elements. Adding each as a raw relator gives the three quotient rows above. The first two are inequivalent marked groups, with unchanged type and end markings. Every normal order-two subgroup is central, so these three exhaust all order-1024 quotients of this universal, and exactly two belong to the prescribed smooth class. Example 4.3 has no quotient of order 1024; Example 4.4 has only itself. These statements concern these exact orders and do not extrapolate centrality to larger kernels.

### 7.4. Square-lattice centers and the exceptional infinite row

Retain the finite smooth square-quotient classification quoted in source Lemma 5.1: a finite smooth quotient of [4,4] lies in one of the two families obtained by adding \((abcb)^{s}\)=1, of order 8s², or \((abc)^{2s}\)=1, of order 16s², for a positive integer s. The former has |abcb|=s and |abc|=2s; the latter has |abcb|=2s and |abc|=2s. The square and diagonal decompositions are now supplied by A3.2, including s=1. In the marking used here they are
\[
 (\langle a,c^b\rangle\times\langle c,a^b\rangle)\rtimes\langle b\rangle,
 \qquad
 (\langle b,b^{ac}\rangle\times\langle b^a,b^c\rangle)\rtimes\langle a,c\rangle,
\]
respectively. Each factor has order 2s and the complements have orders two and four. To check the marking in the second expression, its two pairs of reflection axes are x−y=0,1 and x+y=1,0; their products translate by (−1,1) and (1,1). The perpendicular factors, independent translations and complement parity check are exactly those in A3.2. The source instead prints the pairs \(\langle b,b^a\rangle\), \(\langle b^c,b^{ac}\rangle\). That pairing is erroneous for general s: \(bb^a=(ba)^2\) has order two, so its first factor always has order four. The classification is retained; this structural correction and its proof are not assumed from it. Only the finite scope is used; the infinite Coxeter group itself is not asserted to admit such an s.

Use the common affine model of §3 after reversing its endpoints and conjugating all three generators by b. Since the lattices are invariant under the coordinate swap, the same square and diagonal quotients have coordinates

\[
a(x,y)=(1-x,y),\quad b(x,y)=(y,x),\quad c(x,y)=(x,-y).
\tag{N5}
\]

Its group is W=ℤ²⋊D₈; t=abcb translates by (1,0), (abc)² translates by (1,1), (bc)² is (0,−I), and (ab)² is ((1,1),−I). The two finite families are W/sℤ² and W/L_s, where L_s=⟨(s,s),(s,−s)⟩. The §3 affine normal forms establish these identifications; equivalently the displayed source relations give surjections onto these affine images of the stated orders, hence isomorphisms.

**Proposition N5 (all source center formulas).** For s=\(2^{m}\), in W/sℤ² the center is ⟨(ab)²,(bc)²⟩ when m=1 and ⟨\((abc)^{s}\)⟩ when m≥2. In W/L_s it is ⟨ac,(ab)²,(bc)²⟩ when m=0 and ⟨\((abcb)^{s}\)⟩ when m≥1.

*Proof.* In a central affine pair (v,M), commutation with all translations forces M to act trivially on T=ℤ²/L. If the signed-permutation action on T is faithful, M=I and the center is \(T^{D_8}\).

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

the presentation checker of Appendix C proves directly that these two raw groups have order 1024 and full IP, and identifies them with the two and only two census markings whose ordered ends are {4,4}\*128 and {4,4}\*64. Unequal end orders rule out their becoming equal under reversal. This proves the exact exceptional classification without repeating the source's separate case analysis or presuming its presentations finite.

The finite execution in the presentation checker of Appendix C totals 214 complete presentations and 43840 actual IP meets: 72 defining Atlas models, 34 source example/literal-table presentations, the two exceptional presentations, and 106 finite universal presentations. Its distinct logical role from the census program of Appendix C is preserved: the universal-kernel proof gives exhaustion, while complete raw coset tables and exact marked isomorphisms give presentation and name recognition. All code and mathematical data are included as complete external appendices with the bindings in Appendix C. These are exact finite computations conditional on the stated algorithms, not Lean proofs or experimental extrapolations. The concluding source suggestion about geometric realizations, a separate classification of all degenerate products, and historical novelty of the corrections are outside the contract.


## 8. Free extensions and two-primary torsion

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

In each of the three free-extension identifications the common subgroup
is proper in both factors, as the face/flag action or the new reflection
shows. In the second factor of the first two constructions its index
is two. Every factor has two-primary torsion: in the chiral case the
**rotation subgroup** of the facet embeds in \(\Gamma(K)\), and its
extension by \(C_2\) suffices to prove the property for \(\Gamma(F)\).
All factors are finitely generated by their finite marked sets. U.Amalgam
and, when needed, its finite-extension clause prove exactly **F016
Theorems 7.1, 7.2 and 7.3**, including infinite input groups. No assertion
that all elements have finite order is made.


## 9. Source contracts, corrections and attribution

The F013 common-quotient theorem is recovered by a different kernel. Its
specified auxiliary subgroup is false in general. We include the proof
of the correction so that no false historical claim is counted as a
corollary of this manuscript.

In the path model (A-F), name the central edge coordinates
\(c_1,\ldots,c_{d-1}\), and put
\[
 \sigma_i=r_{i-1}r_i,\quad
 A_i=\langle\sigma_1,\ldots,\sigma_{i-1},\sigma_i^2,
                  \sigma_{i+1},\ldots,\sigma_{d-1}\rangle,
 \quad C=\bigcap_i\Phi(A_i).                              \tag{A-X1}
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
 \quad(d\ge3).                                          \tag{A-X2}
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
so their orders cannot be multiplied as in its page-11 argument; (A-S2)
uses the correct lattice index. In its chiral extension proof the full
facet automorphism group need not embed in the chiral group; §8 only
uses its rotation subgroup and a finite index-two extension.


The [HFLh] structural display reverses the square and diagonal parity cases on both pp. 7 and 8 of the retained author version. Its stated dihedral exponents are nonintegral in those respective parities. The affine quotient calculation in §3 gives the corrected assignments in (A-H3), agreeing with the source's preceding calculation. The second cyclic subgroup's displayed definition also repeats the first pair word; its correct generator is \((bc)^4\), as used in Theorem A.H. These literal erroneous displays are not asserted as true. Proposition A3.2 rederives both decompositions of [HFLh, Lemma 3.1], already attributed there to McMullen–Schulte, for every integer \(q\ge2\). Theorem A.H recovers its complete principal Theorem 3.2 with these stated corrections. It does not prove Conjecture 3.3 or infer nonexistence from the construction.

The diagonal factor pairing quoted in [GLP18, Lemma 5.1(ii)] is also corrected in §7.4. Its printed first factor has order four independently of the lattice parameter; A3.2 supplies the correct two factors and complement for every positive parameter. The affine center proofs and finite classification certificates do not use the erroneous pairing. The source’s two-family classification remains a separate retained input.

The exact intake is the six specified editions in the references. The following
is the principal-result map; the companion ledger expands every normalized
statement, multipart clause and all 33 [GLP18] numbered/table records.

| Source | Target contract | Derivation and actual U call |
|---|---|---|
| [HFLa], Theorem 1.2 | Every admissible rank, order and sequence of 2-power adjacent orders | A4.1; square seed; U.SK with two-generator proper-parabolic checks |
| [HFLb], Theorem 1.2 | Rank-three existence in the stated n≥10 range | d=3 specialization of A4.1 |
| [HFLb], Theorem 1.3 | All 2+2+4 high-type families; completeness, bare orders/IP and marking distinction | §5; A3.1; cyclic-core input; A2.5/U.Nilpotent/U.Ladder seed and exact relation checks |
| [HFLh], Theorem 3.2 and auxiliary Lemma 3.1 | Exact three-generator presentation, order, pair orders, regular geometry, cyclic kernel product and corrected quotient structure | §3 affine words/decompositions; A4.1 with U.SK.Geometry; A.H sharp presentation bound via U.Order |
| [HS26], Theorems 1.1–1.2 | Canonical marked quotient and geometric cover for every finite nondegenerate rank | A2.1–A2.4; U.Phi; retained cover correspondence |
| [CFHS25], Theorem 5.1(a–d) | Exact prescribed sections/order, flatness and all required FAP cuts | A4.2 path binding; U.SK antichain, γ3, separator and deletion clauses |
| [CFHS25], Theorem 5.3 | Exact quotient of the universal local presentation | A4.3 normalization, actual local embeddings and finite order bound |
| [CFHS25], Theorem 6.1(a–b) | Alternating semiregular assembly and exact full automorphism order | A4.2 fork binding; two-deletion fiber isomorphism; retained assembly theorem |
| [CFHS25], Theorems 7.1–7.3 | Regular, chiral and alternating free extensions, including infinite input | §8; all geometric embeddings/properness checked; U.Amalgam |
| [GLP18], §§2–3/Table 1 | Marked quotient criteria, central descent and all binary lift patterns | §6; U.Q/U.Phi; explicit center-in-product argument |
| [GLP18], Example 3.9/Tables 2–4 | Every stated raw presentation and intended named target; diagnosed literal discrepancies | §7.2; complete coset tables and generator-preserving isomorphisms |
| [GLP18], Examples 4.3–4.5 | Exact universals and their order 1024 smooth quotients | §7.3; complete raw presentation orders/IP and all central involutions |
| [GLP18], Lemmas 5.1–5.4/Theorem 5.5 | Lattice centers, retained infinite decomposition, kernel location and exactly two exceptional targets | §7.4; A3.1 affine model; U.Phi; exact census and presentations |
| [GLP18], Tables 5–6 | All 125 rank 3,105 rank 4 and 8 rank 5 reversal classes; all 107 facet rows and universal orders | A2.5/U.Nilpotent/U.Ladder plus all-parabolic census and exact named-object recognition |

The [HS26] auxiliary kernel assertions are corrected above; its two principal
existence conclusions remain recovered. The [CFHS25] diagonal-translation and
chiral-facet proof steps use the corrected arguments stated here. In [GLP18],
Corollary 3.7 stops at order8, Table 4's literal rows remain distinguished from
their repaired targets, and reversed facet markings in Table 6 are explicit.
The retained inputs are part of the contract, not silently counted as newly
proved results. No open question, historical novelty claim, unnumbered small-n
classification or separate census of degenerate products is included. The
power-polytope recollections in [CFHS25] are not extra source targets.

This scientific organization and the supported-kernel applications are repository
work, with the support-inclusion simplification credited to independent reviewer
122. The source authors receive credit for the original results and
constructions. The classical ingredients of U and the new assembly carry no
historical-priority claim. Removing one declared U dependency only invalidates
the recorded derivation; it does not show that the conclusion has no other proof.

## Appendix C. Complete computational proof interface

There are four complete external artifacts, all part of this volume's proof
cost: `phase78_n009_integration_census.g`,
`phase78_n009_integration_finite.g`,
`phase78_n009_integration_data.g` and
`phase78_n009_integration_run.py`. Their legacy filenames identify established
reusable artifacts; no surrounding manuscript is imported by those filenames.
The first three contain every executed mathematical instruction and all 72 named
Atlas presentations,107 Table 6 rows and source relators. The fourth is the
complete no-clobber orchestration and output checker. Source editions and
artifacts are hash-bound in the companion ledger with their retained verified executions.

The exact algorithms assumed are GAP's finite permutation/pc group arithmetic,
subgroup intersection and complete Todd–Coxeter enumeration, and NQ's universal
nilpotent quotient algorithm. A completed coset table at the trivial subgroup
establishes the raw presentation order; a finite image alone would not suffice.
No source count is used to prune candidate generation, and no saved certificate,
private primary file, permutation-array atlas or SmallGroups catalogue is read.

For every (d,k), the census constructs \(U_{T,k}\) from its original marked
nilpotent quotient map, transports those same generators, and enumerates every
U-normal index-two hyperplane preimage k times. Only equal subgroups are
deduplicated. Its binary subgroup key is used only after checking that every
ambient relative pc order is two. A2.5 supplies completeness. Every terminal
candidate is subjected both to the kernel-profile test and to all \(4^{d}\) actual
marked subgroup meets, including rejected candidates. Reversal is computed on
the markings; the observed fixed count and the two-element orbit formula give
the generator-set classes. The order 256 seed evaluates the four distinct word
patterns on each oriented type-{4,8} marking, so its use in §5 is an explicit
finite implication with no hidden classification assumption.

The presentation checker constructs all raw groups from complete relators,
finishes the trivial-subgroup coset table, evaluates all defining relations,
checks generation, exact involution/product orders and all subset intersections.
It verifies each facet name by an actual generator-preserving isomorphism.
Dual names are computed using reversed generators. It enumerates all central
involutions in the order 2048 example and checks every quotient. For each finite
Table 6 row it combines both complete facet presentations and distant-end
commutation, proves the raw universal order and verifies both facet embeddings.
The one infinite row invokes the precisely stated retained decomposition; it
is never sent to an unbounded finite-order computation.

The complete run requires 539264 census meets,214 raw presentations and 43840
additional meets,428 exact facet identifications and all 107 Table 6 rows. These
are expected results checked after exhaustive generation, not assumptions
proving it. Successful replay establishes the finite conditional obligations,
not a Lean formalization or a substitute for the parameter proofs.

From the public repository root, run:

```sh
python3 -B -O research/case_study/phase78_n009_integration_run.py --output-dir /private/tmp/NEW-two-group-certificate
```

The output path must not exist. The artifact manifest records source/program
hashes, installed versions, complete logs and all generated mathematical data.
The application ledger charges the four source files in full, plus the complete
shared U body and all written hypotheses in A. Rendered mathematical
pages, certificate bytes and any cumulative multi-volume accounting will be
reported separately after complete review; the supported-kernel acquisition
cost is not waived because it has several users.

## References and source-version boundary

[U] *Marked groups, kernels and intersections*, companion manuscript, version 3.

[HFLh] D.-D. Hou, Y.-Q. Feng and D. Leemans, *Existence of regular 3-hypertopes with \(2^n\) chambers*, arXiv:1901.09034v1, 23 January 2019. The retained author PDF has eleven pages, SHA-256 `9d15089679be3828ff9291b4926ef3e3bd1a602449c67ce76ea17c7d9d1a6bfd`. The structural parity and repeated-pair-word corrections are given in §9; no journal-version collation is inferred.


[HFLa] D.-D. Hou, Y.-Q. Feng and D. Leemans, *On regular polytopes of 2-power order*, revised author PDF dated 8 November 2019, journal 2020, DOI 10.1007/s00454-019-00119-5. Exact retained primary file: `sources/catalogue_L032.pdf`.

[HFLb] D.-D. Hou, Y.-Q. Feng and D. Leemans, *Existence of regular 3-polytopes of order \(2^{n}\)*, arXiv:1802.08947v2, 22 January 2019; journal catalogue title *2-groups behaving as automorphism groups of regular 3-polytopes*. Exact retained primary file: `sources/catalogue_L035.pdf`.

[HS26] D.-D. Hou and E. Schulte, *String C-groups of 2-power order project onto a common string C-group*, arXiv:2605.20691v1, submitted 20 May 2026, PDF dated 21 May. Exact retained primary file: `sources/catalogue_F013.pdf`.

[CFHS25] G. Cunningham, Y.-Q. Feng, D.-D. Hou and E. Schulte, *Symmetric polytopes whose automorphism groups are 2-groups*, arXiv:2512.15511v1, submitted 17 December 2025, PDF dated 18 December. Exact retained primary file: `sources/symmetric_2groups2025.pdf`.


[GLP18] Y. Gomi, M. L. Loyola and M. L. A. N. De Las Peñas, *String C-groups of order 1024*, Contributions to Discrete Mathematics **13**(1) (2018), 1–22, DOI [10.55016/ojs/cdm.v13i1.62475](https://doi.org/10.55016/ojs/cdm.v13i1.62475). [Primary journal PDF](https://cdm.ucalgary.ca/article/download/62475/46803), SHA256 `0618a57cb5ff35c13587877818a2e77bce442cf2c561f204b6d5e5e095fa2fda`.

Its quoted standard intersection criteria are attributed to M. Conder and D. Oliveros, *The intersection condition for regular polytopes*, JCTA **120** (2013), 1291–1304. The universal and finite square-quotient inputs are quoted from McMullen–Schulte, *Abstract Regular Polytopes* (2002), the latter on pp. 364–365, 368. Its exceptional infinite decomposition is quoted from McMullen–Schulte, *Regular polytopes from twisted Coxeter groups and unitary reflexion groups*, Advances in Mathematics **82** (1990), 35–87. Those earlier proofs are retained in the precise quoted forms; no claim of fresh acquisition or rederivation is made.

The named-object data are credited to M. I. Hartley's Atlas of Small Regular Polytopes; the complete defining-data artifact records the exact primary URL and snapshot hash for every defining presentation. The URL may contain a catalogue identifier, but replay neither calls SmallGroups nor assumes a catalogue is complete. The entire new finite search and recognition were run with GAP 4.15.1 and NQ 2.5.11. 


The retained cyclic-core result is Lucchini's theorem in the form recorded by
Isaacs, *Finite Group Theory*, Theorem 2.20. The retained alternating assembly
is Monson–Schulte, *The assembly problem for alternating semiregular polytopes*
(2020), Theorem 5.3 in its FAP case. The chiral free-extension theorem is
Schulte–Weiss, *Free extensions of chiral polytopes* (1995); the universal
alternating construction is Monson–Schulte (2012,2021), in the exact forms
stated in §8. These prior proofs are retained rather than included as additional
compressed sources. The regular-polytope and marked-cover correspondences are
the standard McMullen–Schulte framework, with the scopes stated in §1.
