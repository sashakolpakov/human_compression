"""Independent exact verification of every finite unitary parameter witness.

Standard-library polynomial arithmetic; does not import the author's GAP
code, finite-field implementation, or sieve checker. It independently
reconstructs the finite field list and all sieve decisions. The written
curve, character-sum, generation and intersection proofs remain inputs.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import permutations
import json
from math import isqrt, prod
from pathlib import Path


def factors(n):
    result = []
    trial = 2
    while trial * trial <= n:
        if n % trial == 0:
            result.append(trial)
            while n % trial == 0:
                n //= trial
        trial += 1 if trial == 2 else 2
    if n > 1:
        result.append(n)
    return result


def prime(p):
    return p >= 2 and all(p % d for d in range(2, isqrt(p) + 1))


def trim(a):
    while a and a[-1] == 0:
        a.pop()
    return a


def remainder(a, b, p):
    a, b = trim(list(a)), trim(list(b))
    assert b
    leading_inverse = pow(b[-1], -1, p)
    while len(a) >= len(b):
        coefficient = a[-1] * leading_inverse % p
        shift = len(a) - len(b)
        for i, x in enumerate(b):
            a[i + shift] = (a[i + shift] - coefficient * x) % p
        trim(a)
    return a


def gcd(a, b, p):
    while b:
        a, b = b, remainder(a, b, p)
    if not a:
        return []
    scale = pow(a[-1], -1, p)
    return [(x * scale) % p for x in a]


class Quotient:
    def __init__(self, p, modulus):
        assert prime(p) and modulus[-1] == 1
        assert all(type(x) is int and 0 <= x < p for x in modulus)
        self.p, self.modulus, self.n = p, modulus, len(modulus) - 1
        self.zero = (0,) * self.n
        self.one = (1,) + (0,) * (self.n - 1)

    def element(self, a):
        assert len(a) == self.n and all(type(x) is int and 0 <= x < self.p for x in a)
        return tuple(a)

    def add(self, a, b):
        return tuple((x + y) % self.p for x, y in zip(a, b))

    def neg(self, a):
        return tuple(-x % self.p for x in a)

    def sub(self, a, b):
        return self.add(a, self.neg(b))

    def mul(self, a, b):
        product = [0] * (2 * self.n - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    product[i + j] += x * y
        for i in range(len(product) - 1, self.n - 1, -1):
            leading = product[i] % self.p
            if leading:
                for j in range(self.n):
                    product[i - self.n + j] -= leading * self.modulus[j]
        return tuple(x % self.p for x in product[:self.n])

    def power(self, a, exponent):
        result = self.one
        while exponent:
            if exponent & 1:
                result = self.mul(result, a)
            a = self.mul(a, a)
            exponent //= 2
        return result

    def irreducible(self):
        # Rabin criterion: f divides X^(p^n)-X, with coprime tests for
        # every prime divisor of n. Polynomial gcd is computed separately.
        generator = (0, 1) + (0,) * (self.n - 2)
        frobenius = [generator]
        for _ in range(self.n):
            frobenius.append(self.power(frobenius[-1], self.p))
        assert frobenius[-1] == generator
        for divisor in factors(self.n):
            difference = list(self.sub(frobenius[self.n // divisor], generator))
            assert gcd(self.modulus, trim(difference), self.p) == [1]

    def inverse(self, a):
        assert a != self.zero
        result = self.power(a, self.p ** self.n - 2)
        assert self.mul(a, result) == self.one
        return result

    def divide(self, a, b):
        return self.mul(a, self.inverse(b))

    def exact_order(self, a, order):
        assert a != self.zero and self.power(a, order) == self.one
        for divisor in factors(order):
            assert self.power(a, order // divisor) != self.one

    def identity(self):
        return tuple(tuple(self.one if i == j else self.zero for j in range(4)) for i in range(4))

    def matrix_mul(self, a, b):
        result = []
        for i in range(4):
            row = []
            for j in range(4):
                value = self.zero
                for k in range(4):
                    if a[i][k] != self.zero and b[k][j] != self.zero:
                        value = self.add(value, self.mul(a[i][k], b[k][j]))
                row.append(value)
            result.append(tuple(row))
        return tuple(result)

    def matrix_power(self, a, exponent):
        result = self.identity()
        while exponent:
            if exponent & 1:
                result = self.matrix_mul(result, a)
            a = self.matrix_mul(a, a)
            exponent //= 2
        return result

    def scalar(self, a):
        return all(a[i][j] == (a[0][0] if i == j else self.zero)
                   for i in range(4) for j in range(4))

    def determinant(self, a):
        answer = self.zero
        for perm in permutations(range(4)):
            term = self.one
            for i in range(4):
                term = self.mul(term, a[i][perm[i]])
            inversions = sum(perm[i] > perm[j] for i in range(4) for j in range(i + 1, 4))
            answer = self.sub(answer, term) if inversions % 2 else self.add(answer, term)
        return answer


def verify_record(record):
    q, p, e = (record[k] for k in ('q', 'p', 'exponent'))
    assert prime(p) and p >= 5 and type(e) is int and e >= 1
    assert q == p ** e and q % 4 == 1
    field = Quotient(p, record['modulus_low_to_high'])
    assert field.n == 2 * e
    field.irreducible()
    zero, one = field.zero, field.one
    minus = field.neg(one)
    two = field.add(one, one)
    delta, x, y, k, i = [field.element(record[key]) for key in ('delta', 'x', 'y', 'k', 'i')]
    assert delta != zero and field.power(delta, q) == field.neg(delta)
    assert k != zero and field.power(k, q) == field.neg(k)
    assert field.power(i, q) == i and field.mul(i, i) == minus
    k2 = field.mul(k, k)
    assert field.power(k2, q) == k2
    for r in factors(e):
        assert field.power(k2, p ** (e // r)) != k2
    if record['branch'] == 'elliptic_primitive_pair':
        assert q > 5 and x != zero and y != zero
        assert field.power(x, q) == x and field.power(y, q) == y
        d = field.mul(delta, delta)
        assert field.power(d, (q - 1) // 2) == minus
        dx2 = field.mul(d, field.mul(x, x))
        field.exact_order(dx2, q - 1)
        curve = field.sub(field.add(field.mul(field.mul(d, x), field.mul(y, y)),
                                   field.mul(two, field.mul(dx2, y))),
                          field.add(x, field.mul(two, y)))
        assert curve == zero
        lam = field.mul(delta, x)
        dy = field.mul(delta, y)
        mu = field.divide(field.sub(dy, one), field.add(dy, one))
        assert field.power(mu, q + 1) == one
        field.exact_order(field.mul(mu, mu), (q + 1) // 2)
        t = field.sub(lam, field.inverse(lam))
        tp = field.sub(mu, field.inverse(mu))
        assert field.mul(t, tp) == two
        assert k == field.neg(field.add(t, tp))
        expected_order = q * q - 1
    else:
        assert record['branch'] == 'retained_q5_plus' and q == 5
        expected_order = 26

    r1 = ((one,zero,zero,zero),(zero,zero,zero,one),
          (zero,zero,minus,zero),(zero,one,zero,zero))
    r2 = ((zero,i,zero,zero),(i,zero,zero,zero),
          (zero,zero,k,field.sub(i,k)),(zero,zero,field.add(i,k),field.neg(k)))
    matrix = field.matrix_mul(r1, r2)
    h = tuple(tuple((one if row % 2 == 0 else minus) if row == col else zero
                    for col in range(4)) for row in range(4))
    adjoint = tuple(tuple(field.power(matrix[col][row], q) for col in range(4)) for row in range(4))
    assert field.matrix_mul(field.matrix_mul(matrix, h), adjoint) == h
    assert field.determinant(matrix) == one
    assert expected_order == record['projective_middle_order']
    assert factors(expected_order) == record['order_prime_divisors']
    final_power = field.matrix_power(matrix, expected_order)
    assert field.scalar(final_power)
    for r in factors(expected_order):
        assert not field.scalar(field.matrix_power(matrix, expected_order // r))
    return {'q': q, 'p': p, 'exponent': e, 'polynomial_degree': field.n,
            'irreducible': True, 'full_square_field': True,
            'special_unitary': True, 'projective_order': expected_order,
            'matrix_order_power_is_identity': final_power == field.identity()}


def sieve_coefficient(primes, core_size):
    remaining = primes[core_size:]
    if not remaining:
        return Fraction(8 * 2 ** core_size - 6)
    delta = Fraction(1) - sum((Fraction(1, p) for p in remaining), Fraction(0))
    if delta <= 0:
        return None
    return 8 * 2 ** core_size * (2 + Fraction(len(remaining) - 1) / delta) - 6


def complete_arithmetic():
    cutoff = 98660
    # Trial primality and trial factorization, independent of the author's
    # Eratosthenes/smallest-prime-factor implementation.
    primes = [p for p in range(5, cutoff) if prime(p)]
    fields = {}
    for p in primes:
        e, q = 1, p
        while q < cutoff:
            if q % 4 == 1:
                assert q not in fields
                fields[q] = (p, e)
            e, q = e + 1, q * p
    uncovered = []
    for q in sorted(fields):
        support = sorted(set(factors(q - 1) + factors(q + 1)) - {2})
        valid = False
        for c in range(len(support) + 1):
            coefficient = sieve_coefficient(support, c)
            if coefficient is not None and Fraction((q - 3) ** 2) > q * coefficient ** 2:
                valid = True
                break
        if not valid:
            uncovered.append(q)
    odd_primes = [3] + primes
    previous = 3715232694272
    rows = []
    for w, c, new in [(17,2,2135383),(10,1,255289),(9,1,160372),(8,1,98660)]:
        assert 8 * prod(odd_primes[:w + 1]) >= previous ** 2
        a = sieve_coefficient(odd_primes[:w], c)
        threshold = (a + 1) ** 2
        assert a > 2 and new - 1 < threshold <= new
        rows.append({'previous': previous, 'omega_max': w, 'core_size': c, 'cutoff': new})
        previous = new
    assert len(fields) == 4795 and len(uncovered) == 406 and max(uncovered) == 43889
    return fields, uncovered, rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--witnesses', type=Path, default=Path(__file__).with_name('phase13_unitary_witnesses.json'))
    parser.add_argument('--output', type=Path, default=Path(__file__).with_suffix('.json'))
    args = parser.parse_args()
    witness_bytes = args.witnesses.read_bytes()
    data = json.loads(witness_bytes)
    fields, exceptions, bootstraps = complete_arithmetic()
    witnesses = data['witnesses']
    assert [w['q'] for w in witnesses] == exceptions
    assert len(witnesses) == data['input_fields'] == 406
    results = []
    for witness in witnesses:
        assert (witness['p'], witness['exponent']) == fields[witness['q']]
        results.append(verify_record(witness))
    report = {
        'status': 'PASS', 'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'witness_file': args.witnesses.name, 'witness_sha256': sha256(witness_bytes).hexdigest(),
        'arithmetic': {'eligible_fields': len(fields), 'exceptions': exceptions, 'bootstraps': bootstraps},
        'results': results,
        'scope': 'Independent complete finite-range arithmetic and all 406 explicit polynomial-field witnesses, including irreducibility and exact projective matrix order.',
        'retained_written_inputs': ['Smooth elliptic curve and character-sum/sieve theorems',
                                    'Uniform matrix generation and intersection proofs',
                                    'Characteristic-three family and maximum-rank upper bound'],
        'not_claimed': ['External peer review or priority', 'Lean formalization', 'Rank-four existence for q=3 mod4'],
    }
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: independently reconstructed 4795 fields, 406 exceptions, all polynomial/field/matrix witnesses.')


if __name__ == '__main__':
    main()
