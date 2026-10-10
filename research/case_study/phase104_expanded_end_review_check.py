#!/usr/bin/env python3
"""Independent all-parabolic affine audit: bit-plane F3 arithmetic and Schreier loops.

No author program is imported. The bound author certificate is checked as data.
The output is new; original sources and the public repository remain untouched.
"""
import argparse
from collections import deque
import hashlib
import itertools
import json
import os
from pathlib import Path
import time

MANIFEST = 'phase102_expanded_end_covers_manifest.json'
MANIFEST_SHA = 'f5273849cf506f08aab9180ddbf77a969ea26821604d3ec6e8468bd14bda21b8'
MODEL = 'phase66_coprime_cover_permutation_model.json'
CERTIFICATE = 'phase102_expanded_end_covers_certificate.json'
WIDTH = 1024
MASK = (1 << WIDTH) - 1
ZERO = (0, 0)


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def binding(path):
    raw = path.read_bytes()
    return dict(sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))


def plus(a, b):
    # Bit positions encode coefficients one and two, respectively.
    a1, a2 = a
    b1, b2 = b
    az = MASK ^ (a1 | a2)
    bz = MASK ^ (b1 | b2)
    return ((a1 & bz) | (az & b1) | (a2 & b2),
            (a2 & bz) | (az & b2) | (a1 & b1))


def neg(v):
    return v[1], v[0]


def minus(a, b):
    return plus(a, neg(b))


def move(v, permutation):
    result = []
    for plane in v:
        image = 0
        while plane:
            bit = plane & -plane
            image |= 1 << permutation[bit.bit_length() - 1]
            plane ^= bit
        result.append(image)
    return tuple(result)


def sparse(v):
    return [[j, 1 if (v[0] >> j) & 1 else 2]
            for j in range(WIDTH) if ((v[0] | v[1]) >> j) & 1]


def unit(j):
    return 1 << j, 0


class Basis:
    """Independent highest-coordinate elimination using two integer bit planes."""
    def __init__(self, vectors=()):
        self.rows = {}
        for v in vectors:
            self.insert(v)

    def reduce(self, v):
        while v != ZERO:
            p = (v[0] | v[1]).bit_length() - 1
            row = self.rows.get(p)
            if row is None:
                break
            v = minus(v, neg(row) if (v[1] >> p) & 1 else row)
        return v

    def insert(self, v):
        v = self.reduce(v)
        if v == ZERO:
            return False
        p = (v[0] | v[1]).bit_length() - 1
        self.rows[p] = neg(v) if (v[1] >> p) & 1 else v
        return True

    def contains(self, v):
        return self.reduce(v) == ZERO

    def vectors(self):
        return [self.rows[p] for p in sorted(self.rows, reverse=True)]

    def __len__(self):
        return len(self.rows)


def span(*spaces):
    return Basis(itertools.chain.from_iterable(s.vectors() for s in spaces))


def same_space(first, second):
    return (len(first) == len(second)
            and all(first.contains(v) for v in second.vectors())
            and all(second.contains(v) for v in first.vectors()))


def product(first, second):
    return tuple(second[first[j]] for j in range(len(first)))


def inverse(permutation):
    result = [0] * len(permutation)
    for i, j in enumerate(permutation):
        result[j] = i
    return result


