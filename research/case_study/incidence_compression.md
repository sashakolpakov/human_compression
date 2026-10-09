# Incidence results derived from relation matrices

This is a second-stage reduction, not merely a common vocabulary. It derives
the designated-action version of the principal theorem of L029, the criterion of L008, the principal construction
and parameters of L030, and substantial geometric results of L009 from a small
set of explicit relation calculations. The classification theorem in L009 and
the code distances in L050 are not claimed as consequences. See the final table
for the remaining inputs. All references below are to the local catalogue IDs.

## 1. Audit and extension of the torsor theorem

The subgroup/partition bijection, Hadamard intersection, ordinary product
`A_H A_K=|H∩K| A_(HK)`, typed coset Helly criterion, and regular-case residual
generation criterion in [torsor_matrix_theory.md](torsor_matrix_theory.md) are
correct. In the residue statement, flag transitivity is essential: it makes the
internal parabolic coset model an incidence isomorphism. With only transitivity
on proper flags, it is still a bijection on vertices and preserves edges, but may
miss edges. Those missing edges are exactly what the chiral rank-two argument
below needs. Also, when the common stabilizer B is nontrivial, permutations inside
a B-coset are invisible on the geometry; the original torsor and the chamber set
must not be identified.

Here is the useful extension. Use left cosets, put H_J=∩_(j∈J)H_j, and suppose
G is transitive on flags of type J. The possible vertices of type k incident with
the base J-flag are the cosets xH_k with

    x ∈ S_(J,k) := ∩_(j∈J) H_j H_k.

The H_J-orbits on this fiber, hence the G-orbits on flags of type J∪{k}, are

    H_J \ S_(J,k) / H_k.                         (F)

This follows by normalizing the J-part of a flag; two normalized extensions are
equivalent exactly when an element stabilizing the J-part maps one to the other.
It proves the arbitrary-orbit-count version of L008 Theorem3.2, not just its
two-orbit special case. If H_J=1, the number of orbits is |S_(J,k)|/|H_k|, and
every normalized extension has trivial stabilizer. In matrix terms, S_(J,k) is
the intersection of the supports of A_(H_j)A_(H_k). Thus a product/intersection
calculation directly counts chamber orbits; no incidence graph need be built.

## 2. A short reduction of the designated-action version of L029

Let I have r≥3 elements, α_0=1, a_ij=α_i^(-1)α_j, and

    P_S=⟨a_ij : i,j∈S⟩,  H_i=P_(I\{i}).

Assume the C+-intersection property. Repeated intersections give
H_J=P_(I\J); in particular H_J=1 when |J|=r−1. This also shows that condition(ii)
of L008 Theorem1.1 is automatic for a C+-group of rank at least three.

**Proper-flag criterion.** If the associated coset system is a geometry and G
is transitive on every proper flag type, it is residually connected.

Proof: normalize a proper flag of type J. Transitivity on J∪{i} implies that the
vertices in its residue are H_J/(H_J∩H_i). The internal coset incidence graph
is a spanning subgraph. If |I\J|≥3, its defining subgroups
P_((I\J)\{i}) generate P_(I\J): each generator a_uv belongs to one of them,
choosing i different from u,v. The Boolean-closure criterion connects the residue.

If I\J={u,v}, the parabolic is H=⟨a_uv⟩, and the two vertex stabilizers are
trivial. The residue therefore has two copies of H as vertex sets. It contains
both matching edge sets

    h_left — h_right,       h_left — (h a_uv^(-1))_right.

The first is the standard chamber orbit. The second is supplied by the explicit
neighboring chamber described in the next paragraph. Their union is a cycle of
length 2|H|, or a doubly infinite path if H is infinite. Equivalently its
bipartite incidence matrix is I+P_(a_uv), and connectedness is just generation
of H by a_uv. Extra edges do not harm connectedness. This proves the criterion.

The explicit chambers needed here are C={H_i} and

    D_i = (C\{H_i}) ∪ {α_i^(-1)α_j H_i},  j≠i.

The definition is independent of j: the ratios of representatives lie in H_i.
These are chambers. For the one incidence not witnessed by the displayed
representative, choose a third index and use a_jk=a_ji a_ik. They are distinct
from C by independence of the C+-generators. Moreover

    (α_j^(-1)α_i) D_i = D_j.                    (N)

For indices other than i,j the multiplier lies in H_l; at i it cancels the
modified coset, and at j it creates the new one. This verifies all coordinates.

