# Eleven named manuscripts → one continuous replacement

**The declared principal results of eleven manuscripts spanning 1998–2026
follow as explicit corollaries of one continuous manuscript**, relative to
its disclosed background and corrected source contracts. The
[independent extension review](research/case_study/phase70_petrial_integration_recent_audit.md)
and [root admission](research/case_study/phase76_eleven_source_root_audit.md)
pass. There is no approved eleven-source length factor yet.

Read the [complete manuscript](research/case_study/phase65_petrial_integration_manuscript.md)
with its [exact contract ledger](research/case_study/phase65_petrial_integration_ledger.json).
It incorporates the ten-source reference correction and adds a shared
action-kernel theorem, gallery lemma and complete Petrial proof. Its original
pending-review heading is frozen; the linked later reviews supply the current
status.

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
| N013 | Montero–Ivić Weiss, *Locally Spherical Hypertopes from Generalised Cubes* (arXiv:2001.11082v1, 2020) | Halving, generalized-cube applications and the declared exact local/toroidal models |
| N016 | Cunningham, *Chiral polytopes whose smallest regular cover is a polytope* (25 July 2023 author manuscript; 2024 publication) | Proved criterion and consequences, family obstruction, square-map application and finite two-cover example |
| L108 | Bonheure–Buekenhout–Leemans, *On the Petrials of thin rank 3 geometries* (2001) | Principal obstruction, connectivity, thin-case group equality and biduality; unconditional embedding corrected |

```text
{N001, N003, N008, L032, L035, F013, F016, L088, N013, N016, L108}
    → Compress_11.
```

The ledger has 87 rows, including qualifications, corrected assertions and
unproved questions. It is not a count of 87 proved theorems. L108 uses a
complete authored browser rendering; a primary PDF has not been acquired.
All earlier version restrictions and retained inputs remain explicit.

## What the shared theory adds

The earlier image/kernel, relative-generation, primitive-coordinate,
square-lattice and endpoint arguments remain inside the manuscript. The
new action theorem identifies the same kernel on retained objects and
constructed objects when two maps are supplied: an injective equivariant
encoding by retained elements or subsets, and a surjective equivariant
forgetting map. The kernel is the intersection of retained stabilizer cores.

That theorem now has three checked applications: typed cosets, the geometric
endpoint construction and set-valued Petrials. A shared gallery proof supplies
free chamber actions and the exact residue stabilizers. In the Petrial case,
the kernel is `core_G(<a>)`, where a changes the old face. This exposes why
an unconditional automorphism-group embedding fails. Under the thinness
hypothesis, an order-two panel preimage forces the kernel to vanish.

The full Petrial argument still proves the obstruction, connectivity,
regularity and injectivity of the recovered old-face subsets. It covers
infinite groups and residues. These necessary branch arguments remain in
the replacement; the short final corollary depends on them.

## Attribution, cost and checks

The source authors receive credit for the operation and original results.
The [new attribution ledger](research/case_study/phase65_petrial_integration_attribution.json)
separates source ideas, integration arguments, reused phase25 work and
corrections. The [ten-source margin reader](ATTRIBUTION.md) remains a
separate frozen edition; its annotations have not been transferred silently
to this new manuscript. No historical novelty is claimed for the elementary
action or gallery lemmas.

The replacement has 25 numbered sections, 229,791 bytes and five complete
programs totaling 25,954 bytes. Adding this source costs 28,061 raw bytes,
including the full 10,533-byte Python controls. These are disclosed costs,
not a measured compression factor. The **1.6713× ten-source lower bound**
applies only to [Compress_10](COMPRESS_10.md).

The independent review reads all new proofs and actual applications, and
inherits the complete earlier integration review for unchanged branches.
All 79 earlier proof spans survive: 73 byte-for-byte, six with only the
already approved reference correction. Nineteen whole sections and all four
GAP programs are unchanged. Fresh author, independent and public executions
agree on seven Petrial examples, including two nonfaithful actions.

Run the public structural and finite-control checker in a new directory:

```sh
python3 research/case_study/phase75_eleven_source_verify.py \
  --output-dir /tmp/human-compression-eleven-new --run-petrial
```

It needs only distributed files and Python's standard library. It verifies
the exact proof spans and programs and runs the seven finite controls; it
does not machine-check the written proofs or reread private source captures.
The [independent wrapper audit](research/case_study/phase77_eleven_wrapper_recent_audit.md)
also checks rejected altered inputs and execution with assertions enabled.
The 41 Lean components retain their individual scopes; this extension adds
no new formal module. General conjectures and the separate
[cover-family theorem](COVER_FAMILY.md) are outside this assembly's claimed
principal-result reduction.
