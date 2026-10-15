"""Exact integer-affine checks for the stated infinite-grid marking."""
from itertools import product,permutations

def need(b,m):
    if not b:raise ValueError(m)

ID=((1,2,3),(0,0,0))
def point(g,v):
    a,b=g
    return tuple((1 if j>0 else -1)*v[abs(j)-1]+b[i]for i,j in enumerate(a))

def compose(g,h):
    a,b=g;c,d=h
    return (tuple((1 if j>0 else -1)*c[abs(j)-1]for j in a),point(g,d))

def power(g,n):
    z=ID
    for _ in range(n):z=compose(z,g)
    return z

def cell(g,obj):
    kind,anchor,axes=obj
    vertices=[]
    for mask in product([0,1],repeat=len(axes)):
        v=list(anchor)
        for i,bit in zip(axes,mask):v[i]+=bit
        vertices.append(point(g,v))
    low=tuple(min(v[i]for v in vertices)for i in range(3))
    high=tuple(max(v[i]for v in vertices)for i in range(3))
    need(all(b-a in (0,1)for a,b in zip(low,high)),'unit cubical image')
    return kind,low,tuple(i for i in range(3)if high[i]!=low[i])

def run():
    marks=[((-2,-1,3),(1,1,0)),((2,1,3),(0,0,0)),((1,3,2),(0,0,0)),((1,2,-3),(0,0,0))]
    expected=[[1,2,3,2],[2,1,3,2],[3,3,1,4],[2,2,4,1]]
    need(all(power(g,2)==ID and g!=ID for g in marks),'four involutions')
    actual=[]
    for g in marks:
        row=[]
        for h in marks:
            gh=compose(g,h)
            order=next((n for n in range(1,5)if power(gh,n)==ID),None)
            row.append(order)
        actual.append(row)
    need(actual==expected,'exact pair matrix')
    chamber=[(0,(0,0,0),()),(1,(1,0,0),()),(2,(0,0,0),(0,1)),(3,(0,0,0),(0,1,2))]
    for i,g in enumerate(marks):
        need([cell(g,x)==x for x in chamber]==[j!=i for j in range(4)],'exact adjacent base chamber')
    images=set()
    for p in permutations([1,2,3]):
        for signs in product([-1,1],repeat=3):
            g=(tuple(a*s for a,s in zip(p,signs)),(0,0,0))
            images.add(tuple(cell(g,x)for x in chamber))
    need(len(images)==48,'48 distinct base-vertex chambers')
    return dict(status='PASS',pair_matrix=actual,adjacent_chamber_checks=16,signed_chambers=48,infinite_geometry_proved_in_text=True)

if __name__=='__main__':
    import json
    print(json.dumps(run()))
