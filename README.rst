Human Compression
=================

Can reusable mathematics and capable language-model agents recover decades
of published results in shorter, complete papers? This project tests that
question through explicit proofs, attribution and measured comparisons.

The fixed catalogue contains 161 original manuscripts. At the intake cutoff,
102 full texts had been retrieved and 27 manuscripts had admitted recoveries
of specified principal results. These are progress counts, not a boundary
on the work. Every accessible original in the catalogue remains in the
compression programme, including papers whose replacement proofs have not
yet been written. Source retrieval continues within these 161 titles.

The `register of every original <audit/corpus/v1/README.rst>`_ and
`subsequent admissions <audit/corpus/latest.json>`_ now record **106
accessible manuscripts: 35 with admitted principal-result recoveries and
71 awaiting complete recovery**. The other **55 remain retrieval targets**.
The register gives each original's source, mathematical targets, proof
evidence and next obligation. All thirty-five admitted recoveries now have
measured comparisons. The newly obtained
`L084 erratum <audit/corpus/access/erratum-2006/README.rst>`_ awaits recovery.
The complete `L100 institutional preprint <audit/corpus/access/halle-preprint/README.rst>`_
also joins the recovery queue. The catalogue itself has not grown.

An accessible paper awaiting a proof or measurement is pending, not excluded.
A complete authored rendering is a usable source even when its PDF is
unavailable. An original without a usable full text stays in the retrieval
queue and receives no numerical comparison until its source can be checked.
Each published numerical comparison identifies the originals whose declared
principal results its current proofs recover. The remaining accessible
originals stay on the programme until their proofs and comparisons are done.

The `consolidated comparison <audit/overview/v4/packet/summary.pdf>`_ gives
all fourteen measured topics, all thirty-five individual factors and complete
program costs in six pages. The `topic graph
<audit/overview/v4/packet/whole_topics.svg>`_ shows every complete common paper
and application. Two graphs show the `first seventeen
<audit/overview/v4/packet/conditional_1.svg>`_ and `remaining eighteen
<audit/overview/v4/packet/conditional_2.svg>`_ source/application comparisons.
The `numerical overview <audit/overview/v4/README.rst>`_ links exact tables,
inputs and independent arithmetic and graph review.

The new `gluing topic <papers/topic-gluing/v1/README.rst>`_ supplies two common
papers and an application recovering the main results of L010. Its complete
written factor is **0.677**, or **0.508** with all printed programs. Its
application factor is **2.342** after acquiring both whole common papers and
all declared programs. The `complete numerical audit
<audit/gluing-measurement/v1/README.rst>`_ retains every cost and qualification.

B now uses one complete common paper; the enlarged orbit topic includes both
N007 and N006 with all companion papers. Each topic pays its entire common
theory once, independently of other topics. Earlier reports remain preserved.

.. list-table:: Current measured sets within the recovery programme
   :header-rows: 1

   * - Topic
     - Measured / recovered originals
     - Whole written factor
     - With printed programs
   * - A: Supported kernels and finite two-groups
     - 7 / 7
     - 1.571
     - 1.124
   * - B: Coset geometries and symmetric markings
     - 5 / 5
     - 1.094
     - 0.981
   * - C: Chamber operations and binary translations
     - 5 / 5
     - 1.292
     - 1.052
   * - D: Stabilizers and geometry enumeration
     - 3 / 3
     - 1.053
     - 0.660
   * - E: Projective groups
     - 3 / 3
     - 1.816
     - 1.523
   * - F: Odd kernels and marked semidirect products
     - 1 / 1
     - 1.264
     - 0.875
   * - G: Linear spaces and support
     - 2 / 2
     - 0.630
     - 0.433
   * - Affine constructions
     - 1 / 1
     - 0.786
     - 0.556
   * - Group representations by geometries
     - 1 / 1
     - 1.015
     - 0.746
   * - Chamber systems and covers
     - 2 / 2
     - 0.982
     - 0.811
   * - Matching extensions
     - 1 / 1
     - 1.119
     - 0.976
   * - Chiral enumeration
     - 1 / 1
     - 0.925
     - 0.674
   * - Orbit and semidirect constructions
     - 2 / 2
     - 1.129
     - Unavailable; 0.170 with full raw software
   * - Gluing by common points and synchronized trees
     - 1 / 1
     - 0.677
     - 0.508

These are text costs, not minimum proof complexities. The reports specify
the complete program boundary, raw-code alternatives, retained external
proofs, graphic costs and counting-unit sensitivity. B and C use complete
available text, including authored non-PDF sources and page furniture; the
other comparisons use calibrated PDF text with repeated furniture removed.
No pooled factor is inferred across these representations. Factors below
one stay in the comparison. A near-unity factor shows little saving by our
current proofs; it does not establish originality. For D, the applications
cost 29,855 against 47,894 for the sources, but the common theory adds 15,632.
Further reuse must be proved before it earns a larger measured saving.

Read the `audit protocol <audit/protocol.pdf>`_ and its
`TeX source <audit/protocol.tex>`_. The historical cutoff is recorded in
`audit/intake.json <audit/intake.json>`_. Its carry-over restrictions describe
that earlier stage, not the current programme across all accessible originals.

Common proofs for finite two-groups
----------------------------------

The `common theory <papers/topic-a/v2/umbrella.pdf>`_ proves how separately
supported kernels determine marked subgroup intersections, how to recognize
the resulting presentations, and how a finite quotient bounds a search
through normal kernels. Seven complete applications recover the following
principal result sets. Their proofs, retained inputs and corrections have
passed independent mathematical and source review.

.. list-table:: Seven source manuscripts and the results recovered
   :header-rows: 1
   :widths: 34 44 22

   * - Source, authors and edition
     - Declared principal results
     - Our application
   * - L032: Hou–Feng–Leemans, *On regular polytopes of 2-power order*;
       revised author manuscript, 8 November 2019
     - Theorem 1.2 for every stated rank, type and order, with the necessary bound
     - `Prescribed orders <papers/topic-a/v2/two-power-orders.pdf>`_
   * - L034: Hou–Feng–Leemans, *Existence of regular 3-hypertopes with 2^n
       chambers*; arXiv:1901.09034v1
     - Lemma 3.1 and Theorem 3.2: presentation, order, structure and geometry;
       explicit corrections
     - `Three-generator hypertopes <papers/topic-a/v2/three-generator-hypertopes.pdf>`_
   * - F016: Cunningham–Feng–Hou–Schulte, *Symmetric polytopes whose
       automorphism groups are 2-groups*; arXiv:2512.15511v1
     - Square classification, section assemblies, presentations and three
       free extensions; stated geometric inputs retained
     - `Square sections and extensions <papers/topic-a/v2/square-sections-and-free-extensions.pdf>`_
   * - F013: Hou–Schulte, *String C-groups of 2-power order project onto a
       common string C-group*; arXiv:2605.20691v1
     - Both principal common-quotient and covering theorems in all ranks;
       auxiliary correction kept separate
     - `Common quotients <papers/topic-a/v2/common-two-group-quotient.pdf>`_
   * - L035: Hou–Feng–Leemans, *Existence of regular 3-polytopes of order
       2^n*; arXiv:1802.08947v2
     - Theorems 1.2–1.3: full existence range and all three high-type
       classifications, with converse and finite seed checks
     - `High-type classifications <papers/topic-a/v2/high-type-two-groups.pdf>`_
   * - N009: Gomi–Loyola–De Las Peñas, *String C-groups of order 1024*;
       Contributions to Discrete Mathematics 13(1) (2018), 1–22
     - Nondegenerate marked classification, all six source tables and
       finite universal orders; explicit literal corrections
     - `Markings of order 1024 <papers/topic-a/v2/order-1024-markings.pdf>`_
   * - L128: Leemans–Spiga–Tranchida, *Hypertopes with prescribed diagram
       symmetries*; arXiv:2610.09711v1, nine pages
     - Every graph diagram, full groups and correlations, exact orders and
       parabolics, two-group minima and the unrestricted rank-three minimum;
       the proper-quotient assertion requires the same diagram
     - `Graph symmetries <papers/topic-a/extensions/diagram-symmetries/v1/graph_symmetries.pdf>`_

