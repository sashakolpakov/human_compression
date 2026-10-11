#!/usr/bin/env python3
"""Independent ownership, graph-union and reader arithmetic audit.

Reuses only the independently accepted PDF extraction/calibration interface.
The proposed semantic cuts and supplement table are data, manually reviewed.
No author allocator, graph-cost checker, reader builder or arithmetic is imported.
Primary text and private boundary-reading extracts are never exported by this runner.
"""
import argparse, bisect, collections, copy, csv, hashlib, importlib.util, json, re, sys, unicodedata
from fractions import Fraction
from pathlib import Path
sys.dont_write_bytecode=True
V=('raw_untrimmed','raw_selected','calibrated_selected'); F=('NFC','NFKC')
M=('whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace')
PIN='d78d618ed35ffb31d260ded85d27627f8db43a435a5fe4cd02822dd510beb718'
def need(b,s):
 if not b: raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def module(p,name):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def zeros():return {v:{f:{m:0 for m in M} for f in F} for v in V}
def add(xs):
 xs=list(xs);return {v:{f:{m:sum(x[v][f][m] for x in xs) for m in M} for f in F} for v in V}
def metrics(t):
 collapsed=' '.join(t.split()); runs=0;before=False
 for c in t:
  now=c.isalnum()
  if now and not before:runs+=1
  before=now
 return dict(zip(M,[len(t.split()),runs,sum(not c.isspace() for c in t),len(collapsed),len(collapsed.encode())]))
def normalized_allocation(t,spans,form):
 chunks=[unicodedata.normalize(form,t[s['start']:s['end']]) for s in spans]
 norm=''.join(chunks);need(norm==unicodedata.normalize(form,t),'normalization boundary')
 labels=[s['owner'] for s,c in zip(spans,chunks) for _ in c]
 out={s['owner']:dict.fromkeys(M,0) for s in spans};lastspace=True;lastalpha=False
 for i,(c,o) in enumerate(zip(norm,labels)):
  space=c.isspace();alpha=c.isalnum()
  if not space:
   out[o][M[2]]+=1;out[o][M[3]]+=1;out[o][M[4]]+=len(c.encode())
   if lastspace:out[o][M[0]]+=1
  elif not lastspace:
   # The first character of this whitespace run owns its one collapsed space.
   j=i
   while j<len(norm) and norm[j].isspace():j+=1
   if j<len(norm):out[o][M[3]]+=1;out[o][M[4]]+=1
  if alpha and not lastalpha:out[o][M[1]]+=1
  lastspace=space;lastalpha=alpha
 need({m:sum(x[m] for x in out.values()) for m in M}==metrics(norm),'independent token conservation')
 return out

def texts_and_bindings(root):
 q=root/'topic_C_measurement';sys.path.insert(0,str(q))
 ex=module(q/'extract_inputs.py','accepted_c_extractor');need(ex.pypdf.__version__=='6.13.0','pinned PDF parser')
 spec=read(q/'source_input_spec.json')['sources']|read(q/'replacement_input_spec.json')['ours']
 text={k:dict(zip(V,ex.document(root,k,b)[:3])) for k,b in spec.items()}
 return text,spec

