#!/usr/bin/env python3
"""Author integrity, no-clobber and semantic controls for the finite rewrite certificate."""
import argparse
import hashlib
import json
import os
import re
import time
from pathlib import Path
import shutil
import subprocess
import sys

BASE = Path(__file__).resolve().parent
INPUTS = ["LabelEightCriticalPairs.lean", "LabelEightFiniteCertificate.lean",
          "LabelEightAlphabet.lean", "dependency_manifest.json"]


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--packages", type=Path, required=True)
    ap.add_argument("--lean", required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    out = args.output_dir.absolute()
    require(not out.exists() and not out.is_symlink(), "Fresh control output required")
    out.mkdir(parents=True, exist_ok=False)
    source_dir = BASE / "formal"
    runner = BASE / "phase167_label_eight_check.py"
    before = {n: sha(source_dir / n) for n in INPUTS}
    reports = []

    def reject(case, sources, destination, expected):
        command = [sys.executable, "-B", "-O", str(runner),
                   "--packages", str(args.packages), "--lean", args.lean,
                   "--source-dir", str(sources), "--output-dir", str(destination)]
        run = subprocess.run(command, capture_output=True, text=True, timeout=30)
        require(run.returncode != 0 and expected in run.stderr, "Control failed: " + case)
        reports.append({"case": case, "exit_code": run.returncode, "expected": expected,
                        "stdout": run.stdout, "stderr": run.stderr})

    for name in INPUTS:
        stage = out / ("changed_" + name)
        stage.mkdir()
        for item in INPUTS:
            shutil.copyfile(source_dir / item, stage / item)
        changed = stage / name
        changed.write_bytes(changed.read_bytes() + b"\n")
        destination = out / ("rejected_" + name)
        expected = ("Frozen dependency manifest changed" if name.endswith(".json")
                    else "Frozen source changed: " + name)
        reject("changed_" + name, stage, destination, expected)
        require(not destination.exists() and not destination.is_symlink(),
                "Changed input created output")
    regular = out / "regular"
    regular.write_bytes(b"unchanged regular file\n")
    regular_sha = sha(regular)
    reject("occupied_regular", source_dir, regular, "Fresh output directory required")
    require(sha(regular) == regular_sha, "Regular file changed")
    directory = out / "directory"
    directory.mkdir()
    marker = directory / "marker"
    marker.write_bytes(b"unchanged directory\n")
    marker_sha = sha(marker)
    reject("occupied_directory", source_dir, directory, "Fresh output directory required")
    require(list(directory.iterdir()) == [marker] and sha(marker) == marker_sha,
            "Directory changed")
    live = out / "live_link"
    live.symlink_to(regular)
    reject("live_symlink", source_dir, live, "Fresh output directory required")
    require(live.is_symlink() and live.readlink() == regular and sha(regular) == regular_sha,
            "Live link changed")
    missing = out / "missing_target"
    dangling = out / "dangling_link"
    dangling.symlink_to(missing)
    reject("dangling_symlink", source_dir, dangling, "Fresh output directory required")
    require(dangling.is_symlink() and dangling.readlink() == missing and not missing.exists(),
            "Dangling link changed")
    # These controls deliberately bypass the frozen-source hash guard to test
    # the mathematics. Each mutated core must still compile; the exact true
    # claim is then rejected while the false value is kernel-proved first.
    dependency = json.loads((source_dir / "dependency_manifest.json").read_text())
    libraries = [args.packages.resolve() / item["name"] / ".lake/build/lib/lean"
                 for item in dependency["packages"]]
    original = (source_dir / "LabelEightCriticalPairs.lean").read_text()
    mutations = [
        ("omitted_left_tail", "[y d j, w d j, w d i]", "[y d j, w d j]", (2, 1, 0)),
        ("omitted_edge_commutator", "if i = j + 1 then [w d j, w d i]",
         "if i = j + 1 then []", (2, 1, 0)),
        ("omitted_triple_commutator", "if j = i + 1 then [w d i, w d (i + 1)]",
         "if j = i + 1 then []", (15, 1, 0)),
        ("collapsed_edge_square", "then [w d (decode d a).2] else []",
         "then [] else []", (1, 0, 0)),
    ]
    for case, old, new, triple in mutations:
        require(original.count(old) == 1, "Ambiguous mutation: " + case)
        stage = out / case
        stage.mkdir()
        core = stage / "LabelEightCriticalPairs.lean"
        core.write_text(original.replace(old, new))
        env = dict(os.environ)
        env["ELAN_TOOLCHAIN"] = dependency["lean"]
        env["LEAN_PATH"] = os.pathsep.join(map(str, [stage] + libraries))
        start = time.monotonic()
        compiled = subprocess.run([args.lean, "-o", str(stage / "LabelEightCriticalPairs.olean"),
                                   str(core)], cwd=stage, env=env, capture_output=True,
                                  text=True, timeout=120)
        (stage / "core.log").write_text(compiled.stdout + compiled.stderr)
        require(compiled.returncode == 0 and not compiled.stderr.strip()
                and not re.search(r"sorryAx|warning:|error:", compiled.stdout),
                "Mutated core failed before the mathematical control: " + case)
        a, b, c = triple
        expression = f"criticalCheck 14 32 {a} {b} {c}"
        test = stage / "FalseJoinability.lean"
        test.write_text("import LabelEightCriticalPairs\n"
                        "open MathCompression.LabelEightCriticalPairs\n"
                        f"example : {expression} = false := by decide\n"
                        f"example : {expression} = true := by decide\n")
        rejected = subprocess.run([args.lean, str(test)], cwd=stage, env=env,
                                  capture_output=True, text=True, timeout=120)
        (stage / "rejection.log").write_text(rejected.stdout + rejected.stderr)
        require(rejected.returncode != 0 and not rejected.stderr.strip()
                and rejected.stdout.count("error:") == 1
                and "FalseJoinability.lean:4:" in rejected.stdout
                and "decide" in rejected.stdout,
                "Semantic mutation was not rejected at the exact false claim: " + case)
        reports.append({"case": case, "mutated_source_sha256": sha(core),
                        "critical_triple": list(triple), "false_value_kernel_proved": True,
                        "true_value_kernel_rejected": True,
                        "seconds": time.monotonic() - start,
                        "core_log_sha256": sha(stage / "core.log"),
                        "rejection_log_sha256": sha(stage / "rejection.log"),
                        "diagnostic": rejected.stdout})
    require(before == {n: sha(source_dir / n) for n in INPUTS}, "Original input changed")
    result = {"status": "PASS", "controls": reports, "control_count": len(reports),
              "input_hashes": before, "runner_sha256": sha(runner),
              "control_program_sha256": sha(Path(__file__)),
              "author_controls_not_independent_review": True,
              "formal_proof_supplied_by_compiler_run_not_these_controls": True}
    (out / "report.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "controls": len(reports), "output": str(out)}, indent=2))


if __name__ == "__main__":
    main()
