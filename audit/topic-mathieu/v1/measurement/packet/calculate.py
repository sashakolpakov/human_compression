#!/usr/bin/env python3
"""Exact arithmetic on separately accepted complete L073 text/file counts."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, localcontext
import json,hashlib
ROOT=Path(__file__).resolve().parent
PINS={'input_manifest':'bbef6f90211122f5b5db138bfadd8bb1538bd88f1d6dd7b41dd175e268512de2','review_manifest':'e33647116d0bd471cba28eb43448090153f7a6dde8b3e366fbaaa30670a50467'}
VARIANTS=['raw_untrimmed','raw_selected','calibrated_selected']; FORMS=['NFC','NFKC']
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
DOCS=['L073','U','A1','CLASSES','ROWS','CODE']; APP=['A1','CLASSES','ROWS']; GROUPS=['programs','required_raw_data','drivers','generated_outputs']
UNKNOWN={'full_graphics':None,'retained_external_proofs':None,'full_catalogue_construction_and_algorithm_proofs':None,'full_formalization':None}
def need(x,m):
    if not x:raise ValueError(m)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def fraction(n,d):
    need(type(n)is int and type(d)is int and n>0 and d>0,'positive integer costs');f=Fraction(n,d)
    with localcontext() as c:
        c.prec=50;decimal=f'{Decimal(n)/Decimal(d):.12f}'
    return dict(numerator=n,denominator=d,reduced_numerator=f.numerator,reduced_denominator=f.denominator,decimal=decimal)
def load(root=ROOT):
    protocol=read(root/'protocol.json');data={}
    for r in protocol['inputs']:
        p=Path(r['path']);need(not p.is_absolute()and '..'not in p.parts,'local relative evidence');f=root/p
        need(f.stat().st_size==r['bytes']and sha(f)==r['sha256'],'exact copied evidence '+r['key']);data[r['key']]=read(f)
    for key,pin in PINS.items():need(sha(root/'inputs'/(key+'.json'))==pin,'accepted input/review pin')
    mapping={'policy':'policy.json','counts':'author_counts.json','boundary':'accounting_boundary.json','input_protocol':'protocol.json','modular_acceptance':'modular_acceptance.json'}
    for manifest,keys in [('input_manifest',mapping),('review_manifest',{'review':'review.json','recount':'recount.json'})]:
        entries={r['path']:r for r in data[manifest]['exports']}
        for key,name in keys.items():
            e=entries[name];f=root/'inputs'/(key+'.json');need(e['bytes']==f.stat().st_size and e['sha256']==sha(f),'original manifest owns copied record '+key)
    need(protocol['primary']==['raw_untrimmed','NFC','characters_without_whitespace'],'fixed raw primary')
    need(protocol['written']==['U']+APP and protocol['application']==APP,'complete document boundary')
    validate_inputs(data)
    return data

def validate_inputs(d):
    p=d['policy'];a=d['counts'];i=d['recount'];v=d['review'];b=d['boundary']
    need(v['status']=='ACCEPTED_UNCHANGED_INPUTS'and v['author_manifest']['sha256']==PINS['input_manifest'],'distinct accepted input boundary')
    need(v['reviewer']=='enumeration_volume'and v['author']=='enumeration_review','distinct roles')
    need(p['source_id']=='L073'and p['original_manuscripts']==1,'one exact source')
    need((p['source_clauses'],p['physical_source_rows'],p['rank_two_classes'],p['rank_three_classes'])==(14,431,81,431),'corrected complete contract')
    need(p['variants']==VARIANTS and p['normalizations']==FORMS and p['units']==UNITS,'fixed thirty coordinates')
    need(list(a['documents'])==DOCS and [a['documents'][k]['pages']for k in DOCS]==[9,2,5,10,9,11],'all46 complete PDF pages')
    need(a['documents']==i['document_counts'],'independent complete document recount')
    need(list(a['raw_files'])==GROUPS,'four whole raw inventory groups')
    need(p['application_document_keys']==APP,'all24 application pages')
    need(p['whole_common_paper_charged']and p['no_old_umbrella_or_other_application_premise']and p['no_L095_special_group_theorem']and not p['cross_topic_discount'],'complete common closure')
    need(p['no_complete_predecessor_recovery']and p['historical_download_not_used'] is True,'historical limits')
    need(p['formal_declarations']==0 and p['formal']==[],'no formal credit')
    need(p['unknown_costs']==UNKNOWN and a['unknown_costs']==UNKNOWN,'unknown costs null')
    need(a['ratio']is None and p['ratio']is None,'no imported factor')
    for kind,count,bytecount in [('programs',7,34695),('required_raw_data',2,83965),('drivers',3,20542),('generated_outputs',10,1567120)]:
        files=a['raw_files'][kind];need(len(files)==count and sum(x['bytes']for x in files.values())==bytecount,'complete '+kind)
        need(set(files)=={x['path']for x in p[kind]},'policy/raw roster '+kind)
        for path,row in files.items():
            other=i['raw_counts'][kind][path]
            need(all(row[k]==other[k]for k in ['bytes','sha256','metrics']),'independent raw count '+path)
    program=list(a['raw_files']['programs']);data=list(a['raw_files']['required_raw_data'])
    need(b['written']==dict(source_documents=['L073'],replacement_documents=['U']+APP,required_raw_files=[]),'complete written boundary')
    need(b['computation_printed']==dict(source_documents=['L073'],replacement_documents=['U']+APP+['CODE'],required_raw_files=data),'mandatory data with printed code')
    need(b['computation_raw']==dict(source_documents=['L073'],replacement_documents=['U']+APP,required_raw_files=program+data),'mandatory data with whole raw code')
    need(b['conditional']['application_documents']==APP and b['conditional']['prepaid_common_documents']==['U']and b['conditional']['additional_prepaid_raw_data']==data,'conditional complete acquisition')
    need(d['modular_acceptance']['expected_manifest_sha256']=='dba5b09e539f6149ca16f251c28d1bb5e31354202041e35035e29a0333304f0e','distinct modular acceptance')

def derive_row(v,f,u,c,raw):
    app=sum(c[k]for k in APP);w=c['U']+app;data=raw['required_raw_data'];s=c['L073'];printed=w+c['CODE']+data;programraw=w+raw['programs']+data
    return dict(variant=v,normalization=f,unit=u,costs=c,raw_costs=raw,
        totals=dict(source=s,common=c['U'],applications=app,written=w,including_printed_programs_and_data=printed,including_raw_programs_and_data=programraw),
        comparisons=dict(written=fraction(s,w),including_printed_programs_and_data=fraction(s,printed),including_raw_programs_and_data=fraction(s,programraw),conditional_application=fraction(s,app)),
        conditional_acquisition=dict(whole_common=['U'],whole_application=APP,common_cost=c['U'],printed_program_cost=c['CODE'],raw_program_cost=raw['programs'],mandatory_raw_data_cost=data,printed_upfront=c['U']+c['CODE']+data,raw_upfront=c['U']+raw['programs']+data,local_application_cost=app,unknown_retained_costs_remain=True))

def calculate(root=ROOT):
    d=load(root);a=d['counts'];p=d['policy'];rows=[]
    for v in VARIANTS:
        for f in FORMS:
            for u in UNITS:
                c={k:a['documents'][k]['metrics'][v][f][u]for k in DOCS}
                raw={k:sum(x['metrics'][f][u]for x in a['raw_files'][k].values())for k in GROUPS}
                rows.append(derive_row(v,f,u,c,raw))
    inventory={kind:[dict(path=path,bytes=x['bytes'],sha256=x['sha256'],role=x['role'])for path,x in files.items()]for kind,files in a['raw_files'].items()}
    result=dict(status='AUTHOR_NUMERICAL_CANDIDATE_PENDING_DISTINCT_ROOT_REVIEW',topic='MathieuCensus',title='Complete Mathieu geometry census',source_ids=['L073'],source_title='Rank three residually connected geometries for M22, revisited',source_authors=['Dimitri Leemans','Peter Rowley'],
        input_manifests=PINS,source_clauses=14,source_rows=431,rank_two_classes=81,rank_three_classes=431,coordinate_count=30,exact_fraction_count=120,combined_fractions=90,conditional_fractions=30,
        whole_documents=DOCS,physical_pages=[9,2,5,10,9,11],coordinates=rows,primary=rows[2],raw_inventory=inventory,
        boundary=dict(written_documents=['U']+APP,application_documents=APP,whole_common_once=True,whole_application_pages=24,whole_programs=7,mandatory_data_files=2,mandatory_data_bytes=83965,programs_bytes=34695,programs_are_required_mathematical_inputs=True,
            printed_and_raw_alternatives=True,data_paid_in_both_computational_routes=True,separate_drivers=3,separate_driver_bytes=20542,separate_generated_outputs=10,separate_output_bytes=1567120,formal_files=0,formal_declarations=0,unknown_costs=UNKNOWN,
            printed_code_is_not_printed_data_substitute=True,no_cross_topic_discount=True,no_free_old_umbrella=True,no_L095_special_theorem=True,no_unavailable_geo_identities_claimed=True,predecessor_is_retained_not_new_original=True,
            statement='Corrected complete 81 rank-two and 431 rank-three classes, with all 431 literal source-row dispositions; not unavailable historical geo[] identities.',
            conditional='After entire common paper, one whole seven-program representation, both complete raw JSON files and retained premises; all24 local pages remain charged.',
            interpretation='Complete-document representation lengths, not minimum proof complexity or total effort. The full retained proof, graphics and catalogue construction costs are unknown.',retained_inputs=p['retained_theorems'],retained_notation_source=p['retained_notation_source'],external_computational_inputs=p['external_computational_inputs']),
        author_role='enumeration_review authored the arithmetic and earlier science/modular/input packets. Distinct root scientific/modular acceptance and enumeration_volume input acceptance are reused. This arithmetic/reader awaits distinct root review.',new_source_credit=0,new_question_credit=0,new_formal_credit=0,primary_material_exported=False)
    validate_result(result)
    return result

def validate_result(r):
    need(len(r['coordinates'])==30 and {(x['variant'],x['normalization'],x['unit'])for x in r['coordinates']}=={(v,f,u)for v in VARIANTS for f in FORMS for u in UNITS},'complete unique coordinate set')
    for x in r['coordinates']:
        need(list(x['costs'])==DOCS and list(x['raw_costs'])==GROUPS,'all document/raw components')
        expected=derive_row(x['variant'],x['normalization'],x['unit'],x['costs'],x['raw_costs']);need(x==expected,'full denominator/fraction/acquisition arithmetic')
    need(r['primary']==r['coordinates'][2]and(r['primary']['variant'],r['primary']['normalization'],r['primary']['unit'])==('raw_untrimmed','NFC','characters_without_whitespace'),'fixed raw primary')
    need((r['coordinate_count'],r['exact_fraction_count'],r['combined_fractions'],r['conditional_fractions'])==(30,120,90,30),'summary counts')
    b=r['boundary'];need(b['written_documents']==['U']+APP and b['application_documents']==APP and b['whole_common_once']and b['whole_application_pages']==24,'full common/application boundary')
    for k,v in dict(whole_programs=7,mandatory_data_files=2,mandatory_data_bytes=83965,programs_bytes=34695,separate_drivers=3,separate_driver_bytes=20542,separate_generated_outputs=10,separate_output_bytes=1567120,formal_files=0,formal_declarations=0).items():need(b[k]==v,'inventory '+k)
    for k in ['programs_are_required_mathematical_inputs','printed_and_raw_alternatives','data_paid_in_both_computational_routes','printed_code_is_not_printed_data_substitute','no_cross_topic_discount','no_free_old_umbrella','no_L095_special_theorem','no_unavailable_geo_identities_claimed','predecessor_is_retained_not_new_original']:need(b[k]is True,'scope '+k)
    need(b['unknown_costs']==UNKNOWN,'unknown costs null')
    need(r['whole_documents']==DOCS and r['physical_pages']==[9,2,5,10,9,11],'complete pages')
    need((r['source_clauses'],r['source_rows'],r['rank_two_classes'],r['rank_three_classes'])==(14,431,81,431),'corrected source scope')
    need(all(r[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'zero new credit')
