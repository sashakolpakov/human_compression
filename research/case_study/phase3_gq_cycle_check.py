"""Independent exact girth-cycle checks for chamber-deleted W(3,q).

Prime fields only. No graph or finite-geometry library is used.  The graph is
constructed directly from totally isotropic projective lines of an alternating
form; the comparison Wenger graph uses its two defining coordinate equations.
"""
from collections import deque
from itertools import product
import json
from pathlib import Path


def projective(v, q):
    c = next(x for x in v if x)
    return tuple(x * pow(c, -1, q) % q for x in v)


def symplectic_gq(q):
    pts = sorted({projective(v, q) for v in product(range(q), repeat=4) if any(v)})
    ids = {v: i for i, v in enumerate(pts)}
    lines = set()
    for i, u in enumerate(pts):
        for j in range(i):
            v = pts[j]
            if (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2]) % q:
                continue
            line = {j}
            line.update(ids[projective(tuple((u[k]+t*v[k]) % q for k in range(4)), q)]
                        for t in range(q))
            assert len(line) == q+1
            lines.add(frozenset(line))
    assert len(pts) == len(lines) == (q+1)*(q*q+1)
    adj = [set() for _ in range(len(pts)+len(lines))]
    for j, line in enumerate(sorted(lines, key=lambda x: tuple(sorted(x))), len(pts)):
        for i in line:
            adj[i].add(j)
            adj[j].add(i)
    assert all(len(x) == q+1 for x in adj)
    p = 0
    ell = min(adj[p])
    deleted = {p, ell}
    frontier = deleted.copy()
    for _ in range(2):
        frontier = set().union(*(adj[v] for v in frontier)) - deleted
        deleted.update(frontier)
    kept = sorted(set(range(len(adj))) - deleted)
    reindex = {v: i for i, v in enumerate(kept)}
    out = [{reindex[w] for w in adj[v] if w in reindex} for v in kept]
    assert len(out) == 2*q**3 and all(len(x) == q for x in out)
    return out


def wenger(q):
    tuples = list(product(range(q), repeat=3))
    ids = {v: i for i, v in enumerate(tuples)}
    m = len(tuples)
    adj = [set() for _ in range(2*m)]
    for i, (p1,p2,p3) in enumerate(tuples):
        for l1 in range(q):
            l2 = (p1*l1-p2) % q
            l3 = (p1*l2-p3) % q
            j = m + ids[(l1,l2,l3)]
            adj[i].add(j)
            adj[j].add(i)
    return adj


def moment_wenger(q):
    tuples = list(product(range(q), repeat=3))
    ids = {v: i for i, v in enumerate(tuples)}
    m = len(tuples)
    adj = [set() for _ in range(2*m)]
    for i, (x,u,v) in enumerate(tuples):
        for y in range(q):
            j = m + ids[(y, (x*y-u) % q, (x*y*y-v) % q)]
            adj[i].add(j)
            adj[j].add(i)
    return adj


def check_coordinate_isomorphism(q, recursive, moment):
    tuples = list(product(range(q), repeat=3))
    ids = {v:i for i,v in enumerate(tuples)}
    m = len(tuples)
    mapping = [m+ids[(x,u,(v+x*u) % q)] for x,u,v in tuples]+list(range(m))
    assert len(set(mapping)) == 2*m
    assert all({mapping[j] for j in recursive[i]} == moment[mapping[i]]
               for i in range(2*m))


def disjoint_path_cycles(adj, u, v):
    # A cycle is the fixed edge plus two length-three paths and their middle edge.
    def paths(root, excluded):
        out = []
        def rec(path):
            if len(path) == 4:
                out.append(tuple(path))
            else:
                for w in adj[path[-1]]:
                    if w not in path and (len(path)>1 or w != excluded):
                        rec(path+[w])
        rec([root])
        return out
    left, right = paths(u,v), paths(v,u)
    return sum(1 for p in left for r in right
               if r[-1] in adj[p[-1]] and set(p).isdisjoint(r))


def edge_cycles(adj, u, v, length):
    # Every cycle through {u,v} has exactly one orientation beginning u,v.
    target = u
    def dfs(path):
        if len(path) == length:
            return int(target in adj[path[-1]])
        return sum(dfs(path+[w]) for w in adj[path[-1]] if w not in path)
    return dfs([u,v])


def girth(adj):
    best = len(adj)+1
    for root in range(len(adj)):
        ds = {root: 0}
        parent = {root: -1}
        queue = deque([root])
        while queue:
            x = queue.popleft()
            if 2*ds[x] >= best:
                continue
            for y in adj[x]:
                if y not in ds:
                    ds[y] = ds[x]+1
                    parent[y] = x
                    queue.append(y)
                elif parent[x] != y:
                    best = min(best, ds[x]+ds[y]+1)
    return best


def main():
    data = []
    for q in (3,5,7):
        row = {"q": q,
               "conjectured_lambda": (q-1)**3*(q-2),
               "porupsanszki_2023_lambda": (q-1)**2*((q-2)**2+1)}
        for name, constructor in (("symplectic_chamber_deletion", symplectic_gq),
                                  ("wenger", wenger), ("moment_wenger", moment_wenger)):
            adj = constructor(q)
            samples = sorted({0, len(adj)//3, len(adj)//2, len(adj)-1})
            counts = [edge_cycles(adj,u,min(adj[u]),8) for u in samples]
            g = girth(adj)
            assert g == 8
            row[name] = {"vertices":len(adj), "degree":q, "girth":g,
                         "sample_edge_cycle_counts": counts}
            assert counts == [row["porupsanszki_2023_lambda"]]*len(samples)
            path_count = disjoint_path_cycles(adj, 0, min(adj[0]))
            assert path_count == counts[0]
            row[name]["independent_disjoint_path_count"] = path_count
        check_coordinate_isomorphism(q, wenger(q), moment_wenger(q))
        row["recursive_to_moment_isomorphism_checked_on_every_edge"] = True
        print(json.dumps(row), flush=True)
        data.append(row)
    Path(__file__).with_suffix(".json").write_text(json.dumps(data, indent=2)+"\n")
    print("ALL EXACT GRAPH CHECKS PASS")


if __name__ == "__main__":
    main()
