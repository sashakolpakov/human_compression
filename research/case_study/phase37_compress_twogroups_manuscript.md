# Quotients, deletion maps and cyclic cores of marked two-groups

**Compress_B, private integrated manuscript, 10 October 2026.** This is a new
standalone replacement draft for the declared main-result contracts of L032,
L035, F013 and F016. It is not a claim that four entire papers, their cited
background, or all their auxiliary assertions have been replaced. N009 and its
order-1024 census are excluded. No manuscript-length factor or priority claim
is assigned. The companion ledger fixes source versions and dependencies.

The common core has three operations: transport intersections through an
explicit kernel; construct compatible marked groups by deletion maps; and
separate supports in a lower-central graded Lie ring. The same square-lattice
seed supplies arbitrary-order existence, bounded rank-three quotients, and
prescribed local sections. The high-type classification needs an additional
bounded cyclic-extension calculation and a finite census, both charged below.
The universal infinite extensions need retained geometric identifications;
their torsion argument is proved here. These are genuine extra costs, not
consequences of merely renaming a group as a kernel or a core.

## 1. Conventions, target contract and retained background

For a group marked by involutions \(r_i\), \(i\in V\), write
\(G_I=\langle r_i:i\in I\rangle\). Its intersection property (IP) is
\(G_I\cap G_J=G_{I\cap J}\) for all subsets. A string C-group has IP and
\([r_i,r_j]=1\) when \(|i-j|>1\); it is nondegenerate if consecutive
generators do not commute. Its type records their product orders. All marked
isomorphisms preserve the ordered generators. Write
\([x,y]=x^{-1}y^{-1}xy\), \(x^y=y^{-1}xy\), and \(D_8\) for the dihedral
group of order eight. The lower central series is \(\gamma_j(G)\).

The precise numbered targets are:

* **L032, Theorem 1.2:** for \(d\ge3\), \(n\ge5\), \(k_i\ge2\), and
  \(\sum_{i=1}^{d-1}k_i\le n-1\), existence of a string C-group of order
  \(2^n\) and type \(\{2^{k_1},\ldots,2^{k_{d-1}}\}\).
* **L035, Theorem 1.2:** the rank-three assertion above for \(n\ge10\).
  **Theorem 1.3:** for \(n\ge10\), complete classification of the marked
  order-\(2^n\) string C-groups of types \(\{4,2^{n-3}\}\),
  \(\{4,2^{n-4}\}\), \(\{4,2^{n-5}\}\), including recognition of all
  eight displayed presentations, not just construction of quotients of them.
* **F013, Theorems 1.1 and 1.2:** every finite nondegenerate rank-\(d\)
  two-group string C-group, \(d\ge2\), maps by its marking onto Conder's
  group of order \(2^{2d-1}\); equivalently the regular polytope covers the
  corresponding \(C_d\). The specified auxiliary Frattini kernel in that
  source is not imported and is corrected in §10.
* **F016, Theorem 5.1(a–d):** for \(d\ge3\), \(n_3,\ldots,n_d\ge5\), a
  finite regular \(d\)-polytope whose consecutive rank-three sections are
  the unique regular square maps \(\{4,4\}_{(n_j)}\) of order \(2^{n_j}\),
  whose group has order \(2^{\sum n_j-3(d-3)}\), which is
  \((d-4,d-1)\)-flat (hence flat) for \(d\ge4\), and has the flat
  amalgamation property (FAP) for co-\((d-4)\)-faces, co-\((d-3)\)-faces,
  and facets. **Theorem 5.3:** the constructed group is the universal group
  with these local sections, modulo
  \([ (r_i r_{i+1})^2,(r_{i+2}r_{i+3})^2]=1\), \(0\le i\le d-4\).
  **Theorem 6.1(a–b):** for \(d\ge4\), \(n_3,\ldots,n_{d-1},m_{d-1}\ge5\),
  an alternating semiregular \(d\)-polytope with the two regular facet types
  \((n_3,\ldots,n_{d-2},n_{d-1})\) and
  \((n_3,\ldots,n_{d-2},m_{d-1})\), and group order
  \(2^{\sum_{j=3}^{d-2}n_j+n_{d-1}+m_{d-1}-3(d-3)}\), doubled precisely
  when \(n_{d-1}=m_{d-1}\). At \(d=4\) the common facet of those facets is
  a square and the shared list is empty. **Theorems 7.1–7.3:** respectively
  the free regular extension, the free extension of an *oriented chiral*
  polytope with *directly regular facets*, and the universal alternating
  semiregular extension of two regular polytopes with isomorphic facets,
  have infinite two-groups when the input automorphism groups are finite
  or infinite two-groups. These extension targets retain the source's
  standing input rank \(d\ge3\). Here “infinite two-group” means finitely generated,
  infinite, with every finite-order element of two-power order; it does not
  mean a torsion group.

