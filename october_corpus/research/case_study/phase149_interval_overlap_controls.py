#!/usr/bin/env python3
"""Exercise the interval proof runner in an isolated portable input layout."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def snapshot(root):
    records = {}
    for item in sorted(root.rglob("*")):
        key = item.relative_to(root).as_posix()
        if item.is_symlink():
            records[key] = {"symlink": os.readlink(item)}
        elif item.is_file():
            records[key] = {"sha256": sha(item), "bytes": item.stat().st_size}
        elif item.is_dir():
            records[key] = {"directory": True}
    return records


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--study-root", type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument("--packages", type=Path, required=True)
    ap.add_argument("--lean", required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    root = args.output_dir.absolute()
    require(not os.path.lexists(root), "Fresh control output directory required")
    root.mkdir(parents=True, exist_ok=False)
    isolated = root / "isolated"
    (isolated / "formal").mkdir(parents=True)
    names = ["phase149_interval_overlap_check.py", "formal/IntervalOverlapCancellation.lean",
             "formal/dependency_manifest.json"]
    for name in names:
        shutil.copyfile(args.study_root / name, isolated / name)
    original = snapshot(isolated)
    command = [sys.executable, "-B", "-O", str(isolated / names[0]),
               "--packages", str(args.packages.resolve()), "--lean", args.lean]

    def run(output):
        return subprocess.run(command + ["--output-dir", str(output)], cwd=root,
                              capture_output=True, text=True, timeout=180)

    fresh = root / "portable_replay"
    replay = run(fresh)
    require(replay.returncode == 0, replay.stdout + replay.stderr)
    report = json.loads((fresh / "report.json").read_text())
    require(report["status"] == "PASS", "Portable compile did not pass")
    require(snapshot(isolated) == original, "Portable input changed")
    occupied = root / "occupied"
    occupied.mkdir()
    (occupied / "file").write_bytes(b"preserve file\n")
    (occupied / "directory").mkdir()
    (occupied / "directory" / "sentinel").write_bytes(b"preserve directory\n")
    (occupied / "live").symlink_to("file")
    (occupied / "dangling").symlink_to("missing")
    before = snapshot(occupied)
    tests = []
    for name in ["file", "directory", "live", "dangling"]:
        result = run(occupied / name)
        require(result.returncode != 0 and "Fresh output directory required" in result.stderr,
                "No-clobber control failed: " + name)
        require(snapshot(occupied) == before, "Occupied path changed: " + name)
        tests.append({"control": "occupied " + name, "rejected": True,
                      "all_occupied_entries_unchanged": True})
    before_replay = snapshot(fresh)
    result = run(fresh)
    require(result.returncode != 0 and "Fresh output directory required" in result.stderr,
            "Successful-output reuse was not rejected")
    require(snapshot(fresh) == before_replay, "Successful output changed")
    tests.append({"control": "existing successful output", "rejected": True,
                  "all_existing_entries_unchanged": True})
    for name, expected in [(names[1], "Frozen source changed"),
                           (names[2], "Frozen dependency manifest changed")]:
        target = isolated / name
        original_bytes = target.read_bytes()
        output = root / ("mutation_" + target.stem)
        try:
            target.write_bytes(original_bytes + b"\n")
            result = run(output)
            require(result.returncode != 0 and expected in result.stderr,
                    "Input mutation not rejected: " + name)
            require(not os.path.lexists(output), "Mutation created output: " + name)
        finally:
            target.write_bytes(original_bytes)
        require(snapshot(isolated) == original, "Mutated input was not restored")
        tests.append({"control": "mutation " + name, "rejected": True,
                      "output_not_created": True, "all_inputs_restored": True})
    result = {"status": "PASS", "date": "2026-10-10",
              "control_script_sha256": sha(Path(__file__)),
              "isolated_input_count": len(names), "isolated_input_bindings": original,
              "portable_replay": report, "portable_replay_report_sha256": sha(fresh / "report.json"),
              "controls": tests, "controls_passed": len(tests),
              "private_proof_inputs_used": False,
              "standard_external_package_checkouts_used": True,
              "scope": "Portable fresh proof compilation plus five no-clobber and two bound-input mutation controls; not an independent mathematical review."}
    (root / "report.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "controls": len(tests),
                      "portable_compile_seconds": report["seconds"], "output": str(root)}, indent=2))


if __name__ == "__main__":
    main()
