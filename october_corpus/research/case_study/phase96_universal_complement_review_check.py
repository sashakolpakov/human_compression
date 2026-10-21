#!/usr/bin/env python3
"""Independent finite diagnostics for the written phase90 bridge; not its proof.

Uses only the standard library, original permutations and elementary free words.
No author graph, elimination, spanning-tree or phase92 routine is imported.
"""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mul(p, q):
    """Right action: apply p, then q."""
    return tuple(q[i] for i in p)


def subgroup(gens, identity):
    seen = {identity}
    queue = deque([identity])
    while queue:
        p = queue.popleft()
        for q in gens:
            x = mul(p, q)
            if x not in seen:
                seen.add(x)
                queue.append(x)
    return seen


def cosets(group, local):
    remain = set(group)
    labels, parts = {}, []
    while remain:
        g = min(remain)
        part = {mul(h, g) for h in local}
        require(part <= remain, 'cosets overlap')
        label = len(parts)
        for h in part:
            labels[h] = label
        parts.append(part)
        remain -= part
    return labels, parts


def inv(w):
    return tuple(-x for x in reversed(w))


def red(w):
    out = []
    for x in w:
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    return tuple(out)


def subst(w, images):
    return red(y for x in w for y in (images[x] if x > 0 else inv(images[-x])))


def run_case(name, gens, expected):
    identity = tuple(range(len(gens[0])))
    require(all(mul(g, g) == identity for g in gens), 'involutions')
    require(all(mul(gens[i], gens[j]) == mul(gens[j], gens[i])
                for i in range(4) for j in range(i + 2, 4)), 'string commutations')
    group = subgroup(gens, identity)
    A = subgroup(gens[:3], identity)
    B = subgroup(gens[1:], identity)
    C = subgroup(gens[1:3], identity)
    I = A & B
    ea, pa = cosets(group, A)
    eb, pb = cosets(group, B)
    ec, pc = cosets(group, C)
    na, nb, ne = len(pa), len(pb), len(pc)
    endpoints = []
    for part in pc:
        require(len({ea[g] for g in part}) == len({eb[g] for g in part}) == 1,
                'edge endpoint not well-defined')
        g = min(part)
        endpoints.append((na + eb[g], ea[g]))
    root = ea[identity]
    adjacency = [[] for _ in range(na + nb)]
    for e, (u, v) in enumerate(endpoints, 1):
        adjacency[u].append((v, e))
        adjacency[v].append((u, -e))
    paths = {root: ()}
    tree = set()
    queue = deque([root])
    while queue:
        u = queue.popleft()
        for v, signed in adjacency[u]:
            if v not in paths:
                paths[v] = paths[u] + (signed,)
                tree.add(abs(signed))
                queue.append(v)
    require(len(paths) == na + nb and len(tree) == na + nb - 1, 'not a tree')

    # New free generators retain old tree labels; loop labels exceed ne.
    forward, backward, loop_images = {}, {}, {}
    for e, (u, v) in enumerate(endpoints, 1):
        se = () if e in tree else (ne + e,)
        loop_images[e] = se
        forward[e] = inv(paths[u]) + se + paths[v]
        if e in tree:
            backward[e] = (e,)
        else:
            backward[ne + e] = paths[u] + (e,) + inv(paths[v])
    require(all(subst(forward[e], backward) == (e,) for e in forward),
            'edge change is not invertible')
    require(all(subst(w, forward) == (e,) for e, w in backward.items()),
            'inverse change is not invertible')

    def closes(word, start):
        pos = start
        for signed in word:
            u, v = endpoints[abs(signed) - 1]
            if signed < 0:
                u, v = v, u
            if u != pos:
                return False
            pos = v
        return pos == start

    words = []
    for g in sorted(group):
        a = ec[g] + 1
        b = ec[mul(gens[3], g)] + 1
        c = ec[mul(gens[0], g)] + 1
        d = ec[mul(mul(gens[3], gens[0]), g)] + 1
        w = (-d, c, -a, b)
        start = ea[mul(gens[3], g)]
        require(closes(w, start), 'square boundary orientation')
        require(not closes((d, c, -a, b), start), 'broken-square adverse control')
        transformed = subst(w, forward)
        square_loop = subst(w, loop_images)
        require(transformed == red(inv(paths[start]) + square_loop + paths[start]),
                'tree factors do not telescope')
        words.append(w)

    defects = sorted({ec[g] + 1 for g in I})
    for e in defects:
        w = (-(ec[identity] + 1), e)
        require(closes(w, root), 'defect not a root loop')
        require(subst(w, forward) == subst(w, loop_images), 'defect has tree factors')
    require(len(defects) * len(C) == len(I), 'defect coset index')
    counts = [len(group), len(A), len(B), len(C), len(I), ne, na, nb, len(tree)]
    require(counts == expected, f'{name}: unexpected exact counts {counts}')
    return {
        'name': name, 'group_A_B_C_I_orders': counts[:5],
        'edges': ne, 'A_vertices': na, 'B_vertices': nb,
        'spanning_tree_edges_1based': sorted(tree),
        'graph_free_rank': ne - na - nb + 1,
        'all_ordered_cells_checked': len(words),
        'distinct_literal_cells': len(set(words)),
        'defect_edge_labels_1based': defects,
        'change_of_free_generators_checked_both_directions': True,
        'every_square_tree_telescope_and_every_defect_checked': True,
        'reversed_first_edge_adverse_control_rejected_for_every_cell': True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), 'refusing to overwrite existing output')
    names = {
        'phase90_universal_complement_bridge_manifest.json': 'b30ddbcf0cecca56ab7584f21aa4ec47fd12ca077c3adb6a29d6b1a6e1c51d7c',
        'phase90_universal_complement_bridge.md': '685ad72ffa0c9964693d54a52e3ee79d6b7d754c1b4c520d2b0eabe7087c50c3',
        'phase90_universal_complement_bridge_ledger.json': '2b4d84af8550e242560acd70d1f3557b109d7158fdcf4b9cb733851b6ceaa2f9',
        'phase66_coprime_cover_permutation_model.json': '0247990a79729513799e8fe85d49dec74fade6b32a9aff8746a3fa4c0e8a2338',
    }
    for name, expected in names.items():
        require(sha(args.base / name) == expected, f'input hash mismatch: {name}')
    m = json.loads((args.base / 'phase66_coprime_cover_permutation_model.json').read_text())
    gens = [tuple(i - 1 for i in g) for g in m['generators']]
    result = [run_case('Gamma2_quotient_1024', gens, [1024, 128, 128, 8, 16, 128, 8, 8, 15])]
    s5 = []
    for i in range(4):
        g = list(range(5))
        g[i], g[i + 1] = g[i + 1], g[i]
        s5.append(tuple(g))
    result.append(run_case('S5_adjacent_transpositions', s5, [120, 24, 24, 6, 6, 20, 5, 5, 9]))
    for name, expected in names.items():
        require(sha(args.base / name) == expected, f'input changed: {name}')
    payload = {
        'status': 'PASS', 'input_bindings': names, 'cases': result,
        'scope': 'Independent finite diagnostics only. Written uniform proof is reviewed separately. No phase92 classification or infinite-parameter inference.',
    }
    with args.output.open('x') as out:
        json.dump(payload, out, indent=2, sort_keys=True)
        out.write('\n')
    print(json.dumps({'status': 'PASS', 'cases': len(result), 'output': str(args.output)}))


if __name__ == '__main__':
    main()
