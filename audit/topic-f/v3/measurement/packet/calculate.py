#!/usr/bin/env python3
"""Exact arithmetic on independently accepted complete expanded Topic F counts."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
import hashlib,json
ROOT=Path(__file__).resolve().parent
PINS={'input_manifest':'4835714ae78f8069a7b53f6181b770a2b40286eadf8a2c53cc652b96c4ccea0a','review_manifest':'caf7bb421e325234f2565bece89032d44ee8781c5aea18b09c4ac4bc3fae99c5'}
VARIANTS=['raw_untrimmed','raw_selected','calibrated_selected'];FORMS=['NFC','NFKC']
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
SOURCES=['L014','L007'];APP=['A1','A2'];DOCS=SOURCES+['U']+APP+['CODE'];GROUPS=['programs','operational_drivers','formal_files']
UNKNOWN={k:None for k in ['full_retained_CP_proof','full_Huppert_Schmidt_proofs','classical_external_proofs','source_graphics_and_formula_layout','complete_runtime_and_external_software','operational_engineering']}
def need(x,m):
 if not x:raise ValueError(m)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fraction(n,d):
 need(type(n)is int and type(d)is int and n>0 and d>0,'positive integer costs');f=Fraction(n,d)
 with localcontext()as c:c.prec=50;decimal=f'{Decimal(n)/Decimal(d):.12f}'
 return dict(numerator=n,denominator=d,reduced_numerator=f.numerator,reduced_denominator=f.denominator,decimal=decimal)
def load(root=ROOT):
 protocol=read(root/'protocol.json');data={}
 for row in protocol['inputs']:
  p=Path(row['path']);need(not p.is_absolute()and '..'not in p.parts,'local relative evidence');p=root/p
  need(p.stat().st_size==row['bytes']and sha(p)==row['sha256'],'exact copied evidence '+row['key']);data[row['key']]=read(p)
 for k,pin in PINS.items():need(sha(root/'inputs'/(k+'.json'))==pin,'accepted manifest pin '+k)
 for row in protocol['inputs']:
  if row['original_export']=='manifest.json':continue
  entries={e['path']:e for e in data[row['original_manifest']]['exports']};e=entries[row['original_export']]
  need((e['bytes'],e['sha256'])==(row['bytes'],row['sha256']),'original manifest owns evidence '+row['key'])
 need(protocol['primary']==['raw_untrimmed','NFC','characters_without_whitespace'],'fixed raw primary')
 need(protocol['source']==SOURCES and protocol['written']==['U']+APP and protocol['conditional']==dict(zip(SOURCES,APP)),'full document boundary')
 need(protocol['all_programs_validation']and protocol['programs_are_not_uniform_proof_premises']and protocol['no_cross_topic_discount'],'program roles and full costs')
 validate_inputs(data);validate_correction(root,protocol,data);return data

def validate_inputs(d):
 p=d['policy'];a=d['counts'];i=d['recount'];v=d['review'];b=d['boundary']
 need(v['status']=='ROOT_ACCEPTED_COMPLETE_EXPANDED_TOPIC_F_INPUTS'and v['input_manifest_sha256']==PINS['input_manifest'],'distinct accepted inputs')
 need(v['factors_now_permitted_for_exact_reviewed_inputs']is True and v['scientific_adoption_manifest_sha256']=='2d460b6a74eeef341b8bcd9a4153168b97e2e02cef56fcf4556562e20a6562b9','review authority and science scope')
 need(p['source_ids']==SOURCES and p['original_count']==2 and(p['source_dispositions'],p['inherited_L014_rows'],p['L007_rows'])==(63,25,38),'complete two-original contract')
 need(p['variants']==VARIANTS and p['normalizations']==FORMS and p['units']==UNITS,'thirty fixed coordinates')
 need(p['primary_coordinate']==dict(variant='raw_untrimmed',normalization='NFC',unit=UNITS[2]),'preselected primary')
 need(list(a['documents'])==DOCS and[a['documents'][k]['pages']for k in DOCS]==[12,22,7,5,6,9],'61 complete PDF pages')
 need(a['documents']==i['documents']and a['raw_files']==i['raw_files'],'independent340-cell recount exact equality')
 need(p['written_documents']==['U']+APP and p['applications']=={k:[v]for k,v in zip(SOURCES,APP)}and p['whole_common']==['U'],'whole common and both applications')
 need(list(a['raw_files'])==GROUPS,'all three whole raw inventories')
 for kind,count,bytecount in [('programs',9,25501),('operational_drivers',4,33222),('formal_files',3,9398)]:
  files=a['raw_files'][kind];need(len(files)==count and sum(x['bytes']for x in files.values())==bytecount,'complete '+kind)
  need(set(files)=={x['path']for x in p[kind]}and all(x['whole_file']for x in p[kind]),'whole policy roster '+kind)
  for row in p[kind]:need((row['bytes'],row['sha256'])==(files[row['path']]['bytes'],files[row['path']]['sha256']),'exact raw binding '+row['path'])
 need(all(x['logical_role']=='validation_not_uniform_proof_premise'for x in p['programs']),'all9 validation only')
 need((p['formal_declarations'],p['new_formal_declarations'])==(12,3)and all(not x['source_specific_instance']for x in p['formal_files']),'partial12-declaration scope')
 need(not p['cross_topic_discount']and not p['old_Topic_F_common_free_premise'],'no inherited discount')
 need(p['unknown_costs']==UNKNOWN and a['unknown_costs']==UNKNOWN and v['retained_unknown_costs']==UNKNOWN,'unknown costs null')
 need(a['ratio']is None and p['ratio']is None and not v['factors_computed'],'input review is not arithmetic acceptance')
 need(b['all_original_pages']==34 and b['all_replacement_pages']==27 and b['all_rows']==63 and b['whole_replacements']==['U','A1','A2','CODE'],'complete source boundary')
 need(v['all_nine_declared_programs_acquired_for_conditional']and not v['full_source_formalized'],'conditional and formal boundaries')

CORRECTION_PINS={
 'previous_manifest.json':'855ea109031cf316640f2f2d8263d50227a4ca2c98d65b745c8d8bb8b0869bcb',
 'source_listing_review_manifest.json':'d53e51227c61b70064ecf8d5a6b6cf560ce484961f82ff2ef7a9d7e2c2e926f5',
 'final_policy_review.json':'f7afd332147cac53f3a6ae44c729e8fcf9a6e09396c270dda37719f3f60df337'}
COMPARISONS=['written','conditional_L014','conditional_L007']
def validate_correction(root,protocol,data):
 rows=protocol['correction_evidence']
 need(len(rows)==10 and len({x['path']for x in rows})==10,'complete correction evidence')
 for x in rows:
  p=Path(x['path']);need(not p.is_absolute()and '..'not in p.parts,'relative correction evidence')
  need((root/p).stat().st_size==x['bytes']and sha(root/p)==x['sha256'],'exact correction evidence '+str(p))
 for name,pin in CORRECTION_PINS.items():need(sha(root/'correction_evidence'/name)==pin,'fixed correction pin '+name)
 e=root/'correction_evidence';prior=read(e/'previous_manifest.json');entry=next(x for x in prior['exports']if x['path']=='results.json');need(sha(e/'previous_results.json')==entry['sha256']and(e/'previous_results.json').stat().st_size==entry['bytes'],'immutable predecessor result')
 m=read(e/'source_listing_review_manifest.json')
 for name in ['review.json','bindings.json']:
  z=next(x for x in m['exports']if x['path']==name);f=e/('source_listing_'+name);need(sha(f)==z['sha256']and f.stat().st_size==z['bytes'],'prior listing review owns evidence')
 final=read(e/'final_policy_review.json');need(final['status']=='ACCEPTED_FINAL_SYMMETRIC_POLICY_PRESENTATION','accepted policy presentation')
 for x in final['files']:
  f=e/Path(x['path']).name;need(sha(f)==x['sha256']and f.stat().st_size==x['bytes'],'four reviewed policy files')
 policy=read(e/'policy.json');need(policy['current_measurement']['symmetric_validation_inclusive_factors']is None,'no symmetric software factor available')
 need(protocol['public_policy_commit']=='eddda09725a0738bb5dc77489cb06d6221736714','published policy commit')
 need(protocol['allowed_comparisons']==COMPARISONS,'only symmetric manuscript comparisons')
 need(protocol['conditional_prepaid']==['whole U','actual retained mathematical premises whose full costs remain unknown'],'validation not required for conditional comparison')
 # The earlier review's all-program-prepayment field is historical metadata,
 # superseded here by the user's current policy; its accepted counts are unchanged.

def derive_row(v,f,u,c,raw):
 s=sum(c[k]for k in SOURCES);app=sum(c[k]for k in APP);w=c['U']+app
 return dict(variant=v,normalization=f,unit=u,costs=c,raw_costs=raw,
  totals=dict(source=s,common=c['U'],applications=app,written=w),
  comparisons=dict(written=fraction(s,w),conditional_L014=fraction(c['L014'],c['A1']),conditional_L007=fraction(c['L007'],c['A2'])),
  optional_validation_inventory=dict(printed=c['CODE'],raw_alternative=raw['programs'],representations_alternative=True,source_software_cost=None,symmetric_software_inclusive_factor=None,used_as_uniform_proof_premise=False),
  conditional_acquisition=dict(whole_common=['U'],common_cost=c['U'],local_application_costs={k:c[a]for k,a in zip(SOURCES,APP)},unknown_retained_costs_remain=True,optional_validation_required=False))

def calculate(root=ROOT):
 d=load(root);a=d['counts'];p=d['policy'];rows=[]
 for v in VARIANTS:
  for f in FORMS:
   for u in UNITS:
    c={k:a['documents'][k]['metrics'][v][f][u]for k in DOCS};raw={k:sum(x['metrics'][f][u]for x in a['raw_files'][k].values())for k in GROUPS};rows.append(derive_row(v,f,u,c,raw))
 result=dict(status='AUTHOR_SYMMETRIC_NUMERICAL_CANDIDATE_PENDING_DISTINCT_ROOT_REVIEW',topic='OddKernels',title='Odd kernels and cyclotomic constructions',source_ids=SOURCES,
 source_titles={'L014':'String C-groups of order 4p^m','L007':'Chiral 3-polytopes of order 2p^m'},input_manifests=PINS,source_dispositions=63,coordinate_count=30,exact_fraction_count=90,combined_fractions=30,conditional_fractions=60,whole_documents=DOCS,physical_pages=[12,22,7,5,6,9],coordinates=rows,primary=rows[2],raw_inventory={k:p[k]for k in GROUPS},
 boundary=dict(written_documents=['U']+APP,application_map=dict(zip(SOURCES,APP)),whole_common_once=True,whole_programs=9,programs_bytes=25501,validation_programs=9,uniform_finite_premise_programs=0,printed_and_raw_alternatives=True,separate_drivers=4,separate_driver_bytes=33222,formal_files=3,separate_formal_bytes=9398,formal_declarations=12,reused_declarations=9,new_generic_declarations=3,full_source_formalized=False,no_source_specific_Lean_instance=True,no_cross_topic_discount=True,no_free_inherited_common=True,conditional_prepays_whole_common_and_actual_retained_premises=True,optional_validation_required_for_conditional=False,source_validation_software_cost=None,symmetric_software_inclusive_factor=None,unknown_costs=UNKNOWN,source_corrections=d['boundary'],interpretation='Complete manuscript representation lengths, not minimal proof complexity or total effort. Optional validation excluded from both sides; source and replacement manuscript listings screened at the declared bounded scope. All nine complete validation files are inventoried separately, not required proof inputs.',old_L014_selected_headline=25115,new_L014_raw_primary=25574,previous_one_source_edition_preserved=True),
 policy_correction=dict(public_commit='eddda09725a0738bb5dc77489cb06d6221736714',previous_manifest_sha256=CORRECTION_PINS['previous_manifest.json'],previous_numeric_packet_remains_immutable=True,all_document_and_raw_costs_unchanged=True,all_written_and_conditional_fractions_unchanged=True,removed_asymmetric_fractions=60,embedded_optional_validation_listings_found=False,manuscript_cuts_made=False,listing_basis='Prior complete proof/source reading plus bound exact-source scan, not a claim about all nineteen historical topics.'),
 author_role='enumeration_review authored both this additive arithmetic and the predecessor. Root independently accepted inputs and science; bounded source-listing audit discloses this role. This is author evidence, not independent numerical acceptance.',new_source_credit=0,new_question_credit=0,new_formal_credit=0,primary_material_exported=False)
 validate_result(result);prior=read(root/'correction_evidence/previous_results.json');check_preservation(result,prior);return result

def check_preservation(r,old):
 need(len(old['coordinates'])==30,'all predecessor coordinates')
 for x,y in zip(r['coordinates'],old['coordinates']):
  need(all(x[k]==y[k]for k in ['variant','normalization','unit','costs','raw_costs']),'all original 270 component cells unchanged')
  need(all(x['comparisons'][k]==y['comparisons'][k]for k in COMPARISONS),'all90 preserved exact fractions')
 need(r['raw_inventory']==old['raw_inventory'],'all16 whole raw file bindings unchanged')
 need(r['boundary']['source_corrections']==old['boundary']['source_corrections'],'all original source qualifications unchanged')
 return dict(status='PASS',coordinates=30,component_cells_unchanged=270,whole_raw_files_unchanged=16,preserved_written_fractions=30,preserved_conditional_fractions=60,asymmetric_fractions_removed=60,source_extraction_or_science_rerun=False)

def validate_result(r):
 need(len(r['coordinates'])==30 and{(x['variant'],x['normalization'],x['unit'])for x in r['coordinates']}=={(v,f,u)for v in VARIANTS for f in FORMS for u in UNITS},'complete unique coordinates')
 for x in r['coordinates']:
  need(list(x['costs'])==DOCS and list(x['raw_costs'])==GROUPS,'all PDF/raw components');need(x==derive_row(x['variant'],x['normalization'],x['unit'],x['costs'],x['raw_costs']),'full denominator/fraction/inventory arithmetic')
 need(r['primary']==r['coordinates'][2],'fixed raw primary')
 need((r['coordinate_count'],r['exact_fraction_count'],r['combined_fractions'],r['conditional_fractions'])==(30,90,30,60),'summary counts')
 b=r['boundary'];need(b['written_documents']==['U']+APP and b['application_map']==dict(zip(SOURCES,APP))and b['whole_common_once'],'whole common and both applications')
 for k,v in dict(whole_programs=9,programs_bytes=25501,validation_programs=9,uniform_finite_premise_programs=0,separate_drivers=4,separate_driver_bytes=33222,formal_files=3,separate_formal_bytes=9398,formal_declarations=12,reused_declarations=9,new_generic_declarations=3,old_L014_selected_headline=25115,new_L014_raw_primary=25574).items():need(b[k]==v,'inventory/scope '+k)
 for k in ['printed_and_raw_alternatives','no_source_specific_Lean_instance','no_cross_topic_discount','no_free_inherited_common','conditional_prepays_whole_common_and_actual_retained_premises','previous_one_source_edition_preserved']:need(b[k]is True,'scope '+k)
 need(b['optional_validation_required_for_conditional']is False and b['source_validation_software_cost']is None and b['symmetric_software_inclusive_factor']is None,'symmetric validation policy')
 need(b['full_source_formalized']is False and b['unknown_costs']==UNKNOWN,'partial formal and unknown costs')
 need(r['source_ids']==SOURCES and r['source_dispositions']==63 and r['whole_documents']==DOCS and r['physical_pages']==[12,22,7,5,6,9],'complete exact source/document scope')
 need(all(r[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit'])and r['primary_material_exported']is False,'no new credit or primary exports')
 need(r['policy_correction']['removed_asymmetric_fractions']==60 and r['policy_correction']['manuscript_cuts_made']is False and r['policy_correction']['embedded_optional_validation_listings_found']is False,'exact bounded policy correction')
