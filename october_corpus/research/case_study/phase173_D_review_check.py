#!/usr/bin/env python3
"""Independent binding, source-span, scope and cost audit; not a proof checker."""
import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

MANIFEST = "e751777d290a0f2974f912b7b6ecfa71066e4d951a9e92c352a3b9060070e721"
LEDGER = "ab71112f0eedb237bc29d9a188520e7e133da9f74b7fa891627c956490ac8724"
CORE_REVIEW = "97c8c659ef15a0fb0ff0fb05264a3d32b3189cd8fe5dddf8794b98c2946fef74"


def require(test, message):
    if not test:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def bound(root, item):
    rel = Path(item["path"])
    require(not rel.is_absolute() and ".." not in rel.parts, "unsafe binding")
    data = (root / rel).read_bytes()
    require(len(data) == item["bytes"], "byte count: " + str(rel))
    require(digest(data) == item["sha256"], "digest: " + str(rel))


def span_check(text, span):
    start, end = span["start_codepoint"], span["end_codepoint_exclusive"]
    require(0 <= start < end <= len(text), "span bounds")
    part = text[start:end]
    require(part.startswith(span["heading"] + "\n"), "span heading")
    require(start == 0 or text[start - 1] == "\n", "span start boundary")
    require(end == len(text) or text[end - 1] == "\n", "span end boundary")
    require(len(part.encode()) == span["bytes"], "span bytes")
    require(digest(part.encode()) == span["sha256_utf8"], "span digest")
    require(text[:start].count("\n") + 1 == span["start_line"], "start line")
    require(text[:end].count("\n") == span["end_line"], "end line")


def ledger_check(root, ledger):
    require(ledger["complete_principal_source_contracts"] == ["L066", "L074", "L104"], "complete source scope")
    require(ledger["qualified_source_components"] == ["L073"], "qualified source scope")
    require(ledger["extra_source_credit"] == 0, "new credit")
    require(ledger["ratio"] is None, "unmeasured ratio")
    bound(root, ledger["manuscript"])
    bound(root, ledger["umbrella"])
    text = (root / ledger["manuscript"]["path"]).read_text()
    rows = ledger["contracts"]
    require(len(rows) == ledger["source_inventory_count"] == 41, "row count")
    require(len({row["id"] for row in rows}) == 41, "duplicate source row")
    require(Counter(row["source_id"] for row in rows) == Counter(L066=16, L074=17, L104=4, L073=4), "source row totals")
    sections = ledger["sections"]
    for span in sections.values():
        span_check(text, span)
    spans = 0
    for row in rows:
        require(row["Lean_end_to_end"] is False, "unsupported Lean claim")
        require(bool(row["attribution"].strip()), "missing attribution")
        require(bool(row["proof_spans"]), "missing proof/scope span")
        for span in row["proof_spans"]:
            span_check(text, span)
            require(span in sections.values(), "span not a complete named section")
            spans += 1
    by_id = {r["id"]: r for r in rows}
    require(by_id["L104.4"]["status"] == "remaining_secondary_body_and_supplement_obligations", "J2 omitted body assertions")
    require(by_id["L073.4"]["status"] == "open_comparison_obligation", "M22 unresolved table")
    require(ledger["formal_scope"]["complete_source_theorem_Lean_certificates"] == 0, "Lean source count")
    require(ledger["formal_scope"]["new_formal_certificate"] is False, "new Lean claim")
    return {"source_rows": len(rows), "source_rows_by_source": dict(Counter(r["source_id"] for r in rows)), "section_spans": len(sections), "row_span_bindings": spans}


