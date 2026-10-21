"""Small literal structure certificates on the fixed retained subgroup sets."""
import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,functools,itertools,json,time
from pathlib import Path
P=Path(__file__).resolve().parent;G=P.parent
def need(v,s):
    if not v:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def mul(p,q):return tuple(q[x]for x in p)
def inv(p):
    out=[0]*len(p)
    for i,x in enumerate(p):out[x]=i
    return tuple(out)
def image(mask,p):return sum(1<<p[i]for i in range(21)if mask>>i&1)
def parity(p):return sum(p[i]>p[j]for i in range(len(p))for j in range(i+1,len(p)))%2
class Context:
    def __init__(self):
        raw=read(G/'palette_serialization_v1/derived/group_elements.json');self.es=[tuple(x-1 for x in p)for p in raw['elements']];self.index={p:i for i,p in enumerate(self.es)};self.one=self.index[tuple(range(21))]
        self.inverse=[self.index[inv(p)]for p in self.es]
        self.meta=read(G/'constructions_component_v1/expected/model.json');self.hyper=[x for r in self.meta['hyperoval_orbits']for x in r];self.baers=[x for r in read(G/'baer_component_v1/inputs/baer_orbits.json')['orbits']for x in r]
    @functools.lru_cache(maxsize=300000)
    def product(self,a,b):return self.index[mul(self.es[a],self.es[b])]
    def power(self,a,k):
        r=self.one
        for _ in range(k):r=self.product(r,a)
        return r
    def conjugate(self,a,b):return self.product(self.product(self.inverse[b],a),b)
    def closure(self,gs):
        out=[self.one];seen=set(out)
        for x in out:
            for g in gs:
                y=self.product(x,g)
                if y not in seen:seen.add(y);out.append(y)
        return seen
    def generators(self,H):
        gs=[];K={self.one}
        for x in sorted(H):
            if x not in K:gs.append(x);K=self.closure(gs);need(K<=H,'actual subgroup closure')
            if K==H:return gs
        need(K==H,'actual generating list');return gs
    def order(self,x):
        y=x;k=1
        while y!=self.one:y=self.product(y,x);k+=1;need(k<=20160,'finite order')
        return k

