"""Literal matrix-group control, without GAP/SymPy or author imports."""
import sys
if sys.flags.optimize: raise RuntimeError('Ordinary Python required')
import argparse,json
from itertools import combinations
from pathlib import Path

def case(p,degree,a,kind):
    q=p**degree
    def add(x,y):
        if degree==1:return (x+y)%p
        return (x%p+y%p)%p+p*((x//p+y//p)%p)
    def neg(x):
        if degree==1:return -x%p
        return (-x%p)+p*(-(x//p)%p)
    def mul(x,y):
        if degree==1:return x*y%p
        # Only F9, with alpha^2=-1, is needed.
        assert p==3 and degree==2
        u,v=x%p,x//p;U,V=y%p,y//p
        return (u*U-v*V)%p+p*((u*V+v*U)%p)
    at=[[add(x,y)for y in range(q)]for x in range(q)]
    mt=[[mul(x,y)for y in range(q)]for x in range(q)]
    assert all(sorted(row)==list(range(q))for row in mt[1:])
    one=(1,0,0,0,1,0,0,0,1);minus=neg(1)
    def product(A,B):
        return tuple(at[at[mt[A[3*i]][B[j]]][mt[A[3*i+1]][B[3+j]]]][mt[A[3*i+2]][B[6+j]]]for i in range(3)for j in range(3))
    def closure(gs):
        seen={one};queue=[one]
        for x in queue:
            for g in gs:
                y=product(x,g)
                if y not in seen:seen.add(y);queue.append(y)
        return frozenset(seen)
    def order(x):
        y=one
        for k in range(1,4*q*q+1):
            y=product(y,x)
            if y==one:return k
        raise AssertionError('order cap')
    D=[(1,0,0,0,minus,0,0,0,minus),(minus,0,0,0,1,0,0,0,minus),(minus,0,0,0,minus,0,0,0,1)]
    if kind=='generic':
        T=(a,neg(add(a,1)),0,add(a,minus),neg(a),0,1,minus,minus)
    elif kind=='product':T=(1,0,0,1,minus,0,1,0,minus)
    elif kind=='heis':T=(1,neg(2),0,0,minus,0,1,minus,minus)
    else:raise AssertionError(kind)
    assert product(T,T)==one
    G=closure(D+[T]);H=closure(D+[T[:6]+(0,0,minus)])
    orders=[order(product(d,T))for d in D]
    # Directly inspect every generated matrix, not a quotient or order-only test.
    scalar=[x for x in G if all(x[3*i+j]==0 for i in range(3)for j in range(3)if i!=j) and x[0]==x[4]==x[8]]
    assert scalar==[one]
    subsets=list(range(8));pairs=0;valid=[];intersections=[]
    for i,j in combinations(range(3),2):
        marks=[D[i],T,D[j]]
        groups=[closure([marks[k]for k in range(3)if s>>k&1])for s in subsets]
        assert groups[7]==G
        failures=[]
        for x in subsets:
            for y in subsets:
                pairs+=1
                if groups[x]&groups[y]!=groups[x&y]:failures.append([x,y])
        valid.append(not failures);intersections.append(len(groups[3]&groups[6]))
    if kind=='generic':
        expected={(5,1,2):(300,[3,6,10]),(3,2,3):(1296,[8,8,6])}[(p,degree,a)]
        assert (len(G),orders)==expected and valid==[True]*3
        kernel={x for x in G if x[:6]==one[:6]}
        assert len(kernel)==q*q and len(G)==len(H)*q*q and kernel&H=={one}
        assert kernel=={(1,0,0,0,1,0,x,y,1)for x in range(q)for y in range(q)}
    elif kind=='product':
        assert len(G)==4*p*p and orders==[p,2*p,2*p] and valid==[True,True,False] and intersections==[2,2,4]
    else:
        assert len(G)==4*p**3 and orders==[p,2*p,2*p] and valid==[True]*3
        unipotents={x for x in G if (x[0],x[4],x[8])==(1,1,1)}
        assert unipotents=={(1,x,0,0,1,0,y,z,1)for x in range(p)for y in range(p)for z in range(p)}
    return dict(field=q,parameter=a,kind=kind,order=len(G),adjacent_orders=orders,
        subset_pairs=pairs,full_ip=valid,end_intersection_orders=intersections,projective_kernel=1)

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    assert not a.out.exists()
    rows=[case(5,1,2,'generic'),case(3,2,3,'generic')]
    rows += [case(p,1,None,k)for p in [3,5]for k in ['product','heis']]
    report=dict(status='PASS_INDEPENDENT_L027_LITERAL_MATRIX_GROUPS',cases=rows,
        subset_pairs=sum(x['subset_pairs']for x in rows),author_programs_imported=False,
        group_library_used=False,uniform_proof_replaced=False)
    a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
