#!/usr/bin/env python3
"""Replay this review's bindings, scope controls and independent finite models.

This verifies the frozen evidence and the stated review boundary. It does not
algorithmically repeat the human mathematical reading. The complete author
program/Lean/render replay is separately preserved under fresh/.
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

HERE=Path(__file__).resolve().parent
PIN='aa21b62e7d9347fe29d184f429c8e89fcb13ba5d5efd2b5dd0dcf827e69aea2c'
PRINCIPAL=['L040.T1.1','L040.T1.2','L040.P3.1','L040.C6.5','L040.T6.6']
def need(b,msg):
    if not b:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def bind(base,row):
    q=Path(row['path']);need(not q.is_absolute() and '..' not in q.parts,'Unsafe binding')
    p=base/q
    need(p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Changed binding '+str(q))
def validate(s,r,f):
    need(s['source_ids']==['L040'],'Exact original identity')
    need(s['primary']['sha256']=='1945f07fb2a0395c9a033b5fc1aeb7f5f40cfcd8b2598d43679cf60eb24de9bb','Accepted edition')
    need(s['primary']['not_final_typeset_journal_pdf'] is True,'No final publisher edition claim')
    need(s['principal_row_ids']==PRINCIPAL and r['principal_statement_targets']==PRINCIPAL,'All five targets')
    need(len(s['contracts'])==35 and len({x['id'] for x in s['contracts']})==35,'Thirty-five distinct dispositions')
    need(len(s['proof_spans'])==25,'Complete written contexts')
    rows={x['id']:x for x in s['contracts']}
    need(rows['L040.C6.5']['status']=='corrected_complete_general_presentation','Corrected general presentation')
    need(rows['L040.C6.5.2']['status']=='literal_statement_refuted','No literal false presentation')
    need(rows['L040.Table1']['status']=='excluded_exact_census_not_claimed','No exact census inflation')
    need(rows['L040.leaf_count']['status']=='excluded_counting_convention_unfixed','No unfixed leaf count')
    need([x['role'] for x in s['program_inventory']]==[
        'required_finite_primitive_inputs','finite_validation','finite_validation',
        'required_only_for_auxiliary_n8_and_validation_of_branching'],'Exact four-program roles')
    need(s['program_boundary']['no_finite_sample_promoted_to_uniform_proof'] is True,'Uniform proof is written')
    need(s['program_boundary']['operational_drivers']==['check.py','formal/check.py'],'Both drivers declared')
    need(s['retained_inputs'][2]['path'] is None and s['retained_inputs'][2]['primary_full_text_locally_available'] is False,'Whiston access limitation')
    need(s['formal_declarations']==8 and f['new_declarations']==8 and f['source_specific_claims'] is False and not s['source_specific_classification_formalized'],'Actual partial formal scope')
    need(s['cost_boundary']['whole_common_paper_charged_once'] and not s['cost_boundary']['cross_topic_discount'],'Whole common theory paid')
    need(all(s['cost_boundary'][k] is None for k in ['ratio','retained_classical_proof_cost','source_graphics_cost','required_catalogue_construction_cost']),'Unknown costs remain unknown')
    need(r['author_manifest_sha256']==PIN and r['author']=='/root/enumeration_volume' and r['reviewer']=='/root/enumeration_review','Actual authorship and edition')
    need(r['new_source_credit']==r['new_question_credit']==r['new_formal_credit']==0 and r['root_admission_required_for_credit'],'No independent self-admission')
    need(r['fresh_replay']['formal_declarations']==8 and r['fresh_replay']['programs']==4 and r['fresh_replay']['rendered_pages']==28,'Fresh replay summary')
    need(r['source_correction']['literal_claim_recovered'] is False,'Review correction boundary')

def controls(s,r,f):
    cases=[
      ('wrong original',lambda a,b,c:a.__setitem__('source_ids',['L041'])),
      ('call accepted source final publisher',lambda a,b,c:a['primary'].__setitem__('not_final_typeset_journal_pdf',False)),
      ('drop principal presentation',lambda a,b,c:a['principal_row_ids'].pop(3)),
      ('drop auxiliary disposition',lambda a,b,c:a['contracts'].pop()),
      ('restore false branching clause',lambda a,b,c:next(x for x in a['contracts'] if x['id']=='L040.C6.5.2').__setitem__('status','recovered_complete')),
      ('claim exact C-rank census',lambda a,b,c:next(x for x in a['contracts'] if x['id']=='L040.Table1').__setitem__('status','recovered_complete')),
      ('demote finite premise',lambda a,b,c:a['program_inventory'][0].__setitem__('role','finite_validation')),
      ('promote finite cases to uniform proof',lambda a,b,c:a['program_boundary'].__setitem__('no_finite_sample_promoted_to_uniform_proof',False)),
      ('claim original Whiston acquisition',lambda a,b,c:a['retained_inputs'][2].__setitem__('primary_full_text_locally_available',True)),
      ('claim full Lean classification',lambda a,b,c:c.__setitem__('source_specific_claims',True)),
      ('price retained proof at zero',lambda a,b,c:a['cost_boundary'].__setitem__('retained_classical_proof_cost',0)),
      ('borrow unpriced earlier umbrella',lambda a,b,c:a['cost_boundary'].__setitem__('cross_topic_discount',True)),
      ('wrong current author',lambda a,b,c:b.__setitem__('author','/root/enumeration_review')),
      ('self-admit principal credit',lambda a,b,c:b.__setitem__('new_source_credit',1)),
    ]
    out=[]
    for name,fn in cases:
        a,b,c=copy.deepcopy((s,r,f));fn(a,b,c)
        try:validate(a,b,c)
        except ValueError as e:out.append({'name':name,'rejected':True,'reason':str(e)})
        else:raise ValueError('Accepted semantic mutation '+name)
    return out

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--packet',type=Path,required=True)
    ap.add_argument('--study-root',type=Path)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--gap',default=shutil.which('gap'))
    args=ap.parse_args()
    need(not os.path.lexists(args.out),'Fresh output required');args.out.mkdir(parents=True)
    A=args.packet.resolve();need(sha(A/'manifest.json')==PIN,'Wrong frozen author')
    b=read(HERE/'author_binding.json');bind(A,b['manifest'])
    for x in b['exports']:bind(A,x)
    if (HERE/'manifest.json').is_file():
        for x in read(HERE/'manifest.json')['exports']:bind(HERE,x)
    external=[]
    if args.study_root:
        for x in b['external_bindings']:
            if x['path'] is not None:bind(args.study_root,x);external.append(x['path'])
    s=read(A/'scope.json');r=read(HERE/'review.json');f=read(A/'formal/scope.json');validate(s,r,f)
    text=(A/'formal/IrredundantNormalization.lean').read_text()
    for x in f['statement_spans']:
        z=text[x['start_codepoint']:x['end_codepoint_exclusive']]
        need(hashlib.sha256(z.encode()).hexdigest()==x['sha256_utf8'],'Formal declaration span changed')
    need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s',text,re.M),'Unsupported formal mechanism')
    for k,x in s['proof_spans'].items():
        z=(A/x['path']).read_text()[x['start_codepoint']:x['end_codepoint_exclusive']]
        need(hashlib.sha256(z.encode()).hexdigest()==x['sha256_utf8'],'Written context changed '+k)
    source_review=read(HERE/'source_clause_review.json')
    need([{k:v for k,v in x.items() if k not in ['independent_disposition','review_note']} for x in source_review['rows']]==s['contracts'],'Clause reading interfaces changed')
    fresh=read(HERE/'fresh/report.json')
    need(fresh['status']=='PASS' and fresh['manifest_sha256']==PIN,'Full fresh replay')
    need([x['pages'] for x in fresh['render']]==[10,11,7] and all(x['per_page_text_identical'] and x['diagnostics']==[] for x in fresh['render']),'Render replay completeness')
    need(len(fresh['programs'])==4 and fresh['formal']['declarations']==8 and fresh['formal']['hypothesis_countermodels']==6,'Complete scoped executions')
    fre=read(HERE/'fresh/formal/report.json')
    axioms=[d for x in fre['modules'] for d in x['axioms']]
    need(len(axioms)==8 and all(set(x['axioms'])<={'propext','Classical.choice','Quot.sound'} for x in axioms),'Fresh standard axiom reports')
    need(args.gap,'GAP required for independent finite diagnostics')
    p=subprocess.run([args.gap,'-q','-T',str(HERE/'independent_models.g')],capture_output=True,text=True,timeout=180)
    (args.out/'independent_models.stdout').write_text(p.stdout);(args.out/'independent_models.stderr').write_text(p.stderr)
    need(p.returncode==0 and not re.search(r'error|warning',p.stdout+p.stderr,re.I),'Independent GAP run failed')
    markers=['TREE_PRESENTATIONS path/star/two-branch each S6 PASS','CONTROL remove-root-leaf: intersection S4 order24 > coreV4 order4 PASS','CONTROL omit-triangle: involutions/pair3 but triangleword order5 PASS','SOURCE_CORRECTION branching S9 has two noncommuting tail neighbours PASS','PASS independent written-interface models']
    need(all(x in p.stdout for x in markers),'Incomplete independent finite run')
    out={'status':'PASS','author_manifest_sha256':PIN,'author_exports':len(b['exports']),'source_rows':35,'proof_contexts':25,'formal_statement_spans':8,'external_bindings':external,'semantic_controls':controls(s,r,f),'independent_models':{'markers':markers,'trust':'Exact GAP presentation/group computations; bounded diagnostics only.'},'preserved_full_author_replay':{'programs':4,'Lean_declarations':8,'hypothesis_countermodels':6,'source_scope_controls':11,'local_controls':5,'rendered_pages':28},'human_proof_review_repeated_by_this_checker':False,'new_source_credit':0,'new_question_credit':0,'ratio':None}
    (args.out/'report.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS','exports':46,'source_rows':35,'controls':len(out['semantic_controls']),'out':str(args.out)}))
if __name__=='__main__':main()
