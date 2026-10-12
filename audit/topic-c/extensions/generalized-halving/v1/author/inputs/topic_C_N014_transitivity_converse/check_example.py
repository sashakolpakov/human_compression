"""Optional exact incidence check; the manuscript supplies the complete proof."""
import itertools as it
import json
from pathlib import Path

V = list(it.combinations(range(1, 6), 2))
g = {1: 2, 2: 1, 3: 3, 4: 4, 5: 5}
twist = lambda v: tuple(sorted(g[x] for x in v))
adj = lambda x, y: not set(x).intersection(twist(y))
assert all(not adj(v, v) for v in V)
assert all(adj(x, y) == adj(y, x) for x in V for y in V)
E = [frozenset((x, y)) for x, y in it.combinations(V, 2) if adj(x, y)]
assert len(E) == 15
assert all(sum(v in e for e in E) == 3 for v in V)
triangles = [t for t in it.combinations(V, 3) if all(adj(x, y) for x, y in it.combinations(t, 2))]
assert len(triangles) == 2 and not any((1, 2) in t for t in triangles)

def incidence(halved):
    levels = [V, V if halved else E, ['+', '-']]
    objects = [(i, x) for i, xs in enumerate(levels) for x in xs]
    def inc(a, b):
        if a[0] == b[0]: return a == b
        if a[0] > b[0]: a, b = b, a
        if b[0] == 2: return True
        return adj(a[1], b[1]) if halved else a[1] in b[1]
    flags = [f for k in range(4) for f in it.combinations(objects, k)
             if all(inc(a, b) for a, b in it.combinations(f, 2))]
    chambers = [f for f in flags if len(f) == 3]
    assert len(chambers) == 60
    assert all(any(set(f) <= set(c) for c in chambers) for f in flags)
    residues = 0
    for f in flags:
        if len(f) > 1: continue
        R = [x for x in objects if x not in f and all(inc(x, y) for y in f)]
        seen = {R[0]}; todo = [R[0]]
        while todo:
            x = todo.pop()
            new = {y for y in R if y not in seen and inc(x, y)}
            seen |= new; todo.extend(new)
        assert len(seen) == len(R)
        residues += 1
    return {'objects': [len(x) for x in levels], 'flags': len(flags), 'chambers': len(chambers), 'connected_residues': residues}

base = ((1, 2), (3, 4))
orbit = set()
for p in it.permutations(range(1, 6)):
    sigma = dict(zip(range(1, 6), p))
    f = lambda x: tuple(sorted(sigma[j] for j in x))
    for x, y in it.product(V, repeat=2):
        assert adj(x, y) == adj(f(x), twist(f(twist(y))))
    orbit.add((f(base[0]), twist(f(twist(base[1])))))
assert len(orbit) == 30 and all(adj(*pair) for pair in orbit)
report = {'status': 'PASS', 'role': 'optional diagnostics only', 'original': incidence(False), 'halved': incidence(True), 'triangles': triangles, 'lower_flag_orbit': len(orbit), 'S5_incidence_checks': 12000}
Path(__file__).with_name('example_report.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report))
