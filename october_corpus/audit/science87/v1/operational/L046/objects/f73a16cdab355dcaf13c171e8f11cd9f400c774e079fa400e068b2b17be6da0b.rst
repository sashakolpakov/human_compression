Distinct review of the L046 maximal-subgroup bounds
===================================================

Decision and roles
------------------

I accept corpus106_L046_maximal_bounds_v1 unchanged, manifest
d7e826cec742417d68173aa748de3b6b44b6a348d63cd6fc85394ff5bd279919.
The new bound and its numerical application were authored by /root.
I, /root/publication_recovery, did not contribute to that argument before
review. I authored the preceding common-counts component, which this proof
acquires. Its distinct root review is bound and accepted separately; this
record does not pretend to review my own earlier work independently.

The accepted conclusion is a genuine contradiction to the stated total
in the fixed published source, using its explicit formula (2.4) convention:
the total is at least 798370, whereas Theorem 1.1(2) asserts 796772.
The exact count for (20,31) is 9118, whereas Table 1 prints 7246. The other
accepted outputs are the 136 exact intervals, the twenty coincident
endpoints, and existence of all 129 source-positive types.

This does not recover the exact full total, the other 116 exact table
counts, or the full chirality and inversion spectrum. It supplies no new
conjecture answer, compression measurement or Lean declaration. I assign
no whole-original admission in this component review. A later source
disposition must keep the refuted principal assertion separate from the
source's remaining claims.

Source convention and retained premises
--------------------------------------

I read the fixed source's opening statements, Theorem 1.1, Section 2.2 and
formula (2.4), as well as the full native table on physical page 11. Its
objects in Section 2.2 are ordered triples (x,y,z), with x an involution,
y of order p, z of order q and xyz=1. The pair (y,z) determines x uniquely.
The source divides the number of generating triples by |Aut(G)|. It does
not divide again by a duality action for p=q. Although Theorem 1.1 uses
braces for pairs, the proof correctly pins its numerical assertion to
the formula actually used to calculate Table 1. In particular the unequal
type (20,31) cannot be explained away by an equal-type duality convention.

I reopened the primary Atlas O'Nan page and inspected the complete cached
HTML acquired by the author. The thirteen maximal-class rows, orders and
indices agree with the stored CTblLib Maxes list. The two classes each of
L3(7):2, L2(31), M11 and A7 are all retained. In particular A7 is entered
twice even though both occurrences have the same table name. These are
conjugacy classes under G, as required by the union bound, not a list of
abstract isomorphism types or a list modulo the outer automorphism.

The named group identifications, the completeness of the maximal-subgroup
classification, the ordinary character tables and |Aut(G)|=2|G| are
explicit borrowed premises. Checking degree squares, orders or arithmetic
alone would not establish those identifications. The proof says this
correctly. I checked the special ONM5 metadata in CTblLib, which identifies
the same order-25920 maximal group despite the abbreviated product notation
in the Atlas display. I also read Wilson's Section 3.3 in the cited survey;
the historical attribution to the independent classifications agrees.
Those classification proofs are not claimed as newly reproduced here.

Primary references checked during this review:

* https://brauer.maths.qmul.ac.uk/Atlas/v3/spor/ON/
* https://webspace.maths.qmul.ac.uk/r.a.wilson/pubs_files/AtlasMaxSporarxiv.pdf

Mathematical argument
--------------------

The action of Aut(G) on generating ordered pairs is free: an automorphism
fixing both generators fixes every word in them. Thus the orbit count is
e_G/|Aut(G)|, with no assumption about stabilizers of nongenerating pairs.

Every nongenerating pair lies in a maximal proper subgroup of the finite
group. For each conjugacy-class representative M, the union over its
conjugates has size at most [G:N_G(M)] x_M, and this in turn is at most
[G:M] x_M. The latter inequality has the correct direction. Overlap of
these sets only makes the subtraction more conservative. Normal maximal
subgroups and coincident abstract group types do not invalidate the bound.
There is no assumed disjointness, subgroup-lattice inversion or accidental
use of [G:M] as an exact number of conjugates. Taking the ceiling only
after division by |Aut(G)| is legitimate because the number of generating
orbits is integral; negative raw lower values are clipped at zero.

The acquired Frobenius formula counts product-one triples. The bijection
(R,S) -> ((RS)^(-1),R,S), with RS of order two, gives exactly the all-pair
quantity needed here. Summing character values over entire order sets is
valid, and the code explicitly checks those sums are integers in every
retained table. No floating-point approximation is used. The source table
is not used to exclude candidates or alter any character sum or bound.
The expected values in the checker are comparisons after the derivation.

