import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
from pathlib import Path
import hashlib,json,shutil,datetime
S=Path('/Users/sasha/medusa/research/leemans');W=S/'reboot_20261013/N010_cone_distinct';P=S/'corpus106_N010_realization_cone_v1';O=S/'corpus106_N010_realization_cone_independent_review'
assert not O.exists()
def h(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def pin(p):return dict(path=str(p.relative_to(S)),**h(p))
assert h(P/'manifest.json')['sha256']=='a2aaf6a508d6088b3cf1ff9a0ccf3ce8a88bf52781606be6bc956ce534e467df'
r=json.loads((W/'fresh01/report.json').read_text());assert r['status']=='PASS_N010_REALIZATION_COMPONENT_BINDINGS' and r['native']['text_identical']
O.mkdir()
for p in W.rglob('*'):
 if p.is_file():
  q=O/p.relative_to(W);q.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(p,q)
deps=[pin(P/'manifest.json')]
for row in json.loads((P/'manifest.json').read_text())['exports']:
 p=P/row['path'];assert h(p)=={k:row[k]for k in ['bytes','sha256']};deps.append(pin(p))
for row in json.loads((P/'dependencies.json').read_text()):
 p=Path(row['path']);assert h(p)=={k:row[k]for k in ['bytes','sha256']};deps.append(pin(p))
(O/'dependencies.json').write_text(json.dumps(deps,indent=2)+'\n')
review=dict(status='ACCEPTED_FINITE_REALIZATION_CONE_COMPONENT',author='/root',reviewer='/root/l044_resume',author_manifest=pin(P/'manifest.json'),complete_mathematical_proof_read=True,all_five_results_checked=True,fresh_session=78372,fresh_report=r,native_pages=4,all_native_pages_directly_viewed=True,source_section=6,source_pages_directly_viewed=[14,15,16],independent_controls=json.loads((W/'independent_controls.json').read_text()),optimization_guards=2,corrections_requested=[],contributions='No mathematical contribution to author proof; prior source-contract audit disclosed.',whole_original_credit=0,new_question_credit=0,new_Lean_credit=0,new_measurements=0,owned_live_handles=[],timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(O/'review.json').write_text(json.dumps(review,indent=2)+'\n')
exports=[dict(path=str(p.relative_to(O)),**h(p))for p in sorted(O.rglob('*'))if p.is_file()]
(O/'manifest.json').write_text(json.dumps(dict(status=review['status'],exports=exports),indent=2)+'\n')
print(json.dumps(dict(path=str(O/'manifest.json'),sha256=h(O/'manifest.json')['sha256'],exports=len(exports))))
