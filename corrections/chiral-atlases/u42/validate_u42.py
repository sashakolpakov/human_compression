"""Literal rank-three positives and automorphism orbits, independent of GAP.

Uses only permutation products, finite closure, and propagation along the
two-generator Cayley graph. Failed transports retain explicit relation words.
"""
import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,json,time
P=Path(__file__).resolve().parent
def need(x,s):
    if not x:raise ValueError(s)
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def mul(a,b):return tuple(b[x]for x in a)
def inv(a):
    b=[0]*len(a)
    for i,x in enumerate(a):b[x]=i
    return tuple(b)
def word_value(gens,w,e):
    z=e
    for x in w:z=mul(z,gens[x-1]if x>0 else inv(gens[-x-1]))
    return z
def cyclic(g,e):
    out={e};x=g
    while x!=e:out.add(x);x=mul(x,g)
    return out
def closure(gens,e):
    elements=[e];seen={e}
    for x in elements:
        for g in gens:
            y=mul(x,g)
            if y not in seen:seen.add(y);elements.append(y)
    return seen
def transport(gens,images,e,group_order):
    """A proposed map must respect every directed generator edge."""
    elements=[e];mapped=[e];parents=[(-1,0)];seen={e:0}
    def spelling(k):
        w=[]
        while k:w.append(parents[k][1]);k=parents[k][0]
        return list(reversed(w))
    for i,x in enumerate(elements):
        for j,(g,h)in enumerate(zip(gens,images),1):
            y=mul(x,g);v=mul(mapped[i],h)
            if y not in seen:
                seen[y]=len(elements);elements.append(y);mapped.append(v);parents.append((i,j))
            elif mapped[seen[y]]!=v:
                w=spelling(i)+[j]+[-s for s in reversed(spelling(seen[y]))]
                need(word_value(gens,w,e)==e and word_value(images,w,e)!=e,'literal relation contradiction')
                return dict(isomorphism=False,witness=w,visited=len(elements))
    need(len(elements)==group_order,'source tuple generates acquired group')
    need(len(set(mapped))==group_order,'proposed successful map is bijective')
    return dict(isomorphism=True,vertices=len(elements),edges=len(elements)*len(gens))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(a.out.is_absolute()and not a.out.exists(),'fresh independent validation');a.out.mkdir();start=time.monotonic()
    model=P/'inputs/group.json';census=P/'inputs/markings.json';d=json.loads(census.read_text());m=json.loads(model.read_text())
    before=[pin(model),pin(census),pin(Path(__file__).resolve())]
    gens=[tuple(x-1 for x in g)for g in m['generators']];e=tuple(range(len(gens[0])));ambient=closure(gens,e)
    need(len(ambient)==25920==m['order']==d['order'],'literal ambient order')
    marks=[(i,r)for i,r in enumerate(d['results'])if not r['regular']]
    need(len(marks)==92,'exact unaltered proposed positive list')
    validated=[];classes=[];comparisons=[]
    for i,r in marks:
        need(r['rank']==3 and len(r['alpha'])==3,'rank-three input')
        alpha=[tuple(x-1 for x in g)for g in r['alpha']]
        need(all(sorted(x)==list(e)for x in alpha)and alpha[0]==e and all(x in ambient for x in alpha),'literal ambient permutations')
        s,t=alpha[1:];u=mul(inv(s),t);ps,pt,pu=cyclic(s,e),cyclic(t,e),cyclic(u,e)
        need(len(pt)==2 and len(ps)>2 and len(pu)>2 and [len(ps),len(pu)]==r['type'],'rotation relations and type')
        need(ps&pt==ps&pu==pt&pu=={e},'all nontrivial proper parabolic intersections')
        need(closure([s,t],e)==ambient,'literal full generation')
        reflection=transport([s,t],[inv(s),inv(t)],e,len(ambient))
        need(not reflection['isomorphism'],'literal obstruction to reflection')
        found=None
        for k,cl in enumerate(classes):
            if cl['type']!=r['type']:continue
            q=transport([s,t],cl['generators'],e,len(ambient));comparisons.append(dict(source=i,target=cl['representative'],**q))
            if q['isomorphism']:found=k;cl['members'].append(i);break
        if found is None:
            found=len(classes);classes.append(dict(representative=i,type=r['type'],generators=[s,t],members=[i]))
        validated.append(dict(census_index=i,rank=3,type=r['type'],class_index=found,reflection_obstruction=reflection['witness']))
        print(json.dumps(dict(validated=len(validated),classes=len(classes),seconds=time.monotonic()-start)),flush=True)
    need(len(classes)==46 and all(len(cl['members'])==2 for cl in classes),'observed complete partition of positive list')
    for cl in classes:cl.pop('generators')
    need(all(pin(Path(x['path']))==x for x in before),'unchanged inputs')
    result=dict(status='PASS_LITERAL_U42_POSITIVES_AND_AUTOMORPHISM_CLASSES',ambient_order=len(ambient),positive_markings=len(marks),automorphism_classes=len(classes),classes=classes,validated=validated,comparisons=comparisons,inputs=before,seconds=time.monotonic()-start,uses_GAP=False,scope='46 distinct positive chiral classes from the acquired geometric recognition theorem. Completeness of the original search is a separate premise; this proves a lower bound without it.',whole_original_credit=0)
    (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ['classes','validated','comparisons','inputs']}))
if __name__=='__main__':main()
