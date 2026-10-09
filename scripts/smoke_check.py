#!/usr/bin/env python3
"""Run selected mathematical certificates without rewriting snapshot reports.

The default --quick suite uses only the Python standard library.  --full
also checks the modular cocycle systems (NumPy required) and three exact
graph constructions. --older checks the 2003/2004 reductions using only
the standard library. Each checker runs in its own temporary directory.
This is a focused reproducibility check, not a verification of every proof.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]
CASE_STUDY = ROOT / "research" / "case_study"


@dataclass(frozen=True)
class Check:
    name: str
    script: str
    report: str
    inputs: tuple[str, ...] = ()
    dependency: str | None = None


QUICK = (
    Check("torsor matrices", "torsor_matrix_check.py", "torsor_matrix_check.json"),
    Check("Suzuki polynomial identities", "suzuki_cycle_check.py", "suzuki_cycle_check.json"),
    Check("eleven finite-field witnesses", "verify_square_witnesses.py",
          "psl2_square_witnesses_independent.json", ("psl2_square_witnesses.json",)),
)
FULL = QUICK + (
    Check("marked cocycle linear systems", "phase3_cocycle_linear_check.py",
          "phase3_cocycle_linear_check.json", dependency="numpy"),
    Check("exact generalized-quadrangle graph counts", "phase3_gq_cycle_check.py",
          "phase3_gq_cycle_check.json"),
)
OLDER = (
    Check("semilinear spread descent", "phase4_spread_descent_check.py",
          "phase4_spread_descent_check.json"),
    Check("geometric shadow intersection", "phase4_shadow_ip_check.py",
          "phase4_shadow_ip_check.json"),
)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def validate_report(check: Check, report: object) -> str:
    """Check the reported scope as well as the child process's exit status."""
    if check.script == "phase3_gq_cycle_check.py":
        if not isinstance(report, list) or [row.get("q") for row in report] != [3, 5, 7]:
            raise ValueError("graph report does not cover q=3,5,7")
        for row in report:
            q = row["q"]
            expected = (q - 1) ** 2 * ((q - 2) ** 2 + 1)
            for name in ("symplectic_chamber_deletion", "wenger", "moment_wenger"):
                graph = row[name]
                if (graph["vertices"], graph["degree"], graph["girth"]) != (2*q**3, q, 8):
                    raise ValueError("incorrect graph parameters")
                counts = graph["sample_edge_cycle_counts"]
                if len(counts) != 4 or any(count != expected for count in counts):
                    raise ValueError("incorrect sampled cycle counts")
                if graph["independent_disjoint_path_count"] != expected:
                    raise ValueError("independent path count disagrees")
            if row.get("recursive_to_moment_isomorphism_checked_on_every_edge") is not True:
                raise ValueError("coordinate isomorphism was not verified")
        return "q=3,5,7; three constructions; independent cycle counts"

    if not isinstance(report, dict):
        raise ValueError("expected a JSON object")
    if check.script == "verify_square_witnesses.py":
        results = report.get("results", [])
        if report.get("all_passed") is not True or len(results) != 11:
            raise ValueError("expected eleven passing witnesses")
        if any(row.get("passed") is not True for row in results):
            raise ValueError("a witness did not pass")
        return "all eleven primitive square witnesses"
    if report.get("status") != "PASS":
        raise ValueError("checker did not report PASS")
    if check.script == "phase4_spread_descent_check.py":
        rows = report.get("results", [])
        expected = [(4, 2, 7, 2), (8, 4, 11811, 109), (6, 2, 31, 4)]
        actual = [(r["ambient_degree"], r["line_dimension"],
                   r["subspaces_containing_one"], r["semilinear_orbits"]) for r in rows]
        if actual != expected:
            raise ValueError("spread census has incomplete scope")
        for row in rows[:2]:
            orbits = row["irreducible_stabilizer_orbits"]
            if len(orbits) != 1 or orbits[0]["subfield"] is not True:
                raise ValueError("prime-degree rigidity check failed")
        if not any(r["subfield"] is False for r in rows[2]["irreducible_stabilizer_orbits"]):
            raise ValueError("missing non-subfield control")
        return "all 11,811 normalized four-spaces over F2 in F256; smaller and boundary cases"
    if check.script == "phase4_shadow_ip_check.py":
        if report.get("counts") != {
            "rank_two_structures": 682, "rank_two_comparisons": 84172,
            "rank_three_structures": 4096, "rank_three_comparisons": 1032192,
            "larger_structures": 48, "larger_comparisons": 38864,
            "residues_checked": 404, "residue_comparisons": 21502,
        }:
            raise ValueError("shadow comparison has incomplete scope")
        obstruction = report["closure_counterexample"]
        if (obstruction["every_flag_extends_to_chamber"] is not True or
            obstruction["closure_passes"] is not True or
            obstruction["flag_witness_exists"] is not False):
            raise ValueError("closure obstruction failed")
        return "682 rank-two and 4,096 rank-three structures; 48 larger examples; 404 residues"
    if check.script == "torsor_matrix_check.py":
        if report["matrix_calculus"]["subgroup_pairs"] != 900:
            raise ValueError("expected all 900 S4 subgroup pairs")
        return "900 S4 subgroup pairs; Helly obstruction; basis-loss example"
    if check.script == "suzuki_cycle_check.py":
        if report.get("all_sixteen_closing_entries_match") is not True:
            raise ValueError("closing matrix identity did not pass")
        return "five universal entries and sixteen Laurent-polynomial entries"
    if len(report.get("results", [])) != 16 or report.get("independent_small_solver_checks") != 144:
        raise ValueError("expected sixteen cocycle systems and 144 solver checks")
    return "sixteen cocycle systems; 144 independent small solver checks"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--quick", action="store_true", help="three standard-library checks (default)")
    mode.add_argument("--full", action="store_true", help="all five checks; requires NumPy")
    mode.add_argument("--older", action="store_true", help="two checks of the 2003/2004 reductions")
    parser.add_argument("--keep-work-dir", action="store_true", help="retain scratch logs and fresh reports")
    parser.add_argument("--timeout", type=float, default=600,
                        help="maximum seconds per checker (default: 600)")
    args = parser.parse_args()
    if sys.version_info < (3, 10):
        parser.error("Python 3.10 or newer is required")
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    suite = "full" if args.full else "older" if args.older else "quick"
    checks = {"full": FULL, "older": OLDER, "quick": QUICK}[suite]
    for check in checks:
        for name in (check.script, *check.inputs):
            if not (CASE_STUDY / name).is_file():
                parser.error(f"missing snapshot input: {CASE_STUDY / name}")
        if check.dependency and importlib.util.find_spec(check.dependency) is None:
            parser.error(f"--full requires {check.dependency}; install it in this Python environment")

    # Include absence in this record: a checker must not create a report in
    # the snapshot either.  Child processes only receive copied input files.
    protected = {CASE_STUDY / name for check in checks
                 for name in (check.script, check.report, *check.inputs)}
    before = {path: digest(path) if path.exists() else None for path in protected}
    scratch = Path(tempfile.mkdtemp(prefix="math-compression-smoke-"))
    env = os.environ.copy()
    env.pop("PYTHONOPTIMIZE", None)  # Assertions in the certificate scripts must run.
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    results = []
    failed = False
    try:
        print(f"Running {suite} suite ({len(checks)} checks).", flush=True)
        for index, check in enumerate(checks, 1):
            work = scratch / Path(check.script).stem
            work.mkdir()
            for name in (check.script, *check.inputs):
                shutil.copy2(CASE_STUDY / name, work / name)
            print(f"[{index}/{len(checks)}] {check.name} ...", flush=True)
            started = time.monotonic()
            record = {"script": check.script, "status": "FAIL"}
            log = work / "console.log"
            try:
                with log.open("w") as stream:
                    completed = subprocess.run(
                        [sys.executable, "-B", check.script], cwd=work, env=env,
                        stdout=stream, stderr=subprocess.STDOUT, timeout=args.timeout, check=False)
                if completed.returncode:
                    raise RuntimeError(f"checker exited with status {completed.returncode}")
                report = json.loads((work / check.report).read_text())
                scope = validate_report(check, report)
                record.update(status="PASS", scope=scope,
                              report_sha256=digest(work / check.report))
                print(f"  PASS: {scope} ({time.monotonic()-started:.2f}s)", flush=True)
            except (OSError, ValueError, KeyError, TypeError, RuntimeError, subprocess.TimeoutExpired) as error:
                failed = True
                record["error"] = str(error)
                print(f"  FAIL: {error}", file=sys.stderr, flush=True)
                if log.exists():
                    print("\n".join(log.read_text(errors="replace").splitlines()[-20:]), file=sys.stderr)
            record["elapsed_seconds"] = round(time.monotonic() - started, 3)
            results.append(record)

        changed = [str(path.relative_to(ROOT)) for path, expected in before.items()
                   if (digest(path) if path.exists() else None) != expected]
        if changed:
            failed = True
            print("FAIL: snapshot files changed: " + ", ".join(sorted(changed)), file=sys.stderr)
        summary = {"status": "FAIL" if failed else "PASS",
                   "suite": suite, "python": sys.version,
                   "snapshot_inputs_and_reports_unchanged": not changed,
                   "results": results}
        (scratch / "smoke_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
        print(f"{'FAIL' if failed else 'PASS'}: {sum(r['status']=='PASS' for r in results)}/{len(checks)} checks; "
              f"snapshot {'changed' if changed else 'unchanged'}.", flush=True)
        return 1 if failed else 0
    finally:
        if failed or args.keep_work_dir:
            print(f"Scratch reports and logs: {scratch}", flush=True)
        else:
            shutil.rmtree(scratch)


if __name__ == "__main__":
    raise SystemExit(main())
