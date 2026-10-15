"""Literal finite models; no subgroup-classification or graph-isomorphism API."""
import sys
if sys.flags.optimize:
    raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse, ast, hashlib, itertools, json
from collections import Counter, deque
from pathlib import Path

def need(ok, why):
    if not ok: raise ValueError(why)

def bits(x):
    while x:
        b=x & -x; yield b.bit_length()-1; x-=b

def mask(xs): return sum(1<<x for x in xs)
def image(s,p): return mask(p[x] for x in bits(s))
def mul(p,q): return tuple(q[x] for x in p)

def closure(gens,n):
    identity=tuple(range(n)); found={identity}; todo=[identity]
    for p in todo:
        for g in gens:
            q=mul(p,g)
            if q not in found: found.add(q);todo.append(q)
    return todo

def orbit(seed, gens):
    found={seed}; todo=[seed]
    for s in todo:
        for p in gens:
            t=image(s,p)
            if t not in found: found.add(t);todo.append(t)
    return sorted(found)

def fm(a,b):
    z=0
    while b:
        if b&1: z^=a
        b>>=1; a<<=1
        if a&4: a^=7
    return z

def fs(xs):
    z=0
    for x in xs: z^=x
    return z

def normalize(v):
    a=next(x for x in v if x)
    inv=next(b for b in range(1,4) if fm(a,b)==1)
    return tuple(fm(x,inv) for x in v)

def determinant(a):
    return fs(fm(fm(a[0][p[0]],a[1][p[1]]),a[2][p[2]]) for p in itertools.permutations(range(3)))

def mat_image(v,a):
    return normalize(tuple(fs(fm(a[i][j],v[j]) for j in range(3)) for i in range(3)))

def coordinate_plane():
    pts=sorted({normalize(v) for v in itertools.product(range(4),repeat=3) if any(v)})
    lines=sorted({mask(i for i,v in enumerate(pts) if fs(fm(x,y) for x,y in zip(a,v))==0) for a in pts})
    need(len(pts)==len(lines)==21,'coordinate plane size')
    return pts,lines

def plane_tables(lines):
    need(len(lines)==21 and len(set(lines))==21 and all(x.bit_count()==5 for x in lines),'plane lines')
    joins={}
    for li,l in enumerate(lines):
        for a,b in itertools.combinations(bits(l),2):
            need((a,b) not in joins,'two lines on a pair');joins[a,b]=li
    need(len(joins)==210,'plane pair coverage')
    meets={}
    for a,b in itertools.combinations(range(21),2):
        m=lines[a]&lines[b];need(m.bit_count()==1,'line meet');meets[a,b]=next(bits(m))
    return joins,meets

def plane_map(source,target,initial):
    """Backtracking joins/meets with an explicit final all-incidences check."""
    sj,sm=plane_tables(source);tj,tm=plane_tables(target)
    def extend(mapping):
        mapping=dict(mapping)
        while True:
            lm={}; reverse={}
            for a,b in itertools.combinations(sorted(mapping),2):
                l=sj[a,b];m=tj[tuple(sorted((mapping[a],mapping[b])))]
                if l in lm and lm[l]!=m: return None
                if m in reverse and reverse[m]!=l:return None
                lm[l]=m;reverse[m]=l
            additions={}
            for a,b in itertools.combinations(sorted(lm),2):
                p=sm[a,b];q=tm[tuple(sorted((lm[a],lm[b])))]
                if p in mapping and mapping[p]!=q:return None
                if p in additions and additions[p]!=q:return None
                additions[p]=q
            enlarged=dict(mapping);enlarged.update(additions)
            if len(set(enlarged.values()))!=len(enlarged):return None
            if len(enlarged)==len(mapping):break
            mapping=enlarged
        if len(mapping)==21:return tuple(mapping[i] for i in range(21))
        options=[]
        for p in range(21):
            if p in mapping:continue
            available=set(range(21))-set(mapping.values())
            for l,m in lm.items():
                available &= set(bits(target[m])) if (source[l]>>p)&1 else set(range(21))-set(bits(target[m]))
            options.append((len(available),p,sorted(available)))
        _,p,available=min(options)
        for q in available:
            ans=extend(mapping | {p:q})
            if ans is not None:return ans
        return None
    ans=extend(initial)
    need(ans is not None and {image(l,ans) for l in source}==set(target),'literal projective map')
    return ans

