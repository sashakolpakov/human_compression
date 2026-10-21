#!/usr/bin/env python3
"""Isolated checks of the independent counter and author renderer refusals."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def require(ok, text):
    if not ok:
        raise RuntimeError(text)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(root):
    result = {}
    for item in sorted(root.rglob("*")):
        name = item.relative_to(root).as_posix()
        if item.is_symlink():
            result[name] = {"symlink": os.readlink(item)}
        elif item.is_file():
            result[name] = {"sha256": sha(item)}
        elif item.is_dir():
            result[name] = {"directory": True}
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--study-root", type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--private-primary-control", action="store_true")
    args = ap.parse_args()
    root = args.study_root.resolve()
    out = args.output_dir.absolute()
    require(not os.path.lexists(out), "Fresh control directory required")
    out.mkdir(parents=True, exist_ok=False)
    public = out / "math_compression/research/case_study"
    public.mkdir(parents=True)
    manifest = json.loads((root / "phase144_manifest.json").read_text())
    names = {entry["path"] for entry in manifest["files"] + manifest["required_shared_inputs"]}
    names.update(["phase144_manifest.json", "phase153_independent_recount.py"])
    for name in names:
        target = public / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / name, target)
    before = snapshot(public)
    counter = [sys.executable, "-B", "-O", str(public / "phase153_independent_recount.py")]
    renderer = [sys.executable, "-B", "-O", str(public / "phase144_measurement.py")]
    rows = []

    def run(label, argv, expected=None, absent=None):
        result = subprocess.run(argv, capture_output=True, text=True, timeout=180)
        (out / (label + ".stdout.txt")).write_text(result.stdout)
        (out / (label + ".stderr.txt")).write_text(result.stderr)
        if expected is None:
            require(result.returncode == 0, result.stdout + result.stderr)
        else:
            require(result.returncode != 0 and expected in result.stderr, "Control failed: " + label)
        if absent is not None:
            require(not os.path.lexists(absent), "Refusal created output: " + label)
        rows.append({"name": label, "passed": True, "returncode": result.returncode})

    positive = out / "portable_recount.json"
    run("portable_positive", counter + ["--output", str(positive)])
    require(snapshot(public) == before, "Portable inputs modified")
    mutations = ["phase144_manifest.json", "phase144_measurement_protocol.json",
                 "phase138_umbrella_v3.md", "phase138_module_A_v2.md",
                 "phase78_n009_integration_census.g", "phase78_n009_integration_finite.g",
                 "phase78_n009_integration_data.g", "phase78_n009_integration_run.py",
                 "phase144_render/replacement.pdf"]
    for i, name in enumerate(mutations):
        target = public / name
        saved = target.read_bytes()
        dest = out / ("mutation_" + str(i) + ".json")
        try:
            target.write_bytes(saved + b"\nMUTATION\n")
            message = "Frozen author manifest changed" if i == 0 else "Bound input changed:"
            run("mutation_" + str(i), counter + ["--output", str(dest)], message, dest)
        finally:
            target.write_bytes(saved)
        require(snapshot(public) == before, "Mutation restoration failed")
    occupied = out / "occupied"
    occupied.mkdir()
    (occupied / "file").write_text("preserve this file\n")
    (occupied / "directory").mkdir()
    (occupied / "directory/sentinel").write_text("preserve this directory\n")
    (occupied / "live").symlink_to("file")
    (occupied / "dangling").symlink_to("absent")
    frozen_occupied = snapshot(occupied)
    for name in ["file", "directory", "live", "dangling"]:
        for label, command, flag, message in [
            ("counter", counter, "--output", "Fresh output required"),
            ("renderer", renderer, "--output-dir", "Refusing existing output directory:")]:
            run(label + "_occupied_" + name,
                command + [flag, str(occupied / name)], message)
            require(snapshot(occupied) == frozen_occupied, "Occupied path modified")
            require(snapshot(public) == before, "A refusal changed inputs")
    if args.private_primary_control:
        source = public / "sources/catalogue_L032.pdf"
        source.parent.mkdir()
        source.write_bytes((root / "sources/catalogue_L032.pdf").read_bytes() + b"\nMUTATION\n")
        dest = out / "changed_primary_must_not_exist.json"
        run("changed_primary", counter + ["--primary", "--output", str(dest)],
            "Primary changed: L032", dest)
        source.unlink()
        source.parent.rmdir()
        require(snapshot(public) == before, "Primary control left input changes")
    result = {"status": "PASS", "control_script_sha256": sha(Path(__file__)),
              "copied_public_input_files": len(names), "public_input_bindings": before,
              "cases": rows, "case_count": len(rows),
              "all_mutated_inputs_restored": True, "all_occupied_paths_unchanged": True,
              "private_primary_control_run": args.private_primary_control,
              "private_primary_needed_for_portable_recount": False,
              "portable_report_sha256": sha(positive),
              "mathematical_GAP_or_Lean_programs_executed": False}
    (out / "report.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "cases": len(rows), "public_files": len(names)}))


if __name__ == "__main__":
    main()