def manifest_check(root, manifest, private):
    require(manifest["complete_principal_contracts"] == ["L066", "L074", "L104"], "manifest source scope")
    require(manifest["qualified_components"] == ["L073"], "manifest qualified scope")
    for key in ["new_Lean_certificate", "new_open_conjecture_solution", "historical_priority_claim", "full_refined_M22_table_complete"]:
        require(manifest[key] is False, "unsupported claim: " + key)
    require(manifest["new_corpus_principal_credit"] == 0, "new corpus credit")
    items = manifest["files"] + manifest["retained_inputs"]
    require(len(manifest["files"]) == 43 and len(manifest["retained_inputs"]) == 168, "manifest binding count")
    require(len({x["path"] for x in items}) == len(items), "duplicate bindings")
    for item in items:
        bound(root, item)
    if private:
        for item in manifest["private_source_inputs"]:
            bound(root, item)
    by_path = {x["path"]: x for x in items}
    cost = manifest["cost"]
    required = [by_path["phase138_umbrella_v3.md"], by_path["phase164_enumeration_manuscript.md"]]
    require(len(cost["mathematical_programs"]) == 11 and len(cost["drivers"]) == 3, "program count")
    for kind, total in [("mathematical_programs", "mathematical_program_bytes"), ("drivers", "driver_bytes")]:
        for item in cost[kind]:
            require(item == by_path[item["path"]], "unbound charged program")
        require(sum(x["bytes"] for x in cost[kind]) == cost[total], "program cost")
        required.extend(cost[kind])
    require(len({x["path"] for x in required}) == len(required), "double-charged input")
    total = sum(x["bytes"] for x in required)
    require(cost["umbrella_bytes"] == 61576 and cost["application_bytes"] == 60471, "written cost")
    require(total == cost["all_required_written_and_executable_bytes"] == 178689, "required total")
    require(cost["matched_source_ratio"] is None and not cost["encoding_independent_compression_claim"], "ratio claim")
    require(manifest["render"]["pages"] == 18 and manifest["render"]["complete_package_page_count"] is None, "page scope")
    required_paths = {x["path"] for x in required}
    support_new = sum(x["bytes"] for x in manifest["files"] if x["path"] not in required_paths)
    support_retained = sum(x["bytes"] for x in manifest["retained_inputs"] if x["path"] not in required_paths)
    require(support_new == manifest["support_export_bytes"], "support export total")
    return {"new_bindings": 43, "retained_bindings": 168, "private_source_bindings_checked": 4 if private else 0,
            "required_written_and_executable_bytes": total, "marginal_without_U_bytes": total - 61576,
            "additional_new_support_bytes": support_new, "additional_retained_support_bytes": support_retained,
            "all_211_unique_bound_file_bytes": sum(x["bytes"] for x in items),
            "scope_of_cost": "Raw file bytes; excludes the author manifest itself, this review, and private source PDFs. Not a proof-length compression ratio."}


def rejection_controls(root, manifest, ledger):
    results = []
    tests = []
    bad = copy.deepcopy(ledger)
    bad["contracts"][0]["proof_spans"][0]["end_codepoint_exclusive"] -= 1
    tests.append(("truncated proof span", lambda: ledger_check(root, bad)))
    # Bind each closure to its own independent edited record.
    bad2 = copy.deepcopy(ledger)
    bad2["complete_principal_source_contracts"].append("L073")
    tests.append(("unearned fourth complete contract", lambda: ledger_check(root, bad2)))
    bad3 = copy.deepcopy(ledger)
    next(r for r in bad3["contracts"] if r["id"] == "L104.4")["status"] = "supplement_only"
    tests.append(("hidden printed J2 gap", lambda: ledger_check(root, bad3)))
    bad4 = copy.deepcopy(manifest)
    bad4["cost"]["drivers"].pop()
    tests.append(("omitted required driver", lambda: manifest_check(root, bad4, False)))
    bad5 = copy.deepcopy(manifest)
    bad5["files"][0]["sha256"] = "0" * 64
    tests.append(("changed frozen binding", lambda: manifest_check(root, bad5, False)))
    bad6 = copy.deepcopy(manifest)
    bad6["new_Lean_certificate"] = True
    tests.append(("invented Lean certificate", lambda: manifest_check(root, bad6, False)))
    for name, operation in tests:
        try:
            operation()
        except ValueError as exc:
            results.append({"case": name, "rejected": True, "reason": str(exc)})
        else:
            raise ValueError("negative control accepted: " + name)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--check-private-sources", action="store_true")
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    require(not args.report.exists() and not args.report.is_symlink(), "report already exists")
    root = args.input_dir.resolve()
    for name, expected in [("phase164_enumeration_manifest.json", MANIFEST), ("phase164_enumeration_ledger.json", LEDGER), ("phase173_m22_review_export.json", CORE_REVIEW)]:
        require(digest((root / name).read_bytes()) == expected, "frozen input: " + name)
    manifest = json.loads((root / "phase164_enumeration_manifest.json").read_text())
    ledger = json.loads((root / "phase164_enumeration_ledger.json").read_text())
    report = {"status": "PASS", "independently_authored": True, "mathematical_proof_checker": False,
              "manifest_sha256": MANIFEST, "ledger_sha256": LEDGER, "M22_review_manifest_sha256": CORE_REVIEW,
              "bindings_and_cost": manifest_check(root, manifest, args.check_private_sources),
              "source_spans": ledger_check(root, ledger), "negative_controls": rejection_controls(root, manifest, ledger),
              "negative_control_scope": "Binding, source-scope and accounting failures only; no claim of mathematical mutation testing."}
    with args.report.open("x") as stream:
        json.dump(report, stream, indent=2)
        stream.write("\n")
    print(json.dumps({"status": "PASS", "report": str(args.report)}))


if __name__ == "__main__":
    main()