def matrix_for(p,pts):
    frame=[pts.index(v) for v in [(1,0,0),(0,1,0),(0,0,1),(1,1,1)]]
    cols=[pts[p[i]] for i in frame[:3]]
    for b,c in itertools.product(range(1,4),repeat=2):
        scales=[1,b,c];a=tuple(tuple(fm(cols[j][i],scales[j]) for j in range(3)) for i in range(3))
        if determinant(a) and mat_image(pts[frame[3]],a)==pts[p[frame[3]]]:
            if all(mat_image(v,a)==pts[p[i]] for i,v in enumerate(pts)):return a
    raise ValueError('retained generator is not projectively linear in literal coordinates')

def load_input(path):
    text=Path(path).read_text();chunk=text.split('CONSTRUCTION_INPUT ',1)[1].split('PASS_CONSTRUCTION_INPUT',1)[0]
    gens,ls=ast.literal_eval(chunk.strip())
    gens=[tuple(x-1 for x in p) for p in gens];lines=sorted(mask(x-1 for x in l) for l in ls)
    need(all(sorted(p)==list(range(21)) for p in gens),'permutation input')
    return gens,lines

def prepare(input_path):
    gens,lines=load_input(input_path);pts,clines=coordinate_plane();j,_=plane_tables(lines)
    frame=next(q for q in itertools.combinations(range(21),4) if all(not any(set(t)<=set(bits(l)) for l in lines) for t in itertools.combinations(q,3)))
    cframe=[pts.index(v) for v in [(1,0,0),(0,1,0),(0,0,1),(1,1,1)]]
    labels=plane_map(clines,lines,dict(zip(cframe,frame)));inv={p:i for i,p in enumerate(labels)}
    matrices=[]
    for p in gens:
        q=tuple(inv[p[labels[i]]] for i in range(21));a=matrix_for(q,pts)
        need(determinant(a)==1,'special linear determinant');matrices.append(a)
        need({image(l,p) for l in lines}==set(lines),'retained generator preserves lines')
    group=closure(gens,21);need(len(group)==20160,'literal group order')
    hypers=[]
    for s in itertools.combinations(range(21),6):
        h=mask(s)
        if all((h&l).bit_count()<=2 for l in lines):hypers.append(h)
    remaining=set(hypers);orbits=[]
    while remaining:
        o=orbit(min(remaining),gens);need(set(o)<=remaining,'orbit partition');orbits.append(o);remaining-=set(o)
    need(len(hypers)==168 and list(map(len,orbits))==[56,56,56],'complete hyperoval orbit inventory')
    # Two explicit normalizing semilinear maps must induce all six ordered orbit choices.
    normalizers=[]
    for transform in [lambda v:(fm(2,v[0]),v[1],v[2]),lambda v:tuple(fm(x,x) for x in v)]:
        p=tuple(labels[pts.index(normalize(transform(pts[inv[i]])))] for i in range(21))
        need({image(l,p) for l in lines}==set(lines),'normalizer plane action')
        pinv=tuple(p.index(i) for i in range(21));gset=set(group)
        need(all(mul(mul(pinv,g),p) in gset for g in gens),'literal normalizing action')
        perm=tuple(next(k for k,o in enumerate(orbits) if image(x[0],p) in o) for x in orbits)
        normalizers.append({'points':p,'hyperoval_orbits':perm})
    choice_group=closure([tuple(x['hyperoval_orbits']) for x in normalizers],3)
    need(len(choice_group)==6,'all ordered distinct hyperoval choices')
    metadata={'field_polynomial':'x^2+x+1','coordinate_points':pts,'coordinate_to_retained':labels,'retained_generators':gens,'generator_matrices':matrices,'lines':lines,'hyperoval_orbits':orbits,'normalizers':normalizers,'group_order':len(group),'six_subsets':54264}
    return gens,group,metadata

