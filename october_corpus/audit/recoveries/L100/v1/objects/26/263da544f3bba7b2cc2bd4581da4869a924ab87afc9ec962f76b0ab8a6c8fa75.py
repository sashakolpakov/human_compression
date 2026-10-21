"""Literal kernel positions, quotient tables and actual complements; no census."""
import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,itertools,json,time
from pathlib import Path
from atoms_v3 import Context,need,read,image,parity
P=Path(__file__).resolve().parent

def quotient(C,H,K):
    need(K<=H and all(C.conjugate(k,h)in K for k in K for h in C.generators(H)),'normal actual local kernel')
    unseen=set(H);cosets=[];lookup={}
    while unseen:
        h=min(unseen);D={C.product(k,h)for k in K};need(D<=unseen,'disjoint kernel cosets')
        j=len(cosets);cosets.append(sorted(D))
        for x in D:lookup[x]=j
        unseen-=D
    reps=[x[0]for x in cosets]
    table=[[lookup[C.product(x,y)]for y in reps]for x in reps]
    return dict(cosets=[[x+1 for x in d]for d in cosets],multiplication=table,identity=lookup[C.one])

def normal(C,H,parts):
    words=[C.one]
    for part in parts:words=[C.product(x,y)for x in words for y in part]
    need(len(words)==len(set(words))==len(H) and set(words)==H,'exact factorization with unique words')
    return [x+1 for x in words]

def vector_basis(C,N,p=2):
    gs=[];K={C.one}
    for x in sorted(N):
        if x not in K:gs.append(x);K=C.closure(gs)
        if K==N:break
    need(K==N and all(C.order(x)in[1,p]for x in N)and all(C.product(x,y)==C.product(y,x)for x in gs for y in gs),'elementary abelian vector group')
    need(p**len(gs)==len(N),'independent vector basis')
    return gs

def projective(C,H,atom,K):
    """Recover the actual translation radical and a geometric Levi complement."""
    lines=C.meta['lines'];gs=C.generators(H)
    fixed_lines=[l for l in lines if all(image(l,C.es[g])==l for g in gs)]
    fixed_points=[x for x in range(21)if all(C.es[g][x]==x for g in gs)]
    if fixed_lines:
        line=fixed_lines[0];domain=[i for i in range(21)if line>>i&1]
        N={h for h in H if all(C.es[h][i]==i for i in domain)}
        point=next(i for i in range(21)if not line>>i&1)
        L={h for h in H if C.es[h][point]==point}
        acts=[tuple(domain.index(C.es[h][i])for i in domain)for h in sorted(L)]
        fixed=dict(line=line,external_point=point)
    else:
        need(fixed_points,'point or line fixed by projective atom');point=fixed_points[0]
        domain=[l for l in lines if l>>point&1]
        N={h for h in H if all(image(l,C.es[h])==l for l in domain)}
        line=next(l for l in lines if not l>>point&1)
        L={h for h in H if image(line,C.es[h])==line}
        acts=[tuple(domain.index(image(l,C.es[h]))for l in domain)for h in sorted(L)]
        fixed=dict(point=point,external_line=line)
    nb=vector_basis(C,N);need(len(N)==16 and len(nb)==4,'actual translation radical')
    need(all(C.conjugate(n,g)in N for n in N for g in gs),'normal radical')
    need(C.closure(C.generators(L))==L and N&L=={C.one}and len(L)*16==len(H),'actual complement')
    need(len(set(acts))==len(L) and all(parity(a)==0 for a in acts),'faithful alternating five-object Levi image')
    need(len(L)in[6,12,60],'exact Levi size')
    # The proper images are distinguished by actual fixed-set geometry, not size alone.
    if len(L)==12:need(any(all(a[i]==i for a in acts)for i in range(5)),'A4 fixes one object')
    if len(L)==6:need(any(all({a[i],a[j]}=={i,j}for a in acts)for i,j in itertools.combinations(range(5),2)),'S3 stabilizes a pair')
    out=dict(atom=atom,radical=[x+1 for x in sorted(N)],radical_basis=[x+1 for x in nb],levi=[x+1 for x in sorted(L)],levi_generators=[x+1 for x in C.generators(L)],levi_five_action=[list(a)for a in acts],fixed_geometry=fixed,normal_forms=normal(C,H,[sorted(N),sorted(L)]))
    if len(K)>1:
        need(K<=N,'boxed kernel lies in the literal translation radical')
        kb=vector_basis(C,K);V={C.one};vb=[]
        for x in sorted(N):
            if x in {C.product(k,v)for k in K for v in V}:continue
            vb.append(x);V=C.closure(vb)
            if len(K)*len(V)==16:break
        need(K&V=={C.one},'radical vector complement')
        out.update(kernel_basis=[x+1 for x in kb],radical_vector_complement=[x+1 for x in sorted(V)],radical_factorization=normal(C,N,[sorted(K),sorted(V)]),complement_invariant_under_levi=all(C.conjugate(v,l)in V for v in V for l in C.generators(L)))
    return out

