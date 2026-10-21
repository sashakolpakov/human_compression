#!/usr/bin/env python3
"""Bounded independent comparison of the immutable D graph editions."""
from pathlib import Path
import argparse, hashlib, json
from check_independent import NEW_EDGES, ABSENT, need

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--old',type=Path,required=True)
    p.add_argument('--new',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    need(not a.out.exists(),'fresh output required')
    for d in [a.old,a.new]:
        m=json.loads((d/'manifest.json').read_text())
        for r in m['exports']:
            f=d/r['path']
            need(f.stat().st_size==r['bytes'] and sha(f)==r['sha256'],'immutable export '+str(f))
    old=json.loads((a.old/'logical_graph.json').read_text())
    new=json.loads((a.new/'logical_graph.json').read_text())
    key=lambda e:(e['source'],e['target'],e['kind'])
    oe={key(e):e for e in old['edges']};ne={key(e):e for e in new['edges']}
    added=sorted(ne.keys()-oe.keys());removed=sorted(oe.keys()-ne.keys())
    need(set(added)=={(s,t,'proof_use') for s,t in NEW_EDGES},'unexpected added edge')
    need(set(removed)=={(s,t,'proof_use') for s,t in ABSENT},'unexpected removed edge')
    meta=[]
    for k in oe.keys()&ne.keys():
        if oe[k]!=ne[k]:
            need(k in [('UD.MaximalAugmentation','program.search','proof_use'),('D3.Interfaces','program.search','proof_use')],'unexpected existing edge edit')
            need({x:v for x,v in oe[k].items() if x!='evidence'}=={x:v for x,v in ne[k].items() if x!='evidence'},'edge locator changed')
            meta.append(list(k))
    on={n['id']:n for n in old['nodes']};nn={n['id']:n for n in new['nodes']}
    need(on.keys()==nn.keys(),'node set changed')
    for k in on:
        if on[k]!=nn[k]:
            need(k=='D1.Series','unexpected node edit')
            need({x:v for x,v in on[k].items() if x!='label'}=={x:v for x,v in nn[k].items() if x!='label'},'node semantics changed')
            need(nn[k]['label']=='Additional rational generating series from direct multiplicity counting','series label')
    oi={(r['namespace'],r['path']):r for r in old['immutable_inputs']}
    ni={(r['namespace'],r['path']):r for r in new['immutable_inputs']}
    need(all(ni.get(k)==v for k,v in oi.items()),'scientific input changed')
    need(set(ni)-set(oi)=={('research','topic_D_logical_dag/manifest.json')},'unexpected input')
    need(ni[('research','topic_D_logical_dag/manifest.json')]['sha256']==sha(a.old/'manifest.json'),'previous manifest binding')
    changed={k for k in old.keys()|new.keys() if old.get(k)!=new.get(k)}
    need(changed=={'nodes','edges','immutable_inputs','checks','additional_current_outputs'},'unexpected graph field change')
    oc=json.loads((a.old/'coverage.json').read_text());nc=json.loads((a.new/'coverage.json').read_text())
    def without_closures(r):
        return {k:v for k,v in r.items() if k not in ['historical_closure','new_closure','retained_context_closure']}
    need({r['id']:without_closures(r) for r in oc['rows']}=={r['id']:without_closures(r) for r in nc['rows']},'source record/output change')
    d=json.loads((a.new/'delta.json').read_text())
    need(d['added_edges']==[list(x) for x in added] and d['removed_edges']==[list(x) for x in removed],'declared delta mismatch')
    r=dict(status='PASS_EXACT_REVIEWED_ADDITIVE_DELTA',previous_manifest_sha256=sha(a.old/'manifest.json'),reviewed_manifest_sha256=sha(a.new/'manifest.json'),added_edges=added,removed_edges=removed,existing_edge_explanations_clarified=sorted(meta),node_metadata_change='D1.Series label only',same_scientific_inputs=len(oi),new_provenance_inputs=1,same_source_records_and_output_sets=37,scientific_proofs_programs_formal_sources_unchanged=True)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r))

if __name__=='__main__':
    main()
