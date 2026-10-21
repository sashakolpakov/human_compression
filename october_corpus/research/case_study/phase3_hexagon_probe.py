"""Exact local 12-cycle counts in the five-coordinate Lie graph, prime q.

The four adjacency equations are those displayed for L(M3,6,q) in Section 2
of arXiv:2311.04401. No identification with a generalized hexagon is assumed.
"""
from functools import lru_cache
from pathlib import Path
import json


def count(q):
    @lru_cache(None)
    def neighbours(v):
        typ, v = v
        out = []
        for a in range(q):
            if typ == 0:
                x,p2,p3,p4,p5 = v
                l2=(x*a-p2)%q
                l3=(x*l2-p3)%q
                l4=(x*l3-p4)%q
                l5=(p2*l3-2*p3*l2+p4*a-p5)%q
                out.append((1,(a,l2,l3,l4,l5)))
            else:
                x,l2,l3,l4,l5 = v
                p2=(a*x-l2)%q
                p3=(a*l2-l3)%q
                p4=(a*l3-l4)%q
                p5=(p2*l3-2*p3*l2+p4*x-l5)%q
                out.append((0,(a,p2,p3,p4,p5)))
        return tuple(out)
    u=(0,(0,0,0,0,0)); v=(1,(0,0,0,0,0))
    def branch(root, excluded):
        paths={root:(root,)}
        seen={root}
        levels=[]
        for d in range(5):
            new={}
            for end,path in paths.items():
                for w in neighbours(end):
                    if len(path)==1 and w==excluded:
                        continue
                    if len(path)>1 and w==path[-2]:
                        continue
                    assert w not in seen, (q,"cycle shorter than12",d,w)
                    assert w not in new, (q,"merging paths shorter than12",d,w)
                    new[w]=path+(w,)
            seen.update(new)
            paths=new
            levels.append(len(paths))
        assert levels==[(q-1)**(d+1) for d in range(5)]
        return paths,seen
    left,seenleft=branch(u,v)
    right,seenright=branch(v,u)
    assert seenleft.isdisjoint(seenright), (q,"root-cross short cycle")
    cycles=0
    for x,path in left.items():
        for y in neighbours(x):
            if y in right:
                assert set(path).isdisjoint(right[y])
                cycles+=1
    return {"q":q,"cycles_through_zero_edge":cycles,
            "conjectured_lambda":(q-1)**5*(q-2),
            "branch_boundary_size":len(left),
            "no_cycle_shorter_than_12_through_root_edge":True,
            "cached_vertices":neighbours.cache_info().currsize}


if __name__=="__main__":
    data=[]
    for q in (3,5,7,11):
        try:
            row=count(q)
        except AssertionError as e:
            row={"q":q,"short_cycle_or_collision":str(e)}
        print(json.dumps(row),flush=True)
        data.append(row)
    Path(__file__).with_suffix(".json").write_text(json.dumps(data,indent=2)+"\n")
