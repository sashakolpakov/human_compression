#!/usr/bin/env python3
"""Negative controls for the triangular termination proof and isolated runner."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess


PRELUDE = """import TriangularWordTermination
open MathCompression.TriangularWordTermination
instance orderDecidable (k n : Nat) : DecidableRel (BlockOrder k n) := by
  induction n generalizing k with
  | zero => intro u v; exact isFalse (fun h => h)
  | succ n ih =>
    haveI := ih (k + 1)
    intro u v
    change Decidable (List.Shortlex (BlockOrder (k + 1) n) (blocks k u) (blocks k v))
    exact decidable_of_iff _ List.shortlex_def.symm
"""
COUNTEREXAMPLES = {
    "lower_tail_in_swap": "BlockOrder 0 2 [0, 1, 0] [1, 0]",
    "square_tail_repeats_input": "BlockOrder 0 2 [0, 0, 0] [0, 0]",
    "swap_direction_reversed": "BlockOrder 0 2 [1, 0] [0, 1]",
    "input_outside_active_interval": "BlockOrder 0 1 [] [1, 1]",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--build-dir", type=Path, required=True)
    ap.add_argument("--packages", type=Path, required=True)
    ap.add_argument("--lean", default="lean")
    ap.add_argument("--source-dir", type=Path, default=Path(__file__).resolve().parent / "formal")
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    root = Path(__file__).resolve().parent
    runner = root / "phase172_termination_check.py"
    spec = importlib.util.spec_from_file_location("phase172_runner", runner)
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    source = args.source_dir.resolve()
    report_path = args.build_dir.resolve() / "report.json"
    report = json.loads(report_path.read_text())
    require(report["status"] == "PASS" and report["runner_sha256"] == sha(runner), "Unbound build report")
    for name, expected, _, _ in checker.MODULES:
        require(sha(source / (name + ".lean")) == expected, "Changed source: " + name)
        built = next(b for b in report["builds"] if b["source"] == name + ".lean")
        require(built["source_sha256"] == expected and
                sha(args.build_dir / (name + ".olean")) == built["object_sha256"],
                "Changed build artifact: " + name)
    out = args.output_dir.absolute()
    require(not out.exists() and not out.is_symlink(), "Fresh output directory required")
    out.mkdir(parents=True)
    dependencies = json.loads((source / "dependency_manifest.json").read_text())
    env = dict(os.environ)
    env["ELAN_TOOLCHAIN"] = dependencies["lean"]
    libraries = [args.packages.resolve() / p["name"] / ".lake/build/lib/lean" for p in dependencies["packages"]]
    env["LEAN_PATH"] = os.pathsep.join(map(str, [args.build_dir.resolve()] + [p for p in libraries if p.is_dir()]))
    lean = shutil.which(args.lean)
    require(lean is not None, "Lean executable missing")
    results = []

    def compile_case(name, text, should_pass, marker=None):
        path = out / (name + ".lean")
        path.write_text(text)
        run = subprocess.run([lean, str(path)], cwd=source, env=env, capture_output=True, text=True, timeout=120)
        log = out / (name + ".log")
        log.write_text(run.stdout + run.stderr)
        if should_pass:
            require(run.returncode == 0 and not re.search(r"error:|warning:|sorryAx|native_decide", log.read_text()),
                    "Counterexample witness failed: " + name)
        else:
            require(run.returncode != 0 and "error" in run.stdout, "Invalid proof unexpectedly accepted: " + name)
            if marker:
                require(marker in run.stdout, "Expected semantic rejection missing: " + name)
        results.append({"name": name, "status": "PASS", "expected_compile_success": should_pass,
                        "exit_code": run.returncode, "source_sha256": sha(path), "log_sha256": sha(log)})

    positive = PRELUDE + "\n" + "\n".join(
        f"theorem {name} : ¬ {statement} := by decide\n#print axioms {name}"
        for name, statement in COUNTEREXAMPLES.items()) + "\n"
    compile_case("counterexample_witnesses", positive, True)
    for name, statement in COUNTEREXAMPLES.items():
        compile_case(name, PRELUDE + f"\nexample : {statement} := by decide\n", False, "decide")

    generic = (source / "TriangularWordTermination.lean").read_text()
    mutations = {
        "empty_relation_replaced_by_true": ("| 0 => fun _ _ => False", "| 0 => fun _ _ => True"),
        "shortlex_replaced_by_lex": ("InvImage (List.Shortlex (BlockOrder (k + 1) n))", "InvImage (List.Lex (BlockOrder (k + 1) n))"),
        "discard_higher_blocks": ("else (blocks k u).modifyHead (a :: ·)", "else blocks k u"),
    }
    for name, (old, new) in mutations.items():
        require(generic.count(old) == 1, "Ambiguous mutation: " + name)
        compile_case(name, generic.replace(old, new), False)

    base_cmd = ["python3", str(runner), "--packages", str(args.packages.resolve()), "--lean", lean]

    def runner_reject(name, src, dest, expected):
        run = subprocess.run(base_cmd + ["--source-dir", str(src), "--output-dir", str(dest)],
                             capture_output=True, text=True, timeout=30)
        log = out / (name + ".log")
        log.write_text(run.stdout + run.stderr)
        require(run.returncode != 0 and expected in log.read_text(), "Missing runner rejection: " + name)
        results.append({"name": name, "status": "PASS", "exit_code": run.returncode,
                        "expected_rejection": expected, "log_sha256": sha(log)})

    for name, _, _, _ in checker.MODULES:
        folder = out / ("changed_" + name)
        folder.mkdir()
        for module, _, _, _ in checker.MODULES:
            shutil.copy2(source / (module + ".lean"), folder / (module + ".lean"))
        shutil.copy2(source / "dependency_manifest.json", folder / "dependency_manifest.json")
        path = folder / (name + ".lean")
        path.write_text(path.read_text() + "\n")
        runner_reject("hash_" + name, folder, folder / "build", "Frozen source changed: " + name)
        require(not (folder / "build").exists(), "Rejected hash check created output")
    for kind in ["file", "directory"]:
        dest = out / ("occupied_" + kind)
        if kind == "file":
            dest.write_text("sentinel\n")
        else:
            dest.mkdir()
            (dest / "sentinel").write_text("sentinel\n")
        runner_reject("occupied_" + kind, source, dest, "Fresh output directory required")
        sentinel = dest if kind == "file" else dest / "sentinel"
        require(sentinel.read_text() == "sentinel\n", "Occupied output was modified")

    final = {"status": "PASS", "date": "2026-10-10", "runner_sha256": sha(Path(__file__)),
             "positive_counterexample_witnesses": 4, "rejected_false_decreases": 4,
             "rejected_proof_mutations": 3, "rejected_changed_inputs": 4,
             "rejected_occupied_outputs": 2, "total_cases": len(results), "cases": results,
             "bound_positive_build_report_sha256": sha(report_path),
             "scope": "Four concrete invalid order-decrease claims are refuted by kernel proofs and their positive claims are rejected; three altered order definitions invalidate the generic proof; frozen-source and fresh-output checks reject the designated changes.",
             "limit": "Failure of these sufficient triangular hypotheses does not prove nontermination of another rewrite system. Proof-mutation rejections are structural checks, not separate mathematical counterexamples."}
    (out / "report.json").write_text(json.dumps(final, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "total_cases": len(results), "output": str(out)}, indent=2))


if __name__ == "__main__":
    main()
