"""Native recipes 4.2--4.7 under an explicit complete butterfly convention."""
import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,importlib.util,itertools,json,time
from pathlib import Path
P=Path(__file__).resolve().parent;G=P.parent
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
o=load('literal_objects',P/'objects_v2.py');j=load('acquired_joins',G/'doubling_component_v1/literal_joins_v3.py')
need=o.need;read=o.read
ROUTES={'4.2':24,'4.3':19,'4.4':22,'4.5':23,'4.6':18,'4.7':17}

class Geometry:
    def __init__(self,meta,baers,records,label,orbit):
        self.label=label;self.types=list(range(4));self.records={tuple(r['subplanes']):r for r in records if r['baer_class']==orbit}
        hs={r['hyperoval_class']for r in self.records.values()};need(len(hs)==1,'exact associated hyperoval class');self.hyperoval_class=next(iter(hs));hyp=meta['hyperoval_orbits'][self.hyperoval_class]
        self.kinds={'4.2':['l','p','h','b'],'4.3':['h','h','B','b'],'4.4':['h','h','p','b'],'4.5':['l','p','h','b'],'4.6':['p','h','B','b'],'4.7':['l','p','B','b']}[label]
        domain={'l':sorted(meta['lines']),'p':[1<<p for p in range(21)],'h':sorted(hyp),'B':baers[orbit],'b':sorted(self.records)}
        self.objects=[domain[k]for k in self.kinds];self.lookups=[{x:i for i,x in enumerate(xs)}for xs in self.objects];self.adj={};self.pair_checks=0
        for t,u in itertools.combinations(range(4),2):
            rows=[0]*len(self.objects[t]);cols=[0]*len(self.objects[u])
            for a,x in enumerate(self.objects[t]):
                for b,y in enumerate(self.objects[u]):
                    self.pair_checks+=1
                    if self.incident(t,x,u,y):rows[a]|=1<<b;cols[b]|=1<<a
            self.adj[t,u]=rows;self.adj[u,t]=cols
    def act(self,t,x,g):return o.butterfly_image(x,g)if self.kinds[t]=='b'else o.image(x,g)
    def incident(self,t,x,u,y):
        if t>u:return self.incident(u,y,t,x)
        L=self.label
        if u==3:
            r=self.records[y];kind=self.kinds[t]
            if kind=='l':
                pole=y[2:]if L=='4.5'else y[:2]
                return bool(x&r['point']) and x&(pole[0]|pole[1])==x
            if kind=='p':return bool(x&(r['plus_triple']^r['point']))
            if kind=='h':return x in r['plus_hyperovals']if L in ['4.3','4.4']and t==1 else x in r['minus_hyperovals']
            if kind=='B':return x in y[:2]if L=='4.7'else x&r['plus_triple']==r['plus_triple']and x not in y[:2]
        if L in ['4.2','4.5']:
            if (t,u)==(0,1):return not bool(x&y)
            if (t,u)==(0,2):return not bool(x&y)if L=='4.2'else bool(x&y)
            if (t,u)==(1,2):return bool(x&y)
        if L in ['4.3','4.4']:
            if (t,u)==(0,1):return x&y==0
            if L=='4.3':return (x&y).bit_count()==4 if t==0 else x&y==0
            return bool(x&y)if t==0 else not bool(x&y)
        if L=='4.6':return bool(x&y)if t==0 else (x&y).bit_count()==4
        if L=='4.7':
            if (t,u)==(0,1):return not bool(x&y)
            if (t,u)==(0,2):return (x&y).bit_count()==3
            return bool(x&y)
        raise ValueError('actual distinct recipe types')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir();start=time.monotonic()
    meta=read(G/'constructions_component_v1/expected/model.json');baers=read(G/'baer_component_v1/inputs/baer_orbits.json')['orbits'];records=read(P/'objects02/result/objects.json')['records']
    A=j.Ambient(read(G/'palette_serialization_v1/derived/group_elements.json'));projection=read(G/'palette_serialization_frozen01/fresh/source_projection.json')['representatives'];auts=[];auto=j.automorphisms(A,meta);out=[]
    for label,index in ROUTES.items():
        target=read(G/f'palette_serialization_v1/derived/model{index}.json')
        for orbit in range(3):
            geo=Geometry(meta,baers,records,label,orbit);found=None
            for ai in range(12):
                if ai==len(auts):auts.append(next(auto))
                name,aut=auts[ai];q=j.attempt(target,projection[index-1],geo,A,aut)
                if q:found=q|dict(automorphism=name,automorphism_generator_images=[list(aut[g])for g in A.generators]);break
            need(found is not None,f'literal map {label}/Baer class {orbit}')
            found.update(source_label=label,catalogue_index=index,baer_class=orbit,hyperoval_class=geo.hyperoval_class,source_pair_checks=geo.pair_checks,source_type_sizes=list(map(len,geo.objects)))
            out.append(found);print(label,orbit,name,found['checks'],flush=True)
            (a.out/'partial.json').write_text(json.dumps(dict(complete_maps=out),indent=2)+'\n')
    result=dict(status='PASS_LITERAL_ORDERED_BUTTERFLY_RECIPES',maps=out,scope='Explicit all-cross singleton butterfly convention; no acceptance of the broader printed two-cross definition.',seconds=time.monotonic()-start,new_ambient_censuses=0,graph_isomorphism_runs=0,source_credit=0)
    (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],flush=True)
if __name__=='__main__':main()
