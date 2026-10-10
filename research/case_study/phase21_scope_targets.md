# Phase 21: exact source targets for the finite-state machinery

Private scope audit, 10 October 2026. No registry or public coverage promotion is made here. The strongest immediate target is the rank-four component of the 2018 order-1024 paper N009. It is newer than the preferred 1996–2006 period; the older works checked below do not supply an unclaimed whole-paper theorem that follows automatically from the new finite-state algorithm.

## 1. What the algorithm does and does not discharge

For a nondegenerate rank-d marked string 2-group of order 2^(2d-1+k), the reviewed fixed-excess theorem gives nilpotency class at most k+2. The finite-state theorem then reduces large rank to finite windows of that class. For d below the window size, it still requires an initial finite classification. A universal algorithm is not itself a reconstruction of a published census, an explicit closed formula, or every presentation in a source table.

For order 1024, the only nondegenerate ranks at least three are:

| rank d | excess k | sufficient class cap | target |
|---|---:|---:|---|
| 3 | 5 | 7 | N009 Table 5: 125 classes up to reversal |
| 4 | 3 | 5 | N009 Table 6: 105 classes up to reversal |
| 5 | 1 | 3 | N009 Table 6: 8 classes up to reversal; already recovered |

Ranks three and four are initial-library problems, not repetitions of a smaller window. An exact universal nilpotent-quotient kernel census is nevertheless practical at rank four. Rank_stability reports an unfiltered enumeration of 1,483 invariant index-eight kernels of the universal rank-four/class-five group's gamma3, with 199 ordered IP markings and 11 reversal-fixed markings, giving (199+11)/2=105. Those figures are a new candidate verification awaiting the final proof, source-type comparison and bound review. They are not accepted here merely because the total matches.

## 2. N009 primary ledger and exact obligations

Gomi, Loyola and De Las Peñas, *String C-groups of order 1024*, Contributions to Discrete Mathematics 13(1) (2018), 1–22. DOI https://doi.org/10.55016/ojs/cdm.v13i1.62475 ; primary PDF https://cdm.ucalgary.ca/article/download/62475/46803 . The PDF and extraction hashes are recorded in `phase21_central_quotient.md`.

The new reading is selected-section reading: definitions/preliminaries, complete central-quotient and relator-lift chain in Section 3, both census tables, universal-presentation statements in Section 4, the statement of Theorem 5.5 and the conclusion. Not every example or the complete Section 5 proof has been read in this phase; no full-paper reading upgrade follows.

| exact source target | current reduction | remaining obligation |
|---|---|---|
| Theorem 3.6, p. 7 | proposed full uniform alternative proof in `phase21_central_quotient.md` | independent written review |
| Theorem 3.8/Table 1, pp. 8–9 | proposed full three-case central relator-lift adapter in the same note | independent review; every candidate still needs order/IP tests |
| Table 5, p. 11 | no completed replacement census in this phase | rank-three class-at-most-seven enumeration, all types, marked equivalences, and any claimed source presentations |
| Table 6 rank four, pp. 14–17 | full normal-kernel search reported by rank_stability | prove enumeration completeness, actual-IP tests, reversal/type counts and source comparison |
| Table 6 rank five, p. 17 | previously recovered from the first-excess classification | no additional credit for reusing the count |
| Theorem 5.5, p. 20 | the new rank-four library can isolate the two fixed facet-orientation cases | facet identities, two exact groups, raw presentation orders and marking/IP verification |
| Theorem 5.3, p. 18 | retained quoted structure theorem for an infinite universal group | not a new N009 theorem and not reproduced by a finite census |

Definition 2.6 identifies groups by an isomorphism mapping the distinguished **set** of generators onto the other. With connected path diagram, a marking permutation must be identity or reversal. Hence the source counts are up to reversal, not ordered marking counts. Abstract group isomorphism alone is insufficient.

Table 5 counts by canonical rank-three type are:

    (4,4):1; (4,8):8; (4,16):14; (4,32):4;
    (4,64):2; (4,128):2; (8,8):22; (8,16):40;
    (8,32):8; (8,64):4; (16,16):10; (16,32):10.

They sum to 125. Table 6 rank-four counts are:

    (4,4,4):4; (4,4,8):10; (4,4,16):4; (4,4,32):2;
    (4,8,4):14; (4,8,8):24; (4,8,16):10; (4,16,4):4;
    (4,16,8):12; (4,32,4):3; (8,4,8):4;
    (8,4,16):4; (8,8,8):10.

