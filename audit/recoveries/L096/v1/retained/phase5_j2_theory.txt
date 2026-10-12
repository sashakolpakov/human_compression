# Independent arbitrary-Borel enumeration for the 2002 J2 classification

This phase extends the certified thin enumeration of `phase4_old_classification.md`. Its target is the entire L104 census: 8 rank-two, 19 rank-three, 3 rank-four geometries, and no higher ranks, under the paper's FT, firmness, RC, RWPRI, `(2T)1`, and `(IP)2` conditions. The original geometry list is not an enumeration input. The complete subgroup catalogue remains an explicit input.

The statement proved in this note is a complete enumeration reduction for every finite ambient group. The J2 search, full automorphism fusion, and independent witness checks have now completed and reproduce the principal census exactly, conditional on the imported subgroup catalogue.

## 1. Finite panel action

Fix a Borel subgroup B of a finite ambient group G. Let P(B) be the finite set of subgroups P of G such that B is maximal proper in P and P acts two-transitively on P/B. The normalizer N_G(B) acts on P(B) by conjugation. Write A_B for the image of this action in the symmetric group on P(B).

For a tuple of panel indices t=(t_1,...,t_r), let P_i be the associated subgroups and put

    K_empty=B,       K_S=<P_i : i in S>.

Every firm FT RC geometry satisfying the source axioms has such a tuple: its panel stabilizers lie in P(B), residual connectedness reconstructs every parabolic by generated joins, and the total join is its acting group. Conjugation by N_G(B), together with type permutation, is exactly the induced action of A_B on unordered panel tuples. The kernel of the normalizer action is irrelevant to this equivalence relation; every element of A_B has a lift in N_G(B).

This is a concrete finite permutation representation, not an assertion that all subgroup diagrams automatically give geometries. The geometry recognition tests remain essential.

## 2. Exact recognition tests

The program retains the arbitrary-rank recognition theorem proved in phase four. It checks:

1. Every meet equality `K_S intersect K_T = K_(S intersect T)`.
2. For every nonempty S, at least one maximal deletion `K_(S minus {i}) < K_S` (RWPRI).
3. For each subset S of at least three types, typed Helly for the maximal parabolics of K_S. Specifically, for H_i=K_(S minus {i}), it tests

       intersection_(j in J) H_i H_j = H_i (intersection_(j in J) H_j)

   by exact right-coset orbit cardinalities. This verifies flag transitivity and the geometry axiom, not merely the subgroup intersection property.
4. For every pair of panels, the coset graph of their join is a partial linear space or a digon (`(IP)2`). Because both panel actions are two-transitive, a single common-neighbour count for two incident-through-a-line distinct points is exact. The program first checks the panel intersection equals B. A digon is recognized by `|P||Q|=|<P,Q>||B|`; otherwise the common-neighbour count must be one.

Firmness and `(2T)1` follow from the definition of P(B), while the generated-join construction and exact meet diagram give residual connectedness once typed Helly has identified the residues. Checking typed Helly for every subset is redundant after full recognition, but is retained as a direct local check.

For the rank-two common-neighbour test, choose x in Q outside B. Neighbours of P are the Q-cosets represented by a right transversal of B in P; neighbours of Px are the right translates of these cosets by x. Every pair of distinct P-type elements incident with Q lies in a single Q-orbit because Q is two-transitive on Q/B. Thus their common-neighbour count does not depend on the chosen x. This remains valid when the local action has a nontrivial kernel.

## 3. Complete augmentation

Suppose representatives of all G-conjugacy classes of subgroups K and all K-conjugacy classes of their maximal subgroups H are supplied. The normalizer-transporter lemma of phase four gives every maximal overgroup of any specified H as an actual subgroup of G. Applying the same construction only to locally two-transitive inclusions gives all of P(B).

Start with all rank-one tuples modulo A_B. To extend a valid tuple, let H be its generated join. For every maximal overgroup K of H, try each panel P in P(B) with P not contained in H and P contained in K. Then `<H,P>=K`. Both proper overgroups and K=G are included. Use representatives under the pointwise stabilizer in A_B of the current panel indices, then run the exact recognition tests and discard equivalent accepted tuples under A_B and type permutations.

**Completeness.** Let a target rank-r geometry have acting group K≤G and Borel B. RWPRI supplies at least one maximal parabolic H of K. The corresponding rank-(r−1) residue has the same Borel and satisfies every retained axiom, so induction places a conjugate of its panel tuple in the preceding level. The remaining panel lies in K and outside H. K appears among the maximal overgroups tried for that child, so the extension is tested. The pointwise-stabilizer orbit representatives lose no extensions. Final type-permutation and A_B equivalence removes duplicates without changing the represented geometries. ∎

It is not claimed that every arbitrary deletion H admits the final extension. Completeness uses the particular maximal parabolic guaranteed by RWPRI.

