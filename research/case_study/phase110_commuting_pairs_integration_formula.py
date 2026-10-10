#!/usr/bin/env python3
"""Optional exact controls; the manuscript proves the uniform statements."""
import argparse
import hashlib
import json
from pathlib import Path

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def geometric(degrees, limit):
    a = [1] + [0] * limit
    for d in degrees:
        for n in range(d, limit + 1):
            a[n] += a[n-d]
    return a

def series(limit):
    s = geometric([1, 1, 1, 2, 2], limit)
    sb = geometric([1, 1], limit)
    a = geometric([1, 2, 2, 2, 4], limit)
    ab = geometric([1, 2], limit)
    return ([s[n]-sb[n]-(sb[n-1] if n else 0) for n in range(limit+1)],
            [a[n]+(a[n-3] if n >= 3 else 0)-ab[n]
             -(ab[n-2] if n >= 2 else 0) for n in range(limit+1)])

def lam(k):
    return (k+2)**2//4

def psi(k, n):
    if k <= n//2:
        return 0
    h = 2*k-n
    return (h*h+2*h)//4 if n % 2 == 0 else (h-1)**2//4+h

def formulas(n):
    twice_s = -3*n+sum(lam(k)*(n-k+2)-psi(k, n) for k in range(1, n+1))
    mu = -2*(n//2)
    d = 0
    for k in range(2, n+1, 2):
        gamma, delta = (k*k+6*k+8)//8, (k*k+2*k)//8
        mu += gamma*((n-k+2)//2)+delta*((n-k+1)//2)
        d += lam(k)-psi(k, n)-1
    need(twice_s % 2 == (mu+d) % 2 == 0, 'Nonintegral formula')
    return twice_s//2, (mu+d)//2

def direct(n):
    s = a = 0
    for t in range(n//2+1):
        for x in range(n+1):
            for y in range(x, n-x-2*t+1):
                for z in range(n-x-y-2*t+1):
                    if not (t > 0 or sum(u > 0 for u in (x, y, z)) >= 2):
                        continue
                    s += 1
                    a += x % 2 == y % 2 == z % 2
    return s, a

def run():
    s, a = series(500)
    for n in range(501):
        need(formulas(n) == (s[n], a[n]), 'Floor/series disagreement at '+str(n))
    for n in range(31):
        need(direct(n) == (s[n], a[n]), 'Direct count disagreement at '+str(n))
    coordinates = 0
    for degree in range(4, 42):
        n = degree//2
        for k in range(1, n+1):
            for l in range(k+1):
                for t in range(l//2+1):
                    for x in range(n-k+1):
                        z, y, f = l-2*t, k-l, degree-2*(x+k)
                        need(min(z,y,f) >= 0 and f+2*(x+y+z)+4*t == degree,
                             'Coordinate inverse failed')
                        need(k == y+z+2*t and l == z+2*t, 'Coordinate forward failed')
                        faithful = t > 0 or sum(u > 0 for u in (x,y,z)) >= 2
                        removed = (x == l == t == 0) or (x == t == 0 and l == k)
                        need(faithful != removed, 'Faithfulness subtraction failed')
                        need((x == y) == (k == x+z+2*t), 'Swap-fixed condition failed')
                        need((k % 2 == 0 and (l+x) % 2 == 0) ==
                             (x % 2 == y % 2 == z % 2), 'Sign condition failed')
                        coordinates += 1
    table = [([1,2,3],0,0),([4,5],3,1),([6],5,1),([7],9,2),([8,9],21,7),
             ([10,11],39,10),([12,13],67,21),([14,15],105,28),([16,17],158,48),
             ([18,19],226,61),([20],315,93),([30],1169,315),([40],3105,855),([50],6774,1795)]
    for degrees, sn, an in table:
        for degree in degrees:
            value = (5,1) if degree == 6 else (s[degree//2],a[degree//2])
            need(value == (sn,an), 'Printed table mismatch')
    return dict(status='PASS',floor_and_series_half_degrees=[0,500],direct_half_degrees=[0,30],
                reversible_coordinates_checked=coordinates,printed_rows=len(table),
                degree_six_values='Supplied by separate complete GAP census, not inferred from coefficients',
                uniform_proof='K(e) and CPI3-CPI9; bounded controls are supplementary',
                program_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    need(not args.output.exists(), 'Refusing existing output')
    report = run()
    with args.output.open('x') as f:
        json.dump(report, f, indent=2)
        f.write('\n')
    print(json.dumps(report))

if __name__ == '__main__':
    main()
