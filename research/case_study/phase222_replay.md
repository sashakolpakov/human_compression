# Replaying the independent general-cover review

The accepted written proof and its limitations are in
`phase222_general_cover_review.md`; its twenty-clause attribution and source
interface audit is in `phase222_source_contract.json`.

The executable review requires this review packet, the fourteen files bound
by `phase216_export.json`, that manifest, and the separately frozen
`formal/CoverKernelChains.lean`. It does not require source PDFs by default.
With the specified Lean and mathlib installation available, run:

```sh
python3 -B -O phase222_check.py --out /fresh/review/output
```

For a different local installation, pass `--lean /path/to/lean` and
`--packages /path/to/.lake/packages`. The required toolchain is Lean 4.32.2
and the required mathlib revision is
`905b95818eb32af7874a58b427f50c1711a5e96c`.

Add `--verify-primary` to verify the eight separately acquired PDFs at the
paths in the source ledger and the frozen phase211 manifest. Those PDFs are
not in the review's public artifact allowlist.

The runner checks the fourteen author bindings before and after execution,
compiles five new and six retained Lean theorems in a fresh directory,
checks the standard axiom reports and three rejected altered proofs, and
reconstructs four independently written finite countermodels to false
weakenings. It refuses existing output paths, including dangling symlinks,
and retains its guards under optimized Python.

A PASS establishes this executable scope. The complete cubical and filling
argument is assessed by the written mathematical review, not by that PASS.
The resulting general theorem allows infinite covers; the stronger finite
minimal-cover question remains separate.
