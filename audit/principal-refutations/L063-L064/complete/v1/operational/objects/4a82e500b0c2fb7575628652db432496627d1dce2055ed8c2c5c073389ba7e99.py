from pathlib import Path
import hashlib,json,datetime
R=Path(__file__).resolve().parent;A=R.parent/'s4_automorphisms'
def need(x,m):
 if not x:raise ValueError(m)
def pin(p):
 p=Path(p).resolve();b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
need(not(R/'manifest.json').exists(),'new independent review')
author=pin(A/'manifest.json');need(author['sha256']=='dcf9e2d2d376c45d2c3aafdb40ee318451d80db428ba5923cd77c46116334a42','exact author')
rows={}
def include(r):
 need(pin(r['path'])==r,'fresh exact binding');need(r['path']not in rows or rows[r['path']]==r,'consistent binding');rows[r['path']]=r
include(author)
for r in json.loads((A/'manifest.json').read_text())['exports']:
 p=A/r['path'];q=pin(p);need(all(q[k]==r[k]for k in ['bytes','sha256']),'author export');include(q)
for r in json.loads((A/'dependencies.json').read_text()):include(r)
report=json.loads((R/'native01/report.json').read_text());need(report['status']=='PASS_S4_AUTOMORPHISMS_EXACT_NATIVE_REPLAY'and report['native_pages']==4,'fresh native replay')
join=json.loads((R/'source_join01.json').read_text());need(join['status']=='PASS_DISTINCT_SOURCE_PAGE_JOIN'and len(join['pages'])==3,'fresh original page join')
parities=[dict(p=p,epsilon=1 if p%8==1 else -1,d=(p-(1 if p%8==1 else -1))//8)for p in [17,23,31,41,47,71,73,79,89]]
need([r['p']for r in parities if r['d']%2==0]==[17,31,47,79],'four exact corrections')
(R/'dependencies.json').write_text(json.dumps([rows[k]for k in sorted(rows)],indent=2)+'\n')
review=dict(status='DISTINCT_ACCEPTED_L063_S4_FULL_AUTOMORPHISMS',reviewer='finite_recoveries',contributing_agents=['root','j3_recovery'],author=author,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),full_proof_read=True,proof_native_pages_viewed=[1,2,3,4],source_physical_pages_viewed=[3,4,22],fresh_native_replay=pin(R/'native01/report.json'),literal_source_page_join=pin(R/'source_join01.json'),accepted_arc_gate=join['accepted_arc_gate'],prime_arithmetic=parities,unresolved_concerns=[],proof_limits=['explicit classical premises retained','q=9 excluded','no whole-source or new principal-refutation credit','no conjecture solution, Lean verification or compression measurement'],new_group_searches=0,whole_source_credit=0,source_refutation_credit=0)
(R/'review.json').write_text(json.dumps(review,indent=2)+'\n')
exports=[]
for p in sorted(R.rglob('*')):
 if p.is_file():q=pin(p);exports.append(dict(path=str(p.relative_to(R)),bytes=q['bytes'],sha256=q['sha256']))
(R/'manifest.json').write_text(json.dumps(dict(status=review['status'],exports=exports),indent=2)+'\n')
print(json.dumps(dict(manifest=pin(R/'manifest.json'),acquired_inputs=len(rows),proof_pages=4,source_pages=3,new_group_searches=0)))
