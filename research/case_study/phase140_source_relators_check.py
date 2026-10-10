#!/usr/bin/env python3
"""Compile the actual ambient characteristic-two relator and exact label-four relation adapter."""
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
MODULES = [('LabelFourRelations.lean',
  '6cda4bb1f0bf2f6efb6e7935db0487961ade5bdd6d5d210a8e84aa63f556e5ab',
  'MathCompression.LabelFourRelations',
  {'adjacent_relations_iff',
   'commutator_eq_square',
   'commutator_iff_reversed_square',
   'cross_relation_iff',
   'first_power_relation',
   'label_four_relations_iff',
   'nested_commutators',
   'third_power_relation'}),
 ('CharacteristicTwoTranslations.lean',
  '430dc7d20ba40b5f0013b129551d136cf9d97088b91b5ddf0bb5652f510ac1cd',
  'MathCompression.CharacteristicTwoTranslations',
  {'equal_label_integer_relation',
   'integer_power_product_mem',
   'integer_power_product_square',
   'polar_preserves',
   'polar_self_zero',
   'quadratic_add',
   'singular_shift',
   'symmetry_involutive',
   'symmetry_pair',
   'symmetry_pair_equiv',
   'symmetry_preserves',
   'translationGroup_conjugate',
   'translationGroup_square',
   'translation_comp',
   'translation_conjugate',
   'translation_covariant',
   'translation_involutive',
   'translation_zero',
   'triple_singular_radical',
   'vector_add_self'})]
MATHLIB_REBUILDS = [('Mathlib.LinearAlgebra.SesquilinearForm.Orthogonal',
  '14d601ff946633833c52d03bef9b03dfd25a2fab9bd756b286d079918c94e9ca'),
 ('Mathlib.LinearAlgebra.QuadraticForm.Basic',
  'fe115743a63c263748739b83fd0b68f5aa20e363a0a913636645e4179ef520d5')]


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
    ancestors = {"Mathlib", "Mathlib/LinearAlgebra",
                 "Mathlib/LinearAlgebra/SesquilinearForm", "Mathlib/LinearAlgebra/QuadraticForm"}
    stems = {name.replace(".", "/") for name, _ in MATHLIB_REBUILDS}

    def overlay(relative):
        directory = output / relative
        directory.mkdir(parents=True, exist_ok=False)
        if not (cached / relative).is_dir():
            return
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
        obj.parent.mkdir(parents=True, exist_ok=True)
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
        "new_substantive_declarations": 28, "existing_recompiled_declarations": 0,
        "freshly_rebuilt_mathlib_modules": upstream_builds,
        "scope": "Actual quadratic-form translations, ambient symmetry-pair and conjugation identities, all-integer relator from the three-vector hypotheses, and exact bidirectional local label-four relation adapter.",
        "ambient_action_proved": True, "all_integer_powers_proved": True,
        "translation_group_and_normalization_derived": True,
        "target_relator_assumed": False, "nondegenerate_form_assumed": False,
        "unproved_placeholders": False, "native_evaluation_axioms": False,
        "trust_boundary": "Both local sources and two pinned Mathlib sources freshly compiled. Pinned package revisions and tracked cleanliness checked; other compiled package dependency objects and the installed compiler remain trusted. The Mathlib namespace overlay reuses cached objects through links and excludes every fresh module stem before any compiler output is written.",
        "exclusions": ["finite-field parameter selection", "BFL intersection and group identification results",
                       "Biss--Dasgupta unitriangular presentation theorem", "formal presented-group isomorphism",
                       "full F014 theorem", "all-label universal-group conjecture", "full U or application formalization",
                       "historical priority", "compression ratio"]
    }
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "new_declarations": 28, "local_modules_compiled": 2,
                      "mathlib_modules_compiled": 2,
                      "seconds": sum(b["seconds"] for b in builds + upstream_builds), "output": str(output)}, indent=2))


if __name__ == "__main__":
    main()
