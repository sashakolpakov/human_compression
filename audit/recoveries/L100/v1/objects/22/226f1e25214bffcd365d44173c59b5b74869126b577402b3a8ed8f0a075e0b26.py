"""Freeze a narrow documentary/endpoint successor; never repeat finite searches."""
import sys
if not __debug__:
    raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import difflib,hashlib,json,shutil
S=Path('/Users/sasha/medusa/research/leemans')
G=S/'geometry/psl3_4';W=G/'source_join_edition02';V=G/'source_join_component_v1';P=G/'source_join_component_v2'
def need(v,s):
    if not v:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
need(not P.exists(),'immutable new packet')
need(pin(V/'manifest.json')['sha256']=='c9fe317d46a97e69fda8b47f803308220a3fd5867d004d6dd4c4129cf30d5702','preserved predecessor')
rows={}
def add(p,r=None):
    p=p.absolute();q=pin(p)
    if r is not None:need(all(q[k]==r[k]for k in ['sha256','bytes']),str(p))
    need(str(p)not in rows or rows[str(p)]==q,'consistent pin');rows[str(p)]=q
for r in read(V/'dependencies.json'):add(Path(r['path']),r)
add(V/'manifest.json')
for r in read(V/'manifest.json')['exports']:add(V/r['path'],r)
for d in ['source_join_frozen01','source_join_transcription02','source_join_edition_controls02']:
    for p in (G/d).rglob('*'):
        if p.is_file()and'__pycache__'not in p.parts:add(p)
need(read(G/'source_join_frozen01/report.json')['status']=='PASS_L100_SOURCE_DIAGRAM_JOIN_COMPONENT','terminal finite predecessor replay')
for p in W.rglob('*'):
    if p.is_file()and'__pycache__'not in p.parts:add(p)
add(Path(__file__).absolute());add(Path(sys.executable));add(Path('/opt/homebrew/bin/pdflatex'));add(Path('/opt/homebrew/bin/gs'))
unchanged=['literal_diagrams.py','construction_join.py','named_residues.py','controls.py','literal_diagrams01/diagrams.json','construction_join03/joins.json','named_residues02/named_residues.json']
for name in unchanged:need((W/name).read_bytes()==(V/name).read_bytes(),'unchanged finite input '+name)
P.mkdir()
for p in W.rglob('*'):
    if p.is_file()and'__pycache__'not in p.parts:
        q=P/p.relative_to(W);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
changed=['source_joins.tex','source_joins.rst','check.py','transcribe_diagrams.py','diagram_inventory02.json','diagram_comparison01.json']
delta=''
for name in changed:
    delta+=''.join(difflib.unified_diff((V/name).read_text().splitlines(True),(P/name).read_text().splitlines(True),fromfile='v1/'+name,tofile='v2/'+name))
for name in ['endpoint_comparison.py','edition_controls.py']:
    delta+=''.join(difflib.unified_diff([],(P/name).read_text().splitlines(True),fromfile='/dev/null',tofile='v2/'+name))
(P/'edition_delta.diff').write_text(delta)
dump(P/'edition_change.json',dict(
    predecessor=pin(V/'manifest.json'),
    predecessor_disposition='PRESERVED; distinct reviewer rejected false documentary missing-bond assertion for diagram 3.5. No v1 mathematical/source-join acceptance is inferred.',
    requested_corrections=['Restore the visible horizontal single bond in preprint diagram 3.5 and withdraw the proposed missing-bond source error.',
                           'Compare both ordered endpoint eccentricities of every printed a/g/b label, in addition to gonality.'],
    unchanged_finite_inputs=[pin(V/n)for n in unchanged],
    acquired_terminal_replay=pin(G/'source_join_frozen01/report.json'),
    replay_scope='Acquire original finite literal residue/construction/named-map computations. Freshly rerun only transcription/comparison, focused endpoint controls, optimization guards and native build.',
    changed_text_files=changed,added_code=['endpoint_comparison.py','edition_controls.py'],
    native_build='native_proof03: two passes, clean log, both final pages directly viewed',
    remaining_proposed_source_corrections=['5.1: panel order at the 210-object node is 1, not printed 2','5.2: same'],
    no_new_target=True,no_whole_source_credit=True))
