#!/usr/bin/env python3
"""Check the Module D driver's refusal of occupied paths and changed programs.

These interface controls do not prove any mathematical classification.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output-dir", type=Path, required=True)
    a = ap.parse_args()
    if os.path.lexists(a.output_dir):
        raise SystemExit("Refusing existing control output path")
    a.output_dir.mkdir(parents=True)
    spec = importlib.util.spec_from_file_location("module_D_driver", ROOT / "phase164_enumeration_run.py")
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    records = []

    def reject(label, output, inputs, marker):
        command = [sys.executable, "-B", "-O", str(ROOT / "phase164_enumeration_run.py"),
                   "--part", "all", "--inputs", str(inputs), "--output-dir", str(output)]
        result = subprocess.run(command, capture_output=True, text=True, timeout=15)
        body = result.stdout + result.stderr
        if result.returncode == 0 or marker not in body:
            raise RuntimeError("Failed interface control: " + label)
        records.append(dict(control=label, rejected=True, marker=marker))

    occupied = a.output_dir / "occupied"
    occupied.mkdir()
    reject("occupied_directory", occupied, ROOT, "Refusing existing output path")
    link = a.output_dir / "dangling_link"
    link.symlink_to(a.output_dir / "missing_target")
    reject("dangling_output_symlink", link, ROOT, "Refusing existing output path")
    for number, changed in enumerate(driver.PROGRAMS):
        inputs = a.output_dir / ("input_" + str(number))
        inputs.mkdir()
        for name in driver.PROGRAMS:
            shutil.copyfile(ROOT / name, inputs / name)
        with (inputs / changed).open("a") as stream:
            stream.write("\n# Interface mutation: this file is not the declared mathematical program.\n")
        output = a.output_dir / ("run_" + str(number))
        reject("changed_" + changed, output, inputs, "Changed program: " + changed)
        if os.path.lexists(output):
            raise RuntimeError("Rejected input created a computation output")
    report = dict(status="PASS", controls=records, count=len(records),
                  scope="Interface refusal only; no mathematical mutation coverage claimed",
                  runner_sha256=hashlib.sha256((ROOT / "phase164_enumeration_run.py").read_bytes()).hexdigest())
    (a.output_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print("MODULE_D_INTERFACE_CONTROLS_PASS", len(records))


if __name__ == "__main__":
    main()
