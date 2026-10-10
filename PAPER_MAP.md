# Paper registry: sources read and results recovered

**161 mathematical works** are indexed: 128 catalogue entries, 17 followups and 16 network additions. **48 entries date from 1996–2006.**
The registry includes books, proceedings papers and errata as well as journal articles.
It records what was obtained, how much was read and which results have been assessed.
It is neither a record of complete proof reading nor an exhaustive bibliography of
every collaborator, student or postdoc. Coauthorship alone does not establish those relationships.

The [current programme](MANUSCRIPT_PROGRAM.md) organizes the new papers by topic,
with a full umbrella for each topic and complete applications to historical papers.
Its A–F tables name the results already available for reworking. The counts below
describe the source records; they do not count completed new application papers
or measure compression.

The [frozen registry](research/case_study/paper_registry.json) contains the detailed
earlier records. The reviewed additions below update the displayed view without
rewriting those records. The [previous paper map](archive/PAPER_MAP.previous.md)
preserves the longer historical assessments, earlier compilation summaries and
their measurements. See the [archive](archive/README.md) for those editions.

## Reading and mathematical progress

| Stage | Meaning |
|---|---|
| Retrieved | A primary full text was obtained and matched to the source. |
| Read | The record distinguishes an abstract, a text search, selected sections and a complete reading. |
| Encoded | A specified result has an explicit representation or test. |
| Rederived | A named theorem, part of a theorem or finite subfamily has a replacement proof, with earlier results used by that proof stated. |
| Main results recovered | The specified main results are recovered; this need not include every auxiliary assertion or imported classification. |
| Proposed answer or new result | An internally checked argument is recorded; external review and verification of historical priority remain. |
| Not assessed | No replacement proof has been assessed. This does not imply that the result is unknown or that any question remains open. |

These categories describe different aspects of the work and overlap. Obtaining a
paper does not establish a replacement proof. Progress on a question quoted in a
survey does not imply that its original source has been read.

| Access category | Works |
|---|---:|
| abstract read | 49 |
| full short text read | 4 |
| full text read | 24 |
| full text search only | 15 |
| metadata and access only | 9 |
| selected sections read | 60 |

**102** works have a retrieved full text; **61** have an explicit representation or a specified conditional or partial derivation; **48** have a recovered result, finite subfamily or stated main result.

The set with **stated main results recovered contains 26 works: L008, L012, L014, L021, L030, L032, L034, L035, L066, L074, L079, L083, L088, L092, L104, L108, F010, F013, F014, F016, N001, N003, N008, N009, N013, N016**.
The exact targets and qualifications govern membership in this set. Proposed
conjecture proofs do not add to it. The [question catalogue](CONJECTURE_RESULTS.md)
keeps answers to questions separate from recovery of published results.

## Reviewed additions to the frozen registry

These additions supply the current counts and the revised entries below. Their
files preserve the exact statements, earlier results used, evidence and remaining work.

