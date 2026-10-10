# Primitive saturation and parabolic lower-central kernels

10 October 2026. Private proposed common theorem joining the Frattini
coordinate branch of Compress_A_v2 to the forest-quotient and deletion
constructions of Compress_B. This is a theorem with explicit corollaries,
not a claim that the two manuscripts have already become one replacement.
It does not replace the symmetric-group classification or give deletion
endomorphisms for tree transpositions. No priority or new source credit is
claimed. Independent review is pending.

The principal bridge is canonical: an irredundant marking of a finite
p-group determines a unique primitive coarsening of every omission
action. For two-group forest markings its fibers split exactly into
third-lower-central fibers and one coordinate for each incident diagram
edge. The restrictions of both kernels to every parabolic are proved,
not presumed. For the prescribed-square-section groups this gives all
face and residue indices by one local formula.

## 1. A universal primitive saturation theorem

Let \(P\) be a finite p-group with an ordered irredundant generating
family \((r_i:i\in V)\), where \(|V|=d\). Write
\(P_I=\langle r_i:i\in I\rangle\), \(F=\Phi(P)\), and
\(\pi:P\to P/F\). Burnside's basis theorem says that
\(P/F\cong\mathbb F_p^d\), with basis \(\bar r_i\).
There is no IP hypothesis in the next theorem and the generators need
not have order p.

**Theorem 1 (primitive saturation).** For every \(I\subseteq V\),
\[
 \Phi(P_I)=P_I\cap F,\qquad
 \widehat P_I:=P_IF
   =\pi^{-1}\bigl(\operatorname{span}(\bar r_i:i\in I)\bigr).
                                                               \tag{1.1}
\]
The groups \(\widehat P_I\) are normal, with
\[
 \widehat P_I\cap\widehat P_J=\widehat P_{I\cap J},\qquad
 [P:\widehat P_I]=p^{d-|I|}.                              \tag{1.2}
\]
Each omission subgroup \(H_i=P_{V\setminus\{i\}}\) has a **unique**
maximal overgroup in \(P\), namely
\(M_i=H_iF\), of index p. Thus the \(M_i\) give the unique family of
primitive coset actions obtained by enlarging the respective \(H_i\)
to proper subgroups. Their typed coset geometry is the complete
d-partite geometry with p elements of each type. Its action kernel is
\(F\), and its faithful group \(P/F\) acts regularly on its
\(p^d\) chambers.

The maps \(gH_i\mapsto gM_i\) preserve incidence and send the orbit
of common-point chambers onto all coordinate chambers. Their exact
type-i fiber size is
\[
 [M_i:H_i]=[F:\Phi(H_i)].                              \tag{1.3}
\]
If \(B=\bigcap_iH_i\), each coordinate chamber has
\([F:F\cap B]\) common-point chambers above it. If the original coset
system has the typed Helly property, these are all its chambers.

**Proof.** The quotient of \(P_I\) in \(P/F\) has dimension \(|I|\),
because it is spanned by that subset of a basis. Its kernel is
\(P_I\cap F\), and it is elementary abelian, so
\(\Phi(P_I)\le P_I\cap F\). On the other hand \(P_I\) is generated
by \(|I|\) elements, and Burnside therefore gives
\(|P_I:\Phi(P_I)|\le p^{|I|}\). The preceding elementary quotient
has exactly that order, so equality forces the first assertion of
(1.1). The preimage assertion and (1.2) follow from coordinate subspaces.

Every maximal subgroup of a finite p-group has index p and contains
\(F\). A maximal subgroup containing \(H_i\) must therefore contain
the preimage of the coordinate hyperplane \(\pi(H_i)\), namely
\(M_i\). That preimage already has index p, giving uniqueness. A
transitive coset action is primitive precisely when its stabilizer is
maximal, so this also proves the stated uniqueness of primitive
coarsenings.

The cosets of \(M_i\) prescribe precisely the i-th coordinate in
\(P/F\). Any assignments to distinct coordinates are consistent and
extend to a full vector. This proves the complete multipartite and
chamber statements. The intersection of the \(M_i\) is \(F\), and all
are normal, giving the action kernel. A type fiber is the set of
\(H_i\)-cosets in one \(M_i\)-coset. The product formula
\(M_i=FH_i\), with \(F\cap H_i=\Phi(H_i)\), gives (1.3).

Common-point chambers of the initial system are parametrized by
\(P/B\): two elements give the same full coset tuple exactly when
their quotient lies in every \(H_i\). Also
\(B\le\bigcap_iM_i=F\). Thus the induced chamber map is
\(P/B\to P/F\), with fiber \([F:B]=[F:F\cap B]\). Every target
chamber lifts by choosing a representative in \(P\). The general
intersection/flag assertion follows because a common point remains a
common point under enlargement; pairwise incidence is preserved even
without the Helly hypothesis. ∎

