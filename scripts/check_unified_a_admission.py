#!/usr/bin/env python3
"""Check the admitted eight-original common theory and its exact measurements."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


def verify(root):
    def need(test, message):
        if not test:
            raise ValueError('UNIFIED_A: ' + message)
    def read(path):
        return json.loads((root / path).read_text())
    def binding(row):
        relative=Path(row['path'])
        need(not relative.is_absolute() and '..' not in relative.parts,'safe binding')
        data=(root/relative).read_bytes()
        need(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],str(relative))
    def module(name,path):
        spec=importlib.util.spec_from_file_location(name,root/path)
        result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
        return result
    base='audit/topic-a/v3/'
    admission=read(base+'admission.json')
    sources=['L032','L034','F016','F013','L035','N009','L128','L012']
    need(admission['status']=='ROOT_ADMITTED_UNIFIED_A_AFFINE_PRINCIPAL_CONTRACTS_AND_SYMMETRIC_MEASUREMENT'
         and admission['source_ids']==sources and admission['principal_originals_added']==[]
         and admission['original_intake_added']==admission['new_source_credit']==admission['new_question_credit']==admission['new_formal_credit']==0,
         'source or credit boundary')
    for key in ['source_dispositions','scientific_scope','formal_scope','measurement','reader',
                'publication_plan','root_publication_replay']:
        binding(admission[key])
    for row in admission['frozen_payloads']+admission['new_guide_bindings']:
        binding(row)
    for row in list(admission['packets'].values())+admission['embedded_input_packets']+[admission['publication_plan']]:
        binding(row);folder=Path(row['path']).parent
        for entry in read(row['path'])['exports']:
            binding(dict(entry,path=str(folder/entry['path'])))
    plan=module('unified_a_publication_plan',base+'publication_plan/check.py')
    scope=plan.validate(read(base+'publication_plan/assembly_map.json'),root,root)
    titles=plan.titles_and_inputs(root)
    need(len(titles)==12 and sum(x['pages'] for x in titles)==98,'all written and program pages')
    need(scope['source_rows']==admission['source_rows']==102
         and scope['inclusive_proof_interfaces']==admission['inclusive_proof_interfaces']==60
         and admission['interfaces_are_disjoint_cost_nodes'] is False,'proof accounting')
    science=read(base+'scientific_review/review.json')
    need(science['status']=='ACCEPTED_SCIENTIFIC_CONSOLIDATION_WITH_EXPLICIT_FORMAL_AND_MEASUREMENT_LIMITS'
         and science['source_ids']==sources and science['blocking_scientific_findings']==[],
         'distinct scientific acceptance')
    formal=read('papers/topic-a/v3/formal_scope.json')
    need(formal['module_count']==14 and formal['new_declarations']==0
         and not formal['whole_volume_formalized'] and not formal['arbitrary_parabolic_theorem_formalized']
         and not admission['whole_source_formalized'],'partial formal scope')
    reviewer=module('unified_a_distinct_numerical',base+'measurement/independent_review/check.py')
    result=reviewer.check(root/base/'measurement/packet',None,None)
    need(result['status']=='PASS_DISTINCT_NUMERICAL_ARITHMETIC_AND_GEOMETRY'
         and result['exact_fractions']==270 and result['actual_SVG_bars']==result['actual_PDF_bars']==27
         and len(result['controls_rejected'])==21,'independent arithmetic and geometry')
    r=read(base+'measurement/packet/results.json');c=r['coordinates'][r['primary_coordinate']]
    need(admission['primary_coordinate']==r['primary_coordinate']=='calibrated_selected/NFC/characters_without_whitespace'
         and admission['primary']==c['written']==result['primary']
         and admission['conditionals']==c['conditional']==result['conditionals'],'admitted fractions')
    need((admission['source_sum'],admission['whole_common'],admission['application_sum'],admission['whole_written'])
         ==(246570,66140,110576,176716),'complete written costs')
    need(admission['required_whole_program_or_data_files']==11
         and admission['inherited_auxiliary_files']==3 and admission['operational_drivers']==2
         and admission['symmetric_program_exclusion']
         and admission['historical_source_software_cost'] is None
         and admission['software_inclusive_factor'] is None,'symmetric program accounting')
    need(read(base+'measurement/root_adoption/adoption.json')['status']=='ROOT_ACCEPTED_UNIFIED_A_AFFINE_NUMERICAL_COMPARISON',
         'root numerical acceptance')
    return dict(status='PASS_UNIFIED_A_ADMISSION',originals=8,new_originals=0,
                source_dispositions=102,inclusive_proof_interfaces=60,literal_titles=12,
                scientific_pages=68,program_pages=30,coordinates=30,exact_fractions=270,
                actual_SVG_bars=27,actual_PDF_bars=27,whole_source_formalized=False,
                software_inclusive_factor=None)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1])
    print(json.dumps(verify(ap.parse_args().repo),indent=2))
