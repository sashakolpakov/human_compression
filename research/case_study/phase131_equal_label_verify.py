#!/usr/bin/env python3
"""Verify frozen proof inputs; optionally replay three bounded model checks.

The all-rank results are written proofs with retained theorems. This
program checks integrity and finite computations, not their general validity.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
MANIFESTS = {
    "phase124_equal_label_manifest.json":
        "857988f12d5e4786d69d8a4e65215347e9fa024153e4f3bc3ad043cf52da8da0",
    "phase124_equal_label_additions_manifest.json":
        "89009a809d77952bd34f433060da30fb513abf545a5cbbc6a59b16d7c500532f",
}
CHECKS = (
    ("phase124_equal_label_model_check.py", "phase124_equal_label_model_check_v2.json",
     "phase131_equal_label_model_root.json"),
    ("phase124_equal_label_char2_check.py", "phase124_equal_label_char2_check.json",
     "phase131_equal_label_char2_root.json"),
    ("phase124_even_label_mix_check.py", "phase124_even_label_mix_check.json",
     "phase131_even_label_mix_root.json"),
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def normalized(report):
    return {k: v for k, v in report.items() if k != "seconds"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    require(not args.output.exists() and not args.output.is_symlink(),
            "Refusing to overwrite an occupied output path")
    checked = set()
    for name, expected in MANIFESTS.items():
        path = ROOT / name
        require(not path.is_symlink() and digest(path) == expected, name)
        manifest = json.loads(path.read_text())
        for record in manifest["artifacts"] + manifest.get("retained", []):
            rel = Path(record["path"])
            require(not rel.is_absolute() and ".." not in rel.parts,
                    "Nonlocal manifest path")
            target = ROOT / rel
            require(not target.is_symlink(), str(rel))
            require(target.stat().st_size == record["bytes"] and
                    digest(target) == record["sha256"], str(rel))
            checked.add(str(rel))
        require(set(manifest["export_allowlist"]) ==
                {record["path"] for record in manifest["artifacts"]} | {name},
                "Unexpected export allowlist")
        checked.add(name)

    reports = []
    with tempfile.TemporaryDirectory(prefix="equal-label-replay-") as scratch:
        for script, original, root_report in CHECKS:
            expected = json.loads((ROOT / original).read_text())
            saved = json.loads((ROOT / root_report).read_text())
            require(expected["status"] == "PASS" and
                    expected["script_sha256"] == digest(ROOT / script), script)
            require(normalized(saved) == normalized(expected), root_report)
            item = {"script": script, "saved_root_report_matches": True}
            if args.replay:
                output = Path(scratch) / root_report
                run = subprocess.run([sys.executable, "-B", "-O", str(ROOT / script),
                                      "--report", str(output)],
                                     cwd=scratch, capture_output=True, text=True,
                                     timeout=180)
                require(run.returncode == 0, script + ": " + run.stderr[-2000:])
                fresh = json.loads(output.read_text())
                require(normalized(fresh) == normalized(expected),
                        script + ": fresh report differs")
                item["fresh_replay_matches"] = True
            reports.append(item)
    result = {
        "status": "PASS", "author_artifacts_checked": len(checked),
        "author_manifests": MANIFESTS, "checks": reports,
        "scope": "Frozen bytes and saved/fresh finite reports only; no general proof or priority certificate",
        "all_label_conjecture_solved": False, "whole_claim_Lean": False,
        "script_sha256": digest(Path(__file__)),
    }
    with args.output.open("x") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