In a chiral action, the two chamber orbits and adjacency imply transitivity on
proper flags: a proper flag extends to adjacent chambers in both orbits, so a
chamber over another flag can be matched in its own orbit. In the present
C+-setting, existence of the required neighbors is also furnished by (N).
The proper-flag criterion therefore proves the version of L029 Theorem1.1 in
which the designated C+-group G itself has the chiral action. Its rank-three
Proposition4.9 follows because coset actions are always transitive on flags of
rank at most two. No finite-group classification or computational seed is used.

**Scope qualification.** The paper defines chirality using the full
type-preserving automorphism group and states Theorem1.1 using that terminology.
Its proof subsequently uses proper-flag transitivity for the designated G.
The argument above does not establish that bridge in the absence of residual
connectedness. Thinness alone cannot justify identifying G with the full group
before chamber connectedness has been proved. Accordingly, this is a complete
reduction of the designated-action version, and of the rank-three corollary,
but is not counted as an unqualified derivation of the source's literal full-
automorphism-group statement. The difference may reflect the intended convention;
it is not a claimed counterexample to the source theorem.

Source: [Leemans–Tranchida, arXiv1911.03227](https://arxiv.org/abs/1911.03227),
published *Algebraic Combinatorics*4(2021),491–499. The reduction retains the
source's distinction between a bijective incidence homomorphism and an
isomorphism; silently replacing the former by the latter would make the
rank-two argument false.

## 3. L008 from a two-point fiber

For the same C+-data, suppose the coset system is a geometry. Fix k and assume
G is transitive on its corank-one k-truncation and

    |∩_(j≠k) H_j H_k| = 2|H_k|.                 (T)

By (F) and H_(I\{k})=1, G has two free chamber orbits, represented by C and D_k.
All D_i lie in the second orbit by (N). Every proper flag of either representative
can be mapped into C: if a flag in D_k omits i, first map D_k to D_i and then
observe that D_i and C have the same i-panel. Consequently every proper flag
type is transitive. Every panel stabilizer is trivial, and the total number of
chambers is 2|G|; hence each panel has exactly two completions. Adjacent chambers
cannot lie in the same G-orbit, since an element mapping one to the other would
fix their panel and therefore be the identity. The proper-flag criterion proves
residual connectedness. Thus (T) constructs a hypertope with two alternating
free G-orbits.

Its full automorphism group either preserves those two orbits or fuses them.
Thinness and chamber connectedness imply that a type-preserving automorphism
fixing a chamber is trivial, by propagation through unique panel mates. Thus
in the fusion case G has index two in the full group and is normal. A reflection
at the base chamber conjugates the standard rotation generators α_i to α_i^(-1).
Conversely an automorphism of G inverting every α_i extends to this chamber
reflection: transport the base chamber and its neighboring chamber orbits,
using the defining coset relations. This is the established marked-inversion
criterion for C+-hypertopes; it is an explicit remaining correspondence input,
not an assertion that an arbitrary matrix similarity is a geometric reflection.

Therefore absence of that inverting automorphism is exactly chirality. This
recovers L008 Theorem1.1, including its truncation, product-size and inversion
tests. The cardinality and all-parameter residue arguments above replace the
main orbit-count proof, rather than assuming it as a black box. The final
marked-inversion correspondence is the short standard input already cited by
that paper from the 2016 hypertope correspondence.

Source: [Zhang–Leemans, arXiv2511.14562](https://arxiv.org/abs/2511.14562).
For infinite groups replace the numerical condition (T) by the assertion that
the normalized extension fiber has exactly two H_k-cosets; cardinal arithmetic
alone cannot express the condition in that setting.

## 4. One flag-matrix theorem connects the 2005 and 2026 constructions

Let S be a finite uniform linear space, with k≥3 points per line and r≥3 lines
per point. On its flag set F={(p,L):p∈L}, let A and B be the zero-one matrices
for equality of point and equality of line. They are invariant partition
matrices whenever a group is flag-transitive. Put

    D=(A−I)(B−I).

The (u,v) entry is one exactly when u=(p,L), v=(p',L'), p∈L', L≠L', and p≠p'.
There is at most one intermediate flag (p,L'), so D is zero-one. The triangle
geometry of L009 has adjacency matrix

    [ 0   D   Dᵀ ]
    [ Dᵀ 0   D  ].                              (Δ)
    [ D   Dᵀ 0  ]

This supplies the canonical triality by cyclic block permutation. More
substantially, the two original partitions can be reconstructed from D:

| Distinct flags u,v | (DDᵀ)[u,v] | (DᵀD)[u,v] |
|---|---:|---:|
| Same point | (r−2)(k−1) | — |
| Different points | 0 or k−2 | — |
| Same line | — | (k−2)(r−1) |
| Different lines | — | 0 or r−2 |

For instance, two flags at the same point have common successors on r−2
other lines, with k−1 point choices each; different points force the single
joining line. The reverse count is dual. Each distinguished value is strictly
larger than the alternatives. Consequently the maximum off-diagonal relation
in DDᵀ is A−I, and that in DᵀD is B−I.

Every type-preserving automorphism of (Δ), even one initially using different
permutations on its three parts, must therefore preserve both flag partitions
on each part. Each part permutation comes from an automorphism of S. The three
permutations are equal: after dividing out one common automorphism, a remaining
part permutation would fix every row or column of D; these are distinct,
because their squared norms (r−1)(k−1) strictly exceed all distinct-row/column
inner products listed above. We have proved

    Aut_type(Δ(S)) = Aut(S).

A correlation reversing the cyclic order transposes D and interchanges the
two reconstructed partitions. It therefore comes from a duality of S; its
square is the square of that underlying correlation. Thus dualities of Δ(S)
exist exactly when dualities of S exist, and polarities (dualities of order two)
correspond as well. This proves the automorphism/duality part of L009 without
reproducing its geometric case analysis.

In fact the full correlation group follows uniformly. Write types as Z/3Z and
let ε:Cor(S)→{1,−1} record whether a correlation preserves or interchanges
points and lines. Its action on flags sends (p,L) to (δp,δL) in the first case,
and to (δL,δp) in the second. The map

    δ̃(f,i)=(δf, ε(δ)i)

is an injective group homomorphism from Cor(S) into Cor(Δ(S)). Together with
τ(f,i)=(f,i+1), it generates all correlations by the reconstruction above, and
δ̃τδ̃^(-1)=τ^(ε(δ)). Its image intersects ⟨τ⟩ trivially because it fixes type0.
Consequently, without any flag-transitivity hypothesis,

    Cor(Δ(S)) ≅ C3 ⋊_ε Cor(S).                 (C)

Here Cor(S) acts on the normal C3 by t↦t^(ε(δ)); in particular a duality
inverts C3 and a collineation centralizes it. No polarity is required for (C).

If S has no duality, this is C3×Aut(S). If S has a duality, the different
exact sequence with kernel Aut(S) and quotient S3 splits exactly when S has
a polarity: a lift of a type transposition has order two precisely when its
underlying duality does. Thus a polarity is needed for the expression
Aut(S)⋊S3 with that natural quotient, but not for (C). This distinguishes the
two extensions discussed in L009 Proposition3.15 and strengthens its formula
to all uniform thick linear spaces.

Chambers correspond bijectively to ordered noncollinear triples of
points, with the three lines forced. Hence flag transitivity of Δ(S) is exactly
transitivity of Aut(S) on those triples. Every panel has k−1 completions.

The matrix count also proves that Δ(S) is connected for every such S. Two flags
sharing their point or their line are joined by a two-step path in (Δ), because
the corresponding displayed common-neighbor count is positive. Those moves
connect the flag set of the connected linear space. Cross-type edges then join
the three copies. This conclusion does not require flag transitivity.

### A common residue, with one pencil removed

Fix a flag (p,L) of S. The rank-two residue of this vertex in Δ(S) has the
following description:

* one part consists of points Q outside L;
* the other consists of flags (a,M), with a∈L\{p}, M≠L and a∈M;
* incidence is Q∈M.

To derive this, a neighbor in the next type is (Q,pQ); a neighbor in the preceding
type is (a,M), with a∈L\{p}; their mutual incidence is precisely Q∈M.

The block residue of the **2005 Van Nypelseer construction** has the same
description with a allowed to range over all of L. Thus the 2026 residue is
obtained by deleting one pencil, not by introducing an unrelated geometry.

For any projective plane, the points outside L form an affine plane, and the
allowed pencils are its parallel classes except one. Any two remaining classes
give a connected grid. For any affine plane of order q≥3, choose two distinct
allowed a,b∈L\{p}. Their non-L lines form two sets of q lines. Their intersection
graph is K_(q,q) minus a perfect matching: precisely parallel pairs do not meet.
This graph is connected, and its edges are all points outside L. Its incidence
subdivision connects the entire residue. These arguments apply even to planes
without coordinates.

For a Hermitian unital, use the norm-shell proof in
[hermitian_unital_proof.md](hermitian_unital_proof.md). Deleting the pencil at p
forbids the isotropic-difference direction p. Choose two other isotropic lines
of the Hermitian plane. Their root subgroups generate SU(2,q), and their moves
still lie in allowed residue edges. SU(2,q) acts transitively on the nonzero
norm shell, so the residue is connected. This proves the stronger statement

    Δ(U_H(q)) is firm and residually connected for every prime power q≥2.

The 2026 paper needs only q=2,4 for flag transitivity. Our result supplies
uniform connectivity, including all larger q, and replaces that geometric
part of its finite checking.

The Hermitian flag-transitivity branch also has a short uniform calculation.
Fix ordered isotropic points e_1,e_3 in the form
h(x,x)=x_1 x_3^q+x_1^q x_3+x_2^(q+1). A third isotropic point not on their
joining line has a unique representative (x_1,1,x_3); both remaining coordinates
are nonzero. The pair stabilizer diag(a,1,a^(−q)) preserves

    z=x_1 x_3^q,       z+z^q=−1.

It acts freely and transitively on each z-fiber, by normalizing x_1 to one.
Thus PGU(3,q) has exactly q orbits on ordered noncollinear triples, indexed by
this trace fiber, and every triple stabilizer in PGU is trivial. Field
automorphisms act on the parameter by z↦z^p. For odd q the parameter −1/2 is
fixed, so the q parameters cannot form one orbit. For q=2^e with e≥3, an orbit
has length at most2e<q, again excluding transitivity. When q=2 the trace-one
fiber is the two non-prime-field elements of F_4. When q=4 its four elements
all have degree four over F_2 (none lies in F_4), so again form one Frobenius
orbit. Hence PΓU(3,q) is transitive precisely for q=2,4. Using the standard
full-automorphism theorem for the classical unital (with the q=2 affine-plane
identification checked separately) proves precisely the Hermitian branch of
L009 Theorem1.1; no small-field search is needed for this branch.

In projective or affine dimension at least three, this residue splits according
to the plane spanned by L and Q: every allowed incidence preserves that plane.
There is more than one such plane. The plane cases above show each piece is
connected. This gives exactly the higher-dimensional obstruction in L009.

The remaining step in L009 Theorems1.1–1.2 is the classification of linear spaces
and groups transitive on ordered noncollinear triples. That uses the earlier
classification of locally two-transitive linear spaces and group exclusions;
it is not implied by (Δ). The matrix theorem compresses the construction,
automorphism recovery, duality test and residual-connectedness classification
once that list is supplied. It must not be counted as an independent proof of
the group classification.

There are two elementary exceptions in the displayed classification list that
should be corrected before using it as a seed. The final published Theorem1.1(5e)
lists A7 acting on a 15-point circle as 3-transitive and asserts the converse.
But |A7|=2520<15·14·13=2730, so that action cannot be 3-transitive. This is
different from the valid PG(3,2) branch: its ordered noncollinear triple count
is15·14·12=2520. Theorem1.1(5a) likewise permits A_v for v≥3, whereas A3 and
A4 are not 3-transitive; the alternating case requires v≥5. These observations
concern the circle branch, which is excluded from the firm triangle geometries
in Theorem1.2. They do not invalidate the thick classification in that theorem.
The statements were checked against the final journal PDF, not only its preprint;
a rendered source page is [preserved locally](sources/README.md).

Sources: [L009, final journal article](https://doi.org/10.5802/alco.482),
[L009, arXiv2504.06025](https://arxiv.org/abs/2504.06025) and
[L092, original primary PDF](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.46/no.2/b46h2lee.pdf).

## 5. Kneser geometry: the whole main construction from a tensor relation

For r≥2, k≥1 and N>rk, put V={1,…,r}×binom([N],k), with adjacency

    (i,A)~(j,B) iff i≠j and A∩B=∅.

Its matrix is (J_r−I_r)⊗K_(N,k), where K_(N,k) is the Kneser disjointness matrix.
The L030 parameters are N=n+k(r−2), n≥2k+1. Every flag is an ordered family
of disjoint k-sets with distinct types. It extends to all types since N>rk.
The symmetric group S_N is transitive on flags of any fixed type. Removing a
flag of s elements simply replaces (N,r) by (N−sk,r−s). This single residue
identity proves all of the following:

* every panel has binom(N−(r−1)k,k) completions, so the geometry is thick;
* every rank-two residue is the bipartite double of KG(n,k);
* every vertex link is KG(N−k,k)⊗K_(r−1);
* each type has binom(N,k) elements;
* S_N acts transitively on maximal cliques.

For completeness, distances in the rank-two residue need only a replacement
count. Put s=n−2k>0 and let |A∩B|=c. In two disjointness steps, at most s entries
of a k-set can change, and any replacement of at most s entries is realizable
by choosing a common disjoint k-set. Hence the exact even distance is
2 ceil((k−c)/s). For an odd path, choose its penultimate k-set disjoint from B;
it can retain at most k−c elements of A, and can attain this value. Thus the
exact odd distance is 2 ceil(c/s)+1. The diameter of the bipartite double is
2 ceil(k/s)+1, attained between the two copies of the same k-set. This also
proves connectedness of every residue.

Two distinct k-sets with intersection c have binom(n−2k+c,k) common neighbors.
For n=2k+1 this number is at most one, excluding four-cycles, and three k-sets
sharing k−1 elements exhibit a six-cycle. For n≥2k+2, two sets sharing k−1
elements have at least two common neighbors, exhibiting a four-cycle. Thus the
gonality is three in the first case and two in the second, exactly the (IP)2
criterion and diagram labels of the paper.

### Automorphisms, including the uncolored graph

Within a type, the largest number of common neighbors in another type occurs
exactly when two k-sets differ in one entry. Therefore the incidence matrix
reconstructs the Johnson graph J(N,k). Its automorphism group is S_N for N>2k:
maximal cliques are stars (all k-sets containing a fixed (k−1)-set) or tops
(all k-sets in a fixed (k+1)-set). Stars are larger, so are preserved. Their
intersection graph is J(N,k−1); induction reduces to k=1. This argument also
shows that the action on stars determines the action on k-sets. Since distinct
k-sets have different disjointness neighborhoods, the permutations induced
on different types must be the same. Thus the type-preserving group is S_N,
and the group permitting type permutations is S_N×S_r.

One can prove that the *uncolored incidence graph* has no further automorphisms.
Let d=binom(N−k,k). On functions of k-sets, filter by the spans of indicators
1_(T⊆A), |T|≤j. K_(N,k) acts on the jth quotient by

    λ_j=(-1)^j binom(N−k−j,k−j).

Indeed its action on the T-indicator is binom(N−k−j,k−j) times
1_(A∩T=∅), and inclusion–exclusion gives the claimed top term. The symmetric
matrix is diagonalizable; its constant eigenvalue is d, and every other
eigenvalue has absolute value at most kd/(N−k). In the tensor graph the least
eigenvalue is therefore −d, with eigenspace consisting exactly of vectors
constant on each type and summing to zero across types: N>rk implies
(r−1)k/(N−k)<1.

The elementary Hoffman bound now gives maximum independent-set size
binom(N,k). Equality forces the centered indicator into that −d eigenspace,
so the unique maximum independent sets are precisely the r types. Every graph
automorphism preserves their partition; the previous argument applies. Hence
the full graph group is S_N×S_r as well.

This proves the principal construction, local graph, diagram, intersection and
automorphism conclusions of L030 from one tensor relation, without a subgroup
classification or an enumeration seed. Two source slips must be kept separate
from the mathematics: the panel *order* is binom(n−k,k)−1 (as its own panel-count
lemma says), and the claimed locally Desargues example has graph group at least
S_7×S_3, not S_7. The source's displayed Corollary5.1 uses the latter smaller
group. Our argument proves the full group is S_7×S_3.

Sources: [original arXiv1811.11438](https://arxiv.org/abs/1811.11438),
[author's revised primary manuscript](https://dipot.ulb.ac.be/dspace/bitstream/2013/301910/3/main-rev.pdf).
The revised manuscript retains both displayed slips. The published paper is
*Art Discrete Appl. Math.*4(2021),#P3.01, DOI10.26493/2590-9770.1328.902.

## 6. A genuine but partial code reduction

For any symmetric adjacency matrix A over a field, its row code is LCD exactly
when im(A)∩ker(A)=0, equivalently zero is a semisimple eigenvalue. If A and its
complement B=J−I−A satisfy AB=0 and A+B is invertible, then

    im(A)=ker(B),  im(B)=ker(A),  V=im(A)⊕im(B).

Thus the two graph codes are complementary orthogonal codes. No codeword
enumeration is needed. For a strongly regular graph,

    A²=(k−μ)I+(λ−μ)A+μJ,  AJ=kJ.

Over F_3 this gives the following L050 conclusions from the four graph parameters:

* (105,72,51,45): A²=0, so the adjacency code is self-orthogonal.
* (120,77,52,44): A²=2A+2J, so AB=0; J−I is invertible since 120≠1 mod3.
* (176,105,68,54): A²=2A, again AB=0 and J−I invertible.
* (253,140,87,65): A²=A+2J. Split V=⟨1⟩⊥1^⊥, since253=1 mod3.
  A acts by2 on ⟨1⟩ and idempotently on 1^⊥. Its whole row code, and the
  augmentation subcode obtained by removing ⟨1⟩, are LCD.

This derives all the advertised LCD/self-orthogonality/complement-dual assertions
by a common projector calculation. It does **not** derive the minimum distances,
weight distributions, exact ranks or irreducible-module claims in L050 Theorem1.
Those are essential extra data; counting the entire paper as compressed would
conceal its main computational and representation-theoretic inputs.

## Coverage accounting

| Paper | What is now derived | Remaining cost |
|---|---|---|
| L029 residual connectedness | Designated-action version of the principal theorem, and rank-three corollary | Bridge from full-Aut chirality to designated-group chirality remains unproved here; no group seed |
| L008 chirality testing | Main orbit-count, thinness and RC criterion | Standard marked-inversion correspondence; actual group inputs remain to be tested |
| L030 Kneser incidence graphs | Main construction, local graphs, full automorphisms, diagram, (IP)2 | No classification seed; displayed source slips corrected |
| L009 triangle triality geometries | Construction, full correlation group, FT equivalence, Hermitian FT branch, connectedness and all needed residual cases | Classification of triple-transitive linear spaces not independently reproved |
| L092 Van Nypelseer | Hermitian-unital conjecture plus its connection to L009 | Full higher-rank Steiner-system classification not covered |
| L050 McLaughlin-subgraph codes | All orthogonality/LCD/complement-dual assertions | Code ranks, distances, weight enumerators and module classifications |

The action criteria derived for L029/L008 overlap substantially, and should
not be presented as independent large breakthroughs. The new common-residue
argument for the two unital constructions and the complete tensor-graph
derivation are substantive additions. This remains a bounded multi-paper
compression, not a proof that dozens of unrelated papers follow automatically
from permutation matrices.

## Independent exact checks

[incidence_matrix_check.py](incidence_matrix_check.py) uses integer matrices
to verify D=(A−I)(B−I), both partition-recovery formulas, and the actual
triangle-residue/deleted-pencil bijection for PG(2,2), PG(2,3), AG(2,3), and
AG(2,5). It also checks every pairwise distance in six bipartite Kneser graphs
and the inclusion-indicator action used in the spectral argument. Output:
[incidence_matrix_check.json](incidence_matrix_check.json), all PASS.

[triangle_unital_check.g](triangle_unital_check.g) builds the unitals from
projective coordinates, deletes one block-residue pencil, and checks the
resulting residue connected for q=2,3,4,5. Vertex counts are12,48,120,240;
degrees are respectively2,3,4,5. Output:
[triangle_unital_check.log](triangle_unital_check.log), all PASS. The script
also retains separately labelled checks from the original unital geometry;
those should not be mistaken for additional triangle-geometry residues.

[kneser_matrix_check.g](kneser_matrix_check.g) independently computes full
uncolored graph automorphism groups using GRAPE. The five checked orders are
240,30240,241920,21772800,144, exactly N!r!. In particular the locally Desargues
63-vertex example has order30240=7!·3!, confirming the correction.
Output: [kneser_matrix_check.log](kneser_matrix_check.log).

[chiral_fiber_check.g](chiral_fiber_check.g) verifies the complete C+-intersection
property, canonical adjacent-chamber transport, all extension fibers, thinness,
and the two chamber orbits for two independent examples. The simplex A5 example
has 120 chambers in two orbits of size60 and admits the marked inverter; the
affine F20 example has40 chambers in two orbits of size20 and no marked inverter.
Output: [chiral_fiber_check.log](chiral_fiber_check.log), both PASS. These finite
checks supplement the general fiber proof and do not establish the L029 bridge.
