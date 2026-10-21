#!/usr/bin/env python3
"""Literal AG(2,3) distinguishes three-edge from four-edge transitivity."""
from collections import deque
from itertools import combinations, product
import json


def require(test, message):
    if not test:
        raise ValueError(message)


def connected(vertices, neighbors):
    vertices = set(vertices)
    if not vertices:
        return False
    seen = {next(iter(vertices))}
    queue = deque(seen)
    while queue:
        x = queue.popleft()
        for y in neighbors[x] & vertices - seen:
            seen.add(y)
            queue.append(y)
    return seen == vertices


def main():
    points = list(product(range(3), repeat=2))
    index = {p:i for i,p in enumerate(points)}
    lines = sorted({tuple(sorted(index[((a+t*x)%3, (b+t*y)%3)] for t in range(3)))
                    for a,b in points for x,y in points if (x,y) != (0,0)})
    flags = [(p,l) for l,L in enumerate(lines) for p in L]
    require(len(lines) == 12 and len(flags) == 36, 'affine plane counts')
    sets = [set(L) for L in lines]
    objects = [(0,p) for p in range(9)] + [(1,l) for l in range(12)] + [(2,f) for f in range(36)]

    def incident(a,b):
        if a[0] > b[0]:
            a,b = b,a
        if a[0] == b[0]:
            return False
        if a[0:1] == (0,) and b[0:1] == (1,):
            return a[1] not in sets[b[1]]
        x,m = flags[b[1]]
        if a[0] == 0:
            return a[1] in sets[m] and a[1] != x
        return sets[a[1]] & sets[m] == {x}

    neighbors = {x:{y for y in objects if incident(x,y)} for x in objects}
    chambers = {(p,l,f) for p in range(9) for l in range(12) for f in range(36)
                if incident((0,p),(1,l)) and incident((0,p),(2,f)) and incident((1,l),(2,f))}
    panels = []
    for a,b in combinations(objects,2):
        if not incident(a,b):
            continue
        completions = neighbors[a] & neighbors[b]
        require(len(completions) >= 2, 'nonfirm or nonextending pair')
        panels.append(len(completions))
    require(all(neighbors[x] for x in objects), 'isolated object')
    require(connected(objects, neighbors), 'disconnected whole geometry')
    for x in objects:
        residue = neighbors[x]
        require(connected(residue, neighbors), 'disconnected rank-two residue')
        types = sorted({y[0] for y in residue})
        left = {y for y in residue if y[0] == types[0]}
        right = residue-left
        digon = all(right <= neighbors[y] for y in left)
        linear = all(len(neighbors[a] & neighbors[b] & right) <= 1
                     for a,b in combinations(left,2))
        require(digon or linear, 'rank-two intersection property')
    group = []
    for a,b,c,d in product(range(3),repeat=4):
        if (a*d-b*c)%3 != 1:
            continue
        for u,v in points:
            group.append(tuple(index[((a*x+b*y+u)%3,(c*x+d*y+v)%3)] for x,y in points))
    require(len(group) == len(set(group)) == 216, 'ASL order')
    line_maps = []
    flag_maps = []
    for g in group:
        lm = [lines.index(tuple(sorted(g[x] for x in L))) for L in lines]
        fm = [flags.index((g[p],lm[l])) for p,l in flags]
        line_maps.append(lm)
        flag_maps.append(fm)
    p,l,f = next(iter(chambers))
    orbit = {(g[p],lm[l],fm[f]) for g,lm,fm in zip(group,line_maps,flag_maps)}
    require(orbit == chambers and len(chambers) == 216, 'not regular chamber action')
    original_flag = flags[0]
    require(len({(g[original_flag[0]],lm[original_flag[1]]) for g,lm in zip(group,line_maps)}) == 36,
            'original flag transitivity')
    paths3 = {(p,m,x,l) for p in range(9) for m,M in enumerate(lines) for x in M
              for l,L in enumerate(lines) if p in M and p != x and x in L and m != l}
    paths4 = {path+(y,) for path in paths3 for y in lines[path[3]] if y != path[2]}
    require(len(paths3) == 216 and len(paths4) == 432, 'path counts')
    p,m,x,l,y = next(iter(paths4))
    orbit4 = {(g[p],lm[m],g[x],lm[l],g[y]) for g,lm in zip(group,line_maps)}
    require(len(orbit4) == 216 and orbit4 < paths4, 'four-edge counterexample')
    print(json.dumps(dict(status='PASS',q=3,object_counts=[9,12,36],chambers=216,
        all_flags_extend=True,firm_panel_sizes=sorted(set(panels)),connected_residues=58,
        rank_two_intersection_checks=57,ASL_order=216,ASL_regular_on_chambers=True,
        ASL_original_flag_transitive=True,three_edge_paths=216,four_edge_paths=432,
        four_edge_orbit_size=216,
        conclusion='Chamber transitivity is three-edge/four-vertex transitivity; the conventional four-edge interpretation of the source claim is false.'),indent=2))


if __name__ == '__main__':
    main()
