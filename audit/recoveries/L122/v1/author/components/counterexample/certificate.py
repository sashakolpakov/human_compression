"""Exact integer certificate for a coset geometry with no order-three type cycle.

No GAP, nauty, group library or graph-isomorphism backend is imported.
Permutations act on the right: mul(p,q)[x] = q[p[x]].
"""
from pathlib import Path
from collections import Counter, defaultdict, deque
import argparse, hashlib, json

HERE=Path(__file__).resolve().parent

def need(t,s):
    if not t:raise ValueError(s)

def mul(p,q):return tuple(q[x] for x in p)
def inv(p):
    q=[0]*len(p)
    for i,x in enumerate(p):q[x]=i
    return tuple(q)
def power(p,n):
    q=tuple(range(len(p)))
    while n:
        if n&1:q=mul(q,p)
        p=mul(p,p);n//=2
    return q
def order(p):
    from math import lcm
    seen=set();out=1
    for x in range(len(p)):
        if x in seen:continue
        n=0;y=x
        while y not in seen:seen.add(y);n+=1;y=p[y]
        out=lcm(out,n)
    return out
def closure(gens,identity,product):
    out={identity};todo=deque([identity])
    while todo:
        x=todo.popleft()
        for g in gens:
            y=product(x,g)
            if y not in out:out.add(y);todo.append(y)
    return out

def refine(adj,fixed,objects):
    colors=[0]*objects+[1]*3
    for i,v in enumerate(fixed):colors[v]=i+2
    history=[]
    while True:
        signatures=[(colors[v],tuple(sorted(Counter(colors[w] for w in adj[v]).items()))) for v in range(len(adj))]
        ids={s:i for i,s in enumerate(sorted(set(signatures)))}
        nxt=[ids[s] for s in signatures];history.append(len(ids))
        if len(set(colors))==len(ids):colors=nxt;break
        colors=nxt
    cells=defaultdict(list)
    for v,c in enumerate(colors):cells[c].append(v)
    return list(cells.values()),history

