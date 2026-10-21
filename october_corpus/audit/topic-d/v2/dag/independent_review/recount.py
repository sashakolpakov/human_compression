#!/usr/bin/env python3
"""Independent character-state allocation and reverse-adjacency union audit.
Only the accepted D extraction/calibration interface is reused. No author cost,
partition-construction, token/regex allocator, route or reader code is imported.
"""
import argparse, collections, copy, csv, hashlib, importlib.util, json, sys, unicodedata
from pathlib import Path
sys.dont_write_bytecode=True
V=('raw_untrimmed','raw_selected','calibrated_selected'); F=('NFC','NFKC')
M=('whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace')
PIN='1a91cbbfa35b12f811dc311e3440c4a60c5b7d074c1f8c4efa68cc8eb40423f3'
def need(c,m):
 if not c:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def zero():return {v:{f:{m:0 for m in M} for f in F} for v in V}
def union_cost(ids,costs):
 ids=set(ids)
 return {v:{f:{m:sum(costs[o][v][f][m] for o in ids) for m in M} for f in F} for v in V}
def allocate(parts, form):
 """State machine, with a pending internal whitespace run; no regex/bisect."""
 result={o:dict.fromkeys(M,0) for o,_ in parts};stream=[]
 for o,t in parts:stream.extend((c,o) for c in unicodedata.normalize(form,t))
 seen=False; prev_space=True;prev_alnum=False;pending=None
 for c,o in stream:
  r=result[o];space=c.isspace();alnum=c.isalnum()
  if alnum and not prev_alnum:r['alphanumeric_units']+=1
  prev_alnum=alnum
  if space:
   if seen and pending is None:pending=o
   prev_space=True;continue
  if prev_space:r['whitespace_tokens']+=1
  if pending is not None:
   result[pending]['characters_with_collapsed_whitespace']+=1
   result[pending]['utf8_bytes_with_collapsed_whitespace']+=1
   pending=None
  r['characters_without_whitespace']+=1;r['characters_with_collapsed_whitespace']+=1
  r['utf8_bytes_with_collapsed_whitespace']+=len(c.encode());seen=True;prev_space=False
 return result, ''.join(c for c,o in stream)
def reverse(g):
 p={n['id']:set() for n in g['nodes']}
 for e in g['edges']:
  if e['kind'] in g['logical_edge_kinds']:p[e['target']].add(e['source'])
 return p
def close(targets,prev):
 seen=set();todo=list(targets)
 while todo:
  n=todo.pop()
  if n not in seen:seen.add(n);todo.extend(prev[n]-seen)
 return seen

