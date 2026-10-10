#!/usr/bin/env python3
"""Read-only evidence checks plus fast refusal tests; no GAP/Lean rerun."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


def bind(path):
    data = path.read_bytes()
    return {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report", type=Path, required=True)
    args = ap.parse_args()
    if args.report.exists() or args.report.is_symlink():
        raise FileExistsError("Existing report refused")
    root = Path(__file__).resolve().parent
    public = root.parents[1] / "math_compression/research/case_study"
    scratch = Path("/private/tmp/hc_phase67_family_public")
    lean_build = Path("/private/tmp/hc_phase68_lean_first")
    expected = {
        "phase67_cover_family_verify.py": "2fcdbfd5c838ea6b1af6db65f78e3b7ac69c5ef21d259222685f55087344c079",
        "phase49_cover_family_check.g": "999a878716810ab4ce476ea2a45c6986d36ef9530a7d02ef3a3871074dab3cfe",
        "phase49_cover_family_theorem.md": "769ddbf891597c3c0d6246ad3f93b354dd02226e02d90cff1eaa250b7bbd4725",
        "phase59_cover_family_recent_audit.json": "efb1466200ba01263dba5532cee6c64379128088d104314208cb4181fb9a82c6",
        "formal/CoverCharacterSeparation.lean": "867acfc453c907055b0658340394c823068b636f1a46813fd4aa783b3b834d79",
        "formal/dependency_manifest.json": "4c716f4ff0ea4940311014c9853c0b8e5aaab8250f8cefdf9f8003845cfb02e3",
        "phase68_cover_character_check.py": "ad46f95fc178b450689ced1dbe03fcfb2ca3cc31b9e3a5fa0f1f867dfc669e1a",
    }
    inputs = {name: bind(root / name) for name in expected}
    assert all(inputs[name]["sha256"] == sha for name, sha in expected.items())
    public_equal = []
    for name in list(expected)[:4]:
        assert (root / name).read_bytes() == (public / name).read_bytes()
        public_equal.append(name)
    for suffix, filename in [("replay.json", "report.json"), ("stdout.log", "stdout.log"),
                             ("stderr.log", "stderr.log"), ("canonical.log", "canonical_stdout.log")]:
        name = "phase67_cover_family_public_" + suffix
        assert (root / name).read_bytes() == (public / name).read_bytes() == (scratch / filename).read_bytes()
        inputs[name] = bind(root / name)
        public_equal.append(name)
    report = json.loads((scratch / "report.json").read_text())
    assert report["status"] == "PASS" and report["exit_code"] == 0 and not report["timed_out"]
    assert report["runner_sha256"] == expected["phase67_cover_family_verify.py"]
    assert report["bound_inputs"] == {k: expected[k] for k in list(expected)[1:4]}
    raw = (scratch / "stdout.log").read_bytes()
    canonical = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    assert canonical.encode() == (scratch / "canonical_stdout.log").read_bytes()
    assert not (scratch / "stderr.log").read_bytes()
    for field, filename in [("stdout_sha256", "stdout.log"), ("stderr_sha256", "stderr.log"),
                            ("canonical_stdout_sha256", "canonical_stdout.log")]:
        assert report[field] == bind(scratch / filename)["sha256"]
    assert report["canonical_stdout_sha256"] == "e89d679dc4de9be0c049002235ccee4bef8548ef7ac3c8ab2197a584e8f77a77"
    assert bind(scratch / "certificate.g")["sha256"] == expected["phase49_cover_family_check.g"]
    pars = [(3, 2, 1), (3, 2, 2), (3, 3, 1), (3, 3, 2)] + [(5, 2, k) for k in range(1, 5)]
    assert [(c["p"], c["alpha"], c["k"]) for c in report["cases"]] == pars
    for case in report["cases"]:
        p, alpha = case["p"], case["alpha"]
        q = p**alpha
        assert case["orders_P_R_T_Q_Qdual_H"] == [4*p*p*q, 4*p**3*q, 4*p*p*q, 4*p**4*q, 4*p**4*q, 4*p**5*q]
    before = {p.name: bind(p) for p in scratch.iterdir() if p.is_file()}
    assert len(before) == 5
    command = ["/Users/sasha/.venvs/global/bin/python", str(public / "phase67_cover_family_verify.py"),
               "--output-dir", str(scratch), "--gap", "/opt/homebrew/bin/gap"]
    refusal = subprocess.run(command, capture_output=True, text=True, timeout=10)
    assert refusal.returncode == 2 and "refusing to overwrite" in refusal.stderr and not refusal.stdout
    after = {p.name: bind(p) for p in scratch.iterdir() if p.is_file()}
    assert before == after

    lean = json.loads((lean_build / "report.json").read_text())
    assert lean["status"] == "PASS" and "version 4.32.2," in lean["lean"]
    assert lean["source_sha256"] == expected["formal/CoverCharacterSeparation.lean"]
    assert lean["runner_sha256"] == expected["phase68_cover_character_check.py"]
    assert lean["dependency_manifest_sha256"] == expected["formal/dependency_manifest.json"]
    log = (lean_build / "build.log").read_text()
    assert bind(lean_build / "build.log")["sha256"] == lean["build_log_sha256"]
    assert not re.search(r"sorryAx|native_decide|warning:|error:", log)
    matches = re.findall(r"'MathCompression\.CoverCharacterSeparation\.([^']+)' depends on axioms: \[([^]]*)\]", log)
    axioms = {n: sorted(a.strip() for a in entries.split(",") if a.strip()) for n, entries in matches}
    assert len(matches) == 3 and axioms == lean["axiom_reports"]
    assert axioms == {
        "no_marked_cover_iso": ["Quot.sound", "propext"],
        "ne_inv_of_odd_prime_order": ["Classical.choice", "Quot.sound", "propext"],
        "no_marked_cover_iso_of_odd_prime_order": ["Classical.choice", "Quot.sound", "propext"],
    }
    deps = json.loads((root / "formal/dependency_manifest.json").read_text())
    assert {i["name"]: i["revision"] for i in lean["dependencies"]} == {i["name"]: i["rev"] for i in deps["packages"]}
    assert all(i["tracked_files_clean"] for i in lean["dependencies"])
    for name in ("formal/CoverCharacterSeparation.scope.md", "phase67_cover_family_no_clobber.json"):
        inputs[name] = bind(root / name)
    for name, value in inputs.items():
        assert bind(root / name) == value
    result = {
        "schema": "phase69_wrapper_formal_interface_evidence_v1", "status": "PASS",
        "script": bind(Path(__file__)), "input_bindings": inputs,
        "private_public_identical_files": public_equal,
        "root_fresh_eight_case_replay_seconds": report["elapsed_seconds"],
        "reviewer_repeated_eight_case_computation": False,
        "canonical_log_exact_previous_match": True,
        "reviewer_fresh_existing_directory_refusal": {
            "argv": command, "returncode": refusal.returncode, "stdout": refusal.stdout,
            "stderr": refusal.stderr, "unchanged_files": before, "file_count": 5},
        "root_Lean_build_report": bind(lean_build / "report.json"),
        "root_Lean_build_log": bind(lean_build / "build.log"),
        "axiom_reports": axioms, "reviewer_repeated_Lean_build": False,
        "trust_boundary": "Existing compiled dependency objects remain trusted. Root build evidence was bound and read; no fresh dependency audit or build is claimed here.",
        "semantic_review_is_separate_written_record": True,
        "inputs_unchanged": True,
    }
    with args.report.open("x") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    print(json.dumps({"status": "PASS", "report": str(args.report), **bind(args.report)}, indent=2))


if __name__ == "__main__":
    main()
