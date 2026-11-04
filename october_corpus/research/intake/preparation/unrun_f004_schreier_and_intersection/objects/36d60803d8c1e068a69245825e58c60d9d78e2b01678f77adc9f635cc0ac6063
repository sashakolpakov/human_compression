"""Literal retained nullspace function; unused commutant/inverse bodies are not loaded."""
import field as f

def nullspace(equations,n,b):
    f.need(type(n)is int and 1<=n<=13 and len(equations)<=49,'small declared linear domain')
    stored={}
    for raw in equations:
        row=list(f.vector(raw,n,b))
        for p,r in sorted(stored.items()):
            b.scalar(1);z=row[p]
            if z:
                for j in range(n):b.scalar(2);row[j]=(row[j]-z*r[j])%11
        pivot=None
        for j,x in enumerate(row):
            b.scalar(1)
            if x:pivot=j;break
        if pivot is None:continue
        z=f.inv(row[pivot],b)
        for j in range(n):b.scalar(1);row[j]=row[j]*z%11
        stored[pivot]=row
    free=[j for j in range(n)if j not in stored];basis=[];b.scalar(n)
    for j in free:
        v=[0]*n;v[j]=1;b.scalar(n)
        for p in sorted(stored,reverse=True):
            z=0
            for k in range(p+1,n):b.scalar(2);z=(z+stored[p][k]*v[k])%11
            b.scalar(1);v[p]=-z%11
        basis.append(v)
    return basis

