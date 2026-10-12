#!/usr/bin/env python3
"""Independent review integrity, scope and bounded mathematical replay."""
import argparse,copy,hashlib,json,re,subprocess,sys
from pathlib import Path
from independent_checks import graph_check,free_check,cross_ratio_check
ROOT=Path(__file__).resolve().parent
AUTHOR_SHA='04985353a54cf4f7050f143c518bdf5673dc43b422518dfb5825a520a36e9f65'
def need(ok,m):
    if not ok:raise ValueError('L126_REVIEW_REJECT '+m)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def file(p,b):need(p.is_file() and not p.is_symlink() and p.stat().st_size==b['bytes'] and sha(p)==b['sha256'],'exact file '+str(p))

def semantics(scope,contract,inventory,formal):
    need(scope['source_ids']==['F010','L126'],'two source IDs')
    need(scope['current_written_boundary']['applications']==['volume/finite-normal-pairs.tex','volume/representations-by-incidence.tex'],'both complete applications')
    need(len(contract['rows'])==31,'all31 source rows')
    rows={r['id']:r for r in contract['rows']}
    need(rows['L126.6.1']['status']=='literal_conclusion_refuted' and rows['L126.6.2']['status']=='literal_conclusion_refuted','literal projective correction')
    need(rows['L126.7.5.quotient']['status']=='corrected_to_S4','full type quotient correction')
    need(all(rows[k]['status']=='proved_weak_existence_with_different_compatible_inner_action' for k in ['L126.7.5.weak','L126.7.6.weak']),'weak action scope')
    need(rows['L126.8.thin']['status']=='literal_unqualified_claim_refuted_connected_replacement_proved','thin scope')
    need(inventory['required_computational_premises']==['certificate/check.py','certificate/graph.json'],'full required finite premise')
    need(len(inventory['files'])==10 and sum(r['role']=='required_finite_certificate' for r in inventory['files'])==1 and sum(r['role']=='optional_validation' for r in inventory['files'])==9,'program roles')
    need([r['path'] for r in inventory['mandatory_data']]==['certificate/graph.json'],'mandatory whole data')
    need(formal['reported_declarations']==22 and formal['new_formal_declarations']==0 and len(formal['modules'])==4,'partial inherited formal counts')
    need(formal['all_scopes_partial'] and not formal['source_principal_formalized'] and not formal['new_panel_permutations_formalized'],'formal limitations')

def controls(out,scope,contract,inv,formal,data):
    results=[]
    tests=[('omit source disposition','contract',lambda x:x['rows'].pop()),
           ('omit retained F010 application','scope',lambda x:x['current_written_boundary']['applications'].pop(0)),
           ('claim literal projective model valid','contract',lambda x:next(r for r in x['rows'] if r['id']=='L126.6.1').update(status='proved_literal')),
           ('restore false square quotient','contract',lambda x:next(r for r in x['rows'] if r['id']=='L126.7.5.quotient').update(status='proved_literal')),
           ('conflate natural and new weak action','contract',lambda x:next(r for r in x['rows'] if r['id']=='L126.7.5.weak').update(status='natural_action_proved')),
           ('drop required graph data','inv',lambda x:x['mandatory_data'].clear()),
           ('demote required certificate','inv',lambda x:next(r for r in x['files'] if r['path']=='certificate/check.py').update(role='optional_validation')),
           ('claim full Lean coverage','formal',lambda x:x.update(source_principal_formalized=True)),
           ('count inherited Lean as new','formal',lambda x:x.update(new_formal_declarations=22))]
    for name,key,change in tests:
        d=copy.deepcopy({'scope':scope,'contract':contract,'inv':inv,'formal':formal});change(d[key])
        try:semantics(d['scope'],d['contract'],d['inv'],d['formal'])
        except ValueError as e:results.append({'control':name,'rejected':str(e)})
        else:raise ValueError('control accepted '+name)
    for name,change in [('graph loop',lambda d:d['adjacency'][0].__setitem__(0,1)),('nonbijective generator',lambda d:d['generators'][0].__setitem__(0,d['generators'][0][1])),('incomplete star',lambda d:d.update(distinguished_star=[1])),('proper group substituted for full',lambda d:d.update(generators=[list(range(1,897))]))]:
        d=copy.deepcopy(data);change(d);p=out/(name.replace(' ','_')+'.json');p.write_text(json.dumps(d))
        try:graph_check(p)
        except ValueError as e:results.append({'control':name,'rejected':str(e)})
        else:raise ValueError('graph control accepted '+name)
    return results

