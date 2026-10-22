"""Check literal premises of the written middle-vertex obstruction.

This is a finite witness check, not a formal proof of the general theorem.
No project imports, graph generation or census transition occurs here.
"""
from collections import deque
from pathlib import Path
import argparse
import hashlib
import json
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(line):
    require(line.endswith(b"\n") and line.count(b"\n") == 1,
            "one complete original record")
    fields = line.split()
    require(fields[0] == b"F009_ROOTED_V1", "original rooted wire")
    values = [int(x) for x in fields[1:]]
    require(len(values) >= 11 and values[:6] == [32, 5, 4, 8, 0, 10]
            and len(values) == 11 + 2 * values[10], "exact target and wire size")
    ordered = list(zip(values[11::2], values[12::2]))
    require(ordered == sorted(set(ordered))
            and all(0 <= u < v < 32 for u, v in ordered), "simple sorted graph")
    edges = set(ordered)
    neighbors = [set() for _ in range(32)]
    for u, v in ordered:
        neighbors[u].add(v)
        neighbors[v].add(u)
    require(all(len(cell) <= 5 for cell in neighbors), "degree at most five")
    require(all(not (neighbors[u] & neighbors[v]) for u, v in ordered),
            "partial graph has no triangle")
    left, middle, right = set(range(1, 6)), set(range(21, 26)), set(range(11, 16))
    seed = {(0, x) for x in left} | {(10, x) for x in right}
    seed |= {(20, x) for x in middle}
    seed |= {(1, x) for x in range(6, 10)}
    seed |= {(11, x) for x in range(16, 20)} | {(9, 21), (19, 25)}
    require(len(seed) == 25 and seed <= edges, "entire prescribed seed")
    require(neighbors[0] == left and neighbors[20] == middle
            and neighbors[10] == right, "three saturated center neighborhoods")
    distance = {0: 0}
    queue = deque([0])
    while queue:
        u = queue.popleft()
        for v in neighbors[u]:
            if v not in distance:
                distance[v] = distance[u] + 1
                queue.append(v)
    require(distance.get(10) == 8, "partial marked distance is exactly eight")
    independent = left | middle | right
    require(len(independent) == 15
            and all(not (neighbors[v] & independent) for v in independent),
            "literal independent set")
    complement = set(range(32)) - independent
    available = complement - {0, 10, 20}
    witnesses = []
    for v in sorted(available):
        defect_neighbors = sorted(neighbors[v] & available)
        if {21, 25} <= neighbors[v] and len(defect_neighbors) >= 2:
            witnesses.append(dict(vertex=v, defect_neighbors=defect_neighbors[:2],
                                  left_middle_neighbor=21, right_middle_neighbor=25))
    require(witnesses, "seed and four-edge obstruction must both be present")
    return dict(family_sha256=hashlib.sha256(line).hexdigest(),
                target=[32, 5, 4, 8], marked_roots=[0, 10],
                partial_edges=len(edges), witnesses=witnesses,
                empty_by_written_theorem=True)


def main():
    require(sys.flags.ignore_environment and sys.flags.no_site
            and sys.dont_write_bytecode and not sys.flags.optimize, "run with -E -B -S")
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--input-sha256", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    source = args.input.resolve(strict=True)
    raw = source.read_bytes()
    require(0 < len(raw) <= 8192, "bounded full input")
    digest = hashlib.sha256(raw).hexdigest()
    require(digest == args.input_sha256, "whole original input SHA256")
    lines = raw.splitlines(keepends=True)
    require(1 <= len(lines) <= 2 and all(len(line) <= 4096 for line in lines),
            "one or two complete bounded families")
    records = [check(line) for line in lines]
    require(len({r["family_sha256"] for r in records}) == len(records), "distinct families")
    output = args.out.absolute()
    require(output.parent.resolve(strict=True) == output.parent
            and not output.exists() and not output.is_symlink(), "fresh absolute output")
    result = dict(schema="MIDDLE_VERTEX_LITERAL_CERTIFICATES_V1", status="PASS",
                  input=dict(path=str(source), bytes=len(raw), sha256=digest),
                  records=records, empty_families=len(records),
                  scope="Literal premises of the independently reviewed written theorem",
                  general_theorem_formally_verified=False, Lean_verified=False,
                  census_complete=False, accepted_census_changed=False,
                  whole_original_credit=0)
    encoded = (json.dumps(result, sort_keys=True, indent=2) + "\n").encode()
    with output.open("xb") as stream:
        require(stream.write(encoded) == len(encoded), "whole exclusive result")
    print(json.dumps(dict(status="PASS", empty_families=len(records),
                          result=dict(path=str(output), bytes=len(encoded),
                                      sha256=hashlib.sha256(encoded).hexdigest())), sort_keys=True))


if __name__ == "__main__":
    main()
