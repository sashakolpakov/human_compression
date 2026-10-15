from pathlib import Path
import json, hashlib, shutil
from datetime import datetime, timezone
S=Path('/Users/sasha/medusa/research/leemans')
W=S/'reboot_20261013/L091_rank_two_distinct'
A=S/'corpus106_L091_rank_two_v1'
P=S/'corpus106_L091_rank_two_independent_review'
STATUS='ACCEPTED_L091_RANK_TWO_COMPONENT_V1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def pin(p):
 p=p.absolute()
 return {'namespace':'study' if p.is_relative_to(S) else 'gap_installation','path':str(p.relative_to(S)) if p.is_relative_to(S) else str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def validate(p,r):
 if p.stat().st_size!=r['bytes'] or sha(p)!=r['sha256']:raise RuntimeError(str(p))
if sha(A/'manifest.json')!='cd5d88b1948e753830dad6e5b19714fdc7531c0b826b27d936901380776b8e12':raise RuntimeError('author changed')
if P.exists():raise RuntimeError('immutable output exists')
P.mkdir()
old=(W/'working_review.rst').read_text()
body=old[old.index('Source and mathematical interfaces'):old.index('Current outcome\n---------------')]
body=body.replace('Root has agreed to record all three domains explicitly and inventory the\ncore GAP/tomlib installation boundary.', 'The final retained_library_inputs.json now explicitly records all three\ndomains and pins the declared core GAP/tomlib installation inventory.')
intro='''Distinct review of the L091 rank-two component
=============================================

Status: ACCEPTED_L091_RANK_TWO_COMPONENT_V1, unchanged final author edition.
Author manifest: corpus106_L091_rank_two_v1/manifest.json,
SHA256 cd5d88b1948e753830dad6e5b19714fdc7531c0b826b27d936901380776b8e12.

Root authored the theorem and programs. This reviewer supplied preliminary
semantic scrutiny and certificate recommendations, including explicit
H<B<G wording and a request for literal automorphism witnesses; the reviewer
did not author the resulting proof or enumeration. The independent reader
performed the complete proof/code/source-interface review and the separate
certificate checks described below. No public files were changed.

'''
end='''Final edition, native output and exact acquisition
-------------------------------------------------

The immutable author manifest, both exported files and all 32 dependencies
were freshly checked. The final proof, native PDF and mathematical inputs
are byte-identical to the fully read working edition. The new retained
library record was read in full and all 770 listed files were rehashed:
512 core library files, 92 selected tomlib data/code files, and 166 installed
package metadata files. The record explicitly acquires complete maximal
subgroup representatives on G, on every one of the twelve local A, and on
every recursive overgroup, together with actual IntermediateSubgroups.
It does not claim that the HS table alone pays these lists. Installation
inventory is not a runtime file trace or a proof of GAP/library correctness.
These retained completeness assumptions remain part of this acceptance.

A fresh two-pass native build completed cleanly, with exact extracted-text
identity to the author PDF. Both final rendered pages were directly viewed.
An initial reviewer helper completed both TeX passes, then attempted the
unavailable /opt/homebrew/bin/pdftotext. Its failed receipt is preserved;
a separate helper continued the existing native build using Ghostscript
text extraction. No mathematical input was changed and no group census was
repeated because of that tool-locator failure.

The preserved working review/report explicitly predate the final author
freeze and still say acceptance pending. They are historical records, not
conflicting final dispositions. final_author01/report.json and this final
review bind the completed exact-edition check. The final author package
itself is a two-export manifest with external exact dependencies; this
review retains that layout and does not pretend it contains copied code.

Conclusion and limits
---------------------

The component proves the fixed source's six total rank-two classes, under
the stated retained subgroup-completeness inputs and Aut(HS) plus type-swap
convention. Its full proof, enumeration coverage, actual common-neighbour
criterion, ten-survivor quotient and literal four identifications pass.
No substantive mathematical or code correction is requested.

This acceptance does not pay the two higher-rank truncation identifications,
the four-nontruncation count, higher ranks, the rank bound, the supplemental
lattice or Hoffman--Singleton constructions. It is not whole L091 recovery,
a new question answer, a measurement, formalization, root adoption, public
registration or any claim of historical priority. No live subprocess is
owned by this reviewer at freeze.
'''
(P/'review.rst').write_text(intro+body+end)
for name in ['working_review.rst','working_report.json','independent.g','run_independent.py','check_final_author.py','finish_native.py','freeze_review.py']:
 shutil.copy2(W/name,P/name)
for name in ['independent01','final_author01']:
 shutil.copytree(W/name,P/name)
paths={}
def add(p,record=None):
 p=p.absolute()
 if record:validate(p,record)
 paths[str(p)]=pin(p)
add(A/'manifest.json')
for r in json.loads((A/'manifest.json').read_text())['exports']:add(A/r['path'],r)
for r in json.loads((A/'dependencies.json').read_text()):add(Path(r['path']),r)
for r in json.loads((S/'reboot_20261013/L091_work/retained_library_inputs.json').read_text())['files']:add(Path(r['path']),r)
for r in json.loads((W/'working_report.json').read_text())['inputs']:
 add(S/r['path'] if r['namespace']=='study' else Path(r['path']),r)
for p in W.rglob('*'):
 if p.is_file():add(p)
for rel in ['topic_D_L096_HS_root_review/review.json','reboot_20261013/L091_rank_two_preliminary_read/review.rst']:
 add(S/rel)
deps=sorted(paths.values(),key=lambda r:(r['namespace'],r['path']))
dump(P/'dependencies.json',deps)
review={
 'status':STATUS,'reviewer':'/root/l044_resume','author':'/root',
 'author_manifest':pin(A/'manifest.json'),
 'accepted_result':'Exactly six total rank-two HS geometries under Aut(HS) and type interchange, with the explicit retained complete subgroup interfaces.',
 'scope':'Rank-two component only; higher-rank, truncation, four-nontruncation and whole-source obligations remain separate.',
 'source':'Fixed older_L091.pdf, all six extracted pages read, physical page 2 directly viewed; Section 2 six-total convention distinguished from Table 1 four nontruncation rows.',
 'roles':'Reviewer preliminary semantic scrutiny/certificate recommendations disclosed; root authorship of proof and enumeration; reviewer independent controls and full distinct audit.',
 'retained_inputs':'Complete MaximalSubgroupClassReps for G, local A and recursive overgroups, and actual IntermediateSubgroups; 770-file installation inventory is not a runtime trace or a correctness proof.',
 'fresh':{'independent_session':61559,'elapsed_seconds':31.8866,'actual_pairs':13,'all_neighbour_pairs':16430,'explicit_bijective_maps':4,'independently_closed_S4_subgroups':30,'incidence_controls':3,'negative_controls':3,'native_pages':2,'native_text_identical':True,'final_author_exports':2,'final_author_dependencies':32,'library_pins':770},
 'full_geometry_census_repeated':False,'operational_failure':'Preserved missing pdftotext helper failure after completed native build; continued exact build with Ghostscript.',
 'dependency_count':len(deps),'whole_original_credit':0,'question_credit':0,'measurement':None,'new_Lean':0,'root_adoption':False,'public_changes':False,
 'time_utc':datetime.now(timezone.utc).isoformat()}
dump(P/'review.json',review)
exports=[{'path':str(p.relative_to(P)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(P.rglob('*')) if p.is_file()]
dump(P/'manifest.json',{'status':STATUS,'exports':exports})
for r in exports:validate(P/r['path'],r)
for r in deps:validate(S/r['path'] if r['namespace']=='study' else Path(r['path']),r)
print(json.dumps({'status':STATUS,'manifest':str(P/'manifest.json'),'sha256':sha(P/'manifest.json'),'exports':len(exports),'dependencies':len(deps)},indent=2))
