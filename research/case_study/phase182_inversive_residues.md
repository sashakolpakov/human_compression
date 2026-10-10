# Residues of the subline construction

Working manuscript, phase182. The mathematical argument below is complete
at its stated scope and awaits independent review. It has not been admitted
to the public manuscript totals or certified in Lean.

## 1. Source and scope

The source is D. Leemans, *A Generalization of a Construction due to
Van Nypelseer*, Beiträge zur Algebra und Geometrie 46 (2005), 561–574
(registry L092). We use its literal Construction2, printed pp.563–564.
Lemma5, printed p.571, asserts that in the subline family the resulting
geometry is residually connected precisely when q=4 and e=2. Proposition2
below corrects this assertion: the condition is e=2, with no restriction
q=4. The distinction between residual connectivity and flag transitivity
is essential. Proposition3 retains the q=4 flag-transitive case.

The source construction and the subline designs are retained mathematics.
The present contribution is a full residue calculation, the correction it
implies, and independently reproducible finite checks. Historical priority
of this correction has not been established. It is not an answer to an
open conjecture. In particular it gives no additional credit for the
source's separately stated Hermitian-unital conjecture.

## 2. The construction and its panels

Let q≥3 be a prime power, e≥2, Q=q^e, and let Ω=P¹(F_Q).
Let B be the family of images of P¹(F_q) under PGL₂(Q). Its members will
be called blocks. This is the classical Steiner system S(3,q+1,Q+1):
every three distinct points belong to precisely one block. To see
uniqueness directly, take an ordered triple to (∞,0,1). The stabilizer
PGL₂(q) of the standard subline is transitive on its ordered triples;
thus every image containing this triple is the standard subline itself.
Consequently two distinct blocks meet in at most two points.

There are

    r = (Q−1)/(q−1)

blocks through a fixed pair T. This follows by partitioning Ω\T into
the q−1 remaining points of each block through T.

Use type labels 0,1,2,3, which are the source labels shifted down by one.
The objects of Γ are:

* type0: an original point x∈Ω;
* type1: m=(T,E), where |T|=2 and T∪E is a block, with T∩E=∅;
* type2: a block B₀;
* type3: a copied point z∈Ω.

Between distinct types the six incidence rules are

    x∼(T,E) iff x∈T;             x∼B₀ iff x∈B₀;
    x∼z iff x≠z;                (T,E)∼B₀ iff T⊆B₀ and E∩B₀=∅;
    (T,E)∼z iff z∈E;            B₀∼z iff z∉B₀.

The fourth condition says exactly that B₀ and T∪E are distinct blocks
through T. We retain the disjointness condition in the definition rather
than silently replacing the source incidence relation.

**Proposition1.** Γ is a firm rank-four geometry. The numbers of chamber
extensions of panels missing types0,1,2,3 are respectively

    2, q, r−1, q−1.

**Proof.** For a panel consisting of m,B₀,z, its possible original points
are the two points of T. For a panel x,B₀,z, choose the second point
u∈B₀\{x}. The unique block B′ through x,u,z intersects B₀ in exactly
{x,u}, so m=({x,u},B′\{x,u}) is the unique completion associated to u.
There are q choices. A panel x,m,z admits all blocks through T other
than T∪E, giving r−1 choices. A panel x,m,B₀ admits the q−1 points of E.

Every incident pair extends to a chamber: this also follows from each of
the six nonempty rank-two incidence graphs described in Section3, all of
whose vertices have a neighbor. Each object is in an incident pair, so
every flag extends. Since q≥3 and r≥q+1, all four panel sizes are at
least two. ∎

## 3. All rank-two residues

Fix an incident pair of types i,j and write R_ij for its residue.
The following table gives all six possibilities. An incidence subdivision
of a complete graph means the bipartite graph between its vertices and
its two-element subsets.

| Fixed types | Remaining incidence graph |
|---|---|
| 0,1 | K_(r−1,q−1) |
| 1,2 | K_(2,q−1) |
| 1,3 | K_(2,r−1) |
| 2,3 | Incidence subdivision of K_(q+1) |
| 0,3 | Points of AG(e,q) other than one point, and lines avoiding that point |
| 0,2 | Points of AG(e,q) outside a fixed line L, and lines meeting L in exactly one point |

Here and below all affine lines are lines over F_q, not arbitrary lines
over a smaller subfield.

