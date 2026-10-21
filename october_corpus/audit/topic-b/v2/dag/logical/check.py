#!/usr/bin/env python3
"""Verify unweighted DAG bindings and controls, not the authored edge semantics."""
import argparse
from collections import Counter,deque
import copy
import hashlib
import json
from pathlib import Path


def need(ok,msg):
 if not ok:raise ValueError(msg)


def sha(data):return hashlib.sha256(data).hexdigest()


def validate(g,c,p,roots):
 nodes={n['id']:n for n in g['nodes']};edges=g['edges'];logical=set(g['logical_edge_kinds'])
 need(len(nodes)==len(g['nodes']),'unique node IDs')
 need(g['edge_orientation']=='prerequisite -> use','orientation')
 need(logical=={'proof_use','definition_use','hypothesis_use','proof_assembly','retained_input_use'},'logical kinds')
 need(g['compression_ratio'] is None and g['new_source_credit']==g['new_question_credit']==0,'no factor or credit')
 need(not g['measurement']['weights_assigned'] and not g['measurement']['exclusive_partition_assigned'],'unweighted graph')
 need(g['source_bindings']['N001']['primary_pdf'] is None and g['source_bindings']['N001']['pdf_cost'] is None,'N001 missing PDF is unknown')
 need(g['required_mathematical_programs']==[],'no omitted required mathematical program')
 need(p['authoritative_map']=='papers/topic-b/v2/mapping_correction/source_contract_map.json','corrected map is authoritative')
 binding_rows={(r['namespace'],r['path']):r for r in g['immutable_inputs']}
 need(len(binding_rows)==len(g['immutable_inputs']),'unique bound inputs')
 for (space,path),r in binding_rows.items():
  need(space in roots and not Path(path).is_absolute() and '..' not in Path(path).parts,'safe relative input')
  raw=(roots[space]/path).read_bytes()
  need(len(raw)==r['bytes'] and sha(raw)==r['sha256'],'input binding: '+path)
 seen_spans=set()
 def span(s):
  key=(s['namespace'],s['path']);need(key in binding_rows,'span file is bound')
  text=(roots[key[0]]/key[1]).read_text();a,b=s['start_codepoint'],s['end_codepoint_exclusive']
  need(0<=a<b<=len(text) and sha(text[a:b].encode())==s['sha256_utf8'],'actual span: '+str(key))
  first=text.count('\n',0,a)+1;last=text.count('\n',0,b-1)+1
  need(s['first_line']==first and s['last_line']==last,'line/codepoint correspondence')
  seen_spans.add((key,a,b))
 for n in nodes.values():
  need(n['cost'] is None,'unknown/unweighted cost is not zero')
  need(n['locators'],'nonempty semantic locator')
  for s in n['locators']:span(s)
  if n.get('parent'):
   need(n['parent'] in nodes and nodes[n['parent']]['document']==n['document'] and nodes[n['parent']]['side']==n['side'],'valid same-document parent')
 pairs=set();degree={x:0 for x in nodes};out={x:[] for x in nodes};pred={x:[] for x in nodes}
 for e in edges:
  a,b,k=e['source'],e['target'],e['kind'];need(a in nodes and b in nodes and a!=b,'valid edge endpoints')
  need((a,b,k) not in pairs,'no duplicate edge');pairs.add((a,b,k))
  need(k in logical or k in g['nonlogical_edge_kinds'],'declared edge kind')
  need(e['evidence'] and e['target_evidence'] and not e['necessity_claim'],'use evidence without minimality claim')
  for s in e['target_evidence']:span(s)
  if k in logical:
   need(nodes[a]['side']!='verification' and nodes[b]['side']!='verification','verification evidence is not a mathematical premise')
   need(not(nodes[a]['side']=='historical' and nodes[b]['side']=='new'),'attribution is not a hidden old-proof premise')
   degree[b]+=1;out[a].append(b);pred[b].append(a)
 q=deque(x for x in degree if degree[x]==0);order=[]
 while q:
  x=q.popleft();order.append(x)
  for y in out[x]:
   degree[y]-=1
   if degree[y]==0:q.append(y)
 need(len(order)==len(nodes),'acyclic mathematical dependency graph')
 def closure(xs):
  found=set(xs);todo=list(xs)
  for x in todo:
   for y in pred[x]:
    if y not in found:found.add(y);todo.append(y)
  return sorted(found)
 expected=dict(nodes=len(nodes),edges=len(edges),nodes_by_side=dict(Counter(n['side'] for n in nodes.values())),
   nodes_by_category=dict(Counter(n['category'] for n in nodes.values())),edges_by_kind=dict(Counter(e['kind'] for e in edges)),source_clauses=30)
 need(g['checks']==expected,'embedded counts equal actual graph')
 for app,node in g['new_application_outputs'].items():need(g['new_output_closures'][app]==closure([node]),'actual application closure')
 raw=json.loads((roots['public']/p['authoritative_map']).read_text());original={r['adapter']:r for r in raw['rows']}
 rows={r['adapter']:r for r in c['rows']}
 need(len(rows)==len(c['rows'])==30 and set(rows)==set(original),'complete unchanged thirty-clause boundary')
 for key,r in rows.items():
  source=original[key]
  for old,new in [('source_contract','preserved_contract'),('source_id','source_id'),('source_reference','source_reference'),('source_span','source_span'),('new_tex_nodes','accepted_owner_nodes'),('new_tex_spans','accepted_owner_spans')]:
   need(source[old]==r[new],'unchanged accepted clause/interface '+key)
  need(r['historical_output'] in nodes and nodes[r['historical_output']]['document']==r['source_id'],'matched source output')
  need(all(x in nodes and nodes[x]['side']=='new' for x in r['new_outputs']),'new actual proof outputs')
  need(r['historical_closure']==closure([r['historical_output']]) and r['new_closure']==closure(r['new_outputs']),'actual clause closures')
  text=(roots['research']/g['source_bindings'][r['source_id']]['documentary_text']['path']).read_text();s=r['source_span']
  need(sha(text[s['start_codepoint']:s['end_codepoint_exclusive']].encode())==s['sha256_utf8'],'original source clause span')
  need(r['cost'] is None,'no clause weight yet')
 need(rows['C10']['accepted_owner_nodes']==['B3.Coordinates','B3.Ladder'] and rows['C11']['accepted_owner_nodes']==['B3.Frattini','B3.Quotient'],'corrected Frattini owners')
 need('B2.Extremal' in rows['B4']['new_outputs'],'arbitrary-family clause includes classification')
 need('B3.Frattini.containment' in rows['C11']['new_outputs'],'core clause includes Frattini containment')
 for source,target,kind in [('h.N008.T3.1.ladder','h.N008.T3.1.propagation','hypothesis_use'),('ext.CFSG','ext.W1','retained_input_use'),('h.L030.L2.2','h.L030.L3.3','proof_use')]:
  need((source,target,kind) in pairs,'independently requested prerequisite')
 need(nodes['h.N008.T3.1.ladder'].get('scope_qualification'),'historical setup versus assembly qualification')
 need(len(nodes['h.L030.L3.3']['documentary_flags'])>=2,'connectedness and boundary qualifications')
 return {'bound_inputs':len(binding_rows),'unique_exact_spans':len(seen_spans),'source_rows':30,'nodes':len(nodes),'edges':len(edges),'logical_topological_nodes':len(order)}


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent)
 ap.add_argument('--sources-root',required=True,type=Path);ap.add_argument('--public-root',required=True,type=Path);ap.add_argument('--out',required=True,type=Path)
 a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output report')
 roots={'research':a.sources_root.resolve(),'public':a.public_root.resolve()}
 g=json.loads((a.packet/'logical_graph.json').read_text());c=json.loads((a.packet/'coverage.json').read_text());p=json.loads((a.packet/'protocol.json').read_text())
 result=validate(g,c,p,roots);controls=[]
 for label in ['missing_clause','wrong_span','reverse_edge_cycle','external_cost_zero','invented_N001_pdf','old_C10_owner','attribution_as_premise','stale_counts','omit_extremal_classification','omit_Frattini_containment']:
  gg,cc,pp=copy.deepcopy(g),copy.deepcopy(c),copy.deepcopy(p)
  if label=='missing_clause':cc['rows'].pop()
  elif label=='wrong_span':gg['nodes'][0]['locators'][0]['sha256_utf8']='0'*64
  elif label=='reverse_edge_cycle':
   e=copy.deepcopy(next(e for e in gg['edges'] if e['kind']=='proof_use'));e['source'],e['target']=e['target'],e['source'];gg['edges'].append(e)
  elif label=='external_cost_zero':gg['nodes'][0]['cost']=0
  elif label=='invented_N001_pdf':gg['source_bindings']['N001']['pdf_cost']=0
  elif label=='old_C10_owner':next(r for r in cc['rows'] if r['adapter']=='C10')['accepted_owner_nodes']=['B3.Frattini']
  elif label=='attribution_as_premise':next(e for e in gg['edges'] if e['kind']=='attribution_identity')['kind']='proof_use'
  elif label=='omit_extremal_classification':next(r for r in cc['rows'] if r['adapter']=='B4')['new_outputs'].remove('B2.Extremal')
  elif label=='omit_Frattini_containment':next(r for r in cc['rows'] if r['adapter']=='C11')['new_outputs'].remove('B3.Frattini.containment')
  else:gg['checks']['edges']+=1
  try:validate(gg,cc,pp,roots)
  except ValueError as exc:controls.append({'name':label,'rejected':True,'reason':str(exc)})
  else:raise RuntimeError('accepted corruption '+label)
 report=dict(status='PASS_AUTHOR_BINDING_DAG_AND_SCOPE_CHECK',**result,controls=controls,
  mathematical_edge_semantics_independently_reviewed=False,weights_assigned=False,new_source_credit=0,new_question_credit=0)
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))


if __name__=='__main__':main()
