Independent review of the Suzuki rank-four construction
======================================================

Verdict
-------

I accept the mathematical construction in author manifest
738b45d441fa6634360450e52755820989c5f41991ec5e46501e6522f2e86fbd.
It gives a chiral abstract polytope of rank four and type {31,31,25}
whose full automorphism group is Sz(32768), under the explicitly retained
Suzuki structure and polytope reconstruction theorems. It is a counterexample
to Theorem 1.1 of the specified arXiv:2010.04080v1 edition. This review does
not assert priority against subsequent literature, a later-edition defect,
Lean formalization, or any compression measurement. Whole-original admission
and the attribution audit remain the root's separate responsibility.

I am distinct from the author and made no contribution to the construction,
the new Bruhat argument, or its source-coordinate diagnosis before review.
Root contributed to the source diagnosis and supplied the basis permutation,
so root's further adoption is not represented as the independent review of
those ideas. I previously reviewed an earlier partial F003 coefficient lemma;
that lemma is not a premise of this construction.

I read the full five-page manuscript, the complete standalone arithmetic
checker and its operational wrapper, the retained proper-face proof and its
earlier distinct review, the whole four-page target preprint, the coordinate
paper's actual matrix and Bruhat definitions, and the rank-four reconstruction
and chirality criterion in LMO Section 2. I viewed all five freshly rebuilt
manuscript pages and five relevant primary-source pages directly.

Field and matrix calculations
-----------------------------

The author's polynomial arithmetic is exact binary polynomial multiplication
modulo X^15+X+1. Its irreducibility checks are the degree-fifteen Rabin tests:
X^(2^15)=X modulo the polynomial, and gcds with X^(2^5)-X and X^(2^3)-X
equal one. Those are precisely the prime-divisor tests for degree fifteen.
The three primitive-root tests cover 32767=7*31*151. Eta=z^1057 therefore
has order 31 and generates the canonical field K of 32 elements. Lambda is
specified as a polynomial in z; it lies outside K. Its displayed cubic over
K vanishes, and the extension degree three makes this its minimal polynomial.

All matrices are products of the displayed standard U, H and J matrices.
Consequently their membership in G is established by construction, not merely
by passing necessary polynomial equations. Restricting theta=256 to K gives
the correct exponent eight. The matrices u and v0 belong to F=Sz(K), and h
is an element of the ambient split torus. The order tests distinguish exact
orders 31, 31 and 25: nonidentity excludes the proper divisors of 31, and
c^5 != 1 excludes both proper divisors of 25. The three product involutions
are also explicitly nonidentity.

I wrote a separate GAP reconstruction using GAP's native GF(2^15), selected
a root of X^15+X+1, and reconstructed the matrices from the printed formulas.
It does not import the author's Python arithmetic or its search output.
It recovers all six orders [31,31,25,2,2,2], the printed field elements and
both displayed involutions, the symplectic and Suzuki equations, the small
parabolic intersections, and the source diagnostic. The run completed in
1.943 seconds with exit zero, unchanged code and empty stderr.

As a separate check on face generation, I constructed the complete standard
1025-point Suzuki ovoid over K and computed the actual permutation actions
of <u,b> and <v0,b>. Each action is transitive and has order 32,537,600,
which is 32^2*(32^2+1)*31. Since the matrices already lie in F, an image
of that full order confirms that each subgroup is F. This is a new finite
reconstruction with different field arithmetic and group algorithms, not
a second invocation of the author's checker. The written face proof below
does not require this extra diagnostic.

Face generation and full ambient generation
-------------------------------------------

At q=32, a proper subgroup containing the element b of order 31 must, by
the retained maximal-subgroup classification, lie in a point stabilizer or
the normalizer of a split torus. The other possible maximal orders are 100,
164 and 20, none divisible by 31. The only point stabilizers containing b
are those of its two fixed ovoid points; they are triangular in the displayed
coordinates. A split-torus normalizer containing b has its unique subgroup
of odd order 31 equal to <b>, hence is the normalizer of this actual standard
torus. That normalizer is diagonal or antidiagonal. The printed u and v0
are in none of these possibilities. Thus <a,b>=<u,b>=F, and, because h
centralizes b, <b,c>=hFh^-1. There is no assumption that an arbitrary
abstractly isomorphic face is the canonical subfield group.

For g in F intersect hFh^-1, both g and h^-1*g*h have entries in K.
If g is in the second Bruhat cell, its (1,4) entry is nonzero. Conjugation
scales that entry by lambda^-514, so lambda^514 lies in K. This is impossible:
514 is coprime to 32767, and the inverse power expresses lambda as a power
of an element of K. Thus g is in the lower-triangular cell U(x,y)H(t).

