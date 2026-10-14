"""Freeze the completed independent source/assembly review; no public writes."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Normal Python is required')
import datetime
import hashlib
import json
import shutil
from pathlib import Path

S=Path('/Users/sasha/medusa/research/leemans')
R=Path('/Users/sasha/medusa/math_compression')
W=S/'reboot_20261013/N010_principal_distinct'
A=S/'corpus106_N010_principal_v2'
P=S/'corpus106_N010_principal_independent_review'
if P.exists():
    raise ValueError('Do not overwrite frozen review')


def pin(p):
    p=p.resolve()
    root,ns=(S,'study') if p.is_relative_to(S) else (R,'public')
    if not p.is_relative_to(root):
        raise ValueError('Unknown review input namespace')
    raw=p.read_bytes()
    return dict(namespace=ns,path=str(p.relative_to(root)),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


expected='ba06d64f5d5e08ff25df0e1fdb98e04362c6d7055ad489b14bbe40c625f8c271'
if pin(A/'manifest.json')['sha256']!=expected:
    raise ValueError('Wrong final author edition')
dep={}


def add(row):
    root={'study':S,'public':R}[row['namespace']]
    actual=pin(root/row['path'])
    if actual!=row:
        raise ValueError('Changed binding '+row['path'])
    dep[(row['namespace'],row['path'])]=row


for row in json.loads((A/'dependencies.json').read_text()):
    add(row)
for author in [S/'corpus106_N010_principal_v1',A]:
    add(pin(author/'manifest.json'))
    for row in json.loads((author/'manifest.json').read_text())['exports']:
        actual=pin(author/row['path'])
        if (actual['bytes'],actual['sha256'])!=(row['bytes'],row['sha256']):
            raise ValueError('Changed author export')
        add(actual)
for folder in ['replay01','replay02','source_native01']:
    for p in (W/folder).rglob('*'):
        if p.is_file() and 'cache' not in p.relative_to(W/folder).parts:
            add(pin(p))
for name in ['source_inventory.py','source_inventory01.json','source_inventory02.json',
             'edition_delta.diff','edition_delta.json','review_working.rst','check_review.py','freeze_review.py']:
    add(pin(W/name))

P.mkdir()
for source,target in [('check_review.py','check.py'),('source_inventory.py','source_inventory.py'),
                      ('source_inventory01.json','source_inventory_v1.json'),
                      ('source_inventory02.json','source_inventory.json'),
                      ('edition_delta.diff','edition_delta.diff'),('edition_delta.json','edition_delta.json')]:
    shutil.copyfile(W/source,P/target)
shutil.copyfile(W/'replay01/report.json',P/'fresh_v1_report.json')
shutil.copyfile(W/'replay02/report.json',P/'fresh_report.json')
text=(W/'review_working.rst').read_text().replace(
    'Independent reading of the N010 survey synthesis\n================================================',
    'Independent review of the N010 survey synthesis\n==============================================').replace(
    'Reviewer: /root/publication_recovery. This is a working record, not final\nacceptance before the requested source-contract successor is inspected.\nThe reviewed author of the new synthesis and neighborliness proof is /root.',
    'Status: ACCEPTED_N010_COMPLETE_SURVEY_DISPOSITION. Reviewer:\n/root/publication_recovery. The exact accepted author edition is\ncorpus106_N010_principal_v2, manifest '+expected+'.\nThe author of the new synthesis and neighborliness proof is /root.').replace(
    'Evidence to be finalized\n-----------------------',
    'Final evidence and decision\n---------------------------').replace(
    'Final successor replay/delta and exact immutable review pins remain to add.',
    'The subsequent two failed cat calls assumed nonexistent author edition_delta\nfilenames; no file changed. I independently generated and retained the exact\nv1-to-v2 literal delta instead. These read-only tooling errors are not author\npacket defects or mathematical failures.\n\n'
    'Final v2 replay93912 is terminal PASS:25exports,5777bindings,17damaged\nscope controls and2pre-output optimization guards. Its11nativepages were\nall directly viewed. The22page volume is page-by-page identical to the\nfinal synthesis plus the exact unabridged components. The independent\nsource inventory passes34ordinal/line/label comparisons,66full bibliography\ncomparisons,51legacy anchor/citation joins,14secondary records and10damaged\nsource controls. R52 supplies the52nd clause.\n\n'
    'The complete edition delta was read. All51prior clause records are\nbyte-equivalent as JSON data; dependencies.json, acquired_packets.json,\nacquired_manuscripts.json, question_table.tex and secondary_table.tex are\nbyte-identical. New mathematical assertions in the common components\nand neighborliness proof are unchanged. The only scientific addition is\nthe explicitly attributed, uninspected-primary R52 statement, routed in\nC07 and stated with its limitation in the prose. All updated counts and\nnew rejection cases agree. V1 and its full replay remain retained.\n\n'
    'I accept the entire final synthesis/source contract at its exact declared\nsurvey-disposition scope. No mathematical or source-routing correction\nremains requested. This acceptance neither independently establishes every\nretained classification nor reproduces17/441, answers remaining source\nquestions, or admits a public original. All whole-original, question, Lean\nand measurement credits remain zero here; public admission belongs to root.')
(P/'review.rst').write_text(text)
review=dict(status='ACCEPTED_N010_COMPLETE_SURVEY_DISPOSITION',source_id='N010',
    author='/root',distinct_reviewer='/root/publication_recovery',author_manifest=pin(A/'manifest.json'),
    predecessor_manifest=pin(S/'corpus106_N010_principal_v1/manifest.json'),
    complete_source_and_principal_proof_read=True,all_immediate_component_proofs_read=True,
    full_wrapper_and_preparation_code_read=True,source_contexts=16,established_clauses=52,
    legacy_clauses_unchanged=51,numbered_questions=34,secondary_records=14,bibliography_entries=66,
    immediate_synthesis_pages=11,immediate_component_pages=11,reading_volume_pages=22,
    older_acquired_proofs_are_additional=True,final_native_pages_directly_viewed=list(range(1,12)),
    source_pages_directly_viewed=[1,7,10,14,15,19,20],fresh_sessions=[60404,93912],
    fresh_exports=25,fresh_dependencies=5777,author_damaged_controls=17,independent_damaged_controls=10,
    author_optimization_guards=2,source_only_aggregates=[17,441],corrected_family_count=137,
    corrected_global_total=None,retained_classifications_reproved=False,present_open_status_claimed=False,
    new_mathematical_contribution=False,
    review_requested_revision='Append explicit retained rank4-finite/rank5-not-all-finite source assertion as R52; fully resolved in v2 without new classification proof.',
    prior_roles_disclosed=['Earlier distinct review of acquired L052 residue theory',
        'Prior authorship/review roles in acquired L045 and L044 proofs, retained with their separate distinct reviews',
        'No authorship of new N010 synthesis, neighborliness or common components'],
    acquired_censuses_repeated=False,new_Lean_declarations=0,new_measurements=0,new_question_credit=0,
    whole_original_credit=0,public_writes=False,current_live_handles=[],
    updated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(P/'review.json').write_text(json.dumps(review,indent=2)+'\n')
(P/'dependencies.json').write_text(json.dumps(sorted(dep.values(),key=lambda r:(r['namespace'],r['path'])),indent=2)+'\n')
exports=[]
for p in sorted(P.iterdir()):
    raw=p.read_bytes();exports.append(dict(path=p.name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
(P/'manifest.json').write_text(json.dumps(dict(status=review['status'],original='N010',exports=exports),indent=2)+'\n')
print(json.dumps(dict(manifest=pin(P/'manifest.json'),exports=len(exports),dependencies=len(dep))))