This is stronger than merely observing that a p-group has a Frattini
quotient: it fixes the unique maximal overgroup of each marked omission,
proves restriction of the Frattini kernel to every parabolic, and gives
the complete fibers. It does not say that an arbitrary intermediate
overgroup of \(H_i\) is normal or that \([H_i,P]\) is a chain.

**Relative form.** Suppose \(B\lhd P\), \(F\le B\), and elements
\(s_1,\ldots,s_r\) generate \(P\) irredundantly relative to \(B\).
Then \(P/B\) is elementary abelian, their images form a basis, and
\[
 \langle B,s_i:i\in I\rangle/B
     =\operatorname{span}(s_iB:i\in I).
                                                               \tag{1.4}
\]
Its omission coset geometry is the complete r-partite p-point geometry.
Indeed generation makes the images span, and any nontrivial linear
relation would violate relative irredundancy. This gives the conclusion
directly, or by applying Theorem 1 to \(P/B\), whose Frattini subgroup
is trivial.

In Compress_A_v2, the normal-subgroup ladder proves \(F\le B\) for a
firm RWPRI geometry. The quotient \(P/F\) being abelian makes such
\(B\) normal. Its relative-generation theorem supplies the strongly
independent relative marking and all parabolic formulas. Equation (1.4)
then gives exactly its finite-p-group coordinate classification, faithful
action and primitive direct-sum conclusion. The ladder and relative
generation are real retained work from that manuscript; Theorem 1 does
not claim to prove them from an arbitrary marking.

## 2. The canonical forest quotient restricts exactly to parabolics

We use the following proved theorem of Compress_B, stated here so the
dependency is precise. If a finite two-group \(G\) is generated by
involutions \((r_i:i\in V)\), has marked IP, and its noncommuting pairs
form a forest \(T\), then
\[
 G/\gamma_3(G)\cong Q_T,
 \quad |Q_T|=2^{|V|+|E(T)|},                              \tag{2.1}
\]
by the marked map. The coordinate model is
\[
 Q_T=\mathbb F_2^V\times\mathbb F_2^{E(T)},\quad
 (v,z)(w,t)=(v+w,z+t+\beta(v,w)),
\]
where an oriented edge e has component
\(\beta_e(v,w)=v_{\mathrm{head}(e)}w_{\mathrm{tail}(e)}\).
Its parabolic on I consists exactly of vertex coordinates supported on
I and edge coordinates supported on edges internal to I. The proof of
(2.1) uses graded support separation across a forest cut and descending
factorization of lower-central layers, with actual IP rather than IP
assumed for intermediate quotients. This is the substantive theorem from
Compress_B being reused, not an unproved claim of the present bridge.

**Theorem 2 (parabolic compatibility of gamma3).** Under these hypotheses,
for every subset I,
\[
 \gamma_3(G)\cap G_I=\gamma_3(G_I).                    \tag{2.2}
\]
Consequently the exact kernel sequence
\[
 1\longrightarrow\gamma_3(G)\longrightarrow
 \Phi(G)=G'\longrightarrow\mathbb F_2^{E(T)}\longrightarrow1
                                                               \tag{2.3}
\]
restricts on every parabolic to
\[
 1\longrightarrow\gamma_3(G_I)\longrightarrow
 \Phi(G_I)=G_I'\longrightarrow
 \mathbb F_2^{E(T[I])}\longrightarrow1.                 \tag{2.4}
\]
Both restrictions are intersections with the global kernels; there is
no assertion of analogous compatibility for every higher lower-central
term.

**Proof.** The subgroup \(G_I\) inherits marked IP, involutory generators,
and the induced forest diagram \(T[I]\). Applying the same forest
quotient theorem to it gives
\[
 |G_I:\gamma_3(G_I)|=2^{|I|+|E(T[I])|}.
\]
The image of \(G_I\) under the global map to \(Q_T\) is exactly its
coordinate parabolic, of the same order. Its kernel is
\(G_I\cap\gamma_3(G)\). Functoriality gives
\(\gamma_3(G_I)\le G_I\cap\gamma_3(G)\); equality of the two finite
indices forces equality of those subgroups. This proves (2.2) without
presuming it in either quotient calculation.

