> **Historical reader — archived from `5401cc9`.** This records the earlier
> compilation programme and its dated scope. Its rates, counts and “current”
> wording do not describe the active topic architecture. Use the
> [current programme](../MANUSCRIPT_PROGRAM.md) or the [archive index](README.md).

# Independent assessment of manuscript-level mathematical compression

10 October 2026. Repository assessed: `math_compression`, clean main snapshot `3928d96e23fd8ecc498d79889fdaaa2b7d5ca2c6`.

**My judgement: the repository contains substantial ingredients for several replacement manuscripts, and some already compact replacement proofs. It does not yet demonstrate the requested achievement of an assembled common manuscript from which every identified main result of a declared intake set follows by short adapters, with a measured manuscript-length ratio.** This is an assessment of the current deliverable, not a claim that such compression is impossible or that the mathematical work is insubstantial.

I am a fresh reviewing agent, not an author of these derivations. I inspected the repository's scope and measurement documents, extracted all principal-labelled registry entries, and read substantive portions of its core proofs and adapters. I did **not** independently reprove every theorem, rerun the complete computational/formal suite, or independently read every intake manuscript. Consequently, the theorem coverage below describes what the written evidence supports as a serious candidate, subject to mathematical/source review; registry labels are not my proof certificates. Primary links below identify the recorded source versions, rather than representing fresh live-source verification. This report is independent internal judgement, not external peer review.

## 1. What should count as the requested result

For a fixed intake set `X,Y,Z,...`, the required deliverable is:

`{all identified main results of X,Y,Z,...} <- Compress(X,Y,Z,...) + explicit adapters + declared common background.`

A useful common theorem must discharge actual work: subgroup intersections, generation, completeness, flag completion, or counting. Merely putting all groups into permutation matrices supplies a shared representation, not automatically a short proof of their different classification results.

The requested primary ratio is

`R_manuscripts = (L(X)+L(Y)+L(Z)+...)/(L(Compress)+L(all necessary adapters and additional explanatory/proof material)).`

Fix versions and an identical length convention before measuring. Full intake-manuscript length is a legitimate numerator for this user-defined manuscript replacement metric **only after every identified main result of every included manuscript is covered**. Report separately any omitted examples, historical discussion, auxiliary false claims or open questions. Main-result replacement does not imply reproduction of every printed sentence. Also report matched-proof lengths as a separate diagnostic; they answer a narrower question and should not silently replace the user's numerator.

The [measurement policy](../MEASUREMENT.md) already makes the key distinction between coverage, proof length, object-description length and new results. The repository's current 160 indexed works, 101 retrieved full texts, 52 encoded works, 38 with some specified existing result rederived, 16 principal-labelled works, and 33 Lean components at that baseline are **not** factors in a manuscript ratio. In particular, the 16 are not 16 manuscripts independently certified by this review. The [registry definition](../research/case_study/paper_registry.json) means “all identified principal results recovered; not every auxiliary lemma or external catalogue.” Identification and scope therefore require their own audit.

## 2. Exact intake candidates: the 16 principal-labelled works

The table records the exact source titles and registry years. N013 is a 2020 preprint published in 2021; F016 is a 2025 preprint. Those version distinctions matter for both target numbering and length.