def calculate(p,text,spec,cuts):
 owner=p['owners'];out={o:zeros() for o in owner};docs={};count=0
 need(set(p['documents'])==set(text),'full nine documents')
 for k,variants in text.items():
  row=p['documents'][k];b=spec[k];need(row['pdf_sha256']==b['pdf_sha256'] and row['pages']==b['pages'],'PDF binding')
  selectedpos=[];raw=variants[V[0]]
  # Independent event projection, not the author selected_positions implementation.
  for inclusion in b['included_spans']:
   at=inclusion['start']
   for e in b['excluded_furniture']:
    if inclusion['start']<=e['start'] and e['end']<=inclusion['end']:
     selectedpos.extend(range(at,e['start']));selectedpos.append(None);at=e['end']
   selectedpos.extend(range(at,inclusion['end']));selectedpos.append(None)
  selectedpos=selectedpos[:-1]
  need(''.join('\n' if i is None else raw[i] for i in selectedpos)==variants[V[1]],'selection projection')
  need(len(selectedpos)==len(variants[V[2]]),'one-codepoint calibration')
  lines=variants[V[2]].splitlines(keepends=True);offsets=[0]
  for line in lines:offsets.append(offsets[-1]+len(line))
  proposed=[]
  for location,name,category in cuts[k]:
   line,needle=(location,None) if isinstance(location,int) else location
   loc=offsets[line-1]
   if needle is not None:
    need(lines[line-1].count(needle)==1,'unique semantic split');loc+=lines[line-1].index(needle)
   proposed.append((loc,name));need(owner[name]=={'id':name,'document':k,'category':category},'semantic owner category')
  need(proposed[0][0]==0 and all(a[0]<b_[0] for a,b_ in zip(proposed,proposed[1:])),'ordered semantic cuts')
  positions=[x[0] for x in proposed]
  selectedowners=[proposed[bisect.bisect_right(positions,i)-1][1] for i in range(len(selectedpos))]
  rawowners=[None]*len(raw)
  for i,j in enumerate(selectedpos):
   if j is not None:rawowners[j]=selectedowners[i]
  for e in b['excluded_furniture']:rawowners[e['start']:e['end']]=[k+'.furniture']*(e['end']-e['start'])
  need(all(rawowners),'all raw characters assigned')
  expectedowner={V[0]:rawowners,V[1]:selectedowners,V[2]:selectedowners};docs[k]=zeros()
  for v,t in variants.items():
   r=row['variants'][v];need((r['length'],r['sha256'])==(len(t),sha(t.encode())),'exact text')
   at=0;labels=[];ps=list(range(len(t))) if v==V[0] else selectedpos
   for s in r['spans']:
    need(s['start']==at and at<s['end']<=len(t),'gap/overlap/empty');o=s['owner'];need(owner[o]['document']==k and s['category']==owner[o]['category'],'owner metadata')
    need(sha(t[at:s['end']].encode())==s['sha256'],'passage hash')
    labels.extend([o]*(s['end']-at));poss=[x for x in ps[at:s['end']] if x is not None]
    page=sorted({max(j+1 for j,bp in enumerate(b['page_bindings']) if bp['start']<=x) for x in poss})
    need(s['physical_pages']==page and s['raw_start']==(min(poss) if poss else None) and s['raw_end']==(max(poss)+1 if poss else None),'physical locators')
    at=s['end'];count+=1
   need(at==len(t) and labels==expectedowner[v],'complete ownership matches declared cuts')
   for f in F:
    a=normalized_allocation(t,r['spans'],f)
    for o,x in a.items():out[o][v][f]=x
    docs[k][v][f]=metrics(unicodedata.normalize(f,t))
  need(add(out[o] for o in owner if owner[o]['document']==k)==docs[k],'full document conservation')
 return out,docs,count

