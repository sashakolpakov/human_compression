# Independent projective-line classification review: replay

The exact author freeze is `phase230_manifest.json`, SHA256
`2adb69dc5b475b0ec2fd629c03286505c4ca88a9e9baecbb5b2d0e5fe79dcec0`.
The independent review is frozen by `phase234_manifest.json`. Copy both
packets preserving their relative paths and non-primary retained inputs.

```sh
python3 -B -O phase234_check.py --out /tmp/phase234-new \
  --gap /path/to/gap \
  --lean /path/to/lean4.32.2/bin/lean \
  --packages /path/to/formal/.lake/packages
```

Use a new output directory. Existing paths and dangling symlinks are refused.
The command checks both freezes, reruns the author's exact finite and Lean
proofs and both deliberate bad-input controls, then runs the independently
written field-extension centralizer checks and two false-weakening examples.
It uses the Python standard library. GAP4.15.1 and Lean4.32.2 were used here.
The author's pinned dependency source revisions and trusted cached objects
remain part of the stated formal boundary.

`--bindings-only` requires neither GAP nor Lean. `--verify-primary` additionally
checks the two private original PDFs and their text extractions against the
author manifest. Those historical documents are not exported by this review.

The finite computation is an actual part of the mathematical proof. In
particular GAP's exact finitely-presented-group order algorithms are retained
computational machinery; a finite permutation image alone would not give the
needed upper bound. The separate centralizer tests are bounded diagnostics
for the written all-field lemma, not a replacement for it. Lean proves five
abstract obstruction lemmas, not the projective classification or its ten
universal-order computations end to end.

All nine pages of the unchanged author PDF were visually inspected. Its
hash, the exact principal-source verdict, the22 reviewed source rows,
retained classical inputs and unpaid secondary statements are recorded in
`phase234_contract.json` and explained in `phase234_review.md`. The two
classifications license at most two principal admissions; root owns the
registry and must count each source at most once. L079's seventeen-case
PΣL2(25) census, Conjecture11 and the named background constructions remain
outside the accepted scope. No open-question answer or ratio is added.

`phase234_manifest.json` is the complete publication allowlist for this
review. It includes review and scope, the independent GAP program and log,
fresh author replay evidence and this portable driver. It excludes primary
PDFs, source extracts and images, rasterized author pages, cached dependency
objects and temporary mutation programs. The immutable author packet remains
separate. Any future measured denominator must charge the required finite
program, retained-input conventions and full chosen topic umbrella under the
declared common metric.
