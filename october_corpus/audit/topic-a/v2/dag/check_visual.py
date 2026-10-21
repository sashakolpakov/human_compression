#!/usr/bin/env python3
"""Check the derived explorer against the unchanged graph and ownership files."""
from pathlib import Path
import argparse,copy,hashlib,json,re,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
def need(value,message):
 if not value:raise ValueError(message)
def load(path):return json.loads(path.read_text())
def validate(view):
 I=HERE/'inputs';g=load(I/'logical/logical_graph.json');w=load(I/'weighted/weights.json');p=load(I/'weighted/partition.json')
 spec=load(I/'public_input_spec.json');protocol=load(HERE/'protocol.json');coverage=load(I/'logical/coverage.json');citations=load(HERE/'citations.json')
 by={n['id']:n for n in view['nodes']};need(len(by)==len(view['nodes']),'Unique display IDs')
 need(view['edges']==g['edges'],'All original directed edges, evidence and kinds')
 need(view['parents']=={n['id']:n['parent'] for n in g['nodes'] if n.get('parent')},'Original grouping')
 need(view['factors']==load(I/'measurement.json')['factors'],'Admitted factors unchanged')
 need(view['owner_weights']==w['owner_weights'] and view['owners']==p['owners'],'Exclusive owner data')
 need(view['logical_node_count']==len(g['nodes']) and view['edge_count']==len(g['edges']),'Graph totals')
 need(view['owner_count']==len(p['owners']),'Owner count')
 need(set(view['documents'])==set(p['documents']),'Complete documents')
 for key,doc in view['documents'].items():
  need(doc['weight']==w['document_totals'][key],'Document metric '+key)
  need(doc['path']==(spec['sources']|spec['ours'])[key]['path'],'Final edition route '+key)
  need(doc['pages']==p['documents'][key]['pages'] and doc['title']==p['documents'][key]['title'],'Title/pages '+key)
  if key in spec['sources']:need(doc['citation']==citations['sources'][key],'Source citation metadata')
 for n in g['nodes']:
  d=by[n['id']];interface=w['logical_node_cost_interfaces'][n['id']]
  for key,value in n.items():
   if key!='side':need(d[key]==value,'Original node field '+n['id']+'/'+key)
  need(d['owners']==interface['owners'] and d['weight']==interface['weight'],'Owner interface '+n['id'])
  need(d['closure']==w['logical_closures'].get(n['id']),'Recorded closure '+n['id'])
  need(d['external']==(n['category']=='external'),'External status')
  if d['external']:need(d['weight'] is None,'Unknown external cost stays unknown')
  current=[dict(l,original_private_path=l['path'],path=protocol['current_evidence_routes'][l['path']]['path']) for l in n.get('locators',[]) if isinstance(l,dict) and l.get('path') in protocol['current_evidence_routes']]
  need(d['current_public_locators']==current,'Current proof locator mapping '+n['id'])
 known={n['id'] for n in g['nodes']};extra={i for i in p['owners'] if i not in known}
 need({n['id'] for n in view['nodes'] if n['cost_only']}=={'owned:'+i for i in extra},'Cost-only owner boxes')
 for i in extra:
  d=by['owned:'+i];need(d['owners']==[i] and d['weight']==w['owner_weights'][i],'Cost-only interface')
 need(all(e['source'] in known and e['target'] in known for e in view['edges']),'No invented cost-only edges')
 for pair in view['pairs']:
  targets=sorted({node for row in coverage['rows'] if row['source_id']==pair['source'] for node in row['new_nodes']})
  need(pair['new_targets']==targets,'Declared current contract targets')
 need({p['id'] for p in view['pairs']}==set(spec['application_sequence']),'Six paired routes')
 need(view['public_target']=='audit/topic-a/v2/dag','HTML publication depth')
 return {'logical_nodes':len(known),'fine_edges':len(g['edges']),'display_nodes':len(by),'documents':len(view['documents'])}
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--visual-dir',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'Fresh report path required')
 view=load(a.visual_dir/'view_data.json');summary=validate(view)
 html=(a.visual_dir/'explorer.html').read_text();embedded=re.search(r'<script id="data" type="application/json">(.*?)</script>',html,re.S)
 need(embedded is not None and json.loads(embedded.group(1))==view,'Embedded payload exact')
 for path in ('explorer.js','explorer.css'):need((HERE/path).read_text() in html,'Actual UI source '+path)
 svg=ET.parse(a.visual_dir/'default_view.svg').getroot();ns={'s':'http://www.w3.org/2000/svg'}
 paths=[x for x in svg.findall('s:path',ns) if x.get('class','').startswith('edge ')]
 need(paths and all(x.get('fill')=='none' and x.get('stroke') and x.get('marker-end') for x in paths),'Explicit SVG edge rendering attributes')
 tests=load(a.visual_dir/'javascript_checks.json');need(tests['status']=='PASS_JAVASCRIPT_INTERFACE_CHECKS' and tests['metric_coordinates']==10,'DOM interface replay')
 need(tests['real_browser_layout_test'] is False,'Do not claim browser layout verification')
 controls=[]
 def reject(name,edit):
  bad=copy.deepcopy(view);edit(bad)
  try:validate(bad)
  except (ValueError,KeyError):controls.append(name)
  else:raise ValueError('Control accepted '+name)
 reject('reversed_semantic_arrow',lambda v:v['edges'][0].update(source=v['edges'][0]['target'],target=v['edges'][0]['source']))
 reject('unknown_external_zero',lambda v:next(n for n in v['nodes'] if n['external']).update(weight=0))
 reject('wrong_A6_edition_route',lambda v:v['documents']['A6'].update(path='old.pdf'))
 reject('changed_factor',lambda v:v['factors']['NFC']['calibrated_selected']['characters_without_whitespace']['written_topic'].update(decimal=12))
 report={'status':'PASS_DERIVED_VIEW_PENDING_INDEPENDENT_REVIEW','projection':summary,'negative_controls_rejected':controls,
  'all_original_edges_and_qualifications_preserved':True,'current_public_locator_routes_checked':True,'new_mathematical_edges':0,
  'svg_edge_count_default':len(paths),'DOM_is_not_browser_layout':True,'primary_text_exported':False}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
