import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
from pathlib import Path
import hashlib,json,shutil,datetime
S=Path('/Users/sasha/medusa/research/leemans');W=S/'reboot_20261013/L033_quotient_distinct';P=S/'corpus106_L033_quotient_kernels_v1';O=S/'corpus106_L033_quotient_kernels_independent_review'
def need(t,m):
 if not t:raise ValueError(m)
def h(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def pin(p):return dict(path=str(p),**h(p))
need(not O.exists(),'fresh review');need(h(P/'manifest.json')['sha256']=='17622931fc2abbf3ca612e8f95c0518856c873fb04ad2c89c8b013cd4fa6abbf','exact author')
r=json.loads((W/'fresh01/report.json').read_text());need(r['status']=='PASS_L033_AFFINE_QUOTIENT_COMPONENT','fresh pass')
O.mkdir()
for n in ['review.rst','independent_geometry.py','independent_geometry01.json','freeze_review.py','source05.png']:shutil.copy2(W/n,O/n)
shutil.copytree(W/'fresh01',O/'fresh')
deps={}
def acquire(p):
 a=pin(p);need(a['path'] not in deps or deps[a['path']]==a,'unique edition');deps[a['path']]=a
acquire(P/'manifest.json')
for a in json.loads((P/'manifest.json').read_text())['exports']:
 p=P/a['path'];need(h(p)=={k:a[k]for k in ['bytes','sha256']},'author export');acquire(p)
for a in json.loads((P/'dependencies.json').read_text()):
 p=Path(a['path']);need(h(p)=={k:a[k]for k in ['bytes','sha256']},'acquired dependency');acquire(p)
(O/'dependencies.json').write_text(json.dumps(list(deps.values()),indent=2)+'\n')
review=dict(status='ACCEPTED_L033_AUXILIARY_QUOTIENT_CORRECTION',author='/root',reviewer='/root/l044_resume',author_manifest=pin(P/'manifest.json'),full_proof_code_source_read=True,native_pages_directly_viewed=[1,2,3],source_pages_directly_viewed=[5,6],source_definitions_read=[2,3,4,5,6],fresh_session=28398,fresh_report=r,independent_controls=json.loads((W/'independent_geometry01.json').read_text()),corrections_requested=[],contributions='No contribution to new author proof or code. Prior distinct review of acquired L052 general theorem disclosed.',whole_original_credit=0,new_question_credit=0,new_Lean_declarations=0,new_measurements=0,owned_live_handles=[],timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(O/'review.json').write_text(json.dumps(review,indent=2)+'\n')
exports=[dict(path=str(p.relative_to(O)),**h(p))for p in sorted(O.rglob('*'))if p.is_file()]
(O/'manifest.json').write_text(json.dumps(dict(status=review['status'],exports=exports),indent=2)+'\n')
print(json.dumps(dict(path=str(O/'manifest.json'),sha256=h(O/'manifest.json')['sha256'],exports=len(exports),dependencies=len(deps))))