The `seventh application's admission
<audit/topic-a/extensions/diagram-symmetries/v1/admission.json>`_ includes a
distinct review of all fourteen source clauses, an independent finite search
and six scoped Lean declarations. It uses the whole existing common paper.
Its three-page application and complete one-page program appendix are included
in the `expanded comparison <audit/ac-extensions-measurement/v1/packet/measurement.pdf>`_.
The seven originals cost 213,803 characters, the whole common theory 49,059
and all applications 87,019: **1.571×** as written. All five printed programs
add 54,210, giving **1.124×**; the raw alternative gives **1.132×**.
After acquiring the whole theory and program bundle, L128/A7 is **2.101×**.
The six earlier application factors are unchanged. The older figures below
remain the comparison of their original six-manuscript set.

The `scope reader <audit/topic-a/v2/SCOPE.rst>`_ states the exact coverage,
exclusions, attribution and formal limits. The `proof admission
<audit/topic-a/v2/admission.json>`_ binds the accepted edition and its
independent reviews. These six existing contracts add no new manuscript
or solved-question credits. The original classifications and constructions
retain their authors' attribution.

The common paper is 17 pages and the earlier six applications total 33 pages.
The `complete computation appendix <papers/topic-a/v2/two-group-computation.pdf>`_
is another 21 pages; all four executable files are in
`required-code <papers/topic-a/v2/required-code>`_. An independent replay
checked the exhaustive census and presentations against all 107 comparison
rows. GAP's exact group algorithms remain an explicit trust boundary.

The `three-page length audit <audit/topic-a/v2/measurement/reader/measurement.pdf>`_ gives
**1.535 times** for the complete written topic and **1.083 times** including
the whole required program. The six source manuscripts total 195,379
characters. Our full theory costs 49,059 and the six applications cost
78,251: together, 127,310. The complete program appendix adds 53,035,
bringing the denominator to 180,345.

.. list-table:: Each application after acquiring the common theory and program
   :header-rows: 1

   * - Source
     - Source characters
     - Application characters
     - Conditional factor
   * - L032
     - 16,558
     - 8,212
     - 2.016
   * - L034
     - 21,433
     - 5,784
     - 3.706
   * - F016
     - 43,983
     - 15,419
     - 2.853
   * - F013
     - 25,562
     - 6,224
     - 4.107
   * - L035
     - 51,019
     - 14,498
     - 3.519
   * - N009
     - 36,824
     - 28,114
     - 1.310

These use NFC non-whitespace characters in complete-document extracted
PDF text, with exact running furniture excluded. Titles, abstracts and
references remain included. The conditional factors assume the **whole
common theory and complete program** have already been acquired; those
costs remain in the whole-topic comparison.

Source diagrams and some image labels, particularly in L035, are absent
from text extraction. Their costs remain unknown, as do unmeasured outside
proofs and historical programs. These are comparisons of known text costs,
not measurements of all visible content or minimum mathematical complexity.
The `complete numerical ledger <audit/topic-a/v2/measurement/results.json>`_
retains five units, two normalizations and the raw extraction sensitivities.
The `cost graph <audit/topic-a/v2/measurement/reader/costs.svg>`_ shows the
common acquisition followed by all six applications. The `numerical admission
<audit/topic-a/v2/measurement/admission.json>`_ records the independent
recount and exact fraction checks.

The `paired proof graph <audit/topic-a/v2/dag/default_view.svg>`_ shows
the historical arguments and their replacements. Download and open the
`interactive explorer <audit/topic-a/v2/dag/explorer.html>`_ to select any
of the six comparisons, expand a theorem's proof, and inspect its costs,
prerequisites and source references. It works without a network connection;
proof links resolve when it is opened within a repository checkout.

The audit assigns every counted passage to one owner: 341 spans across
14 documents. The 236 argument and reference nodes can share these owners,
so their displayed costs must not be added together. Totals count each
passage once, including the complete program appendix. The `graph review
<audit/topic-a/v2/dag_admission.json>`_ records the independent checks and
the remaining limits, including unknown external costs. Static SVG rendering
and interface checks pass; actual browser layout has not been certified.

Forest coordinates and primitive geometries
-------------------------------------------

Topic B's sixteen-page `common theory <papers/topic-b/v3/umbrella.pdf>`_
proves the shared coset, tree, generation and extremal-classification results
used by all five applications. One classification now supplies both arbitrary
maximal independent markings and the involution case. A single normal-quotient
argument and a common extension theorem for nested subsets remove repeated
proofs. Local core, fracture, presentation and retained classification
obligations remain explicit.

.. list-table:: Five source manuscripts and the results recovered
   :header-rows: 1
   :widths: 34 44 22

   * - Source, authors and edition
     - Declared principal results
     - Our application
   * - N001: Buekenhout–Cara, *Some properties of inductively minimal
       geometries* (1998); complete authored browser text
     - Theorem 1, all four clauses; the PRI criterion is stated precisely
     - `Tree coordinates <papers/topic-b/v3/inductively-minimal-geometries.pdf>`_
   * - N003: Cameron–Cara, *Independent generating sets and geometries for
       symmetric groups* (2002); twelve-page author manuscript
     - Eight stated results, including the classification for n >= 7 and
       all three counting conventions
     - `Extremal markings <papers/topic-b/v3/maximal-symmetric-markings.pdf>`_
   * - N008: Archer–Cara–Krempa, *Using the Frattini Subgroup and Independent
       Generating Sets to Study RWPRI Geometries* (2005); published edition
     - Eleven clauses: geometric containment, finite p-group coordinates
       and counts; corrected infinite generating-set converse
     - `Frattini coordinates <papers/topic-b/v3/frattini-coordinate-geometries.pdf>`_
   * - L030: Garcia-Colin–Leemans, *An infinite family of incidence
       geometries whose incidence graphs are locally X*; ten-page revised
       institutional manuscript associated with the 2021 publication
     - Seven clauses, including distances, residues and full graph
       automorphisms; panel, thin-boundary and example corrections retained
     - `Disjoint-subset geometries <papers/topic-b/v3/disjoint-subset-geometries.pdf>`_
   * - L040: Fernandes–Leemans, *C-groups of high rank for the symmetric
       groups* (2018); accepted manuscript, twenty authored pages and cover
     - Ranks n−1 and n−2 in their full ranges: classification, tree
       presentations and regular hypertopes; corrected branching clause
     - `Finite cores and high rank <papers/topic-b/v3/high-rank-symmetric-markings.pdf>`_

The `scientific admission <audit/topic-b/v3/README.rst>`_ preserves all 65
source dispositions and records distinct review of the complete arguments.
The five applications have 3, 4, 4, 5 and 11 pages; the complete four-program
appendix has seven. Fourteen reused Lean declarations verify specified
subgroup and normalization lemmas, not the full classification. The auxiliary
primitive-rank census and unspecified leaf convention remain outside the
principal-result contract. No new original or conjecture answer is added.

The `current five-original comparison
<audit/b-unified-measurement/v1/packet/reader.pdf>`_ is
124,906 / (44,905 + 69,265) = **1.094×**. Including every printed program gives
**0.981×**; the complete raw alternative gives **0.987×**. After full prior
acquisition, the five application factors are **1.970×, 1.942×, 1.618×,
1.848× and 1.770×**. The complete written edition is 4,620 characters shorter
than our previous edition. This measures the present proof method, not an
intrinsic minimum or originality. The previous `two-common-paper comparison
<audit/b5-measurement/v1/packet/measurement.pdf>`_ remains a historical record.

