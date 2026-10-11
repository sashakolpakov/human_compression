Supported kernels and finite two-group quotients
================================================

Six source contracts follow from one common paper and six applications.
The common paper is 17 pages; the applications are 4, 3, 6, 3, 6 and 11
pages. A separate 21-page appendix contains all four required programs.
These page counts describe the edition. They are not a compression factor.
The exact proof acceptance and file bindings are in ``admission.json``.

Sources and recovered results
-----------------------------

.. list-table:: The six applications
   :header-rows: 1
   :widths: 32 43 25

   * - Source and measured edition
     - Recovered results
     - Application and qualifications
   * - L032: Hou, Feng and Leemans, *On regular polytopes of 2-power
       order*. Revised author manuscript, 8 November 2019; published
       in Discrete & Computational Geometry 64 (2020), 339–346.
     - Theorem 1.2 for all stated ranks, types and orders, together with
       the necessary order bound attributed to Conder.
     - ``two-power-orders.pdf``. The particular inductive presentation
       and the separate classification question are outside this contract.
   * - L034: Hou, Feng and Leemans, *Existence of regular 3-hypertopes
       with 2^n chambers*. arXiv:1901.09034v1, 23 January 2019.
     - Lemma 3.1 and the full construction in Theorem 3.2: presentation,
       exact order, marked structure, all pair orders and hypertope geometry.
     - ``three-generator-hypertopes.pdf``. The structural parity display
       and repeated kernel word are corrected explicitly. Question 3.3
       is outside this recovery.
   * - F016: Cunningham, Feng, Hou and Schulte, *Symmetric polytopes whose
       automorphism groups are 2-groups*. arXiv:2512.15511v1,
       18 December 2025.
     - Lemma 4.1; Theorems 5.1, 5.3, 6.1 and 7.1–7.3: square sections,
       flatness, all three flat amalgamation cuts, presentation and marked
       mix, branch automorphisms and three infinite extensions.
     - ``square-sections-and-free-extensions.pdf``. The stated geometric
       assembly and extension theorems remain borrowed inputs. The
       translation coincidence in H_6 and chiral rotation amalgam are explicit.
   * - F013: Hou and Schulte, *String C-groups of 2-power order project
       onto a common string C-group*. arXiv:2605.20691v1, 21 May 2026.
     - Theorems 1.1–1.2 throughout the finite, nondegenerate range:
       a common quotient in every rank and the corresponding polytope cover.
     - ``common-two-group-quotient.pdf``. The auxiliary normal-subgroup
       and order assertions in Theorem 4.2 are corrected separately.
       The principal theorems are recovered.
   * - L035: Hou, Feng and Leemans, *Existence of regular 3-polytopes of
       order 2^n*. arXiv:1802.08947v2, 22 January 2019; published in
       Journal of Group Theory 22 (2019), 579–616.
     - Theorems 1.2–1.3: all stated existence parameters and the complete
       two, two and four families in the three high-type classifications,
       including their presentations, converse arguments and finite seeds.
     - ``high-type-two-groups.pdf``. The cyclic-core theorem and the
       finite seed computation are explicit dependencies.
   * - N009: Gomi, Loyola and De Las Peñas, *String C-groups of order
       1024*. Contributions to Discrete Mathematics 13(1) (2018), 1–22.
     - The nondegenerate marked classification, with 27 numbered source
       records, six tables, 107 comparison rows and the finite universal orders.
     - ``order-1024-markings.pdf``. Literal table and factor-pair corrections
       are stated. The specified smooth-square classification and infinite
       universal decomposition remain borrowed inputs. Geometric realizations
       and a classification of degenerate products are outside the contract.

All paper files are under ``papers/topic-a/v2``. The two source maps beside
this reader give exact locators and proof spans. Recovery here means these
stated principal contracts, including their qualifications. It does not
assert that every ancillary claim or illustration has been reproduced.

What the common arguments do
----------------------------

The common construction places each local extension in its own kernel
coordinate over a shared marked quotient. The proof isolates those kernels
and computes every marked subgroup intersection. A separate recognition
argument proves that the proposed presentations have no additional kernel.
Commuting retractions give an explicit inverse for the compatible product;
the full construction need not be repeated for that step. A further coset
argument supplies the geometric intersection condition where it is needed.

For finite two-groups on a forest, the common quotient and a finite
nilpotent quotient turn classification at fixed excess order into a bounded
search through normal kernels. Affine square models provide the local
examples. Each application still proves its particular relation checks,
normality, quotient identification and geometric conclusions. This is a
common mathematical argument with complete applications, not an inference
from similar wording or group orders.

The original existence theorems, classifications, presentations and geometric
constructions retain their attribution. N009 already used central extensions
and universal quotients; our bounded kernel parametrization does not justify
claiming that its authors searched the abstract catalogue of all groups of
order 1024. No assertion of historical priority follows from this volume.

Retained work and formal verification
------------------------------------

The common paper states its retained inputs explicitly: finite p-group
basis and nilpotence facts, graded Lie identities, Gaussian integer and
plane-tiling facts, regular-polytope correspondence, the specified geometric
assembly and free-extension theorems, Lucchini's cyclic-core theorem,
and the specified N009 square and infinite universal results. External
proof costs remain unknown where they have not been measured. Archived
combined manuscripts supply provenance rather than additional hidden premises.

The Lean library proves the specified generic kernel, generation,
intersection, coset and normal-coordinate statements. Its new commuting
retraction module constructs the actual subgroup of compatible fixed pairs,
proves surjectivity and computes the kernel, and gives an explicit group
isomorphism when the common kernel is trivial. Its eleven checked declarations
comprise four definitions and seven theorems. The concrete deletion maps
and joint faithfulness still require the written application proofs.

No complete one of these six source contracts is claimed as an end-to-end
Lean theorem. In particular, the geometric correspondence, source-specific
presentations, square and forest classifications and complete finite census
retain the written and computational evidence named in their ledgers.

Required computation
--------------------

All four complete programs are included beside their readable appendix.
From ``papers/topic-a/v2``, run::

  python3 -B -O required-code/phase78_n009_integration_run.py \
    --gap /path/to/gap --output-dir /fresh/absolute/output

Keep the four files together. GAP's NQ package is required and the output
directory must be fresh. The runner requires no Markdown, private source
text or previous census. Its exhaustive search uses universal quotients;
named groups and the source tables are comparison outputs, not filters
that could hide an omitted case. GAP's exact group and presentation
algorithms remain an explicit computational trust boundary.

The independent review freshly replayed the full census and presentation
checks and compared the source presentations and all 107 table rows.
The build review preserves the page text of every document; the final
attribution correction has its own record. Earlier staging maps are
historical records whose pending status is superseded by ``admission.json``.

Measurement
-----------

Report the complete topic and each conditional application. The topic pays
for the whole common paper once, all six applications and, in the required
program coordinate, the complete appendix once. Each conditional application
ratio assumes that the whole common paper and complete appendix have already
been acquired. Independent topics each pay for their entire common theory.

PDF text extraction omits some image labels and diagram structure, especially
in L035. The text coordinate therefore measures complete-document extractable
text, not all visible content. Missing graphic and external proof costs
remain unknown. Numerical admission and the weighted dependency audit are
separate from this proof admission.
