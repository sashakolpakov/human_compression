# Uniform triangularity of the label-eight rewrite table

`formal/LabelEightTriangular.lean` proves five statements for the literal
table imported from `LabelEightCriticalPairs.lean`. All ranks d≥3 are
covered. A letter is encoded by a natural number below 5d−7 in the same
r,x,y,z,w order as the written construction.

Every letter in a nonempty square replacement is strictly above the
squared letter. Every correction letter in the swap of a>b is strictly
above a. Both kinds of tail remain below 5d−7. The complete replacement
retains no letter below b, and every contextual rewrite, and every finite
chain of rewrites, preserves any given range lo≤letter<5d−7.

The proof unfolds the actual square and commutator table. Case analysis
and ordinary kernel-checked natural-number arithmetic handle its index
offsets and boundary cases. The context and closure arguments are proved
by membership analysis and induction. No finiteness sample, normalization
assumption, confluence assumption or evaluator axiom replaces these
universal arguments. The five declarations are one local proof component.

The separate termination agent read the full source and imported table;
its exact reading record is `phase174_label_eight_independent_review.md`.
The root then freshly compiled both local files from the public source
tree using the pinned generic verifier. All five new and three retained
axiom reports were parsed and contain only propext, Classical.choice and
Quot.sound. The build report records the actual runtime and dependency
revisions. Installed compiled mathlib objects remain trusted inputs; this
was not a rebuild of all upstream dependencies.

This component supplies the concrete triangular-tail and alphabet
hypotheses for a separate termination proof. It does not itself prove
termination, all-rank local confluence, unique normal forms, the finite
group construction, the intersection property or the polytope result.
The previously published finite critical-pair certificate is unchanged.
No source-compression factor, source-count increment or new conjecture
entry follows from adding this formal component.

Reproduce it from the repository root with:

```sh
python3 -B research/case_study/formal/verify_lean.py LabelEightTriangular.lean --packages PACKAGES --lean LEAN --timeout 180 --output-dir /tmp/NEW-label-eight-triangular
```

Use the pinned compiler and package checkout described in the public
formal README. The fresh build requires the literal core and this file;
it does not rebuild the expensive rank-fourteen finite certificate.
