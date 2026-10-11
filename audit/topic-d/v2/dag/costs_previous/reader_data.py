#!/usr/bin/env python3
"""Derived offline reader. Mathematical and cost originals remain separate."""
import argparse,json
from pathlib import Path
from accounting import add,need,sha
HERE=Path(__file__).resolve().parent
TITLES={'CODE':'Complete programs for finite geometry enumeration'}
def load(p):return json.loads(p.read_text())
def closure(targets,g):
 seen=set(targets);todo=list(targets)
 while todo:
  at=todo.pop()
  for e in g['edges']:
   if e['target']==at and e['kind'] in g['logical_edge_kinds'] and e['source'] not in seen:seen.add(e['source']);todo.append(e['source'])
 return sorted(seen)
def acquisition(p,w,g):
 stages=[];paid=set();known=[];unknown_history=False;previous_external=set();source_by_app={a:s for s,a in g['applications'].items()}
 for key in ['U_D','CODE','D1','D2','D3']:
  full={n for n,o in p['owners'].items() if o['document']==key}
  targets=[n['id'] for n in g['nodes'] if n['document']==key and not n['id'].startswith('program.')]
  names=closure(targets,g)
  used={o for n in names for o in w['node_interfaces'][n]['owners']}
  need(not used-paid-full,'all local paper prerequisites previously acquired '+key)
  added=full-paid;allpaid=paid|full
  need(added==full,'full current local paper charged')
  unknown=sorted(n for n in names if w['node_interfaces'][n]['known_weight'] is None)
  history=None
  if key in source_by_app:
   source=source_by_app[key]
   if source in w['document_costs']:known.append(source)
   else:unknown_history=True
   history={'known_documents':known[:],'known_subtotal':add(w['document_costs'][d] for d in known),'unknown_source':None,'unknown_coefficient':int(unknown_history),'complete_cost':None if unknown_history else add(w['document_costs'][d] for d in known)}
  stages.append({'stage':key,'previous_owner_ids':sorted(paid),'complete_local_owner_ids':sorted(full),'logical_route_owner_ids':sorted(used),'new_owner_ids':sorted(added),'cumulative_owner_ids':sorted(allpaid),'new_cost':add(w['owner_costs'][n] for n in added),'cumulative_cost':add(w['owner_costs'][n] for n in allpaid),'written_cumulative_cost':add(w['owner_costs'][n] for n in allpaid if p['owners'][n]['document']!='CODE'),'reused_owner_ids':sorted(used&paid),'reused_route_cost':add(w['owner_costs'][n] for n in used&paid),'local_text_outside_route':sorted(full-used),'unknown_inputs':unknown,'new_unknown_inputs':sorted(set(unknown)-previous_external),'expanded_cost':None,'historical_cumulative':history})
  paid=allpaid;previous_external.update(unknown)
 return {'stages':stages,'sequence':[r['stage'] for r in stages],'historical_complete_numeric_curve':[x['historical_cumulative']['complete_cost'] for x in stages if x['historical_cumulative']],'scope':'Whole common theory and complete programs acquired once, then each full local application including context. Not a shortest proof or elapsed research effort.','expanded_external_proof_cost':None,'graphic_cost':None}
