# Author checks for the rank-four theorem

The complete argument is in `phase256_two_stage_rank_four.md`. The manuscript
contains the raw-surface construction and end-intersection proof explicitly;
it does not depend on accepting the unfinished earlier phase224 draft.
The earlier surface criterion is also restated with its coefficient proof.

The key new argument is the exact membership test for each middle boundary
class, followed by the finite-field path construction. The nonorientable
case uses a genuinely closed odd walk after p repetitions; connectedness
alone is never substituted for the odd-characteristic criterion.

A root mathematical read found no remaining objection before the independent
phase273 review. One implicit step was made explicit during that reading:
every outside edge has an outside endpoint, both for the top end union and
for the two local unions. The four-color case checks are now written in
Lemmas5 and9. No author acceptance of the independent review is inferred.

The optimized portable replay command is:

```text
python3 -O phase256_check.py --out /fresh/absolute/output
```

An optional `--verify-primary` also verifies the five separately acquired
PDF byte bindings. Those references need not be redistributed for the
portable computation and Lean replay. Lean4.32.2 and the exact mathlib
revision are required; their executable/package paths can be passed to the
runner.

The author replay with primary checks passed in4.383seconds. Five Lean
declarations compiled with only the permitted standard axioms. Removing
transversality, weakening the strict cardinality bound, and repeating an
odd walk an even number of times each failed compilation. Coincident
nonadjacent marks were rejected by the finite checker under Python `-O`.

| Literal diagnostic | Group order | Prime | Raw H1 dimension | Original top complement components | Result |
|---|---:|---:|---:|---:|---|
| Previously used independent marking | 32 | 131 | 9 | 2 | Boundary test and safe paths pass |
| SmallGroup96_117 marking | 96 | 389 | 25 | 2 | Boundary test and safe paths pass |
| SmallGroup96_216 marking | 96 | 389 | 25 | 2 | Boundary test and safe paths pass |
| SmallGroup216_102 marking | 216 | 877 | 55 | 9 | Boundary test and safe paths pass |
| A5×C2 marking | 120 | 487 | 31 | 1 | Nonorientable exterior has a verified closed odd walk |

The first four rows deliberately include failures of the original one-stage
closed-surface test. They are marked-group diagnostics, not newly claimed
polytope monodromy examples. The catalogue-style names record their GAP
acquisition; the exported certificate depends on the literal permutations
and reconstructs the group and its cellulation directly. The last row is
the direct product of the displayed A5 action on five points and the
transposition on two separate points.

For all five inputs, every base-vertex boundary class is tested against both
end homology spaces. Safe translations are checked from three specified
deck coordinates for every fundamental graph loop and for paths to a common
exterior fiber. All qualifying supplied endpoints are tested with the short
escape paths. These are exact finite checks of the argument's interfaces;
they are not an exhaustive enumeration of the cover or a proof for all
groups and all large primes.

Primary readings for this packet are the original general question on
Cunningham–Pellicer PDFp8, the expectation and family example on Cunningham
PDFpp6–7, and Monson–Schulte's Theorem2.4/Remark2.5 and Lemma3.3/Theorem3.4
on PDFpp4–6. The previously reviewed Tomotope infinite-cover theorem is
credited as prior work. Lekše2026 is a priority-search reference only:
maniplex symmetry-type realization is not used to supply polytopality.

The PDF is an ordinary seven-page rendering of the complete markdown
manuscript, not a complexity measurement or a claim about historical page
compression. All seven pages of the initial rendering were visually read;
after the final verification paragraph and author-status edits, the changed
first and last pages were checked again. Rendering diagnostics are recorded
separately. Formal scope remains exactly the five declarations listed in
`phase256_formal_scope.md`.
