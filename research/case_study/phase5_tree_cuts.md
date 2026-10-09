# Tree cuts unify a family of symmetric-group geometries

10 October 2026. Written derivation; independent review and finite checks are
recorded separately. The results recovered below are established mathematics.
No open-problem resolution or priority claim is made for this tree model.

## 1. Source targets and retained input

The network here includes papers without the author who seeded the catalogue:

* Buekenhout–Cara, *Some properties of inductively minimal geometries*,
  Bull. Belg. Math. Soc. Simon Stevin 5 (1998), 213–219,
  DOI [10.36045/bbms/1103409005](https://doi.org/10.36045/bbms/1103409005).
  The primary author-uploaded text was read, including its definitions,
  Lemma 1 and four-part Theorem 1. An independent publisher PDF was not
  obtained. The target is the four principal property characterizations.
* Cara–Lehman–Pasechnik, *On the number of inductively minimal geometries*,
  Theoretical Computer Science 263 (2001), 31–35,
  DOI [10.1016/S0304-3975(00)00228-0](https://doi.org/10.1016/S0304-3975(00)00228-0).
  The target is the tree correspondence announced in the primary abstract.
  Full-text download remains unavailable in this intake; this is not a claim
  to have compared every statement of that paper.
* Cameron–Cara, *Independent generating sets and geometries for symmetric
  groups*, [author manuscript](https://maths.qmul.ac.uk/~pjc/preprints/igsgsn.pdf).
  All twelve manuscript pages were read. Its Corollary 2.3 and Theorem 3.2
  already prove the tree-generator intersection and geometry statements.
  The tree branch is a retained known model, rederived here in subset form.
  We do not replace its classification of all maximal independent generating
  sets, the parity-twisted branch, Whiston's theorem, or its CFSG input.
* Cara–Leemans, *On inductively minimal geometries that satisfy the intersection
  property*, J. Combin. Theory A 111 (2005), 327–330,
  DOI [10.1016/j.jcta.2004.12.006](https://doi.org/10.1016/j.jcta.2004.12.006),
  catalogue L089. The primary abstract and the theorem restatement in the
  2004 Jacobs–Leemans shadow-IP paper were read. The full 2005 text was not
  retrieved. The target is precisely its advertised unique path-diagram
  characterization, rederived below.

To transfer the constructed family to **all inductively minimal pairs**, we
retain the foundational 1997 Buekenhout–Cara–Dehon classification in the form
recalled as Lemma 1 of the 1998 paper: their connected diagrams are exactly
the graphs with no induced cycles longer than three, every edge in a unique
maximal clique, and every vertex in at most two maximal cliques; each permitted
diagram determines a unique pair. Rank one is treated separately. We prove
the diagram-to-tree conversion below. The foundational classification is not
silently replaced by the construction of examples.

## 2. A tree on the natural permutation torsor

Let T be a tree with vertex set Ω, |Ω|=N≥2, and edge set E. For an edge e,
let τ_e be the transposition of its endpoints. For I⊆E, define

    K_I = <τ_e : e∈I>.

**Forest formula.** If C ranges over the components of (Ω,I), then

    K_I = ∏_C Sym(C),       K_I ∩ K_J = K_(I∩J).                 (1)

The first equality follows because edge transpositions in a connected graph
generate its full symmetric group: conjugating along paths produces the
transposition of any two vertices. Different components have disjoint supports.
For the second equality, a permutation belongs to both groups exactly when
it preserves every intersection of their component blocks. Two vertices lie
in such an intersection exactly when their unique tree path uses only edges
in I∩J. Thus those blocks are precisely the components of (Ω,I∩J).

In particular K_E=Sym(Ω), K_empty=1. These are explicit permutation matrices
with a distinguished basis; component partitions perform the subgroup algebra.

Root T. For each edge e, let A_e be the component of T−e away from the root.
These sets are laminar: two are nested or disjoint. Put

    H_e = K_(E\{e}) = Sym(A_e) × Sym(Ω\A_e).

Vertices of type e in the coset system of the H_e identify with subsets X_e
of Ω of size |A_e|. Two vertices of different types are incident exactly when

    |X_e ∩ X_f| = |A_e ∩ A_f|.                               (2)

Indeed, two pairs of subsets are in the same Sym(Ω)-orbit exactly when the
four corresponding Boolean atoms have the same sizes. Formula (2) gives
those sizes, and is therefore the exact coset-incidence condition.

**Laminar Helly lemma.** Every pairwise incident family of these typed subsets
is the image of the corresponding A_e under one permutation of Ω.

To prove this, (2) forces precisely the same inclusion and disjointness
relations as in the corresponding subfamily of the A_e. Add Ω as a root
container. Subtract from each selected container its maximal selected proper
subcontainers. These differences form partitions of Ω in both families;
their sizes agree by subtraction. Choose bijections between corresponding
parts and combine them. The resulting permutation maps every selected A_e
to its prescribed X_e. This works for partial families as well as chambers.

Consequently the coset system is a flag-transitive geometry. Formula (1)
identifies the residue left after fixing the types outside I with the join
of the tree geometries for the nontrivial components of (Ω,I). Its chamber
stabilizer is 1, each panel has two chambers, and its chamber adjacency graph
is the Cayley graph on the generating transpositions. Residual connectedness
also follows from the forest generation formula.

The diagram is the line graph L(T): incident edges give a product of
transpositions of order three, and disjoint edges give order two. Rank-two
residues are therefore hexagons or complete bipartite four-cycles. Every
connected residue with m edges has group Sym(m+1); hence the constructed
pair is inductively minimal under the source definition.

## 3. Four property tests become cuts of a tree

For N≥3, the set stabilizer Sym(A)×Sym(Ω\A) is maximal in Sym(Ω) exactly
when |A|≠|Ω\A|. If the sizes agree, put a=|A|≥2. Its unique proper
overgroup is the unordered two-block stabilizer Sym(a) wr C2, and this
overgroup is maximal.

Here is an elementary proof covering both assertions. The stabilizer contains
all transpositions within each of the two blocks. If an additional permutation
does not preserve the unordered block partition, adjoining the conjugates of
these transpositions introduces a cross-block edge. Their support graph is
then connected, so they generate Sym(Ω). The only possible intermediate
group is the unordered block stabilizer. It differs from the original group
only when the block sizes agree, in which case their index is two. For N=2,
the trivial stabilizer is itself maximal in Sym(2), an explicit exception to
the unequal-size criterion.

The following consequences recover the four parts of the 1998 Theorem 1:

* **RWPRI, local two-transitivity, and rank-two shadow-IP.** In each forest
  residue choose a leaf edge of a nontrivial component. Its deletion gives
  a maximal point stabilizer in the corresponding symmetric factor. Panels
  have two elements with their full transitive action. The rank-two graphs
  above have at most one common neighbor for two same-type vertices, or are
  complete bipartite; hence they satisfy geometric rank-two IP.
* **PRI in every even rank.** Rank is N−1, so even rank makes N odd and every
  edge cut unequal. More precisely, PRI holds exactly when there is no equal
  bipartition edge, with the N=2 exception stated above.
* **The remaining cases are QPRI.** An equal cut gives exactly the two-step
  maximal chain described above; all other cuts are already maximal. Removing
  the corresponding vertex from L(T) gives two components of sizes |A|−1
  and |Ω\A|−1. Thus the source's diagram “middle” condition is exactly an
  equal bipartition edge for N≥4.
* **RPRI exactly for stars.** Every nontrivial subtree of a star is a star,
  so every cut in every component residue is a leaf cut. If T is not a star,
  it contains a three-edge path. The corresponding rank-three residue has
  group Sym(4), and its middle cut is 2+2, which is not primitive. Finally,
  L(T) is complete exactly when T is a star, including the small ranks.

Here PRI refers to primitivity on every type, RPRI to that condition in every
residue, RWPRI to at least one primitive type in every residue, and QPRI to
the source's quasi-maximal stabilizer condition. The action is retained in
each assertion.

## 4. Why geometric shadow-IP forces a path

The geometric intersection property here is the shadow property of the 2004
paper, in every residue. It is stronger than the subgroup intersection
formula (1), which holds for every tree.

If T has a vertex of degree at least three, take three incident edges. Their
residue is the geometry of the claw K_(1,3): three copies A,B,C of a four-point
set, where vertices of different types are incident when their labels differ.
Take target type A, x=(B,1), and the one-element flag F={(B,2)}. Their common
A-shadow is {3,4}. A witness flag with that shadow cannot contain an A-vertex,
which would force a singleton shadow, or a B-vertex, which could not be incident
with both x and F. A C-vertex incident with x and F has label 3 or 4, so cannot
be incident with every element of that shadow. No witness exists, and IP fails.

If T is a path, root it at an endpoint. The cuts A_e have sizes 1,...,N−1
and form a chain. Its geometry is exactly the proper Boolean lattice on Ω,
with subsets incident when comparable. Fix a target size k and any family U
of vertices whose common k-shadow is nonempty. If U contains a k-subset,
the shadow is a singleton and that point itself is a witness. Otherwise put

    L = union of the members of U of size less than k,
    V = intersection of the members of U of size greater than k,

using empty union ∅ and empty intersection Ω. The shadow is exactly

    {Y⊆Ω : |Y|=k and L⊆Y⊆V}.                              (3)

Nonemptiness gives |L|≤k≤|V|. If either bound is equality, the unique Y is
a point witness. Otherwise {L,V}, omitting ∅ or Ω, is a flag of at most two
vertices with precisely shadow (3), and each of its vertices is incident
with every member of U. This gives an explicit bounded-size certificate.

Every residue in this geometry is a join of proper Boolean intervals. In a
join, the shadow of a target type depends only on its own factor. If that
factor is rank one, the shadow is empty, the entire type set, or a singleton;
use no witness for the empty case, the empty flag for the entire set, and
the point for a singleton. Otherwise the interval argument above gives its
witness, automatically incident with the other factors. Thus all residues
satisfy shadow-IP.

We have proved, for this whole tree family,

    geometric shadow-IP in all residues ⇔ T is a path.        (4)

After the retained foundational identification, this recovers the exact
advertised 2005 characterization in every rank. It does not assert that the
2005 authors lacked the idea or that a currently open conjecture was solved.

## 5. Recovering the tree correspondence without a line-graph theorem

Let D be a connected diagram satisfying the three graph conditions in §1,
with at least two vertices. Its maximal cliques meet pairwise in at most
one vertex, since otherwise their common edge would belong to two cliques.
Construct a graph T_D as follows. Give each maximal clique a vertex. A diagram
vertex in two maximal cliques gives an edge joining their vertices. A diagram
vertex in just one maximal clique gives an edge from its clique vertex to
a new leaf. This establishes a bijection V(D)↔E(T_D), and adjacency in D
is exactly adjacency of the corresponding edges. T_D is connected.

It is acyclic. A shortest cycle of length at least four would give an induced
cycle in D on its edge labels, violating the first graph condition. A
triangle of clique vertices would give three pairwise adjacent diagram
vertices lying in one maximal clique, forcing its edges to lie in two
different maximal cliques. Loops and double edges are excluded by construction
and the at-most-one-vertex intersection just proved. Thus T_D is a tree and
D=L(T_D). The one-vertex diagram gives the two-vertex tree separately.

Conversely, the maximal cliques of the line graph of a tree are the edge
stars at its nonleaf vertices. The same reconstruction recovers that tree,
including the single-edge exception. Hence the correspondence is unique
up to graph isomorphism. Combined with the retained 1997 uniqueness theorem,
rank-r inductively minimal pairs correspond to unlabelled trees on r+1
vertices. This supplies the advertised enumeration reduction of the 2001
paper. The tree counts themselves are a separate classical enumeration input.

The later Cameron–Cara manuscript explicitly identifies the transposition
tree model and its geometry. An earlier request for a direct tree construction
must therefore be checked against that later work; it cannot be counted as
a new resolution by this repository.

## 6. Reuse, limitations, and the next extension

One forest formula, one laminar-set argument, and one two-block stabilizer
argument give the group intersections, flag transitivity, residues, all four
1998 property tests, the tree-count reduction, and the 2005 path test. This
is a substantive common derivation, conditional on an explicitly retained
foundational classification. It is not a numerical compression ratio: source
and replacement proof lengths and their dependencies have not been measured.

The 2003 *Truncations of inductively minimal geometries* paper is a natural
next target. Deleting types amounts to contracting unselected edges and
retaining the sizes of the resulting vertex blocks. A classification of all
weighted-tree truncations and their primitivity and IP conditions remains
to be proved and compared with its full primary text. It is not claimed here.

The full maximal-independent-generator classification in the Cameron–Cara
paper also remains outside this reduction. In particular, one must not count
its whole paper as reduced merely because its tree branch is recovered.
