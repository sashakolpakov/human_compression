# Independent review of the N009 Table 6 label adapter

Review date: 10 October 2026. Verdict: **PASS within the stated scope**. No mathematical or transcription gap was found in the frozen [adapter](phase22_N009_table_labels.md), its four GAP checkers, numerical libraries, and row-comparison code. This review does not promote the work to a complete-paper reproduction or make a priority claim.

The reviewed adapter has SHA256 `cd5eaef9dee59defbb2a50071daada6fb91383608d22ea606869109d57b25089`; its 33-entry manifest has SHA256 `4ea4f279833f7eb05848dba8930b7773197fed2ba75484db8dffbbdf0a395f62`. The companion audit JSON binds the exact source, executable, and fresh-report bytes.

## Source identity and orientation

I read the source's Definition 2.6, its p.4 naming convention, the universal presentation and Theorem 4.2, Table 6, and the statement of Theorem 5.3 in the private primary extraction of Gomi–Loyola–De Las Peñas, [*String C-groups of order 1024*](https://cdm.ucalgary.ca/article/download/62475/46803). I also rendered and inspected printed p.16. The four `{4,16,4}` rows really print the right label with type `[4,16]`. The adapter records that spelling and uses the dual ordered marking when identifying the last three generators. It preserves the letters and counts, and independently checks the corresponding dual Atlas names. This is an explicit orientation interpretation of the source, not an asserted erratum.

The source's isomorphism preserves the distinguished generator set. For a connected string of rank at least three, the noncommuting-generator graph is a path, whose only automorphisms are identity and reversal. Ordered marked classes therefore pass to the source convention by the reversal action. For a pair of facet labels `(A,B)`, that action is `(dual(B),dual(A))`. The code uses this action rather than merely swapping two unchanged labels; in particular it correctly allows the nontrivial exchange of the `{8,8}*128a` and `{8,8}*128c` names.

An independent parser in [the replay checker](phase22_N009_labels_rank_check.py) read all 67 saved primary Atlas pages using Python's standard HTML parser. It verified their hashes and canonical-name fields; composed all 212 generator permutations from 8,367 cycles; and compared all 533 literal relator words with the numerical library. The actual cycles are pairwise disjoint within each generator. Thus the author's simpler assignment-based cycle parser introduces no hidden composition assumption for these inputs. The checker also independently parsed every generated GAP data literal and matched it to its JSON library. Downloaded GAP text was not executed. These 67 primary snapshots remain excluded from the public artifact set.

## Marked identifications and completeness boundaries

The checked maps send each ordered Atlas generator to the corresponding ordered facet generator. Existence and bijectivity of these maps identify the marked objects, rather than just their abstract group or order. Exactly one library entry succeeds for each facet. The library supplies names; it does not filter the ambient census or supply its completeness.

For rank four, I checked the literal transport of all 199 saved accepted kernels into the new GAP input, the binary pc-coordinate guard, normality, and quotient index. The new run uniquely identified all 398 facets. Completeness, the reversal flags, and the original actual intersection checks are retained from the frozen phase21 census; this replay is not a second rank-four exhaustion algorithm.

For rank five, the new run independently executes the author's complete 127-hyperplane search in the central elementary-abelian third lower-central subgroup of the universal class-three group. The frozen first-excess theorem supplies the class-three completeness reduction. Each hyperplane is normal because that subgroup is central; every quotient has order 1024 and is tested on all 1,024 parabolic intersections, including rejected candidates. The canonical class-two quotient preserves the distinguished involutions and adjacent orders at least four. There are 130,048 actual intersection comparisons, yielding 15 ordered markings, one reversal-fixed marking, and eight reversal classes. All 30 facets have unique exact marked labels.

## Raw presentations and row equivalence

For each of the 67 Atlas objects, the actual permutation model satisfies every displayed relator. Complete Todd–Coxeter enumeration at the trivial subgroup gives the same finite order. The presentation therefore maps onto the model through the specified generators and is an isomorphism by equality of orders. This verifies the complete presentations used in the amalgams; it does not treat an NQ image as an order upper bound.

The universal presentation places the first facet on markers `1,...,r-1`, the second on `2,...,r`, and adds the sole distant commutation not already contained in a facet presentation, between markers `1` and `r`. The source orders are compared only after coset enumeration; they are not imposed as extra relators. Every row also has a census witness with exactly these marked facets. The map onto that witness ensures that the facet presentations do not collapse inside the universal presented group. The source's standard universal-polytope background is retained explicitly.

The fresh executions verified all 106 finite universal orders: 101 of order 1024 and five of order 2048. The single infinite row retains the McMullen–Schulte decomposition quoted as source Theorem 5.3. Neither a failed enumeration nor a finite nilpotent quotient is used to infer infinity.

The row comparison groups ordered objects by the correct dual-label-pair involution, counts reversal-fixed markings in each invariant block, and applies `(ordered + fixed)/2`. Its dictionary equality checks that no source row or ambient marking is left unmatched. Fresh exact re-extraction of the hash-bound primary text agrees with all 107 factual rows. The resulting 99 rank-four rows contain 105 reversal classes; the eight rank-five rows contain eight classes. All 106 finite universal-order entries agree as well.

## Fresh execution and exact scope

I reran the four unchanged author GAP scripts in a fresh temporary directory, using their frozen numerical inputs. All eight generated JSON outputs were byte-identical to the author's saved outputs. No GAP errors or syntax warnings occurred. The separate [replay report](phase22_N009_labels_rank_check.json) contains the exact script hashes, complete fresh standard output, output hashes, source-data checks, and fresh table-comparison result. It also verifies all 33 original manifest hashes and six retained dependency hashes.

Reproduction with the private primary snapshots available:

```sh
python3 phase22_N009_labels_rank_check.py --primary-sources --output fresh-label-review.json
```

Without the private sources, omit `--primary-sources`; the four mathematical reruns, saved numerical data checks, and table comparison still run. GAP is located using `GAP`, `PATH`, or the explicit `--gap` option. The checker does not overwrite any author artifact.

The evidence combines a written proof/code review, independent primary-data parsing, and fresh executions of the author's algorithms. It retains GAP/NQ and Todd–Coxeter implementation correctness, earlier census/class bounds, and the quoted infinite decomposition. It does not constitute formal verification, an independently implemented group census, a proof of every result in N009, or a novelty determination.
