"""UNRUN finite normal-form enumeration for bipartite quintic order32 graphs.

The fourteen-skeleton theorem is the mathematical input. The intrinsic
ordinary canonicalization lemma still needs independent review. This file
does not read an F009 state, native frontier, graph6 collection or snapshot.
Every artifact remains provisional until actual Root execution review.
"""
import itertools
import json
import os
import resource
import sys
import time
from array import array
from pathlib import Path

ROWS = (
    (0,1,6,6,(0,0),(1,0,0)), (1,1,6,5,(0,0,0),(1,0)),
    (0,2,5,6,(0,),(2,0,0,0)), (0,2,5,6,(0,),(1,1,0,0)),
    (0,2,6,5,(1,0,0),(1,0)), (2,1,5,5,(0,),(1,0,0,0)),
    (1,2,5,5,(1,),(1,0,0,0)), (1,2,5,5,(0,0),(2,0,0)),
    (1,2,5,5,(0,0),(1,1,0)), (0,3,5,5,(2,),(1,0,0,0)),
    (0,3,5,5,(1,0),(2,0,0)), (0,3,5,5,(1,0),(1,1,0)),
    (0,3,5,5,(0,0,0),(3,0)), (0,3,5,5,(0,0,0),(2,1)),
)
PAIR_TYPES = tuple(itertools.combinations(range(6), 2))
POLICY = dict(rss_mib=128, outer_seconds=150, science_seconds=120,
    ram_admission_gib=4, ram_floor_gib=3, disk_admission_gib=10,
    disk_floor_gib=8, data_bytes=2097152, records=4096,
    catalogue_parts=128, input_extent=16777216, read_bytes=67108864)
TABLE_SHA = '458b6914b4164d23398677f5c98099827343619f0b1c78d9006b773ccc7aabad'


def need(ok, why):
    if not ok:
        raise ValueError(why)


def integer(x, lo, hi):
    return type(x) is int and lo <= x <= hi


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'),
        ensure_ascii=True, allow_nan=False) + '\n').encode('ascii')


def strict(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, 'duplicate JSON field')
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError('finite JSON')))


def frozen(value):
    return tuple(frozen(x) for x in value) if type(value) is list else value


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


class BoundedStop(Exception):
    pass


class Guard:
    def __init__(self, volume):
        self.start = time.monotonic()
        self.volume = Path(volume)
        self.steps = 0
        self.check(145)
        need(self.free_disk() >= 10 * 2**30, 'unchanged10GiB disk admission')

    def free_disk(self):
        value = os.statvfs(self.volume)
        return value.f_bavail * value.f_frsize

    def check(self, seconds=120):
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        peak *= 1 if sys.platform == 'darwin' else 1024
        if peak >= 128 * 2**20:
            raise BoundedStop('128MiB worker RSS')
        if time.monotonic() - self.start >= seconds:
            raise BoundedStop('bounded worker time')
        if self.free_disk() < 8 * 2**30:
            raise BoundedStop('unchanged8GiB disk floor')

    def tick(self):
        self.steps += 1
        if self.steps & 127 == 0:
            self.check()


def row_data(index):
    need(integer(index, 1, 14), 'one of fourteen skeletons')
    t, u, nl, nr, ml, mr = ROWS[index - 1]
    return dict(row=index, q=1+t+u, t=t, u=u, nL=nl, nR=nr, mL=ml, mR=mr)


def side_data(row, side):
    need(side in ('L', 'R'), 'literal side')
    m = row['m' + side]
    arities = tuple(4-row['t']-row['u']+x for x in m)
    return row['n' + side], m, arities + ((5-row['u'],) if side == 'L' else ())