def closure(generators, identity):
    words = {identity: ()}
    pending = deque([identity])
    while pending:
        g = pending.popleft()
        for i, generator in generators:
            dest = product(g, generator)
            if dest not in words:
                words[dest] = words[g] + (i,)
                pending.append(dest)
    return words


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study-root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    root, out = args.study_root.resolve(), args.output_dir.absolute()
    require(not os.path.lexists(out), 'Fresh independent output required')
    started = time.monotonic()
    require(binding(root / MANIFEST)['sha256'] == MANIFEST_SHA, 'Frozen author manifest differs')
    manifest = json.loads((root / MANIFEST).read_text())
    records = {MANIFEST: binding(root / MANIFEST)}
    for kind in ['files', 'proof_dependencies', 'context_only_not_proof_premises',
                 'private_primary_bindings_not_exported']:
        for name, record in manifest[kind].items():
            require(binding(root / name) == record, 'Frozen input differs: ' + name)
            records[name] = record
    model = json.loads((root / MODEL).read_text())
    certificate = json.loads((root / CERTIFICATE).read_text())
    generators = [tuple(x - 1 for x in p) for p in model['generators']]
    identity = tuple(range(model['degree']))
    require(len(generators) == 4 and len(identity) == 128, 'Base model degree')
    for s in generators:
        require(sorted(s) == list(identity) and s != identity and product(s, s) == identity,
                'Nontrivial base involution')
    require(len(set(generators)) == 4, 'Distinct base marks')
    words = closure(list(reversed(list(enumerate(generators)))), identity)
    group = sorted(words)
    require(len(group) == 1024, 'Fixed group order')
    gid = {g: i for i, g in enumerate(group)}
    one = gid[identity]
    edges = [[gid[product(g, s)] for s in generators] for g in group]

    # Independent lexicographic coset labels, rather than the author's BFS labels.
    labels, representatives = [], []
    for s in [generators[0], generators[3]]:
        representatives.append(sorted({min(g, product(s, g)) for g in group}))
        index = {g: i for i, g in enumerate(representatives[-1])}
        labels.append({g: index[min(g, product(s, g))] for g in group})
        require(len(index) == 512, 'Coset count')
    actions = []
    for s in generators:
        actions.append([512 * t + labels[t][product(g, s)]
                        for t in range(2) for g in representatives[t]])
    for a in actions:
        require(sorted(a) == list(range(WIDTH)), 'Module generator bijection')
    for t in range(2):
        for g in group:
            for i, s in enumerate(generators):
                require(actions[i][512*t+labels[t][g]] == 512*t+labels[t][product(g, s)],
                        'Coset action well-defined on both members')
    action = {}
    for g in group:
        a = tuple(range(WIDTH))
        for i in words[g]:
            a = product(a, actions[i])
        action[gid[g]] = a
    for g in range(len(group)):
        for i in range(4):
            require(product(action[g], actions[i]) == action[edges[g][i]],
                    'Full finite action does not respect multiplication')
    inv_action = {g: inverse(a) for g, a in action.items()}
    shifts = [ZERO, minus(unit(512+labels[1][identity]), unit(512+labels[1][generators[1]])),
              minus(unit(labels[0][generators[2]]), unit(labels[0][identity])), ZERO]

    def evaluate(word):
        g, v = one, ZERO
        for i in word:
            g, v = edges[g][i], plus(move(v, actions[i]), shifts[i])
        return g, v

    for i in range(4):
        require(evaluate([i, i]) == (one, ZERO), 'Affine involution equation')
    for i, j in [(0, 2), (0, 3), (1, 3)]:
        require(evaluate([i, j]) == evaluate([j, i]), 'Affine string commutation')

    parabolics = {}
    for subset in range(16):
        indices = [i for i in range(3, -1, -1) if subset & (1 << i)]
        lifts = {one: ZERO}
        pending = deque([one])
        while pending:
            g = pending.popleft()
            for i in indices:
                dest = edges[g][i]
                if dest not in lifts:
                    lifts[dest] = plus(move(lifts[g], actions[i]), shifts[i])
                    pending.append(dest)
        kernel = Basis()
        for g, v in lifts.items():
            for i in indices:
                dest = edges[g][i]
                difference = minus(plus(move(v, actions[i]), shifts[i]), lifts[dest])
                # Translation of h_g rho_i h_dest^-1: actual Schreier generator.
                kernel.insert(move(difference, inv_action[dest]))
        require(all(kernel.contains(move(v, actions[i])) for v in kernel.vectors() for i in indices),
                'Full Schreier span not invariant')
        parabolics[subset] = dict(indices=sorted(indices), lifts=lifts, kernel=kernel)
    rel_base, c = evaluate([1, 2] * 4)
    require(rel_base == one and c != ZERO, 'Literal killed relator')
    killed = Basis(move(c, action[g]) for g in range(len(group)))
    full = parabolics[15]['kernel']
    require(all(full.contains(v) for v in killed.vectors()), 'Killed orbit outside full kernel')
    require(all(killed.contains(move(v, a)) for v in killed.vectors() for a in actions),
            'Killed orbit span is not invariant')
    require((len(full), len(killed)) == (257, 127), 'Full or killed rank')
    augmented = {s: span(p['kernel'], killed) for s, p in parabolics.items()}
    dimensions = {s: len(v)-len(killed) for s, v in augmented.items()}
    pairs = []
    for left in range(16):
        for right in range(left, 16):
            common = left & right
            pa, pb, pc = [parabolics[s] for s in [left, right, common]]
            combined = span(augmented[left], augmented[right])
            intersection_dimension = len(augmented[left])+len(augmented[right])-len(combined)-len(killed)
            require(all(augmented[left].contains(v) and augmented[right].contains(v)
                        for v in augmented[common].vectors()), 'Common marked translation inclusion')
            require(intersection_dimension == dimensions[common], 'Wrong translation intersection')
            projected = sorted(set(pa['lifts']) & set(pb['lifts']))
            unwanted = []
            for g in projected:
                delta = minus(pa['lifts'][g], pb['lifts'][g])
                compatible = combined.contains(delta)
                require(compatible == (g in pc['lifts']), 'Affine fiber compatibility differs from IP')
                if not compatible:
                    unwanted.append(g)
            pairs.append(dict(left=pa['indices'], right=pb['indices'], common=pc['indices'],
                              projected_intersection=len(projected),
                              translation_intersection_dimension=intersection_dimension,
                              forbidden_projected_elements=unwanted, IP=True))
    require(len(pairs) == 136, 'All unordered subset pairs')
    orders = []
    for i in range(3):
        found = [n for n in range(1, 25)
                 if (lambda gv: gv[0] == one and killed.contains(gv[1]))(evaluate([i, i+1]*n))]
        require(found, 'Adjacent order not bounded')
        orders.append(min(found))
    require(orders == [24, 4, 24], 'Exact type')

    # Only for decoding published coordinates/element numbers, reconstruct its
    # documented BFS ordering. No author code, basis, or verdict is imported.
    published_group = list(closure(list(enumerate(generators)), identity))
    published_to_new = []
    for t, s in enumerate([generators[0], generators[3]]):
        encountered = set()
        for g in published_group:
            if g not in encountered:
                encountered.update([g, product(s, g)])
                published_to_new.append(512*t+labels[t][g])
    require(sorted(published_to_new) == list(range(WIDTH)), 'Published coordinate translation')

    def decode(entries):
        require(len({j for j, x in entries}) == len(entries), 'Repeated sparse coordinate')
        require(all(0 <= j < WIDTH and x in [1, 2] for j, x in entries), 'Invalid sparse coefficient')
        result = ZERO
        for j, x in entries:
            u = unit(published_to_new[j])
            result = plus(result, u if x == 1 else neg(u))
        return result

    require([decode(s) for s in certificate['shifts']] == shifts, 'Certificate shifts')
    require(decode(certificate['killed_relation_vector']) == c, 'Certificate literal relator vector')
    require(certificate['killed_relation_word_0based'] == [1, 2]*4, 'Certificate relator word')
    require(same_space(Basis(map(decode, certificate['generated_kernel_basis'])), full),
            'Certificate full kernel basis differs')
    require(same_space(Basis(map(decode, certificate['killed_invariant_basis'])), killed),
            'Certificate killed basis differs')
    for p in certificate['parabolics']:
        s = sum(1 << i for i in p['indices'])
        own = parabolics[s]
        require(p['base_order'] == len(own['lifts']) and p['raw_kernel_dimension'] == len(own['kernel']),
                'Certificate parabolic dimensions')
        require(same_space(Basis(map(decode, p['raw_kernel_basis'])), own['kernel']),
                'Certificate raw parabolic basis differs')
    remainder_checks = 0
    for row in certificate['recursive_intersection_tests']:
        ia, ib, ic = [sum(1 << i for i in row[k]) for k in ['A', 'B', 'C']]
        a, b, cpar = [parabolics[s] for s in [ia, ib, ic]]
        comparison = span(augmented[ia], augmented[ib])
        expected_forbidden = (set(a['lifts']) & set(b['lifts'])) - set(cpar['lifts'])
        listed = set()
        for item in row['forbidden_base_cosets']:
            g = gid[published_group[item['base_element']]]
            listed.add(g)
            remainder = decode(item['nonzero_remainder'])
            delta = minus(a['lifts'][g], b['lifts'][g])
            require(not comparison.contains(remainder) and comparison.contains(minus(delta, remainder)),
                    'Published separating remainder has wrong quotient class')
            remainder_checks += 1
        require(listed == expected_forbidden, 'Published forbidden elements not complete')
        require(row['base_orders'] == [len(x['lifts']) for x in [a, b, cpar]], 'Published base orders')
        require(row['image_kernel_dimensions'] == [dimensions[s] for s in [ia, ib, ic]],
                'Published quotient dimensions')
    require(remainder_checks == 8, 'Eight separating remainder classes')
    require(all(binding(root / name) == rec for name, rec in records.items()), 'Original inputs changed')
    report = dict(status='PASS', date='2026-10-10', seconds=time.monotonic()-started,
                  checker=binding(Path(__file__)), reviewed_inputs=records,
                  arithmetic='Independent two-bit-plane exact F3 addition; highest-coordinate pivots; no author module import',
                  enumeration='Lexicographically numbered base permutations and module cosets; reversed-generator Schreier transversals',
                  kernel_method='All actual h_g rho_i h_(g rho_i)^(-1) translation vectors, with inverse-base action; no invariant saturation needed. Invariance separately verified.',
                  base_order=len(group), module_dimension=WIDTH,
                  generated_kernel_dimension=len(full), killed_dimension=len(killed),
                  quotient_kernel_dimension=len(full)-len(killed), exact_type=orders,
                  all_subset_pairs_checked=len(pairs), all_pairs=pairs,
                  parabolics=[dict(indices=p['indices'], projected_order=len(p['lifts']),
                                   raw_kernel_dimension=len(p['kernel']), quotient_kernel_dimension=dimensions[s])
                              for s, p in parabolics.items()],
                  all_published_basis_spaces_equal=True,
                  all_published_separating_remainder_classes_checked=remainder_checks,
                  original_bindings_unchanged=True, author_program_imported=False,
                  phase102_uniform_proof_checked_by_program=False,
                  scope='Independent exact fixed-model affine calculation; uniform transport and geometric/minimality interpretation require the separate mathematical audit.')
    out.mkdir(parents=False)
    with (out / 'report.json').open('x') as f:
        json.dump(report, f, indent=2)
        f.write('\n')
    print(json.dumps(dict(status='PASS', seconds=report['seconds'], ranks=[len(full), len(killed)],
                          all_subset_pairs=len(pairs), report=binding(out / 'report.json')), indent=2))


if __name__ == '__main__':
    main()
