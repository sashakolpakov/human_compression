# An explicit lattice bridge for the cube-input halving family

Private additive proof, 10 October 2026. This note does not change the frozen
Compress_C files. It addresses precisely ledger N12 and the p=4 identification
in N8. Its proof replaces their retained toroidal-identification dependency;
independent review of this replacement is still required. The general halving
theorem and its regularity proof remain those of Compress_C §§3–4. No additional
source is admitted and no compression factor is asserted.

## 1. Coordinate conventions and the actual face poset

Let r≥2 and let L be the r-dimensional cross-polytope with vertices labelled
+e_i,−e_i, 1≤i≤r. A proper face of L chooses at most one vertex from each
antipodal pair. Write Q_r for the cubical tessellation of R^r whose vertices are
Z^r and whose cells are products of unit intervals and integer singletons.
The quotient Q_r/4Z^r has a formal least and greatest face adjoined when viewed
as an abstract polytope. These formal faces are also understood below.

For each pair of binary coordinates belonging to +e_i,−e_i, use the Gray map

    (0,0) ↦ 0,   (1,0) ↦ 1,   (1,1) ↦ 2,   (0,1) ↦ 3     in Z/4Z.   (T1)

**Lemma T1.** The product of these maps is a rank-preserving face-poset
isomorphism 2^L ≅ Q_r/4Z^r. Binary weight modulo two becomes
∑_i x_i modulo two in the cubical coordinates.

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
F with free coordinate set S, write its free intervals as [m_i,m_i+1] for
i∈S and its fixed coordinates as m_j for j∉S. The dual face F* has fixed
coordinate m_i+1/2 for i∈S and free interval [m_j−1/2,m_j+1/2] for j∉S.
This reverses containment: whenever an endpoint is fixed in a subface of F,
the corresponding free interval of the dual contains the fixed midpoint of
F*. It is a bijection onto the shifted cubical tessellation, with dimensions
adding to r. Subtracting (1/2,…,1/2) identifies that tessellation with Q_r.
The construction commutes with translations by 4Z^r, and consequently induces
an order-reversing bijection on the quotient. Thus for the r-cube K=L*, the
source's polytope (2^{K*})* is indeed the cubical toroid
{4,3^(r−2),4}_(4,0,…,0). The string is {4,4} when r=2.
Reversing the source marking moves its last-end halving to first-end halving
of 2^L. Type reversal is kept explicit; no unproved compatibility of a chosen
self-duality with halving is needed.

## 2. The marking and the exact affine quotient

Use the following reflections of R^r:

    a(x_1,x_2,…,x_r) = (1−x_1,x_2,…,x_r),
    b_i swaps x_i and x_(i+1)                         (1≤i<r),
    c(x_1,…,x_(r−1),x_r) = (x_1,…,x_(r−1),−x_r).      (T2)

They generate W=Z^r⋊B_r, where B_r is the signed permutation group. Indeed the
b_i,c generate B_r, including the reflection x_1↦−x_1; its product with a is
translation by ±e_1. Signed permutations then supply every integer translation.
The simplex 1/2≥x_1≥x_2≥⋯≥x_r≥0 is a fundamental chamber. One way to verify
this without a presentation theorem is to translate each coordinate to
[−1/2,1/2], make it nonnegative, and order the coordinates; a point with strict
inequalities has a unique such representative. Its reflected walls are the
displayed generators. Its vertices are the barycentres of a nested flag of
cubical faces, so its chamber system is the barycentric subdivision of Q_r.

The marking in (T2) also agrees with Danzer's marking under (T1). Flipping the
+e_1 bit induces x_1↦1−x_1 modulo four; interchanging antipodal pairs induces
the b_i; swapping the two bits in the last pair induces x_r↦−x_r. These are
the usual base vertex/base flag generators of 2^L. Hence the isomorphism of
Lemma T1 identifies the marked action, not only the unmarked face poset.
The action of W on Q_r/4Z^r has kernel exactly Λ=4Z^r: an affine signed
permutation acting trivially on all vertices has translation zero modulo
four, and its linear part is the identity modulo four; testing the unit
vectors forces that signed permutation to be the identity.

Put b=b_1 and replace a by

    d=aba: (x_1,x_2,x_3,…,x_r)
            ↦(1−x_2,1−x_1,x_3,…,x_r).              (T3)

Let E={v∈Z^r : ∑v_i is even}.

**Lemma T2.** H=⟨d,b_1,…,b_(r−1),c⟩ is exactly E⋊B_r. It has index two
in W and contains Λ. Its fundamental chamber is

    x_1≥x_2≥⋯≥x_r≥0,   x_1+x_2≤1.                (T4)

