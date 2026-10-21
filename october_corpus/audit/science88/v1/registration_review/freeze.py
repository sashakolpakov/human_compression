import sys
if sys.flags.optimize:raise RuntimeError('ordinary Python required')
from pathlib import Path
import json,hashlib,shutil,datetime,difflib
S=Path('/Users/sasha/medusa/research/leemans');W=S/'reboot_20261013/L100_registration_distinct';A=W.parent/'L100_publication_work';R=Path('/Users/sasha/medusa/math_compression');T=A/'trial01';P=S/'computation/publication/science88_registration_review_v1';P.mkdir(parents=True)
def pin(p,root=None):
 b=p.read_bytes();return dict(path=str(p.relative_to(root))if root else str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def dump(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
for n in ['independent.py','optimization_controls.py','freeze.py','installed_difference01.json']:
 shutil.copyfile(W/n,P/n)
for dirname in ['fresh01','independent01','native01','optimization01']:
 shutil.copytree(W/dirname,P/dirname)
(P/'independent02').mkdir()
for name in ['report.json','git_inventory.json']:shutil.copyfile(W/'independent02'/name,P/'independent02'/name)
shutil.copyfile(A/'root_native01/report.json',P/'root_native_correction_report.json')
old=json.loads((T/'audit/science88/v1/history_routes.json').read_text())['routes']
for n in ['README.rst','audit/completion.rst','audit/protocol.tex','scripts/verify_snapshot.py']:
 d=''.join(difflib.unified_diff((T/old[n]['path']).read_text().splitlines(True),(T/n).read_text().splitlines(True),fromfile='baseline/'+n,tofile='candidate/'+n))
 (P/(n.replace('/','_')+'.diff')).write_text(d)
# Every concrete private handoff and installed candidate file is freshly bound.
deps={}
for row in json.loads((A/'registration_handoff_manifest.json').read_text())['files']:
 p=A/row['path'];q=pin(p)
 if any(q[k]!=row[k]for k in ['bytes','sha256']):raise ValueError('changed handoff '+str(p))
 deps[str(p)]=q
for row in json.loads((A/'candidate_manifest.json').read_text())['files']:
 p=R/row['path'];q=pin(p)
 if any(q[k]!=row[k]for k in ['bytes','sha256']):raise ValueError('changed installed candidate '+str(p))
 deps[str(p)]=q
for name in ['registration_ready.json','registration_handoff_manifest.json','candidate_manifest.json','registration_drafts_manifest.json','root_native01/report.json','root_native01/root_built_protocol.log']:
 p=A/name;deps[str(p)]=pin(p)
for n in ['registration_ready.json','candidate_manifest.json','registration_drafts_manifest.json']:shutil.copyfile(A/n,P/n)
dump(P/'dependencies.json',dict(bindings=sorted(deps.values(),key=lambda r:r['path']),namespace='absolute',scope='Exact handoff and installed candidate at distinct review; final root gates and publication manifest update remain separate.'))
dump(P/'native_review.json',dict(pdf=pin(T/'audit/protocol.pdf'),tex=pin(T/'audit/protocol.tex'),directly_viewed_pages=list(range(1,9)),pages=[pin(p,P)for p in sorted((P/'native01').glob('page-*.png'))],result='All eight exact candidate protocol pages directly viewed, readable and clean. Count/scope/new L100 paragraph and retained qualifications checked. Root independently rebuilt identical text and raster pages; its fresh log was preserved before restoring the exact reviewed candidate log.'))
review=dict(status='ACCEPTED_SCIENCE88_REGISTRATION',reviewer='/root/f003_resume',author='/root/publication_recovery',installer='/root',baseline_commit='71b1e9c16b579913a133d0003c3e186c353c7765',author_ready=pin(A/'registration_ready.json'),handoff_manifest=pin(A/'registration_handoff_manifest.json'),candidate_manifest=pin(A/'candidate_manifest.json'),scope='Distinct concrete registration review only. Root final gates, full history, publication manifest update, commit and push remain separate.',proposed_counts=dict(recoveries=88,refutations=9,handled=97,pending=8,measured=53,unmeasured=35,editorial=1),source_ids_changed=['L100'],handoff_files=2964,candidate_files=2937,predecessor_objects=37493,old_functions=205,historical_pointers=9,exact_symlinks=2,independent_false_admissions=8,author_preflight_damages=18,independent_optimization_guards=6,native_pages_directly_viewed=list(range(1,9)),accepted_mathematical_review_sha256='ccc618c2e955e035a3c70d0ba6ea33cf8b16029b03780b80a3803c3722a9ab9f',accepted_operational_review_sha256='2553bef7933beecc332b9733e3c6400ac3acdee912abcaccc8a6af3b0dae889c',public_writes=False,mathematical_census_repeated=False,full_history_repeated=False,new_measurements=0,new_question_credit=0,new_Lean_credit=0,independent_new_scientific_credit=0,all_review_sessions_terminal=True,role_disclosure='Reviewer previously supplied source-only native typography assistance for L100 butterfly and oval clauses. No authorship of this registration or its accepted scientific principal assembly. The installed protocol-log timestamp finding and root restoration are disclosed separately.',reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
dump(P/'review.json',review)
(P/'review.rst').write_text('''Distinct science88 registration review
=====================================

Accepted: the concrete installed candidate binds only the already accepted L100
recovery. The baseline is 71b1e9c16b579913a133d0003c3e186c353c7765. Counts become
88 ordinary recoveries, nine principal refutations, 97 handled originals and
eight pending; the 53 measured originals and all measurement data are unchanged.
This is an operational registration decision, not a new mathematical review.
Root alone owns the final gates, full historical snapshot, commit and push.

I read all three installer/current/history scripts, their full verifier and
narrative changes, the guide, registration parameters, native catalogue entries,
and accepted proposal scope. I acquired the distinct scientific principal and
portable operational acceptance without rerunning their group computations.
The exact 22-page Halle preprint remains the source; the 25-page journal edition
is uncollated. The 55 source dispositions, 29 geometry classes, eight retained
premises, six ancillary corrections and butterfly/oval qualifications remain
visible. The 11 manuscripts total 36 pages; the principal catalogue.tex input is
registered literally. Local primitivity and local two-transitivity are not
conflated. No measurement, new question, Lean or compression claim is added.

The sole fresh private-candidate preflight passed, including its 18 damaged
admissions. My separate script rehashed all 2,964 handoff files and 2,937 actual
installed candidate files, then checked all 37,493 predecessor paths against
Git's actual baseline blob objects rather than trusting the author's inventory.
This includes literal symlink targets and executable modes. Only L100's source
entry changes; every measured entry is literally retained. All 205 old non-main
verifier functions have identical ASTs and source text. The only additions are
the two science88 functions, and main's predecessor/current check replacement
preserves its complete old call sequence.

Eight additional semantic false admissions reject. A separate execution of the
actual historical-view adapter observes all nine restored pointer routes and
two literal symlinks; a changed historical input rejects before that view. The
historical evaluator was explicitly intercepted only to inspect these inputs:
no historical mathematical check was executed or claimed. The real final checker
rejects the ungated candidate. Six real argument/environment optimization probes
reject before filesystem work. All eight exact candidate protocol pages were
directly viewed and are clean and readable.

The initial installed-byte audit found one difference: audit/protocol.log had the
root rebuild timestamp instead of the reviewed trial timestamp. No scientific
file or registration code differed. Root preserved its fresh build log and
restored the exact reviewed log. The initial failed audit, precise difference,
root correction record and successful complete audit are retained. This is an
operational identity correction, not an author scientific or code revision.

I previously supplied only source-typography assistance for L100's butterfly and
oval clauses. That assistance is disclosed and supplies no registration premise.
No public file was written by this reviewer. Root's fresh protocol rebuild and
preflight are separate corroboration; my decision rests on the concrete exact
candidate and independent controls above.
''')
exports=[pin(p,P)for p in sorted(P.rglob('*'))if p.is_file()and p.name!='manifest.json']
dump(P/'manifest.json',dict(status=review['status'],exports=exports))
for row in exports:
 q=pin(P/row['path'],P)
 if q!=row:raise ValueError('export changed')
print(json.dumps(dict(manifest=pin(P/'manifest.json'),exports=len(exports),bindings=len(deps))))
