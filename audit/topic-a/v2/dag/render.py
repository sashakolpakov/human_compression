#!/usr/bin/env python3
"""Derived offline explorer; frozen logical and ownership records stay separate."""
from pathlib import Path
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 if a.out.exists() or a.out.is_symlink():raise ValueError('Fresh visual directory required')
 I=HERE/'inputs';load=lambda p:json.loads((I/p).read_text())
 protocol=json.loads((HERE/'protocol.json').read_text());routes=protocol['current_evidence_routes']
 g=load('logical/logical_graph.json');w=load('weighted/weights.json');p=load('weighted/partition.json');m=load('measurement.json');spec=load('public_input_spec.json');citations=json.loads((HERE/'citations.json').read_text())
 nodes=[];known={n['id'] for n in g['nodes']};parents={n['id']:n['parent'] for n in g['nodes'] if n.get('parent')}
 for n in g['nodes']:
  row=dict(n);row['external']=n['category']=='external';row['side']='historical' if n['side'].startswith('historical') else 'new'
  row['owners']=w['logical_node_cost_interfaces'][n['id']]['owners'];row['weight']=w['logical_node_cost_interfaces'][n['id']]['weight']
  row['weight_scope']=w['logical_node_cost_interfaces'][n['id']]['scope'];row['closure']=w['logical_closures'].get(n['id'])
  row['shared_code_alias']=n['id'].startswith('code.')
  row['cost_only']=False
  row['current_public_locators']=[dict(l,original_private_path=l['path'],path=routes[l['path']]['path']) for l in n.get('locators',[]) if isinstance(l,dict) and l.get('path') in routes]
  nodes.append(row)
 for id,owner in p['owners'].items():
  if id in known:continue
  spans=[s for s in p['documents'][owner['document']]['spans'] if s['node']==id]
  nodes.append({'id':'owned:'+id,'label':owner['label'],'document':owner['document'],
   'side':'historical' if owner['document'] in spec['sources'] else 'new','category':owner['category'],
   'owners':[id],'weight':w['owner_weights'][id],'weight_scope':'Exclusive owned text. No additional mathematical implication is asserted.',
   'external':False,'shared_code_alias':False,'cost_only':True,'locators':spans,'closure':None})
 documents={k:dict(title=d['title'],pages=d['pages'],side='historical' if k in spec['sources'] else 'new',
  path=spec['sources'].get(k,spec['ours'].get(k))['path'],weight=w['document_totals'][k]) for k,d in p['documents'].items()}
 targets={'A1':['L032.T1.2','L032.P2.2'],'A2':['L034.T3.2','L034.L3.1'],'A3':['F016.L4.1','F016.T5.1','F016.T5.3','F016.T6.1','F016.T7.1','F016.T7.2','F016.T7.3'],
          'A4':['F013.main','F013.4.2_statement','F013.4.2c','F013.4.2d','F013.4.2e'],'A5':['L035.T1.2','L035.T1.3'],'A6':[n['id'] for n in g['nodes'] if n['document']=='N009']}
 coverage=load('logical/coverage.json');pairs=[]
 for app,source in zip(spec['application_sequence'],spec['source_sequence']):
  current=sorted({node for row in coverage['rows'] if row['source_id']==source for node in row['new_nodes']})
  pairs.append(dict(id=app,source=source,title=documents[app]['title'],historical_targets=targets[app],new_targets=current))
 for k,row in citations['sources'].items():documents[k]['citation']=row
 logical=['proof_use','retained_input_use','retained_algorithm_use','computational_use','branch_membership','output_assembly','historical_documented_use','historical_asserted_use','definition_use','declared_retained_translation']
 payload={'title':'Two-group constructions and classifications','nodes':nodes,'edges':g['edges'],'parents':parents,
   'logical_edge_kinds':logical,'documents':documents,'pairs':pairs,'owner_weights':w['owner_weights'],'owners':p['owners'],
   'factors':m['factors'],'source_qualifications':g['scope_gaps'],'counts':w['granularity_counts'],
   'logical_node_count':len(g['nodes']),'edge_count':len(g['edges']),'owner_count':len(p['owners']),
   'bindings':{x:sha((I/x).read_bytes()) for x in ('logical/logical_graph.json','weighted/partition.json','weighted/weights.json','measurement_admission.json')},
   'review_status':'The graph, exclusive text ownership, document measurements and publication adapter have independent reviews. The current publication decision is recorded in ../dag_admission.json. Browser layout has not been certified.',
   'public_target':protocol['public_target'],'not_primary_text':True}
 a.out.mkdir(parents=True);(a.out/'view_data.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n')
 css=(HERE/'explorer.css').read_text();js=(HERE/'explorer.js').read_text();template=(HERE/'explorer_template.html').read_text()
 text=json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
 (a.out/'explorer.html').write_text(template.replace('__CSS__',css).replace('__DATA__',text).replace('__JS__',js))
 # Full named overview; every fine edge remains in the frozen logical JSON.
 by={n['id']:n for n in nodes};visible={n['id'] for n in nodes if not n['cost_only'] and n['id'] not in parents}
 dot=['digraph TopicA {','rankdir=LR;','graph [label="Topic A: named argument routes; box costs can overlap; totals count each passage once",labelloc=t];','node [shape=box,style="rounded,filled",fontname="Helvetica",fontsize=10];']
 for id in sorted(visible):
  n=by[id];cost=n['weight'];label=id+'\\n'+n['label']+'\\n'+('external cost unknown' if n['external'] else 'shared complete appendix' if n['shared_code_alias'] else str(cost['NFC']['characters_without_whitespace'])+' NFC nonspace characters' if cost else 'output interface')
  dot.append(json.dumps(id)+' [label='+json.dumps(label,ensure_ascii=False)+',fillcolor="'+('#eeeeee' if n['external'] else '#fff3d8' if n['side']=='historical' else '#e6f2fa')+'"];')
 seen=set()
 for e in g['edges']:
  x,y=parents.get(e['source'],e['source']),parents.get(e['target'],e['target'])
  if x==y or x not in visible or y not in visible or (x,y) in seen:continue
  seen.add((x,y));dot.append(json.dumps(x)+' -> '+json.dumps(y)+(';' if e['kind'] in logical else ' [style=dashed];'))
 dot.append('}');(a.out/'overview.dot').write_text('\n'.join(dot)+'\n')
 print(json.dumps({'derived_nodes':len(nodes),'logical_nodes':len(g['nodes']),'fine_edges':len(g['edges']),'primary_text_exported':False,'out':str(a.out)}))
if __name__=='__main__':main()
