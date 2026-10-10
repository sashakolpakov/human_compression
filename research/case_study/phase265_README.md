# L009 principal application: author packet

This packet recovers the complete corrected principal classifications in
Delaby–Leemans–Tranchida, *Geometries with trialities arising from linear
spaces*, Algebraic Combinatorics9(2)(2026),379–402. The complete common paper
is `phase265_flag_relations.md`; its standalone application is
`phase265_triangle_application.md`. The former is a real reusable proof
object, not a paragraph-cost label assigned to a monolithic manuscript.

`phase265_contract.json` states the precise contract, and
`phase265_source_ledger.json` maps44 source clauses, retained inputs and
exclusions to13 byte-bound proof spans. The dependency DAG exposes the
retained classification and norm-shell inputs. In particular, no claim is
made to recover the square/Desargues auxiliary examples or the external
hypermap catalogue identifier. The principal theorem is not conflated with
the separate cloning question packet.

The original construction and classification targets remain attributed to
the source authors. The determinant-semilinear condition corrects a false
GL-containment necessity, with an exact affine-plane example over F9. Earlier
recorded circle-list corrections are explicitly reused, not rediscovered.
All principal residue diagrams and full correlation groups are included;
field automorphisms correct the source's affine AGL labels.

## Replay

The distributed replay does not need the private primary PDFs. It requires
Python3, GAP4.15.1, Lean4.32.2 and the pinned Mathlib dependencies in
`formal/dependency_manifest.json`. Give their actual installation paths:

```sh
python3 -B -O phase265_check.py \
  --out /fresh/output-directory \
  --gap /path/to/gap \
  --lean /path/to/lean \
  --packages /path/to/.lake/packages
```

Add `--verify-primary` only when the exact privately retained primary PDFs
are present. Every output path must be fresh; dangling symlinks are rejected
before resolution. The runner verifies export and proof-span bindings,
executes the complete F9 frame action, exceptional A7 and U_H(2) interfaces,
the entire U_H(4) residue, nine literal plane/higher-dimensional models, and
four deliberate failing mutations. It then compiles the four actual Lean
matrix/orbit theorems against pinned clean dependencies, checking each axiom
report. It does not treat successful computation as independent acceptance
of the written all-parameter proofs.

The renderer is optional. `phase265_render.py` uses Pandoc, XeLaTeX,
Ghostscript and Python pypdf to render both author papers, preserving the
sources and reporting PDF hashes and diagnostics. The PDF files are our
own manuscripts; primary source PDFs, text extractions and rasters are not
exports.

## Formal and computational boundary

The Lean scope is `phase265_formal_scope.md`. Four declarations certify
actual equal-determinant matrix torsors, the semilinear determinant formula,
the resulting matrix-fiber transport equivalence, and general subgroup orbit
saturation. They do not certify the full group classification, geometric
reconstruction, all residual connectedness, or the complete source theorem.
The all-field and all-dimension statements have written proofs using exact
retained inputs. Finite computations supply complete exceptional cases and
implementation controls, rather than a substitute for those proofs.

The cloning proof is separately frozen in `phase265_cloning_manifest.json`
and reviewed under268. Neither its files nor any question credit is included
in the main manifest. Likewise the source correction is not an answer to an
explicitly open conjecture. No principal-source count or compression rate is
changed by this author packet; independent271 review and root admission are
separate steps.

## Accounting

Charge the complete common paper and application, their necessary finite
programs and formal interface, and the stated retained inputs. In a topic
comparison the full chosen umbrella is charged even when it overlaps a
second topic. The dependency inventory gives bytes, words and presentation
pages only; it is not a matched complexity statistic and supplies no ratio.
