"""Exact source/interface join; acquired finite computations are not repeated."""
import sys
if sys.flags.optimize:raise RuntimeError('Optimized Python is not supported')
sys.dont_write_bytecode=True
import argparse,copy,hashlib,json
from pathlib import Path

def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def validate(a,c,components,scope,general,finite,literal,source):
 need(a['original']==scope['original']=='L052','Exact original')
 need(a['whole_original_credit']==a['new_question_credit']==a['new_Lean_declarations']==a['new_measurements']==0 and a['compression_factor']is None,'No premature credit')
 need(scope['complete_principal_contract']and not scope['all_source_assertions_unchanged']and not scope['classification_completeness_inferred_from_tables'],'Corrected principal boundary')
 expected_h=dict(type_preserving_automorphisms=True,regular_converse_requires_flag_transitivity=True,Cplus_converse_requires_hypertope=True,Cplus_converse_requires_exactly_two_chamber_orbits=True,coset_faithfulness_before_core_quotient=False,ICplus_for_rotation_requires_index_two=True,proper_truncations_claimed_thin=False,geometric_reflection_can_be_nonidentity_when_theta_identity=True)
 need(a['principal_hypotheses']==expected_h,'Every actual geometric hypothesis')
 by={x['id']:x for x in a['claims']};need(len(by)==len(a['claims'])==62,'Exact nonduplicate source register')
 named=['2.1','2.2','3.1','3.2','3.3','3.4','3.5','4.1','4.2','4.3','4.6','5.1','5.2','6.1','6.2','7.1','7.2','8.1','8.2']
 need(c['named_ids']==['N'+x for x in named]and[x['source_clause']for x in general['clauses']]==named,'Complete named clauses')
 for x,z,old in zip(named,general['clauses'],source['named_clauses']):
  r=by['N'+x];need(r['statement']==old['statement']and r['route']['section']==z['route']and r['qualification']==z['qualification'],'Exact acquired general route')
  need(r['status']==('RETAINED_NAMED_CORRESPONDENCE'if x=='5.1'else'ACQUIRED_COMPLETE_PROOF'),'Retained versus acquired named proof')
 need(by['Construction8.1']['status']=='ACQUIRED_WITH_EXPLICIT_GEOMETRIC_HYPOTHESES','Incidence-system construction')
 expected_ids=['T1.'+str(i)for i in range(1,13)]+['T2.'+str(i)for i in range(1,12)]
 need([x['id']for x in c['finite_rows']]==expected_ids and[x['id']for x in finite['rows']]==expected_ids,'All23 finite rows')
 raw={x['id']:x for key in ['table1','table2']for x in source[key]['rows']}
 for r,z in zip(c['finite_rows'],finite['rows']):
  need(r==by[r['id']],'Source/coverage row identity');old=raw[r['id']]
  need(r['parameters']==[old['p'],old['a'],old['b']]and r['full_order']==z['full_order']==old['printed_g']and r['rotation_order']==z['rotation_order']and r['regularity']==z['status'],'Exact finite source/group route')
  need(r['chambers']==r['full_order']*(2 if r['regularity']=='chiral'else 1),'Chiral chamber caption correction')
 need(by['T2.7']['corrected_group']=='Parity subgroup of S5 x S4'and by['T2.7']['source_group']=='A5 x S4','Explicit false group-name correction')
 need(c['examples']==['E4.4','E4.5','E6.3'],'All three examples')
 for x in c['examples']:need(by[x]['status']=='ACQUIRED_COMPLETE_LITERAL_CERTIFICATE','Complete finite example')
 # This is the exact previously verified input to the new written deduction,
 # not an independent subgroup enumeration or a computational proof substitute.
 e=next(x for x in literal['examples']if x['id']=='4.5');need(e['order']==360 and e['ip'][11]==e['ip'][13]==60 and e['ip'][9]==10,'A6 deduction actual acquired subgroup inputs')
 corr=by['C_A6_rotation'];need(corr['status']=='ILLUSTRATION_REFUTED_FROM_ACQUIRED_DATA'and corr['evidence']==dict(supports=[[0,2,3],[0,1,3]],parabolic_groups=['A5','A5'],parabolic_orders=[60,60],intersection_order=10,common_support=[0,3],required_cyclic_order=5,witness='rho0')and not corr['general_Cplus_converse_decided'],'Ancillary correction only, not a general converse')
 need(len(a['corrections'])==4 and {x['id']for x in a['corrections']}=={'K_chamber_captions','K_group_name','K_unit_period','K_A6_illustration'},'All literal source corrections')
 need(c['retained_input_ids']==[x['id']for x in a['retained_inputs']]==['R_string','R_torus_chirality','R_torus_families','R_regular_locally_toroidal'],'Four retained named inputs')
 need(all(not x['full_primary_reacquisition_claimed']for x in a['retained_inputs']),'No invented primary acquisition')
 need('nondegenerate' in a['retained_inputs'][1]['claim']and 'unit periods' in a['retained_inputs'][1]['domain'],'Toroidal parameter boundary retained')
 need(c['question_ids']==[x['id']for x in a['questions']]==['Q9.1','Q9.2','Q9.3','Q9.4','Qtable1-completeness'],'All question dispositions')
 for x in a['questions']:
  need(x==by[x['id']]and x['new_question_credit']==0,'No new question credit')
  need(x['status']==('ACQUIRED_OLD_NEGATIVE_ANSWER_STANDARD_PARABOLICS'if x['id']in ['Q9.3','Q9.4']else'HISTORICAL_QUESTION_NO_NEW_SOLUTION'),'Old answers versus unsolved questions')
 need(len(c['context_ids'])==7 and all(not by[x]['principal_proof_dependency']for x in c['context_ids']),'Attributed contextual antecedents')
 roles=['general_author','general_distinct_review','general_root_adoption','finite_author','finite_distinct_root_review']
 need([x['role']for x in components['packets']]==roles and all(x['review_status']=='ACCEPTED'and x['complete_exports_acquired']for x in components['packets']),'Exact accepted components')
 need(len(components['components'])==2 and all(x['review_state']=='ACCEPTED'for x in components['components']),'No pending component premise')
 need(c['counts']==dict(claims=62,named_clauses=19,acquired_named_clauses=18,retained_named_clauses=1,table1_rows=12,table2_rows=11,examples=3,retained_classifications=4,question_dispositions=5,acquired_old_question_answers=2,unsolved_question_dispositions=3,contextual_antecedents=7,source_corrections=4),'Exact source inventory')
 return c['counts']

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);x=ap.parse_args();P=Path(__file__).resolve().parent;S=x.study.resolve();R=x.repo.resolve();O=x.out.resolve();need(not O.exists()and not O.is_relative_to(P),'Fresh external output')
 a=load(P/'claim_register.json');c=load(P/'coverage.json');m=load(P/'acquired_packets.json');scope=load(P/'scope.json');g=load(S/'corpus106_L052_residue_theory_v1/scope.json');f=load(S/'corpus106_L052_finite_v1/finite_source_map.json');literal=load(S/'corpus106_L052_finite_v1/final_literal_report.json');source=load(S/'corpus106_L052_finite_v1/source_contract01.json')
 report=validate(a,c,m,scope,g,f,literal,source)
 deps=load(P/'dependencies.json')
 for row in deps:
  base={'study':S,'public':R}[row['namespace']];p=(base/row['path']).resolve();need(p.is_relative_to(base)and p.is_file(),'Safe acquired dependency');b=p.read_bytes();need(len(b)==row['bytes']and hashlib.sha256(b).hexdigest()==row['sha256'],'Changed acquired dependency '+row['path'])
 controls=[]
 for case in ['omit_named_clause','lose_table_row','wrong_chiral_chambers','restore_false_group_name','false_A6_Cplus','drop_retained_input','claim_chiral_completeness','new_old_question_credit','remove_two_orbits','automatic_Cplus_geometry','wrong_A6_intersection','pending_component','invent_acquisition']:
  aa,cc,mm,ss=copy.deepcopy((a,c,m,scope));by={r['id']:r for r in aa['claims']}
  if case=='omit_named_clause':aa['claims'].remove(by['N8.2'])
  elif case=='lose_table_row':cc['finite_rows'].pop()
  elif case=='wrong_chiral_chambers':by['T2.4']['chambers']=168
  elif case=='restore_false_group_name':by['T2.7']['corrected_group']='A5 x S4'
  elif case=='false_A6_Cplus':by['C_A6_rotation']['status']='ACCEPTED_CPLUS_EXAMPLE'
  elif case=='drop_retained_input':aa['retained_inputs'].pop()
  elif case=='claim_chiral_completeness':by['Qtable1-completeness']['status']='NEW_COMPLETE_CLASSIFICATION'
  elif case=='new_old_question_credit':aa['questions'][2]['new_question_credit']=1
  elif case=='remove_two_orbits':aa['principal_hypotheses']['Cplus_converse_requires_exactly_two_chamber_orbits']=False
  elif case=='automatic_Cplus_geometry':aa['principal_hypotheses']['Cplus_converse_requires_hypertope']=False
  elif case=='wrong_A6_intersection':by['C_A6_rotation']['evidence']['intersection_order']=5
  elif case=='pending_component':mm['components'][1]['review_state']='PENDING'
  else:aa['retained_inputs'][1]['full_primary_reacquisition_claimed']=True
  try:validate(aa,cc,mm,ss,g,f,literal,source)
  except (ValueError,KeyError):controls.append(case)
  else:raise ValueError('Damaged source join accepted '+case)
 O.mkdir(parents=True);report=dict(status='PASS_COMPLETE_L052_SOURCE_JOIN',counts=report,bindings=len(deps),damaged_controls=controls,acquired_census_repeated=False,whole_original_credit=0);(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
