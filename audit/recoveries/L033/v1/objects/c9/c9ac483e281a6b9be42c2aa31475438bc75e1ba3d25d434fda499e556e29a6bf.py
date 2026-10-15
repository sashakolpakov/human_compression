"""Exact central antipodes in faithful Coxeter representations.

Arithmetic is in Z[phi], represented by (a,b), phi^2=phi+1.
The integral cases use b=0 throughout.
"""
import json
from fractions import Fraction
from verify_weights import matrices, require


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def neg(x):
    return -x[0], -x[1]


def mul(x, y):
    a, b = x
    c, d = y
    return a * c + b * d, a * d + b * c + b * d


def identity(n):
    return [[(int(i == j), 0) for j in range(n)] for i in range(n)]


def product(a, b):
    n = len(a)
    result = [[(0, 0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] = add(result[i][j], mul(a[i][k], b[k][j]))
    return result


def verify():
    cases = []
    for n, power in [(7, 9), (8, 15)]:
        c, _, _ = matrices(n)
        cases.append(('E' + str(n), [[(x, 0) for x in row] for row in c], power))
    f = [[(2 * int(i == j), 0) for j in range(4)] for i in range(4)]
    for i in range(3):
        f[i][i + 1] = f[i + 1][i] = (-1, 0)
    f[1][2] = (-2, 0)
    cases.append(('F4', f, 6))
    for n, power in [(3, 5), (4, 15)]:
        c = [[(2 * int(i == j), 0) for j in range(n)] for i in range(n)]
        for i in range(n - 1):
            c[i][i + 1] = c[i + 1][i] = (0, -1) if i == 0 else (-1, 0)
        cases.append(('H' + str(n), c, power))
    answer = []
    for name, c, power in cases:
        n = len(c)
        w = identity(n)
        for i in range(n):
            s = identity(n)
            s[i] = [add(s[i][j], neg(c[i][j])) for j in range(n)]
            require(product(s, s) == identity(n), 'reflection square')
            w = product(w, s)
        result = identity(n)
        for _ in range(power):
            result = product(result, w)
        expected = [[(-int(i == j), 0) for j in range(n)] for i in range(n)]
        require(result == expected, 'central antipode ' + name)
        answer.append({'type': name, 'power': power, 'coxeter_element': w, 'power_matrix': result})
    return answer


def verify_e6():
    # Arms of lengths 1,2,2. Removing vertex3 leaves the D5 diagram.
    n = 6
    c = [[2 * int(i == j) for j in range(n)] for i in range(n)]
    for i, j in [(0, 1), (0, 2), (2, 3), (0, 4), (4, 5)]:
        c[i][j] = c[j][i] = -1
    a = [[Fraction(x) for x in row] + [Fraction(i == j) for j in range(n)] for i, row in enumerate(c)]
    determinant = Fraction(1)
    for k in range(n):
        pivot = a[k][k]
        require(pivot > 0, 'E6 positive Cartan matrix')
        determinant *= pivot
        a[k] = [x / pivot for x in a[k]]
        for i in range(n):
            if i != k:
                q = a[i][k]
                a[i] = [x - q * y for x, y in zip(a[i], a[k])]
    require(determinant == 3, 'E6 determinant')
    initial = tuple(3 * a[i][n + 3] for i in range(n))
    require(all(x.denominator == 1 for x in initial), 'E6 integral weight')
    initial = tuple(map(int, initial))
    seen = {initial}
    queue = [initial]
    for v in queue:
        for i in range(n):
            image = list(v)
            image[i] -= sum(c[i][j] * v[j] for j in range(n))
            image = tuple(image)
            if image not in seen:
                seen.add(image)
                queue.append(image)
        require(len(queue) <= 1000, 'E6 finite bound')
    require(len(seen) == 27, 'E6 orbit size')
    # A second direct closure check on the exported set.
    for v in seen:
        for i in range(n):
            coordinate = -v[i] + sum(v[j] for j in range(n) if c[i][j] == -1)
            require(v[:i] + (coordinate,) + v[i + 1:] in seen, 'E6 exported closure')
    return {'cartan': c, 'determinant': 3, 'weight_type': 3,
            'initial_scaled_weight': initial, 'orbit': sorted(seen), 'orbit_size': 27,
            'stabilizer_type': 'D5', 'stabilizer_order': 1920, 'group_order': 51840,
            'source_table_entry': '12 times 6 factorial', 'source_entry_value': 8640,
            'corrected_entry': '72 times 6 factorial'}


if __name__ == '__main__':
    print(json.dumps({'antipodes': verify(), 'E6_order': verify_e6()}, indent=2))
