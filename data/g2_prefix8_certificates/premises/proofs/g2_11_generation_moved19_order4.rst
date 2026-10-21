An order19 word, a moved line, and an order4 word
================================================

Written mathematical Source, C5 (/root/c5_terminal_audit), 20 October 2026.
This is a corollary of the existing maximal-subgroup classification, not
a new classification or a claim of historical priority. No group, field,
matrix, word, model, Reader, control or scientific function was evaluated.
No actual marking, end subgroup, original prefix or census is decided.

Statement
---------

Let C be the split Cayley algebra over F11, let V=C_0 be its pure
seven-dimensional space, and use the natural group G=Aut_F11(C)=G2(11).
Let H=<h_1,...,h_r> <= G. Suppose actual H-words evaluate to Y and X with

  Y != I,  Y^19=I,                  X^4=I,  X^2 != I.

Let v be a nonzero row with vY=v. If some actual generator h_j moves its
line, equivalently some s<t satisfies

  v_s (v h_j)_t - v_t (v h_j)_s != 0,

then H=G. No involution, intersection-property or irreducibility
assumption on the generators is needed for this generation conclusion.

The natural action and the full group identity are hypotheses. Merely
having seven-dimensional matrices, an invariant symmetric form, an
abstract group label, or an unjoined catalogue does not establish them.

Complete order19 overgroup check
-------------------------------

The complete odd-characteristic classification is due to Kleidman [K].
We use its full list, restated explicitly in Nguyen [N], proof of
Theorem4.4, printed pp10--11, BEFORE the representation-degree exclusions.
The shorter conclusion of that theorem has cross-characteristic
hypotheses and is not the list used here. At q=11 the types relevant to
the divisibility check are as follows:

.. list-table:: Complete divisibility check
   :header-rows: 1

   * - Maximal type or possible envelope
     - Prime divisors of its order
   * - Either maximal parabolic
     - 2,3,5,11
   * - (SL2(11) circle SL2(11)).2
     - 2,3,5,11
   * - 2^3.L3(2)
     - 2,3,7
   * - SL3(11):2
     - 2,3,5,7,11,19
   * - SU3(11):2
     - 2,3,5,11,37
   * - PGL2(11)
     - 2,3,5,11
   * - G2(2)
     - 2,3,7
   * - J1
     - 2,3,5,7,11,19
   * - L2(8):3 or PGL2(13), if retained
     - 2,3,7 or 2,3,7,13

There is no proper subfield group because11 is prime. Characteristic2
and3 exceptions do not apply. The last row deliberately retains larger
envelopes of the two exceptional L2 possibilities: even without their
field-congruence exclusions, neither contains19. Thus the conclusion
does not depend on pruning those exceptions. In particular every proper
H containing Y lies in a maximal subgroup of type SL3(11):2 or J1.
Both alternatives really have19; J1 must not be silently discarded.
Conjugacy-class uniqueness of either maximal type is not required.

The geometric input is the natural Cayley description of SL3(11):2.
Wilson's retained book, Section4.2.6, printed pp107--108 [W], identifies
it as the full stabilizer of a pure nonisotropic line of norm class-1.
The connected SL3 factor acts naturally and dually on two three-spaces;
the outer half interchanges them and may negate the fixed vector.
Consequently the full normalizer preserves the LINE. All its conjugates
do so. The characteristic3 extra embeddings discussed there are
irrelevant at q=11. Checking only a common fixed vector would miss the
outer sign and would be insufficient.

Why the order19 line is unique
-----------------------------

The following argument also explains the natural-module guard. Let Y
be a nonidentity order19 isometry of a nondegenerate symmetric form on
a seven-dimensional F11-space. Since19 is prime to11, Y is semisimple.
The order of11 modulo19 is3: 11^2=7 and11^3=1 modulo19. Every nontrivial
irreducible factor of t^19-1 over F11 therefore has degree3.

