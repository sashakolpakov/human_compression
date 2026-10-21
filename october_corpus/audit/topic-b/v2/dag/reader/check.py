#!/usr/bin/env python3
"""Bounded derived-reader check; no primary text extraction or proof replay."""
import argparse,copy,hashlib,json
from pathlib import Path
from prepare import derive,need,sha,total,load,FILES,PINS

def validate(packet,data):
 inputs=packet/'inputs'
 for row in load(packet/'input_bindings.json'):
  p=packet/row['reader_path'];need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'copied input hash')
 for path,h in PINS.items():need(sha(inputs/path)==h,'pinned immutable manifest')
 for folder in ['logical','weighted','measurement','ownership_review']:
  for row in load(inputs/folder/'manifest.json')['exports']:
   p=inputs/folder/row['path']
   if p.exists():need(sha(p)==row['sha256'],'exact frozen export')
 expected=derive(inputs);need(data==expected,'complete derived payload')
 p=load(inputs/'weighted/partition.json');w=load(inputs/'weighted/weights.json');g=load(inputs/'logical/logical_graph.json')
 paid=set();cells=0
 for row in data['acquisition']['stages']:
  local={x for x,o in p['owners'].items() if o['document']==row['stage']}
  need(row['previous_owner_ids']==sorted(paid),'exact prior owner set')
  need(row['new_owner_ids']==sorted(local-paid),'complete local paper including all context')
  need(row['new_cost']==w['document_costs'][row['stage']],'new stage equals complete document')
  paid|=local
  need(row['cumulative_owner_ids']==sorted(paid),'exact cumulative owner union')
  need(row['cumulative_cost']==total(paid,w['owner_costs']),'cumulative once-only charge');cells+=20
  need(row['full_dependency_cost'] is None,'external full proof cost stays unknown')
  if row['stage']!='U_B':need(row['historical_cumulative']['unknown_source']=='N001' and row['historical_cumulative']['complete_cost'] is None,'historical series retains missing source')
 need(set(x for x,o in p['owners'].items() if o['document'] in ['U_B','B1','B2','B3','B4'])==paid,'all new text paid')
 need(data['measurement']['primary']['overall_factor'] is None,'no invented overall ratio')
 need(len(data['pairs'])==34 and len([r for r in data['pairs'] if r['id'].startswith('clause:')])==30,'four contracts and thirty clauses')
 need(data['logical_node_count']==184 and data['edge_count']==348,'accepted graph unchanged')
 need(data['acquisition']['source_cumulative_numeric_curve'] is None and data['acquisition']['raw_node_ratio'] is None,'no false historical series or node ratio')
 return dict(acquisition_metric_cells=cells,whole_document_metric_cells=80,logical_nodes=184,fine_edges=348,clause_routes=30,application_routes=4,complete_documents=8,missing_N001_unknown=True)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh report');data=load(a.packet/'view_data.json');result=validate(a.packet,data);controls=[]
 for case in ['drop_context','repeat_umbrella','missing_source_zero','fake_historical_curve','node_ratio','reverse_edge','drop_clause','external_zero']:
  d=copy.deepcopy(data)
  if case=='drop_context':d['acquisition']['stages'][1]['new_owner_ids'].pop()
  elif case=='repeat_umbrella':d['acquisition']['stages'][2]['new_owner_ids']+=d['acquisition']['stages'][0]['new_owner_ids']
  elif case=='missing_source_zero':d['documents']['N001']['weight']=0
  elif case=='fake_historical_curve':d['acquisition']['source_cumulative_numeric_curve']=[0,17765,35302,57539]
  elif case=='node_ratio':d['acquisition']['raw_node_ratio']=73/85
  elif case=='reverse_edge':d['edges'][0]['source'],d['edges'][0]['target']=d['edges'][0]['target'],d['edges'][0]['source']
  elif case=='drop_clause':d['pairs'].pop()
  elif case=='external_zero':d['acquisition']['expanded_external_proof_cost']=0
  try:validate(a.packet,d)
  except ValueError as e:controls.append(dict(name=case,rejected=True,reason=str(e)))
  else:raise ValueError('control accepted: '+case)
 html=(a.packet/'explorer.html').read_text();payload=html.split('<script id="data" type="application/json">')[1].split('</script>')[0]
 need(json.loads(payload)==data,'embedded HTML data matches JSON')
 need(load(a.packet/'acquisition.json')==data['acquisition'],'separate acquisition JSON matches')
 report=dict(status='PASS_DERIVED_READER_CHECK',counts=result,controls=controls,primary_extraction_repeated=False,mathematical_proof_repeated=False,scope='Author adapter consistency only; independent ownership and reader admission remain separate.',bindings={'view_data.json':sha(a.packet/'view_data.json'),'explorer.html':sha(a.packet/'explorer.html')})
 a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
