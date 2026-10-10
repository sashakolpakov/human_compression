#!/usr/bin/env python3
"""Independent checker: block normal forms and full affine enumeration.

Imports no author or earlier-checker routines. Finite certificate interpretation
and the uniform source-family proof are recorded separately in the review.
"""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path


FREE = [1,2,4,5,6,8,9,10,12,14,16,19,21,25,32]
BINDS = {
    'phase92_complement_normal_form_manifest.json': '9695071d5fe0b2ceba04250d772b76ecf669959d22b109c553b2bfbd691414b9',
    'phase92_complement_normal_form_certificate.json': 'aa8b3b608f75c4c6280341f492d784d0fbbb360f3ea9c3fcd344d07892120dfc',
    'phase66_coprime_cover_permutation_model.json': '0247990a79729513799e8fe85d49dec74fade6b32a9aff8746a3fa4c0e8a2338',
    'phase83_word_elimination.json': 'd6cdcab4ea0bfd9a9a75255d5a1da0a1a589306c803d330b0a7a7b659ab86c17',
}


def need(ok, label):
    if not ok:
        raise ValueError(label)


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def inverse(w):
    return [-v for v in w[::-1]]


def freely(w):
    stack = []
    for v in w:
        if stack and stack[-1] == -v:
            stack.pop()
        else:
            stack.append(v)
    return stack


def replace(w, mapping):
    return freely(v for k in w for v in
                  (mapping[abs(k)] if k > 0 else inverse(mapping[abs(k)])))


def block_normal(w):
    # Alternating whole free-group blocks and Klein-four elements.
    blocks = []
    for v in w:
        need(1 <= abs(v) <= 18, 'normal alphabet')
        if abs(v) <= 15:
            if blocks and blocks[-1][0] == 'F':
                block = blocks.pop()[1]
                block = freely(block + [v])
                if block:
                    blocks.append(('F', block))
            else:
                blocks.append(('F', [v]))
        else:
            bits = abs(v) - 15
            if blocks and blocks[-1][0] == 'K':
                bits ^= blocks.pop()[1]
            if bits:
                blocks.append(('K', bits))
    return [v for kind, value in blocks for v in
            (value if kind == 'F' else [15 + value])]


def pmul(p, q):
    return tuple(q[i] for i in p)


def generated(gens, identity):
    seen = {identity}
    pending = deque([identity])
    while pending:
        g = pending.popleft()
        for s in gens:
            v = pmul(g, s)
            if v not in seen:
                seen.add(v)
                pending.append(v)
    return seen


def parity(word):
    out = 0
    for v in word:
        if abs(v) <= 15:
            out ^= 1 << (abs(v) - 1)
        else:
            out ^= (abs(v) - 15) << 15
    return out


