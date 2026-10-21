#!/usr/bin/env python3
"""Append accepted rank augmentation while preserving all seventeen admitted records."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
import argparse,copy,hashlib,json,os,subprocess
import plotting,reader
ROOT=Path(__file__).resolve().parent
PINS={'RankAugmentation':('b4232452cba25cae64bef0091a4adc947d8f679418fe73f1d439b5966ff587b7','444797a88e089d973c1c9df3e82558903c12326c42843ca62c591e8b7c92c59e')}
def need(x,m):
 if not x:raise ValueError('OVERVIEW41_REJECT: '+m)
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
  if public and r.get('public_path'):need((public/r['public_path']).read_bytes()==b,'exact current numerical public mapping')
  if public and r['role']=='fixed_root_publication_candidate':need((public/Path(r['path']).relative_to('/Users/sasha/medusa/math_compression')).read_bytes()==b,'exact fixed publication snapshot')
  if public and r['role']=='committed_baseline':
   rel=Path(r['path']).relative_to('/Users/sasha/medusa/math_compression');need(subprocess.check_output(['git','show',p['admitted_baseline_commit']+':'+str(rel)],cwd=public)==b,'exact committed baseline')
 need(data['previous_admission']['status']=='ROOT_ADMITTED_CONSOLIDATED_NUMERICAL_OVERVIEW40','admitted baseline40')
 for k in ['previous_results','previous_manifest','previous_review']:
  r=p['bindings'][k];rel=str(Path(r['path']).relative_to('/Users/sasha/medusa/math_compression'));need(any(x['path']==rel and x['sha256']==r['sha256']for x in data['previous_admission']['artifacts']),'baseline admission owns '+k)
 for key,(author,review)in PINS.items():
  need(p['bindings'][key+'_manifest']['sha256']==author and p['bindings'][key+'_review_manifest']['sha256']==review==p['new_numerical_reviews'][key],'accepted manifests '+key)
  for suffix in ['results','protocol']:
   need(any(x['path']==suffix+'.json'and x['sha256']==p['bindings'][key+'_'+suffix]['sha256']for x in data[key+'_manifest']['exports']),'numerical manifest owns '+suffix)
  need(any(x['path']=='review.json'and x['sha256']==p['bindings'][key+'_review']['sha256']for x in data[key+'_review_manifest']['exports']),'root manifest owns review')
  rr=data[key+'_review'];need(rr['author_manifest_sha256']==author,'review author pin')
  need(rr['status']=='ACCEPTED_UNCHANGED_DISTINCT_L020_NUMBERS','distinct numerical acceptance')
 rp=data['RankAugmentation_protocol'];need(rp['written']==['U','A1','COUNTER']and rp['application']==['A1','COUNTER']and rp['source']==['L020']and rp['primary']==['raw_untrimmed','NFC','characters_without_whitespace']and rp['alternate_not_additive'],'whole rank augmentation boundary')
 verify_publication(p,data)
 need(p['status']=='PRIVATE_OVERVIEW_CANDIDATE_FROM_DISTINCTLY_ACCEPTED_NUMBERS'and not p['new_factor_acceptance_pending'],'numbers accepted; overview pending')
 return p,data

def verify_publication(p,data):
 old=data['previous_corpus_pointer'];now=data['current_corpus_snapshot'];adm=data['new_admission'];cat=data['current_catalogue']
 need(old['admitted_principal_originals']==40 and old['currently_measured_originals']==40,'actual old40 counts despite historical status')
 need(now['status']=='CURRENT_PROGRAMME_41_ADMITTED_ORIGINALS_106_ACCESSIBLE','correct current41 status')
 need(tuple(now[k]for k in ['originals','accessible_originals','admitted_principal_originals','accessible_pending_complete_recovery','pending_source_retrieval','currently_measured_originals'])==(161,106,41,65,55,41),'actual programme counts')
 for k in ['admitted_original_ids','measured_original_ids']:need(now[k]==sorted(old[k]+['L020']),'add only L020 '+k)
 need(now['accessible_pending_original_ids']==[i for i in old['accessible_pending_original_ids']if i!='L020']and now['retrieval_original_ids']==old['retrieval_original_ids'],'unchanged accessibility boundary')
 need(now['all_originals_remain_active']and not now['all_original_proofs_recovered']and not now['all_conjectures_resolved'],'programme unresolved scope')
 need(adm['status']=='ROOT_ADMITTED_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT_AND_NUMERICAL_COMPARISON'and adm['source_ids']==['L020']and adm['topic']=='RankAugmentation','actual admission')
 need(adm['primary']==data['RankAugmentation_results']['primary']==data['RankAugmentation_review']['primary'],'admission preserves full accepted numerical boundary')
 ref=dict(path='audit/topic-rank-augmentation/v1/admission.json',bytes=p['bindings']['new_admission']['bytes'],sha256=p['bindings']['new_admission']['sha256'])
 need(ref in now['added_admissions']and ref in now['added_measurements'],'snapshot binds new admission')
 for k in PINS:
  for suffix in ['results','manifest','protocol','review','review_manifest']:
   q=p['bindings'][k+'_'+suffix];need(dict(path=q['public_path'],bytes=q['bytes'],sha256=q['sha256'])in adm['artifacts'],'admission binds exact numerical evidence')
 rows=[q for q in cat['entries']if q.get('topic')=='RankAugmentation']
 need([(q['role'],q['application_id'],q['physical_pages'])for q in rows]==[('umbrella','U_Augmentation',5),('application','RA1',3),('application_companion','RA1_counter',3),('program_appendix','Augmentation_code',3)],'full new catalogue source closure')
 need(all(q['admission']==ref['path']and q['measurement_admission']==ref['path']for q in rows),'actual new catalogue admission')

def rank_augmentation(allx):
 x=allx['primary'];c=x['costs'];raw=x['raw_costs'];s=c['L020'];u=c['U'];a=c['A1']+c['COUNTER'];code=c['CODE']
 need(c==dict(L020=33604,U=13904,A1=7242,COUNTER=6854,CODE=10866)and raw==dict(programs=9998,operational_drivers=14096,formal_files=5218),'exact complete costs')
 need(allx['physical_pages']==[19,5,3,3,3],'complete current pages')
 for k,d in [('written',u+a),('including_printed_programs',u+a+code),('including_raw_programs',u+a+raw['programs']),('conditional_application',a)]:accepted_fraction(x['comparisons'][k],s,d)
 t=dict(topic='RankAugmentation',title='Rank augmentation',source_count=1,source_ids=['L020'],pairs=[dict(source='L020',application='RA1',source_cost=s,application_cost=a,source_representation='complete_PDF_raw_untrimmed',conditional=ratio(s,a))],common_theory=u,common_components=dict(whole_common=u),application_components={'RA1':dict(main_application=c['A1'],required_counterproof=c['COUNTER'])},source_sum=s,applications_sum=a,written_denominator=u+a,printed_program_cost=code,raw_program_alternative=raw['programs'],representation='raw_untrimmed_pdf',normalization='NFC',unit='characters_without_whitespace',numerical_status='distinctly_root_accepted_pending_overview_publication',numeric_origin='RankAugmentation_results/primary',written=ratio(s,u+a),including_printed_programs=ratio(s,u+a+code),including_raw_programs=ratio(s,u+a+raw['programs']),including_optional_validation=None,conditional_prepaid=dict(full_common=u,full_declared_printed_programs=code,total=u+code),conditional_raw_alternative_prepaid=dict(full_common=u,full_declared_raw_programs=raw['programs'],total=u+raw['programs']),source_admission='audit/topic-rank-augmentation/v1/admission.json',multi_coordinate_input_retained=True,separate_raw_inventory=dict(programs=9998,program_literal_bytes=11533,drivers=14096,driver_literal_bytes=15947,formal=5218,formal_literal_bytes=6855),program_roles='All three full programs: one required finite example computation, one bounded validation and one supporting counterexample check. Three drivers and two Lean files remain separate; fifteen scoped declarations do not formalize the whole source.',scientific_boundary='Complete19-page arXiv2212.12563v1. Theorem4.1 cases1/2 retain full hypotheses; case3 is false, replaced by the exact corrected criterion and complete S18 counterproof. Introductory Table1 is retained motivating data, not regenerated; larger-orbit and higher-rank questions remain unresolved.',entire_source_pages=19,entire_common_pages=[5],entire_application_pages={'main':3,'counterproof':3},entire_program_pages=3,old_umbrella_free_premise=False,counterproof_free=False,old_two_page_program_appendix_added=False,full_source_formalized=False,scoped_Lean_declarations=15)
 for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']:t[k]=None
 return t

def make(data,p):
 old=data['previous_results'];r=copy.deepcopy(old);r.update(schema='programme.primary_summary.rank_augmentation41.candidate',status='AUTHOR_OVERVIEW_FROM_ACCEPTED_NUMBERS_PENDING_OVERVIEW_REVIEW',topic_count=18,original_manuscript_count=41,currently_published_measured_originals=40,proposed_measured_originals=41,pending_numerical_acceptance=[],pending_overview_review=True,admitted_baseline_commit=p['admitted_baseline_commit'],recovery_status_not_derived_from_measurement=True)
 r['topics']=copy.deepcopy(old['topics'])+[rank_augmentation(data['RankAugmentation_results'])]
 r['notes']=['All seventeen prior topic JSON objects are unchanged. The accepted numerical record adds L020 only.','RankAugmentation pays its whole five-page common theory and both three-page application and counterproof papers. No earlier B theory or counterproof is a free premise.','All three programs are paid in either complete printed or complete raw form. Drivers and fifteen scoped Lean declarations remain separate.','No pooled factor or cross-topic theory discount. Programme counts are derived separately from the root source/admission snapshot, not from numerical equality.','Prior records without a separately measured data field remain unchanged; omission is not a claim that their external data or proofs cost zero.']
 r['candidate_result_bindings']={k:p['bindings'][k+'_results']for k in PINS};r['distinct_numerical_acceptances']={k:p['bindings'][k+'_review_manifest']for k in PINS};r['old_overviews_preserved']=True
 r['programme_snapshot']={k:copy.deepcopy(data['current_corpus_snapshot'][k])for k in ['status','originals','accessible_originals','admitted_principal_originals','accessible_pending_complete_recovery','pending_source_retrieval','currently_measured_originals','all_originals_remain_active','all_original_proofs_recovered','all_conjectures_resolved']}
 r['programme_snapshot_binding']=p['bindings']['current_corpus_snapshot'];r['programme_counts_not_inferred_from_measurement']=True
 validate(r,old);return r

def validate(r,old):
 need(r['topic_count']==len(r['topics'])==18 and r['original_manuscript_count']==41,'18 topics/41 originals')
 need(r['currently_published_measured_originals']==40 and r['proposed_measured_originals']==41 and not r['pending_numerical_acceptance']and r['pending_overview_review'],'candidate scope')
 need(r['pooled_factor']is None and not r['cross_topic_deduplication']and not r['all_registry_manuscripts_completed']and r['registry_manuscripts']==161,'no pooled/completed-corpus claim')
 need(r['topics'][:-1]==old['topics'],'all seventeen prior objects unchanged')
 need(all(r[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'zero overview credit')
 expected=dict(status='CURRENT_PROGRAMME_41_ADMITTED_ORIGINALS_106_ACCESSIBLE',originals=161,accessible_originals=106,admitted_principal_originals=41,accessible_pending_complete_recovery=65,pending_source_retrieval=55,currently_measured_originals=41,all_originals_remain_active=True,all_original_proofs_recovered=False,all_conjectures_resolved=False)
 need(r['programme_snapshot']==expected and r['programme_counts_not_inferred_from_measurement'],'separate corrected programme snapshot')
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
 need(len(ids)==len(set(ids))==41 and set(ids)=={q['source']for t in old['topics']for q in t['pairs']}|{'L020'},'one exact new original')
 t=r['topics'][-1]
 need(t['topic']=='RankAugmentation'and tuple(t[k]for k in ['source_sum','common_theory','applications_sum','printed_program_cost','raw_program_alternative'])==(33604,13904,14096,10866,9998),'complete new costs')
 need(t['application_components']=={'RA1':dict(main_application=7242,required_counterproof=6854)}and t['common_components']==dict(whole_common=13904),'both full local components')
 need(t['conditional_prepaid']==dict(full_common=13904,full_declared_printed_programs=10866,total=24770)and t['conditional_raw_alternative_prepaid']==dict(full_common=13904,full_declared_raw_programs=9998,total=23902),'complete acquisition')
 need(t['representation']=='raw_untrimmed_pdf'and t['entire_source_pages']==19 and t['entire_common_pages']==[5]and t['entire_application_pages']==dict(main=3,counterproof=3)and t['entire_program_pages']==3,'all pages')
 need(all(t[k]is False for k in ['old_umbrella_free_premise','counterproof_free','old_two_page_program_appendix_added','full_source_formalized'])and t['scoped_Lean_declarations']==15,'scope limits')
 need(t['separate_raw_inventory']==dict(programs=9998,program_literal_bytes=11533,drivers=14096,driver_literal_bytes=15947,formal=5218,formal_literal_bytes=6855),'whole separate inventories')
 need('case3 is false'in t['scientific_boundary']and 'not regenerated'in t['scientific_boundary']and 'questions remain unresolved'in t['scientific_boundary'],'source correction and scope')

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
 comparisons=sum(1+int(t['including_printed_programs'] is not None)+int(t['including_raw_programs'] is not None)+int(t.get('including_optional_validation') is not None)+len(t['pairs']) for t in r['topics']);need(comparisons==94,'all exact comparison records')
 dump(out/'build_report.json',dict(status='PASS',topics=18,originals=41,unchanged_topic_records=17,exact_primary_comparisons=comparisons,diagnostics=diag,rendered=render,new_numerical_acceptance_pending=False))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--public-root',type=Path);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='xelatex');a=p.parse_args();build(a.out,a.public_root,a.render,a.xelatex)