class Profiles:
    """Exact margin counts and deterministic interval traversal; no old prefix replay."""
    def __init__(self, row, side, guard):
        self.n, self.m, self.a = side_data(row, side)
        self.guard = guard
        self.width = 1 << len(self.a)
        self.radix = 1
        for value in self.a:
            self.radix *= value + 1
        self.memo = array('i', [-1]) * ((self.width+1)*(self.n+1)*self.radix)
        need(self.memo.itemsize == 4 and len(self.memo) <= 74375, 'proved finite DP state bound')

    def key(self, k, n, rem):
        result = 0
        for value, top in zip(rem, self.a):
            result = result * (top+1) + value
        return (k*(self.n+1)+n)*self.radix + result

    def count(self, k, n, rem):
        self.guard.tick()
        if n == 0:
            return int(not any(rem))
        if k == self.width:
            return 0
        key = self.key(k, n, rem)
        found = self.memo[key]
        if found >= 0:
            return found
        top = min([n] + [rem[j] for j in range(len(rem)) if k >> j & 1])
        answer = 0
        for multiplicity in range(top+1):
            rest = tuple(value-multiplicity*(k >> j & 1)
                         for j, value in enumerate(rem))
            answer += self.count(k+1, n-multiplicity, rest)
        need(answer <= 54264, 'proved DP integer bound')
        self.memo[key] = answer
        return answer

    def total(self):
        return self.count(0, self.n, self.a)

    def interval(self, start, stop):
        need(integer(start, 0, self.total()) and integer(stop, start, self.total()),
             'exact raw mask-profile interval')
        def walk(k, n, rem, prefix, base):
            self.guard.tick()
            if n == 0:
                if not any(rem) and start <= base < stop:
                    yield base, prefix
                return
            if k == self.width:
                return
            top = min([n] + [rem[j] for j in range(len(rem)) if k >> j & 1])
            for multiplicity in range(top+1):
                rest = tuple(value-multiplicity*(k >> j & 1)
                             for j, value in enumerate(rem))
                size = self.count(k+1, n-multiplicity, rest)
                if size and base < stop and start < base+size:
                    yield from walk(k+1, n-multiplicity, rest,
                                    prefix+(k,)*multiplicity, base)
                base += size
        yield from walk(0, self.n, self.a, (), 0)


def port_permutations(m):
    return tuple(p for p in itertools.permutations(range(len(m)))
                 if all(m[i] == m[p[i]] for i in range(len(m))))


def permute_masks(masks, port_map, star):
    b = len(port_map)
    return tuple(sum(1 << port_map[i] for i in range(b) if mask >> i & 1)
        + ((mask >> b & 1) << b if star else 0) for mask in masks)


def equal_mask_maps(masks):
    groups = [tuple(g) for mask, g in itertools.groupby(range(len(masks)), key=masks.__getitem__)
              if mask != 0]
    for choices in itertools.product(*(itertools.permutations(g) for g in groups)):
        result = list(range(len(masks)))
        for group, choice in zip(groups, choices):
            for source, target in zip(group, choice):
                result[source] = target
        yield tuple(result)


