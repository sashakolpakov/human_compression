# Livingstone source audit: author freeze

The author outcome is **literal P recovered; literal Q refuted as printed; explicitly repaired Q recovered**. There is no unchanged whole-source principal admission and no open-conjecture claim. Full independent review is pending. The enumeration reviewer independently confirmed the missing-clause wording and the twelve-versus-two count from the primary page, but did not review the complete new package.

The source is L068, Hartley–Hubard–Leemans (2012), 22 pages. The complete primary text was read; the author additionally viewed physical PDF pages 10, 13, 16, 19, 20 and 22 to check the two definitions, the disputed passages, both stabilizer lattices and both main diagrams. The frozen source hash appears in the ledger. No source full text is included in this export.

The replacement application is `phase179_livingstone_manuscript.md`, rendered as six ordinary A4/11pt pages. All six initial pages were visually inspected; a clipped table was corrected by shortening the headings, and the corrected table and final pages were inspected again. Four underfull-box diagnostics remain; there are no overfull boxes or missing-glyph diagnostics. The PDF includes neither the retained umbrella and C manuscript nor the required programs. Its page count is not the total replacement cost.

The portable reproduction command, from any working directory, is:

```sh
python3 -O /path/to/phase179_run.py \
  --output-dir /new/empty/path \
  --packages /path/to/pinned/.lake/packages \
  --gap /path/to/gap \
  --lean /path/to/lean
```

`--inputs` can point to a copy of the four pinned source inputs. The output path must not exist, including as a dangling symlink. The runner stages all sources privately, verifies hashes before and after execution, checks the pinned Lean dependency revisions and clean tracked sources, and uses a private symlink overlay for cached dependency objects. It executes the retained C finite certificate, the new graph/source bridge, and a fresh Lean compilation. Python assertions are not used as validation gates, so `python3 -O` preserves all checks.

The accepted fresh author run is `/private/tmp/phase179_author_final`. Copies of its three logs and JSON report are under `phase179_author_replay/`. GAP 4.15.1 and TomLib 1.2.11 were used. The retained C calculation took 1.584654 seconds, the new source-object bridge 7.919880 seconds, and Lean 1.247756 seconds; these timings include the recorded run conditions and are not performance guarantees. The current J1 data hash is `576834302b6da30248f34565d6559b857160fdbd67066d1e67c64f0191b8b143`.

Three mathematical mutations reject: omit the induced-quadruple repair, replace P's white-pentagon facet condition by the orange one, or change Q's vertex/block overlap from three to two. Run them with:

```sh
python3 -O /path/to/phase179_controls.py \
  --output-dir /another/new/path --gap /path/to/gap
```

These are author-designed controls, not an independent reimplementation. An earlier exploratory mutation removed the Petersen opposite-edge condition and still passed; on the constructed object families, the other finite conditions made that restriction redundant. It is therefore **not** reported as a rejected control or as an independent theorem of general incidence structures. The final checker preserves the literal source condition.

The generic Lean proof has three freshly checked declarations. `reconstruction` uses `propext`; the finite-set declarations additionally use `Classical.choice` and `Quot.sound`. No `sorry`, extra axiom or native-evaluation certificate is used. This is a useful reusable component, not end-to-end formal verification of J1 or either polytope. The finite counterexample remains an exact GAP certificate with an explicit readable flag and a complete search of its possible type-one extensions.

The local required mathematical and executable text comprises 44,524 UTF-8 bytes: the 21,077-byte application, 12,898-byte GAP checker, 7,449-byte driver and 3,100-byte Lean source. Charging the entire retained U and C manuscripts and the retained C finite program adds 135,006 bytes, for an explicit 179,530-byte written/executable inventory. This is an intentionally unreduced file-level allocation of the retained manuscripts, not a minimal proof-size claim. Presentation, provenance, logs and controls are separately itemized support costs. There is no matched compression ratio.

The twelve-source screen in `phase179_intake_screen.md` is a work queue, not twelve admitted contracts. Root separately owns the L092/phase182 intake; phase177 owns L059 and its neighbours. The new source-specific result of this author task is the L068 audit and the reusable reconstruction component described here.
