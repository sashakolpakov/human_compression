"""Exact finite identification of the six-point Table 2(2) marking.
Required only for this named-model identification; no census is performed.
Permutations use zero-based images and right composition.
"""
from collections import deque
import json


def compose(p,q):
    return tuple(q[x] for x in p)


def closure(gens):
    identity=tuple(range(len(gens[0])))
    seen={identity}
    queue=deque([identity])
    while queue:
        p=queue.popleft()
        for q in gens:
            r=compose(p,q)
            if r not in seen:
                seen.add(r)
                queue.append(r)
    return seen


def main():
    # (a0,a1,a2,b0,b1,x), with reversed path a2,a1,a0,b0,b1,x
    six=((3,2,1,0,4,5),(1,0,2,4,3,5),(0,2,1,3,5,4))
    five=((0,2,1,4,3),(1,0,3,2,4),(0,4,3,2,1))
    paired=tuple(tuple(p)+tuple(6+x for x in q) for p,q in zip(six,five))
    H6,H5,P=closure(six),closure(five),closure(paired)
    if (len(H6),len(H5),len(P))!=(60,60,60):
        raise ValueError('Marked isomorphism certificate failed')
    if any(sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))%2 for p in H5):
        raise ValueError('The five-point image is not contained in A5')
    # A subgroup of A5 of order60 is A5; the paired group has trivial
    # projection kernels and hence identifies the ordered generators.
    print(json.dumps({'status':'PASS','six_point_group_order':len(H6),
        'five_point_group_order':len(H5),'paired_group_order':len(P),
        'source':'L044 Table2(2), physical page27',
        'six_point_generators':six,'five_point_generators':five,
        'source_left_to_right_vertices':[2,1,0,3,4,5]}))

if __name__=='__main__':
    main()
