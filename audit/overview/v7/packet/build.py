#!/usr/bin/env python3
"""Append two accepted censuses while preserving all fifteen admitted records."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
import argparse,copy,hashlib,json,os,subprocess
import plotting,reader
ROOT=Path(__file__).resolve().parent
PINS={'LocallyProjective':('0d548c296855637641592e539c4401895ac38c4c094eaf6f6aa8923f57e058a4','2f9ded604bd5ca6b4b9b882c5b694124eacb653102b9f44e823f04ac731c519a'),'MathieuCensus':('1f7256e911cc3bf0797672e4237a7ef8fe6e6b24cbcca30d13142c82c7dc2d36','b163f3c5bf37ef0406016be81e036c1b7f52a7d5be3245d43f2586081ca88307')}
def need(x,m):
 if not x:raise ValueError('OVERVIEW40_REJECT: '+m)
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def load(p):return json.loads(p.read_text())
def ratio(n,d):
 with localcontext() as c:c.prec=50;v=f'{Decimal(n)/Decimal(d):.12f}'
 return dict(numerator=n,denominator=d,exact_fraction=str(Fraction(n,d)),decimal=v)
def accepted_fraction(x,n,d):
 need(x['numerator']==n and x['denominator']==d and Fraction(x['reduced_numerator'],x['reduced_denominator'])==Fraction(n,d),'accepted rational')
 if 'exact_fraction'in x:need(x['exact_fraction']==str(Fraction(n,d)),'accepted exact fraction')
 if 'decimal'in x:need(x['decimal']==ratio(n,d)['decimal'],'accepted exact display')
 if 'factor'in x:need(abs(Decimal(str(x['factor']))-Decimal(n)/Decimal(d))<Decimal('0.000000000002'),'accepted float')

def load_inputs(public=None):
 p=load(ROOT/'protocol.json');data={}
 for k,r in p['bindings'].items():
  path=Path(r['local']);need(not path.is_absolute()and '..'not in path.parts,'relative local evidence');b=(ROOT/path).read_bytes();need(len(b)==r['bytes']and sha(b)==r['sha256'],'bound input '+k);data[k]=json.loads(b)
  if public and r['role']=='committed_baseline':
   rel=Path(r['path']).relative_to('/Users/sasha/medusa/math_compression');need(subprocess.check_output(['git','show',p['admitted_baseline_commit']+':'+str(rel)],cwd=public)==b,'exact committed baseline')
 need(data['previous_admission']['status']=='ROOT_ADMITTED_CONSOLIDATED_NUMERICAL_OVERVIEW37','admitted baseline37')
 for k in ['previous_results','previous_manifest','previous_review']:
  r=p['bindings'][k];rel=str(Path(r['path']).relative_to('/Users/sasha/medusa/math_compression'));need(any(x['path']==rel and x['sha256']==r['sha256']for x in data['previous_admission']['artifacts']),'baseline admission owns '+k)
 for key,(author,review)in PINS.items():
  need(p['bindings'][key+'_manifest']['sha256']==author and p['bindings'][key+'_review_manifest']['sha256']==review==p['new_numerical_reviews'][key],'accepted manifests '+key)
  for suffix in ['results','protocol']:
   need(any(x['path']==suffix+'.json'and x['sha256']==p['bindings'][key+'_'+suffix]['sha256']for x in data[key+'_manifest']['exports']),'numerical manifest owns '+suffix)
  need(any(x['path']=='review.json'and x['sha256']==p['bindings'][key+'_review']['sha256']for x in data[key+'_review_manifest']['exports']),'root manifest owns review')
  rr=data[key+'_review'];need(rr['author_manifest_sha256']==author,'review author pin')
  need(rr['status']==('ROOT_ACCEPTED_COMPLETE_LOCALLY_PROJECTIVE_NUMBERS'if key=='LocallyProjective'else'ROOT_ACCEPTED_COMPLETE_L073_NUMBERS'),'distinct numerical acceptance')
 lp=data['LocallyProjective_protocol'];need(lp['whole_common']==['U','TABLES']and lp['sources']==['L084','L095']and lp['primary']==['calibrated_selected','NFC','characters_without_whitespace']and lp['full_physical_pages']==40,'whole LP boundary')
 mc=data['MathieuCensus_protocol'];need(mc['written']==['U','A1','CLASSES','ROWS']and mc['application']==['A1','CLASSES','ROWS']and mc['primary']==['raw_untrimmed','NFC','characters_without_whitespace'],'whole Mathieu boundary')
 need(p['status']=='PRIVATE_OVERVIEW_CANDIDATE_FROM_DISTINCTLY_ACCEPTED_NUMBERS'and not p['new_factor_acceptance_pending'],'numbers accepted; overview pending')
 return p,data

def common_fields(key,title,ids,pairs,common,apps,code,raw,data,representation):
 source=sum(q['source_cost']for q in pairs);u=sum(common.values());a=sum(q['application_cost']for q in pairs);written=u+a
 t=dict(topic=key,title=title,source_count=len(ids),source_ids=ids,pairs=pairs,common_theory=u,common_components=common,application_components=apps,source_sum=source,applications_sum=a,written_denominator=written,printed_program_cost=code,raw_program_alternative=raw,mandatory_data_cost=data,mandatory_data_paid_in_both_program_routes=True,representation=representation,normalization='NFC',unit='characters_without_whitespace',numerical_status='distinctly_root_accepted_pending_overview_publication',numeric_origin=key+'_results/primary',written=ratio(source,written),including_printed_programs=ratio(source,written+code+data),including_raw_programs=ratio(source,written+raw+data),including_optional_validation=None,conditional_prepaid=dict(full_common=u,full_declared_printed_programs=code,mandatory_data=data,total=u+code+data),conditional_raw_alternative_prepaid=dict(full_common=u,full_declared_raw_programs=raw,mandatory_data=data,total=u+raw+data),source_admission='Scientific and numerical acceptance retained; this overview awaits distinct review.',multi_coordinate_input_retained=True)
 for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']:t[k]=None
 return t

def locally_projective(allx):
 x=allx['primary'];c=x['document_costs'];s=x['source_cost'];u=x['whole_common_cost'];a=x['application_cost'];code=x['printed_program_cost'];raw=x['raw_program_cost'];data=x['mandatory_data_cost']
 need((s,u,a,code,raw,data)==(26490,25498,11966,22695,22104,28574),'exact LP costs')
 need(c==dict(L084=2071,L095=24419,U=19533,TABLES=5965,A1=4857,A2=7109,CODE=22695),'whole LP documents')
 need(allx['complete_common_documents']==['U','TABLES']and allx['whole_common_charged_once']and allx['all_applications_charged']and not allx['sibling_application_free_premise']and not allx['cross_topic_discount'],'whole LP closure')
 for k,d in [('written_papers',u+a),('printed_programs_plus_mandatory_data',u+a+code+data),('raw_programs_plus_mandatory_data',u+a+raw+data)]:accepted_fraction(x['comparisons'][k],s,d)
 pairs=[]
 for source,app,component in [('L084','LP1','A1'),('L095','LP2','A2')]:
  accepted_fraction(x['conditional_applications'][source],c[source],c[component]);pairs.append(dict(source=source,application=app,source_cost=c[source],application_cost=c[component],source_representation='complete_PDF_calibrated_selected',conditional=ratio(c[source],c[component])))
 t=common_fields('LocallyProjective','Locally projective quotients',['L084','L095'],pairs,dict(whole_common_proof=c['U'],whole_common_tables=c['TABLES']),{'LP1':{'complete_erratum_application':c['A1']},'LP2':{'complete_parent_application':c['A2']}},code,raw,data,'calibrated_selected_pdf')
 t.update(mandatory_data_literal_bytes=39150,mandatory_data_files=1,separate_raw_inventory=dict(programs=raw,mandatory_data=data,drivers=x['operational_driver_cost_separate'],formal=0,generated_output_literal_bytes=3470182),program_roles='All six mathematical programs and whole source_tables.json are retained. Historical data is required for full145-row reconciliation, not a subgroup-enumeration premise. Three drivers and eleven generated outputs stay separately inventoried; zero Lean declarations.',scientific_boundary='Complete two-page L084 publisher erratum and15-page July2003 L095 arXiv v1;52 dispositions and145 historical rows. Unseen journal text and unavailable g.txt are not silently substituted. Source-column and correction qualifications remain.',entire_source_pages={'L084':2,'L095':15},entire_common_pages=[7,5],entire_application_pages={'LP1':2,'LP2':3},entire_program_pages=6,old_umbrella_free_premise=False)
 return t

def mathieu(allx):
 x=allx['primary'];c=x['costs'];raw=x['raw_costs'];s=c['L073'];u=c['U'];a=sum(c[k]for k in ['A1','CLASSES','ROWS']);code=c['CODE'];data=raw['required_raw_data']
 need((s,u,a,code,raw['programs'],data)==(13736,5516,35862,31244,30489,48686),'exact Mathieu costs')
 need(c==dict(L073=13736,U=5516,A1=13178,CLASSES=9480,ROWS=13204,CODE=31244),'all application companions')
 for k,d in [('written',u+a),('including_printed_programs_and_data',u+a+code+data),('including_raw_programs_and_data',u+a+raw['programs']+data),('conditional_application',a)]:accepted_fraction(x['comparisons'][k],s,d)
 need(allx['physical_pages']==[9,2,5,10,9,11]and allx['boundary']['whole_application_pages']==24 and allx['boundary']['no_unavailable_geo_identities_claimed'],'exact corrected census scope')
 q=dict(source='L073',application='MC1',source_cost=s,application_cost=a,source_representation='complete_PDF_raw_untrimmed',conditional=ratio(s,a))
 t=common_fields('MathieuCensus','Complete Mathieu geometry census',['L073'],[q],dict(whole_common=u),{'MC1':dict(main_application=c['A1'],all_class_tables=c['CLASSES'],all_source_row_dispositions=c['ROWS'])},code,raw['programs'],data,'raw_untrimmed_pdf')
 t.update(mandatory_data_literal_bytes=83965,mandatory_data_files=2,separate_raw_inventory=dict(programs=raw['programs'],mandatory_data=data,drivers=raw['drivers'],generated_outputs=raw['generated_outputs'],generated_output_literal_bytes=1567120,formal=0),program_roles='All seven required mathematical programs and both whole JSON inputs. Three auxiliary scripts and ten generated outputs stay separately inventoried; no Lean declarations. Program representations are alternatives, with full JSON in both.',scientific_boundary='Corrected complete81 rank-two and431 rank-three classes, with all431 literal source-row dispositions; not unavailable historical geo[] identities. The48-page predecessor is retained notation, not another recovered original.',entire_source_pages=9,entire_common_pages=[2],entire_application_pages={'main':5,'classes':10,'source_rows':9},entire_program_pages=11,old_umbrella_free_premise=False)
 return t

def make(data,p):
 old=data['previous_results'];r=copy.deepcopy(old);r.update(schema='programme.primary_summary.censuses40.candidate',status='AUTHOR_OVERVIEW_FROM_ACCEPTED_NUMBERS_PENDING_OVERVIEW_REVIEW',topic_count=17,original_manuscript_count=40,currently_published_measured_originals=37,proposed_measured_originals=40,pending_numerical_acceptance=[],pending_overview_review=True,admitted_baseline_commit=p['admitted_baseline_commit'],recovery_status_not_derived_from_measurement=True)
 r['topics']=copy.deepcopy(old['topics'])+[locally_projective(data['LocallyProjective_results']),mathieu(data['MathieuCensus_results'])]
 r['notes']=['All fifteen prior topic JSON objects are unchanged. New accepted numerical records add L084,L095,L073 only.','New CODE fields remain code alone. Each computational denominator additionally pays the new mandatory_data_cost; neither JSON is omitted or hidden as printed code.','LocallyProjective pays whole U and common tables. MathieuCensus pays U and all24 application pages, including both companions.','No pooled factor, cross-topic theory discount or recovery/accessibility count inference.','Prior records without a separately measured data field remain unchanged; omission is not a claim that their external data or proofs cost zero.']
 r['candidate_result_bindings']={k:p['bindings'][k+'_results']for k in PINS};r['distinct_numerical_acceptances']={k:p['bindings'][k+'_review_manifest']for k in PINS};r.pop('new_input_acceptance_manifest_sha256',None);r['old_overviews_preserved']=True
 validate(r,old);return r

def validate(r,old):
 need(r['topic_count']==len(r['topics'])==17 and r['original_manuscript_count']==40,'17 topics/40 originals')
 need(r['currently_published_measured_originals']==37 and r['proposed_measured_originals']==40 and not r['pending_numerical_acceptance']and r['pending_overview_review'],'candidate scope')
 need(r['pooled_factor']is None and not r['cross_topic_deduplication']and not r['all_registry_manuscripts_completed']and r['registry_manuscripts']==161,'no pooled/completed-corpus claim')
 need(r['topics'][:-2]==old['topics'],'all fifteen prior objects unchanged')
 need(all(r[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'zero credit')
 ids=[]
 for t in r['topics']:
  need(sum(t['common_components'].values())==t['common_theory'],'all common components')
  need(sum(q['source_cost']for q in t['pairs'])==t['source_sum']and sum(q['application_cost']for q in t['pairs'])==t['applications_sum'],'complete papers')
  need(t['source_ids']==[q['source']for q in t['pairs']]and t['source_count']==len(t['pairs']),'source roster')
  need(t['written_denominator']==t['common_theory']+t['applications_sum']and t['written']==ratio(t['source_sum'],t['written_denominator']),'written factor')
  data=t['mandatory_data_cost']if 'mandatory_data_cost'in t else 0
  for k,c in [('including_printed_programs',t['printed_program_cost']),('including_raw_programs',t['raw_program_alternative'])]:need(t[k]==(None if c is None else ratio(t['source_sum'],t['written_denominator']+c+data)),'code plus data denominator')
  for q in t['pairs']:
   ids.append(q['source']);need(q['conditional']==ratio(q['source_cost'],q['application_cost']),'exact conditional')
   if 'application_components'in t:need(sum(t['application_components'][q['application']].values())==q['application_cost'],'all application components')
  for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']:need(t[k]is None,'unknown remains null')
 need(len(ids)==len(set(ids))==40 and set(ids)=={q['source']for t in old['topics']for q in t['pairs']}|{'L084','L095','L073'},'three exact new originals')
 for t,key,expected in [(r['topics'][-2],'LocallyProjective',(26490,25498,11966,22695,22104,28574,39150,1)),(r['topics'][-1],'MathieuCensus',(13736,5516,35862,31244,30489,48686,83965,2))]:
  need(t['topic']==key,'topic identity');need(tuple(t[k]for k in ['source_sum','common_theory','applications_sum','printed_program_cost','raw_program_alternative','mandatory_data_cost','mandatory_data_literal_bytes','mandatory_data_files'])==expected,'complete new costs/data')
  need(t['mandatory_data_paid_in_both_program_routes']is True and t['old_umbrella_free_premise']is False,'all declared inputs')
  need(t['conditional_prepaid']==dict(full_common=t['common_theory'],full_declared_printed_programs=t['printed_program_cost'],mandatory_data=t['mandatory_data_cost'],total=t['common_theory']+t['printed_program_cost']+t['mandatory_data_cost']),'full printed acquisition')
  need(t['conditional_raw_alternative_prepaid']==dict(full_common=t['common_theory'],full_declared_raw_programs=t['raw_program_alternative'],mandatory_data=t['mandatory_data_cost'],total=t['common_theory']+t['raw_program_alternative']+t['mandatory_data_cost']),'full raw acquisition')
 lp,mc=r['topics'][-2:];need(lp['representation']=='calibrated_selected_pdf'and mc['representation']=='raw_untrimmed_pdf','distinct representations')
 need(lp['common_components']==dict(whole_common_proof=19533,whole_common_tables=5965)and mc['application_components']['MC1']==dict(main_application=13178,all_class_tables=9480,all_source_row_dispositions=13204),'full companion papers')
 need(lp['entire_source_pages']=={'L084':2,'L095':15}and lp['entire_common_pages']==[7,5]and lp['entire_application_pages']=={'LP1':2,'LP2':3}and lp['entire_program_pages']==6 and mc['entire_source_pages']==9 and mc['entire_common_pages']==[2]and mc['entire_application_pages']==dict(main=5,classes=10,source_rows=9)and mc['entire_program_pages']==11,'complete pages')
 need(lp['separate_raw_inventory']==dict(programs=22104,mandatory_data=28574,drivers=29370,formal=0,generated_output_literal_bytes=3470182),'LP separate inventory')
 need(mc['separate_raw_inventory']==dict(programs=30489,mandatory_data=48686,drivers=18689,generated_outputs=838566,generated_output_literal_bytes=1567120,formal=0),'Mathieu separate inventory')
 need('unavailable historical geo[] identities'in mc['scientific_boundary']and 'not another recovered original'in mc['scientific_boundary']and 'Unseen journal text'in lp['scientific_boundary'],'source qualifications')

def build(out,public=None,render=False,xelatex='xelatex'):
 need(not out.exists() and not out.is_symlink(),'fresh output');out.mkdir(parents=True);p,data=load_inputs(public);r=make(data,p);dump(out/'results.json',r)
 for name,t in plotting.csv_text(r).items():(out/name).write_text(t)
 specs={k:plotting.plot_spec(r,k) for k in ['whole_topics','conditional_1','conditional_2']};dump(out/'plot_data.json',specs)
 os.environ.setdefault('MPLCONFIGDIR',str(out/'mpl-cache'));os.environ.setdefault('XDG_CACHE_HOME',str(out/'cache'))
 for spec in specs.values():plotting.draw(spec,out)
 (out/'summary.tex').write_text(reader.tex(r));diag=[]
 if render:
  for n in [1,2]:
   q=subprocess.run([xelatex,'-interaction=nonstopmode','-halt-on-error','summary.tex'],cwd=out,capture_output=True);(out/f'xelatex-{n}.log').write_bytes(q.stdout+q.stderr);need(q.returncode==0,'complete reader compile')
  diag=[s for s in (out/'summary.log').read_text(errors='replace').splitlines() if any(x in s for x in ['Overfull','Underfull','Missing character','Font Warning','LaTeX Warning'])];need(not diag,'render diagnostics '+str(diag))
 comparisons=sum(1+int(t['including_printed_programs'] is not None)+int(t['including_raw_programs'] is not None)+int(t.get('including_optional_validation') is not None)+len(t['pairs']) for t in r['topics']);need(comparisons==90,'all exact comparison records')
 dump(out/'build_report.json',dict(status='PASS',topics=17,originals=40,unchanged_topic_records=15,exact_primary_comparisons=comparisons,diagnostics=diag,rendered=render,new_numerical_acceptance_pending=False))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--public-root',type=Path);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='xelatex');a=p.parse_args();build(a.out,a.public_root,a.render,a.xelatex)
