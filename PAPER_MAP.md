# Paper map: intake, encoding and proof coverage

This living map distinguishes source access from mathematical progress.
It includes books, proceedings papers and errata as well as journal articles.
The historical inventory is preserved; later assessments apply only to their named targets.

**152 mathematical works** are indexed: 128 catalogue entries and 17 followups and 7 network additions. **46 entries date from 1996–2006.**
This is not complete proof reading or an exhaustive bibliography of every collaborator,
student or postdoc. Coauthorship alone does not establish those relationships.

[Registry](research/case_study/paper_registry.json) · [Introduction](INTRODUCTION.md) · [Reduction scope](research/case_study/torsor_compression_overview.md) · [Historical inventory](research/case_study/literature_inventory.json)

## Read the stages separately

| Stage | Meaning |
|---|---|
| Retrieved | A matched primary full text was accessed; it is not redistributed. |
| Read | Exact scope: abstract, full-text search only, selected sections, or complete short text. |
| Encoded | A specified target has an explicit representation/test; vocabulary alone does not qualify. |
| Rederived | A named theorem, component or finite subfamily has a replacement argument with retained inputs. |
| Principal results rederived | The identified principal results are recovered, not every auxiliary lemma or imported classification. |
| Proposed new result | An internally checked draft consequence; external review and priority verification remain. |
| Unassessed | No replacement-proof assessment is recorded; an empty target list is intentional. This does not mean a source result is unknown or its conjectures remain open. |

These are independent fields. A retrieved paper need not be encoded, and progress on
a problem stated in a survey does not imply its inaccessible original paper was read.

| Access category | Works |
|---|---:|
| abstract read | 50 |
| full short text read | 4 |
| full text read | 1 |
| full text search only | 21 |
| metadata and access only | 9 |
| selected sections read | 67 |

93 works have a retrieved full text; 37 have a specified encoding or conditional/component reduction; 27 have a rederived component, finite subfamily or principal target.
These overlapping totals must not be read as counts of fully reduced papers.

The conservative **principal-result set has 7 works: L008, L030, L032, L035, L066, L104, N001**.
Proposed conjecture proofs are separate and do not increase that count.

## Exact reductions and proposed consequences