The strict chain

    B < K_{1} < K_{1,2} < ... < K_{1,...,r}

shows r≤Ω([G:B]), where Ω counts prime factors with multiplicity. Running through Ω([G:B])+1 therefore must produce an empty level. The program requires that empty level; reaching a numeric cap alone is not accepted as exhaustion.

Finally take B over all G-conjugacy classes of subgroups. Every geometry is reached because its Borel is conjugate to one of them. The final J2 geometries must then be fused under the full automorphism group and arbitrary type permutations; inner conjugacy counts are not compared directly with the paper's final counts.

## 4. Implementation and trust boundary

`phase5_j2_search.g` reads TomLib's named J2 group, its 146 subgroup classes, and their 568 maximal-inclusion classes. Exactly 417 inclusion classes are locally two-transitive. It does not read any original geometry representatives, the Cambridge supplementary archive, or the phase-four witness list.

The program replaces repeated subgroup-tuple conjugacy tests by successive point transporters and point stabilizers in A_B. Necessary pair-residue tests are cached. Each candidate is constrained to a certified maximal overgroup before the expensive higher-rank checks. These are exact reductions of the search space.

`phase5_j2_run.py` records the exact executed script hash and writes a checkpoint after each completed Borel anchor. `--resume` rejects checkpoints if the script hash or checkpoint bytes have changed. Every completed anchor records the empty terminal level. Separate rank checkpoints retain the current panel list and accepted tuples for diagnosis.

The imported completeness of the subgroup catalogue is not reproved. GAP's exact permutation-group algorithms, including subgroup maximality, transporter construction, intersections, and coset actions, are also trusted. This phase aims to eliminate the original *geometry list* as an exhaustion input, not the underlying finite-group classification data.

## 5. Completed principal-result reproduction

All 146 Borel anchors were enumerated to an empty terminal level. The independent output is:

| Rank | Inner conjugacy and type permutations | Aut(J2) and type permutations |
| --- | ---: | ---: |
| 2 | 8 | 8 |
| 3 | 24 | 19 |
| 4 | 5 | 3 |
| At least 5 | 0 | 0 |

This is the complete principal census in [L104, Section 3](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v21n1p77/585). The last row follows from exhaustion of every augmentation branch. It is not an inference that excluding rank five automatically excludes higher ranks.

The search tested 4,072 maximal-augmentation orbit representatives, distributed by ranks two through six as 644, 1,226, 1,931, 271, and 0. Its wall time was about 124 seconds in the recorded environment, including construction of the maximal-inclusion and panel lists from the imported subgroup representatives. The cost of proving the subgroup catalogue complete is not included.

All 30 final representatives passed a separate verifier using maximal parabolics: source-group equality with TomLib J2, generation by the panels, panel reconstruction from parabolic intersections, firmness, flag transitivity, residual connectedness, every RWPRI residue, all two-transitive panel actions, and every rank-two partial-linearity/digon test. This verifier shares the general recognition code from phase four but reads no phase-four geometry data or source geometry list.

The three rank-four geometries have Borel orders 1, 1, and 8. Their maximal parabolic orders are `[12,150,60,60]`, `[150,150,60,60]`, and `[384,384,6048,6048]`, respectively. The independently generated representatives are in `phase5_j2_representatives.g`.

The complete result is conditional on the imported group data and exact GAP operations. The original geometry list is no longer a completeness input. This reproduces the paper's principal classification count, without claiming to rederive every secondary annotation in its supplement, such as full correlation groups or doubling relations. It is an independent computational reproduction, not a claim of novelty for the old classification.

## 6. Reproduction and artifacts

The recorded run used GAP 4.15.1 and TomLib 1.2.11. Python 3 with its standard library is sufficient for the drivers. GAP is found through `GAP`, an explicit `--gap` argument, or the executable search path. No third-party geometry archive is required.

From the repository root, run:

```sh
python3 research/leemans/phase5_j2_run.py
python3 research/leemans/phase5_j2_finish.py
python3 research/leemans/phase5_j2_build_certificate.py
```

The first command performs a fresh full enumeration and writes the 146 terminal checkpoints under `phase5_j2_checkpoints/`. The second checks their hashes, fuses the accepted J2 geometries under the full automorphism group, and verifies every final representative. The third binds the complete output to exact script, input-data, and checkpoint hashes in `phase5_j2_certificate.json`.

`phase5_j2_progress.json` records each completed Borel anchor, and `phase5_j2_final_checks.json` records the final checks. The certificate uses the fresh complete run, not the earlier B=1 development cross-check. All 146 terminal checkpoints are included as numerical mathematical output; larger intermediate rank checkpoints are optional for reproduction and diagnosis. None is an original third-party geometry file.

The enumeration and its completeness argument have not been fully formalized in Lean.
