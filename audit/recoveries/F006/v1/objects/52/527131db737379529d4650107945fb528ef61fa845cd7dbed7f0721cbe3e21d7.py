from pathlib import Path
from pypdf import PdfReader
import json,hashlib,re,copy
S=Path('/Users/sasha/medusa/research/leemans');W=S/'reboot_20261013';O=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pins={}
def pin(p):
 pins[str(p.relative_to(S))]={'path':str(p.relative_to(S)),'bytes':p.stat().st_size,'sha256':h(p)}
def require(x,msg):
 if not x:raise ValueError(msg)
source=S/'sources/coxeter_ranks2025.pdf';pin(source)
p=PdfReader(source);require(len(p.pages)==13,'source length');text=p.pages[11].extract_text();published={}
for line in text.splitlines():
 words=line.split()
 if words and words[0] in ['F4','H4','H3','E6','E7','E8']:
  require(len(words)==8 and words[0] not in published,'source row syntax')
  vals=[]
  for s in words[1:]:
   m=re.fullmatch(r'([0-9]+)(?:\(([0-9]+)\))?',s);require(m is not None,'source cell syntax');vals.append([int(m[1]),int(m[2] or 0)])
  published[words[0]]=vals
require(len(published)==6,'source rows')
models=S/'corpus106_F006_exceptional_work';results={};ordered={};bounds={}
for name,stem,lim,engine in [('F4','F006_F4_restored01',10,models),('H4','F006_H4_restored01',13,models),('E6','F006_E6_restored01',15,models),('E7','F006_E7_inner_restart01',21,models),('E8','central_marks_E8_01',29,S/'corpus106_central_marks_work')]:
 root=W/stem;rp=root/'report.json';d=json.loads(rp.read_text());pin(rp)
 require(d['status']=='EXITED' and d['returncode']==0 and d['complete_marker'] and d['unchanged'],'census receipt')
 for e in d['pins']:
  q=engine/e['path'];require(h(q)==e['sha256'],'census pin');pin(q)
 so=root/'stdout.log';se=root/'stderr.log';require(se.read_bytes()==b'','census stderr');pin(so);pin(se);raw=so.read_text()
 require(raw.count('COMPLETE_EXHAUSTION')==1,'completion marker')
 rr=[]
 for m in re.finditer(r'RANK\s+(\d+)\s+ordered\s+(\d+)\s+self\s+(\d+)\s+dual_classes\s+(\d+)\s+connected_ordered\s+(\d+)\s+connected_self\s+(\d+)\s+connected_dual\s+(\d+)',raw):rr.append(list(map(int,m.groups())))
 require([x[0] for x in rr]==list(range(1,lim+1)),'rank coverage')
 for rank,n,sd,du,nc,sc,dc in rr:
  require(0<=sd<=n and 0<=sc<=nc<=n and sc<=sd,'count range')
  require(2*du==n+sd and 2*dc==nc+sc,'reversal arithmetic')
  require(rank>=3 or n==0,'small ranks')
 c=[[sum(x[6] for x in rr),sum(x[5] for x in rr)]]+[[x[6],x[5]] for x in rr if 3<=x[0]<=7]+[[sum(x[6] for x in rr if x[0]>=8),sum(x[5] for x in rr if x[0]>=8)]]
 a=[[sum(x[3] for x in rr),sum(x[2] for x in rr)]]+[[x[3],x[2]] for x in rr if 3<=x[0]<=7]+[[sum(x[3] for x in rr if x[0]>=8),sum(x[2] for x in rr if x[0]>=8)]]
 require(c==published[name],'source row '+name)
 results[name]={'connected':c,'unrestricted':a,'tuples':sum(x[1] for x in rr),'all_ranks':lim};ordered[name]=rr
 bounds[name]={'full_census_terminal':True,'validation_acceptance':'PENDING_SEPARATE_FROZEN_REVIEW'}
h3=S/'corpus106_F006_small_coxeter_v1/census/report.json';pin(h3);d=json.loads(h3.read_text());require(d['status']=='COMPLETE_FINITE_CENSUS_EXECUTION','H3 receipt');rr=d['rows'];require([r['rank'] for r in rr]==list(range(1,7)),'H3 ranks')
rows={}
for r in rr:
 reps=r['representatives'];require(len(reps)==r['count'],'H3 count');require(sum(t['connected'] for t in reps)==r['connected'],'H3 connected count');require(sum(t['self_dual'] for t in reps)==r['self_dual'],'H3 self count');rows[r['rank']]=[r['connected'],sum(t['connected'] and t['self_dual'] for t in reps)]
c=[[sum(x[i] for x in rows.values()) for i in range(2)]]+[rows.get(k,[0,0]) for k in range(3,8)]+[[0,0]];require(c==published['H3'],'H3 source');results['H3']={'connected':c,'acquired_small_group_component':True}
# The displayed draft tables themselves, including zeros, were read directly.
checks=[]
def reject(label,call):
 try:call()
 except ValueError:checks.append(label)
 else:raise RuntimeError('control accepted '+label)
for label,bad in [('change_E8_rank7',copy.deepcopy(results)),('replace_connected_E7_by_all',copy.deepcopy(results)),('drop_zero_final_column',copy.deepcopy(results))]:
 if label=='change_E8_rank7':bad['E8']['connected'][5][0]+=1
 elif label=='replace_connected_E7_by_all':bad['E7']['connected']=bad['E7']['unrestricted']
 else:bad['F4']['connected'].pop()
 reject(label,lambda:require(all(bad[k]['connected']==published[k] for k in published),'damaged table'))
q=json.loads((W/'F006_model_identification01/report.json').read_text());require(q['status']=='PASS' and q['returncode']==0 and q['complete_marker'] and q['unchanged'],'identity receipt')
for x in q['pins']:
 p=Path(x['path']);require(p.stat().st_size==x['bytes'] and h(p)==x['sha256'],'identity pin');pin(p)
pin(W/'F006_model_identification01/report.json');pin(W/'F006_model_identification01/stdout.log');pin(W/'F006_model_identification01/stderr.log')
base=(models/'E8_model.g').read_bytes();require((S/'corpus106_central_marks_work/E8_model.g').read_bytes().startswith(base),'twist original model transport')
pin(Path(__file__))
report={'status':'PASS_DISTINCT_TERMINAL_CENSUS_AND_SOURCE_COMPARISON','printed_cells':42,'results':results,'ordered_ranks':ordered,'negative_controls':checks,'e8_base_model_byte_exact':True,'pins':list(pins.values()),'pending':['E7 all-subset validation assessment','E8 all-subset validation','frozen author packet'],'whole_original_credit':0}
(O/'evidence_report.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items() if k in ['status','printed_cells','negative_controls','pending']})
