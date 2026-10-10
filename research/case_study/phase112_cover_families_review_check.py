#!/usr/bin/env python3
"""Independent F3/F5 all-parabolic audit, public-only by default.

Dense coefficient arithmetic, highest pivots, reversed Schreier transversals.
The author program is never imported. Optional primary-source hash audit is
separate from the public-only finite calculation and mathematical review.
"""
import argparse
from collections import deque
import hashlib
import itertools
import json
import os
from pathlib import Path
import time

MANIFEST = 'phase109_cover_families_generalization_manifest.json'
MANIFEST_SHA = '33ba4410188b8d6c3b4a0c205d94940155682084294bd858db0637ec3e07c136'
MODEL = 'phase109_cover_families_generalization_model.json'
CERTIFICATE = 'phase109_cover_families_generalization_certificate.json'
WIDTH = 256
ZERO = (0,) * WIDTH
FIELD = None


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def binding(path):
    raw = path.read_bytes()
    return dict(sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))


def plus(a, b):
    return tuple((x+y) % FIELD for x, y in zip(a, b))


def neg(v):
    return tuple(-x % FIELD for x in v)


def minus(a, b):
    return tuple((x-y) % FIELD for x, y in zip(a, b))


def move(v, permutation):
    out = [0] * WIDTH
    for i, x in enumerate(v):
        out[permutation[i]] = x
    return tuple(out)


def unit(j):
    return tuple(int(i == j) for i in range(WIDTH))


class Basis:
    """Highest-coordinate exact elimination on dense integer coefficient tuples."""
    def __init__(self, vectors=()):
        self.rows = {}
        for v in vectors:
            self.insert(v)

    def reduce(self, v):
        v = list(v)
        for p in range(WIDTH - 1, -1, -1):
            x = v[p]
            if not x:
                continue
            row = self.rows.get(p)
            if row is None:
                # Lower existing pivots do not affect the missing leading pivot.
                break
            for i in range(p + 1):
                v[i] = (v[i] - x * row[i]) % FIELD
        return tuple(v)

    def insert(self, v):
        v = self.reduce(v)
        if v == ZERO:
            return False
        p = max(i for i, x in enumerate(v) if x)
        inverse = pow(v[p], -1, FIELD)
        self.rows[p] = tuple(x * inverse % FIELD for x in v)
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