class Engine:
    def __init__(self, guard):
        self.guard = guard
        self.pair_index = None
        self.local_cache = {}

    def local_code(self, masks, omit, m, star):
        """Return code and old-to-new port/side maps attaining it."""
        key = masks, omit, m, star
        found = self.local_cache.get(key)
        if found is not None:
            return found
        best = None
        for ports in port_permutations(m):
            self.guard.tick()
            transformed = permute_masks(masks, ports, star)
            order = tuple(sorted(range(len(masks)), key=lambda i: (transformed[i], i)))
            where = [0]*len(masks)
            for new, old in enumerate(order):
                where[old] = new
            sorted_masks = tuple(transformed[i] for i in order)
            maps = equal_mask_maps(sorted_masks) if omit else [tuple(range(len(masks)))]
            for within in maps:
                self.guard.tick()
                vertices = tuple(within[where[i]] for i in range(len(masks)))
                edges = tuple(sorted(tuple(sorted((vertices[a], vertices[b]))) for a, b in omit))
                candidate = (sorted_masks, edges), ports, vertices
                if best is None or candidate < best:
                    best = candidate
        need(best is not None, 'nonempty local symmetry domain')
        if len(self.local_cache) >= 2048:
            self.local_cache.clear()
        self.local_cache[key] = best
        return best

    def omissions(self):
        if self.pair_index is None:
            result = {}
            for choice in itertools.combinations_with_replacement(range(15), 5):
                self.guard.tick()
                degrees = [0]*6
                for edge in choice:
                    a, b = PAIR_TYPES[edge]
                    degrees[a] += 1
                    degrees[b] += 1
                if max(degrees) <= 4:
                    result.setdefault(tuple(degrees), []).append(bytes(choice))
            self.pair_index = result
        return self.pair_index

    def forms(self, row, side, masks):
        n, m, arities = side_data(row, side)
        star = side == 'L'
        minimal = min(tuple(sorted(permute_masks(masks, p, star))) for p in port_permutations(m))
        if masks != minimal:
            return [], dict(profile_orbit_representative=0, omission_candidates=0)
        if n == 5:
            return [(masks, ())], dict(profile_orbit_representative=1, omission_candidates=1)
        candidates = self.omissions().get(tuple(x.bit_count() for x in masks), ())
        result = []
        for encoded in candidates:
            self.guard.tick()
            omit = tuple(PAIR_TYPES[i] for i in encoded)
            if self.local_code(masks, omit, m, star)[0] == (masks, omit):
                result.append((masks, omit))
        need(len(result) <= 945, 'proved one-profile omission bound')
        return result, dict(profile_orbit_representative=1, omission_candidates=len(candidates))


def check_side(row, side, code):
    n, m, arities = side_data(row, side)
    need(type(code) is tuple and len(code) == 2, 'literal local code')
    masks, omit = code
    need(type(masks) is tuple and len(masks) == n and all(integer(v, 0, (1 << len(arities))-1) for v in masks)
         and masks == tuple(sorted(masks)), 'ordered side masks')
    need(tuple(sum(mask >> j & 1 for mask in masks) for j in range(len(arities))) == arities,
         'all exact side column margins')
    need(type(omit) is tuple and (n == 6 or omit == ()), 'omission role')
    if n == 6:
        need(len(omit) == 5 and omit == tuple(sorted(omit)), 'five unordered omission pairs')
        degree = [0]*6
        for pair in omit:
            need(type(pair) is tuple and len(pair) == 2 and integer(pair[0], 0, 5)
                 and integer(pair[1], pair[0]+1, 5), 'loopless omission edge')
            for vertex in pair:
                degree[vertex] += 1
        need(tuple(degree) == tuple(mask.bit_count() for mask in masks), 'all omission column degrees')


def graph_from_code(code):
    need(type(code) is tuple and len(code) == 10 and integer(code[0], 1, 1), 'versioned complete marked code')
    version, q, t, u, nl, nr, ml, mr, left, right = code
    need(all(integer(x, 0, 6) for x in (q,t,u,nl,nr))
         and type(ml) is tuple and type(mr) is tuple
         and all(integer(x, 0, 3) for x in ml+mr)
         and (t,u,nl,nr,ml,mr) in ROWS and q == 1+t+u, 'one exact middle skeleton')
    row = dict(t=t, u=u, nL=nl, nR=nr, mL=ml, mR=mr)
    check_side(row, 'L', left)
    check_side(row, 'R', right)
    cursor = 3
    def take(n):
        nonlocal cursor
        answer = tuple(range(cursor, cursor+n))
        cursor += n
        return answer
    x0 = take(1+t)
    xi = [take(size) for size in ml+mr]
    l, r, a, c, b = take(nl), take(nr), take(5), take(5), take(5)
    need(cursor == 32, 'exactly thirty-two vertices')
    graph = [0]*32
    def edge(v, w):
        need(v != w and not graph[v] >> w & 1, 'simple construction edge')
        graph[v] |= 1 << w
        graph[w] |= 1 << v
    for vertex in x0:
        for port in b:
            edge(vertex, port)
    for missing, vertices in enumerate(xi):
        for vertex in vertices:
            edge(vertex, 2)
            for index, port in enumerate(b):
                if index != missing:
                    edge(vertex, port)
    for side, vertices, rows, ports, local, endpoint in (
            ('L', l, a, b[:len(ml)], left, 0),
            ('R', r, c, b[len(ml):], right, 1)):
        masks, omit = local
        for index, vertex in enumerate(vertices):
            for j, port in enumerate(ports):
                if masks[index] >> j & 1:
                    edge(vertex, port)
            if side == 'L' and masks[index] >> len(ports) & 1:
                edge(vertex, 2)
        omitted = omit if len(vertices) == 6 else tuple((i,) for i, mask in enumerate(masks)
                                                       for unused in range(mask.bit_count()))
        need(len(omitted) == 5, 'five endpoint rows')
        for row_vertex, missing in zip(rows, omitted):
            edge(endpoint, row_vertex)
            for i, vertex in enumerate(vertices):
                if i not in missing:
                    edge(row_vertex, vertex)
    return tuple(graph)


