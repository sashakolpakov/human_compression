#!/usr/bin/env python3
"""Replay the paired Topic E accounting; primary PDFs must be supplied explicitly.
No primary text is emitted. Dependencies require pypdf 6.13.0 only.
"""
import argparse,bisect,copy,hashlib,importlib.util,json,re,unicodedata
from pathlib import Path
HIST={'L083','L079','L021'}
NEW={'New_U','New_A1','New_A2','New_A3','New_Code','New_Validation'}
ALL=HIST|NEW
METRICS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
def need(x,msg):
 if not x:raise ValueError('PAIRED_DAG_REJECT '+msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def bound(root,row):
 p=root/row['path'];data=p.read_bytes();need(sha(data)==row['sha256'],'bound file '+row['path'])
 if 'bytes' in row:need(len(data)==row['bytes'],'file bytes '+row['path'])
 return p

def validate(part,dag,texts,inputs):
 need(set(part['documents'])==ALL,'nine documents exactly')
 owned={}
 for key,rows in part['documents'].items():
  at=0
  for s in rows:
   a,b=s['start'],s['end'];need(a==at and a<b<=len(texts[key]),'partition gap/overlap '+key);at=b
   need(sha(texts[key][a:b].encode())==s['sha256'],'span text '+key)
   meta=(key,s['category'],s['label']);need(s['node'] not in owned or owned[s['node']]==meta,'unique cost owner');owned[s['node']]=meta
  need(at==len(texts[key]),'complete manuscript '+key)
 nodes=dag['nodes'];by={n['id']:n for n in nodes};need(len(by)==len(nodes),'unique nodes/shared aliases not repeated')
 need(set(owned)=={n['id'] for n in nodes if n['cost_status']=='measured'},'all and only owned leaves')
 old,ld,new=inputs['historical_two_dag.json'],inputs['historical_L021_dag.json'],inputs['new_dag.json']
 expectednodes={n['id']:n for n in old['nodes'] if n['side']=='historical'}
 for d in [ld,new]:
  for n in d['nodes']:
   if n['cost_status']!='owned_by_existing_historical_partition_not_recounted':expectednodes.setdefault(n['id'],n)
 for n in old['nodes']:
  if n['id'] in by:expectednodes.setdefault(n['id'],n)
 need(set(expectednodes)==set(by),'exact input node union')
 for n in nodes:
  orig=expectednodes[n['id']]
  for key,val in orig.items():
   if key not in ['cost_status','cost','charge']:
    need(n.get(key)==val,'preserved original node field '+n['id']+' '+key)
  if n['cost_status']=='measured':need(n['charge'] and owned[n['id']]==(n['document'],n['category'],n['label']),'measured metadata')
  elif n['cost_status']=='rollup_only':need(n['charge'] is False,'aggregate not double charged')
  else:need(n['cost_status']=='conditioned_unknown' and n.get('cost','missing') is None and not n['charge'],'unknown proof cost null')
 # Shared references preserve all existing ownership spans, but are not second graph nodes.
 aliases=[n for n in ld['nodes'] if n['cost_status']=='owned_by_existing_historical_partition_not_recounted']
 need(dag['shared_historical_alias_references']==aliases,'all ten literal historical aliases')
 for n in aliases:
  need([s['sha256'] for rows in part['documents'].values() for s in rows if s['node']==n['id']]==n['cost_owner']['span_sha256'],'shared proof cost owner')
 childowner={}
 for n in nodes:
  if n['cost_status']=='rollup_only':
   need(n['children'] and len(n['children'])==len(set(n['children'])),'distinct aggregate leaves')
   for c in n['children']:
    need(c in owned and c not in childowner,'aggregate leaf once');childowner[c]=n['id']
 need(set(childowner)=={n['id'] for n in nodes if n['category'] in ['theorem_statement','substantive_proof_branch']},'all bundled branches paid once')
 oldby={n['id']:n for n in old['nodes']}
 expectededges=[dict(e,origin_graph='historical_two') for e in old['edges'] if oldby[e['consumer']]['side']=='historical']+[dict(e,origin_graph='historical_L021') for e in ld['edges']]+[dict(e,origin_graph='new') for e in new['edges']]
 need(dag['edges']==expectededges,'exact full inherited edges and documentary qualifications')
 logical=set(dag['logical_edge_kinds']);allow=logical|set(dag['nonlogical_edge_kinds']);graph={n:[] for n in by};seen=set()
 for e in dag['edges']:
  a,b,k=e['prerequisite'],e['consumer'],e['kind'];need(a in by and b in by and a!=b and k in allow,'typed edge endpoints');need((a,b,k) not in seen,'duplicate edge');seen.add((a,b,k))
  ids=by[b].get('children',[b]);ss=[s for rows in part['documents'].values() for s in rows if s['node'] in ids]
  need(e['witness']['consumer_span_hashes']==[s['sha256'] for s in ss],'exact consumer span witness')
  if 'evidence_span' in e['witness']:
   w=e['witness']['evidence_span'];lo,hi=w['start'],w['end'];need(any(s['start']<=lo<hi<=s['end'] for s in ss),'evidence inside owned argument');need(sha(texts[by[b]['document']][lo:hi].encode())==w['sha256'],'evidence subspan')
  if k in logical:graph[a].append(b)
 active=set();done=set()
 def visit(n):
  need(n not in active,'cycle')
  if n in done:return
  active.add(n)
  for c in graph[n]:visit(c)
  active.remove(n);done.add(n)
 for n in by:visit(n)
 need(dag['historical_L021_numbered_item_ownership']==ld['numbered_result_ownership'],'all numbered source items')
 found={a+b for a,b in re.findall(r'(?m)^(Lemma|Theorem|Proposition|Corollary|Remark|Definition) ([0-9]+\.[0-9]+)\.',texts['L021'])}
 need(found==set(ld['numbered_result_ownership']),'numbered items match full primary text')
 need(dag['historical_L021_unresolved_interfaces']==ld['unresolved_interfaces'],'all unresolved source interfaces retained')
 need('both printed proof alternatives' in by['021.L3.9']['closure_caveat'],'alternative-proof union caveat')
 need(dag['no_node_count_ratio'] is True and dag['measurement_pays_all_text'] is True,'declared granularity/full payment')
 return by

def raw_map(binding):
 pieces=[]
 for span in binding['included_spans']:
  at=span['start']
  for f in binding['excluded_furniture']:
   if span['start']<=f['start']<f['end']<=span['end']:
    pieces.append(list(range(at,f['start'])));at=f['end']
  pieces.append(list(range(at,span['end'])))
 out=[]
 for i,c in enumerate(pieces):
  if i:out.append(None)
  out.extend(c)
 return out

def atom_costs(text,spans,form):
 chunks=[unicodedata.normalize(form,text[s['start']:s['end']]) for s in spans];norm=unicodedata.normalize(form,text);need(''.join(chunks)==norm,'normalization boundary')
 ends=[];at=0
 for c in chunks:at+=len(c);ends.append(at)
 out=[dict.fromkeys(METRICS,0) for _ in spans]
 def add(pos,k,v=1):out[bisect.bisect_right(ends,pos)][k]+=v
 for x in re.finditer(r'\S+',norm):add(x.start(),'whitespace_tokens')
 for x in re.finditer(r'[^\W_]+',norm):add(x.start(),'alphanumeric_units')
 for i,c in enumerate(norm):
  if not c.isspace():
   add(i,'characters_without_whitespace');add(i,'characters_with_collapsed_whitespace');add(i,'utf8_bytes_with_collapsed_whitespace',len(c.encode()))
 for x in re.finditer(r'\s+',norm):
  if x.start()>0 and x.end()<len(norm):add(x.start(),'characters_with_collapsed_whitespace');add(x.start(),'utf8_bytes_with_collapsed_whitespace')
 return out

def closure(dag,targets):
 back={n['id']:[] for n in dag['nodes']}
 for e in dag['edges']:
  if e['kind'] in dag['logical_edge_kinds']:back[e['consumer']].append(e['prerequisite'])
 ans=set();todo=list(targets)
 while todo:
  n=todo.pop()
  if n not in ans:ans.add(n);todo.extend(back[n])
 return sorted(ans)

def controls(part,dag,texts,inputs):
 cases=[]
 def reject(name,p=part,d=dag,t=texts):
  try:validate(p,d,t,inputs)
  except ValueError:cases.append(dict(name=name,rejected=True))
  else:raise ValueError('accepted negative control '+name)
 p=copy.deepcopy(part);p['documents']['L083'][1]['start']+=1;reject('historical_partition_gap',p=p)
 p=copy.deepcopy(part);p['documents']['L021'][1]['start']-=1;reject('historical_partition_overlap',p=p)
 t=dict(texts);t['L079']=t['L079'][:-1]+'X';reject('altered_primary_text',t=t)
 p=copy.deepcopy(part);del p['documents']['New_Code'];reject('omitted_required_code',p=p)
 d=copy.deepcopy(dag);d['nodes'].append(copy.deepcopy(next(n for n in d['nodes'] if n['id']=='083.table')));reject('double_charged_shared_historical_table',d=d)
 d=copy.deepcopy(dag);next(n for n in d['nodes'] if n['cost_status']=='rollup_only')['charge']=True;reject('double_charged_parent',d=d)
 d=copy.deepcopy(dag);next(n for n in d['nodes'] if n['cost_status']=='conditioned_unknown')['cost']=0;reject('unknown_library_zero',d=d)
 d=copy.deepcopy(dag);next(n for n in d['nodes'] if n['id']=='021.L3.3')['documentary_status']='proved';reject('false_source_clause_relabelled_proved',d=d)
 d=copy.deepcopy(dag);d['historical_L021_unresolved_interfaces']=[];reject('erased_source_gap',d=d)
 d=copy.deepcopy(dag);d['shared_historical_alias_references'][0]['cost_owner']['span_sha256']=[];reject('altered_reuse_binding',d=d)
 d=copy.deepcopy(dag);d['edges'][0]['witness']['consumer_span_hashes']=['0'*64];reject('unbound_edge',d=d)
 d=copy.deepcopy(dag);next(n for n in d['nodes'] if n['id']=='021.L3.9')['closure_caveat']='minimum proof';reject('alternative_union_called_minimum',d=d)
 d=copy.deepcopy(dag);d['no_node_count_ratio']=False;reject('node_count_ratio',d=d)
 return cases

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--packet-root',type=Path,default=Path(__file__).resolve().parent);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--artifacts-root',type=Path,required=True);ap.add_argument('--layout',choices=['private','public'],default='public');ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh output file');r=a.packet_root;p=read(r/'protocol.json')
 mpath=bound(r,p['measurement']);mp=read(mpath);helper=bound(r,p['helper']);accepted=read(bound(r,p['accepted_measurement']));dag=read(bound(r,p['dag']));part=read(bound(r,p['partition']));inputs={Path(x['path']).name:read(bound(r,x)) for x in p['inputs']}
 spec=importlib.util.spec_from_file_location('measurement_helper',helper);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);need(m.pypdf.__version__==mp['pypdf_version'],'pinned pypdf')
 texts={};checked=[]
 for key,b in (mp['sources']|mp['new']).items():
  bb=copy.deepcopy(b)
  if key in HIST:base=a.sources_root;bb['path']=Path(b['path']).name
  else:base=a.artifacts_root;bb['path']=mp['public_locations'][b['path']] if a.layout=='public' else b['path']
  raw,uncal,cal=m.document(base,key,bb);texts[key]=cal;checked.append(dict(document=key,path=bb['path'],sha256=b['pdf_sha256'],selected_sha256=sha(cal.encode()),pages=b['pages']))
  need(all(m.metrics(uncal,f)[q]==m.metrics(cal,f)[q] for f in p['normalizations'] for q in METRICS),'glyph metric invariance')
 by=validate(part,dag,texts,inputs);forms=p['normalizations'];leaves={n:dict(by[n],costs={f:dict.fromkeys(METRICS,0) for f in forms},spans=[]) for n in {s['node'] for rows in part['documents'].values() for s in rows}};totals={}
 for k,ss in part['documents'].items():
  atoms={f:atom_costs(texts[k],ss,f) for f in forms};totals[k]={}
  for f in forms:
   totals[k][f]={q:sum(x[q] for x in atoms[f]) for q in METRICS};expected={q:m.metrics(texts[k],f)[q] for q in METRICS};need(totals[k][f]==expected,'additive metrics '+k);need(expected=={q:(accepted['costs']['sources']|accepted['costs']['new'])[k][f][q] for q in METRICS},'accepted whole document metric '+k)
  mapping=raw_map((mp['sources']|mp['new'])[k]);need(len(mapping)==len(texts[k]),'raw page map')
  for i,s in enumerate(ss):
   positions=[v for v in mapping[s['start']:s['end']] if v is not None]
   pages=[b['page'] for b in (mp['sources']|mp['new'])[k]['page_bindings'] if b['start']<=max(positions) and b['end']>min(positions)]
   leaves[s['node']]['spans'].append(dict(s,computed_physical_page_range=[min(pages),max(pages)],costs={f:atoms[f][i] for f in forms}))
   for f in forms:
    for q in METRICS:leaves[s['node']]['costs'][f][q]+=atoms[f][i][q]
 rollups=[dict(n,costs={f:{q:sum(leaves[c]['costs'][f][q] for c in n['children']) for q in METRICS} for f in forms}) for n in dag['nodes'] if n['cost_status']=='rollup_only']
 program=[]
 for row in mp['new_programs']:
  path=mp['public_locations'][row['path']] if a.layout=='public' else row['path'];data=(a.artifacts_root/path).read_bytes();need(sha(data)==row['sha256'],'program bytes');need(re.sub(r'\s+','',data.decode()) in re.sub(r'\s+','',texts[row['appendix']]),'complete program in charged PDF');program.append(dict(path=path,sha256=row['sha256'],complete=True))
 def cs(targets):
  ids=closure(dag,targets);charged=[n for n in ids if n in leaves]
  return dict(targets=targets,nodes=ids,charged_leaf_ids=charged,costs={f:{q:sum(leaves[n]['costs'][f][q] for n in charged) for q in METRICS} for f in forms},external_unknown=[n for n in ids if by[n]['cost_status']=='conditioned_unknown'],documentary_flags={n:by[n]['documentary_status'] for n in ids if by[n]['documentary_status'] not in ['printed_argument_or_statement','documentary_source_argument_not_retroactive_endorsement','accepted_new_proof_or_context']},alternative_proof_union_caveats={n:by[n]['closure_caveat'] for n in ids if 'closure_caveat' in by[n]},interpretation=dag['closure_semantics'])
 peroutput={t:cs([t]) for ts in dag['main_outputs_by_document'].values() for t in ts};perpaper={k:cs(ts) for k,ts in dag['main_outputs_by_document'].items()}
 counts={}
 for key in list(part['documents'])+['external']:
  ns=[n for n in dag['nodes'] if n['document']==key] if key!='external' else [n for n in dag['nodes'] if n['cost_status']=='conditioned_unknown'];cats={}
  for n in ns:cats[n['category']]=cats.get(n['category'],0)+1
  counts[key]=dict(total_graph_nodes=len(ns),categories=cats,charged_cost_owners=sum(n['cost_status']=='measured' for n in ns),rollup_only=sum(n['cost_status']=='rollup_only' for n in ns))
 sidecounts={}
 for side in ['historical','replacement']:
  ns=[n for n in dag['nodes'] if n['side']==side];cats={}
  for n in ns:cats[n['category']]=cats.get(n['category'],0)+1
  sidecounts[side]=dict(total_graph_nodes=len(ns),categories=cats,charged_cost_owners=sum(n['cost_status']=='measured' for n in ns),rollup_only=sum(n['cost_status']=='rollup_only' for n in ns))
 full=accepted['comparisons']['NFC']['characters_without_whitespace'];chars=lambda k:totals[k]['NFC']['characters_without_whitespace']
 headlines=dict(primary='NFC characters without whitespace',overall_written=full['source_over_new_written'],known_written_and_required=full['source_over_new_written_and_required'],including_optional_validation=full['source_over_new_written_required_and_validation'],conditional_applications={k:chars(s)/chars(k) for s,k in [('L083','New_A1'),('L079','New_A2'),('L021','New_A3')]},conditional_explanation='Full common theory is acquired once within this topic; each conditional factor divides its complete source manuscript by its complete local application. Required computation is separately charged in the common package. These recover declared main-result contracts, not every historical assertion.',node_count_ratio=None)
 result=dict(status='PASS_PAIRED_ACCOUNTING_AND_BOUND_DOCUMENTARY_DAGS',scope=dag['scope'],checker_sha256=sha(Path(__file__).read_bytes()),protocol_sha256=sha((r/'protocol.json').read_bytes()),dag_sha256=p['dag']['sha256'],partition_sha256=p['partition']['sha256'],all_ninety_metric_cells_match_accepted=True,documents=checked,complete_programs=program,costs=totals,headline_from_accepted_measurement=headlines,node_counts_at_declared_granularity=counts,side_node_counts_without_ratio=sidecounts,granularity_warning=p['granularity_warning'],additive_leaf_nodes=[leaves[n['id']] for n in dag['nodes'] if n['id'] in leaves],named_rollups_not_additional_charges=rollups,external_nodes=[n for n in dag['nodes'] if n['cost_status']=='conditioned_unknown'],per_output_closures=peroutput,per_document_output_closures=perpaper,all_output_union_closure=cs([t for ts in dag['main_outputs_by_document'].values() for t in ts]),shared_historical_ids_charged_once=[n['id'] for n in dag['shared_historical_alias_references']],negative_controls=controls(part,dag,texts,inputs),primary_text_exported=False,limits=dag['conditions'])
 a.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(dict(status=result['status'],nodes=len(by),edges=len(dag['edges']),spans=sum(map(len,part['documents'].values())),metric_cells=90,closures=len(peroutput),shared_historical_aliases=len(dag['shared_historical_alias_references']),controls=len(result['negative_controls']),totals={k:chars(k) for k in totals}),indent=2))
if __name__=='__main__':main()
