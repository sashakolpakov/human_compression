#!/usr/bin/env python3
"""Generate the living paper map; never modify the historical intake inventory.

The explicit updates below describe exact targets, not whole-paper inferences.
Access, encoding, rederivation and principal-result coverage are separate axes.
"""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "research/case_study"
INPUTS = ("literature_inventory.json", "compression_audit_rows.json",
          "workspace_proof_audits.json", "phase4_old_problem_intake.json",
          "older_literature_updates.json", "phase5_network_intake.json",
          "phase6_network_intake.json", "phase16_frattini_geometry_intake.json",
          "phase17_k1_source_intake.json", "phase18_schulte_weiss_intake.json",
          "phase20_linear_rank3_intake.json", "phase22_linear_priority_supplement.json",
          "phase24_L088_sources.json", "phase25_L108_intake.json", "phase25_older_access.json",
          "phase26_access.json", "phase30_source_intake.json", "phase31_cover_prior_art.json", "phase32_L003_source_intake.json",
          "phase32_L111_intake.json", "phase32_L111_scope.json",
          "phase32_L003_geometry_intake.json", "phase32_L003_universal_intake.json",
          "phase32_L111_section6_intake.json", "phase33_L003_even_intake.json",
          "phase33_L003_universal_even_intake.json", "phase33_source_status.json")

