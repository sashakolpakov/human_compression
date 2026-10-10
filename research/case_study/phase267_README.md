# Primitive-square independent review

`phase267_review.md` accepts the complete unchanged arithmetic proof of L043 Conjecture 6.1 and the six limited algebraic declarations in frozen phase266. The source conjecture is bound to arXiv:1606.08017v1 (26 June 2016), p. 22. The retained character theorem was checked in the primary Cohen–Kapetanakis–Reis 2022 PDF, physical p. 4 / printed p. 643. Private primary files are retained hash bindings, not exports.

Replay from this directory, using a fresh output path:

```sh
python3 -B -O phase267_check.py \
  --out /private/tmp/phase267_fresh \
  --gap /opt/homebrew/bin/gap \
  --lean /Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean \
  --packages /Users/sasha/bogachev/formal/.lake/packages \
  --verify-primary
```

Adjust executable and package locations as needed. Omit `--verify-primary` when the private PDFs and extracted texts are unavailable; mathematical bindings, finite checks and formal replay still run. The archived report records a run with all private source hashes verified.

The runner copies the old programs into its fresh output directory. The old witness verifier writes beside itself, and both old Python programs rely on assertions. Do not run them in the frozen source directory or with `-O`. The aggregate driver unsets `PYTHONOPTIMIZE`, starts those children without `-O`, and checks their assertion mode. Its own explicit checks remain active under optimization.

The replay checks 66 nonnested reduction cases, 23 nested fields, all eleven exceptional witnesses, 214,132 independently enumerated primitive pairs, four actual norm embeddings, 3,354 finite algebra pairs, four corrupted certificate/bound variants, and all six Lean declarations with four hypothesis controls. Finite diagnostics supplement the written uniform proof.

`phase267_manifest.json` binds the review, new programs and selected replay outputs. Build products, mutation copies and private primary texts/images are excluded. Phase266 and all old proof files remain unchanged. The review adds no question or principal-source count and makes no historical-priority or complete Lean claim.
