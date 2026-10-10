#!/usr/bin/env python3
"""Build the explicit N009 statement ledger and bind the authored evidence.

This is metadata assembly, not an independent mathematical verification.
The optional primary files are recorded by expected hash and excluded from export.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha(name):
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()


def bind(name):
    return {"path": name, "sha256": sha(name)}


CQ = "phase21_central_quotient.md"
KL = "phase21_kernel_ladder.md"
R3 = "phase22_N009_rank3.md"
LAB = "phase22_N009_table_labels.md"
LA = "phase22_N009_lemma_adapters.md"
P55 = "phase21_N009_presentations.md"
NEW = "phase24_N009_coverage.md"
CHECK = "phase24_N009_examples_check.g"
RUN = "phase24_N009_examples_run.json"
items = []


def item(identifier, pages, status, target, mechanism, evidence=(), retained=(), boundary=None):
    record = {
        "id": identifier, "printed_pages": pages, "status": status,
        "exact_target": target, "adapter_or_verification": mechanism,
        "evidence": list(evidence), "retained_inputs": list(retained),
        "remaining_obligation": None,
    }
    if boundary:
        record["boundary_or_literal_discrepancy"] = boundary
    items.append(record)


item("Definition 2.1", [2], "adopted_definition", "Marked string C-group, actual subset IP, rank, type and nondegeneracy.", "Same ordered marking and all-subset IP used in every certificate.", [NEW, CHECK])
item("Lemma 2.2", [3], "retained_prior_input", "Rank-three IP from the two dihedral facets meeting in the middle involution.", "Standard rank-three criterion retained for written quotient adapters; computational checks use all64 meets.", [CQ, NEW], ["N009 reference2: Conder-Oliveros2013, standard string-IP criterion"])
item("Lemma 2.3", [3], "retained_prior_input", "Rank-four prefix-and-suffix intersection criterion, all four hypotheses.", "Retained known criterion; computational certification instead uses all256 actual meets.", [NEW], ["N009 reference2: Conder-Oliveros2013, standard string-IP criterion"])
item("Lemma 2.4", [3], "retained_prior_input", "Rank-five prefix-and-suffix intersection criterion, all five hypotheses.", "Retained known criterion; corresponding certificates test all1024 actual meets.", [LAB, NEW], ["N009 reference2: Conder-Oliveros2013, standard string-IP criterion"])
item("Lemma 2.5", [3], "rederived", "Distinct endpoint rotation cosets; order at least adjacent order times endpoint parabolic; iterated type-product lower bound.", "Actual IP meets endpoint dihedral in one reflection; no nonidentity rotation is in that subgroup.", [NEW], ["Elementary dihedral normal form"])
item("Definition 2.6", [3], "adopted_definition", "Isomorphism carries the distinguished generator set onto the other set, thus identifying path reversal.", "Exact ordered marked isomorphisms followed by reversal Burnside counts; never abstract-group isomorphism alone.", [KL, R3, LAB, NEW])
item("Theorem 2.7", [4], "rederived_with_standard_background", "Every marked string C-group is a smooth quotient of its string Coxeter group.", "Universal presentation map from marked involutions; adjacent orders are specified exactly.", [NEW], ["Standard Coxeter generating-pair order fact"])
item("Lemma 2.8", [5], "rederived_with_standard_background", "Every nonzero binary assignment on a minimal generating list of a finite2-group extends to a coordinate character.", "Coordinate linear functional on G/Phi(G).", [CQ, LA, NEW], ["Burnside basis theorem"], "Finite2-group scope used throughout the paper and the proof; no infinite-group extension asserted.")
item("Lemma 3.1", [5], "rederived", "Normal subgroup disjoint from the product of the two facets gives a quotient with the same type and actual IP.", "Both facets embed; equality of their images puts r^-1*l in N intersect RL.", [NEW], ["Rank-three intersection criterion"])
item("Lemma 3.2", [5], "rederived", "Normal subgroup contained in one facet, whose displayed quotient marking remains rank two, gives rank-three quotient IP.", "Other facet embeds; preimage of the quotient-facet intersection is the original middle subgroup.", [NEW], ["Rank-three intersection criterion"], "The facet quotient must use the displayed images, not an unrelated possible C-group marking.")
item("Corollary 3.3", [6], "rederived", "A central half-rotation gives a rank-three quotient with one adjacent order halved.", "Normal subgroup lies in one facet; its rotation is disjoint from the other facet.", [CQ, NEW], ["Elementary dihedral quotient facts", "Rank-three intersection criterion"])
item("Lemma 3.4", [6, 7], "rederived", "(i) Four nonidentity central candidates in RL; (ii) central product of half-rotations makes both central; (iii) the remaining central candidate would exclude the other three.", "Unique RL rotation normal form proves(i),(ii); the stronger impossibility in Lemma3.5 also implies(iii).", [CQ], ["Dihedral normal forms", "Burnside basis theorem"])
item("Lemma 3.5", [7], "rederived", "The mixed middle-reflection/half-rotation candidate is not central.", "It has the middle generator's Frattini coordinate; centrality would give a commuting Burnside basis.", [CQ], ["Burnside basis theorem"])
item("Theorem 3.6", [7], "rederived", "Every nondegenerate finite string2-group of rank3 has a central order2 quotient that remains a rank3 string C-group.", "Choose a central half-rotation when available, otherwise a central involution outside RL.", [CQ], ["Finite2-group central involution", "Burnside basis theorem", "Rank-three intersection criterion"])
item("Corollary 3.7", [7], "corrected_scope", "Iterated rank-three central reduction, including degenerate products.", "Degenerate groups are C2 times a dihedral factor; reduce that factor until C2^3.", [CQ, NEW], ["Direct product of disconnected marked components"], "Literal unrestricted statement fails at order8: no rank3 group has order4. Correct iteration stops at C2^3; no claim that this boundary issue is previously unknown.")
item("Theorem 3.8", [8, 9], "rederived", "All rank-three central extensions arise from exactly three adjacent-order lift patterns and binary lifts of the defining extra relators.", "Both adjacent orders cannot double by IP; complete base presentation and central-kernel order sandwich give necessity/completeness.", [CQ], ["A complete defining presentation of the base group"], "The theorem does not certify every choice succeeds: exact order, actual IP and marked deduplication remain necessary.")
item("Example 3.9", [9, 10], "verified_computation", "All type48 order1024 ClassI/II/III cases, intended eight named markings and twelve Table3 assignments.", "Raw finite coset enumeration; exact all-subset IP; five primary base labels; eight marked isomorphisms to the unfiltered census.", [NEW, CHECK, RUN, R3], ["Theorem3.8 relator-lift completeness", "Primary Atlas name data"], "Table4 printed presentation errors are recorded separately; they do not invalidate the eight Table3 targets.")
item("Definition 4.1", [11, 12], "adopted_definition", "Universal group presentation assembled from the two complete marked facet presentations and string commutators.", "Every finite universal order checked from this raw presentation, with exact facet embeddings.", [LAB, NEW])
item("Theorem 4.2", [12], "retained_prior_input", "Every group in a nonempty prescribed-facet class is a quotient of its universal group.", "Quoted universal-group principle retained; finite examples verify the presentation and actual facet hypotheses.", [LAB, NEW], ["N009 reference12: McMullen-Schulte, Abstract Regular Polytopes, p97"])
item("Example 4.3", [12, 13], "verified_computation", "The type444 universal group with facets44*32 and44*128 has order512, hence contributes no order1024 quotient.", "Complete raw presentation, all256IP meets, exact marked facet labels and order obstruction.", [NEW, CHECK, RUN, LAB], ["Theorem4.2", "Complete primary facet presentations"])
item("Example 4.4", [13], "verified_computation", "The type444 universal group with facets44*32 and44*256 has order1024 and is source label444*1024a.", "Complete raw presentation, all256IP meets and exact named facet embeddings; unique same-order quotient.", [NEW, CHECK, RUN, LAB], ["Theorem4.2", "Complete primary facet presentations"])
item("Example 4.5", [13, 14], "verified_computation", "The type448 universal group with facets44*64 and48*128a has order2048 and exactly two smooth order1024 quotients, labels e/f.", "Enumerate the complete central-involution set; independently enumerate all three raw quotient presentations; two preserve type/facets, third type444.", [NEW, CHECK, RUN, LAB], ["Theorem4.2", "Normal subgroup of order2 is central", "Complete primary facet presentations"])
item("Lemma 5.1", [17], "retained_prior_input", "Two square-lattice families of finite smooth quotients of[4,4], with their presentations and orders.", "Explicit retained classification behind the center adapter and source's exceptional-group analysis.", [LA, NEW], ["N009 reference12: McMullen-Schulte, pp364-365,368"])
item("Lemma 5.2", [17], "rederived", "Centers in both power-of-two lattice families, with the listed small-parameter exceptions.", "Faithful affine action for the stable range and explicit small-lattice calculations.", [LA, "phase22_N009_centers_check.py", "phase22_N009_centers_check.json"], ["Lemma5.1 lattice classification"], "No missing m=0 assertion for the first family is silently invented; the source's stated cases and adapter boundaries are explicit.")
item("Theorem 5.3", [18], "retained_prior_input", "The exceptional universal group is infinite and is (W1 times W2) semidirect C2^2, with Wi isomorphic to[4,4] and the displayed conjugation action.", "Quoted structural decomposition retained, not inferred from finite NQ quotients.", [LA, LAB, NEW], ["N009 reference11: McMullen-Schulte1990, Adv.Math.82"])
item("Lemma 5.4", [18], "rederived_conditional_on_quoted_decomposition", "Every order1024 marked quotient in the exceptional class has kernel inside W1 times W2 and retains the displayed C2^2 semidirect factor.", "Two Frattini coordinate characters force the kernel inside the product factor.", [LA], ["Theorem5.3 exact decomposition and action", "Burnside basis theorem"])
item("Theorem 5.5", [20], "rederived_with_exact_census", "Exactly two order1024 groups in the exceptional facet class, with the two printed additional-relation presentations.", "Both raw presentations have order1024 and all actual IP meets; exact facets identified; exhaustive unfiltered rank4 census selects exactly these two markings.", [P55, KL, LAB], ["Exact finite-group algorithms", "Full source equivalence convention"])

assert len(items) == 27
table_records = [
    {"id": "Table 1", "printed_pages": [9], "status": "rederived", "exact_target": "All three presentation lift patterns with order-dividing-two central kernel and complete base relator choices.", "evidence": [CQ]},
    {"id": "Table 2", "printed_pages": [10], "status": "verified_computation", "exact_target": "Four literal complete order512 type48 base presentations and named objects.", "evidence": [NEW, CHECK, RUN, "phase24_N009_atlas_library.json"]},
    {"id": "Table 3", "printed_pages": [10], "status": "verified_computation", "exact_target": "All twelve exact lift assignments, including the two collapsed order512 cases.", "evidence": [NEW, CHECK, "phase24_N009_table3_matches.json"]},
    {"id": "Table 4", "printed_pages": [10], "status": "literal_discrepancy_diagnosed", "exact_target": "All eight printed presentations; rows e/f/h are explicitly distinguished from the corresponding Table3 targets.", "evidence": [NEW, CHECK, "phase24_N009_table4_literal_matches.json"], "literal_target_map": {"a":"a","b":"b","c":"c","d":"d","e":"c","f":"a","g":"g","h":"c"}, "proposed_repair": "In rows e,f,h replace the second displayed relator's RHS identity by tau; this is exactly the corresponding checked Table3(tau,tau) case.", "priority": "No first-discovery or erratum-priority claim; original PDF p10 checked visually."},
    {"id": "Table 5", "printed_pages": [11], "status": "rederived_complete_census", "exact_target": "All twelve type categories and125 reversal classes at rank3/order1024.", "evidence": [R3, "phase22_N009_rank3_certificate.json"]},
    {"id": "Table 6", "printed_pages": [14,15,16,17], "status": "rederived_with_named_objects_and_universal_orders", "exact_target": "All107 rows:99 rank4 and8 rank5;105 and8 reversal classes; exact facet labels and106 finite universal orders plus one retained infinite case.", "evidence": [LAB, "phase22_N009_table_labels_certificate.json", "phase22_N009_labels_rank_audit.md"], "boundary": "Four type4164 rows require the orientation interpretation recorded in the earlier proof; no silent relabeling. Infinite universal order is retained Theorem5.3."},
]
extras = [
    {"id": "Preliminary rank1/rank2 discussion", "printed_pages": [4], "status": "elementary_adapter", "target": "Rank1 groupC2; rank2 group dihedral; order1024 rank2 has the unique marked dihedral class.", "evidence": [NEW]},
    {"id": "Disconnected-marking reduction", "printed_pages": [4], "status": "rederived", "target": "Commuting connected-component groups form an internal direct product by actual IP.", "evidence": [NEW], "boundary": "No new complete list of degenerate product markings is claimed; the paper's principal tables are nondegenerate."},
    {"id": "Concluding geometric-realization direction", "printed_pages": [21], "status": "outside_target", "target": "Further study of geometric properties/realizations of associated polytopes.", "remaining_obligation": "Not settled or counted by the group classification certificates."},
]

source = {
    "id": "N009", "authors": ["Y. Gomi", "M. L. Loyola", "M. L. A. N. De Las Peñas"],
    "title": "String C-groups of order 1024", "year": 2018,
    "journal": "Contributions to Discrete Mathematics 13(1), 1–22",
    "doi": "10.55016/ojs/cdm.v13i1.62475",
    "primary_url": "https://cdm.ucalgary.ca/article/download/62475/46803",
    "reading_scope": "All22pages cumulatively read across source-bound phases; current phase visually checked printedp10.",
    "primary_assets": [
        {"path": "sources/phase17_gomi_loyola2018.pdf", "sha256": "0618a57cb5ff35c13587877818a2e77bce442cf2c561f204b6d5e5e095fa2fda", "exported": False},
        {"path": "sources/phase17_gomi_loyola2018.txt", "sha256": "091caf4266f2ac595aec76def47d451700fff7c80f6d0f3eabeee2e6f31f38e7", "exported": False},
    ],
}

coverage = {
    "schema_version": 1, "date": "2026-10-10", "source": source,
    "scope": "Authored source-bound proposed principal-result coverage; independent review is separate. No public registry promotion.",
    "counts": {"numbered_items": len(items), "tables": len(table_records), "other_scope_records": len(extras), "nondegenerate_reversal_classes": {"rank2":1,"rank3":125,"rank4":105,"rank5":8}},
    "principal_result_candidate": True,
    "literal_document_all_claims_true": False,
    "retained_quoted_statements": ["Theorem4.2", "Lemma5.1", "Theorem5.3"],
    "retained_standard_IP_criteria": ["Lemma2.2", "Lemma2.3", "Lemma2.4"],
    "numbered_statements": items, "tables": table_records, "other_scope": extras,
    "raw_presentation_results": json.loads((ROOT / "phase24_N009_examples_results.json").read_text()),
    "table3_all_cells": json.loads((ROOT / "phase24_N009_table3_matches.json").read_text()),
    "table3_encoding": "Base index1..4=a..d; tuple is(R1,R2)tau exponents; target1..8=a..h at order1024, target9=512d; last two columns are grouporder,tauorder.",
    "table4_all_literal_rows": json.loads((ROOT / "phase24_N009_table4_literal_matches.json").read_text()),
    "table4_encoding": "Indices1..8=a..h; [printedrow,intendedTable3targetactuallydefined].",
    "example_exact_facets": json.loads((ROOT / "phase24_N009_example_facets.json").read_text()),
    "evidence_note": bind(NEW), "execution_report": bind(RUN),
    "not_claimed": ["First discovery of a source correction", "Whole-document literal validity", "Rederivation of explicitly quoted prior classification results", "Complete geometric realization theory", "Matched proof or cross-paper length ratio", "A registry principal-count increment before independent review"],
}
(ROOT / "phase24_N009_coverage.json").write_text(json.dumps(coverage, indent=2) + "\n")

new_files = [
    NEW, "phase24_N009_coverage.json", "phase24_N009_build_coverage.py", CHECK,
    "phase24_N009_examples_run.py", RUN, "phase24_N009_examples_check.log",
    "phase24_N009_examples_results.json", "phase24_N009_table3_matches.json",
    "phase24_N009_table4_literal_matches.json", "phase24_N009_example_facets.json",
    "phase24_N009_census_matches.json", "phase24_N009_atlas_extract.py",
    "phase24_N009_atlas_fetch_plan.json", "phase24_N009_atlas_library.json",
    "phase24_N009_atlas_library.g",
]
deps = [CQ, KL, R3, LAB, LA, P55, "phase22_N009_atlas_library.g", "phase22_N009_rank3.accepted.json", "phase22_N009_table_labels_certificate.json", "phase22_N009_labels_rank_audit.md"]
certificate = {
    "date": "2026-10-10", "status": "AUTHORED_CHECKS_PASS_PENDING_INDEPENDENT_REVIEW",
    "source": source, "scope": coverage["scope"],
    "mathematical_replay": "python3 phase24_N009_examples_run.py --gap gap --output-dir /tmp/N009-phase24-review",
    "execution": json.loads((ROOT / RUN).read_text()),
    "new_originals": [bind(name) for name in new_files],
    "retained_dependencies": [bind(name) for name in deps],
    "source_exclusions": source["primary_assets"] + [
        {"path": "sources/"+record["primary_snapshot"], "url": record["url"], "sha256": record["primary_sha256"], "exported": False}
        for record in json.loads((ROOT / "phase24_N009_atlas_library.json").read_text())
    ],
}
cert_name = "phase24_N009_certificate.json"
(ROOT / cert_name).write_text(json.dumps(certificate, indent=2) + "\n")
manifest = {
    "date": "2026-10-10", "scope": coverage["scope"],
    "original_files": [bind(name) for name in new_files + [cert_name]],
    "retained_dependencies": [bind(name) for name in deps],
    "source_exclusions": certificate["source_exclusions"],
    "self_hash": "Deliberately external; parent snapshot binds this manifest.",
}
manifest_name = "phase24_N009_manifest.json"
(ROOT / manifest_name).write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"numbered_items": len(items), "tables": len(table_records), "original_files_including_manifest": len(new_files)+2, "proof_sha256": sha(NEW), "manifest_sha256": sha(manifest_name)}, indent=2))
