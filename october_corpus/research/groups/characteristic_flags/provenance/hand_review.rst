Independent hand review of characteristic endpoint geometry
===========================================================

Reviewer: /root/f004_flag_proof_review.
Mathematical author: /root/f004_uniform_prefix_theory.
Corrected edition editor: /root.
Disposition: SUPPORTED_WRITTEN_THEORY_WITH_EXPLICIT_APPLICATION_PREMISES.
No mathematical blocker remains in the exact corrected edition reviewed.

Exact scope and history
-----------------------

This review is bound to editions/v2/characteristic_flags.tex, 23,811 bytes,
SHA256 0a9fe51824de83505cae69961d01c6dfaaba329d7a6c152fe34876010cc37bba,
and its 2,011-byte provenance,
SHA256 dc5285c4e039fb38ea150b69f9f61192390dbd77233cb756eb3551bdf070d885.
The original 23,804-byte manuscript 4cc03dc6... and 10,185-byte author
provenance 8fd41675... remain unchanged and are retained as history.
The exact two textual replacements and their inverse reproduce both complete
manuscripts. They correct an auxiliary source matrix description and avoid
an unintended iff after equation (12). They do not change the main proof.
The initial manuscript is not retroactively claimed to contain those fixes.
The companion assessment gives all full source and subject pins.

I read the entire corrected proof, its original provenance, the existing
canonical-vector note and the retained extracted Chen source. This is a
substantive mathematical hand review. No project program was imported,
executed or tested; no group/point/finite-field/matrix kernel, native or
runtime probe, Source/guard/ledger operation, TeX compiler or Lean checker
was run. Only bounded source/metadata reads, identity hashes, exact textual
comparisons and these independent review artifacts were used. Symbolic
identities below were checked by hand. There is no machine-proof claim.

Borrowed theory and field hypothesis
------------------------------------

Theorem 1 of the existing project note Canonical fixed vectors in
characteristic two is the reused ingredient. Its precise claim and coordinate
formula are sufficient here: a self-adjoint operator P over a perfect field
of characteristic two has a unique w(P), with
beta(x,w(P))^2=beta(x,Px), lying in im(P) and equivariant under linear
isometries. Inverse Frobenius makes the square-root functional k-linear;
nondegeneracy identifies it with a vector. Perfectness is an actual
hypothesis, not a claim about an arbitrary imperfect field. Alternating beta
is symmetric in characteristic two, so the borrowed theorem applies.
Linear isometries, rather than semilinear maps, are essential to the stated
pointwise invariance. The new note properly attributes this construction and
makes no historical-priority assertion for standard linear algebra.

Wall forms and the two endpoint lemmas
--------------------------------------

For an isometric involution s, s*=s^{-1}=s, so N=s-I is self-adjoint and
N^2=0. Consequently (im N)^perp=ker N. The Wall form
h(Nx,Ny)=beta(x,Ny) is independent of the representatives in both arguments,
symmetric and nondegenerate by exactly the kernel argument in the text.
Because c_s lies in im N, its defining equation gives
h(u,c_s)^2=h(u,u) on the Wall space. No normalization factor is missing.

For rank N=3 in dimension six, image, kernel and its beta-orthogonal
complement coincide. The three-dimensional nondegenerate symmetric Wall
form cannot be alternating, so c_s is nonzero. Substituting c_s into the
last identity gives h(c_s,c_s)^2=h(c_s,c_s), hence norm zero or one. If the
norm were zero, the restriction to c_s^perp would be alternating on a plane
with radical exactly kc_s, and therefore rank one. Alternating forms have
even rank over any field. Thus the norm is exactly one. The orthogonal
complement W is a nondegenerate alternating plane, with the asserted
orthogonal decomposition kc_s plus W. This checks the critical normalization.

For commuting maximal endpoints, N preserves U=im M=ker M and has kernel
P intersect U there. Thus rank(NM)=3-d for d=dim(P intersect U). The product
image lies in both P and U; 3-d<=d forces d=2 or 3. In the distinct-image
case, L=im(NM) is a line. E restricts to a Wall isometry on P, so M|P is
self-adjoint, square zero and has image L. Hence h_A(Mu,Mv)=0. This proves
isotropy for h_A, not merely for beta. Repeating the same argument with A,E
interchanged proves isotropy for h_E separately. Each endpoint fixes the
other's characteristic vector, so both vectors lie in P intersect U. Their
Wall norms are one, so neither is in L. Both asserted descriptions of the
common plane follow. In particular the independent-vector case is retained;
no false assertion of proportionality is used.

