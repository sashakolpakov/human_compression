The acquired q11 Cayley algebra and its full automorphism group
=============================================================

This is a Source/theory implication, not a new execution or an amendment to
an existing acceptance.  The acquired normalization and invariance imply
inclusion.  An explicit published generating pair identifies the retained
matrix group as G2(11); the classical Cayley-frame count then proves equality.
No new permutation-group order calculation is required for this implication.

Let M be the matrix group used by the acquired q11 frame, and let C be the
eight-dimensional algebra recovered from the exact retained beta and tau.
Keep all three independent acquired premises:

* The frame identifies M faithfully with the exact saved permutation group,
  using both complete generator actions and the determinant-one projective
  frame.  This includes the provenance that M is the retained ChevalleyG(11)
  construction, not an arbitrary frame-matching pair.
* The direct forms certificate checks preservation of beta and tau by both
  actual generating matrices.  Nondegeneracy consequently gives preservation
  of T defined by beta(T(x,y),z)=tau(x,y,z).
* The normalization certificate checks the full quadratic cross-product
  identity and reports kappa=7.  Thus C has product
  (a,x)(b,y)=(ab-7beta(x,y), ay+bx+T(x,y)) and norm
  N(a,x)=a^2+7beta(x,x).  It is a split Cayley algebra over F11.

The first premise alone gives no Cayley identification.  The latter two
give diag(1,M)<=Aut_F11(C), but do not by themselves prove surjectivity.
Here and below M is identified with its extension fixing the scalar unit.

An exact published generator identification
------------------------------------------

Howlett, Rylands and Taylor, ``Matrix generators for exceptional groups of
Lie type'', J. Symbolic Comput. 31 (2001), 429--445, Section 3.6, printed
pages 11--12 of the author manuscript, give a degree-seven G2 representation.
For q not divisible by 3 and q!=2 its generators are h_A(mu), x_A(1)n,
where mu is primitive.  They derive the generation assertion from Steinberg's
Theorems 3.11 and 3.14.  Primary author manuscript:
https://www.maths.usyd.edu.au/u/bobh/hrt.pdf .

This is the relevant case q=11.  It can be joined to the literal installed
GAP constructor without assuming that its name or SetSize is a proof.
Use one-based matrix coordinates and ordinary matrix multiplication.  The
paper has

  h_A(mu)=diag(mu,mu^-1,mu^2,1,mu^-2,mu,mu^-1),
  x_A(1)=I+E12+2E34+E45+E67+E35,
  n=E13-E21+E36-E44-E52+E67+E75.

The seven rows of x_A(1)n are therefore

  -e1+e3,
  -e1,
  -e2-2e4+e6,
  -e2-e4,
  -e2,
  e5+e7,
  e5.

Set R=diag(1,1,1,1/2,1,1,1).  Conjugation R^-1(.)R fixes h_A(mu).
In the second matrix it changes just the two off-diagonal coefficients
(3,4): -2 to -1 and (4,2): -1 to -2.  These are exactly the seven rows of
the second generator in the retained p!=3 branch of GAP's ChevalleyG(q):

  -e1+e3, -e1, -e2-e4+e6, -2e2-e4, -e2, e5+e7, e5.

All seven rows, all signs and all zero entries agree.  Neither generator
is transposed or inverted: this compares the literal matrix groups under
ordinary multiplication, then uses the acquired right-row action bridge.
The first generator also agrees, since mu^(q-2)=mu^-1 and
mu^(q-3)=mu^-2.  The paper permits any primitive mu; GAP uses its inherited
PrimitiveRoot(GF(11)), so no particular field-element encoding is guessed.
This is a symbolic coefficient comparison, not an executed
matrix product or a check on sampled group elements.

Hence the retained constructor group is conjugate to the published G2(11)
group.  This removes any need to treat the nearby ``probably due to Don
Taylor'' comment, the constructor name, or its attached SetSize attribute
as the mathematical justification.  The shared finite-field primitive-root
and ordinary matrix software semantics remain inherited implementation
premises.  The faithful frame then transports this named group to the saved
permutation group.  No unseen historical octonion basis is needed.

Equality with the recovered Cayley automorphism group
----------------------------------------------------

The retained Wilson book proves, in Sections 4.2.2--4.2.3 of the preliminary
edition (physical pages 116--118, numbered 102--104), that automorphisms of a
split Cayley algebra over an odd finite field act simply transitively on
its ordered norm-one Cayley frames.  Counting those frames gives

  |Aut_Fq(C)| = q^6(q^6-1)(q^2-1) = |G2(q)|.

