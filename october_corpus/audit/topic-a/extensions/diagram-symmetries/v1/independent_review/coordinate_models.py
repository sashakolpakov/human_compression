"""Independent finite diagnostics of the written coordinate/geometry interfaces.
No author program or Lean-generated data are imported. This is not the proof
of the uniform theorem; its bilinear and collection arguments are read separately.
"""
from itertools import combinations
import json

def need(p,m):
    if not p: raise ValueError(m)

def model(n,edges,defect=False):
    edges=list(edges);N=1<<(n+len(edges));V=(1<<n)-1
    def beta(v,w):
        return 0 if defect else sum(((v>>j&1)*(w>>i&1))<<k for k,(i,j) in enumerate(edges))
    def mul(a,b):
        v=a&V;w=b&V
        return (v^w)|(( (a>>n)^(b>>n)^beta(v,w))<<n)
    def inv(a):return (a&V)|(((a>>n)^beta(a&V,a&V))<<n)
    def closure(mask):
        out={0};queue=[0]
        for a in queue:
            for i in range(n):
                if mask>>i&1:
                    b=mul(a,1<<i)
                    if b not in out:out.add(b);queue.append(b)
        return out
    sub={}
    for J in range(1<<n):
        E=sum((1<<k) for k,(i,j) in enumerate(edges) if J>>i&1 and J>>j&1)
        expected={x for x in range(N) if (x&V)&~J==0 and (x>>n)&~E==0}
        sub[J]=closure(J);need(sub[J]==expected,'generated-support equality')
    need(len(sub[V])==N,'whole group generation')
    for a in range(N):need(mul(inv(a),a)==0==mul(a,inv(a)),'two-sided inverse')
    for i,j in combinations(range(n),2):
        a=1<<i;b=1<<j;comm=mul(mul(mul(a,b),a),b)
        expected=(1<<(n+edges.index((i,j)))) if (i,j) in edges else 0
        need(comm==expected,'literal edge commutator')
    for J in sub:
        for K in sub:need(sub[J]&sub[K]==sub[J&K],'parabolic intersection')
    cosets=[]
    for i in range(n):
        H=sub[V^(1<<i)];todo=set(range(N));C=[]
        while todo:
            g=min(todo);row={mul(h,g) for h in H};todo-=row
            C.append(sum(1<<x for x in row))
        cosets.append(C)
    flags=[0]*(n+1);chambers=[]
    def visit(i,old,inter):
        if i==n:
            flags[len(old)]+=1
            if len(old)==n:
                need(inter.bit_count()==1,'faithful chamber intersection');chambers.append(old)
            return
        visit(i+1,old,inter)
        for C in cosets[i]:
            if all(C&D for D in old):
                need(inter&C,'typed coset Helly');visit(i+1,old+[C],inter&C)
    visit(0,[],(1<<N)-1)
    need(len(chambers)==N,'complete chamber count')
    return {'rank':n,'edges':edges,'order':N,'type_sizes':[len(C) for C in cosets],
            'all_flag_counts':flags,'IP_identities':(1<<n)**2,'chambers':len(chambers)}

def run():
    rows=[]
    for n in range(1,4):
        E=list(combinations(range(n),2))
        for bits in range(1<<len(E)):rows.append(model(n,[e for k,e in enumerate(E) if bits>>k&1]))
    rows.append(model(4,[(0,1),(1,2),(2,3),(0,3)]))
    rows.append(model(4,list(combinations(range(4),2))))
    rejected=[]
    try:model(3,list(combinations(range(3),2)),True)
    except ValueError as e:rejected.append({'control':'erase_bilinear_term','reason':str(e)})
    need(len(rejected)==1,'false abelianized multiplication rejected')
    # The Boolean quotient remains a regular coset geometry; its diagram is empty.
    boolean=model(3,[]);need(boolean['order']==8 and boolean['chambers']==8,'Boolean quotient')
    return {'status':'PASS','models':rows,'models_checked':len(rows),'controls_rejected':rejected,
            'Boolean_quotient':boolean,'uniform_proof_claim':False}
if __name__=='__main__':print(json.dumps(run(),indent=2))
