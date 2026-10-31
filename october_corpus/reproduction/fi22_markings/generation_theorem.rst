Generation in Fi22 from two supplied prime cycles
================================================

This is an explicit application of the existing maximal-subgroup
avoidance and supplied-cycle arguments. The subgroup classification is
due to Kleidman and Wilson; the earlier O'Nan certificate leg retains its
authors. Root proposed this application to the remaining Fi22 selectors.
The primary-source verification and exposition here are by
/root/readme_final_check. No novelty or new classification is claimed.
No group, point, permutation parser, worker, control or helper was run.

1. The classification premise and its editions
----------------------------------------------

Kleidman--Wilson, Math. Proc. Cambridge Philos. Soc. 102 (1987), 17--23,
Main Theorem(i), states a complete list of 14 conjugacy classes of maximal
subgroups of the SIMPLE group Fi22. Its primary publisher table was
visually inspected in full. The official ATLAS page was separately read
for every listed order. The table below accounts for all 14 classes;
the two repeated types each represent two conjugacy classes. The
machine-readable table records the exact orders and prime factors.

  Type                                    Classes   11 divides?  13 divides?
  2.U6(2)                                    1          yes          no
  O7(3)                                      2           no         yes
  O8+(2):S3                                  1           no          no
  2^10:M22                                   1          yes          no
  2^6:Sp6(2)                                 1           no          no
  (2 x 2^(1+8):U4(2)):2                      1           no          no
  S3 x (U4(3):2)                             1           no          no
  2F4(2)'                                    1           no         yes
  2^(5+8):(S3 x A6)                          1           no          no
  3^(1+6):2^(3+4):3^2:2                       1           no          no
  S10                                        2           no          no
  M12                                        1          yes          no

Only the three types 2.U6(2), 2^10:M22 and M12 have order divisible by11.
Only O7(3) and the Tits group 2F4(2)' have order divisible by13. No proper
maximal subgroup of Fi22 has both divisors.

The March1988 corrigendum, volume103, p383, replaces an internal
Theorem4.1(b) concerning U3(3) subgroups and explicitly preserves the
Main Theorem. It was read in full at the publisher. The1984 precursor
alone is not used as a complete conjugacy-class classification. The
ATLAS webpage retains a porting-incomplete notice; completeness here
comes from the1987 theorem with its1988 correction, not from assuming
that every website table is complete. The classification and its
computer-assisted proof are borrowed premises, not recomputed here.

2. The maximal-avoidance lemma
------------------------------

Let G be the named simple Fi22. If K is a subgroup of G and both11 and13
divide |K|, then K=G. Otherwise the finite proper subgroup K is contained
in a maximal subgroup M. Lagrange's theorem makes both primes divide
|M|, contradicting the complete list.

This statement is deliberately about G. It is false with G replaced
by A=Aut(G): G itself is a proper maximal subgroup of A of index2, and
its order contains both primes. No certificate may silently substitute
membership in A for membership in G.

The accepted original input425eba68 supplies the actual degree3510 G
model, normality of G in A, original generators and complete class and
centralizer joins. The named-Fi22/full-Aut/Out2 identifications remain
attributed premises. The acquired point bridge f774b140 binds the same
original action; a fresh isomorphic ATLAS model is not substituted.

3. A short positive certificate
-------------------------------

For actual original members a,b,c of G, put r=ab and s=bc. Let w11 and
w13 be words in r,s and their inverses. They may be the SAME word. Suppose
the action of w11 contains a closed cycle of exactly11 pairwise distinct
points, and that of w13 a closed cycle of exactly13 pairwise distinct
points. The two lists are not required to be mutually disjoint.

Each supplied cycle has to include its final return edge. It then proves
that the corresponding image permutation has order divisible by its
prime. The image order divides the order of the actual word, so both
primes divide |<r,s>|. All words lie in G by the original membership
premise. The maximal-avoidance lemma gives

  <ab,bc> = G,     hence <a,b,c> = G.

One need not compute the whole permutation order, demand that it equal
11 or13, inspect its other cycles, or require different witness words.
The accepted action is faithful, as in the retained model premise. The
divisibility argument in fact only needs a genuine action homomorphism;
this observation does not relax the original model binding.

The action convention must remain literal: with the existing right-action
convention, x^(ab)=(x^a)^b and x^(bc)=(x^b)^c. Inverse rotation letters
act as b then a, or c then b, respectively, because a,b,c are involutions.
Only the supplied word edges need evaluation. With word length at most64,
the two exact cycles require at most 24*64 rotation evaluations, or3072
individual involution-image evaluations when those maps are directly
available. If b is virtual, every underlying word-image step must also
be charged. This bound is not a measured runtime or a promise that a
bounded supplier will find the witnesses.

4. What the certificate pays
----------------------------

For nonidentity involutions a,b,c with a!=c and ac=ca, the existing
rank_three_intersections.tex applies after generation in the named simple
G is established. It then gives the rank3 string C-group intersection
property; no additional intersection census is necessary. That earlier
proof, its hypotheses and attribution are reused unchanged.

A positive certificate establishes generation for ONE fully identified
marking and therefore its genuinely identified automorphism orbit. A
selector can contain many H-orbits of possible middles. This test does
not partition that domain, prove an orbit weight, or decide how many
markings exist. Complete local coverage, full-Aut weights and the separate
reversal/duality accounting remain required for the final number.

The40 zero-generating selectors already accepted at1dacd3bc are retained.
No witnesses or new counts for the65 remaining selectors are asserted.
A bounded search miss is UNPAID: the criterion is sufficient, not a
necessary condition on the particular words tried. No incomplete orbit
search or failed cycle proposal is a nongeneration proof.

5. Exact reuse boundary
-----------------------

The O'Nan generation_batches/generation.py already has the required
signed-rotation word convention, paired word/cycle representation,
pairwise-distinct typed points, every closing edge, and Saved checking
without proposal replay. Its check_cycle and rotation_word Source spans
are the concrete reusable pattern. The existing implementation itself
is bound to degree122760, primes19/31, an O'Nan factor model, two specific
endpoints and its own maximal-order list. It is NOT a Fi22 runtime or
control gate and is not invoked or retargeted here.

A later small Fi22 checker must instead pin the original Fi22 model and
literal a,b,c provenance, degree3510 and the complete14-class premise.
Its strict Saved reader must accept any valid supplied11/13 witnesses,
perform only their direct edge checks and reproduce the whole canonical
claim. The narrow future interface is in INTERFACE.rst. There is no new
worker, compiled program, runtime gate or control result in this packet.

References
------------

P.B. Kleidman and R.A. Wilson, The maximal subgroups of Fi22, Math. Proc.
Cambridge Philos. Soc.102(1987),17--23, Main Theorem(i):
https://doi.org/10.1017/S0305004100067001 .

Their Corrigendum,103(1988),383:
https://doi.org/10.1017/S0305004100064963 .

Official ATLAS Fi22 page, separate Fi22 and Fi22:2 maximal tables:
https://brauer.maths.qmul.ac.uk/Atlas/v3/group/Fi22 .

PRIMARY_SOURCES.rst records the exact publisher image URLs and access
scope; source_note.json pins the retained local sources and accepted
metadata. This written application grants no whole Original credit.
