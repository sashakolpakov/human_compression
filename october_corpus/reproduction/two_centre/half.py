"""Exact incidence domain for the nonbipartite two-centre family.

Endpoint columns may be zero. The four-shape domain and all-root ordinary
code are justified by the accompanying proofs. No expected cage count or
existing graph catalogue is an input.
"""
import itertools
import os
import resource
import sys
import time
from pathlib import Path

SHAPE_EDGES = (
    ((0,1),(1,2),(2,3)),
    ((0,1),(0,2),(0,3)),
    ((0,1),(1,2),(3,4)),
    ((0,1),(2,3),(4,5)),
)
BOUNDS = ((13,22,6188,2024,12), (16,23,15504,2300,36),
          (11,21,3003,1771,8), (8,20,792,1540,48))
POLICY = dict(rss_mib=128, outer_seconds=150, science_seconds=120,
    ram_admission_gib=4, ram_floor_gib=3, disk_admission_gib=10,
    disk_floor_gib=8, data_bytes=2097152, records=4096,
    input_extent=16777216, read_bytes=67108864, evaluations=4096)


def need(ok, why):
    if not ok:
        raise ValueError(why)


def integer(x, lo, hi):
    return type(x) is int and lo <= x <= hi


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


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length()-1
        mask ^= bit


def graph_from_edges(n, edges):
    graph = [0]*n
    for a,b in edges:
        need(integer(a,0,n-1) and integer(b,0,n-1) and a != b
             and not graph[a] >> b & 1, 'simple construction edge')
        graph[a] |= 1 << b
        graph[b] |= 1 << a
    return tuple(graph)


def pull(mask, order):
    """Bitmask in the new order; order maps new coordinates to old ones."""
    return sum(1 << new for new,old in enumerate(order) if mask >> old & 1)


def ordered_graph(graph, order):
    n = len(graph)
    need(len(order) == n and all(integer(v,0,n-1) for v in order)
         and tuple(sorted(order)) == tuple(range(n)), 'whole vertex permutation')
    return tuple(pull(graph[old], order) for old in order)


def components(graph):
    remaining = set(range(len(graph)))
    answer = []
    while remaining:
        first = min(remaining)
        reached = {first}
        queue = [first]
        for v in queue:
            for w in bits(graph[v]):
                if w not in reached:
                    reached.add(w)
                    queue.append(w)
        remaining -= reached
        answer.append(tuple(sorted(reached)))
    return tuple(answer)


def side_orders(graph):
    """All new-to-old isomorphisms to one of the four fixed side graphs."""
    need(type(graph) is tuple and len(graph) == 7
         and sum(mask.bit_count() for mask in graph) == 6, 'seven side vertices and three edges')
    for v,mask in enumerate(graph):
        need(integer(mask,0,127) and not mask >> v & 1
             and all(graph[w] >> v & 1 for w in bits(mask))
             and all(not graph[w] & mask for w in bits(mask)), 'simple symmetric triangle-free side')
    pieces = components(graph)
    isolates = tuple(part[0] for part in pieces if len(part) == 1)
    active = [part for part in pieces if len(part) > 1]
    orders = []
    if len(active) == 1 and len(active[0]) == 4:
        vertices = active[0]
        centers = [v for v in vertices if graph[v].bit_count() == 3]
        if centers:
            shape = 2
            need(len(centers) == 1, 'one star center')
            center = centers[0]
            for leaves in itertools.permutations(tuple(v for v in vertices if v != center)):
                for extra in itertools.permutations(isolates):
                    orders.append((center,*leaves,*extra))
        else:
            shape = 1
            ends = [v for v in vertices if graph[v].bit_count() == 1]
            need(len(ends) == 2, 'path endpoints')
            for first in ends:
                path = [first]
                previous = -1
                while len(path) < 4:
                    choices = [w for w in bits(graph[path[-1]]) if w != previous]
                    need(len(choices) == 1, 'unique oriented path step')
                    previous = path[-1]
                    path.append(choices[0])
                for extra in itertools.permutations(isolates):
                    orders.append((*path,*extra))
    elif sorted(map(len,active)) == [2,3]:
        shape = 3
        path = next(part for part in active if len(part) == 3)
        edge = next(part for part in active if len(part) == 2)
        center = next(v for v in path if graph[v].bit_count() == 2)
        ends = tuple(v for v in path if v != center)
        for oriented in itertools.permutations(ends):
            for pair in itertools.permutations(edge):
                for extra in itertools.permutations(isolates):
                    orders.append((oriented[0],center,oriented[1],*pair,*extra))
    else:
        shape = 4
        need(sorted(map(len,active)) == [2,2,2] and len(isolates) == 1, 'three separate side edges')
        for blocks in itertools.permutations(active):
            for choices in itertools.product((False,True), repeat=3):
                pairs = [tuple(reversed(pair)) if flip else pair for pair,flip in zip(blocks,choices)]
                orders.append(tuple(v for pair in pairs for v in pair)+isolates)
    standard = graph_from_edges(7, SHAPE_EDGES[shape-1])
    need(len(orders) == len(set(orders)) == BOUNDS[shape-1][4]
         and all(ordered_graph(graph,order) == standard for order in orders), 'complete distinct side maps')
    return shape,tuple(orders)


