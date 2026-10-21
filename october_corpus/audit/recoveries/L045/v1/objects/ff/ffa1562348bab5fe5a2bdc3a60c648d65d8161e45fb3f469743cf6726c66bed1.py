#!/usr/bin/env python3
"""Historical author assembler, not a portable replay entry point."""
import sys
if sys.flags.optimize:raise RuntimeError('optimized execution is not accepted')
from pathlib import Path
import hashlib,json,shutil

S=Path('/Users/sasha/medusa/research/leemans')
GAP=Path('/opt/homebrew/Cellar/gap/4.15.1')
R=Path('/Users/sasha/medusa/math_compression')
W=S/'reboot_20261013/L045_work/classical_work'
OUT=S/'corpus106_L045_linear_unitary_v1'

def need(x,m):
    if not x:raise ValueError(m)
def pin(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')

need(not OUT.exists(),'immutable target already exists')
stage=W/'linear_stage02';need(not stage.exists(),'stage already exists');stage.mkdir()
copies={
 'linear_upper.tex':'linear_upper.tex','linear_upper.pdf':'linear_upper.pdf','linear_upper.log':'linear_upper.log',
 'linear_bounds.py':'linear_bounds.py','linear_bounds01.json':'arithmetic_expected.json',
 'linear_upper_controls.g':'linear_upper_controls.g','linear_upper_controls02.stdout':'literal_expected.stdout',
 'linear_upper_controls02.stderr':'literal_expected.stderr','linear_native_text.txt':'native_text.txt',
 'check_linear.py':'check.py','linear_upper_controls_failed_dictionary.g':'history/failed_dictionary.g',
 'linear_upper_controls01.stdout':'history/failed_dictionary.stdout','linear_upper_controls01.stderr':'history/failed_dictionary.stderr',
 'linear_final_after_bib1.stdout':'history/native1.stdout','linear_final_after_bib1.stderr':'history/native1.stderr',
 'linear_final_after_bib2.stdout':'history/native2.stdout','linear_final_after_bib2.stderr':'history/native2.stderr',
 'primary_attempts04.json':'history/primary_attempts04.json','primary_attempts05.json':'history/primary_attempts05.json'}
for source,target in copies.items():
    p=stage/target;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/source,p)
shutil.copy2(S/'corpus106_L045_classical_lower_v1/lower_bounds.py',stage/'lower_bounds.py')
for i in range(1,5):shutil.copy2(W/f'linear_upper-final-{i:02d}.png',stage/f'native-{i:02d}.png')
root_names=['classical_lower_v1','classical_lower_independent_review','classical_lower_root_adoption','finite_lie_v1','finite_lie_independent_review','finite_lie_root_adoption']
deps={};queue=[];visited=set()
def add(p,expected=None):
    p=p.resolve()
    if p.is_relative_to(S):ns='study';rel=p.relative_to(S).as_posix()
    elif p.is_relative_to(GAP):ns='gap';rel=p.relative_to(GAP).as_posix()
    elif p.is_relative_to(R):ns='public';rel=p.relative_to(R).as_posix()
    else:raise ValueError('unknown dependency namespace '+str(p))
    q=pin(p)
    if expected is not None:need(q=={k:expected[k] for k in ('bytes','sha256')},'changed acquired input '+str(p))
    deps[(ns,rel)]={'namespace':ns,'path':rel,**q}
    if p.name=='manifest.json' and p not in visited:queue.append(p)
def dep_path(item):
    p=Path(item['path'])
    if p.is_absolute():return p
    return {'study':S,'gap':GAP,'public':R,'repo':R}[item.get('namespace','study')]/p
for name in root_names:add(S/('corpus106_L045_'+name)/'manifest.json')
while queue:
    p=queue.pop()
    if p in visited:continue
    visited.add(p);m=json.loads(p.read_text())
    for item in m.get('exports',[]):add(p.parent/item['path'],item)
    for name in ('dependencies.json','bindings.json'):
        f=p.parent/name
        if f.exists():
            d=json.loads(f.read_text());rows=d.get('files',[]) if isinstance(d,dict) else d
            for item in rows:add(dep_path(item),item)
for f in [S/'sources/catalogue_L045.pdf',W.parent/'lawther_liebeck_seitz_2002.pdf',W/'bamberg_errata.html',W/'prepare_linear_packet.py']:
    add(f)
