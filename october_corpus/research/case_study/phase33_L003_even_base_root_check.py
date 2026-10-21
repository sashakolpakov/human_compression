#!/usr/bin/env python3
"""Independent base certificate using Cayley components and all coset flags.

No import of the author implementation. This verifies the modulus-one base,
not the integer voltage or uniform local-group arguments.
"""
import argparse
from collections import Counter, deque
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise SystemExit('Refusing to overwrite saved evidence')
    source = Path(__file__).with_name('phase33_L003_even_voltage.json')
    data = json.loads(source.read_text())
    n = data['degree']
    assert n == 648
    marks = [tuple(range(n, 2*n)) + tuple(range(n))]
    for raw in data['permutations']:
        p = tuple(a-1 for a in raw)
        assert sorted(p) == list(range(n))
        inverse = [None]*n
        for i, j in enumerate(p): inverse[j] = i
        marks.append(tuple(n+i for i in inverse) + p)
    identity = tuple(range(2*n))
    assert all(tuple(g[g[i]] for i in identity) == identity for g in marks)
    elements = [identity]
    index = {identity: 0}
    todo = deque([0])
    right = []
    while todo:
        a = todo.popleft()
        assert a == len(right)
        row = []
        for g in marks:
            p = tuple(g[j] for j in elements[a])
            if p not in index:
                index[p] = len(elements)
                elements.append(p)
                todo.append(index[p])
            row.append(index[p])
        right.append(row)
        assert len(elements) <= 1296
    assert len(elements) == 1296
    left = [[index[tuple(p[j] for j in g)] for g in marks] for p in elements]
    # Explicitly check that these really are commuting left/right actions.
    assert all(left[right[a][j]][i] == right[left[a][i]][j]
               for a in range(1296) for i in range(4) for j in range(4))

    def cosets(mask):
        unseen = set(range(1296))
        rows = []
        while unseen:
            a = min(unseen)
            todo = [a]
            unseen.remove(a)
            bits = 0
            while todo:
                b = todo.pop()
                bits |= 1 << b
                for i in range(4):
                    if mask & (1 << i):
                        c = left[b][i]
                        if c in unseen:
                            unseen.remove(c)
                            todo.append(c)
            rows.append(bits)
        return rows

    all_cosets = {mask: cosets(mask) for mask in range(16)}
    subgroups = [all_cosets[mask][0] for mask in range(16)]
    assert all(subgroups[a] & subgroups[b] == subgroups[a & b]
               for a, b in product(range(16), repeat=2))
    pars = [all_cosets[15 ^ (1 << i)] for i in range(4)]
    assert [len(p) for p in pars] == [36, 27, 27, 12]
    flags_by_type = Counter()
    chambers = []

    def visit(next_type, selected, common, mask):
        # Pairwise incidence is tested independently of the common point.
        assert common, ('pairwise flag lacks common representative', mask)
        flags_by_type[mask] += 1
        if mask == 15:
            assert common.bit_count() == 1
            chambers.append(common)
        for i in range(next_type, 4):
            for coset in pars[i]:
                if all(coset & old for old in selected):
                    visit(i+1, selected+[coset], common & coset, mask | (1 << i))

    visit(0, [], (1 << 1296)-1, 0)
    assert len(chambers) == len(set(chambers)) == 1296
    report = {
        'status': 'PASS',
        'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'data_sha256': sha256(source.read_bytes()).hexdigest(),
        'method': 'Independent literal base closure, commuting Cayley actions, all marked subgroup components and exhaustive pairwise-incident coset flags',
        'group_order': len(elements),
        'left_right_commutation_checks': 1296*16,
        'marked_subgroup_orders': [h.bit_count() for h in subgroups],
        'marked_meets': 256,
        'coset_counts_by_type': [len(p) for p in pars],
        'flags_by_type_mask': dict(sorted(flags_by_type.items())),
        'total_flags': sum(flags_by_type.values()),
        'all_flags_have_common_point': True,
        'chambers_with_unique_representative': len(chambers),
        'scope': 'Base modulus one only; no voltage, local torus, all-parameter or priority inference.'
    }
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print('PHASE33_L003_BASE_ROOT_PASS', report['total_flags'], 'flags')


if __name__ == '__main__':
    main()
