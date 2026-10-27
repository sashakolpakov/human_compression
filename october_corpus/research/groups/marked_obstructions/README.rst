Supplied obstructions for marked matrix groups
=============================================

This package checks supplied invariant lines, common commutants, subgroup
intersection words and pairs of prime-order words. These certify failures
of proposed four-generator markings. It contains the actual retained
witnesses for one F004-associated job, [11,4], over F_11. It performs no
witness search. The prime-order criterion imports a classification theorem;
the other criteria use elementary linear algebra and group theory.

F004's registered source is Malcolm Hoong Wai Chen, *Abstract regular polytopes
of G2(q) in even characteristic*, arXiv:2609.25004v1 (2026), available at
https://arxiv.org/abs/2609.25004 . The dataset here has field q=11, rank four
and fixed prefix number 11, recorded as job [11,4]. It is partial work on that
bounded candidate family. The F004 label records its project provenance;
it does not place this q=11 experiment within the paper's even-characteristic
hypotheses or establish a recovery of the paper.

There are 694 included matrix tuples. The certificate lists have disjoint
original row indices:

* 220 common-line obstructions;
* 314 pair-word intersection obstructions;
* three endpoint-word obstructions and one rank-three overlap obstruction;
* 27 common-commutant obstructions;
* 129 pairs of prime-order words in a single rank-three end.

All 694 rows have supplied certificates. The first 565 obstructions use
elementary matrix and subgroup arguments. The remaining 129 also use the
borrowed maximal-subgroup classification of G2(11), as explained below.
This covers one specified candidate family under the stated original-group
premises, not a completed original, full group census or conjecture resolution.
The corpus's intake counts remain unchanged: 101 of 104 mathematical
manuscripts have complete reviewed treatments; F004 remains unfinished.

Run from a standalone copy
--------------------------

Copy this directory by itself and run:

.. code-block:: sh

   python3 -I -B -S check.py

Only Python's standard library is required. Python 3.10 or newer on Linux or
macOS supplies the signal/resource modules used for the 60-second wall limit
and sampled 128 MiB own-RSS limit. The checker also bounds physical file reads
to 1 MiB and matrix products to 20,000. It does not change inherited kernel
limits or claim that these samples are an OS memory quota.

The default command prints one JSON result and writes no runtime files.
An optional explicit output must be fresh and outside this package:

.. code-block:: sh

   python3 -I -B -S check.py --out /absolute/external/result.json

The checker locates its data relative to its own file, so the working directory
does not matter. No private study tree, GAP installation, original model,
project module, network service or previous result file is required.

A development run from the repository root passed with 8,446 matrix products,
about 0.22 seconds of measured checker time and 26,984,448 bytes of sampled
peak RSS. It checked all 694 certificate rows and created no runtime file.
These are observations of that run, not a portable speed guarantee or a
compression measurement.

What is included and checked
----------------------------

``certificates.json`` is ordinary JSON. Its ``fixture`` is the complete
original 100,429-byte fixture as a JSON value: three fixed matrices, two
ambient matrices, all 694 original-index/representative/final-matrix tuples,
and the retained provenance metadata. The checker reconstructs its canonical
bytes and verifies the original SHA256. Candidate rows and certificate rows
are written individually for inspection. There is no custom matrix codec.

The certificate arrays retain the minimal witness fields from the
original proposals, checked against the subsequent independent proof records
when this package was assembled. Full old proof documents are not copied;
their exact source pins and the original proposal pins are recorded in
``source_pins``. The arithmetic is checked anew from the included numbers,
independently of any earlier PASS field.

The fixed tuple is labelled ``[a,e,b]``. For an included row
``[i, representative, final_matrix]``, the marking is exactly
``(r0,r1,r2,r3) = (a,b,final_matrix,e)``. The row index ``i`` and the raw
catalogue representative are different fields. The checker checks all 694
row positions, distinct representative labels, every nonidentity involution,
and invertibility of the two ambient matrices. It does not reconstruct the
original catalogue or orbit action.

All vectors act on the right: ``v * M``. All matrix and vector operations are
ordinary integer sums reduced modulo 11. No floating-point arithmetic enters
the certificates.

1. A preserved line excludes an ambient element
----------------------------------------------

Let A be a group of invertible linear maps on a vector space V. Suppose
``r0,r1,r2,r3,t`` belong to A, and a nonzero vector v satisfies

.. code-block:: text

   v * ri = lambda_i * v       for i = 0,1,2,3,
   lambda_i != 0,
   v * t not in <v>.

Then every ri preserves the line L = <v>, and so does every element of the
subgroup H generated by them. The element t does not preserve L, hence
``t not in H``. Therefore ``H < A``. This is the stabilizer argument for a
group action; it requires no classification of A or enumeration of H.

For these certificates, each eigenvalue is 1 or -1 (encoded as 10). A record
contains its row index, v, four eigenvalues, ambient generator index, and a
minor ``[j,k,d]``. With w = v*t, the checker verifies all four complete vector
identities and

