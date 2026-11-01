A full end from a finite parent certificate
==========================================

Original setting and borrowed facts
----------------------------------

Let G be the acquired faithful natural matrix model of G2(11), acting on
row vectors in V=F_11^7. The original catalogue and its indexed orbit table
associate the requested positions with actual quartets (a,b,c,e) in G.
The model, membership, faithful-frame and original-orbit interpretation
are borrowed inputs. The replay reconstructs the matrices and checks the
frame equations; it does not identify G from its order or reproduce the
original orbit census.

The shared reader's THEORY.rst gives the precise classification sources.
The complete odd-characteristic maximal-subgroup classification is due
to P. B. Kleidman, The maximal subgroups of the Chevalley groups G2(q) with
q odd, the Ree groups 2G2(q), and their automorphism groups, J. Algebra 117
(1988),30--71, doi:10.1016/0021-8693(88)90239-6. The retained project uses
the full list before the later character exclusions in the proof of
Theorem 4.4 of H. N. Nguyen, Irreducible restrictions of Brauer characters
of the Chevalley group G2(q) to its proper subgroups, arXiv:0910.4994.
The natural line-stabilizer description is retained from R. A. Wilson,
The Finite Simple Groups, author edition, Section 4.2.6. The primary ATLAS
J1 record supplies its order and maximal-subgroup list.

We use the following exact consequences as attributed premises.

1. A proper subgroup of the acquired G containing an element of order 19
   lies in a rational line stabilizer of type SL3(11):2 or in a subgroup J1.
2. Among the proper maximal subgroups of J1, only 19:6 contains 19.
3. The order of J1 is 175,560.

The complete cover is needed. A list restricted by an irreducibility
hypothesis would not justify the first statement.

A fresh test for rational lines
-------------------------------

Lemma 1. Let a,b,c be involutions in GL_7(F_11). They preserve a common
rational line if and only if at least one of the eight systems

    v a = s_a v,    v b = s_b v,    v c = s_c v,

has a nonzero solution, where each s is 1 or -1.

Proof. An involution acting on a preserved one-dimensional space has
scalar s with s^2=1. Since F_11 has odd characteristic, s is 1 or -1.
The converse follows directly from the three row equations. QED.

For each sign triple, the verifier forms the 21 by 7 coefficient matrix
whose equations are those displayed above. It computes its rank by the
shared rank_seven function. Rank 7 makes its kernel zero. Thus eight
fresh full-rank checks exclude all common rational lines of the LEFT end.
The involution hypotheses are freshly checked by check_marks, in the
same original row frame.

The RREF implementation charges seven scalar multiplications for pivot
normalization and fourteen scalar operations for each nonzero row
elimination. Its FIELD counter is cumulative, with a limit of 200,000.
A 21 by 7 system costs at most 7(7 + 20*14) = 2,009 such units. All sixteen systems
therefore cost at most 32,144 units, before observing the actual matrices.
No field bank is reset between signs or cases. These linear units are
reported separately from matrix products, row images and field inverses.

The proper-end alternative
--------------------------

Lemma 2. Put L=<a,b,c>. Assume that a,b,c are the reconstructed original
involutions, that a and c are distinct and commute, that L contains 19,
and that L preserves no rational line. Under the imported classification,
L is either G or the entire J1 subgroup containing it.

Proof. If L is proper in G, the line-stabilizer possibility in the complete
cover contradicts Lemma 1's checked conclusion. Thus L is contained in a
J1 subgroup. If it were proper there, it would lie in a maximal subgroup
containing 19, hence in 19:6. But <a,c> is a Klein four group, whereas the
2-part of |19:6| is 2. This is impossible. QED.

A fixed seed and its orbit
--------------------------

Lemma 3. Let Z in L have exact order 19, and let v be any nonzero vector
with vZ=v. If L is J1, then the orbit v^L has size at most 9,240.

Proof. The stabilizer L_v contains the actual cyclic subgroup <Z>, so
|L_v|>=19. Orbit-stabilizer gives |v^L|<=175560/19=9240. QED.

The replay forms W=ababc and Z=W^7 with the actual LEFT marks, then checks
Z is nonidentity and Z^19=I. Primality gives exact order 19. It checks the
supplied nonzero typed seed directly by vZ=v. No fixed-space uniqueness,
nullity, quadratic norm or exact G-point stabilizer is used in Lemma 3.

The supplied parent records
---------------------------

Each record is a little-endian unsigned 16-bit parent and unsigned 8-bit
label. The root is (65535,255). Every other record i must have parent<i
and label in {0,1,2}. Starting at the actual fixed seed, the verifier computes

    v_i = v_parent(i) * (a,b,c)[label(i)].

Induction places every row in v^L. Rows are literal vectors, with no
projective normalization. The code sum(v_j*11^j) is injective on F_11^7;
the verifier compares all complete codes to establish distinctness.
It checks exact binary length and canonical base64 before replay, and
compares the producer's ordered-code hash only after fresh reconstruction.
The parent list supplies reachability, not closure. No orbit search is
needed to check it.

Theorem. Under the stated borrowed original-model and classification
premises, a verified 9,241-row parent certificate proves L=G and failure
of the original rank-four intersection property.

Proof. The 9,241 distinct reconstructed rows belong to v^L. They contradict
Lemma 3 if L is J1. Lemma 2 leaves L=G. The original fourth mark e is a
nonidentity member of G. Thus the subgroups on the disjoint label sets
{0,1,2} and {3} intersect in <e>, although the subgroup on their empty
intersection is trivial. This violates the intersection property. QED.

Scope and attribution
---------------------

The certificate package covers only positions 2570 and 3017. The original
proposer supplied the parent records and seeds. The separate consumer
reconstructed every parent image before the canonical two-case adoption.
This public frontend reuses that literal parent-checking mathematics and
the existing matrix reader, and adds the fresh complete sign-system check.
The classification, orbit-stabilizer argument and line criterion are
standard or explicitly retained prior work. No historical novelty claim,
new conjecture resolution, Lean verification or whole-paper replacement
is made here.