def independent_rows(graph, size):
    result = []
    for vertices in itertools.combinations(range(7),size):
        mask = sum(1 << v for v in vertices)
        if all(not graph[v] & mask for v in vertices):
            result.append(mask)
    return tuple(sorted(result))


def columns(rows):
    return tuple(sum(mask >> v & 1 for mask in rows) for v in range(7))


def move_rows(rows, order):
    return tuple(sorted(pull(mask,order) for mask in rows))


class Domain:
    """Small complete endpoint index, with no half or census state cache."""
    def __init__(self, shape, guard):
        need(integer(shape,1,4), 'one of four side graphs')
        self.shape, self.guard = shape,guard
        self.graph = graph_from_edges(7,SHAPE_EDGES[shape-1])
        self.degree = tuple(mask.bit_count() for mask in self.graph)
        self.A = independent_rows(self.graph,4)
        self.B = independent_rows(self.graph,3)
        which,self.orders = side_orders(self.graph)
        a,b,self.na,self.nb,aut = BOUNDS[shape-1]
        need(which == shape and len(self.A) == a and len(self.B) == b, 'proved row-type counts')
        self.index = {}
        count = 0
        for ordinal,rows in enumerate(itertools.combinations_with_replacement(self.A,5)):
            guard.tick()
            alpha = columns(rows)
            if all(0 <= value <= 5-d and 0 <= 5-d-value <= 3 for value,d in zip(alpha,self.degree)):
                self.index.setdefault(alpha,[]).append((ordinal,rows))
            count += 1
        need(count == self.na and count <= 15504, 'complete finite endpoint index')

    def ports(self, first, last):
        need(integer(first,0,self.nb) and integer(last,first,self.nb), 'finite port-multiset interval')
        all_rows = itertools.combinations_with_replacement(self.B,3)
        yield from enumerate(itertools.islice(all_rows,first,last), first)

    def port_context(self, rows):
        least = min(move_rows(rows,order) for order in self.orders)
        if least != rows:
            return 'orbit',(),()
        beta = columns(rows)
        alpha = tuple(5-d-value for d,value in zip(self.degree,beta))
        if any(value < 0 for value in alpha):
            return 'margin',(),()
        stabilizer = tuple(order for order in self.orders if move_rows(rows,order) == rows)
        need(stabilizer, 'identity in port stabilizer')
        return 'compatible',self.index.get(alpha,()),stabilizer

    def endpoint_representative(self, rows, stabilizer):
        for order in stabilizer:
            self.guard.tick()
            if move_rows(rows,order) < rows:
                return False
        return True


