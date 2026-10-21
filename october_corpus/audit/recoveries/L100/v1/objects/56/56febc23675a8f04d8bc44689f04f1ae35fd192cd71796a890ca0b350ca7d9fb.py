"""Independent product proof for the mixed-prime rank-three control."""
import sys
if sys.flags.optimize:
    raise RuntimeError('ordinary Python required')
import itertools
import json
from pathlib import Path

p = Path(__file__).resolve().parent
order, mul, reps, incs, rows = json.loads((p/'mixed_control01/models.json').read_text())[0]
assert order == 12 and all(mul[x][y] == mul[y][x] for x in range(12) for y in range(12))
e = next(x for x in range(12) if all(mul[x][y] == y for y in range(12)))
two = {x for x in range(12) if mul[x][x] == e}
three = {x for x in range(12) if mul[mul[x][x]][x] == e}
assert len(two) == 4 and len(three) == 3
spaces = [{e}, *[{e, x} for x in two-{e}], two]
subgroups = {frozenset(mul[x][y] for x in v for y in c)
             for v in spaces for c in [{e}, three]}
assert set(map(frozenset, reps)) == subgroups
family_key = lambda family: tuple(sorted(tuple(sorted(h)) for h in family))
full_counts = {1: 0, 2: 0, 3: 0}
partial_count = 0
for b0, actual_panels, levels, full in rows:
    b = frozenset(b0)
    panels = [h for h in subgroups if b < h and len(h)//len(b) in (2, 3)]
    assert set(map(frozenset, actual_panels)) == set(panels)
    expected = {}
    expected_full = set()
    for size in range(1, len(panels)+1):
        expected[size] = set()
        for family in itertools.combinations(panels, size):
            join = set(b)
            product_index = 1
            for h in family:
                join = {mul[x][y] for x in join for y in h}
                product_index *= len(h)//len(b)
            # In this abelian quotient, injectivity of the multiplication map
            # from the prime-order factors is exactly this cardinality equality.
            if len(join) != len(b)*product_index:
                continue
            key = family_key(family)
            expected[size].add(key)
            if len(join) == order:
                expected_full.add(key)
    for rank, level in enumerate(levels, 1):
        got = [family_key([actual_panels[i] for i in indices]) for indices in level]
        assert len(got) == len(set(got)) and set(got) == expected.get(rank, set())
    assert sum(map(len, levels)) == sum(map(len, expected.values()))
    full_keys = [family_key(family) for family in full]
    assert len(full_keys) == len(set(full_keys)) and set(full_keys) == expected_full
    partial_count += sum(map(len, expected.values()))
    for family in full:
        full_counts[len(family)] += 1
assert full_counts == {1: 4, 2: 6, 3: 3} and partial_count == 32
report = dict(status='PASS_INDEPENDENT_PRODUCT_FAMILIES', group='C3 x C2^2',
              subgroups=10, every_partial_family_compared=True,
              partial_families=partial_count, full_counts=full_counts,
              total_full_families=13, target_census=False,
              reasoning='Subgroups split into the coprime Sylow parts. Prime-index panels in this abelian group give independent quotient factors exactly when the product of indices equals the index of their join. Such coordinate products have all intersection, Helly, primitive-residue and IP2 properties. No augmentation recurrence is used.')
(p/'mixed_analytic02.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report))
