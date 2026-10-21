#!/usr/bin/env python3
"""Fresh pinned replay of the unchanged interval core and its Fin n adapter."""
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


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--packages", type=Path, required=True)
    ap.add_argument("--lean", default="lean")
    ap.add_argument("--study-root", type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    output = args.output_dir.absolute()
    require(not os.path.lexists(output), "Fresh output directory required")
    root = args.study_root.resolve()
    expected = {
        "phase149_interval_overlap_check.py": "6ccc02973432a0f0a1679db31ed24df3faf2727579d5a512c97550c72b0a27ab",
        "formal/IntervalOverlapCancellation.lean": "7a1072ffb966606b7d0371b7c123220a0498d00a2299b8c76f5ccb7c2f8f4ae5",
        "formal/dependency_manifest.json": "4c716f4ff0ea4940311014c9853c0b8e5aaab8250f8cefdf9f8003845cfb02e3",
        "formal/FinIntervalOverlapCancellation.lean": "a951b853c7a33512a2d0293bdef7f8c101d4f1dcf55d8a87482d38fbb3851417",
    }
    for name, value in expected.items():
        require(sha(root / name) == value, "Frozen input changed: " + name)
    adapter = root / "formal/FinIntervalOverlapCancellation.lean"
    require(not re.search(r"\b(sorry|admit|axiom|native_decide|unsafe)\b", adapter.read_text()),
            "Unproved declaration or unsafe evaluation")
    lean = shutil.which(args.lean)
    require(lean is not None, "Lean executable not found")
    lean = str(Path(lean).resolve())
    output.mkdir(parents=True, exist_ok=False)
    core = output / "core"
    run_core = subprocess.run([
        sys.executable, "-B", "-O", str(root / "phase149_interval_overlap_check.py"),
        "--packages", str(args.packages.resolve()), "--lean", lean,
        "--source-dir", str(root / "formal"), "--output-dir", str(core)],
        capture_output=True, text=True, timeout=180)
    (output / "core_runner.log").write_text(run_core.stdout + run_core.stderr)
    require(run_core.returncode == 0, run_core.stdout + run_core.stderr)
    core_report = json.loads((core / "report.json").read_text())
    require(core_report["status"] == "PASS", "Core proof failed")
    deps = json.loads((root / "formal/dependency_manifest.json").read_text())
    libraries = [core]
    for item in deps["packages"]:
        library = args.packages.resolve() / item["name"] / ".lake/build/lib/lean"
        if library.is_dir():
            libraries.append(library)
    env = dict(os.environ)
    env["ELAN_TOOLCHAIN"] = deps["lean"]
    env["LEAN_PATH"] = os.pathsep.join(map(str, libraries))
    executed = output / adapter.name
    shutil.copyfile(adapter, executed)
    obj = output / "FinIntervalOverlapCancellation.olean"
    started = time.monotonic()
    run = subprocess.run([lean, "-o", str(obj), executed.name], cwd=output, env=env,
                         capture_output=True, text=True, timeout=180)
    elapsed = time.monotonic() - started
    log = output / "build.log"
    log.write_text(run.stdout + run.stderr)
    require(run.returncode == 0 and not run.stderr.strip(), run.stdout + run.stderr)
    require(not re.search(r"sorryAx|native_decide|warning:|error:", run.stdout),
            "Unexpected diagnostic or trust axiom")
    namespace = "MathCompression.IntervalOverlapCancellation"
    names = {"fin_val_ordConnected", "fin_val_disjoint_iff", "fin_weights_eq_zero"}
    matches = re.findall("'" + re.escape(namespace) +
                         r"\.([A-Za-z_]+)' depends on axioms: \[([^]]*)\]", run.stdout)
    require(len(matches) == 3 and {n for n, _ in matches} == names,
            "Missing or duplicate axiom report")
    axioms = {}
    for name, values in matches:
        entries = {x.strip() for x in values.split(",") if x.strip()}
        require(entries <= {"propext", "Classical.choice", "Quot.sound"}, "Unexpected axiom")
        axioms[namespace + "." + name] = sorted(entries)
    require(obj.is_file() and not obj.is_symlink(), "Fresh compiler object missing")
    for name, value in expected.items():
        require(sha(root / name) == value, "Frozen input changed during replay: " + name)
    require(sha(executed) == expected["formal/FinIntervalOverlapCancellation.lean"],
            "Executed adapter changed")
    result = {"status": "PASS", "date": "2026-10-10", "lean": core_report["lean"],
              "runner_sha256": sha(Path(__file__)), "input_bindings": expected,
              "core_fresh_replay": core_report, "adapter_seconds": elapsed,
              "adapter_axiom_reports": axioms, "exit_code": run.returncode,
              "stdout": run.stdout, "stderr": run.stderr,
              "log_sha256": sha(log), "object_sha256": sha(obj),
              "new_adapter_declarations": 3, "retained_core_declarations_recompiled": 3,
              "scope": "Exact Fin n consumer adapter including convexity and disjointness transport. No group application assumed or proved.",
              "trust_boundary": core_report["trust_boundary"]}
    (output / "report.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "new_declarations": 3,
                      "core_and_adapter_seconds": core_report["seconds"] + elapsed,
                      "output": str(output)}, indent=2))


if __name__ == "__main__":
    main()
