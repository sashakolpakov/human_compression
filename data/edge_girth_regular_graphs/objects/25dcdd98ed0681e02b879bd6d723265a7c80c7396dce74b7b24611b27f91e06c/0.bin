"""Boolean clauses for the necessary graph conditions; no solver import."""
from itertools import combinations


def neg(x):
    return not x if type(x) is bool else -x


class Formula:
    def __init__(self):
        self.variables = 0
        self.clauses = []
        self.gates = []

    def variable(self):
        self.variables += 1
        return self.variables

    def clause(self, values):
        out = set()
        for x in values:
            if type(x) is bool:
                if x:
                    return
                continue
            if type(x) is not int or not 0 < abs(x) <= self.variables:
                raise ValueError('declared nonzero literal')
            if -x in out:
                return
            out.add(x)
        self.clauses.append(tuple(sorted(out)))

    def disjunction(self, terms):
        terms = list(terms)
        if any(type(x) is bool and x for x in terms):
            return True
        terms = list(dict.fromkeys(x for x in terms if type(x) is not bool))
        if any(-x in terms for x in terms):
            return True
        if not terms:
            return False
        if len(terms) == 1:
            return terms[0]
        y = self.variable()
        self.clause([-y, *terms])
        for x in terms:
            self.clause([y, -x])
        self.gates.append((y, tuple(terms)))
        return y

    def conjunction(self, terms):
        return neg(self.disjunction(neg(x) for x in terms))

    def at_most_one(self, terms):
        previous = False
        for x in terms:
            self.clause([neg(previous), neg(x)])
            previous = self.disjunction([previous, x])
        return previous

    def exactly(self, terms, required):
        terms = list(terms)
        if not 0 <= required <= len(terms):
            self.clause([])
            return
        # s[j] means that at least j of the preceding terms are true.
        s = [True] + [False] * (required + 1)
        for x in terms:
            s = [True] + [self.disjunction([s[j], self.conjunction([x, s[j-1]])])
                          for j in range(1, required + 2)]
        self.clause([s[required]])
        self.clause([neg(s[required + 1])])

    def evaluate(self, edge_values):
        values = dict(edge_values)
        def value(x):
            if type(x) is bool:
                return x
            return values[abs(x)] if x > 0 else not values[abs(x)]
        for y, terms in self.gates:
            values[y] = any(value(x) for x in terms)
        if set(values) != set(range(1, self.variables + 1)):
            raise ValueError('all primary and auxiliary variables assigned')
        return all(any(value(x) for x in clause) for clause in self.clauses)

    def dimacs(self):
        return f'p cnf {self.variables} {len(self.clauses)}\n' + ''.join(
            ' '.join(map(str, clause)) + ' 0\n' for clause in self.clauses)


def cycle_edges(vertices, n):
    if not isinstance(vertices, list) or not 3 <= len(vertices) <= 6:
        raise ValueError('literal short cycle')
    if any(type(v) is not int or not 0 <= v < n for v in vertices):
        raise ValueError('cycle vertex range')
    if len(set(vertices)) != len(vertices):
        raise ValueError('simple cycle')
    return frozenset(tuple(sorted((a, b)))
                     for a, b in zip(vertices, vertices[1:] + vertices[:1]))


def witness_edges(witness, n, base, allowed):
    if set(witness) != {'kind', 'cycles'} or type(witness['cycles']) is not list:
        raise ValueError('literal witness fields')
    cycles = witness['cycles']
    es = [cycle_edges(c, n) for c in cycles]
    if witness['kind'] == 'short_cycle':
        if len(es) != 1 or len(cycles[0]) > 5:
            raise ValueError('short cycle')
    elif witness['kind'] == 'shared_hexagons':
        if len(es) != 2 or any(len(c) != 6 for c in cycles):
            raise ValueError('two hexagons')
        if es[0] == es[1] or not es[0].intersection(es[1]):
            raise ValueError('distinct hexagons sharing an edge')
    else:
        raise ValueError('known obstruction')
    edges = frozenset().union(*es)
    if not edges <= base | allowed:
        raise ValueError('witness inside exact edge domain')
    return tuple(sorted(edges - base))


def build(n, base, allowed, degree=None, cuts=()):
    if type(n) is not int or n < 1:
        raise ValueError('positive finite order')
    base, allowed = frozenset(base), frozenset(allowed)
    pairs = list(combinations(range(n), 2))
    if base & allowed or not base | allowed <= set(pairs):
        raise ValueError('disjoint simple edge domain')
    f = Formula()
    variables = {e: f.variable() for e in sorted(allowed)}
    edge = {e: True if e in base else variables.get(e, False) for e in pairs}
    if degree is not None:
        if type(degree) is not int or not 0 <= degree < n:
            raise ValueError('finite simple degree')
        for v in range(n):
            residual = degree - sum(v in e for e in base)
            f.exactly([x for e, x in variables.items() if v in e], residual)
    common = {}
    domain = base | allowed
    for u, v in pairs:
        paths = []
        for w in range(n):
            if w in (u, v):
                continue
            a, b = tuple(sorted((u, w))), tuple(sorted((v, w)))
            if a in domain and b in domain:
                paths.append(f.conjunction([edge[a], edge[b]]))
        common[u, v] = f.at_most_one(paths)
        f.clause([neg(edge[u, v]), neg(common[u, v])])
    for v, w in sorted(domain):
        for u in range(n):
            if u in (v, w):
                continue
            a, b = tuple(sorted((u, v))), tuple(sorted((u, w)))
            f.clause([neg(edge[v, w]), neg(common[a]), neg(common[b])])
    for witness in cuts:
        f.clause([-variables[e] for e in witness_edges(witness, n, base, allowed)])
    return f, variables