def distances(graph, root):
    result = [-1]*len(graph)
    result[root] = 0
    queue = [root]
    for vertex in queue:
        for other in bits(graph[vertex]):
            if result[other] < 0:
                result[other] = result[vertex]+1
                queue.append(other)
    return tuple(result)


def validate_graph(graph, guard):
    need(type(graph) is tuple and len(graph) == 32, 'order thirty-two')
    for vertex, mask in enumerate(graph):
        need(integer(mask, 0, 2**32-1) and not mask >> vertex & 1 and mask.bit_count() == 5,
             'simple quintic adjacency masks')
        need(all(graph[other] >> vertex & 1 for other in bits(mask)), 'symmetric adjacency')
    distance = tuple(distances(graph, vertex) for vertex in range(32))
    need(all(min(row) >= 0 for row in distance), 'connected graph')
    colors = tuple(x & 1 for x in distance[0])
    need(all(colors[v] != colors[w] for v in range(32) for w in bits(graph[v])), 'bipartite graph')
    need(max(max(row) for row in distance) == 8, 'diameter exactly eight')
    need(any((graph[v] & graph[w]).bit_count() >= 2 for v in range(32) for w in range(v)),
         'a four-cycle exists; bipartiteness excludes shorter cycles')
    guard.tick()
    return distance, colors


def relabel(graph, old_to_new):
    need(all(integer(v, 0, 31) for v in old_to_new)
         and tuple(sorted(old_to_new)) == tuple(range(32)), 'whole vertex permutation')
    result = [0]*32
    for vertex in range(32):
        result[old_to_new[vertex]] = sum(1 << old_to_new[w] for w in bits(graph[vertex]))
    return tuple(result)


def witness_ok(graph, code, new_to_old):
    if not all(integer(v, 0, 31) for v in new_to_old) or tuple(sorted(new_to_old)) != tuple(range(32)):
        return False
    inverse = [0]*32
    for new, old in enumerate(new_to_old):
        inverse[old] = new
    return relabel(graph, inverse) == graph_from_code(code)


