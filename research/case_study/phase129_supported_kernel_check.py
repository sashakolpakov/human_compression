#!/usr/bin/env python3
"""Compile actual supported-kernel generation and its exact local dependencies."""
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
    output.mkdir(parents=True, exist_ok=False)
    env["LEAN_PATH"] = os.pathsep.join(map(str, [output] + libraries))
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
        "new_substantive_declarations": 10, "existing_recompiled_declarations": 6,
        "scope": "Actual support induction, full simultaneous fiber-product generation, every actual parabolic kernel profile and full marked IP.",
        "assumed_kernel_profile": False, "assumed_isolated_word": False,
        "assumed_abelian_kernels": False, "unproved_placeholders": False,
        "native_evaluation_axioms": False,
        "trust_boundary": "All three local sources freshly compiled. Pinned package revisions and tracked cleanliness checked; existing compiled package dependency objects and the installed compiler remain trusted.",
        "exclusions": ["finite cardinality formula", "antichain local-isomorphism corollary",
                       "derived Boolean deletions", "lower-central equality", "separator factorization",
                       "application-specific hypothesis bindings", "complete U or A formalization",
                       "historical priority", "open-conjecture solution", "compression ratio"]
    }
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "new_declarations": 10, "local_modules_compiled": 3,
                      "seconds": sum(b["seconds"] for b in builds), "output": str(output)}, indent=2))


if __name__ == "__main__":
    main()
