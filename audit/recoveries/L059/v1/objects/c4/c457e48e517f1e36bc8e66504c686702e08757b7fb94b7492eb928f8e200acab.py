from pathlib import Path
import collections,copy,hashlib,json,re,sys
from pypdf import PdfReader
if sys.flags.optimize: raise RuntimeError('optimized Python unsupported')
S=Path('/Users/sasha/medusa/research/leemans')
P=S/'corpus106_L059_principal_v2'
W=S/'reboot_20261013/L059_recovery_work'
O=W.parent/'L059_principal_distinct'
def need(v,msg):
 if not v: raise ValueError(msg)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p,x): need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],str(p))
need(sha(P/'manifest.json')=='7bd69a403767f78a4b4702aa7b110b8eabf6d8d128c9cf4c31141f9b389d21d9','author edition')
m=json.loads((P/'manifest.json').read_text())
for x in m['exports']: pin(P/x['path'],x)
d=json.loads((P/'dependencies.json').read_text())
paths={Path(x['path']).resolve():x for x in d}
need(len(paths)==len(d),'duplicate dependency')
for p,x in paths.items():pin(p,x)
rows=json.loads((P/'census_register.json').read_text())
aliases={r['id']:r['retained_id'] for r in json.loads((W/'cubic_2048_bipartite.json').read_text()) if 'retained_id' in r}
count=collections.Counter();read_targets=set();worker_seen=set();old_producer=(W/'current_c4_census.g').read_text()
for r in rows:
 for key in ['witness','worker','receipt','stdout','stderr','basis','oracle','prior_capped_receipt','done']:
  if key in r:need((W/r[key]).resolve() in paths,'unbound '+key+' '+r['graph'])
 worker=W/r['worker'];worker_seen.add(worker)
 for path in re.findall(r'Read\("([^"]+)"\)',worker.read_text()):
  target=(W/path).resolve();need(target in paths,'worker Read dependency '+str(target));read_targets.add(target)
 if 'receipt' in r:
  receipt=json.loads((W/r['receipt']).read_text());count['terminal_receipts']+=1
  actual_name=aliases.get(r['graph'],r['graph']) if r['family']=='symmetric' else r['graph']
  need(receipt['name']==actual_name and receipt['elapsed_seconds']>=0 and receipt['status']=='PASS' and receipt['returncode']==0,'receipt identity')
  text=(W/r['stdout']).read_text()
  complete=re.findall(r'^L059_[A-Z0-9_]*COMPLETE '+re.escape(actual_name)+r' (\d+)(?: \d+)?$',text,re.M)
  need(complete==[str(r['markings'])],'literal completion token '+r['graph'])
  if 'oracle' in r:
   expected=receipt.get('nauty_input_sha256',receipt.get('oracle_sha256'))
   need(expected==sha(W/r['oracle']),'actual oracle');count['exact_oracle_pins']+=1
  for name,digest in receipt.get('library_sha256',{}).items():
   need((W/name).resolve() in paths and sha(W/name)==digest,'actual retry library');count['retry_library_pins']+=1
 else:
  count['old_completed_graphs']+=1
  witness='PrintTo("'+r['witness']+'","L059Result := ",R,";\\n");'
  token='PrintTo("'+r['done']+'","COMPLETE '+r['graph']+' ",Length(R.witnesses)," ",Runtime()-t,"\\n");'
  need(witness in old_producer and token in old_producer and old_producer.index(witness)<old_producer.index(token),'old producer completion order')
  before=old_producer[:old_producer.index(witness)]
  need(before.rfind('R:=P177Census(D);;')>before.rfind('D:=P177Graph('),'complete all-subgroup computation before token')
count['worker_files']=len(worker_seen);count['direct_worker_read_targets']=len(read_targets)
# Recursively close literal Read edges from workers, including the accepted action wrapper.
seen=set();todo=list(read_targets)
while todo:
 p=todo.pop()
 if p in seen:continue
 seen.add(p)
 for name in re.findall(r'Read\("([^"]+)"\)',p.read_text()):
  q=(W/name).resolve();need(q in paths,'nested Read missing '+str(q));todo.append(q)
count['transitive_read_targets']=len(seen)
fresh=PdfReader(O/'native01/faithful_markings.pdf');old=PdfReader(P/'faithful_markings.pdf')
need(len(fresh.pages)==len(old.pages)==10,'native page count')
texts=[]
for i,(a,b) in enumerate(zip(fresh.pages,old.pages),1):
 aa=a.extract_text();bb=b.extract_text();need(aa==bb,'native text page '+str(i));texts.append(hashlib.sha256(aa.encode()).hexdigest())
need('Overfull' not in (O/'native01/faithful_markings.log').read_text(),'native overflow')
def scope_guard(c):
 need(c['counts']=={'graphs':1950,'faithful_markings':4254,'printed_table_cells':39,'symmetric_cubic':[714,1082],'semisymmetric_cubic':[43,102],'subdivisions':[796,1427],'quartic_corrected_scope':[397,1643]},'scope counts')
 need(len(c['qualifications'])==8 and c['open_questions']['new_question_credit']==0,'qualifications/questions')
 need(c['whole_original_credit']==0 and c['new_formal_work']==0 and c['measurements'] is None,'no automatic credit')
c=json.loads((P/'principal_contract.json').read_text());scope_guard(c)
bad=[]
for field in ['graphs','faithful_markings','printed_table_cells']:
 b=copy.deepcopy(c);b['counts'][field]+=1;bad.append(b)
b=copy.deepcopy(c);b['counts']['subdivisions']=[714,1427];bad.append(b)
b=copy.deepcopy(c);b['qualifications'].pop();bad.append(b)
for field in ['whole_original_credit','new_formal_work']:
 b=copy.deepcopy(c);b[field]=1;bad.append(b)
b=copy.deepcopy(c);b['open_questions']['new_question_credit']=1;bad.append(b)
for b in bad:
 try:scope_guard(b)
 except ValueError:pass
 else:raise ValueError('damaged contract accepted')
result={'status':'PASS_DISTINCT_CLOSURE','author_exports':len(m['exports']),'dependencies':len(paths),'dependency_bytes':sum(x['bytes'] for x in d),'execution_closure':dict(count),'fresh_native_pages':10,'page_text_sha256':texts,'direct_native_viewed':list(range(1,11)),'source_physical_pages_viewed':[9,10],'benign_underfull_warning':True,'scope_controls':len(bad),'full_census_repeated':False}
(O/'closure_report.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='page_text_sha256'},sort_keys=True))