**Proof of the table.** For R_01 the fixed marked object determines T,E.
The remaining objects are the r−1 alternative blocks through T and the
q−1 points of E. Each such block avoids E by the Steiner property, so
all these cross-type pairs are incident. In R_12 the remaining original
points are T and the copied points are E, with all incidences present.
In R_13 the remaining objects are T and the r−1 alternative blocks,
again with all incidences present.

For R_23 fix B₀ and z∉B₀. A marked object incident to both is determined
uniquely by its pair T⊆B₀: take the unique block B′ containing T∪{z}.
Its tail is disjoint from B₀. Its original-point neighbors are precisely
T, which gives the stated subdivision.

For the last two cases, use an element of PGL₂(Q) taking the fixed
original point x to ∞. The derived design at ∞ is AG(e,q): deleting
∞ from the blocks containing it gives the sets aF_q+b⊂F_Q, a≠0.
Indeed, affine transformations preserve these sets, and conversely an
image of the standard subline containing ∞ can be represented by a
projectivity fixing ∞ after composing with an element of PGL₂(q).

For R_03 the copied point z is an affine point. Its remaining type2
objects are exactly the affine lines avoiding z. The marked object
whose pair is {∞,u} is uniquely determined by z, namely the block
through ∞,u,z; it exists for every u≠z. Such a marked object is incident
to an avoiding line precisely when u lies on it. This is the fifth row.

For R_02 the fixed block B₀ becomes an affine line L. A remaining marked
object has T={∞,u}, u∈L, and a block B′≠B₀ through T. It therefore
corresponds to an affine line M≠L meeting L at u. Its copied-point
neighbors are exactly M\{u}, all of which lie outside L. Conversely
each affine line meeting L in one point produces one marked object.
This proves the last row. ∎

The first four graphs are connected. The fifth is connected for every
e≥2: given two distinct retained points u,v, their joining line avoids
the removed point unless u,v and that point are collinear. In the latter
case choose w outside that line; the paths through the lines uw and wv
connect u and v. Every retained line has retained points.

In the sixth graph, any retained point w determines the unique affine
plane H=⟨L,w⟩. A retained line through w meets L and is contained in H.
Moving along such a line therefore cannot change H. Conversely the
subgraph associated to H is connected for q≥3. If two outside points
u,v have a joining line not parallel to L, that line meets L and joins
them in the incidence graph. If their joining line is parallel to L,
choose w∈H outside L and outside this parallel line. Such a point exists
because q≥3. Both uw and wv meet L, giving a path. All its line vertices
have q−1 outside points, so there are no additional components.

There are

    (q^(e−1)−1)/(q−1)

affine planes containing L. Thus R_02 has exactly this many components,
each with q(q−1) point vertices and q² line vertices. In particular it
is connected exactly when e=2.

## 4. The higher-rank residues

**Proposition2.** Γ is residually connected if and only if e=2.

**Proof.** All rank-two residues have just been determined, so necessity
follows from R_02. We verify that the residues of ranks three and four
are connected; this verification works for every e≥2.

Fix an original point x. After taking x to ∞, consider the subgraph
between copied points and blocks containing x. It is the nonincidence
graph between points and lines of AG(e,q). Any two affine points have
a common nonincident line: choose a parallel class, which has q^(e−1)
lines, at most two of which meet the specified points. Since q≥3,
at least one remains. Each affine line has an outside point. Hence this
subgraph is connected. Every marked object in the residue is incident
to r−1 such blocks and therefore attaches to it.

Fix a marked object (T,E). Its residue is a complete tripartite geometry
whose parts are the two original points of T, the r−1 alternative blocks
through T, and the q−1 copied points of E. All parts are nonempty.

Fix a block B₀. The original points in B₀ and the copied points outside
B₀ form a complete bipartite subgraph with both parts nonempty. Every
marked object in this residue has an original-point neighbor in T⊆B₀,
so it attaches to that connected subgraph.

Fix a copied point z. For each pair T⊆Ω\{z}, the unique block through
T∪{z} gives one marked object incident to z. Original points and these
marked objects form the incidence subdivision of the complete graph on
Ω\{z}. Every block avoiding z has an original-point neighbor and is
therefore attached to it.

Finally, the original and copied points in the full geometry form a
complete bipartite graph with the matching x=z removed. Since |Ω|≥10,
this graph is connected. Every marked object and every block has an
original-point neighbor. Thus the full incidence graph is connected.

When e=2, all six rank-two residues are connected as well. These exhaust
the residues of rank at least two in a rank-four geometry. ∎

## 5. Flag transitivity is a different condition

