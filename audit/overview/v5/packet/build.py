#!/usr/bin/env python3
"""Add one original to the Operations topic, preserving thirteen exact records."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
import argparse,copy,hashlib,json,os,subprocess
import plotting,reader
ROOT=Path(__file__).resolve().parent

def need(x,m):
 if not x:raise ValueError('OVERVIEW36_REJECT: '+m)
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def load(p):return json.loads(p.read_text())
def ratio(n,d):
 f=Fraction(n,d)
 with localcontext() as c:c.prec=50;dec=f'{Decimal(n)/Decimal(d):.12f}'
 return dict(numerator=n,denominator=d,exact_fraction=str(f),decimal=dec)
def same_ratio(f,n,d):
 need(f['numerator']==n and f['denominator']==d,'exact accepted costs')
 if 'reduced_numerator' in f:need(Fraction(f['reduced_numerator'],f['reduced_denominator'])==Fraction(n,d),'exact reduced fraction')
 if 'decimal' in f:need(abs(Decimal(f['decimal'])-Decimal(n)/Decimal(d))<Decimal('0.000000000002'),'decimal precision')

def load_inputs(public=None):
 p=load(ROOT/'protocol.json');data={}
 for k,r in p['bindings'].items():
  b=(ROOT/r['local']).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'complete bound input '+k);data[k]=json.loads(b)
  if public and r['role']=='committed_baseline':
   rel=Path(r['path']).relative_to('/Users/sasha/medusa/math_compression');need(subprocess.check_output(['git','show',p['admitted_baseline_commit']+':'+str(rel)],cwd=public)==b,'exact committed baseline')
 need(data['previous_admission']['status'].startswith('ROOT_ADMITTED'),'admitted baseline')
 for k in ['previous_results','previous_manifest','previous_review']:
  r=p['bindings'][k];rel=str(Path(r['path']).relative_to('/Users/sasha/medusa/math_compression'));need(any(x['path']==rel and x['sha256']==r['sha256'] for x in data['previous_admission']['artifacts']),'baseline admission covers record')
 r=p['bindings']['Operations_results'];need(any(x['path']=='results.json' and x['sha256']==r['sha256'] for x in data['Operations_manifest']['exports']),'frozen new arithmetic')
 need(p['bindings']['Operations_manifest']['sha256']=='c211bfc7a4ae9e0855874aa0584b0f8dfa85c855390e59fa49659b5b517ef978','exact author candidate')
 need(data['Operations_input_review']['status']=='ROOT_ACCEPTED_COMPLETE_MEASUREMENT_INPUTS' and data['Operations_input_review']['numerical_factor_calculation_may_proceed'],'input acceptance only')
 need(not p['new_factor_acceptance_pending'] and p['status']=='PRIVATE_OVERVIEW_CANDIDATE_FROM_DISTINCTLY_ACCEPTED_NUMBERS','distinct numerical acceptance before overview')
 need(p['bindings']['Operations_review_manifest']['sha256']==p['new_numerical_review_sha256']=='d301b71e5743aa9e5d29a048d6553db644295a6fa4081d5686ab0e42a9f578f5','exact root numerical acceptance')
 need(data['Operations_review']['status']=='ROOT_ACCEPTED_COMPLETE_OPERATIONS_NUMBERS' and data['Operations_review']['author_manifest_sha256']==p['bindings']['Operations_manifest']['sha256'],'accepted exact numerical candidate')
 need(any(x['path']=='review.json' and x['sha256']==p['bindings']['Operations_review']['sha256'] for x in data['Operations_review_manifest']['exports']),'review manifest binds acceptance')
 return p,data

def operations_topic(x):
 pairs=[];components={};appids={'N005':'OP1','N006':'DG2','N007':'DG1'}
 for k,ac in x['application_costs'].items():
  n=x['original_costs'][k];a=appids[k];pairs.append(dict(source=k,application=a,source_cost=n,application_cost=ac,source_representation='complete_PDF_calibrated_selected_encoded_event_proxies',conditional=ratio(n,ac)));same_ratio(x['conditional'][k],n,ac)
  components[a]={'N005_complete':ac} if k=='N005' else {'N007_complete':ac} if k=='N007' else {i:x['document_costs'][i] for i in ['A2','A2nine','A2HN']}
 t=dict(topic='Operations',title='Coset geometries under group operations',source_count=3,source_ids=['N005','N006','N007'],pairs=pairs,common_theory=x['common_theory'],common_components={'whole_current_common':x['common_theory']},application_components=components,source_sum=x['source_sum'],applications_sum=x['all_applications'],written_denominator=x['written_denominator'],printed_program_cost=None,raw_program_alternative=x['whole_software_cost'],representation='calibrated_selected_pdf',normalization='NFC',unit='characters_without_whitespace',numerical_status='distinctly_root_accepted_pending_overview_publication',numeric_origin='Operations_results/primary',written=ratio(x['source_sum'],x['written_denominator']),including_printed_programs=None,including_raw_programs=ratio(x['source_sum'],x['program_inclusive_denominator']),including_optional_validation=None,conditional_prepaid=dict(full_common=x['common_theory'],full_declared_raw_software=x['whole_software_cost'],total=x['common_theory']+x['whole_software_cost'],required_external_data_already_acquired=True,external_bytes_separate=True),separate_raw_inventory=x['raw_file_costs'],source_admission='Private integrated science, citations, inputs and numbers distinctly accepted; joint public admission pending.',program_roles='Twenty-three complete files: seventeen finite proof/witness files and six validations, plus both whole required decoders. Five operational drivers and three partial Lean files separately disclosed.',raw_program_components=dict(twenty_three_full_files=x['whole_program_cost'],both_required_decoders=x['required_decoder_cost']),partial_printed_alternatives=x['partial_printed_costs'],no_complete_printed_route=True,external_bytes=dict(required_representation_files=4,required_representation_bytes=21960689,listed_installed_files=16,listed_installed_bytes=2516249),graphic_proxy_sensitivities_required=True,scientific_publication_map='a404401a91266a9f7612762a07fcaa5b0a2b0315c840e492e8e1ca7303cc913f')
 for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']:t[k]=None
 for k,den in [('written',t['written_denominator']),('including_whole_raw_software',x['program_inclusive_denominator'])]:same_ratio(x['whole'][k],t['source_sum'],den)
 return t

def make(data,p):
 old=data['previous_results'];r=copy.deepcopy(old);r.update(schema='programme.primary_summary.operations36.candidate',status='AUTHOR_OVERVIEW_FROM_ACCEPTED_NUMBERS_PENDING_OVERVIEW_REVIEW',topic_count=14,original_manuscript_count=36,currently_published_measured_originals=35,proposed_measured_originals=36,pending_numerical_acceptance=[],pending_overview_review=True,admitted_baseline_commit=p['admitted_baseline_commit'],recovery_status_not_derived_from_measurement=True)
 r['topics']=[operations_topic(data['Operations_results']['primary']) if t['topic']=='Diagonal' else copy.deepcopy(t) for t in old['topics']]
 r['notes']=['All thirteen unaffected topic objects are preserved exactly, including Gluing.','Only Diagonal is superseded by the joint Operations record: new whole common, all three originals, revised N006/N007 and complete N005 applications.','The Operations numbers have distinct root acceptance; this overview awaits its own acceptance.','No pooled factor or overlap discount between topics; unknown external/graphic/historical costs remain null.','Thirty-six candidate measured originals are not a recovery/accessibility count or completion of the 161-item programme.']
 r['candidate_result_bindings']={'Operations':p['bindings']['Operations_results']};r['distinct_numerical_acceptances']={'Operations':p['bindings']['Operations_review_manifest']};r['new_numerical_input_acceptance']=p['bindings']['Operations_input_review'];r['old_overviews_preserved']=True
 validate(r,old);return r

def validate(r,old):
 need(r['topic_count']==len(r['topics'])==14 and r['original_manuscript_count']==36,'14 topics and 36 candidate originals')
 need(r['currently_published_measured_originals']==35 and r['proposed_measured_originals']==36 and r['pending_numerical_acceptance']==[] and r['pending_overview_review'],'pending acceptance explicit')
 need(r['pooled_factor'] is None and not r['cross_topic_deduplication'] and not r['all_registry_manuscripts_completed'] and r['registry_manuscripts']==161,'no pooled/corpus-completion claim')
 need([t for t in r['topics'] if t['topic']!='Operations']==[t for t in old['topics'] if t['topic']!='Diagonal'],'all thirteen topic objects preserved exactly')
 need(all(r[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'no credits')
 ids=[]
 for t in r['topics']:
  need(sum(t['common_components'].values())==t['common_theory'],'complete common theory')
  need(sum(q['source_cost'] for q in t['pairs'])==t['source_sum'] and sum(q['application_cost'] for q in t['pairs'])==t['applications_sum'],'complete source/application costs')
  need(t['source_ids']==[q['source'] for q in t['pairs']] and t['source_count']==len(t['pairs']),'source roster')
  need(t['written_denominator']==t['common_theory']+t['applications_sum'] and t['written']==ratio(t['source_sum'],t['written_denominator']),'written fraction')
  for key,cost in [('including_printed_programs',t['printed_program_cost']),('including_raw_programs',t['raw_program_alternative'])]:need(t[key]==(None if cost is None else ratio(t['source_sum'],t['written_denominator']+cost)),'whole programme alternative')
  for q in t['pairs']:
   ids.append(q['source']);need(q['conditional']==ratio(q['source_cost'],q['application_cost']),'complete conditional application')
   if 'application_components' in t:need(sum(t['application_components'][q['application']].values())==q['application_cost'],'all companion segments')
  for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']:need(t[k] is None,'unknown cost not zero')
 need(len(ids)==len(set(ids))==36 and set(ids)=={q['source'] for t in old['topics'] for q in t['pairs']}|{'N005'},'exact one added original')
 t=next(t for t in r['topics'] if t['topic']=='Operations');need(t['common_theory']==58215 and t['source_ids']==['N005','N006','N007'] and t['printed_program_cost'] is None and t['no_complete_printed_route'],'whole new theory and three originals')
 need(t['raw_program_components']==dict(twenty_three_full_files=392833,both_required_decoders=11015) and t['raw_program_alternative']==403848,'whole programme')
 need(t['conditional_prepaid']==dict(full_common=58215,full_declared_raw_software=403848,total=462063,required_external_data_already_acquired=True,external_bytes_separate=True),'whole preacquisition')

def build(out,public=None,render=False,xelatex='/opt/homebrew/bin/xelatex'):
 need(not out.exists() and not out.is_symlink(),'fresh output');out.mkdir(parents=True);p,data=load_inputs(public);r=make(data,p);dump(out/'results.json',r)
 for name,t in plotting.csv_text(r).items():(out/name).write_text(t)
 specs={k:plotting.plot_spec(r,k) for k in ['whole_topics','conditional_1','conditional_2']};dump(out/'plot_data.json',specs)
 os.environ.setdefault('MPLCONFIGDIR',str(out/'mpl-cache'));os.environ.setdefault('XDG_CACHE_HOME',str(out/'cache'))
 for spec in specs.values():plotting.draw(spec,out)
 (out/'summary.tex').write_text(reader.tex(r));diagnostics=[]
 if render:
  for i in [1,2]:
   q=subprocess.run([xelatex,'-interaction=nonstopmode','-halt-on-error','summary.tex'],cwd=out,capture_output=True);(out/f'xelatex-{i}.log').write_bytes(q.stdout+q.stderr);need(q.returncode==0,'fresh full reader compile')
  diagnostics=[line for line in (out/'summary.log').read_text(errors='replace').splitlines() if any(x in line for x in ['Overfull','Underfull','Missing character','Font Warning','LaTeX Warning'])];need(not diagnostics,'render diagnostics '+str(diagnostics))
 comparisons=sum(1+int(t['including_printed_programs'] is not None)+int(t['including_raw_programs'] is not None)+int(t.get('including_optional_validation') is not None)+len(t['pairs']) for t in r['topics'])
 dump(out/'build_report.json',dict(status='PASS',topics=14,originals=36,unchanged_topic_records=13,exact_primary_comparisons=comparisons,diagnostics=diagnostics,rendered=render,Operations_numerical_acceptance_pending=False))

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--public-root',type=Path);a.add_argument('--render',action='store_true');a.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');q=a.parse_args();build(q.out,q.public_root,q.render,q.xelatex)
