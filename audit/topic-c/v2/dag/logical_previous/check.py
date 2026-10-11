#!/usr/bin/env python3
"""Check exact locators, fixed clause boundary and typed graph structure, not mathematical truth."""
import argparse,copy,hashlib,json
from collections import Counter,deque
from pathlib import Path

def need(v,msg):
 if not v:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def validate(g,c,p,roots):
 nodes={n['id']:n for n in g['nodes']};need(len(nodes)==len(g['nodes']),'unique nodes')
 logical=set(g['logical_edge_kinds']);nonlogical=set(g['nonlogical_edge_kinds'])
 need(logical=={'proof_use','definition_use','hypothesis_use','proof_assembly','retained_input_use'},'fixed logical kinds')
 need(nonlogical=={'attribution','validation','formal_scope','comparison'},'fixed nonlogical kinds')
 need(g['edge_orientation']=='prerequisite -> use','edge direction')
 need(g['compression_ratio'] is None and g['new_source_credit']==g['new_question_credit']==0,'no invented ratio or credit')
 need(g['measurement']['weights_assigned'] is False and g['measurement']['exclusive_partition_assigned'] is False,'unweighted graph only')
 need(g['source_bindings']['L108']['original_pdf_available'] is False and g['source_bindings']['L108']['pdf_cost'] is None,'missing L108 PDF remains unknown')
 need(g['required_mathematical_programs']==['program.construction','program.census'],'complete required code boundary')
 inputs={(x['namespace'],x['path']):x for x in g['immutable_inputs']};need(len(inputs)==len(g['immutable_inputs']),'unique immutable inputs')
 for (ns,path),r in inputs.items():
  need(ns in roots and not Path(path).is_absolute() and '..' not in Path(path).parts,'safe relative input path')
  b=(roots[ns]/path).read_bytes();need(sha(b)==r['sha256'] and len(b)==r['bytes'],'bound input '+path)
 spans=set()
 def check_span(s):
  key=(s['namespace'],s['path']);need(key in inputs,'span input bound');t=(roots[key[0]]/key[1]).read_text();a,b=s['start_codepoint'],s['end_codepoint_exclusive']
  need(0<=a<b<=len(t),'nonempty span');need(sha(t[a:b].encode())==s['sha256_utf8'],'span hash')
  need(s['first_line']==t.count('\n',0,a)+1 and s['last_line']==t.count('\n',0,b-1)+1,'line/codepoint correspondence')
  if 'browser_display_lines' in s:need(s.get('original_pdf_available') is False,'browser is not original PDF')
  spans.add((key,a,b))
 for n in nodes.values():
  need(n['cost'] is None,'no unknown cost as zero');need(n['locators'],'actual node evidence')
  for s in n['locators']:check_span(s)
  if 'parent' in n:need(n['parent'] in nodes and nodes[n['parent']]['document']==n['document'] and nodes[n['parent']]['side']==n['side'],'same-side same-document parent')
 pairs=set();pred={n:[] for n in nodes};succ={n:[] for n in nodes};degree={n:0 for n in nodes}
 for e in g['edges']:
  s,t,k=e['source'],e['target'],e['kind'];need(s in nodes and t in nodes and s!=t,'valid edge endpoints');need(k in logical|nonlogical,'typed edge');need((s,t,k) not in pairs,'unique edge');pairs.add((s,t,k))
  need(e['evidence'] and e['target_evidence'] and e['necessity_claim'] is False,'use evidence without minimality claim')
  for loc in e['target_evidence']:check_span(loc)
  if k in logical:
   need(nodes[s]['side']!='verification' and nodes[t]['side']!='verification','formal/replay is not proof premise')
   need(not(nodes[s]['side']=='historical' and nodes[t]['side']=='new'),'historical attribution is not a hidden premise')
   pred[t].append(s);succ[s].append(t);degree[t]+=1
 q=deque(x for x in nodes if degree[x]==0);ordered=[]
 while q:
  x=q.popleft();ordered.append(x)
  for y in succ[x]:
   degree[y]-=1
   if degree[y]==0:q.append(y)
 need(len(ordered)==len(nodes),'acyclic logical graph')
 def closure(ids):
  seen=set(ids);todo=list(ids)
  for x in todo:
   need(x in nodes,'output node exists')
   for y in pred[x]:
    if y not in seen:seen.add(y);todo.append(y)
  return sorted(seen)
 tally=dict(nodes=len(nodes),edges=len(g['edges']),nodes_by_side=dict(Counter(n['side'] for n in nodes.values())),nodes_by_category=dict(Counter(n['category'] for n in nodes.values())),edges_by_kind=dict(Counter(e['kind'] for e in g['edges'])),source_clauses=40)
 need(tally==g['checks'],'actual embedded graph tallies')
 raw=json.loads((roots['public']/p['authoritative_scope']).read_text());original={r['id']:r for r in raw['source_result_rows']};rows={r['id']:r for r in c['rows']}
 need(len(rows)==len(c['rows'])==40 and set(rows)==set(original),'complete unchanged forty-row boundary')
 for id,r in rows.items():
  need(r['accepted_record']==original[id] and r['coverage']==original[id]['coverage'],'exact accepted row '+id)
  need(all(nodes[x]['document']==r['source'] and nodes[x]['side']=='historical' for x in r['historical_outputs']),'source output belongs to exact source')
  need(all(nodes[x]['side']=='new' for x in r['new_outputs']),'current output belongs to new proof')
  need(r['historical_closure']==closure(r['historical_outputs']) and r['new_closure']==closure(r['new_outputs']),'actual row closure '+id)
  if r['coverage']=='excluded_auxiliary':need(not r['new_outputs'] and r['exclusion_or_qualification_locator'],'no false recovery of excluded clause')
  else:need(r['new_outputs'],'nonexcluded row has explicit route')
  need(r['cost'] is None,'no clause cost assigned')
 for s,outs in g['new_application_outputs'].items():
  need(outs==sorted(set(x for r in rows.values() if r['source']==s for x in r['new_outputs'])),'application equals declared fixed rows')
  need(g['new_output_closures'][s]==closure(outs),'actual application closure')
 for source,outs in g['additional_current_comparisons'].items():need(g['additional_comparison_closures'][source]==closure(outs),'actual additional comparison closure')
 for source in raw_source_ids(g):need(g['source_bindings'][source]['pdf_cost'] is None,'unmeasured source PDF cost')
 # Preserve every accepted statement/context and complete-region binding, without making them disjoint weights.
 need(len(raw['proof_statements_and_context'])==p['accepted_proof_context_spans']==38 and len(raw['proof_regions'])==p['accepted_complete_regions']==7,'all forty-five original scope bindings')
 for id,d in raw['proof_statements_and_context'].items():
  b=d['binding'];s=nodes[id]['locators'][0];need((s['path'],s['start_codepoint'],s['end_codepoint_exclusive'],s['sha256_utf8'])==('papers/topic-c/v2/'+b['file'],b['start_char'],b['end_char'],b['sha256']),'accepted context preserved '+id)
 for b in raw['proof_regions'].values():
  t=(roots['public']/'papers/topic-c/v2'/b['file']).read_text();need(sha(t[b['start_char']:b['end_char']].encode())==b['sha256'],'complete region preserved')
 for f in p['scientific_edition_verified']:need(inputs['public',f['path']]['sha256']==f['sha256'],'exact edition binding')
 required=[('UC.edgegeneration','C.Parity'),('UC.edgegeneration','F.Marking'),('UC.twist','F.Geometry'),('UC.recognition','UC.cyclicrecognition'),('UC.displacements','UC.cyclicrecognition'),('UC.cyclicrecognition','F.Presentation'),('C.Endpoint','C.Odd'),('C.Odd','C.J1'),('UC.ExtensionOrbits','C.Census'),('program.construction','C.J1'),('program.census','C.Classification'),('UC.Action','C.PetrialAction'),('UC.Action','C.GraphAction.kernel'),('C.Graph.geometry','C.Graph'),('C.GraphAction.kernel','C.Graph'),('C.Graph','C.GraphAction.markers'),('ext.Danzer','C.N013Setup'),('ext.PolytopeCorrespondence','F.Geometry'),('h.J.method','h.J.T5.2'),('h.N.P2.3','h.N.T3.1'),('ext.NSemiregular','h.N.P3.2'),('h.F.P2.5','h.F.cosets'),('h.F.cosets','h.F.T3.4')]
 for s,t in required:need(any(a==s and b==t and k in logical for a,b,k in pairs),'actual substantive route '+s+' -> '+t)
 need(('h.F.displacement','UC.displacements','attribution') in pairs,'source displacement proof attributed')
 need('program.census' in rows['J9']['new_closure'] and 'program.construction' in rows['J1']['new_closure'],'complete J1 required program routes')
 need(not any(x.startswith('program.') for id in ['F1','F2','F3','F4','F5'] for x in rows[id]['new_closure']),'all-n F014 proof does not depend on finite diagnostics')
 need(rows['N14']['new_outputs']==rows['N15']['new_outputs']==[],'two excluded routes')
 for id in ['J10','N13','P4','P7','P8']:need(rows[id]['coverage']=='corrected_or_qualified_assertion','preserved qualification '+id)
 for id in ['h.P.L3.2ii','h.P.length','h.F.model','h.J.figures']:need(nodes[id]['documentary_flags'],'historical defect visibly flagged')
 return dict(**tally,bound_inputs=len(inputs),unique_exact_spans=len(spans),accepted_scope_bindings=45)