.. code-block:: text

   v_j * w_k - v_k * w_j = d != 0  in F_11.

If w were a scalar multiple of v, every such minor would vanish. The displayed
nonzero minor therefore proves that t moves L. This proves literal
noncontainment of one included ambient matrix in the subgroup generated by
the four included marks. Calling that subgroup a proper subgroup of the
original A additionally uses the membership correspondence stated below.

2. A common pair word violates the intersection property
-------------------------------------------------------

For a marking (r0,r1,r2,r3), write G_I for the subgroup generated by the marks
whose indices lie in I, and G_empty = {1}. Its intersection property is

.. code-block:: text

   G_I intersection G_J = G_(I intersection J)  for every I,J.

A supplied common value X in G_I and G_J, but outside the group on their
shared indices, disproves this equation for that pair of index sets.

The pair-word records are six integers
``[i,case,left_k,left_epsilon,right_k,right_epsilon]``. Each side is evaluated
as ``(x*y)^k * x^epsilon``, where ``0 <= k < 128`` and epsilon is 0 or 1.
It is a supplied word, not a claimed description of the whole pair subgroup.
The three cases are:

* case 0: pairs (r0,r1) and (r1,r2), shared generator r1;
* case 1: pairs (r1,r2) and (r2,r3), shared generator r2;
* case 2: pairs (r0,r1) and (r2,r3), no shared generator.

The checker compares both entire matrices and excludes the identity. In
cases 0 and 1 it also excludes the shared mark. That is sufficient because a
nonidentity involution generates exactly the two-element subgroup {1,r}.
In case 2 the required shared subgroup is already trivial. The subgroup
memberships follow from the supplied words alone; no subgroup table or order
calculation is required.

3. Endpoint words and rank-three overlap words
--------------------------------------------

Put H = <r0,r1,r2> and K = <r1,r2,r3>. An endpoint record
``[i,0,target,word]`` has target 0 or 3. Its word has at most 20 digits and
uses only the opposite end: digits 123 for target 0, or 012 for target 3.
If that word equals the omitted nonidentity mark, then the subgroups on
the disjoint index sets ``{target}`` and its opposite three-element set
have a nontrivial intersection. This immediately violates the intersection
property. The three supplied endpoint certificates have indices 289, 304
and 409, and target r0.

An overlap record is ``[i,1,left_word,right_word,m]``. The left and right
words use 012 and 123 respectively and have at most ten digits each. The
checker proves that they have the same full value X, and checks a supplied
integer ``1 <= m <= 128`` with ``R^m = 1``, where R = r1*r2.

For completeness, the shared pair has the following elementary normal form.
For involutions x,y and R = xy, we have ``y = xR`` and
``xR = R^(-1)x``. Repeatedly applying these identities writes every word in
x,y as ``R^k*x^epsilon``. If ``R^m = 1``, k can be reduced modulo m. Conversely
all those expressions are words in x,y. Thus

.. code-block:: text

   <x,y> = { R^k, R^k*x : 0 <= k < m }.

Minimality of m is unnecessary, and the 2m displayed expressions need not
be distinct. After verifying the supplied closing period, the checker tests
X against every displayed expression. If none equals X, then X belongs to
``H intersection K`` but not to ``<r1,r2>``. This disproves the required
intersection for the two rank-three ends. The supplied example has index
301 and m = 10. No word, period or end-subgroup search is performed.

4. Common commutants
-------------------

Suppose X commutes with each marked matrix, but not with an included
ambient element t. The marked subgroup then lies in the centralizer of X,
whereas t does not. This proves that the marked subgroup is proper in
the same ambient group. X need not be invertible. The checker compares
both full products in every commutation equation and in the failed ambient
equation. Four supplied matrices X account for 27 further rows. It performs
no linear solving or commutant search.

This is the same standard criterion developed in the corpus's
``common_commutant`` package, applied to the present field and tuples.

5. Two prime orders in one end
-----------------------------

For each of the remaining 129 rows, two supplied words use the SAME end:
012 or 123. A record is ``[row,end,prime,cofactor,word]``, where end is 0
for 012 and 1 for 123. The digits in the word are local end positions.
The checker evaluates y = word^cofactor and proves y != 1 and y^p = 1.
As p is prime, y has exact order p. The two primes are 19 and 37; the
supplied cofactors are respectively 7 and 3. No word-order search is used.

The classification of maximal subgroups of the finite split group G2(11)
implies that no proper maximal subgroup has order divisible by both 19 and
37. The odd-characteristic classification is due to P. B. Kleidman,
``The maximal subgroups of the Chevalley groups G2(q) with q odd, the Ree
groups 2G2(q), and their automorphism groups``, Journal of Algebra 117
(1988), 30–71, DOI ``10.1016/0021-8693(88)90239-6``. The complete odd-q
table was checked in Table 2, printed page 13, of H. P. Tong-Viet and
T. P. Wakefield, ``On Huppert's conjecture for G2(q), q >= 7``:

