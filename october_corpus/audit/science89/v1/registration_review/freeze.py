import sys
if sys.flags.optimize:raise RuntimeError('ordinary Python required')
from pathlib import Path
import json,hashlib,shutil,datetime,difflib
S=Path('/Users/sasha/medusa/research/leemans');Q=S/'algebra/coxeter_quotients';W=Q/'registration_distinct_work';A=Q/'publication_work';T=A/'trial01';R=Path('/Users/sasha/medusa/math_compression');P=S/'computation/publication/science89_registration_review_v1'
def pin(p,root=None):
 b=p.read_bytes();return dict(path=str(p.relative_to(root))if root else str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def need(v,m):
 if not v:raise ValueError(m)
P.mkdir(parents=True)
for n in ['independent.py','optimization_controls.py','freeze.py','review.rst','fresh_tool_records.json']:shutil.copyfile(W/n,P/n)
(P/'independent01').mkdir()
for n in ['report.json','git_inventory.json']:shutil.copyfile(W/'independent01'/n,P/'independent01'/n)
shutil.copytree(W/'optimization01',P/'optimization01');shutil.copytree(A/'native_trial01',P/'native01')
shutil.copyfile(A/'public_native01/report.json',P/'public_native_report.json')
old=json.loads((T/'audit/science89/v1/history_routes.json').read_text())['routes']
for n in ['README.rst','audit/completion.rst','audit/protocol.tex','scripts/verify_snapshot.py']:
 d=''.join(difflib.unified_diff((T/old[n]['path']).read_text().splitlines(True),(T/n).read_text().splitlines(True),fromfile='baseline/'+n,tofile='candidate/'+n));(P/(n.replace('/','_')+'.diff')).write_text(d)
deps={}
for row in json.loads((A/'registration_handoff_manifest.json').read_text())['files']:
 p=A/row['path'];q=pin(p);need(all(q[k]==row[k]for k in ['bytes','sha256']),'changed handoff');deps[str(p)]=q
for row in json.loads((A/'candidate_manifest.json').read_text())['files']:
 for root in [T,R]:
  p=root/row['path'];q=pin(p);need(all(q[k]==row[k]for k in ['bytes','sha256']),'changed candidate');deps[str(p)]=q
for n in ['registration_ready.json','registration_handoff_manifest.json','candidate_manifest.json','registration_drafts_manifest.json','public_native01/report.json']:
 p=A/n;deps[str(p)]=pin(p)
for n in ['registration_ready.json','candidate_manifest.json','registration_drafts_manifest.json']:shutil.copyfile(A/n,P/n)
dump(P/'dependencies.json',dict(bindings=sorted(deps.values(),key=lambda r:r['path']),namespace='absolute',scope='Exact handoff and trial/installed candidate. Final gates and publication manifest update are separate.'))
dump(P/'native_review.json',dict(pdf=pin(T/'audit/protocol.pdf'),tex=pin(T/'audit/protocol.tex'),directly_viewed_pages=list(range(1,9)),pages=[pin(p,P)for p in sorted((P/'native01').glob('page-*.png'))],result='Eight exact candidate pages directly viewed; clean, readable, no clipping. Public independent text/raster equality and timestamp-sensitive restoration acquired separately.'))
review=dict(status='ACCEPTED_SCIENCE89_REGISTRATION',reviewer='/root/f003_resume',author='/root/publication_recovery',installer='/root/publication_recovery under explicit root delegation',baseline_commit='5cbf9a6908d3a4cb20d1184297764ae8c6d596ab',author_ready=pin(A/'registration_ready.json'),handoff_manifest=pin(A/'registration_handoff_manifest.json'),candidate_manifest=pin(A/'candidate_manifest.json'),scope='Distinct concrete registration only. Authorized publisher retains final gates, full history, publication manifest, commit and push.',proposed_counts=dict(recoveries=89,refutations=9,handled=98,pending=7,measured=53,unmeasured=36,editorial=1),source_ids_changed=['L033'],handoff_files=1285,candidate_files=1260,predecessor_objects=40487,old_functions=207,historical_pointers=9,exact_symlinks=2,independent_false_admissions=8,author_preflight_damages=18,independent_optimization_guards=6,native_pages_directly_viewed=list(range(1,9)),accepted_mathematical_review_sha256='cfde0cdbf82f655eeda8cf9ccb6a036cf3f0293f02cb616a6c493f984863e25b',accepted_operational_review_sha256='fab8cfc9f1bb2b7f7a153c7e3e25aa27cf1974ccff33218fd16ac7ca7fa5d640',public_writes=False,mathematical_census_repeated=False,full_history_repeated=False,new_measurements=0,new_question_credit=0,new_Lean_credit=0,independent_new_scientific_credit=0,all_review_sessions_terminal=True,role_disclosure='Prior distinct reviews of acquired L033 components only; no authorship of principal synthesis, portable closure or registration. Independent operational audit adapted from science88 with changed baseline/source/counts checked.',reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
dump(P/'review.json',review)
checker='''import sys\nif sys.flags.optimize:raise RuntimeError("ordinary Python required")\nfrom pathlib import Path\nimport json,hashlib\nP=Path(__file__).resolve().parent\ndef check(p,r):\n b=p.read_bytes()\n if len(b)!=r["bytes"]or hashlib.sha256(b).hexdigest()!=r["sha256"]:raise ValueError(str(p))\nm=json.loads((P/"manifest.json").read_text())\nfor r in m["exports"]:check(P/r["path"],r)\nd=json.loads((P/"dependencies.json").read_text())\nfor r in d["bindings"]:check(Path(r["path"]),r)\nprint(json.dumps(dict(status="PASS_SCIENCE89_REGISTRATION_REVIEW_INTEGRITY",exports=len(m["exports"]),bindings=len(d["bindings"]))))\n'''
(P/'check.py').write_text(checker)
exports=[pin(p,P)for p in sorted(P.rglob('*'))if p.is_file()and p!=P/'manifest.json']
dump(P/'manifest.json',dict(status=review['status'],exports=exports))
for row in exports:need(pin(P/row['path'],P)==row,'export changed')
print(json.dumps(dict(manifest=pin(P/'manifest.json'),exports=len(exports),bindings=len(deps))))
