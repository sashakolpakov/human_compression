#!/usr/bin/env python3
"""Bounded Topic C publication review; no source extraction or mathematical replay."""
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import tempfile
from pathlib import Path

PIN='0f8251532767b91bac22939beb4871749f1f2fe72b2b78dcf6a793b854c39d7f'
BASE='b9a7f0734540afc797b8c1b9a994afc4f94b291b'
MAPPING={'previous':'topic_C_measurement_results',
         'packet':'topic_C_measurement_results_v2',
         'arithmetic_review':'topic_C_arithmetic_independent_review'}

def need(ok,message):
    if not ok: raise ValueError(message)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--public-root',type=Path,required=True)
    ap.add_argument('--study-root',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'Fresh output required')
    root=a.public_root;relative='audit/topic-c/v2/measurement/';base=root/relative
    need(sha(base/'admission.json')==PIN,'Admission changed during review')
    admission=read(base/'admission.json');copied=0
    for pub,private in MAPPING.items():
        x=base/pub;y=a.study_root/private
        need((x/'manifest.json').read_bytes()==(y/'manifest.json').read_bytes(),'Manifest '+pub)
        for row in read(y/'manifest.json')['exports']:
            need((x/row['path']).read_bytes()==(y/row['path']).read_bytes(),'Frozen export '+pub+'/'+row['path'])
            copied+=1
    for row in admission['artifacts']:
        p=root/row['path'];need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Admission binding')
    old=subprocess.check_output(['git','show',BASE+':scripts/verify_snapshot.py'],cwd=root,text=True)
    current=(root/'scripts/verify_snapshot.py').read_text()
    def funcs(text):
        return {x.name:ast.dump(x,include_attributes=False) for x in ast.parse(text).body
                if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))}
    before=funcs(old);after=funcs(current);previous=set(before)-{'main'}
    need(all(before[k]==after[k] for k in previous),'Existing verifier changed')
    need(set(after)-set(before)=={'check_topic_c_measurement'},'Unexpected new verifier functions')
    changed=subprocess.check_output(['git','diff','--name-only',BASE],cwd=root,text=True).splitlines()
    protected=[p for p in changed if p.startswith(('papers/','research/','audit/topic-a/','audit/topic-b/','audit/topic-e/'))
               or p in ['audit/topic-c/v2/admission.json','audit/completion.json','audit/source_registry.json']]
    need(not protected,'Existing mathematics, counts or earlier topic audits changed')
    for p in base.rglob('*'):
        if p.is_file():
            need(p.suffix not in {'.md','.txt','.olean'},'Unexpected text/cache artifact')
            if p.suffix in {'.pdf','.png'}:
                need(p.parent.name in {'packet','previous'} and p.stem in {'costs','measurement'},'Unexpected primary image/PDF')
    links=[]
    for doc in [base/'README.rst',root/'README.rst',root/'audit/completion.rst']:
        text=doc.read_text()
        for target in re.findall(r'<([^<>]+)>`_',text):
            if '://' in target or target.startswith('#'): continue
            path=target.split('#')[0]
            need((doc.parent/path).exists(),'Broken published link '+str(doc)+': '+target)
            links.append({'document':str(doc.relative_to(root)),'target':target})
    module_spec=importlib.util.spec_from_file_location('c_public_verifier',root/'scripts/verify_snapshot.py')
    v=importlib.util.module_from_spec(module_spec);module_spec.loader.exec_module(v)
    need(v.check_topic_c_measurement()==(270,90),'Public verifier result')
    controls=[];original_load=v.load
    cases=[
      ('program_comparison_promoted','packet/results.json',lambda x:x.update(headline_comparison='complete_printed_programs')),
      ('missing_L108_zero','admission.json',lambda x:x.update(L108_original_pdf_cost=0)),
      ('drop_C3','packet/results.json',lambda x:x['coordinates'][0].__setitem__('all_applications',0)),
      ('double_charge_programs','packet/results.json',lambda x:x['coordinates'][0].__setitem__('complete_denominator',x['coordinates'][0]['complete_denominator']+x['coordinates'][0]['complete_raw_program_cost'])),
      ('conditional_without_common_and_code','packet/results.json',lambda x:x.update(complete_common_and_programs_prepaid_for_conditional_factors=False)),
      ('external_cost_zero','packet/results.json',lambda x:x.update(outside_proof_cost=0)),
      ('missing_required_program','packet/inputs/replacement_input_spec.json',lambda x:x['required_mathematical_programs'].pop()),
      ('new_question_credit','admission.json',lambda x:x.update(new_question_credit=1)),
      ('premature_dependency_acceptance','admission.json',lambda x:x.update(paired_dependency_audit_complete=True))]
    for name,path,change in cases:
        full=relative+path;mut=copy.deepcopy(original_load(full));change(mut)
        v.load=lambda p,match=full,value=mut:copy.deepcopy(value) if p==match else original_load(p)
        try: v.check_topic_c_measurement()
        except (ValueError,KeyError) as error:controls.append({'name':name,'rejected':True,'reason':str(error),'mode':'Parsed-data mutation only; frozen files unchanged'})
        else: raise ValueError('Accepted mutation '+name)
        finally: v.load=original_load
    with tempfile.TemporaryDirectory(prefix='topic-c-public-binding-') as td:
        p=Path(td)/'artifact.json';p.write_text('{}\n');row={'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)}
        p.write_text('{"changed":true}\n');oldroot=v.ROOT;v.ROOT=Path(td)
        try:v.check_bindings([row])
        except ValueError as error:controls.append({'name':'changed_bound_bytes','rejected':True,'reason':str(error),'mode':'Temporary file only'})
        else:raise ValueError('Changed bytes accepted')
        finally:v.ROOT=oldroot
    report={'status':'PASS_BOUNDED_TOPIC_C_PUBLICATION_REVIEW','baseline_commit':BASE,
      'admission_sha256':PIN,'exact_packet_copies':3,'copied_exports':copied,
      'admission_bindings':len(admission['artifacts']),'unchanged_previous_non_main_ASTs':len(previous),
      'new_verifier_result':[270,90],'protected_files_changed':protected,'checked_relative_links':len(links),
      'controls':controls,'source_reextraction':False,'mathematical_or_Lean_or_GAP_replay':False,
      'new_source_credit':0,'new_question_credit':0,'new_factor':None,'public_files_modified':False,
      'reader_bindings':{str(p.relative_to(root)):sha(p) for p in [root/'README.rst',root/'audit/completion.rst',
        root/'audit/work_queue.json',root/'audit/protocol.tex',root/'audit/protocol.pdf',base/'README.rst',
        base/'root_integration.json',root/'scripts/verify_snapshot.py']}}
    a.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['controls','reader_bindings']}))

if __name__=='__main__':main()
