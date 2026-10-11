"""Finite validation of the transversal assumptions; not a proof replacement."""
from fractions import Fraction
from support_controls import countermodels as support_countermodels


def need(value, text):
    if not value:
        raise RuntimeError(text)


def orbit_set(points, permutations):
    return {frozenset(p[x] for p in permutations) for x in points}


def countermodels():
    reports = support_countermodels()
    group = (0, 1)
    action_x = (tuple(range(6)), (1, 0, 3, 2, 4, 5))
    action_e = ((0, 1, 2, 3), (1, 0, 2, 3))
    support_action = ((0, 1, 2, 3), (0, 2, 1, 3))
    p = (0, 1, 0, 1, 2, 2)
    support = (3, 3, 1, 2, 3, 0)
    le = lambda i, j: i == 0 or j == 3 or i == j
    mu = (1, -1, -1, 1)
    representatives = (0, 2, 3)
    for g in group:
        for x in range(6):
            need(p[action_x[g][x]] == action_e[g][p[x]], 'Base equivariance')
            need(support[action_x[g][x]] == support_action[g][support[x]], 'Support equivariance')
    for e in range(4):
        need(sum(any(action_e[g][e] == r for g in group) for r in representatives) == 1,
             'One representative per base orbit')
    top = {x for x in range(6) if support[x] == 3}
    ambient = orbit_set(top, action_x)
    pairs = []
    averages = []
    for r in representatives:
        stabilizer = tuple(g for g in group if action_e[g][r] == r)
        fiber = {x for x in top if p[x] == r}
        local = orbit_set(fiber, tuple(action_x[g] for g in stabilizer))
        pairs.extend((r, o) for o in local)
        fixed_sum = sum(mu[l] * sum(p[x] == r and action_x[g][x] == x and le(support[x], l)
                                      for x in range(6)) for g in stabilizer for l in range(4))
        average = Fraction(fixed_sum, len(stabilizer))
        need(average == len(local), 'Actual local Mobius/Burnside count')
        averages.append(int(average))
    images = [frozenset(action_x[g][next(iter(o))] for g in group) for _, o in pairs]
    need(len(images) == len(set(images)) and set(images) == ambient, 'Actual global bijection')
    need(sum(averages) == len(ambient) == 2, 'Complete global count')
    reports.append({'model': 'two occupied base orbits and one unused base orbit',
                    'global_orbits': 2, 'local_counts': averages, 'actual_bijection': True})
    # Duplicate representatives: trivial one-point group/action, two copies of one base.
    singleton_orbits = orbit_set({0}, ((0,),))
    duplicated_fibers = [(i, o) for i in (0, 1) for o in singleton_orbits]
    duplicate_images = [o for _, o in duplicated_fibers]
    need(len(duplicate_images) > len(set(duplicate_images)), 'Duplicate representatives break injectivity')
    reports.append({'omitted': 'orbit separation of representative indices',
                    'sigma_orbits': len(duplicated_fibers), 'ambient_orbits': len(singleton_orbits), 'injective': False})
    # Missing representative: trivial action on two bases, select only the first.
    two_orbits = orbit_set({0, 1}, ((0, 1),))
    one_fiber = orbit_set({0}, ((0, 1),))
    need(one_fiber < two_orbits, 'Missing representatives break surjectivity')
    reports.append({'omitted': 'coverage of all object bases',
                    'sigma_orbits': len(one_fiber), 'ambient_orbits': len(two_orbits), 'surjective': False})
    # Inequivariant p: C2 acts trivially on X={0,1}, transitively on E={0,1}, p=id.
    # The orbit set of E has one representative, but its stabilizer fiber misses an X orbit.
    trivial_x = ((0, 1), (0, 1))
    swapping_e = ((0, 1), (1, 0))
    need(any(trivial_x[g][x] != swapping_e[g][x] for g in group for x in range(2)),
         'Inequivariant countermodel must violate the precise premise')
    need(len(orbit_set({0, 1}, trivial_x)) == 2 and len(orbit_set({0}, (trivial_x[0],))) == 1,
         'Inequivariant count fails')
    reports.append({'omitted': 'base equivariance', 'sigma_orbits': 1, 'ambient_orbits': 2})
    return reports
