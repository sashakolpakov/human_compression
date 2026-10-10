#!/usr/bin/env python3
"""Independent finite scope examples and exact wrapper rejection controls."""
from __future__ import annotations
import argparse
from itertools import permutations, product
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

BASE = Path(__file__).resolve().parent
RUNNER = BASE / "phase115_coprime_pullback_check.py"
SOURCE = BASE / "formal/CoprimePullback.lean"
DEPENDENCIES = BASE / "formal/dependency_manifest.json"


def require(ok, msg):
    if not ok:
        raise RuntimeError(msg)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def close(generators, one, mul):
    found = {one}
    stack = [one]
    while stack:
        x = stack.pop()
        for g in generators:
            y = mul(x, g)
            if y not in found:
                found.add(y)
                stack.append(y)
    return found


def finite_checks():
    S3 = set(permutations(range(3)))
    one = (0, 1, 2)
    transposition = (1, 0, 2)
    cycle = (1, 2, 0)
    def pmul(a, b):
        return tuple(a[b[i]] for i in range(3))
    def sign(a):
        return sum(a[i] > a[j] for i in range(3) for j in range(i + 1, 3)) % 2
    require(close([transposition, cycle], one, pmul) == S3, "S3 generators")
    # Nonabelian kernel: S3 x C5 over the trivial group.
    mul5 = lambda x, y: (pmul(x[0], y[0]), (x[1] + y[1]) % 5)
    h = close([(transposition, 1), (cycle, 1)], (one, 0), mul5)
    require(h == set(product(S3, range(5))), "Nonabelian full kernel product")
    # Nontrivial base: sign:S3->C2 and reduction:C4->C2.
    mul4 = lambda x, y: (pmul(x[0], y[0]), (x[1] + y[1]) % 4)
    fiber = {(a, b) for a, b in product(S3, range(4)) if sign(a) == b % 2}
    h2 = close([(transposition, 1), (cycle, 0)], (one, 0), mul4)
    require(h2 == fiber and len(fiber) == 12, "Nontrivial-base pullback")
    require({x[0] for x in h2} == S3 and {x[1] for x in h2} == set(range(4)),
            "Both projections in nontrivial-base example")
    # Failure without coprimality: diagonal C2 in C2 x C2.
    add2 = lambda x, y: ((x[0] + y[0]) % 2, (x[1] + y[1]) % 2)
    diagonal = close([(1, 1)], (0, 0), add2)
    full2 = set(product(range(2), repeat=2))
    require(len(diagonal) == 2 and diagonal < full2, "Coprimality counterexample")
    require({x[0] for x in diagonal} == {0, 1} == {x[1] for x in diagonal},
            "Counterexample really has both projections")
    # Failure if second projection omitted, despite coprime kernels 2 and 3.
    add23 = lambda x, y: ((x[0] + y[0]) % 2, (x[1] + y[1]) % 3)
    one_projection = close([(1, 0)], (0, 0), add23)
    require(len(one_projection) == 2 and one_projection < set(product(range(2), range(3))),
            "Surjectivity counterexample")
    # Failure of compatibility inclusion: identity maps of C2 have trivial kernels,
    # but the full product is not the diagonal fiber product.
    require(len(full2) == 4 and full2 != diagonal and (1, 0) not in diagonal,
            "Compatibility counterexample")
    return {
        "status": "PASS",
        "positive_cases": [
            {"case": "nonabelian kernel over trivial base", "kernels": [6, 5],
             "paired_closure_order": len(h), "fiber_product_order": 30},
            {"case": "S3 sign and C4 parity over C2", "kernels": [3, 2],
             "paired_closure_order": len(h2), "fiber_product_order": len(fiber)}
        ],
        "counterexamples": [
            {"omitted_hypothesis": "coprime kernels", "subgroup_order": 2, "fiber_order": 4},
            {"omitted_hypothesis": "second projection surjective", "subgroup_order": 2, "fiber_order": 6},
            {"omitted_hypothesis": "compatibility inclusion", "subgroup_order": 4, "fiber_order": 2}
        ],
        "scope": "Independent finite examples and weakened-hypothesis counterexamples, not proof of the general theorem."
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--packages", type=Path, required=True)
    ap.add_argument("--lean", required=True)
    args = ap.parse_args()
    out = args.output_dir.absolute()
    require(not out.exists() and not out.is_symlink(), "Review output must be fresh")
    out.mkdir(parents=True, exist_ok=False)
    before = {str(p): digest(p.read_bytes()) for p in (RUNNER, SOURCE, DEPENDENCIES)}
    controls = []
    def command(source_dir, output_dir):
        return [sys.executable, "-B", "-O", str(RUNNER),
                "--packages", str(args.packages), "--lean", args.lean,
                "--source-dir", str(source_dir), "--output-dir", str(output_dir)]
    def run_control(label, source_dir, destination, message):
        run = subprocess.run(command(source_dir, destination), capture_output=True,
                             text=True, timeout=30)
        require(run.returncode != 0 and message in run.stderr, "Rejection failed: " + label)
        controls.append({"case": label, "exit_code": run.returncode,
                         "expected_rejection": message, "stdout": run.stdout,
                         "stderr": run.stderr})
    for kind, expected in [
        ("source", "Frozen source changed"), ("manifest", "Frozen dependency manifest changed")]:
        stage = out / ("wrong_" + kind)
        stage.mkdir()
        shutil.copyfile(SOURCE, stage / SOURCE.name)
        shutil.copyfile(DEPENDENCIES, stage / DEPENDENCIES.name)
        target = stage / (SOURCE.name if kind == "source" else DEPENDENCIES.name)
        target.write_bytes(target.read_bytes() + b"\n")
        destination = out / (kind + "_must_not_exist")
        run_control("changed_" + kind, stage, destination, expected)
        require(not destination.exists() and not destination.is_symlink(),
                "Bad input created output: " + kind)
    regular = out / "occupied_file"
    regular.write_bytes(b"independent sentinel\n")
    regular_hash = digest(regular.read_bytes())
    run_control("occupied_regular_file", SOURCE.parent, regular, "Fresh output directory required")
    require(digest(regular.read_bytes()) == regular_hash, "Regular output clobbered")
    directory = out / "occupied_directory"
    directory.mkdir()
    sentinel = directory / "sentinel"
    sentinel.write_bytes(b"directory sentinel\n")
    dir_hash = digest(sentinel.read_bytes())
    run_control("occupied_directory", SOURCE.parent, directory, "Fresh output directory required")
    require(list(directory.iterdir()) == [sentinel] and digest(sentinel.read_bytes()) == dir_hash,
            "Directory output clobbered")
    live = out / "live_symlink"
    live.symlink_to(regular)
    run_control("live_symlink", SOURCE.parent, live, "Fresh output directory required")
    require(live.is_symlink() and live.readlink() == regular and digest(regular.read_bytes()) == regular_hash,
            "Live link clobbered")
    absent = out / "dangling_target"
    dangling = out / "dangling_symlink"
    dangling.symlink_to(absent)
    run_control("dangling_symlink", SOURCE.parent, dangling, "Fresh output directory required")
    require(dangling.is_symlink() and dangling.readlink() == absent and not absent.exists(),
            "Dangling output clobbered")
    require(before == {str(p): digest(p.read_bytes()) for p in (RUNNER, SOURCE, DEPENDENCIES)},
            "Frozen original changed during independent controls")
    report = {"status": "PASS", "controls": controls, "control_count": len(controls),
              "finite_math_checks": finite_checks(), "original_input_hashes": before,
              "review_check_sha256": digest(Path(__file__).read_bytes()),
              "original_sources_modified": False, "public_tree_modified": False}
    (out / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "rejection_controls": len(controls),
                      "positive_math_cases": 2, "weakened_hypothesis_counterexamples": 3,
                      "output": str(out)}, indent=2))


if __name__ == "__main__":
    main()