class Geometry:
    def __init__(self,metadata,variant,choice=(0,1)):
        need(variant in ['5.1','5.2'],'variant')
        self.variant=variant
        need(len(choice)==2 and len(set(choice))==2 and set(choice)<={0,1,2},'hyperoval choice')
        self.objects=[metadata['lines'],[1<<i for i in range(21)],*[metadata['hyperoval_orbits'][i] for i in choice],[mask(s) for s in itertools.combinations(range(21),2)]]
        self.lookups=[{x:i for i,x in enumerate(o)} for o in self.objects]
        self.adj={}
        for i,j in itertools.combinations(range(5),2):
            rows=[]
            for a in self.objects[i]:
                rows.append(mask(b for b,c in enumerate(self.objects[j]) if self.incident(i,a,j,c)))
            self.adj[i,j]=rows
            self.adj[j,i]=[mask(a for a,row in enumerate(rows) if (row>>b)&1) for b in range(len(self.objects[j]))]

    def incident(self,i,a,j,b):
        intersection=(a&b).bit_count()
        if i==0:
            if j==3 and self.variant=='5.1':return intersection!=0
            return intersection==0
        if i==1:return intersection==1
        if (i,j)==(2,3):return intersection==3
        if j==4:return intersection==2
        raise ValueError('unlisted relation')

    def flags(self,types):
        types=tuple(types)
        def visit(prefix,allowed):
            if len(prefix)==len(types):yield tuple(prefix);return
            t=types[len(prefix)]
            for v in bits(allowed[0]):
                rest=[s&self.adj[t,u][v] for u,s in zip(types[len(prefix)+1:],allowed[1:])]
                if all(rest):yield from visit(prefix+[v],rest)
        yield from visit([],[(1<<len(self.objects[t]))-1 for t in types])

    def extensions(self,flag,t):
        allowed=(1<<len(self.objects[t]))-1
        for u,v in flag.items():allowed &= self.adj[u,t][v]
        return allowed

    def object_image(self,t,v,p):return self.lookups[t][image(self.objects[t][v],p)]

def connected(vertices,neighbors):
    vertices=set(vertices)
    if not vertices:return False
    seen={min(vertices)};todo=list(seen)
    for v in todo:
        for u in neighbors(v):
            if u not in seen:seen.add(u);todo.append(u)
    return seen==vertices

def primitive_action(perms):
    """All permutations of a transitive action: invariant pair-graph test."""
    n=len(perms[0]);need({p[0] for p in perms}==set(range(n)),'action transitivity')
    if n<2:return False
    remaining=set(range(1,n));stabilizer=[p for p in perms if p[0]==0]
    while remaining:
        b=min(remaining);orb={p[b] for p in stabilizer};remaining-=orb
        adj=[set() for _ in range(n)]
        for p in perms:a,c=p[0],p[b];adj[a].add(c);adj[c].add(a)
        if not connected(range(n),lambda x:adj[x]):return False
    return True

TABLE1={'012':{'3':5,'4':5},'013':{'2':3,'4':3},'014':{'2':2,'3':2},'023':{'1':3,'4':3},'024':{'1':2,'3':2},'034':{'1':2,'2':2},'123':{'0':3,'4':2},'124':{'0':6,'3':4},'134':{'0':6,'2':4},'234':{'0':3,'1':2}}

