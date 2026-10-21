"""Independent literal-permutation checks; no group-library dependency."""
import argparse
from collections import deque
import json
from pathlib import Path
import sys

if sys.flags.optimize:
    raise SystemExit("optimized Python is unsupported")

def need(p, message):
    if not p:
        raise ValueError(message)

def multiply(p, q):
    return tuple(q[x] for x in p)

def closure(marks):
    n = len(marks[0]); identity = tuple(range(n))
    seen = {identity}; queue = deque([identity])
    while queue:
        p = queue.popleft()
        for q in marks:
            t = multiply(p, q)
            if t not in seen:
                seen.add(t); queue.append(t)
    return seen

def parse_marks(row, n, rank):
    data = row["permutations"]
    need(len(data) == rank, "wrong rank")
    need(all(type(x) is int for p in data for x in p), "noninteger permutation")
    need(all(len(p) == n and sorted(p) == list(range(1, n + 1)) for p in data),
         "not a permutation")
    marks = [tuple(x - 1 for x in p) for p in data]
    identity = tuple(range(n))
    need(all(p != identity and multiply(p, p) == identity for p in marks),
         "not a nonidentity involution")
    need(all(multiply(marks[i], marks[j]) == multiply(marks[j], marks[i])
             for i in range(rank) for j in range(i + 2, rank)), "not a string")
    return marks

def anchors(marks):
    return [a for a in range(len(marks[0])) if marks[0][a] != a
            and all(p[a] == a for p in marks[1:])]

def centralizer_fixing(marks, a):
    """Enumerate all bijections commuting with every mark and fixing a.

    An assigned image forces the images of its complete marked orbit.
    At each unassigned vertex all unused images are tried. Every surviving
    complete map is checked directly, so this is both exhaustive and exact.
    """
    n = len(marks[0]); output = []
    def extend(mapping, reverse, x, y):
        mapping = mapping.copy(); reverse = reverse.copy(); todo = [(x, y)]
        while todo:
            u, v = todo.pop()
            if u in mapping:
                if mapping[u] != v:
                    return
                continue
            if v in reverse:
                return
            mapping[u] = v; reverse[v] = u
            todo.extend((p[u], p[v]) for p in marks)
        if len(mapping) == n:
            result = tuple(mapping[i] for i in range(n))
            need(all(multiply(result, p) == multiply(p, result) for p in marks),
                 "centralizer completion error")
            output.append(result)
            return
        u = next(i for i in range(n) if i not in mapping)
        for v in range(n):
            if v not in reverse:
                extend(mapping, reverse, u, v)
    extend({}, {}, a, a)
    need(len(output) == len(set(output)), "duplicate centralizer maps")
    return output

def run(data):
    small = data["small_exceptions"]; large = data["a11_rank_six"]
    need(len(small) == 15 and len(large) == 4, "incomplete census input")
    need([(r["kind"], r["source_index"]) for r in small] ==
         [("small_transitive", i) for i in range(14)] + [("primitive_markings", 10)],
         "wrong or duplicate small census indices")
    need([r["source_index"] for r in large] == list(range(4)),
         "wrong or duplicate A11 census indices")
    need(len({tuple(tuple(p) for p in r["permutations"]) for r in large}) == 4,
         "duplicate A11 tuple")
    report = {"small": [], "a11": []}
    for row in small:
        n = row["n"]; rank = len(row["permutations"])
        need(n in (6, 8) and rank * 2 > n, "wrong small exception")
        marks = parse_marks(row, n, rank)
        ends = [anchors(marks), anchors(marks[::-1])]
        need(ends == [[], []], "small exception has an endpoint anchor")
        report["small"].append({"kind": row["kind"], "source_index": row["source_index"],
                                "n": n, "rank": rank, "anchors": ends})
    for row in large:
        marks = parse_marks(row, 11, 6)
        for orientation, sequence in enumerate((marks, marks[::-1])):
            points = anchors(sequence)
            entry = {"source_index": row["source_index"], "orientation": orientation,
                     "anchors": [a + 1 for a in points], "witnesses": []}
            for a in points:
                centralizer = centralizer_fixing(sequence[1:], a)
                need(centralizer == [tuple(range(11))], "nontrivial anchored centralizer")
                leaf = list(range(12)); leaf[a], leaf[11] = 11, a
                extended = [tuple(leaf)] + [p + (11,) for p in sequence]
                u = closure(extended[1:5]); v = closure(extended[:4])
                middle = closure(extended[1:4]); inter = u & v
                need(middle <= inter, "middle not contained")
                sizes = [len(u), len(v), len(inter), len(middle)]
                need(sizes == [5040, 5040, 360, 60], "wrong finite obstruction")
                entry["witnesses"].append({"anchor": a + 1, "centralizer_order": 1,
                     "interval": [0, 4], "end_orders": sizes[:2],
                     "intersection_order": sizes[2], "middle_order": sizes[3], "index": 6})
            report["a11"].append(entry)
    report["status"] = "PASS"
    return report

def main():
    p = argparse.ArgumentParser(); p.add_argument("--input", type=Path, default=Path(__file__).with_name("wing_inputs.json")); p.add_argument("--output", type=Path, required=True)
    a = p.parse_args(); result = run(json.loads(a.input.read_text()))
    a.output.write_text(json.dumps(result, indent=2) + "\n")
    print("PASS: 15 small exceptions, 4 A11 representatives, both endpoint orientations")

if __name__ == "__main__":
    main()
