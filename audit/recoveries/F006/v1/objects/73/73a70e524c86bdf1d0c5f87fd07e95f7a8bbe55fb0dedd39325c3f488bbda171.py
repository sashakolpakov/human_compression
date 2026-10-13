#!/usr/bin/env python3
"""Replay the bounded GAP calculation; it is not a complete L047 proof."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

EXPECTED = [
    ("S2xS3", 5, 3, 4, 16, 20, 84, 84, 0, 0, 0),
    ("S2xS4", 6, 4, 12, 48, 68, 148, 148, 0, 0, 0),
    ("S3xS3", 6, 4, 1, 4, 5, 8, 8, 0, 0, 0),
    ("S2xS5", 7, 5, 4, 16, 20, 28, 28, 0, 0, 0),
    ("S3xS4", 7, 5, 6, 24, 34, 34, 34, 0, 0, 0),
    ("S2xS6", 8, 6, 8, 32, 40, 56, 56, 0, 0, 0),
    ("S3xS5", 8, 6, 2, 8, 10, 8, 8, 0, 0, 0),
    ("S4xS4", 8, 6, 9, 36, 57, 30, 30, 0, 0, 0),
    ("T6_9", 6, 4, 1, 4, 5, 8, 8, 2, 0, 0),
    ("T6_11", 6, 4, 12, 48, 68, 148, 148, 152, 0, 0),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--gap", default="gap")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    gap = shutil.which(args.gap)
    if gap is None:
        raise RuntimeError("GAP executable unavailable")
    proc = subprocess.run([gap, "-q", "-b", "run.g"], cwd=root,
                          capture_output=True, text=True, check=False)
    (out / "gap.stdout.log").write_text(proc.stdout)
    (out / "gap.stderr.log").write_text(proc.stderr)
    if proc.returncode or proc.stderr.strip() or "Error," in proc.stdout:
        raise RuntimeError("GAP replay failed; inspect logs")
    rows = []
    for line in proc.stdout.splitlines():
        if line.startswith("SUMMARY|"):
            fields = line.split("|")[1:]
            rows.append((fields[0], *(int(x) for x in fields[1:])))
    if rows != EXPECTED:
        raise RuntimeError("Incomplete or changed finite census")
    if proc.stdout.count("PASS_L047_FINITE_BOUNDARY") != 1:
        raise RuntimeError("Missing completion marker")
    if proc.stdout.count("CONTROL|positive_rank3|6") != 1:
        raise RuntimeError("Missing positive control")
    report = {
        "status": "PASS_BOUNDED_COMPUTATION_ONLY",
        "case_count": len(rows),
        "rows": rows,
        "normalized_markings": sum(r[3] for r in rows),
        "transitive_completions": sum(r[8] for r in rows),
        "independent_completions": sum(r[9] for r in rows),
        "positive_control_completions": 6,
        "negative_controls": ["redundant three-reflection IP", "redundant independence"],
        "scope": "The ten explicit normalized H actions; neither the reduction to these actions nor the full L047 theorem is asserted by this executable.",
        "trust": ["GAP finite permutation group algorithms", "GAP degree-six transitive-group catalogue"],
        "lean_formalized": False,
        "files": {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
                  for name in ["search.g", "run.g", "check.py"]},
    }
    (out / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ["status", "case_count", "normalized_markings", "transitive_completions"]}))


if __name__ == "__main__":
    main()
