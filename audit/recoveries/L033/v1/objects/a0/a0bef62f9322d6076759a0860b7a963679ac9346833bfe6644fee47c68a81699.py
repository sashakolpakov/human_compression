"""Independent exact reader of finite sets covering fundamental-weight orbits.

No orbit-construction code is imported. Containing the initial vector and
being closed under every generator is sufficient for the exclusion proof;
the producer's construction additionally shows every stored point is reached.
"""
import argparse
from fractions import Fraction
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def matrices(n):
    require(n in (7, 8), 'rank')
    c = [[2 * (i == j) for j in range(n)] for i in range(n)]
    for i, j in [(0, 1), (0, 2), (2, 3), (0, 4)] + [(i, i + 1) for i in range(4, n - 1)]:
        c[i][j] = c[j][i] = -1
    a = [[Fraction(x) for x in row] + [Fraction(i == j) for j in range(n)] for i, row in enumerate(c)]
    det = Fraction(1)
    # Sylvester's criterion: each unpivoted Schur diagonal is positive.
    for k in range(n):
        pivot = a[k][k]
        require(pivot > 0, 'positive definiteness')
        det *= pivot
        a[k] = [x / pivot for x in a[k]]
        for i in range(n):
            if i != k:
                factor = a[i][k]
                a[i] = [x - factor * y for x, y in zip(a[i], a[k])]
    require(det == (2 if n == 7 else 1), 'determinant')
    b = [[x * det for x in row[n:]] for row in a]
    require(all(x.denominator == 1 and x > 0 for row in b for x in row), 'positive integral inverse')
    return c, [[int(x) for x in row] for row in b], int(det)


def verify(path, n, k):
    c, b, d = matrices(n)
    with path.open() as stream:
        header = stream.readline().split()
        require(len(header) == 4 and header[:3] == ['ORBIT', str(n), str(k)], 'header')
        count = int(header[3])
        require(0 < count <= 1000000, 'count range')
        rows = []
        previous = None
        for line in stream:
            v = tuple(map(int, line.split()))
            require(len(v) == n and all(abs(x) <= 30 for x in v), 'vector shape')
            require(previous is None or previous < v, 'strict sorting')
            rows.append(v)
            previous = v
        require(len(rows) == count, 'row count')
    points = set(rows)
    require(tuple(b[i][k] for i in range(n)) in points, 'missing fundamental weight')
    neighbors = [[j for j in range(n) if c[i][j] == -1] for i in range(n)]
    for v in rows:
        require(all(v[i] * v[i] <= b[i][i] * b[k][k] for i in range(n)), 'norm coordinate bound')
        positive = [i for i in range(n) if i != k and v[i] == b[i][k]]
        negative = [i for i in range(n) if i != k and v[i] == -b[i][k]]
        require(not (positive and negative), 'negative triangle')
        for i in range(n):
            # Sparse formula independently derived from the Dynkin tree.
            reflected = v[:i] + (-v[i] + sum(v[j] for j in neighbors[i]),) + v[i + 1:]
            require(reflected in points, 'set not reflection closed')
    return {'rank': n, 'vertex_type': k, 'vectors': count, 'reflection_checks': count * n,
            'negative_triangles': 0, 'determinant': d}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate', type=Path)
    parser.add_argument('rank', type=int)
    parser.add_argument('vertex_type', type=int)
    args = parser.parse_args()
    print(json.dumps(verify(args.certificate, args.rank, args.vertex_type)))
