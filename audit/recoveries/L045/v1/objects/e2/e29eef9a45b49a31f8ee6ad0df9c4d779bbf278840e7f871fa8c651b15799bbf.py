"""Bounded integer controls, not a substitute for the uniform written proof."""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
import json
import math

def need(value, message):
    if not value:
        raise ValueError(message)

def factor(n):
    result = {}
    d = 2
    while d*d <= n:
        while n % d == 0:
            result[d] = result.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        result[n] = result.get(n, 0) + 1
    return result

def order(a, m):
    need(math.gcd(a,m) == 1, 'unit for multiplicative order')
    v = a % m
    n = 1
    while v != 1:
        v = v*a % m
        n += 1
    return n

def partitions(n, low=1):
    if n == 0:
        yield ()
    for a in range(low, n+1):
        for tail in partitions(n-a, a):
            yield (a,) + tail

def calculate():
    rows = []
    exclusions = 0
    for q in range(4,258):
        fac = factor(q)
        if len(fac) != 1:
            continue
        p,f = next(iter(fac.items()))
        d = math.gcd(2,q-1)
        A, B = q**3+1, q+1
        primitive = math.prod(r**a for r,a in factor(q*q-q+1).items()
                              if order(p,r) == 6*f)
        need(primitive > 1 and (A//d) % primitive == 0, 'primitive part in projective order')
        for r in factor(primitive):
            need(r >= 6*f+1 and order(q,r) == 6, 'absolute and relative primitive order')
        low_factors = 6*math.prod(q**j-1 for j in range(1,5))
        need(math.gcd(primitive,low_factors) == 1, 'all small-exponent rows')
        exclusions += 1
        need(A//math.gcd(2,A) > q*q-1, 'six-space degree lower bound')
        need((q**3-1) % (A//math.gcd(2,A)) != 0, 'six-space not cubic')
        need(B//math.gcd(2,B) > 2, 'two-space degree')
        if q % 3 == 2:
            need((A//(3*d))*3 == A//d, 'cube order')
            torus = (q*q-q+1)//3
            need(A//(3*d) == torus*(B//d) and B//d > 1, 'unitary three-space exclusion')
            exclusions += 1
        for a in range(1,f):
            if f % a:
                continue
            q0 = p**a
            plus = q0**12*(q0**4-1)**2*(q0**2-1)*(q0**6-1)*4
            need(math.gcd(primitive,plus) == 1, 'plus subfield exclusion')
            exclusions += 1
            if f == 2*a:
                minus = q0**12*(q0**4+1)*(q0**2-1)*(q0**4-1)*(q0**6-1)*4
                need(math.gcd(primitive,minus) == 1, 'minus subfield exclusion')
                exclusions += 1
            if f == 3*a:
                triality = q0**12*(q0**8+q0**4+1)*(q0**6-1)*(q0**2-1)*4
                need(math.gcd(primitive,triality) == 1, 'triality subfield exclusion')
                exclusions += 1
        if f == 1:
            need(primitive == (p*p-p+1)//math.gcd(3,p+1), 'prime-field primitive part formula')
            if p >= 7:
                need(primitive > 7, 'bounded quotient exclusion')
        rows.append(dict(q=q,p=p,f=f,primitive_part=primitive,projective_order=A//d))
    cycle_counts = {}
    for n in (8,10):
        ps = list(partitions(n))
        need(all(math.lcm(*x) != 63 for x in ps), 'permutation order 63 exclusion')
        cycle_counts[str(n)] = len(ps)
    frobenius = {}
    for m in (7,9,21,63):
        orbit = [pow(2,i,m) for i in range(order(2,m))]
        frobenius[str(m)] = orbit
    need(len(frobenius['9']) == 6 and len(frobenius['63']) == 6, 'six-dimensional constituents')
    need(6 not in frobenius['7'] and 62 not in frobenius['63'], 'distinct dual constituents')
    return dict(status='PASS_D4_ARITHMETIC', prime_power_rows=rows, exclusion_checks=exclusions,
                cycle_partitions=cycle_counts, frobenius_orbits=frobenius,
                scope='finite controls of the written uniform proof; no subgroup classification recomputed')

def validate(value):
    need(value == calculate(), 'exact complete arithmetic certificate')
    return len(value['prime_power_rows'])

if __name__ == '__main__':
    print(json.dumps(calculate(), sort_keys=True))
