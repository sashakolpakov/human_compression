"""Literal conjugation certificates for acquired palette groups; no census."""
import sys
if not __debug__:
    raise SystemExit('normal Python required')
sys.dont_write_bytecode = True
import argparse
import array
import collections
import hashlib
import importlib.util
import itertools
import json
import time
from pathlib import Path

P = Path(__file__).resolve().parent
G34 = P.parent
D = G34 / 'palette_serialization_v1/derived'

def need(value, message):
    if not value:
        raise ValueError(message)

def read(path):
    return json.loads(path.read_text())

def mul(p, q):
    return tuple(q[x] for x in p)

def inv(p):
    r = [0] * len(p)
    for i, x in enumerate(p):
        r[x] = i
    return tuple(r)

def pin(path):
    b = path.read_bytes()
    return dict(path=str(path), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())

def module(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

def key(p):
    return bytes(p) if len(p) <= 256 else array.array('H', p).tobytes()

class Context:
    def __init__(self):
        helper = G34 / 'doubling_component_v1/literal_joins_v3.py'
        self.J = module('acquired_joins', helper)
        self.A = self.J.Ambient(read(D / 'group_elements.json'))
        A = self.A
        self.one = tuple(range(21))
        self.identity = A.index[self.one]
        self.parents = {self.identity: None}
        self.edges = {}
        self.order = [self.identity]
        for k in self.order:
            for j, g in enumerate(A.generators):
                v = A.index[mul(A.elements[k], g)]
                if v not in self.parents:
                    self.parents[v] = k
                    self.edges[v] = j
                    self.order.append(v)
        need(len(self.order) == len(A.elements), 'actual generator traversal covers exactly acquired G')
        self.auts = list(self.J.automorphisms(A, read(G34 / 'constructions_component_v1/expected/model.json')))
        need(len(self.auts) == 12, 'twelve explicit coordinate automorphisms')
        self.names = [name for name, _ in self.auts]
        self.autkeys = {b''.join(bytes(a[g]) for g in A.generators): i for i, (_, a) in enumerate(self.auts)}
        need(len(self.autkeys) == 12, 'distinct coordinate automorphisms')
        self.table = []
        for _, a in self.auts:
            row = []
            for _, b in self.auts:
                images = b''.join(bytes(b[a[g]]) for g in A.generators)
                need(images in self.autkeys, 'coordinate representatives form exact complement')
                row.append(self.autkeys[images])
            self.table.append(row)
        self.decompositions = {}
        for t, (_, a) in enumerate(self.auts):
            images = [a[g] for g in A.generators]
            for k, h in enumerate(A.elements):
                hi = inv(h)
                imagekey = b''.join(bytes(mul(mul(hi, g), h)) for g in images)
                need(imagekey not in self.decompositions, 'unique outer/inner decomposition')
                self.decompositions[imagekey] = (t, k)
        need(len(self.decompositions) == 241920, 'explicit distinct coordinate-inner automorphisms')
        self.inputs = [pin(helper), pin(D / 'group_elements.json'),
                       pin(G34 / 'constructions_component_v1/expected/model.json'),
                       pin(G34 / 'source_join_component_v2/construction_join.py'),
                       pin(G34 / 'source_join_component_v2/diagram_comparison01.json'),
                       pin(G34 / 'postprocess_target01/automorphisms.g')]

    def word(self, k):
        result = []
        while self.parents[k] is not None:
            result.append(self.edges[k])
            k = self.parents[k]
        return list(reversed(result))

def subgroup(table, generators):
    result = [0]
    for x in result:
        for y in generators:
            z = table[x][y]
            if z not in result:
                result.append(z)
    return result

def solve_bits(equations, n):
    pivots = {}
    for mask, rhs in equations:
        while mask:
            j = mask.bit_length() - 1
            if j not in pivots:
                pivots[j] = (mask, rhs)
                break
            a, b = pivots[j]
            mask ^= a
            rhs ^= b
        if not mask and rhs:
            return None
    answer = 0
    for j in sorted(pivots):
        mask, rhs = pivots[j]
        if ((answer & mask).bit_count() & 1) ^ rhs:
            answer |= 1 << j
    need(all(((answer & mask).bit_count() & 1) == rhs for mask, rhs in equations), 'literal binary solution')
    return [(answer >> j) & 1 for j in range(n)]

def certify_model(C, index):
    A = C.A
    m = read(D / f'model{index}.json')
    gs = read(D / f'groups{index}.json')
    n = m['n'] + m['rank']
    one = tuple(range(n))
    acts = [tuple(x - 1 for x in g) + tuple(range(m['n'], n)) for g in m['group_action']]
    need(len(acts) == len(A.generators) == 2, 'exact embedded generator correspondence')
    t = min(range(1, m['rank'] + 1), key=lambda u: m['type_sizes'][u - 1])
    xs = [i for i, u in enumerate(m['types']) if u == t]
    local = {x: i for i, x in enumerate(xs)}
    smallgens = [tuple(local[g[x]] for x in xs) for g in acts]
    small = {C.identity: tuple(range(len(xs)))}
    lookup = {key(small[C.identity]): C.identity}
    for k in C.order[1:]:
        small[k] = mul(small[C.parents[k]], smallgens[C.edges[k]])
        code = key(small[k])
        need(code not in lookup, 'chosen actual type action is faithful')
        lookup[code] = k
    fullcache = {C.identity: one}
    def full(k):
        if k not in fullcache:
            p = one
            for j in C.word(k):
                p = mul(p, acts[j])
            fullcache[k] = p
        return fullcache[k]
    checked_vertices = 0
    def decompose(q):
        nonlocal checked_vertices
        need(len(q) == n and sorted(q) == list(range(n)), 'actual full palette permutation')
        qi = inv(q)
        images = []
        ids = []
        for g in acts:
            image = mul(mul(qi, g), q)
            need(all(image[x] in local for x in xs), 'conjugated generator retains chosen type')
            candidate = lookup.get(key(tuple(local[image[x]] for x in xs)))
            need(candidate is not None, 'restriction identifies an actual G element')
            need(full(candidate) == image, 'conjugation identity on ALL object and palette vertices')
            checked_vertices += n
            ids.append(candidate)
            images.append(A.elements[candidate])
        code = b''.join(bytes(x) for x in images)
        need(code in C.decompositions, 'exact coordinate-inner automorphism identification')
        outer, inner = C.decompositions[code]
        return outer, inner, ids
    profiles = {}
    for profile in ['typed', 'correlations']:
        generators = [tuple(x - 1 for x in q) for q in gs[profile + '_generators']]
        data = [decompose(q) for q in generators]
        outer = subgroup(C.table, [x[0] for x in data])
        lifts = {0: one}
        liftwords = {0: []}
        for x in list(outer):
            # subgroup() and this traversal share the exact same ordered generators.
            need(x in lifts, 'quotient BFS order')
            for j, (y, _, _) in enumerate(data):
                z = C.table[x][y]
                if z not in lifts:
                    lifts[z] = mul(lifts[x], generators[j])
                    liftwords[z] = liftwords[x] + [j]
        normalized = {}
        normalization = {}
        for x in outer:
            y, h, images = decompose(lifts[x])
            need(y == x, 'lift exact quotient')
            q = mul(lifts[x], inv(full(h)))
            yy, hh, _ = decompose(q)
            need(yy == x and hh == C.identity, 'normalized exact coordinate automorphism')
            normalized[x] = q
            normalization[x] = h
        image_order = len(A.elements) * len(outer)
        need(gs[profile + '_order'] % image_order == 0, 'conjugation image divides acquired complete group')
        kernel_order = gs[profile + '_order'] // image_order
        need(kernel_order in [1, 2], 'current finite kernel boundary')
        relations = []
        for x in outer:
            for y in outer:
                z = C.table[x][y]
                relations.append(mul(mul(normalized[x], normalized[y]), inv(normalized[z])))
        for q, (x, h, _) in zip(generators, data):
            relations.append(mul(mul(q, inv(full(h))), inv(normalized[x])))
        nontrivial = {q for q in relations if q != one}
        if kernel_order == 1:
            need(not nontrivial, 'faithful conjugation kernel verified on generating relations')
            z = one
        else:
            need(len(nontrivial) == 1, 'explicit unique central involution from generating relations')
            z = next(iter(nontrivial))
            need(mul(z, z) == one, 'kernel element has order two')
            need(all(mul(z, q) == mul(q, z) for q in generators + acts), 'actual central commutation')
        equations = []
        positions = {x: i for i, x in enumerate(outer)}
        for x in outer:
            for y in outer:
                xy = C.table[x][y]
                error = mul(mul(normalized[x], normalized[y]), inv(normalized[xy]))
                need(error in [one, z], 'literal binary central cocycle')
                mask = (1 << positions[x]) ^ (1 << positions[y]) ^ (1 << positions[xy])
                equations.append((mask, int(error != one)))
        bits = solve_bits(equations, len(outer))
        need(bits is not None, 'explicit section exists; no direct product inferred merely from order')
        section = {x: mul(normalized[x], z) if bits[positions[x]] else normalized[x] for x in outer}
        need(section[0] == one, 'section identity')
        need(all(mul(section[x], section[y]) == section[C.table[x][y]] for x in outer for y in outer), 'all literal section relations')
        profiles[profile] = dict(acquired_order=gs[profile + '_order'], image_order=image_order,
            kernel_order=kernel_order, outer_indices=outer, outer_names=[C.names[x] for x in outer],
            generator_decompositions=[dict(outer=x, inner_element=h, image_elements=ids) for x,h,ids in data],
            lift_words={str(x): liftwords[x] for x in outer}, normalization_elements=normalization,
            section_bits=bits, section_permutations={str(x): list(section[x]) for x in outer},
            central_involution=None if kernel_order == 1 else list(z))
    return dict(catalogue_index=index, chosen_faithful_type=t, faithful_type_size=len(xs),
        all_vertex_conjugation_checks=checked_vertices, profiles=profiles,
        inputs=[pin(D / f'model{index}.json'), pin(D / f'groups{index}.json')])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--models', default='')
    a = ap.parse_args()
    need(not a.out.exists(), 'fresh output directory')
    a.out.mkdir()
    started = time.monotonic()
    C = Context()
    (a.out / 'coordinate_group.json').write_text(json.dumps(dict(names=C.names, table=C.table,
        explicit_automorphisms=len(C.decompositions), inputs=C.inputs), indent=2) + '\n')
    print('COORDINATE_GROUP_COMPLETE', time.monotonic() - started, flush=True)
    ids = [] if not a.models else [int(x) for x in a.models.split(',')]
    need(len(ids) == len(set(ids)) and all(1 <= x <= 29 for x in ids), 'distinct explicit model requests')
    records = []
    for i in ids:
        record = certify_model(C, i)
        records.append(record)
        (a.out / f'model{i}.json').write_text(json.dumps(record, indent=2) + '\n')
        print('MODEL_COMPLETE', i, [(k, v['outer_names'], v['kernel_order']) for k,v in record['profiles'].items()], flush=True)
    report = dict(status='PASS_LITERAL_AUT_COR_STRUCTURES', requested_models=ids, completed_models=ids,
        records=[dict(index=r['catalogue_index'], path=f"model{r['catalogue_index']}.json") for r in records],
        seconds=time.monotonic()-started, target_censuses=0, graph_searches=0, source_credit=0,
        runtime=pin(Path(__file__).resolve()))
    (a.out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')

if __name__ == '__main__':
    main()
