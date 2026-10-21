#!/usr/bin/env python3
"""Check bytes, typed edges, exact scope and closures; mathematical semantics need review."""
from pathlib import Path
from collections import Counter,deque
import argparse,copy,hashlib,json
SHA=lambda b:hashlib.sha256(b).hexdigest()
LOGICAL={'proof_use','definition_use','hypothesis_use','proof_assembly','retained_input_use'}
OTHER={'attribution','validation','formal_scope','comparison','operational'}
REQUIRED={'program.exceptional','program.search','program.fusion','program.verify','program.predicates'}
DIAGNOSTICS={'diagnostic.pairs','diagnostic.fields','diagnostic.q8'}
DRIVERS={'driver.pairs','driver.enumeration'}
def need(v,s):
 if not v:raise ValueError(s)
def tally(g):return dict(nodes=len(g['nodes']),edges=len(g['edges']),nodes_by_side=dict(Counter(n['side'] for n in g['nodes'])),nodes_by_category=dict(Counter(n['category'] for n in g['nodes'])),edges_by_kind=dict(Counter(e['kind'] for e in g['edges'])),source_clauses=37)
def validate(g,c,p,roots):
 need(g['edge_orientation']==p['edge_orientation']=='prerequisite -> use','edge orientation')
 need(set(g['logical_edge_kinds'])==set(p['logical_edge_kinds'])==LOGICAL,'logical edge kinds')
 need(set(g['nonlogical_edge_kinds'])==set(p['nonlogical_edge_kinds'])==OTHER,'nonlogical edge kinds')
 need(g['compression_ratio'] is None and g['new_source_credit']==g['new_question_credit']==0,'no ratios or new credits')
 need(g['measurement']['weights_assigned'] is False and g['measurement']['exclusive_partition_assigned'] is False,'logical graph only')
 need(g['source_order']==p['source_order']==['L066','L074','L104'],'exact closed sources')
 ins={(x['namespace'],x['path']):x for x in g['immutable_inputs']};need(len(ins)==len(g['immutable_inputs']),'unique immutable inputs')
 for (ns,path),r in ins.items():
  need(ns in roots and not Path(path).is_absolute() and '..' not in Path(path).parts,'safe input path')
  b=(roots[ns]/path).read_bytes();need(len(b)==r['bytes'] and SHA(b)==r['sha256'],'immutable input '+path)
 checked=set()
 def span(s):
  key=s['namespace'],s['path'];need(key in ins,'locator input bound');t=(roots[key[0]]/key[1]).read_text();a,b=s['start_codepoint'],s['end_codepoint_exclusive'];need(0<=a<b<=len(t),'nonempty exact context');need(SHA(t[a:b].encode())==s['sha256_utf8'],'context hash');need(s['first_line']==t.count('\n',0,a)+1 and s['last_line']==t.count('\n',0,b-1)+1,'line locator');checked.add((key,a,b))
 ns={n['id']:n for n in g['nodes']};need(len(ns)==len(g['nodes']),'unique node ids')
 for n in ns.values():
  need(n['cost'] is None,'unknown cost stays null');need(n['locators'],'actual locator')
  for s in n['locators']:span(s)
 for key,s in g['source_bindings'].items():
  need(s['original_pdf_available'] is True and s['pdf_cost'] is None and s['text_cost'] is None,'available unmeasured PDF')
  need(s['primary_binding']['sha256']==ins['research',s['primary']['path']]['sha256']==s['primary']['sha256'],'source exact edition')
 pairs=set();pred={n:[] for n in ns};succ={n:[] for n in ns};degrees={n:0 for n in ns}
 for e in g['edges']:
  s,t,k=e['source'],e['target'],e['kind'];need(s in ns and t in ns and s!=t,'edge endpoints');need(k in LOGICAL|OTHER,'edge type');need((s,t,k) not in pairs,'no duplicate edges');pairs.add((s,t,k));need(e['evidence'] and e['target_evidence'] and e['necessity_claim'] is False,'evidence without logical-minimality claim')
  for l in e['target_evidence']:span(l)
  if k in LOGICAL:
   need(ns[s]['side']!='verification' and ns[t]['side']!='verification','formal/diagnostic/driver not a mathematical premise')
   need(not(ns[s]['side']=='historical' and ns[t]['side']=='new'),'no old paper as hidden current proof premise')
   pred[t].append(s);succ[s].append(t);degrees[t]+=1
 q=deque(n for n,d in degrees.items() if d==0);order=[]
 while q:
  x=q.popleft();order.append(x)
  for y in succ[x]:
   degrees[y]-=1
   if degrees[y]==0:q.append(y)
 need(len(order)==len(ns),'logical DAG acyclic')
 def closure(outputs):
  seen=set(outputs);todo=list(outputs)
  for x in todo:
   need(x in ns,'closure node exists')
   for y in pred[x]:
    if y not in seen:seen.add(y);todo.append(y)
  return sorted(seen)
 need(g['checks']==tally(g),'inventory agrees; counts not a complexity measure')
 original=json.loads((roots['public']/p['authoritative_scope']).read_text());old={r['id']:r for r in original['contracts']};rows={r['id']:r for r in c['rows']}
 need(len(rows)==len(c['rows'])==p['accepted_contract_rows']==37 and set(rows)==set(old),'all 37 exact contract rows')
 for id,r in rows.items():
  need(r['accepted_record']==old[id],'exact accepted record '+id)
  need(r['historical_outputs']==['h.'+id] and ns['h.'+id]['document']==r['source'],'source output identity')
  need(all(ns[n]['side']=='new' and ns[n]['category']=='proved_statement' for n in r['new_outputs']),'only proved/qualified current outputs')
  need(all(ns[n]['side']=='external' for n in r['retained_input_nodes']),'retained inputs distinct')
  need(all(ns[n]['side']=='new' and ns[n]['category'] in ['scope_context','definition'] for n in r['qualification_context_nodes']),'qualifications explicit context')
  need(r['historical_closure']==closure(r['historical_outputs']) and r['new_closure']==closure(r['new_outputs']) and r['retained_context_closure']==closure(r['retained_input_nodes']),'actual row closures '+id)
  need(r['cost'] is None,'no row cost')
 need(rows['L104.4']['coverage_kind']=='excluded' and rows['L104.4']['new_outputs']==[] and rows['L104.4']['qualification_context_nodes']==['D3.Exclusions'],'no excluded diagrams/Aut/Cor/doubling recovery')
 need(rows['L074.8']['coverage_kind']=='unused_background' and rows['L074.8']['new_outputs']==[],'unused coprimality not rederived')
 for id in ['L074.6','L074.7','L074.10','L074.16']:need(not rows[id]['new_outputs'] and rows[id]['retained_input_nodes'],'retained background not silently proved')
 need(not rows['L066.9']['new_outputs'],'historical attribution not a new theorem')
 need(ns['h.L066.5']['documentary_flags'] and ns['h.L066.6']['documentary_flags'] and ns['h.L066.13']['documentary_flags'],'source corrections/scopes visible')
 need(set(g['required_mathematical_programs'])==REQUIRED and set(g['diagnostic_programs'])==DIAGNOSTICS and set(g['operational_drivers'])==DRIVERS,'complete program roles')
 for id in REQUIRED:need(ns[id]['category']=='required_program' and ns[id]['side']=='new','required mathematical program node')
 for id in DIAGNOSTICS|DRIVERS:need(ns[id]['side']=='verification','diagnostics/drivers nonlogical')
 for s,outs in g['new_application_outputs'].items():
  need(outs==sorted({o for r in rows.values() if r['source']==s for o in r['new_outputs']}),'application output boundary')
  need(g['new_output_closures'][s]==closure(outs),'application closure')
 need(REQUIRED & set(g['new_output_closures']['L066'])=={'program.exceptional'},'D1 only required exceptional code')
 need(REQUIRED <= set(g['new_output_closures']['L066'])|set(g['new_output_closures']['L104']),'all five required programs in actual closures')
 need(not (REQUIRED|DIAGNOSTICS|DRIVERS)&set(g['new_output_closures']['L074']),'uniform Suzuki proof not finite sampling')
 for id,cl in g['additional_current_outputs'].items():need(cl==closure([id]),'additional output closure')
 need(g['unused_common_statement_nodes']==['UD.Normalizer'] and all('UD.Normalizer' not in cl for cl in g['new_output_closures'].values()),'unused normalizer not silently claimed shared/removed')
 need(len(original['proof_spans'])==len(g['accepted_scope_spans'])==p['accepted_proof_context_spans']==19,'all existing proof spans bound')
 for key,s in g['accepted_scope_spans'].items():
  v=original['proof_spans'][key];span(s);need(s['path']=='papers/topic-d/v2/'+v['path'] and (s['start_codepoint'],s['end_codepoint_exclusive'],s['sha256_utf8'])==(v['start_codepoint'],v['end_codepoint_exclusive'],v['sha256_utf8']),'unchanged accepted proof span')
 need(g['formal_evidence']==dict(initial_report_count=10,later_support_report_count=28,later_components=[12,16],first_support_12_counted_again=False,source_specific_instantiations_claimed=False,divisor_number_theoretic_bridge_verified=False),'exact formal scope; no 12+28 double count')
 routes=[('UD.ExtensionOrbits','UD.AdmissibleExtensions'),('ext.Mobius','UD.AdmissibleExtensions'),('UD.AdmissibleExtensions','UD.ExactSupport'),('UD.OrbitData','D1.Multiplicities'),('D1.Reversal','D1.Symmetric'),('UD.ExtensionOrbits','D1.Exceptional'),('program.exceptional','D1.Exceptional'),('D2.Normalization','D2.SubfieldPosition'),('D2.SubfieldPosition','D2.Generation'),('ext.SuzukiMaximals','D2.Generation'),('D2.Generation','D2.IP'),('D2.Generation','D2.Support'),('UD.ExactSupport','D2.Support'),('UD.OddOrbits','D2.Duality'),('UD.ExtensionOrbits','D2.Fibers'),('D2.Fibers','D2.Nested'),('UD.Helly','UD.PanelRecognition'),('UD.PanelRecognition','UD.MaximalAugmentation'),('UD.Transport','UD.MaximalAugmentation'),('UD.ExtensionOrbits','UD.MaximalAugmentation'),('ext.TomLib','D3.Interfaces'),('program.search','D3.Candidates'),('program.fusion','D3.Fusion'),('program.verify','D3.Verified'),('UD.PanelRecognition','program.search'),('UD.LocalTests','program.search'),('D1.Multiplicities','D1.Series'),('h.L066.16','h.L066.4'),('h.L066.16','h.L066.2'),('h.L074.subfields','h.L074.14'),('h.L104.oldsearch','h.L104.2'),('program.predicates','program.verify'),('UD.Termination','D3.NoHigher'),('h.L066.5','h.L066.diagonal'),('h.L074.8','h.L074.IP'),('ext.Leemans2006','h.L074.3'),('h.L104.oldsearch','h.L104.1'),('h.L104.extension','h.L104.1')]
 for s,t in [('program.predicates','program.search'),('D1.Ordered','D1.Series'),('D1.Reversal','D1.Series')]:need(not any(a==s and b==t and k in LOGICAL for a,b,k in pairs),'removed documentary edge must stay absent')
 for s,t in routes:need(any(a==s and b==t and k in LOGICAL for a,b,k in pairs),'required direct route '+s+' -> '+t)
 need(not any(e['source']=='ext.Leemans2006' and ns[e['target']]['side']=='new' and e['kind'] in LOGICAL for e in g['edges']),'no extra old rank theorem premise in current rederivation')
 return dict(**tally(g),immutable_inputs=len(ins),unique_context_spans=len(checked),accepted_context_spans=19,logical_acyclic=True)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent);ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output file')
 g=json.loads((a.packet/'logical_graph.json').read_text());c=json.loads((a.packet/'coverage.json').read_text());p=json.loads((a.packet/'protocol.json').read_text());roots={'research':a.study_root,'public':a.public_root};result=validate(g,c,p,roots);controls=[]
 for label in ['omitted_clause','wrong_span','logical_cycle','required_code_dropped','required_route_dropped','diagnostic_as_proof','formal_as_proof','attribution_as_proof','excluded_diagrams_recovered','classical_input_claimed_proved','source_correction_hidden','external_cost_zero','support_reports_double_counted','divisor_bridge_overclaim','stale_inventory','exact_support_route_omitted']:
  gg,cc,pp=copy.deepcopy(g),copy.deepcopy(c),copy.deepcopy(p)
  if label=='omitted_clause':cc['rows'].pop()
  elif label=='wrong_span':gg['nodes'][0]['locators'][0]['sha256_utf8']='0'*64
  elif label=='logical_cycle':
   e=copy.deepcopy(next(e for e in gg['edges'] if e['kind']=='proof_use'));e['source'],e['target']=e['target'],e['source'];gg['edges'].append(e)
  elif label=='required_code_dropped':gg['required_mathematical_programs'].pop()
  elif label=='required_route_dropped':gg['edges']=[e for e in gg['edges'] if (e['source'],e['target'])!=('program.verify','D3.Verified')]
  elif label=='diagnostic_as_proof':
   e=next(e for e in gg['edges'] if e['kind']=='validation' and e['target']=='diagnostic.fields');e['source'],e['target'],e['kind']=e['target'],e['source'],'proof_use'
  elif label=='formal_as_proof':next(e for e in gg['edges'] if e['kind']=='formal_scope')['kind']='proof_use'
  elif label=='attribution_as_proof':next(e for e in gg['edges'] if e['source']=='h.L066.5' and e['kind']=='attribution')['kind']='proof_use'
  elif label=='excluded_diagrams_recovered':next(r for r in cc['rows'] if r['id']=='L104.4')['new_outputs']=['D3.Verified']
  elif label=='classical_input_claimed_proved':next(r for r in cc['rows'] if r['id']=='L074.16')['new_outputs']=['D2.Generation']
  elif label=='source_correction_hidden':next(n for n in gg['nodes'] if n['id']=='h.L066.5')['documentary_flags']=[]
  elif label=='external_cost_zero':next(n for n in gg['nodes'] if n['side']=='external')['cost']=0
  elif label=='support_reports_double_counted':gg['formal_evidence']['later_support_report_count']=40
  elif label=='divisor_bridge_overclaim':gg['formal_evidence']['divisor_number_theoretic_bridge_verified']=True
  if label=='exact_support_route_omitted':gg['edges']=[e for e in gg['edges'] if (e['source'],e['target'])!=('UD.ExactSupport','D2.Support')]
  if label=='stale_inventory':gg['checks']['edges']+=1
  else:gg['checks']=tally(gg)
  try:validate(gg,cc,pp,roots)
  except ValueError as exc:controls.append(dict(name=label,rejected=True,reason=str(exc)))
  else:raise RuntimeError('corruption accepted '+label)
 report=dict(status='PASS_AUTHOR_LOGICAL_BINDINGS_SCOPE_AND_CONTROLS',**result,negative_controls=controls,independent_semantic_review=False,primary_text_exported=False,weights_assigned=False,compression_ratio=None,new_source_credit=0,new_question_credit=0)
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['nodes_by_category','nodes_by_side','edges_by_kind','negative_controls']}))
if __name__=='__main__':main()
