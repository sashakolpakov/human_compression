# Independent review of the M22 core

The frozen phase164 core, supplemented by the additive source-to-coset bridge, is accepted for the numerical classification and geometric-shadow conclusions stated below. It is **not accepted as a complete replacement of the fourth source's refined table**. This review does not admit the separately evolving Module D manuscript or its other three source contracts.

The author checkpoint is `phase164_m22_core_checkpoint01_manifest.json`, SHA256 `4c6b9b3432011119f100694dddc28caf14dbac0afd7e67c02d034ffbb0ada6e1`. The additional bridge is `phase164_m22_source_bridge.md`, SHA256 `2f2463b68ab0951bf3a6eff753629e1e7c9f6ee3d772319701ec6c9a745947ab`. Both are part of this verdict; omitting the bridge would omit an explicitly reviewed source-interface obligation.

The reviewer is `/root/enumeration_review`. The reviewer did not author the census, shadow program, checkpoint mathematics or additive bridge. A previous reviewer requested the bridge; the present review independently checked its completed proof. The fresh computations below execute the author's programs. They are independently executed, not independently authored implementations of the entire census. A separately authored structural and maximum-flow checker provides an additional, narrower check.

## Accepted contract

Subject to the complete M22 subgroup catalogue and exact finite-group operations identified below, the replacement proves that there are 81 unordered maximal-pair and 431 admissible maximal-triple orbits under the full automorphism action. The triples give exactly the rank-three flag-transitive residually connected geometries with maximal proper object stabilizers, for the specified group-automorphism and arbitrary-type equivalence. Every accepted geometry is firm. The census supplies explicit subgroup representatives and exact Borel-group identities.

The geometric decoding constructs a Steiner system S(5,8,24) and recovers the point, hexad, two heptad, octad, duad, dodecad and endecad shadows. It checks their stabilizers. Identification with the historical MOG model retains the classical uniqueness and Mathieu-group identification for this Steiner system. No source witness list or source table is an input to the census or shadow construction.

