#!/usr/bin/env python3
"""Fresh pinned compilation of the complete interval-overlap cancellation proof."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

SOURCE = "IntervalOverlapCancellation.lean"
SOURCE_SHA = "7a1072ffb966606b7d0371b7c123220a0498d00a2299b8c76f5ccb7c2f8f4ae5"
DEPENDENCY_SHA = "4c716f4ff0ea4940311014c9853c0b8e5aaab8250f8cefdf9f8003845cfb02e3"
NAMESPACE = "MathCompression.IntervalOverlapCancellation"
DECLARATIONS = {"endpoint_mem", "exists_leaf", "weights_eq_zero"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--packages", type=Path, required=True)
    ap.add_argument("--lean", default="lean")
    ap.add_argument("--source-dir", type=Path,
                    default=Path(__file__).resolve().parent / "formal")
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    output = args.output_dir.absolute()
    require(not os.path.lexists(output), "Fresh output directory required")
    source = args.source_dir.resolve() / SOURCE
    dependency = args.source_dir.resolve() / "dependency_manifest.json"
    require(sha(source) == SOURCE_SHA, "Frozen source changed")
    require(sha(dependency) == DEPENDENCY_SHA, "Frozen dependency manifest changed")
    require(not re.search(r"\b(sorry|admit|axiom|native_decide|unsafe)\b", source.read_text()),
            "Unproved declaration, placeholder or unsafe evaluation")
    deps = json.loads(dependency.read_text())
    lean = shutil.which(args.lean)
    require(lean is not None, "Lean executable not found")
    lean = str(Path(lean).resolve())
    env = dict(os.environ)
    env["ELAN_TOOLCHAIN"] = deps["lean"]
    version = subprocess.check_output([lean, "--version"], env=env, text=True).strip()
    expected_version = deps["lean"].split(":")[-1].removeprefix("v")
    require(re.search(r"\bversion " + re.escape(expected_version) + r"(?:,|\s|\))", version),
            "Unexpected Lean version")
    checked, libraries = [], []
    for item in deps["packages"]:
        checkout = args.packages.resolve() / item["name"]
        revision = subprocess.check_output(
            ["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True).strip()
        require(revision == item["rev"], "Wrong dependency revision: " + item["name"])
        clean = subprocess.run(["git", "-C", str(checkout), "diff", "--quiet", "HEAD", "--"])
        require(clean.returncode == 0, "Tracked dependency changed: " + item["name"])
        library = checkout / ".lake/build/lib/lean"
        if library.is_dir():
            libraries.append(library)
        checked.append({"name": item["name"], "revision": revision,
                        "tracked_files_clean": True,
                        "compiled_library_present": library.is_dir()})
    # The source and dependency manifest are copied, not symlinked. All outputs
    # are created inside one new directory; package caches are read only.
    output.mkdir(parents=True, exist_ok=False)
    executed = output / SOURCE
    shutil.copyfile(source, executed)
    shutil.copyfile(dependency, output / dependency.name)
    require(sha(executed) == SOURCE_SHA, "Copied source changed")
    env["LEAN_PATH"] = os.pathsep.join(map(str, libraries))
    obj = output / SOURCE.replace(".lean", ".olean")
    started = time.monotonic()
    run = subprocess.run([lean, "-o", str(obj), executed.name], cwd=output, env=env,
                         capture_output=True, text=True, timeout=180)
    elapsed = time.monotonic() - started
    log = output / "build.log"
    log.write_text(run.stdout + run.stderr)
    require(run.returncode == 0 and not run.stderr.strip(), run.stdout + run.stderr)
    require(not re.search(r"sorryAx|native_decide|warning:|error:", run.stdout),
            "Unexpected diagnostic or trust axiom")
    matches = re.findall("'" + re.escape(NAMESPACE) +
                         r"\.([A-Za-z_]+)' depends on axioms: \[([^]]*)\]", run.stdout)
    require(len(matches) == len(DECLARATIONS) and {n for n, _ in matches} == DECLARATIONS,
            "Missing or duplicate axiom report")
    reports = {}
    for declaration, text in matches:
        axioms = {a.strip() for a in text.split(",") if a.strip()}
        require(axioms <= {"propext", "Classical.choice", "Quot.sound"},
                "Unexpected axiom: " + declaration)
        reports[NAMESPACE + "." + declaration] = sorted(axioms)
    require(obj.is_file() and not obj.is_symlink(), "Fresh compiler object missing")
    for file, expected in [(source, SOURCE_SHA), (executed, SOURCE_SHA),
                           (dependency, DEPENDENCY_SHA),
                           (output / dependency.name, DEPENDENCY_SHA)]:
        require(sha(file) == expected, "Frozen input changed during compilation")
    result = {"status": "PASS", "date": "2026-10-10", "lean": version,
              "runner_sha256": sha(Path(__file__)), "source_sha256": SOURCE_SHA,
              "dependency_manifest_sha256": DEPENDENCY_SHA, "dependencies": checked,
              "seconds": elapsed, "exit_code": run.returncode,
              "log_sha256": sha(log), "object_sha256": sha(obj),
              "axiom_reports": reports, "stdout": run.stdout, "stderr": run.stderr,
              "substantive_declarations": 3, "whole_stated_interval_theorem_checked": True,
              "acyclicity_assumed": False, "additive_cancellation_assumed": False,
              "trust_boundary": "Exact local source freshly compiled with pinned Lean and clean, pinned package checkouts. Installed compiler and cached compiled package objects are retained; they are not freshly rebuilt.",
              "exclusions": ["group parity-fiber construction", "mixed-group intersection theorem",
                             "orthogonal group or polytope identification", "whole F014 conjecture",
                             "historical novelty", "compression ratio"]}
    (output / "report.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "declarations": 3, "seconds": elapsed,
                      "output": str(output)}, indent=2))


if __name__ == "__main__":
    main()
