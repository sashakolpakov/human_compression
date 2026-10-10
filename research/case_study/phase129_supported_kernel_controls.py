#!/usr/bin/env python3
"""Author rejection controls for the pinned supported-kernel compiler wrapper."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

BASE = Path(__file__).resolve().parent
INPUTS = ["LiftCertificate.lean", "CoordinateKernels.lean",
          "SupportedKernelGeneration.lean", "dependency_manifest.json"]


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
    runner = BASE / "phase129_supported_kernel_check.py"
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

    for name in ["SupportedKernelGeneration.lean", "CoordinateKernels.lean", "dependency_manifest.json"]:
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