They sum to 105. For each nonpalindromic type, its count is half the ordered count after identifying the type with its reversal. For palindromic types one must include the reversal-fixed count before dividing by two. Rank-five types (4,4,4,4), (4,4,4,8), (4,4,8,4) have counts 2,2,4 respectively.

Theorem 5.5 fixes facet order 128 and vertex-figure order 64, both of type (4,4). Its two groups have type (4,4,4). Write a,b,c,d for the ordered generators. Both presentations add

    (a b c b)^4 = (b c d)^4 = 1.

The first additionally has `(d c b a b d c)^2=1`; the second has

    (b d c d b a)^2 (c b a b)^2 = 1,
    (a b c b)^2 (b a b d c d)^2 = 1.

Filtering the census by those facet orders should identify the two fixed-orientation markings. However, a class-five NQ calculation of the two displayed presentations proves only their class-five quotients have order 1024. To reproduce the source's full finite-presentation assertion one must establish an upper bound on each raw presentation, for example by successful coset enumeration. Likewise, knowing that the relators vanish in two witnesses proves a quotient claim, not that the raw presentations are finite.

## 3. Older candidates: precise relevance limits

**N010, Schulte–Weiss (2006), Problem 30, printed p. 19.** The reviewed intake `phase18_schulte_weiss_intake.md` distinguishes the original 2006 work from a later PDF compilation date. The problem concerns regular or chiral polytopes with full automorphism order a power of two or twice-prime-factor form. The fixed-class/fixed-excess marked algorithms and rational generating functions are restricted progress. They do not give the full unmarked, chiral, or mixed-prime classification. The existence of a terminating brute-force enumeration for each fixed order is not new by itself. No current-open or full-resolution claim is made.

**L086, Leemans–Vauthier (2006), *An atlas of abstract regular polytopes for small groups*.** The complete primary author abstract describes almost-simple groups with socle order below 900000. This is not Hartley's 2006 small-order atlas (a different paper, cited separately in N009). L086's full body remains unavailable in the present intake. A finite-state theorem for 2-groups does not reproduce this almost-simple census.

**L109 (2000), dihedral RWPRI geometries.** Its exact classification has already been rederived from full primary restatements in L110 and L114, while the original body remains unavailable. The arbitrary coset-geometry/RWPRI axioms differ from string C-group IP; no new credit is earned by renaming this an automaton instance.

**N008 (2005), the Frattini/RWPRI paper.** The complete available paper's new geometry results and finite-group Theorem 2.1 were already rederived in `phase16_frattini_geometry_reduction.md`. Its infinite-group conditional theorem and RWPRI hypotheses remain distinct from finite nondegenerate path markings. This is already credited and supplies no new paper count.

**Other nearby work.** The 2012 nilpotent orientably regular map papers classify orientation-preserving groups, often with unbounded generator orders. They require an explicit reflection/extension and IP adapter before applying this finite alphabet. Their dates also fall outside the twenty-year preference. The 2019 eight-family classification L035 and later construction paper L032 are already rederived by different fixed cyclic-core or construction arguments; a single fixed-class automaton does not automatically reproduce families of unbounded class. F016's infinite-group clauses likewise remain outside the finite-state theorem.

The bounded source search included combinations of “regular maps”, “2-groups”, “nilpotent”, “regular embeddings”, and pre-2007 date restrictions, as well as the existing registry and primary abstracts. It did not identify an uncredited, fully available pre-2007 theorem set that can safely be declared recovered immediately. This is a search limit, not evidence that no such source exists.

## 4. Work order and honest completion conditions

1. Finish the rank-four N009 census certificate, including every canonical type and the exact reversal convention. This is a substantial source census component.
2. Independently review the short uniform central-quotient and relator-lift proofs. These recover two numbered results without a finite computation.
3. Use the complete rank-four library to resolve Theorem 5.5 with raw-presentation order certification, keeping its quoted infinite-group input separate.
4. Assess rank-three/excess-five feasibility. No whole N009 principal-result promotion is warranted while its 125-class component and relevant presentation claims remain unverified.
5. Continue older-source retrieval selectively; do not inflate coverage by counting an abstract algorithm as a source classification.
