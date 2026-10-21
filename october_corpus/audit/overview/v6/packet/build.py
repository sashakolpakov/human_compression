#!/usr/bin/env python3
"""Append RankContraction while preserving all fourteen admitted topic records."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
import argparse,copy,hashlib,json,os,subprocess
import plotting,reader
ROOT=Path(__file__).resolve().parent
AUTHOR='7eb6e66ff1fdd291624a52ef86f2d54906c8a723aad6f9e6f99fbf9593782330'
REVIEW='9e3d09defb11e1a289ea63308608724d7aabea2154777b2d240419c455d73316'
def need(x,m):
 if not x:raise ValueError('OVERVIEW37_REJECT: '+m)
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def load(p):return json.loads(p.read_text())
def ratio(n,d):
 with localcontext() as c:c.prec=50;v=f'{Decimal(n)/Decimal(d):.12f}'
 return dict(numerator=n,denominator=d,exact_fraction=str(Fraction(n,d)),decimal=v)
def accepted_fraction(x,n,d):
 need(x['numerator']==n and x['denominator']==d and Fraction(x['reduced_numerator'],x['reduced_denominator'])==Fraction(n,d) and x['exact_fraction']==str(Fraction(n,d)),'accepted exact fraction')
 need(abs(Decimal(str(x['factor']))-Decimal(n)/Decimal(d))<Decimal('0.000000000002'),'accepted factor')
def load_inputs(public=None):
 p=load(ROOT/'protocol.json');data={}
 for k,r in p['bindings'].items():
  path=Path(r['local']);need(not path.is_absolute() and '..' not in path.parts,'safe local input');b=(ROOT/path).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'complete bound input '+k);data[k]=json.loads(b)
  if public and r['role']=='committed_baseline':
   rel=Path(r['path']).relative_to('/Users/sasha/medusa/math_compression');need(subprocess.check_output(['git','show',p['admitted_baseline_commit']+':'+str(rel)],cwd=public)==b,'exact committed baseline')
 need(data['previous_admission']['status'].startswith('ROOT_ADMITTED'),'admitted baseline')
 for k in ['previous_results','previous_manifest','previous_review']:
  r=p['bindings'][k];rel=str(Path(r['path']).relative_to('/Users/sasha/medusa/math_compression'));need(any(x['path']==rel and x['sha256']==r['sha256'] for x in data['previous_admission']['artifacts']),'baseline admission covers record')
 need(p['bindings']['RankContraction_manifest']['sha256']==AUTHOR and p['bindings']['RankContraction_review_manifest']['sha256']==REVIEW==p['new_numerical_review_sha256'],'exact new author and distinct acceptance')
 for k,name in [('RankContraction_results','results.json'),('RankContraction_protocol','protocol.json')]:need(any(x['path']==name and x['sha256']==p['bindings'][k]['sha256'] for x in data['RankContraction_manifest']['exports']),'accepted author binds '+name)
 need(any(x['path']=='review.json' and x['sha256']==p['bindings']['RankContraction_review']['sha256'] for x in data['RankContraction_review_manifest']['exports']),'root manifest binds actual acceptance')
 rr=data['RankContraction_review'];need(rr['status']=='ROOT_ACCEPTED_COMPLETE_L037_NUMBERS' and rr['author_manifest_sha256']==AUTHOR and rr['coordinates']==30 and rr['exact_fractions']==120,'full distinct numerical acceptance')
 protocol=data['RankContraction_protocol'];need(protocol['primary']==['raw_untrimmed','NFC','characters_without_whitespace'] and protocol['all_page_extent']==[6,3,5,1] and protocol['whole_common_paid_once'] and not protocol['old_Topic_B_common_free_premise'],'complete local input boundary')
 need(p['status']=='PRIVATE_OVERVIEW_CANDIDATE_FROM_DISTINCTLY_ACCEPTED_NUMBERS' and not p['new_factor_acceptance_pending'],'numbers accepted; overview pending')
 return p,data

def new_topic(allx):
 x=allx['primary'];dc=x['document_costs'];s,u,a,c=dc['L037'],dc['U'],dc['A1'],dc['CODE'];raw=x['raw_program_cost'];written=u+a
 need((s,u,a,c,raw)==(15530,6937,10555,2925,2501),'exact new whole costs')
 need(x['written_cost']==written and allx['whole_common_charged_once'] and allx['all_application_pages_charged'] and not allx['old_Topic_B_common_free_premise'],'complete application and common')
 for k,d in [('written_papers',written),('including_printed_program',written+c),('including_raw_program_alternative',written+raw)]:accepted_fraction(x['comparisons'][k],s,d)
 accepted_fraction(x['conditional_application'],s,a)
 t=dict(topic='RankContraction',title='Rank contraction and rank spectra',source_count=1,source_ids=['L037'],pairs=[dict(source='L037',application='RC1',source_cost=s,application_cost=a,source_representation='complete_PDF_raw_untrimmed',conditional=ratio(s,a))],common_theory=u,common_components={'whole_local_theory':u},application_components={'RC1':{'complete_application_including_references':a}},source_sum=s,applications_sum=a,written_denominator=written,printed_program_cost=c,raw_program_alternative=raw,representation='raw_untrimmed_pdf',normalization='NFC',unit='characters_without_whitespace',numerical_status='distinctly_root_accepted_pending_overview_publication',numeric_origin='RankContraction_results/primary',written=ratio(s,written),including_printed_programs=ratio(s,written+c),including_raw_programs=ratio(s,written+raw),including_optional_validation=None,conditional_prepaid=dict(full_common=u,full_declared_printed_programs=c,total=u+c),conditional_raw_alternative_prepaid=dict(full_common=u,full_declared_raw_programs=raw,total=u+raw),separate_raw_inventory=dict(programs=raw,drivers=x['driver_cost_separate'],formal=x['formal_file_cost_separate']),program_roles='One complete GAP program certifies the literal finite examples; not a uniform contraction premise. One whole operational driver and one Lean file with four scoped declarations remain separate.',scientific_boundary='Complete L037 source and admitted 22-row contract. Conjecture5.1 remains open. Literal diagram strings are retained without assigning complete graphical cost.',source_admission='Distinct scientific and numerical root acceptance; current consolidated overview independently pending.',entire_source_pages=6,entire_common_pages=[3],entire_application_pages=5,entire_program_pages=1,old_Topic_B_common_free_premise=False,multi_coordinate_input_retained=True)
 for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']:t[k]=None
 return t

def make(data,p):
 old=data['previous_results'];r=copy.deepcopy(old);r.update(schema='programme.primary_summary.rankcontraction37.candidate',status='AUTHOR_OVERVIEW_FROM_ACCEPTED_NUMBERS_PENDING_OVERVIEW_REVIEW',topic_count=15,original_manuscript_count=37,currently_published_measured_originals=36,proposed_measured_originals=37,pending_numerical_acceptance=[],pending_overview_review=True,admitted_baseline_commit=p['admitted_baseline_commit'],recovery_status_not_derived_from_measurement=True)
 r['topics']=copy.deepcopy(old['topics'])+[new_topic(data['RankContraction_results'])]
 r['notes']=['All fourteen prior topic objects are preserved exactly. RankContraction adds L037 only.','RankContraction pays its entire local common theory and complete application; no old Topic B proof is free, and the old B topic remains independently charged.','Its written factor is below one; its conditional factor requires acquisition of the whole common paper and declared program.','All figures are topic-specific at each preserved representation. No pooled factor or cross-topic overlap discount is formed.','Thirty-seven measured originals are not a recovery/accessibility count or completion of the fixed161 programme.']
 r['candidate_result_bindings']={'RankContraction':p['bindings']['RankContraction_results']};r['distinct_numerical_acceptances']={'RankContraction':p['bindings']['RankContraction_review_manifest']};r.pop('new_numerical_input_acceptance',None);r['new_input_acceptance_manifest_sha256']=data['RankContraction_protocol']['input_review_manifest_sha256'];r['old_overviews_preserved']=True
 validate(r,old);return r

def validate(r,old):
 need(r['topic_count']==len(r['topics'])==15 and r['original_manuscript_count']==37,'15 topics and37 originals')
 need(r['currently_published_measured_originals']==36 and r['proposed_measured_originals']==37 and r['pending_numerical_acceptance']==[] and r['pending_overview_review'],'honest candidate status')
 need(r['pooled_factor'] is None and not r['cross_topic_deduplication'] and not r['all_registry_manuscripts_completed'] and r['registry_manuscripts']==161,'no pooled or complete-corpus claim')
 need(r['topics'][:-1]==old['topics'],'all fourteen previous topic objects unchanged')
 need(all(r[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'no new credit')
 ids=[]
 for t in r['topics']:
  need(sum(t['common_components'].values())==t['common_theory'],'complete common theory')
  need(sum(q['source_cost'] for q in t['pairs'])==t['source_sum'] and sum(q['application_cost'] for q in t['pairs'])==t['applications_sum'],'complete source and application')
  need(t['source_ids']==[q['source'] for q in t['pairs']] and t['source_count']==len(t['pairs']),'source roster')
  need(t['written_denominator']==t['common_theory']+t['applications_sum'] and t['written']==ratio(t['source_sum'],t['written_denominator']),'written factor')
  for k,c in [('including_printed_programs',t['printed_program_cost']),('including_raw_programs',t['raw_program_alternative'])]:need(t[k]==(None if c is None else ratio(t['source_sum'],t['written_denominator']+c)),'whole software alternative')
  for q in t['pairs']:
   ids.append(q['source']);need(q['conditional']==ratio(q['source_cost'],q['application_cost']),'conditional factor')
   if 'application_components' in t:need(sum(t['application_components'][q['application']].values())==q['application_cost'],'all application parts')
  for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']:need(t[k] is None,'unknown not zero')
 need(len(ids)==len(set(ids))==37 and set(ids)=={q['source'] for t in old['topics'] for q in t['pairs']}|{'L037'},'exact added original')
 t=r['topics'][-1];need(t['topic']=='RankContraction' and t['source_ids']==['L037'],'new topic only')
 need((t['source_sum'],t['common_theory'],t['applications_sum'],t['printed_program_cost'],t['raw_program_alternative'])==(15530,6937,10555,2925,2501),'whole fixed L037 costs')
 need(t['conditional_prepaid']==dict(full_common=6937,full_declared_printed_programs=2925,total=9862) and t['conditional_raw_alternative_prepaid']==dict(full_common=6937,full_declared_raw_programs=2501,total=9438),'entire acquisition in either representation')
 need((t['entire_source_pages'],t['entire_common_pages'],t['entire_application_pages'],t['entire_program_pages'])==(6,[3],5,1) and not t['old_Topic_B_common_free_premise'],'full15pages no freeoldB')
 need(t['representation']=='raw_untrimmed_pdf' and t['separate_raw_inventory']==dict(programs=2501,drivers=6114,formal=1280),'raw primary and separate driver/Lean')
 need('Conjecture5.1 remains open' in t['scientific_boundary'] and 'not a uniform contraction premise' in t['program_roles'],'question and finite evidence scope')

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
 comparisons=sum(1+int(t['including_printed_programs'] is not None)+int(t['including_raw_programs'] is not None)+int(t.get('including_optional_validation') is not None)+len(t['pairs']) for t in r['topics']);need(comparisons==81,'all exact comparison records')
 dump(out/'build_report.json',dict(status='PASS',topics=15,originals=37,unchanged_topic_records=14,exact_primary_comparisons=comparisons,diagnostics=diag,rendered=render,new_numerical_acceptance_pending=False))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--public-root',type=Path);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='xelatex');a=p.parse_args();build(a.out,a.public_root,a.render,a.xelatex)
