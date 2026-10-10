"""Compile the Lean certificates with pinned dependencies.

Historical *.check.json files are never overwritten. Fresh compilation outputs
and reports go to .verification/ by default. --check-saved checks recorded hashes,
not Lean proofs. --check-env inspects the compiler and dependency revisions only.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
CERTIFICATES = (
    "LiftCertificate", "FieldIntersection", "TransvectionIntersection",
    "ResidueConnectivity", "ChamberOrbit", "TorsorPartitions",
    "CoordinateKernels", "SuzukiPentagons", "StringIntersection",
    "BooleanShadow", "ConsecutiveShadow", "RankThreeFactorization", "CosetCoordinates",
    "IntertwinerSeparation", "TransvectionForms",
    "InvolutionCentralizers", "BinaryFrattiniActions", "MarkedSquareDescent",
    "GradedSupport", "BooleanRetractions", "PrincipalKernelIntersections",
    "NestedKernelIntersections", "Phase23TransferAnnihilator",
    "EndpointDoublingIntersections", "TwoCosetIntersection",
    "Phase29CosetMonodromy",
    "Phase30AffineData",
    "Phase32VoltageTheory", "Phase32L003Infinitude",
    "ParabolicQuotientTransport",
    "OneExceptionalParabolic",
    "SplitLatticeReduction",
    "CompactAffineData",
    "FibonacciModulus",
    "ParabolicProductComparison",
    "ParabolicMarkedComparison",
    "TriangleWreathQuotient",
    "TriangleWreathInvolutory",
    "TriangleReflection",
    "QuotientIntersectionCriterion",
    "CoverCharacterSeparation",
    "OddKernelWord",
    "OddCoverSeparation",
    "CoprimePullback",
)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selection(args, parser):
    if args.all and args.file:
        parser.error("use either a certificate filename or --all")
    names = list(CERTIFICATES) if args.all or (args.check_saved and not args.file) else [
        Path(args.file or "LiftCertificate.lean").stem
    ]
    if any(name not in CERTIFICATES for name in names):
        parser.error("unknown certificate; choose one of: " + ", ".join(CERTIFICATES))
    pending = set(names)
    to_visit = list(names)
    while to_visit:
        name = to_visit.pop()
        for module in re.findall(r"^import (\w+)\s*$", (ROOT / (name + ".lean")).read_text(), re.M):
            if module in CERTIFICATES and module not in pending:
                pending.add(module)
                to_visit.append(module)
    return [name for name in CERTIFICATES if name in pending]


def check_saved(names):
    failed = False
    for name in names:
        source = ROOT / (name + ".lean")
        report = json.loads(source.with_suffix(".check.json").read_text())
        passed = (report.get("sha256") == sha256(source)
                  and report.get("exit_code") == 0
                  and "sorryAx" not in report.get("stdout", ""))
        print(f"{'PASS' if passed else 'FAIL'} saved record: {name}")
        failed |= not passed
    print("Saved-record consistency only: Lean was not executed.")
    return int(failed)


def environment(args):
    manifest = json.loads((ROOT / "dependency_manifest.json").read_text())
    package_value = args.packages or os.environ.get("MATH_COMPRESSION_PACKAGES")
    packages = Path(package_value).expanduser().resolve() if package_value else ROOT / ".lake/packages"
    lean_value = args.lean or os.environ.get("MATH_COMPRESSION_LEAN") or "lean"
    lean = shutil.which(os.path.expanduser(lean_value))
    if lean is None:
        raise RuntimeError("Lean executable not found; install elan or set --lean / MATH_COMPRESSION_LEAN")
    version_run = subprocess.run([lean, "--version"], cwd=ROOT, capture_output=True, text=True, timeout=30)
    if version_run.returncode:
        raise RuntimeError(version_run.stderr.strip() or "Lean --version failed")
    version = version_run.stdout.strip()
    expected_version = manifest["lean"].split(":")[-1].removeprefix("v")
    if not re.search(r"\bversion " + re.escape(expected_version) + r"(?:,|\s|\))", version):
        raise RuntimeError(f"Expected Lean {expected_version}; found {version}")
    if not packages.is_dir():
        raise RuntimeError(f"Dependency directory does not exist: {packages}\nSee formal/README.md for pinned Lake setup.")
    if shutil.which("git") is None:
        raise RuntimeError("git is required to verify the recorded dependency revisions")
    paths, checked = [], []
    for package in manifest["packages"]:
        checkout = packages / package["name"]
        rev = subprocess.run(["git", "-C", str(checkout), "rev-parse", "HEAD"],
                             capture_output=True, text=True)
        if rev.returncode or rev.stdout.strip() != package["rev"]:
            raise RuntimeError(f"Dependency {package['name']} is absent or differs from its pinned revision")
        dirty = subprocess.run(["git", "-C", str(checkout), "diff", "--quiet", "HEAD", "--"],
                               capture_output=True, text=True)
        if dirty.returncode:
            raise RuntimeError(f"Dependency {package['name']} has tracked changes")
        library = checkout / ".lake/build/lib/lean"
        if library.is_dir():
            paths.append(library)
        checked.append({"name": package["name"], "revision": rev.stdout.strip(),
                        "tracked_files_clean": True, "compiled_library_present": library.is_dir()})
    mathlib = packages / "mathlib/.lake/build/lib/lean/Mathlib"
    if not mathlib.is_dir():
        raise RuntimeError("mathlib compiled files are missing; run `lake exe cache get` in formal/")
    output = (args.output_dir or ROOT / ".verification").expanduser().resolve()
    if output == ROOT:
        raise RuntimeError("Choose an output directory other than formal/ to preserve historical reports")
    env = dict(os.environ)
    # Do not inherit an unrelated LEAN_PATH that could shadow pinned modules.
    env["LEAN_PATH"] = os.pathsep.join(map(str, [output, ROOT / ".lake/build/lib/lean", ROOT] + paths))
    return lean, version, checked, output, env


def prepare_mathlib(names, lean, output, env, timeout):
    """Build missing imported mathlib objects in a private overlay only."""
    libraries = [Path(p) for p in env["LEAN_PATH"].split(os.pathsep)]
    build = next(p for p in libraries if p.name == "lean" and
                 p.parent.name == "lib" and p.parent.parent.name == "build" and
                 p.parent.parent.parent.parent.name == "mathlib")
    checkout = build.parent.parent.parent.parent
    output.mkdir(parents=True, exist_ok=True)
    overlay = output / "Mathlib"
    if not overlay.exists():
        overlay.symlink_to(build / "Mathlib", target_is_directory=True)
    records = []

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

    def ensure(module):
        relative = Path(module.replace(".", "/") + ".olean")
        if any((library / relative).exists() for library in libraries):
            return
        source = checkout / (module.replace(".", "/") + ".lean")
        if not source.is_file():
            raise RuntimeError(f"Missing pinned dependency source: {module}")
        for child in re.findall(r"^(?:public )?import ([A-Za-z0-9_.]+)", source.read_text(), re.M):
            ensure(child)
        target = output / relative
        writable_directory(target.parent)
        source_hash = sha256(source)
        run = subprocess.run([lean, "-o", str(target), str(source)], cwd=checkout,
                             env=env, text=True, capture_output=True, timeout=timeout)
        records.append({"module": module, "source_sha256": source_hash,
                        "exit_code": run.returncode, "stdout": run.stdout, "stderr": run.stderr})
        if run.returncode or sha256(source) != source_hash:
            raise RuntimeError(f"Dependency build failed or source changed: {module}\n"
                               + run.stdout + run.stderr)

    for name in names:
        text = (ROOT / (name + ".lean")).read_text()
        for module in re.findall(r"^import (Mathlib\.[A-Za-z0-9_.]+)", text, re.M):
            ensure(module)
    (output / "dependency_builds.json").write_text(json.dumps({
        "scope": "Only missing imported objects built in private overlay; installed checkout unchanged.",
        "modules": records,
    }, indent=2) + "\n")


def compile_one(name, lean, version, checked, output, env, timeout):
    source = ROOT / (name + ".lean")
    output.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    command = [lean, "-o", str(output / (name + ".olean")), source.name]
    run = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, timeout=timeout)
    report = {
        "source": source.name, "sha256": sha256(source), "exit_code": run.returncode,
        "elapsed_seconds": time.monotonic() - started, "stdout": run.stdout,
        "stderr": run.stderr, "lean": version, "dependency_manifest": "dependency_manifest.json",
        "dependency_manifest_sha256": sha256(ROOT / "dependency_manifest.json"),
        "dependencies": checked, "verification": "fresh compiler run",
        "dependency_scope": "Recorded git HEADs and tracked-file cleanliness checked; compiled dependencies are trusted build inputs.",
    }
    (output / (name + ".check.json")).write_text(json.dumps(report, indent=2) + "\n")
    print(run.stdout, end="")
    print(run.stderr, end="", file=sys.stderr)
    print(f"{name}: LEAN_EXIT_CODE {run.returncode}", flush=True)
    return run.returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", help="certificate filename; default LiftCertificate.lean")
    parser.add_argument("--all", action="store_true", help="compile all certificates in dependency order")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check-saved", action="store_true", help="check historical hashes and recorded exits; no compilation")
    modes.add_argument("--check-env", action="store_true", help="check compiler version and dependency revisions; no compilation")
    parser.add_argument("--packages", help="Lake packages directory; overrides MATH_COMPRESSION_PACKAGES")
    parser.add_argument("--lean", help="Lean executable; overrides MATH_COMPRESSION_LEAN and PATH")
    parser.add_argument("--output-dir", type=Path, help="fresh outputs; default formal/.verification")
    parser.add_argument("--timeout", type=float, default=120, help="per-certificate compiler timeout in seconds")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    names = selection(args, parser)
    try:
        if args.check_saved:
            return check_saved(names)
        lean, version, checked, output, env = environment(args)
        if args.check_env:
            print(version)
            for package in checked:
                print(f"PASS pinned dependency: {package['name']} {package['revision']}")
            print("Environment only: no certificate was compiled.")
            return 0
        prepare_mathlib(names, lean, output, env, args.timeout)
        for name in names:
            code = compile_one(name, lean, version, checked, output, env, args.timeout)
            if code:
                return code
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
        print(f"Verification failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
