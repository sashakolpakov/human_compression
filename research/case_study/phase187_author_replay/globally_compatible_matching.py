#!/usr/bin/env python3
"""Literal three-factor parallel gluing and its common-lift obstruction.

Only Python's standard library is used. No precomputed geometry, group or
incidence certificate is loaded.
"""
import argparse
from collections import Counter, deque
from itertools import combinations, permutations, product
import hashlib
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def compose(g, h):
    return tuple(g[h[i]] for i in range(len(g)))


def inverse(g):
    return tuple(g.index(i) for i in range(len(g)))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    require(not a.output.exists() and not a.output.is_symlink(), 'fresh output required')
    omega = range(8)
    parts = [
        [[0, 1], [2, 3], [4, 5], [6, 7]],
        [[1, 2], [3, 4], [5, 6], [7, 0]],
        [[0, 1, 4, 5], [2, 3, 6, 7]],
        [[1, 2, 5, 6], [0, 3, 4, 7]],
    ]
    parts = tuple(tuple(sorted(tuple(sorted(b)) for b in part)) for part in parts)
    for part in parts:
        require(sorted(x for b in part for x in b) == list(omega), 'directions partition points')
        require(all(len(b) >= 2 for b in part), 'firm base line')
    allblocks = tuple(b for part in parts for b in part)
    require(len(allblocks) == len(set(allblocks)), 'property O: distinct line shadows')
    # At rank two, being a partition gives existence and uniqueness of the
    # line of each direction through every point, hence the parallelism axioms.
    aut = []
    image = set()
    for g in permutations(omega):
        moved = tuple(tuple(sorted(g[x] for x in b)) for b in allblocks)
        if set(moved) != set(allblocks):
            continue
        induced = []
        for part in parts:
            target = tuple(sorted(tuple(sorted(g[x] for x in b)) for b in part))
            require(target in parts, 'every full base automorphism preserves parallelism')
            induced.append(parts.index(target))
        aut.append(g)
        image.add(tuple(induced))
    e = (0, 1, 2, 3)
    aa = (1, 0, 3, 2)
    s = (0, 2, 1, 3)
    t = (0, 3, 2, 1)
    alpha = (e, s, t)
    beta = alpha
    require(len(aut) == 16 and image == {e, aa}, 'complete base action and direction image')
    cosets = [{compose(compose(b, h), inverse(al)) for h in image}
              for al, b in zip(alpha, beta)]
    require(all(cosets[i] & cosets[j] for i, j in combinations(range(3), 2)),
            'all pairwise lift conditions hold')
    require(not set.intersection(*cosets), 'global lift must be obstructed')
    # Check the printed Lemma3.4 membership formula itself, in both ordered
    # directions, rather than relying only on an equivalent coset formulation.
    printed_checks = []
    for j, k in permutations(range(3), 2):
        target = compose(compose(compose(alpha[j], inverse(beta[j])), beta[k]), inverse(alpha[k]))
        hj = {compose(compose(alpha[j], h), inverse(alpha[j])) for h in image}
        hk = {compose(compose(alpha[k], h), inverse(alpha[k])) for h in image}
        require(target in {compose(x, y) for x in hj for y in hk}, 'printed pairwise product condition')
        printed_checks.append([j, k, list(target)])

    def glued(match):
        lines = []
        directions = []
        for d in range(4):
            choices = [parts[inverse(match[j])[d]] for j in range(3)]
            for blocks in product(*choices):
                lines.append(blocks)
                directions.append(d)
        require(len(lines) == len(set(lines)), 'literal tuple objects are distinct')
        sizes = [8, 8, 8, len(lines)]
        offsets = [0, 8, 16, 24]
        types = [i for i, n in enumerate(sizes) for _ in range(n)]
        groups = [list(range(offsets[i], offsets[i] + sizes[i])) for i in range(4)]
        objects = [(j, x) for j in range(3) for x in omega] + [(3, line) for line in lines]
        neighbours = [set() for _ in objects]
        for u, v in combinations(range(len(objects)), 2):
            tu, x = objects[u]
            tv, y = objects[v]
            incident = (tu != tv and tv < 3) or (tu < 3 and tv == 3 and x in y[tu])
            if incident:
                neighbours[u].add(v)
                neighbours[v].add(u)
        flags = [[] for _ in range(5)]
        for n in range(5):
            for type_set in combinations(range(4), n):
                flags[n].extend(f for f in product(*(groups[i] for i in type_set))
                                if all(v in neighbours[u] for u, v in combinations(f, 2)))
        projections = {f for c in flags[4] for n in range(5) for f in combinations(c, n)}
        require(all(f in projections for layer in flags for f in layer), 'all glued flags extend')

        def residue(f):
            used = {types[u] for u in f}
            r = {u for u in range(len(objects)) if types[u] not in used}
            for u in f:
                r &= neighbours[u]
            return r

        checked = Counter()
        for n in range(3):
            for f in flags[n]:
                r = residue(f)
                require(bool(r), 'nonempty glued residue')
                seen = {min(r)}
                queue = deque(seen)
                while queue:
                    u = queue.popleft()
                    new = (neighbours[u] & r) - seen
                    seen.update(new)
                    queue.extend(new)
                require(seen == r, 'every glued rank-at-least-two residue connected')
                checked[4 - n] += 1
        panels = Counter(len(residue(f)) for f in flags[3])
        require(min(panels) >= 2, 'all glued panels firm')
        encoded = {'objects': objects, 'neighbours': [sorted(n) for n in neighbours]}
        return {'line_counts_by_direction': dict(sorted(Counter(directions).items())),
                'object_counts': sizes, 'flag_counts': [len(f) for f in flags],
                'connected_residues_by_rank': dict(sorted(checked.items())),
                'panel_completion_distribution': dict(sorted(panels.items())),
                'every_flag_extends': True, 'firm': True, 'residually_connected': True,
                'incidence_certificate_sha256': hashlib.sha256(json.dumps(encoded, sort_keys=True).encode()).hexdigest()}

    ga, gb = glued(alpha), glued(beta)
    require(ga['object_counts'][-1] == 112 and gb['object_counts'][-1] == 104,
            'different literal gluing object counts')
    report = {'status': 'PASS', 'source': 'Buekenhout-Huybrechts-Pasini1994 Lemma3.4, three factors',
              'base_points': list(omega), 'base_direction_partitions': parts,
              'property_O_verified': True, 'base_full_automorphisms': aut,
              'base_full_automorphism_order': len(aut), 'direction_image': sorted(image),
              'alpha': alpha, 'beta': beta, 'lift_cosets': [sorted(c) for c in cosets],
              'all_six_printed_product_checks': printed_checks,
              'pairwise_intersections': [sorted(cosets[i] & cosets[j]) for i, j in combinations(range(3), 2)],
              'global_intersection_empty': True, 'gluing_alpha': ga, 'gluing_beta': gb,
              'nonisomorphic_even_without_type_preservation': True,
              'reason': 'Total object counts differ:136 versus128',
              'source_lemma_refuted_at_three_factors': True,
              'whole_paper_replaced': False, 'open_conjecture_claim': False,
              'Lean_geometry_certificate': False,
              'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    with a.output.open('x') as f:
        json.dump(report, f, indent=2)
        f.write('\n')
    print('PHASE187_PARALLEL_GLUING_PASS', ga['object_counts'], gb['object_counts'])


if __name__ == '__main__':
    main()
