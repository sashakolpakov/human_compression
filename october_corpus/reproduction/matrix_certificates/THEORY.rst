Invariant lines and the original quartets
========================================

Setting
-------

Let G be the original acquired group, represented on V=F_11^7 using row
vectors. The original prefix and the Cayley catalogue associate each
indexed original quartet with actual matrices (a,b,c,e) in G. The original
model/member, faithful-frame and orbit/member/transport results are
borrowed. The finite replay reconstructs the requested matrices and
checks their equations; it does not reprove those imported associations.

A common invariant line
-----------------------

Lemma. Suppose v is a nonzero row and each of a,b,c,e sends v to a nonzero
scalar multiple of v. If a known member z of G does not preserve the line
L=span(v), then <a,b,c,e> is a proper subgroup of G.

Proof. Products and inverses of line-preserving transformations preserve
L. Thus <a,b,c,e> is contained in the line stabilizer G_L. The supplied
member z lies outside G_L, so G_L is proper. This proves nongeneration.
It asserts nothing about the quartet's intersection property. Faithfulness
is unnecessary for the abstract implication; the imported faithful frame
serves the original-case association. QED.

The 273 nongeneration certificates use three explicit prefix lines; every
case carries all four scalars and an acquired ambient generator moving its
line. These are standard stabilizer arguments, with no classification or novelty claim.

An order-37 word and its unique line
-----------------------------------

Lemma. An element Y of exact order 37 in GL_7(F_11) has a one-dimensional
fixed space, which is its unique invariant F_11-line.

Proof. The order of 11 modulo 37 is six: 11^2=10 and 11^3=-1 modulo 37.
Every nontrivial irreducible factor of X^37-1 over F_11 therefore has
degree six. The polynomial is separable. A nonidentity Y with Y^37=I
must have a nontrivial six-dimensional constituent; dimension seven
leaves exactly one trivial constituent. Its fixed space consequently has
dimension one. On any rational invariant line, Y acts by a scalar whose
order divides both 37 and |F_11^*|=10. That scalar is one, so every such
line is the fixed line already found. QED.

Imported classification statement. In the acquired natural G2(11)
module, every proper subgroup containing an element of order 37 lies
in a maximal subgroup of type SU_3(11):2. The full normalizer, including
its outer half, preserves a nonisotropic rational line. The complete
maximal cover, rather than an irreducibility-restricted list, is needed
for this statement.

Proposition. Let H be one actual end, <a,b,c> or <b,c,e>. Suppose a word
in those same generators yields W, with Y=W^3 nonidentity and Y^37=I.
If an original generator of that same end moves the fixed line of Y,
then H=G.

Proof. Exact order 37 follows from the two displayed tests. If H were
proper, the imported maximal-overgroup statement would give an H-invariant
line. It would be Y-invariant and hence the unique fixed line in the
lemma. The supplied generator moves that line, a contradiction. QED.

Corollary. Such an end proves failure of the original rank-four
intersection property.

Proof. A full left end contains the omitted nonidentity mark e. Therefore
<a,b,c> intersects <e> nontrivially, although the two generating-label sets
are disjoint. The required intersection is the trivial subgroup. The
right-end case uses the omitted mark a in the same way. QED.

The replay finds a left fixed row independently and then explicitly
checks the fixed-row equalities and a nonzero two-coordinate movement
minor. It checks literal same-end word membership, including the cofactor
three. A word of order 37 in the whole quartet or a different end would
not justify this proposition.

Original orbit association
--------------------------

The retained indexed orbit/member/transport bridge supplies the original
representative corresponding to each J index. Conjugation carries a
generated subgroup and its invariant line together, and preserves both
properness and the intersection property. This transfers the certified
representative disposition to its original orbit. The same vector need
not be fixed by every transporter. No new orbit census is asserted.

A supplied row and a six-minor
-----------------------------

Lemma. Let Y be a 7 by 7 matrix over F_11. If a nonzero row v satisfies
vY=v and a 6 by 6 minor of Y-I has nonzero determinant, then Y-I has rank
six and its left kernel is the line spanned by v.

Proof. The nonzero minor gives rank at least six. The displayed nonzero
left kernel row gives rank at most six. Equality follows, and rank-nullity
gives a one-dimensional left kernel. QED.

The new certificates specify the row and both sets of minor indices.
The replay checks the row equation and evaluates the determinant as the
signed sum of its 720 permutation products. This uses no row reduction.
The determinant term count is separate from the inherited RREF operation
counter. Together with the exact order 37 checks and the same-end mover,
the lemma supplies precisely the fixed-line certificate used above.
It introduces no additional classification input or novelty claim.

References and borrowing
------------------------

The complete odd-characteristic maximal-subgroup classification is due
to P. B. Kleidman, The maximal subgroups of the Chevalley groups G2(q)
with q odd, the Ree groups 2G2(q), and their automorphism groups,
J. Algebra 117 (1988), 30--71, doi:10.1016/0021-8693(88)90239-6.
The retained project proof uses the full list in the proof of Theorem 4.4
of H. N. Nguyen, Irreducible restrictions of Brauer characters of the
Chevalley group G2(q) to its proper subgroups, arXiv:0910.4994, before
its later character exclusions. R. A. Wilson, The Finite Simple Groups,
retained author edition, Section 4.2.6, supplies the natural Cayley
line-stabilizer description, including the full outer normalizer.

The fixed-line, stabilizer and omitted-mark arguments are standard or
retained prior project arguments. The original group and frame data are
borrowed mathematical inputs. This package assembles their explicit
finite certificates and a portable arithmetic replay. It claims neither
new classification nor mathematical priority, and supplies no Lean
verification or whole-manuscript recovery.
