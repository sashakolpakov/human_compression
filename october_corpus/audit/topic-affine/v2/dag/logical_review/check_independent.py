#!/usr/bin/env python3
"""Independent graph semantics guards, immutable scope, and prerequisite closure replay.

No imports from the author graph builder/checker; no numerical weighting,
primary extraction, group census or Lean compilation.
"""
import argparse,copy,hashlib,json
from pathlib import Path

LOGICAL={'proof_use','definition_use','hypothesis_use','proof_assembly','retained_input_use'}
NONLOGICAL={'attribution','comparison','validation','formal_scope','operational'}
REQUIRED={'program.kernel64','program.affine64','program.census384','program.fixed','program.kernel66','program.affine66'}
V1='8cb418bd7214ac86306a99ea0918d5187ad462a249ebff73eae6e4c0f9f47eda'
def need(b,s):
 if not b:raise ValueError(s)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def inspect(g,c,scope):
 nodes={n['id']:n for n in g['nodes']};need(len(nodes)==len(g['nodes'])==119,'119 unique nodes')
 edges={(e['source'],e['target'],e['kind']) for e in g['edges']};need(len(edges)==len(g['edges'])==228,'228 unique typed edges')
 need(g['edge_orientation']=='prerequisite -> use' and set(g['logical_edge_kinds'])==LOGICAL,'prerequisite convention')
 need(set(g['nonlogical_edge_kinds'])==NONLOGICAL,'nonlogical types')
 need(all(n['cost'] is None for n in nodes.values()) and g['compression_ratio'] is None,'unmeasured costs remain null')
 need(g['new_source_credit']==g['new_question_credit']==0,'no credit')
 required_edges={
 ('UA.K0','UA.K','proof_use'),('UA.K','UA.SK','proof_use'),('UA.D','UA.SK.Delete','proof_use'),
 ('AL.1','AL.RawInvariant','proof_use'),('AL.RawInvariant','program.affine66','proof_use'),
 ('program.kernel64','AF.Affine64','proof_use'),('program.affine64','AF.Affine64','proof_use'),('AL.2','AF.Affine64','proof_use'),
 ('program.kernel66','AF.Affine66','proof_use'),('program.affine66','AF.Affine66','proof_use'),('AL.2','AF.Affine66','proof_use'),
 ('AL.3','AF.Period64','proof_use'),('AL.3','AF.Period66','proof_use'),
 ('program.fixed','AF.Seed384','proof_use'),('program.fixed','AF.SignExample','proof_use'),
 ('ext.Lucchini','AF.CyclicDescent','retained_input_use'),('ext.SmallGroups','program.census384','retained_input_use'),
 ('program.census384','AF.Census384','proof_use'),('AF.Census384','AF.ExistenceRange','proof_use'),
 ('AF.EqualGeneration','AF.KnownAnswer','proof_use'),('AF.EqualIP','AF.KnownAnswer','proof_use'),
 ('ext.Polytope','AF.KnownAnswer','retained_input_use'),('UA.K','AF.Tetra96','proof_use'),
 ('h.64.Kernels','h.64.Scale','proof_use'),('h.66.Kernels','h.66.Scale','proof_use'),
 ('h.P2.3','h.64.Scale','proof_use'),('h.P2.3','h.66.Scale','proof_use'),
 ('h.P2.8','h.T4.3','proof_use'),('h.P2.8','h.T5.1','proof_use'),
 ('h.L4.5.0','h.T1.3','proof_use'),('h.P2.9','h.L4.7.descent','proof_use'),
 ('h.T5.1','h.C5.2','proof_use'),
 ('UA.SK','AL.4','comparison'),('program.kernel66','program.affine66','operational'),
 ('AL.SmallerPeriods','diagnostic.controls','validation')}
 for e in required_edges:need(e in edges,'missing reviewed interface '+repr(e))
 need(not any(e[0]=='AF.SignIdentity' and e[1]=='diagnostic.controls' for e in edges),'wrong finite-control scope')
 pred={n:set() for n in nodes}
 for a,b,k in edges:
  need(a in nodes and b in nodes and a!=b and k in LOGICAL|NONLOGICAL,'typed endpoints')
  if k in LOGICAL:
   need(nodes[a]['side']!='verification' and nodes[b]['side']!='verification','verification promoted to mathematics')
   need(not(nodes[a]['side']=='historical' and nodes[b]['side']=='new'),'historical use promoted to current proof')
   pred[b].add(a)
 def closure(targets):
  seen=set();active=set()
  def visit(n):
   need(n in nodes,'unknown closure target');need(n not in active,'logical cycle')
   if n in seen:return
   active.add(n)
   for v in pred[n]:visit(v)
   active.remove(n);seen.add(n)
  for n in targets:visit(n)
  return sorted(seen)
 individual={n:closure([n]) for n in nodes}
 need('UA.SK' not in pred['AL.4'],'AL.4 is independently proved')
 need(not any(n.startswith('lean.') or n.startswith('diagnostic.') or n.startswith('driver.') for n in closure(g['full_record_outputs'])),'formal or auxiliary evidence in full proof closure')
 for bad in ['ext.Atlas','ext.CoxeterMoser','ext.ConderTight','ext.ConderBound','ext.MW20','ext.LZ25','ext.Magma','ext.QuotientCriteria']:
  need(bad not in closure(g['full_record_outputs']),'unpaid historical theorem imported '+bad)
 rows={r['id']:r for r in c['rows']};old={r['id']:r for r in scope['source_rows']};need(len(rows)==len(c['rows'])==33 and set(rows)==set(old),'33 source rows')
 row_closures={}
 for id,r in rows.items():
  need(r['accepted_record']==old[id],'changed admitted source contract '+id)
  rr={}
  for outputs,key in [('historical_outputs','historical_closure'),('new_outputs','new_closure'),('retained_input_nodes','retained_context_closure')]:
   rr[key]=closure(r[outputs]);need(rr[key]==r[key],'incorrect output closure '+id+' '+key)
  row_closures[id]=rr
 for id in ['L012.problem1.1','L012.table1','L012.seed_uniqueness']:
  need(rows[id]['coverage_kind']=='excluded' and rows[id]['new_outputs']==[] and rows[id]['qualification_context_nodes']==['AF.Exclusions'],'excluded assertion promoted')
 need(rows['L012.question.type2']['coverage_kind']=='historically_answered_question','old answer claimed new')
 need(rows['L012.L4.5.branch0']['coverage_kind']=='corrected_source_statement' and nodes['h.L4.5.0']['documentary_flags'] and nodes['h.T1.3']['documentary_flags'],'historical false sign hidden')
 need(nodes['h.C5.2']['documentary_flags'],'source wrong cross-reference hidden')
 need(set(g['required_mathematical_programs'])==REQUIRED and REQUIRED<=set(closure(g['new_application_outputs']['L012'])),'six whole proof programs')
 need(g['diagnostic_programs']==['diagnostic.controls'] and set(g['operational_drivers'])=={'driver.check','driver.integrity'},'auxiliary inventory')
 need(g['formal_evidence']==dict(report_count=9,module_counts=[2,3,4],evidence_only=True,application_instantiations_formalized=False),'formal scope')
 for n,t in g['new_application_outputs'].items():need(closure(t)==g['new_output_closures'][n],'principal closure')
 need(closure(g['full_record_outputs'])==g['full_record_closure'],'full-record closure')
 for n,cl in g['additional_current_outputs'].items():need(closure([n])==cl,'additional closure')
 need(g['unused_common_statement_nodes']==['AL.SmallerPeriods','UA.SK.Delete'],'unused common results retained')
 need(g['measurement']['whole_common_paper_paid'] and g['measurement']['complete_six_programs_paid'] and g['measurement']['unused_common_statements_not_removed'],'full future cost boundary')
 return {'status':'PASS_INDEPENDENT_AFFINE_CLOSURES_AND_SEMANTIC_GUARDS','nodes':119,'typed_edges':228,'rows':33,'row_closures_checked':99,'individual_closures_checked':119,'additional_closures_checked':len(g['additional_current_outputs']),'principal_routes_checked':1,'full_record_routes_checked':1,'row_closures':row_closures,'individual_closures':individual}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--previous',type=Path,required=True);ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output')
 roots={'research':a.study_root,'public':a.public_root}
 need(digest(a.previous/'manifest.json')==V1,'frozen initial graph')
 for p in [a.previous,a.packet]:
  for r in read(p/'manifest.json')['exports']:
   q=p/r['path'];need(q.stat().st_size==r['bytes'] and digest(q)==r['sha256'],'frozen export '+str(q))
 g=read(a.packet/'logical_graph.json');c=read(a.packet/'coverage.json');old=read(a.previous/'logical_graph.json');oldc=read(a.previous/'coverage.json')
 need(g['nodes']==old['nodes'],'no graph node/source locator changes')
 added=[e for e in g['edges'] if e not in old['edges']];removed=[e for e in old['edges'] if e not in g['edges']]
 triples=lambda e:{(x['source'],x['target'],x['kind']) for x in e}
 need(triples(added)=={('UA.D','UA.SK.Delete','proof_use'),('AL.SmallerPeriods','diagnostic.controls','validation')} and triples(removed)=={('AF.SignIdentity','diagnostic.controls','validation')},'exact two-interface delta')
 for key in ['new_application_outputs','new_output_closures','full_record_outputs','full_record_closure','additional_current_outputs','unused_common_statement_nodes','source_bindings']:
  need(g[key]==old[key],'unexpected route or input change '+key)
 extra=[r for r in g['immutable_inputs'] if r not in old['immutable_inputs']]
 need(all(r in g['immutable_inputs'] for r in old['immutable_inputs']) and extra==[{'namespace':'research','path':'topic_Affine_logical_dag/manifest.json','bytes':(a.previous/'manifest.json').stat().st_size,'sha256':V1}],'only historical manifest binding added')
 need(c==oldc,'33 coverage rows/closures should be unchanged')
 texts={};count=0
 for row in g['immutable_inputs']:
  p=roots[row['namespace']]/row['path'];need(digest(p)==row['sha256'] and p.stat().st_size==row['bytes'],'immutable graph input '+str(p));count+=1
 def checkloc(x):
  key=(x['namespace'],x['path']);t=texts.setdefault(key,(roots[key[0]]/key[1]).read_text());l,r=x['start_codepoint'],x['end_codepoint_exclusive']
  need(0<=l<r<=len(t) and hashlib.sha256(t[l:r].encode()).hexdigest()==x['sha256_utf8'],'bound context')
  need(t.count('\n',0,l)+1==x['first_line'] and t.count('\n',0,r-1)+1==x['last_line'],'context lines')
 locs=set()
 for x in [s for n in g['nodes'] for s in n['locators']]+[s for e in g['edges'] for s in e['target_evidence']]+list(g['accepted_scope_spans'].values()):
  checkloc(x);locs.add((x['namespace'],x['path'],x['start_codepoint'],x['end_codepoint_exclusive']))
 scope=read(a.public_root/'papers/topic-affine/v2/scope.json');need(len(g['accepted_scope_spans'])==len(scope['proof_regions'])==17,'17 contexts')
 out=inspect(g,c,scope);controls=[]
 for label in ['drop_Boolean_use','comparison_as_proof','raw_lattice_adapter_missing','abstract_kernel_missing','formal_promoted','historical_sign_hidden','excluded_result_recovered','known_answer_new_credit','unknown_cost_zero','wrong_control_scope','hash_as_mathematical_dependency','Lucchini_missing']:
  gg,cc=copy.deepcopy(g),copy.deepcopy(c)
  if label in ['drop_Boolean_use','raw_lattice_adapter_missing','abstract_kernel_missing','Lucchini_missing']:
   pair={'drop_Boolean_use':('UA.D','UA.SK.Delete'),'raw_lattice_adapter_missing':('AL.RawInvariant','program.affine66'),'abstract_kernel_missing':('program.kernel64','AF.Affine64'),'Lucchini_missing':('ext.Lucchini','AF.CyclicDescent')}[label]
   e=next(e for e in gg['edges'] if (e['source'],e['target'])==pair);e['kind']='comparison'
  elif label=='comparison_as_proof':next(e for e in gg['edges'] if e['source']=='UA.SK' and e['target']=='AL.4')['kind']='proof_use'
  elif label=='formal_promoted':next(e for e in gg['edges'] if e['source']=='lean.AffinePeriodIntersections')['kind']='proof_use'
  elif label=='historical_sign_hidden':next(n for n in gg['nodes'] if n['id']=='h.L4.5.0')['documentary_flags']=[]
  elif label=='excluded_result_recovered':
   rr=next(r for r in cc['rows'] if r['id']=='L012.table1');rr['new_outputs']=['AF.ExistenceRange'];rr['new_closure']=out['individual_closures']['AF.ExistenceRange']
  elif label=='known_answer_new_credit':gg['new_question_credit']=1
  elif label=='unknown_cost_zero':gg['nodes'][0]['cost']=0
  elif label=='wrong_control_scope':next(e for e in gg['edges'] if e['target']=='diagnostic.controls' and e['kind']=='validation')['source']='AF.SignIdentity'
  else:next(e for e in gg['edges'] if e['source']=='program.kernel66' and e['target']=='program.affine66')['kind']='proof_use'
  try:inspect(gg,cc,scope)
  except ValueError as e:controls.append({'name':label,'rejected':True,'reason':str(e)})
  else:raise ValueError('accepted control '+label)
 out.update({'manifest_sha256':digest(a.packet/'manifest.json'),'previous_manifest_sha256':V1,'immutable_inputs':count,'exact_contexts':len(locs),'negative_controls':controls,'exact_added_edges':[list(x) for x in sorted(triples(added))],'exact_removed_edges':[list(x) for x in sorted(triples(removed))],'primary_text_exported':False,'GAP_or_Lean_replayed':False,'new_result_credit':0,'compression_ratio':None})
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['row_closures','individual_closures','negative_controls']}))
if __name__=='__main__':main()
