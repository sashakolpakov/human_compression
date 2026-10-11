#!/usr/bin/env python3
"""Build a derived Topic B reader from immutable reviewed accounting inputs."""
import argparse,collections,hashlib,json,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent
FILES={
 'logical/logical_graph.json':'topic_B_logical_dag_v2/logical_graph.json',
 'logical/coverage.json':'topic_B_logical_dag_v2/coverage.json',
 'logical/manifest.json':'topic_B_logical_dag_v2/manifest.json',
 'logical_review/manifest.json':'topic_B_logical_independent_review/manifest.json',
 'weighted/partition.json':'topic_B_weighted_dag_v2/partition.json',
 'weighted/weights.json':'topic_B_weighted_dag_v2/weights.json',
 'weighted/manifest.json':'topic_B_weighted_dag_v2/manifest.json',
 'weighted/correction.json':'topic_B_weighted_dag_v2/correction.json',
 'ownership_review/manifest.json':'topic_B_weighted_independent_review/manifest.json',
 'ownership_review/review.json':'topic_B_weighted_independent_review/review.json',
 'measurement/results.json':'topic_B_measurement_results/results.json',
 'measurement/manifest.json':'topic_B_measurement_results/manifest.json',
 'measurement/source_input_spec.json':'topic_B_measurement/source_input_spec.json',
 'measurement/replacement_input_spec.json':'topic_B_measurement/replacement_input_spec.json',
 'measurement/arithmetic_review_manifest.json':'topic_B_arithmetic_independent_review/manifest.json'}
PINS={'logical/manifest.json':'a825b42e248e2d4fe9a853ff0baefb40c7590642eca8b028e0d6471333e5bf4b',
 'logical_review/manifest.json':'5d848fc049ee84bacd7b38332ce413ffd378228af7f1d568a26448c9935b980f',
 'weighted/manifest.json':'9469f228653cbaee9da9d01fad578b0e842f9bca0337ee850fea7f2b027eceda',
 'ownership_review/manifest.json':'0d56e0f4f3eedbb49743ab10cfa486f70899dd1569452a8be128d687921d7424',
 'measurement/manifest.json':'c61503c52b1e0136b0eb70ebe7993c63dc635933e6ae0bf9a50d7c164d211609'}

def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def save(p,j):p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
def total(ids,costs):
 sample=next(iter(costs.values()))
 return {f:{m:sum(costs[i][f][m] for i in set(ids)) for m in row} for f,row in sample.items()}
def closure(targets,g):
 seen=set(targets);todo=list(targets);logical=set(g['logical_edge_kinds'])
 while todo:
  target=todo.pop()
  for edge in g['edges']:
   if edge['target']==target and edge['kind'] in logical and edge['source'] not in seen:
    seen.add(edge['source']);todo.append(edge['source'])
 return sorted(seen)

def acquisition(p,w,g):
 rows=[];paid=set();previous_external=set();history_known=[]
 for i,key in enumerate(['U_B','B1','B2','B3','B4']):
  full={k for k,o in p['owners'].items() if o['document']==key}
  route=w['new_application_closures'].get(key)
  used=set(route['owners']) if route else set()
  missing=used-paid-full
  need(not missing,'every written prerequisite already paid or included in the complete local paper')
  wanted=paid|full|used;increment=wanted-paid
  unknown=set(route['unknown_inputs']) if route else {name for name in closure([n['id'] for n in g['nodes'] if n['document']=='U_B'],g) if name.startswith('ext.')}
  rows.append(dict(stage=key,previous_owner_ids=sorted(paid),complete_local_owner_ids=sorted(full),
   logical_route_owner_ids=sorted(used),reused_owner_ids=sorted(used&paid),new_owner_ids=sorted(increment),
   cumulative_owner_ids=sorted(wanted),new_cost=total(increment,w['owner_costs']),cumulative_cost=total(wanted,w['owner_costs']),
   reused_route_cost=total(used&paid,w['owner_costs']),local_text_outside_route=sorted(full-used),
   unknown_external_inputs=sorted(unknown),newly_encountered_unknown_external_inputs=sorted(unknown-previous_external),full_dependency_cost=None))
  need(increment==full,'complete paper acquisition equals its entire local ownership set')
  paid=wanted;previous_external|=unknown
  if key!='U_B':
   source=g['applications'][key]
   if source in w['document_costs']:history_known.append(source)
   rows[-1]['historical_cumulative']={'unknown_source':'N001','unknown_coefficient':1,'known_source_documents':history_known[:],
    'known_subtotal':{f:{m:sum(w['document_costs'][d][f][m] for d in history_known) for m in coords} for f,coords in w['document_costs']['U_B'].items()},'complete_cost':None}
 return dict(sequence=[r['stage'] for r in rows],scope='Entire common paper initially paid, then each complete application including context and references. This is a declared reading/acquisition order, not a claim about shortest proofs.',stages=rows,
  source_cumulative_numeric_curve=None,expanded_external_proof_cost=None,graphic_cost=None,raw_node_ratio=None)

CITATIONS={
 'N001':{'authors':'F. Buekenhout and P. Cara (1998)','primary_urls':['https://doi.org/10.36045/bbms/1103409005'],'edition':'Authored browser rendering; original PDF unavailable.'},
 'N003':{'authors':'P. J. Cameron and P. Cara (2002)','primary_urls':['https://doi.org/10.1016/S0021-8693(02)00550-1'],'edition':'Complete twelve-page author manuscript.'},
 'N008':{'authors':'C. Archer, P. Cara and J. Krempa (2005)','primary_urls':[],'edition':'Published nine-page article, Beiträge zur Algebra und Geometrie 46(1), 169–177.'},
 'L030':{'authors':'N. Garcia-Colin and D. Leemans','primary_urls':['https://doi.org/10.26493/2590-9770.1328.902'],'edition':'Exact revised institutional manuscript associated with the 2021 publication.'}}