https://www.personal.kent.edu/~htongvie/Publications/G2.pdf

The original publisher full text was unavailable during this check; the
classification remains a borrowed theorem. At q=11 the table has no proper
subfield or Ree case. Its linear and unitary types have respectively 19
and 37 as divisors, but not both; the exceptional J1 case has 19 but not 37.
The other covering orders also lack at least one prime. The checker verifies
this divisibility specialization; checking numbers does not prove the
completeness of the classified list.

If the end were proper, it would lie in a maximal subgroup. Lagrange's
theorem would force both primes to divide that maximal subgroup's order,
a contradiction. Thus the end is the full original G2(11). The omitted
nonidentity mark belongs to it, so its singleton subgroup meets the end
nontrivially despite their disjoint index sets. The intersection property
therefore fails. This conclusion requires the exact named-group premise;
it is not valid for an arbitrary matrix group with these word orders.

Imported original-group premises
-------------------------------

The finite matrix identities above are unconditional statements about the
included arrays. The final 129 group-theoretic exclusions also require the
classified maximal-subgroup premise. Applying them to the historical F004 group uses the following
explicit premises. They are retained from the original acquisition and are
not proved by this small package.

1. A is the original group identified by job [11,4]. The recorded original
   model, normalization, forms and A=G identification agree with its acquired
   seven-dimensional F_11 matrix frame. The two included ambient matrices
   are the recorded images of elements of that same A.
2. The original domain has 14,763 catalogue entries and 694 orbit rows. Its
   orbit positions, representative indices, fixed prefix and final matrices
   correspond to exactly the tuples in this fixture. The complete domain
   and orbit construction are imported, not generated or checked for
   completeness here.
3. Every marked matrix is the image of the specified original element of A.
   In particular, membership does not follow merely from preserving a norm
   or bilinear form. The original membership/model/frame joins remain premises.
4. The recorded matrix action is faithful. Therefore word equalities and
   inequalities here transport to those original marked elements. The line
   argument needs only their membership and the ambient-element correspondence;
   faithful reflection of equality is used for the intersection obstructions.
5. The acquired orbit correspondence relates representatives through
   prefix-preserving group automorphisms. An automorphism carries the generated
   subgroup and every indexed subgroup to their corresponding images, and
   preserves subgroup intersections and properness. Both obstruction properties
   are therefore invariant. Simultaneous conjugation fixing the prefix is a
   familiar example. This premise transports a representative obstruction to
   its orbit.

The fixture's ``original_membership_provenance`` gives the full original pins,
including the 474,700-byte domain (SHA256 ``14710440...``), 9,384-byte frame
(``b6259de5...``), 3,394-byte faithful-frame acceptance (``a8746058...``),
normalization, model-source join and original raw model. These are historical
references, not files opened by the checker. No equality with a named full
classical or exceptional group is inferred from the matrices alone.

Provenance and attribution
--------------------------

Full SHA256 values and recorded study-relative paths are in ``source_pins``:

* original fixture: 100,429 bytes, ``b2a2d44f31a4...``;
* independent line/mapping proof: 309,917 bytes, ``b21d21fcbfc2...``;
* independent pair-word proof: 56,660 bytes, ``de2d0696ab3a...``;
* independent parabolic-word proof: 14,058 bytes, ``1d12c3949215...``;
* independent final 156-row proof: 80,886 bytes, ``751d49af5343...``;
* the original line, pair-word and parabolic-word proposal documents.

The original mapping export was prepared by /root/first32_result_review.
The line witnesses and mapping verification, and the pair/parabolic proposers,
retain their /root/orbit_mapping_review attribution. The independent pair-word
checker is by /root/readme_structure_audit. The independent parabolic checker
and this portable package are by /root/registration_reuse_review. Bounded
input checking and column-dot arithmetic adapt those earlier word checkers.
The group-action stabilizer argument and alternating-word intersection
arguments are elementary standard mathematics; no novelty claim is made.
The commutant and prime-word proposals were supplied by /root; their
independent final verification and mathematical review are by
/root/readme_structure_audit. The prime-generation criterion reuses the
corpus's earlier ``g2_11_generation_by_prime_witnesses`` theorem, whose
classification input keeps the attribution above.

These source hashes identify earlier artifacts. Apart from reconstructing
the bundled fixture, this checker does not authenticate absent private files,
replay old Tool transports or manufacture a new Source qualification from
historical verification records. Its result is fresh arithmetic verification
of the included certificates, with the stated original-group premises.

Files
-----

``check.py`` is the standalone checker. ``certificates.json`` contains the
shared original fixture, minimal witness records and source attribution.
This README supplies the complete elementary implications and their scope.
There is no new search, full F004 result, catalogue revision, conjecture
claim, Lean formalization or compression measurement in this package.