We retain the regular-polytope/string-C-group correspondence, its marked
quotient/covering correspondence, and its coset face/stabilizer description.
We also retain Burnside's basis theorem, finite nilpotency of finite
two-groups, the lower-central graded Lie construction and generation in
degree one, and the Euclidean algorithm for Gaussian integers. The cyclic
core bound retained in §6 is stated there exactly. The geometric alternating
assembly and free-extension theorems retained in §9 are also stated exactly.
The amalgam normal-form theorem and completeness of the SmallGroups
order-256 catalogue are retained. The **relation-pattern census derived
from that catalogue** is a separately charged finite verification, not
another unnamed classification assumption. No main target from the four
source papers is accepted as background.

## 2. A common kernel and deletion calculus

**Lemma 2.1 (kernel transport).** Let \(\pi:H\twoheadrightarrow B\) preserve
markings and let \(B\) have IP. Put \(K=\ker\pi\) and \(K_I=K\cap H_I\).
Then \(H\) has IP if and only if
\(K_I\cap K_J=K_{I\cap J}\) for all \(I,J\).

**Proof.** Necessity follows by intersection with \(K\). If
\(x\in H_I\cap H_J\), its image is in \(B_{I\cap J}\), so choose
\(y\in H_{I\cap J}\) with \(\pi y=\pi x\). Then
\(xy^{-1}\in K_I\cap K_J=K_{I\cap J}\), and \(x\in H_{I\cap J}\). ∎

**Lemma 2.2 (Boolean deletion).** Suppose every assignment
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

**Theorem 2.3 (compatible products).** Let \(A,B\) have Boolean deletions,
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
generate each kernel, by Lemma 2.2. They generate the displayed semidirect
product. Coordinatewise deletion preserves compatibility: both separator
images are deleted on exactly \(S\cap I\). Lemma 2.2 gives IP, and the
sections, order formula and commutation assertions are immediate. ∎

We will also use a non-split variant with cyclic kernels. Let \(B\) have
IP and retractions to chosen two-generator subgroups
\(B_e=\langle b_i,b_j\rangle\), killing all other markers. Suppose
\(q_e=|b_ib_j|\) is even. For each chosen pair choose a multiple \(m_e\)
and a dihedral group \(D_e=\langle u_e,v_e\rangle\) of order \(2m_e\),
mapping by its reflections to \(B_e\). Form the simultaneous fiber product
of \(B\) and the \(D_e\) over these maps, with the evident marked tuples.

**Theorem 2.4 (independent edge inflation).** These tuples generate the
whole fiber product \(H\), with
\[
 |H|=|B|\prod_e(m_e/q_e),\qquad
 K=\ker(H\to B)=\prod_e C_{m_e/q_e},\qquad
 K\cap H_I=\prod_{e\subseteq I}C_{m_e/q_e}.                 \tag{2.1}
\]
It has IP. Chosen pair orders become \(m_e\), and all other pair orders
remain their base values. Thus string diagrams give string C-groups.

**Proof.** The word \((r_i r_j)^{q_e}\) is a generator of the \(e\)-kernel
and trivial in every other coordinate: another chosen pair contains at
most one of its endpoints, so evenness kills that reflection. These words
generate the entire kernel, while the tuples project onto \(B\). The
same word lies in \(H_I\) when \(e\subseteq I\). Otherwise its coordinate
in \(H_I\) is at most a single reflection subgroup and meets the rotation
kernel trivially. This proves (2.1); its coordinate intersection law and
Lemma 2.1 prove IP. For an unchosen pair, a coordinate projection is a
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

