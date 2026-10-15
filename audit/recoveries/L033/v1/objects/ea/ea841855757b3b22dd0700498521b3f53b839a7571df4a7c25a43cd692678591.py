import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
from pathlib import Path
import json,hashlib,shutil,datetime
S=Path('/Users/sasha/medusa/research/leemans');W=S/'reboot_20261013/L033_spherical_distinct';P=S/'corpus106_L033_spherical_v2';V=S/'corpus106_L033_spherical_v1';O=S/'corpus106_L033_spherical_independent_review'
def need(b,m):
 if not b:raise ValueError(m)
def h(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def pin(p):return dict(path=str(p),**h(p))
need(not O.exists(),'fresh review');need(h(P/'manifest.json')['sha256']=='3b717862fe5e794f339b21441a11b09206796cc638f1c91837367c9c18b49360','final edition')
fresh=json.loads((W/'fresh01/report.json').read_text());delta=json.loads((W/'final02/report.json').read_text());extra=json.loads((W/'independent.json').read_text())
need(fresh['status']=='PASS_L033_SPHERICAL_COMPONENT' and delta['status']=='PASS_FINAL_V2_DELTA_AND_NATIVE' and extra['status']=='PASS_INDEPENDENT_GEOMETRIC_CONTROLS','all terminal successes')
O.mkdir()
for n in ['reading.rst','independent.py','independent.json','final_delta.py','freeze_review.py','source-01.png','source-02.png','source-03.png','source-04.png']:shutil.copyfile(W/n,O/n)
shutil.copyfile(W/'fresh01/report.json',O/'fresh_orbit_report.json');shutil.copytree(W/'final02',O/'final_replay')
reading=(W/'reading.rst').read_text();start=reading.index('The fixed source was read')
review='''Distinct acceptance of the spherical component
===============================================

Accepted final v2 unchanged, subject to its precisely stated retained
classification inputs. The complete six-page proof recovers L033 Theorem
4.2 and the proper-residue assertion of Theorem 4.3. Its E6 order correction
is independently verified. No whole-original, open-question, Lean or
compression credit is granted by this component review.

The following detailed reading concerns the complete unchanged argument
acquired from v1, followed by the final successor audit.

'''+reading[start:]+'''

Final successor and disposition
-------------------------------

The complete literal v1-to-v2 delta was read. It adds the explicitly
identified source E6 order typo and its short orbit-stabilizer proof;
the main classification argument is unchanged. The new Cartan tree has
determinant three. Deleting vertex 3 gives D5, and the fundamental-vector
stabilizer is exactly that standard parabolic, by the retained chamber
theorem. The 27 reachable vectors therefore give order 27*1920=51840.
A separate reviewer orbit in dual coordinates, without the author's
inverse or orbit routine, agrees with all 27 vectors after conversion.
The source page visibly prints 12*6!, so 72*6! is an explicit correction,
not a silently substituted table entry.

The successor's complete 27 exports and 201 dependencies were freshly
verified. Its 15 compressed exceptional orbit certificates, C++ producer,
independent reader and old antipode functions are unchanged. The complete
fresh v1 replay of 899,402 vectors and 7,177,574 reflection checks is
therefore reused by exact byte and AST checks. The only new finite fields
are the E6 orbit size and group order. Its new certificate was freshly
recomputed and checked byte for byte. No redundant exceptional census was
needed. The final TeX was independently rebuilt twice, with identical
six-page text and no layout or reference warnings. All six final pages
were directly viewed, including the changed E6 proof and classification
table. The four source pages were also directly viewed.

All required mathematical, code, source and native interfaces have passed.
Maxwell's theorem is retained through the fixed source with its exact
definition; the primary paper remains unacquired and is not represented
as independently verified. The finite Coxeter representation, chamber,
parabolic and string reconstruction inputs remain attributed. These
qualifications are part of acceptance. Root supplied the E6 correction
independently; the reviewer supplied no new proof to the accepted author
manuscript. There are no owned live review processes.
'''
(O/'review.rst').write_text(review)
deps={}
def acquire(p):
 r=pin(p);old=deps.get(r['path']);need(old is None or old==r,'one bound edition');deps[r['path']]=r
for Q in [P,V]:
 acquire(Q/'manifest.json')
 for r in json.loads((Q/'manifest.json').read_text())['exports']:
  p=Q/r['path'];need(h(p)=={k:r[k]for k in ['bytes','sha256']},'author unchanged');acquire(p)
for r in json.loads((P/'dependencies.json').read_text()):
 p=Path(r['path']);need(h(p)=={k:r[k]for k in ['bytes','sha256']},'dependency unchanged');acquire(p)
for d in ['fresh01','final02']:
 for p in sorted((W/d).rglob('*')):
  if p.is_file():acquire(p)
(O/'dependencies.json').write_text(json.dumps(list(deps.values()),indent=2)+'\n')
record=dict(status='ACCEPTED_L033_SPHERICAL_COMPONENT',author='/root',reviewer='/root/l044_resume',author_manifest=pin(P/'manifest.json'),source_scope=['Theorem4.2','Theorem4.3','Table1 E6 correction'],full_proof_read=True,full_code_read=True,source_pages_directly_viewed=[7,8,9,10],native_pages_directly_viewed=6,full_fresh_orbit_session=30807,full_fresh_orbit_result=fresh,final_delta=delta,independent_controls=extra,retained_inputs=json.loads((P/'scope.json').read_text())['retained_inputs'],contributions='No contribution to new author argument. Previously distinctly reviewed acquired L052 and quotient components. Root independently supplied E6 source correction.',scope='Spherical component only; Euclidean and hyperbolic principal obligations remain separate.',whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None,owned_live_handles=[],timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(O/'review.json').write_text(json.dumps(record,indent=2)+'\n')
exports=[dict(path=str(p.relative_to(O)),**h(p))for p in sorted(O.rglob('*'))if p.is_file()]
(O/'manifest.json').write_text(json.dumps(dict(schema='human-compression-review-v1',status=record['status'],exports=exports),indent=2)+'\n')
print(json.dumps(dict(path=str(O/'manifest.json'),sha256=h(O/'manifest.json')['sha256'],exports=len(exports),dependencies=len(deps))))
