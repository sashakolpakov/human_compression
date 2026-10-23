A common commutant for an entire family of markings
==================================================

Let V be a finite-dimensional vector space over a field F. For X in End(V),
write

  C(X)={M in GL(V): XM=MX}.

This is a subgroup of GL(V). Indeed, if X commutes with M and N, then
XMN=MXN=MNX. If M is invertible, XM=MX implies XM^-1=M^-1X. Thus identity,
products and inverses all belong to C(X).

Proposition 1. Let rho:G -> GL(V) be a homomorphism, let S be a set of
elements of G, and suppose that

  X rho(s)=rho(s) X                 for every s in S,
  X rho(g)!=rho(g) X                for one known element g in G.

Then <S> is a proper subgroup of G.

Proof. The preceding subgroup observation gives rho(<S>) <= C(X). The
second equality failure shows rho(g) is not in this subgroup. Consequently
g is not in <S>, as required. No faithfulness assumption is used. Nor must
X be invertible, belong to rho(G), or be a word in S. An actual escape
already rules out a scalar X. A nonzero entry of X rho(g)-rho(g) X is a
finite certificate of that escape.                                     QED

The collection of matrices commuting with given matrices M1,...,Mr is the
linear subspace of End(V) defined by XM_i-M_iX=0. This permits a linear
search for a witness, but a checker need only test the supplied equalities
and an escape. It need not trust the search method, a canonical solution,
Schur's lemma or a claimed structure of the commutant algebra. The actual
example below was proposed from a previously acquired finite subgroup
table. Its direct certificate does not depend on that choice of search.

Uniformity over subgroup choices
--------------------------------

Corollary 2. Let K=<k1,...,kr> and H=<h1,...,hs> be subgroups of G. Suppose
X commutes with rho(a),rho(b),rho(e), with every rho(ki) and every rho(hj),
but fails to commute with rho(g) for one acquired ambient element g. Then

  <a,b,c,d,e> != G               for every c in K and every d in H.

Proof. Commutation with the supplied bases implies commutation with every
element of rho(K) and rho(H), by closure under products and inverses.
Proposition 1 therefore applies to every displayed marking.             QED

There is no need to enumerate the pairs, identify automorphism orbits,
recognize a maximal subgroup or decide the intersection property of any
individual marking. The original bases must genuinely generate the groups
claimed. A coincidental equality of orders or a few images is insufficient.

Why such a witness must exist in the present case
------------------------------------------------

The following additional argument explains the example's uniform structure.
It is not needed by the direct matrix certificate.

Proposition 3. Suppose G is centerless, [a,e]=[b,e]=1, and

  K=C_G(a,e),                 H=C_G(a,b).

If K is abelian and Z(H) is nontrivial, every <a,b,c,d,e>, c in K, d in H,
is proper in G.

Proof. Since e commutes with a and b, e belongs to H. For z in Z(H),
membership z in H gives [z,a]=[z,b]=1; centrality in H gives [z,e]=1.
Hence z belongs to the FULL centralizer C_G(a,e)=K. Since K is abelian,
z commutes with every c in K. It commutes with every d in H by centrality.
Thus

  Z(H) <= C_G(a,b,c,d,e)          for every c in K and d in H.

Choose 1!=z in Z(H). If those five elements generated G, z would belong
to Z(G), a contradiction. Notice that a and b need not themselves belong
to H: their commutation with z follows from H's definition.              QED

If every element of a group K squares to1, then K is abelian, since
xy=(xy)^-1=y^-1x^-1=yx. If a finite nontrivial group H has order2^r, its
center is nontrivial: in the conjugation class equation, every noncentral
class has size a positive power of2 greater than1, so |Z(H)| is even.
Since the center contains identity, its even cardinality is at least2.
These two elementary facts apply when |K|=|H|=512 and all511 nonidentity
elements of K are involutions. Under a faithful representation, a nonidentity
z supplied by Proposition 3 yields an ordinary matrix witness of Corollary2.
The direct check below removes the centerlessness/faithfulness hypotheses
from the final properness implication by verifying an actual ambient escape.

The retained original application
---------------------------------

The case comes from the project treatment of corpus manuscript F004:
Malcolm Hoong Wai Chen, Abstract regular polytopes of G2(q) in even
characteristic, arXiv:2609.25004v1 (2026). The original enumeration, named
group and its classification results remain the original author's work.
This package addresses only the project obligation labelled prefix621,
rank5, for the SAME original G2(8) action. It does not recover that entire
manuscript or establish a new conjecture.

A string C-marking of rank5 has generators (a,b,c,d,e). Its nonadjacent
generators commute, so every completion of the fixed original prefix has
c in C_G(a,e) and d in C_G(a,b). Thus Corollary2 covers the whole extension
domain once the full original centralizer bases have been identified.
The package contains their nine images each, together with the fixed images
in the explicit order a,e,b,K1,...,K9,H1,...,H9. It checks a witness against
ALL21 and checks an escape against one of the TWO ORIGINAL ambient images.

The complete finite image tables have orders512 and512 and contain511 and
119 nonidentity involutions. The checker recomputes those facts: each table
has identity and a topological word tree giving containment in its generated
group; every matrix is distinct; every right basis edge stays inside the
table. Since the basis matrices are invertible, this finite closed monoid
is the generated group. Squaring EVERY element gives all and only the
nonidentity involutions. The raw image-pair count is511*119=60809. Under
the retained faithful original correspondence, this is also the raw original
pair count. It is not an automorphism-orbit count or a class count.

All arithmetic uses the included actual GF8 tables. The new entrypoint
checks the field axioms on all8 elements, then uses exact borrowed matrix
and witness definitions. In this example the supplied X is

  [1 0 0 0 u 0]
  [0 1 0 0 0 u]
  [0 0 1 0 0 0]
  [0 0 0 1 0 0]
  [0 0 0 0 1 0]
  [0 0 0 0 0 1],

where u is field CODE3, not an integer scalar3. For the second original
ambient image, the products Xg and gX differ in entry(row1,column4): their
codes are3 and0. The checker verifies all these equalities and inequalities
with the actual included field tables; it does not infer them from a label.

What this package retains
-------------------------

The correctness of the representation on the ORIGINAL group, the original
membership/labels of the three fixed marks and two ambient generators, and
the equality of the supplied original bases with FULL C_G(a,e), C_G(a,b)
are retained premises. They were acquired separately using whole original
actions and centralizers. They are listed in provenance/retained_premises.json.
The present small package does not repeat that acquisition, reconstruct G,
run GAP, compare every original projective point, or prove a named-group
identification. Checking field axioms, matrix tables and a commutator does
not establish those original correspondences.

Subject to those premises, the certificate excludes every rank5 completion
of this prefix, including pairs not explicitly selected by the old accessor.
It does not prove a whole small-field census, rank6 statement or full F004
recovery. No manuscript compression factor, historical priority, new open
conjecture solution or Lean verification is asserted here.

Attribution
-----------

Centralizers, finite p-group centers and invariant separation in a
representation are standard. The project's Root coordinator identified the
uniform centralizer obstruction and proposed the ordinary commutant escape.
Navigation wrote the argument and witness kernel and prepared this portable
package. Final authored the reused field/matrix arithmetic, original-member
lifting and finite-table checker. Existing model/centralizer acquisitions
and original-paper results retain their prior attribution. The exact
definition spans and full Source hashes are recorded and checked in
provenance/source_derivation.json; no independent new implementation of
those borrowed definitions is claimed.