## 3. One square-lattice seed, its quotient and its uniqueness

Let
\[
 a(x,y)=(-x,y),\quad b(x,y)=(y,x),\quad c(x,y)=(x,1-y).
\]
These generate \(W=\mathbb Z^2\rtimes D_8\), of type \(\{4,4\}\), with
\(ac=ca\). Its presentation is
\[
 W=\langle a,b,c\mid a^2=b^2=c^2=(ab)^4=(bc)^4=(ac)^2=1\rangle. \tag{3.1}
\]
Here is an algebraic normal-form proof. Put \(d=bab\), \(y_0=cd\), and
\(x_0=by_0b\). The relations give \([a,d]=1\), \([a,y_0]=1\),
\(dy_0d=y_0^{-1}\), \(ax_0a=x_0^{-1}\), and conjugation by \(b\) swaps
\(x_0,y_0\). Substitution of \(bc=x_0ab\) makes \((bc)^4=1\) equivalent
to \([x_0,y_0]=1\). Thus every word collects to \(x_0^u y_0^v M\),
\(M\in\langle a,b\rangle=D_8\). In the affine model \(x_0,y_0\) are the
unit translations, so these forms are distinct. This proves (3.1).

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
also survive. Thus \(H_n\) has Boolean deletions and IP by Lemma 2.2.

Moreover,
\[
 \gamma_3(W)=2\mathbb Z^2,
 \qquad \gamma_3(H_n)=2\mathbb Z^2/\Lambda_n,
 \qquad |\gamma_3(H_n)|=2^{n-5}.                         \tag{3.2}
\]
Indeed reduction modulo \(2\mathbb Z^2\) makes the adjacent squares
central; conversely \([[a,b],c]\) and \([[b,c],a]\) give the two doubled
unit translations, up to signs. Thus \(H_5\) is class two of order 32.
The squared translations are not always independent cyclic subgroups:
in \(H_6\) they coincide and have order two. Formula (3.2) uses a lattice
index and does not make the false independence assertion.

**Lemma 3.1 (square-map recognition).** Every finite two-group string
C-group of type \(\{4,4\}\) and order \(2^n\) is marked-isomorphic to
\(H_n\); necessarily \(n\ge5\).

**Proof.** The two dihedral parabolics have orders eight and intersect in
order two, so their product already has 32 elements. The universal group
(3.1) maps onto the given group. Burnside's theorem gives elementary
abelianization of rank three: involutory generators make the abelianization
elementary, and IP makes the marking irredundant. Hence word parity is a
homomorphism onto \(C_2\), and the kernel of (3.1) lies in the subgroup
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

## 4. Every allowed rank, order and type

**Corollary 4.1 (L032 1.2 and L035 1.2).** The existence targets in §1
hold.

**Proof.** Put \(\delta=n-1-\sum_i k_i\ge0\) and use the Boolean seed
\(B=C_2^{d-3}\times H_{\delta+5}\), with the independent \(C_2\)
markers first. Its consecutive orders are two until the last two, which
are four. Inflate consecutive pair \(i\) to \(2^{k_i}\) by Theorem 2.4.
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
\(2^{t-2}\). Modulo their product one obtains (3.1). In its affine model
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

## 5. A canonical class-two quotient from graded support

**Lemma 5.1 (descending lift).** Let \(G\) be finite nilpotent and let
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

**Lemma 5.2 (graded support).** Let a positively graded Lie algebra be
generated in degree one by disjoint sets \(X,Y\), with subalgebras
\(L_X,L_Y\). If \([x,y]\in L_Y\) for \(x\in X,y\in Y\), then
\(L=L_X+L_Y\), degree by degree.

**Proof.** The derivation \(\operatorname{ad}x\) preserves \(L_Y\)
because it does so on its generators. Iterated brackets of those
derivations also preserve \(L_Y\), by Jacobi. Hence
\([L_X,L_Y]\subseteq L_Y\), and \(L_X+L_Y\) is a Lie subalgebra
containing all generators. The argument holds in characteristic two. ∎

