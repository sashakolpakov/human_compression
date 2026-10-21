#!/usr/bin/env python3
"""Compile the supported-kernel consequences and their exact retained proof closure."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

DEPENDENCY_SHA = "4c716f4ff0ea4940311014c9853c0b8e5aaab8250f8cefdf9f8003845cfb02e3"
MODULES = [
    ("LiftCertificate.lean",
     "d8429bd867cbc8ea29c6af9768d93df49c5be027328f2b25fa32102cbc3009d7",
     "LeemansLift",
     {"reversing_preserves_power_subgroup", "noReverser_of_cyclic_kernel",
      "cyclic_intersection_transfer", "intersection_of_image_and_kernel"}),
    ("CoordinateKernels.lean",
     "168fb88f08a5f7a4bc41d403ac1e288fe8a7641c3714fc23ac80295414fac4d6",
     "LeemansCoordinates",
     {"coordinate_kernel_meet", "intersection_transport_with_coordinates"}),
    ("SupportedKernelGeneration.lean",
     "1fb99082407826a390e975432c5f12d1e665ac66af9d18fbb75532af5a57f10a",
     "MathCompression.SupportedKernelGeneration",
     {"triangular_isolation", "coordinate_mem_marked_inter", "marked_compatibility",
      "marked_base_fixed", "local_kernel_witness", "pure_kernel_mem", "kernel_profile",
      "generated_eq_fiber", "marked_intersection_property", "supported_kernel_construction"}),
    ("SupportedKernelConsequences.lean",
     "12f45316150aeaa73b3de38ea1338daa5d23dfa678bebf0f07504fac9adf5083",
     "MathCompression.SupportedKernelGeneration",
     {"baseProjection_range", "kernelCoordinatesEquiv", "parabolic_cardinality",
      "local_projection_bijective", "separator_factorization",
      "pure_kernel_mem_lowerCentralSeries", "lowerCentralSeries_eq_kernel"}),
]
MATHLIB_REBUILDS = [
    ("Mathlib.GroupTheory.Commutator.Finite",
     "42f43c83c3b42913128aa30933a73363c485cf2bc69fc613214486004b504ca0"),
    ("Mathlib.GroupTheory.Nilpotent",
     "fc6e3be0b9f9cd7999d8a8c2232ce111055d6fe8be6e8dce335fe4581079ca87"),
]


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
    require(not output.exists() and not output.is_symlink(), "Fresh output directory required")
    source_dir = args.source_dir.resolve()
    dependency_file = source_dir / "dependency_manifest.json"
    require(sha(dependency_file) == DEPENDENCY_SHA, "Frozen dependency manifest changed")
    for name, expected, _, _ in MODULES:
        source = source_dir / name
        require(sha(source) == expected, "Frozen source changed: " + name)
        require(not re.search(r"\b(sorry|admit|axiom)\b", source.read_text()),
                "Unproved source declaration or placeholder: " + name)
    dependencies = json.loads(dependency_file.read_text())
    lean = shutil.which(args.lean)
    require(lean is not None, "Lean executable not found")
    env = dict(os.environ)
    env["ELAN_TOOLCHAIN"] = dependencies["lean"]
    version = subprocess.check_output([lean, "--version"], env=env, text=True).strip()
    expected_version = dependencies["lean"].split(":")[-1].removeprefix("v")
    require(re.search(r"\bversion " + re.escape(expected_version) + r"(?:,|\s|\))", version),
            "Unexpected Lean version")
    checked, libraries = [], []
    for item in dependencies["packages"]:
        checkout = args.packages.resolve() / item["name"]
        rev = subprocess.check_output(
            ["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True).strip()
        require(rev == item["rev"], "Wrong dependency revision: " + item["name"])
        clean = subprocess.run(["git", "-C", str(checkout), "diff", "--quiet", "HEAD", "--"])
        require(clean.returncode == 0, "Tracked dependency changed: " + item["name"])
        library = checkout / ".lake/build/lib/lean"
        if library.is_dir():
            libraries.append(library)
        checked.append({"name": item["name"], "revision": rev, "tracked_files_clean": True,
                        "compiled_library_present": library.is_dir()})
    mathlib = args.packages.resolve() / "mathlib"
    for name, expected in MATHLIB_REBUILDS:
        source = mathlib / (name.replace(".", "/") + ".lean")
        require(sha(source) == expected, "Frozen Mathlib source changed: " + name)
    output.mkdir(parents=True, exist_ok=False)
    # Lean selects one root for a module namespace. Construct a private overlay
    # which reuses every cached Mathlib object except these two fresh rebuilds.
    # Never link any target stem which the compiler can overwrite.
    cached = mathlib / ".lake/build/lib/lean"
    ancestors = {"Mathlib", "Mathlib/GroupTheory", "Mathlib/GroupTheory/Commutator"}
    stems = {name.replace(".", "/") for name, _ in MATHLIB_REBUILDS}

    def overlay(relative):
        directory = output / relative
        directory.mkdir(parents=True, exist_ok=False)
        for item in sorted((cached / relative).iterdir()):
            rel = item.relative_to(cached).as_posix()
            if rel in ancestors:
                overlay(rel)
            elif not any(rel == stem or rel.startswith(stem + ".") for stem in stems):
                (output / rel).symlink_to(item)

    overlay("Mathlib")
    env["LEAN_PATH"] = os.pathsep.join(map(str, [output] + libraries))
    upstream_builds = []
    for name, expected in MATHLIB_REBUILDS:
        source = mathlib / (name.replace(".", "/") + ".lean")
        obj = output / (name.replace(".", "/") + ".olean")
        require(not obj.exists() and not obj.is_symlink(), "Fresh Mathlib object required")
        started = time.monotonic()
        run = subprocess.run([lean, "-o", str(obj), str(source)], cwd=mathlib, env=env,
                             capture_output=True, text=True, timeout=180)
        elapsed = time.monotonic() - started
        log = output / (name + ".log")
        log.write_text(run.stdout + run.stderr)
        require(run.returncode == 0 and not run.stderr.strip(), run.stdout + run.stderr)
        require(not re.search(r"sorryAx|native_decide|warning:|error:", run.stdout),
                "Unexpected Mathlib diagnostic: " + name)
        require(obj.is_file() and not obj.is_symlink(), "Fresh Mathlib object missing")
        require(sha(source) == expected, "Mathlib source changed during execution: " + name)
        upstream_builds.append({"module": name, "source_sha256": expected,
                                "seconds": elapsed, "exit_code": run.returncode,
                                "object_sha256": sha(obj), "log_sha256": sha(log),
                                "stdout": run.stdout, "stderr": run.stderr})
    builds = []
    for name, expected_sha, namespace, declarations in MODULES:
        source = source_dir / name
        require(sha(source) == expected_sha, "Frozen source changed during execution: " + name)
        started = time.monotonic()
        obj = output / name.replace(".lean", ".olean")
        run = subprocess.run([lean, "-o", str(obj), str(source)], cwd=source_dir, env=env,
                             capture_output=True, text=True, timeout=180)
        elapsed = time.monotonic() - started
        log = output / name.replace(".lean", ".log")
        log.write_text(run.stdout + run.stderr)
        require(run.returncode == 0 and not run.stderr.strip(), run.stdout + run.stderr)
        require(not re.search(r"sorryAx|native_decide|warning:|error:", run.stdout),
                "Unexpected diagnostic or trust axiom: " + name)
        matches = re.findall(
            "'" + re.escape(namespace) + r"\.([A-Za-z_]+)' depends on axioms: \[([^]]*)\]",
            run.stdout)
        require(len(matches) == len(declarations) and {n for n, _ in matches} == declarations,
                "Missing or duplicate axiom report: " + name)
        reports = {}
        for declaration, text in matches:
            axioms = {a.strip() for a in text.split(",") if a.strip()}
            require(axioms <= {"propext", "Classical.choice", "Quot.sound"},
                    "Unexpected axiom: " + declaration)
            reports[namespace + "." + declaration] = sorted(axioms)
        require(obj.is_file(), "Compiler object missing: " + name)
        builds.append({"source": name, "source_sha256": expected_sha,
                       "seconds": elapsed, "exit_code": run.returncode,
                       "log_sha256": sha(log), "object_sha256": sha(obj),
                       "axiom_reports": reports, "stdout": run.stdout, "stderr": run.stderr})
    require(sha(dependency_file) == DEPENDENCY_SHA, "Frozen dependency manifest changed during execution")
    for name, expected, _, _ in MODULES:
        require(sha(source_dir / name) == expected, "Frozen source changed during execution: " + name)
    report = {
        "status": "PASS", "date": "2026-10-10", "lean": version,
        "runner_sha256": sha(Path(__file__)),
        "dependency_manifest_sha256": DEPENDENCY_SHA, "dependencies": checked, "builds": builds,
        "new_substantive_declarations": 7, "existing_recompiled_declarations": 16,
        "freshly_rebuilt_mathlib_modules": upstream_builds,
        "scope": "All-parabolic cardinality, antichain local projection bijectivity, separator factorization and all-parabolic lower-central equality, derived from the retained actual supported-kernel construction.",
        "assumed_kernel_profile": False, "assumed_isolated_word": False,
        "assumed_abelian_kernels": False, "unproved_placeholders": False,
        "native_evaluation_axioms": False,
        "trust_boundary": "All four local sources and two pinned Mathlib sources freshly compiled. Pinned package revisions and tracked cleanliness checked; other compiled package dependency objects and the installed compiler remain trusted. The Mathlib namespace overlay links cached objects read-only and excludes every fresh module stem.",
        "exclusions": ["derived Boolean deletions", "typed Helly transfer",
                       "application-specific hypothesis bindings", "complete U or A formalization",
                       "historical priority", "open-conjecture solution", "compression ratio"]
    }
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "new_declarations": 7, "local_modules_compiled": 4,
                      "mathlib_modules_compiled": 2,
                      "seconds": sum(b["seconds"] for b in builds + upstream_builds), "output": str(output)}, indent=2))


if __name__ == "__main__":
    main()
