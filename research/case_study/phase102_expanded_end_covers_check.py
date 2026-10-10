#!/usr/bin/env python3
"""Exact F3 affine cover with expanded ends; no group-size enumeration.

The proof of completeness of the kernel/intersection calculations is supplied
in the accompanying manuscript. All arithmetic here is exact modulo three.
"""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parent
MODEL = 'phase66_coprime_cover_permutation_model.json'
MODEL_SHA = '0247990a79729513799e8fe85d49dec74fade6b32a9aff8746a3fa4c0e8a2338'
FIELD = 3


def require(ok, label):
    if not ok:
        raise ValueError(label)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def clean(v):
    return {i:x % FIELD for i,x in v.items() if x % FIELD}


def add(a,b,scale=1):
    out = a.copy()
    for i,x in b.items():
        out[i] = (out.get(i,0) + scale*x) % FIELD
        if out[i] == 0:
            del out[i]
    return out


def moved(v, permutation):
    return {permutation[i]:x for i,x in v.items()}


def encoded(v):
    return [[i,x] for i,x in sorted(v.items())]


class Space:
    """Incremental exact row echelon basis with least-coordinate pivots."""
    def __init__(self, vectors=()):
        self.rows = {}
        for v in vectors:
            self.insert(v)

    def remainder(self, v):
        v = clean(v)
        while v:
            pivot = min(v)
            if pivot not in self.rows:
                break
            v = add(v, self.rows[pivot], -v[pivot])
        return v

    def insert(self, v):
        v = self.remainder(v)
        if v:
            pivot = min(v)
            inv = pow(v[pivot], -1, FIELD)
            self.rows[pivot] = {i:x*inv % FIELD for i,x in v.items()}

    def contains(self, v):
        return not self.remainder(v)

    def dimension(self):
        return len(self.rows)

    def basis(self):
        return [self.rows[i] for i in sorted(self.rows)]

    def serial(self):
        return [encoded(v) for v in self.basis()]


def sumspace(*spaces):
    return Space(v for s in spaces for v in s.basis())


def invariant_closure(vectors, generators, actions):
    span = Space(vectors)
    while True:
        old_dim = span.dimension()
        for v in span.basis():
            for i in generators:
                span.insert(moved(v,actions[i]))
        if span.dimension() == old_dim:
            break
    require(all(span.contains(moved(v,actions[i])) for v in span.basis()
                for i in generators), 'failed invariant closure')
    return span


def perm_product(g,h):
    """Right action: first g, then h."""
    return tuple(h[i] for i in g)


