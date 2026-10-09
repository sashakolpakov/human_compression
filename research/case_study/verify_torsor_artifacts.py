"""Validate saved certificate integrity; this does not rerun mathematical checks."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


lean_reports = []
for name in ["LiftCertificate", "FieldIntersection", "TransvectionIntersection",
             "ResidueConnectivity", "ChamberOrbit", "TorsorPartitions",
             "CoordinateKernels", "SuzukiPentagons", "StringIntersection"]:
    source = ROOT / "formal" / (name + ".lean")
    report_path = source.with_suffix(".check.json")
    report = json.loads(report_path.read_text())
    assert report["exit_code"] == 0, name
    assert report["sha256"] == digest(source), (name, "stale report")
    assert "sorryAx" not in report["stdout"], name
    assert source.with_suffix(".olean").is_file(), name
    lean_reports.append({"source": str(source.relative_to(ROOT)),
                         "sha256": digest(source),
                         "report": str(report_path.relative_to(ROOT)),
                         "report_sha256": digest(report_path),
                         "saved_exit_code": 0,
                         "source_hash_matches": True})

json_checks = []
for name in ["torsor_matrix_check", "commuting_pairs_formula_check",
             "elementary_action_counts", "incidence_matrix_check",
             "phase2_cubic_lattice_check", "suzuki_cycle_check",
             "phase3_extension_check", "phase3_cocycle_linear_check"]:
    report_path = ROOT / (name + ".json")
    report = json.loads(report_path.read_text())
    assert report["status"] == "PASS", name
    if "source_sha256" in report:
        assert report["source_sha256"] == digest(ROOT / (name + ".py")), name
    for source_name, expected in report.get("input_hashes", {}).items():
        assert digest(ROOT / source_name) == expected, source_name
    json_checks.append({"report": report_path.name,
                        "sha256": digest(report_path),
                        "recorded_status": "PASS",
                        "embedded_source_hashes_checked":
                        "source_sha256" in report or "input_hashes" in report})

gq_path = ROOT / "phase3_gq_cycle_check.json"
gq = json.loads(gq_path.read_text())
assert [row["q"] for row in gq] == [3, 5, 7]
for row in gq:
    q = row["q"]
    expected = (q - 1) ** 2 * ((q - 2) ** 2 + 1)
    assert row["recursive_to_moment_isomorphism_checked_on_every_edge"]
    for name in ["symplectic_chamber_deletion", "wenger", "moment_wenger"]:
        sample = row[name]
        assert (sample["vertices"], sample["degree"], sample["girth"]) == (2*q**3, q, 8)
        assert sample["sample_edge_cycle_counts"] == [expected] * 4
        assert sample["independent_disjoint_path_count"] == expected
json_checks.append({"report": gq_path.name, "sha256": digest(gq_path),
                    "saved_results_consistent": True,
                    "scope": "Saved graph parameters and two saved cycle counts agree; graphs not rebuilt."})

log_checks = []
for name in ["commuting_pairs_exception_check", "phase2_edge_inflation_check",
             "phase2_cubic_kernel_check", "classification_rank2_census",
             "classification_field_orbits", "kneser_matrix_check",
             "chiral_fiber_check", "triangle_unital_check",
             "phase3_256_census", "phase3_order_bound_check",
             "phase3_suzuki_probe", "phase3_cyclic_tpp_search"]:
    script = ROOT / (name + ".g")
    output = ROOT / ("suzuki_coset_check.log" if name == "phase3_suzuki_probe"
                     else name + ".log")
    text = output.read_text()
    assert "PASS" in text, name
    assert "Error," not in text and "Syntax error" not in text, name
    log_checks.append({"script": script.name, "script_sha256": digest(script),
                       "log": output.name, "log_sha256": digest(output),
                       "success_marker_present": True})

witness_path = ROOT / "classification_witness_check.json"
witness = json.loads(witness_path.read_text())
assert witness["pass"] and witness["returncode"] == 0
assert witness["script_sha256"] == digest(ROOT / "classification_verify_witnesses.py")
for item in witness["inputs"]:
    assert digest(ROOT / item["file"]) == item["sha256"], item["file"]

classification = json.loads((ROOT / "classification_compression_certificate.json").read_text())
assert classification["status"] == "passed"
for item in classification["artifacts"]:
    assert digest(ROOT / item["file"]) == item["sha256"], item["file"]
for item in classification["imported_subgroup_data"]:
    assert digest(Path(item["file"])) == item["sha256"], item["file"]

phase3_certificates = []
for name in ["phase3_classification_certificate.json", "phase3_gq_certificate.json",
             "suzuki_cycle_certificate.json", "phase3_cyclic_tpp_certificate.json",
             "phase3_bounded_families_certificate.json"]:
    report_path = ROOT / name
    report = json.loads(report_path.read_text())
    for source_name, expected in report["sha256"].items():
        assert digest(ROOT / source_name) == expected, (name, source_name)
    phase3_certificates.append({"file": name, "sha256": digest(report_path),
                                "input_hashes_match": True,
                                "input_count": len(report["sha256"])})

notes = ["torsor_matrix_theory.md", "torsor_compression_overview.md",
         "commuting_pairs_compression.md", "elementary_action_theorem.md",
         "compression_phase2.md", "phase2_cubic_lattices.md",
         "classification_compression.md", "incidence_compression.md",
         "phase3_classification.md", "phase3_order_bound.md",
         "suzuki_cycle_proof.md", "phase3_egr_conjecture_audit.md",
         "phase3_psl4.md", "phase3_bounded_families.md",
         "phase3_cyclic_tpp_exploration.md"]
inventories = ["compression_phase2_constructions.csv", "incidence_certificates.json",
               "classification_compression_certificate.json",
               "classification_J2_representatives.json",
               "classification_Sz8_representatives.json",
               "formal/dependency_manifest.json", "workspace_proof_audits.json"]

manifest = {
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "status": "PASS",
    "verification_mode": "Saved-output integrity audit, not a new execution of all mathematical checks.",
    "limitations": [
        "Nine Lean modules certify their stated components, not complete paper reductions.",
        "GAP computations trust its algorithms and explicitly identified input catalogues.",
        "A source hash or PASS marker is not independently a proof of the mathematical claim.",
        "Written infinite-family arguments require mathematical review beyond finite examples.",
    ],
    "lean_reports": lean_reports,
    "json_checks": json_checks,
    "gap_logs": log_checks,
    "phase3_certificate_input_hashes": phase3_certificates,
    "standalone_classification_witness_check": {
        "report": witness_path.name, "sha256": digest(witness_path),
        "input_hashes_match": True, "recorded_pass": True,
        "scope": "Validity of 8 J2 and 29 Sz8 objects; not completeness or pairwise inequivalence."},
    "classification_input_hashes": {
        "artifact_count": len(classification["artifacts"]),
        "imported_data_file_count": len(classification["imported_subgroup_data"]),
        "all_match": True},
    "proof_drafts": [{"file": name, "sha256": digest(ROOT / name)} for name in notes],
    "input_and_scope_inventories": [{"file": name, "sha256": digest(ROOT / name)}
                                   for name in inventories],
}
target = ROOT / "torsor_verification_manifest.json"
target.write_text(json.dumps(manifest, indent=2) + "\n")
print(f"PASS: {len(lean_reports)} current Lean reports, {len(json_checks)} JSON checks, "
      f"{len(log_checks)} GAP logs, {len(phase3_certificates)} phase-three certificates, "
      "and 37 exported witnesses.")
print("Saved", target)