# id: status, exact target, replacement method, retained inputs, evidence paths,
# remaining work. Semicolons separate inputs and evidence paths.
UPDATES = {
    "L003": (
        "partial_progress", "Section9 rotational presentation with ((3,0),(2,0),(1,1),(s,0)); algebraic consequence near Problem9.2",
        "An exact216-state integer-voltage action proves the displayed group infinite for every positive6|s. Complete finite Schreier data describe its image as a rank-six free abelian extension of an order216 quotient. Lean proves Infinite of the literal s6 PresentedGroup; exact finite quotients216m6 of the image follow in the written proof.",
        "Standard free abelian subgroup structure and the elementary Schreier telescoping argument; Primary source presentation and parameter substitution, independently read",
        "phase32_L003_infinite_presentation.md;phase32_L003_manifest.json;phase32_L003_rank_audit.md;phase32_L003_root_audit.md;phase32_L003_root_second_audit.md;phase32_L003_formal_manifest.json;formal/Phase32L003Infinitude.scope.md",
        "Literal Problem9.2 remains unsettled by this package. Infinite presented groups can have suitable finite quotients; exact geometric residues and finite quotient conditions are separate obligations. Other parameter values, principal source results, current priority and end-to-end formalization remain unverified. No infinity marker."),
    "L111": (
        "component_rederived", "Complete Theorem4.1, including arbitrary rank and both A1/A2/A3 and B1/B2 input formulations",
        "Exact chamber and residue maps recover construction, rank-two classes, residual and strong connectivity in both directions, designated action and disjoint-pair iteration. Full parity monodromy explains the positive finite-rank cover adapter; direct path and truncation proofs extend the complete statement to arbitrary rank.",
        "Elementary graph path parity; Source graph convention and geometry axioms, including extension of arbitrary flags to chambers",
        "phase32_L111_theory.md;phase32_L111_arbitrary_rank.md;phase32_L111_scope.json;phase32_L111_manifest.json;phase32_L111_rank_audit.md;phase32_L111_root_audit.md;phase32_L111_arbitrary_root_audit.md;phase32_L111_check.json",
        "Complete primary body/PDF, remaining auxiliary statements and application tables remain outside the audited scope. Section6 is handled by a separate statement ledger with two counterexamples to indexed assertions. No principal-paper credit, matched ratio or novelty claim."),
    "L007": (
        "proposed_new_result", "Section 7 omitted even-exponent non-tight existence range, 6 <= m <= p+1",
        "Central cyclic fiber-product lift preserves intersections and forbids a reversing automorphism.",
        "Source odd-exponent seed and compatible cyclic quotient; Source nonexistence and other existence ranges",
        "central_lift_proof.md;central_lift_audit.md;formal/LiftCertificate.lean",
        "External review and priority verification. Other principal group-enumeration statements are not rederived. The source's apparent tight/non-tight typo is disclosed."),
    "L008": (
        "principal_results_rederived", "Theorem 1.1",
        "Double-coset extension fibers and cyclic matching residues derive the principal chirality criterion.",
        "Standard marked-inversion correspondence for C+-hypertopes",
        "incidence_compression.md",
        "External review; no end-to-end formalization or claim about every auxiliary result."),
    "L009": (
        "component_rederived", "Construction and symmetry results; Hermitian branch of the classification",
        "Flag relation D=(A-I)(B-I), common-neighbor reconstruction and norm-shell residues.",
        "Classification of the underlying linear spaces; Standard automorphism description of Hermitian unitals where used",
        "incidence_compression.md;incidence_certificates.json",
        "Complete the remaining underlying-linear-space classification derivations."),
    "L012": (
        "component_rederived", "Theorem 5.1 and Corollary 5.2",
        "Three affine generators, an index-48 presentation certificate and three invariant lattices.",
        "Explicit finite presentation/Schreier certificate",
        "phase2_cubic_lattices.md;phase2_cubic_lattice_check.json",
        "Other type classifications and nonexistence results remain outside this reduction."),
    "L025": (
        "proposed_new_result", "Conjecture 3.2; separate audit of Conjecture 4.5 and later Wenger claims",
        "Three matrix entries solve the Suzuki five-step word; a separate Vandermonde argument counts Wenger cycles.",
        "Exact source Suzuki subgroup/graph identification; Finite-field Suzuki matrix model",
        "suzuki_cycle_proof.md;formal/SuzukiPentagons.lean;suzuki_cycle_certificate.json;phase3_egr_conjecture_audit.md",
        "Conjecture 4.5 existence remains unresolved. Other principal statements are not all rederived. External review and priority verification remain; Lean covers the matrix word, not graph identification."),
    "L029": (
        "component_rederived", "Designated-action version of Theorem 1.1; rank-three Proposition 4.9",
        "Two cyclic matchings connect rank-two residues; generated parabolics connect higher residues.",
        "C+-intersection property; Proper-flag transitivity of the designated action",
        "incidence_compression.md",
        "The bridge from the source's full-automorphism chirality convention to the designated action remains unproved here."),
    "L030": (
        "principal_results_rederived", "Theorem 4.9; Corollaries 4.10-4.11 and principal construction",
        "K_r tensor KG(N,k), exact distances, residues and a spectral automorphism argument.",
        "Standard Kneser graph eigenspaces with their parameter hypotheses",
        "incidence_compression.md;incidence_matrix_check.json",
        "The note records corrections to two checked source displays. External review remains."),
    "L032": (
        "principal_results_rederived", "Theorem 1.2",
        "Explicit square-grid seed and independent dihedral inflations prove every allowed rank/order/type existence case.",
        "String C-group/regular-polytope correspondence",
        "compression_phase2.md;formal/CoordinateKernels.lean",
        "This existence theorem does not classify every group of the given order. Lean covers abstract kernel transport only."),
    "L034": (
        "component_rederived", "Theorem 3.2; complete proposed proof of Conjecture 3.3 in its stated parameter range",
        "The existing grid/dihedral construction is rederived. Two equivariant square maps through successive Frattini layers prove the cyclic-subgroup TPP inequality for all finite 2-groups; the odd-prime argument extends it to every finite nilpotent group. The regular-hypertope adapter gives n>=s+t+l without an additional order or class cutoff.",
        "Regular-hypertope flag transitivity and typed coset Helly identity in the geometry-to-TPP adapter; Lubotzky-Mann powerful-group power structure and factorization for the given generating list; Elementary finite-p-group and Sylow facts; The new uniform proof does not retain finite group catalogues or the marked-isobicyclic classification",
        "compression_phase2.md;phase3_order_bound.md;phase11_odd_nilpotent.md;phase14_cyclic_tpp.md;phase14_cyclic_tpp_certificate.json;phase14_cyclic_tpp_audit.md;phase14_cyclic_tpp_audit.json;phase14_cyclic_tpp_independent_audit.md;phase14_cyclic_tpp_independent_audit.json;phase14_cyclic_tpp_status.md;phase14_cyclic_tpp_status.json;phase14_powerful_source_recheck.md;formal/BinaryFrattiniActions.lean;formal/MarkedSquareDescent.lean;formal/MarkedSquareDescent.scope.md",
        "External review and current priority verification remain. The bounded search found no later resolution, but its latest explicit open checkpoint is the original 2019 source. Lean checks finite action and equivariant transport components; the group and geometric arguments remain written proofs. The source's alternate dihedral-by-dihedral quotient display is not separately verified. No whole-paper reduction or infinity marker is assigned."),
    "L035": (
        "principal_results_rederived", "Theorems 1.2 and 1.3",
        "Grid existence construction, bounded cyclic-core quotient and eight binary extension models prove completeness.",
        "Lucchini cyclic-core theorem; Burnside basis theorem; SmallGroups completeness for the order-256 census",
        "phase3_classification.md;phase3_classification_certificate.json;phase3_bounded_families.md",
        "External review; the all-parameter classification is not formalized end to end and the retained finite catalogue is not rederived."),
    "L043": (
        "proposed_new_result", "Conjectures 6.1 and 6.2; missing nonprime-field case of the introductory classification",
        "Primitive character sums, subfield/transvection position and direct trace/reversal obstructions.",
        "Multiplicative Weil bound and primitive indicator; Dickson subgroup classification; Aut(PSL2)=PΓL2; Polytope correspondence",
        "psl2_square_proof.md;psl2_chiral_corollary.md;psl2_square_witnesses_independent.json;formal/FieldIntersection.lean;formal/TransvectionIntersection.lean",
        "External review and priority verification. The character argument and full geometric consequence are not formalized; other published principal results are not all rederived."),
    "L048": (
        "proposed_new_result", "Odd-characteristic PSL4 maximum rank four; exact conjecture read in L120, Conjecture 2, Section 5.7",
        "Projective commutator forms, Pauli supports, endpoint Jordan algebras and a three-endpoint intertwiner obstruction exclude every rank above four. The same proof gives a bilinear-form alternative for finite irreducible connected projective string actions in dimension four.",
        "Published Brooksbank-Leemans rank-four existence; Elementary-abelian projective representation dimension bound; Written finite-field/projective identifications",
        "phase8_psl4_rank6.md;phase3_psl4_rank7.md;phase3_psl4.md;phase7_psl4.md;phase7_psl4_zero_product.md;phase7_psl4_zero_product_audit.json;formal/StringIntersection.lean;formal/IntertwinerSeparation.lean;formal/IntertwinerSeparation.scope.md",
        "Complete written argument with internal independent review and exact symbolic checks; publication priority and external review remain. The original L048 rank-four construction is retained, not rederived; this is no whole-paper reduction. Lean formalizes specified components only."),
    "L050": (
        "component_rederived", "Orthogonality, LCD and complement-dual assertions",
        "Adjacency identities and complementary projections over F3.",
        "Source graph parameters; F017 already gives a relevant general regular-graph LCD result",
        "incidence_compression.md",
        "Ranks, minimum distances, weight enumerators and invariant-module classifications remain."),
    "L052": (
        "proposed_new_result", "Problems 9.3 and 9.4 under the standard parabolic coset construction",
        "Thin chamber-orbit closure and a direct rank-three residue argument.",
        "Exact standard coset construction and geometry assumptions",
        "coset_geometry_obstructions.md;hypertope_questions_independent_audit.md;formal/ChamberOrbit.lean",
        "External review and priority verification. Other questions and principal constructions are not all rederived."),
    "L063": (
        "component_rederived", "Complete A4-A4 family in Table 5; relevant Table 2 comparison",
        "Additive torsor F_(3^e)/F3, sign/Frobenius orbits and nonfree Frobenius correction.",
        "Dickson subgroup classification; Aut(PSL2)=PΓL2",
        "classification_compression.md;classification_field_orbits.log",
        "Other subgroup rows and completeness remain. Composite-degree extensions are not RWPRI. The ordered/unordered discrepancy is version-specific."),
    "L066": (
        "principal_results_rederived", "All four principal counting and degree-six polyhedron results",
        "Five C2^2-action multiplicities, rational generating functions and an exact degree-six orbit certificate.",
        "Automorphisms of symmetric/alternating groups including degree-six exceptions",
        "commuting_pairs_compression.md;elementary_action_theorem.md;commuting_pairs_formula_check.json;phase9_L066_matched_proof.md;phase9_L066_measurement.md;phase9_L066_measurement_protocol.json",
        "External review; no priority claim for classical orbit, Burnside or Möbius ingredients. The first matched-proof ratio measures only Theorems 1.1/1.2 outside degree six, conditional on the declared common background; it is not a whole-paper ratio."),
    "L074": (
        "principal_results_rederived", "Theorems 1 and 2: distinct commuting-involution pair count and complete Suzuki polyhedron count, with nondegeneracy",
        "Unique normalized triples (z(1),wz(c)w,z(b)) turn inner-conjugacy classes into two field coordinates. Their joint field is exactly the generated Suzuki subgroup. Frobenius and duality orbits give both counts, with an all-parameter derivation of the published nested lambda/psi formula.",
        "Classical Suzuki maximal-subgroup types, root/torus centralizers, ovoid action, subfield embeddings, automorphism group and simplicity; String C-group/regular-polytope correspondence; Exact finite-field and GAP algorithms only for the separate finite diagnostics",
        "phase10_suzuki_marked_fields.md;phase10_suzuki_marked_intake.json;phase10_suzuki_marked_fields_independent_audit.md;phase10_suzuki_marked_fields_independent_audit.json;phase10_suzuki_marked_fields_check.json;phase10_suzuki_marked_groups_check.json;phase10_suzuki_marked_fields_independent_run.json;phase10_suzuki_marked_groups_independent_run.json;formal/InvolutionCentralizers.lean;formal/InvolutionCentralizers.scope.md",
        "Both principal counts are recovered for every stated odd field exponent. Classical Suzuki structure remains an input. No whole-paper proof-length ratio, end-to-end formalization or novelty claim; external review remains."),
    "L085": (
        "component_rederived", "Full principal rank/existence theorem as restated in L074, Theorem 3",
        "Centralizers force a nontrivial central string generator in every rank at least four. A full-field normalized triple gives rank-three existence, and the odd outer quotient excludes involution generation in every proper almost-simple extension.",
        "Classical Suzuki involution and odd-element centralizers, maximal-subgroup types, ovoid action, compatible subfield embeddings and simplicity; Aut(Sz(2^N))/Sz(2^N) has odd order N; String C-group/regular-polytope correspondence",
        "phase10_suzuki_marked_fields.md;phase10_suzuki_marked_intake.json;phase10_suzuki_marked_fields_independent_audit.md;phase10_suzuki_marked_fields_independent_audit.json;phase10_suzuki_marked_groups_check.json;formal/InvolutionCentralizers.lean;formal/InvolutionCentralizers.scope.md",
        "The exact principal theorem is read in the primary L074 restatement. The original L085 full body remains unavailable, so its auxiliary statements and original proof are not compared and no whole-paper reduction is claimed. External review remains."),
    "L120": (
        "partial_progress", "Conjecture 2, section 5.7: proposed odd-PSL4 maximum four; Problem 7: odd linear intermediate groups have rank at most four",
        "The dimension-four form alternative combines with a monomial torus obstruction, transvection equations and the self-centralizing simple socle. The upper bound also applies to PSU4(q)<=G<=PGU4(q). A uniform matrix template generates SU4(q) for q=1 mod4 and has projective IP whenever the middle order is q^2-1 or q^2+1, using two auxiliary forms and a regular-torus bound. An elliptic primitive-character sieve and 406 independently checked field witnesses prove parameter existence for every odd q=1 mod4; characteristic three uses the rational curve from phase twelve. A second sphere template, twisted norm curve and primitive sieve cover q=3 mod4, q>=7, with 1699 independently checked exceptional parameter records and full q7/q11 finite group certificates. Together these prove maximum rank four for every odd q>=5. The failed-IP control remains.",
        "Written phase-eight structural theorem; Simplicity of the natural socles; Published rank-four existence for PSL4 and rank-three existence for odd PSU4(q), q>=5; PGL2 maximal-subgroup classification, rank-one unitary identification and perfection; Standard projective unitary order formula and GAP exact finite-field, matrix, orbit and subgroup algorithms; Katz Euler/trace/weight and Lang character-sheaf machinery; Hasse-Weil for the smooth genus-one curves; The stated symplectic torus list and recursive string C-group IP criterion; Exact primitive sieves and all 406 first-family and 1699 second-family exceptional parameter records",
        "phase9_linear_unitary.md;phase9_linear_unitary_intake.json;phase9_linear_unitary_audit.md;phase9_linear_unitary_status.md;phase8_psl4_rank6.md;formal/TransvectionForms.lean;formal/TransvectionForms.scope.md;phase10_unitary_matrix_certificate.md;phase10_unitary_matrix_intake.json;phase10_unitary_matrix_check.json;phase10_unitary_matrix_independent_audit.md;phase10_unitary_matrix_independent_run.json;phase11_unitary_template.md;phase11_unitary_intersection.md;phase11_unitary_manifest.json;phase11_unitary_examples_root_check.json;phase12_unitary_parameters.md;phase12_unitary_root_audit.md;phase12_unitary_root_audit.json;phase13_unitary_elliptic.md;phase13_unitary_sieve.md;phase13_unitary_manifest.json;phase13_unitary_independent_check.json;phase13_unitary_sieve_independent_audit.md;phase13_unitary_priority_audit.md;phase13_root_review.md;phase14_unitary_q7.md;phase14_unitary_q7_check.json;phase14_unitary_q7_root_check.json;phase14_unitary_q7_manifest.json;phase15_unitary_sieve.md;phase15_unitary_generation.md;phase15_unitary_intersection.md;phase15_unitary_parameter_reduction.md;phase15_unitary_curve.md;phase15_unitary_manifest.json;phase15_unitary_independent_audit.md;phase15_unitary_sieve_independent_check.json;phase15_unitary_witnesses_independent_check.json;phase15_unitary_q11.md;phase15_unitary_q11_root_check.json",
        "Problem 7 concerns linear socles and remains incomplete for field and graph extensions. The odd linear diagonal interval has maximum rank four at socle index one or two; index four forbids involution generation. A separate companion theorem now gives maximum rank four for the diagonal index-two unitary extension at every odd q>=3. Rank-three existence is now supplied for the diagonal unitary index-two extension at every odd q>=3, with a separate finite q3 base. The new linear template supplies rank three for the proper index-two group at q=1 mod4 and also independently constructs the already published q=3 mod4 range. With the retained q3 case and earlier rank-four/upper-bound results, every odd linear diagonal index-two extension has rank set {3,4}. A possible 2026 thesis and further source overlap remain priority leads. The two curve/sieve constructions give the simple PSU4(q) rank set {3,4} for odd q>=5, retaining published rank-three existence; PSU4(3) itself has no representation by retained published input. All generation, intersection and character arguments retain their stated inputs. Other survey targets are not collectively settled. Conjecture 2 is cross-referenced under L048, not counted twice; publication priority and external review remain."),
    "L088": (
        "principal_results_rederived", "Six principal construction Theorems 3.2, 4.2, 5.2, 5.4, 6.2, 7.2 and their generation lemmas",
        "One odd-endpoint overlap criterion and a central involution twist generate all six source-defined markings from one explicit seed. Typed coset Helly, panel and residue recognition are proved separately; a presentation order sandwich identifies the seed.",
        "GAP exact group and completed Todd-Coxeter algorithms; TomLib named J1 group only; Spherical Coxeter [3,5] order120; Introductory exhaustive six-only/no-higher-rank classification retained, not rederived",
        "phase24_L088_theory.md;phase24_L088_sources.json;phase24_L088_certificate.json;phase24_L088_manifest.json;phase25_L088_rank_audit.md;phase25_L088_rank_audit.json;formal/EndpointDoublingIntersections.lean;formal/EndpointDoublingIntersections.scope.md",
        "All six principal new constructions and generation lemmas are recovered. The introductory exhaustive classification is quoted background, and Section8 does not become an exhaustive new search. Printed Gamma3/Gamma4 figure labels are transposed relative to their defining sections. Lean proves the mixed-intersection bridge only; geometric Helly and J1 computations remain separate. No matched ratio, novelty or source-correction priority claim."),
    "L108": (
        "principal_results_rederived", "Theorem1, Lemma3.1 definition adapter, Lemma3.2(i),(iii),(iv), with the unconditional part(ii) explicitly corrected",
        "Retain the kernel of the action on vertices and edges. Thin connected residues force one commuting pair; the resulting marking proves thin-case regularity, faithfulness, automorphism equality and biduality, also for infinite groups.",
        "Elementary group actions, dihedral normal forms and incidence connectivity; Conventional map/Petrie-walk definition",
        "phase25_L108_reduction.md;phase25_L108_intake.json;phase25_L108_check.json;phase25_L108_manifest.json;phase25_L108_rank_audit.md;phase25_L108_rank_audit.json",
        "The principal obstruction follows from thinness of the Petrial alone. Literal unconditional automorphism inclusion and the nonthin length/order assertion have explicit counterexamples and are not counted as proved. External atlas classifications and examples are not reproduced. No matched ratio, full Lean proof or correction-priority claim; external review remains."),
    "L092": (
        "proposed_new_result", "Conjecture 1, Section 4.6, p. 569",
        "An SU(2,q) norm-shell torsor and generating root-group moves connect the difficult residue.",
        "Specified elementary Hermitian and finite-field facts; Separate chamber/panel verification for Construction 3",
        "hermitian_unital_proof.md;hermitian_unital_check.log;formal/ResidueConnectivity.lean",
        "External review and priority verification. Other constructions and applications in the paper are not all rederived; Lean checks abstract connectivity only."),
    "L096": (
        "generic_encoding", "Sections 2-3 shadow-IP decision problem and known rank-two characterization",
        "An exact Boolean flag-witness criterion and orbit reduction, distinct from C-group subgroup IP.",
        "Exact source shadow/residue conventions; Actual admissible flag data",
        "phase4_shadow_ip.md;phase4_shadow_ip_check.json;phase4_shadow_ip_audit.json",
        "The original Magma implementation and sporadic classification tables are not rerun. No performance claim or whole-paper reproduction is made."),
    "L102": (
        "proposed_new_result", "Section 5.1.2 uniqueness question; existence and uniqueness of spaces in Theorem 6.1(1)",
        "Prime local orbit degree and cyclic semilinear descent force a Desarguesian spread; the scalar affine action realizes every admissible prime-repunit case.",
        "Source Proposition 5.2 translation/spread reduction; Two-sided local primitivity in the one-dimensional affine semilinear case",
        "phase4_old_problem_audit.md;phase4_spread_descent_audit.md;phase4_spread_descent_check.json",
        "External review and priority verification. This identifies the spaces in the narrow source case, not every possible acting subgroup, all flag-transitive spread spaces, or the other principal classification cases."),
    "L098": (
        "component_rederived", "The firm/FT/RC/RWPRI/(IP)2/(2T)1 M23 census stated in the primary abstract and later primary tables",
        "The common panel engine exhausts all 204 Borel anchors and gives 4,13,21,10 classes in ranks two through five, then none; all 48 witnesses pass independent recognition and the archived higher-rank list matches exactly.",
        "Complete M23 subgroup catalogue from GAP TomLib; GAP exact group algorithms; Explicit Aut(G)/type equivalence convention",
        "phase7_sporadic_theory.md;phase7_sporadic_source_audit.md;phase7_sporadic_M23_2T_certificate.json",
        "Original article body and supplement conventions remain unavailable; no claim to reproduce every construction or diagram. Catalogue completeness is retained; no whole-paper or novelty claim."),
    "L101": (
        "component_rederived", "The firm/FT/RC/RWPRI/(IP)2/(2T)1 M22 census stated in the primary abstract and later primary tables",
        "The common panel engine exhausts all 156 Borel anchors and gives 7,25,16,9 classes in ranks two through five, then none; all 57 witnesses pass independent recognition and the archived higher-rank list matches exactly.",
        "Complete M22 subgroup catalogue from GAP TomLib; GAP exact group algorithms; Explicit Aut(G)/type equivalence convention",
        "phase7_sporadic_theory.md;phase7_sporadic_source_audit.md;phase7_sporadic_M22_2T_certificate.json",
        "Original two-page article body and supplement conventions remain unavailable; no claim to reproduce every construction or diagram. Catalogue completeness is retained; no whole-paper or novelty claim."),
    "L104": (
        "principal_results_rederived", "Complete principal census: 8 rank-two, 19 rank-three, 3 rank-four geometries, and no higher ranks",
        "Arbitrary-Borel panel augmentation exhausts all ranks; normalizer permutation actions and full automorphism/type fusion recover the census without source geometry lists.",
        "Complete J2 subgroup-class data from GAP TomLib; GAP exact finite-group algorithms; Written arbitrary-rank recognition and completeness theorem",
        "phase5_j2_theory.md;phase5_j2_certificate.json;phase5_j2_progress.json;phase5_j2_root_review.md",
        "The subgroup catalogue and every secondary supplement annotation are not rederived. No end-to-end Lean formalization; external review remains."),
    "L105": (
        "component_rederived", "M12 broader RWPRI/(IP)2 census and rank-five conclusion stated in the abstract",
        "The common primitive-panel engine exhausts all Borel anchors: 13,21,20,1 classes in ranks two through five, then none; all 55 representatives independently recognized.",
        "Complete M12 subgroup catalogue from GAP TomLib; GAP exact group algorithms; Explicit Aut(G)/type equivalence convention",
        "phase6_sporadic_theory.md;phase6_sporadic_source_audit.md;phase6_sporadic_M12_certificate.json;phase6_sporadic_M12_archive_compare.json",
        "Original full text unavailable; its corrected J1 entry has not been identified. M12's old summary-table discrepancy and archive omission are version-specific observations, not a claim of correcting the unread article."),
    "L124": (
        "component_rederived", "No RWPRI/(IP)2 M12 geometry of rank at least six, as stated in the primary abstract",
        "Complete primitive-panel augmentation terminates at empty levels for every Borel and derives the rank-five maximum.",
        "Complete M12 subgroup catalogue from GAP TomLib; GAP exact algorithms; Uniform written recognition and exhaustion theorem",
        "phase6_sporadic_theory.md;phase6_sporadic_source_audit.md;phase6_sporadic_M12_certificate.json",
        "Chapter body unavailable; individual constructions and the original sixteen-page proof have not been compared. Catalogue completeness is retained, not rederived."),
    "L125": (
        "component_rederived", "The firm/FT/RC/RWPRI/(IP)2 J1 classification problem stated in the primary abstract",
        "The same primitive-panel engine gives 22,8,2 classes in ranks two,three,four and none higher, exhausting all 40 Borel anchors and independently recognizing every witness.",
        "Complete J1 subgroup catalogue from GAP TomLib; GAP exact algorithms; Explicit Aut(G)/type equivalence convention",
        "phase6_sporadic_theory.md;phase6_sporadic_source_audit.md;phase6_sporadic_J1_certificate.json",
        "The original chapter and its exact entry-by-entry equivalence convention remain unavailable. L105's correction is recorded but its exact old missing entry is not identified. No whole-paper or novelty claim."),
    "L109": (
        "component_rederived", "Complete all-rank three-family classification and counts quoted in L110 Theorem 4; rank-two theorem quoted in L114 Theorem 5.1",
        "Rank-two rigidity upgrades RWPRI to every parabolic edge being maximal; dihedral subgroup arithmetic gives three patterns, CRT Helly and an all-rank counting formula.",
        "Elementary subgroup structure of cyclic and dihedral groups; Exact equivalence convention retains the specified group action",
        "phase5_dihedral_classification.md;phase5_dihedral_check.json;phase5_dihedral_audit.md;phase5_dihedral_intake.json",
        "L109 full text remains unavailable; its complete all-rank principal classification is available in the primary L110 restatement, but every original statement has not been compared. No new-conjecture or whole-paper claim."),
    "L110": (
        "partial_progress", "Rank-three shape decisions; rank-four Construction 6 types; all parameterized existence assertions of Constructions 8,9,11; uniform nonmaximality for intended Construction 10; literal Theorem 5 omitted pure-subfield boundary",
        "Compatible binary tori, Lang descent and independent coset coordinates give all-rank geometries. Pure subfields are RWPRI exactly when the bottom exponent exceeds one. Mixed-parabolic overgroups form a scalar-subspace lattice, uniformly obstructing Construction 10's prescribed intersections.",
        "Lang–Steinberg surjectivity; Standard exceptional Suzuki endomorphism; Classical torus/subfield maximality and involution centralizers; Schur–Zassenhaus complement conjugacy; Exact source parameter restrictions",
        "phase8_suzuki_subfields.md;phase8_suzuki_subfields_intake.json;phase7_suzuki_descent.md;phase7_suzuki_torus_families.md;phase7_suzuki_intake.json;formal/CosetCoordinates.lean;formal/CosetCoordinates.scope.md;phase6_suzuki_realization.md;phase5_suzuki_higher.md",
        "A corrected exhaustive classification, other higher-rank constructions and arbitrary relative embedding classes remain. Construction 10 bare intersections exist but fail RWPRI; its geometry/FT is not asserted. Original whole-paper reduction, publication priority and external review remain."),
    "L114": (
        "proposed_new_result", "Theorem 5.5 exhaustiveness: explicit omitted geometry in Sz(2^15); decisions for every printed shape in Theorems 5.3 and 5.5",
        "A common binary F16 algebra gives commuting order-13/order-41 matrices, with exact intersections 52,164,20 and 4. Classical maximality proves RWPRI; factorization proves flag transitivity. The earlier per-shape decisions remain separate.",
        "Standard Suzuki matrix/Bruhat model; Torus-normalizer and prime-degree subfield maximality; Candidate-list completeness is withdrawn, not retained",
        "phase6_suzuki_realization.md;phase6_suzuki_torus_check.json;formal/RankThreeFactorization.lean;formal/RankThreeFactorization.scope.md;phase5_suzuki_higher.md;phase5_suzuki_independent_audit.md",
        "A corrected exhaustive list, relative embedding classes and publication priority remain unresolved. The exact counterexample is internally reviewed and computationally checked; Lean covers its abstract Helly implication, not the matrix instantiation. Historical phase-five completeness assumptions are superseded."),
    "L089": (
        "component_rederived", "Advertised characterization of inductively minimal geometries with geometric intersection property",
        "Tree-cut geometry has shadow-IP in every residue exactly for paths: a claw residue obstructs it and Boolean intervals provide at-most-two-vertex witnesses.",
        "Foundational 1997 classification of inductively minimal pairs; Known transposition-tree model",
        "phase5_tree_cuts.md;phase5_tree_check.json;phase5_tree_audit.md;formal/BooleanShadow.lean;formal/BooleanShadow.scope.md",
        "Full 2005 text unavailable; target is the primary abstract and exact earlier restatement. Foundational classification retained, no new-resolution claim."),
    "N001": (
        "principal_results_rederived", "Four parts of Theorem 1: RWPRI/(2T)1/(IP)2, even-rank PRI, QPRI/middle criterion, and RPRI/complete-diagram criterion",
        "Forest component groups and two-block stabilizers reduce all property tests to leaf cuts, balanced cuts and stars.",
        "Foundational 1997 classification and uniqueness of inductively minimal pairs; Known transposition-tree model",
        "phase5_tree_cuts.md;phase5_tree_check.json;phase5_tree_audit.md;phase16_older_source_access.md",
        "Foundational classification remains an input. The complete indexed primary text is now read, including the formerly missing proof sections; the original PDF remains unavailable. No end-to-end Lean proof or numerical compression ratio. External review remains."),
    "N002": (
        "component_rederived", "Tree correspondence announced in the primary abstract",
        "An explicit maximal-clique reconstruction converts the foundational diagram conditions into a unique tree; tree-cut geometry realizes it.",
        "Foundational 1997 uniqueness/classification theorem; Classical enumeration of unlabelled trees where numerical counts are used",
        "phase5_tree_cuts.md;phase5_tree_check.json;phase5_tree_audit.md",
        "Source full text unavailable; no full-paper comparison or novel resolution of its historical direct-construction question."),
    "N003": (
        "principal_results_rederived", "All eight numbered results: finite-group Theorems 1.1 and 3.1; n>=7 Theorem 2.1, Corollaries 2.2-2.4, Theorem 3.2 and Corollary 3.3",
        "Forest cut intersections reconstruct both maximal generator families. The sign kernel gives all subgroup meets; weighted laminar cuts with a parity type give both geometries. Module, counting, overgroup and panel adapters recover the remaining numbered results.",
        "Whiston maximum independent-family bound and equality-generation assertion W1; Exact Whiston omission-subgroup trichotomy W2, retaining CFSG dependence; Cayley labelled-tree count; Standard G1-G4 coset-geometry criteria",
        "phase15_N003_matched_proof.md;phase15_N003_measurement.md;phase15_N003_measurement_protocol.json;phase15_N003_measurement.json;phase15_N003_matched_audit.md;phase15_N003_measurement_scope_audit.md;phase15_N003_scope_check.json;phase12_N003_reduction.md;phase12_N003_source_scope.json;phase12_N003_check.json;phase12_N003_root_audit.md;phase12_N003_root_audit.json;phase12_N003_root_check.json;phase5_tree_cuts.md;phase6_weighted_tree.md",
        "The retained Whiston inputs are not rederived, and the proof is not CFSG-free. Unnumbered small-degree exceptional computations and open questions are excluded. General bounds are assessed for finite groups. The matched ratio 9680/7260=4/3 covers all eight numbered targets under the declared common background, with independent proof and accounting audits; it is not a whole-paper or corpus ratio. No complete Lean formalization; external review remains."),
    "F013": (
        "principal_results_rederived", "arXiv:2605.20691v1, Theorems 1.1 and 1.2; separate counterexamples to Theorem 4.2(c),(d),(e), with C defined by equations (7)-(9)",
        "Graded Lie support separation and descending factorization across disjoint parabolics prove independent edge commutators modulo gamma3 for every finite 2-group with a forest diagram and marked IP. An explicit graph cocycle identifies the canonical quotient; paths recover the complete common-quotient and polytope-covering statements. The earlier path examples still contradict the specified Frattini-intersection kernel assertions.",
        "Burnside basis theorem; Ordinary lower-central graded Lie construction and generation in degree one; Finite nilpotency; Standard marked C-group/regular-polytope covering correspondence; Elementary square collection for the separate auxiliary counterexamples",
        "phase15_graded_support.md;phase15_graded_support_scope.md;phase15_graded_support_certificate.json;phase15_graded_support_independent_audit.md;phase15_graded_support_root_audit.md;phase15_quotient_ip.md;phase15_quotient_ip_certificate.json;phase12_path_cocycle.md;phase12_path_cocycle_check.json;phase12_hou_schulte_independent_audit.md;phase12_hou_schulte_independent_audit.json;phase12_hou_schulte_root.log",
        "Both identified principal results are recovered without a class cutoff; the false auxiliary kernel assertions are not repaired. This is a replacement proof of an already stated theorem, not resolution of a conjecture left open by that source. Forest-extension priority and external review remain unverified. No matched-length ratio, end-to-end Lean proof or infinity marker."),
    "F016": (
        "principal_results_rederived", "Theorems 5.1(a-d), 5.3, 6.1(a-b), and 7.1-7.3; Lemma 4.1 relative to square-torus classification",
        "Boolean deletion maps give marked IP and split kernels. Compatible path and two-branch fiber products recover the finite regular and alternating semiregular constructions, orders and flatness. A four-marker identity gives the entire finite presentation; an amalgam normal-form argument proves the three infinite-extension torsion statements under the source's convention.",
        "Regular-polytope/string-C-group correspondence; Classification of regular square maps by invariant translation lattices; Monson-Schulte tail-triangle construction and full-automorphism criterion; The three geometric universal-extension/amalgam identifications; Amalgam normal-form theorem",
        "phase16_fiber_products.md;phase16_fiber_products_certificate.json;phase16_fiber_products_independent_audit.md;phase16_fiber_products_independent_audit.json;phase16_fiber_products_check.json;phase16_fiber_products_independent_run.json;formal/BooleanRetractions.lean;formal/BooleanRetractions.scope.md;phase16_fixed_excess.md;phase16_fixed_excess_certificate.json;phase16_fixed_excess_independent_audit.md;phase16_fixed_excess_independent_audit.json",
        "All six identified principal theorems are recovered with the stated geometric inputs. Quoted earlier constructions, the full geometric bridges and every informal remark are not rederived. Lean proves Boolean range intersections and the four-marker implication only. The fixed-excess core theorem is a companion application, not additional paper credit. No matched-length ratio or priority claim; external review remains."),
    "N008": (
        "principal_results_rederived", "Theorem 2.1 in finite-group scope; Theorem 3.1 including infinite groups; Proposition 3.2, Corollary 3.3, Theorem 3.4, Proposition 3.5, Lemma 3.6, Proposition 3.7, Theorem 3.8 and the Section 4.2 residue Frattini test",
        "An irredundant subgroup-intersection family with one maximal chain contains the Frattini subgroup in its Borel. Exact coset-kernel transport gives the quotient correspondence; an elementary coordinate basis classifies every finite-p-group example. Relative generation and deletion tests give the finite generating-set theorem.",
        "Elementary subgroup correspondence and the Frattini definition; Finite-p-group Frattini quotient is elementary abelian; Zorn's lemma for the relatively finitely generated infinite-group case",
        "phase16_frattini_geometry_reduction.md;phase16_frattini_geometry_intake.json;phase16_frattini_manifest.json;phase16_frattini_root_audit.md;phase16_frattini_root_audit.json;phase16_frattini_coordinate_check.json;phase16_frattini_root_check.json;phase16_older_source_access.md",
        "Scope is all principal new geometric results and the finite relative-generating-set theorem. The unqualified infinite-group converse of Theorem 2.1 requires an extra hypothesis; its explicit scope counterexample is separate from correction priority. Quoted Gaschütz Theorem 4.1, historical SmallGroups counts and Frattini-computation algorithms are not rederived or rerun. No matched ratio or end-to-end formalization; external review remains."),
    "N009": (
        "principal_results_rederived", "Complete principal nondegenerate order1024 classification in all ranks, named facets and universal orders; central-extension and exceptional-presentation mechanisms; every numbered item and table mapped, with explicit literal-source qualifications",
        "A dihedral product normal form and Burnside basis exclude the bad central quotient; an order sandwich proves the three relator-lift cases. The universal class-five path group, complete invariant index-two kernel ladder and exact kernel-profile IP test recover all rank-four marked groups. Reversal gives every source type count. Two direct Todd-Coxeter computations prove the exceptional presentations have order1024, and the complete census proves there are exactly two with the specified oriented facets. The prior first-excess classification already recovers the rank-five counts.",
        "Reviewed canonical forest quotient and class bound; Burnside basis theorem and elementary dihedral facts; GAP/NQ universal nilpotent-quotient and exact subgroup algorithms; Todd-Coxeter coset enumeration; Earlier first/second-excess uniqueness of the two named rank-three facets",
        "phase21_central_quotient.md;phase21_N009_presentations.md;phase21_N009_manifest.json;phase21_N009_presentations_certificate.json;phase21_N009_source_compare.json;phase21_kernel_ladder.md;phase21_rank4_census.json;phase21_kernel_root_audit.json;phase17_k1_classification.md;phase17_k1_source_intake.json;formal/PrincipalKernelIntersections.lean;formal/PrincipalKernelIntersections.scope.md",
        "Principal classification and constructive mechanisms recovered: rank2/3/4/5 counts1/125/105/8, with higher ranks excluded. All27 numbered items and six tables have an explicit ledger. Quoted lattice classification, universal-polytope interpretation, infinite decomposition and standard IP criteria remain inputs. Literal Corollary3.7 stops at order8; Table4 e/f/h require the recorded RHS repairs; four Table6 labels retain an explicit dual-orientation interpretation. Geometric realizations, correction priority, a matched proof-length ratio and end-to-end formalization remain outside this credit."),
    "N011": (
        "source_theorem_retained", "Theorem 2, printed p.248: exact PGL_n(q) commuting-pair involution-generation criterion",
        "Retain the published theorem. In dimension four and odd characteristic it gives PGL4(q) rank-three existence exactly for q=3 mod4, using the source's rank-three adapter.",
        "Markovskaya–Nuzhin Theorem 2 and its source proof; Same-marking rank-three intersection principle",
        "phase20_linear_rank3_intake.md;phase20_linear_rank3_intake.json;phase20_unitary_rank3_status.md",
        "Selected statement, preliminary passages and the n4 construction on pp256-258 read; no complete source-proof audit or rederivation credit. The related N012 thesis now supplies an earlier public claim for the proper index-two subgroup at q=5 mod8, with a defect in its printed witness. The q=1 mod8 group in that thesis is a different central extension. No source compression or infinity-marker credit."),
    "N012": (
        "related_only", "Theorem 4.3.1 and Corollary 4.3.1, pp70–75; printed n4 witness p72; Theorem 3.3.1 as context",
        "Identify Q4=GL±4/Z(SL4): it is the diagonal index-two group for q=3 mod4 and q=5 mod8, but PSL4 times C2 for q=1 mod8. The printed beta has noncentral square and projective order four. This records a prior claim and a limited witness defect, without deciding the existence theorem from that defect.",
        "Primary thesis definitions and stated claims; Elementary determinant and scalar-center calculations",
        "phase22_linear_priority_supplement.md;phase22_linear_priority_supplement.json;phase22_linear_priority_audit.json;phase22_root_audit.json",
        "Selected sections only, not a whole-thesis proof audit. No theorem rederivation, principal-result, matched-ratio or novelty credit. The separate 2026 subscription article remains an unexhausted lead; q=1 mod8 priority remains unverified."),
    "N010": (
        "partial_progress", "Problem 30, printed p.19: restricted regular two-group components",
        "Canonical bounded cores classify ordered nondegenerate regular two-group markings at fixed excess. A global marked-kernel basis gives every class-at-most-three marking in every rank, with a two-state transfer formula and Fibonacci total. Separated first-excess cores give the unrestricted leading coefficient 5^k/k! and a lower-degree higher-class contribution.",
        "Actual marked intersection property and nondegenerate path condition; Reviewed forest quotient and canonical central attachment; Elementary edge/triple seed covers; Regular-polytope/string-C-group correspondence",
        "phase18_schulte_weiss_intake.md;phase18_schulte_weiss_intake.json;phase18_class_three.md;phase18_class_three_manifest.json;phase18_class_three_root_audit.json;phase18_class_three_independent_audit.json;phase18_class_three_status.md;phase18_leading_coefficient.md;phase18_leading_coefficient_rank_audit.json",
        "The original unmarked group characterization, chiral cases and orders 2^k p remain outside these conclusions. Exact unrestricted excess-three counts are now supplied by a complete finite graph and integer-vector certificate; higher excess coefficients remain uncomputed. This is progress on a restricted component, not a solution of Problem 30 or a rederivation of the survey. Publication priority, complete formalization and a matched proof-length ratio remain unestablished."),
    "F015": (
        "component_rederived", "Complete selected Propositions11 and13, including presentations, orders, geometry and toroidal assertion; p,s>=2 and n>=3,s>=2 respectively",
        "Nested shadows give geometric halving, the even-coordinate subgroup gives its order, and a uniform Reidemeister–Schreier calculation proves the complete fork presentations. The translation lattice lies in the parity kernel.",
        "Original matching/Danzer constructions, lattice Lemma7, Corollaries9/12 and original presentation Proposition10; Standard Coxeter classification and toroidal lattice labels",
        "phase30_source_adapters.md;phase30_source_intake.json;phase30_source_manifest.json;phase30_source_rank_audit.md;phase30_source_geometry_check.json;phase30_source_presentations_check.json",
        "Complete selected propositions only. Other source families and principal targets remain unrederived; no whole-paper or principal-result credit. Uniform arguments are written, with finite presentation diagnostics; no matched ratio or novelty claim."),
    "N004": (
        "component_rederived", "Advertised RWPRI/(IP)2 truncation target, via a complete weighted-tree model",
        "Contract omitted edges and retain component sizes as weights; forest and laminar incidence formulas give exact primitivity, local two-transitivity, rank-two and full-shadow criteria.",
        "Foundational classification identifying inductively minimal pairs with the known tree model; Exact published theorem-by-theorem comparison remains unavailable",
        "phase6_weighted_tree.md;phase6_weighted_tree_check.json;phase6_weighted_tree_independent_audit.md;formal/ConsecutiveShadow.lean;formal/ConsecutiveShadow.scope.md",
        "The all-parameter model theorem is proved and internally reviewed; original full text remains unavailable. No whole-paper equivalence, abstract isomorphism classification or novelty claim."),
    "L115": (
        "finite_subfamily_reproduced", "Corollary 8.1: 29 rank-two geometries of Sz(8)",
        "Normalizer-orbit classification with type reversal; 75 inner classes fuse to 29.",
        "Complete Sz(8) subgroup-class data from GAP TomLib",
        "classification_compression.md;classification_compression_certificate.json;classification_witness_check.json",
        "All-q Theorem 7.1 is not rederived. A finite corollary does not give whole-paper coverage."),
}