For the special type, only the two L2(31) maximal classes have order
divisible by 31. Their actual element-order sets omit 20. Thus no proper
subgroup can contain the prescribed pair, and all such pairs generate G.
The all-pair count 8403431565957120 divided by 921631011840 is exactly 9118.
This argument requires the retained complete maximal list but no explicit
representative enumeration of the O'Nan group.

Different (p,q) types are invariant under automorphisms, so their orbit
sets are disjoint. Summing their individual lower bounds is valid. The
sixteen lower row sums in the manuscript add to 798370, exceeding the
source total by 1598. This difference is a proved lower discrepancy, not
the exact difference between the true and printed totals.

Among the twenty exact intervals, (3,3) has value zero. The other six
source-excluded types have nontrivial upper intervals and are not excluded
by this component. The manuscript correctly declines to infer general
nonexistence from a zero lower bound. Agreement of a printed entry with
an interval is likewise not represented as an exact verification.

Code and independent arithmetic
-------------------------------

I read maximal_vectors.g, maximal_controls.g, bounds.py and check.py in
full. The fresh author checker, session 82059, finished with exit zero,
empty GAP stderr, all 136 intervals unchanged and four rebuilt native
pages. It re-extracted the actual irreducible-character data and reran
the complete five-group controls.

The GAP vector extractor enumerates every irreducible character and every
actual element order, summing class size times the character value.
It preserves the full Maxes sequence; sorting is used only to avoid
extracting the same named table twice. The Python evaluator subsequently
iterates the unsimplified thirteen-class list. Thus neither class names
nor isomorphic repetitions are dropped from the subtraction. Its exact
ceiling expression also handles negative raw numerators correctly.

The small controls enumerate every subgroup and every ordered pair of the
relevant types in S3, D8, A4, S4 and A5. Their maximal subgroup tests are
literal containment tests; the inequality and free-orbit divisibility are
then checked directly. They test the implementation and do not substitute
for the uniform proof.

I added two independent calculations. First, a separate GAP program sums
ClassMultiplicationCoefficient(t,i,j,k) times the size of the target
involution class. I read its GAP implementation and checked that this is
the coefficient for a fixed element of the third class. The character
there is conjugated; involution values are real, so it is the required
product-involution count. This computes 574 available type counts across
the thirteen distinct named tables by a different aggregation from the
author's order-vector expression. Session 81845 completed in 1.70 seconds
with exit zero, empty stderr and the complete marker.

Second, a separately written Python program parses the exported integer
vectors, clears all character-degree denominators with their least common
multiple, and performs exact integer division. It imports none of the
author's arithmetic functions. Every one of the 574 class-constant counts
agrees. It then computes all thirteen contributions for each of the 136
target types and obtains the same intervals and aggregate. The primary
Atlas HTML is parsed independently to check all thirteen orders and
indices against the actual table sequence.

This independent parser also extracts all 136 printed entries directly
from physical page 11 of the source PDF. Their total is 796772. Exactly
one printed entry lies outside its calculated interval: (20,31), printed
7246 versus the exact 9118. The sets of positive types agree exactly,
and their number is 129. The twenty coincident intervals and all sixteen
row lower sums agree with the author ledger.

Reviewer diagnostics initially caught an extra parenthesis in the new GAP
script and parsing mistakes in the new Python audit. None supplied a
completed certificate. One additional reviewer assumption that the first
irreducible character is always trivial was false for a retained table;
the corrected check identifies its unique trivial row without assuming
character order. The author code does not make that assumption. The final
separate audits pass and no author packet was changed.

Native inspection, guards and scope
----------------------------------

I directly viewed all four freshly rebuilt manuscript pages. Their text
matches the frozen author's PDF and there is no overfull content. I also
directly viewed the source's Theorem 1.1, formula (2.4) and the native
rotated Table 1; the (20,31) entry is literally 7246. The source total and
that cell are not extraction guesses.

The frozen checker rejects optimized Python before it creates its output
directory; this was freshly tested. It verifies all author exports and
131 direct dependencies, requires empty GAP stderr and an exact terminal
marker, compares both fresh outputs, and constructs its comparison only
after deriving the bounds. The standalone arithmetic contains explicit
checks rather than assertions. No large group census or old timed-out
search was restarted.

This acceptance retains all external classification costs and the prior
distinct acceptance of the common proof. It accepts the new mathematical
contradiction and the specified bounded positive results, while keeping
the remaining claims and whole-source/publication disposition separate.
