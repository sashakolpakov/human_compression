#!/usr/bin/env python3
"""Historical author assembler; the frozen check.py is the replay interface."""
import sys
if sys.flags.optimize:raise RuntimeError('optimized execution is not accepted')
from pathlib import Path
import hashlib,json,shutil
S=Path('/Users/sasha/medusa/research/leemans')
GAP=Path('/opt/homebrew/Cellar/gap/4.15.1')
R=Path('/Users/sasha/medusa/math_compression')
W=S/'reboot_20261013/L045_work/classical_work'
OUT=S/'corpus106_L045_symplectic_upper_v1'
def need(x,m):
    if not x:raise ValueError(m)
def pin(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
root_names=['classical_lower_v1','classical_lower_independent_review','classical_lower_root_adoption','finite_lie_v1','finite_lie_independent_review','finite_lie_root_adoption','linear_unitary_v1','linear_unitary_independent_review','linear_unitary_root_adoption']
for n in root_names:need((S/('corpus106_L045_'+n)/'manifest.json').exists(),'required acquired proof/review absent '+n)
need(not OUT.exists(),'immutable target exists')
stage=W/'symplectic_stage01';need(not stage.exists(),'stage exists');stage.mkdir()
copies={
 'symplectic_upper.tex':'symplectic_upper.tex','symplectic_upper.pdf':'symplectic_upper.pdf','symplectic_upper.log':'symplectic_upper.log',
 'symplectic_bounds.py':'symplectic_bounds.py','symplectic_bounds04.json':'arithmetic_expected.json',
 'symplectic_controls.g':'symplectic_controls.g','symplectic_controls01.stdout':'literal_expected.stdout','symplectic_controls01.stderr':'literal_expected.stderr',
 'symplectic_controls01.json':'history/original_literal_receipt.json','symplectic_native_text.txt':'native_text.txt','check_symplectic.py':'check.py',
 'symplectic_upper_before_unitary_cover.tex':'history/before_unitary_cover.tex','symplectic_bounds_before_unitary_cover.py':'history/before_unitary_cover.py','symplectic_bounds01_before_unitary_cover.json':'history/before_unitary_cover_report.json',
 'symplectic_upper_low_cover_pending.tex':'history/low_cover_pending.tex',
 'symplectic_final_bsw1.stdout':'history/native1.stdout','symplectic_final_bsw1.stderr':'history/native1.stderr','symplectic_final_bsw2.stdout':'history/native2.stdout','symplectic_final_bsw2.stderr':'history/native2.stderr',
 'bubboloni_spiga_weigel_2022.provenance.json':'source_acquisition.json'}
for src,dst in copies.items():
    p=stage/dst;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/src,p)
shutil.copy2(S/'corpus106_L045_classical_lower_v1/lower_bounds.py',stage/'lower_bounds.py')
for i in range(1,5):shutil.copy2(W/f'symplectic_upper-final-{i:02d}.png',stage/f'native-{i:02d}.png')
deps={};queue=[];visited=set()
def add(p,expected=None):
    p=p.resolve()
    for ns,base in [('study',S),('gap',GAP),('public',R)]:
        if p.is_relative_to(base):rel=p.relative_to(base).as_posix();break
    else:raise ValueError('unknown namespace '+str(p))
    q=pin(p)
    if expected is not None:need(q=={k:expected[k] for k in ('bytes','sha256')},'changed acquired bytes '+str(p))
    deps[(ns,rel)]={'namespace':ns,'path':rel,**q}
    if p.name=='manifest.json' and p not in visited:queue.append(p)
def dep_path(item):
    p=Path(item['path'])
    return p if p.is_absolute() else {'study':S,'gap':GAP,'public':R,'repo':R}[item.get('namespace','study')]/p
for n in root_names:add(S/('corpus106_L045_'+n)/'manifest.json')
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
for f in [S/'sources/catalogue_L045.pdf',W/'bubboloni_spiga_weigel_2022.pdf',W.parent/'orthogonal_work/bubboloni_lucido_weigel_2011.pdf',W.parent/'aschbacher_seitz_1976.pdf',W.parent/'aschbacher_seitz_corrections_1978.pdf',W.parent/'burness_thomas_2017.pdf',W/'prepare_symplectic_packet.py']:
    add(f)
