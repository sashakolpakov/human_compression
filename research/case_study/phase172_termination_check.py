#!/usr/bin/env python3
"""Rebuild the all-rank triangular termination proof against pinned dependencies."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import shutil
import subprocess
import sys
import time

DEPENDENCY_SHA = "4c716f4ff0ea4940311014c9853c0b8e5aaab8250f8cefdf9f8003845cfb02e3"
SHORTLEX_SHA = "8915797c76b26751c81ce5fad927ed68db034d10e5c386afb15115e7afd24ddb"
BASE = "MathCompression.LabelEightCriticalPairs."
GENERIC = "MathCompression.TriangularWordTermination."
MODULES = [
    ("LabelEightCriticalPairs", "22dce0b70cba3f4a9c9e3608bda7ee829e7d3d7352ec96d887e2a2b3a07a092d",
     BASE, {"next_sound", "collect_reachable", "criticalCheck_sound"}),
    ("LabelEightTriangular", "89be51e09e7465668e5c8390b3f5f5ceff009a14f4f19f2318d30950c0b82f64",
     BASE, {"square_tail_triangular", "correction_triangular", "rule_mem_bounds",
            "uniform_step_preserves_range", "uniform_reachable_preserves_range"}),
    ("TriangularWordTermination", "e1c1c5fcee7b7b97f4d29570224268e57770eac45cdad923f41d2c8488aed99c",
     GENERIC, {"blockOrder_wf", "blockOrder_context", "square_decreases", "swap_decreases",
               "triangular_termination"}),
    ("LabelEightTermination", "fd8e45b246d9d61f9eb1166bea29db45cde7f4cb932e92c4f884b33995794f65",
     BASE, {"uniform_step_refines_triangular", "uniform_step_decreases", "uniform_step_accessible",
            "uniform_bounded_step_wf", "collector_terminates_of_accessible", "uniform_collector_terminates"}),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def overlay_mathlib(source, target, relative=Path("Mathlib")):
    """Private directory overlay: cached objects are read through symlinks only."""
    target.mkdir()
    for item in source.iterdir():
        rel = relative / item.name
        out = target / item.name
        if rel in [Path("Mathlib/Data"), Path("Mathlib/Data/List")]:
            overlay_mathlib(item, out, rel)
        elif rel.parent == Path("Mathlib/Data/List") and item.name.startswith("Shortlex."):
            continue
        else:
            out.symlink_to(item, target_is_directory=item.is_dir())


def build(lean, source, obj, cwd, env, expected_declarations):
    started = time.monotonic()
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    run = subprocess.run([lean, "-o", str(obj), str(source)], cwd=cwd, env=env,
                         capture_output=True, text=True, timeout=900)
    elapsed = time.monotonic() - started
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    log = obj.with_suffix(".log")
    log.write_text(run.stdout + run.stderr)
    require(run.returncode == 0 and not run.stderr.strip(), run.stdout + run.stderr)
    require(not re.search(r"sorryAx|native_decide|warning:|error:", run.stdout),
            "Unexpected diagnostic or trust assumption: " + source.name)
    matches = re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]", run.stdout)
    matches += [(name, "") for name in re.findall(r"'([^']+)' does not depend on any axioms", run.stdout)]
    require(len(matches) == len(expected_declarations) and {name for name, _ in matches} == expected_declarations,
            "Missing or duplicate axiom report: " + source.name)
    reports = {}
    for name, text in matches:
        axioms = {a.strip() for a in text.split(",") if a.strip()}
        require(axioms <= {"propext", "Classical.choice", "Quot.sound"}, "Unexpected axiom: " + name)
        reports[name] = sorted(axioms)
    require(obj.is_file() and not obj.is_symlink(), "Fresh object missing: " + source.name)
    return {"source": source.name, "source_sha256": sha(source), "seconds": elapsed,
            "exit_code": run.returncode, "child_user_seconds": after.ru_utime - before.ru_utime,
            "child_system_seconds": after.ru_stime - before.ru_stime,
            "cumulative_child_peak_rss_raw": after.ru_maxrss,
            "peak_rss_units": "bytes" if sys.platform == "darwin" else "KiB",
            "object_sha256": sha(obj), "log_sha256": sha(log), "axiom_reports": reports,
            "stdout": run.stdout, "stderr": run.stderr}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--packages", type=Path, required=True)
    ap.add_argument("--lean", default="lean")
    ap.add_argument("--source-dir", type=Path, default=Path(__file__).resolve().parent / "formal")
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    output = args.output_dir.absolute()
    require(not output.exists() and not output.is_symlink(), "Fresh output directory required")
    source_dir = args.source_dir.resolve()
    dependency = source_dir / "dependency_manifest.json"
    require(sha(dependency) == DEPENDENCY_SHA, "Frozen dependency manifest changed")
    for name, expected, _, _ in MODULES:
        source = source_dir / (name + ".lean")
        require(sha(source) == expected, "Frozen source changed: " + name)
        require(not re.search(r"\b(sorry|admit|axiom|native_decide)\b", source.read_text()),
                "Unproved or native-evaluated declaration: " + name)
    dependencies = json.loads(dependency.read_text())
    lean = shutil.which(args.lean)
    require(lean is not None, "Lean executable not found")
    env = dict(os.environ)
    env["ELAN_TOOLCHAIN"] = dependencies["lean"]
    version = subprocess.check_output([lean, "--version"], env=env, text=True).strip()
    require(re.search(r"\bversion 4\.32\.2(?:,|\s|\))", version), "Unexpected Lean version")
    libraries, checked = [], []
    packages = args.packages.resolve()
    for item in dependencies["packages"]:
        checkout = packages / item["name"]
        revision = subprocess.check_output(["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True).strip()
        require(revision == item["rev"], "Wrong dependency revision: " + item["name"])
        clean = subprocess.run(["git", "-C", str(checkout), "diff", "--quiet", "HEAD", "--"])
        require(clean.returncode == 0, "Tracked dependency changed: " + item["name"])
        library = checkout / ".lake/build/lib/lean"
        if library.is_dir():
            libraries.append(library)
        checked.append({"name": item["name"], "revision": revision,
                        "tracked_files_clean": True, "compiled_library_present": library.is_dir()})
    upstream = packages / "mathlib/Mathlib/Data/List/Shortlex.lean"
    require(sha(upstream) == SHORTLEX_SHA, "Pinned Shortlex source changed")
    output.mkdir(parents=True, exist_ok=False)
    overlay_mathlib(packages / "mathlib/.lake/build/lib/lean/Mathlib", output / "Mathlib")
    env["LEAN_PATH"] = os.pathsep.join(map(str, [output] + libraries))
    upstream_build = build(lean, upstream, output / "Mathlib/Data/List/Shortlex.olean",
                           packages / "mathlib", env, set())
    builds = []
    for name, expected, namespace, declarations in MODULES:
        source = source_dir / (name + ".lean")
        require(sha(source) == expected, "Source changed during execution: " + name)
        builds.append(build(lean, source, output / (name + ".olean"), source_dir, env,
                            {namespace + name for name in declarations}))
    require(sha(dependency) == DEPENDENCY_SHA and sha(upstream) == SHORTLEX_SHA,
            "Dependency source changed during execution")
    for name, expected, _, _ in MODULES:
        require(sha(source_dir / (name + ".lean")) == expected, "Source changed during execution: " + name)
    report = {"status": "PASS", "date": "2026-10-10", "lean": version,
              "runner_sha256": sha(Path(__file__)), "dependency_manifest_sha256": DEPENDENCY_SHA,
              "dependencies": checked, "upstream_builds": [upstream_build], "builds": builds,
              "new_modules": 2, "retained_modules": 2, "new_printed_declarations": 11,
              "total_printed_declarations": 19,
              "scope": "Generic well-founded triangular rewriting, two-sided contextual decrease, actual all-rank label-eight termination for d >= 3 on its finite alphabet, and existence of sufficient fuel for the literal collector.",
              "termination_assumed": False, "confluence_assumed": False,
              "sufficient_fuel_assumed": False, "native_evaluation_axioms": False,
              "trust_boundary": "The pinned upstream Shortlex source and all four local sources are freshly compiled. Other dependency objects are reused from checked package revisions through a private symlink overlay; the package cache is never written. The installed compiler and those cached dependency objects remain trusted. Inherited LEAN_PATH is replaced.",
              "exclusions": ["all-rank local confluence", "all-rank confluence",
                             "unique normal forms", "group order", "intersection property",
                             "all-integer source relators", "complete polytope construction",
                             "uniform numerical fuel bound", "source compression ratio", "priority"]}
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "new_modules": 2, "new_printed_declarations": 11,
                      "seconds": sum(b["seconds"] for b in builds) + upstream_build["seconds"],
                      "output": str(output)}, indent=2))


if __name__ == "__main__":
    main()
