#!/usr/bin/env python3
"""Exact bounded semantic correction audit; does not permit proof/source edits."""
import argparse,copy,hashlib,json
from pathlib import Path

def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compare(root,newcost,newgraph):
 oldp=load(root/'topic_D_dag_costs/partition.json');p=load(newcost/'partition.json')
 oldw=load(root/'topic_D_dag_costs/weights.json');w=load(newcost/'weights.json')
 oldg=load(root/'topic_D_logical_dag_v2/logical_graph.json');g=load(newgraph/'logical_graph.json')
 need(g['nodes']==oldg['nodes'],'all137 nodes/locators/scopes unchanged')
 need(len(g['edges'])==len(oldg['edges'])+1,'exactly one extra edge')
 for e in oldg['edges']:need(e in g['edges'],'every original edge unchanged')
 added=[e for e in g['edges'] if e not in oldg['edges']]
 need(len(added)==1 and (added[0]['source'],added[0]['target'],added[0]['kind'])==('UD.ExactSupport','D2.Support','proof_use'),'literal invoked theorem prerequisite')
 for k in ['source_bindings','accepted_scope_spans','applications','new_application_outputs','required_mathematical_programs','diagnostic_programs','operational_drivers','formal_evidence','logical_edge_kinds']:
  need(g[k]==oldg[k],'unchanged mathematical/retained boundary '+k)
 expected=copy.deepcopy(oldp['owners']);expected['h.L074.9']['category']='statement';need(p['owners']==expected,'exact one owner category correction')
 expected=copy.deepcopy(oldp['documents']);changed=0
 for d in expected.values():
  for v in d['variants'].values():
   for s in v['spans']:
    if s['owner']=='h.L074.9':s['category']='statement';changed+=1
 need(p['documents']==expected,'all offsets/hashes/owners unchanged; only statement span labels')
 for k in ['owner_costs','document_costs','raw_program_alternative','raw_operational_drivers','complete_historical_pdf_cost']:
  need(w[k]==oldw[k],'all measured costs unchanged '+k)
 repairs={'h.L074.12':'h.L074.composite_setup','D2.Duality':'D2.Polyhedra.setup'}
 for n,old in oldw['node_interfaces'].items():
  expected=set(old['owners'])|({repairs[n]} if n in repairs else set())
  need(set(w['node_interfaces'][n]['owners'])==expected and len(w['node_interfaces'][n]['owners'])==len(expected),'only two shared owner repairs '+n)
  need(w['node_interfaces'][n]['unknown_reason']==old['unknown_reason'],'unknown status unchanged')
 need(load(newcost/'view_data.json')['measurement']==load(root/'topic_D_dag_costs/view_data.json')['measurement'],'all whole/conditional factors unchanged')
 # The two exact setup passages are definitions, not an extra theorem premise.
 # In particular no backwards Polyhedra -> Duality edge is introduced.
 need(not any(e['source']=='D2.Polyhedra' and e['target']=='D2.Duality' for e in added),'no artificial circular dependency')
 return {'status':'PASS_EXACT_FOUR_REPAIR_DELTA','owner_categories_changed':1,'span_category_cells_changed':changed,'shared_owner_interfaces_changed':2,'added_logical_edges':1,'unchanged_nodes':len(g['nodes']),'unchanged_original_edges':len(oldg['edges']),'current_edges':len(g['edges']),'all_owner_and_document_costs_byte_equivalent_as_JSON':True,'all_accepted_factors_unchanged':True,'scientific_and_source_scope_unchanged':True}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--study-root',type=Path,required=True);a.add_argument('--costs',type=Path,required=True);a.add_argument('--logical',type=Path,required=True);a.add_argument('--out',type=Path,required=True);x=a.parse_args();r=compare(x.study_root,x.costs,x.logical);need(not x.out.exists(),'fresh report');x.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
