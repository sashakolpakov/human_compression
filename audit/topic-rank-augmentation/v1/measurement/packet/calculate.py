"""Exact complete-document arithmetic; no extraction or scientific execution."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
import json,hashlib
ROOT=Path(__file__).resolve().parent
PINS={'input_manifest':'fb6b56fa264b35faec3ac8151023cf5ad083d25e5e9eed0ffce68f5e0ce9e439','review_manifest':'32dae3ac7ef573d886c774f513136d7e29ebd3e7e119a9761e6ab7a50e1c1588'}
VARIANTS=['raw_untrimmed','raw_selected','calibrated_selected'];FORMS=['NFC','NFKC']
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
DOCS=['L020','U','A1','COUNTER','CODE'];APP=['A1','COUNTER'];GROUPS=['programs','operational_drivers','formal_files']
UNKNOWN={k:None for k in ['full_retained_classical_proofs','complete_runtime_implementation','historical_software','graphics_and_layout','full_formalization']}
def need(x,m):
 if not x:raise ValueError(m)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fraction(n,d):
 need(type(n)is int and type(d)is int and n>0 and d>0,'positive integer lengths');f=Fraction(n,d)
 with localcontext()as ctx:ctx.prec=50;decimal=f'{Decimal(n)/Decimal(d):.12f}'
 return dict(numerator=n,denominator=d,reduced_numerator=f.numerator,reduced_denominator=f.denominator,decimal=decimal)
def load(root=ROOT):
 p=read(root/'protocol.json');data={}
 for r in p['inputs']:
  rel=Path(r['path']);need(not rel.is_absolute()and '..'not in rel.parts,'local input path');f=root/rel;need(f.stat().st_size==r['bytes']and sha(f)==r['sha256'],'exact selected evidence '+r['key']);data[r['key']]=read(f)
 for k,pin in PINS.items():need(sha(root/'inputs'/(k+'.json'))==pin,'accepted manifest pin')
 for key,rows in [('input_manifest',{'policy':'policy.json','counts':'author_counts.json','input_protocol':'protocol.json'}),('review_manifest',{'review':'review.json','recount':'recount.json'})]:
  exports={r['path']:r for r in data[key]['exports']}
  for k,path in rows.items():
   f=root/'inputs'/(k+'.json');r=exports[path];need(r['bytes']==f.stat().st_size and r['sha256']==sha(f),'manifest owns selected evidence '+k)
 need(p['primary']==['raw_untrimmed','NFC','characters_without_whitespace']and p['written']==['U']+APP and p['application']==APP,'fixed numerical boundary')
 need(p['alternate_not_additive']and p['whole_programs_acquired_for_conditional']and not p['independent_numerical_acceptance'],'alternative representation and review scope')
 validate_inputs(data);return data

def validate_inputs(d):
 p=d['policy'];a=d['counts'];i=d['recount'];v=d['review']
 need(v['status']=='ACCEPTED_UNCHANGED_DISTINCT_L020_MEASUREMENT_INPUTS'and v['author_manifest_sha256']==PINS['input_manifest'],'distinct input acceptance')
 need(p['source_ids']==['L020']and p['original_count']==1 and p['source_dispositions']==19,'one corrected principal source')
 need(p['variants']==VARIANTS and p['normalizations']==FORMS and p['units']==UNITS,'all thirty coordinates')
 need(list(a['documents'])==DOCS and [a['documents'][k]['pages']for k in DOCS]==[19,5,3,3,3],'all thirty-three physical pages')
 need(p['whole_common']==['U']and p['written_documents']==['U']+APP and p['applications']=={'L020':APP},'whole required local counterproof')
 need(not p['cross_topic_discount']and not p['old_Topic_B_common_free_premise'],'no free older common theory')
 need(p['old_two_page_program_appendix']=='replaced, not added','whole updated program appendix')
 need(p['formal_declarations']==15 and p['unknown_costs']==UNKNOWN and a['ratio']is None and p['ratio']is None,'scoped evidence and unknowns')
 for k,x in a['documents'].items():need(x['metrics']==i['documents'][k]['metrics']and x['pdf_sha256']==i['documents'][k]['pdf_sha256'],'independent PDF counts '+k)
 for kind,count,bytes_ in [('programs',3,11533),('operational_drivers',3,15947),('formal_files',2,6855)]:
  files=a['raw_files'][kind];need(len(files)==count and sum(x['bytes']for x in files.values())==bytes_,'complete raw '+kind);need(set(files)=={x['path']for x in p[kind]},'whole file roster')
  for path,x in files.items():need(all(x[k]==i['raw_files'][kind][path][k]for k in ['bytes','sha256','metrics']),'independent raw counts '+path)
 need([x['logical_role']for x in p['programs']]==['required_finite_certificates_for_three_source_examples','bounded_validation_not_uniform_premise','transparent_S18_certificate_supporting_complete_written_proof'],'three distinct program roles')

def derive_row(v,f,u,c,raw):
 app=sum(c[k]for k in APP);w=c['U']+app;s=c['L020']
 return dict(variant=v,normalization=f,unit=u,costs=c,raw_costs=raw,totals=dict(source=s,common=c['U'],applications=app,written=w,with_printed_programs=w+c['CODE'],with_raw_programs=w+raw['programs']),comparisons=dict(written=fraction(s,w),including_printed_programs=fraction(s,w+c['CODE']),including_raw_programs=fraction(s,w+raw['programs']),conditional_application=fraction(s,app)),conditional_acquisition=dict(whole_common=['U'],whole_application=APP,common_cost=c['U'],printed_program_cost=c['CODE'],raw_program_cost=raw['programs'],printed_upfront=c['U']+c['CODE'],raw_upfront=c['U']+raw['programs'],local_application_cost=app,unknown_retained_costs_remain=True))
def calculate(root=ROOT):
 d=load(root);a=d['counts'];p=d['policy'];rows=[]
 for v in VARIANTS:
  for f in FORMS:
   for u in UNITS:
    c={k:a['documents'][k]['metrics'][v][f][u]for k in DOCS};raw={k:sum(x['metrics'][f][u]for x in a['raw_files'][k].values())for k in GROUPS};rows.append(derive_row(v,f,u,c,raw))
 inventory={kind:[dict(path=x['path'],bytes=x['bytes'],sha256=x['sha256'],role=x.get('logical_role',x.get('role','operational_driver')))for x in p[kind]]for kind in GROUPS}
 r=dict(status='AUTHOR_NUMERICAL_CANDIDATE_PENDING_DISTINCT_ROOT_REVIEW',topic='RankAugmentation',source_ids=['L020'],source_title='A rank augmentation theorem for rank 3 string C-group representations of the symmetric groups',source_authors=['Julie De Saedeleer','Dimitri Leemans','Jessica Mulpas'],source_edition='arXiv:2212.12563v1, 23 December 2022',source_dispositions=19,input_manifests=PINS,coordinate_count=30,exact_fraction_count=120,combined_fractions=90,conditional_fractions=30,whole_documents=DOCS,physical_pages=[19,5,3,3,3],coordinates=rows,primary=rows[2],raw_inventory=inventory,boundary=dict(written_documents=['U']+APP,application_documents=APP,whole_common_once=True,whole_application_pages=6,whole_programs=3,program_bytes=11533,program_roles=[x['logical_role']for x in p['programs']],separate_drivers=3,separate_driver_bytes=15947,separate_formal_files=2,separate_formal_bytes=6855,partial_Lean_declarations=15,whole_source_formalized=False,printed_raw_alternatives=True,old_program_appendix_replaced=True,no_free_old_B=True,no_cross_topic_discount=True,unknown_costs=UNKNOWN,source_correction=p['source_correction'],retained_intro_Table1=p['retained_intro_Table1'],retained_limits=p['background_qualifications'],conditional='After the whole five-page common paper, all three whole declared programs and retained premises; both three-page local papers remain charged.',interpretation='Lengths of complete available texts, not minimum proof complexity, research effort or a pooled cross-topic factor.'),author_role='enumeration_review authors this numerical packet and previously independently reviewed inputs authored by enumeration_volume. The distinct root scientific reviews are reused. Numerical acceptance must come from a different reviewer.',new_source_credit=0,new_question_credit=0,new_formal_credit=0,primary_material_exported=False)
 validate_result(r);return r

def validate_result(r):
 need(len(r['coordinates'])==30 and {(x['variant'],x['normalization'],x['unit'])for x in r['coordinates']}=={(v,f,u)for v in VARIANTS for f in FORMS for u in UNITS},'unique complete coordinate set')
 for x in r['coordinates']:
  need(list(x['costs'])==DOCS and list(x['raw_costs'])==GROUPS,'all components');need(x==derive_row(x['variant'],x['normalization'],x['unit'],x['costs'],x['raw_costs']),'whole arithmetic and acquisition')
 need(r['primary']==r['coordinates'][2]and(r['primary']['variant'],r['primary']['normalization'],r['primary']['unit'])==('raw_untrimmed','NFC','characters_without_whitespace'),'fixed raw primary')
 need((r['coordinate_count'],r['exact_fraction_count'],r['combined_fractions'],r['conditional_fractions'])==(30,120,90,30),'summary counts')
 b=r['boundary'];need(b['written_documents']==['U']+APP and b['application_documents']==APP and b['whole_common_once']and b['whole_application_pages']==6,'whole application and counterproof')
 for k,v in dict(whole_programs=3,program_bytes=11533,separate_drivers=3,separate_driver_bytes=15947,separate_formal_files=2,separate_formal_bytes=6855,partial_Lean_declarations=15,whole_source_formalized=False).items():need(b[k]==v,'inventory '+k)
 need(b['program_roles']==['required_finite_certificates_for_three_source_examples','bounded_validation_not_uniform_premise','transparent_S18_certificate_supporting_complete_written_proof'],'exact computational roles')
 for k in ['printed_raw_alternatives','old_program_appendix_replaced','no_free_old_B','no_cross_topic_discount']:need(b[k]is True,'scope '+k)
 need(b['unknown_costs']==UNKNOWN and 'case3 false' in b['source_correction']and 'not regenerated' in b['retained_intro_Table1'],'retained/corrected scope')
 need(r['whole_documents']==DOCS and r['physical_pages']==[19,5,3,3,3]and r['source_dispositions']==19 and r['source_ids']==['L020'],'one full source with nineteen dispositions')
 need(all(r[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'no numerical credit')
