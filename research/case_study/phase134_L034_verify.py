#!/usr/bin/env python3
"""Check the corrected attachment and charge every required proof artifact.

This verifies frozen bytes and accounting, not mathematical validity.
"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FROZEN = {
    "phase130_manifest.json": "2da34395fc89144959952c9cb64b611c6c96694ff252d2ea3ae6efb795b68cb5",
    "phase130_geometry_erratum_manifest.json": "3463aac5e97703f4da2b2b9fdc0ca7c09fcab7448f804a08c040a64994c825ba",
    "phase117_two_group_application_checkpoint04.json": "4f5b965e8c58f01e8bd407e0e1aeabf51e26bdddb9a0dd0d35c483d41f4c101d",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study-root", type=Path, default=ROOT)
    parser.add_argument("--primary-check", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists() and not args.output.is_symlink(), "Fresh output required")
    root = args.study_root.resolve()
    checked = {}

    def check(row):
        path = root / row["path"]
        require(path.is_file() and sha(path) == row["sha256"], "Changed or missing " + row["path"])
        size = row.get("bytes", row.get("utf8_bytes"))
        require(size is None or path.stat().st_size == size, "Changed size " + row["path"])
        checked[row["path"]] = {"sha256": row["sha256"], "bytes": path.stat().st_size}

    for name, expected in FROZEN.items():
        check({"path": name, "sha256": expected})
    manifest = json.loads((root / "phase130_manifest.json").read_text())
    for row in manifest["exports"] + manifest["required_shared_bindings"]:
        check(row)
    erratum = json.loads((root / "phase130_geometry_erratum_manifest.json").read_text())
    check(erratum["frozen_input"])
    check(erratum["correction"])
    intake = json.loads((root / "phase130_intake.json").read_text())
    body = (root / "phase130_typed_helly_L034.md").read_text()
    for section in intake["proof_sections"]:
        text = body[section["start_codepoint"]:section["end_codepoint_exclusive"]]
        require(hashlib.sha256(text.encode()).hexdigest() == section["sha256_utf8"], "Changed proof span")
    if args.primary_check:
        for row in intake["private_primary_bindings"]:
            check(row)
    base = json.loads((root / "phase117_two_group_application_checkpoint04.json").read_text())
    charged = [base["umbrella_required_cost"], base["application"]]
    charged += base["complete_external_certificate_cost"]
    charged += [erratum["frozen_input"], erratum["correction"]]
    require(len(charged) == len({row["path"] for row in charged}) == 8, "Repeated or missing proof cost")
    for row in charged:
        check(row)
    cost = sum(checked[row["path"]]["bytes"] for row in charged)
    require(cost == 208750, "Unexpected complete corrected cost")
    require(intake["conjecture_3_3_solved"] is False and intake["full_Lean_formalization"] is False
            and intake["ratio"] is None, "Changed scope boundary")
    report = {
        "status": "PASS_INTEGRITY_AND_ACCOUNTING_ONLY",
        "mandatory_geometry_correction_checked": True,
        "checked": checked,
        "charged_proof_files": [row["path"] for row in charged],
        "complete_U_A_corrected_attachment_raw_bytes": cost,
        "private_primary_bytes_checked": args.primary_check,
        "ratio": None,
        "new_mathematical_proof_execution": False,
        "runner_sha256": sha(Path(__file__)),
    }
    with args.output.open("x") as stream:
        stream.write(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "complete_raw_bytes": cost,
                      "output": str(args.output)}))


if __name__ == "__main__":
    main()
