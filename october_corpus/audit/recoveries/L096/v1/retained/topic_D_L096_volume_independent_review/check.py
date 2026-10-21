#!/usr/bin/env python3
"""Independent L096 assembly review. Reads saved exact data; imports no author code."""
from pathlib import Path
import argparse,copy,hashlib,itertools,json,math,re

FILES={'M11':'topic_D_L096_extended_candidate/mathieu_results.json','M12':'topic_D_L096_extended_candidate/mathieu_results.json','J1':'topic_D_L096_J1_extension/results.json','J2':'topic_D_L096_J2_extension/results.json','M22':'topic_D_L096_M22_extension/results.json','M23':'topic_D_L096_M23_extension/results.json','HS':'topic_D_L096_HS_extension/shadow_results.json','J3':'topic_D_L096_J3_extension/shadow_results.json'}
# Fresh transcription of Tables1/3/5/7. Each list is k=3,...,rank,full.
PRINTED={('M11',3):(13,[(6,1,6)]*2),('M11',4):(11,[(2,0,9)]*3),('M12',3):(18,[(7,1,10)]*2),('M12',4):(18,[(4,0,14),(3,0,15),(3,0,15)]),('M12',5):(1,[(1,0,0),(1,0,0),(0,0,1),(0,0,1)]),('M22',3):(25,[(5,8,12)]*2),('M22',4):(16,[(5,4,7),(3,1,12),(3,1,12)]),('M22',5):(9,[(0,1,8)]*4),('M23',3):(13,[(5,1,7)]*2),('M23',4):(21,[(5,2,14),(3,1,17),(3,1,17)]),('M23',5):(10,[(2,1,7),(1,1,8),(1,0,9),(1,0,9)]),('J1',3):(1,[(0,0,1)]*2),('J1',4):(2,[(1,0,1)]*3),('J2',3):(19,[(8,3,8)]*2),('J2',4):(3,[(1,0,2)]*3),('J3',3):(17,[(5,8,4)]*2),('HS',3):(30,[(8,5,17)]*2),('HS',4):(41,[(8,1,32),(5,0,36),(5,0,36)]),('HS',5):(8,[(1,0,7),(1,0,7),(0,1,7),(0,1,7)]),('HS',6):(1,[(0,0,1)]*5)}
# Literal source positive labels, independently transcribed. Empty means no positive assertion.
LABEL3={('M11',3):('3 5 11 12 13 18','4'),('M11',4):('1 4',''),('M12',3):('2 4 5 7 9 16 19','6'),('M12',4):('9 12 19 20',''),('M12',5):('1',''),('M22',3):('1 3 6 12 24','7 8 11 13 17 18 23 25'),('M22',4):('3 9 14 15 16','8 11 12 13'),('M22',5):('','2'),('M23',3):('2 3 5 6 9','13'),('M23',4):('2 4 8 17 19','11 12'),('M23',5):('3 9','8'),('J1',3):('',''),('J1',4):('1',''),('J2',3):('1 2 3 4 9 16 17 18','7 8 10'),('J2',4):('2',''),('J3',3):('2 3 4 7 9','1 5 6 10 13 14 15 17'),('HS',3):('2 4 7 13 14 19 24 25','1 10 20 28 29'),('HS',4):('1 3 5 7 8 14 15 16','40'),('HS',5):('6',''),('HS',6):('','')}
LABEL4={('M11',4):('1 4',''),('M12',4):('9 19 20',''),('M12',5):('1',''),('M22',4):('3 9 14','11'),('M22',5):('','2'),('M23',4):('2 8 19','11'),('M23',5):('3','9'),('J1',4):('1',''),('J2',4):('2',''),('HS',4):('1 3 7 8 14',''),('HS',5):('6',''),('HS',6):('','')}
LABEL5={('M12',5):('',''),('M22',5):('','2'),('M23',5):('3',''),('HS',5):('','6'),('HS',6):('','')}
def need(v,m):
 if not v:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def bind(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def exact(root,row):
 need(bind(root/row['path'])=={k:row[k] for k in ['bytes','sha256']},'binding '+row['path'])
def subsets(n):return {s for k in range(n) for s in itertools.combinations(range(1,n+1),k)}
def rowcheck(r):
 n=r['rank'];need(n>=2,'rank domain');R=r['residues'];S=[tuple(x['fixed_types']) for x in R]
 need(len(S)==len(set(S)) and set(S)==subsets(n),'exact fixed-type universe')
 out=[]
 for x in R:
  need(x['types']==[i for i in range(1,n+1) if i not in x['fixed_types']],'remaining type complement')
  k=n-len(x['fixed_types']);need(x['residue_rank']==k,'residue rank')
  need(r['order']%x['order']==0 and x['flag_orbit_size']==r['order']//x['order'],'actual flag orbit')
  if k>=2:
   ts=x['type_results'];need(len(ts)==k and all(type(v)is bool for v in ts),'all direction decisions')
   need(x['IP']==all(ts) and x['WIP']==any(ts),'local all/exists')
 for k in range(2,n+1):
  rr=[x for x in R if x['residue_rank']==k];ip=all(all(x['type_results']) for x in rr);wp=all(any(x['type_results']) for x in rr)
  old=[x for x in r['by_rank'] if x['rank']==k];need(len(old)==1,'rank report uniqueness');old=old[0]
  need(old['IPk']==ip and old['WIPk']==wp,'all residues, locally existential type')
  need(old['base_residues']==math.comb(n,k) and old['actual_residues']==sum(x['flag_orbit_size'] for x in rr),'base/actual residue count')
  out.append({'rank':k,'IPk':ip,'WIPk':wp})
 need(r['IP']==all(x['IPk'] for x in out) and r['WIP']==all(x['WIPk'] for x in out),'full residual quantifier')
 need(all(type(v)is bool for v in r['filters'].values()),'actual boolean eligibility')
 return out

def science_scope(d):
 need(d['full_source_recovered']is False and d['new_original_credit']==0 and d['new_conjecture_credit']==0 and d['measurements']is None,'partial scope only')
 need(d['old_topic_D_common_paid_whole']is True and d['new_common_paid_whole']is True,'whole common dependencies')

def required_layer(inv):
 rows={x['path']:x for x in inv['all_occurrences']}
 expected={'topic_D_L096_volume_v2/assemble.py':'required_aggregate_reconstruction_program','topic_D_L096_volume_v2/build_boundary.py':'operational_whole_file_inventory_driver','topic_D_L096_volume_v2/check.py':'operational_integrity_and_render_checker','topic_D_L096_table_contract/source_tables.json':'required_source_contract_data'}
 expected.update({p:'required_mathematical_directional_results' for p in sorted(set(FILES.values()))})
 for p,role in expected.items():need(p in rows and rows[p]['role']==role and rows[p]['whole_file']is True,'whole current layer '+p)
 return expected

def delta(root,packet,inv):
 old=root/'topic_D_L096_volume';m=load(old/'manifest.json');need(bind(old/'manifest.json')['sha256']=='934e09aca01eb7d780713a06e366df2fa15beac87280ada16fcc9265cc92d538','original immutable pin')
 changes=[]
 for x in m['exports']:
  exact(old,x)
  if (old/x['path']).read_bytes()!=(packet/x['path']).read_bytes():changes.append(x['path'])
 need(set(changes)=={'README.rst','author_replay.json','build_boundary.py','check.py','scope.json','whole_program_inventory.json'},'exact metadata/code delta')
 oldinv=load(old/'whole_program_inventory.json');need(inv['all_occurrences'][:859]==oldinv['all_occurrences'],'all inherited roles unchanged')
 req=required_layer(inv);added=inv['all_occurrences'][859:];need(len(added)==11 and {x['path'] for x in added}==set(req),'exact eleven added files')
 return {'unchanged_original_exports':len(m['exports'])-len(changes),'changed_original_exports':changes,'added_whole_file_occurrences':11}

def migration(root,packet):
 count=0
 def bodies(s):
  raw=re.findall(r'\\begin\{proof\}(.*?)\\end\{proof\}',s,re.S)
  return [re.sub(r'\s+',' ',x.replace('U-','').replace('thin-triples','thin').replace('thin-recognize','recognize')).strip() for x in raw]
 for x in load(packet/'migration.json')['fragments']:
  exact(root,x['source']);text=(root/x['source']['path']).read_text();target=(packet/x['target']).read_text()
  need(hashlib.sha256(target.encode()).hexdigest()==x['target_sha256'],'migration target hash')
  if 'source_start' in x:
   fragment=text[text.index(x['source_start']):text.index(x['source_end_exclusive'])]
   need(hashlib.sha256(fragment.encode()).hexdigest()==x['source_snippet_sha256'],'entire source snippet')
   need(bodies(fragment)==bodies(target),'complete migrated proof bodies')
   if x['literal_equal']:need(fragment==target,'literal full migration')
   count+=len(bodies(fragment))
 need(count==14,'all fourteen migrated proofs')
 return count

def evaluate(root,packet):
 m=load(packet/'manifest.json');[exact(packet,x) for x in m['exports']]
 dep=load(packet/'accepted_dependencies.json');binding_count=0
 for c in dep['accepted_components']:
  exact(root,c['author_manifest']);exact(root,c['accepted_by']);binding_count+=2
 for x in dep['all_frozen_component_exports']:exact(root,x);binding_count+=1
 for c in dep['retained_complete_censuses']:
  exact(root,c['certificate']);binding_count+=1
  for x in c['complete_artifact_bindings']:exact(root,x);binding_count+=1
 proof_count=migration(root,packet)
 d=load(packet/'combined_results.json');science_scope(load(packet/'scope.json'));classes={};allrows=[];rejected=[];nr=nt=actual=0
 for g,path in FILES.items():
  rows=load(root/path)['rows']
  if g in ['M11','M12']:rows=[r for r in rows if r['member'].startswith(g.lower()+'.')]
  for r in rows:
   q=rowcheck(r);allrows.append(r);nr+=len(r['residues']);nt+=sum(len(x.get('type_results',[])) for x in r['residues']);actual+=sum(x['flag_orbit_size'] for x in r['residues'])
   if not all(r['filters'].values()):rejected.append((g,r['rank'],r['active_row']));continue
   need(r['filters'].get('RWPRI',r.get('retained_RWPRI',False))is True,'RWPRI premise')
   key=(g,r['rank'],r['active_row']);need(key not in classes,'unique representative');classes[key]=(r,q)
 need(len(classes)==278,'278 current classes');need(sorted(rejected)==[('M12',3,15),('M12',3,17),('M12',3,20),('M12',4,4),('M12',4,7)],'five excluded Mathieu rows')
 need(len(d['classes'])==278,'aggregate completeness')
 for c in d['classes']:
  key=(c['group'],c['rank'],c['active']);need(key in classes,'actual representative');r,q=classes[key]
  for ck,rk in [('member','member'),('construction','construction_row'),('order','order'),('borel_order','borel_order'),('parabolic_orders','parabolic_orders'),('IP','IP'),('WIP','WIP')]:need(c[ck]==r[rk],'aggregate '+ck)
  need(c['by_rank']==q and c['historical_label']is None,'aggregate quantifier/unknown label')
  need(c['base_residues_including_panels']==len(r['residues']) and c['rank_at_least_two_residues']==sum(x['residue_rank']>=2 for x in r['residues']) and c['direction_decisions']==sum(len(x.get('type_results',[])) for x in r['residues']),'aggregate extent')
 expected={};expectedlabels=[]
 for (g,n),(total,triples) in PRINTED.items():
  ks=list(range(3,n+1))+['full']
  for k,t in zip(ks,triples):
   if k==6:continue # Source's separate negative HS6.1 sentence, not a table row.
   expected[g,n,k]=(total,t)
   lab=LABEL3[g,n] if k==3 else LABEL4[g,n] if k==4 else LABEL5[g,n] if k==5 else (LABEL3[g,n] if n==3 else LABEL4[g,n] if n==4 else LABEL5[g,n] if n==5 else ('',''))
   for words,claim in zip(lab,['IP','WIP_ONLY']):
    expectedlabels.extend((g,n,f'{n}.{j}',k,claim) for j in words.split())
 need(len(expected)==57,'independent57');need(len(d['comparisons'])==57,'reported57');agrees=0
 for c in d['comparisons']:
  key=(c['group'],c['rank'],c['property_rank']);need(key in expected,'source table key');tot,triple=expected[key]
  need(c['source_total']==tot and tuple(c['source_counts'][x] for x in ['IP','WIP_only','not_WIP'])==triple,'literal source counts')
  rr=[(r,q) for (g,n,a),(r,q) in classes.items() if (g,n)==key[:2]];pred=[(r['IP'],r['WIP']) if key[2]=='full' else next((x['IPk'],x['WIPk']) for x in q if x['rank']==key[2]) for r,q in rr]
  got=(sum(i for i,w in pred),sum(w and not i for i,w in pred),sum(not w for i,w in pred))
  need(c['computed_total']==len(rr) and tuple(c['computed_counts'][x] for x in ['IP','WIP_only','not_WIP'])==got,'independent aggregate counts')
  same=got==triple and len(rr)==tot;need(c['count_agrees']==same,'agreement flag');agrees+=same
 need(agrees==53,'exact four source differences')
 labels=load(packet/'historical_label_claims.json')['claims'];need(len(labels)==232,'positive-label occurrence boundary')
 need(sorted((x['group'],x['rank'],x['label'],str(x['property_rank']),x['claim']) for x in labels)==sorted((g,n,l,str(k),c) for g,n,l,k,c in expectedlabels),'literal positive-label transcription')
 need(all(x['current_family']is None and x['status']=='NO_VERIFIED_HISTORICAL_CORRESPONDENCE' for x in labels),'historical correspondence unresolved')
 sm=load(packet/'source_map.json');need(len(sm['main_and_count_clauses'])==73 and len({x['id'] for x in sm['main_and_count_clauses']})==73,'73 distinct source dispositions');need(sm['historical_label_claims']==labels,'source label coverage');need(sm['full_source_recovered']is False,'no whole source credit')
 for field in ['primary','primary_text']:exact(root,sm[field])
 inv=load(packet/'whole_program_inventory.json');[exact(root,x) for x in inv['all_occurrences']]
 groups={}
 for x in inv['all_occurrences']:groups.setdefault(x['sha256'],[]).append(x)
 need(len(groups)==len(inv['unique_contents']),'distinct-content inventory')
 for x in inv['unique_contents']:
  rr=groups[x['sha256']];need(x['bytes']==rr[0]['bytes'] and x['paths']==sorted({r['path'] for r in rr}) and x['roles']==sorted({r['role'] for r in rr}),'union of whole-file paths/roles')
 need(inv['measurement_factor']is None and inv['external_software_cost']is None and inv['primary_graphics_cost']is None,'unknown costs never zero')
 delta_result=delta(root,packet,inv) if (packet/'inventory_correction.json').exists() else None
 controls=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,IndexError):controls.append(name);return
  raise ValueError('control accepted: '+name)
 sample=allrows[0]
 def bad(change):r=copy.deepcopy(sample);change(r);rowcheck(r)
 reject('missing base panel',lambda:bad(lambda r:r['residues'].pop()))
 reject('duplicate fixed subset',lambda:bad(lambda r:r['residues'].__setitem__(1,copy.deepcopy(r['residues'][0]))))
 reject('wrong type complement',lambda:bad(lambda r:r['residues'][0]['types'].reverse()))
 reject('rank zero substitution',lambda:bad(lambda r:r['residues'][0].__setitem__('residue_rank',0)))
 reject('lost direction',lambda:bad(lambda r:r['residues'][0]['type_results'].pop()))
 reject('direction boolean changed',lambda:bad(lambda r:r['residues'][0]['type_results'].__setitem__(0,not r['residues'][0]['type_results'][0])))
 reject('actual flag multiplicity lost',lambda:bad(lambda r:r['residues'][1].__setitem__('flag_orbit_size',1)))
 reject('full IP inverted',lambda:bad(lambda r:r.__setitem__('IP',not r['IP'])))
 reject('full WIP inverted',lambda:bad(lambda r:r.__setitem__('WIP',not r['WIP'])))
 reject('rank base count changed',lambda:bad(lambda r:r['by_rank'][0].__setitem__('base_residues',1)))
 reject('rank actual count changed',lambda:bad(lambda r:r['by_rank'][0].__setitem__('actual_residues',1)))
 weak=next(r for r in allrows if any(x.get('WIP') and not x.get('IP') for x in r['residues']))
 r=copy.deepcopy(weak);x=next(x for x in r['residues'] if x.get('WIP') and not x.get('IP'));x['WIP']=all(x['type_results']);reject('WIP incorrectly universal',lambda:rowcheck(r))
 for field,val in [('full_source_recovered',True),('new_original_credit',1),('new_conjecture_credit',1),('measurements',1),('old_topic_D_common_paid_whole',False),('new_common_paid_whole',False)]:
  s=load(packet/'scope.json');s[field]=val;reject('scope '+field,lambda s=s:science_scope(s))
 if delta_result:
  for path in required_layer(inv):
   broken=copy.deepcopy(inv);broken['all_occurrences']=[x for x in broken['all_occurrences'] if x['path']!=path];reject('omit current layer '+path,lambda broken=broken:required_layer(broken))
  broken=copy.deepcopy(inv);next(x for x in broken['all_occurrences'] if x['path']=='topic_D_L096_volume_v2/assemble.py')['role']='optional_validation';reject('required aggregator relabeled optional',lambda:required_layer(broken))
 return {'status':'PASS','inventory_delta':delta_result,'migrated_proof_environments':proof_count,'manifest_sha256':bind(packet/'manifest.json')['sha256'],'author_exports':len(m['exports']),'accepted_dependency_bindings':binding_count,'actual_input_rows':len(allrows),'accepted_classes':len(classes),'all_base_residues_including_panels':nr,'all_direction_bits':nt,'actual_residue_multiplicity':actual,'source_count_rows':57,'source_count_matches':agrees,'independently_transcribed_positive_label_occurrences':len(expectedlabels),'source_dispositions':73,'inventory_occurrences':len(inv['all_occurrences']),'inventory_contents':len(groups),'controls':controls,'control_count':len(controls),'no_author_imports':True,'no_group_or_formal_reexecution':True}

def main():
 p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--author',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=evaluate(a.study_root.resolve(),a.author.resolve() if a.author else a.study_root/'topic_D_L096_volume');a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
