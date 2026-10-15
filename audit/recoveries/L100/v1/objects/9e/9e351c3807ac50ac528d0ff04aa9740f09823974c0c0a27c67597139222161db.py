"""Literal six choices for source Geometry4.11, with explicit dual orbit choice."""
import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,importlib.util,itertools,json,time
from pathlib import Path
P=Path(__file__).resolve().parent;G=P.parent
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
o=load('oval_objects',P/'objects_v2.py');j=load('oval_joins',G/'doubling_component_v1/literal_joins_v3.py');c=load('oval_coordinates',G/'constructions_component_v1/constructions.py')
need=o.need;read=o.read
def polarity(meta):
    points=meta['coordinate_points'];labels=meta['coordinate_to_retained'];result={}
    for i,a in enumerate(points):result[1<<labels[i]]=o.mask(labels[k]for k,v in enumerate(points)if c.fs(c.fm(x,y)for x,y in zip(a,v))==0)
    need(set(result.values())==set(meta['lines']),'actual coordinate point-line polarity')
    need(all(bool(p&result[q])==bool(q&result[p])for p in result for q in result),'literal incidence reversing polarity')
    return result
def domains(meta,baers,records):
    pol=polarity(meta);inverse={v:k for k,v in pol.items()};classof={b:i for i,orb in enumerate(baers)for b in orb}
    dualclasses=[]
    for orb in baers:
        dualsets={sum(inverse[l]for l in meta['lines']if (l&b).bit_count()==3)for b in orb}
        cs={classof[b]for b in dualsets};need(len(cs)==1 and dualsets==set(baers[next(iter(cs))]),'exact Baer class under coordinate duality');dualclasses.append(next(iter(cs)))
    mates=[]
    for i in range(3):
        hs={r['hyperoval_class']for r in records if r['baer_class']==i};need(len(hs)==1,'unique actual even hyperoval class');mates.append(next(iter(hs)))
    ovs=[];dvs=[]
    for hyp in meta['hyperoval_orbits']:
        oval=sorted((h^(1<<p),1<<p)for h in hyp for p in o.bits(h));need(len(oval)==len(set(x for x,n in oval))==336,'distinct ovals and unique supplied nuclei')
        for x,n in oval:
            need(x.bit_count()==5 and not x&n,'five oval points and external nucleus')
            need(all((l&x).bit_count()<=2 for l in meta['lines']),'no three oval points collinear')
            tangents=[l for l in meta['lines']if (l&x).bit_count()==1]
            need(len(tangents)==5 and all(l&n for l in tangents),'five concurrent tangents at actual nucleus')
        dual=sorted((tuple(sorted(pol[1<<p]for p in o.bits(x))),pol[n])for x,n in oval)
        ovs.append(oval);dvs.append(dual)
    return ovs,dvs,dict(point_line_polarity=[[p,l]for p,l in sorted(pol.items())],dual_baer_classes=dualclasses,even_hyperoval_mates=mates,oval_class_sizes=list(map(len,ovs)))
class Geometry:
    def __init__(self,baers,ovs,dvs,metadata,choice):
        self.types=list(range(4));self.choice=choice;self.oval_class=metadata['even_hyperoval_mates'][choice[0]];self.dual_class=metadata['even_hyperoval_mates'][metadata['dual_baer_classes'][choice[1]]]
        self.objects=[baers[choice[0]],baers[choice[1]],ovs[self.oval_class],dvs[self.dual_class]];self.lookups=[{x:i for i,x in enumerate(xs)}for xs in self.objects];self.adj={};self.pair_checks=0
        for t,u in itertools.combinations(range(4),2):
            rows=[0]*len(self.objects[t]);cols=[0]*len(self.objects[u])
            for a,x in enumerate(self.objects[t]):
                for b,y in enumerate(self.objects[u]):
                    self.pair_checks+=1
                    if self.incident(t,x,u,y):rows[a]|=1<<b;cols[b]|=1<<a
            self.adj[t,u]=rows;self.adj[u,t]=cols
    def act(self,t,x,g):
        if t<2:return o.image(x,g)
        if t==2:return(o.image(x[0],g),o.image(x[1],g))
        return(tuple(sorted(o.image(l,g)for l in x[0])),o.image(x[1],g))
    def incident(self,t,x,u,y):
        if t>u:return self.incident(u,y,t,x)
        if (t,u)==(0,1):return x&y==0
        if (t,u)==(0,2):return(x&y[0]).bit_count()==4
        if (t,u)==(0,3):return(x&y[1]).bit_count()==3 and all((x&l).bit_count()==1 for l in y[0])
        if (t,u)==(1,2):return bool(x&y[1])and x&y[0]==0
        if (t,u)==(1,3):return sum((x&l).bit_count()==3 for l in y[0])==4
        if (t,u)==(2,3):return(x[0]&y[1]).bit_count()==2 and all((x[0]&~y[1])&l==0 for l in y[0])
        raise ValueError('different actual types')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir();start=time.monotonic()
    meta=read(G/'constructions_component_v1/expected/model.json');baers=read(G/'baer_component_v1/inputs/baer_orbits.json')['orbits'];records=read(P/'objects02/result/objects.json')['records'];ovs,dvs,metadata=domains(meta,baers,records)
    A=j.Ambient(read(G/'palette_serialization_v1/derived/group_elements.json'));projection=read(G/'palette_serialization_frozen01/fresh/source_projection.json')['representatives'][24];target=read(G/'palette_serialization_v1/derived/model25.json');auts=[];auto=j.automorphisms(A,meta);maps=[]
    for choice in itertools.permutations(range(3),2):
        geo=Geometry(baers,ovs,dvs,metadata,choice);found=None
        for ai in range(12):
            if ai==len(auts):auts.append(next(auto))
            name,aut=auts[ai];q=j.attempt(target,projection,geo,A,aut)
            if q:found=q|dict(automorphism=name,automorphism_generator_images=[list(aut[g])for g in A.generators]);break
        need(found is not None,'complete positive oval map '+str(choice))
        found.update(source_label='4.11',catalogue_index=25,baer_classes=list(choice),oval_hyperoval_class=geo.oval_class,dual_oval_hyperoval_class=geo.dual_class,source_pair_checks=geo.pair_checks,source_type_sizes=list(map(len,geo.objects)))
        maps.append(found);print(choice,name,found['checks'],flush=True);(a.out/'partial.json').write_text(json.dumps(dict(complete_maps=maps),indent=2)+'\n')
    result=dict(status='PASS_LITERAL_OVAL_DUAL_OVAL_CONSTRUCTIONS',metadata=metadata,maps=maps,seconds=time.monotonic()-start,scope='Explicit oval and dual-oval class choices for each ordered pair of distinct Baer classes; no arbitrary-orbit-choice assertion.',new_ambient_censuses=0,graph_isomorphism_runs=0,source_credit=0)
    (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],flush=True)
if __name__=='__main__':main()
