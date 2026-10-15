import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import hashlib,json,shutil
W=Path(__file__).resolve().parent;S=W.parents[1];D=S/'corpus106_L100_rank_two_independent_review'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def load(p):return json.loads(p.read_text())
def pin(p,base=None):
 b=p.read_bytes();return {'path':str(p.relative_to(base))if base else str(p.resolve()),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
need(not D.exists(),'new immutable review')
need(load(W/'final02/report.json')['status']=='PASS_FINAL_L100_RANK_TWO_V2_REVIEW_CHECK','final exact-edition pass')
need(load(W/'literal02.json')['status']=='PASS_INDEPENDENT_LITERAL_L100_CANDIDATE_CHECKS','literal independent pass')
text=(W/'working_review.rst').read_text()
start=text.index('Root authored the manuscript')
text=text[start:]
text=text.replace('is a typesetting issue separate from the classwise2T correction; v2 is awaited.','is a typesetting issue separate from the classwise2T correction; both issues\nare resolved by the exact v2 edition reviewed below.')
text=text.replace('The intended eventual scope is seven rank-two classes,','The accepted corrected-v2 scope is seven rank-two classes,')
intro='''Distinct review of the L100 rank-two component
=============================================

Decision: ACCEPTED_L100_RANK_TWO_COMPONENT_V2.
Exact author: corpus106_L100_rank_two_v2/manifest.json,
SHA ff40f6de14f2676f867c8fccf4f8a2065a3741bd900cb4960bb9bfa33bb19971.
The v1 blanket local2T assertion was rejected; acceptance is for its corrected
successor. The complete original remains pending. No public file was written.

'''
end='''
Exact final edition and disposition
-----------------------------------

I read the complete v2 manuscript, classwise source rows, scope and literal
manuscript diff. The only mathematical prose correction is the reported
local2T output: class2.2 has flags false,true, all six other classes true,true.
The statement of the all-pairs incidence lemma is equivalently shortened to
avoid the overfull line. The source table now marks precisely the six local2T
classes, and the degree15/stabilizer24 divisibility explanation is explicit.
All algorithm, result, candidate, incidence and witness bytes are unchanged.
The entire v1 author packet and all36 dependencies rehash unchanged.

Final session77721 passes all50 v2 direct bindings and the preserved v1 pins.
It rehashes and acquires the already completed ordinary oracle and all seven
specific damaged-data controls, the two optimization guards and the literal
Python check; it does not repeat those scientific operations. It compares
every v2 source flag against the literal actual H-orbit result. The fresh
two-pass v2 native build is free of warnings and overfull/underfull boxes,
has exact text identity with the author PDF, and both final pages were
directly viewed. Working and final statuses remain distinct in the record.

Accept the corrected rank-two component under its explicit retained complete
subgroup interfaces. This acceptance is not whole L100 recovery, an assertion
about current source questions, a measurement, formalization, priority claim,
root adoption or publication. All reviewer processes are terminal at freeze.
The runnable check_review.py rechecks the exact evidence closure without
rerunning a subgroup census; final_check.py and review_checks.py retain their
original historical working-path assumptions and are execution provenance.
'''
(W/'review.rst').write_text(intro+text+end)
dump(W/'review.json',{'status':'ACCEPTED_L100_RANK_TWO_COMPONENT_V2','reviewer':'/root/publication_recovery','author':'/root','author_manifest':pin(S/'corpus106_L100_rank_two_v2/manifest.json'),'scope':'seven rank-two classes, orders, type sizes, local degrees and exact classwise local2T flags; no whole original','correction_contribution':'Reviewer literal calculation detected false all-local2T prose, supplied exact flags and degree15/stabilizer24 obstruction; author issued immutable v2. No enumeration code or candidate contribution.','proof_complete_read':True,'source_native_pages_directly_viewed':[1,2,3,4,6,7,8],'native_final_pages_directly_viewed':[1,2],'retained_inputs':'complete ambient/local/recursive maximal-subgroup and actual-intermediate-subgroup interfaces;770-file installation inventory is provenance, not a complete runtime trace','independent':load(W/'literal02.json'),'final':load(W/'final02/report.json'),'failures_preserved':['author oracle01 ordered-transversal comparison','reviewer literal01 blanket all2T failure','reviewer fresh01 v1 native overflow'],'whole_original_credit':0,'new_question_credit':0,'new_measurements':0,'new_Lean':0,'public_writes':False,'owned_live_handles':[]})
deps={}
def add(p):
 p=Path(p);r=pin(p);old=deps.get(r['path']);need(old in [None,r],'one exact current path');deps[r['path']]=r
for name in ['corpus106_L100_rank_two_v1','corpus106_L100_rank_two_v2','corpus106_L091_rank_two_root_adoption','corpus106_L091_rank_two_independent_review']:
 q=S/name;add(q/'manifest.json')
 for r in load(q/'manifest.json')['exports']:add(q/r['path'])
 for r in load(q/'dependencies.json'):
  p=Path(r['path']);p=p if p.is_absolute()else S/p
  add(p);need(all(deps[str(p.resolve())][k]==r[k]for k in ['bytes','sha256']),'acquired exact dependency')
for r in load(S/'reboot_20261013/L091_work/retained_library_inputs.json')['files']:add(r['path'])
for q in [Path(sys.executable).resolve(),Path('/opt/homebrew/bin/gap').resolve(),Path('/opt/homebrew/bin/pdflatex').resolve(),Path('/opt/homebrew/bin/gs').resolve()]:add(q)
import pypdf
for q in Path(pypdf.__file__).parent.rglob('*.py'):add(q)
for q in sorted(W.rglob('*')):
 if q.is_file()and '__pycache__'not in q.parts:add(q)
shutil.copytree(W,D,ignore=shutil.ignore_patterns('__pycache__'))
dump(D/'dependencies.json',list(deps.values()))
(D/'README.rst').write_text('''L100 corrected rank-two distinct review
======================================

Read review.rst and review.json. The exact corrected author v2 is accepted;
v1's false blanket local2T assertion and both reviewer failure receipts remain
historical evidence. Seven classes, including primitive/non-2T class2.2, are
certified under the declared retained subgroup-completeness inputs.

Normal Python check_review.py --out NEW_ABSOLUTE rechecks all review exports,
exact dependencies and terminal evidence; no census or target is launched.
The independent Python permutation/coset validator and exact literal GAP
export are included. Native final02 contains both directly viewed pages.
Whole-source higher ranks, fusion counts, Aut/Cor and constructions are unpaid.
''')
exports=[pin(q,D)for q in sorted(D.rglob('*'))if q.is_file()]
dump(D/'manifest.json',{'status':'ACCEPTED_L100_RANK_TWO_COMPONENT_V2','exports':exports,'dependencies':len(deps),'whole_original_credit':0})
print(json.dumps({'manifest':pin(D/'manifest.json'),'exports':len(exports),'dependencies':len(deps)}))
