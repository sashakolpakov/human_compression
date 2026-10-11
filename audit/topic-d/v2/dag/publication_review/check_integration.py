#!/usr/bin/env python3
"""Bounded review of Topic D publication wiring; no primary extraction/proof replay.

Semantic mutations replace parsed in-memory records after byte integrity checks.
The separate binding control runs with all integrity checks active. No public
file is changed. This checks the integration, not the accepted mathematics.
"""
import argparse, ast, copy, hashlib, importlib.util, json, re, subprocess
from pathlib import Path

BASELINE='fe91a420a9120a0566b474209c71e1732cc5bebe'
PREFIX='audit/topic-d/v2/dag/'
def require(b,s):
    if not b: raise ValueError(s)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--study',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    require(not a.out.exists(),'fresh output required')
    repo=a.repo;script=repo/'scripts/verify_snapshot.py'
    before=subprocess.check_output(['git','show',BASELINE+':scripts/verify_snapshot.py'],cwd=repo,text=True)
    after=script.read_text()
    defs=lambda s:{n.name:n for n in ast.parse(s).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
    bd,ad=defs(before),defs(after)
    unchanged=[]
    for k,n in bd.items():
        if k=='main':continue
        require(k in ad and ast.dump(n,include_attributes=False)==ast.dump(ad[k],include_attributes=False),'old verifier changed '+k);unchanged.append(k)
    require(set(ad)-set(bd)=={'check_topic_d_dag'},'unexpected added function')
    calls=lambda node:[n.func.id for n in ast.walk(node) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id.startswith('check_')]
    bc,ac=calls(bd['main']),calls(ad['main'])
    require([x for x in ac if x!='check_topic_d_dag']==bc and ac.count('check_topic_d_dag')==1,'main changed old validation calls')
    mapping=read(repo/PREFIX/'publication_mapping.json');admission=read(repo/PREFIX/'admission.json')
    copies=[];count=0
    for private,public in mapping['private_to_public'].items():
        old=a.study/private;new=repo/public
        require((old/'manifest.json').read_bytes()==(new/'manifest.json').read_bytes(),'manifest relocation '+private)
        manifest=read(old/'manifest.json')
        require(sha(new/'manifest.json')==mapping['packet_manifests'][new.name]==admission['packet_manifests'][new.name],'manifest pin '+private)
        for r in manifest['exports']:
            x,y=old/r['path'],new/r['path']
            require(x.read_bytes()==y.read_bytes() and sha(y)==r['sha256'] and y.stat().st_size==r['bytes'],'exact export '+str(y));count+=1
        copies.append({'private':private,'public':public,'manifest_sha256':sha(new/'manifest.json'),'exports':len(manifest['exports'])})
    require(count==169 and len(copies)==10,'archive counts')
    for r in admission['artifacts']:
        x=repo/r['path'];require(sha(x)==r['sha256'] and x.stat().st_size==r['bytes'],'admission artifact '+str(x))
    require(len(admission['artifacts'])==183,'admission inventory count')
    spec=importlib.util.spec_from_file_location('reviewed_d_integration',script);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    prior={}
    for name in ['check_topic_d_proofs','check_topic_d_support_formal','check_topic_d_measurement']:
        prior[name]=getattr(m,name)()
    positive=m.check_topic_d_dag();require(positive==(240,116),'new positive result')
    original_load=m.load; controls=[]
    def run_control(name,target,change,expected):
        def mutated(path):
            data=original_load(path)
            if str(path)==target:
                data=copy.deepcopy(data);change(data)
            return data
        m.load=mutated
        try:m.check_topic_d_dag()
        except ValueError as e:
            require(expected in str(e),'wrong rejection for '+name+': '+str(e));controls.append({'name':name,'rejected':True,'reason':str(e),'mechanism':'in-memory parsed-record mutation; disk bytes and prior integrity guards unchanged'})
        else:raise ValueError('accepted mutation '+name)
        finally:m.load=original_load
    def binding_change(x):x['artifacts'][0]['sha256']='0'*64
    run_control('changed_audited_artifact',PREFIX+'admission.json',binding_change,'Changed audited artifact')
    run_control('wrong_preserved_export_count',PREFIX+'admission.json',lambda x:x.__setitem__('preserved_frozen_exports',168),'frozen graph inventory')
    run_control('lost_support_premise',PREFIX+'logical/logical_graph.json',lambda x:x['edges'].__setitem__(slice(None),[e for e in x['edges'] if not(e['source']=='UD.ExactSupport' and e['target']=='D2.Support')]),'exact logical correction')
    run_control('lost_restored_theorem_setup',PREFIX+'costs/weights.json',lambda x:x['node_interfaces']['h.L074.12']['owners'].remove('h.L074.composite_setup'),'reviewed passage correction')
    run_control('unknown_external_cost_set_to_zero',PREFIX+'costs/weights.json',lambda x:x['node_interfaces']['ext.Mobius'].__setitem__('known_weight',0),'node owners or unknown cost')
    run_control('duplicate_theorem_owner',PREFIX+'costs/weights.json',lambda x:x['node_interfaces']['D2.Duality']['owners'].append(x['node_interfaces']['D2.Duality']['owners'][0]),'node owners or unknown cost')
    def location_change(x):
        next(n for n in x['nodes'] if n.get('current_public_locators'))['current_public_locators'][0]['start_codepoint']+=1
    run_control('changed_public_proof_locator',PREFIX+'costs/view_data.json',location_change,'exact public proof locator')
    run_control('incorrect_whole_written_denominator',PREFIX+'admission.json',lambda x:x.__setitem__('primary_written_denominator',45486),'admission summary')
    run_control('invented_historical_program_cost',PREFIX+'admission.json',lambda x:x.__setitem__('historical_software_cost',0),'invents a cost')
    # The common acquisition object occurs twice. Mutate both copies to reach the
    # whole-context check rather than merely the duplicate-data equality check.
    def bad_acq(d):d['stages'][2]['complete_local_owner_ids'].pop()
    def two_load(path):
        data=original_load(path)
        if str(path)==PREFIX+'costs/acquisition.json':data=copy.deepcopy(data);bad_acq(data)
        if str(path)==PREFIX+'costs/view_data.json':data=copy.deepcopy(data);bad_acq(data['acquisition'])
        return data
    m.load=two_load
    try:m.check_topic_d_dag()
    except ValueError as e:
        require('acquisition omits context' in str(e),'wrong acquisition rejection');controls.append({'name':'omitted_complete_local_context','rejected':True,'reason':str(e),'mechanism':'same parsed acquisition mutation in its two views'})
    else:raise ValueError('accepted context omission')
    finally:m.load=original_load
    require(m.check_topic_d_dag()==positive,'unmodified checker no longer passes')
    # Reader's old binding ledger is provenance, not the selected graph. Check
    # actual source selection, embedded edition pin and whole-program links.
    gen=(repo/PREFIX/'costs/reader_data.py').read_text();checker=(repo/PREFIX/'costs/check_reader.py').read_text()
    require("topic_D_logical_dag_v3/logical_graph.json" in gen and "topic_D_logical_dag_v3/coverage.json" in gen,'reader generator not v3')
    require("topic_D_logical_dag_v3/logical_graph.json" in checker,'reader validator not v3')
    current=read(repo/PREFIX/'costs/input_bindings.json')['inputs'];historical=read(repo/PREFIX/'costs/reader_input_bindings.json')['inputs']
    require(any(r['path']=='topic_D_logical_dag_v3/manifest.json' and r['sha256']==admission['packet_manifests']['logical'] for r in current),'operative v3 binding')
    require(any('topic_D_logical_dag_v2/' in r['path'] for r in historical),'old reader provenance not preserved')
    hrefs=[]
    for fn in ['README.rst',PREFIX+'README.rst']:
        txt=(repo/fn).read_text()
        for href in re.findall(r'<([^<>]+)>`_',txt):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',href):continue
            target=href.split('#')[0]
            if not target:continue
            x=(repo/fn).parent/target
            require(x.exists(),'broken local documentation link '+fn+' '+target);hrefs.append({'document':fn,'target':target})
    files=['scripts/verify_snapshot.py','README.rst','audit/protocol.tex','audit/protocol.pdf',PREFIX+'admission.json',PREFIX+'publication_mapping.json',PREFIX+'README.rst',PREFIX+'costs/view_data.json',PREFIX+'costs/input_bindings.json',PREFIX+'costs/reader_input_bindings.json',PREFIX+'costs/public_links.json']
    bindings=[{'path':x,'bytes':(repo/x).stat().st_size,'sha256':sha(repo/x)} for x in files]
    report={'status':'PASS_BOUNDED_INDEPENDENT_D_DAG_PUBLICATION_INTEGRATION','baseline':BASELINE,'unchanged_prior_non_main_functions':unchanged,'prior_check_results':prior,'new_check_result':positive,'exact_copied_exports':count,'exact_archive_manifests':copies,'admission_artifacts':183,'negative_controls':controls,'local_document_links':hrefs,'reader_selection':{'current_graph':'logical_v3','historical_reader_input_bindings_retained':True,'generator_and_validator_select_v3':True,'private_inputs_still_needed_for_fresh_extraction':True},'bindings':bindings,'full_primary_or_mathematical_replay_performed':False,'public_files_changed_by_reviewer':False,'real_browser_test':False}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'old_functions':len(unchanged),'copies':count,'controls':len(controls),'new_check':positive,'links':len(hrefs)}))
if __name__=='__main__':main()