READING_UPDATES = {
    "L003": ("selected_sections_read", "Primary internal pages17–19: complete rotational presentation, Table8, surrounding finite-family prose and Problem9.2; later2021 first-family theorem and corrections compared. No current-resolution claim.", "phase32_L003_source_intake.json"),
    "L111": ("selected_sections_read", "Primary indexed definitions, graph convention, both theorem input formulations, complete verbal Theorem4.1 and Construction5.1, and relevant section5 proofs. Arbitrary-rank flag quantifiers independently checked. Complete body/PDF and application tables remain unavailable.", "phase32_L111_scope.json"),
    "F015": ("selected_sections_read", "Sections2.2–2.4 and orthoplex Section3.2 including Proposition13; not all family proofs.", "phase26_access.json"),
    "L088": ("full_text_read", "All ten primary pages and six construction proofs read; figures on pages9–10 independently visually checked. The exhaustive introductory classification is retained background.", "phase24_L088_sources.json"),
    "L108": ("full_text_read", "All seven printed pages19–25, definitions, statements, proofs and references read from the complete primary authored rendering. Publisher PDF unavailable.", "phase25_L108_intake.json"),
    "N009": ("full_text_read", "All22 primary pages read cumulatively across source-bound audits; the final independent review matches all27 numbered items and allsix tables. Root and the independent reviewer visually inspected printedp10. This reading record does not claim literal validity of every printed assertion.", "phase24_N009_coverage.md"),
    "F013": ("full_text_read", "Complete eleven-page cached primary manuscript read by root; definitions (7)-(9) and Theorem 4.2 compared independently on PDF pages 5-8 and in versioned v1 HTML. Header dates differ; the exact checked claims are recorded in the proof.", "phase12_path_cocycle.md"),
    "F016": ("full_text_read", "All nineteen pages of arXiv:2512.15511v1 read by root, including references and all six principal statements/proofs. The independent reviewer read the full targeted sections 4-7. The title-page date is 18 December 2025 and the arXiv stamp is 17 December 2025.", "phase16_fiber_products.md"),
    "N001": ("full_text_read", "Complete seven-page authored text read through the indexed Academia rendering, including all definitions, Lemmas 1-7, Corollaries 1-2, Theorem 1 and proofs. Formerly missing pages 217-218 are present. Original PDF still unavailable; no original-PDF extraction or matched ratio is claimed.", "phase16_older_source_access.md"),
    "N008": ("full_text_read", "Complete nine-page primary PDF read, including every numbered statement and proof, computational remarks and references. Two EMIS mirrors returned identical validated PDF bytes.", "phase16_frattini_geometry_reduction.md"),
    "L074": ("full_text_read", "All twelve pages of the primary author manuscript read, dated 27 September 2011; journal publication is 2010. Both principal counting theorems, their full proofs, the subgroup table and the L085 restatement are checked.", "phase10_suzuki_marked_fields.md"),
    "L085": ("abstract_read", "Original author abstract read; original full body remains unavailable. The complete principal rank/existence theorem is read through its primary restatement in L074, Theorem 3, manuscript p.5. The Luxembourg szpoly3 révisé PDF was identity-checked and belongs to L074, not L085; no original L085 section reading is inferred.", "phase16_older_source_access.md"),
    "L091": ("selected_sections_read", "Pages 231–233 visually read, including Table 1 and local-two-transitivity/truncation conventions; no HS census reproduction.", "phase6_sporadic_source_audit.md"),
    "L110": ("selected_sections_read", "Rank-three R1–R13, higher-rank construction context and p.11 flag-transitivity uncertainty checked; exact hypotheses compared with L114.", "phase5_suzuki_intake.json"),
    "L114": ("selected_sections_read", "Theorems 5.3–5.5 and their case analyses read; printed pp.58–60 visually checked; Lemma3.11 and final p.61 realization qualification checked.", "phase5_suzuki_intake.json"),
    "N003": ("full_text_read", "All twelve pages read independently by root and the proof author; all eight numbered statements and complete proofs matched to the new forest/parity reduction. Exact source spans and retained Whiston inputs are recorded.", "phase12_N003_source_scope.json"),
    "L028": ("selected_sections_read", "Theorem 4.3 and the two generator parameterizations checked in the exact component audit.", "compression_audit.md"),
    "L029": ("selected_sections_read", "Theorem 1.1, chirality definitions and proof use of the designated action checked.", "incidence_compression.md"),
    "L030": ("selected_sections_read", "Principal construction, theorem/corollaries and the source displays corrected in the reduction checked.", "incidence_compression.md"),
    "L032": ("selected_sections_read", "Principal Theorem 1.2 and its all-rank order/type hypotheses checked.", "compression_phase2.md"),
    "L063": ("selected_sections_read", "Sections 2 and 4.1, Tables 2 and 5, and the publisher appendix proof of Proposition 26 checked.", "classification_compression.md"),
    "L066": ("selected_sections_read", "All four main statements, floor-formula argument, printed table and degree-six conclusions checked.", "commuting_pairs_compression.md"),
    "L104": ("full_short_text_read", "All five pages read by rank_stability; confirmed in the root's registry review on 2026-10-09. Section 3 counts compared in the classification reduction.", "classification_compression.md"),
}


