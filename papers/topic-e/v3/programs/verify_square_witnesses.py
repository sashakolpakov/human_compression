"""Independent standard-library verification of primitive square witnesses.

Finite-field arithmetic is implemented directly in polynomial quotients.
No GAP/Sage/SymPy output is assumed correct. A quotient generator of order
p**degree-1 certifies that all its nonzero elements are units, hence that
the quotient is a field. Exact exponent tests certify this order.
"""
from pathlib import Path
import hashlib
import json
from math import gcd
import time


def prime_factors(n):
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


class Quotient:
    def __init__(self, p, modulus):
        assert p > 2 and prime_factors(p) == [p]
        assert modulus[-1] == 1
        self.p, self.modulus = p, modulus
        self.degree = len(modulus) - 1
        self.q = p ** self.degree
        self.zero = (0,) * self.degree
        self.one = self.scalar(1)
        self.x = (0, 1) + (0,) * (self.degree - 2)

    def scalar(self, n):
        return (n % self.p,) + (0,) * (self.degree - 1)

    def add(self, x, y):
        return tuple((a + b) % self.p for a, b in zip(x, y))

    def neg(self, x):
        return tuple(-a % self.p for a in x)

    def sub(self, x, y):
        return self.add(x, self.neg(y))

    def mul(self, x, y):
        n, p = self.degree, self.p
        out = [0] * (2 * n - 1)
        for i, a in enumerate(x):
            for j, b in enumerate(y):
                out[i + j] += a * b
        for k in range(2 * n - 2, n - 1, -1):
            coefficient = out[k] % p
            for j in range(n):
                out[k - n + j] -= coefficient * self.modulus[j]
        return tuple(a % p for a in out[:n])

    def power(self, x, n):
        assert n >= 0
        value = self.one
        while n:
            if n & 1:
                value = self.mul(value, x)
            x = self.mul(x, x)
            n >>= 1
        return value

    def inverse(self, x):
        assert x != self.zero
        value = self.power(x, self.q - 2)
        assert self.mul(x, value) == self.one
        return value

    def primitive(self, x):
        order = self.q - 1
        assert self.power(x, order) == self.one
        for r in prime_factors(order):
            assert self.power(x, order // r) != self.one

    def nonzero_square(self, x):
        assert x != self.zero
        assert self.power(x, (self.q - 1) // 2) == self.one


def polynomial_mul(F, a, b):
    result = [F.zero] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i+j] = F.add(result[i+j], F.mul(x, y))
    return result


def norm_quartic(F, j):
    u = F.add(j, F.inverse(j))
    polynomial = [F.one]
    for i in range(F.degree):
        ui = F.power(u, F.p ** i)
        c = F.mul(ui, ui)
        edge = F.sub(c, F.scalar(4))
        middle = F.neg(F.add(F.mul(F.scalar(2), c), F.scalar(8)))
        polynomial = polynomial_mul(F, polynomial,
                                    [edge, F.zero, middle, F.zero, edge])
    assert all(all(c == 0 for c in coefficient[1:]) for coefficient in polynomial)
    return [coefficient[0] for coefficient in polynomial]


def evaluate(F, coefficients, x):
    result = F.zero
    for c in reversed(coefficients):
        result = F.add(F.mul(result, x), F.scalar(c))
    return result


def check_coprime(record):
    p, a, b = record['p'], record['a'], record['b']
    assert 1 < a < b and a % 2 == b % 2 == 1 and gcd(a, b) == 1
    A = Quotient(p, record['j1_minpoly'])
    B = Quotient(p, record['j2_minpoly'])
    assert (A.degree, B.degree) == (a, b)
    A.primitive(A.x)
    B.primitive(B.x)
    polynomial = norm_quartic(A, A.x)
    assert polynomial == record['normpoly']
    value = evaluate(B, polynomial, B.x)
    B.nonzero_square(value)
    return {'kind': 'coprime', 'p': p, 'a': a, 'b': b,
            'norm_value_coefficients': value, 'passed': True}


def check_nested(record):
    p, e = record['p'], record['e']
    assert e > 1 and e % 2 == 1
    F = Quotient(p, record['j1_minpoly'])
    assert F.degree == e
    F.primitive(F.x)
    j1 = F.power(F.x, record['j1_exponent'])
    j2 = F.power(F.x, record['j2_exponent'])
    F.primitive(j1)
    F.primitive(j2)
    u = F.add(j1, F.inverse(j1))
    v = F.add(j2, F.inverse(j2))
    u2, v2 = F.mul(u, u), F.mul(v, v)
    omega = F.sub(F.mul(u2, v2), F.mul(F.scalar(4), F.add(u2, v2)))
    F.nonzero_square(omega)
    return {'kind': 'nested', 'p': p, 'e': e,
            'omega_coefficients': omega, 'passed': True}


def main():
    root = Path(__file__).resolve().parent
    data_path = root / 'psl2_square_witnesses.json'
    data = json.loads(data_path.read_text())
    expected_coprime = {(3, 3, 5), (5, 3, 5), (3, 3, 7),
                        (3, 5, 7), (3, 5, 9), (3, 7, 9)}
    expected_nested = {(3, 3), (3, 5), (5, 3), (7, 3), (11, 3)}
    assert {(r['p'], r['a'], r['b']) for r in data if r['kind'] == 'coprime'} == expected_coprime
    assert {(r['p'], r['e']) for r in data if r['kind'] == 'nested'} == expected_nested
    started = time.monotonic()
    results = [check_coprime(r) if r['kind'] == 'coprime' else check_nested(r)
               for r in data]
    assert len(results) == 11
    report = {'verifier_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'data_sha256': hashlib.sha256(data_path.read_bytes()).hexdigest(),
              'elapsed_seconds': time.monotonic() - started, 'results': results,
              'all_passed': True}
    (root / 'psl2_square_witnesses_independent.json').write_text(
        json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
