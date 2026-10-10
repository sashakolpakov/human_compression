# M22 census and source-table comparison: author checkpoint

This is private author work, not independent admission of L073 or of Module D. The original three-source Module D contract is unchanged. The fourth-source expansion remains incomplete under the deliberately stronger full-table contract fixed before enumeration.

## Proved finite work and its hypotheses

The new search uses the complete GAP TomLib M22 subgroup catalogue, the named permutation group and exact finite-group algorithms. It reads no geometry list or target count. The written E.PrimitiveTriples criterion and U.ExtensionOrbits explain the admissibility tests and complete stabilizer-fiber traversal. The run finds 81 maximal-pair orbits and 431 admissible maximal-triple orbits under the full automorphism image and arbitrary type reordering. It tests 11,866 triples, accepts 1,193 before fusion and applies exact orbit transporters for the final fusion.

A separate post-enumeration checker verifies all 81 and 431 witnesses, their pairwise orbit inequivalence, and 1,293 instances each of the three-type flag-transitivity test, residue generation and firm-panel index. This second computation verifies witnesses and fusion, not exhaustiveness; the complete census and its written search theorem remain necessary.

The permutation normalizer has order 1,774,080, but its centralizer of M22 has order two, coming from the two fixed points. Its automorphism image therefore has order 887,040, equal to the separately computed automorphism group. The census does not count the two fixed-point permutations as additional automorphisms.

The geometric decoding takes the eight maximal classes in source order. Their shadows have sizes 1,6,7,7,8,2,12,11. The class families have 22,77,176,176,330,231,616,672 subgroups, respectively. Each of the first seven kinds has one shadow; an endecad subgroup has exactly two complementary shadows. Every shadow has exactly the asserted subgroup stabilizer. Adding the two fixed points to hexads, one fixed point to each appropriate heptad family, and no fixed point to octads produces 759 blocks. Every one of the 42,504 five-subsets of the 24-point set lies in exactly one block. The 2,576 symmetric differences of pairs of octads meeting in two points recover the dodecads. The source's 616 dodecads and 1,344 endecads are then checked directly.

Identification with the particular MOG labeling in L073 retains the classical uniqueness of S(5,8,24) and the standard M24/two-point-stabilizer identification. Curtis's 1976 primary publisher abstract explicitly states uniqueness; it was read, but no claim of reading his complete proof is made. No historical numbering of the 431 geometries is inferred from uniqueness.

## Exact source reading

All nine primary PDF pages were individually viewed. `phase164_L073_visual_review.json` binds those private rasters and the primary PDF. The 431 table rows retain their physical page, literal label, printed number and flattened Borel label. The raw table is not an enumeration input. Superscripts and subscripts are interpreted only when the precise meaning has been verified; the inherited Kilic–Rowley subscripts are still a separate gap.

There are 431 rows but 430 distinct printed indices. On physical page 4, both M134(1,0,0) and M135(1,0,0) are printed with Number 61; Number 62 is absent. This is a literal primary-page observation, not an OCR defect. It does not identify which row was intended to be 62.

There is also an elementary contradiction in the printed row M133(0,3,1), Number 72, Borel S3, physical page 4. Physical page 3 defines Mabc(tab,tac,tbc) by tab=|Xa∩Xb|, tac=|Xa∩Xc| and tbc=|Xb∩Xc|. The same page defines type 1 as a point of the 22-point set and type 3 as a heptad. Thus the second coordinate of M133 is the intersection of one point with a heptad and is at most one. The printed value three cannot satisfy that definition. This does not determine the intended corrected label or its external witness number.

## Diagnostic, not completed matching

`phase164_m22_match.py` intentionally forgets the unknown refined subscripts and colon labels and compares only the three source classes, three ordinary intersection sizes and Borel order. Both choices of each endecad, all type permutations and the global interchange of the two heptad families are allowed. The independently computed table admits a coarse/order bipartite matching of 419 of 431 source rows. Eleven source rows have no order-compatible witness even at that weaker level; one further row is unmatched because of a collision in the full bipartite matching. A coarse match is not proof of a refined source label, and the chosen maximum matching is not an identification of the authors' intended numbering.

The detailed JSON records every row and every candidate, including an empty list when appropriate. Beyond the elementary impossible point/heptad row and duplicate Number 61, these discrepancies remain author diagnostics until checked against the exact source conventions and independently audited. They are not collectively advertised as published errors merely because the candidate census agrees with the headline count.

The primary Borel-order histogram and the newly computed one also disagree in some small orders. The diagnostic uses explicitly documented order interpretations, including powers lost in flat extraction. It is a reason to inspect the table further, not permission to silently replace printed entries.

## Material comparison gaps

The source refers the meanings of its refined pair-orbit subscripts and colon labels to Kilic–Rowley, Note di Matematica 22 (2003/04), 107–154. The author publication list and Manchester institutional abstract were read; the full primary article has not been acquired. Ordinary publisher retrieval timed out. No full-text reading is claimed.

The source's author landing page is accessible and contains a link to `m22.pri.rk3`, but the linked current URL returned a saved 404 response. The geometry file itself was not acquired or read. A preliminary progress sentence describing it as accessible was too strong: only the landing page and link were accessible. No source-file witness correspondence is claimed.

The remaining work is exact source-label reconstruction or a fully explicit corrected table contract, with all unresolved intended-label questions stated. The new complete census and Steiner model do not erase this obligation. No fourth whole-source credit is requested at this checkpoint.
