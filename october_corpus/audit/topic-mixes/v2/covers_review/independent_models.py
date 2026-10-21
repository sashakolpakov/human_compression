#!/usr/bin/env python3
"""Independent finite diagnostics; no imports of author algorithms or tables.
The all-parameter proof remains the reviewed written semidirect argument.
"""
import argparse,itertools,json
from collections import Counter,deque

def need(ok,why):
    if not ok:raise RuntimeError(why)
def orbit(adj,root,colors,allowed=None):
    seen={root};todo=[root]
    for x in todo:
        for i in colors:
            y=adj(x,i)
            if allowed is not None and y not in allowed:continue
            if y not in seen:seen.add(y);todo.append(y)
    return frozenset(seen)
def partition(points,adj,colors):
    left=set(points);parts=[]
    while left:
        c=orbit(adj,min(left),colors);need(c<=left,'component closure')
        parts.append(c);left-=c
    return parts
def geom(points,adj,rank):
    points=list(points);allset=set(points)
    need(len(orbit(adj,points[0],range(rank)))==len(points),'connectivity')
    for x in points:
        ys=[adj(x,i) for i in range(rank)]
        need(len(set(ys+[x]))==rank+1,'simple properly colored graph')
        for i in range(rank):
            need(adj(ys[i],i)==x,'involution')
            for j in range(i+2,rank):need(adj(ys[i],j)==adj(ys[j],i),'distant square')
    fs=[partition(points,adj,[j for j in range(rank) if j!=i]) for i in range(rank)]
    tables=[{x:j for j,f in enumerate(ff) for x in f} for ff in fs]
    fibres=Counter(tuple(t[x] for t in tables)for x in points)
    dia=Counter()
    padded=[[frozenset(points)]]+fs+[[frozenset(points)]]
    for i in range(rank):
        for low in padded[i]:
            for high in padded[i+2]:
                if low&high:dia[sum(bool(f&low)and bool(f&high)for f in fs[i])]+=1
    return {'flags':len(points),'face_numbers':list(map(len,fs)),
        'flag_fiber_sizes':sorted(set(fibres.values())),
        'diamond_distribution':dict(dia)},fs

def product(p,q):return tuple(q[p[i]] for i in range(16))
ID=tuple(range(16))
def base():
    # Independent integer encodings of the two binary affine planes.
    rr=(tuple(x^1 for x in range(16)),
        tuple(x^((x&1)<<1)^((x&4)<<1) for x in range(16)),
        tuple(x^((x&2)>>1)^((x&8)>>1) for x in range(16)),
        tuple(x^8 for x in range(16)))
    perms={ID};todo=[ID]
    for p in todo:
        for r in rr:
            q=product(p,r)
            if q not in perms:perms.add(q);todo.append(q)
    need(len(perms)==96,'independent affine group size')
    T={tuple(x^v for x in range(16))for v in range(16)}
    need(T<=perms,'literal translations')
    ordered=[ID]+sorted(perms-{ID});ix={p:i for i,p in enumerate(ordered)}
    adj=[[ix[product(p,r)]for r in rr]for p in ordered]
    left=[[ix[product(r,p)]for r in rr]for p in ordered]
    translation={ix[p]for p in T}
    def z(a,i):
        if i!=2:return 0
        return 1 if a in translation else (-1 if adj[a][2]in translation else 0)
    def h(a):return 0 if a in translation or left[a][1]in translation else 1
    need(sum(z(a,2)==1 for a in range(96))==16,'sixteen positive origins')
    for a,i in itertools.product(range(96),range(4)):
        need(z(adj[a][i],i)==-z(a,i),'dart reversal')
        need(z(left[a][1],i)==-z(a,i)+h(adj[a][i])-h(a),'all integer gauge identities')
        for j,s in [(0,1),(2,-1),(3,1)]:need(z(left[a][j],i)==s*z(a,i),'other literal lifts')
    o=orbit(lambda x,i:adj[x][i],0,[0,2,3])
    need(len(o)==16 and len(o&translation)==8,'edge split')
    # All source relations are directly checked on the independent permutations.
    words=[(i,i)for i in range(4)]+[(0,1)*4,(1,2)*3,(2,3)*4,(0,2)*2,(0,3)*2,(1,3)*2,(0,1,2)*3,(1,2,3)*3]
    for w in words:
        p=ID
        for i in w:p=product(p,rr[i])
        need(p==ID,'source universal relator')
    return adj,z