The preserved earlier `complete available-text comparison
<audit/available-text/v1/packet/measurement.pdf>`_ includes four originals,
using N001's complete authored rendering. Its written factor is **1.236×**:
73,012 / (14,124 + 44,959), charging the whole common theory once.
After acquiring it, the four application factors are **1.970×, 1.255×,
1.618× and 1.848×**. No mathematical program is required by these proofs.

These are NFC nonspace character counts with running furniture retained
throughout: literal rendered text for N001 and untrimmed PDF text for all
other documents. The `common/application graph
<audit/available-text/v1/packet/B-costs.svg>`_ and `independent audit
<audit/available-text/v1/README.rst>`_ state this representation explicitly.
The earlier `PDF-only measurement <audit/topic-b/v2/measurement/README.rst>`_
is preserved as a historical comparison; its missing PDF is not grounds for
excluding N001. Graphic and retained external-proof costs remain unknown.

The `proof routes and acquisition costs
<audit/topic-b/v2/dag/reader/reader.pdf>`_ explain the same comparison through
paired dependency graphs. The `standalone explorer
<audit/topic-b/v2/dag/reader/explorer.html>`_ can be downloaded and opened
locally to select any of the thirty source clauses. The
`static graph <audit/topic-b/v2/dag/reader/default.svg>`_ shows one application
of the common forest theory. Every complete paper remains charged; overlapping
graph boxes refer to shared passages and are never summed as separate costs.
The `graph audit <audit/topic-b/v2/dag/README.rst>`_ records the independent
mathematical review, text accounting and reader checks. These graphs add no
new result or conjecture credit.

Chamber operations and binary translations
-----------------------------------------

Topic C's `common theory <papers/topic-c/v2/umbrella.pdf>`_ presents even
binary translations by differences along a connected graph. A covariance
identity then gives an explicit inverse for the resulting group presentation.
The generalized-cube and equal-parameter applications share the graph
argument; the latter replaces an order comparison by inverse homomorphisms.
The common paper also includes the complete geometric operation arguments.
The fifth application adds a common incidence reconstruction note.

.. list-table:: Five source manuscripts and the results recovered
   :header-rows: 1
   :widths: 34 44 22

   * - Source, authors and edition
     - Declared principal results
     - Our application
   * - L088: Hartley–Leemans, *On the thin regular geometries of rank four
       for the Janko group J1* (2005); ten-page journal article
     - Six constructions, failed operations and the complete rank census;
       a figure-label correction remains explicit
     - `Janko geometries <papers/topic-c/v2/janko-geometries.pdf>`_
   * - N013: Montero–Ivić Weiss, *Locally spherical hypertopes from
       generalised cubes*; arXiv v1, 2020
     - Parity, local sphericity and toroidal identifications; nonsphericity
       qualification and two excluded auxiliary claims remain explicit
     - `Generalized cubes <papers/topic-c/v2/halving-generalized-cubes.pdf>`_
   * - L108: Bonheure–Buekenhout–Leemans, *On the Petrials of thin rank 3
       geometries* (2001); complete authored text of printed pages 19–25
     - Natural action kernel, thinness obstruction and recovery; corrected
       embedding and length assertions; original PDF unavailable
     - `Petrials <papers/topic-c/v2/petrials-and-faithful-actions.pdf>`_
   * - F014: Li–Zhang, *Regular 3-polytopes of type {n,n}*; arXiv v1, 2025
     - Marked construction, matrices and universal presentation; corrected
       multiplication convention and separate small-parameter case
     - `Equal adjacent parameters <papers/topic-c/v2/equal-adjacent-parameters.pdf>`_
   * - L068: Hartley–Hubard–Leemans, *Regular 4-polytopes from the Livingstone
       graph of Janko's first group*; Journal of Algebraic Combinatorics 35
       (2012), 193–214
     - Complete graph constructions, face and flag-stabilizer tables and full
       group J1; the second construction is literal, while the first needs
       the explicitly stated induced-quadruple condition
     - `Livingstone polytopes <papers/topic-c/extensions/livingstone/v1/livingstone-polytopes.pdf>`_

The `Livingstone admission
<audit/topic-c/extensions/livingstone/v1/admission.json>`_ records all seventeen
source dispositions, the literal counterexample and its repair, fresh exact
computations and three reused Lean incidence lemmas. The complete
`incidence note <papers/topic-c/extensions/livingstone/v1/incidence-reconstruction.pdf>`_
adds two pages to the common input; the application has six pages and its
`complete program appendix <papers/topic-c/extensions/livingstone/v1/programs.pdf>`_
has eight. The `expanded comparison <audit/ac-extensions-measurement/v1/packet/measurement.pdf>`_
charges the shared construction once and retains the whole old exhaustive census.
The five originals cost 118,433 characters, the complete enlarged common theory
30,437 and all applications 61,248: **1.292×** as written. The three complete
printed programs add 20,933, giving **1.052×**; raw files give **1.061×**.
After acquiring the whole enlarged theory and bundle, L068/C5 is **2.603×**.
The four earlier application factors remain unchanged. The following figures
cover that earlier four-original set only.

The earlier common paper has ten pages and its four applications total seventeen.
The `four-page program appendix <papers/topic-c/v2/required-programs.pdf>`_
contains both complete programs required for the Janko census. The
`independent review <audit/topic-c/v2/independent_review/review.pdf>`_
checked all forty contract rows, including their corrections and exclusions,
and freshly reproduced the full census: six rank-four classes and no
rank-five classes. Retained subgroup data and classical classifications
remain explicit inputs.

Nine new Lean declarations verify the general inverse argument; seven
unchanged declarations verify supporting displacement and intersection
statements. All sixteen were freshly compiled. The specific augmentation
maps, geometric applications and finite census remain outside Lean.
The `publication guide <papers/topic-c/v2/PUBLICATION.rst>`_ gives the exact
scope and separate replay commands.

The preserved earlier `complete available-text comparison
<audit/available-text/v1/packet/measurement.pdf>`_ includes four originals,
using L108's complete authored rendering. Its written factor is **1.037×**:
73,953 / (27,142 + 44,163). Including both complete required programs gives
**0.923×** as printed, or **0.929×** using their raw files instead.

After acquiring the whole common theory and both programs, the individual
factors are **1.164×, 1.730×, 1.275× and 2.956×**, respectively. The
`common/application graph <audit/available-text/v1/packet/C-costs.svg>`_
shows every complete component. Running furniture remains included
throughout: L108 uses literal rendered text and the other documents use
untrimmed PDF text. The earlier `PDF-only audit
<audit/topic-c/v2/measurement/README.rst>`_ is preserved separately.
The accepted `dependency and cost reader
<audit/topic-c/v2/dag/costs/reader.pdf>`_ now traces all forty clauses through
the historical and current proofs. Download the `offline explorer
<audit/topic-c/v2/dag/costs/explorer.html>`_ to inspect a selected result,
its prerequisites and source locations. The `acquisition plot
<audit/topic-c/v2/dag/costs/acquisition.pdf>`_ shows the entire common paper,
program appendix and four applications in sequence.

The graph uses 199 exclusive passage owners and preserves all 270 measured
document coordinates. Overlapping statements are counted once in each
prerequisite union; every complete paper still includes its context and
references. No node-count factor is reported. The `review guide
<audit/topic-c/v2/dag/README.rst>`_ records the independent semantic and
cost checks, the corrected reader, and the unknown outside costs. Static
figures and deterministic DOM behavior were checked; a real-browser layout
test has not been performed.
These are four existing principal contracts; the higher-rank question
associated with F014 stays separate.

Stabilizers, support and geometry enumeration
--------------------------------------------

The `common theory <papers/topic-d/v2/umbrella.pdf>`_ counts admissible
extensions through their stabilizers and exact support. It combines
classical orbit counting and Möbius inversion, and contains complete
recognition and augmentation proofs for coset geometries with an arbitrary
chamber stabilizer. The applications supply the local group arguments
and computations.