None of these nontrivial factors is self-reciprocal. If a primitive root
zeta and its inverse were in the same Frobenius orbit, some power of11
would equal-1 modulo19, impossible in the order3 subgroup <11>.
Nondegeneracy of the invariant bilinear form pairs each nontrivial
simple constituent perfectly with its dual. Their multiplicities are
equal: equivalently, after scalar extension, the lambda-eigenspace is
orthogonal to all eigenspaces except that for lambda^-1, with which it
pairs nondegenerately. The nontrivial part hence has dimension at least6,
and its dimension is a positive multiple of6. Dimension7 forces exactly
one dual pair of cubic constituents and one trivial constituent.
Therefore Fix_V(Y) has dimension1 and is nonisotropic.

On any rational Y-invariant line the eigenvalue lies in F11^* and has
order dividing both19 and10. It is consequently1, so this fixed line is
the UNIQUE rational Y-invariant line. The given v spans it.

This statement is false for arbitrary GL7(F11): a cubic order19 block
plus a four-dimensional identity block has fixed dimension4. Such a
block alone cannot preserve a nondegenerate symmetric form because its
dual cubic constituent is absent. Thus the acquired nondegenerate form
and actual isometry join are material. Alternatively an independently
verified rank(Y-I)=6 plus vY=v supplies uniqueness directly, but it does
not replace the natural Cayley premise for the overgroup geometry.

The J1 exclusion and its sources
-------------------------------

J1 has elementary abelian Sylow2-subgroups of order8, so it has no
element of order4. Here is a short verification from explicitly recorded
structure, rather than from its order alone. The ATLAS J1 page [A]
records |J1|=2^3*3*5*7*11*19 and a subgroup2^3:7:3. Its normal2^3 is
elementary abelian and already has the full2-part of |J1|, so it is a
Sylow2-subgroup. Sylow conjugacy makes every2-subgroup lie in a
conjugate of that elementary abelian group. In particular a cyclic4
cannot occur. Wilson Section5.9.1 independently records the same
monomial subgroup and order.

There is also a direct primary-research-text check: Li, Moghaddamfar,
Vasil'ev and Wang [L], Lemma3.9(2), printed p6, give

  mu(J1)={6,7,10,11,15,19},

where mu is the set of element orders maximal under divisibility.
Every element order divides a member of that list; none is divisible
by4. Their cited origin is the printed ATLAS, p36, and the online ATLAS
conjugacy-class list agrees. Janko's original construction and
characterization are the historical source [J]. The publisher full text
of[J] was not retrieved in this check; the actual primary texts read
for the exclusion are[L] and the ATLAS authors' group record[A].

Proof of the generation criterion
---------------------------------

Suppose H<G and choose a maximal overgroup M. The complete list leaves
only the two types above. If M is SL3(11):2, it preserves a rational
pure line L. Since Y belongs to M, L is Y-invariant, hence is precisely
<v> by uniqueness. Every generator h_i would preserve <v>, contrary
to the displayed nonzero minor. Thus this maximal type is excluded.

If M is J1, its element X would have order4. Indeed X^4=I and X^2!=I
give exact order4. This contradicts the J1 exclusion. No proper maximal
overgroup remains, so H=G. This proves the statement.

The two extra ingredients are individually essential to this argument.
A moved19 line alone leaves the genuine J1 alternative. A19-word and
a4-word alone leave SL3(11):2, which has both orders. No implication
from a missed4-word search, or a missed moved-line witness, is asserted.
The positive criterion needs no split/nonsplit squareclass decision for
the fixed line: movement excludes every line-stabilizing overgroup.

One may replace4 by any independently certified order n that does not
divide any of6,7,10,11,15,19. The same proof excludes J1 after the moved
line has excluded SL3:2. Such a variant also requires actual existence
and word membership in the ambient group; the spectrum statement does
not manufacture a witness or a search-length guarantee.

Exact certificate and application duties
----------------------------------------

