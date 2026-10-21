#!/usr/bin/env python3
"""Optional finite diagnostics only; the uniform analytic proof is written."""
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import product
from math import factorial


def require(value, message):
    if not value:
        raise ValueError(message)


def run():
    differences = Counter(i-j for i in range(4) for j in range(4))
    require([differences[j] for j in range(4)] == [4, 3, 2, 1],
            'exact Fourier coefficients')
    matrices = []
    for n1, n2, m1, m2 in product([2, 3], [2, 3], range(4), range(2)):
        det = n1*n2-m1*m2
        require(det >= 1, 'canonical determinant')
        widths = (Fraction(n2+m1, det), Fraction(n1+m2, det))
        require(max(widths) <= 6, 'bounded inverse projection widths')
        matrices.append([n1, n2, m1, m2, det])
    # Actual exponent vectors, not a Boolean list of desired assertions.
    vectors = [v for v in product(range(4), repeat=4) if max(v) >= 2]
    pairs = same = distinct = 0
    for u in vectors:
        q1 = max(j for j, v in enumerate(u) if v >= 2)
        for v in vectors:
            q2 = max(j for j, w in enumerate(v) if w >= 2)
            if q1 == q2:
                same += 1
            else:
                a, b, i, j = (u, v, q1, q2) if q1 > q2 else (v, u, q2, q1)
                require(b[i] <= 1, 'largest-prime cross exponent')
                require(a[i]*b[j]-a[j]*b[i] >= 1, 'actual pair determinant')
                distinct += 1
            pairs += 1
    # Without the largest-prime rule, different assigned primes need not
    # give independent constraints: both divisors may have exponent vector (2,2).
    require(2*2-2*2 == 0, 'unrestricted assignment countermodel')
    for exponent, target in [(Fraction(5, 2), 12), (Fraction(14, 5), 16)]:
        require(sum(exponent**j/factorial(j) for j in range(9)) > target,
                'rational exponential-series logarithm bound')
    require(Fraction(49,25)-Fraction(103,120)-Fraction(21,20) == Fraction(31,600),
            'exact rational saving margin')
    with localcontext() as ctx:
        ctx.prec = 65
        D = Decimal
        eps, c, kappa = D(1)/100, D(49)/50, D(21)/20
        a1 = (1+eps)*D(12).ln()-D(5)/3
        a2 = (1+eps)*D(16).ln()-2
        margin = 2*c-max(a1, a2)-kappa
        require(margin > D('.0669'), 'strict final logarithmic margin')
        require((1+eps)*D(4).ln() < 2, 'divisor bound L squared')
        require(D(1)/(2*(1+eps)) > D(1)/5, 'smooth-part separation slopes')
        require(2*D('.9')-max(a1, a2) < 1,
                'source c=.9 cannot be transplanted into the repaired proof')
        constants = dict(alpha1=str(a1), alpha2=str(a2),
                         saving=str(2*c-max(a1, a2)),
                         margin_above_21_over_20=str(margin))
    return {'role': 'OPTIONAL_VALIDATION_NOT_A_MATHEMATICAL_PREMISE',
            'fourier_nonnegative_coefficients': [4, 3, 2, 1],
            'allowed_matrices': len(matrices), 'minimum_determinant': min(r[-1] for r in matrices),
            'actual_exponent_pairs': pairs, 'same_assignment': same,
            'different_assignment': distinct,
            'unrestricted_assignment_countermodel': [[2, 2], [2, 2]],
            'rational_margin_above_21_over_20': '31/600',
            'constants': constants,
            'limitations': 'No finite sample certifies asymptotic prime estimates or density. No Mondrian partition is searched.'}


if __name__ == '__main__':
    import json
    print(json.dumps(run(), indent=2))
