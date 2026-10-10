# Replaying the independent toroidal-pyramid review

Keep the complete frozen224 and239 packets, their declared dependencies, and this review together. Primary PDF files are optional at runtime; they were read as specified in the review and are separately bound. They are not exported as our work.

```sh
python3 -B -O phase242_check.py \
  --out /private/tmp/phase242_fresh \
  --gap /opt/homebrew/bin/gap \
  --lean /Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean \
  --packages /Users/sasha/bogachev/formal/.lake/packages
```

Use a fresh output path and adjust executable paths for the local installation. The driver verifies the two immutable author manifests, all their exports and bound dependencies, this review, the exact Lean version and every package revision. `--verify-primary` additionally checks the two retained PDFs and their bound extractions. `--bindings-only` omits executable replay.

The full replay executes both frozen author drivers, compares their literal witnesses to the frozen output, then runs the independently authored native-GAP orientation calculation and Python surface calculation. The review contains the general mathematical argument; the bounded computations cannot replace it. The output reports four new and nine inherited Lean statements, not thirteen new statements or a complete formal proof.

The source allowlist is `sources/phase227_stratified2022.pdf`, its `.txt` extraction, `sources/phase224_MonsonSchulte.pdf` and its `.txt` extraction. No primary PDF pages or substantial source text are exported by this packet. Cached imported Lean objects and GAP's exact algorithms remain trusted components.