.. list-table:: Three source manuscripts and the results recovered
   :header-rows: 1
   :widths: 34 44 22

   * - Source, authors and edition
     - Declared principal results
     - Our application
   * - L066: Kiefer–Leemans, *On pairs of commuting involutions in Sym(n)
       and Alt(n)*; nine-page author edition, 2013
     - Pair counts in every degree and the complete degree-six
       polyhedron classification; source proof correction explicit
     - `Commuting involutions <papers/topic-d/v2/commuting-involutions.pdf>`_
   * - L074: Kiefer–Leemans, *On the number of abstract regular polytopes
       whose automorphism group is a Suzuki simple group Sz(q)*;
       twelve-page author edition dated 27 September 2011
     - Both uniform counting formulas, generation, intersections, rank
       and duality; classical Suzuki structure retained
     - `Suzuki polyhedra <papers/topic-d/v2/suzuki-polyhedra.pdf>`_
   * - L104: Leemans, *The residually weakly primitive geometries of J₂*;
       five-page journal article, 2002
     - Complete 8/19/3 census and absence of higher ranks under the stated
       subgroup catalogue; printed diagrams, Aut/Cor groups and doubling
       relation excluded
     - `Hall–Janko geometries <papers/topic-d/v2/hall-janko-geometries.pdf>`_

The common paper has six pages and the three applications total thirteen.
The `twelve-page program appendix <papers/topic-d/v2/program-appendix.pdf>`_
contains eight complete mathematical programs: five required computations
and three diagnostics. The independent review checked all 37 source rows,
all 31 rendered pages and a fresh full program run. All 146 Hall–Janko
anchors terminated, and all thirty final geometries passed verification.

Ten scoped Lean declarations were freshly compiled. They cover the
stabilizer-fiber correspondence, the odd-period action argument and an
abstract rank obstruction. They do not formalize the whole source results
or the finite census. The `publication guide
<papers/topic-d/v2/PUBLICATION.rst>`_ gives attribution, qualifications,
formal boundaries and replay commands. A separately reviewed
`Lean supplement <audit/topic-d/v2/support-formal/README.rst>`_ now verifies
the generic global orbit decomposition and the full Möbius–Burnside
support formula. All 28 declaration reports passed a fresh independent
compilation; source-specific applications remain outside that supplement.
Those proof admissions add no source or solved-question credit.

The separate `length audit <audit/topic-d/v2/measurement/README.rst>`_
now gives **1.053 times** for the whole written topic and **0.660 times**
including the whole program appendix. The three source manuscripts cost
47,894 characters; our common theory costs 15,632 and the three applications
29,855. Thus the written denominator is 45,487. The complete appendix adds
27,070, giving 72,557. Its cost outweighs the written saving in this comparison.

.. list-table:: Each result after acquiring the whole common theory and programs
   :header-rows: 1

   * - Source
     - Source characters
     - Application characters
     - Conditional factor
   * - L066
     - 20,916
     - 10,989
     - 1.903
   * - L074
     - 20,661
     - 13,367
     - 1.546
   * - L104
     - 6,317
     - 5,499
     - 1.149

These use NFC characters without whitespace and count complete documents.
The individual ratios assume the whole theory and all eight mathematical
programs have already been acquired. Substituting their full raw code for
the printed appendix gives 0.668; the two representations are alternatives.
Both execution drivers are inventoried separately. Historical software,
external proofs and unextracted graphics retain unknown costs. The
`two-page calculation <audit/topic-d/v2/measurement/packet/measurement.pdf>`_
shows all denominators and qualifications.

The `paired dependency audit <audit/topic-d/v2/dag/README.rst>`_ is now
independently accepted. Its `offline explorer
<audit/topic-d/v2/dag/costs/explorer.html>`_ shows the historical and current
arguments for all 37 clauses. The 137 nodes refer to 220 exclusive passage
owners; prerequisite unions prevent shared statements from being counted twice.
Context, unused common theorems and all eight programs remain paid in the
complete comparison. The `acquisition plot
<audit/topic-d/v2/dag/costs/acquisition.pdf>`_ shows the whole common paper,
programs and three complete applications in their declared reading order.
The graph changes none of the combined or individual manuscript ratios.

Common proofs for projective groups
----------------------------------

The `current common theory <papers/topic-e/v2/umbrella.pdf>`_ proves a
classification of string markings with two proper exceptional end groups.
It derives the intersection property rather than assuming it. A common
centralizer argument and one finite quotient theorem now supply the
classification steps for three applications. Their complete statements,
proofs, borrowed inputs and source corrections are in editable TeX beside
the PDFs.

.. list-table:: Three source manuscripts and the results recovered
   :header-rows: 1
   :widths: 34 44 22

   * - Source and authors
     - Declared principal results
     - Our application
   * - L083: Leemans–Schulte, *Groups of type L2(q) acting on polytopes*
     - PSL classification, complete universal table and stated 11-cell/57-cell geometry
     - `PSL polytopes <papers/topic-e/v2/psl-polytopes.pdf>`_
   * - L079: Leemans–Schulte, *Polytopes with groups of type PGL2(q)*
     - Theorem 10: the unique rank-at-least-four case is the 4-simplex
     - `PGL polytopes <papers/topic-e/v2/pgl-polytopes.pdf>`_
   * - L021: Leemans–Toledo, *Maniplexes with automorphism group PSL(2,q)*
     - Rank and end-group restrictions, extension and infinite constructions; explicit corrections
     - `Projective maniplexes <papers/topic-e/v2/projective-maniplexes.pdf>`_

These contracts do not include every auxiliary assertion. In particular,
L079's semilinear census and the separate PGL conjectures are outside this
comparison. Exact editions, exceptions and retained classical inputs are
bound in the `proof admission <audit/topic-e/v2/admission.json>`_ and
`independent mathematical review <audit/topic-e/v2/independent_proof_review.json>`_.
The prior finite presentations and classifications retain their original
attribution. No historical priority or new solved-question claim is added.

The `three-source measurement <audit/topic-e/v2/measurement.pdf>`_ uses
complete manuscript lengths, measured in normalized non-whitespace
characters:

.. list-table:: Complete topic and conditional application costs
   :header-rows: 1

   * - Comparison
     - Factor
   * - All three source manuscripts / common theory plus all three applications
     - 1.816
   * - Same comparison including our full required finite program
     - 1.523
   * - Also include the complete diagnostic program
     - 1.372
   * - L083 / its application, after acquiring the common theory and program
     - 6.957
   * - L079 / its application, on the same basis
     - 11.271
   * - L021 / its application, on the same basis
     - 2.018

The two headline measures are the whole topic and each application after
acquiring the common theory. Required program costs are shown alongside
them.

The full written denominator is 39,303 characters: the common theory costs
19,790, followed by applications of 3,002, 1,855 and 14,656. The required
program adds 7,565 and diagnostics add 5,173. All three source manuscripts
total 71,375. Our previous proofs of these same results occupied 53,895
written characters; the new proofs remove 14,592. Including diagnostics,
the combined code is slightly longer than before. The gain therefore does
not come from discarding diagnostic code.

The earlier edition at commit ``6d203fd`` gave 1.851 overall. Clearer
explanation adds 735 characters in the current edition, charged under the
same rule. The mathematical results and programs are unchanged.

These are costs of concrete complete proofs under the stated source
contracts, not estimates of minimum mathematical complexity. Historical
program costs and external library proof costs remain unknown. The two
program-inclusive factors are known-cost comparisons. All ten length
coordinates, the fixed boundary and an independent recount are retained.
The `cost graphs <audit/topic-e/v2/costs.svg>`_ show the acquisition and
application stages; `summary.json <audit/topic-e/v2/summary.json>`_ records
the two headline measures.
The earlier `two-source audit <audit/topic-e/measurement.pdf>`_ is a
baseline of the older proofs, not the current result or a limit on what
further common ideas could achieve.

The `paired dependency graphs <audit/topic-e/v2/dag/default_view.svg>`_
show which arguments supply each result. Download and open the
`interactive explorer <audit/topic-e/v2/dag/explorer.html>`_ to switch
between historical and new proofs, inspect individual costs and expand
the branches inside a theorem. It works locally without a network connection.

