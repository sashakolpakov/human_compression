#!/usr/bin/env python3
"""Compile the all-parameter real-reflection infinitude Lean certificate against the pinned dependency checkout.

The installed checkout is read only. Missing compiled mathlib dependencies are
built in a fresh private overlay; existing dependency objects are symlinked.
The output directory must not exist. No source download or package mutation.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--packages", type=Path, required=True)
    ap.add_argument("--lean", default="lean")
    ap.add_argument("--source-dir", type=Path, default=Path(__file__).resolve().parent / "formal")
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    lean = shutil.which(args.lean)
    if lean is None:
        raise SystemExit("Lean executable not found")
    packages = args.packages.resolve()
    source_dir = args.source_dir.resolve()
    dependency_manifest = source_dir / "dependency_manifest.json"
    manifest = json.loads(dependency_manifest.read_text())
    version = subprocess.check_output([lean, "--version"], text=True).strip()
    expected_version = manifest["lean"].split(":")[-1].removeprefix("v")
    if not re.search(r"\bversion " + re.escape(expected_version) + r"(?:,|\s|\))", version):
        raise SystemExit(f"Expected the pinned Lean {expected_version}")
    package_paths, checked = [], []
    for package in manifest["packages"]:
        checkout = packages / package["name"]
        rev = subprocess.run(["git", "-C", str(checkout), "rev-parse", "HEAD"],
                             capture_output=True, text=True)
        if rev.returncode or rev.stdout.strip() != package["rev"]:
            raise RuntimeError(f"Dependency {package['name']} differs from the pinned revision")
        dirty = subprocess.run(["git", "-C", str(checkout), "diff", "--quiet", "HEAD", "--"],
                               capture_output=True, text=True)
        if dirty.returncode:
            raise RuntimeError(f"Dependency {package['name']} has tracked changes")
        library = checkout / ".lake/build/lib/lean"
        if library.is_dir():
            package_paths.append(library)
        checked.append({"name": package["name"], "revision": rev.stdout.strip(),
                        "tracked_files_clean": True, "compiled_library_present": library.is_dir()})
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=False)
    mathlib = packages / "mathlib"
    build = mathlib / ".lake/build/lib/lean"
    if not (build / "Mathlib").is_dir():
        raise SystemExit("Expected a built mathlib checkout under --packages/mathlib")
    (output / "Mathlib").symlink_to(build / "Mathlib", target_is_directory=True)
    env = dict(os.environ)
    env["LEAN_PATH"] = os.pathsep.join(map(str, [output] + package_paths))
    dependency_records = []

    def writable_directory(path):
        if path == output:
            return
        writable_directory(path.parent)
        if path.is_symlink():
            original = path.resolve()
            path.unlink()
            path.mkdir()
            for child in original.iterdir():
                (path / child.name).symlink_to(child, target_is_directory=child.is_dir())
        elif not path.exists():
            path.mkdir()

    def build_missing(module):
        relative = Path(module.replace(".", "/") + ".olean")
        if (output / relative).exists() or any((p / relative).exists() for p in package_paths):
            return
        source = mathlib / (module.replace(".", "/") + ".lean")
        if not source.is_file():
            raise RuntimeError(f"Missing source for dependency {module}")
        for child in re.findall(r"^(?:public )?import ([A-Za-z0-9_.]+)", source.read_text(), re.M):
            build_missing(child)
        target = output / relative
        writable_directory(target.parent)
        proc = subprocess.run([lean, "-o", str(target), str(source)], cwd=mathlib,
                              env=env, text=True, capture_output=True, timeout=120)
        dependency_records.append({"module": module, "source_sha256": sha(source),
                                   "exit_code": proc.returncode,
                                   "stdout": proc.stdout, "stderr": proc.stderr})
        if proc.returncode:
            raise RuntimeError(proc.stdout + proc.stderr)

    build_missing("Mathlib.GroupTheory.PresentedGroup")
    build_missing("Mathlib.GroupTheory.SemidirectProduct")
    build_missing("Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic")
    records = []
    for name in ("TriangleWreathQuotient", "TriangleWreathInvolutory", "TriangleReflection"):
        source = source_dir / (name + ".lean")
        source_hash = sha(source)
        if name == "TriangleWreathQuotient" and source_hash != "9ff4d19715bd716ce46c1bd284b3070fa44e485e17e0115229f3a971e3f93055":
            raise RuntimeError("The frozen rotational dependency differs from its binding")
        if name == "TriangleWreathInvolutory" and source_hash != "bb1821dab93c385a418c0bf3fd84a2e106766e38f2262e28949e2a9be9baca98":
            raise RuntimeError("The frozen involutory dependency differs from its binding")
        started = time.monotonic()
        proc = subprocess.run([lean, "-o", str(output / (name + ".olean")), str(source)],
                              cwd=source_dir, env=env, text=True, capture_output=True, timeout=300)
        record = {"source": source.name, "sha256": source_hash, "exit_code": proc.returncode,
                  "elapsed_seconds": time.monotonic() - started,
                  "stdout": proc.stdout, "stderr": proc.stderr}
        records.append(record)
        print(name, proc.returncode, flush=True)
        print(proc.stdout, end="", flush=True)
        if proc.returncode or "sorryAx" in proc.stdout or "native_decide.ax" in proc.stdout:
            raise RuntimeError(proc.stdout + proc.stderr)
        if sha(source) != source_hash:
            raise RuntimeError("The Lean source changed during compilation")
        expected = {
            "TriangleWreathQuotient": {"ten_relators", "sourceMap", "coordinateMap_surjective", "source_infinite_of_triangle"},
            "TriangleWreathInvolutory": {"universalRows_valid", "universalMap", "universalCoordinate_surjective", "universal_infinite_of_triangle"},
            "TriangleReflection": {"parameter_relation", "triangle_infinite", "rotational_source_infinite", "universal_source_infinite"},
        }[name]
        checks = re.findall(r"'MathCompression\.(?:TriangleWreath|TriangleReflection)\.([A-Za-z_]+)' depends on axioms: \[([^]]*)\]", proc.stdout)
        if {name for name, _ in checks} != expected:
            raise RuntimeError("Expected central axiom reports were not all printed")
        for theorem, axioms in checks:
            found = {x.strip() for x in axioms.split(",")}
            if found - {"propext", "Classical.choice", "Quot.sound"}:
                raise RuntimeError(f"Unexpected axiom dependency of {theorem}: {found}")
        record["checked_axiom_declarations"] = sorted(expected)
    report = {"status": "PASS", "lean": version, "runner_sha256": sha(Path(__file__)),
              "modules": records, "locally_compiled_dependencies": dependency_records,
              "dependency_manifest_sha256": sha(dependency_manifest),
              "dependencies": checked,
              "dependency_scope": "Pinned git HEADs and tracked-file cleanliness checked; only manifest-listed package libraries used. Existing compiled dependency objects remain trusted build inputs.",
              "scope": "Kernel-checked infinitude of the exact Triangle s, Source s, and Universal s for every natural s>=6. The real reflection representation, finite-order parameter relation, and all-parameter orbit growth are proved; there is no triangle-infinitude hypothesis.",
              "axioms": ["propext", "Classical.choice", "Quot.sound"],
              "native_evaluation_axioms": False, "unproved_placeholders": False}
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