def calculate(model, certificate, field):
    global FIELD
    FIELD = field
    generators = [tuple(x - 1 for x in p) for p in model['generators']]
    identity = tuple(range(model['degree']))
    require(len(generators) == 4 and len(identity) == 16, 'Base model degree')
    for s in generators:
        require(sorted(s) == list(identity) and s != identity and product(s, s) == identity,
                'Nontrivial base involution')
    require(len(set(generators)) == 4, 'Distinct base marks')
    words = closure(list(reversed(list(enumerate(generators)))), identity)
    group = sorted(words)
    require(len(group) == 256, 'Fixed group order')
    gid = {g: i for i, g in enumerate(group)}
    one = gid[identity]
    edges = [[gid[product(g, s)] for s in generators] for g in group]


    def pwr(g, n):
        out = identity
        base = g if n >= 0 else tuple(inverse(g))
        for _ in range(abs(n)):
            out = product(out, base)
        return out
    def mul(*items):
        out = identity
        for item in items:
            out = product(out, item)
        return out
    a, b, c = [product(generators[i], generators[i+1]) for i in range(3)]
    require(all(pwr(x,4)==identity and pwr(x,2)!=identity for x in [a,b,c]), 'Base type 444')
    require(all(pwr(x,2)==identity for x in [mul(a,b),mul(b,c),mul(a,b,c)]), 'Rotation square relations')
    # These are literal LHS times inverse RHS, after reducing q/4 and e mod4.
    defects = [mul(b,pwr(a,2),pwr(b,-1),pwr(a,-2)),
               mul(pwr(c,2),b,pwr(c,-2),pwr(b,-1)),
               mul(pwr(b,-1),a,pwr(b,3),a),
               mul(b,pwr(a,-1),pwr(b,-3),pwr(a,-1)),
               mul(pwr(c,-1),b,pwr(c,-1),pwr(b,-3)),
               mul(c,pwr(b,-1),c,pwr(b,3))]
    kappa = defects[0]
    require(kappa != identity and pwr(kappa,2)==identity and all(x==kappa for x in defects), 'Six reduced source words')
    require(all(product(kappa,s)==product(s,kappa) for s in generators), 'Central reduced defect')

    # Independent lexicographic coset labels, rather than the author's BFS labels.
    labels, representatives = [], []
    for s in [generators[0], generators[3]]:
        representatives.append(sorted({min(g, product(s, g)) for g in group}))
        index = {g: i for i, g in enumerate(representatives[-1])}
        labels.append({g: index[min(g, product(s, g))] for g in group})
        require(len(index) == 128, 'Coset count')
    actions = []
    for s in generators:
        actions.append([128 * t + labels[t][product(g, s)]
                        for t in range(2) for g in representatives[t]])
    for a in actions:
        require(sorted(a) == list(range(WIDTH)), 'Module generator bijection')
    for t in range(2):
        for g in group:
            for i, s in enumerate(generators):
                require(actions[i][128*t+labels[t][g]] == 128*t+labels[t][product(g, s)],
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
    shifts = [ZERO, minus(unit(128+labels[1][identity]), unit(128+labels[1][generators[1]])),
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
    require(gid[kappa] in parabolics[7]['lifts'] and gid[kappa] in parabolics[14]['lifts'] and gid[kappa] not in parabolics[6]['lifts'], 'Reduced defect/end interface')
    require([len(parabolics[x]['lifts']) for x in [7,14,6]] == [64,64,8], 'Base end and medial orders')
    require(len(set(parabolics[7]['lifts']) & set(parabolics[14]['lifts'])) == 16, 'Base end intersection')
    rel_base, c = evaluate([1, 2] * 4)
    require(rel_base == one and c != ZERO, 'Literal killed relator')
    killed = Basis(move(c, action[g]) for g in range(len(group)))
    full = parabolics[15]['kernel']
    require(all(full.contains(v) for v in killed.vectors()), 'Killed orbit outside full kernel')
    require(all(killed.contains(move(v, a)) for v in killed.vectors() for a in actions),
            'Killed orbit span is not invariant')
    require((len(full), len(killed)) == (65, 31), 'Full or killed rank')
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
    require(orders == [4*FIELD, 4, 4*FIELD], 'Exact type')

    # Only for decoding published coordinates/element numbers, reconstruct its
    # documented BFS ordering. No author code, basis, or verdict is imported.
    published_group = list(closure(list(enumerate(generators)), identity))
    published_to_new = []
    for t, s in enumerate([generators[0], generators[3]]):
        encountered = set()
        for g in published_group:
            if g not in encountered:
                encountered.update([g, product(s, g)])
                published_to_new.append(128*t+labels[t][g])
    require(sorted(published_to_new) == list(range(WIDTH)), 'Published coordinate translation')

    def decode(entries):
        require(len({j for j, x in entries}) == len(entries), 'Repeated sparse coordinate')
        require(all(0 <= j < WIDTH and 1 <= x < FIELD for j, x in entries), 'Invalid sparse coefficient')
        result = ZERO
        for j, x in entries:
            u = unit(published_to_new[j])
            result = plus(result, tuple(x * z % FIELD for z in u))
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
    require(certificate['field'] == FIELD and certificate['base_order']==256 and certificate['ambient_module_dimension']==256, 'Certificate field/base/dimension')
    require(certificate['generated_kernel_dimension']==65 and certificate['killed_invariant_dimension']==31 and certificate['cover_kernel_dimension']==34, 'Certificate global dimensions')
    require(certificate['cover_degree']==str(FIELD)+'^34' and certificate['full_fixed_order']=='256*'+str(FIELD)+'^34', 'Certificate exact degree/order')
    require(certificate['fixed_cover_type']==orders and certificate['base_marked_orders']==[4,4,4], 'Certificate marked orders')
    require(certificate['six_reduced_source_relators_equal_central_involution'] is True and certificate['defect_outside_medial_and_in_both_ends'] is True, 'Certificate source-interface flags')
    require(published_group[certificate['common_reduced_source_defect']]==kappa, 'Certificate marked defect')
    return dict(field=FIELD, base_order=len(group), module_dimension=WIDTH,
                generated_kernel_dimension=len(full), killed_dimension=len(killed),
                quotient_kernel_dimension=len(full)-len(killed), exact_type=orders,
                exact_cover_degree=FIELD**34, exact_cover_order=256*FIELD**34,
                all_subset_pairs_checked=len(pairs), all_pairs=pairs,
                parabolics=[dict(indices=p['indices'], projected_order=len(p['lifts']),
                                 raw_kernel_dimension=len(p['kernel']), quotient_kernel_dimension=dimensions[sub])
                            for sub,p in parabolics.items()],
                all_published_basis_spaces_equal=True,
                all_published_separating_remainder_classes_checked=remainder_checks,
                six_literal_reduced_source_words_verified=True,
                defect_outside_medial_and_in_both_ends=True)



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-root', type=Path, default=Path(__file__).resolve().parent,
                        help='Directory containing the exact nine public phase109 exports')
    parser.add_argument('--private-source-root', type=Path,
                        help='Optional additional original/context/combined-theorem bindings; not needed for finite replay')
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    root, out = args.input_root.resolve(), args.output_dir.absolute()
    require(not os.path.lexists(out), 'Fresh independent output required')
    started = time.monotonic()
    require(binding(root / MANIFEST)['sha256'] == MANIFEST_SHA, 'Frozen author manifest differs')
    manifest = json.loads((root / MANIFEST).read_text())
    records = {MANIFEST: binding(root / MANIFEST)}
    for name, record in manifest['files'].items():
        require(binding(root / name) == record, 'Frozen public input differs: ' + name)
        records[name] = record
    require(set(manifest['export_allowlist']) == set(records), 'Exact nine public inputs')
    private_records = {}
    if args.private_source_root is not None:
        for kind in ['private_primary_bindings_not_exported', 'five_family_combination_only_dependencies', 'context_only_not_proof_premises']:
            for name, record in manifest[kind].items():
                require(binding(args.private_source_root / name) == record, 'Optional original binding differs: '+name)
                private_records[name] = record
    model = json.loads((root / MODEL).read_text())
    certificate = json.loads((root / CERTIFICATE).read_text())
    require([x['field'] for x in certificate['fields']] == [3,5], 'Two separate fields required')
    results = [calculate(model, cert, field) for cert,field in zip(certificate['fields'], [3,5])]
    require(all(binding(root / name) == rec for name,rec in records.items()), 'Public inputs changed')
    require(all(binding(args.private_source_root / name) == rec for name,rec in private_records.items()), 'Optional originals changed')
    report = dict(status='PASS', date='2026-10-10', seconds=time.monotonic()-started,
                  checker=binding(Path(__file__)), public_reviewed_inputs=records,
                  optional_original_bindings=private_records,
                  default_replay_requires_private_files=False,
                  arithmetic='Independent dense integer coefficient tuples over F3 and F5; highest-coordinate pivots; no author module import',
                  enumeration='Lexicographically numbered base permutations/module cosets; reversed-generator Schreier transversals',
                  kernel_method='Actual h_g rho_i h_(g rho_i)^(-1) translation generators, including inverse-base action; separate invariance check, no invariant saturation',
                  fields=results, all_subset_pairs_checked=sum(r['all_subset_pairs_checked'] for r in results),
                  original_bindings_unchanged=True, author_program_imported=False,
                  uniform_proof_checked_by_program=False,
                  scope='Exact two-field fixed-model affine arithmetic; uniform source transport, geometry and minimality require the written independent audit')
    out.mkdir(parents=False)
    with (out/'report.json').open('x') as f:
        json.dump(report,f,indent=2);f.write('\n')
    print(json.dumps(dict(status='PASS',seconds=report['seconds'],all_subset_pairs=272,report=binding(out/'report.json')),indent=2))


if __name__ == '__main__':
    main()