def derive(inputs):
 g=load(inputs/'logical/logical_graph.json');c=load(inputs/'logical/coverage.json');w=load(inputs/'weighted/weights.json');p=load(inputs/'weighted/partition.json');m=load(inputs/'measurement/results.json')
 specs=load(inputs/'measurement/source_input_spec.json')['sources']|load(inputs/'measurement/replacement_input_spec.json')['ours']
 nodes=[];parents={n['id']:n['parent'] for n in g['nodes'] if n.get('parent')};known={n['id'] for n in g['nodes']}
 for n in g['nodes']:
  row=dict(n);link=w['node_interfaces'][n['id']];ids=closure([n['id']],g);paid=sorted({x for k in ids for x in w['node_interfaces'][k]['owners']})
  docs={p['owners'][k]['document'] for k in paid}
  row.update(external=n['side'] in ['external','verification'],verification=n['side']=='verification',side='historical' if n['side']=='historical' else 'new',document=n['document'] or 'external',owners=link['owners'],weight=link['weight'],weight_scope=link['cost_status'],cost_only=False,shared_code_alias=False,
   documentary_validity='; '.join(n.get('documentary_flags',[])),current_public_locators=[l for l in n['locators'] if l.get('namespace')=='public'],
   closure={'unique_owner_ids':paid,'known_owned_text_subtotal':total(paid,w['owner_costs']),'unknown_external_nodes':[k for k in ids if w['node_interfaces'][k]['weight'] is None],
   'other_document_text_not_in_this_graph_closure':[k for k,o in p['owners'].items() if o['document'] in docs and k not in paid]})
  nodes.append(row)
 for key,o in p['owners'].items():
  if key in known:continue
  nodes.append(dict(id='owned:'+key,label=o['label'],document=o['document'],side='historical' if o['document'] in g['source_order'] else 'new',category=o['category'],owners=[key],weight=w['owner_costs'][key],weight_scope='Exclusive passage; no additional mathematical implication is asserted.',external=False,verification=False,cost_only=True,shared_code_alias=False,locators=[s for s in p['documents'][o['document']]['spans'] if s['node']==key],closure=None))
 documents={}
 for key,title in g['document_titles'].items():
  row=specs.get(key);new=key not in g['source_order'];path='papers/topic-b/v2/'+Path(row['path']).name if row and new else None
  documents[key]=dict(title=title,pages=len(row['page_bindings']) if row else None,side='new' if new else 'historical',path=path,weight=w['document_costs'].get(key),citation=dict(CITATIONS[key],title=title,bound_edition_title=title) if key in CITATIONS else None)
 pairs=[]
 for app,source in g['applications'].items():
  rows=[r for r in c['rows'] if r['source_id']==source]
  pairs.append(dict(id=app,source=source,title=documents[app]['title'],historical_targets=sorted({r['historical_output'] for r in rows}),new_targets=[g['new_application_outputs'][app]]))
 for r in c['rows']:
  pairs.append(dict(id='clause:'+r['adapter'],source=r['source_id'],title=r['source_reference'],historical_targets=[r['historical_output']],new_targets=r['new_outputs'],statement=r['preserved_contract']))
 return dict(title='Forest coordinates and relative generation',nodes=nodes,edges=g['edges'],parents=parents,logical_edge_kinds=g['logical_edge_kinds'],documents=documents,pairs=pairs,owner_weights=w['owner_costs'],owners=p['owners'],measurement=m,acquisition=acquisition(p,w,g),
  counts=g['checks'],logical_node_count=len(g['nodes']),edge_count=len(g['edges']),owner_count=len(p['owners']),source_qualifications=g['limits'],review_status='Logical dependencies, exclusive passage ownership and whole-document measurements independently accepted. This separate reader remains subject to independent review; see its bound review records.',public_target='audit/topic-b/v2/dag/reader',not_primary_text=True,
  bindings={str(q.relative_to(inputs)):sha(q) for q in sorted(inputs.rglob('*.json'))})

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh reader output directory required');a.out.mkdir(parents=True);bindings=[]
 for target,source in FILES.items():
  q=a.study_root/source;h=sha(q)
  if target in PINS:need(h==PINS[target],'frozen input '+source)
  dest=a.out/'inputs'/target;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(q,dest)
  bindings.append(dict(private_path=source,reader_path='inputs/'+target,bytes=q.stat().st_size,sha256=h))
 for folder in ['logical','weighted','measurement','ownership_review']:
  manifest=load(a.out/'inputs'/folder/'manifest.json')
  for row in manifest['exports']:
   local=a.out/'inputs'/folder/row['path']
   if local.exists():need(sha(local)==row['sha256'],'frozen export '+str(local))
 data=derive(a.out/'inputs');save(a.out/'view_data.json',data);save(a.out/'acquisition.json',data['acquisition']);save(a.out/'input_bindings.json',bindings)
 payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
 html=(HERE/'explorer_template.html').read_text().replace('__CSS__',(HERE/'explorer.css').read_text()).replace('__DATA__',payload).replace('__JS__',(HERE/'explorer.js').read_text())
 (a.out/'explorer.html').write_text(html)
 print(json.dumps({'status':'UNFROZEN_DERIVED_READER','nodes':len(data['nodes']),'logical_nodes':data['logical_node_count'],'fine_edges':data['edge_count'],'clauses':30,'acquisition_stages':5,'out':str(a.out)}))
if __name__=='__main__':main()