def certify(C,row):
    H={i-1 for i in row['element_positions']};gs=C.generators(H);n=len(H);orders={h:C.order(h)for h in H}
    result=dict(atom=row['atom'],order=n,generators=[g+1 for g in gs]);pows=C.power;prod=C.product;one=C.one
    def normal(words):
        need(len(words)==len(set(words))==n and set(words)==H,'every literal normal form exactly once');return [x+1 for x in words]
    def cyclic(a,k):return [pows(a,i)for i in range(k)]
    def on_points(mask,name,degree,alternating=False):
        xs=[i for i in range(21)if mask>>i&1];need(len(xs)==degree,'exact geometric object size');lookup={x:i for i,x in enumerate(xs)}
        acts=[]
        for h in sorted(H):
            need(image(mask,C.es[h])==mask,'all subgroup elements stabilize object');acts.append(tuple(lookup[C.es[h][x]]for x in xs))
        need(len(set(acts))==n,'faithful actual object action')
        if alternating:need(all(parity(p)==0 for p in acts)and n==__import__('math').factorial(degree)//2,'full alternating image')
        return result|dict(name=name,method='faithful_geometric_action',object_mask=mask,induced_permutations=[list(p)for p in acts])
    if n in [360,60]:
        for h in C.hyper:
            if not all(image(h,C.es[g])==h for g in gs):continue
            if n==360:return on_points(h,'A6',6,True)
            for p in range(21):
                if h>>p&1 and all(C.es[g][p]==p for g in gs):return on_points(h^(1<<p),'A5',5,True)|dict(parent_hyperoval=h,fixed_nucleus=p)
        if n==60:
            remaining=set(C.meta['lines'])
            while remaining:
                orbit=[min(remaining)];seen=set(orbit)
                for l in orbit:
                    for g in gs:
                        y=image(l,C.es[g])
                        if y not in seen:seen.add(y);orbit.append(y)
                remaining-=seen
                if len(orbit)!=5:continue
                orbit.sort();lookup={l:i for i,l in enumerate(orbit)}
                acts=[tuple(lookup[image(l,C.es[h])]for l in orbit)for h in sorted(H)]
                need(len(set(acts))==60 and all(parity(x)==0 for x in acts),'faithful alternating five-line action')
                return result|dict(name='A5',method='faithful_dual_oval_action',line_masks=orbit,induced_permutations=[list(p)for p in acts])
        raise ValueError('no exact hyperoval/oval or dual-oval action')
    if n==168:
        for b in C.baers:
            if not all(image(b,C.es[g])==b for g in gs):continue
            out=on_points(b,'L3(2)',7);lines=sorted({l&b for l in C.meta['lines']if(l&b).bit_count()==3});need(len(lines)==7,'actual Fano lines')
            need(all(len([l for l in lines if l>>i&1 and l>>j&1])==1 for i,j in itertools.combinations([x for x in range(21)if b>>x&1],2)),'Fano pair incidence')
            need(all({image(l,C.es[g])for l in lines}==set(lines)for g in gs),'full Fano incidence action');return out|dict(fano_lines=lines,frame_bound=168)
        raise ValueError('no exact Fano plane stabilized')
    if n in [960,96,192]:
        points=[i for i in range(21)if all(C.es[g][i]==i for g in gs)];lines=[l for l in C.meta['lines']if all(image(l,C.es[g])==l for g in gs)]
        if n==960:
            need(points or lines,'actual point or line stabilizer');return result|dict(name='2^4:A5',method='projective_stabilizer',point=points[0]if points else None,line=lines[0]if lines else None,stabilizer_order=960)
        if n==192:
            flags=[(p,l)for p in points for l in lines if l>>p&1];need(flags,'actual incident flag stabilizer');return result|dict(name='2^4:A4',method='projective_stabilizer',point=flags[0][0],line=flags[0][1],stabilizer_order=192)
        for x,y in itertools.combinations(range(21),2):
            if all({C.es[g][x],C.es[g][y]}=={x,y}for g in gs):return result|dict(name='2^4:S3',method='projective_stabilizer',point_pair=[x,y],stabilizer_order=96)
        for x,y in itertools.combinations(C.meta['lines'],2):
            if all({image(x,C.es[g]),image(y,C.es[g])}=={x,y}for g in gs):return result|dict(name='2^4:S3',method='projective_stabilizer',line_pair=[x,y],stabilizer_order=96)
        raise ValueError('no actual unordered pair stabilized')
    if max(orders.values())<=2:
        need(n&(n-1)==0,'elementary abelian order');basis=[];K={one}
        for x in sorted(H):
            if x not in K:basis.append(x);K=C.closure(basis)
            if K==H:break
        words=[one]
        for x in basis:words += [prod(w,x)for w in words]
        return result|dict(name='1'if n==1 else '2'if n==2 else f'2^{len(basis)}',method='elementary_abelian',basis=[x+1 for x in basis],normal_forms=normal(words))
    if max(orders.values())==n:
        x=next(x for x in sorted(H)if orders[x]==n);return result|dict(name=str(n),method='cyclic',generator=x+1,normal_forms=normal(cyclic(x,n)))
    if n in [12,24]:
        triples=sorted({frozenset(cyclic(h,3))for h in H if orders[h]==3},key=lambda x:tuple(sorted(x)));need(len(triples)==4,'four actual cyclic three-subgroups')
        lookup={K:i for i,K in enumerate(triples)};acts=[tuple(lookup[frozenset(C.conjugate(x,h)for x in K)]for K in triples)for h in sorted(H)]
        need(len(set(acts))==n and(n==24 or all(parity(p)==0 for p in acts)),'faithful full alternating/symmetric four-point action')
        return result|dict(name='A4'if n==12 else'S4',method='four_cyclic_subgroups',subgroups=[[x+1 for x in sorted(K)]for K in triples],induced_permutations=[list(p)for p in acts])
    if n in [6,21]:
        k=3 if n==6 else 7;l=2 if n==6 else 3
        for a in sorted(H):
            if orders[a]!=k:continue
            for b in sorted(H):
                if orders[b]!=l:continue
                exponent=next((i for i in range(1,k)if C.conjugate(a,b)==pows(a,i)),None)
                if exponent not in ([2]if n==6 else[2,4]):continue
                words=[prod(pows(a,i),pows(b,j))for i in range(k)for j in range(l)]
                if len(set(words))==n:return result|dict(name='S3'if n==6 else'7:3',method='cyclic_semidirect',generators=[a+1,b+1],conjugation_exponent=exponent,normal_forms=normal(words))
    if n in [8,16]:
        quaternion=sum(o==2 for o in orders.values())in[1,3]
        for a in sorted(H):
            if orders[a]!=4:continue
            for b in sorted(H):
                if orders[b]!=(4 if quaternion else 2)or C.conjugate(a,b)!=C.inverse[a]:continue
                if quaternion and pows(a,2)!=pows(b,2):continue
                core=[prod(pows(a,i),pows(b,j))for i in range(4)for j in range(2)]
                if len(set(core))!=8:continue
                if n==8:return result|dict(name='Q8'if quaternion else'D8',method='quaternion_or_dihedral',generators=[a+1,b+1],normal_forms=normal(core))
                for z in sorted(H-set(core)):
                    if orders[z]==2 and all(prod(z,g)==prod(g,z)for g in [a,b]):
                        return result|dict(name='2xQ8'if quaternion else'2xD8',method='split_central_product',generators=[a+1,b+1,z+1],normal_forms=normal(core+[prod(w,z)for w in core]))
    if n in [18,36,72]:
        N={x for x,o in orders.items()if o in [1,3]};need(len(N)==9 and C.closure(sorted(N))==N,'actual normal elementary three-square candidate')
        a=next(x for x in sorted(N)if x!=one);b=next(x for x in sorted(N)if x not in cyclic(a,3));coords={prod(pows(a,i),pows(b,j)):(i,j)for i in range(3)for j in range(3)}
        need(len(coords)==9 and prod(a,b)==prod(b,a),'exact E9 coordinates')
        need(all(C.conjugate(x,g)in N for x in N for g in gs),'actual E9 normality')
        complement=None
        if n in [18,36]:
            k=n//9;r=next(x for x in sorted(H)if orders[x]==k);complement=cyclic(r,k);cg=[r]
        else:
            for r in sorted(H):
                if orders[r]!=4:continue
                for s in sorted(H):
                    if orders[s]==4 and pows(r,2)==pows(s,2)and C.conjugate(r,s)==C.inverse[r]:
                        K=C.closure([r,s])
                        if len(K)==8:complement=sorted(K);cg=[r,s];break
                if complement is not None:break
        need(complement is not None and len(set(complement)&N)==1,'exact complement')
        matrices=[]
        for h in complement:
            x=coords[C.conjugate(a,h)];y=coords[C.conjugate(b,h)];matrices.append([x[0],y[0],x[1],y[1]])
        need(len({tuple(M)for M in matrices})==len(complement),'faithful complement action')
        if n==18:need(set(map(tuple,matrices))=={(1,0,0,1),(2,0,0,2)},'inversion action')
        if n==36:
            M=matrices[1];need(((M[0]*M[0]+M[1]*M[2])%3,(M[0]*M[1]+M[1]*M[3])%3,(M[2]*M[0]+M[3]*M[2])%3,(M[2]*M[1]+M[3]*M[3])%3)==(2,0,0,2),'irreducible C4 square-minus-identity action')
        if n==72:
            standard={(1,0,0,1),(2,0,0,2)}|{(a,b,c,d)for a,b,c,d in itertools.product(range(3),repeat=4)if(a+d)%3==0 and(a*d-b*c)%3==1}
            need(set(map(tuple,matrices))==standard and len(standard)==8,'literal standard quaternion action in GL2(3)')
        words=[prod(x,h)for x in coords for h in complement]
        return result|dict(name={18:'3:S3',36:'3^2:4',72:'3^2:Q8'}[n],method='elementary_three_semidirect',normal_basis=[a+1,b+1],complement_generators=[x+1 for x in cg],complement_elements=[x+1 for x in complement],action_matrices=matrices,normal_forms=normal(words))
    raise ValueError('unpaid atom '+str(row['atom'])+' order '+str(n))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir();t=time.monotonic();C=Context();source=read(P/'input01/inventory.json');records=[]
    for row in source['atoms']:
        result=certify(C,row);records.append(result);print('ATOM',row['atom'],result['name'],result['method'],flush=True)
        (a.out/'partial.json').write_text(json.dumps(dict(records=records),indent=2)+'\n')
    (a.out/'report.json').write_text(json.dumps(dict(status='COMPLETE_LITERAL_ATOM_CERTIFICATES',atoms=records,seconds=time.monotonic()-t,target_censuses=0,source_credit=0),indent=2)+'\n')
if __name__=='__main__':main()
