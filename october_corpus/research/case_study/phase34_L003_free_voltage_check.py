#!/usr/bin/env python3
"""Literal free-word certificate for largeness of the nine-relator rotation group."""
import argparse
from collections import deque
from hashlib import sha256
import json
from pathlib import Path


def reduce_word(word):
    out = []
    for a in word:
        if out and out[-1] == -a:
            out.pop()
        else:
            out.append(a)
    return out


def inverse(word):
    return [-a for a in reversed(word)]


def power(word, n):
    return (word if n >= 0 else inverse(word)) * abs(n)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--data', type=Path, default=Path(__file__).with_name('phase34_L003_free_voltage_data.json'))
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise SystemExit('Refusing to overwrite an existing report')
    raw = args.data.read_bytes()
    permutations, voltages, witnesses = json.loads(raw)
    n = len(permutations[0])
    assert n == 648 and len(permutations) == len(voltages) == 3
    permutations = [[a - 1 for a in p] for p in permutations]
    assert all(sorted(p) == list(range(n)) for p in permutations)
    assert all(len(v) == n for v in voltages)
    assert all(all(a in (-2, -1, 1, 2) for a in w) and reduce_word(w) == w
               for v in voltages for w in v)
    inverses = [[p.index(i) for i in range(n)] for p in permutations]

    def act(word, state=0):
        voltage = []
        for a in word:
            j = abs(a) - 1
            assert 0 <= j < 3
            if a > 0:
                voltage = reduce_word(voltage + voltages[j][state])
                state = permutations[j][state]
            else:
                state = inverses[j][state]
                voltage = reduce_word(voltage + inverse(voltages[j][state]))
        return state, voltage

    x, y, z = [1], [2], [3]
    relators = [power(x, 6), power(y, 3), power(z, 2), power(z + x, 3),
                power(z + y, 6), power(inverse(x) + y, 2),
                power(inverse(y) + power(x, -2), 3), power(z + power(x, 3), 2),
                inverse(x) + z + power(inverse(y) + z, 2) + z + x + power(z + y, 2)]
    for rel in relators:
        for i in range(n):
            assert act(rel, i) == (i, []), (rel, i, act(rel, i))

    orbit, queue = {0}, deque([0])
    while queue:
        i = queue.popleft()
        for p in permutations:
            if p[i] not in orbit:
                orbit.add(p[i]); queue.append(p[i])
    assert len(orbit) == n

    shortest = {}
    for word, expected in witnesses:
        assert expected in ([1], [2]) and act(word) == (0, expected)
        a = expected[0]
        if a not in shortest or (len(word), word) < (len(shortest[a]), shortest[a]):
            shortest[a] = word
    assert set(shortest) == {1, 2}
    torus = y + power(z + y, 2)
    assert all(act(power(torus, 2), i)[0] == i for i in range(n))
    torus_loops = [act(power(torus, 2), i)[1] for i in range(n)]
    report = {
        'result': 'PASS', 'group': 'P_omit: the first-nine rotational relators',
        'degree': n, 'transitive_base_action': True,
        'relator_state_checks': n * len(relators),
        'free_rank': 2, 'all_listed_schreier_witnesses_checked': len(witnesses),
        'shortest_surjectivity_witnesses': {str(a): w for a, w in sorted(shortest.items())},
        'maximum_edge_voltage_length': max(map(len, sum(voltages, []))),
        'torus_squared_base_permutation_identity': True,
        'torus_squared_nontrivial_fibers': sum(bool(w) for w in torus_loops),
        'torus_squared_distinct_voltages': sorted({tuple(w) for w in torus_loops}),
        'data_sha256': sha256(raw).hexdigest(),
        'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope': 'An index-648 subgroup surjects onto F2. No GAP/RRS/NQ dependency in this verification; no odd-parameter existence or geometry assertion.'
    }
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: 5832 literal free-word relator checks; transitive 648-state action; two onto-F2 witnesses.')


if __name__ == '__main__':
    main()
