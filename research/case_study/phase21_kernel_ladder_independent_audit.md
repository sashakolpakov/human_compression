# Independent review of the guarded invariant-kernel census

10 October 2026. Survey/source-audit agent review, independent of the author's proof and implementation. **PASS: no gap found in the full written argument or the final guarded census code.** This is an internal review, not external peer review or a fresh execution of the rank-five GAP run.

Final proof reviewed: `phase21_kernel_ladder.md`, SHA256 `68821f3d0c1b1eb870e200da724220b942e703811ec643eb489f1158b92fc9b9`.
Final guarded executable reviewed: `phase21_kernel_census.g`, SHA256 `385e863b18e9a6a876290fc05564b1529304340cfbe719690ca74c55f743d4fc`.

## Mathematical checks

* The canonical forest quotient gives gamma3 order eight at excess three. Strict lower-central decrease in a finite nilpotent 2-group yields class at most five, and [gamma3,gamma3] lies in gamma6=1. This justifies both the universal class-five source and the abelian target-kernel types; it is not an empirical class bound.
* The finitely generated nilpotent quotient of the involution path presentation is finite: its graded factors are finitely generated and killed by two. Universal deletion maps prove actual IP on this particular universal group. No assertion that deletion maps or IP pass to arbitrary quotients is made.
* Every target corresponds to exactly one normal kernel of index eight in the universal gamma3, by the marked canonical class-two quotient. Distinct kernels are precisely distinct ordered marked groups. Passing to reversal requires only the universal reversal automorphism; no further abstract-group automorphism division is appropriate.
* The index-two step works for arbitrary ambient-normal M, including nonabelian M. Necessity and sufficiency of containing Phi(M)[M,U] were checked. The completeness argument through a nonzero invariant character is valid because the ambient quotient is a 2-group acting on an odd number of nonzero dual vectors. Iterating gives every desired kernel, rather than merely kernels admitting a guessed parameter presentation.
* The exact restriction K intersect U_S=gamma3(U_S) follows by applying the actual universal deletion map. For a candidate N, the kernel profile in K/N is exactly the intersection of K/N with each marked parabolic. The common image in the canonical quotient can be lifted from the intersection parabolic; the residual element lies in the two kernel profiles. This proves the stated if-and-only-if IP recognition and does not assume quotient IP generally.

## Code and evidence checks

The entire final GAP source was read. It retains images of the original involutions through both the NQ epimorphism and the pc isomorphism; the pc generators do not replace the marking. All hyperplanes are enumerated, normality and indices are asserted, and exact canonical induced pc sequences are used for subgroup deduplication. During review I requested the explicit relative-order-two assertion needed for the binary coordinate encoding; the final executed code contains it. This is a reviewed correction before final freeze, not an unacknowledged inference about the pc representation.

The guarded executable rejects failed small-kernel profiles early, then performs every full marked intersection on each survivor. The final proof explicitly corrects the inherited broad comment about every candidate: the executable, report counts and mathematical pruning theorem agree. The earlier direct rank-four probe checked all candidate quotients through a separate recognition path but shared the enumeration machinery; its stated independence limit is accurate.

I freshly checked the saved reports and coordinate files with a separate standard-library script: all recorded script/log/checkpoint/accepted-file hashes match; deterministic gzip contents match their uncompressed hashes; every checkpoint is unique; accepted kernel keys belong to the exhausted final level; type, class/kernel, reversal-fixed and orbit totals agree with the accepted records. This validates saved-artifact consistency, not the NQ or subgroup computations themselves. Results:

| Rank | Candidate kernels | Ordered accepted | Fixed by reversal | Reversal classes |
|---|---:|---:|---:|---:|
| 3 | 61 | 37 | 3 | 20 |
| 4 | 1483 | 199 | 11 | 105 |
| 5 | 35971 | 584 | 8 | 296 |

The survivor intersection counts are exactly accepted times 4^rank: 2368, 50944 and 598016. The final rank-five report is bound in the accompanying JSON. No new GAP census execution is claimed by this audit.

## Source and scope checks

I independently inspected N009's generator-set isomorphism convention and Table 6, and wrote the separate source comparison checking all thirteen rank-four type totals with the reversal fixed-point correction. Its two fixed-orientation exceptional markings match the separate raw-presentation certificate. Rank-five in this census means order 4096, not N009's rank-five order 1024; the proof distinguishes these. Likewise the rank-three order-256 census is not N009's excess-five order-1024 component.

The mathematical input from `phase15_graded_support.md` and the exact GAP/NQ algorithms remain retained. The resulting finite alphabet has not yet been used to compute a complete all-rank transition system or a third-excess formula. No source-presentation candidate filter, SmallGroups catalogue, new formalization, novelty claim, matched-length ratio or entire-paper credit is inferred from this package.
