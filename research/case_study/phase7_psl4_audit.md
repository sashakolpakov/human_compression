# Internal review of the phase-seven PSL4 endpoint reduction

10 October 2026. This records internal mathematical review, not external
peer review or a publication-priority determination.

The reviewed result is [phase7_psl4.md](phase7_psl4.md), Propositions A–C.
For a hypothetical rank-five string C-group generating natural PSL(4,q),
q odd, both endpoint products have nontrivial unipotent parts I+N,I+M,
and N²=M²=NM=MN=0. The ranks of N,M are one or two. Ranks five and six
remain unresolved by this reviewed note.

The drafting agent was `recent_conjectures`; the independent internal
reviewer was the root agent. The reviewer reported no gap in:

- Proposition A: the irreducibility of multiplicity-free constituent orbit
  sums, the repeated-character separated support, and the repeated-simple
  two-dimensional tensor alternatives. The explicit dependence on
  phase3_psl4.md, §6, is essential for reducible mixed-sign endpoint actions.
- Proposition B: the (3,1) centralizer involution calculation, the four
  reflection normal forms, the condition b≠0 from the nilpotent square,
  the common symmetric form, and the middle constraint 2u bd t+w z=0.
- Proposition C: the regular truncated-polynomial module basis, its
  one-dimensional common kernel, the simultaneous outer weight choice,
  and the reduction to the existing tensor obstruction.

During review, the draft temporarily treated the semisimple 2+1+1 case
as an uncovered exception. Reading the complete earlier §6 supplied the
missing cited argument, including the trace-zero and mixed-sign cases;
the final proof states this dependency explicitly. This was a dependency
check, not evidence that a finite symbolic calculation covers module types.

The drafting agent executed `phase7_psl4_check.py` with Python 3 and
SymPy 1.14.0: **30 exact algebra checks passed**. Reproduce with

```sh
python3 phase7_psl4_check.py --output /tmp/phase7_psl4_fresh.json
```

The checks cover the displayed matrix identities. The written proof retains
responsibility for case coverage, Maschke and Schur arguments, and the
previously proved common-form obstruction. The companion JSON binds this
review to the proof, checker, report and prior proof dependencies by SHA256.

The separate zero-product working classification is not reviewed or
promoted by this record. Nothing here claims an exclusion of rank six or
a resolution of the full maximum-rank conjecture.
