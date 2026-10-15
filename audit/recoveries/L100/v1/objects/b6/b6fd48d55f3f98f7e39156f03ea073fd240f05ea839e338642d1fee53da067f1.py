import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,itertools,json
from pathlib import Path
import objects_v2 as o
import recipes as b
import ovals as v
P=Path(__file__).resolve().parent;G=P.parent;j=b.j
def read(p):return json.loads(p.read_text())
def expected(name):
    if (P/'expected').is_dir():return read(P/'expected'/name)
    return read(P/{'objects.json':'objects02/result/objects.json','recipes.json':'recipes01/result/report.json','ovals.json':'ovals01/result/report.json','ambiguity.json':'ambiguity01.json'}[name])
class Context:
    def __init__(self):
        self.meta=read(G/'constructions_component_v1/expected/model.json');self.baers=read(G/'baer_component_v1/inputs/baer_orbits.json')['orbits'];self.A=j.Ambient(read(G/'palette_serialization_v1/derived/group_elements.json'))
        self.objects=expected('objects.json');self.records=self.objects['records'];self.auts={};self.iter=j.automorphisms(self.A,self.meta);self.geometries={};self.models={}
        self.ovs,self.dvs,self.metadata=v.domains(self.meta,self.baers,self.records)
    def aut(self,name):
        while name not in self.auts:
            try:k,x=next(self.iter)
            except StopIteration:raise ValueError('unknown positive-map automorphism')
            self.auts[k]=x
        return self.auts[name]
    def geometry(self,r):
        key=(r['source_label'],tuple(r['baer_classes'])if r['source_label']=='4.11'else r['baer_class'])
        if key not in self.geometries:
            self.geometries[key]=v.Geometry(self.baers,self.ovs,self.dvs,self.metadata,key[1])if key[0]=='4.11'else b.Geometry(self.meta,self.baers,self.records,*key)
        return self.geometries[key]
    def validate(self,r):
        label=r['source_label'];index=25 if label=='4.11'else b.ROUTES[label];o.need(r['catalogue_index']==index,'exact source-catalogue join')
        if index not in self.models:self.models[index]=read(G/f'palette_serialization_v1/derived/model{index}.json')
        target=self.models[index];geo=self.geometry(r);aut=self.aut(r['automorphism'])
        o.need(r['source_type_sizes']==list(map(len,geo.objects))and r['source_pair_checks']==geo.pair_checks,'exact source domains and full predicate count')
        if label=='4.11':o.need((r['oval_hyperoval_class'],r['dual_oval_hyperoval_class'])==(geo.oval_class,geo.dual_class),'explicit compatible oval class choices')
        else:o.need(r['hyperoval_class']==geo.hyperoval_class,'actual butterfly hyperoval class')
        o.need(r['automorphism_generator_images']==[list(aut[g])for g in self.A.generators],'exact prescribed automorphism generator images')
        types=[t-1 for t in r['target_to_derived_types']];base=r['base_indices']
        o.need(sorted(types)==list(range(4))and len(base)==4 and all(type(x)==int and 0<=x<len(geo.objects[t])for x,t in zip(base,types)),'complete valid type/base data')
        checks=j.verify_map(target,geo,self.A,aut,types,base,r['object_images']);o.need(checks==r['checks'],'all literal map check totals');return checks
