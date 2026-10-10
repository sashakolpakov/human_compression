# Working source compilation: thirteen principal contracts

**Required later correction:** the quoted N009 diagonal factors must be
read with the [corrected affine proof](research/case_study/phase138_N009_decomposition_erratum.md)
and [independent review](research/case_study/phase143_n009_decomposition_review.md).
This adds 5,967 required bytes to the historical inventory below, giving
357,315 bytes. The principal classification targets and census are unchanged.

This compilation is retained as reusable source material for the new
[umbrella and module programme](MANUSCRIPT_PROGRAM.md). It is not that
programme's product or benchmark.

**Thirteen declared principal-result contracts now follow from one
continuous manuscript**, with the recorded retained background and
source corrections. The [complete manuscript](research/case_study/phase110_commuting_pairs_integration_manuscript.md)
must be read with the [corrected contract ledger](research/case_study/phase116_commuting_pairs_corrected_ledger.json).
The [independent review](research/case_study/phase114_commuting_pairs_review.md)
and [root admission](research/case_study/phase120_thirteen_root_admission.md)
pass. This is internal review, not external peer review.

**The thirteen-source compression factor is unmeasured.** Its full
351,348-byte text includes all branches and eleven complete programs.
The twelve-source token lower bound of 1.347128 applies only to the
earlier manuscript. A source-count arrow alone does not measure savings.

## Exact intake

| ID | Authors and manuscript | Principal-result contract |
|---|---|---|
| N001 | Buekenhout–Cara, *Some properties of inductively minimal geometries* (1998) | Theorem 1, retaining the earlier foundational classification |
| N003 | Cameron–Cara, *Independent generating sets and geometries for symmetric groups* (2002) | Eight numbered targets, with finite-group scope and symmetric degree at least seven |
| N008 | Archer–Cara–Krempa, *Using the Frattini Subgroup and Independent Generating Sets to Study RWPRI Geometries* (2005) | Principal geometric and relative-generation results; unrestricted infinite converse corrected |
| L032 | Hou–Feng–Leemans, *On regular polytopes of 2-power order* (2020; revised 2019 author version) | Prescribed type and exact order existence |
| L035 | Hou–Feng–Leemans, *Existence of regular 3-polytopes of order 2^n* (arXiv:1802.08947v2, 2019) | Existence and complete eight-presentation classification with converses |
| F013 | Hou–Schulte, *String C-groups of 2-power order project onto a common string C-group* (arXiv:2605.20691v1, 2026) | Principal common-quotient and covering results |
| F016 | Cunningham–Feng–Hou–Schulte, *Symmetric polytopes whose automorphism groups are 2-groups* (arXiv:2512.15511v1, 2025) | Declared regular, alternating and free-extension clauses, orders and presentations |
| L088 | Hartley–Leemans, *On the thin regular geometries of rank four for the Janko group J1* (2005) | Six constructions, exhaustive rank-four classification and higher-rank exclusion |
| N013 | Montero–Ivić Weiss, *Locally Spherical Hypertopes from Generalised Cubes* (arXiv:2001.11082v1, 2020) | Halving, generalized-cube applications and declared exact local/toroidal models |
| N016 | Cunningham, *Chiral polytopes whose smallest regular cover is a polytope* (25 July 2023 author manuscript; 2024 publication) | Proved criterion and consequences, family obstruction, square-map application and finite two-cover example |
| L108 | Bonheure–Buekenhout–Leemans, *On the Petrials of thin rank 3 geometries* (2001) | Principal obstruction, connectivity, thin-case group equality and biduality; unconditional embedding corrected |
| N009 | Gomi–Loyola–De Las Peñas, *String C-groups of order 1024*, Contributions to Discrete Mathematics 13(1) (2018), 1–22, DOI [10.55016/ojs/cdm.v13i1.62475](https://doi.org/10.55016/ojs/cdm.v13i1.62475) | Complete nondegenerate marked classification, central descent/lifts, exact finite presentations and universal orders; quoted prior interfaces and literal-source corrections explicit |
| L066 | Kiefer–Leemans, *On pairs of commuting involutions in Sym(n) and Alt(n)* (2013; complete nine-page author PDF) | Theorems 1.1 and 1.2 including degree six, Theorem 3.6 and regular-polyhedron Theorem 4.4; all numbered items and printed tables accounted for |

```text
{N001, N003, N008, L032, L035, F013, F016, L088, N013, N016, L108, N009, L066}
    → Compress_13.
```

The 136 ledger rows include definitions, retained results, corrections
and unresolved questions. They are not 136 new theorems. The thirteen
contracts span 1998–2026 and overlap all preceding assemblies.

## What the additional shared theorem does

The finite-action theorem K(e) decomposes an action into orbits G/H,
computes its kernel from subgroup cores, and obtains centralizers and
normalizers from orbit multiplicities. For elementary abelian two-groups,
index-two stabilizers give the complete parity character. An equivariant
projection of configurations reduces extension orbits to stabilizer
orbits in its fibers.

There are two actual applications: the commuting-involution counts and
the earlier J1 extension census. For commuting endpoints, five orbit
multiplicities describe every action of C2 x C2; faithfulness, evenness
and endpoint reversal become explicit arithmetic conditions. Summing
them derives both all-degree formulas. Exceptional degree six is handled
separately by a complete census, including the full ambient automorphism
group. Classical orbit, core, centralizer and parity ideas remain credited.

The independent census examines 41,175 raw configurations and 138,240
subgroup intersections. It gives exactly two S6 regular polyhedra up to
isomorphism and duality and none for A6. It retains GAP's exact algorithms
and the string-C-group/polytope correspondence, but does not use the
published classification to filter candidates. All nine source pages
were individually inspected by the independent reviewer.

## Correction, verification and cost

Review discovered defective proof spans in the original phase110 ledger.
The additive phase116 correction supplies all sixteen complete spans;
the independent semantic checker also rejects hash-consistent truncated
or incorrect intervals. The original ledger alone fails admission.
Every one of the 120 preceding contract rows, 23 complete old sections
and all eight old program bodies is unchanged.

The new assembly has 27 numbered sections and eleven complete code/data
blocks totaling 93,086 bytes. Its raw size is 33,432 bytes larger than
the twelve-source version. This is cost accounting, not evidence of
compression. Complete source and replacement measurements remain work.
Retained background proofs remain explicit imports. This assembly adds
no Lean theorem, open-conjecture result or historical-priority claim.

From the repository root, choose fresh output paths:

```sh
python3 -B -O research/case_study/phase116_commuting_pairs_correction.py \
  --output /tmp/human-compression-thirteen-ledger.json
python3 -B -O research/case_study/phase114_commuting_pairs_review_check.py \
  --output-dir /tmp/human-compression-thirteen-review
python3 -B -O research/case_study/phase114_commuting_pairs_review_controls.py \
  --output-dir /tmp/human-compression-thirteen-controls
```

Python and GAP are required for the mathematical replay; the default
commands need only public inputs. Frozen pending-stage wording in older
artifacts is preserved; the root admission records the later verdict.
