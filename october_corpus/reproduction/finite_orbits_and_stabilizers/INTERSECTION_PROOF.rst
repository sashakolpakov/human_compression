One common element outside the middle
======================================

Let g0,g1,g2,g3 be the explicit four supplied matrices over F11.  The checker
validates canonical field entries, four distinct nonidentity involutions,
and all three string commutations.  Put H=<g0,g1,g2>, R=<g1,g2,g3> and
D=<g1,g2>.

The certificate supplies a LEFT word using only0,1,2, a RIGHT word using
only1,2,3, and a bounded positive power.  The checker multiplies the full
seven-dimensional matrices in literal right-row order and verifies

             value(LEFT word) = value(RIGHT word)^power = x.

Thus x belongs to both H and R.  It freshly enumerates the complete dihedral
D, with full matrix equality and a fixed rotation cap.  It accepts only
after proving x is nonidentity and outside that complete set.  Consequently

                    H intersect R is not D.

This directly violates the intersection-property axiom.  No endpoint order,
full H certificate, RIGHT enumeration, fixed line, prime19, classification,
named subgroup, or local-to-global IP theorem is necessary for this proof.
Failure to complete D or any other failed check gives no verified decision.

Discovery and word extraction are untrusted
-------------------------------------------

The earlier complete H certificate helped discover the element. An
untrusted utility expands its S9*T2866 coordinate into a proposed left
word by following the two word trees. Each selected stabilizer
generator is T_i*g_j*reverse(T_target); reversal gives the inverse because
the letters are involutions.  It concatenates the stabilizer word and the
final transversal and freely cancels adjacent equal labels.

The public runtime never opens that carrier, reads its coordinates, trusts
its closure, or assumes the extractor was correct.  Both proposed words are
freshly evaluated.  A wrong extractor can cause rejection, not a false
positive matrix certificate.  Existing public verify.py remains available
for the older, separately stated H-order certificates.

The published left word has length 78, obtained from 80 letters by cancelling
one adjacent pair. The right word is g1*g2*g3*g2*g3*g2 and its exponent is 2.
Both expressions are supplied explicitly in the case file. The complete
middle subgroup has order 10. Fresh checks in both directories verified
the equality and nonmembership using 107 matrix products. The validation
record states the execution limits and control results separately.

Original identity and attribution
---------------------------------

Suppose the supplied matrices are the images, in the stated literal order,
of the retained Original quartet under its faithful natural F11 right-row
action.  Faithfulness transfers the checked word equality to that quartet;
the image outside D precludes membership in its Original middle subgroup.
This is the separate provenance premise connecting the matrix certificate
to the named case.  Descriptive names or hashes do not authenticate it.

The census claim is from Chen's F004 manuscript, arXiv:2609.25004v1 (2026),
Section 4 and Table 2.  Its matrix formulas in even characteristic do not
provide the F11 model used here.  The named faithful F11 model, marking and
enumeration provenance are separately retained project inputs.
Candidate1099 and its row identifier are from the project's retained
enumeration, not a claim that the manuscript prints that quartet.  Direct
word membership, dihedral normal forms and the intersection axiom are
standard group theory; no historical novelty is asserted.

This is a portable re-verification of one already registered exclusion.
It claims no new manuscript, conjecture, census, group recognition, Lean
formalization, further case payment or compression measurement.
