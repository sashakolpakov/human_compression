from pathlib import Path
import hashlib,json,datetime,shutil
from pypdf import PdfReader
s=Path('/Users/sasha/medusa/research/leemans');w=Path(__file__).resolve().parent;a=s/'topic_B_L019_small_symmetric_v2'
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def need(x,m):
 if not x:raise RuntimeError(m)
deps=[pin(a/'manifest.json')]
for base,rows in [(a,json.loads((a/'manifest.json').read_text())['exports']),(s,json.loads((a/'dependencies.json').read_text()))]:
 for r in rows:
  p=base/r['path'];z=pin(p);need(z['bytes']==r['bytes']and z['sha256']==r['sha256'],'binding '+str(p));deps.append(z)
old=s/'topic_B_L019_small_symmetric_v1';deps.append(pin(old/'manifest.json'))
for r in json.loads((old/'manifest.json').read_text())['exports']:
 p=old/r['path'];z=pin(p);need(z['bytes']==r['bytes']and z['sha256']==r['sha256'],'old edition');deps.append(z)
for n in ['six.g','eight.g','eight_tuples.json','verify_eight.py','check.py','permutation_library.py']:need((old/n).read_bytes()==(a/n).read_bytes(),'unchanged scientific code')
x=[p.extract_text()for p in PdfReader(a/'small_symmetric.pdf').pages];y=[p.extract_text()for p in PdfReader(w/'replay01/native/small_symmetric.pdf').pages];need(x==y and len(y)==2,'native equality')
(w/'native_comparison.json').write_text(json.dumps({'status':'PASS','pages':2,'author_fresh_text_equal':True,'all_pages_directly_viewed':True,'final_warnings':False},indent=2)+'\n')
(w/'dependencies.json').write_text(json.dumps(deps,indent=2)+'\n')
r={'status':'ACCEPTED_L019_SMALL_SYMMETRIC_BOUNDARY_V2','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'author_manifest':pin(a/'manifest.json'),'scope':'Actual critical Sym_m rank m/2+1 plus even six-point rank-three A5 attachment, even m<=8 has a sufficient internal perfect split.','pending':'m>=10, stability correspondence and base counts','whole_original_credit':0,'new_question_credit':0,'new_Lean':0,'measurement':None,'fresh_replay':'terminal75401','independent_subset_pairs':9216,'independent_S4_complete_markings':12,'independent_S4_fractured_simplex':6,'native_pages_directly_viewed':[1,2],'all_author_bytes_unchanged':True,'authorship_disclosure':'Prior acquired anchored-even distinct review and older L038 authorship only; no contribution to this new component.'};(w/'review.json').write_text(json.dumps(r,indent=2)+'\n')
out=s/'topic_B_L019_small_symmetric_independent_review';need(not out.exists(),'immutable destination');out.mkdir()
for p in sorted(w.rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(w)
 if '__pycache__'in rel.parts or p.suffix in ['.aux','.out','.log','.pyc']:continue
 t=out/rel;t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,t)
exports=[]
for p in sorted(out.rglob('*')):
 if p.is_file():q=pin(p);q['path']=str(p.relative_to(out));exports.append(q)
(out/'manifest.json').write_text(json.dumps({'status':r['status'],'exports':exports,'whole_original_credit':0},indent=2)+'\n');print(pin(out/'manifest.json'));print(len(exports),'exports',len(deps),'bindings')