Every text span has one cost owner. A theorem box sums its branches without
charging them again, and the complete manuscript totals include context
and references. Historical assertions retain their recorded qualifications.
Raw node counts alone are not complexity ratios. Separate topic umbrellas
are each charged in full even when they overlap. The exact accounting and
its limits are in the `graph review <audit/topic-e/v2/dag_admission.json>`_
and the `audit protocol <audit/protocol.pdf>`_.

Translation lattices and mixed-prime polyhedra
---------------------------------------------

The `common theory <papers/topic-affine/v2/umbrella.pdf>`_ identifies an
affine presentation and tests its distinguished subgroup intersections
uniformly over all translation periods. It includes the full kernel and
square-group proofs used in this topic.

.. list-table:: Source manuscript and recovered results
   :header-rows: 1
   :widths: 34 44 22

   * - Source, authors and edition
     - Declared principal results
     - Our application
   * - L012: Hou–Feng–Leemans, *Regular 3-polytopes of order 2^n p*;
       arXiv:2001.02945v2, 14 July 2024
     - Type restriction, arbitrary odd-factor construction, both complete
       cubic families and the exact existence range for type {6,2^s};
       one explicit auxiliary presentation correction
     - `Regular polyhedra with one odd prime factor
       <papers/topic-affine/v2/mixed-prime-polyhedra.pdf>`_

The common paper is seven pages and the application nine pages. The
`complete program appendix <papers/topic-affine/v2/required-programs.pdf>`_
adds eight pages. Independent review checked all 33 source-ledger rows,
all six programs, nine scoped Lean declarations and the full catalogue
search over 20,169 groups of order 384. A separate matrix calculation
checked the source words, translation lattices and parabolic intersections.

The `publication reader <papers/topic-affine/v2/PUBLICATION.rst>`_ states
the exact attribution, retained inputs and exclusions. The general source
classification problem is outside this recovery; the equal-label existence
question was already answered in the literature. The sign correction earns
no conjecture credit. Lean verifies the stated quotient, period and sign
lemmas; it does not formalize the complete classification.

This completed the manuscripts for one existing principal contract,
bringing that count at this stage to 22 of the fixed 27. The `length audit
<audit/topic-affine/v2/measurement/README.rst>`_ gives **0.786 times combined**:
the whole source costs 32,767 characters, against 19,070 for the common paper
and 22,638 for the application, or 41,708 together. The complete written
replacement is longer than this single source by the declared measure.

After acquiring the whole common theory and all six required programs, the
local source/application ratio is **1.447 times**: 32,767 / 22,638. The full
common paper remains charged in the combined comparison, including proofs
also used elsewhere. The complete printed program appendix adds 17,250,
giving **0.556 times** including programs. All six raw files give **0.561
times** as an alternative representation. Three auxiliary scripts and three
formal files are inventoried separately. The `two-page calculation
<audit/topic-affine/v2/measurement/packet/measurement.pdf>`_ shows the formulas,
exclusions and unknown costs.

The `paired dependency audit <audit/topic-affine/v2/dag/README.rst>`_ now
connects the historical and current proofs to their measured passages. Its
`two-page reader <audit/topic-affine/v2/dag/costs/reader.pdf>`_ and separate
`historical <audit/topic-affine/v2/dag/costs/historical_graph.svg>`_ and
`current <audit/topic-affine/v2/dag/costs/new_graph.svg>`_ graphs show which
arguments are reused. Every passage is charged once in a dependency union;
all complete-document costs and the combined and individual ratios above
remain unchanged. The audit checks 194 exclusive passage owners and 222
prerequisite unions. Node counts are not compression factors.

Odd kernels and cyclotomic polyhedra
------------------------------------

The `common theory <papers/topic-f/v2/umbrella.pdf>`_ combines an inverted
orbit, two character components and explicit cyclotomic coordinates.
These arguments supply the kernel structure, abelian classification and
nonabelian constructions in one application.

.. list-table:: Source manuscript and recovered results
   :header-rows: 1
   :widths: 34 44 22

   * - Source, authors and edition
     - Declared principal results
     - Our application
   * - L014: Hou–Feng–Leemans–Qu, *String C-groups of order 4p^m*;
       arXiv:2407.10388v1, 15 July 2024
     - Normal odd kernel and generator number; corrected abelian/tight
       classification; nonabelian examples for every stated parameter;
       exact source presentation, automorphisms and auxiliary identities
     - `Regular polyhedra with an odd kernel of index four
       <papers/topic-f/v2/odd-kernel-polyhedra.pdf>`_

The common paper has four pages and the application five. One cyclotomic
lattice calculation proves the coordinate orders and the presentation
relations, and transports the automorphisms back to the source's named
generators. This replaces its coefficient-table calculation. The original
results retain their authorship; the underlying cyclotomic arithmetic is
classical. The `publication reader <papers/topic-f/v2/PUBLICATION.rst>`_
explains the exact contribution, attribution and limitations.

The `independent review <audit/topic-f/v2/independent_review/review.pdf>`_
checked both entire proofs and all 25 source/audit records, including the
preprint's corrected marking. The tightness converse explicitly retains
Cunningham–Pellicer's classification; its complete external proof cost is
unknown. The source's introductory census and general Hughes classification
are excluded. These qualifications are part of the recovered contract.

The four-page `validation appendix <papers/topic-f/v2/program-appendix.pdf>`_
prints all three programs. They check eleven marked models and five literal
presentations, with all 64 subset intersections in each tested marking.
The written theorems hold for every stated parameter without relying on
those finite examples. Five reused Lean declarations verify the specified
subgroup intersections and group identities; the full application is not
formalized in Lean.

At that stage, the number of contracts with complete canonical applications
and common theory reached 23 of 27. It adds no source or solved-question
credit. The `length audit <audit/topic-f/v2/measurement/README.rst>`_ now
gives **1.264 times combined**: 25,115 / (7,118 + 12,744), charging the whole
common theory once. After acquiring that theory and the complete declared
validation package, the application ratio is **1.971 times**: 25,115 / 12,744.

The complete validation appendix adds 8,837 characters, giving **0.875 times**
including validation; all three raw programs give **0.899 times** instead.
Two operational drivers and the Lean file are priced separately. The
`two-page calculation <audit/topic-f/v2/measurement/packet/measurement.pdf>`_
shows every denominator, the cost graph and alternative units. These are
written-length comparisons with explicit exclusions and unknown external
costs. Paired proof dependencies and passage costs remain pending.

Flag relations and incidence residues
------------------------------------

Topic G now has one `complete common paper <papers/topic-g/v2/umbrella.pdf>`_
and two applications. The common proofs reconstruct points and lines from
relations on flags, express Steiner chambers through successive stabilizer
orbits, and use explicit Hermitian transport to identify and connect residues.
All project proofs needed by the applications are included in the edition.

.. list-table:: Two source manuscripts and their recovered principal results
   :header-rows: 1
   :widths: 34 44 22

   * - Source, authors and edition
     - Declared principal results
     - Our application
   * - L009: Delaby--Leemans--Tranchida, *Geometries with trialities arising
       from linear spaces*; Algebraic Combinatorics 9(2) (2026), 379--402
     - Triangle construction and reconstruction, corrected action
       classification, automorphisms, correlations, residues and diagrams;
       affine determinant and polarity qualifications explicit
     - `Triangle geometries <papers/topic-g/v2/triangle-geometries.pdf>`_
   * - L092: Leemans, *A generalization of a construction due to Van
       Nypelseer*; Beiträge zur Algebra und Geometrie 46 (2005), 561--574
     - Corrected classification from linear spaces and Steiner designs,
       uniform residue arguments and exceptional group data; exact parameter,
       numerical and path-convention corrections explicit
     - `Geometries from Steiner designs
       <papers/topic-g/v2/steiner-geometries.pdf>`_