An involution-generated group's abelianization is elementary abelian
of exponent two; hence for a finite two-group \(\Phi(G)=G'\). IP
makes the marking irredundant, and the same holds in every parabolic.
Theorem 1 therefore gives \(\Phi(G_I)=G_I\cap\Phi(G)\). The derived
subgroup of \(Q_T\) is precisely its independent central edge space.
For its I-parabolic it is precisely the internal-edge subspace. Taking
images of the derived subgroups and applying (2.2) proves both exact
sequences and all restriction assertions. ∎

**Corollary 2.1 (exact omission and primitive-collapse indices).** Put
\(H_i=G_{V\setminus\{i\}}\), \(M_i=H_i\Phi(G)\), and write
\(\deg_T(i)\) for the degree of vertex i. Then
\[
 [G:H_i]=2^{1+\deg_T(i)}
       [\gamma_3(G):\gamma_3(H_i)],\qquad
 [M_i:H_i]=2^{\deg_T(i)}
       [\gamma_3(G):\gamma_3(H_i)].                      \tag{2.5}
\]
Every formula holds in every induced parabolic system after replacing
V by S, T by \(T[S]\), and G by \(G_S\). These are also formulas for
actual residues whenever the original geometry has the standard
parabolic residues.

**Proof.** Apply (2.1) to G and \(H_i\), whose induced forest has one
fewer vertex and \(\deg_T(i)\) fewer edges. Divide their orders and
then use \([G:M_i]=2\). The subgroup relation between the two gamma3
groups makes the remaining ratio an actual index. The induced-system statement
has exactly the same hypotheses. ∎

**Corollary 2.2 (complete primitivity profile).** The action of G on
\(G/H_i\) is primitive if and only if i is isolated in T. The same
criterion in \(T[S]\) applies in every parabolic. Thus the coset system
is globally WPRI precisely if T has an isolated vertex; it is PRI
precisely if T has no edges. Whenever it is a geometry with the standard
parabolic residues, it is RWPRI precisely if T has no edges. In that
case \(G=C_2^{|V|}\), and it is exactly the coordinate geometry of
Theorem 1.

**Proof.** If i has a neighbor, (2.5) gives \([G:H_i]\ge4\), so the
omission subgroup is not maximal in a finite two-group. If i is isolated,
\(r_i\) centralizes \(H_i\) and IP makes their intersection trivial,
so \(G=\langle r_i\rangle\times H_i\) and the index is two. This is
primitive. For residual weak primitivity, the endpoints of any edge
give a rank-two induced residue with no isolated vertex, so RWPRI fails.
If there are no edges the marking is independent and commuting, giving
the asserted elementary abelian group and all primitive residues. ∎

The point of this corollary is not to identify RWPRI with IP. It computes
exactly their difference in this family. In particular nondegenerate
two-group string C-groups have no globally primitive face type, despite
their full IP and regular polytope actions.

## 3. The quotient geometry and its independent edge fibers

The canonical reductions factor as
\[
 G\longrightarrow Q_T\longrightarrow\mathbb F_2^V,
\]
with respective kernels \(\gamma_3(G)\) and the independent edge
space. By Theorem 2 the parabolic kernels in the first map are exactly
\(\gamma_3(G_I)\); in the second they are exactly the internal-edge
subspaces. Consequently the type-i map of maximal-parabolic cosets in
the first stage has fiber
\([\gamma_3(G):\gamma_3(H_i)]\), while the second has fiber
\(2^{\deg_T(i)}\). Their product is (2.5). A common-point chamber has
respectively \(|\gamma_3(G)|\) and \(2^{|E(T)|}\) lifts, since IP
makes the full Borel trivial. No quotient is asserted to leave the
original geometry isomorphic unless its kernel lies in the Borel.

For completeness the canonical model's maximal-parabolic cosets have
the typed Helly property, even for an arbitrary graph in place of T.
Here is a proof rather than an inference from IP. Projection onto the
vertex space gives coordinate hyperplane cosets. For any pairwise
intersecting family, choose a common vertex vector and translate by a
lift of it. Each projected coset is now a standard coordinate hyperplane,
so each original coset has a representative in the central edge group Z.
For type i, its intersection with Z is the subspace \(Z_i\) on edges
not incident with i. Thus its central coset specifies exactly the
incident-edge coordinates. If two original cosets meet, a common element
projects into the intersection of their coordinate hyperplanes. Their
parabolic intersection has that full vertex image, by the coordinate
support formula. Multiplying by a suitable element of that intersection
moves a common point into Z. Hence the corresponding central cosets
meet. Pairwise intersection of the \(z_i+Z_i\) says all prescribed
values of each edge coordinate agree; choosing those values produces
one point in every coset. This proves Helly.

Together with the explicit marked IP and parabolic generation, the usual
coset geometry criterion makes \(Q_T\)'s system a regular thin geometry.
For a path it is the regular polytope \(C_d\). If the starting G-system
also has typed Helly (in particular for a string C-group), the two-stage
map is a chamber-surjective map of the actual geometries, with the exact
fiber counts above. For a general forest marking without such a
geometric hypothesis we assert only the coset-system and common-point
chamber statements, avoiding any assumption that IP alone proves Helly.

## 4. Short specialization to the prescribed-square-section groups

Let \(G=G(n_3,\ldots,n_d)\), \(n_j\ge5\), be the group built by
Boolean fiber products of the square-map groups of order \(2^{n_j}\),
with label bags
\(W_j=\{j-3,j-2,j-1\}\), \(3\le j\le d\). Put
\(\alpha_j=n_j-5\). Compress_B proves in its actual tuple construction
that
\[
 \gamma_3(G)=\prod_{j=3}^d K_j,\qquad |K_j|=2^{\alpha_j},
\]
where \(K_j\) is the third lower-central subgroup of the j-th seed,
occupying only its own tuple coordinate. This is a direct product of
groups; it does not assert independence of the two squared translations
inside a single diagonal seed.

**Corollary 4.1 (all parabolic kernels and face indices).** For any subset S,
\[
 \gamma_3(G_S)=\prod_{W_j\subseteq S}K_j,
 \quad |G_S|=2^{\,|S|+|E(T[S])|+
                         \sum_{W_j\subseteq S}\alpha_j},       \tag{4.1}
\]
where T is the path on \(0,\ldots,d-1\). For \(i\in S\),
\[
 [G_S:G_{S\setminus\{i\}}]
 =2^{1+\deg_{T[S]}(i)+
             \sum_{W_j\subseteq S,\ i\in W_j}\alpha_j}.       \tag{4.2}
\]
In particular the number of rank-i faces in the full regular polytope is
\[
 f_i=2^{1+\deg_T(i)+\sum_{j:\ i\in W_j}(n_j-5)}.         \tag{4.3}
\]
Its type-i collapse to the primitive coordinate geometry has half this
fiber size, and its two stages have factors
\(2^{\sum_{j:i\in W_j}(n_j-5)}\) and \(2^{\deg_T(i)}\).

**Proof.** If \(W_j\subseteq S\), the entire embedded triple lies in
\(G_S\), so \(K_j\le\gamma_3(G_S)\). If the bag is not contained
in S, its coordinate image of \(G_S\) is generated by at most two
local markers, a group of class at most two. Its image of
\(\gamma_3(G_S)\) is therefore trivial. Since the global gamma3 group
is the stated coordinate product, these two facts prove the first
formula, including its trivial factors. Apply the forest quotient theorem
to \(G_S\) to obtain its order, and divide for (4.2). Face stabilizers
in the regular-polytope correspondence are the omission parabolics, so
(4.3) follows. The primitive target has two elements of each type,
giving the last assertions. ∎

For example the endpoint face counts reduce immediately to
\(f_0=2^{n_3-3}\) and \(f_{d-1}=2^{n_d-3}\). An interior type depends
on at most three consecutive seed parameters. In the smallest case
all \(n_j=5\), the endpoint counts are four and all interior counts
are eight. Every residue is handled by the same subset formula (4.2),
including disconnected induced subpaths. These are genuine short
corollaries of the common kernel theorem; they do not import another
face-enumeration result from F016.

## 5. What this does and does not combine

Theorem 1 supplies the canonical coordinate geometry that appears in
the finite-p-group Frattini branch of Compress_A_v2. Theorem 2 and
Corollary 2.1 refine that same saturation through the class-two quotient
proved in Compress_B. Corollary 4.1 gives explicit family and residue
data by substituting the independently proved tuple kernels. The
intermediate quotient, its exact parabolic restrictions and the
primitivity obstruction are common mathematical consequences, not a
shared vocabulary imposed on unrelated proofs.

This joins the **Frattini branch** of A to B. It does not subsume A's
symmetric-group forest theorem, extremal-marking classification or its
Whiston-dependent completeness proof. Adjacent tree transpositions in
\(S_n\) satisfy \((\tau_e\tau_f)^3=1\); deleting one but retaining
the other would send that relation to a nontrivial transposition.
Therefore those markings generally have no Boolean deletion maps.
Their IP comes from component partitions and unique paths, and their
flag completion comes from laminar sets. Those arguments remain
charged if a future combined manuscript is attempted.

The retained inputs here are Burnside's theorem, elementary finite
p-group maximal-subgroup facts, the already proved forest quotient
theorem with its explicit coordinate model, the already proved tuple
kernel factorization for the final parameter corollary, and the stated
standard coset/polytope correspondences. No additional four-paper
completion claim, numerator admission or compression factor follows
from this proposal alone.
