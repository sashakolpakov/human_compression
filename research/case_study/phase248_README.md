# Independent review: odd-primary kernels

Read `phase248_review.md` for the mathematical audit and
`phase248_contract.json` for all twenty-five reviewed source dispositions.
The accepted object is the frozen phase236 principal L014 contract,
with its explicit marking correction and retained Cunningham–Pellicer
theorem. No author artifact is modified. There is no conjecture or ratio
claim.

The independent program `phase248_presentation_check.g` reconstructs five
literal source presentations in GAP, without using the author’s matrices.
It verifies exact finite orders, the two automorphisms, the marked
semidirect products and all sixty-four intersections. A coordinate-plane
countermodel checks that the prime-index hypothesis cannot be omitted.

Run the complete portable review from a directory containing the bound
artifacts, with a fresh output path:

```sh
python3 -B -O phase248_check.py --out /private/tmp/phase248_fresh \
  --gap /opt/homebrew/bin/gap \
  --lean /Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean \
  --packages /Users/sasha/bogachev/formal/.lake/packages
```

Add `--verify-primary` if the two bound L014 source files are available.
Without that option the executable replay is PDF-free. The review binds
all author exports, the dependency manifest, its own exports, the ten
source-proof spans and twenty-five row dispositions. It freshly reruns
the author’s eleven examples, three semantic mutations and five Lean
proofs, then the independent literal presentations. Existing output paths
and symlinks are refused, including dangling symlinks.

The artifact allowlist is precisely `phase248_manifest.json` plus its
`exports`, `phase236_manifest.json` plus its `exports`, and
`formal/dependency_manifest.json`. The optional source files are the two
`source_artifacts` in the review manifest. GAP, the pinned Lean compiler,
and the pinned dependency trees with compiled libraries are external
execution dependencies. The primary Cunningham–Pellicer theorem was read
remotely; it has no local binding. Finite computations and five formal
interfaces do not replace the complete written all-parameter proof.

The review logs are audit evidence. They do not create additional source
credit or a second mathematical proof charge for the author’s examples.
