import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,itertools,json
from pathlib import Path
import literal_joins_v3 as c
import fusion_join as f
P=Path(__file__).resolve().parent;G=P.parent;D=G/'palette_serialization_v1/derived'
def read(p):return json.loads(p.read_text())
def paths():
    if (P/'expected').is_dir():return P/'expected/doubling.json',P/'expected/truncation.json',P/'expected/fusion.json'
    return P/'doubling01/result/report.json',P/'truncation02/result/report.json',P/'fusion01/report.json'
class Context:
    def __init__(self):
        self.A=c.Ambient(read(D/'group_elements.json'));self.meta=read(G/'constructions_component_v1/expected/model.json')
        self.labels={r['label']:r['candidates'][0]['catalogue_index']for r in read(G/'source_join_component_v2/diagram_comparison01.json')['rows']}
        self.models={};self.auts={};self.iter=c.automorphisms(self.A,self.meta)
    def model(self,i):
        if i not in self.models:self.models[i]=c.Model(read(D/f'model{i}.json'),self.A)
        return self.models[i]
    def aut(self,name):
        while name not in self.auts:
            try:k,a=next(self.iter)
            except StopIteration:raise ValueError('unknown automorphism')
            self.auts[k]=a
        return self.auts[name]
    def map(self,r):
        c.need(r['source_index']==self.labels[r['source_label']] and r['target_index']==self.labels[r['target_label']],'exact source-to-catalogue index join')
        m=self.model(r['source_index']);target=self.model(r['target_index']).raw
        ts=[t-1 for t in r['source_types']];c.need(len(set(ts))==len(ts) and all(0<=t<m.raw['rank']for t in ts),'literal retained types')
        point=None if r['point_type']is None else r['point_type']-1;pair=None if r['pair_type']is None else r['pair_type']-1
        c.need((point is None)==(pair is None),'matched doubling descriptor')
        geom=c.Geometry(m,types=ts,point=point,pair=pair);aut=self.aut(r['automorphism'])
        c.need(r['automorphism_generator_images']==[list(aut[g])for g in self.A.generators],'exact automorphism images')
        c.need(len(geom.shadows)==r['two_point_shadows'] and geom.sufficient_checks==r['sufficient_relation_checks'],'exact shadow/condition checks')
        types=[t-1 for t in r['target_to_derived_types']];base=r['base_indices']
        c.need(len(base)==target['rank'] and all(type(i)==int and 0<=i<len(geom.objects[t])for i,t in zip(base,types)),'valid literal base')
        checks=c.verify_map(target,geom,self.A,aut,types,base,r['object_images']);c.need(checks==r['checks'],'all recorded map checks');return checks
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();c.need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
    dp,tp,fp=paths();double,trunc,fusion=map(read,[dp,tp,fp]);C=Context();checks=[]
    c.need([(r['source_label'],r['target_label'])for r in double['routes']]==[('2.7','2.6'),('4.1','4.8'),('5.2','5.3'),('5.1','5.4')],'all four exact doubling routes')
    prior=read(G/'source_join_component_v2/construction_join03/joins.json')['routes'];prior=[r for r in prior if len(r['retained_types'])<5]
    c.need(trunc['acquired_prior_routes']==prior and len(prior)==8,'eight prior joins acquired unchanged')
    new=trunc['acquired_prefix_maps']+trunc['routes'];c.need(len(new)==16,'sixteen new positive truncation maps')
    inventory=read(G/'source_join_component_v2/diagram_inventory02.json')['rows'];printed=[]
    for r in inventory:
        if 'truncation' in r['construction_route']:printed.extend((x,r['label'])for x in r['construction_route'].split('truncation',1)[1].split(';',1)[0].split('/'))
    expected=set(printed)-{('5.3','3.6')}|{('5.2','3.6')}
    actual=[(r['model'],r['source_label'])for r in prior]+[(r['source_label'],r['target_label'])for r in new]
    c.need(len(printed)==len(actual)==len(expected)==24 and set(actual)==expected,'complete printed-route disposition and explicit one-link repair')
    for r in double['routes']+new:checks.append(C.map(r))
    correction=trunc['source_corrections'];c.need(len(correction)==1,'one source-link correction')
    e=correction[0];c.need((e['physical_page'],e['printed_parent'],e['target'],e['proposed_parent'])==(9,'5.3','3.6','5.2'),'exact native source scope')
    c.need(C.model(C.labels['5.3']).raw['type_sizes']==e['printed_parent_sizes'] and C.model(C.labels['3.6']).raw['type_sizes']==e['target_sizes'],'actual literal cardinalities')
    c.need(210 in e['target_sizes'] and 210 not in e['printed_parent_sizes'],'symbolic truncation impossibility')
    models={i:read(D/f'model{i}.json')for i in range(1,30)}
    rows=f.extract((G/'incremental_target02/result.g').read_text());fresh=f.join(rows,inventory,read(G/'source_join_component_v2/diagram_comparison01.json')['rows'],models)
    c.need(fresh==fusion['rows'],'all29 exact fusion joins')
    result=dict(status='PASS_L100_DOUBLING_TRUNCATION_FUSION_REPLAY',fresh_doubling_maps=4,fresh_truncation_maps=16,acquired_truncation_maps=8,printed_valid_truncations=23,corrected_truncation_maps=1,source_fusion_rows=29,acquired_family_members=145,checks=checks,target_runs=0,map_search_runs=0,graph_or_group_censuses=0,principal_classification_refuted=False,whole_source_credit=0)
    (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