Main theorem: the moving branch
--------------------------------

Every mark except B=t_1 centralizes A and fixes c_A. If B fixes c_A too,
the first fixed-vector alternative is proved. Otherwise use the Wall form
of E on U, put c=c_E and decompose U=kc orthogonal to W. Both A and B
centralize E, fix c and preserve W. The image of (A-I)|U is L. Its
self-adjointness and its killing c put L in W. Its restriction to W is
nonzero, square zero and rank one, with both image and kernel equal to L.

The common-plane description writes c_A=a c+b ell with ell nonzero in L.
The coefficient a is h_E(c_A,c_E), and a cannot vanish because c_A is not
in L. The moving assumption makes B|W nontrivial. Its difference has its
own image/kernel line L_B, different from L: equality would make B fix ell
and therefore c_A. No implicit division by b is required.

For R=(AB)|W, a fixed vector w would satisfy Aw=Bw. Both differences then
lie in L intersect L_B=0, so w lies in both kernel lines and is zero. Since
R is symplectic on a plane, det R=1. Its polynomial is X^2+tau X+1, and
det(R-I)=tau in characteristic two. Thus tau is nonzero. Cayley--Hamilton
annihilates W. On kc, g=AB acts as the identity, and the same polynomial
acts by 1+tau+1=tau. Applying it to c_A yields exactly
(g^2+tau g+I)c_A=a tau c_E. Both factors being divided by are nonzero.

The penultimate mark D=t_{r-2} commutes with A and B when r>=5: its distance
from B is r-3>=2. It fixes c_A and commutes with g, hence fixes the left
side of that identity and therefore c_E. Every other mark equals E or
centralizes E, so also fixes c_E. This proves the second alternative.
The equal-image case is the separate common-Lagrangian argument: every mark
centralizes at least one endpoint and preserves their common image. Both
alternatives imply reducibility. Neither intersection property, independence
of marks nor faithfulness is used. The rank-five threshold is checked at
the exact place where it is needed, with no rank-four claim.

Algebraic witness and scalar powers
-----------------------------------

The canonical-vector image of self-adjoint elements in k[A,B] is a subspace:
w(alpha^2 P+gamma^2 Q)=alpha w(P)+gamma w(Q). The common symplectic
centralizer fixes it pointwise. This yields the general prefix criterion
because only the penultimate mark can fail to centralize E, and that mark
centralizes A,B. The additional fixed-image equations from the older project
criterion are therefore unnecessary in this specific use. This is a new
application of the borrowed construction, not a reproof of its authorship.

For g=AB, all P_i=g^i(A-I)g^{-i} are self-adjoint and belong to k[A,B]:
inverse words are still words since A,B are involutions. Equivariance gives
w(P_i)=g^i c_A. With the coefficients tau^2 and divisor (a tau)^2 as
printed, inverse Frobenius gives
w(P)=(g^2 c_A+tau g c_A+c_A)/(a tau)=c_E.
The squares in equation (12) are necessary and are correct. The new wording
states nonvanishing in the moving branch, without claiming an iff.

The coordinate identity P^T J=JP says JP is symmetric. Its off-diagonal
terms cancel, so beta(x,Px) has diagonal coefficients diag(JP), and
w(P)=J^{-1}sqrt(diag(JP)). Thus the two equations in (11) plus an actual
word expression certify w(P)=c_E. They are linear in the word coefficients
for a fixed word list. An incomplete failed word search is rightly assigned
no negative conclusion. Completeness of an algebra basis is unnecessary for
one accepting witness.

Mixed ranks and the abstract example
------------------------------------