Direct diagonal conjugation gives U(x*lambda^256,y*lambda^258)H(t).
The result still belongs to the triangular cell of F, and uniqueness of
the root and torus parameters puts both root parameters in K. If x is
nonzero, lambda^256 would lie in K; if x=0 and y is nonzero, lambda^258
would lie in K. Both exponents are coprime to 32767. Hence x=y=0.
Conversely H(K) commutes with h and is contained in both faces. This proves
F intersect hFh^-1=H(K)=<b>, exactly, for every element of the two groups.
The argument does not infer an intersection from element samples or group
orders alone.

The canonical F is maximal in G because 15/5=3 is prime, by the declared
Suzuki subfield theorem. Its conjugate is distinct: their intersection has
order 31, smaller than |F|. The rotations therefore generate a subgroup
strictly containing F and hence the entire G. No ambient group census is
required; the large ambient order is obtained from the classical formula.

Intersection property and chirality
----------------------------------

The actual cited LMO page four explicitly gives the rank-four criterion C3':
<a> intersect <b>=1, <b> intersect <c>=1, and the two face groups intersect
in <b>. I checked this in the primary PDF, together with relations C1/C2
and the following reflection-extension criterion. Thus the manuscript is
using the appropriate rotation intersection condition, not the involutory
string C-group condition for a different generating system.

The first cyclic intersection is trivial because both cyclic groups have
prime order 31: equality would put ab in an odd-order group, contradicting
its order two. The second is trivial since gcd(31,25)=1. The full face
intersection was proved above by Bruhat coordinates. These are all three
conditions of C3', so the reconstruction theorem applies. For additional
control, the independent GAP reconstruction also verifies the other two
rank-three parabolics <a,bc> and <ab,c>, of orders 62 and 50; their mutual
intersection is <abc>, and their intersections with the large faces are
exactly the asserted cyclic subgroups. These additional finite checks are
not substituted for the full face-intersection proof.

Any reflection extension would induce an automorphism alpha with
alpha(a)=a^-1, alpha(b)=a^2*b and alpha(c)=c. Applying these assignments
twice fixes all three generators, so even if the criterion were formulated
without the word involutory, such an automorphism would have order at most
two. It is nonidentity because a has odd order 31. Its image in Out(G),
of odd order 15, is trivial. It is therefore conjugation by some s in G.
Since G is centreless, alpha^2=1 forces s^2=1; since alpha is nonidentity,
s is an involution. But alpha fixes c, whereas the centralizer of the
nonidentity odd-order element c has odd order. No such s exists. This
establishes chirality and, by the reconstruction theorem, the stated full
automorphism group, not merely the existence of an abstract rotation triple.

Source diagnosis and precise edition boundary
---------------------------------------------

The basis permutation P=(1 2)(3 4) preserves J. Conjugating the old pair
order (12,13,24,34), including its output-coordinate permutation, gives
(24,12,34,13), exactly the source's Wilson product order. This explains
the model change algebraically; the finite checker also verifies it on
every relevant matrix. The normalizing matrix is constructed from U and H
and sends abc to J. The resulting inverse first rotation is symmetric and
satisfies xJx=J. Both independent arithmetic systems give the nonzero
equation-13 residual 28331 in the specified polynomial basis.

The target source's page two restricts Wilson invariance to symplectically
orthogonal pairs. Its page three imposes that identity also on (e1,e4) and
(e2,e3), each with symplectic pairing one. The displayed counterexample
satisfies the valid orthogonal identities and fails the extra imposed one.
The map x -> xJ also bijects the set xJx=J with the identity and all
involutions, yielding (q^2+1)(q-1)+1 elements, whereas the source's displayed
classification gives q. The defect in that intermediate argument and the
rank-four polytope counterexample are separate conclusions; the latter
additionally requires all generation, intersection and chirality steps above.

The review is limited to the fixed preprint edition actually read. It makes
no assertion about later versions or whether a correction or this example
already appears elsewhere. There is one minor bibliographic locator error:
the Recognition reference ends with Section 2, but its displayed matrices
and Bruhat formulas are in Section 1, physical page one. This should read
Section 1 in the publication edition. It does not affect the theorem or the
bound source, and the frozen author packet has not been altered.

Evidence and remaining responsibility
------------------------------------

The fresh author replay verifies all eleven exports, ten external bindings,
eight operational scope controls, exact arithmetic equality and all five
native page texts. The independent GAP program and its complete clean receipt
are retained separately. Every new native page was directly viewed, as were
LMO pages three and four, target pages two and three, and the coordinate
source's first page. The whole four-page target was read in extraction too.
The exact finite computations and classical structural/reconstruction
theorems remain explicit premises. No Lean kernel verification is claimed.
The next step is a root adoption and precise correction record for F003,
with earlier partial results preserved as historical work rather than
misrepresented as a proof of the now-refuted all-field assertion.
