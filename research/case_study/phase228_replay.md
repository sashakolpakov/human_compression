# Phase228 independent review: replay and scope

This review accepts the complete written phase207 umbrella and its declared
L032 principal contract. It does not admit a new source, a solved open question,
a measured compression ratio, a complete multi-source topic, or an end-to-end
Lean proof of either manuscript. The full review is
`phase228_topic_A_review.md`; the 24-clause map is
`phase228_source_contract.json`.

## Portable binding replay

Place the exact `phase207_export.json`, its fifteen listed exports, and all
exports in `phase228_manifest.json` together, preserving relative paths. Then:

```sh
python3 -B -O phase228_check.py --out /tmp/phase228-new-report.json
```

The output file must not exist, including as a dangling symlink. This command
uses only the Python standard library. It checks all exported byte bindings,
the complete provenance partition, native text metrics, formal-log bindings
and standard axiom reports, archived render bindings, and the explicit scope
and accounting boundaries. It does not rerun Lean, typeset documents, review
mathematics, or repeat visual judgment.

With the fourteen exact retained inputs from the author manifest available,
including the privately retrieved source PDF and extraction, add
`--verify-retained`. With both retained predecessor manuscripts available,
add `--rebuild` for a fresh byte-exact provenance-builder invocation:

```sh
python3 -B -O phase228_check.py --verify-retained --rebuild \
  --out /tmp/phase228-new-full-binding-report.json
```

The source PDF is not a required public export. Its bibliographic edition,
clause and hash are given in the contract; the reviewer read the complete
mathematical body and visually checked the principal statements.

## Fresh retained Lean execution

The independent review freshly ran the unchanged phase137 runner, not only
its archived report. With the five local modules, runner and pinned dependency
manifest from the retained bindings, Lean4.32.2 and the specified Mathlib
checkout available:

```sh
python3 -B -O phase137_supported_kernel_helly_check.py \
  --packages /path/to/formal/.lake/packages \
  --lean /path/to/lean4.32.2/bin/lean \
  --output-dir /tmp/phase228-new-lean
```

Use a fresh output directory. The bound independent report is
`phase228_retained_lean_report.json`, with seven corresponding logs. Five local
modules and two selected Mathlib modules were freshly compiled. All thirty-four
selected standard-only axiom reports are inherited in phase207. The report's
older eleven-new/twenty-three-old labels refer to phase137. This is partial
formal coverage, as specified in the review; no source-to-polytope existence
theorem has been formally composed.

## Optional render replay

The reviewer rendered the unchanged complete manuscripts and inspected all
fifteen umbrella pages and four application pages. The renderer requires
Python with `pypdf`, and `pandoc`, `xelatex`, `gs` on PATH, with STIXGeneral,
STIX Two Text and Menlo fonts. The configuration is separately frozen.

```sh
python3 -B -O phase228_render.py --out /tmp/phase228-new-render
```

Use a fresh output directory. A newly rendered PDF may have a different hash
because PDF metadata and tool versions can differ. The stored PDF hashes bind
the exact reviewed rendering. Inspect the new output and diagnostics rather
than interpreting byte equality as a mathematical requirement. The script
checks preservation of mathematical, table and code AST nodes and writes
layout evidence. The original source PDF's eight pages were not reset in this
format; **15+4 versus 8 is not a matched compression ratio**.

## Export allowlist and costs

`phase228_manifest.json` is the complete review export allowlist. It includes
our review, scope and cost records, renderer and configuration, our two rendered
PDFs and extracted texts, their logs, and the fresh retained Lean evidence. It
excludes the historical source PDF, its extraction, source page images,
intermediate render images, tool caches and object files. Author phase207 is
retained unchanged and is listed separately in the manifest.

The complete chosen umbrella is charged within Topic A even when its first
application uses only one branch. Any other topic independently pays its whole
chosen umbrella. Native full-file measurements here do not replace a matched
source/replacement proof-cost metric. The remaining five planned application
papers and the chronological acquisition measurements remain unfinished.