Its chamber system is the halved cubical geometry, and the marked finite
halving group and geometry are H/Λ and the quotient of that chamber system
by Λ, respectively.

**Proof.** Every displayed generator preserves the parity of an integral
vertex's coordinate sum, so H≤E⋊B_r. It contains B_r. The product of d with
the B_r-reflection (x_1,x_2)↦(−x_2,−x_1) is translation by e_1+e_2.
Conjugating by B_r gives every ±e_i±e_j. These span E: subtract multiples of
e_i−e_r, i<r, to leave an even multiple of e_r, and use
2e_r=(e_r+e_1)+(e_r−e_1). This works also for r=2. Thus equality holds and
the index is two. Since every 4e_i is in E, Λ≤H.

The region (T4) is the union of the preceding W chamber and its reflection
in the a-wall x_1=1/2. On their common wall the two chambers glue; the other
wall x_1=x_2 is paired with its a-image x_1+x_2=1. All other walls agree.
Because W=H⊔Ha and the interiors of W chambers are disjoint, these doubled
chambers tile R^r under H, each once. Their wall reflections are exactly
d,b_1,…,b_(r−1),c. Equivalently, their chamber labels are the old cubical
flags with the initial vertex chosen in one parity class, pairing the two
old flags differing only at that vertex. The two ends of the old edge
become the two new vertex types; the higher faces retain their type. This
is precisely the graph-halving construction of Compress_C §3.

Finally, translations in Λ preserve both vertex colors and take cubical
faces to cubical faces. The same flag pairing therefore commutes with Λ.
Every finite chamber has a lift, and two lifts yield the same finite chamber
exactly when they differ by Λ. Wall adjacencies are the marked reflections
modulo Λ. The maximal parabolics are the images of the corresponding wall
subgroups, so the typed coset geometry also agrees. Regularity, thinness and
residual connectedness of the finite geometry follow from the already proved
halving theorem; they are not inferred solely from being a group quotient. ∎

For r≥3, the walls (T4) have the affine fork diagram B̃_r: d and b_1 commute;
both meet b_2 with product order three, successive b_i have order three, and
b_(r−1)c has order four. All other distinct wall pairs commute. This follows
directly from (T2)–(T3), or from their mirror angles. Thus its rank-(r+1)
quotient has the source's type {4,3^(r−3),3/3}. Here the quotient lattice is
exactly 4Z^r in the original coordinates; the subscript (4,0,…,0) denotes
the lattice generated by that vector's signed-permutation orbit. This proves
the source's all-rank toroidal identification, including the marking. Its
group order is [E:4Z^r]|B_r|=(4^r/2)2^r r!=2^(3r−1)r!, agreeing with the
separate parity-module calculation. The order is a check, not the proof.

The coordinate convention can be checked directly against Ens's primary
paper: its equations (3.1), (4.1) are (T2), (T3) for r=3; its §2 definition of
Λ_s uses the signed-permutation orbit of s, and Theorem 4.3 denotes the
corresponding Coxeter-complex quotient by that lattice. Thus s=(4,0,0) here
is literally the same parameter. The target extends this convention to
larger r. No classification theorem about all invariant lattices is needed.
[Ens, *Rank 4 toroidal hypertopes*, pp.70–75](https://www.researchgate.net/publication/325538081_Rank_4_toroidal_hypertopes).

## 3. The rank-three square map and its changed lattice basis

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
{4,4}_(2,2). Lemma T1 and the explicit duality already identify the original
map as {4,4}_(4,0). This completes both p=4 names in ledger N8.

## 4. Source and proof accounting

The frozen target is Montero–Weiss, arXiv:2001.11082v1, §§3–4, especially
pp.9–10. The cube construction and the precise target names were reread
from the existing bound primary text. Ens's primary paper was selectively
read in the web-rendered complete article at the link above: pp.70–75,
definitions of the lattice notation, equations (3.1), (4.1), the translation
description, and Theorem 4.3. Its entire classification proof and later
sections were not independently reviewed. Publisher access failed; no local
PDF bytes or page screenshots of Ens are claimed. Its definitions are used
only to match notation; the particular quotient is proved above.

New dependency delta: remove the retained toroidal identifications from C
ledger N12 and the p=4 part of N8 **if this note passes independent review**.
Retain Danzer's general construction/full-group theorem where C uses it,
the reviewed geometric halving theorem, and C's other explicit background.
The argument here proves this cross-polytope input directly and needs no
new exhaustive computation, numerical experiment, catalogue, or Lean claim.
It does not extend C's intake to Ens's classification paper, nor replace any
of that paper's classification or chirality results.
