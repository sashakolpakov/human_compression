# Independent review of the geometric halving bridge

10 October 2026. **PASS with component/source-only coverage.** This review checks the selected published hypotheses, the implication for the support filter, the S6 geometric obstruction, and the limited matching-diagram order calculation. It does not credit an entire cited paper as rederived.

The final source adapter has SHA256 `3b38496e77f2cde987bd82314dc9492bca56ce342e2e01a46cd608a553710251`; all bindings are in the companion JSON. I read the entire [source adapter](phase26_halving_source_adapter.md), [bounded access note](phase26_access.md), and [coset checker](phase26_s6_geometry_check.py). I also read the selected primary passages specified below. No frozen author or public file was edited.

## Exact hypotheses and retained source results

Piedade–Tranchida, arXiv:2405.19050v1, has title-page date 29 May 2024. I checked the definitions of B1 and B2, Theorem 4.4 and its proof, and Lemma 4.5 and Proposition 4.7 with their proofs on PDF pages 14–15. The overlap condition is already explicitly identified with B1 in Lemma 4.5. Their geometric conclusion requires B1, B2 **and an original regular hypertope**. It is not a theorem about every involutory marking with subgroup IP.

The adapter's consequence is valid: the published theorem supplies a regular hypertope for the changed marking, hence its actual subgroup IP. Applying that IP to `H_I,H_J` shows that recovering the removed generator on both supports recovers it on their intersection. Thus the support family is intersection closed under the published hypotheses. This argument retains the geometric theorem; it neither proves that B2 is equivalent to the support condition nor removes the original geometry requirement. The source's hemicube Example 4.9 already shows that B2 need not be necessary for a successful operation.

I also checked all of Montero–Weiss §3, including Theorem 3.1, Proposition 3.2 and Corollary 3.3 in arXiv:2001.11082v1. Reversing generator order gives the stated endpoint operation. The face-poset lattice hypothesis supplies the unique common ridge in the special parabolic meet. Flag transitivity uses the cited tail-triangle semiregular-polytope machinery separately. The adapter correctly retains that input instead of treating subgroup IP as sufficient.

For Piedade's 2023 paper I checked §§2.3–2.4 and the orthoplex application in §3.2, including Proposition 13. For a finite centrally symmetric regular polytope and integer `2≤s<∞`, the matching diagram gives a direct product of `m` dihedral factors of order `2s`, and the retained diagram action gives the stated semidirect product. Its order and the index-two parity calculation give `(2s)^m |Aut(P)|` and half that number respectively. For the orthoplex this is `(4s)^n n!` and `(4s)^n n!/2`, agreeing with the source. The finite restriction is relevant: infinitely many components would give the restricted product in the Coxeter construction. These order identities do not rederive the full presentations, residue types or geometric existence statements. The differing corollary numbering between the 2020 preprint and the 2023 citation is left explicit.

The inaccessible 2000 and 2008 bodies remain limited-access records. The bridge does not promote later restatements or an author abstract to a full reading of those originals. I did not repeat every network access attempt; my source verification used the saved primary passages and the cited accessible manuscripts.

## Independent geometric description of the S6 obstruction

I derived the following model directly from the stabilizers of the six-point marking, before comparing it with the author's coset diagnostic:

- Type 0 consists of the fifteen two-element subsets of `{1,...,6}`.
- Type 1 consists of the sixty edges of the Johnson graph `J(6,2)`: two type-0 objects are adjacent when they have one common point.
- Each of types 2 and 3 is a copy of the ten unordered partitions into two blocks of size three. A type-0 pair is incident with a partition when its two points lie in different blocks. A Johnson edge is incident when both endpoint pairs cross the partition. Opposite-type partitions are incident exactly when they are distinct.

The base subgroup orders `48,12,72,72` are the full stabilizer orders of these four objects. In each typed pair the diagonal S6 orbit of the base objects is exactly the incidence just described, so this is the actual coset incidence, not an alternative model chosen to fit its counts.

Take the vertex `{5,6}` and the two partitions

`{1,2,6}|{3,4,5}` and `{1,2,5}|{3,4,6}`.

The vertex crosses both partitions and the partitions are distinct, so these three objects form a flag. Their common vertex shadow is

`{ {1,3}, {1,4}, {2,3}, {2,4}, {5,6} }`.

The first four pairs induce a four-cycle in `J(6,2)`; `{5,6}` is isolated. Therefore no Johnson edge through `{5,6}` is incident with both partitions. This flag has no completion of type 1, proving that the original coset system is not a geometry.

There are ten choices for the type-2 partition and nine distinct choices for the type-3 partition. Every such pair has exactly one isolated common-crossing pair, giving exactly 90 unextendible flags of this type. This independently explains the finite diagnostic's count. B1 holds because the vertex-edge truncation is the simple Johnson graph. B2 holds by the exact edge-incidence description. Thus B1, B2 and the old subgroup IP can all hold while the original regular-hypertope hypothesis fails.

## Fresh finite replay and coverage limit

I ran the unchanged standard-library coset checker into [phase26_halving_source_rank_audit.run.json](phase26_halving_source_rank_audit.run.json). The fresh report is byte-identical to the author's saved report. I checked its implementation: it enumerates every typed coset, every pairwise-incident family, their common group-element intersections, every possible chamber extension, and every instance of B1 and B2. The saved normalized coset witness can be reconstructed from the literal generators and representatives; it need not coincide with the differently normalized witness above.

The run confirms order 720, all 256 old subgroup-IP meets, type sizes `15,60,10,10`, exactly 720 full chambers and exactly 90 flags with no completion. All 90 also have no common group representative, and every other flag has one. Every corank-one flag has either zero or two completions. Full-chamber transitivity consequently does not imply flag transitivity or the geometry axiom here.

The scope is a source bridge, a conditional algebraic consequence, an exact counterexample to omitting the original geometry hypothesis, and a semidirect-product order component. It does not refute the cited geometric theorems, prove their geometric hypotheses from arbitrary C-group data, supply a new classification, or justify whole-paper principal credit. No new publication-priority claim or Lean formalization is made.
