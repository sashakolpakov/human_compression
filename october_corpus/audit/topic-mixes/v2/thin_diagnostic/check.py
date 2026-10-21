#!/usr/bin/env python3
"""Independent bit-state check of the proposed L016 Lemma3.5 counterexample.

The construction was proposed by rewrite_termination. This checker imports
none of that author's programs. It checks only this finite instance, not the
other source results or the all-parameter replacement construction.
"""
import json
from collections import Counter
from pathlib import Path
import sys


def need(test, why):
    if not test:
        raise ValueError(why)


def bit(x, i):
    return (x >> i) & 1


def step(x, colour, lifted):
    y = x ^ (1 << colour)
    if colour == 0 and bit(x, 1):
        y ^= 16
    if colour == 2 and bit(x, 3):
        y ^= 16
    if lifted and ((colour == 1 and bit(x, 2)) or (colour == 2 and bit(x, 3))):
        y ^= 32
    return y


def components(states, colours, lifted):
    remaining = set(states)
    answer = []
    while remaining:
        todo = [min(remaining)]
        reached = set(todo)
        while todo:
            x = todo.pop()
            for i in colours:
                y = step(x, i, lifted)
                need(y in states, 'component universe closed')
                if y not in reached:
                    reached.add(y)
                    todo.append(y)
        remaining -= reached
        answer.append(frozenset(reached))
    return answer


def model(lifted):
    states = set(range(64 if lifted else 32))
    for x in states:
        neighbours = [step(x, i, lifted) for i in range(4)]
        need(x not in neighbours and len(set(neighbours)) == 4, 'simple properly coloured graph')
        for i in range(4):
            need(step(neighbours[i], i, lifted) == x, 'involutory adjacency')
            for j in range(i + 2, 4):
                a = step(neighbours[i], j, lifted)
                b = step(neighbours[j], i, lifted)
                need(a == b and len({x, neighbours[i], neighbours[j], a}) == 4,
                     'nonconsecutive colours give genuine4cycles')
    need(len(components(states, range(4), lifted)) == 1, 'connected maniplex')
    faces = {i: components(states, [j for j in range(4) if j != i], lifted) for i in range(4)}
    faces[-1] = faces[4] = [frozenset(states)]
    for i in range(-1, 3):
        for j in range(i + 1, 4):
            for k in range(j + 1, 5):
                for a in faces[i]:
                    for b in faces[j]:
                        for c in faces[k]:
                            need(not (a & b and b & c) or bool(a & c), 'actual face order transitive')
    intervals = []
    for i in range(4):
        for lower in faces[i - 1]:
            for upper in faces[i + 1]:
                if lower & upper:
                    middle = [f for f in faces[i] if f & lower and f & upper]
                    intervals.append(len(middle))
    intersections = []
    for x in states:
        chamber = [next(f for f in faces[i] if x in f) for i in range(4)]
        intersections.append(len(set.intersection(*map(set, chamber))))
    return states, faces, dict(flags=len(states), face_counts=[len(faces[i]) for i in range(4)],
                               diamond_sizes=dict(sorted(Counter(intervals).items())),
                               flag_fibre_sizes=dict(sorted(Counter(intersections).items())))


def main():
    path = Path(sys.argv[1])
    need(not path.exists(), 'fresh result file')
    base, bf, br = model(False)
    cover, cf, cr = model(True)
    for x in cover:
        for i in range(4):
            need(step(x, i, True) % 32 == step(x % 32, i, False), 'projection preserves every coloured edge')
    preimages = []
    for i in range(4):
        for f in bf[i]:
            need(f == frozenset(x for x in base if bit(x, i) == bit(min(f), i)), 'base face is fixed coordinate')
            lifted_face = frozenset(x for x in cover if x % 32 in f)
            pieces = components(lifted_face, [j for j in range(4) if j != i], True)
            expected = 1 if i in [0, 3] else 2
            need(len(pieces) == expected and all(p in cf[i] for p in pieces), 'literal lemma face-preimage hypothesis')
            preimages.append(dict(rank=i, base_coordinate=bit(min(f), i), components=len(pieces)))
    vertex = frozenset(x for x in cover if bit(x, 0) == 0)
    two_face = frozenset(x for x in cover if bit(x, 2) == 0 and bit(x, 5) == 0)
    need(vertex in cf[0] and two_face in cf[2] and vertex & two_face, 'specified incident endpoint faces')
    middle = [f for f in cf[1] if f & vertex and f & two_face]
    witnesses = []
    for f in middle:
        x = min(f & vertex & two_face)
        witnesses.append(dict(flag=x, bits=[bit(x, i) for i in range(6)],
                              one_face_labels=[bit(x, 1), bit(x, 5) ^ bit(x, 4) ^ (bit(x, 0) & bit(x, 1))]))
    need(len(middle) == 4 and len({tuple(r['one_face_labels']) for r in witnesses}) == 4, 'four intermediate edges')
    need(set(br['diamond_sizes']) == {2} and set(br['flag_fibre_sizes']) == {2}, 'thin unfaithful base')
    need(4 in cr['diamond_sizes'] and set(cr['flag_fibre_sizes']) == {1}, 'faithful nonthin cover')
    result = dict(status='PASS_LITERAL_L016_LEMMA3_5_COUNTERMODEL', base=br, cover=cr,
                  every_face_preimage=preimages, diamond_witness=witnesses,
                  author_proposal='rewrite_termination', independent_implementation='root integer bit states',
                  source='arXiv2305.01372v2 physical page5 Lemma3.5',
                  whole_source_recovery=False, open_conjecture_credit=0)
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