def analyze(p,w,d,g,c,acq,text,spec,cuts,supp,raw):
 costs,docs,spans=calculate(p,text,spec,cuts)
 need(costs==w['owner_costs'] and docs==w['document_costs'],'all independent allocations')
 nodes={n['id']:n for n in g['nodes']};parent={n['id']:n['parent'] for n in g['nodes'] if n.get('parent')};children=collections.defaultdict(set)
 for n,par in parent.items():children[par].add(n)
 def descendants(n):
  found={n};queue=[n]
  while queue:
   q=queue.pop()
   for x in children[q]-found:found.add(x);queue.append(x)
  return found
 interfaces={}
 for n,node in nodes.items():
  unknown=node['side'] in ['external','verification'] or node['document']=='L108';ids=set()
  if not unknown:
   for x in descendants(n):
    ids.update(o for o in p['owners'] if o==x or o.startswith(x+'.'));ids.update(supp.get(x,[]))
    if x in parent and parent[x]+'.statement' in p['owners']:ids.add(parent[x]+'.statement')
  interfaces[n]=ids;l=w['node_interfaces'][n]
  need(sorted(ids)==l['owners'] and l['known_weight']==(None if unknown else add(costs[o] for o in ids)),'node interface '+n)
  need(not l['charged_again'] and l['expanded_dependency_cost'] is None,'no alias/external charge')
 predecessors=collections.defaultdict(set)
 for e in g['edges']:
  if e['kind'] in g['logical_edge_kinds']:predecessors[e['target']].add(e['source'])
 def closure(targets):
  reached=set(targets);queue=list(targets)
  while queue:
   for x in predecessors[queue.pop()]-reached:reached.add(x);queue.append(x)
  return reached
 def owners(names):return set().union(*(interfaces[n] for n in names)) if names else set()
 def check_route(row,targets):
  ns=closure(targets);os=owners(ns)
  need(row['logical_nodes']==sorted(ns) and row['owners']==sorted(os),'independent route union')
  need(row['known_extracted_subtotal']==add(costs[o] for o in os),'route cost')
  need(row['unknown_inputs']==sorted(n for n in ns if w['node_interfaces'][n]['known_weight'] is None),'route unknowns')
  need(row['expanded_dependency_cost'] is None and row['graphics_cost'] is None,'unknown costs null')
  expectraw=add(costs[o] for o in os if p['owners'][o]['document']!='CODE')
  for n in set(raw)&ns:
   for v in V:
    for f in F:
     for m in M:expectraw[v][f][m]+=raw[n][f][m]
  need(expectraw==row['raw_program_alternative_subtotal'],'whole raw program alternative')
  need(row['by_document']=={k:add(costs[o] for o in os if p['owners'][o]['document']==k) for k in sorted({p['owners'][o]['document'] for o in os})},'route document allocation')
 rows={r['id']:r for r in w['source_contract_closures']};need(len(rows)==len(c['rows'])==40,'all clauses')
 for r in c['rows']:
  check_route(rows[r['id']]['historical'],r['historical_outputs']);check_route(rows[r['id']]['replacement'],r['new_outputs'])
 for key,targets in g['new_application_outputs'].items():check_route(w['new_application_closures'][key],targets)
 for key,targets in g['additional_current_comparisons'].items():check_route(w['additional_current_comparisons'][key],targets)
 viewnodes={n['id']:n for n in d['nodes']};need(d['edges']==g['edges'] and d['parents']==parent,'logical graph unchanged')
 for n in nodes:
  row=viewnodes[n];ns=closure([n]);os=owners(ns)
  need(row['owners']==sorted(interfaces[n]) and row['weight']==w['node_interfaces'][n]['known_weight'],'view own cost')
  need(row['closure']['unique_owner_ids']==sorted(os) and row['closure']['known_owned_text_subtotal']==add(costs[o] for o in os),'view prerequisite cost')
  need(row['closure']['unknown_external_nodes']==sorted(x for x in ns if w['node_interfaces'][x]['known_weight'] is None),'view unknown input')
 paid=set();history=[];unknown=False;src={'C1':'L088','C2':'N013','C3':'L108','C4':'F014'}
 need(acq==d['acquisition'] and acq['historical_complete_numeric_curve'] is None,'same symbolic acquisition')
 for step,key in zip(acq['stages'],['U_C','CODE','C1','C2','C3','C4']):
  full={o for o,b in p['owners'].items() if b['document']==key};ns=closure([n for n,b in nodes.items() if b['document']==key and not n.startswith('program.')]);used=owners(ns)
  need(not used-paid-full and not paid&full,'acquisition dependency/pay once')
  expected={'previous_owner_ids':paid,'complete_local_owner_ids':full,'logical_route_owner_ids':used,'new_owner_ids':full,'cumulative_owner_ids':paid|full,'reused_owner_ids':used&paid,'local_text_outside_route':full-used}
  for f,x in expected.items():need(step[f]==sorted(x),'acquisition owner set '+f)
  for f,x in [('new_cost',full),('cumulative_cost',paid|full),('written_cumulative_cost',{o for o in paid|full if p['owners'][o]['document']!='CODE'}),('reused_route_cost',used&paid)]:need(step[f]==add(costs[o] for o in x),'acquisition full cost '+f)
  if key in src:
   s=src[key]
   if s=='L108':unknown=True
   else:history.append(s)
   h=step['historical_cumulative'];need(h['known_documents']==history and h['known_subtotal']==add(docs[s] for s in history) and h['unknown_coefficient']==int(unknown),'symbolic historical cost')
   need(h['complete_cost']==(None if unknown else add(docs[s] for s in history)),'unknown historical total')
  paid|=full
 need(paid=={o for o,b in p['owners'].items() if b['document'] in ['U_C','CODE','C1','C2','C3','C4']},'all complete papers and full programs')
 fractions=0
 for coord in d['measurement']['coordinates']:
  v,f,m=coord['variant'],coord['normalization'],coord['unit'];value=lambda k:docs[k][v][f][m]
  common=value('U_C');apps=sum(value(k) for k in src);known=sum(value(k) for k in ['L088','N013','F014']);printed=value('CODE');rawsum=sum(x[f][m] for x in raw.values())
  expected={'common_theory':common,'all_applications':apps,'written_denominator':common+apps,'complete_printed_program_cost':printed,'complete_raw_program_cost':rawsum,'complete_denominator':common+apps+printed,'raw_program_denominator':common+apps+rawsum,'known_source_sum':known}
  for k,x in expected.items():need(coord[k]==x,'complete document coordinate '+k)
  need(coord['overall_factor'] is None and coord['complete_source_sum'] is None,'no incomplete overall scalar')
  for k,den in [('written_papers_only',common+apps),('complete_printed_programs',common+apps+printed),('complete_raw_programs',common+apps+rawsum)]:
   r=coord['overall_formulas'][k];need(r['unknown_numerator_coefficient']==1 and r['unknown_source']=='L108' and r['known_numerator']==known and r['denominator']==den and r['overall_factor'] is None,'whole symbolic fraction')
  for r in coord['per_result']:
   s,a=r['source'],r['application'];need(r['application_cost']==value(a),'full local denominator')
   if s=='L108':need(r['source_cost'] is None and r['factor'] is None and r['fraction'] is None,'missing conditional source')
   else:
    x=Fraction(value(s),value(a));need(r['source_cost']==value(s) and r['fraction']==str(x) and r['factor']==float(x),'conditional reduced fraction');fractions+=1
 need(len(d['measurement']['coordinates'])==30 and fractions==90,'all30 policies/90 known conditional fractions')
 need(d['measurement']['complete_common_and_programs_prepaid_for_conditional_factors'] is True,'conditional prepayment explicit')
 need(p['missing_L108_original_pdf_cost'] is None and p['node_count_ratio'] is None,'missing/node claims')
 for k in ['complete_historical_pdf_cost','expanded_external_proof_cost','graphic_cost','compression_ratio']:need(w[k] is None,'unknown not zero '+k)
 return {'owners':len(costs),'documents':len(docs),'metric_coordinates':30,'owner_metric_cells':len(costs)*30,'document_metric_cells':len(docs)*30,'span_count':spans,'node_interfaces':len(nodes),'output_routes':85,'reader_node_closures':len(nodes),'conditional_exact_fractions':fractions,'symbolic_overall_coordinates':90,'acquisition_stages':6,'primary_current_written':docs['U_C']['calibrated_selected']['NFC'][M[2]]+sum(docs[k]['calibrated_selected']['NFC'][M[2]] for k in src)}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh output');root=a.study_root;packet=root/'topic_C_dag_costs';need(sha((packet/'manifest.json').read_bytes())==PIN,'frozen author')
 for r in read(packet/'manifest.json')['exports']:
  # Frozen packets use relative paths; account for filename conventions explicitly.
  path=r.get('path',r.get('file'));data=(packet/path).read_bytes();need(sha(data)==r['sha256'] and len(data)==r['bytes'],'author export '+path)
 for r in read(packet/'input_bindings.json')['inputs']:
  rel=Path(r['path']);need(not rel.is_absolute() and '..' not in rel.parts,'safe retained path');data=(root/rel).read_bytes();need(sha(data)==r['sha256'] and len(data)==r['bytes'],'retained input '+str(rel))
 p=read(packet/'partition.json');w=read(packet/'weights.json');d=read(packet/'view_data.json');acq=read(packet/'acquisition.json');g=read(root/'topic_C_logical_dag_v2/logical_graph.json');c=read(root/'topic_C_logical_dag_v2/coverage.json')
 text,spec=texts_and_bindings(root);declarations=module(packet/'boundaries.py','proposed_semantic_cuts');cuts=declarations.boundaries();supp=declarations.supplements()
 raw={}
 for n,b in w['raw_program_alternative'].items():
  b=b['binding'];data=(root/b['path']).read_bytes();need(sha(data)==b['sha256'],'complete raw program binding');raw[n]={f:metrics(unicodedata.normalize(f,data.decode())) for f in F}
 result=analyze(p,w,d,g,c,acq,text,spec,cuts,supp,raw)
 with (packet/'owner_costs.csv').open(newline='') as f:csvrows=list(csv.DictReader(f))
 need(len(csvrows)==len(p['owners'])*6,'all CSV rows')
 for r in csvrows:
  o,v,f=r['owner'],r['variant'],r['normalization'];need(r['document']==p['owners'][o]['document'] and r['category']==p['owners'][o]['category'],'CSV owner identity')
  need({m:int(r[m]) for m in M}==w['owner_costs'][o][v][f],'all CSV units')
 controls=[]
 for name in ['owner_gap','owner_overlap','owner_wrong_hash','source_zero','external_zero','drop_shared_statement','duplicate_program_owner','omit_program_wrapper','wrong_atomic_cost','context_unpaid','reuse_discount','known_history_after_missing','missing_application_denominator','wrong_conditional_fraction','reverse_logical_arrow']:
  pp,ww,dd,gg,aa=copy.deepcopy((p,w,d,g,acq))
  ss=pp['documents']['C4']['variants']['calibrated_selected']['spans']
  if name=='owner_gap':ss[1]['start']+=1
  elif name=='owner_overlap':ss[1]['start']-=1
  elif name=='owner_wrong_hash':ss[1]['sha256']='0'*64
  elif name=='source_zero':pp['missing_L108_original_pdf_cost']=0
  elif name=='external_zero':ww['node_interfaces']['ext.Danzer']['known_weight']=zeros()
  elif name=='drop_shared_statement':ww['node_interfaces']['C.Graph.geometry']['owners'].remove('C.Graph.statement')
  elif name=='duplicate_program_owner':ww['new_application_closures']['L088']['owners'].append('program.construction.printed')
  elif name=='omit_program_wrapper':ww['node_interfaces']['program.census']['owners'].remove('CODE.wrapper')
  elif name=='wrong_atomic_cost':ww['owner_costs']['UC.front']['calibrated_selected']['NFKC'][M[0]]+=1
  elif name=='context_unpaid':aa['stages'][2]['new_owner_ids'].remove('C1.front');dd['acquisition']=aa
  elif name=='reuse_discount':aa['stages'][2]['new_cost']['calibrated_selected']['NFC'][M[2]]-=1;dd['acquisition']=aa
  elif name=='known_history_after_missing':aa['stages'][4]['historical_cumulative']['complete_cost']=zeros();dd['acquisition']=aa
  elif name=='missing_application_denominator':dd['measurement']['coordinates'][0]['written_denominator']-=1
  elif name=='wrong_conditional_fraction':dd['measurement']['coordinates'][0]['per_result'][0]['fraction']='1'
  else:gg['edges'][0]['source'],gg['edges'][0]['target']=gg['edges'][0]['target'],gg['edges'][0]['source']
  try:analyze(pp,ww,dd,gg,c,aa,text,spec,cuts,supp,raw)
  except ValueError as e:controls.append({'name':name,'rejected':True,'reason':str(e)})
  else:raise ValueError('corruption accepted '+name)
 report={'status':'PASS_INDEPENDENT_OWNERSHIP_UNIONS_ARITHMETIC',**result,'CSV_rows':len(csvrows),'controls':controls,'author_manifest_sha256':PIN,'checker_sha256':sha(Path(__file__).read_bytes()),'scope':'Accepted extraction reused; allocation, closure unions, symbolic accounting and exact fractions independently implemented. Semantic cuts require separate manual review. No font/source mathematical re-review or new scalar claim.','primary_text_exported':False,'node_count_factor':None}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
