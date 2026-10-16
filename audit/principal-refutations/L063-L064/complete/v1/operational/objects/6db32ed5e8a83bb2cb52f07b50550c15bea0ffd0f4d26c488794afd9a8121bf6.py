from pathlib import Path
import json,hashlib,shutil
S=Path('/Users/sasha/medusa/research/leemans'); P=S/'geometry/psl2_rank_two'; W=P/'s4_automorphisms_work'; A=P/'s4_automorphisms'
if A.exists(): raise ValueError('already exists')
def pin(p):
 b=p.read_bytes(); return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(p,d): p.write_text(json.dumps(d,indent=2)+'\n')
A.mkdir(); shutil.copytree(W/'native01',A/'native'); shutil.copyfile(W/'s4_pairs.tex',A/'s4_pairs.tex'); shutil.copyfile(W/'native01/s4_pairs.pdf',A/'s4_pairs.pdf')
code=(P/'scalar_orbits/check.py').read_text().replace('orbits.tex','s4_pairs.tex').replace('orbits.pdf','s4_pairs.pdf').replace('!= 5','!= 4').replace('native_pages=5','native_pages=4').replace('source_claim_groups=6','source_claim_groups=3').replace('PASS_SCALAR_ORBITS_EXACT_NATIVE_REPLAY','PASS_S4_AUTOMORPHISMS_EXACT_NATIVE_REPLAY')
(A/'check.py').write_text(code)
(A/'source').mkdir()
for i in [3,22]:
 for ext in ['pdf','png']:
  shutil.copyfile(P/f'arc_actions_independent_review/source/page-{i:02d}.{ext}',A/f'source/L063-{i:02d}.{ext}')
for ext in ['pdf','png']:
 name=f'L063-04.pdf' if ext=='pdf' else 'L063-p04.png'
 shutil.copyfile(P/'scalar_orbits/source'/name,A/f'source/L063-04.{ext}')
shutil.copyfile(P/'full_automorphisms/classical_premises.json',A/'classical_premises.json')
write(A/'scope.json',{'source':'L063','claims':[{'claim':'Table 3 rows 7--8 conjugacy and automorphism counts','disposition':'RECOVERED_UNDER_SOURCE_UNORDERED_CONVENTION','source_physical_pages':[3,4]},{'claim':'Full graph groups on physical page22 (printed386)','recovered_primes':[23,41,71,73,89],'corrected_primes':[17,31,47,79],'replacement_for_corrected':'PSL(2,p) x C2','source_printed_all_nine':'PGL(2,p)'},{'claim':'Exact local and full arc-transitivity length four','premise_gate':str(P/'arc_actions_root_adoption/manifest.json'),'proof':str(P/'arc_actions/arcs.tex'),'source_rows':['Table3 Gamma7','Table3 Gamma8']}],'hypotheses':'p prime >=7; p = +/-1 modulo8; actual S4,S4 parabolics meeting in D8','q9_separate':True,'classical_premises':['PSL2(p) simplicity and Aut=PGL2(p)','two maximal S4 classes fused by outer automorphisms','cyclic torus centralizers and dihedral normalizers','Tutte cubic arc-transitive vertex stabilizer bound48'],'contributions':{'root':'Tutte/core/centralizer upper-bound route','j3_recovery':'normalizer parity, overgroups, explicit type maps and combined manuscript'},'requires_distinct_third_agent_review':True,'new_group_searches':0,'whole_source_credit':0,'additional_principal_refutation_credit':0,'lean_credit':0,'compression_measurement':None})
write(A/'native_review.json',{'pages':4,'directly_viewed':[1,2,3,4],'dpi':105,'overfull_boxes':False,'status':'AUTHOR_VISUAL_REVIEW_ONLY'})
(A/'development.rst').write_text('The first complete four-page draft is preserved in s4_automorphisms_work/native01. No mathematical revision or finite group search was needed before this freeze. The author viewed all four native pages. The root contributed the upper-bound route and cannot supply the required distinct review alone. The exact source images remain documentary premises for eventual public transport.\n')
deps={}
def add(p,expected=None):
 p=Path(p).resolve(); r=pin(p)
 if expected and r!={k:expected[k] for k in ('bytes','sha256')}: raise ValueError(str(p))
 if str(p) in deps:return
 deps[str(p)]={'path':str(p),**r}
 if p.name=='manifest.json':
  o=json.loads(p.read_text())
  for x in o.get('exports',[]):add(p.parent/x['path'],x)
 elif p.name=='dependencies.json':
  o=json.loads(p.read_text())
  if isinstance(o,list):
   for x in o:
    if 'path'in x and Path(x['path']).is_absolute():add(x['path'],x)
for p in [P/'arc_actions_root_adoption/manifest.json',P/'full_automorphisms/manifest.json',S/'sources/catalogue_L063.pdf',S/'sources/catalogue_L063.txt',P/'scalar_orbits/check.py']:add(p)
for line in (W/'native01/s4_pairs.fls').read_text().splitlines():
 if line.startswith('INPUT '):
  p=Path(line[6:]); p=p if p.is_absolute() else W/'native01'/p
  if p.exists() and not p.is_relative_to(W):add(p)
add(Path('/private/tmp/freeze_s4_oct16.py'))
write(A/'dependencies.json',list(deps.values()))
write(A/'manifest.json',{'status':'L063_S4_FULL_AUTOMORPHISMS_AWAITING_DISTINCT_REVIEW','exports':[{'path':str(p.relative_to(A)),**pin(p)} for p in sorted(A.rglob('*')) if p.is_file()]})
print(pin(A/'manifest.json')); print('dependencies',len(deps))