def certify(geometry,group,types=(0,1,2,3,4),source_label=None):
    types=tuple(types);position={t:i for i,t in enumerate(types)}
    chambers=list(geometry.flags(types));need(chambers,'nonempty chambers');base=dict(zip(types,chambers[0]))
    images=[tuple(geometry.object_image(t,base[t],p) for t in types) for p in group]
    need(set(images)==set(chambers),'complete chamber orbit')
    if len(types)==5:need(len(set(images))==len(group),'kernel-free regular chamber action')
    flag_rows=[];residue_rows=[];table={}
    for k in range(len(types)+1):
        for ts in itertools.combinations(types,k):
            fs=list(geometry.flags(ts));projections={tuple(c[position[t]] for t in ts) for c in chambers}
            need(set(fs)==projections,'partial flag not in a chamber')
            # Complete chamber orbit and literal projection equality imply transitivity on every flag type.
            flag={t:base[t] for t in ts};remaining=[t for t in types if t not in ts]
            stab=[p for p,c in zip(group,images) if all(c[position[t]]==base[t] for t in ts)]
            need(len(fs)*len(stab)==len(group),'flag orbit stabilizer')
            allowed={t:list(bits(geometry.extensions(flag,t))) for t in remaining}
            flag_rows.append({'types':ts,'count':len(fs),'stabilizer_order':len(stab),'extensions':{str(t):len(v) for t,v in allowed.items()}})
            if k==len(types)-2:table[''.join(map(str,ts))]={str(t):len(v) for t,v in allowed.items()}
            if k==len(types)-1:need(all(len(v)>=2 for v in allowed.values()),'firmness')
            if not remaining:continue
            vertices=[(t,v) for t,vs in allowed.items() for v in vs]
            if len(remaining)>=2:
                need(connected(vertices,lambda tv:((u,w) for u,vs in allowed.items() if u!=tv[0] for w in vs if (geometry.adj[tv[0],u][tv[1]]>>w)&1)),'residue connectivity')
            primitive=[];two=[]
            for t,vs in allowed.items():
                pos={v:i for i,v in enumerate(vs)}
                ps=[tuple(pos[geometry.object_image(t,v,p)] for v in vs) for p in stab]
                need(all(sorted(p)==list(range(len(vs))) for p in ps),'residue action')
                primitive.append(primitive_action(ps))
                two.append(len(vs)>1 and {p[1] for p in ps if p[0]==0}==set(range(1,len(vs))))
            need(any(primitive),'RWPRI residue')
            ip=None
            if len(remaining)==2:
                i,j=remaining;left,right=allowed[i],allowed[j]
                complete=all((geometry.adj[i,j][x]&mask(right))==mask(right) for x in left)
                ip=complete or all((geometry.adj[i,j][x]&geometry.adj[i,j][y]&mask(right)).bit_count()<=1 for x,y in itertools.combinations(left,2))
                need(ip,'rank-two IP2')
            residue_rows.append({'fixed_types':ts,'remaining_types':remaining,'type_sizes':[len(allowed[t]) for t in remaining],'stabilizer_order':len(stab),'primitive_actions':primitive,'two_transitive_actions':two,'IP2_if_rank_two':ip})
    if len(types)==5:
        need(len(chambers)==20160,'source chamber count')
        if geometry.variant=='5.1':need(table==TABLE1,'source Table 1')
    return {'model':geometry.variant,'source_label':source_label or geometry.variant,'retained_types':[t+1 for t in types],'chambers':len(chambers),'base_chamber':base,'base_objects':[geometry.objects[t][base[t]] for t in types],'flag_rows':flag_rows,'residue_rows':residue_rows,'rank_two_extension_table':table,'scope':'literal construction/truncation, not classification'}

def check_isomorphism(source,target,point_map):
    maps=[]
    for t in range(5):
        m=tuple(target.lookups[t][image(v,point_map)] for v in source.objects[t])
        need(sorted(m)==list(range(len(target.objects[t]))),'object map bijection');maps.append(m)
    count=0
    for i,j in itertools.combinations(range(5),2):
        for a,row in enumerate(source.adj[i,j]):
            need(image(row,maps[j])==target.adj[i,j][maps[i][a]],'literal all-incidence isomorphism');count+=len(target.objects[j])
    return {'object_maps':maps,'pair_tests':count}

