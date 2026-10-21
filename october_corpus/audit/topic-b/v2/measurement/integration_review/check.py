#!/usr/bin/env python3
"""Bounded read-only Topic B measurement publication integration review."""
import argparse, ast, copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
BASELINE='608e5b0a995adea3b2934fc77fca3661f778e2d5'
BASE='audit/topic-b/v2/measurement/'
PINS={'packet/manifest.json':'c61503c52b1e0136b0eb70ebe7993c63dc635933e6ae0bf9a50d7c164d211609',
      'arithmetic_review/manifest.json':'8ed72316d4a73735f83b3f83522b8e11bc7594dc583418e1182e0c09a2539c17'}
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n):return ast.dump(n,include_attributes=False)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    root=a.public_root.resolve();need(not a.out.exists(),'fresh output')
    spec=importlib.util.spec_from_file_location('measurement_public_review',root/'scripts/verify_snapshot.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);load=m.load
    admission=load(BASE+'admission.json')
    need(sha(root/BASE/'admission.json')=='4cef3709c9fb6018cba1e3aaedcf6887caf8223b071be7f2f5a6b413ce771df9','exact admission')
    m.check_bindings(admission['artifacts']);preserved=0
    for relative,h in PINS.items():
        p=root/BASE/relative;need(sha(p)==h,'frozen packet pin')
        for row in json.loads(p.read_text())['exports']:
            q=p.parent/row['path'];need(q.stat().st_size==row['bytes'] and sha(q)==row['sha256'],'frozen export')
            preserved+=1
    need(m.check_topic_b_measurement()==(240,90),'positive new standard check')
    need(m.check_topic_b_proofs()==(30,6),'existing mathematical check preserved')
    previous=subprocess.check_output(['git','show',BASELINE+':scripts/verify_snapshot.py'],cwd=root,text=True)
    old={n.name:n for n in ast.parse(previous).body if isinstance(n,ast.FunctionDef)}
    new={n.name:n for n in ast.parse((root/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,ast.FunctionDef)}
    need(set(new)-set(old)=={'check_topic_b_measurement'} and set(old)<=set(new),'only one new verifier function')
    need(all(dump(v)==dump(new[k]) for k,v in old.items() if k!='main'),'old non-main functions unchanged')
    original_main=copy.deepcopy(old['main'])
    # One obsolete status suffix is intentionally removed after measurement admission.
    for n in ast.walk(original_main):
        if isinstance(n,ast.Constant) and isinstance(n.value,str) and n.value==' separately checked Lean declarations; no measured ratio yet.':
            n.value=' separately checked Lean declarations.'
    current=copy.deepcopy(new['main']);oldstat=[dump(n) for n in original_main.body]
    extra=[n for n in current.body if dump(n) not in oldstat]
    need(len(extra)==2 and any('check_topic_b_measurement' in dump(n) for n in extra)
         and any('b_fractions' in dump(n) for n in extra),'only measurement main call/output added')
    current.body=[n for n in current.body if dump(n) in oldstat]
    need(dump(current)==dump(original_main),'old main checks and order preserved, one obsolete status suffix updated')
    for name in ['papers/catalogue.json','scripts/build_papers.py','research/case_study/formal/lakefile.lean',
                 'audit/topic-b/v2/admission.json','papers/topic-b/v2/manifest.json']:
        need((root/name).read_bytes()==subprocess.check_output(['git','show',BASELINE+':'+name],cwd=root),'unchanged existing scientific binding: '+name)
    need(admission['source_ids']==['N001','N003','N008','L030'] and admission['application_ids']==['B1','B2','B3','B4'],'same four contracts')
    need(admission['proof_admission']=='audit/topic-b/v2/admission.json'
         and sha(root/admission['proof_admission'])==admission['proof_admission_sha256'],'mathematical admission route')
    fresh=load(BASE+'root_replay.json');original=load(BASE+'arithmetic_review/report.json')
    for k in ['coordinates','exact_known_conditional_fractions','unknown_conditional_coordinates','unknown_overall_coordinates',
              'overall_CSV_rows','conditional_CSV_rows','primary','controls','reader_pages','reader_page_hashes','checker_sha256']:
        need(fresh[k]==original[k],'public fresh/independent equality: '+k)
    routes=[]
    for name in ['README.rst','audit/completion.rst',BASE+'README.rst']:
        p=root/name;text=p.read_text()
        for target in re.findall(r'<([^<>]+)>`_',text):
            if re.match(r'^[a-z]+:',target) or target.startswith('#'):continue
            path=(p.parent/target.split('#')[0]).resolve()
            need(path.exists(),'reader link exists: '+name+' '+target)
            routes.append(dict(document=name,target=target))
    summary=(root/'README.rst').read_text()
    for phrase in ['57,539','59,061','1.254','1.576','1.811','B1 remains in the denominator','paired dependency audit is still in progress']:
        need(phrase in summary,'root summary scope: '+phrase)
    queue=load('audit/work_queue.json')
    # Human reviewed queue/protocol wording is bound below, not used to infer new mathematics.
    cases=[
      ('invent_overall_factor',BASE+'admission.json',lambda d:d.update(overall_factor=1.2)),
      ('add_source_credit',BASE+'admission.json',lambda d:d.update(new_source_credit=1)),
      ('claim_completed_dependency_audit',BASE+'admission.json',lambda d:d.update(paired_dependency_audit_complete=True)),
      ('claim_repeated_primary_extraction',BASE+'admission.json',lambda d:d.update(full_source_reextraction_in_arithmetic_review=True)),
      ('wrong_review_binding',BASE+'arithmetic_review/review.json',lambda d:d.update(author_manifest_sha256='0'*64)),
      ('unaccepted_input_recount',BASE+'packet/independent/review.json',lambda d:d.update(status='PENDING')),
      ('drop_B1_cost',BASE+'packet/results.json',lambda d:d['coordinates'][0].update(complete_denominator=1)),
      ('invent_N001_zero',BASE+'packet/results.json',lambda d:d['coordinates'][0]['per_result'][0].update(source_cost=0)),
      ('omit_measured_B1',BASE+'packet/inputs/publication_binding.json',lambda d:d['scientific_documents'].pop('B1')),
      ('lose_control',BASE+'root_replay.json',lambda d:d['controls'].pop()),
      ('wrong_current_PDF_route',BASE+'packet/inputs/publication_binding.json',lambda d:d['scientific_documents']['B1'].update(public_path='papers/topic-b/v2/umbrella.pdf'))]
    controls=[]
    for name,route,edit in cases:
        changed=copy.deepcopy(load(route));edit(changed)
        m.load=lambda p,route=route,changed=changed:copy.deepcopy(changed) if str(p)==route else load(p)
        try:m.check_topic_b_measurement()
        except (ValueError,KeyError) as e:controls.append(dict(name=name,rejected=True,reason=str(e)))
        else:controls.append(dict(name=name,rejected=False))
        finally:m.load=load
    need(all(c['rejected'] for c in controls),'all in-memory semantic corruptions rejected')
    names=['scripts/verify_snapshot.py',BASE+'admission.json',BASE+'README.rst',BASE+'root_replay.json',
           'README.rst','audit/completion.rst','audit/work_queue.json','audit/protocol.tex']
    report=dict(status='PASS_BOUNDED_TOPIC_B_MEASUREMENT_PUBLICATION_REVIEW',baseline_commit=BASELINE,
        frozen_exports_preserved=preserved,admission_artifact_bindings=len(admission['artifacts']),
        standard_measurement_result=[240,90],standard_mathematical_result=[30,6],
        old_non_main_verifier_functions_unchanged=len(old)-1,old_main_statements_preserved=True,
        catalogue_and_scientific_build_inputs_unchanged=True,public_replay_matches_independent=True,
        controls=controls,controls_are_in_memory_load_overrides=True,checked_reader_links=routes,
        reviewed_bindings=[dict(path=n,bytes=(root/n).stat().st_size,sha256=sha(root/n)) for n in names],
        protocol_PDF_reviewed=False,primary_extraction_or_mathematics_repeated=False,public_files_modified=False)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','frozen_exports_preserved','admission_artifact_bindings','old_non_main_verifier_functions_unchanged']}))
if __name__=='__main__':main()