def marked_code(graph, endpoints, midpoint, colors, engine):
    p, last = endpoints
    a, b, c = set(bits(graph[p])), set(bits(graph[midpoint])), set(bits(graph[last]))
    need(len(a | b | c) == 15, 'three disjoint center neighborhoods')
    opposite = {v for v in range(32) if colors[v] != colors[p]}
    extra = opposite - a - b - c
    need(len(extra) == 1, 'unique extra vertex')
    z = next(iter(extra))
    same = set(range(32)) - opposite
    left = {v for v in same-{p,last,midpoint} if set(bits(graph[v])) & a}
    right = {v for v in same-{p,last,midpoint} if set(bits(graph[v])) & c}
    need(not left & right, 'disjoint endpoint sides')
    core = same - left - right - {p,last}
    star_side = set(bits(graph[z])) - core
    need(star_side and (star_side <= left or star_side <= right), 'one star side')
    if star_side <= right:
        p, last, a, c, left, right = last, p, c, a, right, left
    x0 = {v for v in core if set(bits(graph[v])) == b}
    need(midpoint in x0, 'chosen midpoint in central twin class')
    xi = {port: set() for port in b}
    for vertex in core-x0:
        missing = b - set(bits(graph[vertex]))
        need(len(missing) == 1 and set(bits(graph[vertex])) == (b-missing) | {z},
             'exact nonisolated middle class')
        xi[next(iter(missing))].add(vertex)
    t, u = len(x0)-1, len(core-x0)
    bp_left = {port for port in b if set(bits(graph[port])) & left}
    bp_right = {port for port in b if set(bits(graph[port])) & right}
    need(not bp_left & bp_right and bp_left | bp_right == b, 'exact side port partition')
    local_results = []
    port_orders = []
    side_orders = []
    row_orders = []
    m_values = []
    for side, side_vertices, ports, rows in (
            ('L', left, bp_left, a), ('R', right, bp_right, c)):
        vertices = tuple(sorted(side_vertices))
        ports = tuple(sorted(ports, key=lambda v: (-len(xi[v]), v)))
        m = tuple(len(xi[v]) for v in ports)
        masks = tuple(sum(1 << j for j, port in enumerate(ports) if graph[v] >> port & 1)
            + ((int(graph[v] >> z & 1) << len(ports)) if side == 'L' else 0) for v in vertices)
        missing_rows = tuple(tuple(i for i, v in enumerate(vertices) if not graph[row] >> v & 1)
                             for row in rows)
        need(all(len(item) == len(vertices)-4 for item in missing_rows), 'four neighbors per endpoint row')
        omit = tuple(sorted(missing_rows)) if len(vertices) == 6 else ()
        result, port_map, vertex_map = engine.local_code(masks, omit, m, side == 'L')
        reordered_ports = [None]*len(ports)
        reordered_side = [None]*len(vertices)
        for old, new in enumerate(port_map):
            reordered_ports[new] = ports[old]
        for old, new in enumerate(vertex_map):
            reordered_side[new] = vertices[old]
        def omission_key(row):
            return tuple(sorted(vertex_map[i] for i, v in enumerate(vertices) if not graph[row] >> v & 1)), row
        local_results.append(result)
        port_orders.extend(reordered_ports)
        side_orders.extend(reordered_side)
        row_orders.extend(sorted(rows, key=omission_key))
        m_values.append(m)
    code = (1, len(core), t, u, len(left), len(right), *m_values, *local_results)
    order = (p,last,z,midpoint,*sorted(x0-{midpoint}),
             *(v for port in port_orders for v in sorted(xi[port])),
             *side_orders,*row_orders,*port_orders)
    need(witness_ok(graph, code, order), 'complete marked-code permutation witness')
    return code, order


def ordinary_code(graph, engine):
    """Exact class-specific uncolored canonical code, with an explicit isomorphism."""
    distance, colors = validate_graph(graph, engine.guard)
    twins = {}
    for vertex, mask in enumerate(graph):
        twins.setdefault(mask, []).append(vertex)
    representatives = tuple(min(vertices) for vertices in twins.values())
    endpoints = [(a,b) for a,b in itertools.combinations(representatives, 2) if distance[a][b] == 8]
    need(1 <= len(endpoints) <= 2, 'proved intrinsic endpoint-pair bound')
    candidates = []
    for first, last in endpoints:
        middle = [v for v in representatives if distance[first][v] == distance[last][v] == 4]
        need(1 <= len(middle) <= 4, 'proved intrinsic midpoint-class bound')
        for midpoint in middle:
            engine.guard.tick()
            candidates.append(marked_code(graph, (first,last), midpoint, colors, engine))
    need(len(candidates) <= 8, 'proved full ordinary root-choice bound')
    return min(candidates)



if __name__ == '__main__':
    raise SystemExit('UNRUN mathematical library; fresh Root review and bounded caller required.')