def model(data):
    gens=[tuple(p) for p in data['T_generators']]
    a=tuple(data['a']);b=tuple(data['b']);one=tuple(range(18))
    for p in gens+[a,b]:need(sorted(p)==list(one),'degree18 permutation')
    T=closure(gens,one,mul);need(len(T)==2448,'T order2448')
    need(a in T and b in T and order(a)==9 and order(b)==2,'actual marked elements')
    a3=power(a,3)
    H0=closure([a3,b],one,mul);need(len(H0)==12,'projected subgroup order12')
    gm=lambda x,y:((x[0]+y[0])%3,mul(x[1],y[1]))
    gi=lambda x:((-x[0])%3,inv(x[1]))
    G=sorted((i,t) for i in range(3) for t in T);Gpos={x:i for i,x in enumerate(G)}
    e=(0,one);c=(1,one);aa=(0,a)
    H=closure([(1,a3),(0,b)],e,gm)
    need(len(H)==12 and {(x[1]) for x in H}==H0,'graph subgroup H')
    sigma=lambda x:(x[0],mul(mul(inv(a),x[1]),a))
    Hs=[H,{sigma(x) for x in H},{sigma(sigma(x)) for x in H}]
    need(len({frozenset(h) for h in Hs})==3 and {sigma(x) for x in Hs[2]}==H,'three distinct cyclic parabolics')
    need(set.intersection(*Hs)=={e,(1,a3),(2,power(a,6))},'exact triple intersection')
    need(all(len(Hs[i]&Hs[j])==3 for i in range(3) for j in range(i)),'pair intersections')
    need(len(closure(list(set.union(*Hs)),e,gm))==7344,'parabolics generate G')
    reps=[];owners=[];cosets=[]
    for h in Hs:
        own=[-1]*len(G);local=[]
        for k,g in enumerate(G):
            if own[k]!=-1:continue
            members=sorted(Gpos[gm(x,g)] for x in h)
            j=len(local);local.append(members);reps.append(g)
            for x in members:
                need(own[x]==-1,'disjoint cosets');own[x]=j
        need(len(local)==612 and min(own)>=0,'complete right-coset partition')
        owners.append(own);cosets.append(local)
    n=612;N=3*n
    vertex=lambda typ,x:typ*n+owners[typ][Gpos[x]]
    adj=[set() for _ in range(N)]
    for k in range(len(G)):
        vs=[i*n+owners[i][k] for i in range(3)]
        for i in range(3):
            for j in range(i):adj[vs[i]].add(vs[j]);adj[vs[j]].add(vs[i])
    need(all(len(z)==8 for z in adj),'valency8')
    reached={0};todo=deque([0])
    while todo:
        for w in adj[todo.popleft()]:
            if w not in reached:reached.add(w);todo.append(w)
    need(len(reached)==N,'connected incidence graph')
    action=lambda x:tuple(vertex(v//n,gm(reps[v],x)) for v in range(N))
    sig=tuple(vertex((v//n+1)%3,sigma(reps[v])) for v in range(N))
    ident=tuple(range(N));rc=action(c);ra=action(aa)
    z=mul(sig,inv(ra))
    need(order(sig)==9 and order(z)==9 and power(z,3)==rc,'central ninth root of c')
    actions=[rc]+[action((0,g)) for g in gens]
    need(all(mul(z,g)==mul(g,z) for g in actions),'z centralizes the full typed G')
    need(all(action(x)!=ident for x in set.intersection(*Hs)-{e}),'faithful coset action')
    for p in actions+[sig,z]:
        need(sorted(p)==list(range(N)),'actual incidence permutation')
        need(all({p[w] for w in adj[v]}==adj[p[v]] for v in range(N)),'incidence preservation')
    # An incident pair contains a common group element; its three cosets form a chamber.
    chambers=sum(len(adj[v]&adj[w]) for v in range(n) for w in adj[v] if n<=w<2*n)
    need(chambers==2448,'all actual chambers counted')
    augmented=[sorted(row|{N+v//n}) for v,row in enumerate(adj)]+[list(range(i*n,(i+1)*n)) for i in range(3)]
    return dict(T=T,G=G,Gpos=Gpos,owners=owners,reps=reps,adj=adj,augmented=augmented,
                vertex=vertex,actions=actions,sigma=sig,z=z,ra=ra,rc=rc,chambers=chambers)

def verify(data):
    m=model(data);n=612;N=1836;aug=m['augmented']
    u,v,w=data['refinement_base']
    need(u<N and v in m['adj'][u] and w<N,'ordered edge and third object')
    cells,history=refine(aug,[u,v],N)
    cell=next(c for c in cells if w in c)
    need(len(cell)==3,'edge stabilizer has an invariant three-cell')
    need(cell==[1,441,481] and history==[9,21,60,187,579,630,633,633],'literal edge-refinement record')
    final,h2=refine(aug,[u,v,w],N)
    need(len(final)==N+3,'three fixed objects force identity')
    need(h2==[11,28,126,786,1822,1839,1839],'literal discrete-refinement record')
    reflection=tuple(data['reflection'])
    need(sorted(reflection)==list(range(N+3)),'full reflection permutation')
    need(order(reflection)==2,'reflection is an involution')
    need(all({reflection[x] for x in row}==set(aug[reflection[i]]) for i,row in enumerate(aug)),'reflection preserves entire augmented graph')
    need(all(reflection[i]<N for i in range(N)) and sorted(reflection[N:])==list(range(N,N+3)),'reflection preserves the two colors')
    need(sum(reflection[N+i]!=N+i for i in range(3))==2,'reflection has type transposition')
    # Construct a Sylow 3-subgroup explicitly: two commuting independent order-nine factors.
    z=m['z'];a=m['ra'];need(mul(z,a)==mul(a,z),'Sylow factors commute')
    sylow={mul(power(z,i),power(a,j)) for i in range(9) for j in range(9)}
    need(len(sylow)==81,'explicit Sylow has81 elements')
    distribution=Counter(order(p) for p in sylow)
    need(distribution=={1:1,3:8,9:72},'complete Sylow order distribution')
    need(all(all(p[x]//n==x//n for x in range(N)) for p in sylow if order(p)==3),'all order-three Sylow elements preserve each type')
    sig=m['sigma'];sig_minus2=power(sig,7)
    reset=tuple(sig[x] if x//n<2 else sig_minus2[x] for x in range(N))
    need(order(reset)==3,'literal reset has order3 as a permutation')
    bad=next(((x,y,reset[x],reset[y]) for x in range(N) for y in sorted(m['adj'][x]) if reset[y] not in m['adj'][reset[x]]),None)
    need(bad is not None,'reset fails incidence on this actual coset geometry')
    need(all(len(m['adj'][x]&m['adj'][y])==1 for x in range(N) for y in m['adj'][x]),'every panel has exactly one completion')
    upper=N*8*len(cell);need(upper==44064 and upper//81%3!=0,'exact whole group bound and full3part')
    # Group lower bound is proved in the manuscript: <G,z> has order22032 and reflection lies outside.
    return dict(status='PASS_EXACT_COUNTEREXAMPLE_CERTIFICATE',group_order=7344,
                parabolic_order=12,pair_intersection=3,triple_intersection=3,
                objects_per_type=612,objects=N,incidence_degree=8,edges=sum(map(len,m['adj']))//2,
                chambers=m['chambers'],sigma_order=9,central_type_cycle_order=9,
                faithful=True,connected=True,full_correlation_order=upper,
                full_typed_order=7344,refinement_base=[u,v,w],edge_cell=cell,
                edge_refinement=history,three_fixed_refinement=h2,
                sylow_order=81,sylow_order_distribution=dict(sorted(distribution.items())),
                order3_type_cycles=0,
                panels=1,firm=False,residually_connected=False,
                literal_reset_nonincidence_witness=list(bad),
                adjacency_sha256=hashlib.sha256(json.dumps([sorted(s) for s in m['adj']],separators=(',',':')).encode()).hexdigest(),
                automorphism_search_backend_used=False)

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    need(not a.out.exists(),'fresh output directory');a.out.mkdir(parents=True)
    report=verify(json.loads((HERE/'data.json').read_text()))
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