def load(name):
    return json.loads((STUDY / name).read_text())


def reading_category(scope, available):
    if "abstract" in scope and not available:
        return "abstract_read"
    if not available:
        return "metadata_and_access_only"
    if scope in {"read_full_short_paper", "read_full_short_editorial"}:
        return "full_short_text_read"
    if scope == "complete_all_9_pages_statements_proofs_and_references":
        return "full_text_read"
    if scope == "full_text_searched_for_open_problems":
        return "full_text_search_only"
    return "selected_sections_read"


def evidence(path, scope):
    suffix = Path(path).suffix
    kind = {".lean": "formal_component", ".json": "saved_record",
            ".log": "saved_run", ".md": "written_argument_or_audit"}.get(suffix, "artifact")
    return {"file": "research/case_study/" + path, "kind": kind,
            "scope": scope + "; consult the artifact for its exact assumptions and verification boundary"}


def record(row, baseline, overlay, later_readings, older_access):
    identifier = row["id"]
    available = bool(row.get("fulltext_available"))
    preferred = older_access.get(identifier, {}).get("primary_abstract_url")
    urls = [a["url"] for a in row.get("assets", []) if a.get("url")]
    if preferred:
        urls.append(preferred)
    urls += [urljoin("https://leemans.dimitri.web.ulb.be/papers.html", u)
             for u in row.get("source_urls", [])
             if not u.rstrip("/").endswith("/papers.html")]
    if identifier == "L084":  # the original-paper abstract is not the erratum
        urls = []
    if identifier == "L107":
        # The generic m23 abstract is the different classification entry L098.
        urls = [u for u in urls if not u.endswith("/abstracts/m23.html")]
    raw_year = row.get("publication_year_from_catalogue")
    r = {
        "id": identifier, "title": row["title"],
        "year": int(raw_year) if str(raw_year).isdigit() else None,
        "year_label_from_inventory": raw_year, "citation": row.get("citation"),
        "kind": row.get("category"),
        "origin": "catalogue" if identifier.startswith("L") else ("network" if identifier.startswith("N") else "followup"),
        "primary_urls": list(dict.fromkeys(urls)),
        "access_coverage": {
            "retrieved_full_text": available,
            "reading_category": reading_category(row.get("reading_scope", ""), available),
            "reading_scope_verbatim": row.get("reading_scope"),
            "historical_reading_category": reading_category(row.get("reading_scope", ""), available),
            "additional_readings": [],
            "retrieval_status": row.get("retrieval_status"),
            "notes": row.get("status_note"), "public_fulltext_distributed": False,
        },
        "exact_target": [], "method": [], "retained_inputs": [],
        "evidence": [evidence(row.get("intake_file", "phase5_network_intake.json") if identifier.startswith("N") else "literature_inventory.json", identifier + " intake only")],
        "status": "unassessed",
        "remaining_work": ["Identify and read exact theorem targets; assess a replacement derivation and record retained inputs."],
        "encoded": False, "rederived": False, "full_principal_results": False,
        "proposed_new_result": False,
        "historical_compression_assessment": baseline.get(identifier),
        "later_workspace_overlay": overlay.get(identifier),
        "external_review": "No external review of repository derivations recorded.",
    }
    if identifier in later_readings:
        later = later_readings[identifier]
        r["access_coverage"]["additional_readings"].append({
            "source": "research/case_study/phase4_old_problem_intake.json",
            "reading_depth": later["reading_depth"],
        })
        r["access_coverage"]["reading_category"] = "selected_sections_read"
    if identifier in READING_UPDATES:
        category, depth, source = READING_UPDATES[identifier]
        r["access_coverage"]["additional_readings"].append({
            "source": "research/case_study/" + source, "reading_depth": depth,
            "basis": "Explicit target/source audit, recorded during registry review; no claim of reading beyond the stated scope.",
        })
        r["access_coverage"]["reading_category"] = category
    if identifier in baseline:
        old = baseline[identifier]
        verdict = old["verdict"]
        r["status"] = {
            "outside_core": "outside_current_core", "core_source": "source_theorem_retained",
            "structural_template": "related_only", "transfer_tail": "conditional_component",
            "verified_component": "component_rederived", "verified_new_application": "proposed_new_result",
        }[verdict]
        r["exact_target"] = [{"reference": old["exact_statement"],
                              "scope": old["verified_reduction_or_relation"],
                              "relation_to_source": "historical_baseline_only"}]
        r["method"] = [old["verified_reduction_or_relation"]]
        r["retained_inputs"] = [old["essential_remaining_input"]]
        r["remaining_work"] = [old["essential_remaining_input"],
                               "This baseline is not a complete principal-result reduction."]
        r["encoded"] = verdict in {"transfer_tail", "verified_component", "verified_new_application"}
        r["rederived"] = verdict in {"transfer_tail", "verified_component"}
        r["evidence"].append(evidence("compression_audit.md", old["exact_statement"]))
    if identifier in UPDATES:
        status, ref, method, retained, paths, remaining = UPDATES[identifier]
        r.update(status=status, method=[method],
                 retained_inputs=[x.strip() for x in retained.split(";")],
                 remaining_work=[remaining], encoded=True,
                 rederived=status in {"principal_results_rederived", "component_rederived", "finite_subfamily_reproduced"},
                 full_principal_results=status == "principal_results_rederived",
                 proposed_new_result=status in {"proposed_new_result", "partial_progress"})
        r["exact_target"] = [{"reference": ref, "scope": method,
                              "relation_to_source": "proposed_consequence" if r["proposed_new_result"]
                              else "specified_existing_target_or_encoding"}]
        r["evidence"] = r["evidence"][:1] + [evidence(x, ref) for x in paths.split(";")]
    if identifier == "L003":
        r["exact_target"].append({"reference":"Universal regular object and finite residue-preserving quotients at fixed source parameter6", "scope":"The four-involution universal group U6=P6 semidirect C2 is an actual infinite regular hypertope. Every even coordinate modulus gives a finite regular quotient with the same exact four toroidal residues; their orders are unbounded. The modulus is not the source parameter.", "relation_to_source":"proposed_fixed_parameter_consequence"})
        r["method"].append("Injectivity on maximal parabolics lifts full subgroup IP and typed coset Helly from one exact modulus-two group of order27648. Local torus order bounds attain equality; reflection-invariant local lattices identify the rotation subgroup of the universal group.")
        r["evidence"] += [evidence(n, "Fixed-s6 geometric and universal corollary") for n in ("phase32_L003_fixed_parameter_hypertopes.md", "phase32_L003_geometry_manifest.json", "phase32_L003_geometry_rank_audit.md", "phase32_L003_geometry_root_audit.md", "phase32_L003_universal_hypertope.md", "phase32_L003_universal_manifest.json", "phase32_L003_universal_root_audit.md", "formal/ParabolicQuotientTransport.scope.md")]
        r["access_coverage"]["additional_readings"].append({"source":"research/case_study/phase32_L003_geometry_intake.json", "reading_depth":"Exact equation2.3 local-generator substitutions, standard triangular torus lattice and source section3 universality definition compared with the fixed-s6 construction."})
        r["remaining_work"] = ["The varying-source-parameter question, other principal paper results and priority remain unresolved here. No identification of the monomial image with the universal group and no general coordinate-quotient order formula. Formal components do not constitute an end-to-end formalization of the source/geometric adapter. No infinity marker."]
    if identifier == "L003":
        r["exact_target"].append({"reference":"Every even exact source parameter in the second proposed family", "scope":"Finite regular hypertope with ordered parameters((3,0),(2,0),(1,1),(s,0)) for every even s>=2. Marked universal U_s also exists, equals P_s semidirect C2, and is infinite for6|s.", "relation_to_source":"proposed_infinite_parameter_subfamily"})
        r["method"].append("One-exceptional quotient transport; three fixed integral parabolics and a determinant-minus-one translation minor identify the growing torus by matching order bounds. A separate independent Cayley-component census checks all5287 base flags.")
        r["evidence"] += [evidence(n,"All-even finite and universal regular hypertopes") for n in ("phase33_L003_even_family.md","phase33_L003_even_manifest.json","phase33_L003_even_rank_audit.md","phase33_L003_even_root_audit.md","phase33_L003_even_base_root_check.json","phase33_L003_universal_even.md","phase33_L003_universal_even_root_audit.md","phase33_source_status.md")]
        r["access_coverage"]["additional_readings"].append({"source":"research/case_study/phase33_L003_even_intake.json", "reading_depth":"Exact source presentation, ordered residue adapters, Table8 and Problem9.2 rechecked for the genuinely varying even parameter."})
        r["remaining_work"] = ["Uniform odd-parameter existence, universal orders at other parameters, current priority and end-to-end formalization remain unverified. N015 main-theorem overlap remains undetermined because its complete body was not obtained. Infinitely many exact finite parameters are proved; no complete all-integer claim or infinity marker."]
    if identifier == "L003":
        r["exact_target"].append({"reference":"Exact order of the specified even-parameter quotients", "scope":"Full integral image has a saturated rank6 translation kernel and quotient order1296. Literal reduction has kernel mL, so |G_m|=1296m^6 for all m>=1. No splitting or universal-order assertion.", "relation_to_source":"specified_quotient_order_consequence"})
        r["evidence"] += [evidence(n,"Exact even-family quotient order") for n in ("phase34_L003_even_order.md","phase34_L003_even_order_manifest.json","phase34_L003_even_order_root_audit.md","formal/SplitLatticeReduction.scope.md")]
    if identifier == "L003":
        r["exact_target"].append({"reference":"Every source parameter divisible by three, and combined universal existence", "scope":"Finite regular hypertope at s=3m>=3 with exact local orders36,108m²,48,108. Together the two families cover2|s or3|s. Marked regular U_s=P_s semidirect C2 exists throughout that union.", "relation_to_source":"second_infinite_parameter_subfamily"})
        r["method"].append("Scaled unit translation minor modulo2m, exact base order13824 and three injective parabolics; one-exceptional transport. Independent exhaustive base census checks56225 flags.")
        r["evidence"] += [evidence(n,"Multiples-of-three and combined universal scope") for n in ("phase34_L003_triple_family.md","phase34_L003_triple_manifest.json","phase34_L003_triple_root_audit.md","phase34_L003_triple_base_root_check.json","phase34_L003_combined_universal.md")]
        r["remaining_work"] = ["Uniform existence at parameters coprime to6, further universal orders, current priority and end-to-end formalization remain unverified. N015 full main-theorem comparison is still unavailable. No all-integer claim or infinity marker."]
    if identifier == "L003":
        r["exact_target"].append({"reference":"Standalone compact model of the even-parameter family", "scope":"Four integral affine maps in dimension6, translation kernel2Z6 and linear quotient1296; reduction modulo2m has order1296m6 and gives the same marked regular groups as the original voltage construction.", "relation_to_source":"compact_verified_quotient_family"})
        r["method"].append("Small integral matrices, complete Schreier translation certificate, faithful reduction modulo2 and a rational affine intertwiner. The standalone construction needs no old voltage data.")
        r["evidence"] += [evidence(n,"Compact affine model and exact comparison") for n in ("phase35_L003_affine_model.md","phase35_L003_affine_manifest.json","phase35_L003_affine_root_audit.md","phase35_L003_affine_check.json","phase35_L003_affine_compare.json","formal/CompactAffineData.scope.md")]
    if identifier == "L034":
        # The existing construction and the proposed conjecture proof are separate axes.
        r["proposed_new_result"] = True
        r["exact_target"] = [
            {"reference": "Theorem 3.2", "scope": "The specified grid/dihedral construction is rederived; its alternate quotient display remains unverified.",
             "relation_to_source": "specified_existing_target_or_encoding"},
            {"reference": "Conjecture 3.3, complete stated range n>=10, s,t>=2, l>=1",
             "scope": "The proposed all-2-group cyclic TPP theorem and regular-hypertope adapter exclude n<s+t+l. The written proof retains powerful-group structure and elementary finite-p-group facts, with no finite catalogue or isobicyclic classification. Internal reviews passed; current priority remains unverified.",
             "relation_to_source": "proposed_consequence"},
            {"reference": "Stronger companion theorem: cyclic subgroup TPP in every finite nilpotent group",
             "scope": "Every three cyclic subgroups with TPP have order product at most the ambient group order. No order or nilpotency-class cutoff. Cyclicity and nilpotence remain essential scope restrictions.",
             "relation_to_source": "proposed_uniform_companion_application"},
        ]
    if identifier in {"N013", "N014"}:
        lattice = identifier == "N013"
        r.update(status="principal_results_rederived" if lattice else "proposed_new_result",
                 encoded=True, rederived=lattice, full_principal_results=lattice,
                 proposed_new_result=not lattice)
        ref = ("Complete principal construction and section4 applications; Theorem3.1, Proposition3.2, Corollary3.3 and Lemma2.4, arXiv2001.11082v1"
               if lattice else "Construction3.6; residual-connectivity claims of Proposition3.13, Theorem3.18 and introductory TheoremA, arXiv2405.19050v1")
        scope = ("Complete geometric halving construction plus generalized-cube even-coordinate groups, orders, polygon counts, self-duality, genus, actual spherical residues and stated finite hyperbolic examples. All eight numbered items and the principal unnumbered applications are accounted for relative to retained background. Remark4.1 needs a rank qualification; literal whole-document truth is not asserted."
                 if lattice else "Exact parity-compatible repair, plus a regular rank-four B1/B2 counterexample with 983040 chambers and 122880 disconnected transformed rank-two residues. The residual-connectivity and hypertope-preservation claims fail even for a regular input. The literal TheoremB/4.4 coset-isomorphism assertion is not refuted; the revised journal body remains unverified.")
        r["exact_target"] = [{"reference": ref, "scope": scope,
                              "relation_to_source": "specified_existing_component" if lattice else "version_bound_counterexample_and_conditional_repair"}]
        r["method"] = ["Use components of the canonical bipartite double cover of each graph shadow; common-component intersections control chamber completion and every residue. For regular inputs PC equals the principal endpoint-support filter."]
        r["retained_inputs"] = ["Basic regular-polytope/hypertope and coset correspondences; actual residual connectivity of the original geometry; B1/B2 and the stated lattice hypothesis when applicable."]
        if not lattice:
            r["retained_inputs"].append("Published Lemma4.5 overlap identification is attributed. The literal TheoremB/4.4 coset-isomorphism assertion is distinct from the false surrounding hypertope/C-group-preservation claim.")
        r["evidence"] += [evidence(n, ref) for n in (
            "phase26_halving_source_adapter.md", "phase27_parity_theory.md",
            "phase27_parity_manifest.json", "phase27_parity_sources.json",
            "phase27_parity_shadow_rank_audit.md", "phase27_parity_shadow_rank_audit.json",
            "phase27_parity_shadow_check.json", "phase27_parity_shadow_rank_check.json",
            "phase27_halving_version_status.md", "phase27_halving_version_status.json")]
        r["access_coverage"]["additional_readings"].append({
            "source":"research/case_study/phase27_parity_sources.json",
            "reading_depth":"Sections1–3 and exact geometric construction proofs read; section4 applications not audited." if lattice else "Full sections3–4 construction and halving arguments read; section5 applications excluded. Exact arXiv version audited; revised journal body unavailable."})
        r["remaining_work"] = ["Application sections and all principal paper targets remain incomplete. No whole-paper reduction, matched proof-length ratio, publication priority or infinity marker. Complete geometric argument is written, not formalized end to end."]
        if lattice:
            r["method"].append("Nested-shadow cover recognition, even-coordinate semidirect products, direct spherical-residue identification and a coordinate genus count.")
            r["retained_inputs"] += ["Danzer's original generalized-cube construction; standard finite/affine/hyperbolic Coxeter classifications and toroidal labels; quoted Tits/coset background and Pellicer extension."]
            r["evidence"] += [evidence(n, ref) for n in ("phase30_source_adapters.md", "phase30_source_intake.json", "phase30_source_manifest.json", "phase30_source_rank_audit.md", "phase30_source_geometry_check.json")]
            r["access_coverage"]["reading_category"] = "full_text_read"
            r["access_coverage"]["additional_readings"].append({"source":"research/case_study/phase30_source_intake.json", "reading_depth":"Sections1–4 read across the source audits, with all numbered items and principal unnumbered applications explicitly mapped."})
            r["remaining_work"] = ["No literal whole-document truth, matched ratio, novelty or end-to-end formalization claim. The reference[9] comparison is unverified; the auxiliary semiregular identification and Pellicer construction are retained. Remark4.1 is rank-qualified in the source ledger."]
        else:
            r["method"].append("An explicit regular {5,5} seed with group A5 times C2 and an invariant binary code gives an actual affine hypertope. Odd individual shadows meet in squares. Changed local parabolics have orders160,160 and intersection8 instead of4.")
            r["method"].append("Characteristic surface covers and an orbit-versus-dimension bound give infinitely many regular examples at the same rank and diagram; the separate corollary covers every integer n>=2 coprime to6.")
            r["evidence"] += [evidence(n, ref) for n in ("phase30_affine_map.md", "phase30_affine_map_manifest.json", "phase30_affine_root_audit.md", "phase30_affine_map_second_audit.md", "phase30_regular_halving_root_check.json", "phase30_affine_formal_manifest.json", "formal/Phase30AffineData.scope.md")]
            r["evidence"] += [evidence(n, ref) for n in ("phase31_affine_covers.md", "phase31_affine_covers_manifest.json", "phase31_affine_covers_root_audit.md", "phase31_seed_surface_check.json", "phase31_cover_prior_art.md")]
            r["access_coverage"]["additional_readings"].append({"source":"research/case_study/phase30_affine_root_audit.json", "reading_depth":"Exact introduction TheoremsA/B, standing assumptions, Theorem3.18 and section4 through Theorem4.4/degeneracy discussion rechecked against the regular-input counterexample; arXivv1 only."})
            r["remaining_work"] = ["Section5 applications and full principal-paper reduction remain incomplete. Literal TheoremB/4.4 coset isomorphism is not disproved. Revised journal body, correction priority, matched ratio and end-to-end formalization remain unverified. This is a theorem counterexample, not a documented open-conjecture resolution; no infinity marker."]
    if identifier in {"L081", "L111"}:
        r["access_coverage"]["additional_readings"].append({"source":"research/case_study/phase26_access.json", "reading_depth":"Renewed bounded primary-source access; original full body unavailable. Later primary restatements are attributed separately."})
    if identifier == "L111":
        r["access_coverage"]["additional_readings"].append({"source":"research/case_study/phase31_older_source_targets.md", "reading_depth":"Selected author-indexed Theorem4.1/B1/B2 excerpts and construction leads; complete body and diagrams still unavailable. No theorem or fulltext credit."})
    if identifier == "L111":
        r["primary_urls"] += ["https://doi.org/10.36045/bbms/1103055618", "https://www.researchgate.net/publication/29655004_New_geometries_for_finite_groups_and_polytopes"]
        r["access_coverage"]["historical_notes"] = r["access_coverage"].get("notes")
        r["access_coverage"].update(retrieval_status="selected_primary_indexed_passages_read_complete_body_unavailable",
            notes="Complete single Theorem4.1 and literal construction now source-matched and independently rederived, including arbitrary rank. No complete-body, application-table or principal-paper credit.")
    if identifier == "L111":
        r["exact_target"].append({"reference":"Section6 merging/splitting constructions and exact limits", "scope":"Arbitrary-rank Theorem6.1 construction/(i)/(ii)/forward(iii) and Theorem6.2 rederived. Unrestricted6.1(iii) converse and Cor6.1 fail on explicit geometries under the accessed hypotheses.", "relation_to_source":"reduction_with_separate_counterexamples"})
        r["method"].append("Exact chamber/residue models, subdivision paths, a specified global bipartition and parity cohomology; explicit full automorphism orders128/512 and odd square tori.")
        r["evidence"] += [evidence(n,"Section6 source-bound reduction and counterexamples") for n in ("phase32_L111_section6_theory.md","phase32_L111_section6_ledger.json","phase32_L111_section6_manifest.json","phase32_L111_section6_root_audit.md","phase32_L111_section6_rank_audit.md","phase32_L111_section6_recent_audit.md","phase32_L111_section6_check.json")]
        r["numbered_statement_ledger"] = load("phase32_L111_section6_ledger.json")["statement_level_targets"]
        r["access_coverage"]["additional_readings"].append({"source":"research/case_study/phase32_L111_section6_intake.json", "reading_depth":"Complete verbal Theorems6.1/6.2, constructions, Cor6.1/proof and selected source definitions read in primary indexed passages; diagram images and complete PDF unavailable."})
        r["access_coverage"]["notes"] = "Theorem4.1 and positive section6 statements source-matched; two separate indexed-statement counterexamples. No complete-body, application-table or principal-paper credit."
        r["remaining_work"] = ["Remaining auxiliary statements/application tables, complete PDF, later corrections and correction priority are unverified. No literal whole-paper validity, matched ratio or infinity marker."]
    if identifier == "N005":
        r["access_coverage"]["additional_readings"].append({"source":"research/case_study/phase31_cover_prior_art.json", "reading_depth":"Proposition2.2, Definitions4.1/4.5/4.6 and Theorem4.12/Corollary4.13 with displayed proofs; primary rendered preprint only, not final journal body. No new reduction credit."})
    if identifier == "L108":
        r["historical_catalogue_title"] = r["title"]
        r["title"] = "On the Petrials of thin rank 3 geometries"
        r["citation"] = "D. Bonheure, F. Buekenhout and D. Leemans. Journal of Geometry 71 (2001), 19–25. DOI 10.1007/s00022-001-8548-2."
        r["primary_urls"] += ["https://link.springer.com/article/10.1007/s00022-001-8548-2", "https://www.academia.edu/82511046/On_the_Petrials_of_thin_rank_3_geometries"]
        r["access_coverage"]["historical_notes"] = r["access_coverage"].get("notes")
        r["access_coverage"].update(retrieved_full_text=True, original_pdf_available=False,
            source_representation="complete_rendered_primary_authored_text",
            retrieval_status="complete_rendered_primary_text_accessed_original_pdf_unavailable",
            notes="Complete article read and source-bound structural reduction independently reviewed. Unconditional auxiliary claims are corrected explicitly; no literal whole-document validity claim.")
        r["numbered_statement_ledger"] = load("phase25_L108_intake.json")["numbered_statements"]
    if identifier == "L103":
        r["access_coverage"]["additional_readings"].append({"source": "research/case_study/phase25_older_access.json", "reading_depth": "Bounded renewed access attempt; body unavailable, abstract only. Primary publisher confirms year2002; 2003 is a review-date ambiguity."})
    if identifier == "L088":
        r["primary_urls"].append("https://msp.org/iig/2005/1-1/iig-v1-n1-p08-s.pdf")
        r["access_coverage"]["notes"] = "Complete primary PDF read. Six principal construction theorems rederived and independently checked. Exhaustive global classification remains retained. Figure-label transposition is explicit."
    if identifier == "N003":
        r["access_coverage"]["historical_notes"] = r["access_coverage"].get("notes", "")
        r["access_coverage"]["notes"] = "The complete primary manuscript has been read and all eight numbered targets rederived in the finite-group/n>=7 scope. Whiston W1/W2 remain retained inputs; the earlier tree-only assessment is superseded. Phase15 independently audits a compact complete proof and its matched 4/3 description-length ratio."
    if identifier == "N001":
        r["primary_urls"].append("https://www.academia.edu/54639280/Some_properties_of_inductively_minimal_geometries")
        r["access_coverage"]["historical_notes"] = r["access_coverage"].get("notes", "")
        r["access_coverage"].update(
            retrieved_full_text=True, original_pdf_available=False,
            source_representation="complete_indexed_rendering_of_primary_text",
            retrieval_status="complete_rendered_primary_text_accessed_original_pdf_unavailable",
            notes="Complete authored text is now read, including all formerly missing proof sections. The private browser record identifies the authored body separately from website navigation. The original PDF remains unavailable; this access improvement adds no theorem credit and no new measurement ratio.")
    if identifier == "N008":
        r["source_intake_id"] = "ACK2005_unassigned"
        r["source_intake_id_note"] = "Assigned living-registry ID N008; frozen intake bytes and original ID are unchanged."
        r["access_coverage"]["original_pdf_available"] = True
        r["excluded_source_claims"] = load("phase16_frattini_geometry_intake.json")["excluded"]
        r["exact_target"] = [
            {"reference": "Theorem 2.1, finite groups",
             "scope": "Relative independent generation is equivalent modulo the Frattini subgroup. The unrestricted infinite converse is not asserted; a scope counterexample is recorded separately.",
             "relation_to_source": "specified_existing_target_or_encoding"},
            {"reference": "Theorem 3.1; Proposition 3.2; Corollary 3.3; Theorem 3.4",
             "scope": "The Frattini subgroup lies in the Borel, including the theorem's infinite-group setting because the finite maximal chain supplies relative finite generation. Exact coset-kernel transport preserves the stated geometry and residue conditions.",
             "relation_to_source": "specified_existing_target_or_encoding"},
            {"reference": "Proposition 3.5; Lemma 3.6; Proposition 3.7; Theorem 3.8",
             "scope": "Coordinate hyperplanes classify all firm RWPRI finite-p-group coset geometries in the source conventions: they are direct sums of primitive rank-one geometries.",
             "relation_to_source": "specified_existing_target_or_encoding"},
            {"reference": "Section 4.2 residue Frattini test",
             "scope": "Apply the subgroup ladder inside each residue group to obtain the exact necessary Frattini-containment test, not a sufficient recognition criterion.",
             "relation_to_source": "specified_existing_target_or_encoding"},
        ]
    if identifier == "F013":
        r["access_coverage"]["historical_notes"] = r["access_coverage"].get("notes", "")
        r["access_coverage"]["notes"] = "Complete cached manuscript read; primary pages1-4 rechecked for the exact principal-target adapter. Phase15 graded support recovers both principal Theorems1.1-1.2 in all classes and ranks. The phase-twelve counterexamples to specified auxiliary C conclusions in v1 Theorem4.2(c-e) remain valid."
        r["exact_target"] = [{
            "reference": "arXiv:2605.20691v1, Theorems 1.1 and 1.2, every finite nondegenerate string C-group of 2-power order and rank d>=2",
            "scope": "The marked quotient G/gamma3 is the path-cocycle group of order 2^(2d-1), with no nilpotency-class cutoff. The retained standard correspondence gives the equivalent regular-polytope covering statement. A broader theorem handles every forest diagram.",
            "relation_to_source": "principal_results_rederived",
        }, {
            "reference": "arXiv:2605.20691v1, Theorem 4.2(c),(d),(e), with C defined by equations (7)-(9)",
            "scope": "The all-rank path cocycle gives the wrong asserted kernel size, quotient order and equality C=gamma3 for every d>=4. The separate main common-quotient existence claim is not refuted.",
            "relation_to_source": "counterexample_to_specified_assertions",
        }]
        r["primary_urls"].append("https://arxiv.org/html/2605.20691v1")
    if identifier == "L074":
        r["exact_target"] = [
            {"reference": "Theorem 1", "scope": "Exact isomorphism-class count of unordered pairs of distinct commuting involutions for every stated odd field exponent.",
             "relation_to_source": "specified_existing_target_or_encoding"},
            {"reference": "Theorem 2", "scope": "Complete Suzuki polyhedron count up to isomorphism and duality, including nondegeneracy; the compact formula is proved equal to the published nested formula in all parameters.",
             "relation_to_source": "specified_existing_target_or_encoding"},
        ]
        r["primary_urls"].append("https://math.uni.lu/kiefer/Publications/szpoly3%20r%C3%A9vis%C3%A9.pdf")
        r["primary_urls"] = list(dict.fromkeys(r["primary_urls"]))
    if identifier == "L085":
        foreign_url = "https://math.uni.lu/kiefer/Publications/szpoly3%20r%C3%A9vis%C3%A9.pdf"
        r["primary_urls"] = [u for u in r["primary_urls"] if u != foreign_url]
        r["cross_references"] = [{
            "paper_id": "L074", "url": foreign_url,
            "scope": "Verified full text of the distinct Kiefer-Leemans counting paper, containing the principal L085 theorem as Theorem 3. This is not an L085 full-text URL.",
        }]
        r["evidence"].append(evidence("phase16_older_source_access.md", "L074/L085 primary PDF identity audit"))
    if identifier == "F016":
        r["primary_urls"] = ["https://arxiv.org/abs/2512.15511v1", "https://arxiv.org/pdf/2512.15511v1"]
        r["access_coverage"]["historical_notes"] = r["access_coverage"].get("notes", "")
        r["access_coverage"]["notes"] = "Complete nineteen-page version read. Six principal theorems rederived with explicit retained geometric inputs. The infinite-group terminology permits infinite-order elements; all finite-order elements must have two-power order. The fixed-excess theorem is a separate companion application, not another paper reduction."
        r["exact_target"] = [
            {"reference": "Theorem 5.1(a-d)",
             "scope": "Every prescribed toroidal triple sequence: existence, exact group order, specified flatness and all stated FAP assertions, via path fiber products and deletion maps.",
             "relation_to_source": "principal_results_rederived"},
            {"reference": "Theorem 5.3",
             "scope": "Complete all-rank presentation with the stated disjoint-edge-square commutator relators. Lattice-index kernel counts avoid assuming the two squared translations intersect trivially.",
             "relation_to_source": "principal_results_rederived"},
            {"reference": "Theorem 6.1(a-b)",
             "scope": "The alternating semiregular construction and both full-automorphism order cases, conditional on the expressly retained tail-triangle geometric theorem.",
             "relation_to_source": "principal_results_rederived"},
            {"reference": "Theorems 7.1, 7.2 and 7.3",
             "scope": "All three free-extension results, including infinite input groups, use the source's two-primary-torsion convention and retained geometric amalgam identifications.",
             "relation_to_source": "principal_results_rederived"},
            {"reference": "Lemma 4.1",
             "scope": "The two-power square-torus parameter classification relative to the standard classification by invariant lattices.",
             "relation_to_source": "specified_existing_target_or_encoding"},
            {"reference": "Companion fixed-excess theorem for all finite nondegenerate two-group string C-groups",
             "scope": "For rank d>=3 and |G|=2^(2d-1+k), k>=0, supp(gamma3(G)) has at most 3k vertices in at most k intervals. For k>0 its closed neighborhood has at most 5k vertices and core order at most 2^(11k-1). The exact attachment presentation and central cocycle give a canonical bijection with finite cores: every qualifying core attaches automatically, with no global order/IP acceptance test. All bounds are sharp; for each fixed positive k the ordered-marking count is a polynomial of degree k for every d>=6k-1. Its rational generating function has finite core multiplicities; the rederived F016 family gives the lower bound. Those multiplicities have not been enumerated. For k=0 the canonical group is unique. This is not a second paper-credit item or an efficient core census.",
             "relation_to_source": "proposed_uniform_companion_application"},
        ]
        r["proposed_new_result"] = True
        for name in ("phase16_central_join.md", "phase16_central_join_independent_audit.json", "phase16_central_join_root_review.json"):
            r["evidence"].append(evidence(name, "Exact central attachment and eventual polynomial count; companion result"))
        r["retained_inputs"].append("For the companion fixed-excess theorem: reviewed all-class forest quotient theorem; the rederived F016 family supplies sharpness and the counting lower bound")
        r["exact_target"][-1]["scope"] += " Phase18 determines the leading coefficient exactly as 5^k/k!, proves the higher-class contribution has eventual degree at most k-1, and classifies all class-at-most-three markings by a two-state transfer matrix. Phase19 also determines every excess-two coefficient: a_2(d)=(25d^2-107d+122)/2 for d>=3, including 9d-20 class-four markings. Unrestricted lower coefficients at excess at least three remain uncomputed here."
        for name in ("phase18_class_three.md", "phase18_class_three_root_audit.json",
                     "phase18_leading_coefficient.md", "phase18_leading_coefficient_rank_audit.json"):
            r["evidence"].append(evidence(name, "All-rank class-three classification and fixed-excess leading coefficient; companion results"))
    if identifier == "L120":
        r["exact_target"][0]["scope"] = "Dimension-four bilinear-form obstructions give the stated odd linear and unitary intermediate-group upper bounds, with the phase-eight PSL4 argument retained. Field and graph extensions are not covered."
        r["exact_target"].append({
            "reference": "Problem 7, diagonal linear interval PSL4(q)<=G<=PGL4(q), every odd q",
            "scope": "An explicit four-matrix template gives type {4,2p,2p} on the diagonal index-two subgroup for q=p^e. Together with the retained upper bound and published simple-socle existence, maximum rank is four at socle index one or two; index four has no involution generating set. This does not assert rank-three extension existence or field/graph cases.",
            "relation_to_source": "proposed_resolution_of_exact_subcase",
            "retained_inputs": ["Burnside basis theorem and unitriangular abelianization", "Elementary matrix generation", "Recursive marked intersection criterion", "Earlier written rank-four upper bound", "Published simple-socle rank-four existence only for the interval corollary"],
        })
        r["method"].append("Prime-field triangular generators plus one field parameter produce every elementary root. A symmetric-form intersection inside the known triangular subgroup has exactly 4p elements, giving the full rank-four IP without an orthogonal subgroup classification.")
        for name in ("phase16_linear_diagonal.md", "phase16_linear_diagonal_manifest.json",
                     "phase16_linear_diagonal_independent_audit.json", "phase16_linear_diagonal_root_audit.json",
                     "phase16_linear_diagonal_status.md", "phase16_linear_diagonal_status.json"):
            r["evidence"].append(evidence(name, "Odd linear diagonal interval; exact subcase, priority unverified"))
        r["exact_target"].append({
            "reference": "Companion unitary application: maximum rank four and rank set {3,4} for PSU4(q), every odd q>=5",
            "scope": "Two curve/character-sieve constructions, complete exceptional parameter certificates and full q7/q11 group/IP checks give rank-four existence in both odd congruence classes. Generation/intersection and the separate rank obstruction are written proofs. Published rank-three existence is retained; PSU4(3) has no representation by retained published input. Broader almost-simple survey scope remains unresolved.",
            "relation_to_source": "proposed_uniform_companion_application",
        })
        r["exact_target"].append({
            "reference": "Companion diagonal unitary extension theorem, every odd q>=3",
            "scope": "The unique diagonal index-two extension of PSU4(q) inside PGU4(q) has type {4,2(q+1),2p} and maximum rank four. Both congruence branches have written proofs; q=3 generation uses an exact natural-action order certificate. This is not a unitary instance of the survey's linear Problem 7, nor a rank-three or field/graph extension theorem.",
            "relation_to_source": "proposed_uniform_companion_application",
        })
        r["method"].append("A common four-matrix template and an auxiliary semilinear involution reduce the two maximal-parabolic intersection to a binary orthogonal group. Explicit vertex eigenvalues control arbitrary projective similitude multipliers in both congruence branches.")
        for name in ("phase17_unitary_diagonal.md", "phase17_unitary_twisted.md",
                     "phase17_unitary_manifest.json", "phase17_unitary_root_audit.json",
                     "phase17_unitary_diagonal_independent_audit.json",
                     "phase17_unitary_twisted_independent_audit.json",
                     "phase17_unitary_diagonal_status.md", "phase17_unitary_diagonal_status.json"):
            r["evidence"].append(evidence(name, "All odd diagonal index-two unitary groups; companion result, priority unverified"))
        r["exact_target"].append({
            "reference": "Companion dimension-four rank-three form alternative and direct-fold obstructions",
            "scope": "Irreducible projective involution triples without a bilinear similarity form have two specified endpoint/middle eigenspace configurations. Both direct folds of the frozen rank-four linear and unitary templates are uniformly proper subgroups. This is not a rank-three existence or nonexistence theorem for their ambient groups.",
            "relation_to_source": "proposed_uniform_companion_application",
        })
        for name in ("phase18_rank3_forms.md", "phase18_rank3_forms_independent_audit.json",
                     "phase18_rank3_forms_root_audit.json"):
            r["evidence"].append(evidence(name, "Form-space argument and uniform failure of the two specified folds"))
    if identifier == "L120":
        r["exact_target"].append({
            "reference": "Companion rank-three diagonal unitary extension theorem in two congruence families",
            "scope": "For odd q>=5 with q=1 mod4 or q=3 mod8, explicit unitary involutions generate the diagonal index-two extension and satisfy actual IP. Its rank set is {3,4} with the retained upper bound and rank-four construction. At q=7 mod8 this triple generates only the simple socle. It does not settle q=3, the remaining diagonal-extension family, linear rank-three extensions or field/graph cases. Simple-socle rank-three existence was already known; extension priority is unverified.",
            "relation_to_source": "proposed_uniform_companion_application",
        })
        for name in ("phase19_unitary_rank3.md", "phase19_unitary_rank3_manifest.json",
                     "phase19_unitary_rank3_independent_audit.json", "phase19_unitary_rank3_root_audit.json",
                     "phase19_unitary_rank3_status.md", "phase19_unitary_rank3_status.json"):
            r["evidence"].append(evidence(name, "Rank-three unitary generation and exact intersection adapter; specified congruence families only"))
    if identifier in {"F016", "N010"}:
        r["exact_target"].append({
            "reference": "Companion complete excess-two ordered-marking classification",
            "scope": "For d>=3, exactly (25d^2-107d+122)/2 nondegenerate ordered string C-group markings of order 2^(2d+1). Of these 9d-20 have class four: 4d-8 with cyclic gamma3, and 5d-12 with elementary-abelian gamma3. The exact constructions and marked presentations establish completeness. Lean verifies the nested-kernel IP adapter under its explicit profile assumptions, not the full classification. The independent rank-three quotient census is a bounded diagnostic. No additional principal-paper credit or priority claim.",
            "relation_to_source": "proposed_uniform_companion_application",
        })
        for name in ("phase19_k2_classification.md", "phase19_k2_manifest.json",
                     "phase19_k2_independent_audit.json", "phase19_k2_root_audit.json",
                     "formal/NestedKernelIntersections.lean", "formal/NestedKernelIntersections.scope.md"):
            r["evidence"].append(evidence(name, "All-rank excess-two classification; restricted regular two-group component"))
    if identifier == "L120":
        r["exact_target"].append({
            "reference": "Companion exact rank set {3,4} for every odd diagonal unitary index-two extension",
            "scope": "For every odd q>=3, the unique index-two extension U2(q) over PSU4(q) has rank three. The uniform proof covers q>=5 via a scalar-normalized anti-isometry, full rank-one projection, radical and opposite-root generation; q3 has exact polynomial-coordinate and plane-action certificates. Earlier upper bounds and rank-four constructions give rank set {3,4}. This does not give a representation for the simple PSU4(3), nor solve the whole current Kourovka21.101 almost-simple classification. Priority remains unverified.",
            "relation_to_source": "proposed_uniform_companion_application",
        })
        for name in ("phase20_unitary_rank3.md", "phase20_unitary_rank3_manifest.json",
                     "phase20_unitary_rank3_independent_audit.json", "phase20_unitary_rank3_root_audit.json",
                     "phase20_unitary_rank3_status.md", "phase20_linear_rank3_intake.md"):
            r["evidence"].append(evidence(name, "All odd unitary diagonal extensions and updated published linear baseline"))
    if identifier in {"F016", "N010"}:
        r["exact_target"].append({
            "reference": "Companion finite-state classification at every fixed nilpotency class",
            "scope": "For fixed c>=2, ordered nondegenerate finite two-group string C-groups of class at most c correspond exactly to accepted walks in an effectively finite graph of c-windows and boundary deletion kernels. Compatible semidirect/diagonal gluing, coset Helly and exact deletion update prove construction, actual IP and uniqueness. The rank/excess generating function is rational. At excess k>=1, class<=k+2 and windows of order<=2^(3k+3) suffice. No efficient general library enumeration, unmarked/chiral classification or full Problem30 resolution is claimed.",
            "relation_to_source": "proposed_uniform_companion_application",
        })
        for name in ("phase20_finite_state.md", "phase20_finite_state_manifest.json",
                     "phase20_finite_state_independent_audit.json", "phase20_finite_state_root_audit.json",
                     "phase20_finite_state_status.md"):
            r["evidence"].append(evidence(name, "Fixed-class finite transition theorem and smaller fixed-excess local alphabet"))
    if identifier == "L120":
        r["exact_target"].append({
            "reference": "Companion exact rank set {3,4} for every odd linear diagonal index-two extension",
            "scope": "For every odd q>=5, explicit nonsquare-endpoint matrices generate the index-two extension L2(q) over PSL4(q), with actual rank-three IP. Independent rank-one factors, Jordan radical forcing and root extraction prove generation. Earlier bounds, rank-four constructions and published q3 existence give exact rank set {3,4} for every odd q>=3. The q=3 mod4 range is already published, and the N012 thesis contains a prior q=5 mod8 claim with a printed-witness defect. Its q=1 mod8 quotient is a different group; priority for L2 there remains unverified. Field/graph extensions remain outside this result.",
            "relation_to_source": "proposed_uniform_companion_application",
        })
        for name in ("phase21_linear_rank3.md", "phase21_linear_rank3_manifest.json",
                     "phase21_linear_rank3_independent_audit.json", "phase21_linear_rank3_root_audit.json",
                     "phase21_linear_rank3_status.md", "phase21_linear_rank3_status.json"):
            r["evidence"].append(evidence(name, "All odd linear diagonal index-two extensions; publication priority unverified"))
        r["method"].append("The common cocycle/complement theorem replaces the additive-kernel generation steps in the linear and unitary constructions. Independent factors work over every field and arbitrary block sizes; the coupled unitary criterion holds for odd q>=5 and has an explicit proper-complement counterexample at q=3. Full projected image, ambient roots and IP remain separate.")
        for name in ("phase23_generation_core.md", "phase23_generation_core_independent_audit.json",
                     "phase23_generation_core_root_audit.json"):
            r["evidence"].append(evidence(name, "Shared generation step; no new paper or novelty credit"))
    if identifier in {"F016", "N010"}:
        r["exact_target"].append({
            "reference": "Companion exact third-excess ordered-marking count in every rank",
            "scope": "For rank d>=4 and order2^(2d+2), a3(d)=(125d^3-855d^2+2380d-2646)/6; rank3 has37. All706 rank-five windows give708 states and1522 edges. The exact2832-coordinate identity (T-I)^4 v7=0 gives an alternate all-rank proof without the eventual-polynomiality input. Ranks4–6 use separate exact bases. GAP/NQ and the finite-state completeness theorem remain inputs; no unmarked or reversal count, whole-problem solution or priority claim.",
            "relation_to_source": "proposed_uniform_companion_application",
        })
        for name in ("phase22_excess3_transitions.md", "phase22_excess3_annihilator.md",
                     "phase22_excess3_certificate.json", "phase22_excess3_independent_audit.json",
                     "phase22_excess3_root_audit.json", "phase22_excess3_status.md"):
            r["evidence"].append(evidence(name, "Complete excess-three graph and exact all-rank count"))
    if identifier == "N011":
        for name in ("phase21_linear_rank3_status.md", "phase21_linear_rank3_status.json"):
            r["evidence"].append(evidence(name, "Additional selected source reading and possible theorem overlap; no rederivation credit"))
        r["encoded"] = False
        r["rederived"] = False
        r["full_principal_results"] = False
        r["proposed_new_result"] = False
        r["exact_target"][0]["relation_to_source"] = "source_theorem_retained"
    if identifier in {"L120", "N011", "N012"}:
        r["evidence"].append(evidence("phase22_linear_priority_supplement.md", "Primary thesis quotient identification and limited printed-witness diagnostic"))
    if identifier == "N012":
        r.update(encoded=False, rederived=False, full_principal_results=False, proposed_new_result=False)
        r["exact_target"][0]["relation_to_source"] = "prior_claim_located_printed_witness_defective"
    if identifier == "N009":
        r["method"].append("The class-seven invariant-kernel census handles a nonabelian universal gamma3, checks all401 candidates and all25664 actual meets, and recovers125 rank-three classes and all12type counts. Affine fixed translations give every center formula in Lemma5.2, including both small exceptions; independent Frattini characters give Lemma5.4 under its retained infinite decomposition.")
        r["retained_inputs"] += ["Quoted affine lattice-family identification (Lemma5.1)", "Quoted infinite semidirect decomposition (Theorem5.3)"]
        for name in ("phase22_N009_rank3.md", "phase22_N009_rank3_certificate.json",
                     "phase22_N009_lemma_adapters.md", "phase22_root_audit.md", "phase22_root_audit.json"):
            r["evidence"].append(evidence(name, "Complete rank-three census and two numbered lemma adapters"))
        r["method"].append("Exact marked isomorphisms identify all428 facets in the rank-four/five censuses. Correct dual-label pairing recovers all107 Table6 rows; complete Todd-Coxeter tables verify all106 finite universal orders. The single infinite order retains quoted Theorem5.3.")
        for name in ("phase22_N009_table_labels.md", "phase22_N009_table_labels_certificate.json",
                     "phase22_N009_labels_rank_audit.md", "phase22_N009_labels_rank_audit.json"):
            r["evidence"].append(evidence(name, "All Table6 marked labels and finite universal orders; independent primary-data review and fresh replay"))
        r["exact_target"].append({
            "reference": "Table 6, all107 rows",
            "scope": "All99 rank-four rows and eight rank-five rows, exact marked facet labels and all106 finite universal-group orders. Four printed vertex types are explicitly interpreted using dual markings. The sole infinite row and standard universal-polytope correspondence remain quoted inputs.",
            "relation_to_source": "complete_table_rederivation_with_retained_background",
        })
        r["method"].append("One raw-presentation checker closes all remaining finite examples with34 complete coset enumerations and3328 fullIP meets. The endpoint-coset index bound excludes higher ranks. Exact marked maps expose three literal Table4 duplicates and verify their Table3-consistent repairs; the order-eight central-reduction boundary is explicit.")
        r["retained_inputs"] += ["Quoted standard string-IP criteria (Lemmas2.2–2.4)", "Source Theorem4.2 universal-polytope interpretation"]
        for name in ("phase24_N009_coverage.md", "phase24_N009_coverage.json", "phase24_N009_certificate.json",
                     "phase24_N009_rank_audit.md", "phase24_N009_rank_audit.json"):
            r["evidence"].append(evidence(name, "Complete principal-result coverage with all numbered items and literal source qualifications; independent review passed"))
        r["exact_target"].append({
            "reference": "Example3.9/Tables2–4; Examples4.3–4.5; preliminary rank bounds and quotient lemmas",
            "scope": "All34 raw presentations and their actual IP, exact named bases/facets, all12 Table3 assignments, all8 type48 census markings and the three exhaustive Example4.5 central kernels. Printed Table4 e/f/h identify c/a/c; changing each second RHS to tau gives the distinct Table3 targets. No correction-priority claim.",
            "relation_to_source": "complete_principal_reduction_with_explicit_literal_corrections",
        })
        r["proposed_new_result"] = True
        r["exact_target"].append({
            "reference": "Companion all-rank first-excess classification",
            "scope": "Exactly 5d−10 ordered marked nondegenerate string C-group two-groups of order 2^(2d), for every d>=3. A nonzero binary vector of d−1 edge and d−2 triple parameters describes every involutory string-marked central cover of C_d with kernel gamma3 of order two; IP holds exactly when its active supports have a least member. This uniform theorem is not additional principal-paper credit.",
            "relation_to_source": "proposed_uniform_companion_application",
        })
    if identifier == "N010":
        r["proposed_new_result"] = True
        r["access_coverage"]["notes"] = "Selected Problem 30 passage, front matter and corresponding TeX read; not the entire survey. The 2024 PDF title date is a default compilation date, while arXiv v1 and journal publication are 2006. No whole-problem or current-priority claim."
    if identifier == "L114" and identifier not in UPDATES:
        r["exact_target"] = [{"reference": "Theorems 5.3-5.5 and final paragraph p. 61",
                              "scope": "Realization of the listed rank-three Suzuki RWPRI sublattices beyond Sz(8).",
                              "relation_to_source": "historical_question_current_status_unverified"}]
        r["remaining_work"] = ["Check later primary realizations and complete the geometric realization problem; current external resolution status remains unverified."]
    if identifier == "L084":
        r["remaining_work"] = ["Obtain the actual 2006 erratum, Math. Z. 253, 433-434; the original paper is not this source."]
    if identifier == "N005":
        r["status"] = "related_only"
        r["exact_target"] = [{"reference": "Section 1.1; Proposition 2.2; selected construction definitions and theorem statements",
                              "scope": "Existing general theory for compatible amalgamation, HNN extension and twisting, including the standard typed-Helly equivalences.",
                              "relation_to_source": "prior_art_not_a_replacement_proof"}]
        r["retained_inputs"] = row["retained_inputs"]
        r["remaining_work"] = ["Read and compare complete construction proofs before asserting a replacement theorem. No compression or novelty credit from shared vocabulary."]
    return r


