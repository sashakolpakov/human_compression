from pathlib import Path
import json,hashlib,datetime,shutil
from pypdf import PdfReader
S=Path('/Users/sasha/medusa/research/leemans');W=Path(__file__).resolve().parent;A=S/'topic_B_L019_degree_ten_v1'
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def need(x,m):
 if not x:raise RuntimeError(m)
deps=[pin(A/'manifest.json')];need(deps[0]['sha256']=='e4e41edb482c7d8df356212082e85af0c8b449112d90ac9157fbabdadebca5d7','author edition')
for base,rows in [(A,json.loads((A/'manifest.json').read_text())['exports']),(S,json.loads((A/'dependencies.json').read_text()))]:
 for r in rows:
  z=pin(base/r['path']);need(all(z[k]==r[k]for k in ['bytes','sha256']),'exact binding '+r['path']);deps.append(z)
x=[p.extract_text()for p in PdfReader(A/'degree_ten.pdf').pages];y=[p.extract_text()for p in PdfReader(W/'replay01/degree_ten.pdf').pages];need(x==y and len(y)==2,'native text equality');log=(W/'replay01/degree_ten.log').read_text();need(not any(t in log for t in ['Overfull','Underfull','LaTeX Warning']),'native warning')
(W/'dependencies.json').write_text(json.dumps(deps,indent=2)+'\n');review={'status':'ACCEPTED_L019_DEGREE_TEN_COMPONENT','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'author_manifest':pin(A/'manifest.json'),'fresh_replay':'89719 terminal0','fresh_report':pin(W/'replay01/report.json'),'extra_controls':pin(W/'independent_controls.json'),'native_pages_directly_viewed':[1,2],'native_text_equal':True,'author_unchanged':True,'scope':'Anchored fractured natural S10 rank6 with actual supported even-prefix kernels; critical attachment m10 only.','remaining':'Critical m>=12, contraction and stability up to isomorphism/duality, principal base counts.','whole_original_credit':0,'new_question_credit':0,'new_Lean':0,'measurement':None,'independence':'No contribution to new proof/code; prior acquired anchored-even and small-symmetric reviews disclosed.'};(W/'review.json').write_text(json.dumps(review,indent=2)+'\n');O=S/'topic_B_L019_degree_ten_independent_review';need(not O.exists(),'immutable destination');O.mkdir()
for p in sorted(W.rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(W)
 if '__pycache__'in rel.parts or p.suffix in ['.aux','.out','.pyc']:continue
 q=O/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
exports=[]
for p in sorted(O.rglob('*')):
 if p.is_file():z=pin(p);z['path']=str(p.relative_to(O));exports.append(z)
(O/'manifest.json').write_text(json.dumps({'status':review['status'],'exports':exports,'whole_original_credit':0},indent=2)+'\n');print(pin(O/'manifest.json'));print('exports',len(exports),'bindings',len(deps))
