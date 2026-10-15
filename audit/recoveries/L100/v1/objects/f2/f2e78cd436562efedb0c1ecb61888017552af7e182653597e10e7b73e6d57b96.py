"""Validate literal saved witnesses; no search for generators or structures."""
import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,copy,itertools,json,math
from pathlib import Path
from atoms_v3 import Context,need,read,image,parity
P=Path(__file__).resolve().parent

def forms(C,H,parts,record):
    words=[C.one]
    for part in parts:words=[C.product(x,y)for x in words for y in part]
    need([x+1 for x in words]==record and len(words)==len(set(words))==len(H)and set(words)==H,'actual unique normal forms')

def validate_atom(C,H,r):
    n=len(H);gs=[g-1 for g in r['generators']];need(n==r['order']and set(gs)<=H and C.closure(gs)==H,'actual atom generators')
    name=r['name'];m=r['method'];powers=lambda x,k:[C.power(x,i)for i in range(k)]
    if m in ['faithful_geometric_action','faithful_dual_oval_action','four_cyclic_subgroups']:
        if m=='faithful_geometric_action':
            mask=r['object_mask'];domain=[i for i in range(21)if mask>>i&1]
            maps=[tuple(domain.index(C.es[h][i])for i in domain)for h in sorted(H)]
        elif m=='faithful_dual_oval_action':
            domain=r['line_masks'];need(len(set(domain))==5 and set(domain)<=set(C.meta['lines']),'five actual lines')
            maps=[tuple(domain.index(image(l,C.es[h]))for l in domain)for h in sorted(H)]
        else:
            domain=[frozenset(x-1 for x in K)for K in r['subgroups']]
            need(len(set(domain))==4 and all(len(K)==3 and C.closure(sorted(K))==K for K in domain),'four literal C3 subgroups')
            maps=[tuple(domain.index(frozenset(C.conjugate(x,h)for x in K))for K in domain)for h in sorted(H)]
        need([list(a)for a in maps]==r['induced_permutations']and len(set(maps))==n,'literal faithful action')
        if name in ['A4','A5','A6']:need(n==math.factorial(len(domain))//2 and all(parity(a)==0 for a in maps),'full alternating image')
        elif name=='S4':need(len(domain)==4 and n==24,'full symmetric four action')
        elif name=='L3(2)':
            lines=r['fano_lines'];need(len(domain)==7 and n==168 and len(lines)==7 and set(lines)=={l&r['object_mask']for l in C.meta['lines']if(l&r['object_mask']).bit_count()==3},'actual Fano plane')
            need(all(sum(l>>i&1 and l>>j&1 for l in lines)==1 for i,j in itertools.combinations(domain,2)),'Fano pair axiom')
            need(all({image(l,C.es[g])for l in lines}==set(lines)for g in gs),'literal Fano automorphisms')
        else:raise ValueError('unknown faithful name')
    elif m=='projective_stabilizer':
        need(name=={960:'2^4:A5',192:'2^4:A4',96:'2^4:S3'}[n],'projective structural name')
        if r.get('point')is not None:need(all(C.es[g][r['point']]==r['point']for g in gs),'literal fixed point')
        if r.get('line')is not None:need(r['line']in C.meta['lines']and all(image(r['line'],C.es[g])==r['line']for g in gs),'literal fixed line')
        if 'point_pair'in r:need(len(set(r['point_pair']))==2 and all({C.es[g][x]for x in r['point_pair']}==set(r['point_pair'])for g in gs),'literal point pair')
        if 'line_pair'in r:need(len(set(r['line_pair']))==2 and set(r['line_pair'])<=set(C.meta['lines'])and all({image(x,C.es[g])for x in r['line_pair']}==set(r['line_pair'])for g in gs),'literal line pair')
    elif m=='elementary_abelian':
        bs=[x-1 for x in r['basis']];need(all(C.power(x,2)==C.one for x in bs)and all(C.product(x,y)==C.product(y,x)for x in bs for y in bs),'commuting involution basis')
        words=[C.one]
        for x in bs:words += [C.product(w,x)for w in words]
        need([x+1 for x in words]==r['normal_forms']and len(words)==len(set(words))==n and set(words)==H,'binary normal forms')
        need(name==('1'if n==1 else'2'if n==2 else f'2^{len(bs)}'),'elementary group name')
    elif m=='cyclic':
        a=r['generator']-1;forms(C,H,[powers(a,n)],r['normal_forms']);need(name==str(n),'cyclic group name')
    elif m=='cyclic_semidirect':
        a,b=gs;k,l=(3,2)if name=='S3'else(7,3);need(name in['S3','7:3']and C.order(a)==k and C.order(b)==l,'cyclic semidirect orders')
        e=r['conjugation_exponent'];need(e in([2]if k==3 else[2,4])and C.conjugate(a,b)==C.power(a,e),'literal nontrivial cyclic action');forms(C,H,[powers(a,k),powers(b,l)],r['normal_forms'])
    elif m in ['quaternion_or_dihedral','split_central_product']:
        a,b=gs[:2];q='Q8'in name;need(name in['Q8','D8','2xQ8','2xD8']and C.order(a)==4 and C.order(b)==(4 if q else 2)and C.conjugate(a,b)==C.inverse[a],'actual quaternion/dihedral relations')
        if q:need(C.power(a,2)==C.power(b,2),'common quaternion square')
        core=[C.product(x,y)for x in powers(a,4)for y in powers(b,2)];need(len(set(core))==8,'eight-element core')
        words=core
        if m=='split_central_product':
            z=gs[2];need(C.order(z)==2 and z not in core and all(C.product(z,g)==C.product(g,z)for g in[a,b]),'disjoint central involution');words=core+[C.product(w,z)for w in core]
        need([x+1 for x in words]==r['normal_forms']and set(words)==H and len(set(words))==n,'literal direct-factor words')
    elif m=='elementary_three_semidirect':
        a,b=[x-1 for x in r['normal_basis']];need(C.order(a)==C.order(b)==3 and C.product(a,b)==C.product(b,a),'commuting order-three basis')
        coords={C.product(C.power(a,i),C.power(b,j)):(i,j)for i in range(3)for j in range(3)};need(len(coords)==9,'nine distinct translations')
        L=[x-1 for x in r['complement_elements']];cg=[x-1 for x in r['complement_generators']];need(C.closure(cg)==set(L)and set(coords)&set(L)=={C.one},'literal complement')
        need(all(C.conjugate(x,g)in coords for x in coords for g in gs),'normal translations')
        mats=[]
        for h in L:
            x=coords[C.conjugate(a,h)];y=coords[C.conjugate(b,h)];mats.append([x[0],y[0],x[1],y[1]])
        need(mats==r['action_matrices']and len(set(map(tuple,mats)))==len(L),'faithful literal action matrices')
        I=(1,0,0,1);minus=(2,0,0,2)
        if n==18:need(name=='3:S3'and set(map(tuple,mats))=={I,minus},'inversion semidirect')
        elif n==36:
            need(name=='3^2:4'and len(cg)==1 and C.order(cg[0])==4,'cyclic-four complement');h=C.power(cg[0],2);need(C.conjugate(a,h)==C.inverse[a]and C.conjugate(b,h)==C.inverse[b],'square acts minus identity')
        elif n==72:
            standard={I,minus}|{(a,b,c,d)for a,b,c,d in itertools.product(range(3),repeat=4)if(a+d)%3==0 and(a*d-b*c)%3==1};need(name=='3^2:Q8'and len(standard)==8 and set(map(tuple,mats))==standard,'standard quaternion matrices')
        else:raise ValueError('unknown three-semidir name')
        forms(C,H,[list(coords),L],r['normal_forms'])
    else:raise ValueError('unknown atom method')

def validate_kernel(C,H,K,r):
    need(len(H)==r['parabolic_order']and len(K)==r['kernel_order']and len(H)//len(K)==r['quotient_order']and K<=H,'kernel sizes and inclusion')
    gs=C.generators(H);need(all(C.conjugate(k,g)in K for k in K for g in gs),'actual kernel normality')
    if len(K)>1:
        q=r['quotient'];cosets=[set(x-1 for x in d)for d in q['cosets']];need(sum(map(len,cosets))==len(H)and set.union(*cosets)==H and all(len(d)==len(K)for d in cosets),'whole disjoint quotient partition')
        pos={x:i for i,d in enumerate(cosets)for x in d};reps=[min(d)for d in cosets]
        need(all({C.product(k,h)for k in K}==d for h,d in zip(reps,cosets)),'actual kernel cosets')
        need(q['multiplication']==[[pos[C.product(x,y)]for y in reps]for x in reps]and q['identity']==pos[C.one],'literal quotient multiplication')
    else:need(r['extension']=='TRIVIAL_KERNEL'and r['quotient']==dict(identity_map_to_atom=r['parabolic_atom']),'trivial kernel identity')
    if 'projective'in r:
        p=r['projective'];N={x-1 for x in p['radical']};L={x-1 for x in p['levi']};nb=[x-1 for x in p['radical_basis']];lg=[x-1 for x in p['levi_generators']]
        need(len(N)==16 and len(nb)==4 and C.closure(nb)==N and all(C.power(x,2)==C.one for x in N),'actual elementary radical')
        need(N<=H and L<=H and C.closure(lg)==L and N&L=={C.one}and all(C.conjugate(x,g)in N for x in N for g in gs),'actual semidirect factors')
        f=p['fixed_geometry']
        if 'external_point'in f:
            line=f['line'];point=f['external_point'];need(line in C.meta['lines']and not line>>point&1,'nonincident complementary point')
            domain=[i for i in range(21)if line>>i&1];need(N=={h for h in H if all(C.es[h][i]==i for i in domain)}and L=={h for h in H if C.es[h][point]==point},'literal geometric factors')
            acts=[tuple(domain.index(C.es[h][i])for i in domain)for h in sorted(L)]
        else:
            point=f['point'];line=f['external_line'];need(line in C.meta['lines']and not line>>point&1,'nonincident complementary line');domain=[l for l in C.meta['lines']if l>>point&1]
            need(N=={h for h in H if all(image(l,C.es[h])==l for l in domain)}and L=={h for h in H if image(line,C.es[h])==line},'literal dual geometric factors');acts=[tuple(domain.index(image(l,C.es[h]))for l in domain)for h in sorted(L)]
        need(p['levi_five_action']==[list(a)for a in acts]and len(set(acts))==len(L)and all(parity(a)==0 for a in acts),'faithful Levi action')
        if len(L)==12:need(any(all(a[i]==i for a in acts)for i in range(5)),'A4 image')
        elif len(L)==6:need(any(all({a[i],a[j]}=={i,j}for a in acts)for i,j in itertools.combinations(range(5),2)),'S3 image')
        else:need(len(L)==60,'A5 image')
        forms(C,H,[sorted(N),sorted(L)],p['normal_forms'])
        if len(K)>1:
            V={x-1 for x in p['radical_vector_complement']};need(K<=N and V<=N and K&V=={C.one}and C.closure(sorted(V))==V,'actual radical subspaces');forms(C,N,[sorted(K),sorted(V)],p['radical_factorization']);need(p['complement_invariant_under_levi']==all(C.conjugate(v,g)in V for v in V for g in lg),'no unproved invariant complement')
    e=r['extension']
    if e=='NONSPLIT_INDEX_TWO':need(len(H)==72 and len(K)==36 and r['outside_orders']==[[x+1,C.order(x)]for x in sorted(H-K)]and all(C.order(x)!=2 for x in H-K),'no index-two complement')
    elif e=='NONSPLIT_CENTRAL':need(len(H)==16 and len(K)==2 and all(C.product(k,h)==C.product(h,k)for k in K for h in H)and all(C.power(h,2)in K for h in H)and any(C.order(h)==4 for h in H),'nonsplit central extension')
    elif e in ['SPLIT','DIRECT_PRODUCT']:
        L={x-1 for x in r['central_complement'if e=='DIRECT_PRODUCT'else'complement']};need(C.closure(sorted(L))==L and L<=H and K&L=={C.one},'actual extension complement');forms(C,H,[sorted(K),sorted(L)],r['normal_forms'])
        if e=='DIRECT_PRODUCT':need(all(C.product(k,l)==C.product(l,k)for k in K for l in L),'central direct factor')
    else:need(e in['TRIVIAL_KERNEL','RADICAL_DECOMPOSITION_WITH_LEVI'],'known extension scope')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--atoms',type=Path,required=True);ap.add_argument('--kernels',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir();C=Context();src=read(P/'input01/inventory.json');sets={r['atom']:{x-1 for x in r['element_positions']}for r in src['atoms']};ar=read(a.atoms)['atoms'];kr=read(a.kernels)['certificates'];need(len(ar)==77 and len({r['atom']for r in ar})==77,'complete distinct atoms')
    for r in ar:validate_atom(C,sets[r['atom']],r)
    for r in kr.values():validate_kernel(C,sets[r['parabolic_atom']],sets[r['kernel_atom']],r)
    failures=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError,TypeError,StopIteration):failures.append(name);return
        raise ValueError('damaged witness accepted: '+name)
    for method in sorted({r['method']for r in ar}):
        r=copy.deepcopy(next(r for r in ar if r['method']==method and r['order']>1));r['generators']=[C.one+1];reject('wrong-generators-'+method,lambda r=r:validate_atom(C,sets[r['atom']],r))
    for method in ['faithful_geometric_action','faithful_dual_oval_action','four_cyclic_subgroups']:
        r=copy.deepcopy(next(r for r in ar if r['method']==method));r['induced_permutations'][0]=r['induced_permutations'][1];reject('damaged-action-'+method,lambda r=r:validate_atom(C,sets[r['atom']],r))
    for extension in ['NONSPLIT_INDEX_TWO','NONSPLIT_CENTRAL','SPLIT','DIRECT_PRODUCT','RADICAL_DECOMPOSITION_WITH_LEVI']:
        r=copy.deepcopy(next(r for r in kr.values()if r['extension']==extension));r['kernel_order']+=1;reject('wrong-kernel-'+extension,lambda r=r:validate_kernel(C,sets[r['parabolic_atom']],sets[r['kernel_atom']],r))
    r=copy.deepcopy(next(r for r in kr.values()if r['kernel_order']>1));r['quotient']['multiplication'][0][0]=1-r['quotient']['multiplication'][0][0];reject('wrong-quotient-table',lambda:validate_kernel(C,sets[r['parabolic_atom']],sets[r['kernel_atom']],r))
    r=copy.deepcopy(next(r for r in kr.values()if 'projective'in r));r['projective']['levi'][0]=C.one+1;r['projective']['levi'][1]=C.one+1;reject('fake-Levi-factor',lambda:validate_kernel(C,sets[r['parabolic_atom']],sets[r['kernel_atom']],r))
    r=copy.deepcopy(next(r for r in ar if r['method']=='elementary_three_semidirect'));r['action_matrices'][0]=[0,0,0,0];reject('wrong-action-matrix',lambda:validate_atom(C,sets[r['atom']],r))
    out=dict(status='PASS_LITERAL_PARABOLIC_WITNESSES',atoms=len(ar),kernel_certificates=len(kr),damage_controls=failures,target_censuses=0,source_credit=0);(a.out/'report.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