def phase6_network_rows():
    """Normalize the later intake without rewriting its recorded schema."""
    result = []
    for source in load("phase6_network_intake.json")["rows"]:
        available = "fulltext_url" in source
        urls = [source["primary_url"]]
        if available:
            urls.append(source["fulltext_url"])
        if "journal_doi" in source:
            urls.append("https://doi.org/" + source["journal_doi"])
        result.append({
            "id": source["id"], "title": source["title"],
            "publication_year_from_catalogue": source["year"],
            "citation": ", ".join(source["authors"]) + ". " + source.get("venue", source.get("journal_metadata", "arXiv:" + source.get("arxiv", ""))),
            "category": "Network publication", "mathematical": True,
            "fulltext_available": available,
            "reading_scope": "selected_sections_read" if available else "primary_abstract_read_fulltext_unavailable",
            "retrieval_status": "primary_text_accessed" if available else "primary_abstract_or_metadata",
            "status_note": source["coverage_status"] + " " + source.get("source_access", "Reading: " + "; ".join(source.get("reading_scope", []))) + " " + source.get("metadata_caution", ""),
            "assets": [{"url": u} for u in urls], "source_urls": [],
            "intake_file": "phase6_network_intake.json",
            "retained_inputs": source["retained_inputs"],
        })
    return result


