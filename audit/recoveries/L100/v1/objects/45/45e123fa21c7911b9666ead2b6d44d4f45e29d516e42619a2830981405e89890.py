"""Literal finite projective objects from acquired point and subplane data."""
import sys
if not __debug__: raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,itertools,json,time
from pathlib import Path
P=Path(__file__).resolve().parent;G=P.parent
def need(v,s):
    if not v:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def bits(x):
    while x:
        y=x&-x;yield y.bit_length()-1;x-=y
def mask(xs):return sum(1<<x for x in xs)
def image(x,g):return mask(g[p]for p in bits(x))
def mul(p,q):return tuple(q[x]for x in p)
def inv(p):
    r=[0]*len(p)
    for i,j in enumerate(p):r[j]=i
    return tuple(r)
def butterfly_image(b,g):return tuple(sorted(image(x,g)for x in b[:2]))+tuple(sorted(image(x,g)for x in b[2:]))
def closure(gens):
    e=tuple(range(len(gens[0])));found={e};todo=[e]
    for p in todo:
        for q in gens:
            r=mul(p,q)
            if r not in found:found.add(r);todo.append(r)
    return found
def structural_stabilizer(stab):
    domain=set(stab);e=tuple(range(21))
    need(len(domain)==16 and all(mul(p,q)in domain for p in stab for q in stab),'literal stabilizer group of order16')
    for a in stab:
        a2=mul(a,a)
        if a2==e or mul(a2,a2)!=e:continue
        for b in stab:
            if b==e or mul(b,b)!=e or mul(mul(b,a),b)!=inv(a):continue
            d=closure([a,b])
            if len(d)!=8:continue
            for z in stab:
                if z in d or mul(z,z)!=e or any(mul(z,x)!=mul(x,z)for x in [a,b]):continue
                words=[];ak=e
                for i in range(4):
                    for j in range(2):
                        for k in range(2):words.append(mul(mul(ak,b if j else e),z if k else e))
                    ak=mul(ak,a)
                need(set(words)==domain and len(set(words))==16,'complete D8 times C2 normal forms')
                return dict(a=list(a),b=list(b),z=list(z),normal_forms=[list(x)for x in words],presentation='a^4=b^2=z^2=1, bab=a^-1, [a,z]=[b,z]=1; 16 distinct normal forms')
    raise ValueError('explicit D8 times C2 structure')

def construct(meta,baer_orbits):
    lines=meta['lines'];hyp=meta['hyperoval_orbits'];allh={h:i for i,orb in enumerate(hyp)for h in orb}
    bs=sorted(b for orb in baer_orbits for b in orb);classof={b:i for i,orb in enumerate(baer_orbits)for b in orb}
    need(len(bs)==len(set(bs))==360,'acquired complete Baer inventory')
    pairs={};tested=0
    for b,c in itertools.combinations(bs,2):
        tested+=1;t=b&c
        if t.bit_count()==3 and any(t&l==t for l in lines):pairs.setdefault(t,[]).append((b,c))
    records=[];ambiguities=[]
    for t,pluspairs in sorted(pairs.items()):
        ls=[l for l in lines if l&t==t];need(len(ls)==1,'unique central line from three points');line=ls[0]
        for plus in pluspairs:
            candidates=set()
            for p in bits(t):
                point=1<<p;u=(line^t)|point
                for minus in pairs.get(u,[]):
                    if len(set(plus+minus))!=4:continue
                    if all(x&y==point for x in plus for y in minus):candidates.add(minus)
            need(len(candidates)==1,'unique completion under explicit all-cross singleton rule')
            minus=next(iter(candidates));b=plus+minus;u=minus[0]&minus[1];point=t&u
            need(point.bit_count()==1 and t|u==line,'exact central pair')
            need(len({classof[x]for x in b})==1,'four subplanes lie in one actual orbit')
            hp=tuple((x&~line)|(u^point)for x in plus);hm=tuple((x&~line)|(t^point)for x in minus)
            need(len(set(hp+hm))==4 and all(h in allh for h in hp+hm),'four actual hyperovals from quadrangles')
            need(len({allh[h]for h in hp+hm})==1,'one associated hyperoval class')
            associated=allh[hp[0]]
            need(all((x&h).bit_count()%2==0 for x in b for h in hyp[associated]),'even Baer-hyperoval association')
            pole_lines=[]
            for pole in [plus,minus]:
                a={l for l in lines if l&point and (l&pole[0]).bit_count()==3}
                c={l for l in lines if l&point and (l&pole[1]).bit_count()==3}
                need(a==c and len(a)==3 and line in a,'extended subplane lines in either member of a pole coincide at central point')
                pole_lines.append(sorted(a-{line}))
            records.append(dict(subplanes=list(b),baer_class=classof[b[0]],hyperoval_class=associated,point=point,line=line,plus_triple=t,minus_triple=u,plus_hyperovals=list(hp),minus_hyperovals=list(hm),plus_lines=pole_lines[0],minus_lines=pole_lines[1]))
    need(len(records)==3780,'complete pair-based ordered butterfly inventory')
    records.sort(key=lambda x:x['subplanes']);lookup={tuple(r['subplanes']):r for r in records}
    for r in records:
        b=tuple(r['subplanes']);need(b[2:]+b[:2]in lookup,'opposite ordering retained')
    return records,dict(all_Baer_pairs=tested,collinear_three_pairs=sum(map(len,pairs.values())),ordered_butterflies=len(records),unordered_butterflies=len(records)//2,orbit_sizes=[sum(r['baer_class']==i for r in records)for i in range(3)])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir();start=time.monotonic()
    meta=read(G/'constructions_component_v1/expected/model.json');orbits=read(G/'baer_component_v1/inputs/baer_orbits.json')['orbits'];records,inventory=construct(meta,orbits)
    raw=read(G/'palette_serialization_v1/derived/group_elements.json');elements=[tuple(x-1 for x in p)for p in raw['elements']];gens=[tuple(g)for g in meta['retained_generators']]
    checks=[]
    for i in range(3):
        orb={tuple(r['subplanes'])for r in records if r['baer_class']==i};seed=min(orb);found={seed};todo=[seed]
        for x in todo:
            for g in gens:
                y=butterfly_image(x,g);need(y in orb,'actual generator closure')
                if y not in found:found.add(y);todo.append(y)
        need(found==orb,'actual transitive ordered butterfly action')
        stab=[g for g in elements if butterfly_image(seed,g)==seed]
        checks.append(dict(baer_class=i,seed=list(seed),orbit_size=len(orb),stabilizer_size=len(stab),structure=structural_stabilizer(stab)))
    out=dict(status='PASS_COMPLETE_LITERAL_BUTTERFLY_OBJECTS',inventory=inventory,records=records,stabilizers=checks,seconds=time.monotonic()-start,new_ambient_censuses=0)
    (a.out/'objects.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k not in ['records','stabilizers']}),flush=True)
if __name__=='__main__':main()
