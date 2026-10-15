from pathlib import Path
import hashlib,json,shutil
W=Path(__file__).resolve().parent;C=W.parent;P=C/'cubic_example_v1';O=C/'cubic_example_review_v1'
def read(p):return json.loads(p.read_text())
def save(p,r):p.write_text(json.dumps(r,indent=2)+'\n')
def need(v,m):
    if not v:raise ValueError(m)
def pin(p):
    p=p.resolve();b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
need(not O.exists(),'fresh review');a=pin(P/'manifest.json');need(a['sha256']=='c9faad77d2093ee331b3d400ceaea5974af579bf52b6aadc6397f9aac626ce46','author')
need(read(W/'execution01/receipt.json')['status']=='CLEAN_FINITE_RETURN','fresh');need(read(W/'independent01/report.json')['status']=='PASS_INDEPENDENT_CUBIC_DUAL_AND_RESIDUES','independent')
O.mkdir();copies={'review.rst':'review.rst','review_check.py':'check.py','freeze_review.py':'freeze_review.py','run_review.py':'run_review.py','independent.py':'independent.py','execution01/receipt.json':'fresh_receipt.json','fresh01/report.json':'fresh_report.json','independent01/report.json':'independent_report.json'}
for i in [1,2]:copies[f'fresh01/native/page-{i:02d}.png']=f'page-{i:02d}.png'
for x,y in copies.items():shutil.copyfile(W/x,O/y)
save(O/'review.json',dict(status='ACCEPTED_L033_CUBIC_EXAMPLE_COMPONENT_V1',author_manifest=a,author='/root',reviewer='/root/publication_recovery',author_bytes_changed=False,new_contribution_to_author=False,complete_proof_code_source_read=True,source_native=pin(C/'cubic_example_work/source05.png'),source_page=5,native_pages_viewed=[1,2],fresh_receipt=pin(W/'execution01/receipt.json'),independent_report=pin(W/'independent01/report.json'),reviewer_failure=pin(W/'development01/syntax_failure.json'),changes_requested=[],retained_premises=['Standard cubic Coxeter realization','Accepted universal affine subgroup/presentation lemma before finite parameters'],whole_original_credit=0,new_Lean=0,new_question_credit=0,measurement=None))
deps={r['path']:r for r in read(W/'execution01/inputs.json')}
for p in [p for p in W.rglob('*')if p.is_file()and '__pycache__'not in p.parts]:
    r=pin(p)
    if r['path']in deps:need(deps[r['path']]==r,'stable input')
    deps[r['path']]=r
for r in deps.values():need(pin(Path(r['path']))==r,'exact binding')
save(O/'dependencies.json',[deps[k]for k in sorted(deps)]);exports=[]
for p in sorted(O.rglob('*')):
    if p.is_file():
        r=pin(p);r['path']=str(p.relative_to(O));exports.append(r)
save(O/'manifest.json',dict(status='ACCEPTED_L033_CUBIC_EXAMPLE_COMPONENT_V1',exports=exports));print(json.dumps(dict(manifest=pin(O/'manifest.json'),exports=len(exports),dependencies=len(deps))))
