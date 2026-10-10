# Topic E: Projective-line centralizers and exceptional facets

This topic now has three actual papers:

1. [Centralizers, facets and finite amalgams on the projective line](phase238_topic_E_umbrella.md) is the common theory U_E. It contains the full centralizer, rank and facet reductions, and the complete finite table with its proof interface.
2. [The two projective special linear four-polytopes](phase238_L083_application.md) is application A1. It derives the PSL₂ classification, uniqueness, local geometry and stated universality.
3. [The simplex as the unique higher-rank projective general linear polytope](phase238_L079_application.md) is application A2. It derives the PGL₂ classification and the unique simplex marking independently of A1.

These rework the accepted combined proof. They add no principal-source or conjecture credit. L083 and L079 each retain their previously reviewed principal classification contract; neither becomes a whole-paper replacement. The exact 22-row source ledger is in `phase238_contract.json`. The seventeen-case PΣL₂(25) census is still unpaid, and the distinct Conjecture 11 is outside this recovery. Its historical answer is being recorded separately; it is not described as currently open.

The common mathematical dependency is `phase230_finite_check.g`, used once in this topic. Its exact GAP calculations establish the six local marking classes and the ten presented universal groups, then verify their markings and coset properties. Five inherited Lean declarations verify only the abstract normalizer obstruction. The classification proofs, projective centralizers and universal-order calculations are not fully Lean certified. Subsequent matrix-formalization work is not silently added to this frozen dependency graph.

The builder copies the complete reviewed common proof, with exact provenance, and makes its retained covering correspondence explicit. The applications supply their separate quotient exclusions and geometry. This is a mathematical split with a real common interface; neither application repeats the common proofs or assumes the other application.

Run the full portable replay in a fresh output directory:

```sh
python3 -B -O phase238_check.py \
  --out /private/tmp/phase238_fresh \
  --gap /opt/homebrew/bin/gap \
  --lean /Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean \
  --packages /Users/sasha/bogachev/formal/.lake/packages
```

The output path must not exist, including as a symlink. The driver verifies all author bindings, rebuilds the exact common paper in memory, and replays the unchanged finite and partial formal proofs with both false controls. `--bindings-only` omits the executable replay. `--verify-primary` additionally checks the locally retained source PDFs and extractions; those primary files are not exported as our work. Executable and package paths can be changed to the local installation, with the declared versions and revisions preserved.

`phase238_dependency.json` records the proof edges and exact required files. The measurement note and bound source-span proposal distinguish a future matched comparison from ordinary size inventory. Full U_E and its required program are charged once inside this topic, followed by each full application. Every other topic pays its entire chosen umbrella independently, even when it overlaps U_E. There is no cross-topic discount and no compression ratio at this checkpoint.

This is a two-source topic, not the requested eventual twelve-source volume. Its complete applications are correspondingly short. They have not been padded to twenty pages. All rendered pages are included for ordinary scholarly review; page counts are not a compression statistic. The split itself still requires independent review before replacing the combined manuscript as the public topic presentation.
