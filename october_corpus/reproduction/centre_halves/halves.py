"""Exact centre-three half presentations and ordinary unrooted codes.

No expected number of classes is an input, a bound, or a stopping condition.
The accompanying proof and separately accepted complete intervals are required.
"""
import itertools
import math
import os
import resource
import sys
import time
from pathlib import Path

SHAPES = (
('K2+4I',((0,1),)),
('P3+3I',((0,1),(1,2))),
('2K2+2I',((0,1),(2,3))),
('P4+2I',((0,1),(1,2),(2,3))),
('K1,3+2I',((0,1),(0,2),(0,3))),
('P3+K2+I',((0,1),(1,2),(3,4))),
('3K2',((0,1),(2,3),(4,5))),
('P5+I',((0,1),(1,2),(2,3),(3,4))),
('K1,4+I',((0,1),(0,2),(0,3),(0,4))),
('T5+I',((0,1),(0,2),(0,3),(3,4))),
('C4+2I',((0,1),(1,2),(2,3),(3,0))),
('P4+K2',((0,1),(1,2),(2,3),(4,5))),
('K1,3+K2',((0,1),(0,2),(0,3),(4,5))),
('2P3',((0,1),(1,2),(3,4),(4,5))))
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
  """New coordinates; order maps new positions to old vertices."""
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
    reached = {min(remaining)}
    queue = list(reached)
    for v in queue:
      for w in bits(graph[v]):
        if w not in reached:
          reached.add(w)
          queue.append(w)
    remaining -= reached
    answer.append(tuple(sorted(reached)))
  return tuple(answer)


def signature(graph):
  return tuple(sorted((len(c),tuple(sorted(graph[v].bit_count() for v in c)))
            for c in components(graph)))


def side_orders(graph, b, meter):
  """All720 trials, at most48 maps; bounded invocation-local cache."""
  need(integer(b,1,4) and type(graph) is tuple and len(graph) == 6
    and sum(x.bit_count() for x in graph) == 2*(5-b), 'complete D6 side')
  for v,mask in enumerate(graph):
    need(integer(mask,0,63) and not mask >> v & 1
      and all(graph[w] >> v & 1 for w in bits(mask))
      and all(not graph[w] & mask for w in bits(mask)), 'triangle-free symmetric side')
  key = b,graph
  if key in meter.cache:
    meter.counts['side_cache_hits'] += 1
    return meter.cache[key]
  candidates = [(i+1,graph_from_edges(6,edges)) for i,(_,edges) in enumerate(SHAPES)
         if len(edges) == 5-b]
  found = [(s,g) for s,g in candidates if signature(g) == signature(graph)]
  need(len(found) == 1, 'unique full triangle-free')
  shape,standard = found[0]
  orders = []
  for order in itertools.permutations(range(6)):
    meter.guard.tick()
    meter.counts['raw_side_trials'] += 1
    if ordered_graph(graph,order) == standard:
      orders.append(order)
  need(1 <= len(orders) <= 48, 'all side maps,')
  result = shape,tuple(orders)
  if len(meter.cache) < 128:
    meter.cache[key] = result
  return result


class Meter:
  def __init__(self, guard):
    self.guard, self.cache = guard,{}
    self.counts = dict(raw_side_trials=0,side_cache_hits=0,
             root_trials=0,canonical_candidates=0,canonical_calls=0,
             row_index_candidates=0,port_maps=0,endpoint_maps=0)


def independent_rows(graph, size):
  result = []
  for vertices in itertools.combinations(range(6),size):
    mask = sum(1 << v for v in vertices)
    if all(not graph[v] & mask for v in vertices):
      result.append(mask)
  return tuple(sorted(result))


def columns(rows):
  return tuple(sum(mask >> v & 1 for mask in rows) for v in range(6))


def move_rows(rows, order):
  return tuple(sorted(pull(mask,order) for mask in rows))


class Domain:
  def __init__(self, b, shape, meter):
    need(integer(b,1,4) and integer(shape,1,len(SHAPES))
      and len(SHAPES[shape-1][1]) == 5-b, 'exact b and')
    self.b, self.shape, self.meter = b,shape,meter
    self.graph = graph_from_edges(6,SHAPES[shape-1][1])
    self.degree = tuple(x.bit_count() for x in self.graph)
    self.A, self.B = independent_rows(self.graph,4),independent_rows(self.graph,2)
    self.na = math.comb(len(self.A)+4,5)
    self.nb = math.comb(len(self.B)+b-1,b)
    self.orders = side_orders(self.graph,b,meter)[1]
    self.index = {}
    count = 0
    for ordinal,rows in enumerate(itertools.combinations_with_replacement(self.A,5)):
      meter.guard.tick()
      meter.counts['row_index_candidates'] += 1
      alpha = columns(rows)
      if all(0 <= 5-d-a <= b for a,d in zip(alpha,self.degree)):
        self.index.setdefault(alpha,[]).append((ordinal,rows))
      count += 1
    need(count == self.na <= 11628 and self.nb <= 3060, 'whole finite row')

  def ports(self, first, last):
    need(integer(first,0,self.nb) and integer(last,first,self.nb), 'port ordinal interval')
    yield from enumerate(itertools.islice(
      itertools.combinations_with_replacement(self.B,self.b),first,last),first)

  def port_context(self, rows):
    images = []
    for order in self.orders:
      self.meter.guard.tick()
      self.meter.counts['port_maps'] += 1
      images.append(move_rows(rows,order))
    if min(images) != rows:
      return 'orbit',(),()
    alpha = tuple(5-d-beta for d,beta in zip(self.degree,columns(rows)))
    if any(not 0 <= a <= 5 for a in alpha):
      return 'margin',(),()
    stabilizer = tuple(o for o,image in zip(self.orders,images) if image == rows)
    need(stabilizer, 'identity in port')
    return 'compatible',self.index.get(alpha,()),stabilizer

  def endpoint_representative(self, rows, stabilizer):
    for order in stabilizer:
      self.meter.guard.tick()
      self.meter.counts['endpoint_maps'] += 1
      if move_rows(rows,order) < rows:
        return False
    return True


