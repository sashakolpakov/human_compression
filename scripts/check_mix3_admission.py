#!/usr/bin/env python3
"""Check the three-original Mixes admission, including exact reused payloads."""
import argparse,hashlib,importlib.util,json,subprocess,sys,tempfile
from pathlib import Path


def verify(root):
    def need(test,message):
        if not test:raise ValueError('MIX3: '+message)
    def read(path):return json.loads((root/path).read_text())
    def binding(row):
        p=Path(row['path']);need(not p.is_absolute() and '..' not in p.parts,'safe binding')
        b=(root/p).read_bytes();need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],str(p))
    def module(name,path):
        spec=importlib.util.spec_from_file_location(name,root/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
    base='audit/topic-mixes/v3/';a=read(base+'admission.json')
    need(a['status']=='ROOT_ADMITTED_CORRECTED_PRINCIPAL_CONTRACTS_AND_SYMMETRIC_MEASUREMENT'
         and a['source_ids']==['F005','L016','F007'] and a['principal_originals_added']==['F007']
         and a['original_intake_added']==a['new_question_credit']==a['new_formal_credit']==0,'scope or credit')
    for key in ['F007_source_contract','retained_prior_admission','measurement','reader','publication_plan','root_publication_replay']:
        binding(a[key])
    for row in a['new_payloads']+a['existing_payload_references']+a['new_guide_bindings']:
        binding(row)
    for row in a['accepted_packets']+[a['publication_plan']]:
        binding(row);folder=Path(row['path']).parent
        for e in read(row['path'])['exports']:binding(dict(e,path=str(folder/e['path'])))
    plan=module('mix3_publication_plan',base+'publication_plan/check.py')
    assembled=plan.validate(read(base+'publication_plan/assembly_map.json'),root,root)
    titles=plan.closures(root)
    need(assembled['new_copies']==130 and assembled['existing_payload_references']==114
         and len(titles)==12 and sum(r['pages']for r in titles)==52,'complete public assembly')
    need(read(base+'science_review/review.json')['status']=='INDEPENDENTLY_ACCEPTED_F007_CORRECTED_PRINCIPAL_PROOF_V2'
         and read(base+'science_review/review.json')['remaining_corrections_requested']==[]
         and read(base+'science_adoption/adoption.json')['status']=='ROOT_ACCEPTED_F007_CORRECTED_PRINCIPAL_PROOF',
         'distinct science and adoption')
    need(read(base+'measurement/independent_review/review.json')['status']=='ROOT_ACCEPTED_DISTINCT_NUMERICAL_REVIEW',
         'distinct numerical acceptance')
    with tempfile.TemporaryDirectory(prefix='mix3-independent-') as temp:
        out=Path(temp)/'report.json'
        result=subprocess.run([sys.executable,'-B','-O',str(root/base/'measurement/independent_review/recount.py'),
            '--packet',str(root/base/'measurement/packet'),'--out',str(out)],capture_output=True,text=True)
        need(result.returncode==0,'distinct numerical replay: '+result.stderr[-2000:])
        numerical=json.loads(out.read_text())
    need(numerical['exact_fractions']==120 and numerical['SVG_bars']==numerical['PDF_bars']==16,'numerical scope')
    r=read(base+'measurement/packet/results.json');c=r['primary']
    need(a['primary']==c['written']==numerical['primary_whole']
         and a['conditionals']==c['conditional']==numerical['primary_individual']
         and (a['source_sum'],a['whole_common'],a['application_sum'],a['whole_written'])==(156570,34757,68693,103450),
         'admitted exact factors')
    need(a['symmetric_program_exclusion'] and a['historical_source_software_cost'] is None
         and a['software_inclusive_factor'] is None and not a['whole_source_formalized'],'bounded cost and formal claims')
    need(a['source_dispositions']==dict(F005=35,L016=19,F007_numbered=48,F007_additional=6),'all source dispositions')
    return dict(status='PASS_MIX3_ADMISSION',originals=3,new_originals=1,new_original_ids=['F007'],
                current_catalogue_rows=10,historical_inventory_rows=2,scientific_pages=40,program_pages=12,
                coordinates=30,exact_fractions=120,actual_SVG_bars=16,actual_PDF_bars=16,
                software_inclusive_factor=None,whole_source_formalized=False)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1])
    print(json.dumps(verify(ap.parse_args().repo),indent=2))
