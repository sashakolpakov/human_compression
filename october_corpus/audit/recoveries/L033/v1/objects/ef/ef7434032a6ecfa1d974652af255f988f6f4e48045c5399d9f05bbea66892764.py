"""Exact central antipodes in faithful Coxeter representations.

Arithmetic is in Z[phi], represented by (a,b), phi^2=phi+1.
The integral cases use b=0 throughout.
"""
import json
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


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