**Retained input, for e=2.** The automorphism group of this subline design lies in
PΓL₂(Q). One may use Kantor, *Homogeneous designs and geometric lattices*,
J. Combin. Theory A38 (1985), 66–74, Theorem3 and its proof on p.73.
The proof explicitly bounds the relevant three-transitive group by
PΓL₂(Q); this upper bound is omitted from the abbreviated theorem
statement reproduced as L092 Theorem10. PGL₂(Q) acts on the design and
is sharply three-transitive on Ω, so the hypothesis applies to its full
automorphism group. Here Q+1=q²+1 is neither a power of two nor one of
the Mathieu degrees, which excludes the other cases of that proof.
The semilinear projectivities do preserve the subline design, so equality
holds. This classification input is retained, not reproved here.

We also need to relate design automorphisms to type-preserving geometry
automorphisms. The incidence of original with copied points is inequality,
so their permutations agree. Incidence with type2 objects then says
that this common permutation preserves the block family. A marked object
is determined by its two original-point neighbors T and its copied-point
neighbors E, so its image is determined as well. Conversely every design
automorphism preserves all six incidence rules. Thus the two type-preserving
automorphism groups agree. No larger unexamined geometry group is being
used in the following counting argument.

**Proposition3.** For e=2 and q=p^f≥3, Γ is flag-transitive if and only
if q=4. Consequently the conjunction of firmness, residual connectivity
and flag transitivity in this subline family still holds exactly at
(q,e)=(4,2).

**Proof.** Count a chamber by choosing, in order, its original point x,
the other point u of T, its copied point z, and then its source block B₀.
The first three form an ordered triple of distinct points. They determine
the block B′=T∪E uniquely. There are r−1=q alternative blocks B₀ through
T. Consequently

    |Ch(Γ)| = (Q+1)Q(Q−1)q = |PGL₂(Q)|q.

The retained automorphism bound gives

    |Aut(Γ)| = 2f |PGL₂(Q)|.

Flag transitivity would imply q divides 2f, in particular q≤2f. If p≥3,
then p^f≥3^f>2f for every f≥1. If p=2, the assumption q≥3 gives f≥2;
2^f≤2f holds only for f=2, since it is false at f=3 and remains false
by induction. Thus q=4 is necessary.

For sufficiency set Q=16. PGL₂(16) is transitive on flags (x,T,B₀)
with x∈T⊂B₀: take B₀ to P¹(F₄), then use PGL₂(4) inside its stabilizer
to take x and the other point of T to ∞ and0. With these choices fixed,
the alternative blocks through T are

    B′_α = {∞} ∪ αF₄,

where αF₄* ranges over the four nonidentity elements of the cyclic
quotient F₁₆*/F₄* of order5. The Frobenius map z↦z² fixes the chosen
base flag and acts on this quotient by multiplication by2 on exponents.
It cycles the four nonidentity classes. Once B′_α has been selected,
the scalars in F₄* fix x,T,B₀ and B′_α and act transitively on its three
possible copied points z∈αF₄*. The stabilizer of (x,T,B₀) is therefore
transitive on its chamber extensions. This proves chamber transitivity,
and every flag extends by Proposition1. ∎

## 6. Exact finite check and remaining admission work

`phase182_inversive_geometry_check.py` constructs F₉ explicitly, generates
the 30 blocks of S(3,4,10), and checks every triple of distinct points.
It builds the literal four-type incidence relation and checks every flag,
panel and residue of rank at least two. The object counts are
10,180,30,10; the flag counts, including the empty flag, are
1,230,1650,3600,2160. Every flag extends; panel sizes are2 or3; all1881
residues of rank at least two are connected. This is a finite counterexample
to the printed residual-connectivity assertion at q=3,e=2.

The generated semilinear subgroup has two chamber orbits of lengths720
and1440. The Python checker alone does not prove this is the full group;
the full-group claim in Proposition3 uses the separately attributed input
and the reconstruction argument above. An independent GAP reconstruction
and review are in progress. Neither checker certifies the uniform proof
in Lean. The remaining source contracts, including the Mathieu branches,
are not covered by this note, and L092 is not counted as a fully replaced
manuscript on the basis of this correction.

Primary references:

* [L092 primary PDF](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.46/no.2/b46h2lee.pdf),
  local SHA256 `f76a72aeec658ace5d821519a686c3041e455d3a1c5c4276988bd711ba830403`.
* [Kantor primary PDF](https://pages.uoregon.edu/kantor/PAPERS/homogeneousdes.pdf),
  Theorem3 and proof, printed p.73. Read through the web PDF service;
  local PDF acquisition did not succeed in this pass.
