# Admission of the uniform square-torus cover theorem

10 October 2026. The independent phase242 review accepts the complete
written theorem in phase239 and its phase224 specialization. Root read
the manuscript, review, fourteen-clause contract, Lean source and replay
programs, and reran both author programs and the independent computations
from the public copy.

The author manifests have SHA256
`60253cfc8c886749476fd19bba5a9813221161f47e5aa8ea29401786bdb5772f`
(phase224) and
`6ee2cf7e548a4075c52ad54ba14a8753ce116001d5dd454718f4150efff4d135`
(phase239). The independent review manifest has SHA256
`6f8094cc8235c179133eb1ab8ce322c8c1815782eea5b877727626a2e16b5952`.
Their 46 exports and three manifests are preserved byte for byte.
The author-frozen headers retain their historical pending-review wording;
the later independent review and this admission record the accepted status.

## Accepted mathematical content

For every n≥3 and prime ℓ not dividing 2n, the pyramid over the square
torus {4,4}_(n,0) has a finite regular cover with kernel (F_ℓ)^642 over its
marked monodromy. For every odd n≥3, it has infinitely many finite minimal
regular covers, with positive ℓ-power degrees and exponent at most 642.
The conditional transfer through the marked smallest reflexible cover
of a base polyhedron is also accepted.

The proof establishes the all-n quantifier by the affine action and its
restricted injectivity, followed by a fixed subgroup calculation. It does
not extrapolate from sample parameters. Coprime pullback works on each
parabolic and does not assume a split extension. Distinct permitted primes
give different orders of the finite minimal descendants.

For the final transfer sentence, the precise covering criterion is this:
a regular cover has universal normal kernel N; if the target flag
stabilizer is H, the covering condition is N≤core(H). Normality makes this
equivalent to containment in a conjugate of H. Thus a *marked* monodromy
isomorphism preserves the admissible kernels. This is the review's precise
interpretation of the manuscript's brief stabilizer explanation.

The old existence theorem and toroidal non-C classification remain cited
inputs. The n=3 proof is subsumed and is not another family credit. No
arbitrary-polytope finite theorem, classification of minimal descendants,
complete source replacement, historical priority or compression ratio is
admitted.

## Fresh verification

The [public report](../research/case_study/phase247_public_replay/report.json)
records fresh successful author and independent replays. The native GAP
review independently reconstructs the orientation group, quotient and
actual kernel intersections. The separate surface program checks all edge
incidences and vertex links, orientability and the three connected
complements; it recovers 3840 vertices, 7680 edges and 3200 faces.

The new canonical PyramidKernelTransport file contains four elementary
statements. Fresh execution also verifies nine retained statements. All
thirteen use standard Lean axioms. Three false weakenings fail, with
explicit mathematical counterexamples explained in the review. Finite
controls reject the wrong affine reflection, omission of the middle-layer
constraint and a missing surface disk. Generated failing Lean sources are
kept with their failure logs outside the canonical library.

The driver checks Lean 4.32.2 and all pinned package revisions and clean
source trees. Compiled dependency objects and GAP's exact algorithms remain
trusted. Surface topology, the all-n geometric argument, the retained
classification and the complete application remain outside Lean.

The canonical file count rises 84→85; 84 use no native-evaluation axioms
and the one legacy transfer file retains its four recorded native axioms.
The 23 principal-source contracts and eleven question entries do not change.
Primary publications are referenced and hash-bound, not redistributed.