| ID | Named manuscript and year | Identified main target and important qualification |
|---|---|---|
| L008 | [Testing chirality on hypertopes (2026)](https://arxiv.org/pdf/2511.14562) | Theorem 1.1, including truncation, product-size and inversion requirements; standard marked-inversion correspondence retained. |
| L030 | [An infinite family of locally X graphs based on incidence geometries (2021)](https://arxiv.org/pdf/1811.11438v1) | Principal construction, Theorem 4.9 and Corollaries 4.10–4.11: parameters, local graph/residues, distances and automorphisms; Kneser eigenspace facts retained and two source displays corrected. |
| L032 | [On regular polytopes of 2-power order (2020)](https://dipot.ulb.ac.be/dspace/bitstream/2013/292444/3/HRRPR-revised.pdf) | Theorem 1.2, every permitted rank/order/type existence case. This is not classification of all groups of that order. |
| L035 | [2-groups behaving as automorphism groups of regular 3-polytopes (2019)](https://arxiv.org/pdf/1802.08947v2) | Theorems 1.2 and 1.3: existence **and** complete eight-family high-type classification; Lucchini, Burnside and order-256 SmallGroups completeness retained. |
| L066 | [On pairs of commuting involutions in Sym(n) and Alt(n) (2013)](https://math.uni.lu/kiefer/Publications/Involutions.pdf) | Four principal results: Theorems 1.1/1.2 counting and 3.6/4.4 degree-six polyhedron results; exceptional automorphisms and the finite degree-six adapter must be included. |
| L074 | [On the number of abstract regular polytopes whose automorphism group is a Suzuki simple group Sz(q) (2010)](https://math.uni.lu/kiefer/Publications/szpoly3%20r%C3%A9vis%C3%A9.pdf) | Both principal Theorems 1 and 2, all stated odd field exponents, including equivalence to the nested published formula; classical Suzuki structure retained. The accessed manuscript is a later revision, so freeze its exact bytes. |
| L088 | [On the thin regular geometries of rank four for the Janko group J(1) (2005)](https://msp.org/iig/2005/1-1/iig-v1-n1-p08-s.pdf) | Six construction Theorems 3.2, 4.2, 5.2, 5.4, 6.2, 7.2 and generation lemmas. The introductory exhaustive six-only/no-higher-rank classification is retained background, not newly rederived. |
| L104 | [The residually weakly primitive geometries of J_2 (2002)](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v21n1p77/585) | Complete principal census: 8 rank-two, 19 rank-three, 3 rank-four and no higher-rank geometries; complete J2 subgroup-class data retained. |
| L108 | [On the Petrials of thin rank 3 geometries (2001)](https://link.springer.com/article/10.1007/s00022-001-8548-2) | Theorem 1 obstruction and valid thin-case structural conclusions of Lemma 3.2. Its unconditional part (ii) is corrected, not proved; a nonthin length assertion also has a counterexample. |
| F013 | [String C-groups of 2-power order project onto a common string C-group (2026)](https://arxiv.org/html/2605.20691v1) | Theorems 1.1/1.2 for all finite nondegenerate two-group string markings, rank at least two; auxiliary Theorem 4.2(c–e) assertions are counterexample targets, not recovered literal assertions. |
| F016 | [Symmetric polytopes whose automorphism groups are 2-groups (2025)](https://arxiv.org/abs/2512.15511v1) | Six principal Theorems 5.1, 5.3, 6.1, 7.1–7.3, with all stated clauses. Tail-triangle geometry and universal-extension/amalgam identifications retained. |
| N001 | [Some properties of inductively minimal geometries (1998)](https://doi.org/10.36045/bbms/1103409005) | Four parts of Theorem 1: RWPRI/(2T)1/(IP)2, even-rank PRI, QPRI criterion and RPRI criterion; foundational 1997 classification/uniqueness retained. Indexed full text recorded as read, original PDF unavailable. |
| N003 | [Independent generating sets and geometries for symmetric groups (2002)](https://maths.qmul.ac.uk/~pjc/preprints/igsgsn.pdf) | All eight numbered results: Theorems 1.1, 2.1, 3.1, 3.2 and Corollaries 2.2–2.4, 3.3, in finite-group and n≥7 scope. Whiston W1 **and** CFSG-dependent W2 retained; unnumbered small-degree exceptions excluded. |
| N008 | [Using the Frattini Subgroup and Independent Generating Sets to Study RWPRI Geometries (2005)](https://ftp.gwdg.de/pub/EMIS/journals/BAG/vol.46/no.1/b46h1car.pdf) | Principal geometric results, finite relative-generation Theorem 2.1 and residue test; the unrestricted infinite converse needs an added hypothesis and is not recovered as printed. Gaschütz, historical catalogues and algorithms retained/excluded as specified. |
| N009 | [String C-groups of order 1024 (2018)](https://cdm.ucalgary.ca/article/download/62475/46803) | Principal nondegenerate census in ranks 2–5 (1,125,105,8 classes), higher-rank exclusion, central mechanisms, exceptional presentations, facets and universal orders. Ledger has all 27 numbered items and six tables; retained earlier results, repaired presentation entries and orientation conventions remain explicit. |
| N013 | [Locally Spherical Hypertopes from Generalised Cubes (2020 preprint; 2021 journal)](https://arxiv.org/abs/2001.11082v1) | Complete principal construction and §4 applications, including Theorem 3.1, Proposition 3.2, Corollary 3.3, Lemma 2.4; generalized-cube background, Coxeter classifications and Pellicer extension retained. Remark 4.1 is rank-qualified. |

These qualifications are material. If the user intends an excluded statement as a main result—for example, L088's exhaustive classification—then that paper cannot yet enter the approved whole-manuscript numerator under the present target set. False auxiliary claims must be listed as corrected, never counted as corollaries of a sound common theory.

## 3. Concrete `X,Y,Z -> Compress` mappings

### A. Forest cuts and relative generation: the strongest small multi-paper candidate

`N001 (1998) + N003 (2002) [+ N008 (2005)] -> Compress_A: Forest cuts, relative generators and Frattini kernels.`

The shared mechanism is concrete: tree transpositions generate products of component symmetric groups, unique paths give exact subgroup intersections, laminar cuts give common flag representatives, and maximal subgroup chains connect relative generators to primitive geometry. The sign-kernel construction handles the second symmetric-group family. Adding N008 requires a further Frattini-ladder theorem, quotient transport and a coordinate-hyperplane theorem; it is a coherent extension, not literally an immediate consequence of tree cuts alone.

Targets are exactly the four N001 conclusions, the eight N003 numbered results, and the scoped N008 results in the table. The retained inputs are N001's 1997 classification, N003's Whiston W1/W2 and Cayley formula, standard coset criteria, and N008's elementary p-group Frattini fact/Zorn argument in the stated infinite case. W2 must not be collapsed into the weaker numerical bound W1.

**What exists:** [tree core](../research/case_study/phase5_tree_cuts.md), [weighted/parity extension](../research/case_study/phase6_weighted_tree.md), an actual [compact eight-result replacement proof](../research/case_study/phase15_N003_matched_proof.md), and a substantive [Frattini replacement note](../research/case_study/phase16_frattini_geometry_reduction.md). These contain proofs, not just proposed encodings. The N003 proof also contains significant module, overgroup and arbitrary-parabolic arguments: they belong in the denominator.

**What still needs assembly:** one notation, one account of geometry axioms, explicit N001 source corollaries, optional N008 chapter, and a common input list. A credible short replacement is plausible; no common manuscript or measured multi-paper factor is present. Start with N001+N003 and add N008 only if its extra chapter improves scope without disguising its cost.

### B. Marked two-groups: strongest broad mathematical programme, substantial adapters

`L032 (2020) + L035 (2019) + F013 (2026) + F016 (2025) [+ N009 (2018)] -> Compress_B: Quotients, deletion maps and bounded cores of marked two-groups.`

Actual shared theorems include kernel/intersection transport, Boolean deletion retractions, fiber-product generation and order, dihedral edge inflation, the canonical forest/path quotient, and bounded cyclic extensions described by affine cocycle equations. These are useful structural replacements for repeated order and intersection work.

The exact recovery paths are:

- L032 Theorem 1.2 and L035 Theorem 1.2: square-grid seed plus independent edge inflation.
- L035 Theorem 1.3: cyclic-core reduction **plus** the explicit eight models, completeness proof and bounded order-256 census. Inflation alone does not prove classification.
- F013 Theorems 1.1/1.2: graded support separation and the resulting path quotient, followed by the covering correspondence.
- F016 Theorems 5.1/5.3: rank-three lattice seeds, Boolean fiber products and presentation recognition; Theorem 6.1 adds its retained geometric bridge; Theorems 7.1–7.3 use a separate amalgam torsion argument. The manuscript itself correctly distinguishes fiber products from free products with amalgamation.
- N009: kernel ladders and profiles plus rank-three enumeration, presentation recognition, named-facet isomorphisms and all finite universal orders. The full statement ledger shows that a general quotient lemma alone is far from enough.

Evidence: [inflation and seeds](../research/case_study/compression_phase2.md), [eight-family classification](../research/case_study/phase3_classification.md), [bounded extension theorem](../research/case_study/phase3_bounded_families.md), [forest quotient proof](../research/case_study/phase15_graded_support.md), [six F016 theorem adapters](../research/case_study/phase16_fiber_products.md), [N009 complete ledger](../research/case_study/phase24_N009_coverage.md).

Retained inputs include Burnside, Lucchini, SmallGroups completeness for the specified L035 branch, standard polytope correspondences, square-lattice classification, tail-triangle/universal amalgam geometry, and GAP/NQ/Todd–Coxeter algorithmic correctness where used. N009 additionally retains its cited infinite decomposition and other earlier results.

**Judgement:** a real common toolkit and detailed adapters exist; an assembled short manuscript has not been demonstrated. This is the best broad candidate, but the current evidence does not justify calling every adapter “relatively straightforward.” N009 is particularly expensive. First assemble the four-paper bundle, then measure N009's marginal cost including its necessary certificate/data interface before admitting it to the intake set. Do not use a count of 105 or 125 classes as a substitute for the proof and data needed to recover the named classification.

### C. Endpoint operations and actual geometry

`L088 (2005) + N013 (2020/2021) [+ L108 (2001)] -> Compress_C: Marking operations, kernels and geometric recognition.`

The [endpoint theorem](../research/case_study/phase26_halving_core.md) gives an exact criterion: one parabolic overlap and a least-support/intersection-closed recovery family. This is meaningful compression of many subgroup-meet cases. The [graph-cover theorem](../research/case_study/phase27_parity_theory.md) handles flag completion, residual connectivity and residue transport separately; its parity condition cannot be omitted just because a marking has intersection property.

L088's six markings come from one seed, endpoint conjugation and a central involution twist; source presentation identification and actual geometric tests remain necessary. N013's construction and applications require nested-shadow recognition and even-coordinate generalized-cube groups. L108's obstruction uses a different retained-object action/kernel argument; it can fit thematically, but it is not already shown to be a short corollary of endpoint halving.

Evidence: [L088 proof](../research/case_study/phase24_L088_theory.md), [N013 application adapters](../research/case_study/phase30_source_adapters.md), [L108 proof/corrections](../research/case_study/phase25_L108_reduction.md). Retain J1 group data and exact algorithms, the earlier exhaustive J1 classification, Danzer/Pellicer and relevant Coxeter classifications, standard geometry correspondences, and conventional Petrie-walk definitions.

**Judgement:** good potential for an operation-and-recognition manuscript; full assembly and a proof of shortness remain. Prefer L088+N013 as the initial multi-paper target. Include L108 only with an honest separate kernel lemma and corrected target statement. A fresh source audit must decide whether the retained exhaustive J1 classification is background or part of the user's intended main-result set.

### D. Two counting papers: shared orbit principle, different hard inputs

`L066 (2013) + L074 (2010) -> Compress_D: Marked-action normal forms and orbit counting.`

L066 decomposes a finite `C2^2`-set into five orbit types, then imposes faithfulness/parity and generator interchange. L074 first normalizes Suzuki generating triples using field coordinates, proves generation by a field-of-definition criterion and checks intersection/rank; only then do Burnside/Möbius counting and formula conversion apply.

Evidence: [pair-counting proof](../research/case_study/commuting_pairs_compression.md), [general elementary-action theorem](../research/case_study/elementary_action_theorem.md), [Suzuki normalization/counting proof](../research/case_study/phase10_suzuki_marked_fields.md). Retain symmetric/alternating automorphism structure including degree-six exceptions, and the explicitly enumerated classical Suzuki structure.

**Judgement:** two convincing source-specific reductions exist, but a common Burnside theorem by itself does not make the Suzuki structural adapter short. L066's degree-six polyhedron results also need their finite adapter. This could be a paired replacement manuscript, but its actual advantage over two separate short notes must be measured. The additional L085 rank/existence consequence in the Suzuki note is a selected theorem from another manuscript, not automatic permission to add all of L085 to the whole-manuscript numerator.

### E. Finite coset census: one whole-paper candidate with partial neighbours

`L104 (2002) -> Compress_E: Arbitrary-Borel panel augmentation and automorphism fusion.`

The [general census theorem](../research/case_study/phase5_j2_theory.md) supplies arbitrary-rank completeness and a normalizer-action search; the J2 instance recovers all principal counts without taking the source's geometry list as input. It does take a complete subgroup catalogue. Other sporadic entries may share this mechanism, but their original full texts, exact supplement conventions or full-main-result scope remain incomplete in the registry.

**Judgement:** a credible single-paper replacement with reusable algorithmic theory; no established multi-manuscript `Compress` for the neighbouring sporadic papers. Full subgroup-catalogue cost must be either explicitly common background or separately charged. A short search program and a short human proof are different deliverables.

### F. Chirality and Kneser geometry: do not force a common core

`L008 (2026) -> Compress_F1: Double-coset extension fibers and the chirality criterion.`

`L030 (2021) -> Compress_F2: Tensor Kneser incidence and its automorphisms.`

Both are developed in [incidence_compression.md](../research/case_study/incidence_compression.md). L008 uses two-point fibers and marked inversion. L030 uses `K_r tensor KG(N,k)`, set combinatorics, exact distances and a spectral automorphism argument. Those are different mechanisms. The [torsor/partition core](../research/case_study/torsor_matrix_theory.md) gives a rigorous common language and useful Helly/residue tests, but it does not supply the needed Kneser eigenspace theorem or chirality correspondence.

**Judgement:** each is a plausible short replacement; putting them in the same file is not evidence of genuine cross-paper compression. No common manuscript covering all sixteen with uniformly short corollaries is established by the matrix language.

## 4. What the two existing numbers actually establish

The [L066 measurement](../research/case_study/phase9_L066_measurement.md) is `10,668/3,192 = 127/38 ≈ 3.3421`. It compares selected proof spans for Theorems 1.1/1.2 outside degree six. It excludes the two polyhedron results, degree-six exceptional work, target statements and manuscript exposition. Its retained common background is explicit. This is genuine evidence of a shorter proof description for that theorem pair, not a whole-L066 or multi-paper factor.

The [N003 measurement](../research/case_study/phase15_N003_measurement.md) is `9,680/7,260 = 4/3 ≈ 1.3333` in normalized non-whitespace characters. It covers all eight numbered targets in the stated scope and charges the module, forest/sign, overgroup, flag and panel arguments. It retains Whiston W1/W2 and other declared common background; manuscript front matter, target statements and excluded unnumbered material are outside the matched spans. It is still not the user's full-manuscript ratio.

These two ratios must not be averaged, multiplied, applied to the sixteen-paper count, or promoted into a corpus estimate. Neither a six-coordinate affine realization replacing 1,296 coordinates nor fixed-excess class-index bits measures proof-manuscript compression. I have no defensible aggregate number to report, and no basis for promising that the final manuscript-level ratio will exceed one for every bundle.

## 5. Practical steps to produce an actual publishable `Compress`

1. **Freeze one intake contract.** Start with N001+N003, or L032+L035+F013+F016. Record exact source versions, hashes, source lengths, all main results and their full hypotheses. Have a fresh reader identify main results from abstracts, introductions, conclusions and theorem statements before consulting registry labels. For N001, obtain a stable authoritative full-text representation or document why manuscript-length measurement is unavailable; do not infer it from an abstract or page count.
2. **Make the replacement an actual standalone text.** Write definitions and the common theorems in publication order; prove them once. Remove chronological phase narration. State every intake main result as a labelled corollary, with a direct chain to the common theorems. Include full adapters rather than links to a dozen working notes. An appendix is part of the manuscript and its length counts.
3. **Use a dependency matrix.** One row per source main result; columns for exact source statement/version, common theorem, adapter, imported theorem/data, scope correction, proof status and check. This exposes circular imports and cases where the purported adapter contains most of the source-specific proof. An inherited source main theorem cannot be treated as free input to its own rederivation.
4. **Close the particular bundle's gaps.** For A: explicit N001 cut-property corollaries, unchanged Whiston hypotheses, exact N008 infinite scope if added. For B: eight-family completeness, every clause of all six F016 theorems, separate amalgam proof, and all canonical quotient hypotheses. For C: actual Helly/residual-connectivity proofs and application residues. For D: degree-six results and exact Suzuki formula equivalence. For N009: named outputs, universal orders, retained infinite row and corrected presentations. These are concrete manuscript work items, not requests for more breadth.
5. **Publish a retained-input declaration.** State the common background once, distinguishing standard foundations from substantial classifications and catalogues. If Suzuki or J2 subgroup structure, Whiston W2, SmallGroups, or a universal-geometric theorem is not expanded, call the result conditional on that input. Give a sensitivity/expanded-background column where feasible. The project need not reprove all mathematics from axioms, but it must not turn a missing proof into a free citation selectively.
6. **Measure exactly the user's deliverable.** Count the full frozen intake manuscripts with one declared text convention, and the actual complete replacement, all necessary adapters and any additional dependencies using that convention. State treatment of references, abstracts, tables and duplicated source preliminaries in advance. Report the user's sum-of-manuscripts numerator and, separately, a deduplicated-source/proof-span diagnostic; they answer different questions. Charge the common replacement once and report marginal cost of each added manuscript. Do not count a source at whole-manuscript length before its main-result coverage audit passes.
7. **Keep certificate costs visible.** Give separate prose, executable algorithm, indispensable data and formal-source columns. If a classification relies on a finite certificate, supply enough data and a checker to recover the stated named output, and report that cost. For a bundled artifact ratio, use matched bundle conventions on both sides. Avoid crediting a one-line call to an uncharged classifier as the entire proof.
8. **Run independent review on the final text.** A mathematician or fresh reviewing process must trace each corollary using only the replacement and declared background, and flag every nontrivial missing bridge. Recheck source-version corrections and replay necessary exact computations. Existing partial Lean components can support precisely their interfaces; their count cannot certify all source applications.
9. **Prepare submission on its mathematical contribution.** Explain which structural theorem replaces repeated arguments, where the savings occur, and what is inherited. Publish source hashes/locations and original measurement tools without redistributing third-party text. External review and priority checking are separate from an internally consistent compression measurement. A completed and reviewed draft can be called a replacement manuscript before journal acceptance; “publishable” remains an editorial judgement, not a property certified by a ratio.

The first concrete deliverable should therefore be **one finished replacement PDF/source plus a closed main-result matrix and a reproducible manuscript-length report**, not another expansion of the paper count. A small successful bundle would satisfy the user's criterion more directly than a larger unassembled registry.

## 6. Original research must remain a separate ledger

The repository also contains substantial proposed new mathematics: fixed-excess classifications and counting formulas, finite-state descriptions, linear/unitary rank constructions and obstructions, nilpotent cyclic-TPP consequences, source corrections, and toroidal hypertope constructions. They may strengthen a replacement manuscript or merit separate papers, but they do not increase the length of already-compressed source proofs merely by being new.

At the assessed baseline, the toroidal work claims regular finite existence at parameters divisible by two or three, with exact listed local residues, a compact six-coordinate even family, and further universal-group structure. It explicitly leaves parameters coprime to six unresolved in that geometric sense. A dated post-baseline update was committed while this review was being completed: `6a3725e359fe2189f01d1e22c3289bb418d832f2`. Its README reports an [eight-dimensional tensor model](../research/case_study/phase35_L003_tensor_model.md) giving every exact parameter s≥3 and every required local group for s≥4, with a [uniform Fibonacci arithmetic Lean component](../research/case_study/formal/FibonacciModulus.scope.md), bringing the component count to 34. I read that updated scope statement but did not independently verify the new model or compile its certificate. Its global intersection and coset flag conditions remain pending; it is not an all-parameter hypertope theorem and changes neither the sixteen-paper coverage nor the compression conclusion. Local parabolics, relators and orders do not alone establish all flags, flag transitivity or residual connectivity.

Likewise, a replacement proof of F013's stated main theorem is compression/rederivation, while an extension beyond it is a separate result. A counterexample to a published auxiliary assertion is a correction with a source-version boundary, not proof of the false assertion and not automatically resolution of an independently documented open problem. None yields an infinite numerical compression ratio. Priority is unverified for the proposed new results, and internal agreement or a scoped Lean lemma does not resolve priority.

**Current best answer:** there is enough concrete mathematics to justify building several `Compress` manuscripts now. There is no justified single aggregate ratio, no demonstrated one-core compression of all sixteen, and no need to disguise those limitations. The work most directly missing is a closed intake contract, integrated exposition, fully charged adapters and independent main-result review—not a new name for the existing counts.
