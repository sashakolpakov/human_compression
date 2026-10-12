#!/usr/bin/env python3
"""Bound the literal HS roster, exact eligibility, family partition and shadows.
Default: verify retained complete executions and every residual quantifier.
--programs: fresh exact maximality, full optimized partition and all shadows.
No classification census is run; no historical geometry suffix is inferred.
"""
import argparse,collections,copy,hashlib,itertools,json,re,shutil,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def parse(p,prefix='RESULT|'):
 s=p.read_text().replace('\\\n','');need('Error,' not in s and 'Syntax warning' not in s,'GAP diagnostic')
 return [json.loads(x[len(prefix):]) for x in s.splitlines() if x.startswith(prefix)]
def pairs(p):
 ans=[]
 for line in p.read_text().splitlines():
  if line.startswith('MATCH|'):
   _,m,a,c,k,r=line.split('|');ans.append(dict(member=m,active_row=int(a),construction_row=int(c),class_id=int(k),representative_input_row=int(r)))
 return ans

def geometry(r):
 n=r['rank'];I=set(range(1,n+1));expected={tuple(c) for k in range(n) for c in itertools.combinations(sorted(I),k)}
 need(r['order']==44352000 and not r['published_label_verified'],'scope/ambient')
 need(len(r['residues'])==len(expected) and {tuple(x['fixed_types']) for x in r['residues']}==expected,'all proper fixed sets')
 for x in r['residues']:
  rest=sorted(I-set(x['fixed_types']));k=len(rest)
  need(x['types']==rest and x['residue_rank']==k,'residue complement')
  need(x['flag_transitive'] and x['order']*x['flag_orbit_size']==44352000,'all actual flag translates')
  need(x['extension_tests']==k*2**(k-1) and len(x['parabolic_orders'])==k,'all extension tests')
  need(x['connected'],'residual connectivity')
  if k==1:need(x['panel_size']==x['order']//x['parabolic_orders'][0] and x['panel_size']>=2 and x['firm'] and x['two_transitive'],'actual panel hypotheses')
 return n

def eligibility(rows):
 need(len(rows)==124,'complete eligibility roster')
 for num,r in enumerate(rows,1):
  n=geometry(r);need(n==(3 if num<=44 else 4 if num<=111 else 5 if num<=123 else 6),'literal rank blocks')
  need(not r['computed_all_ranks'] and 'retained_RWPRI' not in r,'actual primitivity and deferred higher shadows')
  for x in r['residues']:
   ts=x['primitive_checked_types'];ds=x['primitive_checked_degrees'];vs=x['primitive_types'];order=sorted(x['types'],key=lambda t:(x['order']//x['parabolic_orders'][x['types'].index(t)],t))
   need(ts==order[:len(ts)] and 1<=len(ts)<=len(order) and ds==[x['order']//x['parabolic_orders'][x['types'].index(t)] for t in ts],'tested primitive type prefix')
   need(len(vs)==len(ts) and all(type(v) is bool for v in vs) and vs[-1] and not any(vs[:-1]),'existential first successful type')
   if num<=6:need(x['primitivity_status']=='computed_actual_coset_actions_in_increasing_index_order' and 'primitive_certificates' not in x,'retained six actual actions')
   else:
    need(x['primitivity_status']=='computed_exact_double_coset_maximality' and len(x['primitive_certificates'])==len(ts),'complete maximality certificates')
    for c,d,v in zip(x['primitive_certificates'],ds,vs):
     need(c['index']==d and c['value']==v,'certificate identity')
     if d==1:need(not v and c['reason']=='degree_one_excluded' and c['tested']==0,'exclude vacuous index-one primitive action')
     else:
      need(c['tested']==len(c['generated_orders'])>=1 and c['outside_double_cosets']>=c['tested'],'outside roster length')
      if v:need(c['tested']==c['outside_double_cosets'] and all(z==x['order'] for z in c['generated_orders']),'all outside representatives generate')
      else:need(d>1 and x['order']//d<c['intermediate_order']<x['order'] and c['generated_orders'][-1]==c['intermediate_order'] and c['outside_representative'] and c['intermediate_generators'],'proper intermediate witness')
   if x['residue_rank']==2:need(x['type_results']==[True,True] and x['IP'] and x['WIP'],'every rank-two intersection test')
  need(r['filters']==dict(IP2=True,RWPRI=True,firm=True,flag_transitive=True,residually_connected=True,twoT1=True) and r['source_filter_pass'] and r['tested_geometry_checks_pass'],'all actual source filters')
 need(sum(len(r['residues']) for r in rows)==1748,'all eligibility residues')
 return dict(entries=124,base_residues=1748,direct_action_entries=6,maximality_entries=118)

def partition(f,e):
 rr=f['rows'];need(len(rr)==124 and f['historical_names_verified'] is False and f['census_completeness_retained_source_only'] is True,'partition scope')
 seen={}
 for num,(r,er) in enumerate(zip(rr,e),1):
  need((r['member'],r['active_row'],r['construction_row'])==(er['member'],er['active_row'],er['construction_row']),'literal row identity')
  k=r['class_id'];rep=r['representative_input_row'];need(1<=rep<=num,'earliest representative')
  if k not in seen:need(k==len(seen)+1 and rep==num,'new class order');seen[k]=r
  need(seen[k]['representative_input_row']==rep,'same representative')
 need(list(seen.values())==f['classes'] and len(seen)==80,'80 exact earliest representatives')
 need(dict(collections.Counter(e[r['representative_input_row']-1]['rank'] for r in f['classes']))=={3:30,4:41,5:8,6:1},'class rank counts')
 need(dict(collections.Counter(collections.Counter(r['class_id'] for r in rr).values()))=={1:36,2:44},'whole-family duplicate multiplicities')
 return seen

def shadows(rows,e,f):
 need(len(rows)==80,'all distinct shadow families');classes=partition(f,e);count=dirs=0
 for c,r in enumerate(rows,1):
  need(r['shadow_class']==c and r['literal_input_row']==classes[c]['representative_input_row'],'exact representative route');er=e[r['literal_input_row']-1]
  for k in ['active_row','construction_row','member','rank','order','borel_order','parabolic_orders']:need(r[k]==er[k],'eligibility and shadow identity')
  n=geometry(r);need(r['computed_all_ranks'] and r['retained_RWPRI'] and r['retained_RWPRI_basis']=='computed_eligibility_same_literal_HS_input','reuse actual eligibility only')
  byfixed={tuple(x['fixed_types']):x for x in er['residues']}
  for x in r['residues']:
   ex=byfixed[tuple(x['fixed_types'])]
   for k in ['order','parabolic_orders','flag_transitive','flag_orbit_size','connected','extension_tests']:need(x[k]==ex[k],'same actual residue')
   need(x['primitivity_status']=='reused_actual_eligibility_same_literal_input','honest reused primitivity');count+=1;k=x['residue_rank']
   if k>=2:
    need(len(x['type_results'])==k and all(type(t) is bool for t in x['type_results']),'all shadow directions')
    need(x['IP']==all(x['type_results']) and x['WIP']==any(x['type_results']),'local all/exists quantifiers')
    need(sorted(w['type'] for w in x['negative_witnesses'])==[t for t,v in zip(x['types'],x['type_results']) if not v],'all negative witnesses')
    for w in x['negative_witnesses']:need(w['intersection_size']==len(w['intersection_representatives'])>1 and w['representative'],'nonempty nonsingleton obstruction')
    dirs+=k
  br=[]
  for k in range(2,n+1):
   xx=[x for x in r['residues'] if x['residue_rank']==k];br.append(dict(rank=k,base_residues=len(xx),actual_residues=sum(x['flag_orbit_size'] for x in xx),IPk=all(x['IP'] for x in xx),WIPk=all(x['WIP'] for x in xx)))
  need(r['by_rank']==br and r['IP']==all(x['IPk'] for x in br) and r['WIP']==all(x['WIPk'] for x in br),'all ranks and actual translates')
 need((count,dirs)==(1136,2204),'shadow coverage')
 ag={}
 for n in range(3,7):
  rr=[r for r in rows if r['rank']==n]
  for k in [*range(2,n+1),'full']:
   v=[(r['IP'],r['WIP']) if k=='full' else next((x['IPk'],x['WIPk']) for x in r['by_rank'] if x['rank']==k) for r in rr]
   ag[f'{n}:{k}']=dict(IP=sum(i for i,w in v),WIP_only=sum(w and not i for i,w in v),not_WIP=sum(not w for i,w in v))
 return dict(base_residues_including_panels=count,rank_at_least_two_base_residues=sum(x['residue_rank']>=2 for r in rows for x in r['residues']),directions=dirs,aggregates=ag)

def profile_text(e):
 out=[]
 for r in e:
  keys=[x['fixed_types'] for x in r['residues']]+[list(range(1,r['rank']+1))];orders=[x['order'] for x in r['residues']]+[r['borel_order']]
  out.append('rec(keys:='+str(keys)+',orders:='+str(orders)+')')
 return 'L096Profiles:=['+',\n'.join(out)+'];;\n'

def signature(rows):
 rows=copy.deepcopy(rows)
 for r in rows:
  for x in r['residues']:
   for k in ['negative_witnesses','orbit_tests','witness_tests']:x.pop(k,None)
 return rows

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--programs',action='store_true');ap.add_argument('--render',action='store_true');a=ap.parse_args();o=a.out;need(not o.exists(),'fresh output');o.mkdir(parents=True)
 if (ROOT/'manifest.json').exists():
  for b in load(ROOT/'manifest.json')['exports']:need(sha(ROOT/b['path'])==b['sha256'] and (ROOT/b['path']).stat().st_size==b['bytes'],'immutable '+b['path'])
 for b in load(ROOT/'bindings.json')['inputs']:
  p=a.study_root/b['path'];need(sha(p)==b['sha256'] and p.stat().st_size==b['bytes'],'retained '+b['path'])
 need((ROOT/'shadow_residues_sparse.g').read_bytes()==(a.study_root/'topic_D_L096_J2_extension/shadow_residues_sparse.g').read_bytes(),'exact unchanged sparse mathematics')
 need((ROOT/'prepare_archive.py').read_bytes()==(a.study_root/'topic_D_L096_extended_candidate/prepare_archive.py').read_bytes(),'unchanged literal parser')
 e=load(ROOT/'eligibility_results.json')['rows'];f=load(ROOT/'family_partition.json');r=load(ROOT/'shadow_results.json')['rows'];el=eligibility(e);cv=shadows(r,e,f)
 need(profile_text(e)==(ROOT/'intersection_profiles.g').read_text(),'all actual intersection-order profiles')
 er=parse(ROOT/'receipts/direct_first_six/stdout.log')+parse(ROOT/'receipts/maximality_remaining/stdout.log');need(e==er,'exact complete eligibility execution receipts')
 fr=pairs(ROOT/'receipts/family_first_31/stdout.log')+pairs(ROOT/'receipts/family_remaining/stdout.log');need(fr==f['rows'],'unchanged 31-prefix and exact new93 matches')
 need(parse(ROOT/'receipts/shadows_all/stdout.log')==r,'all80 shadow execution receipts')
 need('PASS_ACTUAL_MAXIMALITY_VALIDATION' in (ROOT/'receipts/maximality_validation/stdout.log').read_text(),'31 actual-action comparison')
 need('PASS_PROFILE_MATCHING' in (ROOT/'receipts/matcher_validation/stdout.log').read_text(),'30 discriminating matcher comparisons')
 sr=[x for x in load(a.study_root/'topic_D_L096_table_contract/source_tables.json')['rows'] if x['group']=='HS'];need(sr==load(ROOT/'source_count_rows.json') and len(sr)==13,'literal source rows')
 for x in sr:need(cv['aggregates'][str(x['rank'])+':'+str(x['property_rank'])]==x['source_counts'] and sum(y['rank']==x['rank'] for y in r)==x['source_total'],'source count comparison')
 need(cv['aggregates']['6:6']==dict(IP=0,WIP_only=0,not_WIP=1),'rank-six source statement')
 controls=[]
 def reject(name,fun):
  ee,ff,rr=copy.deepcopy((e,f,r));fun(ee,ff,rr)
  try:eligibility(ee);shadows(rr,ee,ff)
  except (ValueError,KeyError,IndexError,TypeError):controls.append(name);return
  raise ValueError('accepted mutation '+name)
 reject('drop_literal_input',lambda e,f,r:e.pop());reject('drop_distinct_shadow',lambda e,f,r:r.pop());reject('claim_historical_name',lambda e,f,r:r[0].update(published_label_verified=True));reject('drop_residue',lambda e,f,r:r[0]['residues'].pop());reject('bad_flag_multiplicity',lambda e,f,r:r[0]['residues'][0].update(flag_orbit_size=2));reject('false_FT',lambda e,f,r:e[0]['residues'][0].update(flag_transitive=False));reject('fake_actual_primitive_type',lambda e,f,r:e[6]['residues'][0]['primitive_types'].__setitem__(-1,False));reject('missing_outside_double_coset',lambda e,f,r:e[6]['residues'][0]['primitive_certificates'][-1].update(outside_double_cosets=99999));reject('missing_intermediate_witness',lambda e,f,r:next(c for z in e[6:] for x in z['residues'] for c in x['primitive_certificates'] if 'intermediate_generators' in c).update(intermediate_generators=[]));reject('drop_negative_shadow_witness',lambda e,f,r:next(x for z in r for x in z['residues'] if x.get('negative_witnesses'))['negative_witnesses'].pop());reject('wrong_weak_quantifier',lambda e,f,r:next(z for z in r if not z['WIP']).update(WIP=True));reject('wrong_panel_size',lambda e,f,r:next(x for x in e[0]['residues'] if x['residue_rank']==1).update(panel_size=1));reject('bad_representative_route',lambda e,f,r:r[0].update(literal_input_row=2));reject('merge_distinct_class',lambda e,f,r:f['rows'][0].update(class_id=2));reject('alter_eligibility_scope',lambda e,f,r:e[0].update(computed_all_ranks=True));reject('claim_retained_prior_RWPRI',lambda e,f,r:e[0].update(retained_RWPRI=True));reject('empty_primitive_test_prefix',lambda e,f,r:e[0]['residues'][0].update(primitive_checked_types=[]));reject('wrong_full_residue_IP',lambda e,f,r:r[0].update(IP=not r[0]['IP']))
 q=subprocess.run(['/Users/sasha/.venvs/global/bin/python','-B','-O',str(ROOT/'prepare_archive.py'),'--archive',str(a.study_root/'sources/L096_supplementary_archive.tar'),'--out',str(o/'archive_data'),'--members','hs.rk3','hs.rk4','hs.rk5','hs.rk6'],capture_output=True,text=True,timeout=30);need(q.returncode==0,q.stderr)
 for n in ['selected_inputs.json','inputs.g','archive_inventory.json']:need((o/'archive_data'/n).read_bytes()==(ROOT/'archive_data'/n).read_bytes(),'source literal '+n)
 execution=[]
 if a.programs:
  for p in ROOT.glob('*.g'):shutil.copyfile(p,o/p.name)
  # Preserve the original six direct-action outputs as a distinct route; this
  # optional full maximality replay compares all truth values, not algorithms.
  ss=(ROOT/'eligibility_remaining.g').read_text().replace('[7..Length(L096Inputs)]','[1..Length(L096Inputs)]');(o/'eligibility_fresh.g').write_text(ss)
  for script,limit,marker in [('eligibility_fresh.g',180,'PASS_HS_REMAINING_ELIGIBILITY'),('partition_complete.g',180,'PASS_HS_WHOLE_FAMILY_PARTITION'),('shadows.g',90,'PASS_HS_ALL_CLASS_SHADOWS')]:
   t=time.monotonic();q=subprocess.run(['/opt/homebrew/bin/gap','-q','-b',script],cwd=o,capture_output=True,text=True,timeout=limit);(o/(script+'.stdout.log')).write_text(q.stdout);(o/(script+'.stderr.log')).write_text(q.stderr);need(q.returncode==0 and not q.stderr and marker in q.stdout and 'Error,' not in q.stdout,'fresh clean '+script);execution.append(dict(script=script,seconds=time.monotonic()-t))
  ne=parse(o/'eligibility_fresh.g.stdout.log');need(len(ne)==124,'fresh all124 eligibility')
  for x,y in zip(ne,e):
   need(x['filters']==y['filters'] and x['source_filter_pass']==y['source_filter_pass'],'fresh actual eligibility')
   for a1,b1 in zip(x['residues'],y['residues']):
    for key in ['fixed_types','order','parabolic_orders','primitive_checked_types','primitive_types','primitive_checked_degrees']:need(a1[key]==b1[key],'fresh primitive predicate')
  need(pairs(o/'partition_complete.g.stdout.log')==f['rows'],'fresh full optimized family partition');nr=parse(o/'shadows.g.stdout.log');shadows(nr,e,f);need(signature(nr)==signature(r),'fresh all shadow truths')
 if a.render:
  from pypdf import PdfReader
  for n in ['higman_sims_shadows.tex','maximality_criterion.tex','matching_criterion.tex']:shutil.copyfile(ROOT/n,o/n)
  for k in [1,2]:
   q=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','higman_sims_shadows.tex'],cwd=o,capture_output=True,text=True,timeout=30);(o/f'render{k}.log').write_text(q.stdout+q.stderr);need(q.returncode==0,'render')
  need(not any(x in q.stdout for x in ['Overfull','undefined','Missing character']),'render diagnostics');need([x.extract_text() for x in PdfReader(ROOT/'higman_sims_shadows.pdf').pages]==[x.extract_text() for x in PdfReader(o/'higman_sims_shadows.pdf').pages],'identical page texts')
 report=dict(status='PASS',eligibility=el,coverage=cv,controls=controls,source_count_rows=13,rank_six_statement=True,whole_family_classes=80,execution=execution,historical_labels_verified=False,retained_global_classification=True,new_census=False,new_Lean=0,whole_source_credit=0)
 (o/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