def build(root,packet):
 g=load(root/'topic_D_logical_dag_v2/logical_graph.json');c=load(root/'topic_D_logical_dag_v2/coverage.json');w=load(packet/'weights.json');p=load(packet/'partition.json');m=load(root/'topic_D_measurement_results/results.json')
 specs=load(root/'topic_D_measurement_v2/source_input_spec.json')['sources']|load(root/'topic_D_measurement_v2/replacement_input_spec.json')['ours']
 public=load(root/'topic_D_measurement_v2/publication_binding.json')['scientific_documents']
 title=TITLES|{k:v['title'] for k,v in g['source_bindings'].items()}|g['document_titles'];docs={}
 CITES={k:{'authors':', '.join(v['authors'])+' ('+str(v['year'])+')','edition':v['edition'],'primary_urls':[]} for k,v in g['source_bindings'].items()}
 for k,t in title.items():
  b=specs.get(k);docs[k]={'title':t,'pages':b['pages'] if b else None,'weight':w['document_costs'].get(k),'side':'historical' if k in g['source_order'] else 'new','path':public[k]['public_path'] if k in public else None,'citation':CITES.get(k)}
 nodes=[];parents={n['id']:n['parent'] for n in g['nodes'] if n.get('parent')};known={n['id'] for n in g['nodes']}
 for n in g['nodes']:
  link=w['node_interfaces'][n['id']];ns=closure([n['id']],g);paid=sorted({o for i in ns for o in w['node_interfaces'][i]['owners']});documents={p['owners'][o]['document'] for o in paid}
  nodes.append(dict(n,document=n['document'] or 'external',side='historical' if n['side']=='historical' else 'new',external=link['known_weight'] is None,verification=n['side']=='verification',owners=link['owners'],weight=link['known_weight'],raw_driver=w['raw_operational_drivers'].get(n['id']),program_role=('diagnostic' if n['id'].startswith('diagnostic.') else 'required' if n['id'].startswith('program.') else None),weight_scope='Unite shared passage owners before summing; this box is not an additional charge.',cost_only=False,shared_code_alias=n['id'].startswith(('program.','diagnostic.')),documentary_validity='; '.join(n['documentary_flags']),current_public_locators=[l for l in n['locators'] if l['namespace']=='public'],closure={'unique_owner_ids':paid,'known_owned_text_subtotal':add(w['owner_costs'][o] for o in paid),'unknown_external_nodes':[i for i in ns if w['node_interfaces'][i]['known_weight'] is None],'other_document_text_not_in_this_graph_closure':[o for o,x in p['owners'].items() if x['document'] in documents and o not in paid]}))
 owners={n:dict(o,label=n+' — '+o['category'].replace('_',' ')) for n,o in p['owners'].items()}
 for n,o in owners.items():
  if n not in known:
   nodes.append(dict(id='owned:'+n,label=o['label'],document=o['document'],side='historical' if o['document'] in g['source_order'] else 'new',category=o['category'],owners=[n],weight=w['owner_costs'][n],weight_scope='Exclusive text owner; no extra mathematical implication.',external=False,verification=False,cost_only=True,shared_code_alias=False,locators=[s for s in p['documents'][o['document']]['variants']['calibrated_selected']['spans'] if s['owner']==n],closure=None))
 pairs=[]
 for source,app in g['applications'].items():
  rows=[r for r in c['rows'] if r['source']==source]
  pairs.append({'id':app,'source':source,'title':title[app],'historical_targets':sorted({n for r in rows for n in r['historical_outputs']}),'new_targets':g['new_application_outputs'][source],'statement':'Fixed complete application contract; the complete-paper comparison is shown separately from this selected prerequisite union.'})
 for r in c['rows']:
  record=r['accepted_record'];pairs.append({'id':'clause:'+r['id'],'source':r['source'],'title':r['id']+' — '+r['coverage_kind'],'historical_targets':r['historical_outputs'],'new_targets':r['new_outputs'],'context_targets':r['retained_input_nodes']+r['qualification_context_nodes'],'statement':record['reference']+': '+record.get('conclusion','The source clause and its qualifications are located in the graph below.')+' Status: '+r['coverage_kind'].replace('_',' ')+('. No recovered proof output; the view shows the retained input or qualification only.' if not r['new_outputs'] else '')})
 for name,names in g['additional_current_outputs'].items():
  target=next(n for n in g['nodes'] if n['id']==name)
  source=next(k for k,v in g['applications'].items() if v==target['document'])
  pairs.append({'id':'additional:'+name,'source':source,'title':target['label'],'historical_targets':[],'new_targets':[name],'statement':'Additional current output; no historical counterpart or new source credit is asserted.'})
 data={'title':'Stabilizers, support and finite geometry enumeration','nodes':nodes,'edges':g['edges'],'parents':parents,'logical_edge_kinds':g['logical_edge_kinds'],'documents':docs,'pairs':pairs,'owner_weights':w['owner_costs'],'owners':owners,'measurement':m,'acquisition':acquisition(p,w,g),'counts':g['checks'],'logical_node_count':len(g['nodes']),'edge_count':len(g['edges']),'owner_count':len(owners),'source_qualifications':g['limits'],'review_status':'Logical graph and complete-document measurements independently accepted. This new ownership and reader packet is an author proposal awaiting independent review.','bindings':{str(f.relative_to(root)):sha(f.read_bytes()) for f in [root/'topic_D_logical_dag_v2/manifest.json',root/'topic_D_logical_dag_independent_review/manifest.json',root/'topic_D_measurement_results/manifest.json']}}
 return data

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--packet',type=Path,default=HERE);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh reader directory');a.out.mkdir(parents=True)
 data=build(a.study_root,a.packet)
 for f,x in [('view_data.json',data),('acquisition.json',data['acquisition'])]:(a.out/f).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
 html=(HERE/'explorer_template.html').read_text().replace('__CSS__',(HERE/'explorer.css').read_text()).replace('__JS__',(HERE/'explorer.js').read_text()).replace('__DATA__',json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/'))
 (a.out/'explorer.html').write_text(html)
 print(json.dumps({'nodes':len(data['nodes']),'routes':len(data['pairs']),'stages':len(data['acquisition']['stages'])}))
if __name__=='__main__':main()
