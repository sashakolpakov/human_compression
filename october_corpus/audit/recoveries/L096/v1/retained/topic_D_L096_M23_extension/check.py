#!/usr/bin/env python3
"""Whole-family matching and a complete bounded M23 residue replay; no census."""
import argparse,collections,copy,hashlib,itertools,json,re,shutil,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def need(t,m):
 if not t:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def parse(p,prefix):
 s=p.read_text().replace('\\\n','');need('Error,' not in s and 'Syntax warning' not in s,'GAP diagnostic')
 return [json.loads(x[len(prefix):]) for x in s.splitlines() if x.startswith(prefix)]
def validate(rows):
 need(len(rows)==44 and [r['construction_row'] for r in rows]==list(range(5,49)),'complete prior roster')
 count=types=0
 for r in rows:
  n=3 if r['construction_row']<18 else (4 if r['construction_row']<39 else 5);I=set(range(1,n+1));expected={tuple(c) for k in range(n) for c in itertools.combinations(sorted(I),k)}
  need(r['rank']==n and r['order']==10200960 and r['computed_all_ranks'] and not r['published_label_verified'],'fixed scope')
  need(r['member']=='prior_m23.rk'+str(n) and r['active_row']==r['construction_row']-{3:4,4:17,5:38}[n],'prior identity')
  need(r['retained_RWPRI'] is True and r['retained_RWPRI_basis']=='accepted_complete_phase7_M23_2T_census_exact_representative','retained primitivity premise')
  need(len(r['residues'])==len(expected) and {tuple(x['fixed_types']) for x in r['residues']}==expected,'all proper fixed-type sets')
  for x in r['residues']:
   rest=sorted(I-set(x['fixed_types']));k=len(rest);count+=1
   need(x['types']==rest and x['residue_rank']==k,'residue complement')
   need(x['flag_transitive'] and x['order']*x['flag_orbit_size']==10200960,'actual flag orbit')
   need(x['extension_tests']==k*2**(k-1) and len(x['parabolic_orders'])==k,'every extension and parabolic')
   need(x['primitivity_status']=='retained_from_accepted_exact_family' and 'primitive_types' not in x,'honest uncomputed primitivity')
   if k>=2:
    need(len(x['type_results'])==k and all(type(t) is bool for t in x['type_results']),'all directions')
    need(x['IP']==all(x['type_results']) and x['WIP']==any(x['type_results']),'local quantifiers')
    need(sorted(w['type'] for w in x['negative_witnesses'])==[i for i,t in zip(rest,x['type_results']) if not t],'all negative directions')
    for w in x['negative_witnesses']:
     need(w['intersection_size']==len(w['intersection_representatives'])>1 and len(w['representative'])>0,'actual failed intersection')
    types+=k
   else:need(x['firm']==(x['panel_size']>=2) and x['panel_size']==x['order']//x['parabolic_orders'][0],'panel data')
  br=[]
  for k in range(2,n+1):
   rr=[x for x in r['residues'] if x['residue_rank']==k]
   br.append(dict(rank=k,base_residues=len(rr),actual_residues=sum(x['flag_orbit_size'] for x in rr),IPk=all(x['IP'] for x in rr),WIPk=all(x['WIP'] for x in rr)))
  need(r['by_rank']==br and r['IP']==all(x['IPk'] for x in br) and r['WIP']==all(x['WIPk'] for x in br),'full residual quantifiers')
  panels=[x for x in r['residues'] if x['residue_rank']==1]
  filters=dict(flag_transitive=True,firm=all(x['firm'] for x in panels),residually_connected=all(x['connected'] for x in r['residues']),twoT1=all(x['two_transitive'] for x in panels),IP2=br[0]['IPk'])
  need(r['filters']==filters and r['tested_geometry_checks_pass']==all(filters.values()) and all(filters.values()),'all newly checked geometry hypotheses')
 aggregates={}
 for n in [3,4,5]:
  rr=[r for r in rows if r['rank']==n]
  for k in range(2,n+1):
   a=[next(x for x in r['by_rank'] if x['rank']==k) for r in rr]
   aggregates[f'{n}:{k}']=[sum(x['IPk'] for x in a),sum(x['WIPk'] and not x['IPk'] for x in a),sum(not x['WIPk'] for x in a)]
 expected={'3:2':[13,0,0],'3:3':[5,1,7],'4:2':[21,0,0],'4:3':[5,2,14],'4:4':[3,1,17],'5:2':[10,0,0],'5:3':[2,1,7],'5:4':[1,1,8],'5:5':[1,0,9]}
 need(aggregates==expected,'complete source aggregate rows')
 need((count,types)==(716,1455),'complete coverage counts')
 return dict(rows=44,base_residues_including_panels=count,rank_at_least_two_base_residues=sum(x['residue_rank']>=2 for r in rows for x in r['residues']),type_decisions=types,aggregates=aggregates)
def signature(rows):
 out=copy.deepcopy(rows)
 for r in out:
  for x in r['residues']:
   for k in ['negative_witnesses','orbit_tests','witness_tests']:x.pop(k,None)
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args();o=a.out;need(not o.exists(),'fresh output');o.mkdir(parents=True)
 if (ROOT/'manifest.json').exists():
  for e in load(ROOT/'manifest.json')['exports']:need(sha(ROOT/e['path'])==e['sha256'] and (ROOT/e['path']).stat().st_size==e['bytes'],'frozen export '+e['path'])
 for e in load(ROOT/'bindings.json')['inputs']:
  p=a.study_root/e['path'];need(sha(p)==e['sha256'] and p.stat().st_size==e['bytes'],'retained input '+e['path'])
 base=a.study_root/'topic_D_L096_extended_candidate'
 for n in ['prepare_archive.py']:need((ROOT/n).read_bytes()==(base/n).read_bytes(),'accepted unchanged '+n)
 need((ROOT/'prior_representatives.g').read_bytes()==(a.study_root/'phase7_sporadic_M23_2T_representatives.g').read_bytes(),'complete retained witness file')
 prior=a.study_root/'topic_D_L096_J2_extension/shadow_residues_sparse.g';need((ROOT/'shadow_residues_sparse.g').read_text().replace('accepted_complete_phase7_M23_2T_census_exact_representative','accepted_complete_phase5_J2_census_exact_representative')==prior.read_text(),'exact unchanged mathematical adapter');rows=load(ROOT/'results.json')['rows'];coverage=validate(rows)
 controls=[]
 def reject(name,mutate):
  d=copy.deepcopy(rows);mutate(d)
  try:validate(d)
  except (ValueError,KeyError,IndexError,TypeError):controls.append(name);return
  raise ValueError('accepted mutation '+name)
 reject('drop_complete_prior_case',lambda d:d.pop(19));reject('assume_published_label',lambda d:d[0].update(published_label_verified=True));reject('drop_proper_residue',lambda d:d[0]['residues'].pop());reject('wrong_actual_multiplicity',lambda d:d[0]['residues'][0].update(flag_orbit_size=2));reject('false_FT',lambda d:d[0]['residues'][0].update(flag_transitive=False));reject('erase_retained_RWPRI',lambda d:d[0].update(retained_RWPRI=False));reject('claim_primitivity_retested',lambda d:d[0]['residues'][0].update(primitive_types=[True]));reject('omit_negative_witness',lambda d:next(x for r in d for x in r['residues'] if x.get('negative_witnesses'))['negative_witnesses'].pop());reject('wrong_full_weak_quantifier',lambda d:next(r for r in d if not r['WIP']).update(WIP=True));reject('wrong_panel_size',lambda d:next(x for x in d[19]['residues'] if x['residue_rank']==1).update(panel_size=1));reject('wrong_prior_identity',lambda d:d[0].update(active_row=2));reject('omit_flag_extension',lambda d:d[0]['residues'][0].update(extension_tests=0))
 r=subprocess.run(['/Users/sasha/.venvs/global/bin/python','-B','-O',str(ROOT/'prepare_archive.py'),'--archive',str(a.study_root/'sources/L096_supplementary_archive.tar'),'--out',str(o/'archive_data'),'--members','m23.rk3','m23.rk4','m23.rk5'],capture_output=True,text=True,timeout=30);need(r.returncode==0,r.stderr)
 for n in ['selected_inputs.json','inputs.g','archive_inventory.json']:need((o/'archive_data'/n).read_bytes()==(ROOT/'archive_data'/n).read_bytes(),'literal archive '+n)
 for n in ['shadow_residues_sparse.g','prior_representatives.g','prior_inputs.g','prior_roster.g','match_prior.g','run.g']:shutil.copyfile(ROOT/n,o/n)
 execution=[]
 for f,limit,marker in [('prior_roster.g',30,'PASS_M23_PRIOR_ROSTER'),('match_prior.g',120,'PASS_M23_PRIOR_MATCH'),('run.g',180,'PASS_M23_SHADOWS')]:
  t=time.monotonic();r=subprocess.run(['/opt/homebrew/bin/gap','-q','-b',f],cwd=o,capture_output=True,text=True,timeout=limit);(o/(f+'.stdout.log')).write_text(r.stdout);(o/(f+'.stderr.log')).write_text(r.stderr);need(r.returncode==0 and not r.stderr and marker in r.stdout and 'Error,' not in r.stdout,'clean '+f);execution.append(dict(script=f,seconds=time.monotonic()-t))
 need((o/'prior_inputs.g').read_bytes()==(ROOT/'prior_inputs.g').read_bytes(),'fresh complete prior roster')
 fresh=parse(o/'run.g.stdout.log','RESULT|');validate(fresh);need(signature(fresh)==signature(rows),'all fresh residue decisions')
 matches=[];inp=load(ROOT/'archive_data/selected_inputs.json')
 for line in (o/'match_prior.g.stdout.log').read_text().splitlines():
  if line.startswith('MATCH|'):
   _,member,num,hits,orders=line.split('|');hs=[int(s) for s in re.findall(r'\d+',hits)];need(len(hs)==1,'one actual family match');num=int(num);matches.append(dict(member=member,active_row=num,construction_row=inp[member]['metadata']['active_to_construction'][num-1],prior_class=hs[0]))
 need(matches==load(ROOT/'correspondence.json')['archive_to_prior'],'all 44 exact family correspondences')
 source=[r for r in load(a.study_root/'topic_D_L096_table_contract/source_tables.json')['rows'] if r['group']=='M23'];need(source==load(ROOT/'source_count_rows.json'),'all literal source count rows')
 for sr in source:
  rr=[r for r in rows if r['rank']==sr['rank']]
  pairs=[(r['IP'],r['WIP']) if sr['property_rank']=='full' else next((x['IPk'],x['WIPk']) for x in r['by_rank'] if x['rank']==sr['property_rank']) for r in rr]
  counts=dict(IP=sum(i for i,w in pairs),WIP_only=sum(w and not i for i,w in pairs),not_WIP=sum(not w for i,w in pairs));need(len(rr)==sr['source_total'] and counts==sr['source_counts'],'actual source aggregate comparison')
 freq=collections.Counter(x['prior_class'] for x in matches)
 need(len(matches)==44 and set(freq)==set(range(5,49)),'complete active and retained population')
 need({str(k):v for k,v in freq.items() if v>1}==load(ROOT/'correspondence.json')['duplicate_classes'],'exact duplicate classes')
 if a.render:
  from pypdf import PdfReader
  shutil.copyfile(ROOT/'mathieu_twenty_three_shadows.tex',o/'mathieu_twenty_three_shadows.tex')
  for i in [1,2]:
   r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','mathieu_twenty_three_shadows.tex'],cwd=o,capture_output=True,text=True,timeout=30);(o/f'render{i}.log').write_text(r.stdout+r.stderr);need(r.returncode==0,'render')
  need(not any(x in r.stdout for x in ['Overfull','undefined','Missing character']),'render diagnostics');need([p.extract_text() for p in PdfReader(o/'mathieu_twenty_three_shadows.pdf').pages]==[p.extract_text() for p in PdfReader(ROOT/'mathieu_twenty_three_shadows.pdf').pages],'exact page text')
 report=dict(status='PASS',coverage=coverage,matched_archive_rows=len(matches),duplicate_classes=load(ROOT/'correspondence.json')['duplicate_classes'],retained_J2_sparse_adapter=True,controls=controls,execution=execution,old_census_repeated=False,published_labels_verified=False,full_source_credit=0)
 (o/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