save(stage/'dependencies.json',{'files':sorted(deps.values(),key=lambda x:(x['namespace'],x['path']))})
save(stage/'acquired_packets.json',[{'path':'corpus106_L045_'+n+'/manifest.json',**pin(S/('corpus106_L045_'+n)/'manifest.json')} for n in root_names])
save(stage/'scope.json',{'status':'AUTHOR_FROZEN_AWAITING_DISTINCT_REVIEW','proved':'The positive generating-pair branch for every simple PSp_(2m)(q), m>=2, relative to the complete named BSW2022 Lemma5.1 maximal-overgroup classification and exact standard automorphism/form inputs. Accepted finite35 covers eight exceptional simple parameters; Sp4(2) is nonsimple and excluded.','excluded':['No orthogonal assertion','No complete L045 admission','No maximal-subgroup classification proof','No new census','No new question, priority, measurement or Lean credit'],'whole_original_credit':0})
save(stage/'retained_inputs.json',{
 'cover':{'source':'Bubboloni-Spiga-Weigel arXiv2208.08756v1 Lemma5.1, physical40','range':'Natural dimension n=2m>=4 except(n,q)=(4,2)','types':['Sp_(2m/r)(q^r).r for prime r|m','GU_m(q).2 for odd m and q','O^-_(2m)(q) for even q','(m,q)=(4,2): PSL2(17), acquired finite35','(m,q)=(2,3): 2_-^(1+4).A5, acquired finite35'],'statement_acquired_and_read':True,'prior_MSW1994_full_proof_acquired':False,'classification_reproved':False,'multiplicities':'The present proof derives fixed-element uniqueness using irreducible Singer powers and exact quadratic-form differences.'},
 'source_correction':'The target LL Table4 omits the odd m,q unitary overgroup. It is explicitly included here; no reliance on the incomplete printed Sp cover.',
 'outer_fixed_groups':'AS1976 Section19 (19.3)-(19.5), physical76-78, complete passages read/native viewed; full1978 erratum read. Exceptional Sp4(q) graph-field fixed group Sz(q) only for odd field exponent.',
 'suzuki_involutions':'BT2017 Proposition2.3/Table5, one class with centralizer q^2; exact group order gives (q-1)(q^2+1).',
 'numerical_upper':'LLS2002 Proposition1.3 acquired through complete linear packet dependencies.',
 'acquired_new_proofs':'Complete lower, finite35 and linear J_n calculation author/distinct review chains retained.',
 'software':'GAP4.15.1, standard Python exact integer/rational arithmetic, pdfLaTeX; finite controls support the full written uniform argument, not a classification census.'})
save(stage/'source_map.json',{'original':'L045','fixed_source_sha256':pin(S/'sources/catalogue_L045.pdf')['sha256'],'routes':[{'source':'Theorem1.1 positive symplectic branch, Section4','recovery':'Complete symplectic_upper.tex plus accepted finite35'},{'source':'Table3 torus/projective reverser assertions','recovery':'Direct trace model, all ordinary field cosets excluded, exact exceptional Sp4 graph-field bound'},{'source':'Table4 missing GU_m(q).2','recovery':'Corrected complete BSW2022 Lemma5.1 retained explicitly; unique fixed-element multiplicities proved'},{'source':'Table5 unexpanded inequalities','recovery':'Exact normalizer fibres, all-rank inequalities and explicit finite remainders'}],'whole_source':False})
save(stage/'attribution.json',{'target_authors':'Dimitri Leemans and Martin W. Liebeck','new_mathematics_author':'publication_recovery','root_contributions':['Torus-torsor organization over outer cosets','Found the missing unitary overgroup through acquired BLW2011 Lemma3.1','Initial finite35 candidates and word criterion, retained with exact earlier roles'],'author_additions':['Direct symplectic torus and outer exclusion','Exact degree-four normalizer fibres and characteristic-two centralizer','Full uniform inequalities including missing unitary overgroup','Acquired all-rank BSW2022 Lemma5.1 and proved fixed-element multiplicities'],'classification':'Named borrowed result; no independent reconstruction of MSW1994 classification proof.'})
save(stage/'development.json',{'preserved_drafts':['history/before_unitary_cover.tex','history/low_cover_pending.tex'],'first_draft_status':'Unfrozen Sp draft used incomplete LL Table4 before root supplied BLW. Not accepted or credited.','correction':'GU term added and all arithmetic rerun; BSW all-rank primary statement later paid low-rank interface before freeze.','controls':'Original literal controls unchanged; arithmetic expectation includes the actual corrected cover and Singer-power tests. No historical finite search repeated.'})
save(stage/'visual_record.json',{'directly_viewed':['All four final manuscript pages','Fixed L045 source physical7-9','BSW2022 physical40','AS1976 physical76-78','BT2017 physical8/10','LLS2002 physical9-12'],'builds':2,'warnings':False,'overfull':False,'source_originals':'Hash-bound full local PDFs; source excerpt derivatives remain private work.'})
(stage/'README.rst').write_text('''Symplectic generating pairs: complete bounded branch
====================================================

Read all four pages of symplectic_upper.tex/PDF, retained_inputs.json and the
acquired proofs. The actual GU overgroup missing from LL Table4 is charged.
BSW2022 Lemma5.1 supplies the complete classification including small ranks;
the two additional exceptions are accepted finite35 inputs. The original
MSW1994 proof was not obtained. Fixed-element multiplicities, normalizer
inclusion, reverser types and every unbounded inequality are written here.

Fresh replay, with unused absolute output:

  /Users/sasha/.venvs/global/bin/python check.py --study /Users/sasha/medusa/research/leemans --out /ABS/NEW --render

The replay checks the complete acquired byte closure,732 arithmetic cases,
literal even Sp4 centralizers and odd GL2/GU2 normalizer fibres,six trace models,
all Singer-power degree controls,damaged records,optimization guards and the
four-page native rebuild. It does not rerun any large or historical census.
Samples are controls; the manuscript proves uniform coverage. No whole L045,
orthogonal,measurement,new-question or Lean credit is claimed.

Historical incomplete draft/code/report are explicitly retained and uncredited.
check.py is the immutable replay entry point; the private assembler is provenance.
''')
exports=[{'path':p.relative_to(stage).as_posix(),**pin(p)} for p in sorted(stage.rglob('*')) if p.is_file()]
save(stage/'manifest.json',{'schema':1,'packet':'corpus106_L045_symplectic_upper_v1','status':'AUTHOR_FROZEN_AWAITING_DISTINCT_REVIEW','exports':exports})
shutil.copytree(stage,OUT)
print(json.dumps({'packet':str(OUT),'manifest':pin(OUT/'manifest.json'),'exports':len(exports),'bindings':len(deps),'acquired_manifests':len(visited)}))