This recovers the numerical theorem and the independently reconstructed geometric model associated with Leemans–Rowley, *Rank three residually connected geometries for M22, revisited* (2010), DOI [10.37236/453](https://doi.org/10.37236/453). Its full row-by-row table contract remains a separate obligation.

## Mathematical checks

**Coset realization.** The source assumes flag transitivity of the distinguished acting group. Thus the map from a right coset $H_i g$ to the translate $x_i^g$ of a base-chamber object is onto each type, and equality of images is equivalent to equality of cosets. Common representatives imply incidence. Conversely, transitivity on the incident two-object flags supplies a common representative. The proof therefore gives an equivariant incidence isomorphism; it does not merely construct one geometry with the desired stabilizers. No unproved assertion that all abstract incidence automorphisms normalize the acting group enters this argument.

**Repeated maximal stabilizers.** This is a necessary completeness check because the census uses sets of distinct subgroups. If all three stabilizers equal a proper subgroup $H$, the incidence graph is a disjoint union indexed by the distinct right cosets of $H$. If just two equal $H$ and the third is a different maximal subgroup $K$, the residue at the base $K$-object is a disjoint union of edges indexed by $(H\cap K)\backslash K$. Its index is at least two, since $K$ is not contained in the distinct maximal subgroup $H$. Both cases contradict residual connectedness. The additive bridge correctly excludes all repetitions before enumeration.

**Recognition.** Every incident pair of cosets has a common representative, so all flags of each fixed two-type set form one orbit. For the base pair of types $j,k$, the completions of type $i$ are exactly $R_{ij}\cap R_{ik}$. The orbit of the base completion under $H_j\cap H_k$ has size $[H_j\cap H_k:B]$. Equality of this size with the completion set is therefore equivalent to chamber transitivity. Since every pair is a translate of a base pair, this also ensures every pair extends to a chamber. One chosen type suffices for this test; the separate validator correctly checks all three.

Once this common-chamber property holds, a residue at an $i$-object is the bipartite coset graph inside $H_i$ on $H_i\cap H_j$ and $H_i\cap H_k$. The standard path/word argument identifies connectedness with generation of $H_i$ by these two intersections. Distinct maximal subgroups generate $G$, giving connectedness at the empty flag. These are precisely the residual-connectedness conditions of rank three. If one panel had only a single completion, one pairwise intersection would equal $B$ and the generation equality at an adjacent object would generate only a proper intersection. Thus the stated firmness implication is valid.

**Exhaustive augmentation.** The complete maximal-subgroup set is first partitioned under the automorphism action. Fixing one member and taking its stabilizer orbits on the others covers every ordered pair; full fusion gives unordered pair representatives. For each such pair, orbits of its setwise stabilizer on the remaining maximal subgroups cover every possible third member. Every triple has a pair and hence is represented in this traversal. Its generation and completion tests are invariant. The final full-orbit fusion is necessary because different distinguished pairs can lead to the same triple orbit, and the program performs it.

The program's preliminary size signatures are only invariant bucket keys; exact `RepresentativeAction` calls perform the final orbit comparison. Equal signatures are never treated as a proof of equivalence. The proof is conditional on the complete supplied catalogue; checking which supplied classes are maximal does not independently prove catalogue completeness.

**Automorphism image.** In the degree-24 catalogue model the two fixed points produce a nontrivial permutation centralizer. The ambient normalizer therefore cannot be counted as the automorphism group. The code compares its order modulo the centralizer with the independently computed full automorphism-group order, and then uses its actual action on maximal subgroups. The fresh witness check also compares the latter image order with the full automorphism-group order. The value used for orbit counting is 887,040, not 1,774,080. Even a nonfaithful image on this object set would preserve the same orbits; the explicit equality here gives a further check.

**Geometric shadows.** The fixed-point, orbit-size and stabilizer tests are exact subgroup and set computations. The octad construction verifies all 42,504 five-subsets, each with multiplicity one among 759 blocks. Thus it verifies an actual Steiner system, not just its block count. Pairwise symmetric differences recover 2,576 dodecads, and the relevant restrictions recover exactly the claimed dodecad and endecad families. Each endecad subgroup has two complementary shadows; the geometry objects are cosets of the subgroup, so the two shadows must not be counted as different object stabilizers. The stated simplicity/core argument makes the action on these coset objects faithful.

## Fresh replay and its trust boundary

The exact author runner was executed in the new directory `/private/tmp/phase173_m22_independent_replay`, with GAP 4.15.1 and TomLib 1.2.11. The elapsed times were 0.783 seconds for environment discovery, 11.851 seconds for the complete census, 5.989 seconds for the witness validator and 12.902 seconds for the Steiner/shadow reconstruction: 31.525 seconds in total. These are one local run's wall times, not performance guarantees. No new peak-memory measurement was made.

The replay obtained:

| Check | Result |
| --- | ---: |
| Supplied subgroup conjugacy classes | 156 |
| Maximal classes / actual maximal subgroups | 8 / 2,300 |
| Maximal-pair orbits | 81 |
| Tested triples / accepted before final fusion | 11,866 / 1,193 |
| Final maximal-triple orbits | 431 |
| Three-type completion checks | 1,293 |
| Residue-generation checks | 1,293 |
| Firm-panel checks | 1,293 |
| Steiner blocks / five-subsets | 759 / 42,504 |
| Dodecads | 2,576 |

The regenerated witness file has SHA256 `ec5ac0724e8dff8a1f1842347ba28efd03ff0a9bb81cdc1b139540ae06ff45cb`; the regenerated shadow data has SHA256 `5e91bf8aef1817cdd27ed9d76167433d8b65bc9838d94144c17cd6c4410c0fe0`. Both are byte-for-byte equal to the frozen author outputs. The stage logs and report are retained as `phase173_m22_*` review artifacts. The GAP syntax warnings concern functions closing over loop-level global variables; inspection and successful execution show that each value is assigned before the relevant function is called. These warnings are not silently treated as mathematical failures or as proofs of correctness.

The independent structural checker verifies the frozen input hashes, the additive bridge, the fresh run's logs, the exact numerical output lines and both output hashes. It recomputes the coarse source-row candidate edges from the shadow data, then computes a maximum matching by unit-capacity network flow; this differs from the author's depth-first augmenting-path implementation. Both give 419 matches. The Borel-order interpretation is still the author's explicitly recorded coarse interpretation, not a formal reconstruction of every printed group label. Six altered diagnostics are rejected: a deleted source row, a repeated witness identifier, an altered printed number, an inflated matching total, an invented candidate edge and a truncated comparison. These controls test the stated structural boundary, not independence or completeness of the mathematical search.

The finite trust base includes GAP's exact subgroup, automorphism, transporter, intersection and identification algorithms; TomLib's complete M22 subgroup data; and the classical group model. The geometric identification also retains the classical uniqueness of S(5,8,24) and its automorphism-group identification. None of this package is an end-to-end Lean proof. The existence and validity checks on the 431 witnesses alone would not prove exhaustion; the complete census and reviewed augmentation argument are essential.

## Source comparison and the withheld contract

The reviewer read the complete nine-page primary extraction and directly viewed physical pages 3, 4 and 5. This is not a claim of a fresh visual inspection of all nine pages; the author's earlier all-page visual record is retained separately. The source PDF hash is `595809bceeb03e663fa3c7b15219d6141d9fcbfce207fb5d4eab514e90f77341`.

The primary page images confirm two limited observations: Number 61 is printed twice, and the row $M_{133}(0,3,1)$ conflicts with the source's intersection-size definition because one of those two shadows is a point. Neither observation determines the intended corrected row or witness number. The transcription preserves 431 physical rows and 430 distinct printed numbers.

The independent coarse matching leaves eleven source rows with no order-compatible witness and one further collision. It intentionally discards refined subscripts and colon labels. Accordingly it is weaker than the agreed source contract, even for matched rows. The older Kilic–Rowley notation dependency and the historical external witness-number correspondence remain unresolved. A renewed bounded web search found the [Manchester institutional abstract and publication record](https://research.manchester.ac.uk/en/publications/on-rank-2-and-rank-3-residually-connected-geometries-for-m22/) but did not retrieve the older full text. No claim of reading it or of knowing the intended label corrections is made.

The acceptance decision is therefore divided as follows:

| Obligation | Verdict |
| --- | --- |
| Source geometry to distinct maximal-subgroup coset system | Accepted with the additive bridge |
| Exact rank-three admissibility and firmness | Accepted |
| Complete automorphism/type traversal | Accepted, conditional on catalogue and exact algorithms |
| 81/431 census and explicit witnesses | Accepted |
| Actual Steiner reconstruction and geometric shadow identification | Accepted with the declared classical identification |
| Every refined printed row and Borel label matched | Not accepted; comparison remains incomplete |
| Original intended external witness numbers recovered | Not accepted |
| Whole fourth-source replacement, Lean proof or open-conjecture solution | Not claimed |

## Attribution and cost

The prior classification and the source conventions are due to the cited authors. Burnside/orbit-stabilizer reasoning, coset realizations, residue generation and stabilizer-fiber enumeration are classical ingredients. The project's contribution here is an explicit common interface, complete local source-converse proof, independent-input census, reproducible witness/shadow reconstruction and audit trail. This review establishes neither historical priority nor a new conjecture solution.

A transparent raw byte inventory for this specific core is 61,576 bytes of the shared U3 manuscript, 9,653 bytes of frozen core mathematics, 3,225 bytes of the additive bridge and 12,389 bytes for the three GAP programs plus the author runner. Charging U3 once gives 86,843 bytes. The marginal core plus bridge and programs is 25,267 bytes. This excludes the separately itemized witness/diagnostic data, source assets and review artifacts; they remain part of the reproducibility archive. The local-legs note repeats material already present in the core and is not charged a second time to this minimal reading route. These are file inventories, not a matched mathematical compression factor. The missing refined-table contract prevents a claim that this package replaces all nine source pages.

To reproduce the accepted finite component, run the existing author replay in a fresh output directory, then run `phase173_m22_review_check.py --replay-dir PATH --report NEW_JSON`. Add `--check-private-source` only in the private research tree with the bound source PDF available. The default structural check requires the public-eligible author checkpoint files and retained U3, but not distribution of the private primary PDF. Neither command overwrites an existing result path.
