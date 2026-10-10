#!/usr/bin/env python3
"""Exact finite arithmetic/symbolic checks; not a proof of the sheaf bound."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import math
import sympy as s


def is_prime_trial(n):
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


def factor_trial(n):
    ans = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            ans[p] = ans.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        ans[n] = ans.get(n, 0) + 1
    return ans


rows = []
for e in range(1, 8):
    q = 9**e
    m = q - 1
    while m % 2 == 0:
        m //= 2
    n = (q + 1) // 2
    fm, fn = factor_trial(m), factor_trial(n)
    assert all(is_prime_trial(p) for p in list(fm) + list(fn))
    assert math.prod(p**a for p, a in fm.items()) == m
    assert math.prod(p**a for p, a in fn.items()) == n
    w = (2**len(fm) - 1) * (2**len(fn) - 1)
    margin = (q + 1)**2 - 4 * q * w**2
    assert margin > 0 and math.gcd(m, n) == 1
    assert math.gcd(m*n, 6) == 1 and 16*m*n < q*q
    rows.append(dict(e=e, q=q, m=m, n=n, factor_m=fm, factor_n=fn,
                     mixed_character_weight=w, squared_margin=margin))

small_primes = [p for p in range(5, 64) if is_prime_trial(p)]
assert len(small_primes) == 16
const_left = 2**96
const_right = 13**6 * math.prod(small_primes)
assert const_left < const_right
threshold = 26**6 // 16
assert 26**6 % 16 == 0 and threshold == 19307236
assert 9**8 > threshold

X, lam, tt, kk, y = s.symbols('X lam tt kk y')
mu = (lam - 1)/(lam + 1)
t = lam - 1/lam
tp = mu - 1/mu
assert s.cancel(t*tp + 4) == 0
# The factorization needs tt*tp=2, true in characteristic three.
poly_diff = s.expand((X**2-tt*X-1)*(X**2-2/tt*X-1)
                     -(X**4+(-tt-2/tt)*X**3-(-tt-2/tt)*X+1))
assert poly_diff == 0
assert s.Poly(s.together(t*tp-2).as_numer_denom()[0], lam, modulus=3).is_zero
# For every q0 >=3, q0^6-1 >(q0+1)^4. Positive coefficients after q0=y+3.
order_gap = s.Poly(s.expand((y+3)**6-1-(y+4)**4), y)
assert all(c > 0 for c in order_gap.all_coeffs())

base = Path(__file__).resolve().parent
report = {
    'status': 'PASS',
    'executed_at_utc': datetime.now(timezone.utc).isoformat(),
    'scope': ['Exact trial-division factorizations and positivity for e=1..7',
              'Universal divisor constant and e>=8 threshold',
              'Rational Cayley identity and middle polynomial factorization',
              'Polynomial inequality used in full-square-field lemma'],
    'not_certified': ['The cohomological character-sum theorem',
                      'Uniform group generation and intersection property'],
    'arithmetic_rows': rows,
    'small_primes': small_primes,
    'constant_comparison': {'left': const_left, 'right': const_right},
    'q_threshold': threshold,
    'proper_subfield_gap_coefficients': [int(c) for c in order_gap.all_coeffs()],
    'sympy_version': s.__version__,
    'input_sha256': {
        p.name: sha256(p.read_bytes()).hexdigest()
        for p in [Path(__file__).resolve(), base/'phase12_unitary_parameters.md']
    }
}
out = base/'phase12_unitary_parameters_check.json'
out.write_text(json.dumps(report, indent=2) + '\n')
print('PASS: seven exact arithmetic rows; uniform constant/threshold; three symbolic identities; subfield inequality.')
