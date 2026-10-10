#!/usr/bin/env python3
"""Compile the marked-cover character separation using pinned dependencies.

The dependency checkout is read only. The output directory must be new.
Existing compiled dependency objects remain trusted build inputs.
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


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--packages", type=Path, required=True)
    ap.add_argument("--lean", default="lean")
    ap.add_argument("--source-dir", type=Path, default=Path(__file__).resolve().parent / "formal")
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    source_dir = args.source_dir.resolve()
    dependency_file = source_dir / "dependency_manifest.json"
    dependencies = json.loads(dependency_file.read_text())
    lean = shutil.which(args.lean)
    if lean is None:
        raise RuntimeError("Lean executable not found")
    env = dict(os.environ)
    env["ELAN_TOOLCHAIN"] = dependencies["lean"]
    version = subprocess.check_output([lean, "--version"], env=env, text=True).strip()
    expected = dependencies["lean"].split(":")[-1].removeprefix("v")
    if not re.search(r"\bversion " + re.escape(expected) + r"(?:,|\s|\))", version):
        raise RuntimeError("Unexpected Lean version: " + version)
    checked, libraries = [], []
    packages = args.packages.resolve()
    for item in dependencies["packages"]:
        checkout = packages / item["name"]
        rev = subprocess.check_output(["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True).strip()
        if rev != item["rev"]:
            raise RuntimeError("Wrong dependency revision: " + item["name"])
        if subprocess.run(["git", "-C", str(checkout), "diff", "--quiet", "HEAD", "--"]).returncode:
            raise RuntimeError("Tracked dependency changes: " + item["name"])
        library = checkout / ".lake/build/lib/lean"
        if library.is_dir():
            libraries.append(library)
        checked.append({"name": item["name"], "revision": rev,
                        "tracked_files_clean": True, "compiled_library_present": library.is_dir()})
    env["LEAN_PATH"] = os.pathsep.join(map(str, libraries))
    source = source_dir / "CoverCharacterSeparation.lean"
    source_hash = sha(source)
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    result = subprocess.run([lean, "-o", str(output / "CoverCharacterSeparation.olean"), str(source)],
                            cwd=source_dir, env=env, capture_output=True, text=True, timeout=120)
    elapsed = time.monotonic() - started
    (output / "build.log").write_text(result.stdout + result.stderr)
    if result.returncode or result.stderr.strip() or re.search(r"sorryAx|native_decide|warning:|error:", result.stdout):
        raise RuntimeError(result.stdout + result.stderr)
    declarations = {"no_marked_cover_iso", "ne_inv_of_odd_prime_order",
                    "no_marked_cover_iso_of_odd_prime_order"}
    reports = re.findall(r"'MathCompression\.CoverCharacterSeparation\.([A-Za-z_]+)' depends on axioms: \[([^]]*)\]", result.stdout)
    if {name for name, _ in reports} != declarations or len(reports) != len(declarations):
        raise RuntimeError("Missing or duplicate axiom reports")
    axiom_reports = {}
    for name, text in reports:
        axioms = {x.strip() for x in text.split(",") if x.strip()}
        if axioms - {"propext", "Classical.choice", "Quot.sound"}:
            raise RuntimeError("Unexpected axioms: " + repr(axioms))
        axiom_reports[name] = sorted(axioms)
    if sha(source) != source_hash:
        raise RuntimeError("Source changed during compilation")
    report = {"status": "PASS", "date": "2026-10-10", "lean": version,
              "source": source.name, "source_sha256": source_hash,
              "runner_sha256": sha(Path(__file__)), "seconds": elapsed,
              "dependency_manifest_sha256": sha(dependency_file),
              "dependencies": checked, "axiom_reports": axiom_reports,
              "build_log_sha256": sha(output / "build.log"),
              "trust_boundary": "Pinned git revisions and tracked-file cleanliness checked; only pinned package libraries used. Existing compiled dependency objects remain trusted build inputs.",
              "scope": "Different inversion/fixed actions on a kernel obstruct a marked isomorphism over a common base; includes the odd-prime-order specialization.",
              "exclusions": ["existence and order of the family kernels", "verification of the family action tables", "polytope recognition and minimality", "historical priority", "general cover conjecture"],
              "unproved_placeholders": False, "native_evaluation_axioms": False}
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