def build(model):
    require(model['degree'] == 128, 'model degree')
    generators = [tuple(i-1 for i in s) for s in model['generators']]
    identity = tuple(range(128))
    require(len(generators) == 4 and all(sorted(s) == list(identity) for s in generators), 'permutations')
    require(all(perm_product(s,s) == identity for s in generators), 'marked involutions')
    require(all(perm_product(generators[i],generators[j]) == perm_product(generators[j],generators[i])
                for i,j in [(0,2),(0,3),(1,3)]), 'base string relations')
    group, seen = [identity], {identity}
    for g in group:
        for s in generators:
            h = perm_product(g,s)
            if h not in seen:
                seen.add(h);group.append(h)
    require(len(group) == 1024, 'base group order')
    number = {g:i for i,g in enumerate(group)}
    edges = [[number[perm_product(g,s)] for s in generators] for g in group]
    # Two edge types: right cosets <r0>g, then right cosets <r3>g.
    cosets = []
    for s in [generators[0],generators[3]]:
        labels, parts = {}, []
        for g in group:
            if g not in labels:
                h = perm_product(s,g)
                require(h not in labels and h != g, 'bad edge coset')
                k = len(parts)
                parts.append((g,h));labels[g] = labels[h] = k
        require(len(parts) == 512 and len(labels) == 1024, 'edge coset count')
        cosets.append((labels,parts))
    actions = []
    for s in generators:
        a = []
        for ty,(labels,parts) in enumerate(cosets):
            for g,h in parts:
                require(labels[perm_product(g,s)] == labels[perm_product(h,s)], 'coset action not well-defined')
                a.append(512*ty + labels[perm_product(g,s)])
        require(sorted(a) == list(range(1024)), 'edge action permutation')
        actions.append(a)
    shifts = [
        {},
        clean({512+cosets[1][0][identity]:1, 512+cosets[1][0][generators[1]]:-1}),
        clean({cosets[0][0][identity]:-1, cosets[0][0][generators[2]]:1}),
        {},
    ]
    require(all(add(moved(shifts[i],actions[i]),shifts[i]) == {} for i in range(4)), 'affine involutions')
    require(all(add(moved(shifts[i],actions[j]),shifts[j]) ==
                add(moved(shifts[j],actions[i]),shifts[i]) for i,j in [(0,2),(0,3),(1,3)]),
            'affine string relations')

    def word(indices):
        g,v = 0,{}
        for i in indices:
            g = edges[g][i]
            v = add(moved(v,actions[i]),shifts[i])
        return g,v

    def local(indices):
        lifts, pending, loops = {0:{}}, deque([0]), []
        edge_count = 0
        while pending:
            g = pending.popleft()
            for i in indices:
                dest = edges[g][i]
                new = add(moved(lifts[g],actions[i]),shifts[i])
                if dest in lifts:
                    loops.append(add(new,lifts[dest],-1))
                else:
                    lifts[dest] = new;pending.append(dest)
                edge_count += 1
        span = invariant_closure(loops,indices,actions)
        return {'indices':indices,'lifts':lifts,'kernel':span,'schreier_edges':edge_count}

    subsets = [(0,1,2,3),(0,1,2),(1,2,3),(0,1),(1,2),(2,3),(1,),(2,)]
    subgroups = {s:local(s) for s in subsets}
    full = subgroups[(0,1,2,3)]['kernel']
    g,c = word([1,2]*4)
    require(g == 0 and c, 'medial relation translation')
    killed = invariant_closure([c],range(4),actions)
    require(all(full.contains(v) for v in killed.basis()), 'killed space outside generated kernel')
    require(full.dimension() == 257 and killed.dimension() == 127, 'global dimensions')
    require(killed.contains(c), 'medial relation not killed')

    def check_intersection(sa,sb,sc):
        a,b,c = [subgroups[s] for s in [sa,sb,sc]]
        ma,mb,mc = [sumspace(killed,t['kernel']) for t in [a,b,c]]
        total = sumspace(ma,b['kernel'])
        di = ma.dimension()+mb.dimension()-total.dimension()-killed.dimension()
        dc = mc.dimension()-killed.dimension()
        common = set(a['lifts']) & set(b['lifts'])
        need_common = set(c['lifts'])
        require(need_common <= common, 'base common subgroup inclusion')
        forbidden = sorted(common-need_common)
        residues = []
        for h in forbidden:
            delta = add(a['lifts'][h],b['lifts'][h],-1)
            rem = total.remainder(delta)
            require(rem, 'unwanted base-intersection coset survives')
            residues.append({'base_element':h,'nonzero_remainder':encoded(rem)})
        # Shared marked subgroup is included automatically; equal fiber
        # dimension and no extra projected coset prove exact equality.
        require(di == dc, 'excess kernel intersection')
        return {'A':sa,'B':sb,'C':sc,'base_orders':[len(t['lifts']) for t in [a,b,c]],
            'base_intersection_order':len(common),
            'image_kernel_dimensions':[t.dimension()-killed.dimension() for t in [ma,mb,mc]],
            'intersection_kernel_dimension':di,'forbidden_base_cosets':residues,
            'IP':True}

    tests = [check_intersection((0,1,2),(1,2,3),(1,2)),
             check_intersection((0,1),(1,2),(1,)),
             check_intersection((1,2),(2,3),(2,))]
    require(tests[0]['base_orders'] == [128,128,8] and
            tests[0]['image_kernel_dimensions'] == [17,17,0] and
            tests[0]['base_intersection_order'] == 16, 'top intersection totals')
    require(tests[1]['image_kernel_dimensions'] == [1,0,0] and
            tests[2]['image_kernel_dimensions'] == [0,1,0], 'local kernel totals')
    require(tests[1]['base_orders'] == [16,8,2] and tests[2]['base_orders'] == [8,16,2] and
            tests[1]['base_intersection_order'] == tests[2]['base_intersection_order'] == 2,
            'local base intersection totals')
    product_orders = []
    for i in range(3):
        n = 0
        while True:
            n += 1
            require(n <= 24, 'adjacent product order bound')
            base,v = word([i,i+1]*n)
            if base == 0 and killed.contains(v):
                break
        product_orders.append(n)
    require(product_orders == [24,4,24], 'fixed cover type')
    return {
        'format':'expanded-end-affine-cover-F3-v1','field':3,
        'model_sha256':MODEL_SHA,'base_order':1024,'ambient_module_dimension':1024,
        'coset_types':['<r0>g','<r3>g'],'coset_enumeration':'breadth-first base group, first unseen representative',
        'right_affine_multiplication':'(v,g)(u,h)=(v^h+u,gh)',
        'shifts':[encoded(v) for v in shifts],
        'killed_relation_word_0based':[1,2]*4,'killed_relation_vector':encoded(c),
        'generated_kernel_dimension':257,'killed_invariant_dimension':127,
        'cover_kernel_dimension':130,'cover_degree':'3^130','full_fixed_order':'1024*3^130',
        'generated_kernel_basis':full.serial(),'killed_invariant_basis':killed.serial(),
        'parabolics':[{ 'indices':s,'base_order':len(v['lifts']),
                       'raw_kernel_dimension':v['kernel'].dimension(),
                       'schreier_edges_checked':v['schreier_edges'],
                       'raw_kernel_basis':v['kernel'].serial()}
                      for s,v in subgroups.items() if len(s)<4],
        'recursive_intersection_tests':tests,'fixed_cover_type':product_orders,
        'involutions_and_string_relations_before_quotient':True,
        'all_kernel_spaces_closed_under_their_actual_parabolic_actions':True,
        'no_group_order_enumeration_or_floating_point':True,
        'scope':'Fixed1024 base exact affine cover. Full-family pullback and minimal-descendant statements are separately proved in the manuscript.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--expected-certificate',type=Path)
    args = parser.parse_args()
    require(not args.output_dir.exists() and not args.output_dir.is_symlink(), 'fresh output directory required')
    started = time.monotonic()
    raw = (ROOT/MODEL).read_bytes()
    require(digest(raw) == MODEL_SHA, 'model hash mismatch')
    result = build(json.loads(raw))
    require((ROOT/MODEL).read_bytes() == raw, 'model changed during calculation')
    certificate = (json.dumps(result,indent=2)+'\n').encode()
    if args.expected_certificate:
        require(args.expected_certificate.read_bytes() == certificate, 'expected certificate differs')
    args.output_dir.mkdir(parents=True,exist_ok=False)
    (args.output_dir/'certificate.json').write_bytes(certificate)
    report = {'status':'PASS','date':'2026-10-10','seconds':time.monotonic()-started,
        'program_sha256':digest(Path(__file__).read_bytes()),'model_sha256':MODEL_SHA,
        'certificate_sha256':digest(certificate),'field':3,'base_order':1024,
        'generated_kernel_dimension':257,'killed_dimension':127,'cover_kernel_dimension':130,
        'cover_degree':'3^130','fixed_cover_type':[24,4,24],
        'end_kernel_dimensions':[17,17],'medial_kernel_dimension':0,
        'recursive_IP_checks':3,'original_defect_cosets_separated':8,
        'scope':'Author finite calculation. Independent mathematical review and uniform written proof remain separate.'}
    (args.output_dir/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
