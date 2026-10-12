#!/usr/bin/env python3
"""Bound the literal J3 roster, exact eligibility, family partition and shadows.
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
 need(r['order']==50232960 and not r['published_label_verified'],'scope/ambient')
 need(len(r['residues'])==len(expected) and {tuple(x['fixed_types']) for x in r['residues']}==expected,'all proper fixed sets')
 for x in r['residues']:
  rest=sorted(I-set(x['fixed_types']));k=len(rest)
  need(x['types']==rest and x['residue_rank']==k,'residue complement')
  need(x['flag_transitive'] and x['order']*x['flag_orbit_size']==50232960,'all actual flag translates')
  need(x['extension_tests']==k*2**(k-1) and len(x['parabolic_orders'])==k,'all extension tests')
  need(x['connected'],'residual connectivity')
  if k==1:need(x['panel_size']==x['order']//x['parabolic_orders'][0] and x['panel_size']>=2 and x['firm'] and x['two_transitive'],'actual panel hypotheses')
 return n

def eligibility(rows):
 need(len(rows)==21,'complete eligibility roster')
 for num,r in enumerate(rows,1):
  n=geometry(r);need(n==3,'literal rank blocks')
  need(not r['computed_all_ranks'] and 'retained_RWPRI' not in r,'actual primitivity and deferred higher shadows')
  for x in r['residues']:
   ts=x['primitive_checked_types'];ds=x['primitive_checked_degrees'];vs=x['primitive_types'];order=sorted(x['types'],key=lambda t:(x['order']//x['parabolic_orders'][x['types'].index(t)],t))
   need(ts==order[:len(ts)] and 1<=len(ts)<=len(order) and ds==[x['order']//x['parabolic_orders'][x['types'].index(t)] for t in ts],'tested primitive type prefix')
   need(len(vs)==len(ts) and all(type(v) is bool for v in vs) and vs[-1] and not any(vs[:-1]),'existential first successful type')
   if num<=0:need(x['primitivity_status']=='computed_actual_coset_actions_in_increasing_index_order' and 'primitive_certificates' not in x,'retained six actual actions')
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
 need(sum(len(r['residues']) for r in rows)==147,'all eligibility residues')
 return dict(entries=21,base_residues=147,direct_action_entries=0,maximality_entries=21)

def partition(f,e):
 rr=f['rows'];need(len(rr)==21 and f['historical_labels_verified'] is False,'partition scope');seen={}
 for num,(r,er) in enumerate(zip(rr,e),1):
  need((r['member'],r['active_row'],r['construction_row'])==(er['member'],er['active_row'],er['construction_row']),'literal row identity')
  k=r['class_id'];rep=r['representative_input_row'];need(1<=rep<=num,'earliest representative')
  if k not in seen:need(k==len(seen)+1 and rep==num,'new class order');seen[k]=r
  need(seen[k]['representative_input_row']==rep,'same representative')
 need(list(seen.values())==f['classes'] and len(seen)==19,'19 exact earliest representatives')
 need(dict(collections.Counter(collections.Counter(r['class_id'] for r in rr).values()))=={1:17,2:2},'whole-family duplicate multiplicities')
 need([(i+1,r['representative_input_row']) for i,r in enumerate(rr) if i+1!=r['representative_input_row']]==[(14,13),(17,16)],'exact duplicate routes')
 return seen

def shadows(rows,e,f):
 need(len(rows)==19,'all distinct shadow families');classes=partition(f,e);count=dirs=0
 for c,r in enumerate(rows,1):
  need(r['shadow_class']==c and r['literal_input_row']==classes[c]['representative_input_row'],'exact representative route');er=e[r['literal_input_row']-1]
  for k in ['active_row','construction_row','member','rank','order','borel_order','parabolic_orders']:need(r[k]==er[k],'eligibility and shadow identity')
  n=geometry(r);need(r['computed_all_ranks'] and r['retained_RWPRI'] and r['retained_RWPRI_basis']=='computed_eligibility_same_literal_J3_input','reuse actual eligibility only')
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
 need((count,dirs)==(133,171),'shadow coverage')
 ag={}
 for n in [3]:
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

def structural_separation(data,rows):
 need([r['row'] for r in data]==[7,8,9,10,11],'entire ambiguous population')
 inv={}
 for r in data:
  need({tuple(x['types']) for x in r['subgroups']}=={tuple(J) for k in range(1,4) for J in itertools.combinations([1,2,3],k)},'all nonempty local intersections')
  inv[r['row']]=[]
  for x in r['subgroups']:
   need(sum(v for o,v in x['class_shape'])==x['order'],'complete conjugacy class shapes')
   if len(x['types'])==1 and x['order']==96:inv[r['row']].append(sum(v for o,v in x['class_shape'] if o==2))
 need(inv=={7:[27],8:[15],9:[27,27],10:[15,15],11:[15,15]},'actual involution distinctions')
 rr={r['literal_input_row']:r for r in rows};need(rr[10]['IP'] and not rr[11]['WIP'],'remaining equal-structure pair distinguished by full IP')
 return inv

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--programs',action='store_true');ap.add_argument('--render',action='store_true');a=ap.parse_args();o=a.out;need(not o.exists(),'fresh output');o.mkdir(parents=True)
 if (ROOT/'manifest.json').exists():
  for b in load(ROOT/'manifest.json')['exports']:need(sha(ROOT/b['path'])==b['sha256'] and (ROOT/b['path']).stat().st_size==b['bytes'],'immutable '+b['path'])
 for b in load(ROOT/'bindings.json')['inputs']:
  p=a.study_root/b['path'];need(sha(p)==b['sha256'] and p.stat().st_size==b['bytes'],'retained '+b['path'])
 for n,old in [('shadow_residues_sparse.g','topic_D_L096_J2_extension'),('actual_maximality.g','topic_D_L096_HS_extension'),('prepare_archive.py','topic_D_L096_extended_candidate')]:need((ROOT/n).read_bytes()==(a.study_root/old/n).read_bytes(),'unchanged '+n)
 e=load(ROOT/'eligibility_results.json')['rows'];f=load(ROOT/'family_partition.json');r=load(ROOT/'shadow_results.json')['rows'];el=eligibility(e);cv=shadows(r,e,f)
 need(profile_text(e)==(ROOT/'intersection_profiles.g').read_text(),'all actual intersection orders')
 er=[]
 for n in ['eligibility_1','eligibility_2_8','eligibility_9_15','eligibility_16_21']:er+=parse(ROOT/'receipts'/n/'stdout.log')
 need(er==e,'complete actual eligibility receipts');need(pairs(ROOT/'receipts/full_partition/stdout.log')==f['rows'],'complete exact partition receipt');need(parse(ROOT/'receipts/all_shadows/stdout.log')==r,'all19 shadow receipts')
 need(pairs(ROOT/'receipts/stalled_full_aut/stdout.log')==f['rows'][:7],'preserved original7 prefix')
 need('VALIDATION|144|24|120' in (ROOT/'receipts/inner_outer_validation/stdout.log').read_text(),'full-Aut reference comparisons')
 structures=parse(ROOT/'receipts/actual_witnesses/local_structure.g.stdout.log','STRUCTURE|');invs=structural_separation(structures,r)
 ws=parse(ROOT/'receipts/actual_witnesses/positive_witnesses.g.stdout.log','WITNESS|');need([x['pair'] for x in ws]==[[14,13],[17,16]],'both actual positive transporters')
 for w in ws:
  need(sorted(w['type_indices'])==[1,2,3] and w['outer_index'] in [1,2],'transporter type/coset')
  need(len(w['automorphism_generator_images'])==len(w['ambient_generators'])>=1,'complete automorphism generator images')
  for perm in [w['inner_conjugator'],*w['automorphism_generator_images'],*w['ambient_generators']]:need(sorted(perm)==list(range(1,6157)),'literal6156-point permutation witness')
 sr=[x for x in load(a.study_root/'topic_D_L096_table_contract/source_tables.json')['rows'] if x['group']=='J3'];need(sr==load(ROOT/'source_count_rows.json') and len(sr)==2,'exact source claims')
 for x in sr:need(x['source_total']==17 and x['source_counts']==dict(IP=5,WIP_only=8,not_WIP=4),'preserved historical counts')
 need(cv['aggregates']['3:full']==dict(IP=6,WIP_only=8,not_WIP=5),'computed supplied-roster counts')
 need(load(ROOT/'scope.json')['historical_labels_verified'] is False and load(ROOT/'scope.json')['source_claimed_classes']==17 and load(ROOT/'scope.json')['exact_Aut_type_classes']==19,'explicit unresolved population correspondence')
 controls=[]
 def reject(name,fun):
  ee,ff,rr=copy.deepcopy((e,f,r));fun(ee,ff,rr)
  try:eligibility(ee);shadows(rr,ee,ff)
  except (ValueError,KeyError,IndexError,TypeError):controls.append(name);return
  raise ValueError('accepted mutation '+name)
 reject('drop_literal',lambda e,f,r:e.pop());reject('drop_class',lambda e,f,r:r.pop());reject('historical_label_assumed',lambda e,f,r:r[0].update(published_label_verified=True));reject('drop_residue',lambda e,f,r:r[0]['residues'].pop());reject('wrong_multiplicity',lambda e,f,r:r[0]['residues'][0].update(flag_orbit_size=2));reject('false_FT',lambda e,f,r:e[0]['residues'][0].update(flag_transitive=False));reject('primitive_without_test',lambda e,f,r:e[0]['residues'][0].update(primitive_checked_types=[]));reject('omit_double_coset',lambda e,f,r:e[0]['residues'][0]['primitive_certificates'][-1].update(outside_double_cosets=999));reject('negative_without_intermediate',lambda e,f,r:next(c for z in e for x in z['residues'] for c in x['primitive_certificates'] if 'intermediate_generators' in c).update(intermediate_generators=[]));reject('omit_shadow_obstruction',lambda e,f,r:next(x for z in r for x in z['residues'] if x.get('negative_witnesses'))['negative_witnesses'].pop());reject('wrong_weak_quantifier',lambda e,f,r:next(z for z in r if not z['WIP']).update(WIP=True));reject('bad_panel_size',lambda e,f,r:next(x for x in e[0]['residues'] if x['residue_rank']==1).update(panel_size=1));reject('wrong_representative',lambda e,f,r:r[0].update(literal_input_row=2));reject('merge_distinct_classes',lambda e,f,r:f['rows'][0].update(class_id=2));reject('invent_prior_RWPRI',lambda e,f,r:e[0].update(retained_RWPRI=True));reject('wrong_full_IP',lambda e,f,r:r[0].update(IP=not r[0]['IP']))
 bad=copy.deepcopy(structures);next(x for x in bad[0]['subgroups'] if len(x['types'])==1 and x['order']==96)['class_shape'][0][1]+=1
 try:structural_separation(bad,r)
 except ValueError:controls.append('corrupt_conjugacy_class_shape')
 else:raise ValueError('accepted bad structural count')
 q=subprocess.run(['/Users/sasha/.venvs/global/bin/python','-B','-O',str(ROOT/'prepare_archive.py'),'--archive',str(a.study_root/'sources/L096_supplementary_archive.tar'),'--out',str(o/'archive_data'),'--members','j3.rk3'],capture_output=True,text=True,timeout=30);need(q.returncode==0,q.stderr)
 for n in ['selected_inputs.json','inputs.g','archive_inventory.json']:need((o/'archive_data'/n).read_bytes()==(ROOT/'archive_data'/n).read_bytes(),'literal archive '+n)
 execution=[]
 if a.programs:
  for p in ROOT.glob('*.g'):shutil.copyfile(p,o/p.name)
  for script,limit,marker in [('validate_inner_outer.g',30,'PASS_INNER_OUTER_VALIDATION'),('partition_inner_outer.g',120,'PASS_J3_WHOLE_FAMILY_PARTITION'),('positive_witnesses.g',90,'PASS_J3_ACTUAL_POSITIVE_WITNESSES'),('local_structure.g',30,'PASS_LOCAL_STRUCTURE'),('shadows.g',120,'PASS_J3_ALL_CLASS_SHADOWS')]:
   t=time.monotonic();q=subprocess.run(['/opt/homebrew/bin/gap','-q','-b',script],cwd=o,capture_output=True,text=True,timeout=limit);(o/(script+'.stdout.log')).write_text(q.stdout);(o/(script+'.stderr.log')).write_text(q.stderr);need(q.returncode==0 and not q.stderr and marker in q.stdout and 'Error,' not in q.stdout,'fresh clean '+script);execution.append(dict(script=script,seconds=time.monotonic()-t))
  need(pairs(o/'partition_inner_outer.g.stdout.log')==f['rows'],'fresh exact family partition');nr=parse(o/'shadows.g.stdout.log');shadows(nr,e,f);need(signature(nr)==signature(r),'all fresh shadow truths');need(parse(o/'local_structure.g.stdout.log','STRUCTURE|')==structures,'all actual local group invariants');structural_separation(structures,nr)
 if a.render:
  from pypdf import PdfReader
  shutil.copyfile(ROOT/'third_janko_shadows.tex',o/'third_janko_shadows.tex')
  for k in [1,2]:
   q=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','third_janko_shadows.tex'],cwd=o,capture_output=True,text=True,timeout=30);(o/f'render{k}.log').write_text(q.stdout+q.stderr);need(q.returncode==0,'render')
  need(not any(x in q.stdout for x in ['Overfull','undefined','Missing character']),'render diagnostics');need([x.extract_text() for x in PdfReader(ROOT/'third_janko_shadows.pdf').pages]==[x.extract_text() for x in PdfReader(o/'third_janko_shadows.pdf').pages],'identical pages')
 report=dict(status='PASS',eligibility=el,coverage=cv,classes=19,source_claim=17,discrepancy_preserved=True,local_involution_counts=invs,explicit_positive_transporters=2,controls=controls,execution=execution,old_census_repeated=False,historical_labels_verified=False,whole_source_credit=0)
 (o/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
