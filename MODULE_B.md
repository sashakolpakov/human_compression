# Module B: Forest coordinates and primitive coset geometries

Read the complete [16-page manuscript](research/case_study/phase132_module_B_render/application.pdf)
or its [Markdown source](research/case_study/phase132_module_B_manuscript.md).
The [independent review](research/case_study/phase141_module_B_review.md)
and [root admission](research/case_study/phase139_module_B_root_admission.md)
accept its four-source declared mathematical contract with explicit source
corrections and retained inputs.

    U + Forest coordinates and primitive coset geometries
        -> declared principal results of N001, N003, N008 and L030.

| Source | Results derived |
|---|---|
| Buekenhout–Cara, *Some properties of inductively minimal geometries* (1998), N001 | All four clauses of Theorem 1 from unit-tree coordinates and the retained earlier classification |
| Cameron–Cara, *Independent generating sets and geometries for symmetric groups* (2002), N003 | Extremal markings, three counting conventions, strong and relative independence, and maximum-rank geometry recognition in the stated degree and finite numerical ranges |
| Archer–Cara–Krempa, *Using the Frattini Subgroup and Independent Generating Sets to Study RWPRI Geometries* (2005), N008 | Geometric Frattini containment, quotient transport, finite-p-group classification and residue tests, with the infinite generator-converse correction |
| García-Colín–Leemans, *An infinite family of locally X graphs based on incidence geometries* (2021), L030 | The weighted-star construction, residues, distances, diagram parameters and full graph automorphism groups, with three explicit source corrections |

One weighted-forest theorem computes subgroup intersections and completes
partial flags. Its unit-weight, sign-kernel and weighted-star specializations
supply three geometry constructions. U's relative-generation and Frattini
results supply the other coordinate description. The classification,
distance and full-automorphism arguments are included in the application.

The [contract ledger](research/case_study/phase132_module_B_checkpoint03.json)
contains 30 records bound to 22 proof nodes. These are source-contract rows,
not 30 newly discovered theorems. The earlier inductively minimal
classification and Whiston's results remain attributed inputs. The exact
source editions and reading limits are recorded in the
[intake](research/case_study/phase132_module_B_intake.json). In particular,
N001 is available as a complete authored transcription with damaged
diagrams, rather than an independently acquired original PDF.

The manuscript has 16 pages in ordinary A4, 11pt format. Its full body costs
64,827 UTF-8 bytes; the complete retained U-v2 adds 56,096, for **120,923 bytes**
with U charged once. No executable certificate is needed to complete these
written proofs. This is an inventory; a matched source compression factor
has not yet been measured. The six selected U proof spans alone are not
used as a discounted denominator.

Root read the complete manuscript and its used U proofs. Independent
review checked all four available source texts and all contract rows.
Fresh public finite checks passed 29,086 distance pairs, 144 subgroup pairs,
579 partial flags and the exact 63-vertex spectrum. The general conclusions
rest on the written proofs; those finite checks corroborate them.
Full Lean formalization remains incomplete.

```sh
python3 -B -O research/case_study/phase132_module_B_verify.py --output /tmp/NEW-module-B-integrity.json
python3 -B -O research/case_study/phase141_module_B_independent.py --output /tmp/NEW-module-B-finite.json
```

The first command checks documentary integrity; the second executes the
bounded independent diagnostics. Both work with the public files. Primary
publications and their page images are referenced, not redistributed.
Open-question results remain in the separate [question-results catalogue](CONJECTURE_RESULTS.md).
