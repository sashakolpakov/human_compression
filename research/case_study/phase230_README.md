# Dihedral centralizers and regular polytopes over a projective line

This private author package gives one complete written derivation of the principal rank-at-least-four classifications for PSL₂(q) and PGL₂(q). It is ready for independent review. The historical conclusions are credited to Leemans–Schulte; the 11-cell and 57-cell are credited to Grünbaum and Coxeter. No new open-conjecture solution or whole-paper compression rate is claimed.

Read `phase230_rank_one_classification.md` or its nine-page PDF, then the exact source ledger and contract. The common argument uses dihedral-centralizer descent and an odd-order normalizer obstruction. Dickson's subgroup types, the usual projective-group structure facts and the string C-group/polytope correspondence are explicit retained inputs.

The exact finite replay covers six exceptional rank-three marking classes, their presentations, all fourteen compatible ordered local pairs, the ten duality representatives, their universal group orders, and every subset-intersection identity for the resulting rank-four markings. It additionally verifies group identifications, self-duality, face counts, the 11-cell's complete graph and the auxiliary order-96 group's structure. GAP's exact finite-presentation machinery supplies the universal-order calculations; these are not formal Lean order certificates.

The Lean file proves five general algebraic steps ending in the facet-normalizer obstruction. It does not formalize the projective-matrix calculation, Dickson's classification or the finite enumerations. All five declarations compile with only the standard axioms `propext`, `Classical.choice` and `Quot.sound`.

Run in a fresh output directory:

```sh
python3 -B -O phase230_check.py \
  --out /private/tmp/phase230_independent_replay \
  --gap /opt/homebrew/bin/gap \
  --lean /Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean \
  --packages /Users/sasha/bogachev/formal/.lake/packages
```

Adjust executable and package paths for the local installation. The driver checks the package revisions in `formal/dependency_manifest.json` and requires Lean 4.32.2. The supplied author replay passed under Python optimization. A wrong Petrie relation and a dependent distinguished marking are both rejected by the mathematical checks. The output-directory preflight rejects existing paths and symlinks.

The PDF was rendered with:

```sh
pandoc phase230_rank_one_classification.md --from=markdown \
  --pdf-engine=xelatex -V geometry:margin=25mm -V fontsize=11pt \
  -o phase230_rank_one_classification.pdf
```

The retained primary PDFs and extracted text are bound by hashes; they are not exported as new work. Both primary texts were read completely, and L083's ten-row table was also inspected visually. The source ledger distinguishes replaced auxiliary arguments from retained background and unpaid material.

In particular, L079's additional seventeen-case PΣL₂(25) census is unpaid. Its Conjecture 11 is not solved or asserted currently open here. L083's one-relation J₁ × PSL₂(19) and chiral constructions cite other prior sources and are not rederived. These qualifications stay attached to any principal-contract admission.

No public files, earlier frozen records, corpus credits or compression measurements are changed by this author package.
