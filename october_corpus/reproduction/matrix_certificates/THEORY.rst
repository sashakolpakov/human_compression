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

The common prefix and the new spectrum certificates
----------------------------------------------------

Put D=<a,b>, L=<a,b,c> and H=<a,b,c,e>. The acquired prefix has
|D|=12 and the exact full centralizer

  U=C_G(a,b)=C_G(a,b,e)=S={1,z,e,ze}, z=(ab)^3, |S|=4.

This full equality is imported from its accepted complete acquisition
and proof. Counting the three supplied involutions alone does not prove it.
The replay checks their actual prefix identities and involution equations.

Lemma (coprime subgroups in a parabolic). If P=Q semidirect M, where Q
is a finite p-group, every subgroup A of order prime to p is conjugate
by Q into M. Consequently C_G(A) contains a conjugate of Z(M).

Proof. Projection injects A into M. In the inverse image Q semidirect B
of its image B, the actual A and the standard B are complements to Q.
For clarity, the relevant complement conjugacy has a short proof.
Induct on |Q| and take the nontrivial characteristic elementary abelian
subgroup E=Omega_1(Z(Q)). Quotient induction first makes the two
complements equal modulo E. In E semidirect B a complement is the graph
of a cocycle f satisfying f(bd)=f(b)+b.f(d). Since |B| is invertible in
F_p, averaging gives f(b)=v-b.v for v=|B|^-1 sum_d f(d). Conjugation
by v in E identifies the complement with B. This proves Q-conjugacy.
Conjugating Z(M) back proves the centralizer inclusion. QED.

Both split maximal parabolics of G2(11) have an embedded GL2(11) Levi
and an 11-group radical. Their Levi centers have order 10. Since 12 is
prime to 11, a parabolic containing D would put such an order-10 group
inside C_G(D), of order 4. This is impossible. Thus the fixed prefix
excludes both parabolics before c or an adjacent order is considered.
The full split Levi, not a projective quotient, is used here.

Now C_G(L)=S intersect C_G(c). A nonidentity element of this intersection
also commutes with e, so H is contained in its proper centralizer and is
nongenerating. Otherwise C_G(L)=1, excluding every involution-centralizer
overgroup without any prior generation assumption.

For the new cases, the exact original a,b,e sign systems are checked.
Their eight kernel dimensions are 0,0,0,1,0,1,1,0 in lexicographic sign
order with signs 1,-1. The three nonzero kernels are spanned by the
three supplied prefix lines. Summing over the sign of e gives pair-sign
dimensions 0,1,1,1 for a,b. Since e commutes with a,b, every common
a,b line is consequently one of these three e-stable lines. Checking
that c moves all three therefore proves absence of a rational L-line.
No per-case rank computation or inference from a search miss is used.

The complete maximal cover now leaves only J1, G2(2), 2^3.PSL3(2) and
PGL2(11) for a proper L. Both G2(2) and 2^3.PSL3(2) have only the primes
2,3,7 in their orders, so neither contains a factor 5 or 11. The maximal J1 element
orders under divisibility are {6,7,10,11,15,19}; PGL2(11) orders divide
10,11 or 12. Thus an actual L-element order divisible by 5 or 11,
outside {5,10,11,15}, forces L=G. The order-5 cases are not excluded.
The same follows from 24-divisibility: the elementary exponent-two
kernel argument excludes 24 in 2^3.PSL3(2), and the faithful full G2(2)
embedding in GL6(2) excludes 24 there; J1 and PGL2(11) also lack it.
The GL6(2) proof uses an order-three semisimple constituent and a
unipotent order-eight block, requiring at least seven dimensions.
A cyclic subgroup with order divisible by 24 contains an exact order-24
power. With L=G the nonidentity omitted mark e violates IP as above.

The replay checks each carried order m directly: x^m=I and
x^(m/r)!=I for every prime r dividing m. The carried m divides 1320,
so the prime list 2,3,5,11 is complete. A mere annihilating multiple
would not suffice. Actual commutator coordinates are checked by their
nonzero matrix-entry differences, not by a producer verdict.

The two separate order-19 arguments
----------------------------------

The complete maximal cover says that a proper natural subgroup containing
19 lies in split SL3(11):2 or J1. Left-line absence excludes the first.
Only 19:6 among proper J1 maximal subgroups contains 19; it cannot contain
the actual Klein four <a,c>. Thus a left end with19 is J1 or G.
Elementary abelian Sylow 2 in J1 exclude an order-4 element. This proves
the separate position 3630 obstruction from its exact left 19 and 4 words.

For position 1556 let ell be the supplied nonzero line. The replay checks
that b and c preserve it and that bc has exact order 10, so D=<b,c> has
order 20 and fixes ell. If L=J1, orbit–stabilizer bounds the L-orbit of
ell by 175560/20=8778. A tree of 8779 distinct reachable lines excludes
that alternative. Each nonroot node has an earlier parent and one of
the actual left generator labels 0,1,2. The verifier checks the parent
image by direct field loops and canonical projective normalization.
Induction proves every line reachable; distinctness gives the lower
bound. Closure is neither supplied nor required. The left 19/J1-or-G
alternative then gives L=G and IP failure. No full right-unitary
identification, right 37 replay or full ambient orbit is needed.

Further attribution
-------------------

The full centralizer input has digest 9d2f9c739a8a5f42... . The complete
maximal cover is the retained Kleidman/Nguyen/Wilson input cited below.
Both split Levi factors are GL2 in Z. Lin, The Lyndon–Demushkin method
and crystalline lifts of G2-valued Galois representations, Algebra and
Number Theory 19(2025),415–456, publisher Sections 7.1.4 and 7.1.6,
doi:10.2140/ant.2025.19.415. The J1 spectrum is recorded in
Li–Moghaddamfar–Vasil'ev–Wang, arXiv:2312.07907v1, Lemma 3.9(2), and
the primary ATLAS record supplies the maximal/Sylow facts. The primary
ATLAS U3(3) page explicitly gives the faithful dimension-six GF2
representation for the FULL U3(3):2=G2(2).

Complement conjugacy, averaging, centralizers, rank and orbit–stabilizer
are standard. The shared prefix exclusion and these finite applications
are assembled here without a historical novelty claim. These remain
negative dispositions within the unfinished original classification.

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