**Theorem 5.3 (forest quotient).** Suppose \(G\) is a finite two-group
with marked IP, and its noncommuting pairs form a forest \(T\) on
\(d\) vertices and \(m\) edges. Then edge commutators are independent
in \(G'/\gamma_3(G)\), and \(G/\gamma_3(G)\) is the marked group
\[
 (v,z)(w,t)=(v+w,z+t+\beta(v,w)),\quad
 v,w\in\mathbb F_2^d,\ z,t\in\mathbb F_2^m,               \tag{5.1}
\]
where, after orienting each edge, its component of \(\beta\) is
\(v_{\rm head}w_{\rm tail}\). Its order is \(2^{d+m}\).

**Proof.** IP gives irredundancy, so Burnside gives
\(G/G'=C_2^d\) and \(G'\cap\langle r_i\rangle=1\).
The lower-central graded Lie ring is generated by these degree-one
elements; all its graded components are \(\mathbb F_2\)-spaces by
bilinearity. Edge commutators span degree two. If they satisfy a nonzero
linear relation, root each forest component and choose a participating
edge whose child endpoint has maximal depth in its component. Removing
it separates the descendant set \(X\) from all other vertices \(Y\),
and no other participating edge is internal to \(X\). The relation
therefore writes the only nonzero cross bracket as a sum of brackets
internal to \(Y\). Lemma 5.2 shows every graded component is generated
by pure \(X\)- and pure \(Y\)-brackets. Their representatives lie in
\(G_X\cap\gamma_j(G)\) and \(G_Y\cap\gamma_j(G)\).

Actual IP gives \(G_X\cap G_Y=1\), so Lemma 5.1 gives
\(G'=(G'\cap G_X)(G'\cap G_Y)\). For the crossing endpoints
\(x\in X,y\in Y\), write \([r_x,r_y]=uv\) accordingly. Then
\(u\in G_X\cap G_{\{x\}\cup Y}=\langle r_x\rangle\), whence
\(u=1\); next \([r_x,r_y]\in G_Y\cap G_{\{x,y\}}=\langle r_y\rangle\),
so it too is one. This contradicts that the edge is noncommuting.
Independence follows.

Bilinearity makes (5.1) associative; its coordinate markers are
involutions with independent central edge commutators. It is generated
by those markers, and its parabolic on \(I\) consists exactly of vertex
coordinates supported on \(I\) and edge coordinates supported on edges
internal to \(I\). Thus it has IP. Collection in the corresponding
class-two presentation gives at most \(2^{d+m}\) elements, and this
coordinate model attains the bound. Independence in \(G'/\gamma_3(G)\)
gives the same order for \(G/\gamma_3(G)\); hence the marked map is an
isomorphism. ∎

**Corollary 5.4 (F013 1.1–1.2).** For every finite nondegenerate two-group
string C-group of rank \(d\ge2\),
\(G/\gamma_3(G)\cong G(C_d)\), of order \(2^{2d-1}\); the associated
polytope covers \(C_d\).

**Proof.** Its diagram is a path, so \(m=d-1\). Conder's marked
presentation has involutions, distant commutation, adjacent order four,
and adjacent squares central. The model (5.1) realizes that presentation
with the maximal collected order, identifying it with \(G(C_d)\).
The retained marked covering correspondence gives the geometric assertion.
This also proves uniqueness of the minimal object in the declared finite
nondegenerate class. ∎

Notice that no intermediate quotient was assumed to retain IP. Lemma 5.1
is the step that prevents that circular assumption.

## 6. Bounded cyclic cores and their binary extension models

We now prove the additional classification needed by L035. This section is
source-specific work, sharing its square quotient and kernel transport with
the earlier construction; its length must remain in the replacement.

The retained **cyclic core theorem of Lucchini** says: if a cyclic proper
subgroup \(M\) of a finite group \(H\) has core \(K\), then
\(|M:K|<|H:M|\). Here \(K\) is the largest normal subgroup of \(H\)
contained in \(M\). We use the form recorded in Isaacs, *Finite Group
Theory*, Theorem 2.20, also stated as L035 Proposition 2.9.

**Theorem 6.1 (bounded cyclic quotient).** Let \((G;a,b,c)\) be a
rank-three string C-group of order \(2^{t+s}\), type \(\{4,2^t\}\),
with \(s\ge3\) and \(t\ge s-2\). Put
\[
 r=bc,\quad m=2^t,\quad d_0=(ab)^2,\quad
 A=\langle r^{2^{s-2}}\rangle.
\]
Then \(A\lhd G\), and \(G/A\) is a string C-group of order
\(2^{2s-2}\) and type \(\{4,2^{s-2}\}\).

**Proof.** The even-word subgroup \(H=\langle ab,bc\rangle\) has
index at most two. Burnside and IP give \(G/G'=C_2^3\), where its image
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
 r^a=d_0r,\quad d_0^a=d_0,\quad r^c=r^{-1},\quad d_0^c=d_0^r       \tag{6.1}
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
 (u+u',v+v',w+w',e+e'+\beta(vu'+wv')).                    \tag{6.2}
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
 N=(D\rtimes\langle r\rangle)/\langle zr^{-m/2}\rangle.       \tag{6.3}
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
form (6.3) gives \(d_0\notin\langle r\rangle\), leaving exactly
\(\langle b\rangle\). The three generators are independent (already
\(a\notin\langle b,c\rangle\), and the pair orders exclude the others),
so this proves rank-three IP. Direct substitution yields
\[
 \begin{array}{ll}
 s=3:&[d_0,c]=z^\epsilon,\\
 s=4:&[d_0,r^2]=z^\epsilon,\\
 s=5:&[a,r^2]^2=z^\beta,\qquad[a,r^4]=z^\nu.
 \end{array}                                                   \tag{6.4}
\]
They are invariant words of the ordered marking and distinguish the two,
two and four models within their branches.

## 7. Completeness and exact recognition of all eight presentations

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

**Theorem 7.1 (high-type completeness).** Every group in the three
classes of L035 Theorem 1.3 is exactly one of the marked models of §6;
each displayed source presentation defines that model.

**Proof, first branch.** For \(s=3\), Theorem 6.1 gives a quotient of
type \(\{4,2\}\) and order sixteen, necessarily \(D_8\times C_2\).
Thus \(h=[d_0,r]\in A=\langle r^2\rangle\). Since it commutes with
\(r\), and \(d_0\) centralizes \(A\),
\(h^2=[d_0,r^2]=1\). Hence \(h=1\) or \(z\), and (6.1) makes this
exactly \([d_0,c]=z^\epsilon\). The conjugates of \(d_0\) obey
\(d_1=d_0z^\epsilon\); (6.1) forces all the first model's actions and
normal forms. The resulting surjection from that model onto the actual
group is between groups of the same order, hence an isomorphism.

**Second branch.** For \(s=4\), the quotient of order 64 and type
\(\{4,4\}\) is \(H_6\), by Lemma 3.1. In that affine quotient
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

**Third-branch lifts.** For \(s=5\), Theorem 6.1 gives
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
Let \(N=\langle d_0,r\rangle\). Equations (6.1) make it normal, with
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
the table in §6, and (6.1) forces the actions of the commuting complement
\(\langle a,c\rangle\). The model maps onto \(G\) and has its order
\(32m\), so is isomorphic. This proves completeness of the eight models.

It remains to recognize the **bare presentations**, where the target
order cannot yet be assumed. Let \(P\) be one of them and
\(z=r^{m/2}\), initially of order at most two. For \(G_1,G_2\), if
\(\epsilon=1\), \(a\) centralizes \(z=[d_0,c]\) since it centralizes
\(d_0,c\); \(b,c\) centralize it since they invert \(r\). If
\(\epsilon=0\), \(d_0\) is central; (6.1) and the evenness of \(m/2\)
then make \(z\) central too. Collection gives at most \(8m\) normal
forms, attained by the first model.

For \(G_3,G_4\), \(d_2=d_0z^\epsilon\). If \(\epsilon=0\), applying
\(a\) as in the second-branch argument gives \([d_0,d_1]=1\), after
which the model relations and centrality of \(z\) follow. If
\(\epsilon=1\), \([d_0,r^2]=z\) implies that conjugation by \(d_0\)
inverts \(z\); as \(z^2=1\), it centralizes \(z\). Thus \(z\)
commutes with \(r\) and all \(d_i\). Write \(j=[d_0,d_1]\).
Applying \(a\) to the equation for \(d_2\), and using (6.1), gives
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

## 8. Prescribed square sections and their complete presentation

For \(d\ge3\) and \(n_3,\ldots,n_d\ge5\), place \(H_{n_{i+3}}\)
on the label bag \(\{i,i+1,i+2\}\), \(0\le i\le d-3\). Glue the
successive bags over their shared \(D_8\) using Theorem 2.3. At each
step the previous group and the new seed embed, with their given
markings. Thus all adjacent orders remain four, distant markers
commute, every deletion exists, and the group \(G(n_3,\ldots,n_d)\)
has IP. Its exact order is
\[
 |G(n_3,\ldots,n_d)|
 =\frac{\prod_{j=3}^d2^{n_j}}{8^{d-3}}
 =2^{\sum_{j=3}^d n_j-3(d-3)}.                           \tag{8.1}
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
 G/\gamma_3(G)=G(C_d).                                  \tag{8.2}
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
with \(\gamma_3(G)\), and (8.1) gives the canonical quotient order.
Thus (8.2) is one construction meeting the bound in Theorem 5.3 at every
rank, rather than an unrelated counting trick.

We next prove that this construction has the exact additional presentation
claimed in **F016 Theorem 5.3**. The only extra identity needed is local.

**Lemma 8.1 (four-marker centralization).** Suppose \(a,b,c,d\) are
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
\(P_0\), and Lemma 2.2 proves its IP without assuming finiteness. The
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
 \quad(0\le i\le d-4).                                  \tag{8.3}
\]
The constructed group satisfies these relations. For (8.3), no tuple
coordinate contains both disjoint edges; the edge missing one endpoint
has square one in that coordinate. Hence \(Q\twoheadrightarrow G\).
Each triple embeds in \(Q\), since its map onward to the embedded
triple in \(G\) is injective. Its third lower-central subgroup \(K_i\)
is generated by its two squared translations and has order
\(2^{n_{i+3}-5}\), by (3.2). Lemma 8.1 and its reversed version show
that the nearest outside markers centralize \(K_i\), while the farther
markers do so by string commutation. Thus every \(K_i\lhd Q\).
Their product \(K\) is finite of order at most
\(2^{\sum_j(n_j-5)}\). Modulo it all triples are class two; the same
local-to-global centralization argument used for (8.2) makes \(Q/K\)
class two. Collecting markers and central edge commutators gives
\( |Q/K|\le2^{2d-1}\). Therefore
\[
 |Q|\le2^{\sum_j(n_j-5)+2d-1}
      =2^{\sum_j n_j-3(d-3)}=|G|.
\]
The order comparison principle identifies \(Q=G\) as marked groups.
Since \(P_0\) is the universal type group just constructed, this is
exactly its quotient by (8.3). The finite group presentation, the
universal group and both intersection properties have all been proved
using the same deletion calculus.

## 9. Branched products and infinite extensions

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

Apply §8 to the two lists
\((n_3,\ldots,n_{d-2},n_{d-1})\) and
\((n_3,\ldots,n_{d-2},m_{d-1})\). Their common facet \(K\) has list
\((n_3,\ldots,n_{d-2})\), or is the square if \(d=4\). Theorem 2.3
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

**Lemma 9.1 (torsion and amalgams).** Let “two-primary torsion” mean that
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
All factors are finitely generated by their finite marked sets. Lemma 9.1
and, when needed, its finite-extension clause prove exactly **F016
Theorems 7.1, 7.2 and 7.3**, including infinite input groups. No assertion
that all elements have finite order is made.

## 10. Corrections, exclusions and the boundary of the result

The F013 common-quotient theorem is recovered by a different kernel. Its
specified auxiliary subgroup is false in general. We include the proof
of the correction so that no false historical claim is counted as a
corollary of this manuscript.

In the path model (5.1), name the central edge coordinates
\(c_1,\ldots,c_{d-1}\), and put
\[
 \sigma_i=r_{i-1}r_i,\quad
 A_i=\langle\sigma_1,\ldots,\sigma_{i-1},\sigma_i^2,
                  \sigma_{i+1},\ldots,\sigma_{d-1}\rangle,
 \quad C=\bigcap_i\Phi(A_i).                              \tag{10.1}
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
 \quad(d\ge3).                                          \tag{10.2}
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
so their orders cannot be multiplied as in its page-11 argument; (3.2)
uses the correct lattice index. In its chiral extension proof the full
facet automorphism group need not embed in the chiral group; §9 only
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
semiregular geometry have real costs. Admission of all four manuscripts
to any length numerator requires independent review of this assembled
text and the bound finite certificate, not merely historical reviews of
separate ingredients. No four-paper completion or compression ratio is
certified by the present author draft.

## Appendix A. The finite completeness calculation, fully specified

The following GAP algorithm is part of the proof cost in §7. The only
classification supplied to it is the complete catalogue of groups of
order 256. All arithmetic, Frattini groups, conjugacy classes,
centralizers and intersections are exact finite group operations.

```gap
ids := IdsOfAllSmallGroups(256, AbelianInvariants, [[2,2,2]]);
counts := [0,0,0,0]; total := 0; active := 0;
for id in ids do
  g := SmallGroup(id); phi := FrattiniSubgroup(g);
  hom := NaturalHomomorphismByNormalSubgroup(g,phi);
  rs := Filtered(List(ConjugacyClasses(g),Representative),
                 x -> Order(x)=8 and not x in phi);
  if Length(rs)=0 then continue; fi;
  active := active+1;
  invs := Filtered(Elements(g),x -> Order(x)=2);
  for r in rs do
    candidates := Set(Filtered(invs,c -> r^c=r^-1 and
      not Image(hom,c) in Group(Image(hom,r))));
    cr := Elements(Centralizer(g,r));
    while Length(candidates)>0 do
      c := candidates[1];
      candidates := Difference(candidates,Set(cr,x -> c^x));
      b := r*c;
      plane := Group(Image(hom,r),Image(hom,c));
      aas := Filtered(invs,a -> not Image(hom,a) in plane and
                      a*c=c*a and Order(a*b)=4);
      for a in aas do
        if Size(Intersection(Group(a,b),Group(b,c)))<>2 then
          continue;
        fi;
        total := total+1; d0 := (a*b)^2; z := r^4;
        matches := [];
        if Comm(a,r^2)^2=One(g) and Comm(a,r^4)=One(g) then
          Add(matches,1); fi;
        if Comm(a,r^2)^2=z and Comm(a,r^4)=One(g) then
          Add(matches,2); fi;
        if Comm(d0,r^2)=z then Add(matches,3); fi;
        if Comm((r^2)^a,r)=z then Add(matches,4); fi;
        if Length(matches)<>1 then Error("pattern failure"); fi;
        counts[matches[1]] := counts[matches[1]]+1;
      od;
    od;
  od;
od;
Assert(0,Length(ids)=1651 and active=1641 and total=92);
Assert(0,counts=[64,4,16,8]);
```

The excluded catalogue groups cannot have the required marking by
Burnside. For the included groups, \(r,c,a\) pass a basis test in the
Frattini quotient, and \(a,b,c\) are recovered by the invertible change
\(b=rc\); generation follows. The normalizations by conjugation never
lose a word relation or parabolic-intersection outcome. Conversely any
admissible marking normalizes to one examined in the loops. Each row's
identifiers in §7 are recorded by the executable version accompanying
the ledger; only the exhaustive relation implications, not those
identifiers or anchored multiplicities, enter the infinite-parameter
proof. Source and output hashes, runtime versions and fresh-run status
belong to the ledger. No computation of groups above order 256 is used
in the completeness argument.