source=S/'corpus161_access_supplement_v4/primary/L100_Halle_1999_preprint.pdf'
dump(P/'source_crop_provenance.json',dict(source=pin(source),physical_page=9,zero_based_page=8,
    crop_box=[110,480,220,580],coordinate_units='PDF points; original page coordinates',
    crop_pdf=pin(W/'source35_detail02.pdf'),crop_png=pin(W/'source35_detail02.png'),
    method='pypdf retained page content with the stated crop box; Ghostscript rendered the crop box at 500 dpi. No source drawing was edited.',
    raster_command=['/opt/homebrew/bin/gs','-q','-dNOPAUSE','-dBATCH','-dUseCropBox','-sDEVICE=png16m','-r500','-sOutputFile=source35_detail02.png','source35_detail02.pdf'],
    preserved_failed_display=pin(W/'source35_detail01.png'),
    failed_display_scope='An earlier viewport display attempt produced a blank image. Retained as a failed display, not evidence of an absent bond.',
    direct_visual_conclusion='The horizontal base segment connects the two bottom nodes. It is a single bond. The v1 omission is an author transcription error.'))
dump(P/'roles.json',dict(author='publication_recovery',root_role='Distinct reviewer of v1: identified the erroneous missing-bond transcription and requested ordered endpoint comparisons. These are explicit review corrections.',
    unchanged_components='Their original author/reviewer roles remain acquired exactly.',distinct_review='Required for this v2; no acceptance is claimed by the author packet.'))
dump(P/'acquired_roots.json',dict(previous_roots=read(V/'acquired_roots.json'),preserved_v1=pin(V/'manifest.json'),terminal_v1_finite_replay=pin(G/'source_join_frozen01/report.json'),v1_documentary_acceptance=False))
dump(P/'handoff.json',dict(status='AUTHOR_COMPLETE_AWAITING_DISTINCT_REVIEW',command=[str(Path(sys.executable)),str(P/'check.py'),'--out',str(G/'source_join_distinct_fresh02'),'--render'],
    scope='29 preprint diagram joins, acquiring 52 canonical residue maps and 10 construction/truncation maps; correcting the author 3.5 transcription; checking eight ordered numerical triples; only two remaining proposed preprint panel-order corrections.',
    exclusions=['Journal-edition textual identity','Abstract group-name claims','Remaining constructions and general doubling','Whole-source credit','New census/target/Lean/measurement']))
(P/'README.rst').write_text('L100 source joins, corrected edition 2\n====================================\n\n'
 'Read source_joins.tex/pdf (two pages), edition_change.json and edition_delta.diff.\n'
 'The preprint DOES contain the single bottom bond in diagram 3.5. The v1 missing-bond assertion was an author transcription error identified by the distinct reviewer and is withdrawn. V1 and its finite replay remain immutable.\n\n'
 'The successor checks both ordered endpoints of all eight printed numerical bond triples. Only the panel-order labels in 5.1 and 5.2 remain proposed source corrections, and only for the exact retained preprint.\n\n'
 'Default replay acquires the unchanged terminal v1 residue/construction/named-map calculations and freshly runs the changed transcription/comparison, focused endpoint controls, guards and optional native build. It does not repeat group, coset, graph or construction searches.\n'
 'Run check.py --out NEW_ABSOLUTE --render. The original source, all native diagrams and failed attempts are retained or exactly acquired. The 25-page journal edition remains uncollated.\n')
dump(P/'dependencies.json',sorted(rows.values(),key=lambda r:r['path']))
exports=[]
for p in sorted(P.rglob('*')):
    if p.is_file():q=pin(p);q['path']=str(p.relative_to(P));exports.append(q)
dump(P/'manifest.json',dict(status='AUTHOR_COMPLETE_L100_SOURCE_DIAGRAM_JOINS_V2',exports=exports,dependencies=len(rows)))
print(json.dumps(pin(P/'manifest.json')));print('exports',len(exports),'dependencies',len(rows))
