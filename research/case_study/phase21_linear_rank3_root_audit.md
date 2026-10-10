# Phase 21 linear rank-three root review

10 October 2026. **PASS for the stated written theorem and exact diagnostics.**
This is an internal mathematical review, not external review or verification
of publication priority. The accompanying JSON binds the final proof bytes.

Root read every section of the standalone proof. The two rank-one images
are full: the trace-square differences exclude proper subfields, and the
exceptional cases include a separate characteristic-three calculation at
q=9. The retained automorphism theorem then makes a diagonal Goursat graph
impossible: it would force a primitive element to have order dividing
p^j+1<q−1. Both lifts from PSL2 to SL2 use perfection correctly.

The nonzero radical argument does not assume a splitting theorem. If its
kernel vanished, the central Levi involution would split the four-dimensional
space into two invariant planes, contradicting the exhibited Jordan block
of size three. Double root differences prove irreducibility of the additive
radical even for subgroups initially only linear over the prime field.
The explicit conjugate and three subsequent commutators supply every
remaining elementary root. Determinants modulo fourth powers identify
the exact diagonal index-two projective group.

The endpoint and adjacent-pair checks support the retained same-marking
intersection argument. Root caught a coordinate typo in Av during review;
the final proof and symbolic checker have the corrected vector
(0,1,nu,0). No theorem hypothesis or conclusion changed.

Root reopened the primary Guralnick–Zieve author manuscript, Appendix,
printed p.42, immediately before Lemma A.5. It explicitly identifies
Aut(PSL2(q)) with PGammaL2(q), including the q=9 parameter used here.
Only the needed appendix passage was read; its polynomial results are
not rederived or counted as research coverage.

Fresh execution of unchanged checker copies in a temporary directory gave:

* 34 exact symbolic checks with SymPy 1.14.0;
* all six GAP fields q=5,7,9,13,17,25;
* both full rank-one projection orders in each field;
* all 48 marked subgroup closures and 384 exact subgroup meets;
* the determinant-constrained ambient order in each projective point action.

These runs reproduce existing diagnostic cases, adding no new parameter
coverage. The first symbolic attempt used a scratch-directory default Python
without SymPy and stopped at import; the recorded successful run used the
existing global Python environment. No dependency was installed.

The all-parameter conclusion comes from the written proof, not extrapolation
from those fields. The rank-set corollary retains the earlier rank upper
bound and rank-four construction, and the published q=3 rank-three case.
The q=3 mod4 existence range is already published; other possible overlap
and the 2026 thesis lead remain in the bounded status audit. No infinity
marker, matched-length ratio, whole-survey resolution or new Lean theorem
is assigned.
