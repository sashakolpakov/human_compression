"""Canonical F11 data and charged elementary arithmetic; no space solver."""
I=bytes(int(i==j)for i in range(7)for j in range(7))
INV=(0,1,6,4,3,9,2,8,7,5,10)

def need(ok,message):
    if not ok:raise ValueError(message)

def vector(raw,n,b):
    b.scalar(n)
    need(type(raw)in(list,tuple)and len(raw)==n and all(type(x)is int and 0<=x<11 for x in raw),'whole canonical field row')
    return tuple(raw)

def middle(raw,b):
    need(type(raw)is list and len(raw)==2,'exact two ordered middle marks')
    out=[]
    for mat in raw:
        need(type(mat)is list and len(mat)==7,'seven complete matrix rows')
        out.append(bytes(x for row in mat for x in vector(row,7,b)))
    for mat in out:need(b.multiply(mat,mat)==I,'both complete middle involution equations')
    return tuple(out)

def inv(x,b):
    b.scalar(2);need(type(x)is int and 0<x<11,'nonzero canonical pivot')
    y=INV[x];need(x*y%11==1,'literal F11 inverse check');return y

def normalize(v,b):
    first=None
    for x in v:
        b.scalar(1)
        if x:first=x;break
    need(first is not None,'nonzero supplied seed')
    y=inv(first,b);out=[]
    for x in v:b.scalar(1);out.append(x*y%11)
    return out

def equations(g,signs,b):
    rows=[]
    for mat,sign in zip(g,signs):
        for j in range(7):
            row=[]
            for i in range(7):
                b.scalar(1);row.append((mat[7*i+j]-(sign if i==j else 0))%11)
            rows.append(tuple(row))
    return rows

def selected(blocks,b):
    out=[]
    for i,block in enumerate(blocks):
        if block['nullspace_basis']:
            out.append(dict(block=i,basis=0,signs=block['signs'],
                vector=normalize(block['nullspace_basis'][0],b)))
    return out