| ID | Work | Exact target | Scope and remaining work |
|---|---|---|---|
| L007 | [Chiral polytopes of order 2p m](https://amc-journal.eu/index.php/amc/article/download/3716/2232) | Section 7 omitted even-exponent non-tight existence range, 6 <= m <= p+1 | [proposed new result](research/case_study/central_lift_proof.md). External review and priority verification. Other principal group-enumeration statements are not rederived. The source's apparent tight/non-tight typo is disclosed. |
| L008 | [Testing chirality on hypertopes](https://arxiv.org/pdf/2511.14562) | Theorem 1.1 | [principal results rederived](research/case_study/incidence_compression.md). External review; no end-to-end formalization or claim about every auxiliary result. |
| L009 | [Geometries with trialities arising from linear spaces](https://arxiv.org/pdf/2504.06025) | Construction and symmetry results; Hermitian branch of the classification | [component rederived](research/case_study/incidence_compression.md). Complete the remaining underlying-linear-space classification derivations. |
| L012 | [Regular 3-polytopes of order 2 n p](https://arxiv.org/pdf/2001.02945) | Theorem 5.1 and Corollary 5.2 | [component rederived](research/case_study/phase2_cubic_lattices.md). Other type classifications and nonexistence results remain outside this reduction. |
| L025 | [Edge-girth-regular graphs arising from biaffine planes and Suzuki groups](https://arxiv.org/pdf/2108.06636v1) | Conjecture 3.2; separate audit of Conjecture 4.5 and later Wenger claims | [proposed new result](research/case_study/suzuki_cycle_proof.md). Conjecture 4.5 existence remains unresolved. Other principal statements are not all rederived. External review and priority verification remain; Lean covers the matrix word, not graph identification. |
| L029 | [On residual connectedness in chiral geometries](https://arxiv.org/pdf/1911.03227v1) | Designated-action version of Theorem 1.1; rank-three Proposition 4.9 | [component rederived](research/case_study/incidence_compression.md). The bridge from the source's full-automorphism chirality convention to the designated action remains unproved here. |
| L030 | [An infinite family of locally X graphs based on incidence geometries](https://arxiv.org/pdf/1811.11438v1) | Theorem 4.9; Corollaries 4.10-4.11 and principal construction | [principal results rederived](research/case_study/incidence_compression.md). The note records corrections to two checked source displays. External review remains. |
| L032 | [On regular polytopes of 2-power order](https://dipot.ulb.ac.be/dspace/bitstream/2013/292444/3/HRRPR-revised.pdf) | Theorem 1.2 | [principal results rederived](research/case_study/compression_phase2.md). This existence theorem does not classify every group of the given order. Lean covers abstract kernel transport only. |
| L034 | [Existence of regular 3-hypertopes with 2 n chambers](https://dipot.ulb.ac.be/dspace/bitstream/2013/287227/5/Hy2g.pdf) | Theorem 3.2; specified cases of Conjecture 3.3 | [component rederived](research/case_study/compression_phase2.md). Full Conjecture 3.3 remains unresolved. The source's alternate dihedral-by-dihedral quotient display is not separately verified. |
| L035 | [2-groups behaving as automorphism groups of regular 3-polytopes](https://arxiv.org/pdf/1802.08947v2) | Theorems 1.2 and 1.3 | [principal results rederived](research/case_study/phase3_classification.md). External review; the all-parameter classification is not formalized end to end and the retained finite catalogue is not rederived. |
| L043 | [Projective linear groups as automorphism groups of chiral polytopes](https://arxiv.org/pdf/1606.08017) | Conjectures 6.1 and 6.2; missing nonprime-field case of the introductory classification | [proposed new result](research/case_study/psl2_square_proof.md). External review and priority verification. The character argument and full geometric consequence are not formalized; other published principal results are not all rederived. |
| L048 | [Polytopes of large rank for PSL(4,q)](https://digitalcommons.bucknell.edu/fac_journ/1204/) | Odd-characteristic PSL4 maximum rank; exact conjecture read in L120, Conjecture 2 | [partial progress](research/case_study/phase3_psl4_rank7.md). Rank six remains, so maximum rank four is not proved. L048 full text was unavailable; progress through the survey does not imply it was read. External review and priority remain. |
| L050 | [Linear codes with complementary duals from some strongly regular subgraphs of the McLaughlin graph](https://www.mathos.unios.hr/mc/index.php/mc/article/download/1537/388) | Orthogonality, LCD and complement-dual assertions | [component rederived](research/case_study/incidence_compression.md). Ranks, minimum distances, weight enumerators and invariant-module classifications remain. |
| L052 | [Highly symmetric hypertopes](https://ria.ua.pt/bitstream/10773/16681/1/2016DFW.pdf) | Problems 9.3 and 9.4 under the standard parabolic coset construction | [proposed new result](research/case_study/coset_geometry_obstructions.md). External review and priority verification. Other questions and principal constructions are not all rederived. |
| L063 | [The rank two geometries of the PSL(2,q) groups : part II](https://amc-journal.eu/index.php/amc/article/download/181/241) | Complete A4-A4 family in Table 5; relevant Table 2 comparison | [component rederived](research/case_study/classification_compression.md). Other subgroup rows and completeness remain. Composite-degree extensions are not RWPRI. The ordered/unordered discrepancy is version-specific. |
| L066 | [On pairs of commuting involutions in Sym(n) and Alt(n)](https://math.uni.lu/kiefer/Publications/Involutions.pdf) | All four principal counting and degree-six polyhedron results | [principal results rederived](research/case_study/commuting_pairs_compression.md). External review; no priority claim for classical orbit, Burnside or Möbius ingredients. |
| L089 | [On inductively minimal geometries that satisfy the intersection property](https://leemans.dimitri.web.ulb.be/abstracts/imgip.html) | Advertised characterization of inductively minimal geometries with geometric intersection property | [component rederived](research/case_study/phase5_tree_cuts.md). Full 2005 text unavailable; target is the primary abstract and exact earlier restatement. Foundational classification retained, no new-resolution claim. |
| L092 | [A generalization of a construction due to Van Nypelseer](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.46/no.2/b46h2lee.pdf) | Conjecture 1, Section 4.6, p. 569 | [proposed new result](research/case_study/hermitian_unital_proof.md). External review and priority verification. Other constructions and applications in the paper are not all rederived; Lean checks abstract connectivity only. |
| L096 | [An algorithmic analysis of the intersection property](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/2108DB59271CED59B950340F28252A28/S1461157000001133a.pdf/div-class-title-an-algorithmic-analysis-of-the-intersection-property-div.pdf) | Sections 2-3 shadow-IP decision problem and known rank-two characterization | [generic encoding](research/case_study/phase4_shadow_ip.md). The original Magma implementation and sporadic classification tables are not rerun. No performance claim or whole-paper reproduction is made. |
| L098 | [The residually weakly primitive geometries of M_23](https://www.math.auckland.ac.nz/~dleemans/abstracts/m23.html) | The firm/FT/RC/RWPRI/(IP)2/(2T)1 M23 census stated in the primary abstract and later primary tables | [component rederived](research/case_study/phase7_sporadic_theory.md). Original article body and supplement conventions remain unavailable; no claim to reproduce every construction or diagram. Catalogue completeness is retained; no whole-paper or novelty claim. |
| L101 | [The residually weakly primitive geometries of M_22](https://www.math.auckland.ac.nz/~dleemans/abstracts/m22.html) | The firm/FT/RC/RWPRI/(IP)2/(2T)1 M22 census stated in the primary abstract and later primary tables | [component rederived](research/case_study/phase7_sporadic_theory.md). Original two-page article body and supplement conventions remain unavailable; no claim to reproduce every construction or diagram. Catalogue completeness is retained; no whole-paper or novelty claim. |
| L102 | [RWPRI and (2T)_1 flag-transitive linear spaces](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.44/no.1/b44h1bue.pdf) | Section 5.1.2 uniqueness question; existence and uniqueness of spaces in Theorem 6.1(1) | [proposed new result](research/case_study/phase4_old_problem_audit.md). External review and priority verification. This identifies the spaces in the narrow source case, not every possible acting subgroup, all flag-transitive spread spaces, or the other principal classification cases. |
| L104 | [The residually weakly primitive geometries of J_2](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v21n1p77/585) | Complete principal census: 8 rank-two, 19 rank-three, 3 rank-four geometries, and no higher ranks | [principal results rederived](research/case_study/phase5_j2_theory.md). The subgroup catalogue and every secondary supplement annotation are not rederived. No end-to-end Lean formalization; external review remains. |
| L105 | [Constructing coset geometries with Magma : An application to the sporadic groups M(12) and J(1)](https://www.math.auckland.ac.nz/~dleemans/abstracts/algo.html) | M12 broader RWPRI/(IP)2 census and rank-five conclusion stated in the abstract | [component rederived](research/case_study/phase6_sporadic_theory.md). Original full text unavailable; its corrected J1 entry has not been identified. M12's old summary-table discrepancy and archive omission are version-specific observations, not a claim of correcting the unread article. |
| L109 | [The residually weakly primitive geometries of the Dihedral Groups](https://www.math.auckland.ac.nz/~dleemans/abstracts/d2n.html) | Complete all-rank three-family classification and counts quoted in L110 Theorem 4; rank-two theorem quoted in L114 Theorem 5.1 | [component rederived](research/case_study/phase5_dihedral_classification.md). L109 full text remains unavailable; its complete all-rank principal classification is available in the primary L110 restatement, but every original statement has not been compared. No new-conjecture or whole-paper claim. |
| L110 | [The residually weakly primitive pre-geometries of the Suzuki simple groups](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v20n1p1/995) | Rank-three shape decisions; rank-four geometry with Construction 6 parabolic types; all admissible parameterized existence assertions of Constructions 8 and 9 | [partial progress](research/case_study/phase7_suzuki_descent.md). A corrected exhaustive classification, other higher-rank constructions and relative embedding classes remain. The two entire parameterized existence assertions are recovered, including overlapping-prime cases, with FT and RC for their canonical realizations; no classification of all embeddings. Priority and external review remain. |
| L114 | [The rank 3 geometries of the simple Suzuki groups Sz(q)](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v19n1p43/837) | Theorem 5.5 exhaustiveness: explicit omitted geometry in Sz(2^15); decisions for every printed shape in Theorems 5.3 and 5.5 | [proposed new result](research/case_study/phase6_suzuki_realization.md). A corrected exhaustive list, relative embedding classes and publication priority remain unresolved. The exact counterexample is internally reviewed and computationally checked; Lean covers its abstract Helly implication, not the matrix instantiation. Historical phase-five completeness assumptions are superseded. |
| L115 | [The Rank 2 Geometries of the Simple Suzuki Groups Sz(q)](https://emis.de/ft/11479) | Corollary 8.1: 29 rank-two geometries of Sz(8) | [finite subfamily reproduced](research/case_study/classification_compression.md). All-q Theorem 7.1 is not rederived. A finite corollary does not give whole-paper coverage. |
| L124 | [On Flag-Transitive Incidence Geometries of Rank 6 for the Mathieu Group M(12)](https://www.math.auckland.ac.nz/~dleemans/abstracts/m12.html) | No RWPRI/(IP)2 M12 geometry of rank at least six, as stated in the primary abstract | [component rederived](research/case_study/phase6_sporadic_theory.md). Chapter body unavailable; individual constructions and the original sixteen-page proof have not been compared. Catalogue completeness is retained, not rederived. |
| L125 | [The Residually Weakly Primitive Geometries of the Janko Group J(1)](https://www.math.auckland.ac.nz/~dleemans/abstracts/j1.html) | The firm/FT/RC/RWPRI/(IP)2 J1 classification problem stated in the primary abstract | [component rederived](research/case_study/phase6_sporadic_theory.md). The original chapter and its exact entry-by-entry equivalence convention remain unavailable. L105's correction is recorded but its exact old missing entry is not identified. No whole-paper or novelty claim. |
| N001 | [Some properties of inductively minimal geometries](https://doi.org/10.36045/bbms/1103409005) | Four parts of Theorem 1: RWPRI/(2T)1/(IP)2, even-rank PRI, QPRI/middle criterion, and RPRI/complete-diagram criterion | [principal results rederived](research/case_study/phase5_tree_cuts.md). Foundational classification remains an input; no end-to-end Lean proof or numerical compression ratio. External review remains. |
| N002 | [On the number of inductively minimal geometries](https://doi.org/10.1016/S0304-3975(00)00228-0) | Tree correspondence announced in the primary abstract | [component rederived](research/case_study/phase5_tree_cuts.md). Source full text unavailable; no full-paper comparison or novel resolution of its historical direct-construction question. |
| N003 | [Independent generating sets and geometries for symmetric groups](https://maths.qmul.ac.uk/~pjc/preprints/igsgsn.pdf) | Tree-transposition branch of Corollary 2.3 and Theorem 3.2 | [component rederived](research/case_study/phase5_tree_cuts.md). Parity-twisted branch, full maximal-independent-generator classification and other general group results are not rederived. |
| N004 | [Truncations of inductively minimal geometries](https://doi.org/10.1016/S0012-365X(02)00603-9) | Advertised RWPRI/(IP)2 truncation target, via a complete weighted-tree model | [component rederived](research/case_study/phase6_weighted_tree.md). The all-parameter model theorem is proved and internally reviewed; original full text remains unavailable. No whole-paper equivalence, abstract isomorphism classification or novelty claim. |

## The 1996–2006 track

The older entries now include these explicit reductions and proof targets:

- **L102 (2003):** the one-dimensional affine RWPRI spread-space question has a
  proposed existence-and-uniqueness solution by cyclic semilinear descent and
  an explicit scalar affine action. It retains the translation/spread reduction
  and both local primitivity hypotheses. Arbitrary acting subgroups and general
  flag-transitive spread spaces are not classified; external review and priority remain.
- **L092 (2005):** the Hermitian-unital conjecture has a proposed uniform proof via
  an SU(2,q) torsor. This does not rederive every construction in the source paper.
- **L104 (2002):** independent arbitrary-Borel augmentation recovers the full
  principal 8/19/3 census and excludes higher ranks, with every branch exhausted.
  The source geometry list is not an input; complete GAP subgroup data remain.
- **L125/L105/L124 (1998–2002):** the generalized engine admits every primitive
  panel, giving complete explicit J1/M11/M12 censuses under Aut(G)/type equivalence.
  It recovers the stated M12 rank bound. Original chapter/article bodies remain
  unavailable; M11's separate census is not the maximal-subgroup problem L119.
- **L109 (2000):** cyclic/dihedral rank-two rigidity and CRT give an all-rank
  arithmetic classification. Its full all-rank theorem is matched through L110; the original
  full text is unavailable, so a whole-paper comparison remains open.
- **N001–N003 and L089 (1998–2005):** one tree-cut derivation gives the four
  1998 property tests, the tree correspondence, the known transposition-tree
  geometry branch, and the advertised 2005 path/shadow-IP characterization.
  The foundational 1997 classification is retained; source access differs by work.
- **N004 (2003):** contraction with vertex weights incorporates every tree-family
  truncation. Exact local and full-shadow criteria are proved, with a new Lean
  witness theorem for retained consecutive ranks. The source full text remains
  unavailable, so this is a model-level/advertised-target reduction only.
- **L114/L110 (1999–2001):** trace/torus constructions realize the prime-case
  patterns and decides every printed composite-field pattern. Four have impossible
  intersections; a fifth exists as an embedded lattice but fails RWPRI. A further
  exact matrix example in Sz(2^15) is firm, residually connected, flag-transitive
  and RWPRI, but absent from the asserted exhaustive list. Completeness of that
  list is withdrawn. A rank-four extension matches Construction 6 parabolic
  types; its flag transitivity and a corrected general classification remain.
- **L115 (1998):** the 29-object Sz(8) corollary is reproduced, while the all-q
  theorem remains. Witness validity and catalogue-dependent completeness are separate.
- **L096 (2004):** geometric shadow-IP has a Boolean witness criterion. It is
  distinct from C-group subgroup IP. The exact decision/orbit reduction is proved;
  the original Magma implementation and sporadic tables are not rerun.

The source-level limitations below are retained verbatim in the JSON. L102's
historical intake says current status was unverified; the later proof entry is a
proposed result, not a silent rewrite of that historical search. L114's realization
question now has the proposed complete displayed-lattice decisions above. L084 is a distinct erratum that still needs
its own full text. Abstract summaries identify topics, not proved theorem reductions.

| Year / ID | Work and primary link | Access / progress | Recorded source scope and remaining work |
|---|---|---|---|
| 1996 / L118 | [On the List of Finite Primitive Permutation Groups of Degree Less Than 50](https://www.math.auckland.ac.nz/~dleemans/abstracts/primlist.html) | abstract read; unassessed | Author abstract completes Sims-list structures. Author-posted corrections: P25N21 orbit pattern 1^5,10^2; P31N2 is D62. |
| 1996 / L119 | [All Geometries of the Mathieu Group M(11) Based on Maximal Subgroups](https://www.math.auckland.ac.nz/~dleemans/abstracts/m11.html) | abstract read; unassessed | Author abstract classifies M11 geometries whose element stabilizers are maximal, under specified incidence axioms. |
| 1997 / L117 | [Two Nearly Isomorphic Groups](https://www.math.auckland.ac.nz/~dleemans/abstracts/twoiso.html) | abstract read; unassessed | Author abstract gives two degree-49 groups with isomorphic conjugacy-class subgroup posets and corresponding normal quotients. |
| 1997 / L123 | [The residually weakly primitive geometries of the Suzuki simple group Sz(8)](https://www.math.auckland.ac.nz/~dleemans/abstracts/sz8.html) | abstract read; unassessed | Correct author abstract is the Sz(8)-specific RWPRI classification, not the general Suzuki pregeometry paper wrongly downloaded earlier as catalogue_L123.pdf. |
| 1998 / L115 | [The Rank 2 Geometries of the Simple Suzuki Groups Sz(q)](https://emis.de/ft/11479) | selected sections read; finite subfamily reproduced | Entire extracted text searched; section9 future-work context read. Theorem7.1 classifies rank-two Suzuki geometries. Historical proposed higher-rank Suzuki work appears in L114/L110; analogous PSL2 work appears in later papers. No new named conjecture extracted. Remaining: All-q Theorem 7.1 is not rederived. A finite corollary does not give whole-paper coverage. |
| 1998 / L116 | [Thin geometries for the Suzuki simple group Sz(8)](https://www.math.auckland.ac.nz/~dleemans/abstracts/sz8thin.html) | abstract read; unassessed | Author abstract states 183 thin residually connected Sz(8) geometries, all rank three, with computed truncations. |
| 1998 / L124 | [On Flag-Transitive Incidence Geometries of Rank 6 for the Mathieu Group M(12)](https://www.math.auckland.ac.nz/~dleemans/abstracts/m12.html) | abstract read; component rederived | Author abstract excludes M12 RWPRI/IP2 geometries of rank at least six. Remaining: Chapter body unavailable; individual constructions and the original sixteen-page proof have not been compared. Catalogue completeness is retained, not rederived. |
| 1998 / L125 | [The Residually Weakly Primitive Geometries of the Janko Group J(1)](https://www.math.auckland.ac.nz/~dleemans/abstracts/j1.html) | abstract read; component rederived | Author abstract classifies J1 RWPRI/IP2 geometries; later L105 reports a missing geometry, so original list needs that correction. Remaining: The original chapter and its exact entry-by-entry equivalence convention remain unavailable. L105's correction is recorded but its exact old missing entry is not identified. No whole-paper or novelty claim. |
| 1998 / N001 | [Some properties of inductively minimal geometries](https://doi.org/10.36045/bbms/1103409005) | selected sections read; principal results rederived | Primary author-uploaded text: definitions, foundational Lemma 1, four-part Theorem 1 and proof components read. Publisher PDF returned an HTML challenge; no PDF identity asserted. Remaining: Foundational classification remains an input; no end-to-end Lean proof or numerical compression ratio. External review remains. |
| 1999 / L002 | [An Atlas of Residually Weakly Primitive Geometries for Small Groups](https://leemans.dimitri.web.ulb.be/abstracts/atlas.html) | abstract read; unassessed | Author abstract and errata read; book full text not located. |
| 1999 / L112 | [On a geometry of Ivanov and Shpectorov for the O'Nan sporadic simple group](https://www.math.auckland.ac.nz/~dleemans/abstracts/on.html) | abstract read; unassessed | Author abstract bounds O’Nan RWPRI/IP2 ranks with M11 or J1 parabolics. |
| 1999 / L113 | [An Atlas of regular thin geometries for small groups](https://www.math.auckland.ac.nz/~dleemans/abstracts/atlasthin.html) | abstract read; unassessed | Author abstract describes a computed atlas of regular thin geometries; thin need not mean string. |
| 1999 / L114 | [The rank 3 geometries of the simple Suzuki groups Sz(q)](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v19n1p43/837) | selected sections read; proposed new result | OCR of all21pages searched; introduction, Theorem6.1 and final paragraph p61 read. Theorems5.3–5.5 list possible rank-three RWPRI sublattices. Final paragraph explicitly leaves realization of all candidates unproved (Sz8 realized). No current-resolution claim. Later reading: Theorems 5.3–5.5 and their case analyses read; printed pp.58–60 visually checked; Lemma3.11 and final p.61 realization qualification checked. Remaining: A corrected exhaustive list, relative embedding classes and publication priority remain unresolved. The exact counterexample is internally reviewed and computationally checked; Lean covers its abstract Helly implication, not the matrix instantiation. Historical phase-five completeness assumptions are superseded. |
| 2000 / L006 | [Incidence Geometry](https://leemans.dimitri.web.ulb.be/abstracts/incgeom.html) | abstract read; unassessed | Author abstract read; historical2000 Magma handbook chapter not obtained. Current software documentation is not the same version. |
| 2000 / L109 | [The residually weakly primitive geometries of the Dihedral Groups](https://www.math.auckland.ac.nz/~dleemans/abstracts/d2n.html) | abstract read; component rederived | Author abstract states classification of RWPRI geometries of dihedral groups. Remaining: L109 full text remains unavailable; its complete all-rank principal classification is available in the primary L110 restatement, but every original statement has not been compared. No new-conjecture or whole-paper claim. |
| 2000 / L110 | [The residually weakly primitive pre-geometries of the Suzuki simple groups](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v20n1p1/995) | selected sections read; partial progress | PDF identity checked against title. Entire extracted text searched for conjectures, problems, questions, unknown cases and future work; no claim to have read every proof. Later reading: Rank-three R1–R13, higher-rank construction context and p.11 flag-transitivity uncertainty checked; exact hypotheses compared with L114. Remaining: A corrected exhaustive classification, other higher-rank constructions and relative embedding classes remain. The two entire parameterized existence assertions are recovered, including overlapping-prime cases, with FT and RC for their canonical realizations; no classification of all embeddings. Priority and external review remain. |
| 2000 / L111 | [New geometries for finite groups and polytopes](https://www.math.auckland.ac.nz/~dleemans/abstracts/ngeo.html) | abstract read; unassessed | Author abstract describes two general construction methods under diagram hypotheses. |
| 2001 / L106 | [On a rank five geometry of Meixner for the Mathieu group M(12)](https://www.math.auckland.ac.nz/~dleemans/abstracts/m12b.html) | abstract read; unassessed | Author abstract constructs Meixner’s M12 rank-five geometry and establishes RWPRI/IP2. |
| 2001 / L107 | [Some rank five geometries related to the Mathieu group M(23)](https://www.math.auckland.ac.nz/~dleemans/abstracts/m23rk5.html) | abstract read; unassessed | Author abstract constructs six rank-five M23 geometries. |
| 2001 / L108 | [On the Petrials of thin regular rank three geometries](https://www.math.auckland.ac.nz/~dleemans/abstracts/petrie.html) | abstract read; unassessed | Author abstract proves that a thin regular rank-three geometry with thin regular Petrial has a linear diagram. |
| 2001 / N002 | [On the number of inductively minimal geometries](https://doi.org/10.1016/S0304-3975(00)00228-0) | abstract read; component rederived | Primary abstract and later Cameron–Cara tree-model restatement read. Full-text download unavailable in this intake; no complete source-statement comparison. Remaining: Source full text unavailable; no full-paper comparison or novel resolution of its historical direct-construction question. |
| 2002 / L103 | [The RWPRI geometries of Sym(5) x 2](https://www.math.auckland.ac.nz/~dleemans/abstracts/s5x2.html) | abstract read; unassessed | Author abstract describes the RWPRI geometries of Sym(5) x 2 and direct-sum/extension constructions. |
| 2002 / L104 | [The residually weakly primitive geometries of J_2](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v21n1p77/585) | full short text read; principal results rederived | PDF identity checked against title. Entire extracted text searched for conjectures, problems, questions, unknown cases and future work; no claim to have read every proof. Later reading: All five pages read by rank_stability; confirmed in the root's registry review on 2026-10-09. Section 3 counts compared in the classification reduction. Remaining: The subgroup catalogue and every secondary supplement annotation are not rederived. No end-to-end Lean formalization; external review remains. |
| 2002 / L105 | [Constructing coset geometries with Magma : An application to the sporadic groups M(12) and J(1)](https://www.math.auckland.ac.nz/~dleemans/abstracts/algo.html) | abstract read; component rederived | Author abstract describes a Magma algorithm, a missed J1 geometry correcting L125, and M12 rank-five examples. Remaining: Original full text unavailable; its corrected J1 entry has not been identified. M12's old summary-table discrepancy and archive omission are version-specific observations, not a claim of correcting the unread article. |
| 2002 / N003 | [Independent generating sets and geometries for symmetric groups](https://maths.qmul.ac.uk/~pjc/preprints/igsgsn.pdf) | full text read; component rederived | All twelve pages of the author manuscript read. Tree branch is rederived; maximal independent generator classification, parity-twisted branch and Whiston/CFSG dependencies are retained. Later reading: All twelve pages of the author manuscript read; publication identity checked against the author catalogue and publisher. Remaining: Parity-twisted branch, full maximal-independent-generator classification and other general group results are not rederived. |
| 2003 / L005 | [Residually weakly primitive geometries of small sporadic and almost simple groups : a synthesis](https://leemans.dimitri.web.ulb.be/abstracts/synthese.html) | metadata and access only; unassessed | Exact-title author catalogue/OpenAlex and primary publisher or institutional locations searched; no accessible primary full text obtained. No inference that the work contains no open problems. |
| 2003 / L099 | [On a rank four geometry for the Hall-Janko sporadic group](https://www.sciencedirect.com/science/article/pii/S0097316502000225) | abstract read; unassessed | Publisher abstract constructs a rank-four Hall–Janko geometry from the degree63 graph on100points; no full-text audit. |
| 2003 / L100 | [Geometries for the group PSL(3,4)](https://www.math.auckland.ac.nz/~dleemans/abstracts/psl34.html) | abstract read; unassessed | Author abstract describes RWPRI/IP2 classification and constructions for PSL(3,4). |
| 2003 / L101 | [The residually weakly primitive geometries of M_22](https://www.math.auckland.ac.nz/~dleemans/abstracts/m22.html) | abstract read; component rederived | Correct author abstract is M22 classification. Earlier catalogue_L101.pdf is a wrong J2 paper and must not count. Remaining: Original two-page article body and supplement conventions remain unavailable; no claim to reproduce every construction or diagram. Catalogue completeness is retained; no whole-paper or novelty claim. |
| 2003 / L102 | [RWPRI and (2T)_1 flag-transitive linear spaces](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.44/no.1/b44h1bue.pdf) | selected sections read; proposed new result | Entire extracted text searched; introduction and section5.1.2 question context read. Asks whether all flag-transitive RWPRI spaces of spread type are Desarguesian. Context is the one-dimensional affine semilinear case G≤AΓL(1,p^d); do not generalize the question to all spread spaces. Current resolution status unverified. Later reading: Definitions 2.2, Proposition 5.2, Sections 5.1-5.3, and Theorem 6.1 read; not merely a keyword search. Remaining: External review and priority verification. This identifies the spaces in the narrow source case, not every possible acting subgroup, all flag-transitive spread spaces, or the other principal classification cases. |
| 2003 / N004 | [Truncations of inductively minimal geometries](https://doi.org/10.1016/S0012-365X(02)00603-9) | abstract read; component rederived | Intake only; independent model theorem has separate proof and checker. Abstract and primary metadata only; full text not obtained.  Remaining: The all-parameter model theorem is proved and internally reviewed; original full text remains unavailable. No whole-paper equivalence, abstract isomorphism classification or novelty claim. |
| 2004 / L093 | [Constructions of rank five geometries for the Mathieu group M_22](https://www.math.auckland.ac.nz/~dleemans/abstracts/m22rk5.html) | abstract read; unassessed | Author abstract describes nine rank-five geometries for M22. |
| 2004 / L094 | [The residually weakly primitive geometries of PSL(3,q) with q < 8](https://link.springer.com/article/10.1007/s00010-003-2695-5) | abstract read; unassessed | Publisher abstract announces RWPRI/(2T)1 geometries of PSL(3,q), q<8. |
| 2004 / L095 | [Quotients of a universal locally projective polytope of type {5,3,5}](https://arxiv.org/pdf/math/0307075v1) | full text search only; unassessed | PDF identity checked against title. Entire extracted text searched for conjectures, problems, questions, unknown cases and future work; no claim to have read every proof. |
| 2004 / L096 | [An algorithmic analysis of the intersection property](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/2108DB59271CED59B950340F28252A28/S1461157000001133a.pdf/div-class-title-an-algorithmic-analysis-of-the-intersection-property-div.pdf) | selected sections read; generic encoding | PDF identity checked against title. Entire extracted text searched for conjectures, problems, questions, unknown cases and future work; no claim to have read every proof. Later reading: Sections 2-3 and Figure 1 proof/pruning observations read; sporadic tables in Sections 4-5 not recomputed. Remaining: The original Magma implementation and sporadic classification tables are not rerun. No performance claim or whole-paper reproduction is made. |
| 2004 / L097 | [The residually weakly primitive geometries of J_3](https://www.math.auckland.ac.nz/~dleemans/abstracts/j3.html) | abstract read; unassessed | Correct author abstract is J3 classification. Earlier catalogue_L097.pdf is a wrong J2 paper and must not count. |
| 2004 / L098 | [The residually weakly primitive geometries of M_23](https://www.math.auckland.ac.nz/~dleemans/abstracts/m23.html) | abstract read; component rederived | Correct author abstract is M23 classification. Earlier catalogue_L098.pdf is a wrong J2 paper and must not count. Remaining: Original article body and supplement conventions remain unavailable; no claim to reproduce every construction or diagram. Catalogue completeness is retained; no whole-paper or novelty claim. |
| 2005 / L087 | [Two rank six geometries for the Higman-Sims sporadic group](https://www.sciencedirect.com/science/article/pii/S0012365X05000221) | abstract read; unassessed | Publisher abstract constructs two rank-six Higman–Sims geometries, each with five M22 rank-five residues. |
| 2005 / L088 | [On the thin regular geometries of rank four for the Janko group J(1)](https://msp.org/iig/2005/1-1/iig-v1-n1-p08-s.pdf) | full text search only; unassessed | PDF identity checked against title. Entire extracted text searched for conjectures, problems, questions, unknown cases and future work; no claim to have read every proof. |
| 2005 / L089 | [On inductively minimal geometries that satisfy the intersection property](https://leemans.dimitri.web.ulb.be/abstracts/imgip.html) | metadata and access only; component rederived | Author abstract link returned404. ULB deposited Elsevier_23581.pdf returned login HTML, not article PDF; metadata and access attempts only. Remaining: Full 2005 text unavailable; target is the primary abstract and exact earlier restatement. Foundational classification retained, no new-resolution claim. |
| 2005 / L090 | [A family of geometries related to the Suzuki tower](https://www.math.auckland.ac.nz/~dleemans/abstracts/suz.html) | abstract read; unassessed | Author abstract describes a five-geometry chain related to the Suzuki tower. |
| 2005 / L091 | [The residually weakly primitive geometries of HS](https://ajc.maths.uq.edu.au/pdf/33/ajc_v33_p231.pdf) | selected sections read; unassessed | OCR of all six pages searched, introductory and section-four problem contexts read. Mentions partially answering an older open problem via Hoffman–Singleton graph extensions; section-four natural question is answered in the paper. No new standalone unresolved conjecture identified. Later reading: Pages 231–233 visually read, including Table 1 and local-two-transitivity/truncation conventions; no HS census reproduction. |
| 2005 / L092 | [A generalization of a construction due to Van Nypelseer](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.46/no.2/b46h2lee.pdf) | selected sections read; proposed new result | Entire extracted text searched; constructions 1–3, Lemmas 1–3 and section4.6 read. Conjecture1 on p569: Γ(U_H(q)) is firm, residually connected and flag-transitive for all q>2. Source checks q≤16. Historical conjecture; present external resolution status not established. A new proof attempt is recorded separately. Later reading: Construction and conjecture were previously read in primary full text; existing full project proof re-read for this intake. Remaining: External review and priority verification. Other constructions and applications in the paper are not all rederived; Lean checks abstract connectivity only. |
| 2006 / L084 | Errata : "Quotients of a universal locally projective polytope of type {5,3,5}" | metadata and access only; unassessed | Erratum identity trap: old author abstract /535.html and arXiv math/0307075 point to the original paper, not this separate 2006 erratum. Erratum bibliographic identity is Math.Z.253,433–434; correct full text not obtained. Do not count original paper as erratum read. Remaining: Obtain the actual 2006 erratum, Math. Z. 253, 433-434; the original paper is not this source. |
| 2006 / L085 | [Almost simple groups of Suzuki type acting on polytopes](https://www.math.auckland.ac.nz/~dleemans/abstracts/szpoly.html) | abstract read; unassessed | Author abstract gives the Suzuki almost-simple string C-group classification: the group must be Suzuki and rank three. |
| 2006 / L086 | [An atlas of abstract regular polytopes for small groups](https://www.math.auckland.ac.nz/~dleemans/abstracts/atlaspoly.html) | abstract read; unassessed | Author abstract describes a computed atlas for small simple groups; no full-text conjecture audit possible. |

Earlier mistaken PDF identities for L097, L098, L101 and L123 are explicitly
rejected by the intake: those records remain at abstract depth. L125's original
J1 list must be read with the later correction reported by L105.

## Complete mathematical intake

All mathematical records are included, even where no exact target is assessed.
The JSON contains citations, primary links, verbatim access notes, methods, retained
inputs, evidence, remaining work and the earlier assessment for comparison.

| ID | Year | Work | Access | Mathematical stage |
|---|---:|---|---|---|
| L001 | 2008 | [Residually weakly primitive and locally two-transitive geometries for sporadic groups](http://www.academieroyale.be/cgi?usr=sky9b3xg5q&lg=fr&pag=774&tab=87&rec=47&frm=0&id=3843&flux=64191805) | metadata and access only | unassessed |
| L002 | 1999 | [An Atlas of Residually Weakly Primitive Geometries for Small Groups](https://leemans.dimitri.web.ulb.be/abstracts/atlas.html) | abstract read | unassessed |
| L003 | 2018 | [Hexagonal extensions of toroidal maps and hypermaps](https://ria.ua.pt/bitstream/10773/23862/1/2018DFW.pdf) | selected sections read | unassessed |
| L004 | 2014 | [Chiral polytopes and Suzuki simple groups](https://link.springer.com/content/pdf/10.1007/978-1-4939-0781-6_9.pdf) | abstract read | unassessed |
| L005 | 2003 | [Residually weakly primitive geometries of small sporadic and almost simple groups : a synthesis](https://leemans.dimitri.web.ulb.be/abstracts/synthese.html) | metadata and access only | unassessed |
| L006 | 2000 | [Incidence Geometry](https://leemans.dimitri.web.ulb.be/abstracts/incgeom.html) | abstract read | unassessed |
| L007 | unconfirmed | [Chiral polytopes of order 2p m](https://amc-journal.eu/index.php/amc/article/download/3716/2232) | selected sections read | proposed new result |
| L008 | 2026 | [Testing chirality on hypertopes](https://arxiv.org/pdf/2511.14562) | selected sections read | principal results rederived |
| L009 | 2026 | [Geometries with trialities arising from linear spaces](https://arxiv.org/pdf/2504.06025) | selected sections read | component rederived |
| L010 | 2026 | [Two gluing methods for string C-group representations of the symmetric groups](https://arxiv.org/pdf/2504.17535) | selected sections read | related only |
| L011 | 2026 | [On simple groups that admit a string C-group representation](https://dipot.ulb.ac.be/dspace/bitstream/2013/397490/3/simpleGroups6.pdf) | selected sections read | related only |
| L012 | 2025 | [Regular 3-polytopes of order 2 n p](https://arxiv.org/pdf/2001.02945) | selected sections read | component rederived |
| L013 | 2025 | [A note on girth-diameter cages](https://arxiv.org/pdf/2401.15539) | selected sections read | outside current core |
| L014 | 2025 | [String C-groups of order 4p m](https://arxiv.org/pdf/2407.10388) | full text search only | related only |
| L015 | 2025 | [Flag transitive geometries with trialities and no dualities coming from Suzuki groups](https://arxiv.org/pdf/2311.13522) | full text search only | related only |
| L016 | 2025 | [Faithful and thin non-polytopal maniplexes](https://arxiv.org/pdf/2305.01372) | selected sections read | related only |
| L017 | 2024 | [On trialities and their absolute geometries](https://dipot.ulb.ac.be/dspace/bitstream/2013/375808/3/revisionAbsolute.pdf) | full text search only | related only |
| L018 | 2024 | [There is no perfect Mondrian partition for squares of side lengths less than 1001](https://arxiv.org/pdf/2311.02385) | selected sections read | outside current core |
| L019 | 2024 | [The number of string C-groups of high rank](https://arxiv.org/pdf/2212.12723) | selected sections read | related only |
| L020 | 2024 | [A rank augmentation theorem for rank 3 string C-group representations of the symmetric groups](https://arxiv.org/pdf/2212.12563) | selected sections read | related only |
| L021 | 2023 | [Maniplexes with automorphism group PSL(2,q)](https://dipot.ulb.ac.be/dspace/bitstream/2013/359689/3/projectivemaniplexes_final.pdf) | selected sections read | related only |
| L022 | 2023 | [Preface to the Special Issue in Memoriam of Jacques Tits](https://msp.org/iig/2023/20-2/p01.xhtml) | full short text read | unassessed |
| L023 | 2023 | [Incidence geometries with trialities coming from maps with Wilson trialities](https://arxiv.org/pdf/2208.08215v2) | full text search only | related only |
| L024 | 2022 | [String C-groups with real Schur index 2](https://arxiv.org/pdf/2201.01313) | selected sections read | outside current core |
| L025 | 2022 | [Edge-girth-regular graphs arising from biaffine planes and Suzuki groups](https://arxiv.org/pdf/2108.06636v1) | selected sections read | proposed new result |
| L026 | 2022 | [The String C-group representations of the Suzuki, Rudvalis and O'Nan sporadic groups](https://adam-journal.eu/index.php/ADAM/article/download/1405/1405) | selected sections read | related only |
| L027 | 2022 | [On chiral polytopes having a group PSL(3,q) as automorphism group](https://dipot.ulb.ac.be/dspace/bitstream/2013/333283/3/psl3-final.pdf) | selected sections read | related only |
| L028 | 2021 | [A new algorithm to classify chiral polytopes with a given automorphism group](https://arxiv.org/pdf/1912.02287v1) | selected sections read | component rederived |
| L029 | 2021 | [On residual connectedness in chiral geometries](https://arxiv.org/pdf/1911.03227v1) | selected sections read | component rederived |
| L030 | 2021 | [An infinite family of locally X graphs based on incidence geometries](https://arxiv.org/pdf/1811.11438v1) | selected sections read | principal results rederived |
| L031 | 2020 | [Orthogonal groups in characteristic 2 acting on polytopes of high rank](https://arxiv.org/pdf/1709.02219) | selected sections read | conditional component |
| L032 | 2020 | [On regular polytopes of 2-power order](https://dipot.ulb.ac.be/dspace/bitstream/2013/292444/3/HRRPR-revised.pdf) | selected sections read | principal results rederived |
| L033 | 2020 | [An exploration of locally spherical regular hypertopes](https://dipot.ulb.ac.be/dspace/bitstream/2013/309163/3/LSRH-revised.pdf) | selected sections read | unassessed |
| L034 | 2019 | [Existence of regular 3-hypertopes with 2 n chambers](https://dipot.ulb.ac.be/dspace/bitstream/2013/287227/5/Hy2g.pdf) | selected sections read | component rederived |
| L035 | 2019 | [2-groups behaving as automorphism groups of regular 3-polytopes](https://arxiv.org/pdf/1802.08947v2) | selected sections read | principal results rederived |
| L036 | 2019 | [On primitive geometries of rank two](https://adam-journal.eu/index.php/ADAM/article/download/1301/1075) | full text search only | unassessed |
| L037 | 2019 | [Rank reduction of string C-group representations](https://arxiv.org/pdf/1812.01055) | full short text read | source theorem retained |
| L038 | 2019 | [String C-group representations of alternating groups](https://arxiv.org/pdf/1810.12450) | selected sections read | conditional component |
| L039 | 2018 | [Groups of Ree type in characteristic 3 acting on polytopes](https://arxiv.org/pdf/1501.01125) | selected sections read | related only |
| L040 | 2018 | [C-groups of high rank for the symmetric groups](https://arxiv.org/pdf/1510.08990v1) | full text search only | unassessed |
| L041 | 2018 | [Hypertopes with tetrahedral diagram](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v25i3p22/pdf/) | full text search only | unassessed |
| L042 | 2018 | [An extension of the classification of high rank regular polytopes](https://arxiv.org/pdf/1509.01032v1) | full text search only | unassessed |
| L043 | 2017 | [Projective linear groups as automorphism groups of chiral polytopes](https://arxiv.org/pdf/1606.08017) | selected sections read | proposed new result |
| L044 | 2017 | [Highest rank of a polytope for A n](https://arxiv.org/pdf/1605.09173v1) | selected sections read | related only |
| L045 | 2017 | [Chiral polyhedra and finite simple groups](https://arxiv.org/pdf/1603.07713v3) | full text search only | unassessed |
| L046 | 2016 | [Algorithmic enumeration of regular maps](https://amc-journal.eu/index.php/amc/article/download/544/857) | selected sections read | unassessed |
| L047 | 2016 | [String C-groups as transitive subgroups of Sym(n)](https://arxiv.org/pdf/1410.5863v1) | selected sections read | unassessed |
| L048 | 2016 | [Polytopes of large rank for PSL(4,q)](https://digitalcommons.bucknell.edu/fac_journ/1204/) | abstract read | partial progress |
| L049 | 2016 | Two-transitive pairs in PSL(2,q) | metadata and access only | unassessed |
| L050 | 2016 | [Linear codes with complementary duals from some strongly regular subgraphs of the McLaughlin graph](https://www.mathos.unios.hr/mc/index.php/mc/article/download/1537/388) | selected sections read | component rederived |
| L051 | 2016 | [Chiral polyhedra arising from almost simple groups with socle PSL(2,q)](https://link.springer.com/article/10.1007/s10801-016-0669-7) | abstract read | unassessed |
| L052 | 2016 | [Highly symmetric hypertopes](https://ria.ua.pt/bitstream/10773/16681/1/2016DFW.pdf) | selected sections read | proposed new result |
| L053 | 2015 | [Almost simple groups with socle PSL(2,q) acting on abstract regular polytopes](https://dipot.ulb.ac.be/dspace/bitstream/2013/187644/1/Elsevier_171271.pdf) | abstract read | unassessed |
| L054 | 2015 | [An Atlas of subgroup lattices of finite almost simple groups](https://arxiv.org/pdf/1306.4820v2) | full text search only | unassessed |
| L055 | 2015 | [C-groups of PSL(2,q) and PGL(2,q)](https://dipot.ulb.ac.be/dspace/bitstream/2013/195928/1/Elsevier_179555.pdf) | abstract read | unassessed |
| L056 | 2015 | [Chiral polyhedra and projective lines](https://www.matem.unam.mx/~eugenia/papers/pslChiral.pdf) | selected sections read | unassessed |
| L057 | 2015 | [C-groups of Suzuki type](https://link.springer.com/content/pdf/10.1007/s10801-015-0605-2.pdf) | abstract read | unassessed |
| L058 | 2014 | [Abstract regular polytopes for the O'Nan group](https://dipot.ulb.ac.be/dspace/handle/2013/172544) | metadata and access only | unassessed |
| L059 | 2014 | [Core-free, rank two coset geometries from edge-transitive bipartite graphs](https://arxiv.org/pdf/1106.5704v2) | selected sections read | unassessed |
| L060 | 2013 | [Locally 2-arc-transitive complete bipartite graphs](https://dipot.ulb.ac.be/dspace/handle/2013/219392) | abstract read | unassessed |
| L061 | 2013 | [Binary codes of some strongly regular graphs of the McLaughlin graph](https://link.springer.com/content/pdf/10.1007/s10623-011-9589-7.pdf) | abstract read | unassessed |
| L062 | 2013 | [Corrigendum to "Polytopes of high rank for the symmetric groups"](https://www.sciencedirect.com/science/article/pii/S0001870812003805) | abstract read | unassessed |
| L063 | 2013 | [The rank two geometries of the PSL(2,q) groups : part II](https://amc-journal.eu/index.php/amc/article/download/181/241) | selected sections read | component rederived |
| L064 | 2013 | [The rank two geometries of the PSL(2,q) groups : part II, Appendix](https://amc-journal.eu/index.php/amc/article/download/181/1862) | full text search only | unassessed |
| L065 | 2013 | [A new algorithm to find apartments in coset geometries](https://leemans.dimitri.web.ulb.be/abstracts/apart2.html) | abstract read | unassessed |
| L066 | 2013 | [On pairs of commuting involutions in Sym(n) and Alt(n)](https://math.uni.lu/kiefer/Publications/Involutions.pdf) | selected sections read | principal results rederived |
| L067 | 2012 | [Polytopes of high rank for the alternating groups](https://dipot.ulb.ac.be/dspace/handle/2013/133342) | metadata and access only | unassessed |
| L068 | 2012 | [Regular 4-polytopes from the Livingstone graph of Janko's first group](https://link.springer.com/content/pdf/10.1007/s10801-011-0300-x.pdf) | full text search only | unassessed |
| L069 | 2012 | [All alternating groups A n with n ≥ 12 have polytopes of rank ⌊ (n-1)/2 ⌋](https://epubs.siam.org/doi/10.1137/110838467) | abstract read | unassessed |
| L070 | 2012 | [Two atlases of abstract chiral polytopes for small groups](https://amc-journal.eu/index.php/amc/article/download/204/192) | full text search only | unassessed |
| L071 | 2012 | [Algorithms for classifying regular polytopes with a fixed automorphism group](https://cdm.ucalgary.ca/article/download/62152/46746) | selected sections read | unassessed |
| L072 | 2011 | [Polytopes of high rank for the symmetric groups](https://dipot.ulb.ac.be/dspace/bitstream/2013/133343/1/Elsevier_115702.pdf) | abstract read | unassessed |
| L073 | 2010 | [Rank three residually connected geometries  for M_{22}, revisited](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v17i1n4/pdf) | full text search only | unassessed |
| L074 | 2010 | [On the number of abstract regular polytopes whose automorphism group is a Suzuki simple group Sz(q)](https://math.uni.lu/kiefer/Publications/szpoly3%20r%C3%A9vis%C3%A9.pdf) | full text search only | outside current core |
| L075 | 2010 | [On the geometry of O'N](https://www.math.auckland.ac.nz/~dleemans/abstracts/onan.html) | abstract read | unassessed |
| L076 | 2010 | [On the rank two geometries of the PSL(2,q) groups : part I](https://amc-journal.eu/index.php/amc/article/download/107/114) | full text search only | unassessed |
| L077 | 2009 | [On locally spherical polytopes of type {5,3,5}](https://doi.org/10.1016/j.disc.2007.12.084) | abstract read | unassessed |
| L078 | 2009 | [Locally s-arc-transitive graphs related to sporadic simple groups](https://www.math.auckland.ac.nz/~dleemans/abstracts/lsarc.html) | abstract read | unassessed |
| L079 | 2009 | [Polytopes with groups of type PGL(2,q)](https://arxiv.org/pdf/0909.1991v1) | selected sections read | unassessed |
| L080 | 2009 | On apartments in incidence geometry | metadata and access only | unassessed |
| L081 | 2008 | [A new Petrie-like construction for abstract polytopes](https://www.math.auckland.ac.nz/~dleemans/abstracts/newpetrie.html) | abstract read | unassessed |
| L082 | 2007 | [A rank six geometry related to the McLaughlin sporadic simple group](https://link.springer.com/article/10.1007/s10623-007-9082-5) | abstract read | unassessed |
| L083 | 2007 | [Groups of type L(2,q) acting on polytopes](https://arxiv.org/pdf/math/0606660v1) | full text search only | unassessed |
| L084 | 2006 | Errata : "Quotients of a universal locally projective polytope of type {5,3,5}" | metadata and access only | unassessed |
| L085 | 2006 | [Almost simple groups of Suzuki type acting on polytopes](https://www.math.auckland.ac.nz/~dleemans/abstracts/szpoly.html) | abstract read | unassessed |
| L086 | 2006 | [An atlas of abstract regular polytopes for small groups](https://www.math.auckland.ac.nz/~dleemans/abstracts/atlaspoly.html) | abstract read | unassessed |
| L087 | 2005 | [Two rank six geometries for the Higman-Sims sporadic group](https://www.sciencedirect.com/science/article/pii/S0012365X05000221) | abstract read | unassessed |
| L088 | 2005 | [On the thin regular geometries of rank four for the Janko group J(1)](https://msp.org/iig/2005/1-1/iig-v1-n1-p08-s.pdf) | full text search only | unassessed |
| L089 | 2005 | [On inductively minimal geometries that satisfy the intersection property](https://leemans.dimitri.web.ulb.be/abstracts/imgip.html) | metadata and access only | component rederived |
| L090 | 2005 | [A family of geometries related to the Suzuki tower](https://www.math.auckland.ac.nz/~dleemans/abstracts/suz.html) | abstract read | unassessed |
| L091 | 2005 | [The residually weakly primitive geometries of HS](https://ajc.maths.uq.edu.au/pdf/33/ajc_v33_p231.pdf) | selected sections read | unassessed |
| L092 | 2005 | [A generalization of a construction due to Van Nypelseer](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.46/no.2/b46h2lee.pdf) | selected sections read | proposed new result |
| L093 | 2004 | [Constructions of rank five geometries for the Mathieu group M_22](https://www.math.auckland.ac.nz/~dleemans/abstracts/m22rk5.html) | abstract read | unassessed |
| L094 | 2004 | [The residually weakly primitive geometries of PSL(3,q) with q < 8](https://link.springer.com/article/10.1007/s00010-003-2695-5) | abstract read | unassessed |
| L095 | 2004 | [Quotients of a universal locally projective polytope of type {5,3,5}](https://arxiv.org/pdf/math/0307075v1) | full text search only | unassessed |
| L096 | 2004 | [An algorithmic analysis of the intersection property](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/2108DB59271CED59B950340F28252A28/S1461157000001133a.pdf/div-class-title-an-algorithmic-analysis-of-the-intersection-property-div.pdf) | selected sections read | generic encoding |
| L097 | 2004 | [The residually weakly primitive geometries of J_3](https://www.math.auckland.ac.nz/~dleemans/abstracts/j3.html) | abstract read | unassessed |
| L098 | 2004 | [The residually weakly primitive geometries of M_23](https://www.math.auckland.ac.nz/~dleemans/abstracts/m23.html) | abstract read | component rederived |
| L099 | 2003 | [On a rank four geometry for the Hall-Janko sporadic group](https://www.sciencedirect.com/science/article/pii/S0097316502000225) | abstract read | unassessed |
| L100 | 2003 | [Geometries for the group PSL(3,4)](https://www.math.auckland.ac.nz/~dleemans/abstracts/psl34.html) | abstract read | unassessed |
| L101 | 2003 | [The residually weakly primitive geometries of M_22](https://www.math.auckland.ac.nz/~dleemans/abstracts/m22.html) | abstract read | component rederived |
| L102 | 2003 | [RWPRI and (2T)_1 flag-transitive linear spaces](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.44/no.1/b44h1bue.pdf) | selected sections read | proposed new result |
| L103 | 2002 | [The RWPRI geometries of Sym(5) x 2](https://www.math.auckland.ac.nz/~dleemans/abstracts/s5x2.html) | abstract read | unassessed |
| L104 | 2002 | [The residually weakly primitive geometries of J_2](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v21n1p77/585) | full short text read | principal results rederived |
| L105 | 2002 | [Constructing coset geometries with Magma : An application to the sporadic groups M(12) and J(1)](https://www.math.auckland.ac.nz/~dleemans/abstracts/algo.html) | abstract read | component rederived |
| L106 | 2001 | [On a rank five geometry of Meixner for the Mathieu group M(12)](https://www.math.auckland.ac.nz/~dleemans/abstracts/m12b.html) | abstract read | unassessed |
| L107 | 2001 | [Some rank five geometries related to the Mathieu group M(23)](https://www.math.auckland.ac.nz/~dleemans/abstracts/m23rk5.html) | abstract read | unassessed |
| L108 | 2001 | [On the Petrials of thin regular rank three geometries](https://www.math.auckland.ac.nz/~dleemans/abstracts/petrie.html) | abstract read | unassessed |
| L109 | 2000 | [The residually weakly primitive geometries of the Dihedral Groups](https://www.math.auckland.ac.nz/~dleemans/abstracts/d2n.html) | abstract read | component rederived |
| L110 | 2000 | [The residually weakly primitive pre-geometries of the Suzuki simple groups](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v20n1p1/995) | selected sections read | partial progress |
| L111 | 2000 | [New geometries for finite groups and polytopes](https://www.math.auckland.ac.nz/~dleemans/abstracts/ngeo.html) | abstract read | unassessed |
| L112 | 1999 | [On a geometry of Ivanov and Shpectorov for the O'Nan sporadic simple group](https://www.math.auckland.ac.nz/~dleemans/abstracts/on.html) | abstract read | unassessed |
| L113 | 1999 | [An Atlas of regular thin geometries for small groups](https://www.math.auckland.ac.nz/~dleemans/abstracts/atlasthin.html) | abstract read | unassessed |
| L114 | 1999 | [The rank 3 geometries of the simple Suzuki groups Sz(q)](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v19n1p43/837) | selected sections read | proposed new result |
| L115 | 1998 | [The Rank 2 Geometries of the Simple Suzuki Groups Sz(q)](https://emis.de/ft/11479) | selected sections read | finite subfamily reproduced |
| L116 | 1998 | [Thin geometries for the Suzuki simple group Sz(8)](https://www.math.auckland.ac.nz/~dleemans/abstracts/sz8thin.html) | abstract read | unassessed |
| L117 | 1997 | [Two Nearly Isomorphic Groups](https://www.math.auckland.ac.nz/~dleemans/abstracts/twoiso.html) | abstract read | unassessed |
| L118 | 1996 | [On the List of Finite Primitive Permutation Groups of Degree Less Than 50](https://www.math.auckland.ac.nz/~dleemans/abstracts/primlist.html) | abstract read | unassessed |
| L119 | 1996 | [All Geometries of the Mathieu Group M(11) Based on Maximal Subgroups](https://www.math.auckland.ac.nz/~dleemans/abstracts/m11.html) | abstract read | unassessed |
| L120 | 2021 | [String C-group representations of almost simple groups: a survey](https://arxiv.org/pdf/1910.08843) | selected sections read | unassessed |
| L121 | 2021 | [Two families of locally toroidal regular 4-hypertopes arising from toroids](https://dipot.ulb.ac.be/dspace/bitstream/2013/301629/3/FLPWrev.pdf) | full text search only | unassessed |
| L122 | 2019 | [Coset geometries with trialities and their reduced incidence graphs](https://www.iam.fmph.uniba.sk/amuc/ojs/index.php/amuc/article/download/1309/743) | full text search only | unassessed |
| L123 | 1997 | [The residually weakly primitive geometries of the Suzuki simple group Sz(8)](https://www.math.auckland.ac.nz/~dleemans/abstracts/sz8.html) | abstract read | unassessed |
| L124 | 1998 | [On Flag-Transitive Incidence Geometries of Rank 6 for the Mathieu Group M(12)](https://www.math.auckland.ac.nz/~dleemans/abstracts/m12.html) | abstract read | component rederived |
| L125 | 1998 | [The Residually Weakly Primitive Geometries of the Janko Group J(1)](https://www.math.auckland.ac.nz/~dleemans/abstracts/j1.html) | abstract read | component rederived |
| L126 | unconfirmed | [Groups represented by incidence geometries](https://arxiv.org/pdf/2506.10464) | selected sections read | unassessed |
| L127 | unconfirmed | Tight chiral polyhedra of order 2p m | metadata and access only | unassessed |
| L128 | unconfirmed | [Hypertopes with prescribed diagram symmetries](https://arxiv.org/pdf/2610.09711) | selected sections read | unassessed |
| F001 | 2021 | [On the ranks of string C-group representations for symplectic and orthogonal groups](https://arxiv.org/pdf/1912.05512) | selected sections read | unassessed |
| F002 | 2025 | [String C-group representations of transitive groups: a case study with degree 11](https://arxiv.org/pdf/2302.11943) | selected sections read | unassessed |
| F003 | 2021 | [On the rank of Suzuki polytopes: an answer to Hubard and Leemans](https://arxiv.org/pdf/2010.04080) | full short text read | unassessed |
| F004 | 2026 | [Abstract regular polytopes of G2(q) in even characteristic](https://arxiv.org/pdf/2609.25004) | selected sections read | unassessed |
| F005 | 2025 | [Polytopality criteria for the mix of polytopes and maniplexes](https://arxiv.org/pdf/2506.19334) | selected sections read | unassessed |
| F006 | 2025 | [Abstract Regular Polytopes of Finite Irreducible Coxeter Groups](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v32i4p18/pdf/) | selected sections read | unassessed |
| F007 | 2026 | [Faithfulness in maniplexes](https://dirros.openscience.si/Dokument.php?id=49623&lang=eng) | selected sections read | unassessed |
| F008 | 2026 | [On solutions to the Mondrian Puzzle](https://tenenb.perso.math.cnrs.fr/PPP/Mondrian.pdf) | selected sections read | unassessed |
| F009 | 2026 | [On the order-diameter ratio of girth-diameter cages](https://arxiv.org/pdf/2511.21144) | selected sections read | unassessed |
| F010 | 2025 | [Every finite group is represented by a finite incidence geometry](https://arxiv.org/pdf/2511.02410) | selected sections read | unassessed |
| F011 | 2024 | [Explicit constructions of Diophantine tuples over finite fields](https://link.springer.com/content/pdf/10.1007/s11139-024-00888-5.pdf) | selected sections read | unassessed |
| F012 | 2025 | [Exhaustive generation of edge-girth-regular graphs](https://arxiv.org/pdf/2401.08271) | selected sections read | unassessed |
| F013 | 2026 | [String C-groups of 2-power order project onto a common string C-group](https://arxiv.org/pdf/2605.20691) | selected sections read | unassessed |
| F014 | 2025 | [Regular 3-polytopes of type {n,n}](https://arxiv.org/pdf/2505.09505) | selected sections read | unassessed |
| F015 | 2023 | [Infinite Families of Hypertopes from Centrally Symmetric Polytopes](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v30i2p20/pdf/) | selected sections read | unassessed |
| F016 | 2025 | [Symmetric polytopes whose automorphism groups are 2-groups](https://arxiv.org/pdf/2512.15511) | selected sections read | unassessed |
| F017 | 2018 | [LCD codes from adjacency matrices of graphs](https://www.math.clemson.edu/~keyj/Key/LCD_KeyRod.pdf) | selected sections read | unassessed |
| N001 | 1998 | [Some properties of inductively minimal geometries](https://doi.org/10.36045/bbms/1103409005) | selected sections read | principal results rederived |
| N002 | 2001 | [On the number of inductively minimal geometries](https://doi.org/10.1016/S0304-3975(00)00228-0) | abstract read | component rederived |
| N003 | 2002 | [Independent generating sets and geometries for symmetric groups](https://maths.qmul.ac.uk/~pjc/preprints/igsgsn.pdf) | full text read | component rederived |
| N004 | 2003 | [Truncations of inductively minimal geometries](https://doi.org/10.1016/S0012-365X(02)00603-9) | abstract read | component rederived |
| N005 | 2025 | [From Group Operations to Geometric Structures: Amalgamations, HNN-Extensions, and Twisting in Coset Geometries](https://arxiv.org/abs/2505.24662) | selected sections read | related only |
| N006 | 2026 | [The geometry of wreath and semi-direct products](https://arxiv.org/abs/2605.04646v2) | abstract read | unassessed |
| N007 | 2026 | [Coset geometries acting on their elements: The j-diagonals twisting](https://arxiv.org/abs/2608.23223v1) | abstract read | unassessed |

## Updating the map

Record source identity and access first. Promote a target only with an exact
statement, replacement derivation and explicit retained inputs. New conjecture
proofs do not count as rederivations of all published principal results. Generic
encodings do not count as reproductions of classification tables.

The builder reads historical inputs without changing them. Its explicit target
updates and input hashes make promotions reviewable. Run:

```sh
python3 scripts/build_paper_registry.py
```

This rebuilds metadata and documentation; it does not rerun proofs, refresh
the literature search or certify the publication snapshot.
See [REPRODUCING.md](REPRODUCING.md) for the separate checks.
