"""Involution lower bounds from explicit class centralizer orders.

The retained classification input is Burness--Thomas, arXiv:1707.03562,
Proposition 2.3, Remark 2.2 and Table 5.  This file proves the arithmetic
consequences, not that classification.  Every selected class is in the
simple group; its inner-diagonal class is the same class.
"""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
from fractions import Fraction
from math import comb
from pathlib import Path
import json


def add(a, b):
    c = [0] * max(len(a), len(b))
    for i, x in enumerate(a):
        c[i] += x
    for i, x in enumerate(b):
        c[i] += x
    while len(c) > 1 and c[-1] == 0:
        c.pop()
    return c


def scale(a, x):
    return [x * v for v in a]


def mul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return c


def mon(n):
    return [0] * n + [1]


def fact(n, sign=1):
    return add(mon(n), [-sign])


def product(terms):
    result = [1]
    for term in terms:
        result = mul(result, term)
    return result


def sl(n, eps=1, field_power=1):
    return product([mon(field_power * n * (n - 1) // 2)] +
                   [fact(field_power * i, eps ** i) for i in range(2, n + 1)])


def sp(m):
    """Order of Sp(2m,q)."""
    return product([mon(m * m)] + [fact(2 * i) for i in range(1, m + 1)])


def so_plus(m):
    """Order of SO+(2m,q) for odd q."""
    return product([mon(m * (m - 1)), fact(m)] +
                   [fact(2 * i) for i in range(1, m)])


orders = {
    'E8': product([mon(120)] + [fact(i) for i in [2, 8, 12, 14, 18, 20, 24, 30]]),
    'E7': product([mon(63)] + [fact(i) for i in [2, 6, 8, 10, 12, 14, 18]]),
    'E6+': product([mon(36)] + [fact(i) for i in [2, 5, 6, 8, 9, 12]]),
    'E6-': product([mon(36)] + [fact(i, (-1) ** i) for i in [2, 5, 6, 8, 9, 12]]),
    'F4': product([mon(24)] + [fact(i) for i in [2, 6, 8, 12]]),
    'G2': product([mon(6), fact(2), fact(6)]),
    '3D4': product([mon(12), add(add(mon(8), mon(4)), [1]), fact(6), fact(2)]),
    '2F4': product([mon(12), fact(6, -1), fact(4), fact(3, -1), fact(1)]),
    '2G2': product([mon(3), fact(3, -1), fact(1)]),
    '2B2': product([mon(2), fact(2, -1), fact(1)]),
}


def verify(name, family, cls, centralizer, exponent, denominator, minimum, condition):
    # |J:C_J(t)| > q^exponent/denominator iff this polynomial is positive.
    delta = add(scale(orders[family], denominator), scale(mul(mon(exponent), centralizer), -1))
    shifted = [sum(delta[i] * comb(i, j) * minimum ** (i - j)
                   for i in range(j, len(delta))) for j in range(len(delta))]
    if shifted[0] <= 0 or any(x < 0 for x in shifted):
        raise ValueError((name, shifted[0], [i for i, x in enumerate(shifted) if x < 0]))
    return dict(name=name, family=family, selected_class=cls,
                condition=condition, minimum=minimum,
                group_order=orders[family], centralizer_order=centralizer,
                lower_exponent=exponent, lower_denominator=denominator,
                difference=delta, shifted_coefficients=shifted)


def main():
    rows = []
    def v(name, family, cls, centralizer, exponent, denominator, minimum, condition):
        rows.append(verify(name, family, cls, centralizer, exponent, denominator, minimum, condition))
    v('E8 odd', 'E8', 't1', so_plus(8), 128, 2, 3, 'q odd')
    v('E8 even', 'E8', 'A1^4', mul(mon(84), sp(4)), 128, 2, 2, 'q even')
    for eps in (1, -1):
        v('E7 odd epsilon='+str(eps), 'E7', 't4' if eps == 1 else "t4 prime",
          scale(sl(8, eps), 2), 70, 4, 3, 'q odd, q=epsilon modulo 4')
    v('E7 even', 'E7', 'A1^4', mul(mon(42), sp(3)), 70, 4, 2, 'q even')
    for eps in (1, -1):
        family = 'E6+' if eps == 1 else 'E6-'
        v(family+' odd', family, 't2', mul(sl(2), sl(6, eps)), 40, 2, 3, 'q odd')
        v(family+' even', family, 'A1^3', product([mon(27), sl(2), sl(3, eps)]),
          40, 2, 2, 'q even')
    v('F4 odd', 'F4', 't1', mul(sl(2), sp(3)), 28, 2, 3, 'q odd')
    v('F4 even', 'F4', 'A1 A1tilde', product([mon(18), sl(2), sl(2)]), 28, 2, 2, 'q even')
    v('G2 odd', 'G2', 't1', mul(sl(2), sl(2)), 8, 2, 3, 'q odd')
    v('G2 even', 'G2', 'A1tilde', mul(mon(3), sl(2)), 8, 2, 4, 'q even, q>2')
    v('3D4 odd', '3D4', 't2', mul(sl(2), sl(2, field_power=3)), 16, 2, 3, 'q odd')
    v('3D4 even', '3D4', 'A1^3', mul(mon(9), sl(2)), 16, 2, 2, 'q even')
    v('2F4', '2F4', 'A1 A1tilde', mul(mon(9), sl(2)), 14, 2, 8, 'q=2^(2a+1), a>=1')
    v('2G2', '2G2', 't1', sl(2), 4, 2, 27, 'q=3^(2a+1), a>=1')
    v('2B2', '2B2', 'A1tilde^2', mon(2), 3, 2, 8, 'q=2^(2a+1), a>=1')
    report = dict(status='PASS_ARITHMETIC_FROM_EXPLICIT_CLASS_ORDERS', rows=rows,
                  retained_input='Burness--Thomas Proposition2.3, Remark2.2, Table5 and standard group orders',
                  proof='All coefficients after q=z+minimum are nonnegative; the constant is positive. The chosen class is a subset of the involutions.',
                  whole_original_credit=0)
    Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2)+'\n')
    print('PASS', len(rows), 'explicit centralizer cases')


if __name__ == '__main__':
    main()
