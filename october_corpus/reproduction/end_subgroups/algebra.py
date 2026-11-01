"""Literal retained canonical matrix/marking/dihedral helpers; no model recognition."""
import field as f
I=f.I

def matrix(raw,b):
    f.need(type(raw)is list and len(raw)==7,'seven whole matrix rows')
    return bytes(x for row in raw for x in f.vector(row,7,b))

def rows(a):
    return [list(a[7*i:7*i+7])for i in range(7)]

def marking(raw,b):
    f.need(type(raw)is list and len(raw)==4,'four original marks in order')
    g=tuple(matrix(a,b)for a in raw)
    f.need(len(set(g))==4 and all(a!=I for a in g),'four distinct nonidentity marks')
    for a in g:f.need(b.multiply(a,a)==I,'each complete involution equation')
    for i,j in((0,2),(0,3),(1,3)):
        f.need(b.multiply(g[i],g[j])==b.multiply(g[j],g[i]),'all three string commutations')
    return g

def dihedral(a,c,b,cap=256):
    r=b.multiply(a,c);power=I;rot=[]
    for n in range(1,cap+1):
        rot.append(power);power=b.multiply(power,r)
        if power==I:break
    else:return None
    f.need(n>=2,'distinct nonidentity involutions have rotation order at least2')
    reflections=[b.multiply(x,a)for x in rot]
    group=set(rot+reflections)
    f.need(len(group)==2*n,'complete dihedral normal form and full byte distinctness')
    return n,group

