# Independent equal-label application review: replay

The author freeze is `phase229_manifest.json`, SHA256
`75a07ebe73b2cfd31db5d2904130f41c47f344eb74cbd92d86cca9f18776621e`.
The independent freeze is `phase232_manifest.json`. Preserve relative paths.
All author exports and the non-primary retained bindings must be present.

A fresh full scoped replay is:

```sh
python3 -B -O phase232_check.py --out /tmp/phase232-new \
  --lean /path/to/lean4.32.2/bin/lean \
  --packages /path/to/formal/.lake/packages \
  --gap /path/to/gap
```

Use an output directory that does not already exist. The checker refuses
existing paths and dangling symlinks. It runs the frozen Lean proof with the
pinned dependencies, reruns the author's small models, and independently
checks the literal permutation realization with GAP and two controls. It
does not infer an all-n proof from the finite examples. Standard library
Python suffices for the runner; GAP4.15.1 and Lean4.32.2 were used in review.

`--bindings-only` verifies the exact packet without requiring Lean or GAP.
Add `--verify-primary` when the privately retained original source PDFs are
available. Original PDFs, extractions and page images are not public exports.

The five-page review rendering is `phase232_application.pdf`. To regenerate
it, use Python with `pypdf`, plus `pandoc`, `xelatex`, `gs` and the fonts in
the frozen configuration:

```sh
python3 -B -O phase232_render.py --out /tmp/phase232-new-render
```

The renderer is an adaptation of the frozen phase228 layout helper. Its only
mathematical-display layout change is an explicit line break in dependency
path18 after its second arrow; the exact original and formatted bodies are
recorded in the report. All words, arrows and equation tags remain. Source
Math/Table/Code ASTs are checked before the typesetting-only transformation.
The immutable author manuscript is never edited. Regenerated PDF metadata
may change its binary hash. The stored PDF binds the exact five pages visually
reviewed; a fresh rendering needs its own inspection.

Read `phase232_review.md` and `phase232_contract.json` for the mathematical
verdict and scope. The original Corollary3.6 quantifies primes p; the proof's
extension to all integer p≥2 is valid and is recorded separately. Principal
source admission is licensed only once for F014, with the source's displayed
multiplication correction explicit. No open-question credit, measured ratio,
complete Lean theorem or whole-paper auxiliary coverage is claimed.

The manifest is the exact export allowlist. It includes our review and scope,
fresh Lean and finite evidence, the independent GAP code, optional renderer
and configuration, reviewed PDF and extraction, and replay instructions.
It excludes all historical primary documents, source page images, intermediate
rasterizations, dependency caches and Lean object files. The mathematical
papers retain their own dependencies; this review manifest is not a substitute
for a matched topic cost accounting.