def kernel_certificate(C,H,K,hrec,krec):
    q=quotient(C,H,K)if len(K)>1 else dict(identity_map_to_atom=hrec['atom'])
    r=dict(parabolic_atom=hrec['atom'],kernel_atom=krec['atom'],parabolic_order=len(H),kernel_order=len(K),quotient_order=len(H)//len(K),quotient=q)
    if len(H)in[96,192,960]:r['projective']=projective(C,H,hrec['atom'],K)
    if len(K)==1:return r|dict(extension='TRIVIAL_KERNEL')
    if len(H)==72:
        need(len(K)==36,'index-two affine quaternion kernel')
        outside=sorted(H-K);need(all(C.order(h)!=2 for h in outside),'no involution outside the kernel')
        r.update(extension='NONSPLIT_INDEX_TWO',outside_orders=[[x+1,C.order(x)]for x in outside],quotient_name='2')
    elif len(H)==16 and len(K)==8:
        need(krec['name']=='Q8','actual quaternion kernel')
        z=next(x for x in sorted(H-K)if C.order(x)==2 and all(C.product(x,k)==C.product(k,x)for k in K))
        r.update(extension='DIRECT_PRODUCT',central_complement=[C.one+1,z+1],normal_forms=normal(C,H,[sorted(K),[C.one,z]]),quotient_name='2')
    elif len(H)==16 and len(K)==4:
        need(krec['name']=='4','actual cyclic-four kernel');found=None
        for a,b in itertools.combinations(sorted(H-K),2):
            if C.order(a)!=2 or C.order(b)!=2 or C.product(a,b)!=C.product(b,a):continue
            L=C.closure([a,b])
            if len(L)==4 and L&K=={C.one}:found=(a,b,L);break
        need(found is not None,'actual elementary-four complement');a,b,L=found
        r.update(extension='SPLIT',complement=[x+1 for x in sorted(L)],complement_generators=[a+1,b+1],normal_forms=normal(C,H,[sorted(K),sorted(L)]),quotient_name='2^2')
    elif len(H)==16 and len(K)==2:
        need(all(C.product(k,h)==C.product(h,k)for k in K for h in H),'central boxed involution')
        need(all(C.power(h,2)in K for h in H),'elementary quotient exponent')
        # A complement to this central kernel would make H elementary abelian.
        need(any(C.order(h)==4 for h in H),'non-elementary actual group')
        r.update(extension='NONSPLIT_CENTRAL',quotient_name='2^3')
    elif len(H)==18:
        need(len(K)==3,'actual cyclic-three kernel');a=next(x for x in sorted(H-K)if C.order(x)==3)
        N=C.closure([a]);need(N&K=={C.one},'independent three factor')
        b=next(x for x in sorted(H)if C.order(x)==2);L=C.closure([a,b]);need(len(L)==6 and L&K=={C.one},'actual S3 complement')
        r.update(extension='SPLIT',quotient_name='S3',complement=[x+1 for x in sorted(L)],complement_generators=[a+1,b+1],normal_forms=normal(C,H,[sorted(K),sorted(L)]))
    elif len(H)in[96,192,960]:r['extension']='RADICAL_DECOMPOSITION_WITH_LEVI'
    else:raise ValueError('unhandled actual nontrivial kernel')
    return r

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--atoms',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir();t=time.monotonic();C=Context();src=read(P/'input01/inventory.json');atoms={r['atom']:r for r in read(a.atoms)['atoms']};sets={r['atom']:{x-1 for x in r['element_positions']}for r in src['atoms']};records={};routes=[]
    for row in src['routes']:
        for p in row['parabolics']:
            h=p['parabolic_atom'];k=p['kernel_atom'];key=f'{h}:{k}'
            if key not in records:records[key]=kernel_certificate(C,sets[h],sets[k],atoms[h],atoms[k])
            routes.append(dict(label=row['label'],catalogue=row['catalogue'],source_node=p['source_node'],type=p['type'],certificate=key))
    out=dict(status='COMPLETE_LITERAL_KERNEL_EXTENSIONS',certificates=records,routes=routes,seconds=time.monotonic()-t,target_censuses=0,source_credit=0)
    (a.out/'report.json').write_text(json.dumps(out,indent=2)+'\n');print('COMPLETE_KERNEL_EXTENSIONS',len(records),len(routes),flush=True)
if __name__=='__main__':main()