def raw_source_ids(g):return g['source_order']

def refresh(g):
 g['checks']=dict(nodes=len(g['nodes']),edges=len(g['edges']),nodes_by_side=dict(Counter(n['side'] for n in g['nodes'])),nodes_by_category=dict(Counter(n['category'] for n in g['nodes'])),edges_by_kind=dict(Counter(e['kind'] for e in g['edges'])),source_clauses=40)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output')
 g=json.loads((a.packet/'logical_graph.json').read_text());c=json.loads((a.packet/'coverage.json').read_text());p=json.loads((a.packet/'protocol.json').read_text());roots={'research':a.sources_root.resolve(),'public':a.public_root.resolve()};result=validate(g,c,p,roots);controls=[]
 for label in ['missing_clause','wrong_span','logical_cycle','missing_required_code','external_cost_zero','invented_L108_PDF','promote_excluded_comparison','drop_source_correction','attribution_as_premise','Lean_as_premise','drop_shared_inverse','stale_tally']:
  gg,cc,pp=copy.deepcopy(g),copy.deepcopy(c),copy.deepcopy(p)
  if label=='missing_clause':cc['rows'].pop()
  elif label=='wrong_span':gg['nodes'][0]['locators'][0]['sha256_utf8']='0'*64
  elif label=='logical_cycle':
   e=copy.deepcopy(next(e for e in gg['edges'] if e['kind']=='proof_use'));e['source'],e['target']=e['target'],e['source'];gg['edges'].append(e)
  elif label=='missing_required_code':gg['required_mathematical_programs'].pop()
  elif label=='external_cost_zero':next(n for n in gg['nodes'] if n['side']=='external')['cost']=0
  elif label=='invented_L108_PDF':gg['source_bindings']['L108']['original_pdf_available']=True
  elif label=='promote_excluded_comparison':next(r for r in cc['rows'] if r['id']=='N14')['new_outputs']=['C.Spherical']
  elif label=='drop_source_correction':next(n for n in gg['nodes'] if n['id']=='h.P.L3.2ii')['documentary_flags']=[]
  elif label=='attribution_as_premise':next(e for e in gg['edges'] if e['source']=='h.F.displacement' and e['target']=='UC.displacements')['kind']='proof_use'
  elif label=='Lean_as_premise':next(e for e in gg['edges'] if e['kind']=='formal_scope')['kind']='proof_use'
  elif label=='drop_shared_inverse':gg['edges']=[e for e in gg['edges'] if (e['source'],e['target'])!=('UC.cyclicrecognition','F.Presentation')]
  if label!='stale_tally':refresh(gg)
  else:gg['checks']['edges']+=1
  try:validate(gg,cc,pp,roots)
  except ValueError as exc:controls.append(dict(name=label,rejected=True,reason=str(exc)))
  else:raise RuntimeError('accepted corrupt control '+label)
 report=dict(status='PASS_AUTHOR_BINDING_TYPED_DAG_AND_SCOPE',**result,controls=controls,mathematical_edge_semantics_independently_reviewed=False,weights_assigned=False,new_source_credit=0,new_question_credit=0)
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
