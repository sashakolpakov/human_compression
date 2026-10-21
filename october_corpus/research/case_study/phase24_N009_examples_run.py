#!/usr/bin/env python3
"""Re-run the N009 finite-presentation checks in an isolated temporary directory.

The mathematical checker uses GAP and NQ. Primary PDFs/HTML, BeautifulSoup,
SmallGroups and the phase22 census executable are not execution dependencies.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parent
INPUTS = [
    "phase24_N009_examples_check.g",
    "phase24_N009_atlas_library.g",
    "phase22_N009_atlas_library.g",
    "phase22_N009_rank3.accepted.json",
]
OUTPUTS = [
    "phase24_N009_examples_results.json",
    "phase24_N009_table3_matches.json",
    "phase24_N009_table4_literal_matches.json",
    "phase24_N009_example_facets.json",
    "phase24_N009_census_matches.json",
]
PASS = (
    "PASS raw_presentations=34 exact_IP_meets=3328; eight distinct "
    "Table3/Example3.9 target markings; all twelve Table3 assignments; "
    "Table4 literal e->c,f->a,h->c; three exhaustive Example4.5 central involutions."
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gap", default="gap")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=1200)
    args = parser.parse_args()
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="phase24-N009-") as directory:
        scratch = Path(directory)
        for name in INPUTS:
            shutil.copy2(ROOT / name, scratch / name)
        run = subprocess.run(
            [args.gap, "-q", "phase24_N009_examples_check.g"],
            cwd=scratch, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, timeout=args.timeout, check=False,
        )
        log = out / "phase24_N009_examples_check.log"
        log.write_text(run.stdout)
        if run.returncode != 0 or PASS not in run.stdout:
            raise RuntimeError(f"GAP did not reach the complete PASS marker; inspect {log}")
        if re.search(r"(^|\n)(Error,|Syntax error:|brk>)", run.stdout):
            raise RuntimeError(f"GAP error despite terminal marker; inspect {log}")
        for name in OUTPUTS:
            json.loads((scratch / name).read_text())
            shutil.copy2(scratch / name, out / name)
    results = json.loads((out / OUTPUTS[0]).read_text())
    assignments = json.loads((out / OUTPUTS[1]).read_text())
    literal = json.loads((out / OUTPUTS[2]).read_text())
    facets = json.loads((out / OUTPUTS[3]).read_text())
    census = json.loads((out / OUTPUTS[4]).read_text())
    assert len(results) == 34 and len(assignments) == 12
    assert literal == [[1, 1], [2, 2], [3, 3], [4, 4], [5, 3], [6, 1], [7, 7], [8, 3]]
    assert len(facets) == 5
    assert len(census) == 8 and sorted(x[1] for x in census) == list(range(1, 9))
    versions = re.search(r"SOFTWARE GAP=(\S+) NQ=(\S+)", run.stdout)
    assert versions is not None
    report = {
        "status": "PASS",
        "scope": "Raw finite presentations, actual marked IP and exact named-object/census adapters; not a fresh full census.",
        "software": {"GAP": versions[1], "NQ": versions[2]},
        "raw_presentations": 34,
        "actual_marked_subgroup_meets": 3328,
        "table3_assignments": 12,
        "distinct_order1024_type48_targets": 8,
        "exact_primary_order512_Atlas_labels": 5,
        "exact_example_facet_labels": 10,
        "example45_all_central_involutions": 3,
        "literal_table4_index_map": literal,
        "exit_code": run.returncode,
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "inputs": [{"path": name, "sha256": sha(ROOT / name)} for name in INPUTS],
        "runner": {"path": Path(__file__).name, "sha256": sha(Path(__file__))},
        "outputs": [{"path": name, "sha256": sha(out / name)} for name in OUTPUTS + [log.name]],
    }
    (out / "phase24_N009_examples_run.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ["status", "raw_presentations", "actual_marked_subgroup_meets", "elapsed_seconds"]}))


if __name__ == "__main__":
    main()
