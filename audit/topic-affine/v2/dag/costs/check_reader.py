#!/usr/bin/env python3
"""Validate both static graphs and complete-library acquisition without a browser claim."""
import argparse,copy,json,sys,xml.etree.ElementTree as ET
from pathlib import Path
sys.dont_write_bytecode=True
from accounting import need,add,sha
from build_reader import build,primary
HERE=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_text())
NS={'s':'http://www.w3.org/2000/svg'}

def verify(g,w,p,graphs,ac,svgs):
 by={n['id']:n for n in g['nodes']};counts={}
 for side,rec in graphs.items():
  keep={n for n,r in by.items() if r['side']==side}
  while True:
   old=set(keep);keep|={e['source'] for e in g['edges'] if e['target'] in keep and e['kind'] in g['logical_edge_kinds']}
   if old==keep:break
  expected=[{'source':e['source'],'target':e['target'],'kind':e['kind']} for e in g['edges'] if e['source'] in keep and e['target'] in keep and e['kind'] in g['logical_edge_kinds']]
  need(rec['nodes']==sorted(keep) and rec['edges']==expected,'complete '+side+' logical graph')
  svg=ET.fromstring(svgs[side]);nn={e.attrib['data-node']:e for e in svg.findall('s:g',NS)};ee=svg.findall('s:path',NS)
  need(set(nn)==keep and len(nn)==len(keep),'all SVG nodes')
  need([(e.attrib['data-source'],e.attrib['data-target']) for e in ee]==[(e['source'],e['target']) for e in expected],'all SVG arrows in prerequisite direction')
  for n,el in nn.items():
   texts=el.findall('s:text',NS);strings=[''.join(e.itertext()) for e in texts];link=w['node_interfaces'][n]
   need(strings[0]==n,'exact displayed ID')
   need(strings[-1]==('External proof: unknown' if link['known_weight'] is None else f'Interface text: {primary(link["known_weight"]):,}'),'exact visible node costs')
   need(' '.join(strings[1:-1])==by[n]['label'],'complete wrapped mathematical label')
   rect=el.find('s:rect',NS);x,y=float(rect.attrib['x']),float(rect.attrib['y']);width,height=float(rect.attrib['width']),float(rect.attrib['height'])
   need(all(x<float(t.attrib['x'])<x+width and y<float(t.attrib['y'])<y+height for t in texts),'text origins within box')
   if by[n]['documentary_flags']:need(rect.attrib['fill']=='#fff1e9','source qualification visible')
  need(rec['expanded_external_proof_cost'] is None and rec['node_count_factor'] is None,'unknown graph cost')
  counts[side]={'nodes':len(keep),'logical_edges':len(expected)}
 need([s['stage'] for s in ac['stages']]==['U_Affine','CODE','AF1'],'whole-topic acquisition order')
 paid=set()
 for stage in ac['stages']:
  full={n for n,o in p['owners'].items() if o['document']==stage['stage']};need(not full&paid,'disjoint acquisition');paid|=full
  need(stage['complete_owner_ids']==sorted(full) and stage['cumulative_owner_ids']==sorted(paid),'all paper owners including unused statements')
  need(stage['new_cost']==add(w['owner_costs'][n] for n in full) and stage['cumulative_cost']==add(w['owner_costs'][n] for n in paid),'whole acquisition arithmetic')
 need(ac['historical_full_document_cost']==w['document_costs']['L012'],'whole source acquisition reference')
 need(ac['expanded_external_proof_cost'] is None and ac['graphics_cost'] is None and ac['cross_topic_discount'] is False,'no hidden discounts')
 return counts

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 g=load(a.study_root/'topic_Affine_logical_dag_v2/logical_graph.json');w=load(HERE/'weights.json');p=load(HERE/'partition.json');graphs=load(HERE/'graphs.json');ac=load(HERE/'acquisition.json');svgs={s:(HERE/f'{s}_graph.svg').read_text() for s in graphs}
 counts=verify(g,w,p,graphs,ac,svgs)
 regen=a.out/'regenerated';regen.mkdir();build(a.study_root,regen)
 for f in ['graphs.json','acquisition.json','historical_graph.svg','new_graph.svg','reader.tex','reader_input_bindings.json']:need((regen/f).read_bytes()==(HERE/f).read_bytes(),'exact derived view regeneration '+f)
 controls=[]
 tests=[('reverse_arrow',lambda gg,aa,ss:gg['new']['edges'][0].update(source=gg['new']['edges'][0]['target'])),
 ('drop_historical_node',lambda gg,aa,ss:gg['historical']['nodes'].pop()),
 ('external_proof_free',lambda gg,aa,ss:ss.update(historical=ss['historical'].replace('External proof: unknown','External proof: 0',1))),
 ('wrong_node_cost',lambda gg,aa,ss:ss.update(new=ss['new'].replace('Interface text: 516','Interface text: 0',1))),
 ('remove_source_warning',lambda gg,aa,ss:ss.update(historical=ss['historical'].replace('#fff1e9','#faf1db',1))),
 ('drop_unused_common_owner',lambda gg,aa,ss:aa['stages'][0]['complete_owner_ids'].remove('AL.SmallerPeriods')),
 ('repeat_program_acquisition',lambda gg,aa,ss:aa['stages'][1]['cumulative_owner_ids'].append('program.kernel64.printed')),
 ('waive_other_topic_theory',lambda gg,aa,ss:aa.update(cross_topic_discount=True))]
 for name,mut in tests:
  gg,aa,ss=copy.deepcopy(graphs),copy.deepcopy(ac),copy.deepcopy(svgs);mut(gg,aa,ss)
  try:verify(g,w,p,gg,aa,ss)
  except ValueError as e:controls.append({'name':name,'rejected':True,'reason':str(e)})
  else:raise ValueError('visual control accepted '+name)
 report={'status':'PASS_STATIC_READER_DATA_AND_SVG','graphs':counts,'controls':controls,'actual_browser_test':False,'owner_union_scope':'node labels overlap; full acquisition sums disjoint document owners','reader_pdf_semantic_review':'separately documented visual reading'}
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(counts))
if __name__=='__main__':main()