| Sources | Results and qualifications | Record |
|---|---|---|
| L073 and L104 | L073: 81 rank-two and 431 rank-three classes, witnesses and geometric shadows; refined correspondence with the printed table remains incomplete. L104: the fixed 8/19/3 census in ranks 2/3/4 and exclusion of higher ranks; further diagrams, full geometric automorphism and correlation groups, and the doubling assertion remain outside the recovered results. | [Reviewed census addition](research/case_study/phase181_registry_overlay.json) |
| L092 | Corrected rank-three applications, complete higher-rank Steiner classification and rank-six M24 construction. The two quoted classifications remain external inputs; partial linearity in Theorem 1 and missing Pasini named-residue maps remain explicit. Lean verifies specified finite incidences and counterexamples. The existing Hermitian-unital answer is counted separately, once. | [Earlier corrections](research/case_study/phase185_L092_overlay.json); [main-result admission](research/case_study/phase208_L092_overlay.json); [proof reader](DESIGN_RESIDUES.md) |
| L068 | Complete primary text read; construction P recovered as printed and Q recovered after an explicit repair. This adds a partial derivation, with the necessary group and graph inputs stated. | [Construction review](research/case_study/phase189_L068_overlay.json); [proof reader](GRAPH_INCIDENCE.md) |
| F010 | The main constructive theorems are recovered in a complete written argument, with local corrections. Lean verifies the stated hexagon component, not the universal constructions. | [Reviewed addition](research/case_study/phase193_F010_overlay.json); [proof reader](FINITE_INCIDENCE_REPRESENTATIONS.md) |
| F014 | All stated positive rank-three main results in arXiv v1: exact construction, matrices, universal presentation and both corollaries. Montero–Ivić Weiss supply the earlier polygon construction; the printed inverse-action convention is corrected. The higher-rank counterexample is a separate result. | [Reviewed addition](research/case_study/phase233_F014_overlay.json); [complete application](EQUAL_LABEL_POLYGONS.md) |
| L079 and L083 | Both complete specified rank-at-least-four PGL₂/PSL₂ classifications, their rank restrictions, universal table and stated geometric properties. L079’s extra seventeen-case census and Conjecture 11 are excluded. | [Reviewed addition](research/case_study/phase235_projective_line_overlay.json); [common proof](PROJECTIVE_LINE_POLYTOPES.md) |
| L014 | Complete normal-Sylow structure, abelian/tight classification and all-parameter nonabelian construction, with the exact presentation and corrected v1 marking. The tightness converse retains Cunningham–Pellicer. | [Reviewed addition](research/case_study/phase249_L014_overlay.json); [complete application](ODD_KERNEL_POLYHEDRA.md) |
| L012 | Complete declared mixed-prime type restriction, odd-factor presentation, exact existence range and all six affine families. Corrected period sign; Burnside, Lucchini, the order-384 catalogue and earlier umbrella/cubic proofs remain inputs. General classification, full Table 1 and ancillary seed uniqueness are excluded. | [Reviewed addition](research/case_study/phase259_L012_overlay.json); [complete application and affine theory](MIXED_PRIME_POLYHEDRA.md) |
| L021 | Complete corrected principal PSL rank/end-group restrictions, two-proper-end classification, torus extension theorem and both source families. Natural-subfield qualifications, omitted S₄ ends and self-duality corrections are explicit. The four-family PGL question is counted separately, once; no full marking census or full Lean theorem is claimed. | [Principal admission](research/case_study/phase264_L021_principal_overlay.json); [PSL proof and review](PROJECTIVE_LINE_MANIPLEXES.md); [separate question admission](research/case_study/phase262_L021_question_overlay.json); [PGL answer](PGL_MANIPLEX_FAMILIES.md) |

Earlier mistaken PDF identifications for L097, L098, L101 and L123 remain
explicitly rejected; those entries have only abstract-level access. L125's
original J1 list must be read with the later correction reported by L105.

## Complete registry

All 161 records appear below, including papers for which no exact result has
been assessed. Each result label is limited by its detailed statement and
remaining-work record in the frozen JSON or the reviewed additions above.

