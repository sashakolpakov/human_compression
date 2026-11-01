"""Seed supplier: forward elimination with complete row-combination witnesses."""
import field as f

def kernel(rows,b):
    m=len(rows);stored={}
    for index,raw in enumerate(rows):
        a=list(f.vector(raw,7,b));b.scalar(m);c=[0]*m;c[index]=1
        for p,(r,coeff)in sorted(stored.items()):
            b.scalar(1);z=a[p]
            if z:
                for j in range(7):b.scalar(2);a[j]=(a[j]-z*r[j])%11
                for j in range(m):b.scalar(2);c[j]=(c[j]-z*coeff[j])%11
        pivot=None
        for j in range(7):
            b.scalar(1)
            if a[j]:pivot=j;break
        if pivot is None:continue
        z=f.inv(a[pivot],b)
        for j in range(7):b.scalar(1);a[j]=a[j]*z%11
        for j in range(m):b.scalar(1);c[j]=c[j]*z%11
        stored[pivot]=(tuple(a),tuple(c))
    pivots=sorted(stored);free=[j for j in range(7)if j not in stored];basis=[]
    b.scalar(7)
    for j in free:
        b.scalar(7);v=[0]*7;v[j]=1
        for p in reversed(pivots):
            z=0
            for k in range(p+1,7):b.scalar(2);z=(z+stored[p][0][k]*v[k])%11
            b.scalar(1);v[p]=-z%11
        basis.append(v)
    return dict(rank=len(pivots),pivots=pivots,echelon_rows=[list(stored[p][0])for p in pivots],
        row_combinations=[list(stored[p][1])for p in pivots],nullspace_basis=basis)

def supply(g,b):
    blocks=[]
    for signs in ([1,1],[1,10],[10,1],[10,10]):
        block=kernel(f.equations(g,signs,b),b)
        block.update(kind='JOINT_SIGNS',signs=signs);blocks.append(block)
    return dict(space_type='FOUR_JOINT_SIGN_SPACES',blocks=blocks,
        selected_seeds=f.selected(blocks,b))