def main():
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--study-root',type=Path);a=p.parse_args()
    need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
    if (ROOT/'manifest.json').exists():
        for b in read(ROOT/'manifest.json')['exports']:file(ROOT/b['path'],b)
    packet=a.packet.resolve();need(sha(packet/'manifest.json')==AUTHOR_SHA,'author manifest pin')
    m=read(packet/'manifest.json');need(len(m['exports'])==131,'131 author exports')
    for b in m['exports']:file(packet/b['path'],b)
    scope=read(packet/'scope.json');contract=read(packet/'source_contract.json');inv=read(packet/'program_inventory.json');formal=read(packet/'formal/scope.json');semantics(scope,contract,inv,formal)
    contexts=read(packet/'proof_map.json')['contexts'];need(len(contexts)==37,'37 contexts')
    for row in contexts:
        text=(packet/row['path']).read_text();need(hashlib.sha256(text[row['start']:row['end']].encode()).hexdigest()==row['sha256'],'proof span '+row['id'])
    migration=read(packet/'migration.json')
    for row in migration['unchanged_old_sections']:
        need(sha(packet/row['new'])==row['old_sha256']==row['new_sha256'],'old proof transfer')
        if a.study_root:need((a.study_root/row['old']).read_bytes()==(packet/row['new']).read_bytes(),'independent old byte identity')
    appendix=(packet/'volume/program-appendix.tex').read_text()
    includes=re.findall(r'\\VerbatimInput(?:\[[^]]*\])?\{([^}]+)\}',appendix)
    need({str((Path('volume')/x).as_posix()).replace('volume/../','') for x in includes}=={r['path'] for r in inv['files']} and len(includes)==10,'whole10 appendix inputs')
    old=read(ROOT/'evidence/topic_Representation_root_adoption__review.json');need(old['roles']['current_author']=='enumeration_volume' and old['roles']['independent_reviewer']=='enumeration_review','historical authorship')
    replay=read(ROOT/'fresh_author/report.json');need(replay['formal']['declarations']==22 and replay['programs']['negative_controls']==10,'actual fresh reports')
    need([r['pages'] for r in replay['render']]==[12,5,12,16] and all(r['matched_frozen_page_text'] for r in replay['render']),'45 fresh page texts')
    expected=read(ROOT/'independent_results.json');actual={'status':'PASS_INDEPENDENT_BOUNDED_CHECKS','graph':graph_check(packet/'certificate/graph.json'),'free_panel':free_check(),'F4':cross_ratio_check(),'author_code_imports':False}
    need(json.loads(json.dumps(actual))==expected,'independent literal graph/word/field replay')
    control=controls(a.out,scope,contract,inv,formal,read(packet/'certificate/graph.json'))
    report={'status':'PASS_DISTINCT_SCIENTIFIC_REVIEW_REPLAY','author_manifest_sha256':AUTHOR_SHA,'author_exports':131,'L126_dispositions':31,'retained_F010_blocks':6,'proof_contexts':37,'old_proof_sections_unchanged':8,'required_programs':1,'required_data_files':1,'optional_validation_programs':9,'scoped_inherited_Lean_reports':22,'fresh_render_pages':45,'independent':actual,'independent_controls':control,'uniform_proofs_automatically_verified':False,'author_code_imported_for_independent_checks':False}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['status','author_exports','L126_dispositions','proof_contexts','fresh_render_pages']}))
if __name__=='__main__':main()
