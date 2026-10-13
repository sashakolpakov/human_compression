from pathlib import Path
import hashlib,json,re,ast,subprocess
from portable_paths import S, W, resolve, verify_pin
A=S/'corpus106_L071_Co3_v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,s):
 if not x:raise ValueError(s)
expected='8046a3b83c00cf09ef258bac8a3a378c1eb99c93cb51242154b247edd72f894d'
need(sha(A/'manifest.json')==expected,'author manifest')
m=json.loads((A/'manifest.json').read_text());d=json.loads((A/'dependencies.json').read_text())
for root,ls in [(A,m['exports']),(S,d['bindings'])]:
 for x in ls:
  verify_pin(x,root)
run=S/'reboot_20261013/double_coset/Co3_01';val=S/'reboot_20261013/L071_Co3_validation01'
for root in [run,val]:
 r=json.loads((root/'report.json').read_text());need(r['status']=='EXITED' and r['returncode']==0 and r['complete_marker'] and r['unchanged'],'terminal receipt')
 need((root/'stderr.log').read_bytes()==b'','empty stderr')
 for x in r['pins']:
  p=resolve(x['path'], S/'corpus106_double_coset_work')
  need(sha(p)==x['sha256'],'execution pin '+str(p))
# Accepted source extraction; no new primary-source reading is claimed.
frozen=json.loads((A/'co3_source_tables.json').read_text())
cells={rank:{tuple(x['type']):x['count'] for x in frozen['rows'][str(rank)]} for rank in [3,4,5]}
need([len(cells[i]) for i in [3,4,5]]==[225,565,34],'824 accepted source cells')
# Re-extract the exact literal leaves and compare the whole validation input bytes.
raw=(run/'stdout.log').read_text();need(raw.count('COMPLETE_EXHAUSTION')==1,'completion')
need('MODEL Co3 ORDER 495766656000 AUT_ORDER 495766656000' in raw,'model/aut guard')
marks=list(re.finditer(r'COMPLETE_TUPLES_RANK_(\d+) ',raw));need([int(x[1]) for x in marks]==list(range(1,39)),'all ranks')
rebuilt=['recordedMarks:=[];;']
for x in marks:
 rank=int(x[1]);start=raw.index('[',x.end());depth=0
 for end in range(start,len(raw)):
  depth+=(raw[end]=='[')-(raw[end]==']')
  if depth==0:break
 lit=raw[start:end+1];need(re.fullmatch(r'[\s\d,()\[\]]+',lit) is not None,'literal permutations')
 rebuilt.append(f'recordedMarks[{rank}]:='+lit+';;')
need(('\n'.join(rebuilt)+'\n').encode()==(val/'records.g').read_bytes(),'complete unchanged validation tuple stream')
counts={int(a):int(b) for a,b in re.findall(r'^RANK (\d+) ordered (\d+)',raw,re.M)}
need(set(counts)==set(range(1,39)),'all census rows');need({k:v for k,v in counts.items() if v}=={3:21118,4:1746,5:44},'census totals')
log=(val/'stdout.log').read_text();need(log.count('COMPLETE_CO3_VALIDATION')==1 and 'ALL_CO3_TABLE_CELLS_AND_FULL_IP_PASS TUPLES 22908 PRINTED_CELLS 824' in log,'all tuple validation')
verified={};ms=list(re.finditer(r'VERIFIED_TYPE_COUNTS (\d+) ',log));need([int(x[1]) for x in ms]==list(range(1,39)),'all validated ranks')
for x in ms:
 start=log.index('[',x.end());dep=0
 for end in range(start,len(log)):
  dep+=(log[end]=='[')-(log[end]==']')
  if dep==0:break
 ls=ast.literal_eval(log[start:end+1]);verified[int(x[1])]={tuple(a):b for a,b in ls}
for rank in range(1,39):need(verified[rank]=={k:v for k,v in cells.get(rank,{}).items() if v},'all positive cells and unlisted zeros '+str(rank))
# Verify the generated checker is exactly the source's literal code and the expected table is exact.
code=(A/'validate_co3.py').read_text();tree=ast.parse(code);literal_code=None
for node in tree.body:
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='code' for t in node.targets):literal_code=ast.literal_eval(node.value)
need(literal_code==(val/'validate.g').read_text(),'whole generated checker')
es=(val/'expected.g').read_text();e=ast.literal_eval(es.split(':=',1)[1].rsplit(';;',1)[0]);need({(rank,tuple(typ)):n for rank,typ,n in e}=={(rank,typ):n for rank,cs in cells.items() for typ,n in cs.items()},'all expected cells')
r={'status':'PASS_PORTABLE_EXECUTION_RECONSTRUCTION_AGAINST_ACCEPTED_SOURCE_TABLE','author_manifest_sha256':expected,'exports':len(m['exports']),'external_bindings':len(d['bindings']),'all_execution_pins_current':True,'accepted_source_cell_counts':[225,565,34],'source_cells_equal':True,'all_literal_tuple_bytes_equal':True,'tuple_total':sum(counts.values()),'all_ranks_through':38,'all_printed_cells_and_unlisted_zeros_equal':True,'generated_checker_exact':True,'native_rebuild_repeated':False,'long_enumeration_or_validation_repeated':False,'whole_original_credit':0}
(W/'replay_report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
