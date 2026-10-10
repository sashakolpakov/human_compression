#!/usr/bin/env python3
"""Independent scratch replay and numerical coset-table checks for L088.

The GAP scripts are the frozen author's implementations. The independent
Python certificate checks all presentation relators on their actual table.
"""
import argparse
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table_check(table):
    assert len(table) == 8
    n = len(table[0])
    assert n == 1463
    assert all(sorted(row) == list(range(1, n + 1)) for row in table)
    generators = table[::2]
    for i, row in enumerate(generators):
        assert table[2 * i + 1] == row
        assert all(row[row[p] - 1] == p + 1 for p in range(n))
    # Exact literal source words in the order a,b,c,d = 0,1,2,3.
    relators = [[i, i] for i in range(4)]
    relators += [[0, 1] * 5, [0, 2] * 2, [0, 3] * 2,
                 [1, 2] * 3, [1, 3] * 2, [2, 3] * 5,
                 [0, 1, 2] * 5, ([3, 2, 1] * 5 + [0]) * 3]
    for word in relators:
        for p in range(1, n + 1):
            q = p
            for i in word:
                q = generators[i][q - 1]
            assert q == p
    seen = {1}
    queue = deque([1])
    while queue:
        p = queue.popleft()
        for g in generators:
            q = g[p - 1]
            if q not in seen:
                seen.add(q)
                queue.append(q)
    assert len(seen) == n
    assert all(g[0] == 1 for g in generators[1:])
    return dict(degree=n, generators=4, inverse_rows_verified=4,
                literal_relators=len(relators), relator_point_evaluations=len(relators) * n,
                orbit_size=len(seen), basepoint_fixed_by_bcd=True,
                scope="Independent permutation/coset-table consistency. Exact presentation-index upper bound still retains complete Todd–Coxeter correctness and the spherical facet bound.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--directory", type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument("--gap", default=os.environ.get("GAP") or shutil.which("gap"))
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    assert args.gap
    root = args.directory.resolve()
    inputs = ["phase24_L088_check.g", "phase24_L088_presentation.g", "phase24_L088_seed.json"]
    with tempfile.TemporaryDirectory(prefix="L088_independent_") as tmp:
        scratch = Path(tmp)
        for name in inputs:
            shutil.copy2(root / name, scratch / name)

        def execute(name):
            cp = subprocess.run([args.gap, "-q", "-T", name], cwd=scratch,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                check=True, timeout=600)
            text = cp.stdout.decode()
            marker = "L088_ALL_SIX_PASS" if name.endswith("check.g") else "PRESENTATION_PASS"
            assert marker in text
            assert not re.search(r"(^|\n)(Error,|Syntax error:|brk>)", text)
            return dict(script=name, sha256=sha(root / name), stdout=text,
                        stdout_sha256=hashlib.sha256(cp.stdout).hexdigest())

        with ThreadPoolExecutor(max_workers=2) as pool:
            runs = list(pool.map(execute, inputs[:2]))
        generated = []
        for name in ["phase24_L088_results.g", "phase24_L088_coset_table.json"]:
            assert (scratch / name).read_bytes() == (root / name).read_bytes()
            generated.append(dict(path=name, sha256=sha(scratch / name), byte_identical=True))
        table = json.loads((scratch / "phase24_L088_coset_table.json").read_text())
        independent = table_check(table)
        summary = []
        pattern = r"GEOMETRY (\d+) PAIRS (\[[^\]]*\]) PARABOLICS (\[[^\]]*\]).* IP (\d+) HELLY (\d+) PASS"
        for line in runs[0]["stdout"].splitlines():
            m = re.fullmatch(pattern, line)
            if m:
                summary.append(dict(marking=int(m[1]), pair_orders=json.loads(m[2]),
                                    parabolic_orders=json.loads(m[3]),
                                    actual_meets=int(m[4]), typed_Helly=int(m[5])))
        assert len(summary) == 6
        assert all(x["actual_meets"] == 256 and x["typed_Helly"] == 28 for x in summary)
        multisets = [tuple(sorted(x["parabolic_orders"])) for x in summary]
        assert len(set(multisets)) == 6
        assert multisets[2] == (20, 60, 60, 120)
        assert multisets[3] == (20, 60, 120, 120)
        report = dict(schema_version=1, status="PASS", checker_sha256=sha(Path(__file__)),
                      input_bindings=[dict(path=n, sha256=sha(root / n)) for n in inputs],
                      fresh_GAP_runs=runs, generated_outputs=generated,
                      independent_coset_table_check=independent, markings=summary,
                      six_order_multisets_pairwise_distinct=True,
                      scope="Fresh execution of both unchanged author scripts plus independent finite table checks. No new classification census, quotient-IP assumption, or full Lean claim.")
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(dict(status="PASS", geometries=6, actual_meets=1536,
                          typed_Helly=168, independent_relator_points=independent["relator_point_evaluations"],
                          output_sha256=sha(args.output))))


if __name__ == "__main__":
    main()
