"""Independent literal S5/A5 control and integer recomputation of all bounds."""
import sys
if sys.flags.optimize:
    raise RuntimeError('normal Python required')
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


D = Path(__file__).resolve().parent
S = D.parents[1]
P = S/'corpus106_L045_sporadic_counting_v1'
data = json.loads((P/'data.json').read_text())
tables = {t[0]: t for t in data[3]}
def count(t, order):
    return sum(s for d, s in zip(t[3], t[4]) if d == order)
arithmetic = []
for row in data[4]:
    gn, an, cl, prime = row[:4]
    g, a = tables[gn], tables[an]
    terms = [Fraction(g[5][cl-1]*count(tables[name], prime)*count(tables[name], 2), tables[name][2]) for name in g[7]]
    B = sum(terms, Fraction(0))
    mu = max(count(tables[name], 2) for name in a[7] if gn == an or tables[name][1] != g[1])
    idx = row[5][cl-1]-1
    R = a[5][idx]*mu if a[6][idx] == idx+1 else 0
    i2 = count(g, 2)
    need(B == Fraction(*row[9]) and mu == row[10] and R == row[11] and i2 == row[12], 'independent literal arithmetic')
    need((i2-R)*B.denominator > B.numerator, 'cross-multiplied strict inequality')
    arithmetic.append(dict(group=gn, maximal_classes=len(g[7]), B=[B.numerator, B.denominator], R=R, margin=[(i2-B-R).numerator, (i2-B-R).denominator]))

perms = list(itertools.permutations(range(5)))
index = {p: i for i, p in enumerate(perms)}
mul = [[index[tuple(b[a[i]] for i in range(5))] for b in perms] for a in perms]
e = index[tuple(range(5))]
inverse = [next(j for j in range(120) if mul[i][j] == e) for i in range(120)]
orders = []
for x in range(120):
    y, order = x, 1
    while y != e:
        y, order = mul[y][x], order+1
    orders.append(order)
A = frozenset(range(120))
G = frozenset(i for i, p in enumerate(perms) if sum(p[j] > p[k] for j in range(5) for k in range(j+1, 5)) % 2 == 0)
def close(gens):
    result, queue = {e}, [e]
    for y in queue:
        for x in gens:
            z = mul[y][x]
            if z not in result:
                result.add(z)
                queue.append(z)
    return frozenset(result)
def subgroups(group):
    first = frozenset([e])
    seen, queue = {first}, [(first, ())]
    for H, gens in queue:
        for x in group-H:
            K = close(gens+(x,))
            if K not in seen:
                seen.add(K)
                queue.append((K, gens+(x,)))
    proper = seen-{group}
    maximal = [H for H in proper if not any(H < K for K in proper)]
    return seen, maximal
allA, maxA = subgroups(A)
allG, maxG = subgroups(G)
def conjugate(H, x):
    return frozenset(mul[mul[inverse[x]][h]][x] for h in H)
remaining, max_classes = set(maxG), []
while remaining:
    H = min(remaining, key=lambda h: tuple(sorted(h)))
    orbit = {conjugate(H, x) for x in G}
    need(orbit <= remaining, 'complete disjoint actual conjugacy class')
    remaining -= orbit
    max_classes.append((H, orbit))
involG = {g for g in G if orders[g] == 2}
mu = max(len(H & involG) for H in maxA if H != G)
mu_lemma = max(sum(orders[x] == 2 for x in H) for H in maxA if H != G)
for alpha in (g for g in G if orders[g] == 2):
    cg = {h for h in G if mul[h][alpha] == mul[alpha][h]}
    ca = {h for h in A if mul[h][alpha] == mul[alpha][h]}
    need(len(ca) == 2*len(cg), 'actual outer centralizer condition')
cases, overgroups = 0, 0
for x in G:
    prime = orders[x]
    if prime not in [3, 5]:
        continue
    cx = sum(mul[h][x] == mul[x][h] for h in G)
    cax = sum(mul[h][x] == mul[x][h] for h in A)
    xclass = {mul[mul[inverse[h]][x]][h] for h in G}
    B = Fraction(0)
    for H, orbit in max_classes:
        actual = sum(x in K for K in orbit)
        exact = Fraction(cx*len(xclass & H), len(H))
        need(actual == exact, 'literal overgroup formula')
        B += Fraction(cx*sum(orders[h] == prime for h in H)*len(H & involG), len(H))
        overgroups += 1
    bad_generation = {t for t in involG if close((x, t)) != G}
    all_inverters = {a for a in A if mul[mul[inverse[a]][x]][a] == inverse[x]}
    need(not all_inverters or len(all_inverters) == cax, 'literal inverter coset')
    inv_inverters = {a for a in all_inverters if orders[a] == 2}
    bad_reversal = {t for t in involG if any(mul[a][t] == mul[t][a] for a in inv_inverters)}
    need(len(bad_generation) <= B and len(bad_reversal) <= cax*mu_lemma, 'both excluded sets bounded')
    for alpha in inv_inverters:
        fixed = {t for t in involG if mul[alpha][t] == mul[t][alpha]}
        ca = {h for h in A if mul[alpha][h] == mul[h][alpha]}
        need(any(ca <= H for H in maxA if H != G) and len(fixed) <= mu_lemma, 'actual containing non-socle maximal')
    cases += 1
report = dict(status='PASS_INDEPENDENT_COUNTING_CONTROLS', arithmetic_rows=arithmetic,
              literal_group='A5 inside S5; all elements and subgroups explicitly enumerated',
              A_subgroups=len(allA), G_subgroups=len(allG), G_maximal_classes=len(max_classes),
              selected_prime_elements=cases, exact_overgroup_checks=overgroups,
              mu=mu_lemma, source_row_credit=0)
(D/'independent_control_report.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k != 'arithmetic_rows'}))
