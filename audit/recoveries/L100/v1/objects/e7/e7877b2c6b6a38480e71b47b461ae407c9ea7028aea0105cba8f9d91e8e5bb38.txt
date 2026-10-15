# A common panel census for M22 and M23

This phase applies the same arbitrary-rank recognition and exhaustion theorem used for J2, J1, M11 and M12 to two further old classification targets. The intended class is firm, flag-transitive, residually connected, residually weakly primitive (RWPRI) coset geometries satisfying the rank-two intersection condition `(IP)2` and local two-transitivity `(2T)1`. Equivalence is under the full automorphism group of the specified group and arbitrary permutation of types.

**Status:** both complete enumerations and all independent witness checks passed. The certificates bind each calculation to its exact executed sources, inputs and terminal checkpoints.

| Group | Catalogue target | Subgroup conjugacy classes imported | Published total counts, ranks 3–5 | Published nontruncation counts, ranks 2–5 |
|---|---|---:|---|---|
| M22 | L101, 2003 | 156 | (25,16,9) | (1,20,12,9) |
| M23 | L098, 2004 | 204 | (13,21,10) | (0,3,16,10) |

M22 gives **7,25,16,9** classes in ranks 2–5 and none above rank five; all 57 witnesses pass independent recognition. Its nontruncation counts are **1,20,12,9**, agreeing exactly with both primary comparisons. Its 156-anchor search took about 325 seconds. M23 gives **4,13,21,10** classes in ranks 2–5 and none above rank five; all 48 witnesses pass. Its nontruncation counts are **0,3,16,10**, also matching both primary tables exactly. Its 204-anchor search took about 404 seconds. The two new groups therefore contribute 360 exhausted stabilizer anchors and 105 independently recognized witnesses.

The numerical sources and their access limitations are documented in [the source audit](phase7_sporadic_source_audit.md). No original geometry list is read during enumeration or needed to certify completeness.

## Uniform theorem and retained input

The recognition and maximal-residue augmentation proofs are those in [phase-six theory, §§2–4](phase6_sporadic_theory.md). They apply to every finite group; the locally two-transitive specialization merely restricts a panel inclusion `B < P` to one with two `B`-double cosets in `P`.

Explicitly, for each subgroup B and each finite family of overgroups P_i, put `K_S = <B,P_i : i in S>`. Require:

1. B is maximal in each P_i, and `|B\P_i/B| = 2`.
2. `K_S intersect K_T = K_(S intersect T)` for all S,T.
3. Every nonempty K_S has at least one deletion subgroup maximal in K_S.
4. The deletion-parabolic coset systems of all subfamilies of size at least three satisfy typed Helly, so every partial flag has a common group element.
5. Every two-panel residue is a partial linear space or a digon.

These conditions are necessary and sufficient for a geometry of the stated class with acting group K_I and Borel B. In particular, local two-transitivity is the panel condition in item 1, not an assumption that the ambient permutation action is two-transitive. The two-panel condition uses all relevant B-double cosets; no single-orbit shortcut is used.

A complete subgroup catalogue supplies representatives B of all conjugacy classes. Maximal subgroups of every catalogue representative, exact transporters, and normalizer orbits supply the actual maximal overgroups of each partial join. Every valid RWPRI tuple has a maximal deletion, so it occurs by augmenting a stored lower-rank tuple through one maximal overgroup. This includes the final extension to G. The assertion is not that every deletion is maximal.

Every extension strictly enlarges its join. The prime-factor bound `rank <= Omega([G:B])` is only a mathematically justified upper bound on this chain length. The implementation additionally computes an empty next level, records it in a terminal checkpoint for every Borel anchor, and refuses completion otherwise. A chosen rank cutoff is not exhaustion evidence.

The imported input remains substantial: TomLib's complete subgroup-conjugacy catalogue and GAP's exact finite-group algorithms. The common theorem eliminates separate geometry-enumeration arguments; it does not replace the subgroup classifications. No part of this arbitrary-rank enumeration theorem is claimed as fully Lean formalized.

## Marked torsor interpretation

