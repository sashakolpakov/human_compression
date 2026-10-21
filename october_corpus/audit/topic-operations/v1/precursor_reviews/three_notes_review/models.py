"""Bounded independent checks; no author mathematical program is imported."""
import itertools
import json

def need(condition, message):
    if not condition:
        raise ValueError(message)

def inter(family, whole):
    result = set(whole)
    for item in family:
        result.intersection_update(item)
    return frozenset(result)

def span(gens):
    result = {0}
    for g in gens:
        result |= {x ^ g for x in tuple(result)}
    return frozenset(result)

space = frozenset(range(8))
subspaces = sorted({span(g) for n in range(4)
                    for g in itertools.combinations(range(1, 8), n)},
                   key=lambda h: (len(h), sorted(h)))
need(len(subspaces) == 16, 'all F2^3 subspaces')
families = firm_families = inclusions = 0
for rank in range(5):
    for family in itertools.combinations(subspaces, rank):
        families += 1
        borel = inter(family, space)
        minimal = [inter(family[:i] + family[i+1:], space) for i in range(rank)]
        if not all(h > borel for h in minimal):
            continue
        firm_families += 1
        pars = [inter([family[i] for i in range(rank) if mask >> i & 1], space)
                for mask in range(1 << rank)]
        for j, k in itertools.product(range(1 << rank), repeat=2):
            need((pars[j] <= pars[k]) == (k & j == k), 'firm Boolean implication')
            inclusions += 1

# The exact nonfirm indexed-lattice example in the reviewed root note.
axes = [span([2, 4]), span([1, 4]), span([1, 2]), span([4])]
phi = lambda x: ((x << 1) & 7) | (x >> 2)
parabolics = {inter([axes[i] for i in range(4) if mask >> i & 1], space)
              for mask in range(16)}
need(len(parabolics) == 8, 'all eight coordinate parabolics')
need({frozenset(map(phi, h)) for h in parabolics} == parabolics, 'unlabelled admissible')
need(frozenset(map(phi, axes[3])) != axes[3], 'indexed compatibility is absent')
need(span([4, phi(4), phi(phi(4))]) == space, 'actual stable-letter orbit closure')
need(inter(axes[1:], space) == inter(axes, space), 'nonfirm panel detected')

def finite_cosets(group, mul, sub):
    return {frozenset(mul(x, h) for h in sub) for x in group}

def join_model(swapping):
    group = tuple(itertools.product(range(4), range(2)))
    def action(b, a):
        return ((a & 1) << 1) | ((a & 2) >> 1) if swapping and b else a
    def mul(x, y):
        return (x[0] ^ action(x[1], y[0]), x[1] ^ y[1])
    orbits = [[0, 1]] if swapping else [[0], [1]]
    original = [frozenset([0, 1]), frozenset([0, 2])]
    coarse = [inter([original[i] for i in orbit], range(4)) for orbit in orbits]
    parabolics = [frozenset(itertools.product(h, range(2))) for h in coarse]
    parabolics += [frozenset(itertools.product(range(4), [0]))]
    cosets = [finite_cosets(group, mul, h) for h in parabolics]
    flags = 0
    def visit(i, chosen):
        nonlocal flags
        if i == len(cosets):
            need(inter(chosen, group), 'literal semidirect flag Helly')
            flags += 1
            return
        visit(i+1, chosen)
        for c in cosets[i]:
            if all(c & d for d in chosen):
                visit(i+1, chosen + [c])
    visit(0, [])
    borel = inter(parabolics, group)
    panels = [len(inter(parabolics[:i] + parabolics[i+1:], group)) // len(borel)
              for i in range(len(parabolics))]
    # Direct Cartesian-fiber check for every coset, not only the panel indices.
    for h, hs in zip(parabolics, cosets):
        for x in group:
            actual = frozenset(mul(x, z) for z in h)
            h_a = {z[0] for z in h}; h_b = {z[1] for z in h}
            expected = frozenset(itertools.product(
                {x[0] ^ action(x[1], z) for z in h_a},
                {x[1] ^ z for z in h_b}))
            need(actual == expected and actual in hs, 'complete coordinate-fiber identity')
    return {'flags': flags, 'panel_indices': panels}

trivial = join_model(False); swap = join_model(True)
need(trivial['panel_indices'] == [2, 2, 2], 'trivial-action join is thin')
need(swap['panel_indices'] == [4, 2], 'nontrivial orbit has four-element panel')

# Free-product reduced words in C2^2 * C2^2. The two Borels are {0,1}.
# These bounded tests check the normal-form obstruction used for infinitely
# many cosets; the all-n argument itself is written in the reviewed note.
def reduce_word(word):
    stack = []
    for factor, value in word:
        if not value:
            continue
        if stack and stack[-1][0] == factor:
            value ^= stack.pop()[1]
            if value:
                stack.append((factor, value))
        else:
            stack.append((factor, value))
    return tuple(stack)
powers = [tuple([(0, 2), (1, 1)] * n) for n in range(41)]
separations = 0
for i, j in itertools.combinations(range(41), 2):
    quotient = reduce_word(tuple(reversed(powers[i])) + powers[j])
    need(any(factor == 0 and value not in [0, 1] for factor, value in quotient),
         'different panel cosets by an outside A syllable')
    separations += 1

controls = []
for label, predicate in [
    ('nonfirm still Boolean', lambda: len(parabolics) == 16),
    ('unlabelled implies named-index compatibility', lambda: frozenset(map(phi, axes[3])) == axes[3]),
    ('raw base survives unchanged', lambda: span([4, phi(4), phi(phi(4))]) == axes[3]),
    ('all semidirect joins are nonthin', lambda: trivial['panel_indices'] != [2,2,2]),
    ('merged two-type orbit stays thin', lambda: swap['panel_indices'] == [2,2]),
    ('nontrivial Borel free panel has size two', lambda: separations <= 1),
]:
    try:
        need(predicate(), label)
    except ValueError:
        controls.append(label)
    else:
        raise ValueError('false weakening survived: '+label)

print(json.dumps({'status': 'PASS', 'bounded_families': families,
                  'firm_families': firm_families, 'Boolean_inclusion_pairs': inclusions,
                  'unlabelled_counterexample_parabolics': len(parabolics),
                  'trivial_join': trivial, 'swapped_join': swap,
                  'distinct_free_panel_coset_pairs': separations,
                  'rejected_controls': controls,
                  'scope': 'Finite validation only; arbitrary-group normal-form/tree/lattice proofs reviewed in writing.'}, indent=2))
