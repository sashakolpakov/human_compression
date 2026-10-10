# Period lattices and mixed-prime polyhedra

This private author package contains a complete proposed principal-result
replacement for Hou–Feng–Leemans, *Regular 3-polytopes of order 2ⁿp*,
bound to arXiv:2001.02945v2 (14 July 2024), 17 pages. Independent review
is required before admission. No source, conjecture or compression credit
is awarded by this package.

Read `phase250_affine_lattice_umbrella.md` (the reusable affine and period
criterion), then `phase250_mixed_prime_application.md` (the complete
application). Matching PDFs are included. The application also uses the
full frozen Topic A umbrella and the earlier complete cubic {6,6}
component; their actual proof files and programs are bound in the manifest.
The 33-row source ledger binds 14 exact proof spans. The contract lists
the main results, retained inputs, corrected auxiliary statement and exclusions.

The new positive work identifies one integral affine group for all three
{6,4} families, proves the exact presentation bridge, and obtains all
periods and dihedral extensions from it. The existing {6,6} component is
reused, including its full written proof and original programs. The
principal existence and type theorems remain attributed to the source.
The first R0 period relation in source Lemma 4.5 needs the displayed sign
correction; the original existence theorem survives. This is a correction
to the bound preprint, not a newly answered open question or a claim about
the uncollated journal edition.

## Replay

From the directory containing this file, choose a nonexistent output path:

```sh
python3 -B -O phase250_check.py \
  --out /private/tmp/phase250_fresh_replay \
  --gap /opt/homebrew/bin/gap \
  --lean /Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean \
  --packages /Users/sasha/bogachev/formal/.lake/packages
```

Add `--verify-primary` when the private source PDFs and text extractions
are present. Without that option the proof/code/dependency bindings are
still verified; only the primary-source file checks are omitted. GAP
4.15.1 with SmallGroups 1.5.4, Python 3, and the pinned Lean dependency
checkout are the tested environment. The historical {6,6} programs run
only in a staged output tree, with Python assertions explicitly enabled.
Frozen historical outputs are never overwritten.

The runner checks exact integer lattices, literal presentations, all
20,169 catalogue groups at order 384, scoped Lean proofs and negative
controls. Executing it cannot substitute for reading the uniform written
proofs. See `phase250_formal_scope.md` and `phase250_provenance.md` for the
remaining trust and attribution boundaries. Full umbrella dependencies
and proof programs remain chargeable; no measured rate is asserted.
