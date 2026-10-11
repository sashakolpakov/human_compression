#!/usr/bin/env python3
"""Append accepted Mixes measurements; preserve all eighteen prior topic objects."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, localcontext
import argparse,copy,hashlib,json,os,subprocess
import plotting,reader
ROOT=Path(__file__).resolve().parent
PINS={'Mixes':('280555bfa0f45388bea391b35ef92c44bdaf9f0b22af79fca6dff469a733b7d0','8e0d5c0f1c3212cf96a02361aad84aec5c26b464c8c7c0f98cb1b984dbf28b52')}
def need(x,m):
 if not x:raise ValueError('OVERVIEW42_REJECT: '+m)
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def load(p):return json.loads(p.read_text())
def ratio(n,d):
 with localcontext() as c:c.prec=50;v=f'{Decimal(n)/Decimal(d):.12f}'
 return dict(numerator=n,denominator=d,exact_fraction=str(Fraction(n,d)),decimal=v)
def accepted_fraction(x,n,d):
 need(x['numerator']==n and x['denominator']==d and Fraction(x['reduced_numerator'],x['reduced_denominator'])==Fraction(n,d),'accepted rational')
 need(x['exact_fraction']==str(Fraction(n,d))and x['decimal']==ratio(n,d)['decimal'],'accepted rational display')
def load_inputs(public=None):
 p=load(ROOT/'protocol.json');data={}
 for k,r in p['bindings'].items():
  path=Path(r['local']);need(not path.is_absolute()and '..'not in path.parts,'relative local evidence');b=(ROOT/path).read_bytes();need(len(b)==r['bytes']and sha(b)==r['sha256'],'bound input '+k);data[k]=json.loads(b)
  if public and r.get('public_path'):need((public/r['public_path']).read_bytes()==b,'exact current numerical mapping')
  if public and r['role']=='fixed_root_publication_candidate':need((public/Path(r['path']).relative_to('/Users/sasha/medusa/math_compression')).read_bytes()==b,'fixed root scope snapshot')
  if public and r['role']=='committed_baseline':
   rel=Path(r['path']).relative_to('/Users/sasha/medusa/math_compression');need(subprocess.check_output(['git','show',p['admitted_baseline_commit']+':'+str(rel)],cwd=public)==b,'exact committed baseline')
 need(data['previous_admission']['status']=='ROOT_ADMITTED_CONSOLIDATED_NUMERICAL_OVERVIEW41','admitted baseline41')
 for k in ['previous_results','previous_manifest','previous_review']:
  r=p['bindings'][k];rel=str(Path(r['path']).relative_to('/Users/sasha/medusa/math_compression'));need(any(x['path']==rel and x['sha256']==r['sha256']for x in data['previous_admission']['artifacts']),'baseline admission owns '+k)
 for key,(author,review)in PINS.items():
  need(p['bindings'][key+'_manifest']['sha256']==author and p['bindings'][key+'_review_manifest']['sha256']==review==p['new_numerical_reviews'][key],'accepted manifests '+key)
  for suffix in ['results','protocol']:need(any(x['path']==suffix+'.json'and x['sha256']==p['bindings'][key+'_'+suffix]['sha256']for x in data[key+'_manifest']['exports']),'numerical manifest owns '+suffix)
  need(any(x['path']=='review.json'and x['sha256']==p['bindings'][key+'_review']['sha256']for x in data[key+'_review_manifest']['exports']),'root manifest owns review')
  rr=data[key+'_review'];need(rr['numerical_manifest_sha256']==author and rr['status']=='ROOT_ACCEPTED_COMPLETE_F005_NUMERICAL_COMPARISON','distinct numerical acceptance')
 rp=data['Mixes_protocol'];need(rp['common_documents']==['U']and rp['application_documents']==['A1','A2']and rp['printed_program_documents']==['CODE1','CODE2']and rp['source_documents']==['F005']and rp['primary']==['raw_untrimmed','NFC','characters_without_whitespace']and rp['raw_and_printed_alternatives'],'complete Mixes boundary')
 verify_publication(p,data)
 need(p['status']=='PRIVATE_OVERVIEW_CANDIDATE_FROM_DISTINCTLY_ACCEPTED_NUMBERS'and not p['new_factor_acceptance_pending'],'numbers accepted; overview pending')
 return p,data

def verify_publication(p,data):
 old=data['previous_corpus_pointer'];now=data['current_corpus_snapshot'];adm=data['new_admission'];cat=data['current_catalogue']
 need(old['admitted_principal_originals']==41 and old['currently_measured_originals']==41,'actual baseline counts')
 # Current programme excludes unavailable originals only by explicit root scope snapshot.
 need(tuple(now[k]for k in ['originals','accessible_originals','admitted_principal_originals','accessible_pending_complete_recovery','pending_source_retrieval','currently_measured_originals','archived_unavailable_originals','historical_originals'])==(106,106,42,64,0,42,55,161),'current accessible-only programme')
 for k in ['admitted_original_ids','measured_original_ids']:need(now[k]==sorted(old[k]+['F005']),'add only F005 '+k)
 need(now['accessible_pending_original_ids']==[i for i in old['accessible_pending_original_ids']if i!='F005'],'unchanged accessible queue except admitted F005')
 need(now['retrieval_original_ids']==[]and now['archived_original_ids']==old['retrieval_original_ids'],'explicit unavailable archive, no live retrieval')
 need(not now['all_original_proofs_recovered']and not now['all_conjectures_resolved'],'programme not complete')
 need(now['active_original_ids']==sorted(old['admitted_original_ids']+old['accessible_pending_original_ids']),'all106 previously accessible originals remain active')
 scope=data['scope_admission'];need(scope['status']=='ROOT_ADMITTED_USER_REQUESTED_ACCESSIBLE_CATALOGUE'and tuple(scope[k]for k in ['active_originals','historical_originals','archived_originals','source_retrieval_in_scope','principal_credit_added','question_credit_added','measurement_factor_changes','singletons_excluded'])==(106,161,55,False,0,0,0,0),'explicit scope admission, no silent exclusion or credit')
 q=p['bindings']['scope_admission'];need(now['scope_admission']==dict(path='audit/corpus/accessible106/admission.json',bytes=q['bytes'],sha256=q['sha256']),'snapshot binds scope adoption')
 need(not now['source_retrieval_in_scope']and not now['all_historical_originals_remain_active'],'archive scope explicit')

 need(adm['status']=='ROOT_ADMITTED_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT_AND_NUMERICAL_COMPARISON'and adm['source_ids']==['F005']and adm['topic']=='Mixes','actual scientific/numerical admission')
 need(adm['primary']==data['Mixes_results']['primary']==data['Mixes_review']['primary'],'admission preserves accepted numerical boundary')
 ref=dict(path='audit/topic-mixes/v1/admission.json',bytes=p['bindings']['new_admission']['bytes'],sha256=p['bindings']['new_admission']['sha256'])
 need(ref in now['added_admissions']and ref in now['added_measurements'],'current snapshot binds Mixes admission')
 for k in PINS:
  for suffix in ['results','manifest','protocol','review','review_manifest']:
   q=p['bindings'][k+'_'+suffix];need(dict(path=q['public_path'],bytes=q['bytes'],sha256=q['sha256'])in adm['artifacts'],'admission binds exact numerical evidence')
 rows=[q for q in cat['entries']if q.get('topic')=='Mixes']
 need([(q['role'],q['application_id'],q['physical_pages'])for q in rows]==[('umbrella','U_Mixes',5),('application','MX1',8),('application_companion','MX1_exceptional',4),('program_appendix','Mixes_code_main',4),('program_appendix','Mixes_code_exceptional',3)],'full current catalogue closure')
 need(all(q['admission']==ref['path']and q['measurement_admission']==ref['path']for q in rows),'actual catalogue admission')
 need(adm['principal_background_rows']==35 and adm['unanswered_final_problems']==3 and adm['formal_declarations']==2 and not adm['prior_correction_free']and not adm['whole_source_formalized'],'scientific boundary not inflated')

def mixes(allx):
 x=allx['primary'];c=x['document_costs'];raw=x['raw_costs'];s=c['F005'];u=c['U'];a=c['A1']+c['A2'];code=c['CODE1']+c['CODE2']
 need(c==dict(F005=57753,U=12615,A1=20788,A2=10289,CODE1=8813,CODE2=7212)and raw==dict(programs=14608,drivers=13674,formal=1714),'exact accepted costs')
 need(allx['document_pages']==dict(F005=21,U=5,A1=8,A2=4,CODE1=4,CODE2=3),'complete current pages')
 for k,d in [('written_papers',u+a),('including_printed_programs',u+a+code),('including_raw_programs_alternative',u+a+raw['programs']),('conditional_application',a)]:accepted_fraction(x['comparisons'][k],s,d)
 inventory={}
 for name,group in allx['raw_file_inventory'].items():
  inventory[name]=sum(q['metrics']['NFC']['characters_without_whitespace']for q in group.values());inventory[name+'_literal_bytes']=sum(q['bytes']for q in group.values())
 need(inventory==dict(programs=14608,programs_literal_bytes=18073,drivers=13674,drivers_literal_bytes=15551,formal=1714,formal_literal_bytes=2436),'whole raw inventory')
 t=dict(topic='Mixes',title='Mixes and intersection fibers',source_count=1,source_ids=['F005'],pairs=[dict(source='F005',application='MX1',source_cost=s,application_cost=a,source_representation='complete_PDF_raw_untrimmed',conditional=ratio(s,a))],common_theory=u,common_components=dict(whole_common=u),application_components={'MX1':dict(main_application=c['A1'],exceptional_application=c['A2'])},source_sum=s,applications_sum=a,written_denominator=u+a,printed_program_cost=code,raw_program_alternative=raw['programs'],representation='raw_untrimmed_pdf',normalization='NFC',unit='characters_without_whitespace',numerical_status='distinctly_root_accepted_pending_overview_publication',numeric_origin='Mixes_results/primary',written=ratio(s,u+a),including_printed_programs=ratio(s,u+a+code),including_raw_programs=ratio(s,u+a+raw['programs']),including_optional_validation=None,conditional_prepaid=dict(full_common=u,full_declared_printed_programs=code,total=u+code),conditional_raw_alternative_prepaid=dict(full_common=u,full_declared_raw_programs=raw['programs'],total=u+raw['programs']),source_admission='audit/topic-mixes/v1/admission.json',multi_coordinate_input_retained=True,separate_raw_inventory=inventory,program_roles='All three complete programs: one required finite certificate and two bounded validations. Three operational drivers and one Lean file remain separate; two generic declarations do not formalize the complete source.',scientific_boundary='Complete 21-page arXiv:2506.19334v1: 35 principal/background dispositions, including five literal counterexample targets and two convention-qualified targets, with corrected criteria. The three final problems remain unanswered. The exceptional four-page application and all its code are paid in full.',entire_source_pages=21,entire_common_pages=[5],entire_application_pages={'main':8,'exceptional':4},entire_program_pages=[4,3],prior_theory_free=False,prior_correction_free=False,full_source_formalized=False,scoped_Lean_declarations=2,unanswered_final_problems=3)
 for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']:t[k]=None
 return t

SNAPSHOT_KEYS=['status','originals','accessible_originals','admitted_principal_originals','accessible_pending_complete_recovery','pending_source_retrieval','currently_measured_originals','archived_unavailable_originals','historical_originals','all_original_proofs_recovered','all_conjectures_resolved']
def make(data,p):
 old=data['previous_results'];r=copy.deepcopy(old);r.update(schema='programme.primary_summary.mixes42.candidate',status='AUTHOR_OVERVIEW_FROM_ACCEPTED_NUMBERS_PENDING_OVERVIEW_REVIEW',topic_count=19,original_manuscript_count=42,currently_published_measured_originals=41,proposed_measured_originals=42,pending_numerical_acceptance=[],pending_overview_review=True,admitted_baseline_commit=p['admitted_baseline_commit'],recovery_status_not_derived_from_measurement=True,registry_manuscripts=106,original_historical_catalogue=161,archived_unavailable=55,active_retrieval=0)
 r['topics']=copy.deepcopy(old['topics'])+[mixes(data['Mixes_results'])]
 r['notes']=['All eighteen prior topic JSON objects are unchanged. The accepted numerical record adds F005 only.','Mixes pays its whole five-page common theory and both eight- and four-page local papers. No earlier correction or program is a free premise.','All three programs are paid in either complete printed or complete raw form. Drivers and two generic Lean declarations remain separate.','The active catalogue is the 106 accessible originals; 55 unavailable originals are archived from the historical 161, with no active retrieval.','No pooled factor or cross-topic theory discount. Programme counts come from the separate root admission/scope snapshot.','Singleton topics remain included; no numerical result is silently excluded.','Omission of an older data field is not a claim that external data or proofs cost zero.']
 r['candidate_result_bindings']={k:p['bindings'][k+'_results']for k in PINS};r['distinct_numerical_acceptances']={k:p['bindings'][k+'_review_manifest']for k in PINS};r['old_overviews_preserved']=True
 r['programme_snapshot']={k:copy.deepcopy(data['current_corpus_snapshot'][k])for k in SNAPSHOT_KEYS};r['programme_snapshot_binding']=p['bindings']['current_corpus_snapshot'];r['programme_counts_not_inferred_from_measurement']=True
 validate(r,old);return r

def validate(r,old):
 need(r['topic_count']==len(r['topics'])==19 and r['original_manuscript_count']==42,'19 topics/42 originals')
 need(r['currently_published_measured_originals']==41 and r['proposed_measured_originals']==42 and not r['pending_numerical_acceptance']and r['pending_overview_review'],'candidate scope')
 need(r['pooled_factor']is None and not r['cross_topic_deduplication']and not r['all_registry_manuscripts_completed'],'no pooled/completed-corpus claim')
 need((r['registry_manuscripts'],r['original_historical_catalogue'],r['archived_unavailable'],r['active_retrieval'])==(106,161,55,0),'active accessible-only scope')
 need(r['topics'][:-1]==old['topics'],'all eighteen prior topic objects unchanged')
 need(all(r[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'zero overview credit')
 snap=r['programme_snapshot'];need(tuple(snap[k]for k in ['originals','accessible_originals','admitted_principal_originals','accessible_pending_complete_recovery','pending_source_retrieval','currently_measured_originals','archived_unavailable_originals','historical_originals'])==(106,106,42,64,0,42,55,161)and not snap['all_original_proofs_recovered']and not snap['all_conjectures_resolved']and r['programme_counts_not_inferred_from_measurement'],'separate corrected programme snapshot')
 need(snap['status']=='CURRENT_PROGRAMME_42_ADMITTED_OF_106_ACTIVE_ORIGINALS','current status identifies scope')
 ids=[]
 for t in r['topics']:
  need(sum(t['common_components'].values())==t['common_theory'],'all common components')
  need(sum(q['source_cost']for q in t['pairs'])==t['source_sum']and sum(q['application_cost']for q in t['pairs'])==t['applications_sum'],'complete papers')
  need(t['source_ids']==[q['source']for q in t['pairs']]and t['source_count']==len(t['pairs']),'source roster')
  need(t['written_denominator']==t['common_theory']+t['applications_sum']and t['written']==ratio(t['source_sum'],t['written_denominator']),'written factor')
  extra=t['mandatory_data_cost']if 'mandatory_data_cost'in t else 0
  for k,c in [('including_printed_programs',t['printed_program_cost']),('including_raw_programs',t['raw_program_alternative'])]:need(t[k]==(None if c is None else ratio(t['source_sum'],t['written_denominator']+c+extra)),'code plus data denominator')
  for q in t['pairs']:
   ids.append(q['source']);need(q['conditional']==ratio(q['source_cost'],q['application_cost']),'exact conditional')
   if 'application_components'in t:need(sum(t['application_components'][q['application']].values())==q['application_cost'],'all application components')
  for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']:need(t[k]is None,'unknown remains null')
 need(len(ids)==len(set(ids))==42 and set(ids)=={q['source']for t in old['topics']for q in t['pairs']}|{'F005'},'one exact new original')
 t=r['topics'][-1]
 need(t['topic']=='Mixes'and tuple(t[k]for k in ['source_sum','common_theory','applications_sum','printed_program_cost','raw_program_alternative'])==(57753,12615,31077,16025,14608),'complete new costs')
 need(t['application_components']=={'MX1':dict(main_application=20788,exceptional_application=10289)}and t['common_components']==dict(whole_common=12615),'both whole local papers')
 need(t['conditional_prepaid']==dict(full_common=12615,full_declared_printed_programs=16025,total=28640)and t['conditional_raw_alternative_prepaid']==dict(full_common=12615,full_declared_raw_programs=14608,total=27223),'full acquisition')
 need(t['representation']=='raw_untrimmed_pdf'and t['entire_source_pages']==21 and t['entire_common_pages']==[5]and t['entire_application_pages']==dict(main=8,exceptional=4)and t['entire_program_pages']==[4,3],'all pages')
 need(not t['prior_theory_free']and not t['prior_correction_free']and not t['full_source_formalized']and t['scoped_Lean_declarations']==2 and t['unanswered_final_problems']==3,'scope limits')
 need(t['separate_raw_inventory']==dict(programs=14608,programs_literal_bytes=18073,drivers=13674,drivers_literal_bytes=15551,formal=1714,formal_literal_bytes=2436),'whole separate inventories')
 need('five literal counterexample targets'in t['scientific_boundary']and 'three final problems remain unanswered'in t['scientific_boundary'],'source correction and scope')

def build(out,public=None,render=False,xelatex='xelatex'):
 need(not out.exists()and not out.is_symlink(),'fresh output');out.mkdir(parents=True);p,data=load_inputs(public);r=make(data,p);dump(out/'results.json',r)
 for name,t in plotting.csv_text(r).items():(out/name).write_text(t)
 specs={k:plotting.plot_spec(r,k)for k in ['whole_topics','conditional_1','conditional_2']};dump(out/'plot_data.json',specs)
 os.environ.setdefault('MPLCONFIGDIR',str(out/'mpl-cache'));os.environ.setdefault('XDG_CACHE_HOME',str(out/'cache'))
 for spec in specs.values():plotting.draw(spec,out)
 (out/'summary.tex').write_text(reader.tex(r));diag=[]
 if render:
  for n in [1,2]:
   q=subprocess.run([xelatex,'-interaction=nonstopmode','-halt-on-error','summary.tex'],cwd=out,capture_output=True);(out/f'xelatex-{n}.log').write_bytes(q.stdout+q.stderr);need(q.returncode==0,'complete reader compile')
  diag=[s for s in(out/'summary.log').read_text(errors='replace').splitlines()if any(x in s for x in ['Overfull','Underfull','Missing character','Font Warning','LaTeX Warning'])];need(not diag,'render diagnostics '+str(diag))
 comparisons=sum(1+int(t['including_printed_programs']is not None)+int(t['including_raw_programs']is not None)+int(t.get('including_optional_validation')is not None)+len(t['pairs'])for t in r['topics']);need(comparisons==98,'all exact comparison records')
 dump(out/'build_report.json',dict(status='PASS',topics=19,originals=42,active_originals=106,archived_unavailable=55,unchanged_topic_records=18,exact_primary_comparisons=comparisons,diagnostics=diag,rendered=render,new_numerical_acceptance_pending=False))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--public-root',type=Path);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='xelatex');a=p.parse_args();build(a.out,a.public_root,a.render,a.xelatex)
