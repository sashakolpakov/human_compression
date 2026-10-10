# N009: exact Table 6 labels and universal-group orders

Private source-bound adapter, 10 October 2026. This closes the label-level obligations left by the earlier type-count comparison. It does not change any phase21 artifact or claim a new principal-paper count.

## 1. Exact result and source convention

For Gomi–Loyola–De Las Peñas, *String C-groups of order 1024*, [primary article](https://cdm.ucalgary.ca/article/download/62475/46803), Table 6, pp.14–17:

* All 99 rank-four rows match the saved exhaustive kernel census, including the **marked facet and vertex-figure labels**, and give 105 classes up to reversal.
* All eight rank-five rows match a complete first-excess calculation, including their marked labels, and give eight classes up to reversal.
* Complete Todd–Coxeter tables verify every one of the 106 finite universal-group orders: 101 are 1024 and five are 2048.
* The single infinite universal row retains the McMullen–Schulte semidirect decomposition quoted as source Theorem 5.3. This is the same explicit retained input as in [the lemma adapter](phase22_N009_lemma_adapters.md).

The four rows of type `{4,16,4}` name their vertex figure with the type `[4,16]`; the last two ordered generators have type `{16,4}`. We therefore use the **dual marking of the named object**, preserving its suffix and all counts. The source identifies dual string C-groups under Definition 2.6. Both spellings and this conversion are recorded, rather than silently replacing the printed label. The spelling was checked in the actual primary PDF image of printed p.16, not only in extracted text. This is an orientation clarification, with no priority or erratum claim.

The source's p.4 naming convention identifies its bracketed names with Hartley's Atlas names. The [primary Atlas FAQ](https://abstract-polytopes.com/atlas-FAQ.html) specifies stable canonical names. A [representative primary page](https://www.abstract-polytopes.com/atlas/64/134/1.html) supplies ordered permutation generators and a finite presentation. We use these primary mathematical data as the **definitions of the names**, not the Atlas's completeness as a classification input.

## 2. Why the comparison is a marked identification

The parsed libraries contain 56 rank-three and 11 rank-four Atlas markings, together with their primary URLs and snapshot SHA256 hashes. Downloaded GAP text is never executed. The extraction scripts accept only cycle notation and words in the declared generators, convert these to numerical permutations/word arrays, and generate small local data files.

For each library entry, the checkers verify the permutation-group order, every adjacent product order, all subgroup intersections, and all displayed relators. A complete coset enumeration of its presentation has the same order as the permutation model. Consequently the displayed presentation and permutation model are isomorphic through the specified generators: the verified relators give a surjection and the equal finite orders give injectivity. There are 67 distinct complete-presentation verifications and 6,400 library intersection checks.

For each facet of each candidate, `GroupHomomorphismByImages` is supplied the **ordered** Atlas generators and the **ordered** facet generators. The map must exist and be bijective. Exactly one library marking passes. Equal abstract group identifiers or equal facet orders would not suffice; no `SmallGroup` lookup is used.

Thus all 398 facets in the 199 ordered rank-four markings and all 30 facets in the 15 ordered rank-five markings receive exact labels. The Atlas library is not used to select or reject candidate ambient groups.

## 3. Census and reversal adapters

### Rank four

The input is the frozen `phase21_rank4_census.accepted.json`, whose 199 kernels were obtained without source labels or counts as filters. The new checker reconstructs the same universal class-five marked group and each quotient from its binary canonical pcgs kernel coordinates. It checks the relative-order-two coordinate hypothesis, normality, and index 1024 before identifying the two facets.

Completeness and all actual-IP checks remain supplied by [the frozen kernel-ladder theorem](phase21_kernel_ladder.md) and its final guarded census. This adapter does not claim an independent second exhaustive rank-four search.

### Rank five

The frozen [first-excess classification](phase17_k1_classification.md) implies that every relevant marking has class at most three and is a quotient of the universal class-three string-involution group by an index-two subgroup of its central elementary-abelian third lower-central subgroup. The new script enumerates **all 127 hyperplanes**, constructs every quotient, and checks all 1,024 subgroup intersections per quotient, for 130,048 comparisons. Exactly 15 ordered markings pass; one is fixed by reversal, giving eight classes. All their facet labels agree with the eight source rows.

### Why the label involution matters

Reversing an ambient marking changes its pair `(A,B)` to `(dual(B),dual(A))`. The library itself determines each dual by another exact marked isomorphism. In particular,

`{8,8}*128a ↔ {8,8}*128c`, while `128b` and `128d` are self-dual.

Consequently one cannot replace the source's same-type rows by unordered pairs of unchanged letter suffixes. The comparison partitions the ordered census by the correct label-pair involution and applies Burnside's formula `(ordered + fixed)/2` within each stable block. All 107 source rows match, with no unused ambient markings or unmatched rows.

## 4. Universal presentations

Let `A=<a0,...,a_(r-2)>` and `B=<b0,...,b_(r-2)>` be adjacent facets, represented by the verified complete presentations. Form a presentation on `s0,...,s_(r-1)` by substituting `a_i=s_i` and `b_i=s_(i+1)` and adjoining `[s0,s_(r-1)]=1`. All other distant commutators already belong to one of the two facet presentations.

This is the source's universal presentation. Its universal property follows directly: any marked group with these facets satisfies all the displayed relators, so it is a quotient. Conversely, for each source row the exhaustive census supplies at least one actual string C-group with those exact facets. The resulting map from the presented group to that witness prevents either facet from collapsing. The usual source Theorem 4.2 supplies the standard universal-polytope interpretation; it is retained background, not a new theorem here.

The checks use complete coset tables at the trivial subgroup, so they prove the order of the raw finite presentation. They are not nilpotent-quotient lower bounds. Of the rank-four rows, 93 have universal order 1024, five have order 2048, and one is infinite. All eight rank-five universal presentations have order 1024. Thus the finite checks cover 106 presentations.

For the exceptional infinite row `({4,4}*128,{4,4}*64)`, the retained decomposition of Theorem 5.3 proves infinitude; [the earlier raw-presentation certificate](phase21_N009_presentations.md) and the exhaustive census supply its two order-1024 quotients. No finite computation is used to infer infinitude.

## 5. Dependency and coverage ledger

| Obligation | Evidence now supplied | Remaining input |
|---|---|---|
| Rank-four candidate completeness | frozen phase21 normal-kernel ladder | GAP/NQ correctness; reviewed all-class support and class bound |
| Rank-four counts with exact facet labels | 398 unique marked isomorphisms; 99 row matches | primary Atlas label-to-marking naming |
| Rank-five completeness and exact labels | all 127 hyperplanes; 130,048 meets; 30 marked isomorphisms | reviewed first-excess theorem; GAP/NQ |
| All finite universal orders in Table 6 | 106 complete Todd–Coxeter tables | GAP coset-enumeration implementation |
| Single infinite universal order | source Theorem 5.3; prior lemma adapter | quoted McMullen–Schulte decomposition |
| Source's standard universal-polytope interpretation | presentation universal property plus exact facet embeddings | quoted source Theorem 4.2 |

No unseen external finite presentation is still needed for Table 6. The quoted infinite decomposition remains a genuine external structural input. The separate primary rank-three census, central-quotient theorem, and center/semidirect adapters address other numbered claims; this note does not automatically certify every illustrative presentation in Tables 2–4 or independently reprove all quoted preliminaries. No whole-paper promotion follows merely from adding these row matches.

## 6. Reproduction and source exclusions

Run in a directory containing this package's original scripts/data and the retained phase21/phase17 notes:

```sh
gap -q phase22_N009_facet_check.g > facet-run.log
gap -q phase22_N009_rank5_labels_check.g > rank5-run.log
gap -q phase22_N009_universal_check.g > universal-run.log
gap -q phase22_N009_universal5_check.g > universal5-run.log
python3 phase22_N009_table_compare.py --output table-comparison-fresh.json
```

The GAP scripts write their named JSON outputs into the working directory; use a scratch copy to preserve the saved reports. The final Python comparison needs only the original mathematical table data and generated results. It does not require a private PDF or website access.

Optional provenance verification can reparse the exact primary extraction with `--source-text PATH`; its expected SHA256 is fixed. The two extraction scripts require the primary HTML snapshots and BeautifulSoup and are provenance recipes, not dependencies of the mathematical reproduction. Primary PDFs, rendered pages, and HTML snapshots remain private and are excluded from the original-artifact allowlist. The extracted numerical permutation and word data carry per-entry primary attribution.

All executions here are the adapter author's own checks. Independent proof/code review is a separate item and must not be inferred from this report. See `phase22_N009_table_labels_certificate.json` and the final manifest for exact bytes.