def validate_presentation(code):
    need(type(code) is tuple and len(code) == 3 and integer(code[0],1,4), 'complete marked half code')
    shape,ports,rows = code
    graph = graph_from_edges(7,SHAPE_EDGES[shape-1])
    for collection,size,count in ((ports,3,3),(rows,4,5)):
        need(type(collection) is tuple and len(collection) == count and collection == tuple(sorted(collection)),
             'complete unordered row multiset')
        for mask in collection:
            need(integer(mask,0,127) and mask.bit_count() == size
                 and all(not graph[v] & mask for v in bits(mask)), 'independent exact-cardinality side row')
    alpha,beta = columns(rows),columns(ports)
    need(all(value >= 0 for value in alpha), 'nonnegative endpoint column incidence')
    need(all(a+b+mask.bit_count() == 5 for a,b,mask in zip(alpha,beta,graph)), 'every side vertex degree five')


def half_from_code(code):
    validate_presentation(code)
    shape,ports,rows = code
    edges = [(0,v) for v in range(1,6)]
    edges += [(6+a,6+b) for a,b in SHAPE_EDGES[shape-1]]
    edges += [(1+i,6+v) for i,mask in enumerate(rows) for v in bits(mask)]
    edges += [(13+i,6+v) for i,mask in enumerate(ports) for v in bits(mask)]
    return graph_from_edges(16,edges)


def validate_half(graph):
    need(type(graph) is tuple and len(graph) == 16, 'sixteen-vertex half')
    for v,mask in enumerate(graph):
        need(integer(mask,0,65535) and not mask >> v & 1
             and mask.bit_count() in (3,5), 'simple degree3or5 half')
        need(all(graph[w] >> v & 1 for w in bits(mask)), 'symmetric half adjacency')
        need(all(not graph[w] & mask for w in bits(mask)), 'triangle-free half')
    ports = tuple(v for v,mask in enumerate(graph) if mask.bit_count() == 3)
    need(len(ports) == 3 and all(not graph[v] & sum(1 << p for p in ports) for v in ports),
         'three intrinsic independent ports')
    need(len(components(graph)) == 1, 'connected half')
    return ports


def witness_ok(graph, code, new_to_old):
    if (len(new_to_old) != 16 or not all(integer(v,0,15) for v in new_to_old)
            or tuple(sorted(new_to_old)) != tuple(range(16))):
        return False
    return ordered_graph(graph,new_to_old) == half_from_code(code)


def canonical_half(graph, guard):
    """All admissible roots and all side maps; no preferred-root coloring."""
    ports = validate_half(graph)
    port_mask = sum(1 << v for v in ports)
    best = None
    choices = 0
    for root,mask in enumerate(graph):
        if root in ports or mask & port_mask:
            continue
        rows = tuple(bits(mask))
        if any(graph[v] & port_mask for v in rows):
            continue
        side = tuple(v for v in range(16) if v != root and v not in rows and v not in ports)
        need(len(side) == 7, 'complete candidate side partition')
        local = tuple(sum(1 << j for j,w in enumerate(side) if graph[v] >> w & 1) for v in side)
        shape,orders = side_orders(local)
        for order in orders:
            guard.tick()
            vertices = tuple(side[v] for v in order)
            def neighbors_in_side(v):
                return sum(1 << j for j,w in enumerate(vertices) if graph[v] >> w & 1)
            row_order = tuple(sorted(rows,key=lambda v:(neighbors_in_side(v),v)))
            port_order = tuple(sorted(ports,key=lambda v:(neighbors_in_side(v),v)))
            code = shape,tuple(neighbors_in_side(v) for v in port_order),tuple(neighbors_in_side(v) for v in row_order)
            permutation = (root,*row_order,*vertices,*port_order)
            candidate = code,permutation
            if best is None or candidate < best:
                best = candidate
            choices += 1
    need(best is not None and choices <= 624, 'complete bounded ordinary root domain')
    need(witness_ok(graph,*best), 'complete16vertex ordinary identification witness')
    return best


if __name__ == '__main__':
    raise SystemExit('Mathematical library; use the accompanying bounded producer.')