def validate_presentation(code):
  need(type(code) is tuple and len(code) == 4 and integer(code[0],1,4)
    and integer(code[1],1,len(SHAPES)), 'whole marked H_b')
  b,shape,ports,rows = code
  need(len(SHAPES[shape-1][1]) == 5-b, 'b and side')
  graph = graph_from_edges(6,SHAPES[shape-1][1])
  for collection,size,count in ((ports,2,b),(rows,4,5)):
    need(type(collection) is tuple and len(collection) == count
      and collection == tuple(sorted(collection)), 'unordered complete row')
    for mask in collection:
      need(integer(mask,0,63) and mask.bit_count() == size
        and all(not graph[v] & mask for v in bits(mask)), 'independent exact-size row')
  need(all(a+beta+g.bit_count() == 5
      for a,beta,g in zip(columns(rows),columns(ports),graph)), 'all six full')


def half_from_code(code):
  validate_presentation(code)
  b,shape,ports,rows = code
  edges = [(0,v) for v in range(1,6)]
  edges += [(6+a,6+c) for a,c in SHAPES[shape-1][1]]
  edges += [(1+i,6+v) for i,mask in enumerate(rows) for v in bits(mask)]
  edges += [(12+i,6+v) for i,mask in enumerate(ports) for v in bits(mask)]
  return graph_from_edges(12+b,edges)


def validate_half(graph):
  need(type(graph) is tuple and integer(len(graph),13,16), 'whole half order13..16')
  n = len(graph)
  for v,mask in enumerate(graph):
    need(integer(mask,0,(1 << n)-1) and not mask >> v & 1
      and mask.bit_count() in (2,5), 'simple degree2or5 half')
    need(all(graph[w] >> v & 1 for w in bits(mask)), 'symmetric half')
    need(all(not graph[w] & mask for w in bits(mask)), 'triangle-free half')
  ports = tuple(v for v,g in enumerate(graph) if g.bit_count() == 2)
  need(len(ports) == n-12 and len(components(graph)) == 1, 'intrinsic ports and')
  need(all(not graph[v] & sum(1 << p for p in ports) for v in ports), 'independent ports')
  return ports


def witness_ok(graph, code, order):
  n = len(graph)
  if len(order) != n or not all(integer(v,0,n-1) for v in order) or tuple(sorted(order)) != tuple(range(n)):
    return False
  return ordered_graph(graph,order) == half_from_code(code)


def canonical_half(graph, meter):
  """All eligible ordinary roots; zero endpoint columns are retained."""
  ports = validate_half(graph)
  b, n = len(ports),len(graph)
  port_mask = sum(1 << v for v in ports)
  best = None
  choices = 0
  meter.counts['canonical_calls'] += 1
  for root,mask in enumerate(graph):
    if root in ports or mask & port_mask:
      continue
    rows = tuple(bits(mask))
    if any(graph[v] & port_mask for v in rows):
      continue
    meter.counts['root_trials'] += 1
    side = tuple(v for v in range(n) if v != root and v not in rows and v not in ports)
    need(len(side) == 6, 'complete ordinary side')
    local = tuple(sum(1 << j for j,w in enumerate(side) if graph[v] >> w & 1) for v in side)
    shape,orders = side_orders(local,b,meter)
    for order in orders:
      meter.guard.tick()
      vertices = tuple(side[v] for v in order)
      def neighbors(v):
        return sum(1 << j for j,w in enumerate(vertices) if graph[v] >> w & 1)
      aa = tuple(sorted(rows,key=lambda v:(neighbors(v),v)))
      pp = tuple(sorted(ports,key=lambda v:(neighbors(v),v)))
      code = b,shape,tuple(neighbors(v) for v in pp),tuple(neighbors(v) for v in aa)
      candidate = code,(root,*aa,*vertices,*pp)
      if best is None or candidate < best:
        best = candidate
      choices += 1
      meter.counts['canonical_candidates'] += 1
  need(best is not None and choices <= 576, 'at most12*48 complete')
  need(witness_ok(graph,*best), 'full at-most16vertex identification')
  return best


if __name__ == '__main__':
  raise SystemExit('Library: use the bounded separately reviewed caller.')