| ID | Year | Work | Reading | Mathematical progress |
|---|---:|---|---|---|
| L001 | 2008 | [Residually weakly primitive and locally two-transitive geometries for sporadic groups](http://www.academieroyale.be/cgi?usr=sky9b3xg5q&lg=fr&pag=774&tab=87&rec=47&frm=0&id=3843&flux=64191805) | metadata and access only | not assessed |
| L002 | 1999 | [An Atlas of Residually Weakly Primitive Geometries for Small Groups](https://leemans.dimitri.web.ulb.be/abstracts/atlas.html) | abstract read | not assessed |
| L003 | 2018 | [Hexagonal extensions of toroidal maps and hypermaps](https://ria.ua.pt/bitstream/10773/23862/1/2018DFW.pdf) | selected sections read | partial progress |
| L004 | 2014 | [Chiral polytopes and Suzuki simple groups](https://link.springer.com/content/pdf/10.1007/978-1-4939-0781-6_9.pdf) | abstract read | not assessed |
| L005 | 2003 | [Residually weakly primitive geometries of small sporadic and almost simple groups : a synthesis](https://leemans.dimitri.web.ulb.be/abstracts/synthese.html) | metadata and access only | not assessed |
| L006 | 2000 | [Incidence Geometry](https://leemans.dimitri.web.ulb.be/abstracts/incgeom.html) | abstract read | not assessed |
| L007 | unconfirmed | [Chiral polytopes of order 2p m](https://amc-journal.eu/index.php/amc/article/download/3716/2232) | selected sections read | proposed answer or new result |
| L008 | 2026 | [Testing chirality on hypertopes](https://arxiv.org/pdf/2511.14562) | selected sections read | stated main results recovered |
| L009 | 2026 | [Geometries with trialities arising from linear spaces](https://arxiv.org/pdf/2504.06025) | selected sections read | part of the results recovered |
| L010 | 2026 | [Two gluing methods for string C-group representations of the symmetric groups](https://arxiv.org/pdf/2504.17535) | selected sections read | related work only |
| L011 | 2026 | [On simple groups that admit a string C-group representation](https://dipot.ulb.ac.be/dspace/bitstream/2013/397490/3/simpleGroups6.pdf) | selected sections read | related work only |
| L012 | 2025 | [Regular 3-polytopes of order 2 n p](https://arxiv.org/pdf/2001.02945) | full text read | [stated main results recovered](research/case_study/phase259_L012_overlay.json) |
| L013 | 2025 | [A note on girth-diameter cages](https://arxiv.org/pdf/2401.15539) | selected sections read | outside the present study |
| L014 | 2025 | [String C-groups of order 4p m](https://arxiv.org/pdf/2407.10388) | full text read | [stated main results recovered](research/case_study/phase249_L014_overlay.json) |
| L015 | 2025 | [Flag transitive geometries with trialities and no dualities coming from Suzuki groups](https://arxiv.org/pdf/2311.13522) | full text search only | related work only |
| L016 | 2025 | [Faithful and thin non-polytopal maniplexes](https://arxiv.org/pdf/2305.01372) | selected sections read | related work only |
| L017 | 2024 | [On trialities and their absolute geometries](https://dipot.ulb.ac.be/dspace/bitstream/2013/375808/3/revisionAbsolute.pdf) | full text search only | related work only |
| L018 | 2024 | [There is no perfect Mondrian partition for squares of side lengths less than 1001](https://arxiv.org/pdf/2311.02385) | selected sections read | outside the present study |
| L019 | 2024 | [The number of string C-groups of high rank](https://arxiv.org/pdf/2212.12723) | selected sections read | related work only |
| L020 | 2024 | [A rank augmentation theorem for rank 3 string C-group representations of the symmetric groups](https://arxiv.org/pdf/2212.12563) | selected sections read | related work only |
| L021 | 2023 | [Maniplexes with automorphism group PSL(2,q)](https://dipot.ulb.ac.be/dspace/bitstream/2013/359689/3/projectivemaniplexes_final.pdf) | full text read | [stated main results recovered](research/case_study/phase264_L021_principal_overlay.json) |
| L022 | 2023 | [Preface to the Special Issue in Memoriam of Jacques Tits](https://msp.org/iig/2023/20-2/p01.xhtml) | full short text read | not assessed |
| L023 | 2023 | [Incidence geometries with trialities coming from maps with Wilson trialities](https://arxiv.org/pdf/2208.08215v2) | full text search only | related work only |
| L024 | 2022 | [String C-groups with real Schur index 2](https://arxiv.org/pdf/2201.01313) | selected sections read | outside the present study |
| L025 | 2022 | [Edge-girth-regular graphs arising from biaffine planes and Suzuki groups](https://arxiv.org/pdf/2108.06636v1) | selected sections read | proposed answer or new result |
| L026 | 2022 | [The String C-group representations of the Suzuki, Rudvalis and O'Nan sporadic groups](https://adam-journal.eu/index.php/ADAM/article/download/1405/1405) | selected sections read | related work only |
| L027 | 2022 | [On chiral polytopes having a group PSL(3,q) as automorphism group](https://dipot.ulb.ac.be/dspace/bitstream/2013/333283/3/psl3-final.pdf) | selected sections read | related work only |
| L028 | 2021 | [A new algorithm to classify chiral polytopes with a given automorphism group](https://arxiv.org/pdf/1912.02287v1) | selected sections read | part of the results recovered |
| L029 | 2021 | [On residual connectedness in chiral geometries](https://arxiv.org/pdf/1911.03227v1) | selected sections read | part of the results recovered |
| L030 | 2021 | [An infinite family of locally X graphs based on incidence geometries](https://arxiv.org/pdf/1811.11438v1) | full text read | stated main results recovered |
| L031 | 2020 | [Orthogonal groups in characteristic 2 acting on polytopes of high rank](https://arxiv.org/pdf/1709.02219) | selected sections read | part recovered under stated assumptions |
| L032 | 2020 | [On regular polytopes of 2-power order](https://dipot.ulb.ac.be/dspace/bitstream/2013/292444/3/HRRPR-revised.pdf) | selected sections read | stated main results recovered |
| L033 | 2020 | [An exploration of locally spherical regular hypertopes](https://dipot.ulb.ac.be/dspace/bitstream/2013/309163/3/LSRH-revised.pdf) | selected sections read | not assessed |
| L034 | 2019 | [Existence of regular 3-hypertopes with 2 n chambers](https://arxiv.org/abs/1901.09034v1) | full text read | stated main results recovered |
| L035 | 2019 | [2-groups behaving as automorphism groups of regular 3-polytopes](https://arxiv.org/pdf/1802.08947v2) | selected sections read | stated main results recovered |
| L036 | 2019 | [On primitive geometries of rank two](https://adam-journal.eu/index.php/ADAM/article/download/1301/1075) | full text search only | not assessed |
| L037 | 2019 | [Rank reduction of string C-group representations](https://arxiv.org/pdf/1812.01055) | full short text read | earlier theorem used as an input |
| L038 | 2019 | [String C-group representations of alternating groups](https://arxiv.org/pdf/1810.12450) | selected sections read | part recovered under stated assumptions |
| L039 | 2018 | [Groups of Ree type in characteristic 3 acting on polytopes](https://arxiv.org/pdf/1501.01125) | selected sections read | related work only |
| L040 | 2018 | [C-groups of high rank for the symmetric groups](https://arxiv.org/pdf/1510.08990v1) | full text search only | not assessed |
| L041 | 2018 | [Hypertopes with tetrahedral diagram](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v25i3p22/pdf/) | full text search only | not assessed |
| L042 | 2018 | [An extension of the classification of high rank regular polytopes](https://arxiv.org/pdf/1509.01032v1) | full text search only | not assessed |
| L043 | 2017 | [Projective linear groups as automorphism groups of chiral polytopes](https://arxiv.org/pdf/1606.08017) | selected sections read | proposed answer or new result |
| L044 | 2017 | [Highest rank of a polytope for A n](https://arxiv.org/pdf/1605.09173v1) | selected sections read | related work only |
| L045 | 2017 | [Chiral polyhedra and finite simple groups](https://arxiv.org/pdf/1603.07713v3) | full text search only | not assessed |
| L046 | 2016 | [Algorithmic enumeration of regular maps](https://amc-journal.eu/index.php/amc/article/download/544/857) | selected sections read | not assessed |
| L047 | 2016 | [String C-groups as transitive subgroups of Sym(n)](https://arxiv.org/pdf/1410.5863v1) | selected sections read | not assessed |
| L048 | 2016 | [Polytopes of large rank for PSL(4,q)](https://digitalcommons.bucknell.edu/fac_journ/1204/) | abstract read | proposed answer or new result |
| L049 | 2016 | Two-transitive pairs in PSL(2,q) | metadata and access only | not assessed |
| L050 | 2016 | [Linear codes with complementary duals from some strongly regular subgraphs of the McLaughlin graph](https://www.mathos.unios.hr/mc/index.php/mc/article/download/1537/388) | selected sections read | part of the results recovered |
| L051 | 2016 | [Chiral polyhedra arising from almost simple groups with socle PSL(2,q)](https://link.springer.com/article/10.1007/s10801-016-0669-7) | abstract read | not assessed |
| L052 | 2016 | [Highly symmetric hypertopes](https://ria.ua.pt/bitstream/10773/16681/1/2016DFW.pdf) | selected sections read | proposed answer or new result |
| L053 | 2015 | [Almost simple groups with socle PSL(2,q) acting on abstract regular polytopes](https://dipot.ulb.ac.be/dspace/bitstream/2013/187644/1/Elsevier_171271.pdf) | abstract read | not assessed |
| L054 | 2015 | [An Atlas of subgroup lattices of finite almost simple groups](https://arxiv.org/pdf/1306.4820v2) | full text search only | not assessed |
| L055 | 2015 | [C-groups of PSL(2,q) and PGL(2,q)](https://dipot.ulb.ac.be/dspace/bitstream/2013/195928/1/Elsevier_179555.pdf) | abstract read | not assessed |
| L056 | 2015 | [Chiral polyhedra and projective lines](https://www.matem.unam.mx/~eugenia/papers/pslChiral.pdf) | selected sections read | not assessed |
| L057 | 2015 | [C-groups of Suzuki type](https://link.springer.com/content/pdf/10.1007/s10801-015-0605-2.pdf) | abstract read | not assessed |
| L058 | 2014 | [Abstract regular polytopes for the O'Nan group](https://dipot.ulb.ac.be/dspace/handle/2013/172544) | metadata and access only | not assessed |
| L059 | 2014 | [Core-free, rank two coset geometries from edge-transitive bipartite graphs](https://arxiv.org/pdf/1106.5704v2) | selected sections read | not assessed |
| L060 | 2013 | [Locally 2-arc-transitive complete bipartite graphs](https://dipot.ulb.ac.be/dspace/handle/2013/219392) | abstract read | not assessed |
| L061 | 2013 | [Binary codes of some strongly regular graphs of the McLaughlin graph](https://link.springer.com/content/pdf/10.1007/s10623-011-9589-7.pdf) | abstract read | not assessed |
| L062 | 2013 | [Corrigendum to "Polytopes of high rank for the symmetric groups"](https://www.sciencedirect.com/science/article/pii/S0001870812003805) | abstract read | not assessed |
| L063 | 2013 | [The rank two geometries of the PSL(2,q) groups : part II](https://amc-journal.eu/index.php/amc/article/download/181/241) | selected sections read | part of the results recovered |
| L064 | 2013 | [The rank two geometries of the PSL(2,q) groups : part II, Appendix](https://amc-journal.eu/index.php/amc/article/download/181/1862) | full text search only | not assessed |
| L065 | 2013 | [A new algorithm to find apartments in coset geometries](https://leemans.dimitri.web.ulb.be/abstracts/apart2.html) | abstract read | not assessed |
| L066 | 2013 | [On pairs of commuting involutions in Sym(n) and Alt(n)](https://math.uni.lu/kiefer/Publications/Involutions.pdf) | full text read | stated main results recovered |
| L067 | 2012 | [Polytopes of high rank for the alternating groups](https://dipot.ulb.ac.be/dspace/handle/2013/133342) | metadata and access only | not assessed |
| L068 | 2012 | [Regular 4-polytopes from the Livingstone graph of Janko's first group](https://link.springer.com/content/pdf/10.1007/s10801-011-0300-x.pdf) | full text read | [part of the results recovered](research/case_study/phase189_L068_overlay.json) |
| L069 | 2012 | [All alternating groups A n with n ≥ 12 have polytopes of rank ⌊ (n-1)/2 ⌋](https://epubs.siam.org/doi/10.1137/110838467) | abstract read | not assessed |
| L070 | 2012 | [Two atlases of abstract chiral polytopes for small groups](https://amc-journal.eu/index.php/amc/article/download/204/192) | full text search only | not assessed |
| L071 | 2012 | [Algorithms for classifying regular polytopes with a fixed automorphism group](https://cdm.ucalgary.ca/article/download/62152/46746) | selected sections read | not assessed |
| L072 | 2011 | [Polytopes of high rank for the symmetric groups](https://dipot.ulb.ac.be/dspace/bitstream/2013/133343/1/Elsevier_115702.pdf) | abstract read | not assessed |
| L073 | 2010 | [Rank three residually connected geometries  for M_{22}, revisited](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v17i1n4/pdf) | full text read | [part of the results recovered](research/case_study/phase181_registry_overlay.json) |
| L074 | 2010 | [On the number of abstract regular polytopes whose automorphism group is a Suzuki simple group Sz(q)](https://math.uni.lu/kiefer/Publications/szpoly3%20r%C3%A9vis%C3%A9.pdf) | full text read | stated main results recovered |
| L075 | 2010 | [On the geometry of O'N](https://www.math.auckland.ac.nz/~dleemans/abstracts/onan.html) | abstract read | not assessed |
| L076 | 2010 | [On the rank two geometries of the PSL(2,q) groups : part I](https://amc-journal.eu/index.php/amc/article/download/107/114) | full text search only | not assessed |
| L077 | 2009 | [On locally spherical polytopes of type {5,3,5}](https://doi.org/10.1016/j.disc.2007.12.084) | abstract read | not assessed |
| L078 | 2009 | [Locally s-arc-transitive graphs related to sporadic simple groups](https://www.math.auckland.ac.nz/~dleemans/abstracts/lsarc.html) | abstract read | not assessed |
| L079 | 2009 | [Polytopes with groups of type PGL(2,q)](https://arxiv.org/pdf/0909.1991v1) | full text read | [stated main results recovered](research/case_study/phase235_projective_line_overlay.json) |
| L080 | 2009 | On apartments in incidence geometry | metadata and access only | not assessed |
| L081 | 2008 | [A new Petrie-like construction for abstract polytopes](https://www.math.auckland.ac.nz/~dleemans/abstracts/newpetrie.html) | abstract read | not assessed |
| L082 | 2007 | [A rank six geometry related to the McLaughlin sporadic simple group](https://link.springer.com/article/10.1007/s10623-007-9082-5) | abstract read | not assessed |
| L083 | 2007 | [Groups of type L(2,q) acting on polytopes](https://arxiv.org/pdf/math/0606660v1) | full text read | [stated main results recovered](research/case_study/phase235_projective_line_overlay.json) |
| L084 | 2006 | Errata : "Quotients of a universal locally projective polytope of type {5,3,5}" | metadata and access only | not assessed |
| L085 | 2006 | [Almost simple groups of Suzuki type acting on polytopes](https://www.math.auckland.ac.nz/~dleemans/abstracts/szpoly.html) | abstract read | part of the results recovered |
| L086 | 2006 | [An atlas of abstract regular polytopes for small groups](https://www.math.auckland.ac.nz/~dleemans/abstracts/atlaspoly.html) | abstract read | not assessed |
| L087 | 2005 | [Two rank six geometries for the Higman-Sims sporadic group](https://www.sciencedirect.com/science/article/pii/S0012365X05000221) | abstract read | not assessed |
| L088 | 2005 | [On the thin regular geometries of rank four for the Janko group J(1)](https://msp.org/iig/2005/1-1/iig-v1-n1-p08-s.pdf) | full text read | stated main results recovered |
| L089 | 2005 | [On inductively minimal geometries that satisfy the intersection property](https://leemans.dimitri.web.ulb.be/abstracts/imgip.html) | metadata and access only | part of the results recovered |
| L090 | 2005 | [A family of geometries related to the Suzuki tower](https://www.math.auckland.ac.nz/~dleemans/abstracts/suz.html) | abstract read | not assessed |
| L091 | 2005 | [The residually weakly primitive geometries of HS](https://ajc.maths.uq.edu.au/pdf/33/ajc_v33_p231.pdf) | selected sections read | not assessed |
| L092 | 2005 | [A generalization of a construction due to Van Nypelseer](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.46/no.2/b46h2lee.pdf) | full text read | [stated main results recovered](research/case_study/phase208_L092_overlay.json) |
| L093 | 2004 | [Constructions of rank five geometries for the Mathieu group M_22](https://www.math.auckland.ac.nz/~dleemans/abstracts/m22rk5.html) | abstract read | not assessed |
| L094 | 2004 | [The residually weakly primitive geometries of PSL(3,q) with q < 8](https://link.springer.com/article/10.1007/s00010-003-2695-5) | abstract read | not assessed |
| L095 | 2004 | [Quotients of a universal locally projective polytope of type {5,3,5}](https://arxiv.org/pdf/math/0307075v1) | full text search only | not assessed |
| L096 | 2004 | [An algorithmic analysis of the intersection property](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/2108DB59271CED59B950340F28252A28/S1461157000001133a.pdf/div-class-title-an-algorithmic-analysis-of-the-intersection-property-div.pdf) | selected sections read | explicit representation or test |
| L097 | 2004 | [The residually weakly primitive geometries of J_3](https://www.math.auckland.ac.nz/~dleemans/abstracts/j3.html) | abstract read | not assessed |
| L098 | 2004 | [The residually weakly primitive geometries of M_23](https://www.math.auckland.ac.nz/~dleemans/abstracts/m23.html) | abstract read | part of the results recovered |
| L099 | 2003 | [On a rank four geometry for the Hall-Janko sporadic group](https://www.sciencedirect.com/science/article/pii/S0097316502000225) | abstract read | not assessed |
| L100 | 2003 | [Geometries for the group PSL(3,4)](https://www.math.auckland.ac.nz/~dleemans/abstracts/psl34.html) | abstract read | not assessed |
| L101 | 2003 | [The residually weakly primitive geometries of M_22](https://www.math.auckland.ac.nz/~dleemans/abstracts/m22.html) | abstract read | part of the results recovered |
| L102 | 2003 | [RWPRI and (2T)_1 flag-transitive linear spaces](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.44/no.1/b44h1bue.pdf) | selected sections read | proposed answer or new result |
| L103 | 2002 | [The RWPRI geometries of Sym(5) x 2](https://www.math.auckland.ac.nz/~dleemans/abstracts/s5x2.html) | abstract read | not assessed |
| L104 | 2002 | [The residually weakly primitive geometries of J_2](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v21n1p77/585) | full short text read | [stated main results recovered](research/case_study/phase181_registry_overlay.json) |
| L105 | 2002 | [Constructing coset geometries with Magma : An application to the sporadic groups M(12) and J(1)](https://www.math.auckland.ac.nz/~dleemans/abstracts/algo.html) | abstract read | part of the results recovered |
| L106 | 2001 | [On a rank five geometry of Meixner for the Mathieu group M(12)](https://www.math.auckland.ac.nz/~dleemans/abstracts/m12b.html) | abstract read | not assessed |
| L107 | 2001 | [Some rank five geometries related to the Mathieu group M(23)](https://www.math.auckland.ac.nz/~dleemans/abstracts/m23rk5.html) | abstract read | not assessed |
| L108 | 2001 | [On the Petrials of thin rank 3 geometries](https://www.math.auckland.ac.nz/~dleemans/abstracts/petrie.html) | full text read | stated main results recovered |
| L109 | 2000 | [The residually weakly primitive geometries of the Dihedral Groups](https://www.math.auckland.ac.nz/~dleemans/abstracts/d2n.html) | abstract read | part of the results recovered |
| L110 | 2000 | [The residually weakly primitive pre-geometries of the Suzuki simple groups](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v20n1p1/995) | selected sections read | partial progress |
| L111 | 2000 | [New geometries for finite groups and polytopes](https://www.math.auckland.ac.nz/~dleemans/abstracts/ngeo.html) | selected sections read | part of the results recovered |
| L112 | 1999 | [On a geometry of Ivanov and Shpectorov for the O'Nan sporadic simple group](https://www.math.auckland.ac.nz/~dleemans/abstracts/on.html) | abstract read | not assessed |
| L113 | 1999 | [An Atlas of regular thin geometries for small groups](https://www.math.auckland.ac.nz/~dleemans/abstracts/atlasthin.html) | abstract read | not assessed |
| L114 | 1999 | [The rank 3 geometries of the simple Suzuki groups Sz(q)](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v19n1p43/837) | selected sections read | proposed answer or new result |
| L115 | 1998 | [The Rank 2 Geometries of the Simple Suzuki Groups Sz(q)](https://emis.de/ft/11479) | selected sections read | a finite subfamily recovered |
| L116 | 1998 | [Thin geometries for the Suzuki simple group Sz(8)](https://www.math.auckland.ac.nz/~dleemans/abstracts/sz8thin.html) | abstract read | not assessed |
| L117 | 1997 | [Two Nearly Isomorphic Groups](https://www.math.auckland.ac.nz/~dleemans/abstracts/twoiso.html) | abstract read | not assessed |
| L118 | 1996 | [On the List of Finite Primitive Permutation Groups of Degree Less Than 50](https://www.math.auckland.ac.nz/~dleemans/abstracts/primlist.html) | abstract read | not assessed |
| L119 | 1996 | [All Geometries of the Mathieu Group M(11) Based on Maximal Subgroups](https://www.math.auckland.ac.nz/~dleemans/abstracts/m11.html) | abstract read | not assessed |
| L120 | 2021 | [String C-group representations of almost simple groups: a survey](https://arxiv.org/pdf/1910.08843) | selected sections read | partial progress |
| L121 | 2021 | [Two families of locally toroidal regular 4-hypertopes arising from toroids](https://dipot.ulb.ac.be/dspace/bitstream/2013/301629/3/FLPWrev.pdf) | full text search only | not assessed |
| L122 | 2019 | [Coset geometries with trialities and their reduced incidence graphs](https://www.iam.fmph.uniba.sk/amuc/ojs/index.php/amuc/article/download/1309/743) | full text search only | not assessed |
| L123 | 1997 | [The residually weakly primitive geometries of the Suzuki simple group Sz(8)](https://www.math.auckland.ac.nz/~dleemans/abstracts/sz8.html) | abstract read | not assessed |
| L124 | 1998 | [On Flag-Transitive Incidence Geometries of Rank 6 for the Mathieu Group M(12)](https://www.math.auckland.ac.nz/~dleemans/abstracts/m12.html) | abstract read | part of the results recovered |
| L125 | 1998 | [The Residually Weakly Primitive Geometries of the Janko Group J(1)](https://www.math.auckland.ac.nz/~dleemans/abstracts/j1.html) | abstract read | part of the results recovered |
| L126 | unconfirmed | [Groups represented by incidence geometries](https://arxiv.org/pdf/2506.10464) | selected sections read | not assessed |
| L127 | unconfirmed | Tight chiral polyhedra of order 2p m | metadata and access only | not assessed |
| L128 | unconfirmed | [Hypertopes with prescribed diagram symmetries](https://arxiv.org/pdf/2610.09711) | selected sections read | not assessed |
| F001 | 2021 | [On the ranks of string C-group representations for symplectic and orthogonal groups](https://arxiv.org/pdf/1912.05512) | selected sections read | not assessed |
| F002 | 2025 | [String C-group representations of transitive groups: a case study with degree 11](https://arxiv.org/pdf/2302.11943) | selected sections read | not assessed |
| F003 | 2021 | [On the rank of Suzuki polytopes: an answer to Hubard and Leemans](https://arxiv.org/pdf/2010.04080) | full short text read | not assessed |
| F004 | 2026 | [Abstract regular polytopes of G2(q) in even characteristic](https://arxiv.org/pdf/2609.25004) | selected sections read | not assessed |
| F005 | 2025 | [Polytopality criteria for the mix of polytopes and maniplexes](https://arxiv.org/pdf/2506.19334) | selected sections read | not assessed |
| F006 | 2025 | [Abstract Regular Polytopes of Finite Irreducible Coxeter Groups](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v32i4p18/pdf/) | selected sections read | not assessed |
| F007 | 2026 | [Faithfulness in maniplexes](https://dirros.openscience.si/Dokument.php?id=49623&lang=eng) | selected sections read | not assessed |
| F008 | 2026 | [On solutions to the Mondrian Puzzle](https://tenenb.perso.math.cnrs.fr/PPP/Mondrian.pdf) | selected sections read | not assessed |
| F009 | 2026 | [On the order-diameter ratio of girth-diameter cages](https://arxiv.org/pdf/2511.21144) | selected sections read | not assessed |
| F010 | 2025 | [Every finite group is represented by a finite incidence geometry](https://arxiv.org/pdf/2511.02410) | full text read | [stated main results recovered](research/case_study/phase193_F010_overlay.json) |
| F011 | 2024 | [Explicit constructions of Diophantine tuples over finite fields](https://link.springer.com/content/pdf/10.1007/s11139-024-00888-5.pdf) | selected sections read | not assessed |
| F012 | 2025 | [Exhaustive generation of edge-girth-regular graphs](https://arxiv.org/pdf/2401.08271) | selected sections read | not assessed |
| F013 | 2026 | [String C-groups of 2-power order project onto a common string C-group](https://arxiv.org/pdf/2605.20691) | full text read | stated main results recovered |
| F014 | 2025 | [Regular 3-polytopes of type {n,n}](https://arxiv.org/pdf/2505.09505) | full text read | [stated main results recovered](research/case_study/phase233_F014_overlay.json) |
| F015 | 2023 | [Infinite Families of Hypertopes from Centrally Symmetric Polytopes](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v30i2p20/pdf/) | selected sections read | part of the results recovered |
| F016 | 2025 | [Symmetric polytopes whose automorphism groups are 2-groups](https://arxiv.org/abs/2512.15511v1) | full text read | stated main results recovered |
| F017 | 2018 | [LCD codes from adjacency matrices of graphs](https://www.math.clemson.edu/~keyj/Key/LCD_KeyRod.pdf) | selected sections read | not assessed |
| N001 | 1998 | [Some properties of inductively minimal geometries](https://doi.org/10.36045/bbms/1103409005) | full text read | stated main results recovered |
| N002 | 2001 | [On the number of inductively minimal geometries](https://doi.org/10.1016/S0304-3975(00)00228-0) | abstract read | part of the results recovered |
| N003 | 2002 | [Independent generating sets and geometries for symmetric groups](https://maths.qmul.ac.uk/~pjc/preprints/igsgsn.pdf) | full text read | stated main results recovered |
| N004 | 2003 | [Truncations of inductively minimal geometries](https://doi.org/10.1016/S0012-365X(02)00603-9) | abstract read | part of the results recovered |
| N005 | 2025 | [From Group Operations to Geometric Structures: Amalgamations, HNN-Extensions, and Twisting in Coset Geometries](https://arxiv.org/abs/2505.24662) | selected sections read | related work only |
| N006 | 2026 | [The geometry of wreath and semi-direct products](https://arxiv.org/abs/2605.04646v2) | abstract read | not assessed |
| N007 | 2026 | [Coset geometries acting on their elements: The j-diagonals twisting](https://arxiv.org/abs/2608.23223v1) | abstract read | not assessed |
| N008 | 2005 | [Using the Frattini Subgroup and Independent Generating Sets to Study RWPRI Geometries](https://ftp.gwdg.de/pub/EMIS/journals/BAG/vol.46/no.1/b46h1car.pdf) | full text read | stated main results recovered |
| N009 | 2018 | [String C-groups of order 1024](https://cdm.ucalgary.ca/article/download/62475/46803) | full text read | stated main results recovered |
| N010 | 2006 | [Problems on polytopes, their groups, and realizations](https://link.springer.com/article/10.1007/s10998-006-0035-y) | selected sections read | partial progress |
| N011 | 2025 | [On generation of the groups GL_n(q) and PGL_n(q) by three involutions, two of which commute](https://journal.imm.uran.ru/2025-v.31-4-fon-03) | selected sections read | earlier theorem used as an input |
| N012 | 2025 | [Linear groups over finite fields and over the ring of integers as automorphism groups of regular polytopes of rank 3](https://sfu.ru/ru/science/dissertations/2b9582cf-c095-4bb6-9b28-c46d7421416e) | selected sections read | related work only |
| N013 | 2020 | [Locally Spherical Hypertopes from Generalised Cubes](https://arxiv.org/abs/2001.11082v1) | full text read | stated main results recovered |
| N014 | 2024 | [Constructing new geometries: a generalized approach to halving for hypertopes](https://arxiv.org/abs/2405.19050v1) | selected sections read | proposed answer or new result |
| N015 | 2024 | [Abelian covers of regular hypertopes](https://www.sciencedirect.com/science/article/abs/pii/S0021869324001534) | abstract read | not assessed |
| N016 | 2024 | [Chiral polytopes whose smallest regular cover is a polytope](https://gabrielcunningham.com/WhichChiralPolytopes.pdf) | full text read | stated main results recovered |

## Rebuilding this reader

The generator reads the frozen registry and its reviewed additions, verifies
their hash chain and counts, and writes only this Markdown page. It does not
change metadata, rerun proofs or refresh the literature search.

```sh
python3 scripts/build_paper_registry.py
python3 scripts/build_paper_registry.py --check
```

A new mathematical assessment needs an exact statement, its proof and the
earlier results it uses. It should be recorded and reviewed before an addition
is included in this reader. Complete formalization, later-literature checks
and measurements remain separate tasks. See [reproduction instructions](REPRODUCING.md).
