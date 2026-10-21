"""Seal completed review evidence without repeating the finite target."""
from pathlib import Path
import hashlib,json,shutil
W=Path(__file__).resolve().parent;C=W.parent;P=C/'divisor_v1';O=C/'divisor_review_v1'
S=C.parents[1]
def read(p):return json.loads(p.read_text())
def save(p,r):p.write_text(json.dumps(r,indent=2)+'\n')
def need(v,m):
    if not v:raise ValueError(m)
def pin(p):
    p=p.resolve();b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def exact(r):need(pin(Path(r['path']))==r,'exact '+r['path'])
need(not O.exists(),'fresh review')
a=pin(P/'manifest.json');need(a['sha256']=='d24447e9377bfd6d0aae82b9ef9b5b81631231226646ef8bbe308dd66353906b','author')
need(read(W/'execution01/receipt.json')['status']=='CLEAN_FINITE_RETURN','clean terminal')
need(read(W/'fresh01/report.json')['status']=='PASS_DIVISOR_TARGET9720','fresh report')
need(read(W/'independent01/report.json')['status']=='PASS_INDEPENDENT_LITERAL_9720_OBSTRUCTION','independent report')
src=S/'reboot_20261013/L033_work/hyperbolic_recovery_work/source14.png'
review=dict(status='ACCEPTED_L033_DIVISOR_TARGET9720_COMPONENT_V1',author_manifest=a,author='/root',reviewer='/root/publication_recovery',author_bytes_changed=False,new_contribution_to_author=False,prior_roles='Reviewer authored acquired L033 core, seed/composed-module and named-group components. Root authored the new divisor restriction, application, proof and checker.',complete_proof_code_source_read=True,source_native=[pin(src)],source_page=14,native_rasters=[dict(page=i,pin=pin(W/f'fresh01/native/page-{i:02d}.png'),directly_viewed=True)for i in range(1,4)],fresh_session=75432,fresh_receipt=pin(W/'execution01/receipt.json'),fresh_report=pin(W/'fresh01/report.json'),independent_report=pin(W/'independent01/report.json'),exact_target=9720,changes_requested=[],retained_premises=['Complete LINS normal-quotient algorithm and classification tables','Acquired complete Coxeter seed and equivalent composed p-module implementation','Exact GAP finite-group and representation routines'],scope_exclusions=['All-indices-through-9720 census','Minimum order','Historical raw3840 result','Whole L033 source recovery'],whole_original_credit=0,new_Lean=0,new_question_credit=0,measurement=None)
O.mkdir()
copies={'review.rst':'review.rst','review_check.py':'check.py','freeze_review.py':'freeze_review.py','run_review.py':'run_review.py','independent.py':'independent.py','execution01/receipt.json':'fresh_receipt.json','fresh01/report.json':'fresh_report.json','independent01/report.json':'independent_report.json','fresh01/negative.json':'negative.json','fresh01/target/stdout':'target.stdout','fresh01/target/receipt.json':'target_receipt.json','fresh01/comparison/stdout':'comparison.stdout','fresh01/controls/stdout':'controls.stdout'}
for i in range(1,4):copies[f'fresh01/native/page-{i:02d}.png']=f'page-{i:02d}.png'
for x,y in copies.items():shutil.copyfile(W/x,O/y)
save(O/'review.json',review)
deps={r['path']:r for r in read(W/'execution01/inputs.json')}
paths=[p for p in W.rglob('*')if p.is_file()and '__pycache__'not in p.parts]+[src]
for p in paths:
    r=pin(p)
    if r['path']in deps:need(deps[r['path']]==r,'stable dependency')
    deps[r['path']]=r
for r in read(W/'independent01/report.json')['inputs']:
    if r['path']in deps:need(deps[r['path']]==r,'stable independent dependency')
    deps[r['path']]=r
for r in deps.values():exact(r)
save(O/'dependencies.json',[deps[k]for k in sorted(deps)])
exports=[]
for p in sorted(O.rglob('*')):
    if p.is_file():
        r=pin(p);r['path']=str(p.relative_to(O));exports.append(r)
save(O/'manifest.json',dict(status=review['status'],exports=exports))
print(json.dumps(dict(status=review['status'],manifest=pin(O/'manifest.json'),exports=len(exports),dependencies=len(deps))))