def phase16_network_rows():
    """Assign a living-map ID without changing the frozen source intake."""
    source = load("phase16_frattini_geometry_intake.json")
    return [{
        "id": "N008", "title": source["title"],
        "publication_year_from_catalogue": source["year"],
        "citation": ", ".join(source["authors"]) + ". " + source["journal"] + " (2005).",
        "category": "Network publication", "mathematical": True,
        "fulltext_available": True, "reading_scope": source["reading"],
        "retrieval_status": "complete_primary_pdf_verified_from_two_identical_mirrors",
        "status_note": source["scope_note"],
        "assets": [{"url": u} for u in source["primary_urls"]], "source_urls": [],
        "intake_file": "phase16_frattini_geometry_intake.json",
    }]


def phase17_network_rows():
    """Normalize the scoped 2018 intake without modifying its original record."""
    source = load("phase17_k1_source_intake.json")
    bib = source["bibliography"]
    return [{
        "id": "N009", "title": bib["title"],
        "publication_year_from_catalogue": bib["year"],
        "citation": ", ".join(bib["authors"]) + ". " + bib["journal"] + " 13(1) (2018), 1–22.",
        "category": "Network publication", "mathematical": True,
        "fulltext_available": True, "reading_scope": "selected_sections_read",
        "retrieval_status": "primary_pdf_retrieved_selected_sections_read",
        "status_note": "Read introduction, dual-class convention and rank-five Table 6 rows; no complete-paper proof audit.",
        "assets": [{"url": bib["primary_pdf_url"]}, {"url": bib["landing_url"]}],
        "source_urls": [], "intake_file": "phase17_k1_source_intake.json",
    }]


