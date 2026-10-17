"""Necessary Boolean conditions for one 21-vertex BFS section."""
import importlib.util
from itertools import combinations
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[2] / 'f012/graph_completion_certificate/cnf.py'
spec = importlib.util.spec_from_file_location('retained_boolean_formula', SOURCE)
common = importlib.util.module_from_spec(spec)
spec.loader.exec_module(common)
Formula, neg = common.Formula, common.neg


def thresholds(f, terms, limit):
    """The j-th entry says at least j inputs are true, for j <= limit."""
    s = [True] + [False] * limit
    for x in terms:
        s = [True] + [f.disjunction([s[j], f.conjunction([x, s[j-1]])])
                      for j in range(1, limit + 1)]
    return s


def build(holes):
    if (type(holes) is not list or len(holes) not in (3, 4)
            or any(type(p) is not list or len(p) != 2
                   or any(type(x) is not int or not 1 <= x <= 3 for x in p)
                   for p in holes)):
        raise ValueError('Three or four literal grid holes')
    missing = set(map(tuple, holes))
    if len(missing) != len(holes) or (1, 1) not in missing:
        raise ValueError('Distinct holes including the geodesic cell 11')
    names = ['u', 'v'] + [f'A{i}' for i in range(1, 4)] + [f'B{j}' for j in range(1, 4)]
    names += [f'C{i}{j}' for i in range(1, 4) for j in range(1, 4) if (i, j) not in missing]
    names += [f'U{i}{j}' for i, j in sorted(missing)] + [f'V{i}{j}' for i, j in sorted(missing)]
    names += ['X'] if len(missing) == 3 else []
    if len(names) != 21 or len(set(names)) != 21:
        raise ValueError('Exactly 21 distinct vertices')
    fixed = [('u', 'v')]
    fixed += [('u', f'A{i}') for i in range(1, 4)]
    fixed += [('v', f'B{j}') for j in range(1, 4)]
    for i in range(1, 4):
        for j in range(1, 4):
            fixed += [(f'A{i}', f'U{i}{j}'), (f'B{j}', f'V{i}{j}')] if (i, j) in missing else [
                (f'A{i}', f'C{i}{j}'), (f'B{j}', f'C{i}{j}')]
    fixed = {frozenset(e) for e in fixed}
    pairs = list(combinations(names, 2))
    # The eight centres/parents already have their four prescribed edges.
    saturated = set(names[:8])
    f = Formula()
    edges = {frozenset((a, b)): (True if frozenset((a, b)) in fixed else
                               False if a in saturated or b in saturated else f.variable())
             for a, b in pairs}
    edge = lambda a, b: edges[frozenset((a, b))]
    layer = {v: [f.variable() for _ in range(6)] for v in names}
    for row in layer.values():
        f.exactly(row, 1)
    anchors = dict(u=2, v=3, A1=1, B1=4, U11=0, V11=5)
    for v, h in anchors.items():
        f.clause([layer[v][h]])
    for v in names:
        degree = thresholds(f, [edge(v, w) for w in names if w != v], 5)
        f.clause([neg(degree[5])])
        for h in range(1, 5):
            f.clause([-layer[v][h], degree[4]])
        # Local layer zero is a nonroot BFS layer: one neighbor precedes it.
        # No positive internal-degree condition is imposed there.
        f.clause([-layer[v][0], neg(degree[4])])
        for h in range(1, 6):
            earlier = f.disjunction(f.conjunction([edge(v, w), layer[w][h-1]])
                                    for w in names if w != v)
            f.clause([-layer[v][h], earlier])
    for h in range(6):
        f.clause([thresholds(f, [layer[v][h] for v in names], 2)[2]])
    for a, b in pairs:
        for h in range(6):
            for k in range(6):
                if abs(h-k) > 1:
                    f.clause([neg(edge(a, b)), -layer[a][h], -layer[b][k]])
        paths = [f.conjunction([edge(a, c), edge(b, c)]) for c in names if c not in (a, b)]
        common_neighbor = f.at_most_one(paths)
        f.clause([neg(edge(a, b)), neg(common_neighbor)])
    metadata = dict(vertices=names, holes=holes, anchors=anchors,
                    fixed_edges=[sorted(e) for e in sorted(fixed, key=lambda e: tuple(sorted(e)))],
                    edge_variables=[dict(vertices=[a, b], variable=edges[frozenset((a, b))])
                                    for a, b in pairs if type(edges[frozenset((a, b))]) is int],
                    layer_variables=layer)
    return f, metadata
