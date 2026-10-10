#!/usr/bin/env python3
"""Verify the exact Module C package and all source/proof bindings.

This is a structural check, not a mathematical proof or a fresh GAP/Lean run.
Private primary bytes are checked only with --primary-check. Public mode has
no private path or primary-source dependency. Existing outputs are refused.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent


def require(test, message):
    if not test:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def bound(record):
    path = ROOT / record["path"]
    require(path.is_file(), "Missing package input: " + record["path"])
    data = path.read_bytes()
    require(sha(data) == record["sha256"], "Changed package input: " + record["path"])
    if "bytes" in record:
        require(len(data) == record["bytes"], "Changed input size: " + record["path"])
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--primary-check", action="store_true")
    args = parser.parse_args()
    require(not os.path.lexists(args.output), "Refusing existing output path")
    manifest_path = ROOT / "phase150_module_C_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    for record in manifest["files"] + manifest["required_shared_inputs"]:
        bound(record)
    if args.primary_check:
        for record in manifest["private_primary_bindings"]:
            bound(record)
    ledger = json.loads((ROOT / "phase150_module_C_ledger.json").read_text())
    manuscript = bound(ledger["manuscript"]).decode()
    bound(ledger["umbrella"])
    require(ledger["selected_source_ids"] == ["L108", "L088", "N013"], "Changed source intake")
    require(len(ledger["scope_records"]) == 35, "Incomplete source scope ledger")
    require(len({row["id"] for row in ledger["scope_records"]}) == 35, "Duplicate scope records")
    theorem_ids = re.findall(r"^\*\*(?:Theorem|Lemma|Corollary) (C\.[A-Za-z0-9]+)[. (]",
                             manuscript, re.M)
    require(len(theorem_ids) == len(set(theorem_ids)) == 17, "Changed local theorem inventory")
    proof_ids = set(ledger["proof_legs"])
    umbrella_ids = set(ledger["exact_U_interfaces"])
    certificate_ids = {"certificate.construction", "certificate.exhaustive"}

    def verify_span(record, name):
        a, b = record["start_char"], record["end_char"]
        require(isinstance(a, int) and isinstance(b, int) and 0 <= a < b <= len(manuscript),
                "Invalid proof span: " + name)
        body = manuscript[a:b].encode()
        require(len(body) == record["bytes"] and sha(body) == record["sha256"],
                "Incorrect full proof binding: " + name)
        require(len(body) > 100, "Heading-only proof span: " + name)

    for name, leg in ledger["proof_legs"].items():
        verify_span(leg["binding"], name)
        require(set(leg["dependencies"]) <= proof_ids | umbrella_ids | certificate_ids,
                "Unresolved dependency: " + name)
    for row in ledger["scope_records"]:
        require(bool(row["complete_proof_ids"]), "Scope record without disposition: " + row["id"])
        require(set(row["complete_proof_ids"]) <= proof_ids, "Unknown proof ID: " + row["id"])
        require(set(row["final_new_proof_spans"]) == set(row["complete_proof_ids"]),
                "Incomplete scope bindings: " + row["id"])
        for name, record in row["final_new_proof_spans"].items():
            verify_span(record, row["id"] + ":" + name)
            require(record == ledger["proof_legs"][name]["binding"], "Divergent duplicate span")
    report = json.loads((ROOT / "phase150_module_C_render/render_report.json").read_text())
    require(report["manuscript"]["sha256"] == sha(manuscript.encode()), "Wrong rendered edition")
    require((ROOT / "phase150_module_C_render/source.md").read_text() == manuscript,
            "Rendered body omitted or changed text")
    require(report["AST_preserved"] is True, "Renderer changed mathematical nodes")
    require(report["pages"] == 18, "Unexpected page inventory")
    require(not any(re.search(r"Overfull|Missing glyph|Missing character", d, re.I)
                    for d in report["diagnostics"]), "Unresolved rendering failure")
    require(sha((ROOT / "phase150_module_C_render/application.pdf").read_bytes()) == report["PDF_sha256"],
            "Changed rendered PDF")
    visual = json.loads((ROOT / "phase150_module_C_visual_review.json").read_text())
    require(visual["status"] == "AUTHOR_VISUAL_PASS" and visual["all_pages_individually_viewed"]
            and visual["pages"] == 18 and [r["page"] for r in visual["page_records"]] == list(range(1, 19)),
            "Incomplete author visual record")
    require(visual["PDF"]["sha256"] == report["PDF_sha256"] and
            visual["manuscript_sha256"] == sha(manuscript.encode()), "Visual review of different edition")
    costs = json.loads((ROOT / "phase150_module_C_costs.json").read_text())
    programs = [bound(record) for record in costs["required_programs"]]
    require(sum(map(len, programs)) == costs["required_program_bytes"], "Incomplete program charge")
    require(len(manuscript.encode()) + sum(map(len, programs)) == costs["C_plus_programs_bytes"],
            "Incomplete application cost")
    require(len(bound(costs["umbrella"])) + costs["C_plus_programs_bytes"] ==
            costs["U_plus_C_plus_programs_bytes"], "Incomplete shared proof cost")
    require(costs["ratio"] is None and costs["full_source_Lean"] is False,
            "Unsupported measurement or formalization claim")
    infrastructure = [bound(record) for record in costs["support_infrastructure"]]
    require(sum(map(len, infrastructure)) == costs["support_infrastructure_bytes"],
            "Incomplete support charge")
    require(costs["charged_core_plus_support_bytes"] == costs["U_plus_C_plus_programs_bytes"] +
            costs["support_infrastructure_bytes"], "Incomplete core plus support inventory")
    old = json.loads(bound(costs["independent_finite_execution_reused"]))
    for record in costs["required_programs"][:2]:
        require(old["input_hashes"][record["path"]] == record["sha256"], "Different reused finite program")
    require(old["census"]["stage_totals"] == [[4, 100016, 40], [5, 21352, 0]] and
            old["census"]["rank4_conjugacy_and_type_classes"] == 6 and
            old["census"]["rank5_classes_in_all_subgroups"] == 0,
            "Different inherited exhaustive conclusion")
    output = {
        "status": "PASS_STRUCTURAL_BINDINGS_ONLY", "manifest_sha256": sha(manifest_path.read_bytes()),
        "checked_files": len(manifest["files"]) + len(manifest["required_shared_inputs"]),
        "private_primary_check": args.primary_check, "source_ids": ledger["selected_source_ids"],
        "scope_records": 35, "proof_nodes": len(proof_ids), "local_numbered_results": 17,
        "exact_U_interfaces": sorted(umbrella_ids), "exposition_pages": report["pages"],
        "required_program_bytes": costs["required_program_bytes"],
        "U_plus_C_plus_programs_bytes": costs["U_plus_C_plus_programs_bytes"],
        "support_infrastructure_bytes": costs["support_infrastructure_bytes"],
        "charged_core_plus_support_bytes": costs["charged_core_plus_support_bytes"],
        "ratio": None, "fresh_GAP_execution": False, "fresh_Lean_execution": False,
        "independent_mathematical_review": False,
    }
    with args.output.open("x") as stream:
        json.dump(output, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print("MODULE_C_STRUCTURAL_BINDINGS_PASS")


if __name__ == "__main__":
    main()
