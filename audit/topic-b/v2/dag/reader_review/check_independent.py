#!/usr/bin/env python3
"""Independent reverse-adjacency and complete-owner audit of the Topic B reader."""
from pathlib import Path
from collections import defaultdict,deque
import argparse,copy,hashlib,json,re
import xml.etree.ElementTree as ET

PIN='723026dcda12b122fd443a3f93bfa33f8b656ef39a417ebe897c49c1ce029f1d'
def need(x,s):
 if not x:raise ValueError('INDEPENDENT_B_READER_REJECT: '+s)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def audit(packet,data,public):
 g=load(packet/'inputs/logical/logical_graph.json');cov=load(packet/'inputs/logical/coverage.json')
 w=load(packet/'inputs/weighted/weights.json');p=load(packet/'inputs/weighted/partition.json')
 measurement=load(packet/'inputs/measurement/results.json')
 need(data['edges']==g['edges'],'literal accepted edge set and direction')
 need(data['source_qualifications']==g['limits'],'all accepted graph qualifications')
 need(data['measurement']==measurement,'all admitted measurement coordinates')
 owners=p['owners'];costs=w['owner_costs'];forms=['NFC','NFKC'];units=list(w['document_costs']['U_B']['NFC'])
 def count(ids):return {f:{m:sum(costs[x][f][m] for x in set(ids)) for m in units} for f in forms}
 original={n['id']:n for n in g['nodes']};view={n['id']:n for n in data['nodes']}
 need(len(view)==len(data['nodes']),'unique rendered node IDs')
 need(data['owners']==owners and data['owner_weights']==costs,'all exact passage owners')
 inverse=defaultdict(set)
 for e in g['edges']:
  if e['kind'] in g['logical_edge_kinds']:inverse[e['target']].add(e['source'])
 def predecessors(start):
  visited=set(start);q=deque(start)
  while q:
   for old in inverse[q.popleft()]:
    if old not in visited:visited.add(old);q.append(old)
  return visited
 def paid(nodes):return set().union(*(set(w['node_interfaces'][n]['owners']) for n in nodes))
 pairs={r['id']:r for r in data['pairs']}
 need(len(pairs)==34,'four application routes plus thirty clauses')
 route_checks=[]
 for row in cov['rows']:
  route=pairs['clause:'+row['adapter']]
  need(route['historical_targets']==[row['historical_output']] and route['new_targets']==row['new_outputs'],'exact clause targets '+row['adapter'])
  need(route['statement']==row['preserved_contract'],'exact preserved contract text')
  route_checks.append(dict(id=route['id'],historical_nodes=sorted(predecessors(route['historical_targets'])),new_nodes=sorted(predecessors(route['new_targets']))))
 for app,source in g['applications'].items():
  route=pairs[app]
  need(route['source']==source and route['historical_targets']==sorted({r['historical_output'] for r in cov['rows'] if r['source_id']==source}) and route['new_targets']==[g['new_application_outputs'][app]],'whole application targets')
 parent={n['id']:n['parent'] for n in g['nodes'] if n.get('parent')}
 need(data['parents']==parent,'literal actual parent memberships')
 def top(n):
  seen=set()
  while n in parent:
   need(n not in seen,'no collapsed parent cycle');seen.add(n);n=parent[n]
  return n
 for n,old in original.items():
  v=view[n];interface=w['node_interfaces'][n]
  need(v['owners']==interface['owners'] and v['weight']==interface['weight'],'correct logical node owner interface')
  need(v['documentary_validity']=='; '.join(old.get('documentary_flags',[])),'documentary qualification retained')
  closure=predecessors([n]);unique=paid(closure);c=v['closure']
  need(c['unique_owner_ids']==sorted(unique) and c['known_owned_text_subtotal']==count(unique),'independent prerequisite owner union')
  need(c['unknown_external_nodes']==sorted(x for x in closure if w['node_interfaces'][x]['weight'] is None),'unknown source/external/verification inputs retained')
  docs={owners[x]['document'] for x in unique}
  need(set(c['other_document_text_not_in_this_graph_closure'])=={x for x,o in owners.items() if o['document'] in docs and x not in unique},'paid context outside a route remains explicit')
 extras=set(view)-set(original)
 need(extras=={'owned:'+x for x in owners if x not in original},'every nonlogical cost owner present once')
 for x in owners:
  if x not in original:
   v=view['owned:'+x];need(v['owners']==[x] and v['weight']==costs[x] and v['cost_only'],'context-only accounting node')
 document_checks={}
 for doc,row in data['documents'].items():
  ids={x for x,o in owners.items() if o['document']==doc}
  if doc=='N001':need(row['weight'] is None and row['pages'] is None,'missing source never zero')
  else:
   need(row['weight']==w['document_costs'][doc]==count(ids),'complete paper equals its disjoint owner sum '+doc)
   document_checks[doc]=count(ids)
 sequence=['U_B','B1','B2','B3','B4'];source_order=['N001','N003','N008','L030'];acq=data['acquisition'];already=set();known=[]
 need(acq['sequence']==sequence and len(acq['stages'])==5,'whole-paper stage order')
 for i,row in enumerate(acq['stages']):
  doc=sequence[i];local={x for x,o in owners.items() if o['document']==doc}
  need(not already.intersection(local),'complete local documents have disjoint ownership')
  route=paid(predecessors([g['new_application_outputs'][doc]])) if i else set()
  need(row['complete_local_owner_ids']==sorted(local) and row['new_owner_ids']==sorted(local),'all local context/statement/proof/reference passages charged')
  need(row['previous_owner_ids']==sorted(already),'prior ownership exact')
  need(row['logical_route_owner_ids']==sorted(route) and row['reused_owner_ids']==sorted(route & already),'already paid recorded prerequisites')
  need(row['new_cost']==count(local) and row['reused_route_cost']==count(route & already),'new and reused cost columns')
  already.update(local)
  need(row['cumulative_owner_ids']==sorted(already) and row['cumulative_cost']==count(already),'cumulative owner union')
  need(row['full_dependency_cost'] is None,'retained full proof cost unknown')
  if i:
   if source_order[i-1]!='N001':known.append(source_order[i-1])
   h=row['historical_cumulative']
   need(h['unknown_source']=='N001' and h['unknown_coefficient']==1 and h['complete_cost'] is None,'exact symbolic missing source')
   expected={f:{m:sum(w['document_costs'][d][f][m] for d in known) for m in units} for f in forms}
   need(h['known_source_documents']==known and h['known_subtotal']==expected,'exact historical known subtotal')
 need(acq['source_cumulative_numeric_curve'] is None and acq['raw_node_ratio'] is None and acq['expanded_external_proof_cost'] is None,'no invented scalar')
 for coord in measurement['coordinates']:
  if coord['variant']!='calibrated_selected':continue
  f=coord['normalization'];m=coord['unit']
  need(coord['complete_denominator']==count(already)[f][m],'admitted complete denominator matches acquisition')
  need(coord['known_source_sum']==sum(w['document_costs'][d][f][m] for d in ['N003','N008','L030']),'admitted symbolic numerator')
 links=[]
 for n in data['nodes']:
  for loc in n.get('current_public_locators',[]):
   target=loc['path'];resolved=(public/'audit/topic-b/v2/dag/reader'/('../../../../../'+target)).resolve()
   need(resolved== (public/target).resolve() and resolved.is_file(),'five-level public proof link '+target)
   links.append(target)
 # Independently build each compact route by equivalence classes of fine nodes.
 collapsed=[]
 for route in data['pairs']:
  allids=predecessors(route['historical_targets']+route['new_targets'])
  for side in ['historical','new']:
   membership={top(n) for n in allids if original[n]['side']==side}
   arrows={(top(e['source']),top(e['target'])) for e in g['edges'] if e['kind'] in g['logical_edge_kinds'] and top(e['source']) in membership and top(e['target']) in membership and top(e['source'])!=top(e['target'])}
   collapsed.append(dict(route=route['id'],side=side,node_ids=sorted(membership),arrows=[list(e) for e in sorted(arrows)]))
 static=load(packet/'static_graph.json');b1=next(r for r in collapsed if r['route']=='B1' and r['side']=='new')
 need(static['displayed_node_ids']==b1['node_ids'] and static['displayed_edges']==[dict(source=a,target=b) for a,b in b1['arrows']],'static graph exact parent quotient')
 # Inspect actual saved browser SVG endpoint geometry, independently of JS.
 svg=ET.parse(packet/'default.svg').getroot();ns={'s':'http://www.w3.org/2000/svg'}
 rects={}
 for group in svg.findall('s:g',ns):
  if 'data-id' in group.attrib:
   rect=group.find('s:rect',ns);rects[group.attrib['data-id']]=(float(rect.attrib['x']),float(rect.attrib['y']))
 need(set(rects)==set(b1['node_ids']),'actual default SVG node membership')
 frompoint={(x+240,y+42):n for n,(x,y) in rects.items()};topoint={(x,y+42):n for n,(x,y) in rects.items()}
 svg_edges=set()
 for path in svg.findall('s:path',ns):
  if 'edge' not in path.attrib.get('class',''):continue
  numbers=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',path.attrib['d'])))
  need(len(numbers)==8,'explicit cubic prerequisite path')
  svg_edges.add((frompoint[tuple(numbers[:2])],topoint[tuple(numbers[-2:])]))
  need(path.attrib.get('stroke')=='#97a6b0' and path.attrib.get('marker-end')=='url(#arrow)','visible directed SVG path')
 need(svg_edges==set(map(tuple,b1['arrows'])),'actual default SVG edges have correct endpoints')
 return dict(status='PASS_INDEPENDENT_OWNER_AND_ROUTE_AUDIT',document_metric_cells=len(document_checks)*10,acquisition_metric_cells=100,logical_node_closure_cells=len(original)*10,clause_routes=route_checks,paired_route_quotients=collapsed,
  default_svg_nodes=len(rects),default_svg_edges=len(svg_edges),current_public_links=len(links),distinct_public_targets=len(set(links)),source_cost_N001=None,new_credits=0,raw_node_factor=None)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh report path')
 need(sha(a.packet/'manifest.json')==PIN,'exact author freeze')
 man=load(a.packet/'manifest.json')
 for row in man['exports']:
  f=a.packet/row['path'];need(f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],'frozen export '+row['path'])
 data=load(a.packet/'view_data.json');result=audit(a.packet,data,a.public_root)
 controls=[]
 for name in ['omit_context','free_umbrella','replace_unknown_by_zero','wrong_clause','wrong_parent','reverse_edge']:
  d=copy.deepcopy(data)
  if name=='omit_context':d['acquisition']['stages'][2]['new_owner_ids'].pop()
  elif name=='free_umbrella':d['acquisition']['stages'][0]['new_cost']['NFC']['characters_without_whitespace']=0
  elif name=='replace_unknown_by_zero':d['documents']['N001']['weight']=0
  elif name=='wrong_clause':d['pairs'][4]['new_targets']=['B4.Source']
  elif name=='wrong_parent':d['parents'][next(iter(d['parents']))]='B4.Source'
  elif name=='reverse_edge':d['edges'][0]['source'],d['edges'][0]['target']=d['edges'][0]['target'],d['edges'][0]['source']
  try:audit(a.packet,d,a.public_root)
  except ValueError as e:controls.append(dict(case=name,rejected=True,reason=str(e)))
  else:raise ValueError('accepted mutation '+name)
 result.update(author_manifest_sha256=PIN,controls=controls,checker_sha256=sha(Path(__file__)))
 a.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ['clause_routes','paired_route_quotients','controls']}))
if __name__=='__main__':main()