Concretely the three choices have counts q^3(q^3+epsilon),
q^2(q^3-epsilon), q(q^2-1), with epsilon=+/-1 according to q modulo 4.
This is the classical frame/order theorem, not a consequence of the new
forms verifier.  Every finite-field Cayley algebra here is split; the
existing normalization proof supplies that hypothesis, including its norm
scale.  Wilson's published edition renumbers these sections 4.3.2--4.3.3.
The author's book/errata page is
https://webspace.maths.qmul.ac.uk/r.a.wilson/TFSG.html .
Its trace-versus-real-part correction does not change this argument: use
the explicitly normalized N and its full polar form 2*7beta throughout.

The inclusion M<=Aut_F11(C), the generator theorem, and the displayed common
finite order prove M=Aut_F11(C).  The retained historical model-preparation
stdout already records the same numerical order 376611192619200, but it is
not needed as a new recognition certificate.  Conversely, if one declines
either the exact constructor-to-frame provenance or the published generator
theorem, normalization plus invariance still yields only inclusion.  Then an
authenticated full-order lower bound or a generating-root certificate would
remain owed; guessing equality from the forms would be invalid.

What the eight-class frame argument now supplies
-----------------------------------------------

The existing odd_alternating_frames_over_finite_fields.tex proves a separate
statement from classical Cayley-frame facts: ordered embeddings C2^3 into
Aut_Fq(C) have eight rational inner-conjugacy classes, indexed by the three
norm squareclasses of labelled frame generators.  This eight-class count
is the existing local proof, not a claim that the cited generator paper
states it or that we have discovered a new theorem.  Its elementary frame
proof does not require the optional Lang-descent argument.

Under the equality above it applies to this actual matrix group, hence to
the saved permutation group through the paid faithful bridge.  Its norm is
the acquired canonical N(1)=1, with pure norm 7beta, so the earlier arbitrary
scalar/squareclass ambiguity is resolved.  The seven pure-character norms
must be computed using 7beta, not an unnormalized beta.  All eight ordered
types remain; the two unlabelled subgroup types or their normalizers do not
replace the ordered domain.

Actual coordinate representatives have not been acquired by this note.
The smallest remaining certificate for using this reduction is eight actual
Cayley frames with prescribed three norm squareclasses.  For each, verify
the basis determinant, the required orthogonalities and products, the three
labelled sign maps and their induced action in the retained coordinates.
Their membership in M would then follow from the proved equality and their
algebra-automorphism property; a large permutation enumeration is unnecessary
for that membership conclusion.  Any use in an old finite census still owes
the exact original-label transport, complete remaining centralizer domains,
weights/positive tuples, and generation/IP predicates.  This note certifies
no representative coordinates, old-inventory coverage, candidate or census.

Exact retained joins
-------------------

The following digests fix the local premises.  Their referenced scientific
coefficient/point tables were not opened or hashed in this assessment.

* Cayley acceptance small_inventory_work/cayley_normalization_acquisition/
  root_acceptance.json: 112192 bytes,
  208431dc9dd0ec31b7688719e12def55682dd35a085f088ba2cd32d34fdde940.
  Its result pin is 47c4f9848a304b7ca821db38271f85e672f29f241790a2203e2ace19307d25a1.
* Direct-forms acceptance small_inventory_work/invariant_forms_acquisition/
  root_acceptance.json: 78082 bytes,
  0ab1b853480874ef685a807d5c72d5f98fba22894e7b5727e7cb6815d0cc1d36;
  result e7a1cc462587152fa838ec8a616cc548442463f8756ba912aadb52e25610447e.
* Faithful frame small_inventory_work/matrix_frame_root_acceptance.json:
  3394 bytes, a8746058d9d1482ac9ed92157f31b765c0998d195efc312d734a8533ddc86498;
  result b6259de58ace64a7bccf97db50e81e4686c5f6f501c3263c86186fadb09e8391.
* invariant_tensor_cayley_normalization.tex: 12530 bytes,
  999a3bcd33b719731cf225fd84b3d9cff8efeae6bd4e87fda134c15f1695a48f.
* odd_alternating_frames_over_finite_fields.tex: 19181 bytes,
  89aaf643b59bb14cacc0d5a391ff48c6b4c51cdc9775d15d819db260db7c9207.
* /opt/homebrew/Cellar/gap/4.15.1/share/gap/grp/simple.gi:
  42745 bytes, 2c5eae2c20cec69425308377f73f9e5bfc256a931f4a8c2daaa67e4a644fbb25;
  ChevalleyG is lines174--239 and the q11 constructor route lines595--612.
* Retained wilson_early_book.txt: 633091 bytes,
  d0af6d76130d73a143e76218c7c66ca0167d06f70d591f9c3482ec8e04fe895f;
  the relevant source is lines5071--5176 with explicit physical-page markers.

Author: /root/unit_actual_review.  Unit previously authored tensor/producer
support and reviewed the Cayley arithmetic acquisition; those are borrowed
scientific premises, not independently replayed arithmetic here.  This work
read only proof/library Source, primary published statements and bounded
acceptance metadata.  No scientific, model, group, field, Reader, worker,
control, validator or process call, manuscript build, state or adoption ran.