For ranks two and three with nonzero commuting product, N|U is a nonzero
square-zero operator on dimension three and has rank one. Its Wall image
line L is isotropic, whereas h_E(c_E,c_E)=1. The rank-two image P is not
contained in U because MP=L is nonzero; P intersect U=L. Thus c_E is not
in P, and A fixes c_E. The plane P is beta-isotropic and c_E belongs to
P^perp, so Z=P+kc_E is a Lagrangian. Its stated intersection and rank-one
actions follow. This configuration by itself gives no invariant subspace
for all intermediate marks; the note does not claim otherwise.

The separate J4/permutation example correctly realizes independent endpoint
vectors: J4^2=I, the two commuting double transpositions have rank-two
differences, common image line k1, product 11^T, and canonical vector 1.
The orthogonal plane extensions contribute sqrt(a)e and sqrt(b)e and make
the full endpoint vectors independent when a,b are distinct and nonzero.
That example is conditional on being able to choose such a,b; it is not an
example over F2. The main theorem itself includes F2, and does not depend on
the existence of this example over every perfect field.

Source boundary and its corrected row convention
-------------------------------------------------

The retained extracted Chen edition explicitly uses rows and fixes y4=1.
On its quotient in basis (y1,y2,y3,y5,y6,y7), the form is antidiagonal.
The displayed first/last matrices give precisely the rank-two/rank-three
pair (13), with nonzero commuting nilpotent product lambda E25. The source
parameter zeta has order q+1 with even q>2: its trace lambda is in Fq,
nonzero, and unequal to one. These hypotheses are retained rather than
replaced by an arbitrary parameter.

In the row convention, the images are P=<e3,e5>, U=<e4,e5,e6>, and
beta(x,x(A-I))=0 while beta(x,x(E-I))=x1^2. Thus c_E=e6 and
Z=<e3,e5,e6>. The second source matrix swaps e2/e3 and e4/e5, moving P,Z.
The corrected fourth matrix is (1 6)(2 4)(3 5), as read from the original
seven displayed rows after quotienting y4. It sends U to <e1,e2,e3> and Z
to <e1,e3,e5>, so the intended noninvariance claims remain true. The original
manuscript's description of it as the six-dimensional antidiagonal matrix
was wrong; v2 corrects that exact auxiliary error. The original source's
Theorem 1.1 supplies generation and the C-string property; those statements
are imported, not proved by this note.

The contragredient g -> rho_row(g^{-1})^T is a homomorphism for the column
representation. Plain transposition on arbitrary group products would be
an antihomomorphism; on the involution marks the stated contragredient does
reduce to transposition. Ranks, endpoint commutation and zero/nonzero
nilpotent product are preserved. Coordinate subspaces must be transported,
not identified by their row coordinate labels. The note now respects that
boundary. The source construction rules out an indiscriminate mixed-rank
nongeneration theorem, without contradicting the maximal-endpoint theorem.

Projective lemma and finite application conditions
--------------------------------------------------

For an actual linear involution over an even finite field, a preserved line
has an eigenvalue lambda with lambda^2=1, hence lambda=1. Its fixed lines
are exactly those of ker(s-I). Rank-nullity and division of the nonzero
vectors by q-1 prove formula (14). The values 37449,73,585,9 and the
strictly increasing inverse rank test are correct. For the commuting
rank-three pair, common fixed lines are those of H: dimension three gives
73 and dimension two gives 9. One asymmetric fixed point also distinguishes
the Lagrangians once both endpoint rank premises are known.

These are conditional facts about ALL projective lines of the stated linear
representation. A permutation action's numerical degree or orbit size does
not supply an equivariant projective identification. No actual count,
endpoint rank/product, second-generator image, family coverage or original
job completion is established by this note. The exact common original group,
model, membership, representation, field, ordered endpoints and ambient
escape premises remain necessary. Semilinear outer automorphisms retain
their separate transport requirements.

The original-group corollary is valid for a nonfaithful representation:
generation would imply generation of the image. A retained ambient diagonal
matrix without an entry equal to field one has invertible d-I and supplies
both fixed-vector escapes in the distinct-image case, PROVIDED its original
ambient membership and common model correspondence apply. Those remain
imported premises. In the equal-image branch an escape from the common
Lagrangian is separately required. No new acquired instance, operational
Source acceptance, Lean certificate, conjecture solution, field census or
compression factor follows from this written theorem alone.