The common theory occupies twelve pages and the applications eight and
twenty-two. The source ledger preserves all 79 records within the two
contracts. External classification theorems retain their attribution and
unknown full proof costs. Ancillary examples and unproved identifications
remain excluded. The `publication guide <papers/topic-g/v2/PUBLICATION.rst>`_
explains the contributions, source qualifications and review boundaries.

The `twenty-page program appendix <papers/topic-g/v2/programs.pdf>`_ prints
thirteen complete programs: four finite mathematical premises, two witness
or certificate programs and seven validations. All were independently run.
Six Lean modules supplied forty freshly checked supporting declarations;
the full geometric applications and external classifications remain outside
their formal scope. Earlier question answers are reused without new credit.

This brought the number of admitted contracts with complete canonical
applications and common theory to 24 of 27. The `length audit
<audit/topic-g/v2/measurement/README.rst>`_ now gives a combined written
factor of **0.630 times**: 73,199 source characters divided by 116,135 for
the whole common paper and both applications. After acquiring the whole
theory and all thirteen programs, the individual factors are **2.119** and
**0.378**. The complete replacement is longer overall, and the Steiner
application remains longer after acquisition. Including the complete
printed program appendix gives **0.433**; using all raw programs instead
gives **0.440**. Retained proof and graphical costs remain unknown. Paired
dependency costs are still being audited.

Recognizable extensions and finite normal pairs
-----------------------------------------------

The `common paper <papers/topic-representation/v2/umbrella.pdf>`_ proves
how recognizing the old vertices, ruling out symmetries that fix them, and
extending every old symmetry determine the full group of a constructed
graph. The application proves the graph hypotheses and recovers the exact
finite normal pair. Both scientific papers have five pages.

.. list-table:: Source manuscript and recovered results
   :header-rows: 1
   :widths: 34 44 22

   * - Source, authors and edition
     - Declared principal results
     - Our application
   * - F010: Díaz Ramos–Molinier–Viruel, *Every finite group is represented
       by a finite incidence geometry*; arXiv:2511.02410v2, 16 December 2025
     - Explicit pair encoding, chamber completion, cleaning, the finite
       normal-pair theorem, the full recursive symmetric family and the
       corrected hexagon example
     - `Finite normal pairs as incidence geometries
       <papers/topic-representation/v2/finite-normal-pairs.pdf>`_