* Retain the original ordered indices/marks, prelift/index transport and
  actual matrix export. Both word evaluations and the moving generator
  must belong to the SAME actual end H, with the recorded right-row
  convention. A word from the other end or the full marking is not an
  H-word certificate. A4-word may be supplied directly; no element-order
  engine is required if its fourth power and nonidentity square are
  independently checked.
* Authenticate the natural seven-dimensional Cayley model and its
  equality with G2(11), its nonsingular invariant form and all actual
  isometries. Retain the existing complete-model/order/generation bridge;
  composition normalization alone does not prove that the whole acquired
  matrix group is G. Kernel or image transport cannot be silently assumed.
* Verify the19-word/nonidentity, the actual fixed-vector equalities,
  nonzero v, and one nonzero moving minor. Rechecking a stored witness is
  a new duty; an old MOVED19_UNPAID label is not itself the certificate.
* To turn H=G into a C-group rejection, join the actual full marking and
  its proper end. In a faithful string C-group marking every subgroup
  generated by a proper subset of independent marks is proper: if a
  missing involution lay in that subgroup, the intersection property
  with its singleton subgroup would force that involution to be trivial.
  Thus a certified full end contradicts the claimed marking IP. This
  last step retains original lift/faithfulness and label duties; it is
  not an automatic census or original-prefix closure.

The frozen proper19 worker still treats moved19 as unpaid, correctly
for its present certificate schema. This note changes no worker,
control, result, journal, accepted rejection or Root gate. A future
implementation would need separate Source review, genuine exact word
verification, actual acquisition/review and disjoint Root adoption.
No current unpaid count changes, no subgroup order is computed and no
broader conjecture is decided. The deduction is a classical
classification corollary with an explicit small certificate interface.

Sources and retained antecedents
--------------------------------

[K] P.B.Kleidman, The maximal subgroups of the Chevalley groups G2(q)
with q odd, the Ree groups2G2(q), and their automorphism groups,
J.Algebra117 (1988),30--71, https://doi.org/10.1016/0021-8693(88)90239-6.
The classification origin; its publisher full text was not newly read.

[N] H.N.Nguyen, Irreducible restrictions of Brauer characters of the
Chevalley group G2(q) to its proper subgroups, primary manuscript
https://arxiv.org/pdf/0910.4994v1, proof of Theorem4.4, pp10--11.
The complete pre-elimination list was read directly for this note.

[W] R.A.Wilson, The Finite Simple Groups, retained preliminary edition,
Sections4.2.6 and5.9.1; author page
https://webspace.maths.qmul.ac.uk/r.a.wilson/TFSG.html.
Local wilson_early_book.txt633091B, SHA256
d0af6d76130d73a143e76218c7c66ca0167d06f70d591f9c3482ec8e04fe895f.

[L] T.Li, A.R.Moghaddamfar, A.V.Vasil'ev and Zh.Wang, On recognition
of the direct squares of the simple groups with abelian Sylow2-subgroups,
primary manuscript https://arxiv.org/pdf/2312.07907v1,
Lemma3.9(2), printed p6; definition of mu in Section2.

[A] ATLAS authors' J1 group record, order/maximal-subgroup and complete
conjugacy-class sections, https://brauer.maths.qmul.ac.uk/Atlas/v3/spor/J1/.
Only written entries were inspected; no representation, word list,
program or database computation was downloaded or evaluated.

[J] Z.Janko, A new finite simple group with abelian Sylow2-subgroups
and its characterization, J.Algebra3 (1966),147--186,
https://doi.org/10.1016/0021-8693(66)90010-X.
Historical origin, not claimed freshly retrieved in full.

Existing f1b6 theorem Source is g2_11_generation_by_prime_witnesses.tex,
26437B, SHA256
f1b6c8a69780c7b8ac88f239627a7ce6889c24203f72ddc35c86fe93e661e76b.
This note is an additional written corollary, leaving that consumed
Source and ceac7edc proper19 Source byte-identical.