def phase18_network_rows():
    """Register the exact 2006 problem source without inflating paper coverage."""
    source = load("phase18_schulte_weiss_intake.json")
    return [{
        "id": "N010", "title": source["title"],
        "publication_year_from_catalogue": source["year"],
        "citation": ", ".join(source["authors"]) + ". " + source["journal"] + " 53 (2006), 231–255.",
        "category": "Network publication", "mathematical": True,
        "fulltext_available": True, "reading_scope": "selected_sections_read",
        "retrieval_status": "primary_v1_pdf_and_TeX_retrieved_selected_sections_read",
        "status_note": "Problem 30 and source/version metadata read; restricted regular two-group progress only.",
        "assets": [{"url": u} for u in source["primary_urls"]],
        "source_urls": [], "intake_file": "phase18_schulte_weiss_intake.json",
    }]


def phase20_network_rows():
    """Retain a newly read published baseline, without reduction credit."""
    source = load("phase20_linear_rank3_intake.json")
    publication = source["publication"]
    return [{
        "id": "N011", "title": source["title"],
        "publication_year_from_catalogue": publication["year"],
        "citation": ", ".join(source["authors"]) + ". " + publication["journal"] + " 31(4) (2025), 247–259.",
        "category": "Network publication", "mathematical": True,
        "fulltext_available": True, "reading_scope": "selected_sections_read",
        "retrieval_status": "primary_pdf_retrieved_selected_sections_read",
        "status_note": source["reading_scope"] + " Published input only, no rederivation credit.",
        "assets": [{"url": u} for u in source["primary_urls"]],
        "source_urls": [], "intake_file": "phase20_linear_rank3_intake.json",
    }]


def phase22_network_rows():
    """Record a thesis priority source without proof-reduction credit."""
    source = load("phase22_linear_priority_supplement.json")
    meta = source["thesis_metadata"]
    return [{
        "id": "N012", "title": meta["title_english"],
        "publication_year_from_catalogue": meta["title_page_year"],
        "citation": meta["author"] + ". Dissertation, Siberian Federal University, title page 2025; defence 14 May 2026.",
        "category": "Network thesis / priority source", "mathematical": True,
        "fulltext_available": True, "reading_scope": "selected_sections_read",
        "retrieval_status": "primary_institutional_pdf_retrieved_selected_sections_read",
        "status_note": "80-page thesis retrieved; definitions, Theorem3.3.1 and selected sections4.2–4.3 read; printed p72 witness visually checked. No whole-thesis audit or reduction credit.",
        "assets": [{"url": item["url"]} for item in source["sources"]],
        "source_urls": [], "intake_file": "phase22_linear_priority_supplement.json",
    }]


def phase26_network_rows():
    """Assign two previously unindexed primary bridges; source reading only."""
    rows = []
    for identifier, source in zip(("N013", "N014"),
            [p for p in load("phase26_access.json")["papers"] if p["id"] is None]):
        rows.append({
            "id": identifier, "title": source["title"],
            "publication_year_from_catalogue": source["year"],
            "citation": ", ".join(source["authors"]) + ". " + source["version"] + ". " + source["version_note"],
            "category": "Network publication / primary bridge", "mathematical": True,
            "fulltext_available": True, "reading_scope": "selected_sections_read",
            "retrieval_status": "primary_pdf_accessed_selected_sections_read",
            "status_note": source["reading"] + " No whole-paper credit.",
            "assets": [{"url": source["primary_url"]}], "source_urls": [],
            "intake_file": "phase26_access.json",
        })
    return rows