def verify(root, packet, out, logical, pin):
 manifest=load(packet/'manifest.json');need(sha((packet/'manifest.json').read_bytes())==pin,'author manifest pin')
 for r in manifest['exports']:
  b=(packet/r['path']).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'export '+r['path'])
 p=load(packet/'partition.json');w=load(packet/'weights.json');g=load(logical/'logical_graph.json');cov=load(logical/'coverage.json')
 d=load(packet/'view_data.json');acq=load(packet/'acquisition.json');prev=reverse(g);nodes={n['id']:n for n in g['nodes']};interfaces=w['node_interfaces'];owners=p['owners']
 need(d['edges']==g['edges'] and d['logical_edge_kinds']==g['logical_edge_kinds'],'unchanged accepted logical edges')
 sys.path.insert(0,str(root/'topic_D_measurement_v2'))
 s=importlib.util.spec_from_file_location('accepted_D_extract',root/'topic_D_measurement_v2/extract_inputs.py');ex=importlib.util.module_from_spec(s);s.loader.exec_module(ex)
 spec=load(root/'topic_D_measurement_v2/source_input_spec.json')['sources']|load(root/'topic_D_measurement_v2/replacement_input_spec.json')['ours']
 adopted=load(root/'topic_D_measurement_independent_review/recount_corrected.json')['documents']
 costs={o:zero() for o in owners};docs={};boundary_records=[];texts={}
 for k,row in spec.items():
  extracted=ex.document(root,k,row);texts[k]=dict(zip(V,extracted[:3]));docs[k]=zero()
  for v in V:
   text=texts[k][v];rec=p['documents'][k]['variants'][v];need(len(text)==rec['length'] and sha(text.encode())==rec['sha256'],'document '+k+'/'+v)
   at=0;parts=[]
   for span in rec['spans']:
    a,b,o=span['start'],span['end'],span['owner'];need(a==at and a<b<=len(text),'partition continuity');need(owners[o]['document']==k and owners[o]['category']==span['category'],'owner identity/category')
    t=text[a:b];need(sha(t.encode())==span['sha256'],'span binding');parts.append((o,t));at=b
    if v=='calibrated_selected':boundary_records.append({'document':k,'owner':o,'category':span['category'],'start':a,'end':b,'sha256':span['sha256'],'pages':span['physical_pages']})
   need(at==len(text),'final suffix')
   for f in F:
    aa,normalized=allocate(parts,f);need(normalized==unicodedata.normalize(f,text),'no normalization across cuts')
    direct,_=allocate([('whole',text)],f);docs[k][v][f]=direct['whole']
    need(direct['whole']=={m:adopted[k]['variants'][v][f][m] for m in M},'accepted whole coordinate')
    for o,counts in aa.items():costs[o][v][f]=counts
  need(union_cost([o for o in owners if owners[o]['document']==k],costs)==docs[k],'complete document conservation')
 need(costs==w['owner_costs'],'all independent owner counts');need(docs==w['document_costs'],'all independent document counts')
 with (packet/'owner_costs.csv').open(newline='') as f:
  rows=list(csv.DictReader(f));need(len(rows)==len(owners)*6,'CSV full rows')
  for r in rows:
   o=r['owner'];need(r['document']==owners[o]['document'] and r['category']==owners[o]['category'],'CSV semantic labels')
   need(all(int(r[m])==costs[o][r['variant']][r['normalization']][m] for m in M),'CSV costs')
 raw={};drivers={}
 for key,dest in [('raw_program_alternative',raw),('raw_operational_drivers',drivers)]:
  for n,r in w[key].items():
   b=(root/r['binding']['path']).read_bytes();need(sha(b)==r['binding']['sha256'] and len(b)==r['binding']['bytes'],'full program bytes')
   dest[n]={f:allocate([('whole',b.decode())],f)[0]['whole'] for f in F};need(dest[n]==r['metrics'],'full raw program metrics')
 for n,i in interfaces.items():
  need(len(set(i['owners']))==len(i['owners']),'duplicate interface owner')
  expected_unknown=nodes[n]['side']=='external' or (nodes[n]['side']=='verification' and not n.startswith('diagnostic.'))
  need((i['known_weight'] is None)==expected_unknown,'known/unknown distinction '+n)
  if expected_unknown:need(i['owners']==[],'unknown has no invented cost')
  else:need(i['known_weight']==union_cost(i['owners'],costs),'interface sum')
  need(i['expanded_dependency_cost'] is None and not i['charged_again'],'no expanded/duplicate cost')
 def route(names,r):
  need(set(r['logical_nodes'])==names,'route exact prerequisites')
  oo={o for n in names for o in interfaces[n]['owners']};need(set(r['owners'])==oo and len(r['owners'])==len(oo),'route owner union')
  need(r['known_extracted_subtotal']==union_cost(oo,costs),'route known subtotal')
  need(r['by_document']=={k:union_cost([o for o in oo if owners[o]['document']==k],costs) for k in {owners[o]['document'] for o in oo}},'route document decomposition')
  need(set(r['unknown_inputs'])=={n for n in names if interfaces[n]['known_weight'] is None},'route unknown inputs')
  alt=union_cost([o for o in oo if owners[o]['document']!='CODE'],costs)
  for v in V:
   for f in F:
    for m in M:alt[v][f][m]+=sum(raw[n][f][m] for n in names if n in raw)
  need(r['raw_program_alternative_subtotal']==alt,'alternate full code no double charge')
  need(r['expanded_dependency_cost'] is None and r['graphics_cost'] is None,'unknown expanded/image')
 nroute=0
 for c,r in zip(cov['rows'],w['source_contract_closures']):
  need(c['id']==r['id'],'coverage order')
  for targets,key in [(c['historical_outputs'],'historical'),(c['new_outputs'],'replacement')]:
   route(close(targets,prev),r[key]);nroute+=1
  route(close(c['retained_input_nodes'],prev)|set(c['qualification_context_nodes']),r['retained_and_qualification_context']);nroute+=1
  if not c['new_outputs']:need(not r['replacement']['owners'],'retained clause not proved output')
 for source,r in w['new_application_closures'].items():route(close(g['new_application_outputs'][source],prev),r);nroute+=1
 for n,r in w['additional_current_comparisons'].items():route(close([n],prev),r);nroute+=1
 for n in d['nodes']:
  if n['id'] not in nodes:continue
  names=close([n['id']],prev);oo={o for i in names for o in interfaces[i]['owners']};cl=n['closure']
  need(set(cl['unique_owner_ids'])==oo and cl['known_owned_text_subtotal']==union_cost(oo,costs),'viewer independently derived closure')
  need(set(cl['unknown_external_nodes'])=={x for x in names if interfaces[x]['known_weight'] is None},'viewer unknowns')
  need(n['owners']==interfaces[n['id']]['owners'] and n['weight']==interfaces[n['id']]['known_weight'],'viewer interface')
 paid=set();history=[];historical_by_app={v:k for k,v in g['applications'].items()}
 for stage in acq['stages']:
  k=stage['stage'];full={o for o in owners if owners[o]['document']==k};used={o for n in close([n['id'] for n in g['nodes'] if n['document']==k and not n['id'].startswith('program.')],prev) for o in interfaces[n]['owners']}
  need(set(stage['previous_owner_ids'])==paid and set(stage['complete_local_owner_ids'])==full,'acquisition full local ownership')
  need(set(stage['new_owner_ids'])==full-paid and set(stage['cumulative_owner_ids'])==paid|full,'acquisition exact set difference')
  need(stage['new_cost']==union_cost(full-paid,costs) and stage['cumulative_cost']==union_cost(paid|full,costs),'acquisition union costs')
  need(stage['written_cumulative_cost']==union_cost([o for o in paid|full if owners[o]['document']!='CODE'],costs),'written excludes code')
  need(set(stage['reused_owner_ids'])==used&paid and stage['reused_route_cost']==union_cost(used&paid,costs),'actual prior text reuse')
  need(set(stage['local_text_outside_route'])==full-used and set(stage['logical_route_owner_ids'])==used,'context remains paid')
  if k in historical_by_app:
   history.append(historical_by_app[k]);expected={v:{f:{m:sum(docs[h][v][f][m] for h in history) for m in M} for f in F} for v in V}
   need(stage['historical_cumulative']['complete_cost']==expected,'historical complete curve')
  paid|=full
 need(set(g['required_mathematical_programs'])==set(n for n in raw if n.startswith('program.')),'five required')
 need(set(g['diagnostic_programs'])==set(n for n in raw if n.startswith('diagnostic.')),'three diagnostics')
 need(all(costs[n+'.printed']['calibrated_selected']['NFC']['characters_without_whitespace']>0 for n in raw),'all eight programs positive')
 need('UD.Normalizer.proof' in paid and 'UD.Normalizer.statement' in paid,'unused normalizer fully acquired')
 need(d['measurement']==load(root/'topic_D_measurement_results/results.json'),'accepted comparisons copied exactly')
 controls=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError):controls.append(name);return
  raise ValueError('control accepted '+name)
 r=w['source_contract_closures'][0]['replacement'];ns=set(r['logical_nodes'])
 for name,mut in [('dropped actual prerequisite',lambda x:x['logical_nodes'].pop()),('duplicated owner',lambda x:x['owners'].append(x['owners'][0])),('undercounted subtotal',lambda x:x['known_extracted_subtotal']['calibrated_selected']['NFC'].__setitem__('characters_without_whitespace',0)),('external input silently zero',lambda x:x['unknown_inputs'].clear()),('printed plus raw double charge',lambda x:x['raw_program_alternative_subtotal']['calibrated_selected']['NFC'].__setitem__('characters_without_whitespace',x['raw_program_alternative_subtotal']['calibrated_selected']['NFC']['characters_without_whitespace']+1)),('graphic cost silently zero',lambda x:x.__setitem__('graphics_cost',0))]:
  z=copy.deepcopy(r);mut(z);reject(name,lambda:route(ns,z))
 # Allocation controls are independent of author validation.
 synthetic=[('a',' A'),('b','B  '),('c','é²')]
 aa,_=allocate(synthetic,'NFKC');need(aa['a']['whitespace_tokens']==1 and aa['b']['whitespace_tokens']==0 and aa['b']['characters_with_collapsed_whitespace']==2,'token and whitespace ownership crosses cuts')
 need(aa['c']['alphanumeric_units']==1,'normalization retained alphanumeric run')
 report={'status':'PASS_INDEPENDENT_D_ALLOCATION_AND_UNIONS','author_manifest_sha256':pin,'reuse':'Accepted D extraction/font calibration only; no author allocator, regex/bisect counting, partition builder, closure or reader imports. Logical semantics and numerical admissions reused, not re-proved.','document_cells':len(docs)*30,'owner_cells':len(owners)*30,'csv_rows':len(rows),'semantic_selected_spans':len(boundary_records),'all_variant_spans':sum(len(r['spans']) for d in p['documents'].values() for r in d['variants'].values()),'interface_coordinate_cells':len(interfaces)*30,'independent_route_unions':nroute,'viewer_node_closures':len(nodes),'full_raw_program_cells':len(raw)*10,'separate_driver_cells':len(drivers)*10,'negative_controls':controls,'allocator_cross_boundary_checks':2,'unknowns_preserved':True,'new_factor_or_credit':False}
 out.mkdir(parents=True,exist_ok=False);(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');(out/'semantic_boundaries.json').write_text(json.dumps(boundary_records,indent=2)+'\n')
 # Private inspection aid, never a review export or publication input.
 for k,text in texts.items():
  (out/(k+'_selected_private.txt')).write_text(text['calibrated_selected'])
  chunks=[]
  for s in p['documents'][k]['variants']['calibrated_selected']['spans']:
   t=text['calibrated_selected'][s['start']:s['end']]
   chunks.append(s['owner']+' | '+s['category']+' | pp'+str(s['physical_pages'])+' | '+str(s['end']-s['start'])+'\nSTART '+t[:220].replace('\n',' ')+'\nEND '+t[-180:].replace('\n',' '))
  (out/(k+'_boundaries_private.txt')).write_text('\n\n'.join(chunks))
 print(json.dumps(report))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--study-root',type=Path,required=True);a.add_argument('--packet',type=Path);a.add_argument('--out',type=Path,required=True);a.add_argument('--logical',type=Path);a.add_argument('--author-pin',default=PIN);x=a.parse_args();verify(x.study_root,x.packet or x.study_root/'topic_D_dag_costs',x.out,x.logical or x.study_root/'topic_D_logical_dag_v2',x.author_pin)