save(stage/'dependencies.json',{'files':sorted(deps.values(),key=lambda x:(x['namespace'],x['path']))})
save(stage/'acquired_packets.json',[{'path':'corpus106_L045_'+n+'/manifest.json',**pin(S/('corpus106_L045_'+n)/'manifest.json')} for n in root_names])
save(stage/'scope.json',{'status':'AUTHOR_FROZEN_AWAITING_DISTINCT_REVIEW','proved':'The positive generating-pair branch for PSL_n(q) and PSU_n(q), n>=4, relative to the explicitly retained linear/unitary maximal-cover classification and standard automorphism/form inputs. Acquired finite35 handles the stated finite parameter routes.','excluded':['No new symplectic assertion','No orthogonal assertion','No whole L045 admission','No maximal-subgroup classification proof','No new numerical census','No measurement, Lean, priority or new-question credit'],'whole_original_credit':0})
save(stage/'retained_inputs.json',{
 'maximal_cover':{'statement':'Exactly the PSL_n and PSU_n rows of fixed source Table4, with stated finite exceptions and multiplicities. The normalizer is included explicitly in the manuscript.','source':'sources/catalogue_L045.pdf, physical pages7-9','provenance':['Bereczky2000 as cited by LL','Bamberg-Penttila2008 as cited by LL','Acquired Bamberg author erratum adds odd-prime extension-field subgroups in odd unitary dimension'],'full_original_classification_proofs_acquired':False,'independent_classification_verification':False,'not_used':'The symplectic Table4 row has a separately identified omitted GU term; this packet makes no symplectic covering claim.'},
 'upper_bound':{'source':'LLS2002 Proposition1.3, complete statement/proof physical10-12 read; physical9-12 directly viewed','inequality':'i2(Aut S)<2(q^(N+r)+q^(N+r-1)) for the simple classical groups used'},
 'structural':['Standard full automorphism description of PSL/PSU','Finite-field trace, Hilbert90 and descent','Ordinary classical-group orders and faithful projective matrix actions'],
 'acquired_proofs':'All six complete author/review/adoption packets named in acquired_packets.json, with recursively closed exact dependencies.',
 'software':'GAP4.15.1 arithmetic and concrete finite field/isometry controls, Python rational/integer controls, pdfLaTeX native build. The written argument proves the unbounded parameter range; finite samples do not replace it.'})
save(stage/'source_map.json',{'original':'L045','source_sha256':pin(S/'sources/catalogue_L045.pdf')['sha256'],'routes':[{'source':'Theorem1.1, positive linear/unitary branch, Section4','recovery':'linear_upper.tex Lemmas1-3 and Proposition4 plus accepted finite35'},{'source':'Tables3-5 implicit reverser/count arithmetic','recovery':'Actual projective centralizer and single outer coset, trace/descent fixed groups, explicit all-rank inequalities'},{'source':'Definition M(x) omits the torus normalizer','recovery':'Normalizer charged by actual extension-field or (n-1)+1 stabilizer'},{'source':'The lower half bound for PSU4','recovery':'Not used; acquired corrected class lower bounds'}],'pending_other_families':['symplectic','orthogonal'],'not_whole_source':True})
save(stage/'attribution.json',{'target_authors':'Dimitri Leemans and Martin W. Liebeck','new_proof_author':'publication_recovery','root_contribution':'Suggested organizing reversers as torus torsors over outer cosets; approved retaining exact published linear/unitary cover with honest classification-provenance limits. No distinct review of this new manuscript claimed yet.','acquired_contributions':'Finite35 candidates and twelve-word criterion from root; finite35 certificate and classical lower proofs by publication_recovery, independently reviewed by l044_resume and root-adopted. Their original attribution files remain acquired.','classification':'No claim to reprove or independently reread the unavailable original classification proofs.'})
save(stage/'development.json',{'first_literal_run':'Failed at GAP dictionary API despite process exit zero; failed source/stdout/stderr preserved. Not mathematical evidence.','accepted_literal_run':'linear_upper_controls02, corrected parameter uniqueness via literal string Set, all exact formulas pass.','source_acquisition':'Full Bereczky and Bamberg-Penttila PDFs unavailable after bounded attempts; do not elevate secondary statements or metadata. The exact published LL rows and acquired author erratum are explicit retained inputs.','packet_split':'Symplectic proof separated before freezing after BLW identified a missing unitary cover term; this frozen packet is linear/unitary only.','finite_controls_not_uniform_proof':True})
save(stage/'visual_record.json',{'directly_viewed':['All four final manuscript pages after full bibliography','Fixed L045 source physical7,8,9','LLS2002 physical9,10,11,12'],'builds':2,'overfull':False,'warnings':False,'source_derivatives':'Source native excerpts and rasters remain private work; full original PDF hashes are dependency-bound.'})
(stage/'README.rst').write_text('''Linear/unitary generating pairs: complete bounded component
=========================================================

Read linear_upper.tex/PDF and retained_inputs.json in full. This derives the
positive PSL/PSU branch for n>=4 from the exact named maximal-cover premise,
with uniform arithmetic, actual projective reversers, and complete acquired
finite exceptions. The original Bereczky/Bamberg-Penttila proofs were not
obtained; this boundary is explicit. No Sp/O or whole-original claim.

Fresh replay (absolute unused output):

  /Users/sasha/.venvs/global/bin/python check.py --study /Users/sasha/medusa/research/leemans --out /ABS/NEW --render

This checks all exact dependency bytes, 2150 arithmetic cases and sixteen
finite routes, seven trace models/813 trace forms, three complete isometry
parameter controls, damaged records, optimization guards and four native
pages. It does not repeat the already reviewed finite35 search. Those complete
proofs, deterministic positive certificates and distinct reviews are acquired.
All unbounded inequalities are proved in the manuscript; samples are controls.

Historical assembler and failed dictionary control are provenance only.
The sole immutable replay entry point is check.py with its local supplied files.
''')
exports=[{'path':p.relative_to(stage).as_posix(),**pin(p)} for p in sorted(stage.rglob('*')) if p.is_file()]
save(stage/'manifest.json',{'schema':1,'packet':'corpus106_L045_linear_unitary_v1','status':'AUTHOR_FROZEN_AWAITING_DISTINCT_REVIEW','exports':exports})
shutil.copytree(stage,OUT)
print(json.dumps({'packet':str(OUT),'manifest':pin(OUT/'manifest.json'),'exports':len(exports),'bindings':len(deps),'acquired_manifests':len(visited)}))
