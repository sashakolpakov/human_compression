from pathlib import Path
import re,json,hashlib,ast
S=Path(__file__).resolve().parents[2]
W=S/'reboot_20261013'
raw=(W/'central_marks_E8_01/stdout.log').read_bytes()
p=W/'F006_E8_full_IP01'
rows=json.loads((p/'input.json').read_text())['rank_counts']
def need(b,m):
 if not b:raise ValueError(m)
def sha(q):return hashlib.sha256(q.read_bytes()).hexdigest()
h=hashlib.sha256();h.update(b'recordedMarks:=[];;\n');counts=[]
for row in rows:
 rank=row[0];prefix=f'COMPLETE_TUPLES_RANK_{rank} '.encode();need(raw.count(prefix)==1,'unique rank')
 start=raw.index(prefix)+len(prefix)
 while raw[start:start+1].isspace():start+=1
 need(raw[start:start+1]==b'[','opening list')
 depth=0;tuples=0;end=None
 for token in re.finditer(br'[\[\]]',raw[start:]):
  if token[0]==b'[':
   depth+=1
   if depth==2:tuples+=1
  else:
   depth-=1
   if depth==0:end=start+token.end();break
 need(end is not None and tuples==row[1],'all original literal tuples')
 h.update(f'recordedMarks[{rank}]:='.encode());h.update(raw[start:end]);h.update(b';;\n');counts.append([rank,tuples])
h.update(('reportedCounts:='+json.dumps([r[1] for r in rows])+';;\n').encode())
need(h.hexdigest()==sha(p/'records.g'),'all validation records byte-exact')
need((p/'model.g').read_bytes()==(S/'corpus106_central_marks_work/E8_model.g').read_bytes(),'same full-action model')
module=S/'corpus106_L071_remaining_censuses_v1/validate.py';code=None
for node in ast.parse(module.read_text()).body:
 if isinstance(node,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='CODE' for x in node.targets):code=ast.literal_eval(node.value)
need(code is not None and code.encode()==(p/'validate.g').read_bytes(),'unchanged retained full-IP validator')
report=dict(status='PASS_EXACT_E8_LITERAL_INPUT_TRANSFER_TERMINAL_VALIDATION_STILL_REQUIRED',ranks=counts,tuples=sum(r[1] for r in rows),subset_pairs=sum(r[1]*4**r[0] for r in rows),records_sha256=h.hexdigest(),finite_checks_repeated=False,whole_original_credit=0)
(Path(__file__).parent/'E8_input_transfer_report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='ranks'}))
