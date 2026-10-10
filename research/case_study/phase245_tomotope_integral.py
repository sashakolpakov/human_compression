#!/usr/bin/env python3
"""Independent integral homology reduction of a supplied finite cell complex.

Only unit row/column operations precede a common factor extraction. The
input geometry is supplied by phase246 and is not reconstructed here.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import time


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def eliminate_units(rows, columns, vectors):
    rows = {i: dict(row) for i, row in enumerate(rows) if row}
    support = defaultdict(set)
    for i, row in rows.items():
        for c in row:
            support[c].add(i)
    ops = []
    active = set(columns)
    while True:
        choices = [(len(row), len(support[c]), i, c)
                   for i, row in rows.items() for c, a in row.items() if abs(a) == 1]
        if not choices:
            break
        _, _, pivot, c = min(choices)
        row = rows[pivot]
        sign = row[c]
        row = {j: a*sign for j, a in row.items()}
        ops.append({'pivot_row': pivot, 'column': c, 'sign': sign,
                    'row': sorted(row.items())})
        # Clear the pivot column by integral row operations.
        for i in list(support[c]):
            if i == pivot:
                continue
            old = rows[i]
            a = old[c]
            for j, b in row.items():
                new = old.get(j, 0)-a*b
                if new:
                    old[j] = new
                    support[j].add(i)
                elif j in old:
                    del old[j]
                    support[j].discard(i)
            if not old:
                del rows[i]
        # Track specified cycle classes under the same quotient reduction.
        for v in vectors:
            a = v.get(c, 0)
            if a:
                for j, b in row.items():
                    new = v.get(j, 0)-a*b
                    if new:
                        v[j] = new
                    else:
                        v.pop(j, None)
        # Column operations now clear the rest of the unit pivot row;
        # its column is zero in every other row, so those rows are unchanged.
        for j in rows[pivot]:
            support[j].discard(pivot)
        del rows[pivot]
        active.remove(c)
        need(not support[c], 'cleared pivot column')
    return list(rows.values()), sorted(active), vectors, ops


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists(), 'fresh output required')
    start = time.monotonic()
    data = json.loads(args.input.read_text())
    endpoints = data['complex']['endpoints']
    faces = [{int(k): int(v) for k, v in row.items()}
             for row in data['complex']['boundaries']]
    nv, ne = data['graph_vertices'], data['graph_edges']
    need(len(endpoints) == ne and len(faces) == data['square_relator_rows'], 'cell counts')
    parent = list(range(nv))
    def root(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    tree = []
    for e, (a, b) in enumerate(endpoints):
        a, b = root(a), root(b)
        if a != b:
            parent[a] = b
            tree.append(e)
    need(len(tree) == nv-1, 'connected graph and maximal tree')
    cotree = sorted(set(range(ne))-set(tree))
    cols = set(cotree)
    for row in faces:
        boundary = [0]*nv
        for e, a in row.items():
            u, v = endpoints[e]
            boundary[u] -= a
            boundary[v] += a
        need(not any(boundary), 'every two-cell boundary is an integral cycle')
    # Non-tree edge coordinates are an integral basis of the cycle lattice.
    rows = [{e: a for e, a in row.items() if e in cols} for row in faces]
    # Duplicate rows, and their negatives, have the same integer row span.
    unique = set()
    for row in rows:
        if row:
            sign = 1 if row[min(row)] > 0 else -1
            unique.add(tuple(sorted((e, sign*a) for e, a in row.items())))
    rows = [dict(row) for row in sorted(unique)]
    base = 0
    defects = []
    for edge in data['defect_edges']:
        need(endpoints[edge] == endpoints[base], 'parallel defect edges')
        defects.append({e: a for e, a in {edge: 1, base: -1}.items() if e in cols})
    residual, active, vectors, operations = eliminate_units(rows, cotree, defects)
    need(len(operations) == 719 and len(active) == 2, 'unit invariant factors')
    need(all(a % 2 == 0 for row in residual for a in row.values()), 'residual lattice lies in twice Z2')
    halved = [{c: a//2 for c, a in row.items()} for row in residual]
    final, final_columns, _, final_ops = eliminate_units(halved, active, [])
    need(not final and not final_columns and len(final_ops) == 2, 'residual lattice equals twice Z2')
    images = [[v.get(c, 0) % 2 for c in active] for v in vectors]
    need(all(any(v) for v in images), 'every specified defect survives integral torsion')
    report = {'status': 'PASS', 'seconds': round(time.monotonic()-start, 3),
              'input_sha256': hashlib.sha256(args.input.read_bytes()).hexdigest(),
              'cells': [nv, ne, len(faces)], 'cycle_rank': len(cotree),
              'distinct_signed_square_rows': len(rows),
              'integer_invariant_factors': {'one': 719, 'two': 2, 'zero': 0},
              'H1_Z': 'C2 x C2', 'remaining_columns': active,
              'defect_images_mod2': images, 'spanning_tree': tree,
              'unit_operations': operations, 'halved_residual_unit_operations': final_ops,
              'scope': 'Independent exact integer reduction of the supplied cellular matrix. Phase246 owns identification with the Tomotope completion.'}
    args.out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if not k.endswith('operations') and k != 'spanning_tree'}))


if __name__ == '__main__':
    main()