This is an independent followup source already in the corpus; its original
results retain their authors' attribution. The `publication guide
<papers/topic-representation/v2/PUBLICATION.rst>`_ gives all six source
blocks and the three corrections: chamber degrees, the completed hexagon's
color-preserving group, and the degree-one recursive base case. The source's
own Theorem A already answers its Question 2.4; no new question is credited.

Eight new generic Lean declarations verify the restriction and extension
criterion. Four reused declarations check local hexagon facts. Concrete
graph recognition and the full representation theorem remain written
proofs. The four-page `validation appendix
<papers/topic-representation/v2/program-appendix.pdf>`_ prints both complete
bounded programs; the uniform proofs do not depend on their finite samples.

This brought the number of admitted contracts with complete canonical
applications and common theory to 25 of 27. The `length audit
<audit/topic-representation/v2/measurement/README.rst>`_ now gives
**1.015 times combined** and **1.852 times for the application**, after
acquiring the whole common paper and both validation programs. The combined
written saving is only 372 characters and reverses under UTF-8 counting,
which gives **0.971**. Including the complete printed appendix gives
**0.746**; the complete raw files are an alternative, giving **0.762**.
This does not establish a consistent saving in complete written length.
Paired dependency costs remain to be audited; no source or question credit
is added.

Chamber fibers, reflections and regular covers
----------------------------------------------

The six-page `common paper <papers/topic-chamber/v2/umbrella.pdf>`_ describes
flag extensions through double cosets, proves an explicit chamber reflection
and isolates cover intersections in the embedded relation kernels. Both
applications supply the geometric hypotheses and local group arguments.

.. list-table:: Source manuscripts and recovered results
   :header-rows: 1
   :widths: 34 44 22

   * - Source, authors and checked edition
     - Declared principal results
     - Our application
   * - L008: W.-J. Zhang and D. Leemans, *Testing chirality on hypertopes*;
       arXiv:2511.14562v1, November 2025; ten pages
     - Theorem 1.1 with both directions, residual connectedness and the
       full automorphism argument; exact coset qualification for infinite groups
     - `A two-coset criterion for chiral hypertopes
       <papers/topic-chamber/v2/testing-chirality.pdf>`_; three pages
   * - N016: Gabe Cunningham, *Chiral polytopes whose smallest regular
       cover is a polytope*; author edition of 25 July 2023; eight pages
     - All proved conclusions, including the square-torus family, five
       specified atomic families and all six groups in the minimal-cover example
     - `Chirality kernels and the smallest regular cover
       <papers/topic-chamber/v2/minimal-regular-covers.pdf>`_; six pages

The `publication guide <papers/topic-chamber/v2/PUBLICATION.rst>`_ records
the retained classifications, exact source qualifications, whole programs
and formal limits. Independent review checked all 27 scope rows, 22 proof
passages, six finite groups and fourteen scoped Lean declarations. Seven
new declarations prove the actual reflection formula; the full geometric
applications remain written mathematics.

**The historical 27 admitted contracts have complete canonical applications
and common theory.** This is a manuscript milestone within the fixed corpus,
not a claim that all 161 indexed papers or their conjectures are resolved.
The `complete length comparison <audit/topic-chamber/v2/measurement/packet/measurement.pdf>`_
now gives **0.982×** for both sources against the whole common paper and both
applications: 35,802 / (15,199 + 21,254). After acquiring the common paper
and both complete programs, the application factors are **2.877×** and
**1.024×**. Including the entire program appendix gives **0.811×**, or
**0.835×** with the raw files instead. The `component graph
<audit/topic-chamber/v2/measurement/packet/complete_costs.svg>`_ shows every
complete paper. The `numerical review <audit/topic-chamber/v2/measurement/README.rst>`_
records all exact fractions, the independent arithmetic and unit sensitivity.
Dependency costs remain to be measured. Earlier cover
answers have a separate `question map <papers/topic-chamber/v2/question_map.json>`_;
general finite minimal-cover multiplicity in all ranks remains unresolved.

Matching extensions and parity
-------------------------------

The `common theory <papers/topic-matching/v1/umbrella.pdf>`_ proves
presentations from permutation orbits, complete parity rewriting and the
needed bipartite halving argument. The common paper is six pages; the
application is seven, with a two-page complete computation appendix.

.. list-table:: Source and results recovered
   :header-rows: 1

   * - Source, authors and edition
     - Principal results recovered
     - Application and qualifications
   * - F015: Claudio Alexandre Piedade, *Infinite Families of Hypertopes
       from Centrally Symmetric Polytopes*; EJC 30(2) (2023), P2.20; 21 pages
     - All eight stated families, corrected defining presentations, orders,
       marked residues, regularity and even-parameter iteration
     - `Spherical families <papers/topic-matching/v1/spherical-families.pdf>`_;
       classical extension, lattice, toroidal and Coxeter inputs retained

Two published 120-cell presentations omit twenty pair relations. We prove
that the literal presentations define infinite groups for every stated
integer parameter, then supply the relations for the intended finite
constructions. An independent reflection-matrix calculation checks all
179,700 vertex pairs. This is a correction of published assertions, not an
open-conjecture answer. Seven reused Lean declarations check component
algebra; the geometry and presentation equivalence remain written proofs.

The `admission <audit/topic-matching/v1/admission.json>`_ adds one original.
The `publication guide <papers/topic-matching/v1/PUBLICATION.rst>`_ links the
full program and review. The `accepted length comparison
<audit/additional-measurements/v1/README.rst>`_ gives
37,951 / (16,732 + 17,168) = **1.119×** as written. Including the complete
printed program gives **0.976×**, or **0.991×** using its whole raw file.
After acquiring the full common theory and program, the application factor
is **2.211×**.

Marked coordinates and chiral enumeration
-----------------------------------------

The four-page `common theory
<papers/topic-chiral-enumeration/v1/phase282_marked_coordinate_umbrella.pdf>`_
proves the subgroup-coordinate dictionary, exact orbit searches and reflection
criterion. The nine-page application proves completeness in every rank.

.. list-table:: Source and results recovered
   :header-rows: 1

   * - Source, authors and edition
     - Principal results recovered
     - Application and qualifications
   * - L028: Buekenhout–Leemans–Tranchida, *A new algorithm to classify
       chiral polytopes with a given automorphism group*; complete revised
       fourteen-page ULB author manuscript associated with the 2021 publication
     - Complete enumeration for finite groups and connected symbols in every
       rank, exact oriented and unrooted equivalence, mathematical table columns
     - `Chiral enumeration
       <papers/topic-chiral-enumeration/v1/phase282_chiral_enumeration.pdf>`_;
       Schulte–Weiss reconstruction and the Liebeck–Shalev bound retained

The source substitution and search idea retain their original attribution.
Duality is not quotiented; historical timings are not reproduced. Independent
review read the full source and both manuscripts, freshly ran the complete
finite/formal checks, and implemented separate native rotation-pair searches.
Seven Lean declarations verify actual subgroup-coordinate and reflection
algebra; the complete algorithm and geometry are written proofs.

The `admission <audit/topic-chiral-enumeration/v1/admission.json>`_ adds one
original and no conjecture answer. The `publication guide
<papers/topic-chiral-enumeration/v1/PUBLICATION.rst>`_ gives replay commands.
The `accepted length comparison <audit/additional-measurements/v1/README.rst>`_
gives 29,599 / (8,831 + 23,171) = **0.925×** as written. Including all three
complete programs gives **0.674×** as printed, or **0.687×** as raw files.
After acquiring the whole common theory and program bundle, the application
factor is **1.277×**. The written result changes to **1.003×** in whitespace
tokens, so the small word saving is sensitive to the unit. The
`current paper catalogue <papers/latest_catalogue.json>`_ preserves these
additions separately from the earlier 27-original audit.

Orbit constructions, diagonal twistings and wreath products
-----------------------------------------------------------

The complete eight-page `common theory
<papers/topic-diagonal/v2/papers/umbrella.pdf>`_ proves the orbit construction
with general chamber stabilizers, as well as module intersections and changes
of marking by cocycles. It extends the earlier five-page N007 theory. The
whole enlarged common paper is charged once for the two originals.

.. list-table:: Source and results recovered
   :header-rows: 1

   * - Source, authors and edition
     - Principal results recovered
     - Application and qualifications
   * - N007: Piedade–Tranchida, *Coset geometries acting on their elements:
       The j-diagonals twisting*; arXiv:2608.23223v1, twelve pages
     - Both constructions, invariant quotients, exact diagram labels,
       the finite tree family and both classical polytope identifications
     - `Diagonal twistings and finite tree diagrams
       <papers/topic-diagonal/v1/diagonal-twistings.pdf>`_;
       classical Coxeter facts and named construction descriptions retained
   * - N006: Piedade–Tranchida, *The geometry of wreath and semi-direct
       products*; arXiv:2605.04646v2, twenty-two pages
     - Joins, generalized twisting, wreath products, all six signed families,
       reversal constructions, all ten affirmative sporadic cases and the
       restricted and unrestricted lamplighter geometries
     - `Joins, wreath products and reversal of polytope markings
       <papers/topic-diagonal/v2/papers/wreath_applications.pdf>`_, with
       complete `nine-case <papers/topic-diagonal/v2/papers/sporadic/sporadic_certificates.pdf>`_
       and `Harada–Norton <papers/topic-diagonal/v2/papers/harada-norton/harada_norton.pdf>`_
       notes; literal source corrections and retained classification inputs
       are explicit, while Fi22 and Fi24-prime remain outside this contract

The `N006 admission <audit/topic-diagonal/v2/README.rst>`_ adds one original,
not ten cases. Its full written application costs eight plus five plus four
pages, including references. Seventeen scoped Lean declarations pass: eight
reused and nine new. They do not formalize the whole geometry, module
generation or sporadic computations. All finite certificates independently
pass generation, full subset intersection and actual flag-product tests.
The Harada–Norton case fills an omission in the source discussion; the O’Nan
existence proof uses a direct witness because the proposed duality route fails.
This recovery adds no open-question credit. The `complete two-original
comparison <audit/diagonal-measurement/v2/packet/reader.pdf>`_ is
78,889 / (19,859 + 50,036) = **1.129×** as written. All nineteen whole
programs and witnesses plus both required decoders add 394,294 characters,
giving **0.170×**. No complete printed software alternative exists. Required
representation files (21,960,689 bytes) and listed installed files (2,516,249
bytes) are separately inventoried. The conditional factors are **1.944×**
and **1.464×**, after acquiring the full theory, software and required data.
The older N007-only factor below remains historical.

Independent review corrected our quotient argument and checked a separate
example with a nontrivial chamber kernel. Eight Lean identities and complete
finite validation pass; the geometry and presentation proofs remain written.
The `admission <audit/topic-diagonal/v1/admission.json>`_ adds one original
and no conjecture answer. The general finite-diagram question remains open
here. The preserved N007-only `complete length
comparison <audit/diagonal-measurement/v1/README.rst>`_ gives 1.007 as written,
0.884 with the full printed validation program, and 1.944 for the application
after acquiring the whole common theory and program. Word and byte units
reverse the near-unit written comparison. The `current additions catalogue
<papers/latest_catalogue.json>`_ records all subsequent admissions.

Two corrections to the rank-extension statements
------------------------------------------------

The `five pages of proofs and distinct checks
<corrections/rank-extension/v1/README.rst>`_ address two statements in
Cameron–Fernandes–Leemans, arXiv:2212.12723v2 (L019). An elementary abelian
example refutes the general endpoint converse in Proposition 2.4. A
nine-point C-marking satisfies every stated hypothesis of Theorem 6.4,
but its prescribed extension fails the intersection property: disjoint
pairs of generators produce the same nonidentity transposition.

The second example is intransitive. It does not disprove a transitive
restriction or the main stability theorem. Both corrections have complete
written proofs and independent finite models; the standard end criterion
is retained and attributed. They add no open-conjecture, full Lean or
whole-manuscript recovery credit. L019 remains in the recovery programme.
The separate `Lean certificate
<corrections/rank-extension/formal/v1/README.rst>`_ verifies the actual
output obstruction in ten declarations, using generated-subgroup closures
and kernel-checked permutation identities. The input C-property and all
source hypotheses remain written proofs.

A correction to the unrestricted HNN construction
-------------------------------------------------

An explicit rank-six coset geometry of S4 satisfies the hypotheses of
Piedade–Tranchida, arXiv:2505.24662v1, Theorem 3.35, while its prescribed HNN
output is neither flag-transitive nor a geometry. The `four-page proof and
distinct review <corrections/nonfirm-hnn/v1/README.rst>`_ give the elementary
input argument, the infinite-group identification and the failed output flag.
Independent finite validations also pass. The example is nonfirm and not
residually connected; it does not refute the restricted assertions. This is
a source-theorem correction, with no numbered-conjecture, historical-priority
or full Lean claim. N005 remains pending as a whole-paper recovery and is not counted in the
35-original numerical comparison.

Regularity of the smallest affine twist
---------------------------------------

The `three-page proof and distinct review
<corrections/affine-twist/v1/README.rst>`_ correct Example 5.11 in the same
preprint. Its twist is regular for every positive parameter, including the
parameter-one case the source calls nonregular. The proof checks the literal
quotient subgroups and retains the standard affine Coxeter realization;
independent finite validation is supplementary. This example correction adds
no whole-paper recovery, numbered-conjecture answer or compression factor.

Answers to the two Fischer cases
--------------------------------

The two possible exceptions in N006, Theorem 5.3, now have separately
reviewed answers: **Fi22:2** has a regular polytope of type **{6,13}** and
a triangular hypertope **(6,6,13)**; **Fi24-prime:2** has types **{6,35}**
and **(6,6,35)**. The `two complete proofs and case ledger
<answers/fischer-extensions/v1/README.rst>`_ include saved witnesses,
full programs, distinct mathematical review and independent coset checks.

These answer both possible-exception cases in the specified preprint edition.
The named groups and representations remain borrowed inputs; the Fi24 proof
also uses the complete maximal-subgroup classification. No historical priority
or full Lean verification is claimed. The results are separate from recovery
of the source's ten affirmative cases, add no original to the corpus and
receive no manuscript-compression factor.

Papers and verification
-----------------------

The `paper catalogue <papers/catalogue.json>`_ distinguishes the new common
proof editions from ten preserved baseline TeX papers. Other topic proofs
remain available in the archive and are material for further common
arguments, not claims of completed compression. The fixed source view is
in `audit/source_registry.json <audit/source_registry.json>`_.

The historical `completion audit <audit/completion.rst>`_ maps the earlier 27 principal
result sets to their proofs and remaining manuscript work. Its resolved
contracts use later admissions where older registry fields are stale.
The catalogue remains fixed; recovery work continues for every accessible
original. A supporting paper on
`normal kernel recognition <papers/formal/normal-kernel-recognition.pdf>`_
replaces two separate finite-order comparisons by one group-theoretic
argument. These lemmas now serve the complete Topic A applications; their
source-specific hypotheses are checked in the written proofs.

The complete `finite program <papers/topic-e/v2/required_finite.g>`_ checks
432 local markings, the six local presentations, all ten universal groups,
their required geometry and the literal correction witnesses. The
`validation program <papers/topic-e/v2/validation.g>`_ and five mutation
controls are separate. GAP's group algorithms remain an explicit trust
boundary; uniform infinite-family claims have written proofs.

The `canonical Lean library <research/case_study/formal>`_ has 100 modules.
The new `extension proofs <papers/formal/marked-involution-extension.pdf>`_
verify nine generic declarations about actual marked tuples, their string
relations and generation. They do not formalize the entire projective
classification. Two further modules prove normal-kernel recognition and
construct the explicit direct-product isomorphism, with fourteen declaration
reports. They do not formalize the applications' source presentations or
geometric conclusions. Build evidence combines the prior fresh run of 96
unchanged modules with the separately checked extension module and the two
kernel modules, followed by the separately checked commuting-retraction
module; every module is in the default build. One unchanged legacy
module uses four recorded native-evaluation axioms. The precise scopes are
in the `extension audit <audit/lean_extension.json>`_,
`kernel audit <audit/normal-kernels/admission.json>`_ and
`commuting-retraction audit <audit/commuting-retractions/admission.json>`_.
The last module proves the compatible-pair inverse for two commuting
retractions, with four checked definitions and seven checked theorems.
Application-specific deletion maps and their joint faithfulness remain
written obligations.

Build and check
---------------

Compile the papers directly from TeX, using XeLaTeX and the fonts named in
the sources::

    python3 scripts/build_papers.py --output-dir /tmp/human-compression-papers

Use a fresh output directory. Markdown and Pandoc are not build inputs.
To build particular documents, repeat ``--paper`` with their exact IDs
from ``papers/catalogue.json`` (or ``audit/protocol``). Shared TeX inputs
must be listed explicitly in the catalogue's ``tex_inputs`` field and
bound in the same proof review. The builder copies only those sources
and records their hashes; a whole source directory is never copied.
The `build review <audit/tex-build/tex_inputs_design_review.rst>`_ records
the checks and the external TeX dependency boundary.

To check both configured Lean components with one command, use the pinned
compiler and dependency cache::

    python3 -B scripts/check_project_lean.py --lean PATH_TO_LEAN --packages PATH_TO_PACKAGES --out /tmp/human-compression-project-lean --jobs 1

This runs the 100-module library checker followed by Topic B's separate
checker. It preserves each fresh report and distinguishes complete and
explicitly selected partial runs. The `runner review <audit/formal-project/README.rst>`_
records fourteen dispatch tests and a fresh Topic B check; that validation
does not claim a fresh run of all 101 sources.

Topic C has its own additional checker, which is not yet dispatched by
that runner::

    python3 -B -O papers/topic-c/v2/formal/check.py --lean PATH_TO_LEAN --packages PATH_TO_PACKAGES --out /tmp/human-compression-topic-c-lean

It checks the three Topic C files and sixteen declarations, including
seven reused declarations. Its scope is detailed in the
`publication guide <papers/topic-c/v2/PUBLICATION.rst>`_.

For the original 100-module Lake library alone::

    cd research/case_study/formal
    lake build

The portable alternative checks every module against an existing pinned
package cache. Supply the compiler and package paths and use one worker::

    python3 scripts/check_lean.py --lean PATH_TO_LEAN --packages PATH_TO_PACKAGES --out /tmp/human-compression-lean --jobs 1

See ``python3 scripts/check_lean.py --help`` for the path arguments. For
file and archive integrity, from the repository root::

    python3 scripts/verify_snapshot.py

Replay the current finite certificate and its mutation controls::

    python3 papers/topic-e/v2/check_common.py --out /tmp/human-compression-finite

Recount the fixed measurement with pypdf 6.13.0 and separately supplied
primary PDFs (their exact paths and hashes are in the protocol)::

    python3 audit/topic-e/v2/measure.py --repo . --sources-root PRIMARY_ROOT --protocol audit/topic-e/v2/protocol.json --out /tmp/human-compression-measurement.json
    python3 audit/topic-e/v2/recount.py --repo . --sources-root PRIMARY_ROOT --out /tmp/human-compression-independent.json

Recount Topic A with the same pypdf version and its separately supplied
primary PDFs::

    python3 -B -O audit/topic-a/v2/measurement/recount.py --sources-root PRIMARY_ROOT --public-root . --out /tmp/human-compression-topic-a-counts

To rebuild its measurement reader and cost graph, use the dependencies
listed in the reader manifest and a fresh output directory::

    python3 -B -O audit/topic-a/v2/measurement/reader/build_reader.py --author-pdf audit/topic-a/v2/measurement/reader/measurement.pdf --out /tmp/human-compression-topic-a-reader

Replay Topic A's proof-cost partition against the same primary PDFs and
the current published manuscripts::

    python3 -B -O audit/topic-a/v2/dag/check.py --sources-root PRIMARY_ROOT --artifacts-root . --out /tmp/human-compression-topic-a-dag

The `graph instructions <audit/topic-a/v2/dag/README.rst>`_ also describe
how to regenerate the explorer and check its controls without the primary PDFs.

Working notes and the intake archive
-----------------------------------

Markdown stays in local working directories and is not tracked on the
current branch. The 992 previously published notes remain byte-for-byte
recoverable at tag ``intake-2026-10-11``, commit
``3b067cc2eba4ac2f2f91248448727639d8ac7c5a``. The new verifier reads these
bytes from Git objects, never from surviving local notes.

The historical ``research/case_study/phase*`` and ``provenance/phase*``
artifacts document earlier editions. Their original replay scripts require
the complete archived tree. Run a historical replay in a separate checkout::

    git worktree add --detach /tmp/human-compression-intake intake-2026-10-11
    cd /tmp/human-compression-intake
    python3 scripts/verify_snapshot.py

That checkout contains its historical Markdown. Current proofs, measurements
and formalization will develop in TeX, Lean and explicit JSON ledgers.

Compression is charged honestly: each topic pays for its full umbrella once,
then its applications, interfaces and required computations. Overlapping
umbrellas are charged separately in independent topic comparisons. Answers
to open questions have a separate ledger and do not inflate recovery counts.
