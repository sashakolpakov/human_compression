from pathlib import Path
import hashlib,json,datetime
R=Path(__file__).resolve().parent;A=R.parent/'cyclic_three'
def need(x,m):
 if not x:raise ValueError(m)
def pin(p):
 p=Path(p).resolve();b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
need(not(R/'manifest.json').exists(),'new independent review')
author=pin(A/'manifest.json');need(author['sha256']=='03864d3e057a782065e34364f79364938bca8ebcb89a623066a102b2ec4f080f','exact author')
rows={}
def include(r):
 need(pin(r['path'])==r,'fresh exact binding');need(r['path']not in rows or rows[r['path']]==r,'consistent binding');rows[r['path']]=r
include(author)
for r in json.loads((A/'manifest.json').read_text())['exports']:
 q=pin(A/r['path']);need(all(q[k]==r[k]for k in ['bytes','sha256']),'author export');include(q)
for r in json.loads((A/'dependencies.json').read_text()):include(r)
report=json.loads((R/'native01/report.json').read_text());need(report['status']=='PASS_CYCLIC_THREE_EXACT_NATIVE_REPLAY'and report['native_pages']==4,'fresh native replay')
join=json.loads((R/'source_join01.json').read_text());need(join['status']=='PASS_SIX_DISTINCT_ORIGINAL_PAGE_JOINS'and len(join['pages'])==6,'exact original source joins')
orbits=json.loads((R/'orbits01.json').read_text());need(orbits['status']=='PASS_INDEPENDENT_REGULAR_ACTION_ORBITS'and orbits['m_values']==30,'independent finite corroboration')
(R/'dependencies.json').write_text(json.dumps([rows[k]for k in sorted(rows)],indent=2)+'\n')
review=dict(status='DISTINCT_ACCEPTED_L063_L064_CYCLIC_THREE_COUNTS',reviewer='finite_recoveries',author_agent='j3_recovery',author=author,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),full_proof_read=True,native_pages_viewed=[1,2,3,4],source_pages_viewed=dict(L063=[2,4,17],L064=[2,3,4]),fresh_native_replay=pin(R/'native01/report.json'),source_page_join=pin(R/'source_join01.json'),independent_orbits=pin(R/'orbits01.json'),unresolved_concerns=[],classical_premises_retained=True,claims=dict(different_types='first five final source counts recovered',equal_types='unordered inner count m+floor(m/2); full Aut count m'),new_group_searches=0,whole_original_credit=0,new_principal_refutation_credit=0,conjecture_credit=0,lean_credit=0,compression_measurement=None)
(R/'review.json').write_text(json.dumps(review,indent=2)+'\n')
exports=[]
for p in sorted(R.rglob('*')):
 if p.is_file():q=pin(p);exports.append(dict(path=str(p.relative_to(R)),bytes=q['bytes'],sha256=q['sha256']))
(R/'manifest.json').write_text(json.dumps(dict(status=review['status'],exports=exports),indent=2)+'\n');print(json.dumps(dict(manifest=pin(R/'manifest.json'),dependencies=len(rows),native_pages=4,source_pages=6,small_orbit_m_values=30)))