def escaped(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def phase31_network_rows():
    """Relevant cover prior art, preview reading only; no result credit."""
    source = load("phase31_cover_prior_art.json")["rows"][0]
    return [{
        "id": "N015", "title": source["title"],
        "publication_year_from_catalogue": source["year"],
        "citation": ", ".join(source["authors"]) + ". Journal of Algebra650 (2024),123–144. DOI " + source["doi"],
        "category": "Network publication / covering prior art", "mathematical": True,
        "fulltext_available": False, "reading_scope": "abstract_and_selected_publisher_preview_passages",
        "retrieval_status": "primary_publisher_preview_only",
        "status_note": "Abstract, introduction and section snippets read. Exact Theorems4.1/4.4 and complete covering hypotheses unavailable; overlap with the new framework undetermined. No reduction or novelty credit.",
        "assets": [{"url":u} for u in source["primary_urls"]], "source_urls": [],
        "intake_file": "phase31_cover_prior_art.json",
    }]


def linked_title(r):
    title = escaped(r["title"])
    return f"[{title}]({r['primary_urls'][0]})" if r["primary_urls"] else title


def stage(r):
    return r["status"].replace("_", " ")


def render(registry):
    rows, counts = registry["entries"], registry["counts"]
    older = [r for r in rows if r["year"] is not None and 1996 <= r["year"] <= 2006]
    principal = ", ".join(r["id"] for r in rows if r["full_principal_results"])
    out = [
        "# Paper map: intake, encoding and proof coverage", "",
        "This living map distinguishes source access from mathematical progress.",
        "It includes books, proceedings papers and errata as well as journal articles.",
        "The historical inventory is preserved; later assessments apply only to their named targets.", "",
        f"**{len(rows)} mathematical works** are indexed: {counts['catalogue']} catalogue entries and "
        f"{counts['followup']} followups and {counts['network']} network additions. **{len(older)} entries date from 1996–2006.**",
        "This is not complete proof reading or an exhaustive bibliography of every collaborator,",
        "student or postdoc. Coauthorship alone does not establish those relationships.", "",
        "[Registry](research/case_study/paper_registry.json) · [Introduction](INTRODUCTION.md) · "
        "[Reduction scope](research/case_study/torsor_compression_overview.md) · "
        "[Historical inventory](research/case_study/literature_inventory.json)", "",
        "## Read the stages separately", "",
        "| Stage | Meaning |", "|---|---|",
        "| Retrieved | A matched primary full text was accessed; it is not redistributed. |",
        "| Read | Exact scope: abstract, full-text search only, selected sections, or complete short text. |",
        "| Encoded | A specified target has an explicit representation/test; vocabulary alone does not qualify. |",
        "| Rederived | A named theorem, component or finite subfamily has a replacement argument with retained inputs. |",
        "| Principal results rederived | The identified principal results are recovered, not every auxiliary lemma or imported classification. |",
        "| Proposed new result | An internally checked draft consequence; external review and priority verification remain. |",
        "| Unassessed | No replacement-proof assessment is recorded; an empty target list is intentional. This does not mean a source result is unknown or its conjectures remain open. |", "",
        "These are independent fields. A retrieved paper need not be encoded, and progress on",
        "a problem stated in a survey does not imply its inaccessible original paper was read.", "",
        "| Access category | Works |", "|---|---:|",
    ]
    out += [f"| {key.replace('_', ' ')} | {value} |" for key, value in sorted(counts["reading_categories"].items())]
    out += [
        "", f"{counts['retrieved_full_text']} works have a retrieved full text; "
        f"{counts['encoded']} have a specified encoding or conditional/component reduction; "
        f"{counts['rederived']} have a rederived component, finite subfamily or principal target.",
        "These overlapping totals must not be read as counts of fully reduced papers.", "",
        f"The conservative **principal-result set has {counts['full_principal_results']} works: {principal}**.",
        "Proposed conjecture proofs are separate and do not increase that count.", "",
        "## Exact reductions and proposed consequences", "",
        "| ID | Work | Exact target | Scope and remaining work |", "|---|---|---|---|",
    ]
    for r in rows:
        if r["id"] not in UPDATES:
            continue
        ref = "; ".join(t["reference"] for t in r["exact_target"])
        proof = next(e["file"] for e in r["evidence"] if e["file"].endswith(".md"))
        companion = {
            "L034": ("Complete proposed conjecture proof", "phase14_cyclic_tpp.md"),
            "L120": ("Every odd q>=5", "phase15_unitary_sieve.md"),
            "F013": ("All-class theorem and source adapter", "phase15_graded_support_scope.md"),
            "F016": ("Fixed-excess companion theorem", "phase16_fixed_excess.md"),
            "N010": ("Fixed-class transition theory and exact low-excess counts", "phase20_finite_state.md"),
        }.get(r["id"])
        extra_link = (f" [{companion[0]}](research/case_study/{companion[1]})."
                      if companion else "")
        out.append(f"| {r['id']} | {linked_title(r)} | {escaped(ref)} | "
                   f"[{stage(r)}]({proof}).{extra_link} {escaped(' '.join(r['remaining_work']))} |")
    out += [
        "", "## The 1996–2006 track", "",
        "The older entries now include these explicit reductions and proof targets:", "",
        "- **N010 (2006):** Problem 30 is matched to the fixed-excess core reduction",
        "  and complete class-at-most-three marking classification. The original",
        "  unmarked, chiral and mixed-order characterization remains outside the result.",
        "  This source addition gives no principal-paper or whole-problem credit.",
        "- **L102 (2003):** the one-dimensional affine RWPRI spread-space question has a",
        "  proposed existence-and-uniqueness solution by cyclic semilinear descent and",
        "  an explicit scalar affine action. It retains the translation/spread reduction",
        "  and both local primitivity hypotheses. Arbitrary acting subgroups and general",
        "  flag-transitive spread spaces are not classified; external review and priority remain.",
        "- **L092 (2005):** the Hermitian-unital conjecture has a proposed uniform proof via",
        "  an SU(2,q) torsor. This does not rederive every construction in the source paper.",
        "- **L104 (2002):** independent arbitrary-Borel augmentation recovers the full",
        "  principal 8/19/3 census and excludes higher ranks, with every branch exhausted.",
        "  The source geometry list is not an input; complete GAP subgroup data remain.",
        "- **L125/L105/L124 (1998–2002):** the generalized engine admits every primitive",
        "  panel, giving complete explicit J1/M11/M12 censuses under Aut(G)/type equivalence.",
        "  It recovers the stated M12 rank bound. Original chapter/article bodies remain",
        "  unavailable; M11's separate census is not the maximal-subgroup problem L119.",
        "- **L109 (2000):** cyclic/dihedral rank-two rigidity and CRT give an all-rank",
        "  arithmetic classification. Its full all-rank theorem is matched through L110; the original",
        "  full text is unavailable, so a whole-paper comparison remains open.",
        "- **L085 (2006):** involution centralizers exclude every string rank above three,",
        "  marked field coordinates give rank-three existence, and the odd outer quotient",
        "  excludes proper almost-simple extensions. The exact principal theorem is matched",
        "  through L074's primary restatement; the original full body remains unavailable.",
        "- **N001–N003 and L089 (1998–2005):** one tree-cut derivation gives the four",
        "  1998 property tests, the tree correspondence, the known transposition-tree",
        "  geometry branch, and the advertised 2005 path/shadow-IP characterization.",
        "  The foundational 1997 classification is retained; source access differs by work.",
        "- **N003 (2002), complete principal targets:** tree cuts and a sign kernel now",
        "  recover all eight numbered results, with general bounds assessed for finite",
        "  groups and the full generator/geometry classifications for n>=7. Whiston's",
        "  maximum-family theorem and omission trichotomy remain explicit inputs;",
        "  the 1997 geometry classification is unnecessary for this separate reduction.",
        "- **N001 (1998), source access:** the complete indexed primary text is now read,",
        "  including the previously missing proof sections. The original PDF remains",
        "  unavailable; this adds source coverage, not another theorem or measured ratio.",
        "- **N008 (2005), Archer–Cara–Krempa:** a subgroup-intersection ladder and exact",
        "  coset-kernel transport recover the principal Frattini reductions; a coordinate",
        "  basis gives the full finite-p-group geometry classification and residue test.",
        "  The finite relative-generating-set theorem is included. Its unqualified infinite",
        "  converse requires an extra hypothesis; the explicitly infinite geometric theorem",
        "  remains valid by relative finite generation. Gaschütz's quoted structure theorem,",
        "  historical SmallGroups counts and Frattini-computation algorithms are excluded.",
        "- **N004 (2003):** contraction with vertex weights incorporates every tree-family",
        "  truncation. Exact local and full-shadow criteria are proved, with a new Lean",
        "  witness theorem for retained consecutive ranks. The source full text remains",
        "  unavailable, so this is a model-level/advertised-target reduction only.",
        "- **L114/L110 (1999–2001):** trace/torus constructions realize the prime-case",
        "  patterns and decide every printed composite-field pattern. Four have impossible",
        "  intersections; a fifth exists as an embedded lattice but fails RWPRI. A further",
        "  exact matrix example in Sz(2^15) is firm, residually connected, flag-transitive",
        "  and RWPRI, but absent from the asserted exhaustive list. Completeness of that",
        "  list is withdrawn. The later descent argument proves flag transitivity of",
        "  the rank-four extension and gives geometries of every rank. A corrected",
        "  general classification and relative embedding classes remain.",
        "- **L115 (1998):** the 29-object Sz(8) corollary is reproduced, while the all-q",
        "  theorem remains. Witness validity and catalogue-dependent completeness are separate.",
        "- **L096 (2004):** geometric shadow-IP has a Boolean witness criterion. It is",
        "  distinct from C-group subgroup IP. The exact decision/orbit reduction is proved;",
        "  the original Magma implementation and sporadic tables are not rerun.", "",
        "The source-level limitations below are retained verbatim in the JSON. L102's",
        "historical intake says current status was unverified; the later proof entry is a",
        "proposed result, not a silent rewrite of that historical search. L114's realization",
        "question now has the proposed complete displayed-lattice decisions above. L084 is a distinct erratum that still needs",
        "its own full text. Abstract summaries identify topics, not proved theorem reductions.", "",
        "| Year / ID | Work and primary link | Access / progress | Recorded source scope and remaining work |",
        "|---|---|---|---|",
    ]
    for r in sorted(older, key=lambda r: (r["year"], r["id"])):
        detail = r["access_coverage"]["notes"] or "No additional reading scope recorded."
        for update in r["access_coverage"]["additional_readings"]:
            detail += " Later reading: " + update["reading_depth"]
        if r["status"] != "unassessed" or r["id"] in {"L084", "L114"}:
            detail += " Remaining: " + " ".join(r["remaining_work"])
        out.append(f"| {r['year']} / {r['id']} | {linked_title(r)} | "
                   f"{r['access_coverage']['reading_category'].replace('_', ' ')}; {stage(r)} | {escaped(detail)} |")
    out += [
        "", "Earlier mistaken PDF identities for L097, L098, L101 and L123 are explicitly",
        "rejected by the intake: those records remain at abstract depth. L125's original",
        "J1 list must be read with the later correction reported by L105.", "",
        "## Complete mathematical intake", "",
        "All mathematical records are included, even where no exact target is assessed.",
        "The JSON contains citations, primary links, verbatim access notes, methods, retained",
        "inputs, evidence, remaining work and the earlier assessment for comparison.", "",
        "| ID | Year | Work | Access | Mathematical stage |", "|---|---:|---|---|---|",
    ]
    for r in rows:
        out.append(f"| {r['id']} | {r['year'] if r['year'] is not None else 'unconfirmed'} | "
                   f"{linked_title(r)} | {r['access_coverage']['reading_category'].replace('_', ' ')} | {stage(r)} |")
    out += [
        "", "## Updating the map", "",
        "Record source identity and access first. Promote a target only with an exact",
        "statement, replacement derivation and explicit retained inputs. New conjecture",
        "proofs do not count as rederivations of all published principal results. Generic",
        "encodings do not count as reproductions of classification tables.", "",
        "The builder reads historical inputs without changing them. Its explicit target",
        "updates and input hashes make promotions reviewable. Run:", "",
        chr(96)*3 + "sh", "python3 scripts/build_paper_registry.py", chr(96)*3, "",
        "This rebuilds metadata and documentation; it does not rerun proofs, refresh",
        "the literature search or certify the publication snapshot.",
        "See [REPRODUCING.md](REPRODUCING.md) for the separate checks.", "",
    ]
    return "\n".join(out)


def main():
    inventory = load("literature_inventory.json")
    baseline = {r["paper_id"]: r for r in load("compression_audit_rows.json")}
    overlay = load("workspace_proof_audits.json")
    later_readings = {r["catalogue_id"]: r for r in load("phase4_old_problem_intake.json")["entries"]}
    older_access = load("older_literature_updates.json")
    rows = [record(r, baseline, overlay, later_readings, older_access)
            for r in inventory["entries"] if r["mathematical"]]
    rows += [record(r, baseline, overlay, later_readings, older_access)
             for r in load("phase5_network_intake.json")["entries"]]
    rows += [record(r, baseline, overlay, later_readings, older_access)
             for r in phase6_network_rows()]
    rows += [record(r, baseline, overlay, later_readings, older_access)
             for r in phase16_network_rows()]
    rows += [record(r, baseline, overlay, later_readings, older_access)
             for r in phase17_network_rows()]
    rows += [record(r, baseline, overlay, later_readings, older_access)
             for r in phase18_network_rows()]
    rows += [record(r, baseline, overlay, later_readings, older_access)
             for r in phase20_network_rows()]
    rows += [record(r, baseline, overlay, later_readings, older_access)
             for r in phase22_network_rows()]
    rows += [record(r, baseline, overlay, later_readings, older_access)
             for r in phase26_network_rows()]
    rows += [record(r, baseline, overlay, later_readings, older_access)
             for r in phase31_network_rows()]
    assert len({r["id"] for r in rows}) == len(rows)
    for r in rows:
        assert not r["full_principal_results"] or r["rederived"]
        assert not (r["rederived"] or r["encoded"]) or r["exact_target"]
        for e in r["evidence"]:
            assert (ROOT/e["file"]).exists(), (r["id"], e["file"])
    counts = {
        "catalogue": sum(r["origin"] == "catalogue" for r in rows),
        "followup": sum(r["origin"] == "followup" for r in rows),
        "network": sum(r["origin"] == "network" for r in rows),
        "retrieved_full_text": sum(r["access_coverage"]["retrieved_full_text"] for r in rows),
        "reading_categories": dict(Counter(r["access_coverage"]["reading_category"] for r in rows)),
        **{key: sum(r[key] for r in rows) for key in ("encoded", "rederived", "full_principal_results")},
        "statuses": dict(Counter(r["status"] for r in rows)),
    }
    registry = {
        "schema_version": 1, "as_of": "2026-10-10",
        "scope": "All indexed mathematical works; access, encoding and proof coverage are separate and explicitly bounded.",
        "source_inventory_scope": inventory["scope"],
        "source_inputs": [{"file": "research/case_study/"+name,
                           "sha256": sha256((STUDY/name).read_bytes()).hexdigest()} for name in INPUTS],
        "builder": "scripts/build_paper_registry.py",
        "builder_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "excluded_nonmathematical_ids": [r["id"] for r in inventory["entries"] if not r["mathematical"]],
        "definitions": {
            "exact_target": "Empty until a statement or component is assessed; a reference alone does not imply all its claims are rederived.",
            "encoded": "Explicit representation/test or specified conditional reduction, not keyword resemblance.",
            "rederived": "A named existing result, component or finite subfamily, with retained hypotheses.",
            "full_principal_results": "All identified principal results recovered; not every auxiliary lemma or external catalogue.",
            "proposed_new_result": "Internally checked draft consequence; no established priority or external peer review.",
            "primary_urls": "Recorded primary/author/repository links, including abstract and metadata pages; access notes retain identity cautions.",
            "evidence": "Written arguments and saved records have their own scopes; this builder does not execute them.",
            "empty_lists": "For an unassessed record, an empty target/method/input list means not yet assessed, not that the paper has no theorem or needs no input.",
        },
        "counts": counts, "entries": rows,
    }
    (STUDY/"paper_registry.json").write_text(json.dumps(registry, indent=2, ensure_ascii=False)+"\n")
    (ROOT/"PAPER_MAP.md").write_text(render(registry))
    print(json.dumps(counts, indent=2))
    print("Wrote two living maps; historical inputs unchanged.")


if __name__ == "__main__":
    main()