def family(m,badj,z,wrong_voltage=False):
    points=list(itertools.product(range(96),range(m)))
    def adj(x,i):
        a,j=x;v=z(a,i)
        if wrong_voltage and a==0 and i==2:v=0
        return(badj[a][i],(j+v)%m)
    # Explicit BFS isomorphism to the pullback by the marked dihedral group.
    mapping={(0,0):(0,0)};todo=[(0,0)]
    for x in todo:
        k,t=mapping[x]
        for i in range(4):
            y=adj(x,i)
            d=((k+((-1)**t if i==2 else 0))%(3*m),t^int(i in (1,2)))
            if y in mapping:need(mapping[y]==d,'literal voltage / dihedral consistency')
            else:mapping[y]=d;todo.append(y)
    need(len(mapping)==96*m,'voltage connectivity')
    pairs={(a,mapping[a,j])for a,j in mapping}
    need(len(pairs)==96*m,'marked pullback bijection')
    subs=[orbit(adj,(0,0),[i for i in range(4)if mask>>i&1])for mask in range(16)]
    for a,b in itertools.product(range(16),repeat=2):need(subs[a]&subs[b]==subs[a&b],'all256 IP')
    r,fs=geom(points,adj,4)
    need(r['face_numbers']==[4,6*m,6*m,4] and r['flag_fiber_sizes']==[1] and set(r['diamond_distribution'])=={2},'polytope face geometry')
    dp=list(itertools.product(points,range(2)))
    def dadj(x,i):return(adj(x[0],i),x[1]^1)
    dr,dfs=geom(dp,dadj,4)
    need(dr['face_numbers']==[4,12*m,12*m,4] and dr['flag_fiber_sizes']==[1] and set(dr['diamond_distribution'])=={2},'double geometry')
    a=next(f for f in dfs[0]if((0,0),0)in f);b=next(f for f in dfs[3]if((0,0),0)in f)
    cc=partition(a&b,dadj,[1,2]);need(sorted(map(len,cc))==[6*m,6*m],'double endpoint obstruction')
    # Direct source raviolo, tested through two successive ranks.
    higher=[];oldpoints=dp;oldadj=dadj
    if m in (1,2):
        for rank in (5,6):
            np=list(itertools.product(oldpoints,range(2)))
            def na(x,i,oldadj=oldadj,rank=rank):
                return (oldadj(x[0],i),x[1])if i<rank-1 else(x[0],x[1]^1)
            gr,gfs=geom(np,na,rank)
            need(gr['flag_fiber_sizes']==[1]and set(gr['diamond_distribution'])=={2},'raviolo faithful thin')
            # The original bad endpoint intersection inside one new facet persists.
            seed=np[0]; ff=[next(f for f in gfs[i]if seed in f)for i in [0,3]+list(range(4,rank))]
            inter=set.intersection(*(set(f)for f in ff));cs=partition(inter,na,[1,2])
            need(sorted(map(len,cs))==[6*m,6*m],'raviolo persistent CIP failure')
            higher.append(gr);oldpoints=np;oldadj=na
    return {'m':m,'base':r,'double':dr,'marked_pullback_pairs':len(pairs),'IP_tests':256,'higher_ranks':higher}

def controls(adj,z):
    labels=[]
    try:family(4,adj,z,True)
    except RuntimeError as e:
        need('dihedral consistency'in str(e),'wrong mutation failure');labels.append('deleted_single_integer_voltage')
    else:raise RuntimeError('accepted deleted voltage')
    bad=lambda x,i:adj[x][0 if i==3 else i]
    try:geom(orbit(bad,0,range(4)),bad,4)
    except RuntimeError as e:
        need(str(e)=='simple properly colored graph','coincident-color rejection');labels.append('coincident_colors_rejected')
    else:raise RuntimeError('accepted coincident colors')
    # Generic projection: dropping image equality makes trivial-fiber data insufficient.
    # W=C2 acts regularly on both Q and X, pi=id, A=B=W, C=1.
    need({0,1}&{0,1}!={0} and ({0,1}&{0})=={0},'projection base premise countermodel')
    labels.append('projection_requires_base_intersection')
    # Gauge identity is necessary even for identity phi,f on a two-vertex edge.
    need(0!=0+1-0,'voltage lift premise countermodel');labels.append('lift_requires_gauge_equation')
    return labels

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args()
    adj,z=base();rows=[family(m,adj,z)for m in(1,2,4,7)]
    result={'status':'PASS','implementation':'independent pure Python permutation/voltage BFS; no author imports',
      'affine_base_order':96,'source_relators':12,'integer_lift_checks':1536,
      'families':rows,'controls':controls(adj,z),'uniform_proof_not_inferred_from_samples':True}
    open(a.out,'w').write(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','samples':4,'rank6_checked':True,'controls':len(result['controls'])}))
if __name__=='__main__':main()
