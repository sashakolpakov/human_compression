from pathlib import Path
import hashlib
import json
import math
import sys

if sys.flags.optimize:
    raise RuntimeError('normal Python required')

def partitions(n, lo=1):
    if n == 0:
        yield ()
    for a in range(lo, n + 1):
        for rest in partitions(n - a, a):
            yield (a,) + rest

cycle_counts = {}
for n in range(7, 11):
    ps = list(partitions(n))
    assert all(math.lcm(*p) != 63 for p in ps)
    cycle_counts[n] = len(ps)

def orbit(a, m):
    r = []
    while a not in r:
        r.append(a)
        a = 2 * a % m
    return r

orbits = {m: orbit(1, m) for m in [3, 7, 21]}
assert orbits == {3: [1, 2], 7: [1, 2, 4], 21: [1, 2, 4, 8, 16, 11]}
assert 6 not in orbits[7] and 20 not in orbits[21]
assert 336 % 9 != 0 and 3 * 8**2 * 65 * 7 == 87360
assert 87360 % 9 != 0
assert 20 % 15 == 5 and -25 % 15 == 5
assert (7*4-7) % 21 == 0 and (7*16-7) % 21 == 0
assert 7*9 == 63 and math.gcd(7, 9) == 1

p = Path(__file__)
report = dict(status='PASS', scope='arithmetic only; no group enumeration',
              cycle_partitions=cycle_counts, frobenius_orbits=orbits,
              source_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
p.with_name('arithmetic_report.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report))