def lin(columns, vector):
    return __import__('functools').reduce(int.__xor__,
        (columns[i] for i in range(17) if (vector >> i) & 1), 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    need(not args.output.exists() and not args.output.is_symlink(), 'fresh output required')
    for name, expected in BINDS.items():
        need(digest(args.base / name) == expected, 'hash mismatch: ' + name)
    cert = json.loads((args.base / 'phase92_complement_normal_form_certificate.json').read_text())
    trace = json.loads((args.base / 'phase83_word_elimination.json').read_text())
    model = json.loads((args.base / 'phase66_coprime_cover_permutation_model.json').read_text())
    gens = [tuple(i - 1 for i in row) for row in model['generators']]
    identity = tuple(range(128))
    group = generated(gens, identity)
    need(len(group) == 1024, 'base order')
    ordered = [identity] + sorted(group - {identity})
    gi = {g: i for i, g in enumerate(ordered)}
    edges = [[gi[pmul(g, s)] for s in gens] for g in ordered]
    quads = sorted({tuple(g[p] + 1 for p in [0,1,38,76]) for g in group})
    need([list(q) for q in quads] == trace['quads'], 'original cell inventory')
    original = [[-d,c,-a,b] for a,b,c,d in quads]
    need(original == trace['originals'], 'original words')

    # Derive every elimination again from its current defining equation.
    active = dict(enumerate(original))
    expansion = {i:[i] for i in range(1,129)}
    deleted = set()
    for step in trace['steps']:
        row, v = step['relation'], step['variable']
        need(row in active and v not in deleted, 'invalid elimination index')
        w = active[row]
        need(w == step['before'], 'before word')
        positions = [j for j,k in enumerate(w) if abs(k) == v]
        need(len(positions) == 1, 'nonunique solved variable')
        j = positions[0]
        left, right = w[:j], w[j+1:]
        solved = freely(inverse(left) + inverse(right) if w[j] > 0 else right + left)
        need(v not in map(abs,solved) and solved == step['replacement'], 'solved expression')
        images = {i:[i] for i in range(1,129)}
        images[v] = solved
        need(replace(w, images) == [], 'equation not solved')
        active = {r:replace(t,images) for r,t in active.items() if r != row}
        active = {r:t for r,t in active.items() if t}
        expansion = {i:replace(t,images) for i,t in expansion.items()}
        deleted.add(v)
    need(len(deleted) == 111 and len(active) == 512, 'elimination totals')
    need(expansion == {int(k):v for k,v in cert['original_generator_survivor_expansions'].items()}, 'expansions')
    fwd = {s:[i+1] for i,s in enumerate(FREE)}
    fwd[7] = [5,16]
    fwd[3] = [1,17,-5,9]
    back = {i+1:[s] for i,s in enumerate(FREE)}
    back[16], back[17] = [-6,7], [-1,3,-12,6]
    need(all(replace(v,back) == [k] for k,v in fwd.items()), 'basis composite one')
    need(all(replace(v,fwd) == [k] for k,v in back.items()), 'basis composite two')
    transformed = {r:replace(w,fwd) for r,w in active.items()}
    need(transformed[30] == [-7,1,17,17,-1,7], 'Y-square witness')
    need(transformed[67] == [-9,5,16,16,-5,9], 'X-square witness')
    need(transformed[176] == [-17,-16,17,16], 'commutator witness')
    need(all(block_normal(w) == [] for w in transformed.values()), 'residual relation')
    normal_images = {i:block_normal(replace(w,fwd)) for i,w in expansion.items()}
    need(normal_images == {int(k):v for k,v in cert['original_generator_target_normal_forms'].items()}, 'forward images')
    need(all(block_normal(replace(w,normal_images)) == [] for w in original), 'original relation')
    need(block_normal(inverse(normal_images[1])+normal_images[40]) == [16], 'marked defect')
    actions = []
    for s in gens:
        action = {i:block_normal(replace([s[abs(k)-1]+1 if k > 0 else -(s[abs(k)-1]+1) for k in w],normal_images)) for i,w in back.items()}
        actions.append(action)
    need(actions == [{int(k):v for k,v in a.items()} for a in cert['action_generator_images']], 'marked automorphisms')
    a = [-2,1]
    need([(s[16],s[17]) for s in actions] == [([18],[17]),([16],[17]),([16],[17]),(a+[18]+inverse(a),a+[17]+inverse(a))], 'displayed finite-factor action')
    matrices = [[parity(action[i]) for i in range(1,18)] for action in actions]
    need(matrices == cert['mod2_module']['action_columns'], 'binary columns')

    # Verify the matrices define the actual 1024-element group action.
    allmat = {0:tuple(1 << i for i in range(17))}
    todo = deque([0])
    checked = 0
    while todo:
        g = todo.popleft()
        for j, m in enumerate(matrices):
            nxt = edges[g][j]
            image = tuple(lin(m,v) for v in allmat[g])
            if nxt in allmat:
                need(image == allmat[nxt], 'binary action multiplication')
            else:
                allmat[nxt] = image
                todo.append(nxt)
            checked += 1
    need(len(allmat) == 1024 and checked == 4096, 'binary action coverage')

    def affine(indices, quotient=False):
        mask = (1 << 16) - 1 if quotient else (1 << 17) - 1
        seen = {(0,0)}
        todo = deque([(0,0)])
        while todo:
            g,v = todo.popleft()
            for j in indices:
                w = (lin(matrices[j],v) ^ (3 if j == 3 else 0)) & mask
                nxt = (edges[g][j],w)
                if nxt not in seen:
                    seen.add(nxt)
                    todo.append(nxt)
        return seen

    full = affine(range(4))
    kernel = {v for g,v in full if g == 0}
    need(len(full) == 4096 and kernel == {0,32768,65536,98304}, 'full affine enumeration')
    ends = [affine(range(3)), affine(range(1,4))]
    medial = affine([1,2])
    need([len(x) for x in ends] == [128,128] and len(medial) == 8 and ends[0]&ends[1] == medial, 'affine end intersection')
    need(all(len({g for g,v in e}) == len(e) for e in ends), 'affine end projection injectivity')
    stable = [v for v in sorted(kernel-{0}) if all(lin(m,v) == v for m in matrices)]
    need(stable == [65536], 'unique invariant line')
    double = affine(range(4), quotient=True)
    need(len(double) == 2048 and {v for g,v in double if g == 0} == {0,32768}, 'double quotient enumeration')

    # Check the literal original free-edge set, independently of the author tree algorithm.
    parts = []
    for local in [gens[:3],gens[1:]]:
        loc = generated(local,identity)
        base = {g[0] for g in loc}
        parts.append(sorted({tuple(sorted(g[i]+1 for i in base)) for g in group}))
    need(parts[0] == [tuple(x) for x in cert['coset_square_complex']['A_blocks']], 'A blocks')
    need(parts[1] == [tuple(x) for x in cert['coset_square_complex']['B_blocks']], 'B blocks')
    incidence = [{e:i for i,block in enumerate(part) for e in block} for part in parts]
    graph = {i:set() for i in range(16)}
    for edge in FREE:
        u,v = incidence[0][edge],8+incidence[1][edge]
        graph[u].add(v); graph[v].add(u)
    reached, pending = {0}, deque([0])
    while pending:
        for v in graph[pending.popleft()]:
            if v not in reached:
                reached.add(v);pending.append(v)
    need(len(reached) == 16 and sum(map(len,graph.values())) == 30, 'specified edge set not a tree')
    for name, expected in BINDS.items():
        need(digest(args.base / name) == expected, 'changed input: '+name)
    report = {'status':'PASS','inputs':BINDS,'eliminations':111,'free_basis_composites':34,
        'original_relations':1024,'residual_relations':512,'independent_normal_form':'alternating whole free-group and V4 blocks',
        'three_literal_reverse_witnesses':True,'displayed_action_table':True,
        'binary_group_action_edges':checked,'explicit_affine_group_order':len(full),
        'explicit_affine_kernel':sorted(kernel),'affine_end_orders':[len(e) for e in ends],
        'affine_end_intersection_order':len(ends[0]&ends[1]),'both_affine_end_projections_injective':True,
        'unique_invariant_line_generator':stable[0],'explicit_double_quotient_order':len(double),
        'specified_original_edges_form_tree':True,'author_code_imported':False,
        'scope':'Exact finite certificate and conventions only. Uniform transport and all-cover completeness use the separately reviewed written proof.'}
    with args.output.open('x') as out:
        json.dump(report,out,indent=2,sort_keys=True);out.write('\n')
    print(json.dumps({'status':'PASS','affine_group_order':len(full),'output':str(args.output)}))


if __name__ == '__main__':
    main()
