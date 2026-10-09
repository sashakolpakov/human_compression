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
          "older_literature_updates.json", "phase5_network_intake.json")

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
        "component_rederived", "Theorem 3.2; specified cases of Conjecture 3.3",
        "Grid/dihedral construction identifies the presentation; cyclic triple-product inequalities give lower-bound classes.",
        "Hypertope correspondence with geometric hypotheses explicitly verified; Bounded group catalogue for the separate finite certificate",
        "compression_phase2.md;phase3_order_bound.md;phase3_cyclic_tpp_exploration.md",
        "Full Conjecture 3.3 remains unresolved. The source's alternate dihedral-by-dihedral quotient display is not separately verified."),
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
        "partial_progress", "Odd-characteristic PSL4 maximum rank; exact conjecture read in L120, Conjecture 2",
        "Projective involution commutator forms, Pauli supports and tensor-form obstructions give upper bound six.",
        "Elementary-abelian projective representation dimension bound; Written finite-field/projective identifications",
        "phase3_psl4_rank7.md;phase3_psl4.md;formal/StringIntersection.lean;psl4_search_results.md",
        "Ranks five and six remain. L048 full text was unavailable; progress through the survey does not imply it was read. External review and priority remain."),
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
        "commuting_pairs_compression.md;elementary_action_theorem.md;commuting_pairs_formula_check.json",
        "External review; no priority claim for classical orbit, Burnside or Möbius ingredients."),
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
    "L104": (
        "principal_results_rederived", "Complete principal census: 8 rank-two, 19 rank-three, 3 rank-four geometries, and no higher ranks",
        "Arbitrary-Borel panel augmentation exhausts all ranks; normalizer permutation actions and full automorphism/type fusion recover the census without source geometry lists.",
        "Complete J2 subgroup-class data from GAP TomLib; GAP exact finite-group algorithms; Written arbitrary-rank recognition and completeness theorem",
        "phase5_j2_theory.md;phase5_j2_certificate.json;phase5_j2_progress.json;phase5_j2_root_review.md",
        "The subgroup catalogue and every secondary supplement annotation are not rederived. No end-to-end Lean formalization; external review remains."),
    "L109": (
        "component_rederived", "Complete all-rank three-family classification and counts quoted in L110 Theorem 4; rank-two theorem quoted in L114 Theorem 5.1",
        "Rank-two rigidity upgrades RWPRI to every parabolic edge being maximal; dihedral subgroup arithmetic gives three patterns, CRT Helly and an all-rank counting formula.",
        "Elementary subgroup structure of cyclic and dihedral groups; Exact equivalence convention retains the specified group action",
        "phase5_dihedral_classification.md;phase5_dihedral_check.json;phase5_dihedral_audit.md;phase5_dihedral_intake.json",
        "L109 full text remains unavailable; its complete all-rank principal classification is available in the primary L110 restatement, but every original statement has not been compared. No new-conjecture or whole-paper claim."),
    "L110": (
        "partial_progress", "Rank-three shapes R1–R13: exact bare-embedding and RWPRI decisions",
        "A trace transversal gives explicit prime-order involution pairs; split-dihedral uniqueness and involution-center rigidity constrain simultaneous subfield positions.",
        "Standard Suzuki subgroup conjugacy and centralizers; Torus normalizers and element-order structure; Exact source parameter restrictions",
        "phase5_suzuki_higher.md;phase5_suzuki_realization.md;phase5_suzuki_higher_intake.json;phase5_suzuki_independent_audit.md",
        "Higher-rank constructions, all relative positions and flag transitivity remain. External priority and review unverified; subgroup realization alone is not geometric classification."),
    "L114": (
        "proposed_new_result", "Theorems 5.3 and 5.5: every displayed parameter shape; final p.61 realization question",
        "All prime-case shapes exist. Composite shapes1,2,3,5 have impossible intersections;4,6,7,8,10 admit RWPRI realizations;9 admits the printed intersections but cannot satisfy RWPRI.",
        "Published candidate-list completeness and Theorem5.4 nonexistence; Standard Suzuki subgroup conjugacy, centralizers, torus structure and prime-degree subfield maximality",
        "phase5_suzuki_higher.md;phase5_suzuki_realization.md;phase5_suzuki_higher_intake.json;phase5_suzuki_independent_audit.md;phase5_suzuki_check.json;phase5_suzuki_higher_check.json",
        "Full flag transitivity, all relative positions and geometric isomorphism classification remain. Publication priority is unverified and external review outstanding; this is a proposed resolution of the displayed-lattice realization question."),
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
    "L115": (
        "finite_subfamily_reproduced", "Corollary 8.1: 29 rank-two geometries of Sz(8)",
        "Normalizer-orbit classification with type reversal; 75 inner classes fuse to 29.",
        "Complete Sz(8) subgroup-class data from GAP TomLib",
        "classification_compression.md;classification_compression_certificate.json;classification_witness_check.json",
        "All-q Theorem 7.1 is not rederived. A finite corollary does not give whole-paper coverage."),
}

READING_UPDATES = {
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
        "evidence": [evidence("phase5_network_intake.json" if identifier.startswith("N") else "literature_inventory.json", identifier + " intake only")],
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
    if identifier == "L114" and identifier not in UPDATES:
        r["exact_target"] = [{"reference": "Theorems 5.3-5.5 and final paragraph p. 61",
                              "scope": "Realization of the listed rank-three Suzuki RWPRI sublattices beyond Sz(8).",
                              "relation_to_source": "historical_question_current_status_unverified"}]
        r["remaining_work"] = ["Check later primary realizations and complete the geometric realization problem; current external resolution status remains unverified."]
    if identifier == "L084":
        r["remaining_work"] = ["Obtain the actual 2006 erratum, Math. Z. 253, 433-434; the original paper is not this source."]
    return r


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
        out.append(f"| {r['id']} | {linked_title(r)} | {escaped(ref)} | "
                   f"[{stage(r)}]({proof}). {escaped(' '.join(r['remaining_work']))} |")
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
        "- **L109 (2000):** cyclic/dihedral rank-two rigidity and CRT give an all-rank",
        "  arithmetic classification. Its full all-rank theorem is matched through L110; the original",
        "  full text is unavailable, so a whole-paper comparison remains open.",
        "- **N001–N003 and L089 (1998–2005):** one tree-cut derivation gives the four",
        "  1998 property tests, the tree correspondence, the known transposition-tree",
        "  geometry branch, and the advertised 2005 path/shadow-IP characterization.",
        "  The foundational 1997 classification is retained; source access differs by work.",
        "- **L114/L110 (1999–2001):** trace/torus constructions realize the prime-case",
        "  patterns and decides every printed composite-field pattern. Four have impossible",
        "  intersections; a fifth exists as an embedded lattice but fails RWPRI. Full flag",
        "  transitivity and embedding classification remain; priority is unverified.",
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