def all_choice_maps(metadata,gens):
    rows=[]
    for variant in ['5.1','5.2']:
        cache={choice:Geometry(metadata,variant,choice) for choice in itertools.permutations(range(3),2)}
        for choice,source in cache.items():
            for i,n in enumerate(metadata['normalizers']):
                target_choice=tuple(n['hyperoval_orbits'][j] for j in choice)
                checked=check_isomorphism(source,cache[target_choice],n['points'])
                rows.append({'variant':variant,'source_choice':choice,'target_choice':target_choice,'normalizer':i,**checked})
        for p in gens:check_isomorphism(cache[(0,1)],cache[(0,1)],p)
    return rows

TRUNCATIONS=[('5.1','4.1',(1,2,3,4)),('5.2','4.1',(1,2,3,4)),
             ('5.1','4.10',(0,2,3,4)),('5.1','3.1',(1,2,4)),
             ('5.2','3.1',(1,2,4)),('5.1','3.6',(2,3,4)),
             ('5.1','2.2',(2,4)),('5.2','2.2',(2,4))]
SOURCE_PROFILES={'4.1':{'types':[21,56,56,210],'panels':[1,3,3,1],'borel':3},
                 '4.10':{'types':[21,56,56,210],'panels':[2,1,1,2],'borel':2},
                 '3.1':{'types':[21,56,210],'panels':[1,3,4],'borel':12},
                 '3.6':{'types':[56,56,210],'panels':[3,3,2],'borel':6},
                 '2.2':{'types':[56,210],'panels':[3,14],'borel':24}}

def truncations(metadata,group):
    rows=[]
    for variant,label,types in TRUNCATIONS:
        geom=Geometry(metadata,variant);r=certify(geom,group,types,label)
        full=list(geom.flags(range(5)));truncated=set(geom.flags(types))
        need({tuple(c[t] for t in types) for c in full}==truncated,'literal truncation chamber surjection')
        panels=[]
        for t in types:
            fixed=tuple(u for u in types if u!=t)
            panels.append(next(x for x in r['flag_rows'] if tuple(x['types'])==fixed)['extensions'][str(t)]-1)
        profile={'types':[len(geom.objects[t]) for t in types],'panels':panels,'borel':r['flag_rows'][-1]['stabilizer_order']}
        need(profile==SOURCE_PROFILES[label],'source truncation numeric profile')
        r['source_profile']=profile;r['identity_object_maps']={str(t+1):list(range(len(geom.objects[t]))) for t in types}
        r['literal_truncation_chamber_surjection']=True;rows.append(r)
    return rows

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    need(not args.out.exists(),'output exists');args.out.mkdir(parents=True)
    gens,group,metadata=prepare(args.input)
    (args.out/'model.json').write_text(json.dumps(metadata,indent=2)+'\n')
    reports=[]
    for variant in ['5.1','5.2']:
        print('MODEL',variant,flush=True);reports.append(certify(Geometry(metadata,variant),group))
        (args.out/('model_'+variant+'.json')).write_text(json.dumps(reports[-1],indent=2)+'\n')
    choices=all_choice_maps(metadata,gens);(args.out/'choice_maps.json').write_text(json.dumps(choices,indent=2)+'\n')
    tr=truncations(metadata,group);(args.out/'truncations.json').write_text(json.dumps(tr,indent=2)+'\n')
    report={'status':'PASS_LITERAL_L100_TWO_CONSTRUCTIONS_AND_TRUNCATIONS','source_whole_credit':0,'classification_claim':False,'models':reports,'truncation_checks':len(tr),'choice_isomorphisms':len(choices),'input_sha256':hashlib.sha256(args.input.read_bytes()).hexdigest()}
    (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],flush=True)
if __name__=='__main__':main()
