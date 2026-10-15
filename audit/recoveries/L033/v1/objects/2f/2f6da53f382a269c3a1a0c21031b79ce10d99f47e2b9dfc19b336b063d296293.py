from pathlib import Path
import hashlib,json,shutil
W=Path(__file__).resolve().parent;C=W.parent;S=C.parents[1];P=C/'small_square_v1';O=C/'small_square_review_v1'
def read(p):return json.loads(p.read_text())
def save(p,r):p.write_text(json.dumps(r,indent=2)+'\n')
def need(v,m):
    if not v:raise ValueError(m)
def pin(p):
    p=p.resolve();b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
need(not O.exists(),'fresh review');a=pin(P/'manifest.json');need(a['sha256']=='d6d218b2ac2297fd0c53f4976c64e5e2e361e503d44e12baa253635bb39369f0','author')
need(read(W/'execution01/receipt.json')['status']=='CLEAN_FINITE_RETURN','fresh');need(read(W/'independent01/report.json')['status']=='PASS_INDEPENDENT_COMPLETE_SQUARE_MARKINGS','independent')
src=S/'reboot_20261013/L033_work/hyperbolic_recovery_work/source14.png'
O.mkdir();copies={'review.rst':'review.rst','review_check.py':'check.py','freeze_review.py':'freeze_review.py','run_review.py':'run_review.py','independent.py':'independent.py','printed_witness.py':'printed_witness.py','printed_witness.json':'printed_witness.json','execution01/receipt.json':'fresh_receipt.json','fresh01/report.json':'fresh_report.json','independent01/report.json':'independent_report.json','fresh01/census/stdout':'census.stdout','fresh01/census/scope.json':'census_scope.json','fresh01/literal.json':'literal.json','fresh01/quotients.json':'quotients.json'}
for i in [1,2]:copies[f'fresh01/native/page-{i:02d}.png']=f'page-{i:02d}.png'
for x,y in copies.items():shutil.copyfile(W/x,O/y)
review=dict(status='ACCEPTED_L033_COMPLETE_SQUARE3535_THROUGH3840',author_manifest=a,author='/root',reviewer='/root/publication_recovery',author_bytes_changed=False,new_contribution_to_author=False,prior_roles='Reviewer authored acquired core, methods, names and earlier positive-only3535 execution. New complete-negative application and proof belong to root.',complete_proof_code_source_read=True,source_native=pin(src),source_page=14,fresh_session=6979,independent_session=86725,native_pages_viewed=[1,2],fresh_receipt=pin(W/'execution01/receipt.json'),independent_report=pin(W/'independent01/report.json'),printed_witness=pin(W/'printed_witness.json'),reviewer_failure=pin(W/'development01/array_comparison_failure.json'),changes_requested=[],retained_premises=['Complete LINS normal-subgroup algorithm and classification tables','Accepted exact Coxeter seeds/composed-module implementation','Exact GAP finite-group and representation routines','Accepted spherical H3 classification and full coset reconstruction'],scope_exclusions=['Universal minimum beyond3840','Named global group for positive1920','All-indices-through9720','Whole L033 source recovery'],whole_original_credit=0,new_Lean=0,new_question_credit=0,measurement=None)
save(O/'review.json',review);deps={r['path']:r for r in read(W/'execution01/inputs.json')}
paths=[p for p in W.rglob('*')if p.is_file()and '__pycache__'not in p.parts]+[src,C/'divisor_review_v1/manifest.json']
for p in paths:
    r=pin(p)
    if r['path']in deps:need(deps[r['path']]==r,'stable dependency')
    deps[r['path']]=r
for r in deps.values():need(pin(Path(r['path']))==r,'exact dependency')
save(O/'dependencies.json',[deps[k]for k in sorted(deps)]);exports=[]
for p in sorted(O.rglob('*')):
    if p.is_file():
        r=pin(p);r['path']=str(p.relative_to(O));exports.append(r)
save(O/'manifest.json',dict(status=review['status'],exports=exports));print(json.dumps(dict(status=review['status'],manifest=pin(O/'manifest.json'),exports=len(exports),dependencies=len(deps))))
