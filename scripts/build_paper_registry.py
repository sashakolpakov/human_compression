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
          "phase6_network_intake.json")

# id: status, exact target, replacement method, retained inputs, evidence paths,
# remaining work. Semicolons separate inputs and evidence paths.
UPDATES = {
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
        "component_rederived", "Theorem 3.2; Conjecture 3.3 for hereditary powerful-Frattini derived groups, including abelian-Frattini and metacyclic groups; pair-order-at-most-eight and earlier finite classes",
        "Grid/dihedral construction identifies the presentation. A marked isobicyclic normal form excludes the extremal cyclic-core case, proving the cyclic-TPP inequality whenever one factor has order at most four and the hypertope bound whenever one pair order is at most eight. The new Frattini action obstruction proves the hereditary powerful-Frattini class and subsumes metacyclic 2-groups. A separate short theorem covers all odd-order nilpotent cyclic TPP triples; it does not settle the source 2-group conjecture.",
        "Hypertope-to-cyclic-TPP reduction with the geometric hypotheses retained; Published classification of marked isobicyclic 2-groups, including its factor-swapping marking; Bounded group catalogue only for the separate finite-order certificate; Lubotzky-Mann powerful-group power-layer and arbitrary-generating-list factorization theorems for the new hereditary class",
        "compression_phase2.md;phase3_order_bound.md;phase3_cyclic_tpp_exploration.md;phase7_cyclic_tpp.md;phase7_cyclic_tpp_certificate.json;phase10_cyclic_tpp.md;phase10_cyclic_tpp_certificate.json;phase10_cyclic_tpp_independent_audit.md;phase10_cyclic_tpp_independent_audit.json;phase11_abelian_frattini.md;phase11_abelian_frattini_certificate.json;phase11_nilpotent_frattini.md;phase11_nilpotent_frattini_intake.json;phase11_powerful_frattini.md;phase11_powerful_frattini_certificate.json;phase11_metacyclic_adapter.md;phase11_odd_nilpotent.md;formal/BinaryFrattiniActions.lean;formal/BinaryFrattiniActions.scope.md",
        "Unrestricted Conjecture 3.3 and cyclic TPP remain unresolved; a minimum remaining hypertope counterexample has all three pair orders at least sixteen, and a minimum cyclic-TPP counterexample has nonpowerful Frattini subgroup. The hereditary condition cannot simply be dropped. The marked isobicyclic classification is retained, not rederived. The source's alternate dihedral-by-dihedral quotient display is not separately verified; external review and priority remain."),
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
        "The dimension-four form alternative combines with a monomial torus obstruction, transvection equations and the self-centralizing simple socle. The upper bound also applies to PSU4(q)<=G<=PGU4(q). A uniform matrix template generates SU4(q) for q=1 mod4 and has projective IP whenever the middle order is q^2-1 or q^2+1, using two auxiliary forms and a regular-torus bound. Exact checks certify maximum rank four for q=5,9,13, with a failed-IP control at q=9.",
        "Written phase-eight structural theorem; Simplicity of the natural socles; Published rank-four existence for PSL4 and rank-three existence for odd PSU4(q), q>=5; PGL2 maximal-subgroup classification, rank-one unitary identification and perfection; Standard projective unitary order formula and GAP exact finite-field, matrix, orbit and subgroup algorithms",
        "phase9_linear_unitary.md;phase9_linear_unitary_intake.json;phase9_linear_unitary_audit.md;phase9_linear_unitary_status.md;phase8_psl4_rank6.md;formal/TransvectionForms.lean;formal/TransvectionForms.scope.md;phase10_unitary_matrix_certificate.md;phase10_unitary_matrix_intake.json;phase10_unitary_matrix_check.json;phase10_unitary_matrix_independent_audit.md;phase10_unitary_matrix_independent_run.json;phase11_unitary_template.md;phase11_unitary_intersection.md;phase11_unitary_manifest.json;phase11_unitary_examples_root_check.json",
        "Problem 7 remains incomplete: field and graph extensions and general index-two existence are unresolved here. PSU4(q) now has maximum rank four at q=5,9,13. The uniform template leaves existence of the required middle-order parameter unproved, and q=3 mod4 is not covered by that construction. Other survey targets are not collectively settled. Conjecture 2 is cross-referenced under L048, not counted as a second solution; priority and external review remain."),
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
        "phase5_tree_cuts.md;phase5_tree_check.json;phase5_tree_audit.md",
        "Foundational classification remains an input; no end-to-end Lean proof or numerical compression ratio. External review remains."),
    "N002": (
        "component_rederived", "Tree correspondence announced in the primary abstract",
        "An explicit maximal-clique reconstruction converts the foundational diagram conditions into a unique tree; tree-cut geometry realizes it.",
        "Foundational 1997 uniqueness/classification theorem; Classical enumeration of unlabelled trees where numerical counts are used",
        "phase5_tree_cuts.md;phase5_tree_check.json;phase5_tree_audit.md",
        "Source full text unavailable; no full-paper comparison or novel resolution of its historical direct-construction question."),
    "N003": (
        "component_rederived", "Tree-transposition branch of Corollary 2.3 and Theorem 3.2",
        "Forest partition intersections and laminar subset incidence give subgroup intersection, flag transitivity, residue structure and RWPRI.",
        "No retained classification needed for the constructed tree branch; Whole-paper generator classification and Whiston/CFSG arguments remain outside this reduction",
        "phase5_tree_cuts.md;phase5_tree_check.json;phase5_tree_audit.md",
        "Parity-twisted branch, full maximal-independent-generator classification and other general group results are not rederived."),
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
    "L074": ("full_text_read", "All twelve pages of the primary author manuscript read, dated 27 September 2011; journal publication is 2010. Both principal counting theorems, their full proofs, the subgroup table and the L085 restatement are checked.", "phase10_suzuki_marked_fields.md"),
    "L085": ("abstract_read", "Original author abstract read; original full body remains unavailable. The complete principal rank/existence theorem is read through its primary restatement in L074, Theorem 3, manuscript p.5; this does not mean the original L085 sections were read.", "phase10_suzuki_marked_fields.md"),
    "L091": ("selected_sections_read", "Pages 231–233 visually read, including Table 1 and local-two-transitivity/truncation conventions; no HS census reproduction.", "phase6_sporadic_source_audit.md"),
    "L110": ("selected_sections_read", "Rank-three R1–R13, higher-rank construction context and p.11 flag-transitivity uncertainty checked; exact hypotheses compared with L114.", "phase5_suzuki_intake.json"),
    "L114": ("selected_sections_read", "Theorems 5.3–5.5 and their case analyses read; printed pp.58–60 visually checked; Lemma3.11 and final p.61 realization qualification checked.", "phase5_suzuki_intake.json"),
    "N003": ("full_text_read", "All twelve pages of the author manuscript read; publication identity checked against the author catalogue and publisher.", "phase5_network_intake.json"),
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
    if identifier == "L034":
        # Existing construction and a proposed conjecture subcase are separate axes.
        r["proposed_new_result"] = True
        r["exact_target"] = [
            {"reference": "Theorem 3.2", "scope": "The specified grid/dihedral construction is rederived; its alternate quotient display remains unverified.",
             "relation_to_source": "specified_existing_target_or_encoding"},
            {"reference": "Conjecture 3.3 when at least one distinguished pair product has order at most eight; earlier specified classes",
             "scope": "Uniform small-factor cyclic-TPP proof using the retained marked isobicyclic classification, with the geometry-to-TPP reduction explicit. No unrestricted resolution.",
             "relation_to_source": "proposed_consequence"},
        ]
    if identifier == "L074":
        r["exact_target"] = [
            {"reference": "Theorem 1", "scope": "Exact isomorphism-class count of unordered pairs of distinct commuting involutions for every stated odd field exponent.",
             "relation_to_source": "specified_existing_target_or_encoding"},
            {"reference": "Theorem 2", "scope": "Complete Suzuki polyhedron count up to isomorphism and duality, including nondegeneracy; the compact formula is proved equal to the published nested formula in all parameters.",
             "relation_to_source": "specified_existing_target_or_encoding"},
        ]
    if identifier == "L085":
        r["primary_urls"].append("https://math.uni.lu/kiefer/Publications/szpoly3%20r%C3%A9vis%C3%A9.pdf")
        r["primary_urls"] = list(dict.fromkeys(r["primary_urls"]))
    if identifier == "L120":
        r["exact_target"][0]["scope"] = "Dimension-four bilinear-form obstructions give the stated odd linear and unitary intermediate-group upper bounds, with the phase-eight PSL4 argument retained. Field and graph extensions are not covered."
        r["exact_target"].append({
            "reference": "Companion unitary application: conditional template and maximum rank four for PSU4(5), PSU4(9), PSU4(13)",
            "scope": "Explicit matrices give uniform generation for q=1 mod4 and full intersection property conditional on middle projective order q^2-1 or q^2+1. Natural-action certificates at q=5,9,13 check all 256 intersections each. Maximality uses the separate phase-nine upper bound; this is not a separate named survey conjecture, and all-field parameter existence remains unresolved.",
            "relation_to_source": "proposed_finite_companion_application",
        })
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


def escaped(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


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
            "L034": ("Uniform Frattini-class proof", "phase11_powerful_frattini.md"),
            "L120": ("Conditional unitary construction", "phase11_unitary_intersection.md"),
        }.get(r["id"])
        extra_link = (f" [{companion[0]}](research/case_study/{companion[1]})."
                      if companion else "")
        out.append(f"| {r['id']} | {linked_title(r)} | {escaped(ref)} | "
                   f"[{stage(r)}]({proof}).{extra_link} {escaped(' '.join(r['remaining_work']))} |")
    out += [
        "", "## The 1996–2006 track", "",
        "The older entries now include these explicit reductions and proof targets:", "",
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
