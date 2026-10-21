#!/usr/bin/env python3
"""Fresh exhaustive kernel census and complete-presentation recognition.

Inputs are exactly three printed GAP/data programs; no saved census, private
primary text, Atlas permutation array or SmallGroups catalogue is read.
The output directory must not exist. GAP/NQ remain trusted exact algorithms.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parent
INPUTS = ["phase78_n009_integration_census.g", "phase78_n009_integration_finite.g", "phase78_n009_integration_data.g"]
CASES = [(3, 3, 61, 37, 3, 20, 3904, [7, 23, 61]), (3, 5, 401, 235, 15, 125, 25664, [7, 23, 61, 147, 401]), (4, 3, 1483, 199, 11, 105, 379648, [31, 267, 1483]), (5, 1, 127, 15, 1, 8, 130048, [127])]
FINAL = "PASS complete_presentations=214 actual_IP_meets=43840 atlas=72 raw_examples=34 exceptional=2 finite_universals=106 exact_census_facets=428 table6_rows=107 table5_rows=12"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--gap", default="gap")
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--timeout", type=int, default=1200)
    args = ap.parse_args()
    out = args.output_dir.resolve()
    require(not out.exists(), "Refusing existing output directory")
    bindings = [{"path": n, "sha256": sha(ROOT / n)} for n in INPUTS]
    out.mkdir(parents=True)
    start = time.monotonic()
    for n in INPUTS:
        shutil.copy2(ROOT / n, out / n)
    timings = {}
    for name, program in [("census", INPUTS[0]), ("finite", INPUTS[1])]:
        t = time.monotonic()
        run = subprocess.run([args.gap, "-q", "-T", program], cwd=out, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=args.timeout, check=False)
        (out / (name + ".log")).write_text(run.stdout)
        (out / (name + ".err")).write_text(run.stderr)
        require(run.returncode == 0 and not run.stderr.strip(), f"{name}: execution error or warning")
        require(not re.search(r"(^|\n)(Error,|Syntax error:|brk>)", run.stdout), f"{name}: GAP failure")
        timings[name] = round(time.monotonic() - t, 6)
    census = (out / "census.log").read_text()
    finite = (out / "finite.log").read_text()
    require(census.count("PASS: complete invariant-kernel ladder") == 4 and FINAL in finite, "Incomplete terminal markers")
    observed = re.findall(r"RESULT rank=(\d+) excess=(\d+) candidates=(\d+) ordered=(\d+) selfdual=(\d+) up_to_reversal=(\d+) actual_meets=(\d+)", census)
    require([tuple(map(int, r)) for r in observed] == [x[:7] for x in CASES], "Census totals differ")
    for d, k, candidates, ordered, fixed, classes, meets, levels in CASES:
        for j, n in enumerate(levels, 1):
            data = json.loads((out / f"phase78_d{d}_k{k}.level{j}.json").read_text())
            require(len(data) == n and len({tuple(x) for x in data}) == n, "Ladder cardinality or duplicate key")
        accepted = json.loads((out / f"phase78_d{d}_k{k}.accepted.json").read_text())
        require(len(accepted) == ordered and sum(x[4] for x in accepted) == fixed, "Accepted cardinality/fixed count")
    seeds = json.loads((out / "phase78_d3_k3.seed.json").read_text())
    require(len(seeds) == 4 and sorted(x[1] for x in seeds) == [1, 2, 3, 4], "All four distinct seed rows")
    read = lambda suffix: json.loads((out / ("phase78_n009_integration_" + suffix + ".json")).read_text())
    require(len(read("all_presentations")) == 214, "Complete presentation count")
    require(read("table4_literal_matches") == [[1, 1], [2, 2], [3, 3], [4, 4], [5, 3], [6, 1], [7, 7], [8, 3]], "Literal correction map")
    require(len(read("table3_matches")) == 12, "Table3 cells")
    require(len(read("facet_matches")) == 214 and len(read("table6_results")) == 107, "Facet/table6 rows")
    require(len(read("universal_orders")) == 106, "Finite universals")
    require(len(read("census_matches")) == 8 and sorted(x[1] for x in read("census_matches")) == list(range(1, 9)), "Eight named source targets")
    versions = re.findall(r"VERSION GAP=(\S+) NQ=(\S+)", census)
    require(len(versions) == 4 and len(set(versions)) == 1, "Software identity")
    for row in bindings:
        require(sha(ROOT / row["path"]) == row["sha256"] == sha(out / row["path"]), "Mathematical input changed during replay")
    files = [{"path": p.name, "sha256": sha(p)} for p in sorted(out.iterdir()) if p.is_file()]
    report = dict(status="PASS", software=dict(zip(["GAP", "NQ"], versions[0])), elapsed_seconds=round(time.monotonic()-start, 6), timings=timings,
        cases=[dict(zip(["rank", "excess", "terminal_kernels", "ordered", "selfdual", "classes", "actual_meets", "ladder_sizes"], c)) for c in CASES],
        total_census_meets=539264, complete_presentations=214, presentation_IP_meets=43840,
        source_table6_rows=107, source_table5_rows=12, named_census_facet_isomorphisms=428,
        source_statement_scope="Corrected principal contract with explicitly retained geometric/square/infinite inputs; no historical novelty or Lean verification.",
        candidate_generation_uses_source_totals=False, SmallGroups_dependency=False, old_census_input=False, private_primary_input=False,
        inputs=bindings, runner=dict(path=Path(__file__).name, sha256=sha(Path(__file__))), outputs=files)
    (out / "phase78_n009_integration_run.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k: report[k] for k in ["status", "software", "elapsed_seconds", "total_census_meets", "complete_presentations", "presentation_IP_meets"]}))


if __name__ == "__main__":
    main()
