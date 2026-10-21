#!/usr/bin/env python3
"""Exact affine intertwiner from the earlier voltage model to six coordinates."""
import argparse
from collections import deque
from hashlib import sha256
import json
from pathlib import Path

from phase35_L003_affine_check import MATRICES, OFFSETS, BASIS_EDGES

COORDINATES = [0, 1, 2, 4, 5, 6]
EXPECTED_MINOR = [
    [0,0,1,-1,0,0], [0,0,0,0,-1,-1], [1,0,0,1,1,0],
    [0,0,-1,0,-1,1], [0,0,0,0,1,0], [1,1,-1,0,0,0],
]
ORIGIN_NUMERATOR = [-44,-6,36,-80,210,-94]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--data', type=Path, default=Path(__file__).with_name(
        'phase33_L003_even_voltage.json'))
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise SystemExit('Refusing to overwrite saved evidence')
    raw = args.data.read_bytes()
    data = json.loads(raw)
    n = data['degree']
    assert n == 648
    pp = [tuple(a-1 for a in row) for row in data['permutations']]
    vv = [tuple(row) for row in data['weights']]
    assert len(pp) == len(vv) == 3
    assert all(sorted(p) == list(range(n)) for p in pp)
    assert all(len(v) == n and all(type(a) is int for a in v) for v in vv)
    D = 2*n
    one = (tuple(range(D)), (0,)*D)
    marks = [(tuple(range(n,D))+tuple(range(n)), (0,)*D)]
    for p, v in zip(pp,vv):
        inv = [0]*n
        for i,j in enumerate(p):
            inv[j] = i
        marks.append((tuple(n+i for i in inv)+p,
                      tuple(-v[i] for i in inv)+v))

    def multiply(a,b):
        p,v = a
        q,w = b
        return tuple(q[i] for i in p), tuple(x+w[i] for x,i in zip(v,p))

    assert all(multiply(g,g) == one for g in marks)
    reps = [one]
    where = {one[0]:0}
    todo = deque([0])
    edges = []
    while todo:
        a = todo.popleft()
        assert a == len(edges)
        row = []
        for mark in marks:
            b = multiply(reps[a],mark)
            if b[0] not in where:
                where[b[0]] = len(reps)
                reps.append(b)
                todo.append(where[b[0]])
            row.append(where[b[0]])
        edges.append(row)
        assert len(reps) <= D
    assert len(reps) == D
    basis = []
    for a,j in BASIS_EDGES:
        image = multiply(reps[a],marks[j])
        target = reps[edges[a][j]]
        assert image[0] == target[0]
        basis.append(tuple(x-y for x,y in zip(image[1],target[1])))
    assert [[b[i] for b in basis] for i in COORDINATES] == EXPECTED_MINOR

    total = [sum(v[i] for p,v in reps) for i in range(D)]
    theta = [total[i]+sum(c*b[i] for c,b in zip(ORIGIN_NUMERATOR,basis))
             for i in range(D)]
    linear_checks = offset_checks = 0
    for (p,v),M,b in zip(marks,MATRICES,OFFSETS):
        for i in range(D):
            for j in range(6):
                assert basis[j][p[i]] == sum(basis[k][i]*M[k][j]
                                             for k in range(6))
                linear_checks += 1
            assert 2*D*v[i]+2*theta[p[i]]-2*theta[i] == D*sum(
                basis[k][i]*b[k] for k in range(6))
            offset_checks += 1
    report = {
        'status':'PASS',
        'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'literal_affine_source_sha256':sha256(Path(__file__).with_name(
            'phase35_L003_affine_check.py').read_bytes()).hexdigest(),
        'voltage_data_sha256':sha256(raw).hexdigest(),
        'underlying_permutation_quotient_order':D,
        'basis_edges_zero_based':BASIS_EDGES,
        'minor_coordinates_zero_based':COORDINATES,
        'basis_minor':EXPECTED_MINOR,
        'origin_shift_numerator':ORIGIN_NUMERATOR,
        'origin_shift_denominator':D,
        'linear_intertwining_coordinate_checks':linear_checks,
        'affine_intertwining_coordinate_checks':offset_checks,
        'embedding':'E(a)=theta+B*a/2; theta=(sum_q voltage(s(q))+B*origin_numerator)/1296',
        'scope':'Exact generator intertwining. Faithfulness and all-modulus marked identification use the written argument and frozen saturated-lattice theorem.'
    }
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PHASE35_L003_AFFINE_COMPARE_PASS',linear_checks,offset_checks)


if __name__ == '__main__':
    main()