def object_checks(C):
    fresh,inventory=o.construct(C.meta,C.baers);o.need(fresh==C.records and inventory==C.objects['inventory'],'complete finite all-cross object inventory')
    quadrangles={};allh=[h for orb in C.meta['hyperoval_orbits']for h in orb]
    for h in allh:
        for q in itertools.combinations(o.bits(h),4):
            x=o.mask(q);o.need(x not in quadrangles,'one hyperoval through each quadrangle');quadrangles[x]=h
    o.need(len(quadrangles)==2520,'all acquired hyperoval quadrangles')
    opposite={};flags={};quadchecks=0
    for r in C.records:
        bs=tuple(r['subplanes']);under=frozenset(bs)
        for x in bs:
            key=(x,r['point'],r['line']);o.need(key not in flags or flags[key]==under,'uniqueness from subplane and central flag');flags[key]=under
        for x in bs[:2]:
            for y in bs[2:]:
                key=tuple(sorted([x,y]));o.need(key not in opposite or opposite[key]==under,'uniqueness from opposite subplanes');opposite[key]=under
        for planes,hyps in [(bs[:2],r['plus_hyperovals']),(bs[2:],r['minus_hyperovals'])]:
            for plane,h in zip(planes,hyps):o.need(quadrangles[plane&~r['line']]==h,'actual unique quadrangle hyperoval');quadchecks+=1
        for pole,ls in [(bs[:2],r['plus_lines']),(bs[2:],r['minus_lines'])]:
            actual=[l for l in C.meta['lines']if l&r['point']and l&(pole[0]|pole[1])==l]
            o.need(sorted(actual)==ls and len(ls)==2,'line in pole means actual line contained in union of two subplanes')
    stabilizers=[]
    for s in C.objects['stabilizers']:
        seed=tuple(s['seed']);orb={tuple(r['subplanes'])for r in C.records if r['baer_class']==s['baer_class']};found={seed};todo=[seed]
        for x in todo:
            for g in C.A.generators:
                y=o.butterfly_image(x,g);o.need(y in orb,'actual butterfly action closure')
                if y not in found:found.add(y);todo.append(y)
        o.need(found==orb and len(orb)==s['orbit_size']==1260,'actual transitivity, not assumed from count')
        stab=[g for g in C.A.elements if o.butterfly_image(seed,g)==seed];o.need(len(stab)==s['stabilizer_size']==16,'actual point-action stabilizer')
        o.need(o.structural_stabilizer(stab)==s['structure'],'explicit complete D8 times C2 normal-form certificate');stabilizers.append(len(stab))
        plane=seed[0];partners={x for x in C.baers[s['baer_class']]if x!=plane and (plane&x).bit_count()==3 and any((plane&x)&l==(plane&x)for l in C.meta['lines'])}
        fix=[g for g in C.A.elements if o.image(plane,g)==plane];q=min(partners);o.need(len(partners)==21 and {o.image(q,g)for g in fix}==partners,'actual subplane-stabilizer transitivity on 21 partners')
    return dict(ordered_objects=3780,stabilizer_orders=stabilizers,unique_quadrangles=2520,quadrangle_links=quadchecks,opposite_pair_keys=len(opposite),central_flag_keys=len(flags))
def ambiguity_checks(C,r):
    source=G.parents[1]/'corpus161_access_supplement_v4/primary/L100_Halle_1999_preprint.pdf'
    import hashlib
    o.need(hashlib.sha256(source.read_bytes()).hexdigest()=='13f207232f40ca0e00674b9e9de02a91e98226b325ddd428320c661e6131ff84','fixed source identity')
    need=o.need;out=[]
    for w in r['witnesses']:
        a,b,c,d=w['ordered_subplane_masks'];p=w['point_mask'];l=w['central_line_mask']
        need(a&c==b&d==p and p.bit_count()==1,'literal two displayed cross conditions')
        need((a&b).bit_count()==(c&d).bit_count()==3 and (a&b)|(c&d)==l and l in C.meta['lines'],'literal displayed collinear triples')
        need(len({a,b,c,d})==4 and all(x in C.baers[0]for x in [a,b,c,d]),'same actual orbit and distinct subplanes')
        need([[ (x&y).bit_count()for y in [c,d]]for x in [a,b]]==w['cross_intersection_sizes'],'all cross-intersection sizes')
        for x,g in zip([a,b,c,d],w['literal_group_maps_from_first']):
            g=tuple(t-1 for t in g);need(g in C.A.index and o.image(a,g)==x,'literal same-orbit witness')
        need([a,b]==r['positive_pole'],'same fixed positive pole');out.append(frozenset([a,b,c,d]))
    need(len(out)==2 and out[0]!=out[1],'distinct unordered completions')
    return dict(explicit_completions=2,qualification='The two displayed conditions alone are insufficient; external conventional meaning not adjudicated.')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();o.need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True);C=Context();objects=object_checks(C)
    R=expected('recipes.json');V=expected('ovals.json');o.need([(x['source_label'],x['baer_class'])for x in R['maps']]==[(l,i)for l in b.ROUTES for i in range(3)],'all eighteen butterfly recipe choices')
    o.need([x['baer_classes']for x in V['maps']]==[list(x)for x in itertools.permutations(range(3),2)],'all six ordered distinct Baer choices')
    o.need(V['metadata']==C.metadata,'exact literal polarity and oval class metadata')
    checks=[C.validate(r)for r in R['maps']+V['maps']];ambiguity=ambiguity_checks(C,expected('ambiguity.json'))
    data=read(G/'source_join_component_v2/literal_diagrams01/diagrams.json')['records'];routes=[]
    for label,index in list(b.ROUTES.items())+[('4.11',25)]:
        rec=next(x for x in data if x['index']==index);routes.append(dict(label=label,catalogue_index=index,acquired_panel_two_transitive=rec['panel_two_transitive']))
    report=dict(status='PASS_L100_BUTTERFLY_OVAL_CONSTRUCTION_REPLAY',objects=objects,butterfly_maps=18,oval_maps=6,map_checks=checks,ambiguity=ambiguity,local_action_routes=routes,new_ambient_censuses=0,map_search_runs=0,whole_source_credit=0)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