The group-dependent data can equivalently be expressed on the regular G-torsor. A subgroup H corresponds to its coset partition, or to the zero-one matrix `A_H = sum_{h in H} R(h)`. Entrywise intersection encodes subgroup intersection; Boolean transitive closure of the union encodes the generated subgroup. Thus the recognition conditions are a finite marked-partition diagram on one common torsor, with exact normalizer/automorphism orbits removing duplicate markings. This is an alternative coordinate description of the proved algorithm, not an extra hypothesis that removes the imported subgroup data or the finite flag checks.

## Independent checks and counting conventions

The search stores representatives modulo ambient conjugacy and type permutation. A separate pass fuses them under Aut(G) and type permutation, using exact successive subgroup transporters and stabilizers. Each witness is then reconstructed from its maximal parabolics and checked by the independently written `phase4_geometry_checks.g`: named-group identification, firmness, residual connectedness, RWPRI, local two-transitivity, all rank-two intersection tests, and flag-transitivity. The verifier does not trust the search's acceptance flags.

The 2004 table reports all objects in the specified class. The 2005 table removes those occurring as truncations of higher-rank objects. Our post-processing tests every relevant type subset of every higher-rank representative, requiring exact Aut(G)/type equivalence. In this phase all higher-rank objects are in the same locally two-transitive class. The broader non-2T convention considered in phase six is a different question and is not silently substituted.

The maximal-object-stabilizer classifications, such as L119 for M11 and the later M22 work of Leemans–Rowley, impose different axioms. They are not counted as consequences of this RWPRI census.

## Reproduction and changes from phase six

Requirements are Python 3, GAP and GAP's TomLib package. GAP is found through the `GAP` environment variable or PATH. From the repository root:

```
python3 research/leemans/phase7_sporadic_run.py M22
python3 research/leemans/phase7_sporadic_finish.py M22
python3 research/leemans/phase7_sporadic_build_certificate.py M22
```

For a fresh replay, use a disposable copy and remove the generated `phase7_sporadic_M22_2T_*` files and checkpoint directory there; preserve the original certified package. The runner refuses to overwrite an existing progress file. Replace M22 by M23 for the second target. The search supports `--resume`, preserving all completed terminal anchors and checking their source/checkpoint hashes. It records an in-progress run before GAP starts, so an interrupted log is not overwritten. Each final certificate binds exact executed sources, logs, witness files, prerequisite verifier, and all terminal checkpoints.

The phase-seven search is a separate fork. Its mathematical tests are unchanged from phase six; group selection is configurable, local two-transitivity is imposed by default, and an order-indexed GAP record replaces a sparse list for the maximal-inclusion lookup. All phase-six executed sources and certificates remain unchanged. HS and J3 are accepted configuration names for possible later work; support in a command-line parser does not assert that those searches ran or finished.

## Separate source-dataset correspondence

After each independent census completed, the corresponding rank-three through rank-five data in the recovered Cambridge supplement were parsed as explicit permutation arrays. The narrow parser accepts only the documented subgroup/list grammar and literal identity symbol; it never executes Magma source. Each source ambient group is identified with the named TomLib group by an exact isomorphism, and each source geometry is independently checked before matching.

The M22 archive contains 36,26,10 raw records and selects 35,22,9 of them. Some raw records are not locally two-transitive; these are verified against the broader axioms and explicitly excluded from this phase's comparison. Remaining duplicates can fuse under Aut(M22) and type permutations. M23 has 13,21,10 raw and selected records. All 72 raw M22 records pass the broader axioms; six fail local two-transitivity and are explicitly excluded. The remaining 66 records cover exactly the 25,16,9 census classes, as do the selected lists. All 44 M23 records pass the required axioms and match the 13,21,10 census classes. Thus the two archives cover every independently generated class of ranks three through five. The comparison certificates report every match, exclusion and coverage set, rather than inferring equivalence from identical counts. They do not cover rank two, whose exhaustion is certified independently.

Reproduce this optional source comparison using an explicitly supplied external archive:

```
python3 research/leemans/phase7_sporadic_archive_compare.py M22 --archive PATH
```

The archive URL and hashes are recorded in the resulting report. The source archive itself is not distributed. Its data do not enter the independent search or its exhaustion proof.

The source-archive comparison is optional. The certificate builder includes it, and validates all its hashes, when the comparison report is present; a fresh census can be certified without downloading any geometry archive. To reproduce the larger published certificate including that comparison, run the archive command after `finish` and before `build_certificate`.
