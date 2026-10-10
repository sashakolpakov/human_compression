# Independent review of the PSL maniplex application

Read `phase263_review.md` for the complete accepted scope and qualifications.
The frozen author packet is phase258, manifest SHA256
`ccd07fd98645aa1ae31213b9c7d3f76501ca5225ae05992b64e7ac9dc80915cc`.

Run from an environment with GAP and the pinned Lean/mathlib packages:

```sh
python3 -B -O phase263_check.py \
  --out /private/tmp/phase263_NEW_OUTPUT \
  --gap /opt/homebrew/bin/gap \
  --lean /Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean \
  --packages /Users/sasha/bogachev/formal/.lake/packages
```

The output path must be fresh. The driver verifies the exact author manifest,
runs the complete author replay including both bound primary PDFs, checks
432 local triples and the two literal witnesses with independent Python
permutation arithmetic, checks six independently constructed field models,
and rejects a corrupted marker. Lean coverage remains the explicitly scoped
three new and two reused interface declarations.

Accepted for one corrected principal PSL source contract after root admission.
No whole-paper, question, priority, full-Lean or compression-ratio claim.
The separate PGL question is phase257/261. No frozen author file was changed.
